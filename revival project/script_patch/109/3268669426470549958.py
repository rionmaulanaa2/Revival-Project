# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/redirect_debug.py
from __future__ import absolute_import
from __future__ import print_function
import six
import imp
import time
import marshal
import zlib
import C_file
import sys
import game3d
enable_sleep = False
REDIRECT_DEBUG = True
DEBUG_SET = set([])

def init_global():
    global DEBUG_SET
    try:
        script_strs = C_file.get_res_file('confs/login_script_conf.txt', '')
        if not script_strs:
            return
        script_list = script_strs.split('\n')
        item_list = []
        for item in script_list:
            py_item = item.split('#')[0].strip()
            print(py_item)
            py_item = py_item.replace('"', '').replace(',', '')
            print(py_item)
            if py_item.endswith('.py'):
                item_list.append(py_item)

        DEBUG_SET = set(item_list)
    except Exception as e:
        print('exp is', str(e))


init_global()

def init_rotor--- This code section failed: ---

  43       0  LOAD_CONST            1  'j2h56ogodh3se'
           3  STORE_FAST            0  'asdf_dn'

  44       6  LOAD_CONST            2  '=dziaq.'
           9  STORE_FAST            1  'asdf_dt'

  45      12  LOAD_CONST            3  '|os=5v7!"-234'
          15  STORE_FAST            2  'asdf_df'

  46      18  STORE_FAST            4  'rotor'
          21  BINARY_MULTIPLY  
          22  LOAD_FAST             1  'asdf_dt'
          25  LOAD_FAST             0  'asdf_dn'
          28  BINARY_ADD       
          29  LOAD_FAST             2  'asdf_df'
          32  BINARY_ADD       
          33  LOAD_CONST            5  5
          36  BINARY_MULTIPLY  
          37  BINARY_ADD       
          38  LOAD_CONST            6  '!'
          41  BINARY_ADD       
          42  LOAD_CONST            7  '#'
          45  BINARY_ADD       
          46  LOAD_FAST             1  'asdf_dt'
          49  LOAD_CONST            8  7
          52  BINARY_MULTIPLY  
          53  BINARY_ADD       
          54  LOAD_FAST             2  'asdf_df'
          57  LOAD_CONST            9  2
          60  BINARY_MULTIPLY  
          61  BINARY_ADD       
          62  LOAD_CONST           10  '*'
          65  BINARY_ADD       
          66  LOAD_CONST           11  '&'
          69  BINARY_ADD       
          70  LOAD_CONST           12  "'"
          73  BINARY_ADD       
          74  STORE_FAST            3  'asdf_tm'

  48      77  LOAD_CONST           13  ''
          80  LOAD_CONST            0  ''
          83  IMPORT_NAME           0  'rotor'
          86  STORE_FAST            4  'rotor'

  49      89  LOAD_FAST             4  'rotor'
          92  LOAD_ATTR             1  'newrotor'
          95  LOAD_FAST             3  'asdf_tm'
          98  CALL_FUNCTION_1       1 
         101  STORE_FAST            5  'rot'

  50     104  LOAD_FAST             5  'rot'
         107  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_FAST' instruction at offset 18


def _reverse_string(s):
    l = list(s)
    l = [ six.int2byte(ord(x) ^ 154) for x in l[0:128] ] + l[128:]
    l.reverse()
    return ''.join(l)


class NpkImporter(object):
    rotor = init_rotor()

    def __init__(self, path):
        self._paths = [
         '.', 'lib', 'engine']

    def check_login_redirect(self, path):
        if not REDIRECT_DEBUG:
            return
        if path.endswith('.nxs'):
            path = path.replace('.nxs', '.py')
        if not (path.startswith('./patch/') or path.startswith('./cython/') or path.startswith('./common/uisys/') or path.startswith('lib/') or path.startswith('./mobile/') or path in DEBUG_SET):
            print(path)
            raise

    def find_module_py(self, fullname, path=None):
        fullname = fullname.replace('.', '/')
        fullname_ext = fullname + '.py'
        pkg_name = fullname + '/__init__.py'
        pkg_name = pkg_name if path is None else path + '/' + pkg_name
        for p in self._paths:
            if C_file.find_file(p + '/' + pkg_name, ''):
                return self
            if C_file.find_file(p + '/' + fullname_ext, ''):
                return self

        return

    def find_module_nxs(self, fullname, path=None):
        fullname = fullname.replace('.', '/')
        fullname_ext = fullname + '.nxs'
        pkg_name = fullname + '/__init__.nxs'
        pkg_name = pkg_name if path is None else path + '/' + pkg_name
        import C_file
        for p in self._paths:
            if C_file.find_file(p + '/' + pkg_name, ''):
                return self
            if C_file.find_file(p + '/' + fullname_ext, ''):
                return self

        return

    def find_module(self, fullname, path=None):
        m = self.find_module_py(fullname, path)
        if not m:
            m = self.find_module_nxs(fullname, path)
        return m

    def load_module_py(self, fullname):
        mod_name = fullname
        fullname = fullname.replace('.', '/')
        fullname_ext = fullname + '.py'
        pkg_name = fullname + '/__init__.py'
        path = ''
        is_pkg = False
        for p in self._paths:
            temp = p + '/' + pkg_name
            if C_file.find_file(temp, ''):
                path = temp
                is_pkg = True
                break
            temp = p + '/' + fullname_ext
            if C_file.find_file(temp, ''):
                path = temp
                is_pkg = False
                break

        if path:
            self.check_login_redirect(path)
            data = C_file.get_file(path, '')
            root_dir = game3d.get_script_path()
            import os
            data = compile(data, os.path.join(root_dir, path), 'exec')
            path = None
            if is_pkg:
                path = [
                 '.']
            return C_file.new_module(mod_name, data, path)
        else:
            return

    def load_module_nxs(self, fullname):
        mod_name = fullname
        fullname = fullname.replace('.', '/')
        fullname_ext = fullname + '.nxs'
        pkg_name = fullname + '/__init__.nxs'
        path = ''
        is_pkg = False
        for p in self._paths:
            temp = p + '/' + pkg_name
            if C_file.find_file(temp, ''):
                path = temp
                is_pkg = True
                break
            temp = p + '/' + fullname_ext
            if C_file.find_file(temp, ''):
                path = temp
                is_pkg = False
                break

        if path:
            self.check_login_redirect(path)
            data = C_file.get_file(path, '')
            data = NpkImporter.rotor.decrypt(data)
            data = zlib.decompress(data)
            data = _reverse_string(data)
            data = marshal.loads(data)
            path = None
            if is_pkg:
                path = [
                 '.']
            return C_file.new_module(mod_name, data, path)
        else:
            return

    def load_module(self, fullname):
        if enable_sleep and imp.lock_held():
            imp.release_lock()
            time.sleep(0.001)
            imp.acquire_lock()
        return self.load_module_py(fullname) or self.load_module_nxs(fullname)


sys.path_hooks.append(NpkImporter)