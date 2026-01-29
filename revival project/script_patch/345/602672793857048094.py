# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/transport/ws/websocket_server.py
import re
import sys
import struct
from base64 import b64encode
from hashlib import sha1
if sys.version_info[0] < 3:
    from SocketServer import ThreadingMixIn, TCPServer, StreamRequestHandler
else:
    from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler
FIN = 128
OPCODE = 15
MASKED = 128
PAYLOAD_LEN = 127
PAYLOAD_LEN_EXT16 = 126
PAYLOAD_LEN_EXT64 = 127
OPCODE_TEXT = 1
CLOSE_CONN = 8

class API(object):

    def run_forever(self):
        try:
            print 'Listening on port %d for clients..' % self.port
            self.serve_forever()
        except KeyboardInterrupt:
            self.server_close()
            print 'Server terminated.'
        except Exception as e:
            print 'ERROR: WebSocketsServer: ' + str(e)
            exit(1)

    def new_client(self, client, server):
        pass

    def client_left(self, client, server):
        pass

    def message_received(self, client, server, message):
        pass

    def set_fn_new_client(self, fn):
        self.new_client = fn

    def set_fn_client_left(self, fn):
        self.client_left = fn

    def set_fn_message_received(self, fn):
        self.message_received = fn

    def send_message(self, client, msg):
        self._unicast_(client, msg)

    def send_message_to_all(self, msg):
        self._multicast_(msg)


class WebsocketServer(ThreadingMixIn, TCPServer, API):
    allow_reuse_address = True
    daemon_threads = True
    clients = []
    id_counter = 0

    def __init__(self, port, host='127.0.0.1'):
        self.port = port
        TCPServer.__init__(self, (host, port), WebSocketHandler)

    def _message_received_(self, handler, msg):
        self.message_received(self.handler_to_client(handler), self, msg)

    def _new_client_(self, handler):
        self.id_counter += 1
        client = {'id': self.id_counter,
           'handler': handler,
           'address': handler.client_address
           }
        self.clients.append(client)
        self.new_client(client, self)

    def _client_left_(self, handler):
        client = self.handler_to_client(handler)
        self.client_left(client, self)
        if client in self.clients:
            self.clients.remove(client)

    def _unicast_(self, to_client, msg):
        to_client['handler'].send_message(msg)

    def _multicast_(self, msg):
        for client in self.clients:
            self._unicast_(client, msg)

    def handler_to_client(self, handler):
        for client in self.clients:
            if client['handler'] == handler:
                return client


class WebSocketHandler(StreamRequestHandler):

    def __init__(self, socket, addr, server):
        self.server = server
        StreamRequestHandler.__init__(self, socket, addr, server)

    def setup(self):
        StreamRequestHandler.setup(self)
        self.keep_alive = True
        self.handshake_done = False
        self.valid_client = False

    def handle(self):
        while self.keep_alive:
            if not self.handshake_done:
                self.handshake()
            elif self.valid_client:
                self.read_next_message()

    def read_bytes(self, num):
        bytes = self.rfile.read(num)
        if sys.version_info[0] < 3:
            return map(ord, bytes)
        else:
            return bytes

    def read_next_message(self):
        b1, b2 = self.read_bytes(2)
        fin = b1 & FIN
        opcode = b1 & OPCODE
        masked = b2 & MASKED
        payload_length = b2 & PAYLOAD_LEN
        if not b1:
            print 'Client closed connection.'
            self.keep_alive = 0
            return
        if opcode == CLOSE_CONN:
            print 'Client asked to close connection.'
            self.keep_alive = 0
            return
        if not masked:
            print 'Client must always be masked.'
            self.keep_alive = 0
            return
        if payload_length == 126:
            payload_length = struct.unpack('>H', self.rfile.read(2))[0]
        elif payload_length == 127:
            payload_length = struct.unpack('>Q', self.rfile.read(8))[0]
        masks = self.read_bytes(4)
        decoded = bytearray()
        res = self.read_bytes(payload_length)
        for char in res:
            char ^= masks[len(decoded) % 4]
            decoded.append(char)

        decoded = str(decoded, encoding='utf-8')
        self.server._message_received_(self, decoded)

    def send_message(self, message):
        self.send_text(message)

    def send_text(self, message):
        if isinstance(message, bytes):
            message = try_decode_UTF8(message)
            if not message:
                print "Can't send message, message is not valid UTF-8"
                return False
        elif isinstance(message, str):
            pass
        else:
            print "Can't send message, message has to be a string or bytes. Given type is %s" % type(message)
            return False
        header = bytearray()
        payload = encode_to_UTF8(message)
        payload_length = len(payload)
        if payload_length <= 125:
            header.append(FIN | OPCODE_TEXT)
            header.append(payload_length)
        elif payload_length >= 126 and payload_length <= 65535:
            header.append(FIN | OPCODE_TEXT)
            header.append(PAYLOAD_LEN_EXT16)
            header.extend(struct.pack('>H', payload_length))
        elif payload_length < 18446744073709551616L:
            header.append(FIN | OPCODE_TEXT)
            header.append(PAYLOAD_LEN_EXT64)
            header.extend(struct.pack('>Q', payload_length))
        else:
            raise Exception('Message is too big. Consider breaking it into chunks.')
            return
        self.request.send(header + payload)

    def handshake(self):
        message = self.request.recv(1024).decode().strip()
        upgrade = re.search('\nupgrade[\\s]*:[\\s]*websocket', message.lower())
        if not upgrade:
            self.keep_alive = False
            return
        key = re.search('\n[sS]ec-[wW]eb[sS]ocket-[kK]ey[\\s]*:[\\s]*(.*)\r\n', message)
        if key:
            key = key.group(1)
        else:
            print 'Client tried to connect but was missing a key'
            self.keep_alive = False
            return
        response = self.make_handshake_response(key)
        self.handshake_done = self.request.send(response.encode())
        self.valid_client = True
        self.server._new_client_(self)

    def make_handshake_response(self, key):
        return 'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: %s\r\n\r\n' % self.calculate_response_key(key)

    def calculate_response_key(self, key):
        GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        hash = sha1(key.encode() + GUID.encode())
        response_key = b64encode(hash.digest()).strip()
        return response_key.decode('ASCII')

    def finish(self):
        self.server._client_left_(self)


def encode_to_UTF8(data):
    try:
        return data.encode('UTF-8')
    except UnicodeEncodeError as e:
        print 'Could not encode data to UTF-8 -- %s' % e
        return False
    except Exception as e:
        raise e
        return False


def try_decode_UTF8(data):
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return False
    except Exception as e:
        raise e


class DummyWebsocketHandler(WebSocketHandler):

    def __init__(self, *_):
        pass