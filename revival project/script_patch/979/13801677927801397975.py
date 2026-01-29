# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/test_utils.py
from __future__ import absolute_import
from __future__ import print_function
import C_file

def add_ignore_res_path(path):
    if not hasattr(C_file, 'add_ignore_res_path'):
        return
    paths = _get_ignore_path_equivalents(path)
    for p in paths:
        C_file.add_ignore_res_path(p)


def remove_ignore_res_path(path):
    if not hasattr(C_file, 'remove_ignore_res_path'):
        return
    paths = _get_ignore_path_equivalents(path)
    for p in paths:
        C_file.remove_ignore_res_path(p)


def clear_ignore_res_path():
    if not hasattr(C_file, 'clear_ignore_res_path'):
        return
    C_file.clear_ignore_res_path()


def is_res_path_ignore(path):
    if not hasattr(C_file, 'is_res_path_ignore'):
        return False
    paths = _get_ignore_path_equivalents(path)
    for p in paths:
        if C_file.is_res_path_ignore(p):
            return True
    else:
        return False


def is_res_path_loaded_ever(path):
    if not hasattr(C_file, 'is_res_path_loaded_ever'):
        return False
    paths = _get_ignore_path_equivalents(path)
    for p in paths:
        if C_file.is_res_path_loaded_ever(p):
            return True
    else:
        return False


def clear_res_paths_loaded_ever_info():
    if not hasattr(C_file, 'clear_res_paths_loaded_ever_info'):
        return
    C_file.clear_res_paths_loaded_ever_info()


def set_collect_res_loaded_ever_switch(on):
    if not hasattr(C_file, 'set_collect_res_loaded_ever_switch'):
        return
    C_file.set_collect_res_loaded_ever_switch(on)


def get_collect_res_loaded_ever_switch():
    if not hasattr(C_file, 'get_collect_res_loaded_ever_switch'):
        return False
    return C_file.get_collect_res_loaded_ever_switch()


def _get_ignore_path_equivalents(path):
    path_set = set()
    path_set.add(path)
    if _is_tex_ignore_path(path):
        path_set = path_set | _get_tex_ignore_path_equivalents(path)
    for path in path_set:
        path_set = path_set | _get_ignore_path_delimiter_equivalents(path)

    return path_set


dynamic_tex_exts = ('.tga', '.pvr', '.ktx', '.dds', '.png')

def _is_tex_ignore_path(path):
    for ext in dynamic_tex_exts:
        if path.find(ext) != -1:
            return True
    else:
        return False


def _get_tex_ignore_path_equivalents(path):
    ret_set = set()
    ret_set.add(path)
    dot_idx = path.rfind('.')
    if dot_idx != -1:
        wo_ext = path[:dot_idx]
        if wo_ext:
            for ext in dynamic_tex_exts:
                ret_set.add(wo_ext + ext)

            from patch.patch_utils import MID_END_SUBFIX
            ret_set.add(wo_ext + '_etc2' + '.ktx')
    return ret_set


def _get_ignore_path_delimiter_equivalents(path):
    ret_set = set()
    ret_set.add(path)
    ret_set.add(path.replace('\\', '/'))
    ret_set.add(path.replace('/', '\\'))
    return ret_set


def ext_mode():
    import os
    import zlib
    from patch import patch_path
    from ext_package import ext_decorator
    ext_decorator.set_ext_debug_mode(True)
    flist_path = patch_path.get_flist_path()
    if not os.path.exists(flist_path):
        print('[ext_mode] failed: file {} not exists'.format(flist_path))
        return
    if not hasattr(C_file, 'set_ignore_res_enable'):
        print('[ext_mode] failed: need up to new engine')
        return
    C_file.set_ignore_res_enable(True)
    all_num = 0
    with open(flist_path, 'rb') as tmp_f:
        f_data = tmp_f.read()
        f_data = zlib.decompress(f_data)
        for line in f_data.splitlines():
            if not line:
                continue
            f_info = line.split('\t')
            if len(f_info) >= 7 and f_info[6] != 'base':
                res_path = f_info[0].replace('\\', '/')
                if not res_path.startswith('res/'):
                    continue
                res_path = res_path[4:]
                res_path2 = res_path.replace('/', '\\')
                C_file.add_ignore_res_path(res_path)
                C_file.add_ignore_res_path(res_path2)
                all_num += 1

    print('[ext_mode] success, ignore res num:', all_num)