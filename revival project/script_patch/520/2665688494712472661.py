# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/nx_file_logic/io_thread_mgr.py
from __future__ import absolute_import
from __future__ import print_function
import os
import six
import C_file
import game3d
from patch import patch_path

class FileThreadWorker(object):

    def __init__(self):
        super(FileThreadWorker, self).__init__()

    def process(self):
        self._thread_del_steam_old_patch()
        self._init_ext_debug()

    def _init_ext_debug(self):
        ext_debug_mode = False
        try:
            if not hasattr(C_file, 'set_ignore_res_enable'):
                print('[ext_debug_mode] failed: need up to new engine')
                return
            if not hasattr(C_file, 'add_ignore_res_path'):
                print('[ext_debug_mode] failed 2: need up to new engine')
                return
            from patch.patch_utils import MAGIC_STRING
            clipboard_text = game3d.get_clipboard_text()
            if clipboard_text.startswith(MAGIC_STRING):
                import json
                clipboard_text = clipboard_text[len(MAGIC_STRING):]
                magic_conf = json.loads(clipboard_text)
                if 'platform' in magic_conf and magic_conf['platform'] == 'base':
                    from ext_package import ext_decorator
                    ext_decorator.set_ext_debug_mode(True)
                    from common.platform.device_info import DeviceInfo
                    DeviceInfo().update_ext_info()
                    C_file.set_ignore_res_enable(True)
                    ext_debug_mode = True
        except Exception as e:
            print('ext debug init except:', str(e))

        if ext_debug_mode:
            self._thread_process_ext_debug()

    def _thread_del_steam_old_patch(self):
        dir_name = os.path.dirname(game3d.get_doc_dir())
        res_week = os.path.join(dir_name, 'res_week_old')
        res_patch = os.path.join(dir_name, 'res_patch_old')
        script_patch = os.path.join(dir_name, 'script_patch_old')
        script_week = os.path.join(dir_name, 'script_week_old')
        if os.path.exists(res_week) or os.path.exists(res_patch) or os.path.exists(script_patch) or os.path.exists(script_week):
            import threading
            import shutil

            def remove_path(in_remove_path):
                if os.path.exists(in_remove_path):
                    try:
                        shutil.rmtree(in_remove_path, True)
                    except Exception as e:
                        print('rmtree except:', str(e))

            def thread_del():
                remove_path(res_week)
                remove_path(res_patch)
                remove_path(script_patch)
                remove_path(script_week)

            t = threading.Thread(target=thread_del)
            t.setDaemon(True)
            t.start()

    def _thread_process_ext_debug(self):
        flist_path = patch_path.get_flist_path()
        if not os.path.exists(flist_path):
            print('[ext_debug_mode] failed: flist.lst not exists!')
            return False

        def _thread_worder():
            import zlib
            all_ext_num = 0
            all_flist_dict = {}
            with open(flist_path, 'rb') as tmp_file:
                flist_data = tmp_file.read()
            flist_data = zlib.decompress(flist_data)
            flist_data = six.ensure_str(flist_data)
            for line in flist_data.splitlines():
                if not line:
                    continue
                info = line.split('\t')
                all_flist_dict[info[0]] = info

            if all_flist_dict:
                for file_name in all_flist_dict:
                    split_info = all_flist_dict[file_name]
                    if len(split_info) >= 7 and split_info[6] != 'base':
                        res_path = split_info[0].replace('\\', '/')
                        if not res_path.startswith('res/'):
                            continue
                        res_path = res_path[4:]
                        res_path2 = res_path.replace('/', '\\')
                        C_file.add_ignore_res_path(res_path)
                        C_file.add_ignore_res_path(res_path2)
                        all_ext_num += 1

                print('[ext_debug_mode] success, ignore res num:', all_ext_num)
            else:
                print('[ext_debug_mode] failed: has no flist info!')

        import threading
        t = threading.Thread(target=_thread_worder)
        t.setDaemon(True)
        t.start()