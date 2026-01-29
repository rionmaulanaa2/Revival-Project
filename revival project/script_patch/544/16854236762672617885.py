# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTVMissileLauncherAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
from logic.gcommon.const import SOUND_TYPE_FIRE
from logic.gcommon.common_const.sync_const import SENDER_MODE_ROTATION_ONLY
from logic.comsys.control_ui.ShotChecker import ShotChecker
import logic.gcommon.common_utils.bcast_utils as bcast
import math3d
import world
ANIM_NAME_TO_SOUND_NAME_MAP = {'shoot': 'Play_tvmissile_fire',
   'reload': 'Play_tvmissile_reload'
   }
FIRE_SFX_PATH = 'effect/fx/weapon/huojiantong/huojiantong_muzzleflash.sfx'

class ComTVMissileLauncherAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_IS_AVATAR': 'is_avatar',
       'G_SHAPE_ID': 'get_shape_id',
       'G_MECHA_SKIN_AND_SHINY_WEAPON_ID': 'get_mecha_skin_and_shiny_weapon_id',
       'E_TRY_LAUNCHER_RELOAD': 'on_try_reload',
       'E_ON_CONTROL_TARGET_CHANGE': 'on_control_target_change',
       'G_FOOT_POSITION': '_get_model_pos',
       'E_ADD_CONTROLLER': 'on_add_controller',
       'E_REMOVE_CONTROLLER': 'on_remove_controller',
       'E_DO_CONTROLLED_APPEARANCE': 'do_controlled_appearance',
       'E_UNDO_CONTROLLED_APPEARANCE': 'undo_controlled_appearance',
       'E_DELTA_YAW': 'on_camera_yaw',
       'E_DELTA_PITCH': 'on_camera_pitch',
       'G_CAM_PITCH': 'get_camera_pitch',
       'G_ACTION_DOWN': 'on_action_btn_down',
       'E_RELOADING': 'on_reload_bullet',
       'E_POST_ACTION': 'on_post_action'
       })
    HANDLER_TYPE = 'TurnHandler'
    MODEL_PATH = 'character/weapons/1068_tvmissile/1068/h.gim'

    def init_from_dict(self, unit_obj, bdict):
        self.sd.ref_controller_id = bdict.get('owner_id', None)
        self.controller_unit = None
        super(ComTVMissileLauncherAppearance, self).init_from_dict(unit_obj, bdict)
        global_data.g_com_sysmgr.add_handler(self)
        self.reload_timer = None
        self.camera_pitch = 0
        return

    def on_init_complete(self):
        self.send_event('E_ACTIVE_SENDER_MODE', SENDER_MODE_ROTATION_ONLY)
        self.send_event('E_ENABLE_MOVE_SYNC_SENDER', False)
        self.send_event('E_SET_SYNC_RECEIVER_ENABLE', False)

    def get_model_info(self, unit_obj, bdict):
        position = bdict.get('position', (0, 390, -95)) or (0, 390, -95)
        pos = math3d.vector(*position)
        return (
         self.MODEL_PATH, None, (pos, self.MODEL_PATH))

    def anim_end_callback(self, model, data=None):
        if model.cur_anim_name != 'idle':
            model.play_animation('idle', 200, world.TRANSIT_TYPE_IMM, 0, world.PLAY_FLAG_DEF_LOOP, 1.0)

    def on_load_model_complete(self, model, user_data):
        super(ComTVMissileLauncherAppearance, self).on_load_model_complete(model, user_data)
        self.send_event('E_HUMAN_MODEL_LOADED', model, None)
        if self.sd.ref_controller_id:
            self.on_add_controller(self.sd.ref_controller_id)
        model.register_on_end_event(self.anim_end_callback)
        return

    def _unregister_reload_timer(self):
        if self.reload_timer:
            global_data.game_mgr.unregister_logic_timer(self.reload_timer)
            self.reload_timer = None
        return

    def destroy(self):
        if self.controller_unit and self.controller_unit.is_valid():
            pos = None
            model = self.controller_unit.ev_g_model()
            if model:
                pos = model.world_position
                pos -= model.world_rotation_matrix.forward * 2
                pos = (pos.x, pos.y, pos.z)
            elif self.model:
                mat = self.model.get_socket_matrix('renwu', world.SPACE_TYPE_WORLD)
                if mat:
                    pos = mat.translation
                    pos -= self.model.world_rotation_matrix.forward * 2
                    pos = (pos.x, pos.y, pos.z)
            if pos:
                self.controller_unit.send_event('E_STOP_CONTROL_TV_MISSILE_LAUNCHER', pos)
        if self.model:
            self.model.unregister_event(self.anim_end_callback, 'end')
        self.controller_unit = None
        global_data.g_com_sysmgr.remove_handler(self)
        self._unregister_reload_timer()
        self.is_avatar() and global_data.emgr.disable_change_weapon_cancel_reload_ui_appearance.emit(False)
        super(ComTVMissileLauncherAppearance, self).destroy()
        return

    def is_avatar(self):
        return self.sd.ref_controller_id == global_data.player.id

    def get_shape_id(self):
        return '1068'

    def get_mecha_skin_and_shiny_weapon_id(self):
        return (-1, -1)

    def do_try_reload(self):
        if self.is_valid():
            self.send_event('E_TRY_RELOAD', PART_WEAPON_POS_MAIN1)
        self.reload_timer = None
        return

    def on_try_reload(self):
        self._unregister_reload_timer()
        self.reload_timer = global_data.game_mgr.register_logic_timer(self.do_try_reload, interval=1, times=1)

    def on_control_target_change(self, target_id, position, is_in_mecha=False, by_init=False):
        if self.is_avatar() and self.unit_obj.id == target_id:
            self.on_try_reload()

    def on_add_controller(self, controller_id):
        entity = global_data.battle.get_entity(controller_id)
        if entity and entity.logic:
            entity.logic.send_event('E_START_CONTROL_TV_MISSILE_LAUNCHER', self.unit_obj.id)

    def on_remove_controller(self, controller_id, off_pos):
        entity = global_data.battle.get_entity(controller_id)
        if entity and entity.logic:
            entity.logic.send_event('E_STOP_CONTROL_TV_MISSILE_LAUNCHER', off_pos)
        else:
            self.undo_controlled_appearance()

    def do_controlled_appearance(self, controller_id):
        self.sd.ref_controller_id = controller_id
        entity = global_data.battle.get_entity(controller_id)
        self.controller_unit = entity.logic
        self.camera_pitch = 0
        if self.is_avatar():
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(self.sd.ref_logic_trans.yaw_target, 0, False)
            self.send_event('E_ENABLE_MOVE_SYNC_SENDER', True)
            global_data.sound_mgr.play_event('Play_tvmissile_on_1p', self.ev_g_position())
        else:
            self.send_event('E_SET_SYNC_RECEIVER_ENABLE', True)
            global_data.sound_mgr.play_event('Play_tvmissile_on_3p', self.ev_g_position())

    def undo_controlled_appearance(self):
        if self.is_avatar():
            self._unregister_reload_timer()
            self.send_event('E_INTERRUPT_RELOAD', PART_WEAPON_POS_MAIN1)
            global_data.emgr.disable_change_weapon_cancel_reload_ui_appearance.emit(False)
            self.send_event('E_ENABLE_MOVE_SYNC_SENDER', False)
            global_data.sound_mgr.play_event('Play_tvmissile_off_1p', self.ev_g_position())
        else:
            self.send_event('E_ENABLE_MOVE_SYNC_SENDER', False)
            global_data.sound_mgr.play_event('Play_tvmissile_off_3p', self.ev_g_position())
        self.sd.ref_controller_id = None
        self.controller_unit = None
        if self.model:
            self.anim_end_callback(self.model)
        return

    def on_camera_yaw(self, yaw, force_change_spd=True):
        self.sd.ref_logic_trans.yaw_target += yaw

    def on_action_yaw(self, data, force=False):
        self.sd.ref_rotatedata.try_set_body_link_head()

    def get_camera_pitch(self):
        if self.is_avatar():
            return global_data.cam_data.pitch
        else:
            return self.camera_pitch

    def on_camera_pitch(self, pitch):
        if self.is_avatar():
            self.send_event('E_ACTION_SYNC_HEAD_PITCH', pitch)
        else:
            self.camera_pitch += pitch

    def on_action_btn_down(self, *args):
        if self.controller_unit and self.controller_unit.is_valid():
            if self.controller_unit.ev_g_try_explode_tv_missile_in_advance():
                return True
        if self.ev_g_check_can_weapon_attack(PART_WEAPON_POS_MAIN1) and not ShotChecker().check_camera_can_shot():
            self.ev_g_try_weapon_attack_begin(PART_WEAPON_POS_MAIN1)
            self.ev_g_try_weapon_attack_end(PART_WEAPON_POS_MAIN1)
            self.on_post_action('shoot', 1.0, sound_suffix='_1p')
            global_data.emgr.camera_play_added_trk_event.emit('1054_FIRE', None, None)
        return True

    def on_reload_bullet(self, reload_time, times, *args):
        if self.ev_g_is_avatar():
            global_data.emgr.on_reload_bullet_event.emit(reload_time, times)
            global_data.emgr.disable_change_weapon_cancel_reload_ui_appearance.emit(True)
        self.on_post_action('reload', 2.0 / reload_time, sound_suffix='_1p')

    def on_post_action(self, anim_name, rate, sound_suffix='_3p'):
        if self.model:
            self.model.play_animation(anim_name, 200, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_DEF_LOOP, rate)
            if anim_name == 'shoot':
                global_data.sfx_mgr.create_sfx_on_model(FIRE_SFX_PATH, self.model, 'fx_fire')
                if global_data.cam_lctarget and not global_data.cam_lctarget.ev_g_is_groupmate(self.sd.ref_controller_id):
                    cur_pos = self.model.position
                    cam_target_position = global_data.cam_lctarget.ev_g_position()
                    if cam_target_position:
                        sound_length_sqr = (cur_pos - cam_target_position).length_sqr
                        global_data.emgr.sound_visible_add.emit(self.unit_obj, self.model.position, SOUND_TYPE_FIRE, sound_length_sqr, self.sd.ref_controller_id)
        global_data.sound_mgr.play_event(ANIM_NAME_TO_SOUND_NAME_MAP[anim_name] + sound_suffix, self.ev_g_position())
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt_crs_server', (bcast.E_POST_ACTION, (anim_name, rate)), True, False, True)