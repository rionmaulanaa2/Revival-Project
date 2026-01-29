# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8009AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI, WEAPON_ID_TO_IGNORE_FIRE_POS_MAP, IS_GRENADE_WEAPON_FLAG
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3
from logic.gcommon.common_const.weapon_const import SHOOT_FROM_CAMERA_OPTIMIZED
from logic.gcommon.common_const.mecha_const import TRIO_STATE_M, TRIO_STATE_S, TRIO_STATE_R
from common.utils.cocos_utils import neox_pos_to_cocos
from logic.gcommon.time_utility import get_server_time
from common.utils.timer import RELEASE
from common.cfg import confmgr
import math3d
import cc
ASSOCIATE_UI_LIST = [
 'FrontSightUI']
STATE_TO_UI_PARAM = {TRIO_STATE_M: ('mode_m', 'gui/ui_res_2/battle/mech_attack/mech_icon_bullet_blue.png'),
   TRIO_STATE_S: ('mode_s', 'gui/ui_res_2/battle/mech_attack/mech_icon_bullet_shotgun.png'),
   TRIO_STATE_R: ('mode_r', 'gui/ui_res_2/battle/mech_attack/mech_icon_missile.png')
   }
STATE_TO_WEAPON_POS_MAP = {TRIO_STATE_M: PART_WEAPON_POS_MAIN1,
   TRIO_STATE_S: PART_WEAPON_POS_MAIN2,
   TRIO_STATE_R: PART_WEAPON_POS_MAIN3
   }
AIM_NODE_SUFFIX = {TRIO_STATE_M: '_m',
   TRIO_STATE_S: '_s',
   TRIO_STATE_R: '_r',
   'FullForce': '_sp'
   }
STATE_TO_LEFTEST_SOCKET_NAME = {TRIO_STATE_M: 'fx_tuji_kaihuo',
   TRIO_STATE_S: 'fx_sandan_kaihuo_zuo',
   TRIO_STATE_R: 'fx_daodan_kaihuo_zuo3'
   }
MAX_FULL_FORCE_ENERGY_PERCENT = 88
MIN_FULL_FORCE_ENERGY_PERCENT = 62
ENERGY_PERCENT_GAP = MAX_FULL_FORCE_ENERGY_PERCENT - MIN_FULL_FORCE_ENERGY_PERCENT

class Mecha8009AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8009'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON,
       PART_WEAPON_POS_MAIN2: MAIN_WEAPON,
       PART_WEAPON_POS_MAIN3: MAIN_WEAPON
       }

    def on_init_panel(self):
        super(Mecha8009AimUI, self).on_init_panel()
        self.init_full_force_widget()
        self._last_anim = None
        return

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel)

        def get_aim_node():
            node = getattr(self.panel, 'nd_aim%s' % AIM_NODE_SUFFIX[self.cur_state], None)
            if node and node.isVisible():
                return node.nd_spread
            else:
                return

        self.aim_spread_mgr.replace_get_aim_node_func(get_aim_node)

    def init_full_force_widget(self):
        self.full_force_widget = global_data.uisystem.load_template_create('battle_mech/fight_hit_mech8009_2', parent=self.panel)
        self.full_force_widget.nd_jet.setVisible(False)

    def on_finalize_panel(self):
        super(Mecha8009AimUI, self).on_finalize_panel()
        if self.full_force_timer is not None:
            global_data.game_mgr.unregister_logic_timer(self.full_force_timer)
            self.full_force_timer = None
        self.full_force_widget = None
        return

    def init_parameters(self):
        self.is_shooting = False
        self.full_force_timer = None
        self.cur_state = TRIO_STATE_M
        self.cur_leftest_socket_name = STATE_TO_LEFTEST_SOCKET_NAME[self.cur_state]
        super(Mecha8009AimUI, self).init_parameters()
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_TRIO_TRANS_STATE', self.on_switch_weapon)
            regist_func('E_ACTIVE_FULL_FORCE', self.active_full_force)
            regist_func('E_REFRESH_MECHA_CONTROL_BUTTON_ICON', self.refresh_mecha_control_button_icon)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.cur_state = self.mecha.ev_g_trio_state()
            self.on_switch_weapon(self.cur_state)
            self.aim_spread_mgr and self.aim_spread_mgr._on_spread()
            enabled, total_time, finish_stamp = self.mecha.ev_g_full_force_enabled_param()
            if enabled:
                self.active_full_force(enabled, total_time, finish_stamp)
                self.refresh_mecha_control_button_icon(True)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_TRIO_TRANS_STATE', self.on_switch_weapon)
            unregist_func('E_ACTIVE_FULL_FORCE', self.active_full_force)
            unregist_func('E_REFRESH_MECHA_CONTROL_BUTTON_ICON', self.refresh_mecha_control_button_icon)
        self.mecha = None
        return

    def active_full_force(self, flag, total_time, finish_timestamp):
        self.full_force_widget.nd_jet.setVisible(flag)
        if flag:
            self.total_time = total_time
            self.finish_timestamp = finish_timestamp
            self.full_force_widget.nd_jet.setVisible(True)
            self.full_force_widget.prog_jet.setPercentage(MAX_FULL_FORCE_ENERGY_PERCENT)
            self.full_force_timer = global_data.game_mgr.register_logic_timer(self.update_full_force_progress, interval=1, times=-1)
            self.cur_state = 'FullForce'
            self.stop_update_front_sight_extra_info()
        else:
            if self.full_force_timer is not None:
                global_data.game_mgr.unregister_logic_timer(self.full_force_timer)
                self.full_force_timer = None
            self.mecha and self.on_switch_weapon(self.mecha.ev_g_trio_state())
        return

    def update_full_force_progress(self):
        cur_left_time = self.finish_timestamp - get_server_time()
        if cur_left_time <= 0:
            cur_left_time = 0
        if self.full_force_widget is not None:
            self.full_force_widget.prog_jet.setPercentage(MIN_FULL_FORCE_ENERGY_PERCENT + ENERGY_PERCENT_GAP * cur_left_time / self.total_time)
        return

    def refresh_mecha_control_button_icon(self, start_full_force=False):
        if start_full_force:
            start_full_force and self.panel.PlayAnimation('mode_sp')
            self.cur_state = 'FullForce'
            self._last_anim = 'mode_sp'

    def on_switch_weapon(self, new_state):
        self.cur_state = new_state
        anim_name, bullet_pic = STATE_TO_UI_PARAM[new_state]
        if self._last_anim:
            if self._last_anim == anim_name:
                return
            self.panel.StopAnimation(self._last_anim)
        self.panel.PlayAnimation(anim_name)
        self._last_anim = anim_name
        if global_data.is_pc_mode:
            mecha_ctrl_ui = global_data.ui_mgr.get_ui('MechaControlMain')
            mecha_ctrl_ui and mecha_ctrl_ui.set_bullet_icon(bullet_pic)
        else:
            self.panel.temp_bullet.img_bullet.SetDisplayFrameByPath('', bullet_pic)
        if self.aim_spread_mgr:
            self.aim_spread_mgr.set_weapon_pos(STATE_TO_WEAPON_POS_MAP[new_state])
        self.cur_leftest_socket_name = STATE_TO_LEFTEST_SOCKET_NAME[self.cur_state]
        self.start_update_front_sight_extra_info(STATE_TO_WEAPON_POS_MAP[self.cur_state])

    def update_extra_info(self):
        if not self.mecha or not self.cur_extra_info_weapon_pos:
            self.update_extra_info_timer = None
            return RELEASE
        else:
            self.update_extra_info_tag ^= 1
            if self.update_extra_info_tag:
                self.fire_pos_blocking = bool(self.mecha.ev_g_pre_check_explode_instant(self.cur_extra_info_weapon_pos))
                self.panel.img_muzzle_blocking.setVisible(self.fire_pos_blocking or self.muzzle_in_barrier)
            else:
                if not self.cur_weapon_ignore_fire_pos:
                    if not self.mecha.sd.ref_wp_bar_mp_weapons:
                        return
                    weapon = self.mecha.sd.ref_wp_bar_mp_weapons.get(self.cur_extra_info_weapon_pos)
                    if not weapon:
                        return
                    weapon_id = weapon.iType
                    if weapon_id not in WEAPON_ID_TO_IGNORE_FIRE_POS_MAP:
                        ignore_fire_pos = confmgr.get('firearm_config', str(weapon_id), 'iIgnoreFirePos')
                        WEAPON_ID_TO_IGNORE_FIRE_POS_MAP[weapon_id] = ignore_fire_pos
                        IS_GRENADE_WEAPON_FLAG[weapon_id] = bool(confmgr.get('grenade_config', str(weapon_id)))
                    self.cur_weapon_ignore_fire_pos = WEAPON_ID_TO_IGNORE_FIRE_POS_MAP[weapon_id]
                    self.cur_weapon_is_grenade = IS_GRENADE_WEAPON_FLAG[weapon_id]
                    if self.cur_weapon_ignore_fire_pos < SHOOT_FROM_CAMERA_OPTIMIZED:
                        self.panel.img_hit_pos.setVisible(False)
                        self._unregister_update_predicted_hit_position_timer()
                if self.cur_weapon_ignore_fire_pos < SHOOT_FROM_CAMERA_OPTIMIZED:
                    return
                scn = global_data.game_mgr.scene
                if not scn:
                    return
                camera = scn.active_camera
                if not camera:
                    return
                extra_ray_check_ret = self.mecha.ev_g_extra_ray_check_hit_pos(self.cur_extra_info_weapon_pos, self.cur_weapon_ignore_fire_pos, self.cur_weapon_is_grenade, self.cur_leftest_socket_name)
                if not extra_ray_check_ret:
                    extra_ray_check_ret = (
                     None, False)
                hit_pos, self.muzzle_in_barrier = extra_ray_check_ret
                self.panel.img_muzzle_blocking.setVisible(self.fire_pos_blocking or self.muzzle_in_barrier)
                if not hit_pos:
                    self.panel.img_hit_pos.setVisible(False)
                    self._unregister_update_predicted_hit_position_timer()
                    return
            x, y = camera.world_to_screen(hit_pos)
            pos = cc.Vec2(*neox_pos_to_cocos(x, y))
            pos = self.panel.convertToNodeSpace(pos)
            if not self.panel.img_hit_pos.isVisible():
                self.panel.img_hit_pos.setVisible(True)
                self.panel.img_hit_pos.setPosition(pos)
                self.cur_predicted_hit_position = math3d.vector2(pos.x, pos.y)
                self.target_predicted_hit_position = self.cur_predicted_hit_position
            else:
                target_predicted_hit_position = math3d.vector2(pos.x, pos.y)
                if not (self.target_predicted_hit_position - target_predicted_hit_position).is_zero:
                    cur_pos = self.panel.img_hit_pos.getPosition()
                    self.cur_predicted_hit_position = math3d.vector2(cur_pos.x, cur_pos.y)
                    self.target_predicted_hit_position = target_predicted_hit_position
                    self.cur_hit_position_intrp_time = 0
                    if not self.update_predicted_hit_position_timer:
                        self._register_update_predicted_hit_position_timer()
            return

    def update_extra_info_for_pve(self):
        if not self.mecha or not self.cur_extra_info_weapon_pos:
            self.update_extra_info_timer = None
            return RELEASE
        else:
            self.update_extra_info_tag ^= 1
            if self.update_extra_info_tag:
                self.fire_pos_blocking = bool(self.mecha.ev_g_pre_check_explode_instant(self.cur_extra_info_weapon_pos))
                self.panel.img_muzzle_blocking.setVisible(self.fire_pos_blocking or self.muzzle_in_barrier)
            else:
                if not self.cur_weapon_ignore_fire_pos:
                    if not self.mecha.sd.ref_wp_bar_mp_weapons:
                        return
                    weapon = self.mecha.sd.ref_wp_bar_mp_weapons.get(self.cur_extra_info_weapon_pos)
                    if not weapon:
                        return
                    weapon_id = weapon.iType
                    if weapon_id not in WEAPON_ID_TO_IGNORE_FIRE_POS_MAP:
                        ignore_fire_pos = confmgr.get('firearm_config', str(weapon_id), 'iIgnoreFirePos')
                        WEAPON_ID_TO_IGNORE_FIRE_POS_MAP[weapon_id] = ignore_fire_pos
                        IS_GRENADE_WEAPON_FLAG[weapon_id] = bool(confmgr.get('grenade_config', str(weapon_id)))
                    self.cur_weapon_ignore_fire_pos = WEAPON_ID_TO_IGNORE_FIRE_POS_MAP[weapon_id]
                    self.cur_weapon_is_grenade = IS_GRENADE_WEAPON_FLAG[weapon_id]
                    if self.cur_weapon_ignore_fire_pos < SHOOT_FROM_CAMERA_OPTIMIZED:
                        self.panel.img_hit_pos.setVisible(False)
                        self._unregister_update_predicted_hit_position_timer()
                if self.cur_weapon_ignore_fire_pos < SHOOT_FROM_CAMERA_OPTIMIZED:
                    return
                scn = global_data.game_mgr.scene
                if not scn:
                    return
                camera = scn.active_camera
                if not camera:
                    return
                extra_ray_check_ret = self.mecha.ev_g_extra_ray_check_hit_pos(self.cur_extra_info_weapon_pos, self.cur_weapon_ignore_fire_pos, self.cur_weapon_is_grenade, self.cur_leftest_socket_name)
                if not extra_ray_check_ret:
                    extra_ray_check_ret = (
                     None, False)
                _, self.muzzle_in_barrier = extra_ray_check_ret
                self.panel.img_muzzle_blocking.setVisible(self.fire_pos_blocking or self.muzzle_in_barrier)
            return