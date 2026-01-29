# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/cythonfilter.py
from __future__ import absolute_import
from __future__ import print_function
import six
import os
import zlib
import version
import six.moves.builtins
from patch import patch_path
ENABLE_CYTHON_IN_DEV = True

class CythonFilter(object):

    def __init__(self):
        self._cython_modules = set()
        script_fdict = six.moves.builtins.__dict__.get('SCRIPT_FLIST_DICT', {})
        self._script_set = {}
        self.init_script_list(script_fdict)
        self.load_from_whitelist()

    def load_flist(self, flist_name, fliter_prefix, compressed=False):
        import C_file
        ret_dict = {}
        try:
            flist_data = ''
            if compressed:
                flist = open(patch_path.get_rw_path(flist_name), 'rb').read()
                flist_data = zlib.decompress(flist)
            else:
                flist_data = C_file.get_res_file(flist_name, '')
            flist_data = flist_data.split('\n')
            prefix_len = len(fliter_prefix)
            for finfo in flist_data:
                if not finfo:
                    continue
                if fliter_prefix and not finfo.startswith(fliter_prefix):
                    continue
                finfo = finfo[prefix_len:]
                finfo = finfo.split('\t')
                ret_dict[finfo[0]] = finfo

        except Exception as e:
            print('exception', str(e))
            return {}

        return ret_dict

    def init_script_list(self, fdict):
        subfix = len('.nxs')
        self._script_set = {}
        for k, v in six.iteritems(fdict):
            self._script_set[k[:-subfix].replace('/', '.')] = v[1]

    def add_changed_file_recursive(self, modname, cython_ref, ret_set):
        if modname not in ret_set:
            ret_set.add(modname)
            for ref_cython in cython_ref.get(modname.split('.')[-1], []):
                self.add_changed_file_recursive(ref_cython, cython_ref, ret_set)

    def load_from_whitelist(self):
        try:
            script_v = int(version.get_script_version())
        except Exception as e:
            print('[Except] get script version except:{}'.format(str(e)))
            script_v = 0

        patch_flist_path = patch_path.get_flist_path()
        flist_exists = os.path.exists(patch_flist_path)
        if not flist_exists and script_v > 0:
            return
        try:
            from cython_scripts import PyInit__cython_modules
            m = PyInit__cython_modules()
            cython_filter = m.cython_filter
            cython_ref = m.cython_ref
        except ImportError:
            return

        if cython_filter and not isinstance(cython_filter[0], tuple):
            return
        check_stage = 0
        check_cython_crc = ''
        check_mode_name = 'logic.gcommon.skill.client.SkillBase'
        if not self._script_set:
            if ENABLE_CYTHON_IN_DEV:
                for modname, crc in cython_filter:
                    if modname:
                        self._cython_modules.add(modname)
                        if modname == check_mode_name:
                            check_cython_crc = crc
                            check_stage = 0

        else:
            changed_cython_set = set()
            for modname, crc in cython_filter:
                if modname and self._script_set.get(modname, crc) != crc:
                    self.add_changed_file_recursive(modname, cython_ref, changed_cython_set)

        for modname, crc in cython_filter:
            if modname and modname not in changed_cython_set:
                self._cython_modules.add(modname)
                if modname == check_mode_name:
                    check_cython_crc = crc
                    check_stage = 1

        try:

            def get_comparable_int_ver(ver_str):
                num0, num1, num2 = ver_str.split('.')
                const_factor = 100000
                return int(num0) * const_factor * const_factor + int(num1) * const_factor + int(num2)

            import game3d
            cmp_ver_str = '1.0.15353'
            now_engine_v = version.get_engine_version()
            need_up_info = get_comparable_int_ver(now_engine_v) <= get_comparable_int_ver(cmp_ver_str)
            if need_up_info and game3d.is_release_version() and check_mode_name in self._cython_modules:
                from ext_package.ext_package_utils import other_err_log
                patch_crc = self._script_set.get(check_mode_name, '')
                other_err_log('CythonEventNotifier_V2', 'crc {}:{}, script_v:{} engine:{} stage:{} flist:{}'.format(patch_crc, check_cython_crc, script_v, now_engine_v, check_stage, flist_exists))
        except Exception as e:
            print('upload CythonEventNotifier except:{}'.format(str(e)))

        if self._cython_modules:
            patch_set = self.get_py_in_patch()
            self._cython_modules.difference_update(patch_set)
        for mod in self._cython_modules:
            pass

    def get_py_in_patch(self):
        return {
         'common.event_notifier'}

    def filter(self, fullname):
        return fullname in self._cython_modules