# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/manager_agents/IOManagerAgent.py
from __future__ import absolute_import
from __future__ import print_function
import os
import time
import C_file
import game3d
import six.moves.builtins
from patch import patch_path
from logic.manager_agents import ManagerAgentBase
SCRIPT_PREFIX_LEN = len(patch_path.SCRIPT_PREFIX)
RES_PREFIX_LEN = len(patch_path.RES_PREFIX)
LOGIC_PROCESS_NUM = 1200

class IOManagerAgent(ManagerAgentBase.ManagerAgentBase):
    ALIAS_NAME = 'io_mgr_agent'

    def init(self, *args):
        super(IOManagerAgent, self).init(False, *args)
        self._init_gen = None
        self._ext_debug_mode = False
        self.init_finished_time = time.time()
        self._org_flist = {}
        self._patch_flist_dict = {}
        self._del_steam_old_patch()
        self._init_ext_debug()
        ret = self.init_indexed_patch_cache()
        if not ret:
            self.need_update = False
            self._clear_dict()
        else:
            self.need_update = True
            self._init_gen = self._process_flist()
        return

    def _init_ext_debug(self):
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
                    self._ext_debug_mode = True
        except Exception as e:
            print('ext debug init except:', str(e))

    def _del_steam_old_patch(self):
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

    def init_indexed_patch_cache(self):
        self.patched_num = 0
        self.unpatched_num = 0
        if global_data.feature_mgr.is_support_insert_file_cache():
            if not C_file.find_res_file(patch_path.ORG_FLIST_FILEPATH, ''):
                return False
            self._org_flist = six.moves.builtins.__dict__.get('ORT_FLIST_DICT', None)
            self._patch_flist_dict = six.moves.builtins.__dict__.get('PATCH_FLIST_DICT', None)
            if not self._org_flist or not self._patch_flist_dict:
                return False
            return True
        else:
            return False
            return

    def get_ext_name(self, f_info):
        if len(f_info) >= 7:
            return f_info[6]
        else:
            return 'base'

    def _process_flist(self):
        from patch import patch_const
        enable_patch_npk = patch_const.ENABLE_PATCH_NPK if hasattr(patch_const, 'ENABLE_PATCH_NPK') else False
        if not self._ext_debug_mode and enable_patch_npk:
            self._clear_dict()
            yield True
        from ext_package import ext_package_utils
        is_real_ext = ext_package_utils.is_real_ext_package()
        if is_real_ext:
            from ext_package import ext_package_manager
            active_ext_name_lst = ext_package_manager.get_ext_package_instance().get_active_ext_name_lst()
            needed_ext_lst = ext_package_utils.get_package_need_ext()
        else:
            active_ext_name_lst = []
            needed_ext_lst = []
        all_ext_num = 0
        all_process_num = 0
        patch_flist_dict = self._patch_flist_dict
        for file_name in patch_flist_dict:
            split_info = patch_flist_dict[file_name]
            if is_real_ext:
                e_name = self.get_ext_name(split_info)
                if e_name not in needed_ext_lst or e_name in active_ext_name_lst:
                    self._update_patched_info(split_info)
            else:
                self._update_patched_info(split_info)
            if self._ext_debug_mode and len(split_info) >= 7 and split_info[6] != 'base':
                res_path = split_info[0].replace('\\', '/')
                if not res_path.startswith('res/'):
                    continue
                res_path = res_path[4:]
                res_path2 = res_path.replace('/', '\\')
                C_file.add_ignore_res_path(res_path)
                C_file.add_ignore_res_path(res_path2)
                all_ext_num += 1
            all_process_num += 1
            if all_process_num > LOGIC_PROCESS_NUM:
                all_process_num = 0
                yield False

        if self._ext_debug_mode:
            print('[ext_debug_mode] success, ignore res num:', all_ext_num)
        print('[IO_mgr] patched:{}, un_patched:{}'.format(self.patched_num, self.unpatched_num))
        print('[IO_mgr] all org:{}, all_patch:{}'.format(len(self._org_flist), len(self._patch_flist_dict)))
        self._clear_dict()
        yield True

    def _update_patched_info(self, split_info):
        file_name = split_info[0]
        if file_name not in self._org_flist:
            self.register_filename(file_name, True)
        elif int(split_info[1]) != int(self._org_flist[file_name][1]):
            self.register_filename(file_name, True)
        else:
            self.register_filename(file_name, False)

    def register_filename(self, filename, is_valid):
        if filename.startswith(patch_path.RES_PREFIX):
            C_file.insert_file_cache_by_tag('patch', filename[RES_PREFIX_LEN:].replace('/', '\\'), C_file.FILE_TYPE_RES, is_valid)
        elif filename.startswith(patch_path.SCRIPT_PREFIX):
            C_file.insert_file_cache_by_tag('patch', filename[SCRIPT_PREFIX_LEN:].replace('/', '\\'), C_file.FILE_TYPE_SCRIPT, is_valid)

    def _clear_dict(self):
        try:
            for dict_name in ('ORT_FLIST_DICT', 'PATCH_FLIST_DICT'):
                if dict_name in six.moves.builtins.__dict__:
                    six.moves.builtins.__dict__[dict_name] = None
                    del six.moves.builtins.__dict__[dict_name]

            self._org_flist = {}
            self._patch_flist_dict = {}
        except Exception as e:
            print('[io_mgr] clear data except:', str(e))

        return

    def on_update(self, dt):
        try:
            if self._init_gen is not None:
                ret = next(self._init_gen)
                if ret:
                    self._init_gen = None
                    self.need_update = False
                else:
                    return
        except Exception as e:
            print('[IO_mgr] gen except:', str(e))
            self.need_update = False
            self._init_gen = None
            self._clear_dict()

        return