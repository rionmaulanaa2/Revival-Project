# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/BaseMechaAimUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
from logic.gcommon.common_const.weapon_const import SHOOT_FROM_CAMERA_OPTIMIZED
from logic.client.const import game_mode_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
from .MechaBulletWidget import MechaBulletWidget, MAIN_WEAPON
from common.utils.cocos_utils import neox_pos_to_cocos
from common.utils.timer import RELEASE, CLOCK
from common.uisys.uielment.CCSprite import CCSprite
from common.utils.cocos_utils import ccp
from common.const import uiconst
from common.cfg import confmgr
import math3d
import cc
WEAPON_ID_TO_IGNORE_FIRE_POS_MAP = {}
IS_GRENADE_WEAPON_FLAG = {}
PREDICTED_HIT_POSITION_INTRP_DURATION = 0.2
TEMP_VEC_2 = math3d.vector2(0, 0)

class BaseMechaAimUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8022'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    IS_FULLSCREEN = True
    ASSOCIATE_UI_LIST = [
     'FrontSightUI']
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def on_init_panel(self):
        self.panel.HasAnimation('show') and self.panel.PlayAnimation('show')
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.init_parameters()
        self.init_aim_spread_mgr()
        self.init_bullet_widget()
        self.hide_main_ui(self.ASSOCIATE_UI_LIST)
        self.init_front_sight_extra_info()

    def init_parameters(self):
        self.player = None
        self.mecha = None
        self.aim_spread_mgr = None
        self.bullet_widget = None
        self.update_extra_info_tag = 1
        self.update_extra_info_timer = None
        self.cur_extra_info_weapon_pos = None
        self.fire_pos_blocking = False
        self.cur_weapon_ignore_fire_pos = None
        self.cur_weapon_is_grenade = False
        self.need_intrp_predicted_hit_position = False
        self.update_predicted_hit_position_timer = None
        self.muzzle_in_barrier = False
        self.cur_predicted_hit_position = math3d.vector2(0, 0)
        self.target_predicted_hit_position = math3d.vector2(0, 0)
        self.cur_hit_position_intrp_time = 0
        emgr = global_data.emgr
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)
        return

    def init_aim_spread_mgr(self):
        raise NotImplementedError('BaseMechaAimUI::init_aim_spread_mgr should be overloaded')

    def init_bullet_widget(self):
        weapon_info = self.WEAPON_INFO
        if global_data.game_mode and global_data.game_mode.is_pve():
            pve_weapon_info = getattr(self.__class__, 'PVE_WEAPON_INFO', None)
            if pve_weapon_info is not None:
                weapon_info = self.PVE_WEAPON_INFO
        if global_data.is_pc_mode or not weapon_info:
            if self.panel.nd_bullet_ob:
                self.panel.nd_bullet_ob.setVisible(False)
                self.panel.nd_bullet_ob.nd_bullet.setVisible(False)
            return
        else:
            self.bullet_widget = MechaBulletWidget(self.panel, weapon_info)
            return

    def on_finalize_panel(self):
        self.stop_update_front_sight_extra_info()
        self._unregister_update_predicted_hit_position_timer()
        self.unbind_ui_event(self.player)
        self.show_main_ui()
        self.player = None
        self.mecha = None
        self.destroy_widget('aim_spread_mgr')
        self.destroy_widget('bullet_widget')
        return

    def disappear(self):
        if self.panel.HasAnimation('disappear'):
            self.panel.PlayAnimation('disappear')
            delay = self.panel.GetAnimationMaxRunTime('disappear')
            self.panel.SetTimeOut(delay, lambda : self.close())
        else:
            self.close()

    def on_cam_lplayer_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        if self.player:
            self.bind_ui_event(self.player)
        if global_data.player and self.player:
            if global_data.player.id != player.id:
                self.on_enter_observe(True)
            else:
                self.on_enter_observe(False)
        self.on_camera_switch_to_state(global_data.cam_data.camera_state_type)

    def on_mecha_setted(self, mecha):
        raise NotImplementedError('BaseMechaAimUI::on_mecha_setted should be overridden')

    def bind_ui_event(self, target):
        pass

    def unbind_ui_event(self, target):
        raise NotImplementedError('BaseMechaAimUI::unbind_ui_event should be overridden')

    def on_enter_observe(self, is_observe):
        if not self.panel.nd_bullet_ob:
            return
        if is_observe:
            self.panel.nd_bullet_ob.setVisible(False)
        else:
            self.panel.nd_bullet_ob.setVisible(True)

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        self.cur_camera_state_type = state
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')

    def init_front_sight_extra_info(self):
        if self.panel.img_muzzle_blocking:
            return
        img_muzzle_blocking = CCSprite.Create('', 'gui/ui_res_2/battle/attack/img_ban.png')
        self.panel.AddChild('img_muzzle_blocking', img_muzzle_blocking)
        img_muzzle_blocking.setAnchorPoint(ccp(0.5, 0.5))
        img_muzzle_blocking.setScale(1.4)
        img_muzzle_blocking.SetPosition('50%', '50%')
        img_muzzle_blocking.setVisible(False)
        if self.panel.img_hit_pos:
            return
        img_hit_pos = CCSprite.Create('', 'gui/ui_res_2/battle/mech_attack/mech_8028/icon_mech_8027hit_type_1.png')
        self.panel.AddChild('img_hit_pos', img_hit_pos)
        img_hit_pos.setAnchorPoint(ccp(0.5, 0.5))
        img_hit_pos.setScale(0.4)
        img_hit_pos.SetPosition('50%', '50%')
        img_hit_pos.setVisible(False)

    def _update_predicted_hit_position(self, dt):
        self.cur_hit_position_intrp_time += dt
        if self.cur_hit_position_intrp_time > PREDICTED_HIT_POSITION_INTRP_DURATION:
            intrp_rate = 1.0
            self.cur_hit_position_intrp_time = PREDICTED_HIT_POSITION_INTRP_DURATION
        else:
            intrp_rate = self.cur_hit_position_intrp_time / PREDICTED_HIT_POSITION_INTRP_DURATION
        TEMP_VEC_2.intrp(self.cur_predicted_hit_position, self.target_predicted_hit_position, intrp_rate)
        self.panel.img_hit_pos.setPosition(cc.Vec2(TEMP_VEC_2.x, TEMP_VEC_2.y))
        if intrp_rate == 1.0:
            self.update_predicted_hit_position_timer = None
            return RELEASE
        else:
            return

    def _register_update_predicted_hit_position_timer(self):
        self.update_predicted_hit_position_timer = global_data.game_mgr.register_logic_timer(self._update_predicted_hit_position, interval=1, times=-1, timedelta=True)

    def _unregister_update_predicted_hit_position_timer(self):
        if self.update_predicted_hit_position_timer:
            global_data.game_mgr.unregister_logic_timer(self.update_predicted_hit_position_timer)
            self.update_predicted_hit_position_timer = None
        return

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
                extra_ray_check_ret = self.mecha.ev_g_extra_ray_check_hit_pos(self.cur_extra_info_weapon_pos, self.cur_weapon_ignore_fire_pos, self.cur_weapon_is_grenade)
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

    def stop_update_front_sight_extra_info(self):
        if self.update_extra_info_timer:
            global_data.game_mgr.unregister_logic_timer(self.update_extra_info_timer)
            self.update_extra_info_timer = None
        self.panel.img_muzzle_blocking.setVisible(False)
        self.panel.img_hit_pos.setVisible(False)
        return

    @execute_by_mode(False, (game_mode_const.GAME_MODE_GOOSE_BEAR,))
    def start_update_front_sight_extra_info(self, weapon_pos, interval=0.1):
        if not self.mecha or not self.mecha.ev_g_is_avatar():
            return
        else:
            self.cur_extra_info_weapon_pos = weapon_pos
            self.cur_weapon_ignore_fire_pos = None
            if global_data.game_mode.is_pve():
                self.panel.img_hit_pos.setVisible(False)
                if self.update_extra_info_timer is None:
                    self.update_extra_info_timer = global_data.game_mgr.register_logic_timer(self.update_extra_info_for_pve, interval=interval, mode=CLOCK)
                self.update_extra_info_for_pve()
            else:
                if self.update_extra_info_timer is None:
                    self.update_extra_info_timer = global_data.game_mgr.register_logic_timer(self.update_extra_info, interval=interval, mode=CLOCK)
                self.update_extra_info()
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
                extra_ray_check_ret = self.mecha.ev_g_extra_ray_check_hit_pos(self.cur_extra_info_weapon_pos, self.cur_weapon_ignore_fire_pos, self.cur_weapon_is_grenade)
                if not extra_ray_check_ret:
                    extra_ray_check_ret = (
                     None, False)
                _, self.muzzle_in_barrier = extra_ray_check_ret
                self.panel.img_muzzle_blocking.setVisible(self.fire_pos_blocking or self.muzzle_in_barrier)
            return