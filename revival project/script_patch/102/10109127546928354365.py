# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/record_sprite_usage.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import os
import time
import json
import C_file
import game3d
from common.framework import Singleton
from common.utils.path import get_neox_dir
from logic.gcommon.time_utility import get_date_str, get_server_time, ONE_WEEK_SECONDS, ONE_MINUTE_SECONDS
from logic.gutils.sprite_usage_uploader import SpriteUsageUploader
import game3d
TIME_OUT = 5
FTP_PORT = 8001
FTP_IP = '10.224.40.205'
EFFECT_INFO_FILE_NAME = 'effect_info.json'
TYPE_SPRITE = 0

class UsageRecorder(Singleton):
    ALIAS_NAME = 'usage_recorder'
    SUPPORT_TYPES = {TYPE_SPRITE}

    def init(self):
        self._root_dir = get_neox_dir()
        self._is_uploading = False
        self._collect_cache_lst = []
        self._last_upload_time = 0
        self._upload_usages = {}
        self._update_interval = ONE_MINUTE_SECONDS * 3
        self._hash_2_path_dict = {}
        self.need_show_filename_list = False
        for ky in self.SUPPORT_TYPES:
            self._upload_usages.setdefault(ky, {})

        self.init_uploader_conf()
        global_data.emgr.scene_after_enter_event += self._on_enter_scene

    def init_uploader_conf(self):
        self.uploader_dict = {TYPE_SPRITE: SpriteUsageUploader(self._root_dir)
           }

    def record_sprite_usage(self, plist, path, info={}):
        ty = TYPE_SPRITE
        if plist:
            key = plist
        else:
            key = path
        if not key:
            return
        self._record_usage(ty, key, info)

    def normalize_path(self, p):
        windows_p = os.path.normpath(p)
        return windows_p.replace('\\', '/')

    def _record_usage(self, ty, key, info):
        if not key:
            return
        nor_path = self.normalize_path(key)
        key = game3d.calc_filename_hash64(nor_path)
        if self._is_uploading:
            self._collect_cache_lst.append((ty, key, info))
            return
        self._upload_usages[ty][key] = info
        if global_data.is_inner_server:
            self._hash_2_path_dict[key] = nor_path

    def _dump_and_upload(self):
        if not self._upload_usages:
            if global_data.is_inner_server:
                print('[UsageRecord] no upload usages')
            return
        if self._is_uploading:
            print('[UsageRecord] is_uploading')
            return
        t = int(get_server_time())
        if t - self._last_upload_time < self._update_interval:
            if global_data.is_inner_server:
                print('[UsageRecord] last upload is within 3 mins, so no upload')
            return
        if global_data.is_inner_server:
            print('[UsageRecord] start upload')
        for ty in self.SUPPORT_TYPES:
            ty_upload_usages = self._upload_usages[ty]
            if len(ty_upload_usages) < 20:
                if global_data.is_inner_server:
                    print('[UsageRecord] too few records, so no upload')
                continue
            uploader = self.uploader_dict.get(ty)
            if uploader:
                self._is_uploading = True

                def uploader_callback(ret, upload_usages_hashed, all_uploaded_usage):
                    self._is_uploading = False
                    if global_data.is_inner_server and self.need_show_filename_list:
                        real_path_dict = {}
                        for f in upload_usages_hashed:
                            if six_ex.long_type(f) in self._hash_2_path_dict:
                                real_path_dict[self._hash_2_path_dict[six_ex.long_type(f)]] = f

                        print('[UsageRecord] all real path ', real_path_dict)
                    self.on_finish_upload(ret, ty)

                uploader.upload(ty_upload_usages, uploader_callback)

    def _upload_file_inner(self, log_path):
        pass

    def on_finish_upload(self, ret, ty):
        if global_data.is_inner_server:
            print('[UsageRecord] on_finish_upload', ret, ty)
        if ret:
            t = int(get_server_time())
            self._last_upload_time = t
            self._upload_usages[ty] = {}
            self._hash_2_path_dict = {}
            for effect_collect_info in self._collect_cache_lst:
                ty, key, info = effect_collect_info
                self._record_usage(ty, key, info)

            self._collect_cache_lst = []

    def _on_enter_scene(self, *args):
        from logic.gcommon.common_const.scene_const import SCENE_LOBBY
        cur_scene = global_data.game_mgr.scene
        if cur_scene.scene_type != SCENE_LOBBY:
            return
        print('_on_enter_scene dump and upload')
        self._dump_and_upload()

    def on_finalize(self):
        self.uploader_dict = {}

    def view_all_upload_usages(self):
        try:
            from mobile.common.JsonConfig import parse
            uploaded_json_path = os.path.join(self._root_dir, 'sp_uploaded_usages.json')
            if os.path.exists(uploaded_json_path):
                all_uploaded_usage = parse(uploaded_json_path)
            else:
                all_uploaded_usage = {}
        except Exception as e:
            log_error('[SpriteUsageUploader] get all uploaded error: %s' % str(e))
            all_uploaded_usage = {}

        self.view_what_is_the_content(set([ six_ex.long_type(i) for i in six_ex.keys(all_uploaded_usage) ]))

    def view_what_is_the_content(self, _usage_set=None):
        if _usage_set is None:
            _usage_set = set(six_ex.keys(self._upload_usages[TYPE_SPRITE]))
        if not _usage_set:
            print('there is no content to be reverted')
            return
        else:
            _useful_info = {}
            import logic
            _src_path = os.path.abspath(logic.__path__[0] + os.path.sep + '..' + os.path.sep + '..')
            res_paths = ['res/gui', 'res_cn/gui']

            def check_in_dict(whole_path):
                whole_path = self.normalize_path(whole_path)
                for res_path_name in res_paths:
                    if res_path_name in whole_path:
                        rel_path = 'gui' + os.path.sep + os.path.relpath(whole_path, _src_path + os.path.sep + res_path_name)
                        rel_path = self.normalize_path(rel_path)
                        path_key = game3d.calc_filename_hash64(rel_path)
                        if path_key in _usage_set:
                            _useful_info[rel_path] = path_key

            from tools.json_tools.for_each_json import for_file_in_res_do
            for_file_in_res_do(check_in_dict, dir_list=res_paths)
            print('_useful_info', _useful_info)
            return