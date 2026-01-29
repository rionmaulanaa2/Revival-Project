# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/mobilecommon.py
from __future__ import absolute_import
import six_ex
import os
try:
    import __pypy__
    pypy = True
except:
    pypy = False

class extendabletype(type):

    def __new__(cls, name, bases, dict):
        if name == '__extend__':
            for cls in bases:
                for key, value in six_ex.items(dict):
                    if key == '__module__':
                        continue
                    setattr(cls, key, value)

            return None
        else:
            return super(extendabletype, cls).__new__(cls, name, bases, dict)
            return None


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class Singleton(object):
    _instance = None

    def init(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.init(*args, **kwargs)
        return cls._instance


class AttrProxy(object):

    def __init__--- This code section failed: ---

  53       0  LOAD_GLOBAL           0  'object'
           3  LOAD_ATTR             1  '__setattr__'
           6  LOAD_ATTR             1  '__setattr__'
           9  LOAD_FAST             1  'attr'
          12  CALL_FUNCTION_3       3 
          15  POP_TOP          

Parse error at or near `CALL_FUNCTION_3' instruction at offset 12

    def __getattr__--- This code section failed: ---

  56       0  LOAD_GLOBAL           0  'object'
           3  LOAD_ATTR             1  '__getattribute__'
           6  LOAD_ATTR             1  '__getattribute__'
           9  CALL_FUNCTION_2       2 
          12  STORE_FAST            2  'attr'

  57      15  LOAD_FAST             2  'attr'
          18  LOAD_ATTR             2  'get'
          21  LOAD_FAST             1  'name'
          24  CALL_FUNCTION_1       1 
          27  STORE_FAST            3  'val'

  58      30  LOAD_FAST             3  'val'
          33  POP_JUMP_IF_TRUE     55  'to 55'

  59      36  LOAD_GLOBAL           3  'AttributeError'
          39  LOAD_CONST            2  'proxy has no attribute(%s)'
          42  LOAD_FAST             1  'name'
          45  BINARY_MODULO    
          46  CALL_FUNCTION_1       1 
          49  RAISE_VARARGS_1       1 
          52  JUMP_FORWARD          0  'to 55'
        55_0  COME_FROM                '52'

  61      55  LOAD_FAST             3  'val'
          58  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9

    def __setattr__--- This code section failed: ---

  64       0  LOAD_GLOBAL           0  'object'
           3  LOAD_ATTR             1  '__getattribute__'
           6  LOAD_ATTR             1  '__getattribute__'
           9  CALL_FUNCTION_2       2 
          12  STORE_FAST            3  'attr'

  65      15  LOAD_FAST             2  'value'
          18  LOAD_FAST             3  'attr'
          21  LOAD_FAST             1  'name'
          24  STORE_SUBSCR     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9


def need_replace_async():
    if os.environ.get('REPLACE_ASYNC') == 'True':
        return True
    return False


replace_async = need_replace_async()
use_pypy = os.environ.get('USE_PYPY') == 'True'
use_ipv6 = False
CONNECT_TYPE_TCP = 1
CONNECT_TYPE_UDP = 2
CONNECT_TYPE_KCP = 3
CONNECT_TYPE_MAP = {'tcp': CONNECT_TYPE_TCP,
   'udp': CONNECT_TYPE_KCP,
   'kcp': CONNECT_TYPE_KCP
   }
KCP_CONNECTION_TIMEOUT = 15000

def architecture():
    import sys
    if sys.platform.startswith('win'):
        return '32bit'
    if sys.platform.startswith('linux'):
        return '64bit'
    raise Exception('error platform')


def get_sockinfo(ip, port):
    import socket
    ip = str(ip)
    port = int(port)
    if use_ipv6:
        flags = getattr(socket, 'AI_DEFAULT', socket.AI_ADDRCONFIG) if getattr(socket, 'has_ipv6', False) else 0
        addrinfos = socket.getaddrinfo(ip, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, flags)
        addrinfo = addrinfos[0]
        family, socktype, proto, cannonname, sockaddr = addrinfo
        return (
         family, sockaddr[0], port)
    else:
        return (
         socket.AF_INET, ip, port)


def import_asiocore():
    if architecture() == '32bit':
        if use_pypy:
            from pypy_asiocore import asiocore
            return asiocore
        else:
            import asiocore
            return asiocore

    elif architecture() == '64bit':
        if use_pypy:
            from pypy_asiocore import asiocore
            return asiocore
        else:
            import asiocore_64
            return asiocore_64

    else:
        raise ValueError('error system architecture')


def import_aoi_data():
    try:
        if use_pypy:
            from pypy_aoidata import aoi_data
            return aoi_data
        import aoi_data
        return aoi_data
    except:
        return

    return


def import_aoi_manager():
    try:
        if use_pypy:
            from pypy_aoimanager import aoi_manager
            return aoi_manager
        import aoi_manager
        return aoi_manager
    except:
        return

    return


asiocore = import_asiocore() if replace_async and not pypy else None
if os.environ.get('USE_KCP') == 'True':
    use_kcp = True if 1 else False
    aoi_data = pypy or import_aoi_data()
    aoi_manager = import_aoi_manager()

class Swallower(object):

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __add__(self, other):
        return 0

    def __sub__(self, other):
        return self

    def __mul__(self, other):
        return 1

    def __div__(self, other):
        return 1

    def __getitem__(self, index):
        return self

    def __neg__(self):
        return -1

    def __iter__(self):
        return self

    def next(self):
        raise StopIteration()


class NonexistentSwallower(Swallower):

    def __nonzero__(self):
        return False