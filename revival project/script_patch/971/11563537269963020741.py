# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComFallReturnClient.py
from __future__ import absolute_import
from common.framework import Singleton
from ..UnitCom import UnitCom
import world
import math3d
import collision
import time
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const.collision_const import GROUP_STATIC_SHOOTUNIT

class ScreenSfxMgr(Singleton):

    def init(self):
        self.cam_player = None
        self.sfx_timer = 0
        self.sfx_id = None
        global_data.emgr.scene_camera_player_setted_event += self.switch_player
        global_data.emgr.extra_scene_added += self.destroy_singleton
        return

    def on_finalize(self):
        global_data.emgr.scene_camera_player_setted_event -= self.switch_player
        global_data.emgr.extra_scene_added -= self.destroy_singleton
        self.on_screen_sfx_finish()
        self.cancel_sfx_timer()
        self.cam_player = None
        return

    def destroy_singleton(self, *args):
        ScreenSfxMgr.finalize()

    def switch_player(self, *args):
        if self.cam_player and self.cam_player is not global_data.cam_lplayer:
            self.cancel_sfx_timer()
            self.on_screen_sfx_finish()

    def show_ui(self, player):
        if global_data.ex_scene_mgr_agent.check_settle_scene_active():
            return False
        if player is not global_data.cam_lplayer:
            return False
        if self.cam_player:
            return False
        self.cam_player = player
        global_data.ui_mgr.show_ui('BattleFallWarnUI', 'logic.comsys.battle')
        self.close_gm_helper()
        return True

    def close_ui(self):
        global_data.ui_mgr.close_ui('BattleFallWarnUI')

    def show_sfx(self, player, lasting_time=4):
        if global_data.ex_scene_mgr_agent.check_settle_scene_active():
            return False
        if player is not global_data.cam_lplayer:
            return False
        if self.cam_player and player is not self.cam_player:
            return False
        ui = global_data.ui_mgr.get_ui('BattleFallWarnUI')
        ui and ui.disappear()
        from logic.gutils.screen_effect_utils import create_screen_effect_directly
        self.sfx_id = create_screen_effect_directly('effect/fx/scenes/common/sidou/kd_chuansong_01_pm.sfx')
        self.cancel_sfx_timer()
        from common.utils.timer import CLOCK
        timer = global_data.game_mgr.get_logic_timer()
        self.sfx_timer = timer.register(func=self.on_screen_sfx_finish, interval=lasting_time, mode=CLOCK, times=1)
        self.close_gm_helper()
        return True

    def on_screen_sfx_finish(self):
        self.close_ui()
        self.destroy_sfx()
        if self.cam_player and self.cam_player.is_enable():
            self.cam_player.send_event('E_KONGDAO_FALL_FINISH')
        self.cam_player = None
        return

    def cancel_sfx_timer(self):
        if self.sfx_timer:
            global_data.game_mgr.get_logic_timer().unregister(self.sfx_timer)
            self.sfx_timer = 0

    def destroy_sfx(self):
        if self.sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.sfx_id)
            self.sfx_id = None
        return

    def close_gm_helper(self):
        from logic.comsys.control_ui.GMHelperUIFactory import GMHelperUIFactory
        GMHelperUIFactory.close_gm_helper_ui()


class ComFallReturnClient(UnitCom):
    BIND_EVENT = {'E_KONGDAO_FALL_STAGE': 'fall_stage',
       'E_KONGDAO_FALL_FINISH': 'on_screen_sfx_finish'
       }

    def __init__(self):
        super(ComFallReturnClient, self).__init__()
        self.below_col = None
        self._scene_sfx = None
        self._scene_col = None
        self._detect_timer = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComFallReturnClient, self).init_from_dict(unit_obj, bdict)
        self._left_times = bdict.get('fall_return_left_times', 0)
        self._stage = bdict.get('fall_stage', battle_const.KD_FALL_STAGE_NONE)
        self.sd.ref_kongdao_falling = self._stage != battle_const.KD_FALL_STAGE_NONE

    def on_init_complete(self):
        if self.ev_g_is_avatar():
            self.create_trigger()

    def destroy(self):
        self.cancel_detect_timer()
        self.remove_trigger()
        self.destroy_col()
        self.destroy_scn_sfx()
        super(ComFallReturnClient, self).destroy()

    def trigger_kongdao_fall(self, pos):
        if self._stage != battle_const.KD_FALL_STAGE_NONE:
            return
        if not self.ev_g_is_avatar():
            return
        from logic.gcommon.common_utils import parachute_utils
        stage = self.sd.ref_parachute_stage
        if parachute_utils.is_need_prepload_cockpit(stage):
            return
        pos = (pos.x, pos.y, pos.z)
        self.send_event('E_CALL_SYNC_METHOD', 'trigger_kongdao_fall', (pos,))
        if self._left_times > 0:
            self.fall_warning()

    def fall_stage(self, stage, *args):
        if stage == battle_const.KD_FALL_STAGE_WARN:
            self.fall_warning(*args)
        elif stage == battle_const.KD_FALL_STAGE_UNDERGROUND:
            self.trans_to_underground(*args)
        elif stage == battle_const.KD_FALL_STAGE_SCN_SFX:
            self.show_reborn_sfx(*args)
        else:
            self.trans_to_land()

    def fall_warning(self, left_time=None):
        if left_time is not None:
            self._left_times = left_time
        if self._stage == battle_const.KD_FALL_STAGE_WARN:
            return
        else:
            self._stage = battle_const.KD_FALL_STAGE_WARN
            self.sd.ref_kongdao_falling = True
            if global_data.ex_scene_mgr_agent.check_settle_scene_active():
                return
            ScreenSfxMgr().show_ui(self.unit_obj)
            return

    def trans_to_underground(self, pos, lasting_time=4):
        self._stage = battle_const.KD_FALL_STAGE_UNDERGROUND
        if global_data.ex_scene_mgr_agent.check_settle_scene_active():
            return
        if ScreenSfxMgr().show_sfx(self.unit_obj, lasting_time):
            ctrl_obj = self.ev_g_control_target()
            if ctrl_obj and ctrl_obj.logic:
                ctrl_obj.logic.send_event('E_HIDE_MODEL')
        if self.ev_g_is_avatar():
            self.create_col(pos)
            if global_data.pc_ctrl_mgr:
                from logic.comsys.battle.BattleUtils import stop_self_fire_and_movement
                stop_self_fire_and_movement()
                global_data.pc_ctrl_mgr.enable_keyboard_control(False)
            ctrl_obj = self.ev_g_control_target()
            if ctrl_obj and ctrl_obj.logic:
                ctrl_obj.logic.send_event('E_FORCE_TRANS_TO_HUMAN')

    def on_screen_sfx_finish(self):
        ctrl_obj = self.ev_g_control_target()
        if ctrl_obj and ctrl_obj.logic:
            ctrl_obj.logic.send_event('E_SHOW_MODEL')
        if self.unit_obj is global_data.player.logic:
            from logic.gcommon.common_const import battle_const
            message = [
             {'i_type': battle_const.FALL_RETURN_LEFT_TIMES,'set_content_func': 'set_fall_return_num',
                'content_args': (
                               self._left_times,)
                }]
            message_type = [
             battle_const.MAIN_NODE_COMMON_INFO]
            global_data.emgr.show_battle_main_message.emit(message, message_type, True, True)

    def create_col(self, pos):
        if not self.below_col:
            import collision
            from logic.gcommon.common_const import collision_const
            size = math3d.vector(200, 2, 200)
            col = collision.col_object(collision.BOX, size)
            col.mask = collision_const.GROUP_CHARACTER_INCLUDE
            col.group = collision_const.TERRAIN_GROUP
            self.scene.scene_col.add_object(col)
            self.below_col = col
        self.below_col.position = math3d.vector(pos[0], pos[1] - 5, pos[2])

    def show_reborn_sfx(self, reborn_pos):
        self._stage = battle_const.KD_FALL_STAGE_SCN_SFX
        if not self.ev_g_is_avatar():
            res_path = 'effect/fx/scenes/common/sidou/kd_chuansong_01.sfx'
            self._scene_sfx = world.sfx(res_path, scene=world.get_active_scene())
            self._scene_sfx.position = math3d.vector(reborn_pos[0], reborn_pos[1] + 5, reborn_pos[2])
            self._scene_sfx.scale = math3d.vector(5, 5, 5)

    def trans_to_land(self):
        self._stage = battle_const.KD_FALL_STAGE_NONE
        self.sd.ref_kongdao_falling = False
        self.destroy_col()
        self.destroy_scn_sfx()
        if self.ev_g_is_avatar():
            if global_data.pc_ctrl_mgr:
                global_data.pc_ctrl_mgr.enable_keyboard_control(True)

    def destroy_scn_sfx(self):
        if self._scene_sfx and self._scene_sfx.valid:
            self._scene_sfx.destroy()
            self._scene_sfx = None
        return

    def destroy_col(self):
        if self.below_col:
            self.scene.scene_col.remove_object(self.below_col)
            self.below_col = None
        return

    def create_trigger(self):
        self.remove_trigger()
        from common.cfg import confmgr
        area_list = confmgr.get('kongdao_trigger', 'Content', default=[])
        if not area_list:
            return
        self._scene_col = world.scene()
        for i, (center, size) in enumerate(area_list):
            center = math3d.vector(*center)
            size = math3d.vector(*size)
            col = collision.col_object(collision.BOX, size * 0.5, GROUP_STATIC_SHOOTUNIT, GROUP_STATIC_SHOOTUNIT)
            self._scene_col.scene_col.add_object(col)
            col.position = center

        from common.utils.timer import CLOCK
        self.cancel_detect_timer()
        self._detect_timer = global_data.game_mgr.register_logic_timer(self.detect, 0.15, mode=CLOCK)

    def remove_trigger(self):
        if self._scene_col:
            self._scene_col.destroy()
            self._scene_col = None
        return

    def cancel_detect_timer(self):
        if self._detect_timer:
            global_data.game_mgr.unregister_logic_timer(self._detect_timer)
            self._detect_timer = 0

    def detect(self, *args):
        if self._stage != battle_const.KD_FALL_STAGE_NONE:
            return
        if self.ev_g_death() or global_data.battle.is_settle:
            self.cancel_detect_timer()
            return
        control_target = self.ev_g_control_target()
        if not control_target or not control_target.logic:
            return
        pos = control_target.logic.ev_g_position()
        if not pos or pos.y > 300:
            return
        end_pos = pos + math3d.vector(0, 1000, 0)
        ret = self._scene_col.scene_col.hit_by_ray(pos, end_pos, 0, GROUP_STATIC_SHOOTUNIT, GROUP_STATIC_SHOOTUNIT, collision.INCLUDE_FILTER)
        if ret[0]:
            self.trigger_kongdao_fall(pos)