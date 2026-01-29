# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8035.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from logic.gutils.tech_pass_utils import set_prez_transparent
from logic.gutils.slash_utils import LockedTargetFinder
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
from math import acos, fabs
import logic.gcommon.common_utils.bcast_utils as bcast
from common.utils.timer import RELEASE
import math3d
import world
import weakref
SHIRANUI_FAN_WEAPON_ID = 803503
DASH_ANIM_WITH_SPECIAL_EFFECT = ('dash_fly_start', 'dash_fly_loop')
WING_ANGLE_UP_BOUNDARY = 1.0
WING_ANGLE_DOWN_BOUNDARY = 0.27
WING_ANGLE_BOUNDARY_DIST = WING_ANGLE_UP_BOUNDARY - WING_ANGLE_DOWN_BOUNDARY
OPACITY_INTRP_SPEED = 255.0 / 0.2
OPACITY_THRESHOLD = 2.0
SLASH_HIT_EFFECT_ID = '100'
SLASH_HIT_SCREEN_EFFECT_ID = '101'
SLASH_HIT_SCREEN_EFFECT_STATE_ID = 'screen_hit'
DASH_EFFECT_ID = '102'
DASH_EFFECT_STATE_ID = 'dash'

class ComMechaEffect8035(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHIRANUI_FAN_CREATED': 'on_shiranui_fan_created',
       'E_SHIRANUI_FAN_DESTROYED': 'on_shiranui_fan_destroyed',
       'E_SHIRANUI_FAN_LOCK_RANGE_ADD_SCALE_CHANGED': 'update_locked_fan_finder_parameters',
       'E_ON_SKIN_SUB_MODEL_LOADED': 'on_skin_sub_model_loaded',
       'E_SHOW_SLASH_HIT_SFX': 'on_show_slash_hit_sfx',
       'E_SHOW_SLASH_HIT_SCREEN_SFX': 'on_show_slash_hit_screen_sfx',
       'E_SHOW_DASH_EFFECT': 'on_show_dash_effect'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8035, self).init_from_dict(unit_obj, bdict)
        self.shiranui_fan_unit_list = []
        self.locked_fan_finder = LockedTargetFinder(self, self.get_candidate_target_func, locked_target_changed_callback=self.locked_fan_changed_callback, get_target_pos_func=self.get_target_pos_func, ignore_enemy_block=True)
        conf = confmgr.get('firearm_config', str(SHIRANUI_FAN_WEAPON_ID), default={})
        self.conf_aim_dist, self.conf_aim_pitch, self.conf_aim_yaw = conf['fAutoAimDistance'] * NEOX_UNIT_SCALE, conf['fAutoAimPitch'], conf['fAutoAimYaw']
        self.sd.ref_cur_locked_fan_unit = None
        self.sd.ref_last_locked_fan_unit = None
        self.sd.ref_switch_locked_fan_unit_time = 0
        self.need_handle_anim_logic = not global_data.feature_mgr.is_support_model_decal()
        self.last_low_body_anim = None
        self.model_ref = None
        self.update_wing_opacity_appearance_timer = None
        self.cur_opacity = 255
        self.target_opacity = 255
        self.opacity_diff_value = 0
        self.opacity_changed_symbol = 1
        return

    def on_init_complete(self):
        self.update_locked_fan_finder_parameters()

    def destroy(self):
        if self.locked_fan_finder:
            self.locked_fan_finder.destroy()
            self.locked_fan_finder = None
        if self.update_wing_opacity_appearance_timer:
            global_data.game_mgr.unregister_logic_timer(self.update_wing_opacity_appearance_timer)
            self.update_wing_opacity_appearance_timer = None
        self.sd.ref_cur_locked_fan_unit = None
        self.sd.ref_last_locked_fan_unit = None
        super(ComMechaEffect8035, self).destroy()
        self.model_ref = None
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8035, self).on_model_loaded(model)
        self.model_ref = weakref.ref(model)

    def on_skin_sub_model_loaded(self):
        if self.ev_g_is_avatar():
            interval = 1
        else:
            lod_level = self.ev_g_lod_level()
            interval = lod_level + 2
        self.update_wing_opacity_appearance_timer = global_data.game_mgr.register_logic_timer(self.update_wing_opacity_appearance, interval=interval, times=-1, timedelta=True)

    def get_candidate_target_func(self):
        return self.shiranui_fan_unit_list

    def locked_fan_changed_callback(self, new_target):
        self.sd.ref_last_locked_fan_unit = self.sd.ref_cur_locked_fan_unit
        self.sd.ref_cur_locked_fan_unit = new_target
        self.sd.ref_switch_locked_fan_unit_time = global_data.game_time
        self.send_event('E_LOCKED_FAN_CHANGED', new_target)

    @staticmethod
    def get_target_pos_func(target):
        return target.ev_g_can_contain_mecha_pos()

    def on_shiranui_fan_created(self, unit_obj):
        if unit_obj not in self.shiranui_fan_unit_list:
            self.shiranui_fan_unit_list.append(unit_obj)
            self.locked_fan_finder.begin()

    def on_shiranui_fan_destroyed(self, unit_obj):
        if unit_obj in self.shiranui_fan_unit_list:
            self.shiranui_fan_unit_list.remove(unit_obj)
        if not self.shiranui_fan_unit_list:
            self.locked_fan_finder.end(need_unlock_target=True)

    def update_locked_fan_finder_parameters(self):
        self.locked_fan_finder.set_parameters_directly(self.conf_aim_dist * (1 + self.sd.ref_shiranui_fan_lock_range_add_scale), (
         self.conf_aim_pitch, self.conf_aim_yaw), 0)

    def on_trigger_anim_effect(self, anim_name, part, force_trigger_effect=False, socket_index=-1):
        need_check = self.need_handle_anim_logic and part == LOW_BODY
        if need_check:
            if anim_name in DASH_ANIM_WITH_SPECIAL_EFFECT and self.last_low_body_anim not in DASH_ANIM_WITH_SPECIAL_EFFECT:
                self.send_event('E_PAUSE_OUTLINE', True)
        super(ComMechaEffect8035, self).on_trigger_anim_effect(anim_name, part, force_trigger_effect, socket_index)
        if need_check:
            if anim_name not in DASH_ANIM_WITH_SPECIAL_EFFECT and self.last_low_body_anim in DASH_ANIM_WITH_SPECIAL_EFFECT:
                self.send_event('E_REFRESH_MODEL')
                self.send_event('E_PAUSE_OUTLINE', False)
            self.last_low_body_anim = anim_name

    def update_mecha_effect_level_for_lod(self, lod_level):
        super(ComMechaEffect8035, self).update_mecha_effect_level_for_lod(lod_level)
        if not self.ev_g_is_avatar():
            if self.update_wing_opacity_appearance_timer:
                interval = lod_level + 2
                global_data.game_mgr.get_logic_timer().set_interval(self.update_wing_opacity_appearance_timer, interval)

    def update_wing_opacity_appearance(self, dt):
        if not self.model_ref:
            return
        else:
            model = self.model_ref()
            if not model or not model.valid:
                return
            if self.sd.ref_model_opacity is None:
                cur_opacity_rate = 1.0
            else:
                cur_opacity_rate = self.sd.ref_model_opacity / 255.0
            wing_model = self.sd.ref_socket_res_agent.model_res_map['wing'][0]
            dir_up = model.get_bone_matrix('bone_wing_r_up', world.SPACE_TYPE_PARENT).right
            dir_down = model.get_bone_matrix('bone_wing_r_down', world.SPACE_TYPE_PARENT).right
            angle = acos(dir_up.dot(dir_down))
            if angle < WING_ANGLE_DOWN_BOUNDARY:
                opacity = 0
                threshold = 0
            elif angle > WING_ANGLE_UP_BOUNDARY:
                opacity = 255 * cur_opacity_rate
                threshold = 0
            else:
                opacity = 255 * (angle - WING_ANGLE_DOWN_BOUNDARY) / WING_ANGLE_BOUNDARY_DIST * cur_opacity_rate
                threshold = OPACITY_THRESHOLD
            if fabs(self.target_opacity - opacity) > threshold:
                self.target_opacity = opacity
                if self.target_opacity > self.cur_opacity:
                    self.opacity_changed_symbol = 1
                else:
                    self.opacity_changed_symbol = -1
                self.opacity_diff_value = fabs(self.target_opacity - self.cur_opacity)
            if self.opacity_diff_value == 0:
                return
            delta_opacity = OPACITY_INTRP_SPEED * dt
            if delta_opacity > self.opacity_diff_value:
                self.cur_opacity = self.target_opacity
                self.opacity_diff_value = 0
            else:
                self.cur_opacity += delta_opacity * self.opacity_changed_symbol
                self.opacity_diff_value -= delta_opacity
            if global_data.is_multi_pass_support:
                wing_model.enable_prez_transparent(True, self.cur_opacity / 255)
            elif global_data.feature_mgr.is_support_ext_tech_fix():
                set_prez_transparent(wing_model, True, int(self.cur_opacity))
            return

    def on_show_slash_hit_sfx(self, pos, rot=None):
        self.on_trigger_disposable_effect(SLASH_HIT_EFFECT_ID, pos, rot, need_sync=True)

    def on_show_slash_hit_screen_sfx(self):
        self.on_trigger_state_effect(SLASH_HIT_SCREEN_EFFECT_STATE_ID, SLASH_HIT_SCREEN_EFFECT_ID, force=True, need_sync=True)

    def on_show_dash_effect(self, flag):
        effect_id = DASH_EFFECT_ID if flag else ''
        self.on_trigger_state_effect(DASH_EFFECT_STATE_ID, effect_id, need_sync=True)