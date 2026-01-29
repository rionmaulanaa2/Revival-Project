# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/GameServerConsole.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
import sys
import datetime
import socket
from code import InteractiveConsole
from six_ex.moves.cStringIO import StringIO
import asyncore
from . import TelnetHandler

def log(lg):
    print(lg)


class TelnetServer(asyncore.dispatcher):

    def __init__(self, host, port, accept_handler, whitelist):
        asyncore.dispatcher.__init__(self)
        self.accept_handler = accept_handler
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.host = host
        self.port = port
        self.clientid = 1
        self.whitelist = whitelist
        self.trybind()
        self.listen(50)
        log('GameServerConsole: ServerIp: %s ServerPort: %s waiting for client...' % (self.host, self.port))

    def trybind(self):
        while 1:
            try:
                self.bind((self.host, self.port))
                break
            except:
                self.port += 1
                if self.port > 65535:
                    raise Exception('Server failed to find a usable port to bind!')

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            ip, port = addr
            if str(ip) in self.whitelist or len(self.whitelist) == 0:
                log('GameServerConsole: Incoming connection from %s' % repr(addr))
                if self.accept_handler(self.clientid, sock):
                    self.clientid = self.clientid + 1
        return

    def handle_close(self):
        asyncore.dispatcher.handle_close(self)

    def handle_expt(self):
        asyncore.dispatcher.handle_expt(self)

    def handle_error(self):
        asyncore.dispatcher.handle_error(self)


class TelnetConnection(asyncore.dispatcher):
    DEFAULT_RECV_BUFFER = 4096

    def __init__(self, clientid, sock, encoding, receive_handler, disconnect_handler):
        self.w_buffer = StringIO()
        asyncore.dispatcher.__init__(self, sock)
        self.sock = sock
        self.clientid = clientid
        self.encoding = encoding
        self.receive_handler = receive_handler
        self.disconnect_handler = disconnect_handler
        self.clientname = None
        self.r_buffer = StringIO()
        self.recv_buffer_size = TelnetConnection.DEFAULT_RECV_BUFFER
        self.telnet_handler = TelnetHandler.TelnetHandler(self)
        return

    def handle_read(self):
        data = self.recv(self.recv_buffer_size)
        if data:
            self.telnet_handler.handle_input(data)

    def handle_write(self):
        buff = self.w_buffer.getvalue()
        if buff:
            sent = self.send(buff)
            self.w_buffer = StringIO()
            self.w_buffer.write(buff[sent:])

    def handle_close(self):
        asyncore.dispatcher.handle_close(self)
        self.disconnect_handler(self)

    def send_data(self, data):
        self.w_buffer.write(data)

    def writable(self):
        return self.w_buffer.getvalue()


class TelnetConsole(InteractiveConsole):

    def __init__(self, client, locals=None, filename='<console>'):
        InteractiveConsole.__init__(self, locals, filename)
        self.client = client

    def interact(self, banner=None):
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = '>>> '

        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = '... '

        cprt = 'Type "help", "copyright", "credits" or "license" for more information.'
        if banner is None:
            self.write('Python %s on %s\r\n%s\r\n(%s)\r\n>>> ' % (
             sys.version, sys.platform, cprt,
             self.__class__.__name__))
        else:
            self.write('%s\n' % str(banner))
        return

    def write(self, data):
        data = data.replace('\r\n', '\n').replace('\n', '\r\n')
        self.client.send_data(data)


class GameServerConsole(object):

    def __init__(self, ip='127.0.0.1', port=9113, encoding='utf-8', whitelist=[], gmcmd_handler=None, on_start_script=''):
        super(GameServerConsole, self).__init__()
        self.hostname = ip
        self.encoding = encoding
        self.gmcmd_handler = gmcmd_handler
        self.on_start_script = on_start_script
        self.port = port
        self.clients = {}
        self.clientnames = {}
        self.consoles = {}
        self.whitelist = whitelist
        import re
        self.keywordList = [
         (
          re.compile('^@$'), 'import objgraph as og'),
         (
          re.compile('^!$'), 'from mobile.distserver.game import GameServerRepo;GameServerRepo.game_server.server.get_status()'),
         (
          re.compile('#(\\S+?)\\.'), "from logic.gutils.SingletonManager import SingletonManager;SingletonManager().get_server_singleton('\\1').")]

    def whenconnect(self, clientid, client):
        log('GameServerConsole: a new connection with Id=%s%s' % ('%d Address:' % clientid, client.getpeername()))
        con = TelnetConnection(clientid, client, self.encoding, self.whenreceive, self.whenexit)
        con.send_data('^] -> set crlf :')
        return True

    def whenreceive(self, client, string):
        if client.clientname:
            if string[0] == '$':
                self.rungmcmd(client, string[1:])
            else:
                self.runscript(client, string)
        elif self.clientnames.__contains__(string):
            client.send_data('%s is exited!!!\r\n' % string)
        else:
            client.clientname = string
            client.send_data('Hello, %s!!!\r\n' % client.clientname)
            self.consoles[client] = TelnetConsole(client)
            self.consoles[client].interact()
            self.addclient(client)
            self.runscript(client, self.on_start_script)
        return True

    def whenexit(self, client):
        self.delclient(client)
        return True

    def rungmcmd(self, client, cmd):
        if cmd == 'users':
            client.send_data('User list(%d):\r\n' % len(self.clients))
            for i in self.clients:
                clt = self.clients[i]
                client.send_data(' %d\t%s\r\n' % (clt.clientid, clt.clientname))

        elif cmd.find('say ') == 0:
            string = ' '.join(cmd.split(' ')[1:])
            now = datetime.datetime.now()
            send_data = '\r\n' + '%s %s\r\n  %s' % (now, client.clientname, string)
            self.sendtoall(send_data, client)
        elif self.gmcmd_handler:
            try:
                args = cmd.split()
                if len(args) > 1:
                    self.gmcmd_handler(args[0], *args[1:])
                else:
                    self.gmcmd_handler(args[0], *[])
            except Exception as e:
                client.send_data(str(e.message) + '\r\n')

        client.send_data(sys.ps1)

    def runscript(self, client, script):
        encoding = getattr(sys.stdin, 'encoding', None)
        if encoding and not isinstance(script, six.text_type):
            script = script.decode(encoding)
        buff = StringIO()
        temp = sys.stdout
        sys.stdout = buff
        script = self.keyword_replace(script)
        more = self.consoles[client].push(script)
        sys.stdout = temp
        self.consoles[client].write(buff.getvalue())
        if more:
            client.send_data(sys.ps2)
        else:
            client.send_data(sys.ps1)
        return

    def keyword_replace(self, script):
        for keyword in self.keywordList:
            m = keyword[0].search(script)
            if m:
                script = keyword[0].sub(keyword[1], script)

        return script

    def start(self):
        self.telnetServer = TelnetServer(self.hostname, self.port, self.whenconnect, self.whitelist)

    def stop(self):
        clients = six_ex.values(self.clients)
        self.clients = {}
        self.clientnames = {}
        self.consoles = {}
        for client in clients:
            client.close()

        if self.telnetServer is not None:
            self.telnetServer.close()
        return

    def sendtoall(self, string, notfor):
        for i in self.clients:
            if not (notfor and notfor.clientid == i):
                self.clients[i].send_data(string + '\r\n' + sys.ps1)

    def addclient(self, client):
        log('GameServerConsole: %s logined!!!\r\n' % (client.clientname,))
        self.sendtoall('\r\n%s logined!!!\r\n' % (client.clientname,) + sys.ps1, client)
        self.clients[client.clientid] = client
        self.clientnames[client.clientname] = client.clientid

    def delclient(self, client):
        log('GameServerConsole: %s logouted!!!' % (client.clientname,))
        self.sendtoall('\r\n%s logouted!!!\r\n' % (client.clientname,) + sys.ps1, client)
        if client.clientid in self.clients:
            del self.clients[client.clientid]
        if client.clientname in self.clientnames:
            del self.clientnames[client.clientname]
        if client in self.consoles:
            del self.consoles[client]


if __name__ == '__main__':
    GameServerConsole().start()
    asyncore.loop()