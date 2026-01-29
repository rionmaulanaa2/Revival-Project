# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/AimRockerUI.py
from __future__ import absolute_import
import math3d
import world
from .ShotChecker import ShotChecker
from common.cfg import confmgr
from common.utils.ui_utils import get_scale
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.client.const import camera_const
from logic.gutils import rocker_utils
from logic.gutils.weapon_utils import is_in_fast_aim_and_fire_mode
from logic.gcommon.common_const import ui_operation_const
from logic.gcommon.common_const import weapon_const
from logic.gcommon.const import AIM_NORMAL_PATH, AIM_SELECT_PATH, RIGHT_AIM_NORMAL_PATH, RIGHT_AIM_SELECT_PATH

class AimRockerUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/aim_rocker'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'aim_button.OnBegin': 'on_aim_btn_begin',
       'aim_button.OnDrag': 'on_aim_btn_drag',
       'aim_button.OnEnd': 'on_aim_btn_end',
       'change_button.OnBegin': '_on_click_change_mode_btn'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'switch_gun_mode': {'node': 'temp_pc'}}

    def on_init_panel(self):
        self.panel.setLocalZOrder(ui_operation_const.FIRE_LOCAL_ZORDER)
        self.last_aim_move_vec = None
        self.init_custom_com()
        self.is_on_aim_when_begin_touch = False
        self.cur_aim_lens = None
        self.sst_setting_map = {}
        self.aim_spawn_radius = self.panel.aim_bar.ConvertToWorldSpacePercentage(100, 50).x - self.panel.aim_bar.ConvertToWorldSpacePercentage(50, 50).x
        self.panel.aim_center_btn.EnableCustomState(True)
        self.init_event()
        self.init_parameters()
        self.process_event(True)
        return

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_parameters(self):
        self.init_weapon_rocker_draggable()
        self.init_aim_rocker_draggable()
        self.init_aim_btn_trigger_way()
        scn = world.get_active_scene()
        player = scn.get_player()
        if player:
            self.on_player_setted(player)
        global_data.emgr.scene_player_setted_event += self.on_player_setted

    def init_rocker_sensitivity(self):
        player = global_data.player
        uoc = ui_operation_const
        sst_ket_list = [uoc.SST_AIM_RD_KEY, uoc.SST_AIM_2M_KEY, uoc.SST_AIM_4M_KEY, uoc.SST_AIM_6M_KEY, uoc.SST_MECHA_07_KEY]
        for key in sst_ket_list:
            self.sst_setting_map[key] = list(player.get_setting(key))

    def process_event(self, is_bind=True):
        emgr = global_data.emgr
        econf = {'sst_common_changed_event': self.on_sst_common_changed,
           'camera_switch_to_state_event': self.on_camera_switch_to_state,
           'main_setting_ui_open_event': self.on_main_setting_ui_open,
           'on_wpbar_switch_cur_event': self.on_weapon_in_hand_changed,
           'weapon_equip_attachment_event': self.on_attachment_changed,
           'weapon_take_off_attachment_event': self.on_attachment_changed,
           'on_leave_state_event': self.on_leave_state,
           'on_weapon_mode_switched': self._on_weapon_mode_switched,
           'weapon_aim_rocker_draggable_changed': self._on_weapon_aim_rocker_draggable_changed,
           'weapon_aim_btn_trigger_changed': self._on_weapon_aim_btn_trigger_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _switch_to_aim_camera(self, *args):
        self.panel.aim_center_btn.SetSelect(True)
        lLenPics = confmgr.get('firearm_component', str(self.cur_aim_lens), 'lLenPics', default=[AIM_NORMAL_PATH, AIM_SELECT_PATH])
        self.panel.icon_aim.SetDisplayFrameByPath('', lLenPics[1])

    def _switch_to_aim_untouch_state(self, *args):
        self.panel.aim_center_btn.SetSelect(False)
        lLenPics = confmgr.get('firearm_component', str(self.cur_aim_lens), 'lLenPics', default=[AIM_NORMAL_PATH, AIM_SELECT_PATH])
        self.panel.icon_aim.SetDisplayFrameByPath('', lLenPics[0])

    def _switch_to_right_aim_camera(self, *args):
        self.panel.aim_center_btn.SetSelect(True)
        self.panel.icon_aim.SetDisplayFrameByPath('', RIGHT_AIM_SELECT_PATH)

    def _switch_to_right_aim_untouch_state(self, *args):
        self.panel.aim_center_btn.SetSelect(False)
        self.panel.icon_aim.SetDisplayFrameByPath('', RIGHT_AIM_NORMAL_PATH)

    def on_player_setted(self, player):
        if player:
            self.init_rocker_sensitivity()
            self.on_weapon_in_hand_changed()

    def init_event(self):
        partcam = global_data.game_mgr.scene.get_com('PartCamera')
        if partcam:
            self.on_camera_switch_to_state(partcam.get_cur_camera_state_type())
        else:
            self.on_camera_switch_to_state(camera_const.THIRD_PERSON_MODEL)

    def on_weapon_in_hand_changed(self, *args):
        if not (global_data.player and global_data.player.logic):
            return
        self._update_aim_ui()
        self._update_change_mode_ui()

    def on_attachment_changed(self, *args):
        if not (global_data.player and global_data.player.logic):
            return
        lplayer = global_data.player.logic
        self.cur_aim_lens = lplayer.ev_g_aim_lens_type()
        self.update_aim_ui_show(self.cur_camera_state_type)

    def on_leave_state(self, leave_state, new_st=None):
        pass

    def _on_bomb_thrown(self, *args):
        self.on_weapon_in_hand_changed(None)
        return

    def _update_aim_ui(self, *args):
        if not (global_data.player and global_data.player.logic):
            return
        else:
            lplayer = global_data.player.logic
            from logic.gutils.item_utils import check_can_right_aim
            if global_data.is_pc_control_enable:
                self.panel.aim_layer.setVisible(False)
                return
            self.cur_aim_lens = lplayer.ev_g_aim_lens_type()
            if self.cur_aim_lens and not global_data.is_pc_mode:
                self.panel.aim_layer.setVisible(True)
            else:
                cur_weapon = lplayer.share_data.ref_wp_bar_cur_weapon
                item_id = None
                if cur_weapon:
                    item_id = cur_weapon.get_item_id()
                need_show = check_can_right_aim(item_id)
                if need_show and not global_data.is_pc_mode:
                    self.panel.aim_layer.setVisible(True)
                else:
                    self.panel.aim_layer.setVisible(False)
            self.update_aim_ui_show(self.cur_camera_state_type)
            return

    def on_finalize_panel(self):
        self.on_player_setted(None)
        global_data.emgr.scene_player_setted_event -= self.on_player_setted
        self.process_event(False)
        self.destroy_widget('custom_ui_com')
        return

    def on_camera_switch_to_state(self, state, *args):
        self.cur_camera_state_type = state
        if state == camera_const.AIM_MODE:
            if global_data.player and global_data.player.logic:
                self.cur_aim_lens = global_data.player.logic.ev_g_aim_lens_type()
        self.update_aim_ui_show(state)

    def update_aim_ui_show(self, state):
        if state == camera_const.AIM_MODE:
            self._switch_to_aim_camera()
        elif state == camera_const.RIGHT_AIM_MODE:
            self._switch_to_right_aim_camera()
        elif self.cur_aim_lens:
            self._switch_to_aim_untouch_state()
        else:
            self._switch_to_right_aim_untouch_state()

    def check_camera_can_shot(self, lplayer):
        return ShotChecker().check_camera_can_shot(lplayer)

    def on_sst_common_changed(self, sst_type, settings):
        self.sst_setting_map[sst_type] = settings

    def on_aim_btn_begin(self, btn, touch):
        efx_pos = self.panel.convertToNodeSpace(self.panel.aim_layer.getParent().convertToWorldSpace(self.panel.aim_layer.getPosition()))
        self.play_touch_effect(global_data.is_key_mocking_ui_event or 'aim_click' if 1 else None, 'click', efx_pos, self.panel.aim_layer.getScale())
        if not (global_data.player and global_data.player.logic):
            return
        else:
            if self.cur_camera_state_type != camera_const.AIM_MODE:
                if self.check_camera_can_shot(global_data.player.logic):
                    return False
            lplayer = global_data.player.logic
            is_on_aim_when_begin_touch = lplayer.sd.ref_in_aim or lplayer.ev_g_in_right_aim()
            self.is_on_aim_when_begin_touch = is_on_aim_when_begin_touch
            return self.start_aim_rocker(btn, touch)

    def start_aim_rocker(self, btn, touch):
        if not (global_data.player and global_data.player.logic):
            return False
        player = global_data.player.logic
        if player.ev_g_aim_lens_type():
            from logic.comsys.battle.BattleUtils import can_lens_aim
            if not can_lens_aim():
                return False
            if not player.sd.ref_in_aim and player.ev_g_status_check_pass('ST_AIM'):
                if global_data.is_allow_sideways:
                    player.send_event('E_TOUCH_AIM_ROCKER')
                else:
                    player.send_event('E_TRY_AIM')
            elif player.sd.ref_in_aim:
                self.on_aim_btn_end(btn, touch)
                return True
        elif not player.ev_g_in_right_aim() and player.ev_g_status_check_pass('ST_RIGHT_AIM'):
            if global_data.is_allow_sideways:
                player.send_event('E_TOUCH_RIGHT_AIM_ROCKER')
            else:
                player.send_event('E_TRY_RIGHT_AIM')
        elif player.ev_g_in_right_aim():
            self.on_aim_btn_end(btn, touch)
            return True
        self.panel.aim_bar.setVisible(True)
        return True

    def on_aim_btn_drag(self, btn, touch):
        if not (global_data.player and global_data.player.logic):
            return
        else:
            if not self._weapon_rocker_draggable:
                return
            player = global_data.player.logic
            if not self._aim_rocker_draggable:
                return
            move_info = self.get_touch_info(touch)
            delta_vec = move_info.get('vec')
            vec_temp = math3d.vector2(delta_vec.x, delta_vec.y)
            if vec_temp.length > 0:
                self.last_aim_move_vec = vec_temp
            elif self.last_aim_move_vec:
                if not self.last_aim_move_vec.is_zero:
                    vec_temp = self.last_aim_move_vec
                    vec_temp.normalize()
                    self.last_aim_move_vec = math3d.vector2(0, 0)
            else:
                return
            pt = move_info.get('pos')
            center_pos = self.panel.aim_bar.ConvertToWorldSpacePercentage(50, 50)
            if player:
                scene = world.get_active_scene()
                ctrl = scene.get_com('PartCtrl')
                if ctrl.is_touching_scene():
                    return
                x_delta = vec_temp.x
                y_delta = vec_temp.y
                if player.sd.ref_in_aim:
                    x_delta, y_delta = self.modify_aim_rotate_dist_by_sensitivity(x_delta, y_delta, pt, center_pos)
                    ctrl.on_touch_slide(x_delta, y_delta, None, pt, False)
                else:
                    ctrl.on_touch_slide(x_delta, y_delta, None, pt, True)
            return

    def on_aim_btn_end(self, btn, touch):
        if not (global_data.player and global_data.player.logic):
            return
        player = global_data.player.logic
        is_click_only = btn.GetMovedDistance() <= get_scale('5w')
        self.panel.aim_bar.setVisible(False)
        aim_btn_press_trigger = self._aim_btn_press_trigger and player.sd.ref_in_aim
        if is_click_only or aim_btn_press_trigger:
            if self.is_on_aim_when_begin_touch or aim_btn_press_trigger:
                if player:
                    if player.sd.ref_in_aim:
                        if global_data.is_allow_sideways:
                            player.send_event('E_RELEASE_AIM_ROCKER')
                        else:
                            player.send_event('E_QUIT_AIM')
                    elif player.ev_g_in_right_aim():
                        if global_data.is_allow_sideways:
                            player.send_event('E_RELEASE_RIGHT_AIM_ROCKER')
                        else:
                            player.send_event('E_QUIT_RIGHT_AIM')
        self.panel.aim_button.SetPosition('50%', '50%')

    def get_touch_info(self, touch):
        touch_info = {'pos': touch.getLocation(),
           'id': touch.getId(),
           'vec': touch.getDelta()
           }
        return touch_info

    def modify_aim_rotate_dist_by_sensitivity(self, x_delta, y_delta, pos, rocker_center):
        if self.cur_aim_lens is None:
            log_error('There is not lens when get aim rocker move!')
            return (
             x_delta, y_delta)
        else:
            if self.cur_aim_lens not in weapon_const.aim_type_dict:
                log_error('Unsupport lens!')
            setting_key = weapon_const.aim_type_dict.get(self.cur_aim_lens, ui_operation_const.SST_AIM_RD_KEY)
            settings = self.sst_setting_map[setting_key]
            x_scale = settings[ui_operation_const.SST_IDX_RIGHT] if pos.x >= rocker_center.x else settings[ui_operation_const.SST_IDX_LEFT]
            x_delta *= settings[ui_operation_const.SST_IDX_BASE] * x_scale
            y_scale = settings[ui_operation_const.SST_IDX_UP] if pos.y >= rocker_center.y else settings[ui_operation_const.SST_IDX_DOWN]
            y_delta *= settings[ui_operation_const.SST_IDX_BASE] * y_scale
            return (
             x_delta, y_delta)

    def on_change_ui_custom_data(self):
        self.aim_spawn_radius = self.panel.aim_bar.ConvertToWorldSpacePercentage(100, 50).x - self.panel.aim_bar.ConvertToWorldSpacePercentage(50, 50).x

    def change_ui_data(self):
        nd = getattr(self.panel, 'aim_button')
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        return (
         w_pos, None, 'nd_step_7')

    def change_ui_data_three(self):
        nd = self.panel.nd_custom.change_layer
        scale = nd.getScale()
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        return (
         w_pos, scale, 'nd_change_mode')

    def on_main_setting_ui_open(self):
        if not (global_data.player and global_data.player.logic):
            return
        player = global_data.player.logic
        if player.ev_g_in_right_aim():
            if global_data.is_allow_sideways:
                player.send_event('E_RELEASE_RIGHT_AIM_ROCKER')
            else:
                player.send_event('E_QUIT_RIGHT_AIM')

    def _on_click_change_mode_btn(self, *args):
        self.panel.PlayAnimation('aim_click')
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_SWITCH_WEAPON_MODE')

    def _update_change_mode_ui(self):
        if global_data.is_pc_mode:
            return
        cur_weapon = global_data.player.logic.share_data.ref_wp_bar_cur_weapon
        if cur_weapon and cur_weapon.is_multi_wp():
            self.panel.change_layer.setVisible(True)
            self._update_mode_btn_pic(cur_weapon)
        else:
            self.panel.change_layer.setVisible(False)
            ui = global_data.ui_mgr.get_ui('GuideUI')
            if ui:
                ui.panel.nd_change_mode.setVisible(False)

    def _on_weapon_mode_switched(self, *args):
        cur_weapon = global_data.player.logic.share_data.ref_wp_bar_cur_weapon
        if cur_weapon and cur_weapon.is_multi_wp():
            self._update_mode_btn_pic(cur_weapon)

    def _update_mode_btn_pic(self, weapon):
        wp_id = weapon.get_item_id()
        mode_pic = confmgr.get('firearm_res_config', str(wp_id), 'cModeBtnPic')
        if mode_pic:
            self.panel.icon_change.SetDisplayFrameByPath('', mode_pic)

    def on_hot_key_opened_state(self):
        super(AimRockerUI, self).on_hot_key_opened_state()
        self._update_aim_ui()

    def on_hot_key_closed_state(self):
        super(AimRockerUI, self).on_hot_key_closed_state()
        self._update_aim_ui()

    def init_weapon_rocker_draggable(self):
        disable_drag = False
        self.set_weapon_rocker_draggable(not disable_drag)

    def set_weapon_rocker_draggable(self, val):
        if global_data.is_pc_mode:
            val = False
        self._weapon_rocker_draggable = val

    def on_weapon_rocker_draggable_change(self, val):
        self.set_weapon_rocker_draggable(not val)

    def init_aim_rocker_draggable(self):
        self._aim_rocker_draggable = global_data.player.get_setting_2(ui_operation_const.WEAPON_AIM_ROCKER_DRAG_ENABLE_KEY)

    def _on_weapon_aim_rocker_draggable_changed(self, val):
        self._aim_rocker_draggable = val

    def init_aim_btn_trigger_way(self):
        self._aim_btn_press_trigger = global_data.player.get_setting_2(ui_operation_const.WEAPON_AIM_PRESS_TRIGGER_KEY)

    def _on_weapon_aim_btn_trigger_changed(self, val):
        self._aim_btn_press_trigger = val

    def get_aim_button(self):
        if not self.panel.isValid():
            return None
        else:
            return self.panel.aim_button