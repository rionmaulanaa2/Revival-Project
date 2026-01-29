# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/patch_npk_before.py
from __future__ import absolute_import
from __future__ import print_function
import os
import json
import zlib
import C_file
import game3d
import six.moves.builtins
PN_SCRIPT_NAME = 'p_script.npk'
LOADER_TAG = 'patch_npk'
SCRIPT_LOADER_TAG = 'script_patch_npk'
PATCH_NPK_FOLDER = 'patch_npk'
PATCH_NPK_INFO_FILENAME = 'patch_npk_info.config'

def get_nx_dir():
    doc_dir = game3d.get_doc_dir()
    if game3d.get_platform() == game3d.PLATFORM_WIN32:
        doc_dir = os.path.dirname(doc_dir)
    elif game3d.get_platform() == game3d.PLATFORM_ANDROID:
        doc_dir = os.path.dirname(doc_dir)
    return doc_dir


def get_patch_npk_dir():
    return os.path.join(get_nx_dir(), PATCH_NPK_FOLDER)


def get_patch_npk_info_file_path():
    npk_dir = get_patch_npk_dir()
    return os.path.join(npk_dir, PATCH_NPK_INFO_FILENAME)


def _insert_patch_npk_before_patch():
    root_dir = get_patch_npk_dir()
    info_path = get_patch_npk_info_file_path()
    if not os.path.exists(info_path):
        print('[patch_npk_before] has no patch npk config')
        return True
    all_res_name_lst = set()
    script_exist = False
    with open(info_path, 'rb') as tmp_file:
        info_data = tmp_file.read()
        info = json.loads(zlib.decompress(info_data))
        for npk_name in info:
            npk_path = os.path.join(root_dir, npk_name)
            record_size = int(info[npk_name].get('size', 0))
            if os.path.exists(npk_path):
                real_size = os.path.getsize(npk_path)
                if int(real_size) != record_size:
                    print('[patch_npk_before] size not match:{} {} {}'.format(npk_name, record_size, real_size))
                    return False
            else:
                print('[patch_npk_before] npk:{} recorded but not exist'.format(npk_name))
                return False
            if npk_name == PN_SCRIPT_NAME:
                script_exist = True
            else:
                all_res_name_lst.add(npk_name)

    print('[patch_npk_before] res:{} script:{}'.format(all_res_name_lst, script_exist))
    try:
        file_name_lst = os.listdir(root_dir)
        for file_name in file_name_lst:
            if file_name.endswith('.npk') and file_name not in all_res_name_lst and file_name != PN_SCRIPT_NAME:
                real_npk_path = os.path.join(root_dir, file_name)
                os.remove(real_npk_path)

    except Exception as e:
        print('[patch_npk_before] remove not record npk except:{}'.format(str(e)))

    C_file.del_fileloader_by_tag(LOADER_TAG)
    C_file.del_fileloader_by_tag(SCRIPT_LOADER_TAG)
    res_pos = 1 if six.moves.builtins.__dict__.get('res_debug', False) else 0
    for npk_name in all_res_name_lst:
        res_npk_path = os.path.join(root_dir, npk_name)
        ret_code = C_file.insert_res_npk_loader(res_npk_path[:-4], LOADER_TAG, 0, res_pos)
        if ret_code < 0:
            print('[ERROR] [patch_npk_before] add res npk loader:{} ret:{}'.format(res_npk_path, ret_code))
            return False
        print('[patch_npk_before] insert res npk loader:{} success'.format(res_npk_path))

    for npk_name in all_res_name_lst:
        flist_path = '{}_flist.txt'.format(npk_name[:-4])
        flist_exists = C_file.find_res_file(flist_path, '')
        if not flist_exists:
            print('[ERROR] [patch_npk_before] insert loader {}, but flist not exists'.format(npk_name))
            return False

    if six.moves.builtins.__dict__.get('script_debug', False):
        script_pos = 1 if 1 else 0
        if script_exist:
            script_npk_path = os.path.join(root_dir, PN_SCRIPT_NAME)
            ret_code = C_file.insert_script_npk_loader(script_npk_path[:-4], SCRIPT_LOADER_TAG, 0, script_pos)
            if ret_code < 0:
                print('[ERROR] [patch_npk_before] add script npk loader:{} ret_code:{}'.format(script_npk_path, ret_code))
                return False
            print('[patch_npk_before] insert script npk loader:{} success'.format(script_npk_path))
            flist_exists = C_file.find_file('p_script_flist.txt', '')
            flist_exists or print('[ERROR] [patch_npk_before] insert script loader, but flist not exists')
            return False
    return True


def insert_patch_npk_before_patch():
    six.moves.builtins.__dict__['PATCH_NPK_ACTIVE'] = False
    try:
        ret = _insert_patch_npk_before_patch()
    except Exception as e:
        print('[insert npk loader] except:', str(e))
        ret = False

    if not ret:
        try:
            six.moves.builtins.__dict__['PATCH_NPK_ACTIVE'] = False
            res_ret = C_file.del_fileloader_by_tag(LOADER_TAG)
            script_ret = C_file.del_fileloader_by_tag(SCRIPT_LOADER_TAG)
            print('[patch_npk_before] insert fail, del loader ret:{} {}'.format(res_ret, script_ret))
        except Exception as e:
            print('[patch_npk_before] del_fileloader_by_tag except:', str(e))

        try:
            from . import patch_path
            saved_flist_path = patch_path.get_flist_path()
            if os.path.exists(saved_flist_path):
                os.remove(saved_flist_path)
        except Exception as e:
            print('[patch_npk_before] remove flist except:', str(e))

    else:
        six.moves.builtins.__dict__['PATCH_NPK_ACTIVE'] = True
    return ret