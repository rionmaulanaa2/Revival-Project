# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/lib/zipfile.py
import struct
import os
import time
import sys
import shutil
import binascii
import cStringIO
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

 146       0  LOAD_GLOBAL           0  'False'
           3  STORE_FAST            1  'result'

 147       6  SETUP_EXCEPT         67  'to 76'

 148       9  LOAD_GLOBAL           1  'hasattr'
          12  LOAD_GLOBAL           1  'hasattr'
          15  CALL_FUNCTION_2       2 
          18  POP_JUMP_IF_FALSE    39  'to 39'

 149      21  LOAD_GLOBAL           2  '_check_zipfile'
          24  LOAD_CONST            2  'fp'
          27  LOAD_FAST             0  'filename'
          30  CALL_FUNCTION_256   256 
          33  STORE_FAST            1  'result'
          36  JUMP_FORWARD         33  'to 72'

 151      39  LOAD_GLOBAL           3  'open'
          42  LOAD_GLOBAL           3  'open'
          45  CALL_FUNCTION_2       2 
          48  SETUP_WITH           19  'to 70'
          51  STORE_FAST            2  'fp'

 152      54  LOAD_GLOBAL           2  '_check_zipfile'
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

 153      76  DUP_TOP          
          77  LOAD_GLOBAL           4  'IOError'
          80  COMPARE_OP           10  'exception-match'
          83  POP_JUMP_IF_FALSE    92  'to 92'
          86  POP_TOP          
          87  POP_TOP          
          88  POP_TOP          

 154      89  JUMP_FORWARD          1  'to 93'
          92  END_FINALLY      
        93_0  COME_FROM                '92'
        93_1  COME_FROM                '73'

 155      93  LOAD_FAST             1  'result'
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
        null_byte = filename.find(chr(0))
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
        if isinstance(self.filename, unicode):
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
                    raise RuntimeError, 'Corrupt extra field %s' % (ln,)
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
        self.key2 = self._crc32(chr(self.key1 >> 24 & 255), self.key2)

    def __call__(self, c):
        c = ord(c)
        k = self.key2 | 2
        c = c ^ k * (k ^ 1) >> 8 & 255
        c = chr(c)
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
                raise RuntimeError, 'Compression requires the (missing) zlib module'
        else:
            raise RuntimeError, 'That compression method is not supported'
        self._allowZip64 = allowZip64
        self._didModify = False
        self.debug = 0
        self.NameToInfo = {}
        self.filelist = []
        self.compression = compression
        self.mode = key = mode.replace('b', '')[0]
        self.pwd = None
        self.comment = ''
        if isinstance(file, basestring):
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
            raise RuntimeError, 'Mode must be "r", "w" or "a"'
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
            raise BadZipfile, 'File is not a zip file'
        if self.debug > 1:
            print endrec
        size_cd = endrec[_ECD_SIZE]
        offset_cd = endrec[_ECD_OFFSET]
        self.comment = endrec[_ECD_COMMENT]
        concat = endrec[_ECD_LOCATION] - size_cd - offset_cd
        if endrec[_ECD_SIGNATURE] == stringEndArchive64:
            concat -= sizeEndCentDir64 + sizeEndCentDir64Locator
        if self.debug > 2:
            inferred = concat + offset_cd
            print 'given, inferred, offset', offset_cd, inferred, concat
        self.start_dir = offset_cd + concat
        fp.seek(self.start_dir, 0)
        data = fp.read(size_cd)
        fp = cStringIO.StringIO(data)
        total = 0
        while total < size_cd:
            centdir = fp.read(sizeCentralDir)
            if centdir[0:4] != stringCentralDir:
                raise BadZipfile, 'Bad magic number for central directory'
            centdir = struct.unpack(structCentralDir, centdir)
            if self.debug > 2:
                print centdir
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
                print 'total', total

    def namelist(self):
        l = []
        for data in self.filelist:
            l.append(data.filename)

        return l

    def infolist(self):
        return self.filelist

    def printdir(self):
        print '%-46s %19s %12s' % ('File Name', 'Modified    ', 'Size')
        for zinfo in self.filelist:
            date = '%d-%02d-%02d %02d:%02d:%02d' % zinfo.date_time[:6]
            print '%-46s %s %12d' % (zinfo.filename, date, zinfo.file_size)

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
            raise RuntimeError, 'open() requires mode "r", "U", or "rU"'
        if not self.fp:
            raise RuntimeError, 'Attempt to read ZIP archive that was already closed'
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
            raise BadZipfile, 'Bad magic number for file header'
        fheader = struct.unpack(structFileHeader, fheader)
        fname = zef_file.read(fheader[_FH_FILENAME_LENGTH])
        if fheader[_FH_EXTRA_FIELD_LENGTH]:
            zef_file.read(fheader[_FH_EXTRA_FIELD_LENGTH])
        if fname != zinfo.orig_filename:
            raise BadZipfile, 'File name in directory "%s" and header "%s" differ.' % (
             zinfo.orig_filename, fname)
        is_encrypted = zinfo.flag_bits & 1
        zd = None
        if is_encrypted:
            if not pwd:
                pwd = self.pwd
            if not pwd:
                raise RuntimeError, 'File %s is encrypted, password required for extraction' % name
            zd = _ZipDecrypter(pwd)
            bytes = zef_file.read(12)
            h = map(zd, bytes[0:12])
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
        target = file(targetpath, 'wb')
        shutil.copyfileobj(source, target)
        source.close()
        target.close()
        return targetpath

    def _writecheck(self, zinfo):
        if zinfo.filename in self.NameToInfo:
            if self.debug:
                print 'Duplicate name:', zinfo.filename
        if self.mode not in ('w', 'a'):
            raise RuntimeError, 'write() requires mode "w" or "a"'
        if not self.fp:
            raise RuntimeError, 'Attempt to write ZIP archive that was already closed'
        if zinfo.compress_type == ZIP_DEFLATED and not zlib:
            raise RuntimeError, 'Compression requires the (missing) zlib module'
        if zinfo.compress_type not in (ZIP_STORED, ZIP_DEFLATED):
            raise RuntimeError, 'That compression method is not supported'
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
                        print >> sys.stderr, (structCentralDir,
                         stringCentralDir, create_version,
                         zinfo.create_system, extract_version, zinfo.reserved,
                         zinfo.flag_bits, zinfo.compress_type, dostime, dosdate,
                         zinfo.CRC, compress_size, file_size,
                         len(zinfo.filename), len(extra_data), len(zinfo.comment),
                         0, zinfo.internal_attr, zinfo.external_attr,
                         header_offset)
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
                    print 'Adding package in', pathname, 'as', basename
                fname, arcname = self._get_codename(initname[0:-3], basename)
                if self.debug:
                    print 'Adding', arcname
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
                            print 'Adding', arcname
                        self.write(fname, arcname)

            else:
                if self.debug:
                    print 'Adding files from directory', pathname
                for filename in os.listdir(pathname):
                    path = os.path.join(pathname, filename)
                    root, ext = os.path.splitext(filename)
                    if ext == '.py':
                        fname, arcname = self._get_codename(path[0:-3], basename)
                        if self.debug:
                            print 'Adding', arcname
                        self.write(fname, arcname)

        else:
            if pathname[-3:] != '.py':
                raise RuntimeError, 'Files added with writepy() must end with ".py"'
            fname, arcname = self._get_codename(pathname[0:-3], basename)
            if self.debug:
                print 'Adding file', arcname
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
                print 'Compiling', file_py
            try:
                py_compile.compile(file_py, file_pyc, None, True)
            except py_compile.PyCompileError as err:
                print err.msg

            fname = file_pyc
        else:
            fname = file_pyc
        archivename = os.path.split(fname)[1]
        if basename:
            archivename = '%s/%s' % (basename, archivename)
        return (fname, archivename)


def main--- This code section failed: ---

1366       0  LOAD_CONST            1  -1
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'textwrap'
           9  STORE_FAST            1  'textwrap'

1367      12  LOAD_FAST             1  'textwrap'
          15  LOAD_ATTR             1  'dedent'

1373      18  LOAD_CONST            2  '        Usage:\n            zipfile.py -l zipfile.zip        # Show listing of a zipfile\n            zipfile.py -t zipfile.zip        # Test if a zipfile is valid\n            zipfile.py -e zipfile.zip target # Extract zipfile into target dir\n            zipfile.py -c zipfile.zip src ... # Create zipfile from sources\n        '
          21  CALL_FUNCTION_1       1 
          24  STORE_FAST            2  'USAGE'

1374      27  LOAD_FAST             0  'args'
          30  LOAD_CONST            0  ''
          33  COMPARE_OP            8  'is'
          36  POP_JUMP_IF_FALSE    55  'to 55'

1375      39  LOAD_GLOBAL           3  'sys'
          42  LOAD_ATTR             4  'argv'
          45  LOAD_CONST            3  1
          48  SLICE+1          
          49  STORE_FAST            0  'args'
          52  JUMP_FORWARD          0  'to 55'
        55_0  COME_FROM                '52'

1377      55  LOAD_FAST             0  'args'
          58  UNARY_NOT        
          59  POP_JUMP_IF_TRUE     75  'to 75'
          62  POP_JUMP_IF_TRUE      4  'to 4'
          65  BINARY_SUBSCR    
          66  LOAD_CONST           19  ('-l', '-c', '-e', '-t')
          69  COMPARE_OP            7  'not-in'
        72_0  COME_FROM                '62'
        72_1  COME_FROM                '59'
          72  POP_JUMP_IF_FALSE    96  'to 96'

1378      75  LOAD_FAST             2  'USAGE'
          78  PRINT_ITEM       
          79  PRINT_NEWLINE_CONT

1379      80  LOAD_GLOBAL           3  'sys'
          83  LOAD_ATTR             5  'exit'
          86  LOAD_CONST            3  1
          89  CALL_FUNCTION_1       1 
          92  POP_TOP          
          93  JUMP_FORWARD          0  'to 96'
        96_0  COME_FROM                '93'

1381      96  JUMP_FORWARD          4  'to 103'
          99  BINARY_SUBSCR    
         100  LOAD_CONST            5  '-l'
       103_0  COME_FROM                '96'
         103  COMPARE_OP            2  '=='
         106  POP_JUMP_IF_FALSE   187  'to 187'

1382     109  LOAD_GLOBAL           6  'len'
         112  LOAD_FAST             0  'args'
         115  CALL_FUNCTION_1       1 
         118  LOAD_CONST            9  2
         121  COMPARE_OP            3  '!='
         124  POP_JUMP_IF_FALSE   148  'to 148'

1383     127  LOAD_FAST             2  'USAGE'
         130  PRINT_ITEM       
         131  PRINT_NEWLINE_CONT

1384     132  LOAD_GLOBAL           3  'sys'
         135  LOAD_ATTR             5  'exit'
         138  LOAD_CONST            3  1
         141  CALL_FUNCTION_1       1 
         144  POP_TOP          
         145  JUMP_FORWARD          0  'to 148'
       148_0  COME_FROM                '145'

1385     148  LOAD_GLOBAL           7  'ZipFile'
         151  LOAD_GLOBAL           3  'sys'
         154  BINARY_SUBSCR    
         155  LOAD_CONST           10  'r'
         158  CALL_FUNCTION_2       2 
         161  STORE_FAST            3  'zf'

1386     164  LOAD_FAST             3  'zf'
         167  LOAD_ATTR             8  'printdir'
         170  CALL_FUNCTION_0       0 
         173  POP_TOP          

1387     174  LOAD_FAST             3  'zf'
         177  LOAD_ATTR             9  'close'
         180  CALL_FUNCTION_0       0 
         183  POP_TOP          
         184  JUMP_FORWARD        532  'to 719'

1389     187  JUMP_FORWARD          4  'to 194'
         190  BINARY_SUBSCR    
         191  LOAD_CONST            8  '-t'
       194_0  COME_FROM                '187'
         194  COMPARE_OP            2  '=='
         197  POP_JUMP_IF_FALSE   298  'to 298'

1390     200  LOAD_GLOBAL           6  'len'
         203  LOAD_FAST             0  'args'
         206  CALL_FUNCTION_1       1 
         209  LOAD_CONST            9  2
         212  COMPARE_OP            3  '!='
         215  POP_JUMP_IF_FALSE   239  'to 239'

1391     218  LOAD_FAST             2  'USAGE'
         221  PRINT_ITEM       
         222  PRINT_NEWLINE_CONT

1392     223  LOAD_GLOBAL           3  'sys'
         226  LOAD_ATTR             5  'exit'
         229  LOAD_CONST            3  1
         232  CALL_FUNCTION_1       1 
         235  POP_TOP          
         236  JUMP_FORWARD          0  'to 239'
       239_0  COME_FROM                '236'

1393     239  LOAD_GLOBAL           7  'ZipFile'
         242  LOAD_GLOBAL           3  'sys'
         245  BINARY_SUBSCR    
         246  LOAD_CONST           10  'r'
         249  CALL_FUNCTION_2       2 
         252  STORE_FAST            3  'zf'

1394     255  LOAD_FAST             3  'zf'
         258  LOAD_ATTR            10  'testzip'
         261  CALL_FUNCTION_0       0 
         264  STORE_FAST            4  'badfile'

1395     267  LOAD_FAST             4  'badfile'
         270  POP_JUMP_IF_FALSE   290  'to 290'

1396     273  LOAD_CONST           11  'The following enclosed file is corrupted: {!r}'
         276  LOAD_ATTR            11  'format'
         279  LOAD_FAST             4  'badfile'
         282  CALL_FUNCTION_1       1 
         285  PRINT_ITEM       
         286  PRINT_NEWLINE_CONT
         287  JUMP_FORWARD          0  'to 290'
       290_0  COME_FROM                '287'

1397     290  LOAD_CONST           12  'Done testing'
         293  PRINT_ITEM       
         294  PRINT_NEWLINE_CONT
         295  JUMP_FORWARD        421  'to 719'

1399     298  JUMP_FORWARD          4  'to 305'
         301  BINARY_SUBSCR    
         302  LOAD_CONST            7  '-e'
       305_0  COME_FROM                '298'
         305  COMPARE_OP            2  '=='
         308  POP_JUMP_IF_FALSE   571  'to 571'

1400     311  LOAD_GLOBAL           6  'len'
         314  LOAD_FAST             0  'args'
         317  CALL_FUNCTION_1       1 
         320  LOAD_CONST           13  3
         323  COMPARE_OP            3  '!='
         326  POP_JUMP_IF_FALSE   350  'to 350'

1401     329  LOAD_FAST             2  'USAGE'
         332  PRINT_ITEM       
         333  PRINT_NEWLINE_CONT

1402     334  LOAD_GLOBAL           3  'sys'
         337  LOAD_ATTR             5  'exit'
         340  LOAD_CONST            3  1
         343  CALL_FUNCTION_1       1 
         346  POP_TOP          
         347  JUMP_FORWARD          0  'to 350'
       350_0  COME_FROM                '347'

1404     350  LOAD_GLOBAL           7  'ZipFile'
         353  LOAD_GLOBAL           3  'sys'
         356  BINARY_SUBSCR    
         357  LOAD_CONST           10  'r'
         360  CALL_FUNCTION_2       2 
         363  STORE_FAST            3  'zf'

1405     366  STORE_FAST            9  'fp'
         369  BINARY_SUBSCR    
         370  STORE_FAST            5  'out'

1406     373  SETUP_LOOP          182  'to 558'
         376  LOAD_FAST             3  'zf'
         379  LOAD_ATTR            12  'namelist'
         382  CALL_FUNCTION_0       0 
         385  GET_ITER         
         386  FOR_ITER            168  'to 557'
         389  STORE_FAST            6  'path'

1407     392  LOAD_FAST             6  'path'
         395  LOAD_ATTR            13  'startswith'
         398  LOAD_CONST           14  './'
         401  CALL_FUNCTION_1       1 
         404  POP_JUMP_IF_FALSE   435  'to 435'

1408     407  LOAD_GLOBAL          14  'os'
         410  LOAD_ATTR            15  'path'
         413  LOAD_ATTR            16  'join'
         416  LOAD_FAST             5  'out'
         419  LOAD_FAST             6  'path'
         422  LOAD_CONST            9  2
         425  SLICE+1          
         426  CALL_FUNCTION_2       2 
         429  STORE_FAST            7  'tgt'
         432  JUMP_FORWARD         21  'to 456'

1410     435  LOAD_GLOBAL          14  'os'
         438  LOAD_ATTR            15  'path'
         441  LOAD_ATTR            16  'join'
         444  LOAD_FAST             5  'out'
         447  LOAD_FAST             6  'path'
         450  CALL_FUNCTION_2       2 
         453  STORE_FAST            7  'tgt'
       456_0  COME_FROM                '432'

1412     456  LOAD_GLOBAL          14  'os'
         459  LOAD_ATTR            15  'path'
         462  LOAD_ATTR            17  'dirname'
         465  LOAD_FAST             7  'tgt'
         468  CALL_FUNCTION_1       1 
         471  STORE_FAST            8  'tgtdir'

1413     474  LOAD_GLOBAL          14  'os'
         477  LOAD_ATTR            15  'path'
         480  LOAD_ATTR            18  'exists'
         483  LOAD_FAST             8  'tgtdir'
         486  CALL_FUNCTION_1       1 
         489  POP_JUMP_IF_TRUE    508  'to 508'

1414     492  LOAD_GLOBAL          14  'os'
         495  LOAD_ATTR            19  'makedirs'
         498  LOAD_FAST             8  'tgtdir'
         501  CALL_FUNCTION_1       1 
         504  POP_TOP          
         505  JUMP_FORWARD          0  'to 508'
       508_0  COME_FROM                '505'

1415     508  LOAD_GLOBAL          20  'open'
         511  LOAD_FAST             7  'tgt'
         514  LOAD_CONST           15  'wb'
         517  CALL_FUNCTION_2       2 
         520  SETUP_WITH           29  'to 552'
         523  STORE_FAST            9  'fp'

1416     526  LOAD_FAST             9  'fp'
         529  LOAD_ATTR            21  'write'
         532  LOAD_FAST             3  'zf'
         535  LOAD_ATTR            22  'read'
         538  LOAD_FAST             6  'path'
         541  CALL_FUNCTION_1       1 
         544  CALL_FUNCTION_1       1 
         547  POP_TOP          
         548  POP_BLOCK        
         549  LOAD_CONST            0  ''
       552_0  COME_FROM_WITH           '520'
         552  WITH_CLEANUP     
         553  END_FINALLY      
         554  JUMP_BACK           386  'to 386'
         557  POP_BLOCK        
       558_0  COME_FROM                '373'

1417     558  LOAD_FAST             3  'zf'
         561  LOAD_ATTR             9  'close'
         564  CALL_FUNCTION_0       0 
         567  POP_TOP          
         568  JUMP_FORWARD        148  'to 719'

1419     571  JUMP_FORWARD          4  'to 578'
         574  BINARY_SUBSCR    
         575  LOAD_CONST            6  '-c'
       578_0  COME_FROM                '571'
         578  COMPARE_OP            2  '=='
         581  POP_JUMP_IF_FALSE   719  'to 719'

1420     584  LOAD_GLOBAL           6  'len'
         587  LOAD_FAST             0  'args'
         590  CALL_FUNCTION_1       1 
         593  LOAD_CONST           13  3
         596  COMPARE_OP            0  '<'
         599  POP_JUMP_IF_FALSE   623  'to 623'

1421     602  LOAD_FAST             2  'USAGE'
         605  PRINT_ITEM       
         606  PRINT_NEWLINE_CONT

1422     607  LOAD_GLOBAL           3  'sys'
         610  LOAD_ATTR             5  'exit'
         613  LOAD_CONST            3  1
         616  CALL_FUNCTION_1       1 
         619  POP_TOP          
         620  JUMP_FORWARD          0  'to 623'
       623_0  COME_FROM                '620'

1424     623  LOAD_CLOSURE          0  'addToZip'
         629  LOAD_CONST               '<code_object addToZip>'
         632  MAKE_CLOSURE_0        0 
         635  STORE_DEREF           0  'addToZip'

1433     638  LOAD_GLOBAL           7  'ZipFile'
         641  LOAD_GLOBAL           3  'sys'
         644  BINARY_SUBSCR    
         645  LOAD_CONST           17  'w'
         648  LOAD_CONST           18  'allowZip64'
         651  LOAD_GLOBAL          23  'True'
         654  CALL_FUNCTION_258   258 
         657  STORE_FAST            3  'zf'

1434     660  SETUP_LOOP           43  'to 706'
         663  SETUP_LOOP            9  'to 675'
         666  SLICE+1          
         667  GET_ITER         
         668  FOR_ITER             34  'to 705'
         671  STORE_FAST           10  'src'

1435     674  LOAD_DEREF            0  'addToZip'
         677  LOAD_FAST             3  'zf'
         680  LOAD_FAST            10  'src'
         683  LOAD_GLOBAL          14  'os'
         686  LOAD_ATTR            15  'path'
         689  LOAD_ATTR            24  'basename'
         692  LOAD_FAST            10  'src'
         695  CALL_FUNCTION_1       1 
         698  CALL_FUNCTION_3       3 
         701  POP_TOP          
         702  JUMP_BACK           668  'to 668'
         705  POP_BLOCK        
       706_0  COME_FROM                '660'

1437     706  LOAD_FAST             3  'zf'
         709  LOAD_ATTR             9  'close'
         712  CALL_FUNCTION_0       0 
         715  POP_TOP          
         716  JUMP_FORWARD          0  'to 719'
       719_0  COME_FROM                '716'
       719_1  COME_FROM                '568'
       719_2  COME_FROM                '295'
       719_3  COME_FROM                '184'
         719  LOAD_CONST            0  ''
         722  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 62


if __name__ == '__main__':
    main()