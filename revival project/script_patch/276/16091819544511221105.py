# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/cython/pyximport/pyximport.py
import sys
import os
import glob
import imp
import cython_globals
mod_name = 'pyximport'
PYX_EXT = '.pyx'
PYXDEP_EXT = '.pyxdep'
PYXBLD_EXT = '.pyxbld'
DEBUG_IMPORT = False

def _print(message, args):
    if args:
        message = message % args
    print message


def _debug(message, *args):
    if DEBUG_IMPORT:
        _print(message, args)


def _info(message, *args):
    _print(message, args)


def _load_pyrex(name, filename):
    pass


def get_distutils_extension--- This code section failed: ---

 100       0  LOAD_GLOBAL           0  'handle_special_build'
           3  LOAD_FAST             0  'modname'
           6  LOAD_FAST             1  'pyxfilename'
           9  CALL_FUNCTION_2       2 
          12  UNPACK_SEQUENCE_2     2 
          15  STORE_FAST            3  'extension_mod'
          18  STORE_FAST            4  'setup_args'

 101      21  LOAD_FAST             3  'extension_mod'
          24  POP_JUMP_IF_TRUE    137  'to 137'

 102      27  LOAD_GLOBAL           1  'isinstance'
          30  LOAD_FAST             1  'pyxfilename'
          33  LOAD_GLOBAL           2  'str'
          36  CALL_FUNCTION_2       2 
          39  POP_JUMP_IF_TRUE     66  'to 66'

 105      42  LOAD_FAST             1  'pyxfilename'
          45  LOAD_ATTR             3  'encode'
          48  LOAD_GLOBAL           4  'sys'
          51  LOAD_ATTR             5  'getfilesystemencoding'
          54  CALL_FUNCTION_0       0 
          57  CALL_FUNCTION_1       1 
          60  STORE_FAST            1  'pyxfilename'
          63  JUMP_FORWARD          0  'to 66'
        66_0  COME_FROM                '63'

 106      66  LOAD_CONST            1  -1
          69  LOAD_CONST            2  ('Extension',)
          72  IMPORT_NAME           6  'distutils.extension'
          75  IMPORT_FROM           7  'Extension'
          78  STORE_FAST            5  'Extension'
          81  POP_TOP          

 107      82  LOAD_FAST             5  'Extension'
          85  LOAD_CONST            3  'name'
          88  LOAD_CONST            4  'sources'
          91  LOAD_FAST             1  'pyxfilename'
          94  BUILD_LIST_1          1 
          97  CALL_FUNCTION_512   512 
         100  STORE_FAST            3  'extension_mod'

 108     103  LOAD_FAST             2  'language_level'
         106  LOAD_CONST            0  ''
         109  COMPARE_OP            9  'is-not'
         112  POP_JUMP_IF_FALSE   137  'to 137'

 109     115  BUILD_MAP_1           1 
         118  LOAD_FAST             2  'language_level'
         121  LOAD_CONST            5  'language_level'
         124  STORE_MAP        
         125  LOAD_FAST             3  'extension_mod'
         128  STORE_ATTR            9  'cython_directives'
         131  JUMP_ABSOLUTE       137  'to 137'
         134  JUMP_FORWARD          0  'to 137'
       137_0  COME_FROM                '134'

 110     137  LOAD_FAST             3  'extension_mod'
         140  LOAD_FAST             4  'setup_args'
         143  BUILD_TUPLE_2         2 
         146  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_512' instruction at offset 97


def handle_special_build(modname, pyxfilename):
    special_build = os.path.splitext(pyxfilename)[0] + PYXBLD_EXT
    ext = None
    setup_args = {}
    if os.path.exists(special_build):
        mod = imp.load_source('XXXX', special_build, open(special_build))
        make_ext = getattr(mod, 'make_ext', None)
        if make_ext:
            ext = make_ext(modname, pyxfilename)
        make_setup_args = getattr(mod, 'make_setup_args', None)
        if make_setup_args:
            setup_args = make_setup_args()
        ext.sources = [ os.path.join(os.path.dirname(special_build), source) for source in ext.sources
                      ]
    return (ext, setup_args)


def handle_dependencies(pyxfilename):
    testing = '_test_files' in globals()
    dependfile = os.path.splitext(pyxfilename)[0] + PYXDEP_EXT
    if os.path.exists(dependfile):
        depends = open(dependfile).readlines()
        depends = [ depend.strip() for depend in depends ]
        files = [
         dependfile]
        for depend in depends:
            fullpath = os.path.join(os.path.dirname(dependfile), depend)
            files.extend(glob.glob(fullpath))

        if testing:
            _test_files[:] = []
        for file in files:
            from distutils.dep_util import newer
            if newer(file, pyxfilename):
                _debug('Rebuilding %s because of %s', pyxfilename, file)
                filetime = os.path.getmtime(file)
                os.utime(pyxfilename, (filetime, filetime))
                if testing:
                    _test_files.append(file)


def build_module--- This code section failed: ---

 179       0  LOAD_GLOBAL           0  'handle_dependencies'
           3  LOAD_FAST             1  'pyxfilename'
           6  CALL_FUNCTION_1       1 
           9  POP_TOP          

 181      10  LOAD_GLOBAL           1  'get_distutils_extension'
          13  LOAD_FAST             0  'name'
          16  LOAD_FAST             1  'pyxfilename'
          19  LOAD_FAST             4  'language_level'
          22  CALL_FUNCTION_3       3 
          25  UNPACK_SEQUENCE_2     2 
          28  STORE_FAST            5  'extension_mod'
          31  STORE_FAST            6  'setup_args'

 182      34  LOAD_GLOBAL           2  'pyxargs'
          37  LOAD_ATTR             3  'build_in_temp'
          40  STORE_FAST            7  'build_in_temp'

 183      43  LOAD_GLOBAL           2  'pyxargs'
          46  LOAD_ATTR             4  'setup_args'
          49  LOAD_ATTR             5  'copy'
          52  CALL_FUNCTION_0       0 
          55  STORE_FAST            8  'sargs'

 184      58  LOAD_FAST             8  'sargs'
          61  LOAD_ATTR             6  'update'
          64  LOAD_FAST             6  'setup_args'
          67  CALL_FUNCTION_1       1 
          70  POP_TOP          

 185      71  LOAD_FAST             8  'sargs'
          74  LOAD_ATTR             7  'pop'
          77  LOAD_CONST            1  'build_in_temp'
          80  LOAD_FAST             7  'build_in_temp'
          83  CALL_FUNCTION_2       2 
          86  STORE_FAST            7  'build_in_temp'

 187      89  LOAD_CONST            2  1
          92  LOAD_CONST            3  ('pyxbuild',)
          95  IMPORT_NAME           8  ''
          98  IMPORT_FROM           9  'pyxbuild'
         101  STORE_FAST            9  'pyxbuild'
         104  POP_TOP          

 188     105  LOAD_FAST             9  'pyxbuild'
         108  LOAD_ATTR            10  'pyx_to_dll'
         111  LOAD_FAST             1  'pyxfilename'
         114  LOAD_FAST             5  'extension_mod'
         117  LOAD_CONST            1  'build_in_temp'

 189     120  LOAD_FAST             7  'build_in_temp'
         123  LOAD_CONST            4  'pyxbuild_dir'

 190     126  LOAD_FAST             2  'pyxbuild_dir'
         129  LOAD_CONST            5  'setup_args'

 191     132  LOAD_FAST             8  'sargs'
         135  LOAD_CONST            6  'inplace'

 192     138  LOAD_FAST             3  'inplace'
         141  LOAD_CONST            7  'reload_support'

 193     144  LOAD_GLOBAL           2  'pyxargs'
         147  LOAD_ATTR            11  'reload_support'
         150  CALL_FUNCTION_1282  1282 
         153  STORE_FAST           10  'so_path'

 196     156  LOAD_GLOBAL          12  'os'
         159  LOAD_ATTR            13  'path'
         162  LOAD_ATTR            14  'join'
         165  LOAD_GLOBAL          12  'os'
         168  LOAD_ATTR            13  'path'
         171  LOAD_ATTR            15  'dirname'
         174  LOAD_FAST            10  'so_path'
         177  CALL_FUNCTION_1       1 
         180  CALL_FUNCTION_8       8 
         183  BINARY_ADD       
         184  CALL_FUNCTION_2       2 
         187  STORE_FAST           11  'junkpath'

 197     190  LOAD_GLOBAL          16  'glob'
         193  LOAD_ATTR            16  'glob'
         196  LOAD_FAST            11  'junkpath'
         199  CALL_FUNCTION_1       1 
         202  STORE_FAST           12  'junkstuff'

 198     205  SETUP_LOOP           79  'to 287'
         208  LOAD_FAST            12  'junkstuff'
         211  GET_ITER         
         212  FOR_ITER             71  'to 286'
         215  STORE_FAST           13  'path'

 199     218  LOAD_FAST            13  'path'
         221  LOAD_FAST            10  'so_path'
         224  COMPARE_OP            3  '!='
         227  POP_JUMP_IF_FALSE   212  'to 212'

 200     230  SETUP_EXCEPT         17  'to 250'

 201     233  LOAD_GLOBAL          12  'os'
         236  LOAD_ATTR            17  'remove'
         239  LOAD_FAST            13  'path'
         242  CALL_FUNCTION_1       1 
         245  POP_TOP          
         246  POP_BLOCK        
         247  JUMP_ABSOLUTE       283  'to 283'
       250_0  COME_FROM                '230'

 202     250  DUP_TOP          
         251  LOAD_GLOBAL          18  'IOError'
         254  COMPARE_OP           10  'exception-match'
         257  POP_JUMP_IF_FALSE   279  'to 279'
         260  POP_TOP          
         261  POP_TOP          
         262  POP_TOP          

 203     263  LOAD_GLOBAL          19  '_info'
         266  LOAD_CONST            9  "Couldn't remove %s"
         269  LOAD_FAST            13  'path'
         272  CALL_FUNCTION_2       2 
         275  POP_TOP          
         276  JUMP_ABSOLUTE       283  'to 283'
         279  END_FINALLY      
       280_0  COME_FROM                '279'
         280  JUMP_BACK           212  'to 212'
         283  JUMP_BACK           212  'to 212'
         286  POP_BLOCK        
       287_0  COME_FROM                '205'

 205     287  LOAD_FAST            10  'so_path'
         290  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_8' instruction at offset 180


def load_module--- This code section failed: ---

 210       0  SETUP_EXCEPT        138  'to 141'

 211       3  LOAD_FAST             6  'so_path'
           6  LOAD_CONST            0  ''
           9  COMPARE_OP            8  'is'
          12  POP_JUMP_IF_FALSE    70  'to 70'

 212      15  LOAD_FAST             3  'is_package'
          18  POP_JUMP_IF_FALSE    31  'to 31'

 213      21  POP_JUMP_IF_FALSE     1  'to 1'
          24  BINARY_ADD       
          25  STORE_FAST            7  'module_name'
          28  JUMP_FORWARD          6  'to 37'

 215      31  LOAD_FAST             0  'name'
          34  STORE_FAST            7  'module_name'
        37_0  COME_FROM                '28'

 216      37  LOAD_NAME             1  'build_module'
          40  LOAD_FAST             7  'module_name'
          43  LOAD_FAST             1  'pyxfilename'
          46  LOAD_FAST             2  'pyxbuild_dir'
          49  LOAD_CONST            2  'inplace'

 217      52  LOAD_FAST             4  'build_inplace'
          55  LOAD_CONST            3  'language_level'
          58  LOAD_FAST             5  'language_level'
          61  CALL_FUNCTION_515   515 
          64  STORE_FAST            6  'so_path'
          67  JUMP_FORWARD          0  'to 70'
        70_0  COME_FROM                '67'

 218      70  LOAD_NAME             2  'imp'
          73  LOAD_ATTR             3  'load_dynamic'
          76  LOAD_FAST             0  'name'
          79  LOAD_FAST             6  'so_path'
          82  CALL_FUNCTION_2       2 
          85  STORE_FAST            8  'mod'

 219      88  LOAD_FAST             3  'is_package'
          91  POP_JUMP_IF_FALSE   137  'to 137'
          94  LOAD_NAME             4  'hasattr'
          97  LOAD_FAST             8  'mod'
         100  LOAD_CONST            4  '__path__'
         103  CALL_FUNCTION_2       2 
         106  UNARY_NOT        
       107_0  COME_FROM                '91'
         107  POP_JUMP_IF_FALSE   137  'to 137'

 220     110  LOAD_NAME             5  'os'
         113  LOAD_ATTR             6  'path'
         116  LOAD_ATTR             7  'dirname'
         119  LOAD_FAST             6  'so_path'
         122  CALL_FUNCTION_1       1 
         125  BUILD_LIST_1          1 
         128  LOAD_FAST             8  'mod'
         131  STORE_ATTR            8  '__path__'
         134  JUMP_FORWARD          0  'to 137'
       137_0  COME_FROM                '134'

 221     137  POP_BLOCK        
         138  JUMP_FORWARD        217  'to 358'
       141_0  COME_FROM                '0'

 222     141  DUP_TOP          
         142  LOAD_NAME             9  'Exception'
         145  COMPARE_OP           10  'exception-match'
         148  POP_JUMP_IF_FALSE   357  'to 357'
         151  POP_TOP          
         152  POP_TOP          
         153  POP_TOP          

 223     154  LOAD_NAME            10  'pyxargs'
         157  LOAD_ATTR            11  'load_py_module_on_import_failure'
         160  POP_JUMP_IF_FALSE   199  'to 199'
         163  LOAD_FAST             1  'pyxfilename'
         166  LOAD_ATTR            12  'endswith'
         169  LOAD_CONST            5  '.py'
         172  CALL_FUNCTION_1       1 
       175_0  COME_FROM                '160'
         175  POP_JUMP_IF_FALSE   199  'to 199'

 225     178  LOAD_NAME             2  'imp'
         181  LOAD_ATTR            13  'load_source'
         184  LOAD_FAST             0  'name'
         187  LOAD_FAST             1  'pyxfilename'
         190  CALL_FUNCTION_2       2 
         193  STORE_FAST            8  'mod'

 226     196  JUMP_ABSOLUTE       358  'to 358'

 228     199  LOAD_NAME            14  'sys'
         202  LOAD_ATTR            15  'exc_info'
         205  CALL_FUNCTION_0       0 
         208  LOAD_CONST            6  1
         211  BINARY_SUBSCR    
         212  STORE_FAST            9  'val'

 230     215  LOAD_FAST             9  'val'
         218  PRINT_ITEM       
         219  PRINT_NEWLINE_CONT

 231     220  LOAD_NAME            14  'sys'
         223  LOAD_ATTR            15  'exc_info'
         226  CALL_FUNCTION_0       0 
         229  LOAD_CONST            7  2
         232  BINARY_SUBSCR    
         233  STORE_FAST           10  'tb'

 232     236  LOAD_CONST            8  -1
         239  LOAD_CONST            0  ''
         242  IMPORT_NAME          16  'traceback'
         245  STORE_FAST           11  'traceback'

 233     248  LOAD_NAME            17  'ImportError'
         251  LOAD_CONST            9  'Building module %s failed: %s'

 234     254  LOAD_FAST             0  'name'
         257  LOAD_FAST            11  'traceback'
         260  LOAD_ATTR            18  'format_exception_only'
         263  LOAD_NAME            14  'sys'
         266  LOAD_ATTR            15  'exc_info'
         269  CALL_FUNCTION_0       0 
         272  LOAD_CONST            7  2
         275  SLICE+2          
         276  CALL_FUNCTION_VAR_0     0 
         279  BUILD_TUPLE_2         2 
         282  BINARY_MODULO    
         283  CALL_FUNCTION_1       1 
         286  STORE_FAST           12  'exc'

 235     289  LOAD_NAME            14  'sys'
         292  LOAD_ATTR            19  'version_info'
         295  LOAD_CONST           10  ''
         298  BINARY_SUBSCR    
         299  LOAD_CONST           11  3
         302  COMPARE_OP            5  '>='
         305  POP_JUMP_IF_FALSE   326  'to 326'

 236     308  LOAD_FAST            12  'exc'
         311  LOAD_ATTR            20  'with_traceback'
         314  LOAD_FAST            10  'tb'
         317  CALL_FUNCTION_1       1 
         320  RAISE_VARARGS_1       1 
         323  JUMP_ABSOLUTE       358  'to 358'

 238     326  LOAD_CONST           12  'raise exc, None, tb'
         329  BUILD_MAP_2           2 
         332  LOAD_FAST            12  'exc'
         335  LOAD_CONST           13  'exc'
         338  STORE_MAP        
         339  LOAD_FAST            10  'tb'
         342  LOAD_CONST           14  'tb'
         345  STORE_MAP        
         346  BUILD_TUPLE_2         2 
         349  LOAD_CONST            0  ''
         352  DUP_TOP          
         353  EXEC_STMT        
         354  JUMP_FORWARD          1  'to 358'
         357  END_FINALLY      
       358_0  COME_FROM                '357'
       358_1  COME_FROM                '138'

 239     358  LOAD_FAST             8  'mod'
         361  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 21


class PyxImporter(object):

    def __init__(self, extension=PYX_EXT, pyxbuild_dir=None, inplace=False, language_level=None):
        self.extension = extension
        self.pyxbuild_dir = pyxbuild_dir
        self.inplace = inplace
        self.language_level = language_level

    def find_module(self, fullname, package_path=None):
        if fullname in sys.modules and not pyxargs.reload_support:
            return None
        else:
            try:
                fp, pathname, (ext, mode, ty) = imp.find_module(fullname, package_path)
                if fp:
                    fp.close()
                if pathname and ty == imp.PKG_DIRECTORY:
                    pkg_file = os.path.join(pathname, '__init__' + self.extension)
                    if os.path.isfile(pkg_file):
                        return PyxLoader(fullname, pathname, init_path=pkg_file, pyxbuild_dir=self.pyxbuild_dir, inplace=self.inplace, language_level=self.language_level)
                if pathname and pathname.endswith(self.extension):
                    return PyxLoader(fullname, pathname, pyxbuild_dir=self.pyxbuild_dir, inplace=self.inplace, language_level=self.language_level)
                if ty != imp.C_EXTENSION:
                    return None
                pyxpath = os.path.splitext(pathname)[0] + self.extension
                if os.path.isfile(pyxpath):
                    return PyxLoader(fullname, pyxpath, pyxbuild_dir=self.pyxbuild_dir, inplace=self.inplace, language_level=self.language_level)
            except ImportError:
                pass

            if '.' in fullname:
                mod_parts = fullname.split('.')
                module_name = mod_parts[-1]
            else:
                module_name = fullname
            pyx_module_name = module_name + self.extension
            if package_path:
                paths = package_path
            else:
                paths = sys.path
            join_path = os.path.join
            is_file = os.path.isfile
            is_abs = os.path.isabs
            abspath = os.path.abspath
            sep = os.path.sep
            for path in paths:
                if not path:
                    path = os.getcwd()
                else:
                    if not is_abs(path):
                        path = abspath(path)
                    if is_file(path + sep + pyx_module_name):
                        return PyxLoader(fullname, join_path(path, pyx_module_name), pyxbuild_dir=self.pyxbuild_dir, inplace=self.inplace, language_level=self.language_level)

            _debug('%s not found' % fullname)
            return None


class PyImporter(PyxImporter):

    def __init__(self, pyxbuild_dir=None, inplace=False, language_level=None):
        if language_level is None:
            language_level = sys.version_info[0]
        self.super = super(PyImporter, self)
        self.super.__init__(extension='.py', pyxbuild_dir=pyxbuild_dir, inplace=inplace, language_level=language_level)
        self.uncompilable_modules = {}
        self.blocked_modules = ['Cython', 'pyxbuild', 'pyximport.pyxbuild',
         'distutils.extension', 'distutils.sysconfig']
        return

    def find_module(self, fullname, package_path=None):
        if fullname in sys.modules:
            return
        else:
            if fullname.startswith('Cython.'):
                return
            if fullname in self.blocked_modules:
                return
            if _lib_loader.knows(fullname):
                return _lib_loader
            _debug("trying import of module '%s'", fullname)
            if fullname in self.uncompilable_modules:
                path, last_modified = self.uncompilable_modules[fullname]
                try:
                    new_last_modified = os.stat(path).st_mtime
                    if new_last_modified > last_modified:
                        return
                except OSError:
                    pass

            self.blocked_modules.append(fullname)
            try:
                importer = self.super.find_module(fullname, package_path)
                if importer is not None:
                    if importer.init_path:
                        path = importer.init_path
                        real_name = fullname + '.__init__'
                    else:
                        path = importer.path
                        real_name = fullname
                    _debug('importer found path %s for module %s', path, real_name)
                    try:
                        so_path = build_module(real_name, path, pyxbuild_dir=self.pyxbuild_dir, language_level=self.language_level, inplace=self.inplace)
                        _lib_loader.add_lib(fullname, path, so_path, is_package=bool(importer.init_path))
                        return _lib_loader
                    except Exception:
                        if DEBUG_IMPORT:
                            import traceback
                            traceback.print_exc()
                        try:
                            last_modified = os.stat(path).st_mtime
                        except OSError:
                            last_modified = 0

                        self.uncompilable_modules[fullname] = (
                         path, last_modified)
                        importer = None

            finally:
                self.blocked_modules.pop()

            return importer


class AnnotatedPyImporter(object):

    def __init__(self, extension='.py', pyxbuild_dir=None, inplace=False, language_level=None):
        self.extension = extension
        self.pyxbuild_dir = pyxbuild_dir
        self.inplace = inplace
        self.language_level = language_level

    def find_module(self, fullname, package_path=None):
        if fullname in sys.modules and not pyxargs.reload_support:
            return
        else:
            package_name, sep, module_name = fullname.rpartition('.')
            if sep == '.':
                package = sys.modules[package_name]
                path = package.__path__
            else:
                path = None
            try:
                fp, pathname, (ext, mode, ty) = imp.find_module(module_name, path)
            except ImportError:
                return

            if ty == imp.PKG_DIRECTORY:
                return
            if ty != imp.PY_SOURCE:
                if fp:
                    fp.close()
                return
            is_annotated = False
            for line in fp:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                is_annotated = line.startswith('import cython')
                break

            fp.close()
            if not is_annotated:
                return
            return PyxLoader(fullname, pathname, pyxbuild_dir=self.pyxbuild_dir, inplace=self.inplace, language_level=self.language_level)


class LibLoader(object):

    def __init__(self):
        self._libs = {}

    def load_module(self, fullname):
        try:
            source_path, so_path, is_package = self._libs[fullname]
        except KeyError:
            raise ValueError('invalid module %s' % fullname)

        _debug("Loading shared library module '%s' from %s", fullname, so_path)
        return load_module(fullname, source_path, so_path=so_path, is_package=is_package)

    def add_lib(self, fullname, path, so_path, is_package):
        self._libs[fullname] = (
         path, so_path, is_package)

    def knows(self, fullname):
        return fullname in self._libs


_lib_loader = LibLoader()

class PyxLoader(object):

    def __init__(self, fullname, path, init_path=None, pyxbuild_dir=None, inplace=False, language_level=None):
        _debug('PyxLoader created for loading %s from %s (init path: %s)', fullname, path, init_path)
        self.fullname = fullname
        self.path, self.init_path = path, init_path
        self.pyxbuild_dir = pyxbuild_dir
        self.inplace = inplace
        self.language_level = language_level

    def load_module(self, fullname):
        if self.init_path:
            module = load_module(fullname, self.init_path, self.pyxbuild_dir, is_package=True, build_inplace=self.inplace, language_level=self.language_level)
            module.__path__ = [self.path]
        else:
            module = load_module(fullname, self.path, self.pyxbuild_dir, build_inplace=self.inplace, language_level=self.language_level)
        return module


class PyxArgs(object):
    build_dir = True
    build_in_temp = True
    setup_args = {}


def _have_importers():
    has_py_importer = False
    has_pyx_importer = False
    has_annopy_importer = False
    for importer in sys.meta_path:
        if isinstance(importer, PyxImporter):
            if isinstance(importer, PyImporter):
                has_py_importer = True
            else:
                has_pyx_importer = True
        if isinstance(importer, AnnotatedPyImporter):
            has_annopy_importer = True

    return (has_py_importer, has_pyx_importer, has_annopy_importer)


def install(script_root, pyximport=True, pyimport=False, annopyimport=False, build_dir=None, build_in_temp=True, setup_args=None, reload_support=False, load_py_module_on_import_failure=False, inplace=False, language_level=None):
    global pyxargs
    cython_globals.script_root = script_root
    cython_globals.cython_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    if setup_args is None:
        setup_args = {}
    if not build_dir:
        build_dir = os.path.join(os.path.expanduser('~'), '.pyxbld')
    pyxargs = PyxArgs()
    pyxargs.build_dir = build_dir
    pyxargs.build_in_temp = build_in_temp
    pyxargs.setup_args = (setup_args or {}).copy()
    pyxargs.reload_support = reload_support
    pyxargs.load_py_module_on_import_failure = load_py_module_on_import_failure
    has_py_importer, has_pyx_importer, has_annopy_importer = _have_importers()
    py_importer, pyx_importer, annopy_importer = (None, None, None)
    if pyimport and not has_py_importer:
        py_importer = PyImporter(pyxbuild_dir=build_dir, inplace=inplace, language_level=language_level)
        import Cython.Compiler.Main
        import Cython.Compiler.Pipeline
        import Cython.Compiler.Optimize
        sys.meta_path.insert(0, py_importer)
    if pyximport and not has_pyx_importer:
        pyx_importer = PyxImporter(pyxbuild_dir=build_dir, inplace=inplace, language_level=language_level)
        sys.meta_path.append(pyx_importer)
    if annopyimport and not has_annopy_importer:
        annopy_importer = AnnotatedPyImporter(pyxbuild_dir=build_dir, inplace=inplace, language_level=language_level)
        sys.meta_path.append(annopy_importer)
    return (
     py_importer, pyx_importer, annopy_importer)


def uninstall(py_importer, pyx_importer, annopy_importer):
    try:
        sys.meta_path.remove(py_importer)
    except ValueError:
        pass

    try:
        sys.meta_path.remove(pyx_importer)
    except ValueError:
        pass

    try:
        sys.meta_path.remove(annopy_importer)
    except ValueError:
        pass


def show_docs():
    import __main__
    __main__.__name__ = mod_name
    for name in dir(__main__):
        item = getattr(__main__, name)
        try:
            setattr(item, '__module__', mod_name)
        except (AttributeError, TypeError):
            pass

    help(__main__)


if __name__ == '__main__':
    show_docs()