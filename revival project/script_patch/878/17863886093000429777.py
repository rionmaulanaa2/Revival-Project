# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/six_ex.py
import sys
import types
import six
PY3 = six.PY3
if six.PY3:
    long_type = int
    import inspect
    inspect.getargspec = inspect.getfullargspec
    import hashlib
    _md5 = hashlib.md5

    def md5_wrapper(s=None):
        if s is None:
            return _md5()
        else:
            tp = type(s)
            if tp is str:
                return _md5(s.encode())
            return _md5(s)


    hashlib.md5 = md5_wrapper
else:
    long_type = long

class LazyImporter(types.ModuleType):

    def __init__(self, module_name):
        self.__name__ = module_name

    def __getattr__(self, name):
        __import__(self.__name__)
        mod = sys.modules[self.__name__]
        return getattr(mod, name)


splitport_attr = six.MovedAttribute('splitport', 'urllib', 'urllib.parse')
six._urllib_parse_moved_attributes.append(splitport_attr)
setattr(six.Module_six_moves_urllib_parse, splitport_attr.name, splitport_attr)
del splitport_attr
if six.PY3:

    def keys(d, **kw):
        return list(d.keys(**kw))


    def items(d, **kw):
        return list(d.items(**kw))


    def values(d, **kw):
        return list(d.values(**kw))


else:

    def keys(d, **kw):
        return d.keys(**kw)


    def items(d, **kw):
        return d.items(**kw)


    def values(d, **kw):
        return d.values(**kw)


class _SixExMetaPathImporter(object):

    def __init__(self, six_module_name):
        self.name = six_module_name
        self.known_modules = {}

    def _add_module(self, mod, *fullnames):
        for fullname in fullnames:
            self.known_modules[self.name + '.' + fullname] = mod

    def _get_module(self, fullname):
        return self.known_modules[self.name + '.' + fullname]

    def find_module(self, fullname, path=None):
        if fullname in self.known_modules:
            return self
        else:
            return None

    def find_spec(self, fullname, path, target=None):
        if fullname in self.known_modules:
            return six.spec_from_loader(fullname, self)
        else:
            return None

    def __get_module(self, fullname):
        try:
            return self.known_modules[fullname]
        except KeyError:
            raise ImportError('This loader does not know module ' + fullname)

    def load_module(self, fullname):
        try:
            return sys.modules[fullname]
        except KeyError:
            pass

        mod = self.__get_module(fullname)
        if isinstance(mod, six.MovedModule):
            mod = mod._resolve()
        else:
            mod.__loader__ = self
        sys.modules[fullname] = mod
        return mod

    def is_package(self, fullname):
        return hasattr(self.__get_module(fullname), '__path__')

    def get_code(self, fullname):
        self.__get_module(fullname)
        return None

    get_source = get_code

    def create_module(self, spec):
        return self.load_module(spec.name)

    def exec_module(self, module):
        pass


_importer = _SixExMetaPathImporter(__name__)

class _MovedItems(six._LazyModule):
    __path__ = []


_moved_attributes = [
 six.MovedAttribute('ifilter', 'itertools', 'builtins', 'ifilter', 'filter'),
 six.MovedAttribute('imap', 'itertools', 'builtins', 'imap', 'map'),
 six.MovedAttribute('izip', 'itertools', 'builtins', 'izip', 'zip'),
 six.MovedModule('cStringIO', 'cStringIO', 'io'),
 six.MovedModule('StringIO', 'StringIO', 'io')]
for attr in _moved_attributes:
    setattr(_MovedItems, attr.name, attr)
    if isinstance(attr, six.MovedModule):
        _importer._add_module(attr, 'moves.' + attr.name)

del attr
_MovedItems._moved_attributes = _moved_attributes
moves = _MovedItems(__name__ + '.moves')
_importer._add_module(moves, 'moves')
__path__ = []
__package__ = __name__
if globals().get('__spec__') is not None:
    __spec__.submodule_search_locations = []
if sys.meta_path:
    for i, importer in enumerate(sys.meta_path):
        if type(importer).__name__ == '_SixExMetaPathImporter' and importer.name == __name__:
            del sys.meta_path[i]
            break

    del i
    del importer
sys.meta_path.append(_importer)
if six.PY3:

    def compare(x, y):
        return (x > y) - (x < y)


else:

    def compare(x, y):
        return cmp(x, y)