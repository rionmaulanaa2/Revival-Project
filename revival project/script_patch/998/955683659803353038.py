# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/HunterPlugin/safaia/redirector.py
import sys
from . import get_instance

class PROT:
    DEVICE_CONNECT = 16
    DEVICE_REJECT = 17
    DEVICE_ACCEPT = 18
    DEVICE_RUN_SCRIPT = 21
    DEVICE_FILE = 22
    DEVICE_OUT = 24
    DEVICE_OUT_BIN = 26
    GZIP_COMPRESSED = 65536
    JSON_SERIALIZED = 131072
    CONTINUOUS_FRAME = 262144


prot = PROT

class DummyMutex(object):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class SafaiaStd(object):

    def __init__(self, origin, _type, _safaia, encoding=None, thread_safe=True):
        super(SafaiaStd, self).__init__()
        self.buf = u''
        if thread_safe:
            import threading
            self._buf_mutex = threading.Lock()
        else:
            self._buf_mutex = DummyMutex()
        self.type = _type
        self._safaia = _safaia
        self.encoding = encoding
        if hasattr(sys, '_safaia_save_origin_std_' + _type):
            self.origin = getattr(sys, '_safaia_save_origin_std_' + _type)
        else:
            self.origin = origin
            setattr(sys, '_safaia_save_origin_std_' + _type, origin)

    def write(self, text):
        try:
            self.origin.write(text)
        except:
            pass

        if type(text) is str:
            try:
                text = text.decode(self.encoding or 'utf-8')
            except:
                text = repr(text).decode('ascii')

        with self._buf_mutex:
            self.buf += text
            while '\n' in self.buf:
                line, self.buf = self.buf.split('\n', 1)
                line = line.rstrip()
                if line:
                    self._safaia.send(prot.DEVICE_OUT, {'type': self.type,'data': line})

    def __getattr__(self, key):
        if hasattr(self.origin, key):
            return getattr(self.origin, key)
        raise AttributeError('self.origin has no attribute ' + key)


class RedirectExtension(get_instance().__class__):

    def __init__(self):
        self.redirect(True)

    def redirect(self, enable):
        if enable:
            if not isinstance(sys.stdout, SafaiaStd):
                sys.stdout = SafaiaStd(sys.stdout, 'stdout', self, self.encoding)
            if not isinstance(sys.stderr, SafaiaStd):
                sys.stderr = SafaiaStd(sys.stderr, 'stderr', self, self.encoding)
        else:
            try:
                sys.stdout = sys.stdout.origin
                sys.stderr = sys.stderr.origin
            except:
                pass