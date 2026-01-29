# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_global_sync/ComObserverGlobalSender.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon import const
from common.framework import Functor
from .ComObserverGlobalSenderBase import ComObserverGlobalSenderBase
import math3d
import world
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.common_utils.parachute_utils import STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_LAND, STAGE_PLANE, STAGE_LAUNCH_PREPARE
import logic.gcommon.cdata.status_config as status_config
import logic.gcommon.common_utils.bcast_utils as bcast

class ComObserverGlobalSender(ComObserverGlobalSenderBase):
    BIND_EVENT = {'E_ARMOR_DATA_CHANGED': 'on_armor_data_changed',
       'E_PARACHUTE_STATUS_CHANGED': 'parachute_status_changed',
       'E_PLANE': 'get_in_plane',
       'E_CAPSULE_SPEED_UP': 'on_speed_up',
       'E_SYNC_CAM_YAW_NORMAL': 'sync_cam_yaw_with_role',
       'E_SYNC_CAM_PITCH_NORMAL': 'sync_cam_pitch_with_role',
       'E_SYNC_CAM_YAW': 'sync_cam_yaw_with_remote',
       'E_SYNC_CAM_PITCH': 'sync_cam_pitch_with_remote',
       'E_ITEM_DATA_CHANGED': 'on_item_data_changed',
       'E_ATTACK_START': ('_puppet_attack_start', -10),
       'E_ATTACK_END': ('_puppet_attack_end', -10),
       'E_LOADING': ('_puppet_reload_bullet', -10),
       'E_ATTACHABLE_ON_HP_CHANGE': 'on_skate_hp_changed',
       'E_SET_CONTROL_TARGET': 'on_set_control_target',
       'E_ON_JUMP_STATE_CHANGE': 'on_jump_state_changed',
       'PARACHUTE_LAND_FINISHED': 'on_parachute_land_finished',
       'E_ON_AIM_SPEAD': 'on_observer_aim_spread_changed',
       'E_UPDATE_VEHICLE_CAMERA': 'on_vehicle_camera_updated',
       'E_GROUPMATE_ROUTE_CHANGED': 'on_groupmate_route_changed',
       'E_ACTION_MOVE': ('_on_action_move', -10),
       'E_ACTION_MOVE_STOP': ('_on_action_move_stop', -10),
       'E_TRY_DRAW_MAP_MARK': ('_try_draw_map_mark', 10)
       }
    DIRECT_FORWARDING_EVENT = {'E_AGENT_COIN_CHANGED': 'on_agent_coin_changed_event',
       'E_GET_CAPSULE': 'on_get_capsule_event',
       'E_CLOTHING_CHANGED': 'on_clothes_data_changed_event',
       'E_ARMOR_DO_DAMAGE': ('on_armor_damage_event', 1),
       'E_PICK_UP_CLOTHING': ('on_pick_up_clothing_event', 1),
       'E_WEAPON_DATA_SWITCHED': 'on_weapon_data_switched_event',
       'E_WPBAR_SWITCH_CUR': 'on_wpbar_switch_cur_event',
       'E_SWITCHED_WP_MODE': 'on_weapon_mode_switched',
       'E_RELOADING': 'on_reload_bullet_event',
       'E_CANCEL_RELOAD': 'on_cancel_reload_event',
       'E_ACTION_BEGIN_ROLL': 'on_begin_roll_event',
       'E_ACTION_BEGIN_RUSH': 'on_begin_roll_event',
       'E_END_ROLL': 'on_end_roll_event',
       'E_END_RUSH_EVENT': 'on_end_roll_event',
       'E_DEATH': ('target_dead_event', 11),
       'E_DEFEATED': ('target_defeated_event', 11),
       'E_REVIVE': ('target_revive_event', 11),
       'E_UPDATE_PICKED_ITEM_NUM': 'update_item_num_event',
       'E_UPDATE_MILEAGE': 'update_mileage_event',
       'E_ON_CONTROL_TARGET_CHANGE': ('switch_control_target_event', 10),
       'E_SHOW_SIDEWAYS_DIR': 'show_sideways_direction_event',
       'E_GLOBAL_BUFF_ADD': 'battle_add_buff',
       'E_GLOBAL_BUFF_DEL': 'battle_remove_buff',
       'E_HUMAN_SET_BUFF_ICON_VIS': 'human_need_update_buff_icon_vis',
       'E_GLOBAL_BUFF_MSG': 'capsule_show_msg',
       'E_SUCCESS_RIGHT_AIM': 'switch_to_right_aim_camera_event',
       'E_QUIT_RIGHT_AIM': 'exit_right_aim_camera_event',
       'E_ON_EQUIP_ATTACHMENT': ('weapon_equip_attachment_event', 10),
       'E_ON_TAKE_OFF_ATTACHMENT': ('weapon_take_off_attachment_event', 10),
       'E_ENTER_STATE': 'on_observer_enter_state_event',
       'E_LEAVE_STATE': 'on_leave_state_event',
       'E_MECHA_CAMERA': 'switch_to_mecha_camera',
       'E_LOADING': 'on_gun_loading_event',
       'E_CANCEL_LOAD': 'on_cancel_gun_loading_event',
       'E_END_LOAD': 'on_cancel_gun_loading_event',
       'E_ON_PICK_UP_WEAPON': 'on_observer_pick_up_weapon',
       'E_WEAPON_DATA_DELETED_SUCCESS': ('on_observer_weapon_deleted', 20),
       'E_UPDATE_TEAMMATE_INFO': ('update_teammate_info_event', 10),
       'E_SET_DRUG_SHORTCUT': ('set_drug_shortcut_event', 10),
       'E_HEALTH_HP_CHANGE': ('on_observer_hp_change_event', 10),
       'E_CTRL_USE_DRUG': ('on_observer_try_use_drug', 10),
       'E_ON_MECHA_CHARGING': ('on_observer_charging_event', 10),
       'E_STATE_CHANGE_CD': ('on_observer_state_change_cd', 10),
       'E_OCCUPY_CHANGE_PROGRESS': ('on_observer_occupy_change_process', 10),
       'E_ACTION_SYNC_CAM_STATE': ('on_sync_cam_state_event', 10),
       'E_NOTIFY_MODULE_CHANGED': ('observer_module_changed_event', 10),
       'E_NOTIFY_ATTACHMENT_CHANGED': ('observer_attachment_changed_event', 10),
       'E_MECHA_INSTALL_MODULE_RESULT': ('observer_install_module_result_event', 10),
       'E_MECHA_UNINSTALL_MODULE_RESULT': ('observer_uninstall_module_result_event', 10),
       'E_MECHA_INSTALL_ATTACHMENT_RESULT': ('observer_install_attachment_result_event', 10),
       'E_SUCCESS_AIM': ('on_observer_success_aim_event', 10),
       'E_QUIT_AIM': ('on_observer_quit_aim_event', 10),
       'E_CTRL_ACCUMULATE': ('on_observer_acummulate', 10),
       'E_FIRE': ('on_observer_fire', 10),
       'E_STOP_AUTO_FIRE': ('on_observer_stop_auto_fire', 10),
       'E_SHOW_MAIN_BATTLE_MESSAGE': 'show_battle_main_message',
       'E_SHOW_BATTLE_MESSAGE_EVENT': 'battle_show_message_event',
       'E_SHOW_MED_R_BATTLE_MESSAGE': 'show_battle_med_r_message',
       'E_ENTER_KING_CAMP': 'on_enter_king_camp_event',
       'E_LEAVE_KING_CAMP': 'on_leave_king_camp_event',
       'E_UPDATE_KILLER': ('update_killer_info', 10),
       'E_ON_HIT': 'on_be_hit_event',
       'E_ON_HIT_OTHER': 'on_hit_other_event',
       'E_TRY_SWITCH_TO_CAMERA_STATE': 'switch_target_to_camera_state_event',
       'E_TRY_REPLACE_LAST_CAMERA_STATE': 'replace_last_camera_state_event',
       'E_SET_CAMERA_FOLLOW_SPEED': 'camera_target_follow_speed_event',
       'E_CUR_BULLET_NUM_CHG': 'on_observer_weapon_bullet_num_changed',
       'E_IN_POISON': 'on_observer_poison_status_changed',
       'E_ON_JOIN_MECHA': ('on_observer_global_join_mecha', 99),
       'E_ON_JOIN_MECHA_START': ('on_observer_global_join_mecha_start', -10),
       'E_ON_LEAVE_MECHA_START': ('on_observer_global_leave_mecha_start', -10),
       'E_SET_KILLER_ID_NAME': ('on_observer_global_killer_camera', 99),
       'E_NOTIFY_UPDATE_RUNE_COUNT': ('update_granbelm_rune_count', 10),
       'E_NOTIFY_UPDATE_RUNE_ID': ('update_granbelm_rune_id', 10),
       'E_NOTIFY_UPDATE_REGION_TAG': ('update_granbelm_region_tag', 10),
       'E_SKILL_INIT_COMPLETE': 'on_skill_init_complete_event',
       'E_ADD_SKILL': ('on_add_skill_event', 10),
       'E_REMOVE_SKILL': ('on_remove_skill_event', 10),
       'E_MEOW_COIN_CHANGE': 'on_meow_coin_change_event',
       'E_OPEN_PARACHUTE': 'on_open_parachute_event'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComObserverGlobalSender, self).init_from_dict(unit_obj, bdict)
        global_data.emgr.parachute_height_changed += self.on_parachute_height_update

    def destroy(self):
        global_data.emgr.parachute_height_changed -= self.on_parachute_height_update
        super(ComObserverGlobalSender, self).destroy()

    def on_armor_data_changed(self, pos, armor):
        global_data.emgr.player_armor_changed.emit(pos, armor)

    def on_parachute_height_update(self, pos_y):
        stage = self.sd.ref_parachute_stage
        if stage not in (STAGE_FREE_DROP,):
            return
        scn = world.get_active_scene()
        if scn:
            pass

    def parachute_status_changed(self, stage):
        emgr = global_data.emgr
        global_data.emgr.on_observer_parachute_stage_changed.emit(stage)
        if stage == STAGE_FREE_DROP:
            emgr.show_screen_effect.emit('ParachuteSlow', {})
            emgr.show_screen_effect.emit('MechaDropEffect', {})
        elif stage in (STAGE_PARACHUTE_DROP, STAGE_LAND):
            emgr.destroy_screen_effect.emit('ParachuteSlow')
            emgr.destroy_screen_effect.emit('MechaDropEffect')
        scn = world.get_active_scene()
        if scn:
            scn.enable_fish_eye(False)
            if stage in (STAGE_FREE_DROP, STAGE_LAUNCH_PREPARE):
                _start_pos, end_pos = self.ev_g_launch_pos()
                scn.viewer_position = end_pos

    def get_in_plane(self):
        global_data.emgr.on_observer_plane_stage_start.emit()

    def sync_cam_yaw_with_role(self, to_yaw):
        global_data.emgr.sync_cam_yaw_with_role.emit(to_yaw)

    def sync_cam_pitch_with_role(self, to_pitch):
        global_data.emgr.sync_cam_pitch_with_role.emit(to_pitch)

    def sync_cam_yaw_with_remote(self, to_yaw, need_slerp, time):
        global_data.emgr.sync_cam_yaw_with_remote.emit(to_yaw, need_slerp, time)

    def sync_cam_pitch_with_remote(self, to_yaw, need_slerp, time):
        global_data.emgr.sync_cam_pitch_with_remote.emit(to_yaw, need_slerp, time)

    def on_speed_up(self, enable):
        global_data.emgr.on_speed_up.emit(enable)

    def on_item_data_changed(self, item_data):
        global_data.emgr.on_item_data_changed_event.emit(item_data)

    def _puppet_attack_start(self, *args):
        if global_data.player.id != self.unit_obj.id:
            self.send_event('E_PUPPET_ATTACK_START')
        global_data.emgr.on_observer_attack_start.emit()

    def _puppet_attack_end(self, *args):
        if global_data.player.id != self.unit_obj.id:
            self.send_event('E_PUPPET_ATTACK_END')
        global_data.emgr.on_observer_attack_end.emit()

    def _puppet_reload_bullet(self, *args):
        global_data.emgr.on_observer_load_bullet.emit()

    def on_skate_hp_changed(self, hp_info, *args):
        global_data.emgr.on_skate_hp_changed.emit(hp_info)

    def on_set_control_target(self, target, *args):
        global_data.emgr.on_observer_control_target_changed.emit(target)

    def on_jump_state_changed(self, state):
        if state == animation_const.JUMP_STATE_FALL_GROUND:
            fall_type = self.ev_g_fall_on_ground_type()
            if fall_type in (animation_const.FALL_ON_GROUND_MEDIUM_SPEED, animation_const.FALL_ON_GROUND_HIGH_SPEED):
                global_data.emgr.camera_shake_event_start.emit(None, 'state_on_ground', -1)
        return

    def on_parachute_land_finished(self, *args):
        global_data.emgr.camera_shake_event_start.emit(None, 'state_on_ground', -1)
        return

    def on_observer_aim_spread_changed(self, *args):
        global_data.emgr.on_observer_aim_spread_changed.emit()

    def on_vehicle_camera_updated(self, target, *args):
        from logic.units.LAirship import LAirship
        if isinstance(target, LAirship):
            global_data.emgr.switch_to_airship_camera.emit()

    def on_groupmate_route_changed(self):
        global_data.emgr.on_groupmate_route_changed.emit()

    def _on_action_move(self, *args):
        if not self.ev_g_get_state(status_config.ST_AIM):
            return
        if len(args) <= 0:
            return
        move_dir = args[0]
        if isinstance(move_dir, list):
            move_dir = math3d.vector(*move_dir)
        global_data.emgr.on_observer_action_move.emit(move_dir)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ACTION_MOVE, (tuple([move_dir.x, move_dir.y, move_dir.z]),)], True)

    def _on_action_move_stop(self, *args):
        global_data.emgr.on_observer_action_move_stop.emit()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ACTION_MOVE_STOP, tuple(args)], True)

    def _try_draw_map_mark(self, *args):
        pass