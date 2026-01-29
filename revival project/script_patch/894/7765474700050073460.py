# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartSnowEffect.py
from __future__ import absolute_import
from six.moves import range
from . import ScenePart
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon.common_const.collision_const import WATER_GROUP, WATER_MASK, TERRAIN_MASK, ICE_GROUP
import collision
import game3d
import random
import math
import math3d
import common.utils.timer as timer
SNOW_SFX = [
 'effect/fx/scenes/common/snow/snow_snowflake_01.sfx',
 'effect/fx/scenes/common/snow/snow_snowflake_02.sfx',
 'effect/fx/scenes/common/snow/snow_snowflake.sfx']
POISON_SNOW_SFX = [
 'effect/fx/scenes/common/snow/snow_snowflake_bao01.sfx',
 'effect/fx/scenes/common/snow/snow_snowflake_bao02.sfx',
 'effect/fx/scenes/common/snow/snow_snowflake_bao.sfx']
ALL_SNOW_COL = ('snow_01_col', 'snow_col')
FAIRWORKS_SFX = 'effect/fx/scenes/common/sidou/yanhu_yewanditu_001.sfx'
FAIRWORKS_INTERVAL = (4, 10)
FAIRWORKS_DISTANCE = (5000, 10000)
FAIRWORKS_RADIAN = 0.5 * math.pi

class PartSnowEffect(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartSnowEffect, self).__init__(scene, name)
        self._player = None
        self.is_in_house = False
        self.is_diving = False
        self.is_poison_inside = False
        self.snow_sfx_enable = False
        self.snow_sfx_id = [None, None, None]
        self.poison_snow_sfx_enable = False
        self.poison_snow_sfx_id = [None, None, None]
        self.all_snow_col_models = []
        self.need_disable_collision_model_names = []
        self.disable_collision_delay_exec = None
        self.fairworks_timer = None
        self.disable_collision_interval = 100
        return

    def on_before_load(self):
        self.clear()
        snow_enable = '1' if global_data.game_mode.is_snow_res() else '0'
        scn = self.scene()
        scn.set_macros({'SNOW_ENABLE': snow_enable})
        if global_data.game_mode.is_snow_res():
            global_data.emgr.scene_camera_target_setted_event += self.on_target_change
            global_data.emgr.switch_judge_camera_event += self.on_switch_judge_camera

            def callback():
                scn.disable_vegetation()

            game3d.delay_exec(1, callback)
            part_fog_and_light = scn.get_com('PartAutoFogAndLight')
            if part_fog_and_light and global_data.game_mode.is_snow_weather():
                part_fog_and_light.load_custom_data('snow_poison')
            self.on_target_change()

    def on_enter(self):
        scn = self.scene()
        if not global_data.game_mode.is_snow_res():
            preload_model_names = scn.get_preload_names()
            for model_name in preload_model_names:
                for snow_col_name in ALL_SNOW_COL:
                    if snow_col_name in model_name:
                        self.all_snow_col_models.append(model_name)
                        model = scn.get_model(model_name)
                        if model:
                            model.active_collision = False
                        else:
                            self.need_disable_collision_model_names.append(model_name)

            self.delay_disable_collision()
        if global_data.game_mode.is_snow_night_weather():
            self.init_fairworks()
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect

    def delay_disable_collision(self):
        if self.need_disable_collision_model_names:

            def callback():
                save_model_names = []
                scn = self.scene()
                for model_name in self.need_disable_collision_model_names:
                    model = scn.get_model(model_name)
                    if model:
                        model.active_collision = False
                    else:
                        save_model_names.append(model_name)

                self.need_disable_collision_model_names = save_model_names
                self.disable_collision_interval *= 1.1
                self.delay_disable_collision()

            self.disable_collision_delay_exec = game3d.delay_exec(self.disable_collision_interval, callback)
        else:
            self.disable_collision_delay_exec = None
        return

    def clear(self):
        if self.disable_collision_delay_exec:
            game3d.cancel_delay_exec(self.disable_collision_delay_exec)
        if global_data.game_mode.is_snow_res():
            global_data.emgr.scene_camera_target_setted_event -= self.on_target_change
            global_data.emgr.switch_judge_camera_event -= self.on_switch_judge_camera

    def on_exit(self):
        self.clear()
        if self.fairworks_timer:
            global_data.game_mgr.unregister_logic_timer(self.fairworks_timer)
            self.fairworks_timer = None
        global_data.emgr.net_login_reconnect_event -= self.on_login_reconnect
        return

    def on_login_reconnect(self):
        if self.fairworks_timer:
            global_data.game_mgr.unregister_logic_timer(self.fairworks_timer)
            self.fairworks_timer = None
            self.delay_random_fairworks()
        return

    def on_target_change(self):
        lplayer = global_data.cam_lplayer
        if self._player and self._player.is_valid():
            self._player.unregist_event('E_IN_HOUSE_STATE_CHANGE', self.on_in_house_state_change)
            self._player.unregist_event('E_PARACHUTE_STATUS_CHANGED', self.check_scene_sfx)
            self._player.unregist_event('E_IN_POISON', self.on_poison_change)
            self._player.unregist_event('E_MODEL_LOADED', self.check_scene_sfx)
            if self._player.sd.ref_is_mecha:
                self._player.unregist_event('E_MECHA_ENTER_DIVING', self.on_enter_diving)
                self._player.unregist_event('E_MECHA_LEAVE_DIVING', self.on_leave_diving)
        self._player = lplayer
        if self._player and self._player.is_valid():
            self._player.regist_event('E_IN_HOUSE_STATE_CHANGE', self.on_in_house_state_change)
            self._player.regist_event('E_PARACHUTE_STATUS_CHANGED', self.check_scene_sfx)
            self._player.regist_event('E_IN_POISON', self.on_poison_change)
            self._player.regist_event('E_MODEL_LOADED', self.check_scene_sfx)
            if self._player.sd.ref_is_mecha:
                self._player.regist_event('E_MECHA_ENTER_DIVING', self.on_enter_diving)
                self._player.regist_event('E_MECHA_LEAVE_DIVING', self.on_leave_diving)
                self.is_diving = self._player.ev_g_is_diving()
            else:
                self.is_diving = False
            self.is_in_house = self._player.ev_g_is_in_house()
            self.is_poison_inside = None
            part_battle = self.scene().get_com('PartBattle')
            if part_battle:
                poison_mgr = part_battle.get_poison_manager()
                self.is_poison_inside = poison_mgr and poison_mgr.is_inside()
            if self.is_poison_inside is None:
                self.is_poison_inside = True
            self.del_snow_scene_sfx()
            self.check_snow_scene_sfx()
            self.del_poision_snow_scene_sfx()
            self.check_poision_snow_scene_sfx()
            if global_data.game_mode.is_snow_weather():
                self.check_fog_density()
        else:
            self.clear_effect()
        return

    def clear_effect(self):
        self.is_poison_inside = None
        self.del_snow_scene_sfx()
        self.del_poision_snow_scene_sfx()
        if global_data.game_mode.is_snow_weather():
            self.check_fog_density()
        return

    def on_in_house_state_change(self, in_house):
        self.is_in_house = in_house
        self.check_scene_sfx()

    def on_enter_diving(self):
        self.is_diving = True
        self.check_scene_sfx()

    def on_leave_diving(self):
        self.is_diving = False
        self.check_scene_sfx()

    def check_scene_sfx(self, *args):
        self.check_snow_scene_sfx()
        self.check_poision_snow_scene_sfx()

    def check_snow_scene_sfx(self, *args):
        if not self.is_diving and not self.is_in_house:
            if not self.snow_sfx_enable:
                self.add_snow_scene_sfx()
        elif self.snow_sfx_enable:
            self.del_snow_scene_sfx()

    def add_snow_scene_sfx(self):
        if not self._player:
            return
        battle = global_data.player.get_battle()
        if battle and battle.is_battle_prepare_stage():
            return
        stage = self._player.share_data.ref_parachute_stage
        if not stage or not parachute_utils.is_in_battle(stage):
            return
        model = self._player.ev_g_model()
        if not model:
            return
        for index in range(len(SNOW_SFX)):
            if index == 0:
                self.snow_sfx_id[index] = global_data.sfx_mgr.create_sfx_on_model(SNOW_SFX[index], model, 'root')
            else:
                self.snow_sfx_id[index] = global_data.sfx_mgr.create_sfx_in_scene(SNOW_SFX[index])

        self.snow_sfx_enable = True

    def del_snow_scene_sfx(self):
        for index in range(len(SNOW_SFX)):
            global_data.sfx_mgr.remove_sfx_by_id(self.snow_sfx_id[index])
            self.snow_sfx_id[index] = None

        self.snow_sfx_enable = False
        return

    def on_poison_change(self, is_in_poison):
        self.is_poison_inside = not is_in_poison
        self.check_poision_snow_scene_sfx()
        if global_data.game_mode.is_snow_weather():
            self.check_fog_density()

    def check_poision_snow_scene_sfx(self, *args):
        if not self.is_diving and not self.is_in_house and not self.is_poison_inside:
            if not self.poison_snow_sfx_enable:
                self.add_poision_snow_scene_sfx()
        elif self.poison_snow_sfx_enable:
            self.del_poision_snow_scene_sfx()

    def add_poision_snow_scene_sfx(self):
        if not self._player or not global_data.player:
            return
        battle = global_data.player.get_battle()
        if battle and battle.is_battle_prepare_stage():
            return
        stage = self._player.share_data.ref_parachute_stage
        if not stage or not parachute_utils.is_in_battle(stage):
            return
        model = self._player.ev_g_model()
        if not model:
            return
        for index in range(len(POISON_SNOW_SFX)):
            if index == 0:
                self.poison_snow_sfx_id[index] = global_data.sfx_mgr.create_sfx_on_model(POISON_SNOW_SFX[index], model, 'root')
            else:
                self.poison_snow_sfx_id[index] = global_data.sfx_mgr.create_sfx_in_scene(POISON_SNOW_SFX[index])

        self.poison_snow_sfx_enable = True

    def del_poision_snow_scene_sfx(self):
        for index in range(len(POISON_SNOW_SFX)):
            global_data.sfx_mgr.remove_sfx_by_id(self.poison_snow_sfx_id[index])
            self.poison_snow_sfx_id[index] = None

        self.poison_snow_sfx_enable = False
        return

    def check_fog_density(self):
        part_fog_and_light = self.scene().get_com('PartAutoFogAndLight')
        if not part_fog_and_light:
            return
        else:
            if not self.is_poison_inside and self.is_poison_inside is not None:
                part_fog_and_light.set_custom_data_fadein()
            else:
                part_fog_and_light.recover_custom_fog_data_fadein()
            return

    def init_fairworks(self):
        self.delay_random_fairworks()

    def delay_random_fairworks(self):

        def cakkback():
            self.delay_random_fairworks()
            self.play_sfx()

        interval = FAIRWORKS_INTERVAL[0] + random.random() * FAIRWORKS_INTERVAL[1]
        self.fairworks_timer = global_data.game_mgr.register_logic_timer(cakkback, interval=interval, times=1, mode=timer.CLOCK)

    def play_sfx(self):
        if global_data.cam_lctarget and global_data.cam_data:
            player_pos = global_data.cam_lctarget.ev_g_model_position()
            if not player_pos:
                return
            distance = FAIRWORKS_DISTANCE[0] + random.random() * FAIRWORKS_DISTANCE[1]
            r = global_data.cam_data.yaw + (random.random() - 0.5) * FAIRWORKS_RADIAN
            x_offset = math.sin(r) * distance
            y_offset = math.cos(r) * distance
            pos = player_pos + math3d.vector(x_offset, 0, y_offset)

            def create_cb(sfx):
                sfx.scale = math3d.vector(10.0, 10.0, 10.0)

            global_data.sfx_mgr.create_sfx_in_scene(FAIRWORKS_SFX, pos, on_create_func=create_cb)

    def on_switch_judge_camera(self, enable, *args):
        if enable:
            self.clear_effect()