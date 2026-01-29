# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/res_verification.py
from __future__ import absolute_import
from __future__ import print_function
import six
import game3d
from patch import patch_utils
from common.framework import SingletonBase

def _get_patched_files():
    patched_files = {}
    try:
        import C_file
        from patch import patch_path
        import zlib
        import time
        start_time = time.time()
        org_flist_data = C_file.get_res_file(patch_path.ORG_FLIST_FILEPATH, '')
        with open(patch_path.get_rw_path(patch_path.FILELIST_FILEPATH), 'rb') as tmp_f:
            flist_data = tmp_f.read()
        flist_data = zlib.decompress(flist_data)
        org_flist = org_flist_data.split('\n')
        flist = flist_data.split('\n')
        org_dict = {}
        flist_dict = {}
        for finfo in flist:
            if not finfo:
                continue
            finfo = finfo.split('\t')
            flist_dict[finfo[0]] = finfo[1]

        for finfo in org_flist:
            if not finfo:
                continue
            finfo = finfo.split('\t')
            org_dict[finfo[0]] = finfo[1]

        for k, v in six.iteritems(flist_dict):
            if k not in org_dict or v != org_dict[k]:
                patched_files[k] = v

        end_time = time.time()
        print('get patched file list cost time: {} s'.format(end_time - start_time))
    except Exception as e:
        print('init flist with error', str(e))

    return patched_files


RES_BUILTIN_LIST = 'res_patch/res_builtin.lst'

class ResVerifier(SingletonBase):

    def init(self):
        self._watch_list = [
         'res/custom_uniforms.xml',
         'script/patch/patch_npk.nxs']
        self._dirty_list = {}
        self._patched_files = {}

    def load(self):
        import zlib
        import C_file
        import os.path
        from patch import patch_path
        full_file = patch_path.get_rw_path(RES_BUILTIN_LIST)
        if os.path.exists(full_file):
            with open(full_file, 'rb') as f:
                zip_data = f.read()
                str_data = zlib.decompress(zip_data)
                self._load(str_data)

    def calc_patched_files(self):
        self._patched_files = _get_patched_files()

    def verify(self):
        patched_files = self._patched_files
        ret = True
        for item in self._watch_list:
            if item in patched_files and self._is_expired(item, patched_files[item]):
                self._update(item, patched_files[item])
                ret = False

        return ret

    def save(self):
        import zlib
        import os
        from patch import patch_path
        str_data = self._save()
        zip_data = zlib.compress(str_data)
        full_path = patch_path.get_rw_path(RES_BUILTIN_LIST)
        dir_name = os.path.dirname(full_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(full_path, 'wb') as f:
            f.write(zip_data)

    def clear(self):
        self._dirty_list = {}
        self._patched_files = {}

    def _load(self, str_data):
        self._dirty_list = {}
        for line in str_data.split('\n'):
            filename, crc = line.strip().split('\t')
            self._dirty_list[filename] = [crc, crc]

    def _is_expired(self, filename, crc):
        return filename not in self._dirty_list or self._dirty_list[filename][0] != crc

    def _update(self, filename, crc):
        self._dirty_list[filename] = [
         self._dirty_list.get(filename, ('0', '0'))[0], crc]

    def _save(self):
        lines = []
        for k, v in six.iteritems(self._dirty_list):
            lines.append('{}\t{}'.format(k, v[1]))

        return '\n'.join(lines)


class ResVerifierNew(object):

    def __init__(self):
        super(ResVerifierNew, self).__init__()
        self._watch_list = [
         'res/custom_uniforms.xml',
         'script/patch/patch_npk.nxs']

    def is_need_restart(self):
        record_patched_files = patch_utils.get_patched_file_dict()
        if record_patched_files is None:
            return False
        else:
            for item in self._watch_list:
                if item in record_patched_files:
                    return True

            return False


def check_need_restart():
    if hasattr(patch_utils, 'get_patched_file_dict'):
        verifier = ResVerifierNew()
        return verifier.is_need_restart()
    try:
        verifier = ResVerifier()
        verifier.load()
        verifier.calc_patched_files()
        is_need_restart = not verifier.verify()
        if is_need_restart:
            verifier.save()
            from patch import patch_const
            if hasattr(patch_const, 'ENABLE_PATCH_NPK') and patch_const.ENABLE_PATCH_NPK:
                import os
                doc_dir = game3d.get_doc_dir()
                tidy_flag_patch = os.path.join(doc_dir, 'need_tidy_flag')
                try:
                    if not os.path.exists(tidy_flag_patch):
                        with open(tidy_flag_patch, 'wb') as tmp_file:
                            tmp_file.write('1')
                except Exception as e:
                    print('[Except] save tidy flag except:', str(e))

            verifier.load()
            if not verifier.verify():
                log_error('save verify list failed')
                is_need_restart = False
        verifier.clear()
        return is_need_restart
    except Exception as e:
        log_error(str(e))
        return False


def restart():
    global_data.game_mgr.try_restart_app()