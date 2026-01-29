# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComOpenAim.py
from __future__ import absolute_import
import copy
from logic.gcommon.component.UnitCom import UnitCom
import math3d
import world
import logic.gcommon.common_utils.status_utils as status_utils
from logic.gcommon.cdata import mecha_status_config
from data.camera_state_const import AIM_MODE, MECHA_MODE_SEVEN, OBSERVE_FREE_MODE
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.vscene.parts.camera.CamAimModelRT import CamAimModelRT
from common.cfg import confmgr
from logic.gcommon.const import PART_WEAPON_POS_MAIN2

class ComOpenAim(UnitCom):
    BIND_EVENT = {'E_OPEN_AIM_CAMERA_ENTER': 'enter',
       'E_OPEN_AIM_CAMERA_EXIT': 'exit',
       'E_DEATH': 'on_mecha_death',
       'E_OPEN_AIM_CAMERA_ANIM': 'play_anim_open_aim',
       'E_OPEN_AIM_CAMERA_PLACE': 'play_anim_open_place',
       'E_OPEN_AIM_CAMERA_ON_FIRE': 'on_fire',
       'E_OPEN_AIM_CAMERA_RELOAD': 'on_reload',
       'G_AIM_LENS': 'get_aim_lens',
       'G_AIM_MODEL_ARGS': 'get_aim_model_args',
       'E_SET_AIM_MODEL_ARGS': 'set_aim_model_args',
       'E_SET_AIM_MODEL_SCALE': 'set_aim_model_scale',
       'G_IN_OPEN_AIM': '_in_open_aim',
       'E_ON_CAM_LCTARGET_SET': '_on_cam_lctarget_set',
       'E_ON_LOSE_CONNECT': '_on_lose_connect',
       'E_ON_SYNC_CAM_STATE_CHANGE': '_on_sync_cam_state_change',
       'E_PLAY_VICTORY_CAMERA': 'on_victory'
       }
    AIM_NOT_OPEN = 0
    AIM_OPENING = 1
    AIM_OPENED = 2
    AIM_CLOSING = 3
    CONFIG_MAP = {8007: {'AIM_POS_SOCKET_NAME': 'gun_position',
              'AIM_SFX_SOCKET_NAME': 'fx_vice_kaihuo',
              'AIM_MODEL_PATH': 'model_new/mecha/8007/8007/aim/aim.gim',
              'AIM_SFX_PATH': 'effect/fx/mecha/8007/8007_vice_xuli.sfx'
              }
       }

    def __init__(self):
        super(ComOpenAim, self).__init__()
        self.aim_model = None
        self.aim_sfx = None
        self.sd.ref_in_open_aim = False
        self.sd.ref_open_aim_weapon_pos = None
        self._last_cam_state = None
        self._aim_cam_rt = None
        self._restore_timer = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComOpenAim, self).init_from_dict(unit_obj, bdict)
        global_data.emgr.camera_switch_to_state_event += self.set_camera_state
        global_data.emgr.camera_enter_free_observe_event += self.on_camera_enter_free_observe_event
        global_data.emgr.camera_leave_free_observe_event += self.on_camera_leave_free_observe_event
        global_data.emgr.scene_observed_player_setted_event += self.on_scene_observed_player_setted_event

    def on_init_complete(self):
        self.init_param()
        self.sd.update_aim_model_trans_func = self.update_aim_model_transformation

    def init_param(self):
        mecha_id = self.sd.ref_mecha_id
        if not mecha_id:
            return
        else:
            self.config = copy.deepcopy(self.CONFIG_MAP.get(mecha_id, None))
            if self.config is None:
                return
            skin_and_shiny_weapon = self.ev_g_mecha_skin_and_shiny_weapon_id()
            if skin_and_shiny_weapon[1] is not None and skin_and_shiny_weapon[1] in (201800761,
                                                                                     201800762,
                                                                                     201800763):
                self.config['AIM_SFX_PATH'] = 'effect/fx/mecha/8007/8007_s_vice_xuli.sfx'
            mecha_id = str(mecha_id)
            data = status_utils.get_behavior_config(str(mecha_id)).get_behavior(mecha_id)
            self.custom_param = data.get(mecha_status_config.MC_SECOND_WEAPON_ATTACK, {}).get('custom_param', {})
            self.switch_action = self.custom_param.get('switch_action', {})
            self.open_aim_anim = self.custom_param.get('open_aim_anim', None)
            self.close_aim_anim = self.custom_param.get('close_aim_anim', None)
            self.close_aim_anim_len = self.custom_param.get('close_aim_anim_len', 1.1)
            self.idle_anim = self.custom_param.get('idle_anim', None)
            self.snipe_idle_anim = self.custom_param.get('snipe_idle_anim', None)
            self.snipe_move_anim = self.custom_param.get('snipe_move_anim', None)
            self.open_aim_duration = self.custom_param.get('open_aim_duration', 1.3)
            scale = self.custom_param.get('aim_model_scale', (1.0, 1.0, 1.0))
            self.aim_model_scale = math3d.vector(scale[0], scale[1], scale[2])
            self.aim_model_rel_yaw = self.custom_param.get('aim_model_rel_yaw', 0.1)
            self.aim_model_rel_pitch = self.custom_param.get('aim_model_rel_pitch', 0.04)
            self.aim_model_y_offset = self.custom_param.get('aim_model_y_offset', -5)
            self.aim_model_xz_offset = self.custom_param.get('aim_model_xz_offset', 5)
            self.aim_model_forward_offset = self.custom_param.get('aim_model_forward_offset', 10)
            self.reocver_camera_state = self.custom_param.get('reocver_camera_state', MECHA_MODE_SEVEN)
            self.aim_need_hide_model = self.custom_param.get('aim_need_hide_model', False)
            self.aim_lens = self.custom_param.get('aim_lens', None)
            return

    def _in_open_aim(self):
        return self.sd.ref_in_open_aim

    def enter(self, weapon_pos=PART_WEAPON_POS_MAIN2):
        if self.unit_obj != global_data.cam_lctarget:
            return
        else:
            if self.sd.ref_in_open_aim:
                return
            if self.config is None:
                return
            self.sd.ref_in_open_aim = True
            self.sd.ref_open_aim_weapon_pos = weapon_pos
            if not self.aim_model:
                model_path = self.config['AIM_MODEL_PATH']
                mecha_id = self.sd.ref_mecha_id
                mecha_fashion_id = self.ev_g_mecha_fashion_id()
                if mecha_fashion_id is not None:
                    from logic.gutils.dress_utils import get_mecha_model_path
                    model_path = get_mecha_model_path(mecha_id, mecha_fashion_id)
                    model_path = model_path.replace('empty.gim', 'aim/aim.gim')
                self.aim_model = world.model(model_path, global_data.game_mgr.scene)
                self.aim_model.scale = math3d.vector(self.aim_model_scale)
            else:
                parent = self.aim_model.get_parent()
                if not parent:
                    global_data.game_mgr.scene.add_object(self.aim_model)
            self.sd.ref_aim_model = self.aim_model
            if not self.aim_sfx:
                self.aim_sfx = world.sfx(self.config['AIM_SFX_PATH'], scene=None)
            else:
                self.aim_sfx.remove_from_parent()
            self.aim_model.bind(self.config['AIM_SFX_SOCKET_NAME'], self.aim_sfx)
            self.aim_model.all_materials.enable_write_alpha = True
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_OPEN_AIM_CAMERA_ENTER, (weapon_pos,)), True, False, True)
            return

    def exit(self):
        if self._restore_timer:
            global_data.game_mgr.unregister_logic_timer(self._restore_timer)
            self._restore_timer = None
        if not self.sd.ref_in_open_aim:
            return
        else:
            if self._aim_cam_rt:
                self._aim_cam_rt.stop()
            self.sd.ref_in_open_aim = False
            self.sd.ref_aim_model = None
            self.sd.ref_open_aim_weapon_pos = None
            self.reset_model_state()
            self.send_event('E_TRY_SWITCH_TO_CAMERA_STATE', self.reocver_camera_state)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_OPEN_AIM_CAMERA_EXIT, ()), True, False, True)
            return

    def on_victory(self, *args):
        if self._restore_timer:
            global_data.game_mgr.unregister_logic_timer(self._restore_timer)
            self._restore_timer = None
        if not self.sd.ref_in_open_aim:
            return
        else:
            if self._aim_cam_rt:
                self._aim_cam_rt.stop()
            self.sd.ref_in_open_aim = False
            self.sd.ref_aim_model = None
            self.sd.ref_open_aim_weapon_pos = None
            self.reset_model_state()
            self.send_event('E_TRY_SWITCH_TO_CAMERA_STATE', self.reocver_camera_state, force_transfer_time=0)
            return

    def destroy(self):
        self.exit()
        if self._aim_cam_rt:
            self._aim_cam_rt.destroy()
            self._aim_cam_rt = None
        if self.aim_model and self.aim_model.valid:
            self.aim_model.destroy()
        self.aim_model = None
        if self.aim_sfx and self.aim_sfx.valid:
            self.aim_sfx.destroy()
        self.aim_sfx = None
        global_data.emgr.camera_switch_to_state_event -= self.set_camera_state
        global_data.emgr.camera_enter_free_observe_event -= self.on_camera_enter_free_observe_event
        global_data.emgr.camera_leave_free_observe_event -= self.on_camera_leave_free_observe_event
        global_data.emgr.scene_observed_player_setted_event -= self.on_scene_observed_player_setted_event
        return

    def play_anim_open_place(self):
        if not self.sd.ref_in_open_aim or not self.aim_lens:
            return
        is_in_observe_free = global_data.emgr.g_get_in_observe_free.emit()[0]
        if is_in_observe_free:
            return
        mecha_model = self.ev_g_model()
        matrix = mecha_model.get_socket_matrix(self.config['AIM_POS_SOCKET_NAME'], world.SPACE_TYPE_WORLD)
        if matrix:
            self.aim_model.world_position = math3d.vector(matrix.translation)
            self.aim_model.world_rotation_matrix = math3d.matrix(mecha_model.world_rotation_matrix)
        len_attr_data = confmgr.get('firearm_component', str(self.aim_lens), 'cAttr', default={})
        aim_magnitude = len_attr_data.get('iLensMagnitude', 2)
        fAimTime = len_attr_data.get('fAimTime', 0.4)
        global_data.emgr.switch_to_aim_camera_event.emit(aim_magnitude, fAimTime, self.aim_need_hide_model, item_id=self.aim_lens)
        if self._aim_cam_rt:
            self._aim_cam_rt.set_render_model(self.aim_model, is_follow_cam=True)
        else:
            fov = 0
            result = global_data.emgr.get_magnification_fov_event.emit()
            if result:
                fov = result[0]
            self._aim_cam_rt = CamAimModelRT(fov)
            scn = global_data.game_mgr.scene
            scn.remove_object(self.aim_model)
            self._aim_cam_rt.set_render_model(self.aim_model, is_follow_cam=True)
        self.send_event('E_HIDE_MODEL')
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_OPEN_AIM_CAMERA_PLACE, ()), True, False, True)

    def play_anim_open_aim(self):
        if not self.sd.ref_in_open_aim:
            return
        self.aim_model.play_animation('snipe_idle', 0.1, world.TRANSIT_TYPE_IMM, 0, world.PLAY_FLAG_LOOP)
        self.aim_sfx.restart()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_OPEN_AIM_CAMERA_ANIM, ()), True, False, True)

    def on_fire(self):
        if self.aim_model:
            self.aim_model.play_animation('snipe_shoot', -1, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_NO_LOOP)
            self.aim_sfx.shutdown(True)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_OPEN_AIM_CAMERA_ON_FIRE, ()), True, False, True)

    def on_reload(self):
        if self.aim_model:
            self.aim_model.play_animation('snipe_reload', 0.2, world.TRANSIT_TYPE_IMM, 0, world.PLAY_FLAG_NO_LOOP)
            self.aim_sfx.shutdown(True)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_OPEN_AIM_CAMERA_RELOAD, ()), True, False, True)

    def reset_model_state(self):
        self.send_event('E_SHOW_MODEL')
        if self.aim_sfx:
            self.aim_sfx.remove_from_parent()
        if self.aim_model:
            self.aim_model.remove_from_parent()

    def update_aim_model_transformation(self):
        self._aim_cam_rt and self._aim_cam_rt.update_transformation()

    def on_mecha_death(self):
        self.exit()

    def get_aim_model_args(self):
        return (
         self.aim_model_rel_yaw, self.aim_model_rel_pitch, self.aim_model_y_offset, self.aim_model_xz_offset, self.aim_model_forward_offset)

    def set_aim_model_args(self, rel_yaw, rel_pitch, y_offset, xz_offset, forward_offset):
        self.aim_model_rel_yaw = rel_yaw
        self.aim_model_rel_pitch = rel_pitch
        self.aim_model_y_offset = y_offset
        self.aim_model_xz_offset = xz_offset
        self.aim_model_forward_offset = forward_offset

    def set_aim_model_scale(self, scale=(1.0, 1.0, 1.0)):
        self.aim_model_scale = math3d.vector(scale[0], scale[1], scale[2])

    def get_aim_lens(self):
        if self.sd.ref_in_open_aim:
            return self.aim_lens
        else:
            return None

    def set_camera_state(self, state, *args):
        if state not in (AIM_MODE, OBSERVE_FREE_MODE):
            self._last_cam_state = state

    def on_camera_enter_free_observe_event(self):
        if not self.sd.ref_in_open_aim:
            return
        else:
            self.reset_model_state()
            self.sd.ref_in_open_aim = False
            self.sd.ref_aim_model = None
            if self._last_cam_state is not None:
                global_data.emgr.switch_observe_camera_state_event.emit(self._last_cam_state)
            return

    def on_camera_leave_free_observe_event(self):
        if self.unit_obj != global_data.cam_lctarget or global_data.player.id and self.sd.ref_driver_id == global_data.player.id:
            return
        if self.is_in_cam_state():
            self.do_restore()

    def on_scene_observed_player_setted_event(self, ltarget):
        if global_data.player.id and self.sd.ref_driver_id == global_data.player.id:
            return
        if not ltarget:
            self.exit()
            return
        if self.sd.ref_driver_id != ltarget.id:
            self.exit()
            self.send_event('E_OPEN_AIM_CAMERA', False)

    def do_restore(self):
        if self.unit_obj != global_data.cam_lctarget or global_data.player.id and self.sd.ref_driver_id == global_data.player.id:
            return
        if not self.is_in_cam_state():
            return
        global_data.emgr.end_slerp_camera_early_event.emit()
        self.enter()
        self.play_anim_open_place()
        self.play_anim_open_aim()
        self.send_event('E_OPEN_AIM_CAMERA', self.sd.ref_in_open_aim)

    def is_in_cam_state(self):
        driver_id = self.sd.ref_driver_id
        if not driver_id:
            return False
        from mobile.common.EntityManager import EntityManager
        driver = EntityManager.getentity(driver_id)
        cam_state = driver.logic.ev_g_cam_state()
        return cam_state == AIM_MODE

    def _on_cam_lctarget_set(self):
        if self.unit_obj != global_data.cam_lctarget:
            return
        if global_data.cam_lplayer and global_data.player and global_data.cam_lplayer.id == global_data.player.id:
            return
        if not self.is_in_cam_state():
            return

        def restore_func():
            self._restore_timer = None
            self.do_restore()
            return

        if self._restore_timer:
            return
        self._restore_timer = global_data.game_mgr.register_logic_timer(lambda : self.do_restore(), 2, times=1)

    def _on_lose_connect(self, *args):
        if self.unit_obj != global_data.cam_lctarget:
            return
        self.exit()
        self.send_event('E_OPEN_AIM_CAMERA', False)

    def _on_sync_cam_state_change(self):
        self._on_cam_lctarget_set()