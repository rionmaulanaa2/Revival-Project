# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/package_utils.py
from __future__ import absolute_import
from __future__ import print_function
import os
import game3d
import six.moves.builtins
import C_file
DOC_DIR = game3d.get_doc_dir()
GAME_FLAG_PATH = os.path.join(DOC_DIR, 'game_flag')
BIN_PATCH_FLAG_PATH = os.path.join(DOC_DIR, 'bin_patch_flag')
GAME_NO_INITED = -1
GAME_INIT_WITH_NPK = 0
GAME_INIT_WITH_PATCH = 1
GAME_INIT_MODE_FLAG = os.path.join(DOC_DIR, 'game_init_mode_flag')
NPK_FLAG_PATH = os.path.join(DOC_DIR, 'npk_res_flag')
REVERTING = False
MINI_PACKAGE_FLAG = bool(C_file.find_res_file('mini_package.flag', ''))

def check_new_package():
    try:
        if not os.path.exists(GAME_FLAG_PATH):
            six.moves.builtins.__dict__['NEW_PACKAGE_FLAG'] = True
            return True
        with open(GAME_FLAG_PATH, 'r') as f:
            flag = f.read()
        if flag != str(game3d.get_engine_version()):
            six.moves.builtins.__dict__['NEW_PACKAGE_FLAG'] = True
            return True
        return False
    except Exception as e:
        print('check new package error, Exception is', str(e))
        six.moves.builtins.__dict__['NEW_PACKAGE_FLAG'] = True
        return True


def modify_package_info():
    six.moves.builtins.__dict__['NEW_PACKAGE_FLAG'] = False
    try:
        dirname = os.path.dirname(GAME_FLAG_PATH)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(GAME_FLAG_PATH, 'w') as tmp_file:
            tmp_file.write(str(game3d.get_engine_version()))
    except Exception as e:
        import exception_hook
        exception_hook.post_error('[new_modify_package_info] write gameflag error {}'.format(str(e)))


def reset_package_info():
    six.moves.builtins.__dict__['NEW_PACKAGE_FLAG'] = False
    with open(GAME_FLAG_PATH, 'w') as tmp_file:
        tmp_file.write(str(0))


def modify_npk_res_mark(npk_version):
    with open(NPK_FLAG_PATH, 'w') as tmp_file:
        tmp_file.write(str(npk_version))


def write_bin_patch_flag():
    pass


def get_game_init_mode():
    try:
        if not os.path.exists(GAME_INIT_MODE_FLAG):
            return GAME_NO_INITED
        with open(GAME_INIT_MODE_FLAG, 'r') as f:
            flag = f.read()
        return int(flag)
    except Exception as e:
        print('[get_game_init_mode] error:{}'.format(str(e)))
        return GAME_NO_INITED


def set_game_init_mode(code):
    if code not in (GAME_NO_INITED, GAME_INIT_WITH_NPK, GAME_INIT_WITH_PATCH):
        return
    try:
        if os.path.exists(GAME_INIT_MODE_FLAG):
            return
        dir_name = os.path.dirname(GAME_INIT_MODE_FLAG)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(GAME_INIT_MODE_FLAG, 'w') as tmp_file:
            tmp_file.write(str(code))
    except Exception as e:
        import exception_hook
        exception_hook.post_error('[set_game_init_mode] error:{}'.format(str(e)))


def can_set_game_init_mode():
    return not os.path.exists(GAME_INIT_MODE_FLAG)


def del_game_init_mode_file():
    try:
        if os.path.exists(GAME_INIT_MODE_FLAG):
            os.remove(GAME_INIT_MODE_FLAG)
    except Exception as e:
        print('[del_game_init_mode_file] error:{}'.format(str(e)))