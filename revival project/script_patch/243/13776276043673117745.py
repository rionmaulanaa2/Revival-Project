# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/FightLeftShotUI.py
from __future__ import absolute_import
import cc
import world
from .ShotChecker import ShotChecker
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.utils.cocos_utils import ccp
from logic.gcommon.cdata.status_config import ST_SHOOT, ST_MOVE
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.common_const.animation_const import MOVE_STATE_WALK
from logic.gcommon.common_const.ui_operation_const import LEFT_CONTROL_ZORDER
from logic.gcommon.const import MAIN_WEAPON_LIST
from logic.gcommon.cdata import status_config
from common.const import uiconst

class FightLeftShotUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_left_shot'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    LEFT_SHOT_HIDE_ACT_TAG = 22001
    ACT_CHECK_TAG = 180224
    UI_ACTION_EVENT = {'aim_one_shot_button_1.OnBegin': 'OnBegin_shot_btn',
       'aim_one_shot_button_1.OnDrag': 'OnDrag_shot_btn',
       'aim_one_shot_button_1.OnEnd': 'OnEnd_shot_btn',
       'aim_one_shot_button_1.OnCancel': 'OnEnd_shot_btn',
       'aim_one_shot_button_2.OnBegin': 'OnBegin_shot_btn',
       'aim_one_shot_button_2.OnDrag': 'OnDrag_shot_btn',
       'aim_one_shot_button_2.OnEnd': 'OnEnd_shot_btn',
       'aim_one_shot_button_2.OnCancel': 'OnEnd_shot_btn'
       }
    GLOBAL_EVENT = {'restart_avatar_fire_by_ui': 'restart_fire'
       }

    def on_init_panel(self):
        self.panel.setLocalZOrder(LEFT_CONTROL_ZORDER)
        self.cur_left_fire_sel = uoc.LF_OPE_DEF
        self.init_custom_com()
        self.init_parameters()
        self.init_event()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {uoc.LF_OPE_KEY: 'cur_left_fire_sel'})

    def init_event(self):
        self.init_left_posture_event()

    def on_finalize_panel(self):
        self.unbind_lf_ui_event(self.player)
        self._change_scale_nd_dict = {}
        self.player = None
        if self.custom_ui_com:
            self.custom_ui_com.destroy()
            self.custom_ui_com = None
        return

    def init_parameters(self):
        self.move_spawn_radius = self.panel.shot_bar.getContentSize().width * self.panel.shot_bar.getScale() * 0.9 / 2.0 * self.panel.nd_rocker.getScale()
        self.player = None
        self.is_last_moved = False
        self.is_rocker_enable = False
        self.is_start_fire = False
        self.is_player_first_setted = False
        self.cur_camera_state = None
        self._is_move_rocker = False
        self.is_trying_fire = False
        self.init_special_scale()
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        if player:
            self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted
        econf = {}
        emgr.bind_events(econf)
        return

    def init_special_scale(self):
        self.panel.aim_one_shot_button_1.EnableCustomState(True)
        self.panel.aim_one_shot_button_2.EnableCustomState(True)
        self._change_scale_nd_dict = {self.panel.aim_one_shot_button_1: self.panel.aim_one_shot_button_1,
           self.panel.aim_one_shot_button_2: self.panel.nd_rocker
           }
        self.update_special_scale()

    def update_special_scale(self):
        self._change_scale_old_info = {self.panel.aim_one_shot_button_1: self.panel.aim_one_shot_button_1.getScale(),
           self.panel.nd_rocker: self.panel.nd_rocker.getScale()
           }

    def on_btn_scale_check(self, btn, is_touch):
        relate_btn = self._change_scale_nd_dict.get(btn, None)
        if not relate_btn:
            return
        else:
            old_scale = self._change_scale_old_info.get(relate_btn)
            if is_touch:
                relate_btn.setScale(old_scale * 1.2)
            else:
                relate_btn.setScale(old_scale)
            return

    def on_player_setted(self, player):
        self.unbind_lf_ui_event(self.player)
        self.player = player
        if self.player:
            if not self.is_player_first_setted:
                self.init_left_fire_opt_select()
                self.is_first_initialize = False
            self.on_weapon_in_hand_changed(None)
            self.bind_lf_ui_event(self.player)
        return

    def init_left_posture_event(self):
        emgr = global_data.emgr
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)

    def OnBegin_shot_btn(self, btn, touch):
        self.is_trying_fire = True
        if self.panel.aim_one_shot_button_1 == btn:
            anim = 'shot_1' if 1 else 'shot_2'
            w, h = btn.GetContentSize()
            pos = btn.convertToWorldSpace(cc.Vec2(w / 2, h / 2))
            self.play_touch_effect(anim, 'fire_click', self.panel.convertToNodeSpace(pos), 1)
            if self.player:
                self.player.send_event('E_IS_KEEP_DOWN_FIRE', True)
                main_sel, sub_sel = self.cur_left_fire_sel
                if sub_sel == uoc.LF_SHOT_AND_MOVE:
                    self._is_move_rocker = True
                self.is_rocker_enable = True
                if self.player:
                    self.player.send_event('E_TRY_CANCEL_RUN_LOCK')
                cur_weapon_pos = self.player.share_data.ref_wp_bar_cur_pos
                if cur_weapon_pos in MAIN_WEAPON_LIST:
                    is_suc = self._start_touch_auto_fire()
                    is_suc or self.panel.DelayCallWithTag(0.05, self._cc_check_can_trigger_act, self.ACT_CHECK_TAG)
        btn.SetSelect(True)
        return True

    def _cc_check_can_trigger_act(self):
        if not self._check_can_trigger_act():
            return 0.05
        return 0

    def check_start_shot(self):
        is_suc = self._check_can_trigger_act()
        if not is_suc:
            self.panel.DelayCallWithTag(0.05, self._cc_check_can_trigger_act, self.ACT_CHECK_TAG)

    def _check_can_trigger_act(self):
        if not self.check_can_shot():
            return False
        return self.try_start_shot()

    def check_can_shot(self):
        from logic.comsys.battle.BattleUtils import can_fire
        if not can_fire():
            return False
        return self._camera_can_shot()

    def _camera_can_shot(self):
        return not ShotChecker().check_camera_can_shot()

    def _start_touch_auto_fire(self):
        is_suc = self._check_can_trigger_act()
        if not is_suc:
            return False
        else:
            return True

    def try_start_shot(self):
        if self.player:
            cur_weapon_pos = self.player.share_data.ref_wp_bar_cur_pos
            if cur_weapon_pos in MAIN_WEAPON_LIST:
                if self.player.ev_g_status_check_pass(ST_SHOOT) and self.player.ev_g_is_can_fire():
                    self.player.send_event('E_START_AUTO_FIRE')
                    self.is_start_fire = True
                    return True
        return False

    def OnEnd_shot_btn(self, btn, touch):
        self.is_trying_fire = False
        if self.player:
            self.player.send_event('E_IS_KEEP_DOWN_FIRE', False)
        btn.SetSelect(False)
        self.stop_rocker()

    def stop_rocker(self):
        if self.is_rocker_enable:
            self.panel.stopActionByTag(self.ACT_CHECK_TAG)
            self.is_rocker_enable = False
            if self.player:
                if self.is_start_fire:
                    self.player.send_event('E_STOP_AUTO_FIRE')
                    self._is_move_rocker = False
                    self.is_start_fire = False
            if self.is_last_moved:
                self.is_last_moved = False
                self._is_move_rocker = False
                if self.player:
                    self.player.send_event('E_ROCK_STOP')
                self.panel.aim_one_shot_button_2.setPosition(self.shot_btn_old_pos)
            if self.player:
                self.player.send_event('E_RELEASE_FIRE_ROCK')

    def OnDrag_shot_btn(self, btn, touch):
        import math3d
        if not self.player:
            return
        if not self.is_rocker_enable:
            return
        if not self._is_move_rocker:
            return
        pt = touch.getLocation()
        touch_begin_pos = touch.getStartLocation()
        self.set_rocker_center_pos(pt, self.move_bar_center_pos, self.panel.aim_one_shot_button_2, self.move_spawn_radius)
        delta_vec = ccp(pt.x - touch_begin_pos.x, pt.y - touch_begin_pos.y)
        if delta_vec.length() > 0:
            delta_vec.normalize()
            move_dir = math3d.vector(delta_vec.x, 0, delta_vec.y)
            if self.player:
                is_can_walk = self.player.ev_g_status_check_pass(ST_MOVE)
                if is_can_walk:
                    self.player.send_event('E_MOVE', move_dir)
                    self.player.send_event('E_MOVE_ROCK', move_dir, False)
                    self.is_last_moved = True

    def set_rocker_center_pos(self, move_pos, center_pos, move_node, radius):
        import math3d
        move_vec = math3d.vector2(move_pos.x - center_pos.x, move_pos.y - center_pos.y)
        move_vec_length = move_vec.length
        if move_vec_length > radius:
            move_vec = move_vec * (radius / move_vec_length)
        spawn_pt = move_node.getParent().convertToNodeSpace(ccp(center_pos.x + move_vec.x, center_pos.y + move_vec.y))
        move_node.SetPosition(spawn_pt.x, spawn_pt.y)

    def on_camera_switch_to_state(self, state, *args):
        self.cur_camera_state = state
        self.check_left_fire_ope()

    def bind_lf_ui_event(self, target):
        if target:
            target.regist_event('E_START_BOMB_ROCKER', self.on_start_bomb_rocker)
            target.regist_event('E_END_BOMB_ROCKER', self.on_end_bomb_rocker)
            target.regist_event('E_WPBAR_SWITCH_CUR', self.on_weapon_in_hand_changed)
            target.regist_event('E_FINISH_SWITCH_GUN', self.on_weapon_in_hand_changed)

    def unbind_lf_ui_event(self, target):
        if target and target.is_valid():
            target.unregist_event('E_START_BOMB_ROCKER', self.on_start_bomb_rocker)
            target.unregist_event('E_END_BOMB_ROCKER', self.on_end_bomb_rocker)
            target.unregist_event('E_WPBAR_SWITCH_CUR', self.on_weapon_in_hand_changed)
            target.unregist_event('E_FINISH_SWITCH_GUN', self.on_weapon_in_hand_changed)

    def on_start_bomb_rocker(self):
        self.hide_aim_one_shot_button()

    def hide_aim_one_shot_button(self):
        self.stop_rocker()
        self.panel.aim_one_shot_button_1.SetEnableTouch(False)
        self.panel.aim_one_shot_button_1.SetEnableTouch(True)
        self.panel.aim_one_shot_button_2.SetEnableTouch(False)
        self.panel.aim_one_shot_button_2.SetEnableTouch(True)
        self.panel.left.setVisible(False)

    def show_aim_one_shot_button(self):
        self.panel.left.setVisible(True)

    def on_end_bomb_rocker(self):
        self.check_left_fire_ope()

    def on_weapon_in_hand_changed(self, _):
        if not self.player:
            return
        cur_weapon_pos = self.player.share_data.ref_wp_bar_cur_pos
        self.check_left_fire_ope()

    def init_left_fire_opt_select(self):
        if not self.player:
            return
        else:
            self.cur_left_fire_sel = None
            global_data.emgr.left_fire_ope_change_event += self.on_switch_left_fire_ope
            self.on_switch_left_fire_ope(self.player.get_owner().get_setting(uoc.LF_OPE_KEY))
            return

    def on_switch_left_fire_ope(self, setting):
        self.cur_left_fire_sel = list(setting)
        self.check_left_fire_ope()
        self.custom_ui_com.refresh_all_custom_ui_conf()

    def check_left_fire_ope(self):
        if not self.player:
            return
        from logic.gcommon import const
        cur_weapon_pos = self.player.share_data.ref_wp_bar_cur_pos
        if cur_weapon_pos in [const.PART_WEAPON_POS_BOMB, const.PART_WEAPON_POS_COLD, const.PART_WEAPON_POS_NONE]:
            self.hide_aim_one_shot_button()
            return
        from logic.client.const.camera_const import AIM_MODE
        main_sel, sub_sel = self.cur_left_fire_sel
        if main_sel == uoc.LEFT_FIRE_ALWAYS_OPEN:
            self.show_aim_one_shot_button()
        elif main_sel == uoc.LEFT_FIRE_SHOW_WHEN_AIM:
            if self.cur_camera_state == AIM_MODE:
                self.show_aim_one_shot_button()
            else:
                self.hide_aim_one_shot_button()
        else:
            self.hide_aim_one_shot_button()
        if sub_sel == uoc.LF_ONLY_SHOT:
            self.aim_one_shot_button_1.setVisible(True)
            self.aim_one_shot_button_2.setVisible(False)
        else:
            self.aim_one_shot_button_1.setVisible(False)
            self.aim_one_shot_button_2.setVisible(True)

    def on_change_ui_custom_data(self):
        self.move_bar_center_pos = self.panel.aim_one_shot_button_2.ConvertToWorldSpacePercentage(50, 50)
        self.shot_btn_old_pos = self.panel.aim_one_shot_button_2.getPosition()
        self.move_spawn_radius = self.move_spawn_radius = self.panel.shot_bar.getContentSize().width * self.panel.shot_bar.getScale() * 0.9 / 2.0 * self.panel.nd_rocker.getScale()
        self.update_special_scale()
        ui = global_data.ui_mgr.get_ui('GuideUI')
        if ui:
            param = self.change_ui_data()
            ui.on_change_ui_inform_guide(*param)

    def change_ui_data(self):
        if self.panel.aim_one_shot_button_1.isVisible():
            nd = self.panel.aim_one_shot_button_1
        else:
            nd = self.panel.aim_one_shot_button_2
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        return (
         w_pos, None, 'nd_step_8')

    def restart_fire(self):
        if self.is_trying_fire:
            if self.panel.aim_one_shot_button_1.GetSelect():
                self.OnEnd_shot_btn(self.panel.aim_one_shot_button_1, None)
                self.OnBegin_shot_btn(self.panel.aim_one_shot_button_1, None)
            else:
                self.OnEnd_shot_btn(self.panel.aim_one_shot_button_2, None)
                self.OnBegin_shot_btn(self.panel.aim_one_shot_button_2, None)
        return

    def do_hide_panel(self):
        super(FightLeftShotUI, self).do_hide_panel()
        if self.panel.aim_one_shot_button_1.GetSelect():
            self.OnEnd_shot_btn(self.panel.aim_one_shot_button_1, None)
        else:
            self.OnEnd_shot_btn(self.panel.aim_one_shot_button_2, None)
        return