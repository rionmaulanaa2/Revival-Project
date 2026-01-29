# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/MountLogic.py
from __future__ import absolute_import
import math
from .StateBase import StateBase, clamp
from logic.gcommon.cdata.mecha_status_config import *
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon import editor
from copy import deepcopy
from logic.gutils import mecha_skin_utils

@editor.state_exporter({('anim_duration', 'param'): {'zh_name': '\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x95\xbf','min_val': 1,'max_val': 4},('mount_duration', 'param'): {'zh_name': '\xe4\xb8\x8a\xe6\x9c\xba\xe7\x94\xb2\xe6\x97\xb6\xe9\x97\xb4','min_val': 1,'max_val': 4},('break_time', 'param'): {'zh_name': '\xe4\xb8\x8a\xe6\x9c\xba\xe7\x94\xb2\xe6\x89\x93\xe6\x96\xad\xe7\x82\xb9','min_val': 1,'max_val': 4}})
class Mount(StateBase):
    BIND_EVENT = {'E_RESUME_MOUNT': 'resume',
       'E_ON_ACTION_ENTER_MECHA': 'active_self',
       'E_TRY_ENABLE_SYNC': 'try_enable_sync',
       'G_MOUNT_TIME': 'get_mount_time',
       'G_MOUNT_SLERP_START_TIME': 'get_mount_slerp_start_time',
       'G_PRE_MOUNT_TRK_INFO': 'get_pre_mount_trk_info',
       'E_TRY_DISABLE_MOVE_SYNC': 'try_disable_move_sync'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Mount, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.anim_duration = self.custom_param.get('anim_duration', 4) * 1.0
        self.mount_duration = self.custom_param.get('mount_duration', 3) * 1.0
        self.break_time = self.custom_param.get('break_time', 2.5) * 1.0
        self.hide_time = self.custom_param.get('hide_time', 2)
        self.camera_slerp_start_time = self.custom_param.get('slerp_start_time', 2.2)
        self.camera_pre_mount_trk_info = self.custom_param.get('pre_mount_trk_info', {})
        action_key = 'share' if self.unit_obj.get_owner().is_share() else 'default'
        self.action_param = self.custom_param.get('action_param', {}).get(action_key)

    def can_break(self):
        if self.ev_g_is_avatar():
            self.send_event('E_ENABLE_SYNC', True)
        break_states = set([MC_MOVE, MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_JUMP_1, MC_DASH])
        self.send_event('E_ADD_WHITE_STATE', break_states, self.sid)

    def get_mount_time(self):
        return self.mount_duration

    def get_mount_slerp_start_time(self):
        return self.camera_slerp_start_time

    def get_pre_mount_trk_info(self):
        return self.camera_pre_mount_trk_info

    def active_self(self):
        if not self.ev_g_is_avatar():
            self.un_avatar_mount()
        else:
            super(Mount, self).active_self()
            bat = self.unit_obj.get_battle()
            if bat and bat.is_in_settle_celebrate_stage() and self.unit_obj.get_owner().is_share():
                unmount_action_param = self.ev_g_celebrate_unmount_action()
                if unmount_action_param:
                    trigger_time, anim_info = self.convert_anim_info(unmount_action_param)
                    clip_name, part, blend_dir, kwargs = anim_info
                    idle_name = self.ev_g_celebrate_idle_anim_name()
                    if self.sd.ref_low_body_anim == idle_name:
                        self.send_event('E_POST_ACTION', clip_name, part, blend_dir, **kwargs)
                        ani_time = self.ev_g_get_anim_length(clip_name)
                        self.send_event('E_ANIM_RATE', part, ani_time / 0.1)
        global_data.game_mgr.delay_exec(self.hide_time, self.hide_driver)

    def enter(self, leave_states):
        super(Mount, self).enter(leave_states)
        if self.ev_g_is_cam_target():
            model = self.ev_g_model()
            if model and model.valid:
                yaw = model.rotation_matrix.forward.yaw
                global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(yaw, 0, False, 0)
        if self.ev_g_is_avatar():
            self.pause()
            global_data.game_mgr.delay_exec(0.3, self.resume)
            self.delay_call(self.break_time, self.can_break)
            self.send_event('E_ANIM_RATE', LOW_BODY, self.anim_duration / self.mount_duration)
        if self.action_param:
            trigger_time, anim_info = self.convert_anim_info(self.action_param)
            clip_name, part, blend_dir, kwargs = anim_info
            self.send_event('E_POST_ACTION', clip_name, part, blend_dir, **kwargs)

    def check_transitions(self):
        if self.elapsed_time > self.mount_duration:
            driver = EntityManager.getentity(self.sd.ref_driver_id)
            if driver and driver.logic:
                driver.logic.send_event('E_MECHA_MOUNT_COMPLETE')
            self.disable_self()
            return MC_STAND
        if self.elapsed_time > self.break_time + 0.1:
            rocker_dir = self.sd.ref_rocker_dir
            if rocker_dir and not rocker_dir.is_zero:
                return MC_MOVE

    def exit(self, enter_states):
        super(Mount, self).exit(enter_states)
        if self.ev_g_is_avatar():
            self.send_event('E_INIT_SPRING_ANI')
        self.send_event('E_ANIM_RATE', LOW_BODY, 1)
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        driver = EntityManager.getentity(self.sd.ref_driver_id)
        if driver and driver.logic:
            driver.logic.send_event('E_HIDE_MODEL')
        if self.ev_g_is_avatar() or self.sd.ref_is_agent:
            self.send_event('E_ENABLE_SYNC', True)
            self.send_event('E_ENABLE_MOVE_SYNC_SENDER', True)
            return
        self.send_event('E_DISABLE_BEHAVIOR')

    def try_enable_sync(self):
        if self.is_active:
            return
        self.send_event('E_ENABLE_SYNC', True)

    def try_disable_move_sync(self):
        if self.is_active:
            if self.sd.ref_is_agent:
                return
            self.send_event('E_ENABLE_MOVE_SYNC_SENDER', False)

    def hide_driver(self):
        driver = EntityManager.getentity(self.sd.ref_driver_id)
        if driver and driver.logic:
            driver.logic.send_event('E_HIDE_MODEL')

    def un_avatar_mount(self):
        self.enter(set())


class MountInFreeSightMode(Mount):

    def enter(self, leave_states):
        super(MountInFreeSightMode, self).enter(leave_states)
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = False

    def exit(self, enter_states):
        super(MountInFreeSightMode, self).exit(enter_states)
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = True


@editor.state_exporter({('eject_time', 'param'): {'zh_name': '\xe5\xbc\xb9\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4','min_val': 0.1,'max_val': 2,'explain': '\xe7\x82\xb9\xe5\x87\xbb\xe7\xa6\xbb\xe5\xbc\x80\xe6\x9c\xba\xe7\x94\xb2\xe6\x8c\x89\xe9\x92\xae\xe5\x90\x8e\xef\xbc\x8c\xe7\xa6\xbb\xe5\xbc\x80\xe6\x9c\xba\xe7\x94\xb2\xe7\x9a\x84\xe5\xae\x9e\xe9\x99\x85\xe6\x97\xb6\xe9\x97\xb4'}})
class UnMount(StateBase):
    BIND_EVENT = {'E_ON_LEAVE_MECHA_START': 'active_self',
       'G_CELEBRATE_UNMOUNT_ACTION': 'get_celebrate_unmount_action',
       'G_CELEBRATE_IDLE_ANIM_NAME': 'get_celebrate_idle_ani_name'
       }

    def read_data_from_custom_param(self):
        self.eject_time = self.custom_param.get('eject_time', 2)
        self.anim_time = self.custom_param.get('anim_time', 4)
        action_key = 'share' if self.unit_obj.get_owner().is_share() else 'default'
        self.action_param = self.custom_param.get('action_param', {}).get(action_key)
        self.eject_anim_time_tag = self.custom_param.get('eject_anim_time_tag', False)
        self.eject_anim_time = self.custom_param.get('eject_anim_time', None) if self.eject_anim_time_tag else None
        return

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(UnMount, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._celebrate_timer = None
        self.read_data_from_custom_param()
        return

    def active_self(self):
        if self.sd.ref_is_robot:
            self.send_event('E_CLEAR_BEHAVIOR')
        if self.ev_g_is_avatar():
            self.send_event('E_LEAVE_MECHA_SENT', False)
            super(UnMount, self).active_self()
        else:
            self.un_avatar_leave()

    def un_avatar_leave(self):
        self.enter(set())
        self.update(0.01)

        def notify_leave():
            if self and self.is_valid():
                self.send_event('E_NOTIFY_PASSENGER_LEAVE')

        global_data.game_mgr.delay_exec(self.eject_time, notify_leave)

    def enter(self, leave_states):
        super(UnMount, self).enter(leave_states)
        self.send_event('E_STOP_WP_TRACK')
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_CLEAR_TWIST_PITCH')
        self.delay_call(self.eject_time, lambda : self.send_event('E_NOTIFY_PASSENGER_LEAVE'))
        if self.action_param:
            if self.eject_anim_time_tag:
                self.send_event('E_ANIM_RATE', LOW_BODY, self.eject_anim_time / self.eject_time)
            trigger_time, anim_info = self.convert_anim_info(self.action_param)
            clip_name, part, blend_dir, kwargs = anim_info
            self.send_event('E_POST_ACTION', clip_name, part, blend_dir, **kwargs)
        bat = self.unit_obj.get_battle()
        if bat and bat.is_in_settle_celebrate_stage() and self.unit_obj.get_owner().is_share():
            self.check_show_celebrate()

    def check_show_celebrate(self):
        action_key = 'share_celebrate'
        celebrate_action_param = self.custom_param.get('action_param', {}).get(action_key, {})
        if celebrate_action_param:

            def celebrate():
                self._celebrate_timer = None
                if self.is_valid():
                    bat = self.unit_obj.get_battle()
                    if bat and bat.is_in_settle_celebrate_stage() and self.unit_obj.get_owner().is_share():
                        self.send_event('E_CLEAR_UP_BODY_ANIM')
                        trigger_time, anim_info = self.convert_anim_info(celebrate_action_param)
                        clip_name, part, blend_dir, kwargs = anim_info
                        self.send_event('E_POST_ACTION', clip_name, part, blend_dir, **kwargs)
                return

            self.clear_celebrate_timer()
            from common.utils.timer import CLOCK
            tmr = global_data.game_mgr.get_logic_timer()
            self._celebrate_timer = tmr.register(func=celebrate, times=1, mode=CLOCK, interval=1)

    def update(self, dt):
        super(UnMount, self).update(dt)
        if self.elapsed_time > self.anim_time:
            self.disable_self()
            if not self.ev_g_is_avatar():
                self.send_event('E_DISABLE_BEHAVIOR')

    def destroy(self):
        super(UnMount, self).destroy()
        self.clear_celebrate_timer()

    def exit(self, enter_states):
        super(UnMount, self).exit(enter_states)
        self.clear_celebrate_timer()

    def clear_celebrate_timer(self):
        if self._celebrate_timer:
            global_data.game_mgr.get_logic_timer().unregister(self._celebrate_timer)
            self._celebrate_timer = None
        return

    def get_celebrate_unmount_action(self):
        action_key = 'share'
        unmount_action_param = self.custom_param.get('action_param', {}).get(action_key)
        if not unmount_action_param:
            action_param = self.state_info.get('action_param', None)
            if action_param:
                if isinstance(action_param, list):
                    unmount_action_param = action_param[-1]
        return unmount_action_param

    def get_celebrate_idle_ani_name(self):
        action_key = 'share_celebrate'
        celebrate_action_param = self.custom_param.get('action_param', {}).get(action_key, {})
        if celebrate_action_param:
            trigger_time, anim_info = self.convert_anim_info(celebrate_action_param)
            clip_name, part, blend_dir, kwargs = anim_info
            return clip_name
        return ''

    def refresh_action_param(self, action_param, custom_param):
        super(UnMount, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.read_data_from_custom_param()