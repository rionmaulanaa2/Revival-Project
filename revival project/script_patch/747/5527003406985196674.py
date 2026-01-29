# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/MonitorConsole.py
from __future__ import absolute_import
from .GameServerConsole import TelnetServer
from .GameServerConsole import TelnetConnection
from .MonitorWatch import access_type_rw, access_type_rb
from . import MonitorManager

class MonitorConsole(object):

    def __init__(self, ip, port, logger, monitormanager, whitelist):
        self.ip = ip
        self.port = port
        self.logger = logger
        self.monitormanager = monitormanager
        self.telnetServer = TelnetServer(ip, port, self.whenconnect, whitelist)

    def whenconnect(self, clientid, client):
        con = TelnetConnection(clientid, client, 'utf-8', self.whenreceive, self.whenexit)
        con.send_data('monitor console command:\r\nmonitor_info\r\nmonitor_set key1 ... keyn value\r\nmonitor_get key1 ... keyn\r\nentering command:\r\n')
        return True

    def process_cmd(self, client, cmd):
        if cmd[0:11] == 'monitor_set':
            cmdlist = cmd.split(' ')
            ret, watch = self.monitormanager.get(cmdlist[1])
            if not ret:
                client.send_data('set monitor value error unregister %s\r\n' % str(cmdlist[1]))
            elif watch.access() == access_type_rb:
                client.send_data('set monitor value is read only %s\r\n' % str(cmdlist[1]))
            else:
                for key in cmdlist[2:len(cmdlist) - 2]:
                    ret, watch = watch.getnode(key)
                    if not ret:
                        client.send_data('set monitor value error unregister %s\r\n' % str(key))
                        return
                    if watch.access() == access_type_rb:
                        client.send_data('set monitor value is read only %s\r\n' % str(key))
                        return

                ret, v = watch.setvalue(cmdlist[len(cmdlist) - 2], cmdlist[len(cmdlist) - 1])
                if ret:
                    client.send_data('set monitor value %s=%s\r\n' % (str(cmdlist[1:len(cmdlist) - 1]), str(v)))
                elif v == None:
                    client.send_data('set monitor value error unregister %s\r\n' % str(cmdlist[len(cmdlist) - 2]))
                elif v == access_type_rb:
                    client.send_data('set monitor value is read only %s\r\n' % str(cmdlist[len(cmdlist) - 2]))
        elif cmd[0:11] == 'monitor_get':
            cmdlist = cmd.split(' ')
            ret, v = self.monitormanager.monitor_get(cmdlist[1:len(cmdlist)])
            if ret:
                client.send_data('get monitor value %s=%s:\r\n' % (str(cmdlist[1:len(cmdlist)]), v))
            else:
                client.send_data('get monitor value error unregister %s\r\n' % str(cmdlist[1:len(cmdlist)]))
        elif cmd[0:12] == 'monitor_info':
            client.send_data('monitor value count=%d:\r\n' % len(self.monitormanager.monitor_info()))
            client.send_data('%s\r\n' % repr(self.monitormanager.monitor_info()))
        return

    def whenreceive(self, client, cmd):
        self.process_cmd(client, cmd)

    def whenexit(self, client):
        self.delclient(client)
        return True


from .proto_python import monitor_server_pb2

class MonitorService(monitor_server_pb2.IMonitorService):

    def __init__(self, logger, monitormanager, whitelist):
        monitor_server_pb2.IMonitorService.__init__(self)
        self.logger = logger
        self.monitormanager = monitormanager
        self.whitelist = whitelist

    def monitor_info(self, controller, _viod, _done):
        rpc_channel = controller.rpc_channel
        stub = monitor_server_pb2.IMonitorService_Stub(rpc_channel)
        reply = monitor_server_pb2.MonitorReply()
        reply.reply = repr(self.monitormanager.monitor_info())
        stub.monitor_info_reply(reply)

    def monitor_set(self, controller, args, _done):
        rpc_channel = controller.rpc_channel
        stub = monitor_server_pb2.IMonitorService_Stub(rpc_channel)
        reply = monitor_server_pb2.MonitorReply()
        ret, watch = self.monitormanager.get(args.key[0])
        if not ret:
            reply.reply = 'set monitor value error unregister %s\r\n' % str(args.key[0])
            stub.monitor_set_reply(reply)
        elif watch.access() == access_type_rb:
            reply.reply = 'set monitor value is read only %s\r\n' % str(args.key[0])
            stub.monitor_set_reply(reply)
            return
        for key in args.key[1:len(args.key) - 1]:
            ret, watch = watch.getnode(key)
            if not ret:
                reply.reply = 'set monitor value error unregister %s\r\n' % str(args.key[0])
                stub.monitor_set_reply(reply)
                return
            if watch.access() == access_type_rb:
                reply.reply = 'set monitor value is read only %s\r\n' % str(args.key[0])
                stub.monitor_set_reply(reply)
                return

        ret, v = watch.setvalue(args.key[len(args.key) - 1], args.value)
        if ret:
            reply.reply = 'set monitor value %s=%s\r\n' % (str(args.key[len(args.key) - 1]), str(args.value))
            stub.monitor_set_reply(reply)
        elif v == None:
            reply.reply = 'set monitor value error unregister %s\r\n' % str(args.key[len(args.key) - 1])
            stub.monitor_set_reply(reply)
        elif v == access_type_rb:
            reply.reply = 'set monitor value is read only %s\r\n' % str(args.key[len(args.key) - 1])
            stub.monitor_set_reply(reply)
        return

    def monitor_get(self, controller, args, _done):
        rpc_channel = controller.rpc_channel
        stub = monitor_server_pb2.IMonitorService_Stub(rpc_channel)
        reply = monitor_server_pb2.MonitorReply()
        ret, v = self.monitormanager.monitor_get(args.key[0:len(args.key)])
        if ret:
            reply.reply = 'get monitor value %s=%s:\r\n' % (str(args.key[0:len(args.key)]), v)
            stub.monitor_get_reply(reply)
        else:
            reply.reply = 'get monitor value error unregister %s\r\n' % str(str(args.key[0:len(args.key)]))
            stub.monitor_get_reply(reply)