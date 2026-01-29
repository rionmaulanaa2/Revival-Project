# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/HunterPlugin/safaia/safaia_base.py
__author__ = 'lxn3032'
import errno
import os
import sys
import inspect
import struct
import functools
import hashlib
import socket
import time
import types
import traceback
import select
try:
    import json
except:
    import simplejson as json

try:
    import safaia_six as six
except ModuleNotFoundError:
    from . import safaia_six as six

DEVICE_CONNECT = 16
DEVICE_ACCEPT = 18
DEVICE_RUN_SCRIPT = 21
DEVICE_OUT = 24

def nothrow(func):

    @functools.wraps(func)
    def wrapped(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except:
            with open(os.path.join(self.get_writable_path(), 'safaia-error.txt'), 'a') as errortxt:
                errortxt.write(traceback.format_exc())

    return wrapped


class Singleton(type):

    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None
        return

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class Py3Encoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


class SimpleProtocolFilter(object):

    def __init__(self, encoding=None):
        super(SimpleProtocolFilter, self).__init__()
        self.buf = ''
        self.encoding = encoding or 'utf-8'
        self.secondary_encoding = 'gbk' if self.encoding == 'utf-8' else 'utf-8'

    def input(self, data):
        self.buf += data
        while len(self.buf) > 8:
            protocol_id, data_len = struct.unpack('ii', self.buf[0:8])
            if len(self.buf) >= data_len + 8:
                content = self.buf[8:data_len + 8]
                self.buf = self.buf[data_len + 8:]
                try:
                    content = content.decode('utf-8')
                except UnicodeDecodeError:
                    repr_content = repr(content)
                    if len(repr_content) > 500:
                        repr_content = repr_content[:500]
                    raise RuntimeError('[safaia] Got unexpected encoded content. {}'.format(repr_content))

                yield (
                 protocol_id, content)
            else:
                break

    def pack(self, protocol_id, content):
        if isinstance(content, dict):
            if six.PY3:
                content = json.dumps(content, cls=Py3Encoder)
            else:
                try:
                    content = json.dumps(content, encoding=self.encoding)
                except UnicodeDecodeError:
                    content = json.dumps(content, encoding=self.secondary_encoding)

        if isinstance(content, six.text_type):
            content = content.encode(self.encoding)
        return struct.pack('ii', protocol_id, len(content)) + content


class SoftMutex(object):

    def __init__(self, poll_intv=0.05):
        self.locked = False
        self.poll_intv = poll_intv

    def __enter__(self):
        while self.locked:
            time.sleep(self.poll_intv)

        self.locked = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.locked = False


class ClientSpec(object):

    def client_init(self):
        pass

    def get_engine_name(self):
        raise NotImplementedError

    def get_uid(self):
        try:
            import uuid
            import urllib2
            os_type = ClientSpec.get_platform(self)
            store_path = None
            if os_type in ('ios', 'android'):
                store_path = self.get_writable_path()
            else:
                if os_type in ('linux', ):
                    store_path = '/tmp'
                elif os_type in ('windows', ):
                    store_path = os.path.join(os.getenv('APPDATA'), 'safaia')
                    if not os.path.exists(store_path):
                        os.makedirs(store_path)
                if store_path:
                    uuid_file_path = os.path.join(store_path, 'safaia.uuid')
                    if not os.path.exists(uuid_file_path):
                        default_timeout = urllib2.socket.getdefaulttimeout()
                        try:
                            try:
                                urllib2.socket.setdefaulttimeout(0.08)
                                prev_uuid = urllib2.urlopen('http://hunter.nie.netease.com/mywork/uid').read()
                            except:
                                prev_uuid = None

                        finally:
                            urllib2.socket.setdefaulttimeout(default_timeout)

                        with open(uuid_file_path, 'w') as f:
                            f.write(prev_uuid or str(uuid.uuid4()).replace('-', '').lower())
                    return open(uuid_file_path, 'r').read().strip()
        except:
            pass

        return

    def get_platform(self):
        if os.getenv('APPDATA') and 'c' <= os.getenv('APPDATA')[0].lower() <= 'z':
            return 'windows'
        if os.path.exists('/private'):
            return 'ios'
        if os.path.exists('/data/local/tmp') or os.path.exists('/sdcard') and os.path.exists('/storage'):
            return 'android'
        if os.path.exists('/home'):
            return 'linux'
        return 'unknown'

    def register_update(self, update_func):
        raise NotImplementedError

    def unregister_update(self):
        raise NotImplementedError

    def get_base_dir(self):
        return '.'

    def get_writable_path(self):
        return self.get_base_dir()

    def get_readable_path(self):
        return self.get_base_dir()


@six.add_metaclass(Singleton)
class SafaiaBase(ClientSpec):
    __version__ = '1.5.1'

    def __init__(self):
        super(SafaiaBase, self).__init__()
        self.p = None
        self.s = None
        self._started = False
        self._send_buf = []
        self._send_buf_mutex = None
        self._thread_safe = True
        self.connect_addr = ('gate-gz.hunter.netease.com', 29006)
        self._disconnect_counter = 0
        self._connect_tries = 0
        self._connect_max_tries = 500
        self._read_size = 262144
        self._intranet_ip = None
        self._connection_init_args = ()
        self._server_finger_print = '0d26a820fb7b308c32fc1680a722acf6f2f0cfb928e38ebe9ed540c760b1df43c42aa5dff2d6c35745c2a23afff1e57afb186d77c66cd22f62f3b9bd7cc1e79f'
        self._pipeline_accepted = False
        self._pipeline_connect_start_time = 0.0
        self._pipeline_accepted_timeout = 5.0
        self._scope = {}
        self.exec_protected = True
        self.encoding = None
        self.devid = None
        self.deviceHttpTunnel = None
        self.deviceUdpTunnel = None
        self.script_interpreter_version = '%d.%d.%d' % sys.version_info[0:3]
        self.update_callbacks = set()
        self.protocol_callbacks = set()
        self.packet_callbacks = set()
        self.run_script_callbacks = set()
        self._interpreter_uri = None
        self.json = json
        return

    def start(self, process, script_lang='python', instruction_set='', default_name='Safaia client', **kwargs):
        if not process:
            raise ValueError('Argument `process` should not be empty value. Please specify a namespace identifier.')
        if not self._started:
            self._started = True
            if 'encoding' in kwargs:
                self.encoding = kwargs['encoding']
            if 'connect_addr' in kwargs:
                self.connect_addr = tuple(kwargs['connect_addr'])
            if 'thread_safe' in kwargs:
                self._thread_safe = kwargs['thread_safe']
            if 'server_finger_print' in kwargs:
                self._server_finger_print = kwargs['server_finger_print']
            if 'connect_max_tries' in kwargs:
                self._connect_max_tries = kwargs['connect_max_tries']
            if 'accepted_timeout' in kwargs:
                self._pipeline_accepted_timeout = kwargs['accepted_timeout']
            if 'read_size' in kwargs:
                self._read_size = kwargs['read_size']
            if 'interpreter_uri' in kwargs:
                self._interpreter_uri = kwargs['interpreter_uri']
            self._send_buf_mutex = self.get_mutex_object()
            self.client_init()
            globals()['Safaia'] = self.__class__
            self._scope['Safaia'] = self.__class__
            try:
                self._connection_init_args = (
                 process, self.connect_addr, script_lang, instruction_set, default_name)
                self.connection_init(*self._connection_init_args)
                self.register_update(self.update)
                print '[safaia] init ok.'
            except:
                traceback.print_exc()
                print '[safaia] core init failed.'

            errfilename = os.path.join(self.get_writable_path(), 'safaia-error.txt')
            if os.path.exists(errfilename) and os.path.isfile(errfilename):
                _, _, _, _, _, _, size, atime, mtime, ctime = os.stat(errfilename)
                if size > 1048576:
                    os.remove(errfilename)

    def stop(self):
        if self._started:
            self._started = False
            try:
                self.unregister_update()
            except:
                traceback.print_exc()

            try:
                self.disconnect()
            except:
                traceback.print_exc()

    def send(self, pid, content):
        if self.s:
            chunk = self.p.pack(pid, content)
            with self._send_buf_mutex:
                self._send_buf.append(chunk)

    @nothrow
    def update(self):
        if not self.s or not self.p:
            self._disconnect_counter += 1
            if self._disconnect_counter > 100:
                self._disconnect_counter = 0
                self._connect_tries += 1
                if self._connect_tries > self._connect_max_tries:
                    self.stop()
                    return
                self.connection_init(*self._connection_init_args)
            return
        for cb in self.update_callbacks:
            try:
                cb()
            except:
                self.update_callbacks.remove(cb)
                traceback.print_exc()
                break

        self._drain_output_buffer()
        if not self._pipeline_accepted:
            if time.time() - self._pipeline_connect_start_time > self._pipeline_accepted_timeout:
                if self._net_writable():
                    print '[safaia] pipeline response timeout, connect another pipeline.'
                else:
                    print '[safaia] tcp endpoint {} connection failed. please restart the game/app.\n[safaia] System library info:\n  socket: {}\n  select: {}\n  json:   {}\n  Safaia: {}\n'.format(self.connect_addr, socket, select, self.json, self.__class__)
                self.disconnect()
                return
        while self._net_readable():
            self._net_update()

        self._drain_output_buffer()

    def _net_readable(self):
        if not self.s:
            return False
        r, w, e = select.select([self.s], [], [], 0)
        return self.s in r

    def _net_writable(self):
        if not self.s:
            return False
        r, w, e = select.select([], [self.s], [], 0)
        return self.s in w

    def _net_update(self):
        time.sleep(0)
        small_chunks = []
        while self._net_readable():
            rx = self.s.recv(self._read_size)
            if not rx:
                self.disconnect()
                return
            small_chunks.append(rx)

        chunk = ''.join(small_chunks)
        if not chunk:
            self.disconnect()
            return
        for prot_id, prot_data in self.p.input(chunk):
            for cb in self.packet_callbacks:
                try:
                    prot_id, prot_data = cb(prot_id, prot_data)
                except:
                    self.packet_callbacks.remove(cb)
                    traceback.print_exc()

            if prot_id == DEVICE_ACCEPT:
                print '[safaia] connect success'
                print prot_data
                packet = json.loads(prot_data)
                self._pipeline_accepted = True
                if not self._server_finger_print:
                    self.exec_protected = False
                    print '[safaia] exec protection released. No server finger print required.'
                else:
                    server_identify_string = packet.get('server_identify_string', '')
                    if isinstance(server_identify_string, six.text_type):
                        server_identify_string = server_identify_string.encode()
                    if self._server_finger_print == hashlib.sha512(server_identify_string).hexdigest():
                        self.exec_protected = False
                        print '[safaia] exec protection released. Server finger print matched.'
                self.devid = packet.get('devid')
                self.deviceHttpTunnel = packet.get('deviceHttpTunnel')
                self.deviceUdpTunnel = packet.get('deviceUdpTunnel')
            elif prot_id == DEVICE_RUN_SCRIPT:
                packet = json.loads(prot_data)
                lang = packet['lang']
                script = packet['data']
                try:
                    if lang == 'python':
                        self.on_main_script(script)
                    else:
                        for cb in self.run_script_callbacks:
                            cb(lang, script)

                except:
                    traceback.print_exc()

            else:
                try:
                    packet = json.loads(prot_data)
                except ValueError:
                    prot_data_path = os.path.join(self.get_writable_path(), 'prot-data.json')
                    with open(prot_data_path, 'wb') as f:
                        f.write(prot_data)
                else:
                    for cb in self.protocol_callbacks:
                        try:
                            cb(prot_id, packet)
                        except:
                            traceback.print_exc()

    @property
    def intranet_ip(self):
        if not self._intranet_ip:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            (s.connect(('8.8.8.8', 53)),)
            self._intranet_ip = s.getsockname()[0]
            s.close()
        return self._intranet_ip

    def on_main_script(self, script):
        if self.exec_protected:
            return
        else:
            if type(script) is dict:
                import base64
                import marshal
                import zlib
                config = script['config']
                b64 = False
                compressed = False
                cutprefix = 0
                if config.get('base64'):
                    b64 = True
                if config.get('compress') == 'zlib':
                    compressed = True
                if config.get('cutprefix') != None:
                    cutprefix = int(config.get('cutprefix'))
                for bcode in script['bcodes']:
                    if b64:
                        bcode = base64.b64decode(bcode)
                    if compressed:
                        bcode = zlib.decompress(bcode)
                    if cutprefix > 0:
                        bcode = bcode[cutprefix:]
                    bcode = marshal.loads(bcode)
                    if six.PY2:
                        exec bcode in self._scope
                    else:
                        exec (
                         bcode, self._scope, self._scope)

            else:
                if self.encoding:
                    if six.PY2:
                        script = '# coding=%s\n%s' % (self.encoding, script.encode(self.encoding))
                    else:
                        script = '# coding=%s\n%s' % (self.encoding, script)
                code = compile(script, '<hunter script>', 'exec')
                if six.PY2:
                    exec code in self._scope
                else:
                    exec (
                     code, self._scope, self._scope)
            return

    def connection_init(self, process, connect_addr, script_lang, instruction_set, default_name):
        self.p = SimpleProtocolFilter(self.encoding)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(0.0)
        self.s.setblocking(False)
        try:
            try:
                self.s.connect_ex(connect_addr)
            except:
                self.disconnect()
                return

        finally:
            self.s.settimeout(0.0)

        connect_info = {'uid': self.get_uid(),
           'name': default_name,
           'gameId': process,
           'owner': '',
           'os': self.get_platform(),
           'script_lang': script_lang,
           'script_interpreter_version': self.script_interpreter_version,
           'instruction_set': instruction_set,
           'engine_name': self.get_engine_name(),
           'encoding': self.encoding,
           'safaia_version': self.__version__,
           'interpreter_uri': self._interpreter_uri,
           'intranet_ip': self.intranet_ip
           }
        self.send(DEVICE_CONNECT, connect_info)
        self._pipeline_accepted = False
        self._pipeline_connect_start_time = time.time()

    def disconnect(self):
        try:
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
        except:
            pass

        self.s = None
        with self._send_buf_mutex:
            self._send_buf = []
        return

    def install(self, module):
        try:
            init_method = None
            predicate = lambda m: inspect.ismethod(m) or inspect.isfunction(m)
            for method_name, original_method in inspect.getmembers(module, predicate):
                if six.PY2:
                    method = types.MethodType(original_method.__func__, self)
                else:
                    method = types.MethodType(original_method, self)
                if method_name == '__init__':
                    init_method = method
                elif not hasattr(self, method_name):
                    setattr(self, method_name, method)

            if init_method:
                init_method()
        except:
            traceback.print_exc()

        return

    def on_update(self, cb):
        self.update_callbacks.add(cb)
        return cb

    def on_protocol(self, cb):
        self.protocol_callbacks.add(cb)
        return cb

    def on_packet(self, cb):
        self.packet_callbacks.add(cb)
        return cb

    def on_script(self, cb):
        self.run_script_callbacks.add(cb)
        return cb

    def _drain_output_buffer(self):
        if not self._net_writable():
            return
        try:
            with self._send_buf_mutex:
                while len(self._send_buf) > 0:
                    while len(self._send_buf[0]) > 0:
                        bytes_sent = self.s.send(self._send_buf[0])
                        self._send_buf[0] = self._send_buf[0][bytes_sent:]

                    self._send_buf.pop(0)

        except socket.error as e:
            if e[0] in (errno.EWOULDBLOCK, errno.EINTR, errno.EAGAIN, 0, 10035, 35, 'timed out'):
                pass
            else:
                try:
                    errfilename = os.path.join(self.get_writable_path(), 'safaia-error.txt')
                    with open(errfilename, 'a') as errortxt:
                        errortxt.write('[errno={}] {}\n'.format(e[0], str(e)))
                except:
                    pass

                self.disconnect()

    def get_mutex_object(self):
        if self._thread_safe:
            import threading
            return threading.Lock()
        else:
            return SoftMutex()