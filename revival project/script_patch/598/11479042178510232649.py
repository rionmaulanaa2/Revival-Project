# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_parachute/ComParachuteFollow.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_utils.parachute_utils import STAGE_PLANE, STAGE_PARACHUTE_DROP, STAGE_LAND, MODE_NOT_FOLLOW, MODE_REAL_FOLLOW, MODE_SIMULATE_FOLLOW
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.cdata.status_config import ST_DEAD
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import logic.gcommon.common_utils.bcast_utils as bcast
import world
import time
import math3d
import collision
UP_UNIT = math3d.vector(0, 1, 0)
TARGET_POS_CONSUME_DURATION = 1.5

class ComParachuteFollow(UnitCom):
    BIND_EVENT = {'E_PARACHUTE_FOLLOW': 'parachute_follow',
       'E_SWITCH_CAMERA_STATE': 'on_camera_state_switched',
       'E_MODEL_LOADED': ('on_model_loaded', 99),
       'E_SWITCH_PARACHUTE_FOLLOW_MODE': 'on_switch_parachute_follow_mode',
       'E_SET_PARACHUTE_FOLLOW_TARGET': 'on_set_parachute_follow_target',
       'E_REFRESH_PARACHUTE_FOLLOW_UPDATE_ORDER': 'refresh_update_order',
       'G_SIMULATE_FOLLOW_ENABLED': 'is_simulate_follow_enabled',
       'E_PARACHUTE_VERTICAL_SPEED_CHANGED': 'on_parachute_vertical_speed_changed',
       'G_PARACHUTE_VERTICAL_SPEED': 'get_parachute_vertical_speed',
       'E_REFRESH_PARACHUTE_FOLLOW_FREE_SIGHT_CAMERA': 'refresh_follow_free_sight_camera'
       }

    def __init__(self):
        super(ComParachuteFollow, self).__init__()
        self.camera = None
        self.model = None
        self.follower_stage = None
        self.follow_lent = None
        self.target_pos = None
        self.quit_clock = 0
        self.max_quit_count = 30
        self.last_drag_self_timestamp = 0
        self.drag_duration = 0.0
        self.max_drag_duration = 6.0
        self.is_in_free_mode = False
        self.tar_yaw = None
        self.tar_pitch = None
        self.is_avatar = False
        self.horizontal_offset = 0.0
        self.target_pos_intrp_offset = None
        self.intrp_cost_time = 0.0
        self.sd.ref_parachute_follow_velocity = math3d.vector(0, 0, 0)
        self.simulate_follow_timer = -1
        self.last_model_yaw = 0.0
        self.update_model_yaw_interval = 0.0
        self.update_anim_dir_interval = 0.0
        self.last_dir_x = 0.0
        self.last_dir_y = 0.0
        self.last_move_state = None
        self.simulate_follow_enabled = False
        self.follow_mode = MODE_NOT_FOLLOW
        self.follow_target_parachute_stage = None
        self.lose_follow_target_executed = False
        self.cur_vertical_speed = 0.0
        self.last_vertical_speed = 0.0
        self.event_registered = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComParachuteFollow, self).init_from_dict(unit_obj, bdict)
        self.follow_mode = bdict.get('follow_mode', MODE_NOT_FOLLOW)
        self.quit_clock = 0
        self.lose_follow_target_executed = False
        self.need_update = False
        self.follow_lent = None
        return

    def on_init_complete(self):
        self.is_avatar = self.ev_g_is_avatar()

    def cache(self):
        super(ComParachuteFollow, self).cache()
        if self.simulate_follow_timer > -1:
            global_data.game_mgr.get_fix_logic_timer().unregister(self.simulate_follow_timer)
            self.simulate_follow_timer = -1
        if self.is_avatar and self.event_registered:
            self.event_registered = False
            global_data.emgr.scene_on_touched -= self.scene_on_touched

    def destroy(self):
        super(ComParachuteFollow, self).destroy()
        if self.simulate_follow_timer > -1:
            global_data.game_mgr.get_fix_logic_timer().unregister(self.simulate_follow_timer)
            self.simulate_follow_timer = -1
        if self.is_avatar and self.event_registered:
            self.event_registered = False
            global_data.emgr.scene_on_touched -= self.scene_on_touched

    @property
    def parachute_follow_enabled(self):
        return self.need_update or self.simulate_follow_enabled

    def on_model_loaded(self, *args):
        if self.is_avatar:
            self.regist_event('E_SYNC_CAM_YAW', self.follow_camera_yaw_sync)
            self.regist_event('E_SYNC_CAM_PITCH', self.follow_camera_pitch_sync)
            if self.ev_g_has_parachute_follower():
                self.send_event('E_HAS_PARACHUTE_FOLLOWER', True)
            if self.event_registered:
                global_data.emgr.enable_free_sight_from_logic.emit(True)
        else:
            groupmate_id_list = self.ev_g_groupmate()
            if groupmate_id_list and global_data.player and global_data.player.id in groupmate_id_list:
                self.on_switch_parachute_follow_mode(self.follow_mode)

    def on_camera_state_switched(self, new_state, old_state, is_finish):
        from data.camera_state_const import FREE_MODEL
        if new_state == old_state or not is_finish:
            return
        else:
            player = global_data.player.logic if global_data.player else None
            if player:
                if new_state == FREE_MODEL:
                    player.send_event('E_HAS_PARACHUTE_FOLLOWER', False)
                elif old_state == FREE_MODEL:
                    player.send_event('E_HAS_PARACHUTE_FOLLOWER', True)
            if not self.need_update and not self.simulate_follow_enabled:
                return
            if new_state == FREE_MODEL:
                self.is_in_free_mode = True
            else:
                global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(self.tar_yaw, None, True, 0.3)
                global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(None, self.tar_pitch, True, 0.3)
                self.is_in_free_mode = False
            return

    def follow_camera_yaw_sync(self, yaw, need_slerp=True, cost_time=0.3):
        if self.parachute_follow_enabled:
            if self._is_need_update_camera_follow():
                global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(yaw, None, need_slerp, cost_time)
            self.tar_yaw = yaw
        return

    def follow_camera_pitch_sync(self, pitch, need_slerp=True, cost_time=0.3):
        if self.parachute_follow_enabled:
            if self._is_need_update_camera_follow():
                global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(None, pitch, need_slerp, cost_time)
            self.tar_pitch = pitch
        return

    def _is_need_update_camera_follow(self):
        ui = global_data.ui_mgr.get_ui('FightSightUI')
        return not (ui and ui.set_camera_enable_for_follow)

    def initialize_model_pos_y(self):
        cur_pos = self.ev_g_position()
        if cur_pos is None:
            return
        else:
            if cur_pos.y < self.target_pos.y + NEOX_UNIT_SCALE or cur_pos.y > self.target_pos.y + 2.5 * NEOX_UNIT_SCALE:
                cur_pos.y = self.target_pos.y + NEOX_UNIT_SCALE
                self.send_event('E_FOOT_POSITION', cur_pos)
            return

    def update_model_rotation(self, dt):
        if self.camera:
            tar_yaw = self.camera.world_rotation_matrix.yaw
            tar_pitch = self.camera.world_rotation_matrix.pitch
            if self.is_in_free_mode:
                tar_yaw = self.tar_yaw
                if self.follow_lent and self.follow_lent.is_valid():
                    tar_yaw = self.follow_lent.ev_g_yaw()
                tar_pitch = self.tar_pitch
            self.send_event('E_ACTION_SET_YAW', tar_yaw)
            self.send_event('E_FOLLOW_PITCH', tar_pitch)
        elif not self.is_avatar:
            self.update_model_yaw_interval += dt
            force_update = self.update_model_yaw_interval > 0.2
            tar_yaw = self.follow_lent.ev_g_yaw()
            if tar_yaw != self.last_model_yaw or force_update:
                self.last_model_yaw = tar_yaw
                self.send_event('E_SET_YAW', tar_yaw)
            if force_update:
                self.update_model_yaw_interval = 0.0

    def lose_follow_target(self):
        self.parachute_follow(False, force=not self.lose_follow_target_executed)
        self.lose_follow_target_executed = True
        ui = global_data.ui_mgr.get_ui('FollowDropUI')
        if ui:
            ui.close()

    def tick(self, dt):
        self.real_follow_tick(dt)

    def on_switch_parachute_follow_mode(self, mode):
        if self.is_avatar:
            return
        if mode == MODE_REAL_FOLLOW:
            self.enable_simulate_follow(False)
        elif mode == MODE_SIMULATE_FOLLOW:
            self.enable_simulate_follow(True)
        self.follow_mode = mode

    def on_set_parachute_follow_target(self, eid):
        if not self.is_avatar and eid is None and self.simulate_follow_enabled:
            self.enable_simulate_follow(False)
        return

    def parachute_follow(self, flag, force=False):
        self.is_avatar = self.ev_g_is_avatar()
        if flag:
            if self.parachute_follow_enabled:
                return
            follow_id = self.sd.ref_parachute_follow_target
            if follow_id is None:
                return
            self.quit_clock = 0
            self.drag_count = 0
            follow_ent = self.battle.get_entity(follow_id)
            if follow_ent and follow_ent.logic and follow_ent.logic.is_valid():
                self.follow_lent = follow_ent.logic
                self._calculate_horizontal_offset(follow_id)
                self.is_avatar and self.follow_lent.send_event('E_SET_PARACHUTE_FOLLOWED', True)
            self.camera = world.get_active_scene().active_camera
            self.follow_target_parachute_stage = None
        else:
            if not self.parachute_follow_enabled and not force:
                return
            self.send_event('E_CALL_SYNC_METHOD', 'follow_parachute', (None, ))
            self.send_event('E_SET_PARACHUTE_FOLLOW_TARGET', None)
            if self.follow_lent and self.follow_lent.is_valid():
                self.is_avatar and self.follow_lent.send_event('E_SET_PARACHUTE_FOLLOWED', False)
            self.camera = None
        global_data.emgr.enable_camera_yaw.emit(not flag)
        if self.is_avatar:
            self.send_event('E_ENABLE_ADJUST_MODEL_YAW', not flag)
            if flag != self.event_registered:
                if flag:
                    self.enable_free_sight_from_logic(True)
                else:
                    ctrl = self.scene.get_com('PartCtrl')
                    if ctrl and not ctrl.is_touching_scene():
                        self.enable_free_sight_from_logic(False)
            self.send_event('E_DISABLE_ROCKER_ANIM_DIR', flag)
        enable_func = self.enable_real_follow if self.follow_mode == MODE_REAL_FOLLOW else self.enable_simulate_follow
        enable_func(flag)
        return

    def _calculate_horizontal_offset(self, follow_id):
        groupmate_id_list = self.ev_g_groupmate()
        self_index, other_follower_index = (-1, -1)
        for index, eid in enumerate(groupmate_id_list):
            if eid == self.unit_obj.id:
                self_index = index
            elif eid != follow_id:
                other_follower_ent = self.battle.get_entity(eid)
                if other_follower_ent and other_follower_ent.logic and other_follower_ent.logic.is_valid():
                    other_follower_index = index

        if other_follower_index == -1:
            self.horizontal_offset = -1.5 * NEOX_UNIT_SCALE
        elif self_index < other_follower_index:
            self.horizontal_offset = -1.5 * NEOX_UNIT_SCALE
        else:
            self.horizontal_offset = 1.5 * NEOX_UNIT_SCALE

    def _update_target_pos(self, dt=0.0):
        target_forward = self.follow_lent.ev_g_model_forward()
        self.target_pos = self.follow_lent.ev_g_position()
        if target_forward:
            self.target_pos -= target_forward * 2.0 * NEOX_UNIT_SCALE
            right = target_forward.cross(UP_UNIT)
            self.target_pos += right * self.horizontal_offset
        self.target_pos.y += 0.9 * NEOX_UNIT_SCALE
        if self.target_pos_intrp_offset:
            self.intrp_cost_time += dt
            if self.intrp_cost_time >= TARGET_POS_CONSUME_DURATION:
                self.intrp_cost_time = TARGET_POS_CONSUME_DURATION
            self.target_pos += self.target_pos_intrp_offset * (1 - self.intrp_cost_time / TARGET_POS_CONSUME_DURATION)
            if self.intrp_cost_time == TARGET_POS_CONSUME_DURATION:
                self.target_pos_intrp_offset = None
        return

    def refresh_update_order(self):
        if self.follow_lent and self.follow_lent.is_valid():
            self.follow_lent.send_event('E_REFRESH_HIGH_FRAME_TICK_TIMER')
        if self.follow_mode == MODE_SIMULATE_FOLLOW:
            if self.simulate_follow_timer > -1:
                global_data.game_mgr.get_fix_logic_timer().unregister(self.simulate_follow_timer)
            self.simulate_follow_timer = global_data.game_mgr.get_fix_logic_timer().register(func=self.simulate_follow_tick, interval=1, timedelta=True)
            self.simulate_follow_tick(0)

    def check_follow_entity_available(self):
        follow_id = self.sd.ref_parachute_follow_target
        if follow_id is None or self.quit_clock >= self.max_quit_count:
            self.is_avatar and self.lose_follow_target()
            return False
        else:
            if not self.follow_lent or not self.follow_lent.is_valid():
                self.quit_clock += 1
                ent = self.battle.get_entity(follow_id)
                if not ent or not ent.logic or not ent.logic.is_valid():
                    return False
                self._calculate_horizontal_offset(follow_id)
                self.follow_lent = ent.logic
                self.is_avatar and self.follow_lent.send_event('E_SET_PARACHUTE_FOLLOWED', True)
                self.refresh_update_order()
            if self.follow_lent.ev_g_get_state(ST_DEAD) or not self.follow_lent.ev_g_connect_state():
                self.is_avatar and self.lose_follow_target()
                return False
            if self.follow_lent.share_data.ref_parachute_stage == STAGE_PLANE:
                self.quit_clock += 1
                return False
            return True

    def real_follow_tick(self, dt):
        if not self.check_follow_entity_available():
            return
        else:
            self.update_model_rotation(dt)
            if self.need_update:
                new_stage = self.follow_lent.share_data.ref_parachute_stage
                cur_pos = self.ev_g_position()
                if cur_pos is None:
                    return
                if new_stage != STAGE_LAND:
                    self._update_target_pos()
                    if cur_pos.y < self.target_pos.y - NEOX_UNIT_SCALE:
                        self.initialize_model_pos_y()
                        cur_time = time.time()
                        interval = cur_time - self.last_drag_self_timestamp
                        if interval < 0.8:
                            self.drag_duration += interval
                            if self.drag_duration > self.max_drag_duration:
                                self.lose_follow_target()
                                return
                        else:
                            self.drag_duration = 0
                        self.last_drag_self_timestamp = cur_time
                if self.target_pos is None:
                    return
                if new_stage == STAGE_PARACHUTE_DROP and new_stage != self.follow_target_parachute_stage:
                    self.initialize_model_pos_y()
                self.follow_target_parachute_stage = new_stage
                cur_pos_high = math3d.vector(cur_pos)
                cur_pos_high.y = self.target_pos.y
                if (self.target_pos - cur_pos_high).length <= 2 * NEOX_UNIT_SCALE:
                    if self.follow_target_parachute_stage != STAGE_LAND:
                        self.enable_real_follow(False)
                        self.target_pos_intrp_offset = self.target_pos - cur_pos
                        self.intrp_cost_time = 0.0
                        self.enable_simulate_follow(True)
                    else:
                        self.lose_follow_target()
                elif self.ev_g_is_character_active():
                    self.send_event('E_MOVE_TO', self.target_pos, 1.0)
                else:
                    self.send_event('E_STOP_MOVE_TO')
                    self.send_event('E_MOVE_STOP')
            return

    def on_parachute_vertical_speed_changed(self, vertical_speed):
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_PARACHUTE_VERTICAL_SPEED_CHANGED, (vertical_speed,), False])
        self.cur_vertical_speed = vertical_speed

    def get_parachute_vertical_speed(self):
        return self.cur_vertical_speed

    def simulate_follow_tick(self, dt):
        if not self.check_follow_entity_available():
            return
        else:
            if self.follow_lent.share_data.ref_parachute_stage == STAGE_LAND:
                self.is_avatar and self.lose_follow_target()
                return
            if self.is_avatar:
                follow_target_vertical_speed = self.follow_lent.ev_g_parachute_vertical_speed()
                if self.last_vertical_speed != follow_target_vertical_speed and follow_target_vertical_speed > 0.0:
                    self.last_vertical_speed = follow_target_vertical_speed
                    global_data.emgr.emit('parachute_speed_changed', follow_target_vertical_speed)
            last_target_pos = self.target_pos
            self._update_target_pos(dt)
            move_vec = math3d.vector(0, 0, 0)
            if last_target_pos is not None and dt > 0:
                move_vec = self.target_pos - last_target_pos
                self.sd.ref_parachute_follow_velocity = move_vec * (1.0 / dt)
                not move_vec.is_zero and move_vec.normalize()
            if G_POS_CHANGE_MGR:
                self.notify_pos_change(self.target_pos)
            else:
                self.send_event('E_POSITION', self.target_pos)
            self.update_model_rotation(dt)
            cur_anim = self.follow_lent.share_data.ref_low_body_anim
            if self.sd.ref_low_body_anim != cur_anim:
                cur_anim_dir_type = self.follow_lent.share_data.ref_low_body_anim_dir_type
                self.send_event('E_POST_ACTION', cur_anim, LOW_BODY, cur_anim_dir_type, loop=True)
            self.update_anim_dir_interval += dt
            force_update = self.update_anim_dir_interval > 0.2
            dir_x = self.follow_lent.share_data.ref_anim_param.get('dir_x', None)
            dir_y = self.follow_lent.share_data.ref_anim_param.get('dir_y', None)
            if force_update or dir_x != self.last_dir_x or dir_y != self.last_dir_y:
                if dir_x is not None:
                    self.last_dir_x = dir_x
                    self.last_dir_y = dir_y
                    self.send_event('E_CHANGE_ANIM_MOVE_DIR', dir_x, dir_y)
            if force_update:
                self.update_anim_dir_interval = 0.0
            if self.is_avatar:
                result = self.scene.scene_col.hit_by_ray(self.target_pos, self.target_pos + move_vec * NEOX_UNIT_SCALE, 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, True)
                if self.ev_g_char_waiting() or result and result[0]:
                    self.enable_simulate_follow(False)
                    if self.target_pos_intrp_offset:
                        self.target_pos_intrp_offset = None
                    if self.is_avatar:
                        self.enable_real_follow(True)
            return

    def enable_real_follow(self, flag):
        if self.need_update == flag:
            return
        self.need_update = flag
        self.send_event('E_SET_ENABLE_INITIATIVE_STOP', not flag)
        if flag:
            self.follow_mode = MODE_REAL_FOLLOW
            self.send_event('E_CALL_SYNC_METHOD', 'switch_follow_parachute_mode', (MODE_REAL_FOLLOW,))
            self.sd.ref_parachute_follow_horizontal_speed_scale = 1.03
            self.sd.ref_parachute_follow_vertical_speed_scale = 1.01
        else:
            self.sd.ref_parachute_follow_horizontal_speed_scale = 1.0
            self.sd.ref_parachute_follow_vertical_speed_scale = 1.0
            self.send_event('E_STOP_MOVE_TO')
            self.send_event('E_MOVE_STOP')

    def enable_simulate_follow(self, flag):
        if self.simulate_follow_enabled == flag:
            return
        self.simulate_follow_enabled = flag
        if flag:
            self.follow_mode = MODE_SIMULATE_FOLLOW
            if self.is_avatar:
                self.send_event('E_CALL_SYNC_METHOD', 'switch_follow_parachute_mode', (MODE_SIMULATE_FOLLOW,))
                self.send_event('E_FORCE_DEACTIVE')
            self.refresh_update_order()
            if not self.simulate_follow_enabled:
                return
        else:
            if self.simulate_follow_timer > -1:
                global_data.game_mgr.get_fix_logic_timer().unregister(self.simulate_follow_timer)
                self.simulate_follow_timer = -1
            if self.is_avatar:
                if self.follow_lent and self.follow_lent.is_valid():
                    self._update_target_pos()
                self.send_event('E_FOOT_POSITION', self.target_pos)
                if not self.ev_g_char_waiting():
                    self.send_event('E_FORCE_ACTIVE')
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0.0, 0.0)
        self.send_event('E_ENABLE_PARACHUTE_SIMULATE_FOLLOWING', flag)

    def is_simulate_follow_enabled(self):
        return self.simulate_follow_enabled

    def enable_free_sight_from_logic(self, flag):
        if flag:
            global_data.emgr.scene_on_touched += self.scene_on_touched
        else:
            global_data.emgr.scene_on_touched -= self.scene_on_touched
        global_data.emgr.enable_free_sight_from_logic.emit(flag)
        self.event_registered = flag

    def scene_on_touched(self, flag):
        if not self.parachute_follow_enabled and not flag:
            if self.event_registered:
                self.enable_free_sight_from_logic(False)

    def refresh_follow_free_sight_camera(self):
        if self.event_registered:
            global_data.emgr.enable_free_sight_from_logic.emit(True)