# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/transport/tcp/ss_asyncore.py
from __future__ import print_function
import select
import socket
import sys
import time
import warnings
import os
from errno import EALREADY, EINPROGRESS, EWOULDBLOCK, ECONNRESET, EINVAL, ENOTCONN, ESHUTDOWN, EINTR, EISCONN, EBADF, ECONNABORTED, EPIPE, EAGAIN, errorcode
WSAEWOULDBLOCK = 10035
WSAEINPROGRESS = 10036
WSAEALREADY = 10037
_DISCONNECTED = frozenset((ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED, EPIPE,
 EBADF))
try:
    socket_map
except NameError:
    socket_map = {}

def _strerror(err):
    try:
        return os.strerror(err)
    except (ValueError, OverflowError, NameError):
        if err in errorcode:
            return errorcode[err]
        return 'Unknown error %s' % err


class ExitNow(Exception):
    pass


_reraised_exceptions = (
 ExitNow, KeyboardInterrupt, SystemExit)

def read(obj):
    try:
        obj.handle_read_event()
    except _reraised_exceptions:
        raise
    except:
        obj.handle_error()


def write(obj):
    try:
        obj.handle_write_event()
    except _reraised_exceptions:
        raise
    except:
        obj.handle_error()


def _exception(obj):
    try:
        obj.handle_expt_event()
    except _reraised_exceptions:
        raise
    except:
        obj.handle_error()


def readwrite(obj, flags):
    try:
        if flags & select.POLLIN:
            obj.handle_read_event()
        if flags & select.POLLOUT:
            obj.handle_write_event()
        if flags & select.POLLPRI:
            obj.handle_expt_event()
        if flags & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
            obj.handle_close()
    except socket.error as e:
        if e.args[0] not in _DISCONNECTED:
            obj.handle_error()
        else:
            obj.handle_close()
    except _reraised_exceptions:
        raise
    except:
        obj.handle_error()


def poll(timeout=0.0, map=None):
    if map is None:
        map = socket_map
    if map:
        r = []
        w = []
        e = []
        for fd, obj in map.items():
            is_r = obj.readable()
            is_w = obj.writable()
            if is_r:
                r.append(fd)
            if is_w and not obj.accepting:
                w.append(fd)
            if is_r or is_w:
                e.append(fd)

        if [] == r == w == e:
            time.sleep(timeout)
            return
        try:
            r, w, e = select.select(r, w, e, timeout)
        except select.error as err:
            if err.args[0] != EINTR:
                raise
            else:
                return

        for fd in r:
            obj = map.get(fd)
            if obj is None:
                continue
            read(obj)

        for fd in w:
            obj = map.get(fd)
            if obj is None:
                continue
            write(obj)

        for fd in e:
            obj = map.get(fd)
            if obj is None:
                continue
            _exception(obj)

    return


def poll2--- This code section failed: ---

 175       0  LOAD_FAST             1  'map'
           3  LOAD_CONST            0  ''
           6  COMPARE_OP            8  'is'
           9  POP_JUMP_IF_FALSE    21  'to 21'

 176      12  LOAD_GLOBAL           1  'socket_map'
          15  STORE_FAST            1  'map'
          18  JUMP_FORWARD          0  'to 21'
        21_0  COME_FROM                '18'

 177      21  LOAD_FAST             0  'timeout'
          24  LOAD_CONST            0  ''
          27  COMPARE_OP            9  'is-not'
          30  POP_JUMP_IF_FALSE    49  'to 49'

 179      33  LOAD_GLOBAL           2  'int'
          36  LOAD_GLOBAL           1  'socket_map'
          39  BINARY_MULTIPLY  
          40  CALL_FUNCTION_1       1 
          43  STORE_FAST            0  'timeout'
          46  JUMP_FORWARD          0  'to 49'
        49_0  COME_FROM                '46'

 180      49  LOAD_GLOBAL           3  'select'
          52  LOAD_ATTR             4  'poll'
          55  CALL_FUNCTION_0       0 
          58  STORE_FAST            2  'pollster'

 181      61  LOAD_FAST             1  'map'
          64  POP_JUMP_IF_FALSE   374  'to 374'

 182      67  SETUP_LOOP          157  'to 227'
          70  LOAD_FAST             1  'map'
          73  LOAD_ATTR             5  'items'
          76  CALL_FUNCTION_0       0 
          79  GET_ITER         
          80  FOR_ITER            143  'to 226'
          83  UNPACK_SEQUENCE_2     2 
          86  STORE_FAST            3  'fd'
          89  STORE_FAST            4  'obj'

 183      92  LOAD_CONST            2  ''
          95  STORE_FAST            5  'flags'

 184      98  LOAD_FAST             4  'obj'
         101  LOAD_ATTR             6  'readable'
         104  CALL_FUNCTION_0       0 
         107  POP_JUMP_IF_FALSE   133  'to 133'

 185     110  LOAD_FAST             5  'flags'
         113  LOAD_GLOBAL           3  'select'
         116  LOAD_ATTR             7  'POLLIN'
         119  LOAD_GLOBAL           3  'select'
         122  LOAD_ATTR             8  'POLLPRI'
         125  BINARY_OR        
         126  INPLACE_OR       
         127  STORE_FAST            5  'flags'
         130  JUMP_FORWARD          0  'to 133'
       133_0  COME_FROM                '130'

 187     133  LOAD_FAST             4  'obj'
         136  LOAD_ATTR             9  'writable'
         139  CALL_FUNCTION_0       0 
         142  POP_JUMP_IF_FALSE   171  'to 171'
         145  LOAD_FAST             4  'obj'
         148  LOAD_ATTR            10  'accepting'
         151  UNARY_NOT        
       152_0  COME_FROM                '142'
         152  POP_JUMP_IF_FALSE   171  'to 171'

 188     155  LOAD_FAST             5  'flags'
         158  LOAD_GLOBAL           3  'select'
         161  LOAD_ATTR            11  'POLLOUT'
         164  INPLACE_OR       
         165  STORE_FAST            5  'flags'
         168  JUMP_FORWARD          0  'to 171'
       171_0  COME_FROM                '168'

 189     171  LOAD_FAST             5  'flags'
         174  POP_JUMP_IF_FALSE    80  'to 80'

 192     177  LOAD_FAST             5  'flags'
         180  LOAD_GLOBAL           3  'select'
         183  LOAD_ATTR            12  'POLLERR'
         186  LOAD_GLOBAL           3  'select'
         189  LOAD_ATTR            13  'POLLHUP'
         192  BINARY_OR        
         193  LOAD_GLOBAL           3  'select'
         196  LOAD_ATTR            14  'POLLNVAL'
         199  BINARY_OR        
         200  INPLACE_OR       
         201  STORE_FAST            5  'flags'

 193     204  LOAD_FAST             2  'pollster'
         207  LOAD_ATTR            15  'register'
         210  LOAD_FAST             3  'fd'
         213  LOAD_FAST             5  'flags'
         216  CALL_FUNCTION_2       2 
         219  POP_TOP          
         220  JUMP_BACK            80  'to 80'
         223  JUMP_BACK            80  'to 80'
         226  POP_BLOCK        
       227_0  COME_FROM                '67'

 194     227  SETUP_EXCEPT         19  'to 249'

 195     230  LOAD_FAST             2  'pollster'
         233  LOAD_ATTR             4  'poll'
         236  LOAD_FAST             0  'timeout'
         239  CALL_FUNCTION_1       1 
         242  STORE_FAST            6  'r'
         245  POP_BLOCK        
         246  JUMP_FORWARD         53  'to 302'
       249_0  COME_FROM                '227'

 196     249  DUP_TOP          
         250  LOAD_GLOBAL           3  'select'
         253  LOAD_ATTR            16  'error'
         256  COMPARE_OP           10  'exception-match'
         259  POP_JUMP_IF_FALSE   301  'to 301'
         262  POP_TOP          
         263  STORE_FAST            7  'err'
         266  POP_TOP          

 197     267  LOAD_FAST             7  'err'
         270  LOAD_ATTR            17  'args'
         273  LOAD_CONST            2  ''
         276  BINARY_SUBSCR    
         277  LOAD_GLOBAL          18  'EINTR'
         280  COMPARE_OP            3  '!='
         283  POP_JUMP_IF_FALSE   292  'to 292'

 198     286  RAISE_VARARGS_0       0 
         289  JUMP_FORWARD          0  'to 292'
       292_0  COME_FROM                '289'

 199     292  BUILD_LIST_0          0 
         295  STORE_FAST            6  'r'
         298  JUMP_FORWARD          1  'to 302'
         301  END_FINALLY      
       302_0  COME_FROM                '301'
       302_1  COME_FROM                '246'

 200     302  SETUP_LOOP           69  'to 374'
         305  LOAD_FAST             6  'r'
         308  GET_ITER         
         309  FOR_ITER             58  'to 370'
         312  UNPACK_SEQUENCE_2     2 
         315  STORE_FAST            3  'fd'
         318  STORE_FAST            5  'flags'

 201     321  LOAD_FAST             1  'map'
         324  LOAD_ATTR            19  'get'
         327  LOAD_FAST             3  'fd'
         330  CALL_FUNCTION_1       1 
         333  STORE_FAST            4  'obj'

 202     336  LOAD_FAST             4  'obj'
         339  LOAD_CONST            0  ''
         342  COMPARE_OP            8  'is'
         345  POP_JUMP_IF_FALSE   354  'to 354'

 203     348  CONTINUE            309  'to 309'
         351  JUMP_FORWARD          0  'to 354'
       354_0  COME_FROM                '351'

 204     354  LOAD_GLOBAL          20  'readwrite'
         357  LOAD_FAST             4  'obj'
         360  LOAD_FAST             5  'flags'
         363  CALL_FUNCTION_2       2 
         366  POP_TOP          
         367  JUMP_BACK           309  'to 309'
         370  POP_BLOCK        
       371_0  COME_FROM                '302'
         371  JUMP_FORWARD          0  'to 374'
       374_0  COME_FROM                '302'
         374  LOAD_CONST            0  ''
         377  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1' instruction at offset 40


poll3 = poll2

def loop(timeout=30.0, use_poll=False, map=None, count=None):
    if map is None:
        map = socket_map
    if use_poll and hasattr(select, 'poll'):
        poll_fun = poll2
    else:
        poll_fun = poll
    if count is None:
        while map:
            poll_fun(timeout, map)

    else:
        while map and count > 0:
            poll_fun(timeout, map)
            count = count - 1

    return


class dispatcher():
    debug = False
    connected = False
    accepting = False
    connecting = False
    closing = False
    addr = None
    ignore_log_types = frozenset(['warning'])

    def __init__(self, sock=None, map=None):
        if map is None:
            self._map = socket_map
        else:
            self._map = map
        self._fileno = None
        if sock:
            sock.setblocking(0)
            self.set_socket(sock, map)
            self.connected = True
            try:
                self.addr = sock.getpeername()
            except socket.error as err:
                if err.args[0] in (ENOTCONN, EINVAL):
                    self.connected = False
                else:
                    self.del_channel(map)
                    raise

        else:
            self.socket = None
        return

    def __repr__(self):
        status = [self.__class__.__module__ + '.' + self.__class__.__name__]
        if self.accepting and self.addr:
            status.append('listening')
        elif self.connected:
            status.append('connected')
        if self.addr is not None:
            try:
                status.append('%s:%d' % self.addr)
            except TypeError:
                status.append(repr(self.addr))

        return '<%s at %#x>' % (' '.join(status), id(self))

    __str__ = __repr__

    def add_channel(self, map=None):
        if map is None:
            map = self._map
        map[self._fileno] = self
        return

    def del_channel(self, map=None):
        fd = self._fileno
        if map is None:
            map = self._map
        if fd in map:
            del map[fd]
        self._fileno = None
        return

    def create_socket(self, family, type):
        self.family_and_type = (
         family, type)
        sock = socket.socket(family, type)
        sock.setblocking(0)
        self.set_socket(sock)

    def set_socket(self, sock, map=None):
        self.socket = sock
        self._fileno = sock.fileno()
        self.add_channel(map)

    def set_reuse_addr(self):
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1)
        except socket.error:
            pass

    def readable(self):
        return True

    def writable(self):
        return True

    def listen(self, num):
        self.accepting = True
        if os.name == 'nt' and num > 5:
            num = 5
        return self.socket.listen(num)

    def bind(self, addr):
        self.addr = addr
        return self.socket.bind(addr)

    def connect(self, address):
        self.connected = False
        self.connecting = True
        err = self.socket.connect_ex(address)
        if err in (EINPROGRESS, EALREADY, EWOULDBLOCK, WSAEWOULDBLOCK, WSAEINPROGRESS,
         WSAEALREADY) or err == EINVAL and os.name in ('nt', 'ce'):
            self.addr = address
            return
        if err in (0, EISCONN):
            self.addr = address
            self.handle_connect_event()
        else:
            raise socket.error(err, errorcode[err])

    def accept(self):
        try:
            conn, addr = self.socket.accept()
        except TypeError:
            return None
        except socket.error as why:
            if why.args[0] in (EWOULDBLOCK, ECONNABORTED, EAGAIN):
                return None
            raise
        else:
            return (
             conn, addr)

        return None

    def send(self, data):
        try:
            result = self.socket.send(data)
            return result
        except socket.error as why:
            if why.args[0] == EWOULDBLOCK:
                return 0
            if why.args[0] in _DISCONNECTED:
                self.handle_close()
                return 0
            raise

    def recv(self, buffer_size):
        try:
            data = self.socket.recv(buffer_size)
            if not data:
                self.handle_close()
                return ''
            return data
        except socket.error as why:
            if why.args[0] in _DISCONNECTED:
                self.handle_close()
                return ''
            raise

    def close(self):
        self.connected = False
        self.accepting = False
        self.connecting = False
        self.del_channel()
        try:
            self.socket.close()
        except socket.error as why:
            if why.args[0] not in (ENOTCONN, EBADF):
                raise

    def __getattr__(self, attr):
        try:
            retattr = getattr(self.socket, attr)
        except AttributeError:
            raise AttributeError("%s instance has no attribute '%s'" % (
             self.__class__.__name__, attr))
        else:
            msg = '%(me)s.%(attr)s is deprecated. Use %(me)s.socket.%(attr)s instead.' % {'me': self.__class__.__name__,'attr': attr}
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return retattr

    def log(self, message):
        sys.stderr.write('log: %s\n' % str(message))

    def log_info(self, message, type='info'):
        if type not in self.ignore_log_types:
            print('%s: %s' % (type, message))

    def handle_read_event(self):
        if self.accepting:
            self.handle_accept()
        elif not self.connected:
            if self.connecting:
                self.handle_connect_event()
            self.handle_read()
        else:
            self.handle_read()

    def handle_connect_event(self):
        err = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if err != 0:
            raise socket.error(err, _strerror(err))
        self.handle_connect()
        self.connected = True
        self.connecting = False

    def handle_write_event(self):
        if self.accepting:
            return
        if not self.connected:
            if self.connecting:
                self.handle_connect_event()
        self.handle_write()

    def handle_expt_event(self):
        err = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if err != 0:
            self.handle_close()
        else:
            self.handle_expt()

    def handle_error(self):
        nil, t, v, tbinfo = compact_traceback()
        try:
            self_repr = repr(self)
        except:
            self_repr = '<__repr__(self) failed for object at %0x>' % id(self)

        self.log_info('uncaptured python exception, closing channel %s (%s:%s %s)' % (
         self_repr,
         t,
         v,
         tbinfo), 'error')
        self.handle_close()

    def handle_expt(self):
        self.log_info('unhandled incoming priority event', 'warning')

    def handle_read(self):
        self.log_info('unhandled read event', 'warning')

    def handle_write(self):
        self.log_info('unhandled write event', 'warning')

    def handle_connect(self):
        self.log_info('unhandled connect event', 'warning')

    def handle_accept(self):
        self.log_info('unhandled accept event', 'warning')

    def handle_close(self):
        self.log_info('unhandled close event', 'warning')
        self.close()


class dispatcher_with_send(dispatcher):

    def __init__(self, sock=None, map=None):
        dispatcher.__init__(self, sock, map)
        self.out_buffer = ''

    def initiate_send(self):
        num_sent = 0
        num_sent = dispatcher.send(self, self.out_buffer[:512])
        self.out_buffer = self.out_buffer[num_sent:]

    def handle_write(self):
        self.initiate_send()

    def writable(self):
        return not self.connected or len(self.out_buffer)

    def send(self, data):
        if self.debug:
            self.log_info('sending %s' % repr(data))
        self.out_buffer = self.out_buffer + data
        self.initiate_send()


def compact_traceback():
    t, v, tb = sys.exc_info()
    tbinfo = []
    if not tb:
        raise AssertionError('traceback does not exist')
    while tb:
        tbinfo.append((
         tb.tb_frame.f_code.co_filename,
         tb.tb_frame.f_code.co_name,
         str(tb.tb_lineno)))
        tb = tb.tb_next

    del tb
    file, function, line = tbinfo[-1]
    info = ' '.join([ '[%s|%s|%s]' % x for x in tbinfo ])
    return (
     (
      file, function, line), t, v, info)


def close_all(map=None, ignore_all=False):
    if map is None:
        map = socket_map
    for x in map.values():
        try:
            x.close()
        except OSError as x:
            if x.args[0] == EBADF:
                pass
            elif not ignore_all:
                raise
        except _reraised_exceptions:
            raise
        except:
            if not ignore_all:
                raise

    map.clear()
    return


if os.name == 'posix':
    import fcntl

    class file_wrapper():

        def __init__(self, fd):
            self.fd = os.dup(fd)

        def recv(self, *args):
            return os.read(self.fd, *args)

        def send(self, *args):
            return os.write(self.fd, *args)

        def getsockopt(self, level, optname, buflen=None):
            if level == socket.SOL_SOCKET and optname == socket.SO_ERROR and not buflen:
                return 0
            raise NotImplementedError('Only asyncore specific behaviour implemented.')

        read = recv
        write = send

        def close(self):
            if self.fd < 0:
                return
            fd = self.fd
            self.fd = -1
            os.close(fd)

        def fileno(self):
            return self.fd


    class file_dispatcher(dispatcher):

        def __init__(self, fd, map=None):
            dispatcher.__init__(self, None, map)
            self.connected = True
            try:
                fd = fd.fileno()
            except AttributeError:
                pass

            self.set_file(fd)
            flags = fcntl.fcntl(fd, fcntl.F_GETFL, 0)
            flags = flags | os.O_NONBLOCK
            fcntl.fcntl(fd, fcntl.F_SETFL, flags)
            return

        def set_file(self, fd):
            self.socket = file_wrapper(fd)
            self._fileno = self.socket.fileno()
            self.add_channel()