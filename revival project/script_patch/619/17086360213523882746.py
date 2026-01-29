# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Lib/msgpack/fallback.py
from __future__ import absolute_import
from six.moves import range
import six
import sys
import array
import struct
if sys.version_info[0] == 3:
    PY3 = True
    int_types = int
    Unicode = str
    xrange = range

    def dict_iteritems(d):
        return d.items()


else:
    PY3 = False
    int_types = (int, long)
    Unicode = unicode

    def dict_iteritems(d):
        return d.iteritems()


if hasattr(sys, 'pypy_version_info'):
    from __pypy__ import newlist_hint
    try:
        from __pypy__.builders import BytesBuilder as StringBuilder
    except ImportError:
        from __pypy__.builders import StringBuilder

    USING_STRINGBUILDER = True

    class StringIO(object):

        def __init__(self, s=''):
            if s:
                self.builder = StringBuilder(len(s))
                self.builder.append(s)
            else:
                self.builder = StringBuilder()

        def write(self, s):
            self.builder.append(s)

        def getvalue(self):
            return self.builder.build()


else:
    USING_STRINGBUILDER = False
    from StringIO import StringIO
    newlist_hint = lambda size: []
from msgpack.exceptions import BufferFull, OutOfData, UnpackValueError, PackValueError, ExtraData
from msgpack import ExtType
EX_SKIP = 0
EX_CONSTRUCT = 1
EX_READ_ARRAY_HEADER = 2
EX_READ_MAP_HEADER = 3
TYPE_IMMEDIATE = 0
TYPE_ARRAY = 1
TYPE_MAP = 2
TYPE_RAW = 3
TYPE_BIN = 4
TYPE_EXT = 5
DEFAULT_RECURSE_LIMIT = 511

def unpack(stream, **kwargs):
    unpacker = Unpacker(stream, **kwargs)
    ret = unpacker._fb_unpack()
    if unpacker._fb_got_extradata():
        raise ExtraData(ret, unpacker._fb_get_extradata())
    return ret


def unpackb(packed, **kwargs):
    unpacker = Unpacker(None, **kwargs)
    unpacker.feed(packed)
    try:
        ret = unpacker._fb_unpack()
    except OutOfData:
        raise UnpackValueError('Data is not enough.')

    if unpacker._fb_got_extradata():
        raise ExtraData(ret, unpacker._fb_get_extradata())
    return ret


class Unpacker(object):

    def __init__(self, file_like=None, read_size=0, use_list=True, object_hook=None, object_pairs_hook=None, list_hook=None, encoding=None, unicode_errors='strict', max_buffer_size=0, ext_hook=ExtType, max_str_len=2147483647, max_bin_len=2147483647, max_array_len=2147483647, max_map_len=2147483647, max_ext_len=2147483647):
        if file_like is None:
            self._fb_feeding = True
        else:
            if not callable(file_like.read):
                raise TypeError('`file_like.read` must be callable')
            self.file_like = file_like
            self._fb_feeding = False
        self._fb_buffers = []
        self._fb_buf_i = 0
        self._fb_buf_o = 0
        self._fb_buf_n = 0
        self._fb_sloppiness = 0
        self._max_buffer_size = max_buffer_size or 2147483647
        if read_size > self._max_buffer_size:
            raise ValueError('read_size must be smaller than max_buffer_size')
        self._read_size = read_size or min(self._max_buffer_size, 4096)
        self._encoding = encoding
        self._unicode_errors = unicode_errors
        self._use_list = use_list
        self._list_hook = list_hook
        self._object_hook = object_hook
        self._object_pairs_hook = object_pairs_hook
        self._ext_hook = ext_hook
        self._max_str_len = max_str_len
        self._max_bin_len = max_bin_len
        self._max_array_len = max_array_len
        self._max_map_len = max_map_len
        self._max_ext_len = max_ext_len
        if list_hook is not None and not callable(list_hook):
            raise TypeError('`list_hook` is not callable')
        if object_hook is not None and not callable(object_hook):
            raise TypeError('`object_hook` is not callable')
        if object_pairs_hook is not None and not callable(object_pairs_hook):
            raise TypeError('`object_pairs_hook` is not callable')
        if object_hook is not None and object_pairs_hook is not None:
            raise TypeError('object_pairs_hook and object_hook are mutually exclusive')
        if not callable(ext_hook):
            raise TypeError('`ext_hook` is not callable')
        return

    def feed(self, next_bytes):
        if isinstance(next_bytes, array.array):
            next_bytes = next_bytes.tostring()
        elif isinstance(next_bytes, bytearray):
            next_bytes = bytes(next_bytes)
        if self._fb_buf_n + len(next_bytes) - self._fb_sloppiness > self._max_buffer_size:
            raise BufferFull
        self._fb_buf_n += len(next_bytes)
        self._fb_buffers.append(next_bytes)

    def _fb_sloppy_consume(self):
        if self._fb_buf_i:
            for i in range(self._fb_buf_i):
                self._fb_buf_n -= len(self._fb_buffers[i])

            self._fb_buffers = self._fb_buffers[self._fb_buf_i:]
            self._fb_buf_i = 0
        if self._fb_buffers:
            self._fb_sloppiness = self._fb_buf_o
        else:
            self._fb_sloppiness = 0

    def _fb_consume(self):
        if self._fb_buf_i:
            for i in range(self._fb_buf_i):
                self._fb_buf_n -= len(self._fb_buffers[i])

            self._fb_buffers = self._fb_buffers[self._fb_buf_i:]
            self._fb_buf_i = 0
        if self._fb_buffers:
            self._fb_buffers[0] = self._fb_buffers[0][self._fb_buf_o:]
            self._fb_buf_n -= self._fb_buf_o
        else:
            self._fb_buf_n = 0
        self._fb_buf_o = 0
        self._fb_sloppiness = 0

    def _fb_got_extradata(self):
        if self._fb_buf_i != len(self._fb_buffers):
            return True
        if self._fb_feeding:
            return False
        if not self.file_like:
            return False
        if self.file_like.read(1):
            return True
        return False

    def __iter__(self):
        return self

    def read_bytes(self, n):
        return self._fb_read(n)

    def _fb_rollback(self):
        self._fb_buf_i = 0
        self._fb_buf_o = self._fb_sloppiness

    def _fb_get_extradata(self):
        bufs = self._fb_buffers[self._fb_buf_i:]
        if bufs:
            bufs[0] = bufs[0][self._fb_buf_o:]
        return ''.join(bufs)

    def _fb_read(self, n, write_bytes=None):
        buffs = self._fb_buffers
        if write_bytes is None and self._fb_buf_i < len(buffs) and self._fb_buf_o + n < len(buffs[self._fb_buf_i]):
            self._fb_buf_o += n
            return buffs[self._fb_buf_i][self._fb_buf_o - n:self._fb_buf_o]
        else:
            ret = ''
            while len(ret) != n:
                sliced = n - len(ret)
                if self._fb_buf_i == len(buffs):
                    if self._fb_feeding:
                        break
                    to_read = sliced
                    if self._read_size > to_read:
                        to_read = self._read_size
                    tmp = self.file_like.read(to_read)
                    if not tmp:
                        break
                    buffs.append(tmp)
                    self._fb_buf_n += len(tmp)
                    continue
                ret += buffs[self._fb_buf_i][self._fb_buf_o:self._fb_buf_o + sliced]
                self._fb_buf_o += sliced
                if self._fb_buf_o >= len(buffs[self._fb_buf_i]):
                    self._fb_buf_o = 0
                    self._fb_buf_i += 1

            if len(ret) != n:
                self._fb_rollback()
                raise OutOfData
            if write_bytes is not None:
                write_bytes(ret)
            return ret

    def _read_header(self, execute=EX_CONSTRUCT, write_bytes=None):
        typ = TYPE_IMMEDIATE
        n = 0
        obj = None
        c = self._fb_read(1, write_bytes)
        b = ord(c)
        if b & 128 == 0:
            obj = b
        elif b & 224 == 224:
            obj = struct.unpack('b', c)[0]
        elif b & 224 == 160:
            n = b & 31
            obj = self._fb_read(n, write_bytes)
            typ = TYPE_RAW
            if n > self._max_str_len:
                raise ValueError('%s exceeds max_str_len(%s)', n, self._max_str_len)
        elif b & 240 == 144:
            n = b & 15
            typ = TYPE_ARRAY
            if n > self._max_array_len:
                raise ValueError('%s exceeds max_array_len(%s)', n, self._max_array_len)
        elif b & 240 == 128:
            n = b & 15
            typ = TYPE_MAP
            if n > self._max_map_len:
                raise ValueError('%s exceeds max_map_len(%s)', n, self._max_map_len)
        elif b == 192:
            obj = None
        elif b == 194:
            obj = False
        elif b == 195:
            obj = True
        elif b == 196:
            typ = TYPE_BIN
            n = struct.unpack('B', self._fb_read(1, write_bytes))[0]
            if n > self._max_bin_len:
                raise ValueError('%s exceeds max_bin_len(%s)' % (n, self._max_bin_len))
            obj = self._fb_read(n, write_bytes)
        elif b == 197:
            typ = TYPE_BIN
            n = struct.unpack('>H', self._fb_read(2, write_bytes))[0]
            if n > self._max_bin_len:
                raise ValueError('%s exceeds max_bin_len(%s)' % (n, self._max_bin_len))
            obj = self._fb_read(n, write_bytes)
        elif b == 198:
            typ = TYPE_BIN
            n = struct.unpack('>I', self._fb_read(4, write_bytes))[0]
            if n > self._max_bin_len:
                raise ValueError('%s exceeds max_bin_len(%s)' % (n, self._max_bin_len))
            obj = self._fb_read(n, write_bytes)
        elif b == 199:
            typ = TYPE_EXT
            L, n = struct.unpack('Bb', self._fb_read(2, write_bytes))
            if L > self._max_ext_len:
                raise ValueError('%s exceeds max_ext_len(%s)' % (L, self._max_ext_len))
            obj = self._fb_read(L, write_bytes)
        elif b == 200:
            typ = TYPE_EXT
            L, n = struct.unpack('>Hb', self._fb_read(3, write_bytes))
            if L > self._max_ext_len:
                raise ValueError('%s exceeds max_ext_len(%s)' % (L, self._max_ext_len))
            obj = self._fb_read(L, write_bytes)
        elif b == 201:
            typ = TYPE_EXT
            L, n = struct.unpack('>Ib', self._fb_read(5, write_bytes))
            if L > self._max_ext_len:
                raise ValueError('%s exceeds max_ext_len(%s)' % (L, self._max_ext_len))
            obj = self._fb_read(L, write_bytes)
        elif b == 202:
            obj = struct.unpack('>f', self._fb_read(4, write_bytes))[0]
        elif b == 203:
            obj = struct.unpack('>d', self._fb_read(8, write_bytes))[0]
        elif b == 204:
            obj = struct.unpack('B', self._fb_read(1, write_bytes))[0]
        elif b == 205:
            obj = struct.unpack('>H', self._fb_read(2, write_bytes))[0]
        elif b == 206:
            obj = struct.unpack('>I', self._fb_read(4, write_bytes))[0]
        elif b == 207:
            obj = struct.unpack('>Q', self._fb_read(8, write_bytes))[0]
        elif b == 208:
            obj = struct.unpack('b', self._fb_read(1, write_bytes))[0]
        elif b == 209:
            obj = struct.unpack('>h', self._fb_read(2, write_bytes))[0]
        elif b == 210:
            obj = struct.unpack('>i', self._fb_read(4, write_bytes))[0]
        elif b == 211:
            obj = struct.unpack('>q', self._fb_read(8, write_bytes))[0]
        elif b == 212:
            typ = TYPE_EXT
            if self._max_ext_len < 1:
                raise ValueError('%s exceeds max_ext_len(%s)' % (1, self._max_ext_len))
            n, obj = struct.unpack('b1s', self._fb_read(2, write_bytes))
        elif b == 213:
            typ = TYPE_EXT
            if self._max_ext_len < 2:
                raise ValueError('%s exceeds max_ext_len(%s)' % (2, self._max_ext_len))
            n, obj = struct.unpack('b2s', self._fb_read(3, write_bytes))
        elif b == 214:
            typ = TYPE_EXT
            if self._max_ext_len < 4:
                raise ValueError('%s exceeds max_ext_len(%s)' % (4, self._max_ext_len))
            n, obj = struct.unpack('b4s', self._fb_read(5, write_bytes))
        elif b == 215:
            typ = TYPE_EXT
            if self._max_ext_len < 8:
                raise ValueError('%s exceeds max_ext_len(%s)' % (8, self._max_ext_len))
            n, obj = struct.unpack('b8s', self._fb_read(9, write_bytes))
        elif b == 216:
            typ = TYPE_EXT
            if self._max_ext_len < 16:
                raise ValueError('%s exceeds max_ext_len(%s)' % (16, self._max_ext_len))
            n, obj = struct.unpack('b16s', self._fb_read(17, write_bytes))
        elif b == 217:
            typ = TYPE_RAW
            n = struct.unpack('B', self._fb_read(1, write_bytes))[0]
            if n > self._max_str_len:
                raise ValueError('%s exceeds max_str_len(%s)', n, self._max_str_len)
            obj = self._fb_read(n, write_bytes)
        elif b == 218:
            typ = TYPE_RAW
            n = struct.unpack('>H', self._fb_read(2, write_bytes))[0]
            if n > self._max_str_len:
                raise ValueError('%s exceeds max_str_len(%s)', n, self._max_str_len)
            obj = self._fb_read(n, write_bytes)
        elif b == 219:
            typ = TYPE_RAW
            n = struct.unpack('>I', self._fb_read(4, write_bytes))[0]
            if n > self._max_str_len:
                raise ValueError('%s exceeds max_str_len(%s)', n, self._max_str_len)
            obj = self._fb_read(n, write_bytes)
        elif b == 220:
            n = struct.unpack('>H', self._fb_read(2, write_bytes))[0]
            if n > self._max_array_len:
                raise ValueError('%s exceeds max_array_len(%s)', n, self._max_array_len)
            typ = TYPE_ARRAY
        elif b == 221:
            n = struct.unpack('>I', self._fb_read(4, write_bytes))[0]
            if n > self._max_array_len:
                raise ValueError('%s exceeds max_array_len(%s)', n, self._max_array_len)
            typ = TYPE_ARRAY
        elif b == 222:
            n = struct.unpack('>H', self._fb_read(2, write_bytes))[0]
            if n > self._max_map_len:
                raise ValueError('%s exceeds max_map_len(%s)', n, self._max_map_len)
            typ = TYPE_MAP
        elif b == 223:
            n = struct.unpack('>I', self._fb_read(4, write_bytes))[0]
            if n > self._max_map_len:
                raise ValueError('%s exceeds max_map_len(%s)', n, self._max_map_len)
            typ = TYPE_MAP
        else:
            raise UnpackValueError('Unknown header: 0x%x' % b)
        return (typ, n, obj)

    def _fb_unpack(self, execute=EX_CONSTRUCT, write_bytes=None):
        typ, n, obj = self._read_header(execute, write_bytes)
        if execute == EX_READ_ARRAY_HEADER:
            if typ != TYPE_ARRAY:
                raise UnpackValueError('Expected array')
            return n
        else:
            if execute == EX_READ_MAP_HEADER:
                if typ != TYPE_MAP:
                    raise UnpackValueError('Expected map')
                return n
            if typ == TYPE_ARRAY:
                if execute == EX_SKIP:
                    for i in range(n):
                        self._fb_unpack(EX_SKIP, write_bytes)

                    return
                ret = newlist_hint(n)
                for i in range(n):
                    ret.append(self._fb_unpack(EX_CONSTRUCT, write_bytes))

                if self._list_hook is not None:
                    ret = self._list_hook(ret)
                if self._use_list:
                    return ret
                return tuple(ret)
            if typ == TYPE_MAP:
                if execute == EX_SKIP:
                    for i in range(n):
                        self._fb_unpack(EX_SKIP, write_bytes)
                        self._fb_unpack(EX_SKIP, write_bytes)

                    return
                if self._object_pairs_hook is not None:
                    ret = self._object_pairs_hook(((self._fb_unpack(EX_CONSTRUCT, write_bytes), self._fb_unpack(EX_CONSTRUCT, write_bytes)) for _ in range(n)))
                else:
                    ret = {}
                    for _ in range(n):
                        key = self._fb_unpack(EX_CONSTRUCT, write_bytes)
                        ret[key] = self._fb_unpack(EX_CONSTRUCT, write_bytes)

                if self._object_hook is not None:
                    ret = self._object_hook(ret)
                return ret
            if execute == EX_SKIP:
                return
            if typ == TYPE_RAW:
                if self._encoding is not None:
                    obj = obj.decode(self._encoding, self._unicode_errors)
                return obj
            if typ == TYPE_EXT:
                return self._ext_hook(n, obj)
            if typ == TYPE_BIN:
                return obj
            return obj

    def next(self):
        try:
            ret = self._fb_unpack(EX_CONSTRUCT, None)
            self._fb_sloppy_consume()
            return ret
        except OutOfData:
            self._fb_consume()
            raise StopIteration

        return

    __next__ = next

    def skip(self, write_bytes=None):
        self._fb_unpack(EX_SKIP, write_bytes)
        self._fb_consume()

    def unpack(self, write_bytes=None):
        ret = self._fb_unpack(EX_CONSTRUCT, write_bytes)
        self._fb_consume()
        return ret

    def read_array_header(self, write_bytes=None):
        ret = self._fb_unpack(EX_READ_ARRAY_HEADER, write_bytes)
        self._fb_consume()
        return ret

    def read_map_header(self, write_bytes=None):
        ret = self._fb_unpack(EX_READ_MAP_HEADER, write_bytes)
        self._fb_consume()
        return ret


class Packer(object):

    def __init__(self, default=None, encoding='utf-8', unicode_errors='strict', use_single_float=False, autoreset=True, use_bin_type=False):
        self._use_float = use_single_float
        self._autoreset = autoreset
        self._use_bin_type = use_bin_type
        self._encoding = encoding
        self._unicode_errors = unicode_errors
        self._buffer = StringIO()
        if default is not None:
            if not callable(default):
                raise TypeError('default must be callable')
        self._default = default
        return

    def _pack(self, obj, nest_limit=DEFAULT_RECURSE_LIMIT, isinstance=isinstance):
        default_used = False
        while True:
            if nest_limit < 0:
                raise PackValueError('recursion limit exceeded')
            if obj is None:
                return self._buffer.write('\xc0')
            if isinstance(obj, bool):
                if obj:
                    return self._buffer.write('\xc3')
                return self._buffer.write('\xc2')
            if isinstance(obj, int_types):
                if 0 <= obj < 128:
                    return self._buffer.write(struct.pack('B', obj))
                if -32 <= obj < 0:
                    return self._buffer.write(struct.pack('b', obj))
                if 128 <= obj <= 255:
                    return self._buffer.write(struct.pack('BB', 204, obj))
                if -128 <= obj < 0:
                    return self._buffer.write(struct.pack('>Bb', 208, obj))
                if 255 < obj <= 65535:
                    return self._buffer.write(struct.pack('>BH', 205, obj))
                if -32768 <= obj < -128:
                    return self._buffer.write(struct.pack('>Bh', 209, obj))
                if 65535 < obj <= 4294967295:
                    return self._buffer.write(struct.pack('>BI', 206, obj))
                if -2147483648 <= obj < -32768:
                    return self._buffer.write(struct.pack('>Bi', 210, obj))
                if 4294967295 < obj <= 18446744073709551615L:
                    return self._buffer.write(struct.pack('>BQ', 207, obj))
                if -9223372036854775808L <= obj < -2147483648:
                    return self._buffer.write(struct.pack('>Bq', 211, obj))
                if not default_used and self._default is not None:
                    obj = self._default(obj)
                    default_used = True
                    continue
                raise PackValueError('Integer value out of range')
            if self._use_bin_type and isinstance(obj, bytes):
                n = len(obj)
                if n <= 255:
                    self._buffer.write(struct.pack('>BB', 196, n))
                elif n <= 65535:
                    self._buffer.write(struct.pack('>BH', 197, n))
                elif n <= 4294967295:
                    self._buffer.write(struct.pack('>BI', 198, n))
                else:
                    raise PackValueError('Bytes is too large')
                return self._buffer.write(obj)
            if isinstance(obj, (Unicode, bytes)):
                if isinstance(obj, Unicode):
                    if self._encoding is None:
                        raise TypeError("Can't encode unicode string: no encoding is specified")
                    obj = obj.encode(self._encoding, self._unicode_errors)
                n = len(obj)
                if n <= 31:
                    self._buffer.write(struct.pack('B', 160 + n))
                elif self._use_bin_type and n <= 255:
                    self._buffer.write(struct.pack('>BB', 217, n))
                elif n <= 65535:
                    self._buffer.write(struct.pack('>BH', 218, n))
                elif n <= 4294967295:
                    self._buffer.write(struct.pack('>BI', 219, n))
                else:
                    raise PackValueError('String is too large')
                return self._buffer.write(obj)
            if isinstance(obj, float):
                if self._use_float:
                    return self._buffer.write(struct.pack('>Bf', 202, obj))
                return self._buffer.write(struct.pack('>Bd', 203, obj))
            if isinstance(obj, ExtType):
                code = obj.code
                data = obj.data
                L = len(data)
                if L == 1:
                    self._buffer.write('\xd4')
                elif L == 2:
                    self._buffer.write('\xd5')
                elif L == 4:
                    self._buffer.write('\xd6')
                elif L == 8:
                    self._buffer.write('\xd7')
                elif L == 16:
                    self._buffer.write('\xd8')
                elif L <= 255:
                    self._buffer.write(struct.pack('>BB', 199, L))
                elif L <= 65535:
                    self._buffer.write(struct.pack('>BH', 200, L))
                else:
                    self._buffer.write(struct.pack('>BI', 201, L))
                self._buffer.write(struct.pack('b', code))
                self._buffer.write(data)
                return
            if isinstance(obj, (list, tuple)):
                n = len(obj)
                self._fb_pack_array_header(n)
                for i in range(n):
                    self._pack(obj[i], nest_limit - 1)

                return
            if isinstance(obj, dict):
                return self._fb_pack_map_pairs(len(obj), dict_iteritems(obj), nest_limit - 1)
            if not default_used and self._default is not None:
                obj = self._default(obj)
                default_used = 1
                continue
            raise TypeError('Cannot serialize %r' % obj)

        return

    def pack(self, obj):
        self._pack(obj)
        ret = self._buffer.getvalue()
        if self._autoreset:
            self._buffer = StringIO()
        elif USING_STRINGBUILDER:
            self._buffer = StringIO(ret)
        return ret

    def pack_map_pairs(self, pairs):
        self._fb_pack_map_pairs(len(pairs), pairs)
        ret = self._buffer.getvalue()
        if self._autoreset:
            self._buffer = StringIO()
        elif USING_STRINGBUILDER:
            self._buffer = StringIO(ret)
        return ret

    def pack_array_header(self, n):
        if n >= 4294967296:
            raise ValueError
        self._fb_pack_array_header(n)
        ret = self._buffer.getvalue()
        if self._autoreset:
            self._buffer = StringIO()
        elif USING_STRINGBUILDER:
            self._buffer = StringIO(ret)
        return ret

    def pack_map_header(self, n):
        if n >= 4294967296:
            raise ValueError
        self._fb_pack_map_header(n)
        ret = self._buffer.getvalue()
        if self._autoreset:
            self._buffer = StringIO()
        elif USING_STRINGBUILDER:
            self._buffer = StringIO(ret)
        return ret

    def pack_ext_type(self, typecode, data):
        if not isinstance(typecode, int):
            raise TypeError('typecode must have int type.')
        if not 0 <= typecode <= 127:
            raise ValueError('typecode should be 0-127')
        if not isinstance(data, bytes):
            raise TypeError('data must have bytes type')
        L = len(data)
        if L > 4294967295:
            raise ValueError('Too large data')
        if L == 1:
            self._buffer.write('\xd4')
        elif L == 2:
            self._buffer.write('\xd5')
        elif L == 4:
            self._buffer.write('\xd6')
        elif L == 8:
            self._buffer.write('\xd7')
        elif L == 16:
            self._buffer.write('\xd8')
        elif L <= 255:
            self._buffer.write('\xc7' + struct.pack('B', L))
        elif L <= 65535:
            self._buffer.write('\xc8' + struct.pack('>H', L))
        else:
            self._buffer.write('\xc9' + struct.pack('>I', L))
        self._buffer.write(struct.pack('B', typecode))
        self._buffer.write(data)

    def _fb_pack_array_header(self, n):
        if n <= 15:
            return self._buffer.write(struct.pack('B', 144 + n))
        if n <= 65535:
            return self._buffer.write(struct.pack('>BH', 220, n))
        if n <= 4294967295:
            return self._buffer.write(struct.pack('>BI', 221, n))
        raise PackValueError('Array is too large')

    def _fb_pack_map_header(self, n):
        if n <= 15:
            return self._buffer.write(struct.pack('B', 128 + n))
        if n <= 65535:
            return self._buffer.write(struct.pack('>BH', 222, n))
        if n <= 4294967295:
            return self._buffer.write(struct.pack('>BI', 223, n))
        raise PackValueError('Dict is too large')

    def _fb_pack_map_pairs(self, n, pairs, nest_limit=DEFAULT_RECURSE_LIMIT):
        self._fb_pack_map_header(n)
        for k, v in pairs:
            self._pack(k, nest_limit - 1)
            self._pack(v, nest_limit - 1)

    def bytes(self):
        return self._buffer.getvalue()

    def reset(self):
        self._buffer = StringIO()