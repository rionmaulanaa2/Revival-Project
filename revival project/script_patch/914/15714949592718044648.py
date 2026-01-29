# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/zipfile.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from six.moves import map
import six
import struct
import os
import time
import sys
import shutil
import binascii
import six_ex.moves.cStringIO
import stat
import io
import re
try:
    import zlib
    crc32 = zlib.crc32
except ImportError:
    zlib = None
    crc32 = binascii.crc32

__all__ = ['BadZipfile', 'error', 'ZIP_STORED', 'ZIP_DEFLATED', 'is_zipfile',
 'ZipInfo', 'ZipFile', 'PyZipFile', 'LargeZipFile']

class BadZipfile(Exception):
    pass


class LargeZipFile(Exception):
    pass


error = BadZipfile
ZIP64_LIMIT = (1 << 31) - 1
ZIP_FILECOUNT_LIMIT = 1 << 16
ZIP_MAX_COMMENT = (1 << 16) - 1
ZIP_STORED = 0
ZIP_DEFLATED = 8
structEndArchive = '<4s4H2LH'
stringEndArchive = 'PK\x05\x06'
sizeEndCentDir = struct.calcsize(structEndArchive)
_ECD_SIGNATURE = 0
_ECD_DISK_NUMBER = 1
_ECD_DISK_START = 2
_ECD_ENTRIES_THIS_DISK = 3
_ECD_ENTRIES_TOTAL = 4
_ECD_SIZE = 5
_ECD_OFFSET = 6
_ECD_COMMENT_SIZE = 7
_ECD_COMMENT = 8
_ECD_LOCATION = 9
structCentralDir = '<4s4B4HL2L5H2L'
stringCentralDir = 'PK\x01\x02'
sizeCentralDir = struct.calcsize(structCentralDir)
_CD_SIGNATURE = 0
_CD_CREATE_VERSION = 1
_CD_CREATE_SYSTEM = 2
_CD_EXTRACT_VERSION = 3
_CD_EXTRACT_SYSTEM = 4
_CD_FLAG_BITS = 5
_CD_COMPRESS_TYPE = 6
_CD_TIME = 7
_CD_DATE = 8
_CD_CRC = 9
_CD_COMPRESSED_SIZE = 10
_CD_UNCOMPRESSED_SIZE = 11
_CD_FILENAME_LENGTH = 12
_CD_EXTRA_FIELD_LENGTH = 13
_CD_COMMENT_LENGTH = 14
_CD_DISK_NUMBER_START = 15
_CD_INTERNAL_FILE_ATTRIBUTES = 16
_CD_EXTERNAL_FILE_ATTRIBUTES = 17
_CD_LOCAL_HEADER_OFFSET = 18
structFileHeader = '<4s2B4HL2L2H'
stringFileHeader = 'PK\x03\x04'
sizeFileHeader = struct.calcsize(structFileHeader)
_FH_SIGNATURE = 0
_FH_EXTRACT_VERSION = 1
_FH_EXTRACT_SYSTEM = 2
_FH_GENERAL_PURPOSE_FLAG_BITS = 3
_FH_COMPRESSION_METHOD = 4
_FH_LAST_MOD_TIME = 5
_FH_LAST_MOD_DATE = 6
_FH_CRC = 7
_FH_COMPRESSED_SIZE = 8
_FH_UNCOMPRESSED_SIZE = 9
_FH_FILENAME_LENGTH = 10
_FH_EXTRA_FIELD_LENGTH = 11
structEndArchive64Locator = '<4sLQL'
stringEndArchive64Locator = 'PK\x06\x07'
sizeEndCentDir64Locator = struct.calcsize(structEndArchive64Locator)
structEndArchive64 = '<4sQ2H2L4Q'
stringEndArchive64 = 'PK\x06\x06'
sizeEndCentDir64 = struct.calcsize(structEndArchive64)
_CD64_SIGNATURE = 0
_CD64_DIRECTORY_RECSIZE = 1
_CD64_CREATE_VERSION = 2
_CD64_EXTRACT_VERSION = 3
_CD64_DISK_NUMBER = 4
_CD64_DISK_NUMBER_START = 5
_CD64_NUMBER_ENTRIES_THIS_DISK = 6
_CD64_NUMBER_ENTRIES_TOTAL = 7
_CD64_DIRECTORY_SIZE = 8
_CD64_OFFSET_START_CENTDIR = 9

def _check_zipfile(fp):
    try:
        if _EndRecData(fp):
            return True
    except IOError:
        pass

    return False


def is_zipfile--- This code section failed: ---

 151       0  LOAD_GLOBAL           0  'False'
           3  STORE_FAST            1  'result'

 152       6  SETUP_EXCEPT         67  'to 76'

 153       9  LOAD_GLOBAL           1  'hasattr'
          12  LOAD_GLOBAL           1  'hasattr'
          15  CALL_FUNCTION_2       2 
          18  POP_JUMP_IF_FALSE    39  'to 39'

 154      21  LOAD_GLOBAL           2  '_check_zipfile'
          24  LOAD_CONST            2  'fp'
          27  LOAD_FAST             0  'filename'
          30  CALL_FUNCTION_256   256 
          33  STORE_FAST            1  'result'
          36  JUMP_FORWARD         33  'to 72'

 156      39  LOAD_GLOBAL           3  'open'
          42  LOAD_GLOBAL           3  'open'
          45  CALL_FUNCTION_2       2 
          48  SETUP_WITH           19  'to 70'
          51  STORE_FAST            2  'fp'

 157      54  LOAD_GLOBAL           2  '_check_zipfile'
          57  LOAD_FAST             2  'fp'
          60  CALL_FUNCTION_1       1 
          63  STORE_FAST            1  'result'
          66  POP_BLOCK        
          67  LOAD_CONST            0  ''
        70_0  COME_FROM_WITH           '48'
          70  WITH_CLEANUP     
          71  END_FINALLY      
        72_0  COME_FROM                '36'
          72  POP_BLOCK        
          73  JUMP_FORWARD         17  'to 93'
        76_0  COME_FROM                '6'

 158      76  DUP_TOP          
          77  LOAD_GLOBAL           4  'IOError'
          80  COMPARE_OP           10  'exception-match'
          83  POP_JUMP_IF_FALSE    92  'to 92'
          86  POP_TOP          
          87  POP_TOP          
          88  POP_TOP          

 159      89  JUMP_FORWARD          1  'to 93'
          92  END_FINALLY      
        93_0  COME_FROM                '92'
        93_1  COME_FROM                '73'

 160      93  LOAD_FAST             1  'result'
          96  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 15


def _EndRecData64(fpin, offset, endrec):
    try:
        fpin.seek(offset - sizeEndCentDir64Locator, 2)
    except IOError:
        return endrec

    data = fpin.read(sizeEndCentDir64Locator)
    sig, diskno, reloff, disks = struct.unpack(structEndArchive64Locator, data)
    if sig != stringEndArchive64Locator:
        return endrec
    if diskno != 0 or disks != 1:
        raise BadZipfile('zipfiles that span multiple disks are not supported')
    fpin.seek(0, 0)
    fpin.seek(offset - sizeEndCentDir64Locator - sizeEndCentDir64, 2)
    data = fpin.read(sizeEndCentDir64)
    sig, sz, create_version, read_version, disk_num, disk_dir, dircount, dircount2, dirsize, diroffset = struct.unpack(structEndArchive64, data)
    if sig != stringEndArchive64:
        return endrec
    endrec[_ECD_SIGNATURE] = sig
    endrec[_ECD_DISK_NUMBER] = disk_num
    endrec[_ECD_DISK_START] = disk_dir
    endrec[_ECD_ENTRIES_THIS_DISK] = dircount
    endrec[_ECD_ENTRIES_TOTAL] = dircount2
    endrec[_ECD_SIZE] = dirsize
    endrec[_ECD_OFFSET] = diroffset
    return endrec


def _EndRecData(fpin):
    fpin.seek(0, 2)
    filesize = fpin.tell()
    try:
        fpin.seek(-sizeEndCentDir, 2)
    except IOError:
        return None

    data = fpin.read()
    if data[0:4] == stringEndArchive and data[-2:] == '\x00\x00':
        endrec = struct.unpack(structEndArchive, data)
        endrec = list(endrec)
        endrec.append('')
        endrec.append(filesize - sizeEndCentDir)
        return _EndRecData64(fpin, -sizeEndCentDir, endrec)
    else:
        maxCommentStart = max(filesize - 65536 - sizeEndCentDir, 0)
        fpin.seek(maxCommentStart, 0)
        data = fpin.read()
        start = data.rfind(stringEndArchive)
        if start >= 0:
            recData = data[start:start + sizeEndCentDir]
            endrec = list(struct.unpack(structEndArchive, recData))
            commentSize = endrec[_ECD_COMMENT_SIZE]
            comment = data[start + sizeEndCentDir:start + sizeEndCentDir + commentSize]
            endrec.append(comment)
            endrec.append(maxCommentStart + start)
            return _EndRecData64(fpin, maxCommentStart + start - filesize, endrec)
        return None


class ZipInfo(object):
    __slots__ = ('orig_filename', 'filename', 'date_time', 'compress_type', 'comment',
                 'extra', 'create_system', 'create_version', 'extract_version', 'reserved',
                 'flag_bits', 'volume', 'internal_attr', 'external_attr', 'header_offset',
                 'CRC', 'compress_size', 'file_size', '_raw_time')

    def __init__(self, filename='NoName', date_time=(1980, 1, 1, 0, 0, 0)):
        self.orig_filename = filename
        null_byte = filename.find(six.int2byte(0))
        if null_byte >= 0:
            filename = filename[0:null_byte]
        if os.sep != '/' and os.sep in filename:
            filename = filename.replace(os.sep, '/')
        self.filename = filename
        self.date_time = date_time
        if date_time[0] < 1980:
            raise ValueError('ZIP does not support timestamps before 1980')
        self.compress_type = ZIP_STORED
        self.comment = ''
        self.extra = ''
        if sys.platform == 'win32':
            self.create_system = 0
        else:
            self.create_system = 3
        self.create_version = 20
        self.extract_version = 20
        self.reserved = 0
        self.flag_bits = 0
        self.volume = 0
        self.internal_attr = 0
        self.external_attr = 0

    def FileHeader(self):
        dt = self.date_time
        dosdate = dt[0] - 1980 << 9 | dt[1] << 5 | dt[2]
        dostime = dt[3] << 11 | dt[4] << 5 | dt[5] // 2
        if self.flag_bits & 8:
            CRC = compress_size = file_size = 0
        else:
            CRC = self.CRC
            compress_size = self.compress_size
            file_size = self.file_size
        extra = self.extra
        if file_size > ZIP64_LIMIT or compress_size > ZIP64_LIMIT:
            fmt = '<HHQQ'
            extra = extra + struct.pack(fmt, 1, struct.calcsize(fmt) - 4, file_size, compress_size)
            file_size = 4294967295
            compress_size = 4294967295
            self.extract_version = max(45, self.extract_version)
            self.create_version = max(45, self.extract_version)
        filename, flag_bits = self._encodeFilenameFlags()
        header = struct.pack(structFileHeader, stringFileHeader, self.extract_version, self.reserved, flag_bits, self.compress_type, dostime, dosdate, CRC, compress_size, file_size, len(filename), len(extra))
        return header + filename + extra

    def _encodeFilenameFlags(self):
        if isinstance(self.filename, six.text_type):
            try:
                return (
                 self.filename.encode('ascii'), self.flag_bits)
            except UnicodeEncodeError:
                return (
                 self.filename.encode('utf-8'), self.flag_bits | 2048)

        else:
            return (
             self.filename, self.flag_bits)

    def _decodeFilename(self):
        if self.flag_bits & 2048:
            return self.filename.decode('utf-8')
        else:
            return self.filename

    def _decodeExtra(self):
        extra = self.extra
        unpack = struct.unpack
        while extra:
            tp, ln = unpack('<HH', extra[:4])
            if tp == 1:
                if ln >= 24:
                    counts = unpack('<QQQ', extra[4:28])
                elif ln == 16:
                    counts = unpack('<QQ', extra[4:20])
                elif ln == 8:
                    counts = unpack('<Q', extra[4:12])
                elif ln == 0:
                    counts = ()
                else:
                    raise RuntimeError('Corrupt extra field %s' % (ln,))
                idx = 0
                if self.file_size in (18446744073709551615L, 4294967295):
                    self.file_size = counts[idx]
                    idx += 1
                if self.compress_size == 4294967295:
                    self.compress_size = counts[idx]
                    idx += 1
                if self.header_offset == 4294967295:
                    old = self.header_offset
                    self.header_offset = counts[idx]
                    idx += 1
            extra = extra[ln + 4:]


class _ZipDecrypter():

    def _GenerateCRCTable():
        poly = 3988292384
        table = [0] * 256
        for i in range(256):
            crc = i
            for j in range(8):
                if crc & 1:
                    crc = crc >> 1 & 2147483647 ^ poly
                else:
                    crc = crc >> 1 & 2147483647

            table[i] = crc

        return table

    crctable = _GenerateCRCTable()

    def _crc32(self, ch, crc):
        return crc >> 8 & 16777215 ^ self.crctable[(crc ^ ord(ch)) & 255]

    def __init__(self, pwd):
        self.key0 = 305419896
        self.key1 = 591751049
        self.key2 = 878082192
        for p in pwd:
            self._UpdateKeys(p)

    def _UpdateKeys(self, c):
        self.key0 = self._crc32(c, self.key0)
        self.key1 = self.key1 + (self.key0 & 255) & 4294967295
        self.key1 = self.key1 * 134775813 + 1 & 4294967295
        self.key2 = self._crc32(six.int2byte(self.key1 >> 24 & 255), self.key2)

    def __call__(self, c):
        c = ord(c)
        k = self.key2 | 2
        c = c ^ k * (k ^ 1) >> 8 & 255
        c = six.int2byte(c)
        self._UpdateKeys(c)
        return c


class ZipExtFile(io.BufferedIOBase):
    MAX_N = 1 << 30
    MIN_READ_SIZE = 4096
    PATTERN = re.compile('^(?P<chunk>[^\\r\\n]+)|(?P<newline>\\n|\\r\\n?)')

    def __init__(self, fileobj, mode, zipinfo, decrypter=None):
        self._fileobj = fileobj
        self._decrypter = decrypter
        self._compress_type = zipinfo.compress_type
        self._compress_size = zipinfo.compress_size
        self._compress_left = zipinfo.compress_size
        if self._compress_type == ZIP_DEFLATED:
            self._decompressor = zlib.decompressobj(-15)
        self._unconsumed = ''
        self._readbuffer = ''
        self._offset = 0
        self._universal = 'U' in mode
        self.newlines = None
        if self._decrypter is not None:
            self._compress_left -= 12
        self.mode = mode
        self.name = zipinfo.filename
        if hasattr(zipinfo, 'CRC'):
            self._expected_crc = zipinfo.CRC
            self._running_crc = crc32('') & 4294967295
        else:
            self._expected_crc = None
        return

    def readline(self, limit=-1):
        if not self._universal and limit < 0:
            i = self._readbuffer.find('\n', self._offset) + 1
            if i > 0:
                line = self._readbuffer[self._offset:i]
                self._offset = i
                return line
        if not self._universal:
            return io.BufferedIOBase.readline(self, limit)
        else:
            line = ''
            while limit < 0 or len(line) < limit:
                readahead = self.peek(2)
                if readahead == '':
                    return line
                match = self.PATTERN.search(readahead)
                newline = match.group('newline')
                if newline is not None:
                    if self.newlines is None:
                        self.newlines = []
                    if newline not in self.newlines:
                        self.newlines.append(newline)
                    self._offset += len(newline)
                    return line + '\n'
                chunk = match.group('chunk')
                if limit >= 0:
                    chunk = chunk[:limit - len(line)]
                self._offset += len(chunk)
                line += chunk

            return line

    def peek(self, n=1):
        if n > len(self._readbuffer) - self._offset:
            chunk = self.read(n)
            self._offset -= len(chunk)
        return self._readbuffer[self._offset:self._offset + 512]

    def readable(self):
        return True

    def read(self, n=-1):
        buf = ''
        if n is None:
            n = -1
        while True:
            if n < 0:
                data = self.read1(n)
            elif n > len(buf):
                data = self.read1(n - len(buf))
            else:
                return buf
            if len(data) == 0:
                return buf
            buf += data

        return

    def _update_crc(self, newdata, eof):
        if self._expected_crc is None:
            return
        else:
            self._running_crc = crc32(newdata, self._running_crc) & 4294967295
            if eof and self._running_crc != self._expected_crc:
                raise BadZipfile('Bad CRC-32 for file %r' % self.name)
            return

    def read1(self, n):
        if n < 0 or n is None:
            n = self.MAX_N
        len_readbuffer = len(self._readbuffer) - self._offset
        if self._compress_left > 0 and n > len_readbuffer + len(self._unconsumed):
            nbytes = n - len_readbuffer - len(self._unconsumed)
            nbytes = max(nbytes, self.MIN_READ_SIZE)
            nbytes = min(nbytes, self._compress_left)
            data = self._fileobj.read(nbytes)
            self._compress_left -= len(data)
            if data and self._decrypter is not None:
                data = ''.join(map(self._decrypter, data))
            if self._compress_type == ZIP_STORED:
                self._update_crc(data, eof=self._compress_left == 0)
                self._readbuffer = self._readbuffer[self._offset:] + data
                self._offset = 0
            else:
                self._unconsumed += data
        if len(self._unconsumed) > 0 and n > len_readbuffer and self._compress_type == ZIP_DEFLATED:
            data = self._decompressor.decompress(self._unconsumed, max(n - len_readbuffer, self.MIN_READ_SIZE))
            self._unconsumed = self._decompressor.unconsumed_tail
            eof = len(self._unconsumed) == 0 and self._compress_left == 0
            if eof:
                data += self._decompressor.flush()
            self._update_crc(data, eof=eof)
            self._readbuffer = self._readbuffer[self._offset:] + data
            self._offset = 0
        data = self._readbuffer[self._offset:self._offset + n]
        self._offset += len(data)
        return data


class ZipFile():
    fp = None

    def __init__(self, file, mode='r', compression=ZIP_STORED, allowZip64=False):
        if mode not in ('r', 'w', 'a'):
            raise RuntimeError('ZipFile() requires mode "r", "w", or "a"')
        if compression == ZIP_STORED:
            pass
        elif compression == ZIP_DEFLATED:
            if not zlib:
                raise RuntimeError('Compression requires the (missing) zlib module')
        else:
            raise RuntimeError('That compression method is not supported')
        self._allowZip64 = allowZip64
        self._didModify = False
        self.debug = 0
        self.NameToInfo = {}
        self.filelist = []
        self.compression = compression
        self.mode = key = mode.replace('b', '')[0]
        self.pwd = None
        self.comment = ''
        if isinstance(file, six.string_types):
            self._filePassed = 0
            self.filename = file
            modeDict = {'r': 'rb','w': 'wb','a': 'r+b'}
            try:
                self.fp = open(file, modeDict[mode])
            except IOError:
                if mode == 'a':
                    mode = key = 'w'
                    self.fp = open(file, modeDict[mode])
                else:
                    raise

        else:
            self._filePassed = 1
            self.fp = file
            self.filename = getattr(file, 'name', None)
        if key == 'r':
            self._GetContents()
        elif key == 'w':
            self._didModify = True
        elif key == 'a':
            try:
                self._RealGetContents()
                self.fp.seek(self.start_dir, 0)
            except BadZipfile:
                self.fp.seek(0, 2)
                self._didModify = True

        else:
            if not self._filePassed:
                self.fp.close()
                self.fp = None
            raise RuntimeError('Mode must be "r", "w" or "a"')
        return

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def _GetContents(self):
        try:
            self._RealGetContents()
        except BadZipfile:
            if not self._filePassed:
                self.fp.close()
                self.fp = None
            raise

        return

    def _RealGetContents(self):
        fp = self.fp
        try:
            endrec = _EndRecData(fp)
        except IOError:
            raise BadZipfile('File is not a zip file')

        if not endrec:
            raise BadZipfile('File is not a zip file')
        if self.debug > 1:
            print(endrec)
        size_cd = endrec[_ECD_SIZE]
        offset_cd = endrec[_ECD_OFFSET]
        self.comment = endrec[_ECD_COMMENT]
        concat = endrec[_ECD_LOCATION] - size_cd - offset_cd
        if endrec[_ECD_SIGNATURE] == stringEndArchive64:
            concat -= sizeEndCentDir64 + sizeEndCentDir64Locator
        if self.debug > 2:
            inferred = concat + offset_cd
            print('given, inferred, offset', offset_cd, inferred, concat)
        self.start_dir = offset_cd + concat
        fp.seek(self.start_dir, 0)
        data = fp.read(size_cd)
        fp = six_ex.moves.cStringIO.StringIO(data)
        total = 0
        while total < size_cd:
            centdir = fp.read(sizeCentralDir)
            if centdir[0:4] != stringCentralDir:
                raise BadZipfile('Bad magic number for central directory')
            centdir = struct.unpack(structCentralDir, centdir)
            if self.debug > 2:
                print(centdir)
            filename = fp.read(centdir[_CD_FILENAME_LENGTH])
            x = ZipInfo(filename)
            x.extra = fp.read(centdir[_CD_EXTRA_FIELD_LENGTH])
            x.comment = fp.read(centdir[_CD_COMMENT_LENGTH])
            x.header_offset = centdir[_CD_LOCAL_HEADER_OFFSET]
            x.create_version, x.create_system, x.extract_version, x.reserved, x.flag_bits, x.compress_type, t, d, x.CRC, x.compress_size, x.file_size = centdir[1:12]
            x.volume, x.internal_attr, x.external_attr = centdir[15:18]
            x._raw_time = t
            x.date_time = ((d >> 9) + 1980, d >> 5 & 15, d & 31,
             t >> 11, t >> 5 & 63, (t & 31) * 2)
            x._decodeExtra()
            x.header_offset = x.header_offset + concat
            x.filename = x._decodeFilename()
            self.filelist.append(x)
            self.NameToInfo[x.filename] = x
            total = total + sizeCentralDir + centdir[_CD_FILENAME_LENGTH] + centdir[_CD_EXTRA_FIELD_LENGTH] + centdir[_CD_COMMENT_LENGTH]
            if self.debug > 2:
                print('total', total)

    def namelist(self):
        l = []
        for data in self.filelist:
            l.append(data.filename)

        return l

    def infolist(self):
        return self.filelist

    def printdir(self):
        print('%-46s %19s %12s' % ('File Name', 'Modified    ', 'Size'))
        for zinfo in self.filelist:
            date = '%d-%02d-%02d %02d:%02d:%02d' % zinfo.date_time[:6]
            print('%-46s %s %12d' % (zinfo.filename, date, zinfo.file_size))

    def testzip(self):
        chunk_size = 1048576
        for zinfo in self.filelist:
            try:
                f = self.open(zinfo.filename, 'r')
                while f.read(chunk_size):
                    pass

            except BadZipfile:
                return zinfo.filename

    def getinfo(self, name):
        info = self.NameToInfo.get(name)
        if info is None:
            raise KeyError('There is no item named %r in the archive' % name)
        return info

    def setpassword(self, pwd):
        self.pwd = pwd

    def read(self, name, pwd=None):
        return self.open(name, 'r', pwd).read()

    def open(self, name, mode='r', pwd=None):
        if mode not in ('r', 'U', 'rU'):
            raise RuntimeError('open() requires mode "r", "U", or "rU"')
        if not self.fp:
            raise RuntimeError('Attempt to read ZIP archive that was already closed')
        if self._filePassed:
            zef_file = self.fp
        else:
            zef_file = open(self.filename, 'rb')
        if isinstance(name, ZipInfo):
            zinfo = name
        else:
            zinfo = self.getinfo(name)
        zef_file.seek(zinfo.header_offset, 0)
        fheader = zef_file.read(sizeFileHeader)
        if fheader[0:4] != stringFileHeader:
            raise BadZipfile('Bad magic number for file header')
        fheader = struct.unpack(structFileHeader, fheader)
        fname = zef_file.read(fheader[_FH_FILENAME_LENGTH])
        if fheader[_FH_EXTRA_FIELD_LENGTH]:
            zef_file.read(fheader[_FH_EXTRA_FIELD_LENGTH])
        if fname != zinfo.orig_filename:
            raise BadZipfile('File name in directory "%s" and header "%s" differ.' % (
             zinfo.orig_filename, fname))
        is_encrypted = zinfo.flag_bits & 1
        zd = None
        if is_encrypted:
            if not pwd:
                pwd = self.pwd
            if not pwd:
                raise RuntimeError('File %s is encrypted, password required for extraction' % name)
            zd = _ZipDecrypter(pwd)
            bytes = zef_file.read(12)
            h = list(map(zd, bytes[0:12]))
            if zinfo.flag_bits & 8:
                check_byte = zinfo._raw_time >> 8 & 255
            else:
                check_byte = zinfo.CRC >> 24 & 255
            if ord(h[11]) != check_byte:
                raise RuntimeError('Bad password for file', name)
        return ZipExtFile(zef_file, mode, zinfo, zd)

    def extract(self, member, path=None, pwd=None):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)
        if path is None:
            path = os.getcwd()
        return self._extract_member(member, path, pwd)

    def extractall(self, path=None, members=None, pwd=None):
        if members is None:
            members = self.namelist()
        for zipinfo in members:
            self.extract(zipinfo, path, pwd)

        return

    def _extract_member(self, member, targetpath, pwd):
        if targetpath[-1:] in (os.path.sep, os.path.altsep) and len(os.path.splitdrive(targetpath)[1]) > 1:
            targetpath = targetpath[:-1]
        if member.filename[0] == '/':
            targetpath = os.path.join(targetpath, member.filename[1:])
        else:
            targetpath = os.path.join(targetpath, member.filename)
        targetpath = os.path.normpath(targetpath)
        upperdirs = os.path.dirname(targetpath)
        if upperdirs and not os.path.exists(upperdirs):
            os.makedirs(upperdirs)
        if member.filename[-1] == '/':
            if not os.path.isdir(targetpath):
                os.mkdir(targetpath)
            return targetpath
        source = self.open(member, pwd=pwd)
        target = open(targetpath, 'wb')
        shutil.copyfileobj(source, target)
        source.close()
        target.close()
        return targetpath

    def _writecheck(self, zinfo):
        if zinfo.filename in self.NameToInfo:
            if self.debug:
                print('Duplicate name:', zinfo.filename)
        if self.mode not in ('w', 'a'):
            raise RuntimeError('write() requires mode "w" or "a"')
        if not self.fp:
            raise RuntimeError('Attempt to write ZIP archive that was already closed')
        if zinfo.compress_type == ZIP_DEFLATED and not zlib:
            raise RuntimeError('Compression requires the (missing) zlib module')
        if zinfo.compress_type not in (ZIP_STORED, ZIP_DEFLATED):
            raise RuntimeError('That compression method is not supported')
        if zinfo.file_size > ZIP64_LIMIT:
            if not self._allowZip64:
                raise LargeZipFile('Filesize would require ZIP64 extensions')
        if zinfo.header_offset > ZIP64_LIMIT:
            if not self._allowZip64:
                raise LargeZipFile('Zipfile size would require ZIP64 extensions')

    def write(self, filename, arcname=None, compress_type=None):
        if not self.fp:
            raise RuntimeError('Attempt to write to ZIP archive that was already closed')
        st = os.stat(filename)
        isdir = stat.S_ISDIR(st.st_mode)
        mtime = time.localtime(st.st_mtime)
        date_time = mtime[0:6]
        if arcname is None:
            arcname = filename
        arcname = os.path.normpath(os.path.splitdrive(arcname)[1])
        while arcname[0] in (os.sep, os.altsep):
            arcname = arcname[1:]

        if isdir:
            arcname += '/'
        zinfo = ZipInfo(arcname, date_time)
        zinfo.external_attr = (st[0] & 65535) << 16
        if compress_type is None:
            zinfo.compress_type = self.compression
        else:
            zinfo.compress_type = compress_type
        zinfo.file_size = st.st_size
        zinfo.flag_bits = 0
        zinfo.header_offset = self.fp.tell()
        self._writecheck(zinfo)
        self._didModify = True
        if isdir:
            zinfo.file_size = 0
            zinfo.compress_size = 0
            zinfo.CRC = 0
            self.filelist.append(zinfo)
            self.NameToInfo[zinfo.filename] = zinfo
            self.fp.write(zinfo.FileHeader())
            return
        else:
            with open(filename, 'rb') as fp:
                zinfo.CRC = CRC = 0
                zinfo.compress_size = compress_size = 0
                zinfo.file_size = file_size = 0
                self.fp.write(zinfo.FileHeader())
                if zinfo.compress_type == ZIP_DEFLATED:
                    cmpr = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15)
                else:
                    cmpr = None
                while 1:
                    buf = fp.read(8192)
                    if not buf:
                        break
                    file_size = file_size + len(buf)
                    CRC = crc32(buf, CRC) & 4294967295
                    if cmpr:
                        buf = cmpr.compress(buf)
                        compress_size = compress_size + len(buf)
                    self.fp.write(buf)

            if cmpr:
                buf = cmpr.flush()
                compress_size = compress_size + len(buf)
                self.fp.write(buf)
                zinfo.compress_size = compress_size
            else:
                zinfo.compress_size = file_size
            zinfo.CRC = CRC
            zinfo.file_size = file_size
            position = self.fp.tell()
            self.fp.seek(zinfo.header_offset + 14, 0)
            self.fp.write(struct.pack('<LLL', zinfo.CRC, zinfo.compress_size, zinfo.file_size))
            self.fp.seek(position, 0)
            self.filelist.append(zinfo)
            self.NameToInfo[zinfo.filename] = zinfo
            return

    def writestr(self, zinfo_or_arcname, bytes, compress_type=None):
        if not isinstance(zinfo_or_arcname, ZipInfo):
            zinfo = ZipInfo(filename=zinfo_or_arcname, date_time=time.localtime(time.time())[:6])
            zinfo.compress_type = self.compression
            zinfo.external_attr = 25165824
        else:
            zinfo = zinfo_or_arcname
        if not self.fp:
            raise RuntimeError('Attempt to write to ZIP archive that was already closed')
        if compress_type is not None:
            zinfo.compress_type = compress_type
        zinfo.file_size = len(bytes)
        zinfo.header_offset = self.fp.tell()
        self._writecheck(zinfo)
        self._didModify = True
        zinfo.CRC = crc32(bytes) & 4294967295
        if zinfo.compress_type == ZIP_DEFLATED:
            co = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15)
            bytes = co.compress(bytes) + co.flush()
            zinfo.compress_size = len(bytes)
        else:
            zinfo.compress_size = zinfo.file_size
        zinfo.header_offset = self.fp.tell()
        self.fp.write(zinfo.FileHeader())
        self.fp.write(bytes)
        self.fp.flush()
        if zinfo.flag_bits & 8:
            self.fp.write(struct.pack('<LLL', zinfo.CRC, zinfo.compress_size, zinfo.file_size))
        self.filelist.append(zinfo)
        self.NameToInfo[zinfo.filename] = zinfo
        return

    def __del__(self):
        self.close()

    def close(self):
        if self.fp is None:
            return
        else:
            if self.mode in ('w', 'a') and self._didModify:
                count = 0
                pos1 = self.fp.tell()
                for zinfo in self.filelist:
                    count = count + 1
                    dt = zinfo.date_time
                    dosdate = dt[0] - 1980 << 9 | dt[1] << 5 | dt[2]
                    dostime = dt[3] << 11 | dt[4] << 5 | dt[5] // 2
                    extra = []
                    if zinfo.file_size > ZIP64_LIMIT or zinfo.compress_size > ZIP64_LIMIT:
                        extra.append(zinfo.file_size)
                        extra.append(zinfo.compress_size)
                        file_size = 4294967295
                        compress_size = 4294967295
                    else:
                        file_size = zinfo.file_size
                        compress_size = zinfo.compress_size
                    if zinfo.header_offset > ZIP64_LIMIT:
                        extra.append(zinfo.header_offset)
                        header_offset = 4294967295
                    else:
                        header_offset = zinfo.header_offset
                    extra_data = zinfo.extra
                    if extra:
                        extra_data = struct.pack(('<HH' + 'Q' * len(extra)), 1, (8 * len(extra)), *extra) + extra_data
                        extract_version = max(45, zinfo.extract_version)
                        create_version = max(45, zinfo.create_version)
                    else:
                        extract_version = zinfo.extract_version
                        create_version = zinfo.create_version
                    try:
                        filename, flag_bits = zinfo._encodeFilenameFlags()
                        centdir = struct.pack(structCentralDir, stringCentralDir, create_version, zinfo.create_system, extract_version, zinfo.reserved, flag_bits, zinfo.compress_type, dostime, dosdate, zinfo.CRC, compress_size, file_size, len(filename), len(extra_data), len(zinfo.comment), 0, zinfo.internal_attr, zinfo.external_attr, header_offset)
                    except DeprecationWarning:
                        print((structCentralDir,
                         stringCentralDir, create_version,
                         zinfo.create_system, extract_version, zinfo.reserved,
                         zinfo.flag_bits, zinfo.compress_type, dostime, dosdate,
                         zinfo.CRC, compress_size, file_size,
                         len(zinfo.filename), len(extra_data), len(zinfo.comment),
                         0, zinfo.internal_attr, zinfo.external_attr,
                         header_offset), file=sys.stderr)
                        raise

                    self.fp.write(centdir)
                    self.fp.write(filename)
                    self.fp.write(extra_data)
                    self.fp.write(zinfo.comment)

                pos2 = self.fp.tell()
                centDirCount = count
                centDirSize = pos2 - pos1
                centDirOffset = pos1
                if centDirCount >= ZIP_FILECOUNT_LIMIT or centDirOffset > ZIP64_LIMIT or centDirSize > ZIP64_LIMIT:
                    zip64endrec = struct.pack(structEndArchive64, stringEndArchive64, 44, 45, 45, 0, 0, centDirCount, centDirCount, centDirSize, centDirOffset)
                    self.fp.write(zip64endrec)
                    zip64locrec = struct.pack(structEndArchive64Locator, stringEndArchive64Locator, 0, pos2, 1)
                    self.fp.write(zip64locrec)
                    centDirCount = min(centDirCount, 65535)
                    centDirSize = min(centDirSize, 4294967295)
                    centDirOffset = min(centDirOffset, 4294967295)
                if len(self.comment) >= ZIP_MAX_COMMENT:
                    if self.debug > 0:
                        msg = 'Archive comment is too long; truncating to %d bytes' % ZIP_MAX_COMMENT
                    self.comment = self.comment[:ZIP_MAX_COMMENT]
                endrec = struct.pack(structEndArchive, stringEndArchive, 0, 0, centDirCount, centDirCount, centDirSize, centDirOffset, len(self.comment))
                self.fp.write(endrec)
                self.fp.write(self.comment)
                self.fp.flush()
            if not self._filePassed:
                self.fp.close()
            self.fp = None
            return


class PyZipFile(ZipFile):

    def writepy(self, pathname, basename=''):
        dir, name = os.path.split(pathname)
        if os.path.isdir(pathname):
            initname = os.path.join(pathname, '__init__.py')
            if os.path.isfile(initname):
                if basename:
                    basename = '%s/%s' % (basename, name)
                else:
                    basename = name
                if self.debug:
                    print('Adding package in', pathname, 'as', basename)
                fname, arcname = self._get_codename(initname[0:-3], basename)
                if self.debug:
                    print('Adding', arcname)
                self.write(fname, arcname)
                dirlist = os.listdir(pathname)
                dirlist.remove('__init__.py')
                for filename in dirlist:
                    path = os.path.join(pathname, filename)
                    root, ext = os.path.splitext(filename)
                    if os.path.isdir(path):
                        if os.path.isfile(os.path.join(path, '__init__.py')):
                            self.writepy(path, basename)
                    elif ext == '.py':
                        fname, arcname = self._get_codename(path[0:-3], basename)
                        if self.debug:
                            print('Adding', arcname)
                        self.write(fname, arcname)

            else:
                if self.debug:
                    print('Adding files from directory', pathname)
                for filename in os.listdir(pathname):
                    path = os.path.join(pathname, filename)
                    root, ext = os.path.splitext(filename)
                    if ext == '.py':
                        fname, arcname = self._get_codename(path[0:-3], basename)
                        if self.debug:
                            print('Adding', arcname)
                        self.write(fname, arcname)

        else:
            if pathname[-3:] != '.py':
                raise RuntimeError('Files added with writepy() must end with ".py"')
            fname, arcname = self._get_codename(pathname[0:-3], basename)
            if self.debug:
                print('Adding file', arcname)
            self.write(fname, arcname)

    def _get_codename(self, pathname, basename):
        file_py = pathname + '.py'
        file_pyc = pathname + '.pyc'
        file_pyo = pathname + '.pyo'
        if os.path.isfile(file_pyo) and os.stat(file_pyo).st_mtime >= os.stat(file_py).st_mtime:
            fname = file_pyo
        elif not os.path.isfile(file_pyc) or os.stat(file_pyc).st_mtime < os.stat(file_py).st_mtime:
            import py_compile
            if self.debug:
                print('Compiling', file_py)
            try:
                py_compile.compile(file_py, file_pyc, None, True)
            except py_compile.PyCompileError as err:
                print(err.msg)

            fname = file_pyc
        else:
            fname = file_pyc
        archivename = os.path.split(fname)[1]
        if basename:
            archivename = '%s/%s' % (basename, archivename)
        return (fname, archivename)


def main--- This code section failed: ---

1364       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'textwrap'
           9  STORE_FAST            1  'textwrap'

1365      12  LOAD_FAST             1  'textwrap'
          15  LOAD_ATTR             1  'dedent'

1371      18  LOAD_CONST            2  '        Usage:\n            zipfile.py -l zipfile.zip        # Show listing of a zipfile\n            zipfile.py -t zipfile.zip        # Test if a zipfile is valid\n            zipfile.py -e zipfile.zip target # Extract zipfile into target dir\n            zipfile.py -c zipfile.zip src ... # Create zipfile from sources\n        '
          21  CALL_FUNCTION_1       1 
          24  STORE_FAST            2  'USAGE'

1372      27  LOAD_FAST             0  'args'
          30  LOAD_CONST            0  ''
          33  COMPARE_OP            8  'is'
          36  POP_JUMP_IF_FALSE    55  'to 55'

1373      39  LOAD_GLOBAL           3  'sys'
          42  LOAD_ATTR             4  'argv'
          45  LOAD_CONST            3  1
          48  SLICE+1          
          49  STORE_FAST            0  'args'
          52  JUMP_FORWARD          0  'to 55'
        55_0  COME_FROM                '52'

1375      55  LOAD_FAST             0  'args'
          58  UNARY_NOT        
          59  POP_JUMP_IF_TRUE     75  'to 75'
          62  POP_JUMP_IF_TRUE      1  'to 1'
          65  BINARY_SUBSCR    
          66  LOAD_CONST           18  ('-l', '-c', '-e', '-t')
          69  COMPARE_OP            7  'not-in'
        72_0  COME_FROM                '62'
        72_1  COME_FROM                '59'
          72  POP_JUMP_IF_FALSE   101  'to 101'

1376      75  LOAD_GLOBAL           5  'print'
          78  LOAD_FAST             2  'USAGE'
          81  CALL_FUNCTION_1       1 
          84  POP_TOP          

1377      85  LOAD_GLOBAL           3  'sys'
          88  LOAD_ATTR             6  'exit'
          91  LOAD_CONST            3  1
          94  CALL_FUNCTION_1       1 
          97  POP_TOP          
          98  JUMP_FORWARD          0  'to 101'
       101_0  COME_FROM                '98'

1379     101  JUMP_FORWARD          1  'to 105'
         104  BINARY_SUBSCR    
       105_0  COME_FROM                '101'
         105  LOAD_CONST            4  '-l'
         108  COMPARE_OP            2  '=='
         111  POP_JUMP_IF_FALSE   197  'to 197'

1380     114  LOAD_GLOBAL           7  'len'
         117  LOAD_FAST             0  'args'
         120  CALL_FUNCTION_1       1 
         123  LOAD_CONST            8  2
         126  COMPARE_OP            3  '!='
         129  POP_JUMP_IF_FALSE   158  'to 158'

1381     132  LOAD_GLOBAL           5  'print'
         135  LOAD_FAST             2  'USAGE'
         138  CALL_FUNCTION_1       1 
         141  POP_TOP          

1382     142  LOAD_GLOBAL           3  'sys'
         145  LOAD_ATTR             6  'exit'
         148  LOAD_CONST            3  1
         151  CALL_FUNCTION_1       1 
         154  POP_TOP          
         155  JUMP_FORWARD          0  'to 158'
       158_0  COME_FROM                '155'

1383     158  LOAD_GLOBAL           8  'ZipFile'
         161  LOAD_GLOBAL           3  'sys'
         164  BINARY_SUBSCR    
         165  LOAD_CONST            9  'r'
         168  CALL_FUNCTION_2       2 
         171  STORE_FAST            3  'zf'

1384     174  LOAD_FAST             3  'zf'
         177  LOAD_ATTR             9  'printdir'
         180  CALL_FUNCTION_0       0 
         183  POP_TOP          

1385     184  LOAD_FAST             3  'zf'
         187  LOAD_ATTR            10  'close'
         190  CALL_FUNCTION_0       0 
         193  POP_TOP          
         194  JUMP_FORWARD        557  'to 754'

1387     197  JUMP_FORWARD          1  'to 201'
         200  BINARY_SUBSCR    
       201_0  COME_FROM                '197'
         201  LOAD_CONST            7  '-t'
         204  COMPARE_OP            2  '=='
         207  POP_JUMP_IF_FALSE   323  'to 323'

1388     210  LOAD_GLOBAL           7  'len'
         213  LOAD_FAST             0  'args'
         216  CALL_FUNCTION_1       1 
         219  LOAD_CONST            8  2
         222  COMPARE_OP            3  '!='
         225  POP_JUMP_IF_FALSE   254  'to 254'

1389     228  LOAD_GLOBAL           5  'print'
         231  LOAD_FAST             2  'USAGE'
         234  CALL_FUNCTION_1       1 
         237  POP_TOP          

1390     238  LOAD_GLOBAL           3  'sys'
         241  LOAD_ATTR             6  'exit'
         244  LOAD_CONST            3  1
         247  CALL_FUNCTION_1       1 
         250  POP_TOP          
         251  JUMP_FORWARD          0  'to 254'
       254_0  COME_FROM                '251'

1391     254  LOAD_GLOBAL           8  'ZipFile'
         257  LOAD_GLOBAL           3  'sys'
         260  BINARY_SUBSCR    
         261  LOAD_CONST            9  'r'
         264  CALL_FUNCTION_2       2 
         267  STORE_FAST            3  'zf'

1392     270  LOAD_FAST             3  'zf'
         273  LOAD_ATTR            11  'testzip'
         276  CALL_FUNCTION_0       0 
         279  STORE_FAST            4  'badfile'

1393     282  LOAD_FAST             4  'badfile'
         285  POP_JUMP_IF_FALSE   310  'to 310'

1394     288  LOAD_GLOBAL           5  'print'
         291  LOAD_CONST           10  'The following enclosed file is corrupted: {!r}'
         294  LOAD_ATTR            12  'format'
         297  LOAD_FAST             4  'badfile'
         300  CALL_FUNCTION_1       1 
         303  CALL_FUNCTION_1       1 
         306  POP_TOP          
         307  JUMP_FORWARD          0  'to 310'
       310_0  COME_FROM                '307'

1395     310  LOAD_GLOBAL           5  'print'
         313  LOAD_CONST           11  'Done testing'
         316  CALL_FUNCTION_1       1 
         319  POP_TOP          
         320  JUMP_FORWARD        431  'to 754'

1397     323  JUMP_FORWARD          1  'to 327'
         326  BINARY_SUBSCR    
       327_0  COME_FROM                '323'
         327  LOAD_CONST            6  '-e'
         330  COMPARE_OP            2  '=='
         333  POP_JUMP_IF_FALSE   601  'to 601'

1398     336  LOAD_GLOBAL           7  'len'
         339  LOAD_FAST             0  'args'
         342  CALL_FUNCTION_1       1 
         345  LOAD_CONST           12  3
         348  COMPARE_OP            3  '!='
         351  POP_JUMP_IF_FALSE   380  'to 380'

1399     354  LOAD_GLOBAL           5  'print'
         357  LOAD_FAST             2  'USAGE'
         360  CALL_FUNCTION_1       1 
         363  POP_TOP          

1400     364  LOAD_GLOBAL           3  'sys'
         367  LOAD_ATTR             6  'exit'
         370  LOAD_CONST            3  1
         373  CALL_FUNCTION_1       1 
         376  POP_TOP          
         377  JUMP_FORWARD          0  'to 380'
       380_0  COME_FROM                '377'

1402     380  LOAD_GLOBAL           8  'ZipFile'
         383  LOAD_GLOBAL           3  'sys'
         386  BINARY_SUBSCR    
         387  LOAD_CONST            9  'r'
         390  CALL_FUNCTION_2       2 
         393  STORE_FAST            3  'zf'

1403     396  STORE_FAST            8  'tgtdir'
         399  BINARY_SUBSCR    
         400  STORE_FAST            5  'out'

1404     403  SETUP_LOOP          182  'to 588'
         406  LOAD_FAST             3  'zf'
         409  LOAD_ATTR            13  'namelist'
         412  CALL_FUNCTION_0       0 
         415  GET_ITER         
         416  FOR_ITER            168  'to 587'
         419  STORE_FAST            6  'path'

1405     422  LOAD_FAST             6  'path'
         425  LOAD_ATTR            14  'startswith'
         428  LOAD_CONST           13  './'
         431  CALL_FUNCTION_1       1 
         434  POP_JUMP_IF_FALSE   465  'to 465'

1406     437  LOAD_GLOBAL          15  'os'
         440  LOAD_ATTR            16  'path'
         443  LOAD_ATTR            17  'join'
         446  LOAD_FAST             5  'out'
         449  LOAD_FAST             6  'path'
         452  LOAD_CONST            8  2
         455  SLICE+1          
         456  CALL_FUNCTION_2       2 
         459  STORE_FAST            7  'tgt'
         462  JUMP_FORWARD         21  'to 486'

1408     465  LOAD_GLOBAL          15  'os'
         468  LOAD_ATTR            16  'path'
         471  LOAD_ATTR            17  'join'
         474  LOAD_FAST             5  'out'
         477  LOAD_FAST             6  'path'
         480  CALL_FUNCTION_2       2 
         483  STORE_FAST            7  'tgt'
       486_0  COME_FROM                '462'

1410     486  LOAD_GLOBAL          15  'os'
         489  LOAD_ATTR            16  'path'
         492  LOAD_ATTR            18  'dirname'
         495  LOAD_FAST             7  'tgt'
         498  CALL_FUNCTION_1       1 
         501  STORE_FAST            8  'tgtdir'

1411     504  LOAD_GLOBAL          15  'os'
         507  LOAD_ATTR            16  'path'
         510  LOAD_ATTR            19  'exists'
         513  LOAD_FAST             8  'tgtdir'
         516  CALL_FUNCTION_1       1 
         519  POP_JUMP_IF_TRUE    538  'to 538'

1412     522  LOAD_GLOBAL          15  'os'
         525  LOAD_ATTR            20  'makedirs'
         528  LOAD_FAST             8  'tgtdir'
         531  CALL_FUNCTION_1       1 
         534  POP_TOP          
         535  JUMP_FORWARD          0  'to 538'
       538_0  COME_FROM                '535'

1413     538  LOAD_GLOBAL          21  'open'
         541  LOAD_FAST             7  'tgt'
         544  LOAD_CONST           14  'wb'
         547  CALL_FUNCTION_2       2 
         550  SETUP_WITH           29  'to 582'
         553  STORE_FAST            9  'fp'

1414     556  LOAD_FAST             9  'fp'
         559  LOAD_ATTR            22  'write'
         562  LOAD_FAST             3  'zf'
         565  LOAD_ATTR            23  'read'
         568  LOAD_FAST             6  'path'
         571  CALL_FUNCTION_1       1 
         574  CALL_FUNCTION_1       1 
         577  POP_TOP          
         578  POP_BLOCK        
         579  LOAD_CONST            0  ''
       582_0  COME_FROM_WITH           '550'
         582  WITH_CLEANUP     
         583  END_FINALLY      
         584  JUMP_BACK           416  'to 416'
         587  POP_BLOCK        
       588_0  COME_FROM                '403'

1415     588  LOAD_FAST             3  'zf'
         591  LOAD_ATTR            10  'close'
         594  CALL_FUNCTION_0       0 
         597  POP_TOP          
         598  JUMP_FORWARD        153  'to 754'

1417     601  JUMP_FORWARD          1  'to 605'
         604  BINARY_SUBSCR    
       605_0  COME_FROM                '601'
         605  LOAD_CONST            5  '-c'
         608  COMPARE_OP            2  '=='
         611  POP_JUMP_IF_FALSE   754  'to 754'

1418     614  LOAD_GLOBAL           7  'len'
         617  LOAD_FAST             0  'args'
         620  CALL_FUNCTION_1       1 
         623  LOAD_CONST           12  3
         626  COMPARE_OP            0  '<'
         629  POP_JUMP_IF_FALSE   658  'to 658'

1419     632  LOAD_GLOBAL           5  'print'
         635  LOAD_FAST             2  'USAGE'
         638  CALL_FUNCTION_1       1 
         641  POP_TOP          

1420     642  LOAD_GLOBAL           3  'sys'
         645  LOAD_ATTR             6  'exit'
         648  LOAD_CONST            3  1
         651  CALL_FUNCTION_1       1 
         654  POP_TOP          
         655  JUMP_FORWARD          0  'to 658'
       658_0  COME_FROM                '655'

1422     658  LOAD_CLOSURE          0  'addToZip'
         664  LOAD_CONST               '<code_object addToZip>'
         667  MAKE_CLOSURE_0        0 
         670  STORE_DEREF           0  'addToZip'

1431     673  LOAD_GLOBAL           8  'ZipFile'
         676  LOAD_GLOBAL           3  'sys'
         679  BINARY_SUBSCR    
         680  LOAD_CONST           16  'w'
         683  LOAD_CONST           17  'allowZip64'
         686  LOAD_GLOBAL          24  'True'
         689  CALL_FUNCTION_258   258 
         692  STORE_FAST            3  'zf'

1432     695  SETUP_LOOP           43  'to 741'
         698  SETUP_LOOP            8  'to 709'
         701  SLICE+1          
         702  GET_ITER         
         703  FOR_ITER             34  'to 740'
         706  STORE_FAST           10  'src'
       709_0  COME_FROM                '698'

1433     709  LOAD_DEREF            0  'addToZip'
         712  LOAD_FAST             3  'zf'
         715  LOAD_FAST            10  'src'
         718  LOAD_GLOBAL          15  'os'
         721  LOAD_ATTR            16  'path'
         724  LOAD_ATTR            25  'basename'
         727  LOAD_FAST            10  'src'
         730  CALL_FUNCTION_1       1 
         733  CALL_FUNCTION_3       3 
         736  POP_TOP          
         737  JUMP_BACK           703  'to 703'
         740  POP_BLOCK        
       741_0  COME_FROM                '695'

1435     741  LOAD_FAST             3  'zf'
         744  LOAD_ATTR            10  'close'
         747  CALL_FUNCTION_0       0 
         750  POP_TOP          
         751  JUMP_FORWARD          0  'to 754'
       754_0  COME_FROM                '751'
       754_1  COME_FROM                '598'
       754_2  COME_FROM                '320'
       754_3  COME_FROM                '194'
         754  LOAD_CONST            0  ''
         757  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 62


if __name__ == '__main__':
    main()