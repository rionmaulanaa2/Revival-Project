# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/FightSightUI.py
from __future__ import absolute_import
import world
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.utils.ui_utils import get_scale
from logic.client.const import camera_const
from logic.gcommon.cdata import status_config as st_const
from logic.gutils import rocker_utils
from data import hot_key_def
import game
from logic.client.const import pc_const
from logic.gutils import pc_utils
BTN_TOOL_BAR = [
 'gui/ui_res_2/battle/button/human_btn_tools_nml.png',
 'gui/ui_res_2/battle/button/human_btn_tools_sel.png',
 'gui/ui_res_2/battle/button/human_btn_tools_nml.png']
MECHA_BYN_TOOL_BAR = ['gui/ui_res_2/battle/button/mech_btn_tools_nml.png',
 'gui/ui_res_2/battle/button/mech_btn_tools_sel.png',
 'gui/ui_res_2/battle/button/mech_btn_tools_nml.png']
SIGHT_BAR = ['gui/ui_res_2/battle/button/human_btn_tools_bar.png', 'gui/ui_res_2/battle/button/mech_btn_tools_nml.png']
from common.const import uiconst

class FightSightUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_sight'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    TRIGGER_ROCKER_DIST = get_scale('5w')
    UI_ACTION_EVENT = {'press_bar.OnBegin': 'OnBegin_sight_btn',
       'press_bar.OnDrag': 'on_drag_sight_btn',
       'press_bar.OnEnd': 'on_end_sight_btn'
       }
    IS_PLAY_OPEN_SOUND = False
    HOT_KEY_FUNC_MAP_SHOW = {'free_sight': {'node': 'temp_pc'}}
    HOT_KEY_FUNC_MAP = {'free_sight.DOWN_UP': 'keyboard_on_free_sight'
       }
    ENABLE_HOT_KEY_SUPPORT = True
    GLOBAL_EVENT = {'pc_hotkey_hint_display_option_changed': '_on_pc_hotkey_hint_display_option_changed',
       'pc_hotkey_hint_switch_toggled': '_on_pc_hotkey_hint_switch_toggled'
       }

    def on_init_panel(self):
        self.init_data()
        self.init_event()
        self.set_camera_state(camera_const.THIRD_PERSON_MODEL)
        self.init_custom_com()
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())
        if global_data.is_pc_mode:
            self.panel.nd_custom.setScale(0.8)
            self.panel.nd_sight.setVisible(False)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.player = None
        if self.custom_ui_com:
            self.custom_ui_com.destroy()
            self.custom_ui_com = None
        return

    def init_event(self):
        bg_map_ui = global_data.ui_mgr.get_ui('BigMapUI')
        if bg_map_ui:
            self.add_hide_count('BigMapUI')
            bg_map_ui._hide_name_list.append(self.__class__.__name__)
        global_data.emgr.camera_switch_to_state_event += self.set_camera_state
        global_data.emgr.sst_free_sight_changed_event += self.on_free_sight_sst_setting
        global_data.emgr.free_sight_ope_change_event += self.on_free_sight_ope_change
        global_data.emgr.show_weapon_scroll_ui_event += self.on_show_weapon_scroll
        global_data.emgr.switch_control_target_event += self.on_ctrl_target_changed
        global_data.emgr.enable_free_sight_from_logic += self.enable_free_sight_from_logic
        global_data.emgr.disable_free_sight_btn += self.disable_free_sight_btn
        import world
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        if player:
            self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted

    def on_hot_key_state_opened(self):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def on_hot_key_state_closed(self):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_display_option_changed(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), now, pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_switch_toggled(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(now, pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def _update_pc_key_hint_related_uis_visibility(self, hint_switch, display_option, pc_op_mode):
        pass

    def on_ctrl_target_changed(self, *args, **kargs):
        if not global_data.cam_lplayer:
            return
        else:
            index = 1 if global_data.cam_lplayer.ev_g_ctrl_mecha() else 0
            btn = [BTN_TOOL_BAR, MECHA_BYN_TOOL_BAR]
            self.panel.sight_bar.SetDisplayFrameByPath('', SIGHT_BAR[index])
            self.panel.sight_button.SetFrames('', btn[index], False, None)
            return

    def on_player_setted(self, player):
        self.unbind_ui_event(player)
        self.player = player
        self.free_sight_btn_locked = False
        self.free_sight_btn_disabled = False
        if player:
            self.bind_ui_event(self.player)

    def set_camera_state(self, state, *args):
        self.camera_state = state
        self.set_btn_state(state in [camera_const.FREE_MODEL, camera_const.OBSERVE_FREE_MODE])
        self.panel.nd_sight.setVisible(state not in [camera_const.AIM_MODE, camera_const.RIGHT_AIM_MODE, camera_const.FREE_DROP_MODE])
        if state not in [camera_const.FREE_MODEL, camera_const.OBSERVE_FREE_MODE]:
            self.on_stop_rocker_show()
            self.is_rocker_enable = False
            self.free_sight_btn_locked = False
        if global_data.is_pc_mode:
            if self.panel and self.panel.nd_sight:
                self.panel.nd_sight.setVisible(False)

    def set_btn_state(self, cond):
        if cond:
            self.panel.sight_button.SetSelect(True)
            if not self.is_rocker_enable:
                self.panel.label_state.setVisible(True)
        else:
            self.panel.sight_button.SetSelect(False)
            self.panel.label_state.setVisible(False)
        if global_data.is_pc_mode:
            if self.panel and self.panel.nd_sight:
                self.panel.nd_sight.setVisible(False)

    def enable_free_sight_from_logic(self, flag):
        if flag == self.free_sight_btn_locked:
            return
        else:
            if flag:
                self.OnBegin_sight_btn(None, None)
                if not self.is_rocker_enable:
                    self.start_sight_rocker()
                self.free_sight_btn_locked = True
            else:
                self.free_sight_btn_locked = False
                self.on_end_sight_btn(None, None)
            return

    def disable_free_sight_btn(self, disable):
        self.free_sight_btn_disabled = disable

    def init_data(self):
        self.drag_scale = 1.0
        self.camera_state = camera_const.THIRD_PERSON_MODEL
        self.player = None
        self.set_camera_enable_for_follow = False
        self.free_sight_btn_locked = False
        self.free_sight_btn_disabled = False
        self.init_rocker_parameters()
        return

    def on_click_sight(self, *args):
        if self.camera_state == camera_const.FREE_MODEL:
            if global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_FREE_CAMERA_STATE', False)
        elif self.camera_state == camera_const.OBSERVE_FREE_MODE:
            if global_data.cam_lplayer and global_data.cam_lplayer.id != global_data.player.id:
                global_data.emgr.camera_leave_free_observe_event.emit()
        elif global_data.cam_lplayer and global_data.cam_lplayer.id != global_data.player.id:
            global_data.emgr.camera_enter_free_observe_event.emit()
        elif self.is_free_camera_available() or self.free_sight_btn_disabled:
            global_data.player.logic.send_event('E_FREE_CAMERA_STATE', True)

    def is_free_camera_available(self):
        if not global_data.player or not global_data.player.logic:
            return False
        else:
            player = global_data.player.logic
            control_target = player.ev_g_control_target()
            if not control_target or not control_target.logic:
                return False
            res = control_target.logic.ev_g_is_can_free_camera()
            if res is not None:
                return res
            return True

    def bind_ui_event(self, target):
        target.regist_event('E_START_BOMB_ROCKER', self.on_start_bomb_rocker)
        target.regist_event('E_END_BOMB_ROCKER', self.on_end_bomb_rocker)
        target.regist_event('E_ENTER_STATE', self.on_enter_state)
        target.regist_event('E_LEAVE_STATE', self.on_leave_state)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            target.unregist_event('E_START_BOMB_ROCKER', self.on_start_bomb_rocker)
            target.unregist_event('E_END_BOMB_ROCKER', self.on_end_bomb_rocker)
            target.unregist_event('E_ENTER_STATE', self.on_enter_state)
            target.unregist_event('E_LEAVE_STATE', self.on_leave_state)

    def on_start_bomb_rocker(self):
        self.add_hide_count('BOMB_ROCKER')

    def on_end_bomb_rocker(self):
        self.add_show_count('BOMB_ROCKER')

    def on_enter_state(self, sid):
        if sid == st_const.ST_PARACHUTE:
            self.drag_scale = 1.5

    def on_leave_state(self, sid, *args):
        if sid == st_const.ST_PARACHUTE:
            self.drag_scale = 1.0

    def init_rocker_parameters(self):
        self.init_player_sst_setting()
        self.init_player_fs_ope_setting()
        self.sight_bar_center_pos = self.panel.sight_bar.ConvertToWorldSpacePercentage(50, 50)
        self.sight_btn_old_pos = self.panel.sight_button.getPosition()
        self.sight_spawn_radius = self.panel.sight_bar.getContentSize().width * self.panel.sight_bar.getScale() * 0.9 / 2.0
        self.is_rocker_enable = False
        self.is_need_slerp = False

    def OnBegin_sight_btn(self, btn, touch):
        if self.free_sight_btn_locked:
            return False
        else:
            if not (global_data.player and global_data.player.logic):
                return False
            if self.free_sight_btn_disabled:
                return False
            if not self.is_free_camera_available():
                global_data.emgr.battle_show_message_event.emit(get_text_local_content(18133))
                return False
            if global_data.player.logic.ev_g_parachute_follow_target() is not None:
                global_data.emgr.enable_camera_yaw.emit(True)
                self.set_camera_enable_for_follow = True
            else:
                self.set_camera_enable_for_follow = False
            self.panel.sight_button.SetSelect(True)
            return True

    def on_end_sight_btn(self, btn, touch):
        if self.free_sight_btn_locked:
            return
        else:
            if global_data.player and global_data.player.logic:
                if global_data.player.logic.ev_g_parachute_follow_target() is not None and not global_data.battle.is_in_island():
                    global_data.emgr.enable_camera_yaw.emit(False)
                elif self.set_camera_enable_for_follow:
                    global_data.emgr.enable_camera_yaw.emit(True)
                self.set_camera_enable_for_follow = False
            self.stop_rocker()
            if self.camera_state not in [camera_const.FREE_MODEL, camera_const.OBSERVE_FREE_MODE]:
                self.set_btn_state(False)
            return

    def stop_rocker(self):
        if self.player:
            if self.is_rocker_enable:
                self.on_stop_rocker_show()
                self.is_rocker_enable = False
                if self.camera_state in [camera_const.FREE_MODEL, camera_const.OBSERVE_FREE_MODE]:
                    self.on_click_sight()
            else:
                from logic.gcommon.common_const import ui_operation_const as uoc
                if self.free_sight_ope_sel != uoc.FS_ONLY_ROCKER and not global_data.is_pc_mode:
                    self.on_click_sight()
                elif self.camera_state == [camera_const.FREE_MODEL, camera_const.OBSERVE_FREE_MODE]:
                    self.on_click_sight()

    def on_stop_rocker_show(self):
        import cc
        self.panel.press_bar.SetEnableTouch(False)
        self.panel.press_bar.SetEnableTouch(True)
        if not self.is_rocker_enable:
            return
        move_act = cc.MoveTo.create(0.1, self.sight_btn_old_pos)

        def _cc_hide_helper():
            self.panel.sight_bar.setVisible(False)

        hide_act = cc.CallFunc.create(_cc_hide_helper)
        self.panel.sight_button.stopAllActions()
        self.panel.sight_button.runAction(cc.Sequence.create([move_act, hide_act]))

    def on_drag_sight_btn(self, btn, touch):
        if not self.player:
            return
        else:
            pt = touch.getLocation()
            if not self.is_rocker_enable:
                if abs(btn.GetMovedDistance()) > FightSightUI.TRIGGER_ROCKER_DIST:
                    self.start_sight_rocker()
                    return
                else:
                    return

            if self.is_rocker_enable:
                rocker_utils.set_rocker_center_pos(pt, self.sight_bar_center_pos, self.panel.sight_button, self.sight_spawn_radius)
                move_delta = touch.getDelta()
                if self.player:
                    scene = world.get_active_scene()
                    ctrl = scene.get_com('PartCtrl')
                    old_x_delta = move_delta.x * self.drag_scale
                    old_y_delta = move_delta.y * self.drag_scale
                    x_delta, y_delta = rocker_utils.modify_rotate_dist_by_sensitivity(self.sst_fr_setting, old_x_delta, old_y_delta, pt, self.sight_bar_center_pos)
                    ctrl.on_touch_slide(x_delta, y_delta, None, pt, False, need_check_speed=False)
            return

    def start_sight_rocker(self):

        def close_slerp():
            self.is_need_slerp = False

        self.panel.sight_button.stopAllActions()
        self.panel.sight_bar.setVisible(True)
        self.panel.label_state.setVisible(False)
        self.is_need_slerp = True
        self.is_rocker_enable = True
        self.panel.nd_sight.stopAllActions()
        self.panel.nd_sight.SetTimeOut(0.3, close_slerp)
        if self.camera_state not in [camera_const.FREE_MODEL, camera_const.OBSERVE_FREE_MODE]:
            self.on_click_sight()

    def init_player_sst_setting(self):
        from logic.gcommon.common_const import ui_operation_const as uoc
        self.sst_fr_setting = list(global_data.player.get_setting(uoc.SST_FS_ROCKER_KEY))

    def on_free_sight_sst_setting(self, val):
        self.sst_fr_setting = list(val)

    def init_player_fs_ope_setting(self):
        from logic.gcommon.common_const import ui_operation_const as uoc
        self.free_sight_ope_sel = global_data.player.get_setting(uoc.FREE_SIGHT_KEY)

    def on_free_sight_ope_change(self, val):
        self.free_sight_ope_sel = val

    def on_change_ui_custom_data(self):
        self.sight_bar_center_pos = self.panel.sight_bar.ConvertToWorldSpacePercentage(50, 50)
        self.sight_btn_old_pos = self.panel.sight_button.getPosition()
        self.sight_spawn_radius = self.panel.sight_bar.getContentSize().width * self.panel.sight_bar.getScale() * 0.9 / 2.0

    def on_show_weapon_scroll(self, is_show):
        if is_show:
            self.add_hide_count('WEAPONSCROLL')
        else:
            self.add_show_count('WEAPONSCROLL')

    def keyboard_on_free_sight(self, msg, keycode):
        if not (global_data.player and global_data.player.logic):
            return
        else:
            if self.free_sight_btn_disabled:
                return
            stage = global_data.player.logic.share_data.ref_parachute_stage
            from logic.gcommon.common_utils import parachute_utils
            if parachute_utils.is_preparing(stage) or parachute_utils.is_sortie_stage(stage):
                return
            is_down = msg in [game.MSG_KEY_DOWN, game.MSG_MOUSE_DOWN]
            if is_down:
                if self.OnBegin_sight_btn(None, None):
                    if not self.is_rocker_enable:
                        self.start_sight_rocker()
            else:
                self.on_end_sight_btn(None, None)
            return