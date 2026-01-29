# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/loading/loadwrapper.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from common.algorithm import resloader
from logic.gutils.shader_warmup import ShaderWarmup
import data.preimport
import six.moves.builtins
import time
import render
from logic.client.const import game_mode_const
from logic.vscene import progress
from logic.gcommon import time_utility
PY_LOAD_PER_FRAME = 5
EFFECT_INFO_FILE_NAME = 'effect_info.json'

class LoadingWrapper(object):

    def __init__(self, notify_loading_ui):
        self._loading_ui = None
        self._scene = None
        self._loading_percent = 0
        self._callback = None
        self._target_percent = 0
        self._res = 0
        self._pre_kind = 0
        self._trans = None
        self._timer_id = None
        self.use_loading_ui = None
        self.percent = 0
        self._frame_funcs = []
        self._frame_funcs_total = 0
        self._frame_funcs_pass = 0
        self._prepared_frames = 5
        self._percent_anim = 0
        self._py_imports = []
        self._py_import_idx = 0
        self._load_start_time = 0
        self.need_warmup = False
        self._warmup_budget = 5.0
        self._need_preload_effect_cache = False
        self._notify_loading_ui = notify_loading_ui
        self._load_ui_parts = []
        self._load_ui_part_cnt = 0
        self.guangmu_play_cnt = 0
        self.guangmu_left_time = 0
        self.guangmu_duration = 0
        global_data.emgr.loading_end_event += self.on_loading_ui_closed
        global_data.emgr.on_play_guangmu += self.on_play_guangmu
        return

    def __del__(self):
        global_data.emgr.loading_end_event -= self.on_loading_ui_closed
        global_data.emgr.on_play_guangmu -= self.on_play_guangmu

    def init_from_dict(self, bdict):
        self.use_loading_ui = bdict.get('use_loading_ui', True)
        is_battle_loading = bdict.get('is_battle', False)
        if self.use_loading_ui:
            if is_battle_loading:
                self._loading_ui = self.get_loading_ui(bdict)
                group_data = bdict['group_data']
                self._loading_ui.init_teammate_widget(group_data)
            else:
                from . import loading
                self._loading_ui = loading.UILoadingWidget()
        if self._loading_ui:
            self._loading_ui.loading_init()
        self.set_percentage(0)
        self._timer_id = global_data.game_mgr.get_logic_timer().register(None, self.update, timedelta=True)
        self._percent_anim = 0
        self.init_event()
        return

    def get_loading_ui(self, bdict):
        battle = global_data.battle
        if battle and battle.need_pvp_loading():
            widget_name = 'SnatchEggPlayerListLoadingWidget' if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SNATCHEGG) else 'PlayerListLoadingWidget'
            preload_ui = global_data.ui_mgr.get_ui(widget_name)
        else:
            preload_ui = None
        if preload_ui:
            return preload_ui
        else:
            loading_ui_cls = self.get_loading_cls()
            return loading_ui_cls(map_id=bdict.get('map_id', 0))
            return

    def get_loading_cls(self):
        from . import battle_loading
        bat = global_data.battle
        if bat:
            max_loading_time = bat.get_max_loading_time()
            if max_loading_time > 0:
                if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SNATCHEGG):
                    return battle_loading.SnatchEggPlayerListLoadingWidget
                else:
                    return battle_loading.PlayerListLoadingWidget

        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GVG,)):
            return battle_loading.GVGLoadingWidget
        else:
            if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
                return battle_loading.DuelLoadingWidget
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CLONE):
                return battle_loading.CloneBattleLoadingWidget
            if global_data.game_mode.is_pve():
                from .pve_loading import PVELoadingWidget
                return PVELoadingWidget
            return battle_loading.BattleLoadingWidget

    def init_event(self):
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect

    def on_login_reconnect(self):
        self.clear_timer()
        self._timer_id = global_data.game_mgr.get_logic_timer().register(None, self.update, timedelta=True)
        return

    def clear(self):
        self.clear_timer()
        self.set_percentage(100)
        self._pre_kind = 0
        if self._loading_ui:
            is_closed = self._loading_ui.loading_end()
            if is_closed:
                self._loading_ui = None
        self._load_ui_parts = []
        self._load_ui_part_cnt = 0
        return

    def clear_timer(self):
        if self._timer_id is not None:
            global_data.game_mgr.get_logic_timer().unregister(self._timer_id)
            self._timer_id = None
        return

    def loading_end(self):
        if self.need_warmup:
            print('loadwrapper time cost', time.time() - self._load_start_time)
            print('compile shader time cost', ShaderWarmup()._total_time_cost)
        self.clear()
        self.end_callback()

    def loading_cancel(self):
        self.clear()

    def end_callback(self):
        if self._scene.valid:
            for foo in self._frame_funcs:
                foo()

            self._frame_funcs = []
            self._frame_funcs_pass = self._frame_funcs_total
        if self._callback:
            self._callback()
        if self._trans:
            self._trans.hide()
        if self._loading_ui:
            self._loading_ui = None
        return

    def get_percentage(self):
        return self.percent

    def set_percentage(self, value):
        self.percent = value
        if self._loading_ui and self._notify_loading_ui:
            self._loading_ui.update_percent(value)

    def add_percentage(self, value):
        self.set_percentage(self.get_percentage() + value)

    def preload_resource(self, callback=None, scene=None, res_objs=[], textures=[], percent=100, frame_funcs=None, need_warmup=False, preload_effect_cache=False):
        self._load_start_time = time.time()
        self._loading_percent = percent
        self._callback = callback
        if frame_funcs:
            self._frame_funcs = []
            self._frame_funcs.extend(frame_funcs)
            if self._loading_ui._widget:
                self._prepared_frames = 5
                self._frame_funcs_pass = 0
                self._frame_funcs_total = len(self._frame_funcs)
                self._pre_kind += 1
        if scene is not None:
            self._scene = scene
            self._pre_kind += 1
        if len(res_objs) + len(textures) > 0:
            self._res = {'res': res_objs,'tex': textures}
            self._pre_kind += 1
        if six.moves.builtins.__dict__.get('GAME_ENV_INITED', False) and not global_data.pymod_inited:
            self._py_imports = data.preimport.namelist
            global_data.pymod_inited = True
        else:
            self._py_imports = []
        if self._py_imports:
            self._pre_kind += 1
        if need_warmup and not ShaderWarmup().warmup_finished:
            self.need_warmup = need_warmup
        if self._pre_kind == 0:
            self.loading_end()
            return
        else:
            stats = [
             0, len(res_objs) + len(textures)]

            def resource_loaded(path=None, data=None):
                stats[0] += 1
                self._target_percent = float(stats[0]) / stats[1]

            for path in res_objs:
                resloader.async_load_res_by_path(path, resloader.ASYNC_RES, async_callback=resource_loaded)

            for path in textures:
                resloader.async_load_res_by_path(path, resloader.ASYNC_TEXURE, async_callback=resource_loaded)

            return

    def preload_effect_cache(self):
        import json
        import C_file
        from common.cfg.jsonconf import convert
        from common.platform.dctool.interface import get_shader_preload_conf_path
        file_name = get_shader_preload_conf_path()
        try:
            conf = json.loads(C_file.get_res_file(file_name, ''))
            conf = convert(conf)
        except Exception as e:
            log_error('preload effect: file load error %s:%s' % (file_name, str(e)))
            return

        new_dict = {}
        res_info_exist = C_file.find_res_file(EFFECT_INFO_FILE_NAME, '')
        if not res_info_exist:
            return
        else:
            try:
                res_effect_info = json.loads(C_file.get_res_file(EFFECT_INFO_FILE_NAME, ''))
            except Exception as e:
                return

            all_num, all_num2, all_num3 = (0, 0, 0)
            from logic.vscene.global_display_setting import GlobalDisplaySeting
            from logic.gcommon.common_const.ui_operation_const import QUALITY_SHADOWMAP_KEY
            lod_level_setting = GlobalDisplaySeting().get_normal_type_lod_level()
            shadow_map_setting = global_data.player.get_setting(QUALITY_SHADOWMAP_KEY)
            for effect_file in conf:
                version = conf[effect_file]['version']
                tmp_file = effect_file.replace('\\', '/')
                effect_info = res_effect_info.get(tmp_file, {})
                if not effect_info:
                    tmp_file = effect_file.replace('/', '\\')
                    effect_info = res_effect_info.get(tmp_file, {})
                    if not effect_info:
                        continue
                same_version = True
                if isinstance(version, dict):
                    json_file = effect_file + '.json'
                    if json_file not in effect_info:
                        same_version = False
                    else:
                        version_conf = version[json_file]
                        version_patch = effect_info[json_file][0]
                        if isinstance(version_conf, list):
                            if version_patch not in version_conf:
                                same_version = False
                        elif isinstance(version_conf, int):
                            if version_conf != version_patch:
                                same_version = False
                        else:
                            same_version = False
                    if not same_version:
                        all_num2 += len(conf[effect_file]['key_lst'])
                        continue
                elif isinstance(version, int):
                    effect_info = effect_info.get(tmp_file, None)
                    if not effect_info:
                        continue
                    effect_version = effect_info[0]
                    if int(effect_version) != int(version):
                        continue
                else:
                    continue
                key_lst = conf[effect_file]['key_lst']
                if not key_lst:
                    continue
                if hasattr(render, 'get_macro_value_from_define_key'):
                    new_key_lst = []
                    for define_key in key_lst:
                        lod_level = render.get_macro_value_from_define_key(effect_file, define_key, 'LOD_LEVEL')
                        shadow_macro = render.get_macro_value_from_define_key(effect_file, define_key, 'SHADOW_MAP_ENABLE')
                        lod_fit = lod_level == -1 or lod_level == lod_level_setting
                        shadow_fit = shadow_macro == -1 or shadow_macro == shadow_map_setting
                        if lod_fit and shadow_fit:
                            new_key_lst.append(define_key)
                        else:
                            all_num3 += 1

                    if new_key_lst:
                        new_dict[effect_file] = new_key_lst
                        all_num += len(new_key_lst)
                else:
                    new_dict[effect_file] = key_lst
                    all_num += len(key_lst)

            if new_dict:
                print('preload num:', all_num, all_num2, all_num3)
                self._need_preload_effect_cache = True
                if self._loading_ui and hasattr(self._loading_ui, 'set_preload_shader_cache_txt'):
                    self._loading_ui.set_preload_shader_cache_txt()
                render.preload_effect_cache(new_dict)
                self._pre_kind += 1
            return

    def update(self, dt):
        if self._loading_ui:
            self._loading_ui.loading_update(dt)
        if self._pre_kind == 0:
            return
        else:
            if self._scene and not self._scene.valid:
                self.set_percentage(100)
                self.loading_end()
                return
            from logic.vscene import scene_type
            if global_data.scene_type == scene_type.SCENE_TYPE_BATTLE and not global_data.battle:
                return
            if self._frame_funcs_pass < self._frame_funcs_total:
                if self._prepared_frames:
                    self._prepared_frames -= 1
                else:
                    self._frame_funcs.pop(0)()
                    self._frame_funcs_pass += 1
            if self._warmup_budget > 0.0 and self.need_warmup:
                print('budget', id(self), self._warmup_budget)
                self._warmup_budget = ShaderWarmup().warmup_time_trial(self._warmup_budget)
            percent = 0
            if self._scene and self._scene.valid:
                if self._scene.is_loaded():
                    percent += 100.0 / self._pre_kind
                else:
                    scene_progress = self._scene.get_progress()
                    if self._scene.get_detail_done() == 1 or scene_progress >= 0.3 and self._scene._percent_st == progress.ST_PERCENT_NONE:
                        scene_progress = 1.0
                    percent += scene_progress * 100 / self._pre_kind
            if self._res is not None:
                percent += self._target_percent * 100 / self._pre_kind
            if self._frame_funcs_total:
                percent += self._frame_funcs_pass * 100.0 / self._frame_funcs_total / self._pre_kind
            if self._py_imports:
                last_percent = percent
                try:
                    for i in range(self._py_import_idx, min(self._py_import_idx + PY_LOAD_PER_FRAME, len(self._py_imports))):
                        try:
                            __import__(self._py_imports[i])
                        except:
                            pass

                        self._py_import_idx += 1

                    percent += float(self._py_import_idx) / len(self._py_imports) * 100.0 / self._pre_kind
                except:
                    self._py_imports = []
                    self._pre_kind -= 1
                    percent = last_percent
                    if self._pre_kind == 0:
                        percent = self._loading_percent
                        self._percent_anim = self._loading_percent

            if self._need_preload_effect_cache:
                ret = render.get_preload_effect_cache_progress()
                if ret == (0, 0):
                    percent += 100.0 / self._pre_kind
                else:
                    now_num, total_num = ret
                    percent += float(now_num) / float(total_num) * 100.0 / self._pre_kind
            is_playing_guangmu = False
            guangmu_percent = max(0, self.guangmu_play_cnt - 1)
            if self.guangmu_left_time > 0:
                is_playing_guangmu = True
                self.guangmu_left_time -= dt
                guangmu_percent += max(0.0, self.guangmu_left_time / self.guangmu_duration)
            elif self.guangmu_play_cnt > 0:
                guangmu_percent += 1
            guangmu_percent *= 100.0
            ui_percent = 1.0
            wait_load_ui_part_cnt = len(self._load_ui_parts)
            if self._scene and self._scene.valid and wait_load_ui_part_cnt > 0:
                part = self._load_ui_parts[0]
                ret = part.load_ui_per_frame(dont_load=is_playing_guangmu)
                ui_percent = (self._load_ui_part_cnt - wait_load_ui_part_cnt + ret) / self._load_ui_part_cnt
                if ret >= 1.0:
                    self.del_frame_load_ui_part(part)
            ui_percent *= 100.0
            percent = (percent * self._pre_kind + ui_percent + guangmu_percent) / (self._pre_kind + 1 + self.guangmu_play_cnt)
            if self.use_loading_ui and percent - self._percent_anim > 10:
                self._percent_anim += 10
            elif percent > self._percent_anim:
                self._percent_anim = percent
            if self._percent_anim >= self._loading_percent:
                self.loading_end()
            else:
                p = self._percent_anim * 0.8 + self.get_percentage() * 0.2
                self.set_percentage(p)
            return

    def add_frame_load_ui_part(self, part):
        if part not in self._load_ui_parts:
            self._load_ui_parts.append(part)
            self._load_ui_part_cnt += 1

    def del_frame_load_ui_part(self, part):
        if part in self._load_ui_parts:
            self._load_ui_parts.remove(part)

    def show(self):
        if self._loading_ui:
            self._loading_ui.show()

    def hide(self):
        if self._loading_ui:
            self._loading_ui.hide()

    def on_loading_ui_closed(self):
        self._loading_ui = None
        return

    def on_play_guangmu(self, soul_id, guangmu_id, next_play_guangmu_time):
        guangmu_dur = next_play_guangmu_time - time_utility.time()
        if guangmu_dur <= 0:
            return
        self.guangmu_play_cnt += 1
        self.guangmu_duration = self.guangmu_left_time = guangmu_dur