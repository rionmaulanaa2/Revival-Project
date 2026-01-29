# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/DriveUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import world
from common.const.uiconst import ROCKER_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.utils.cocos_utils import ccp
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gutils import rocker_utils
from logic.vscene.parts.ctrl.ShortcutFunctionalityMutex import try_claim_shortcut_functionality, try_unclaim_shortcut_functionality, is_all_shortcut_functionality_claimed, claim_shortcut_functionality, unclaim_shortcut_functionality, drive_movement_shortcut_names, DRIVE_MOVE_FOWARD, DRIVE_MOVE_BACKWARD, DRIVE_MOVE_LEFT, DRIVE_MOVE_RIGHT
from logic.gutils import hot_key_utils
from data import hot_key_def
import game
import logic.vscene.parts.ctrl.GamePyHook as game_hook
from common.const import uiconst
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock

class DriveUI(BasePanel):
    PANEL_CONFIG_NAME = 'drive/drive_main'
    DLG_ZORDER = ROCKER_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    MAX_SEAT_NUM = 4
    LOCK_IMG_PIC = 'gui/ui_res_2/battle/drive/bar_lock_sel.png'
    UNLOCK_IMG_PIC = 'gui/ui_res_2/battle/drive/bar_lock_nml.png'
    BTN_SPEED_NORMAL_PIC = 'gui/ui_res_2/battle/drive/btn_speed_nml.png'
    BTN_SPEED_SEL_PIC = 'gui/ui_res_2/battle/drive/btn_speed_sel.png'
    BTN_SPEED_LOCK_PIC = 'gui/ui_res_2/battle/drive/btn_speed_lock.png'
    BTN_FORWARD_NORMAL_PIC = 'gui/ui_res_2/battle/drive/btn_forward_nml.png'
    BTN_FORWARD_SEL_PIC = 'gui/ui_res_2/battle/drive/btn_forward_sel.png'
    BTN_FORWARD_LOCK_PIC = 'gui/ui_res_2/battle/drive/btn_forward_lock.png'
    DELAY_TURN_TAG = 180416
    ENABLE_HOT_KEY_SUPPORT = True
    UI_ACTION_EVENT = {'layer_drive.OnDrag': 'on_drag_drive_layer',
       'layer_drive.OnBegin': 'on_begin_drive_layer',
       'layer_drive.OnEnd': 'on_end_drive_layer',
       'btn_forward.OnBegin': 'on_begin_btn_forward',
       'btn_forward.OnEnd': 'on_end_btn_forward',
       'btn_forward.OnDrag': 'on_drag_btn_forward',
       'btn_back.OnBegin': 'on_begin_btn_back',
       'btn_back.OnEnd': 'on_end_btn_back',
       'layer_bottom.OnBegin': 'on_touch_bottom_begin',
       'layer_bottom.OnEnd': 'on_touch_bottom_end',
       'btn_left.OnBegin': 'on_begin_btn_left',
       'btn_left.OnEnd': 'on_end_btn_left',
       'btn_right.OnBegin': 'on_begin_btn_right',
       'btn_right.OnEnd': 'on_end_btn_right',
       'layer_speed_up.OnBegin': 'on_begin_speed_up',
       'layer_speed_up.OnEnd': 'on_end_speed_up'
       }
    ASSOCIATE_UI_LIST = [
     'FireRockerUI', 'PostureControlUI', 'ThrowRockerUI', 'FrontSightUI', 'FightLeftShotUI', 'BulletReloadUI', 'WeaponBarSelectUI']

    def on_init_panel(self):
        self.init_car_parameter()
        self.init_parameters()
        self.init_event()
        self.init_keyboard_control_parameters()
        if global_data.is_pc_mode:
            self.hide()

    def enter_screen(self):
        super(DriveUI, self).enter_screen()
        if global_data.is_pc_mode:
            self.hide()

    def init_event(self):
        self.set_associated_ui_visible(DriveUI.ASSOCIATE_UI_LIST, False)

    def on_finalize_panel(self):
        self.touch_mock_trigger = None
        self.on_set_car(None)
        self.on_player_setted(None)
        self.set_associated_ui_visible(DriveUI.ASSOCIATE_UI_LIST, True)
        self.set_associated_ui_visible(['MoveRockerUI'], True)
        for name in drive_movement_shortcut_names:
            try_unclaim_shortcut_functionality((name,), 'DriveUIOne')
            try_unclaim_shortcut_functionality((name,), 'DriveUITwo')
            try_unclaim_shortcut_functionality((name,), 'DriveUIKeyboard')

        return

    def init_parameters(self):
        self.player = None
        self.is_player_first_setted = False
        self.seat_ui_node = None
        self.vehicle_ui_node = None
        self.is_driver = False
        self._is_in_touch_bottom = False
        self._is_lock = False
        self.init_buttons_ope_parameters()
        self.cur_drive_ope_sel = global_data.player.get_setting_2(uoc.DRIVE_OPE_KEY)
        self._button_ope = global_data.player.get_setting_2(uoc.DRIVE_OPE_BUTTON_DIR_KEY)
        self.check_button_ope_position()
        self.touch_mock = TouchMock()
        self.touch_mock_trigger = None
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        if player:
            self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted
        econf = {'drive_ui_ope_change_event': self.on_switch_car_ope,
           'camera_switch_to_state_event': self.on_camera_switch_to_state,
           'on_item_data_changed_event': self.on_item_data_changed,
           'drive_ui_button_ope_change_event': self.on_button_ope_change,
           'show_chongci_ui': self.show_chongci_ui,
           'lock_drive_ui': self.lock_drive_ui,
           'get_is_lock': self.get_is_lock
           }
        emgr.bind_events(econf)
        return

    def on_player_setted(self, player):
        self.player = player
        if self.player:
            if not self.is_player_first_setted:
                self.is_player_first_setted = True
            cur_control_target = self.player.ev_g_control_target()
            self.on_switch_control_target(cur_control_target.id, None)
            self.on_camera_switch_to_state(global_data.game_mgr.scene.get_com('PartCamera').get_cur_camera_state_type())
        return

    def on_switch_control_target(self, target_id, _):
        from mobile.common.EntityManager import EntityManager
        from logic.gcommon.common_const import mecha_const
        target = EntityManager.getentity(target_id)
        if target and target.logic and target.logic.is_valid():
            if target.__class__.__name__ == 'MechaTrans':
                if target.logic.ev_g_pattern() == mecha_const.MECHA_PATTERN_VEHICLE:
                    self.show()
                    self.on_set_car(target)
            else:
                if self.panel:
                    self.hide()
                self.on_set_car(None)
        if global_data.is_pc_mode:
            self.hide()
        return

    def init_car_parameter(self):
        self.max_car_health = 100
        self.cur_car_health = 100
        self.cur_speed = 100
        self.max_speed = 100
        self.cur_gas = 10
        self.max_gas = 100
        self.cur_wheels_health_info = {}
        self.passenger_info = {}
        self.seat_list = []
        self.wheels_list = []
        self.cur_vehicle = None
        self.cur_emphasize_label = None
        self.min_ope_turn_offset = 0.2
        self.full_speed_ope_turn_time = 0.2
        self.vehicle_health_pic = ''
        self.vehicle_unhealth_pic = ''
        self.cur_gas_color = None
        return

    def on_set_car(self, vehicle):
        if self.cur_vehicle:
            self.process_bind_car_event(self.cur_vehicle.logic, is_bind=False)
        self.cur_vehicle = vehicle
        if vehicle and vehicle.logic:
            LOGIC_GET_VALUE = vehicle.logic.get_value
            all_v_info = LOGIC_GET_VALUE('G_VEHICLE_ALL_INFO')
            print('all_v_info', all_v_info)
            self.seat_list = LOGIC_GET_VALUE('G_VEHICLE_SEATS')
            vehicle_type = LOGIC_GET_VALUE('G_VEHICLE_TYPE')
            from common.cfg import confmgr
            self.max_turn_offset = confmgr.get('vehicle_data2', str(vehicle_type), 'max_steer', default=0)
            self.min_ope_turn_offset = confmgr.get('vehicle_data2', str(vehicle_type), 'min_ope_turn_angle', default=0.2)
            self.full_speed_ope_turn_time = confmgr.get('vehicle_data2', str(vehicle_type), 'full_speed_ope_turn_time', default=0.2)
            from data import vehicle_data
            vehicle_conf = vehicle_data.data.get(str(vehicle_type), {})
            vehicle_template = vehicle_conf.get('vehicleTemplate', 'drive/item_jeep')
            self.vehicle_health_pic = vehicle_conf.get('cUIHealthPic', '')
            self.vehicle_unhealth_pic = vehicle_conf.get('cUIUnhealthPic', '')
            passenger_info = all_v_info.get('passenger', {})
            cur_speed, max_speed = all_v_info.get('speed', [0, 100])
            self.cur_gas = LOGIC_GET_VALUE('G_VEHICLE_CUR_GAS')
            self.max_gas = LOGIC_GET_VALUE('G_VEHICLE_MAX_GAS')
            if self.panel:
                self.on_car_speed_changed([cur_speed, max_speed])
                self.on_car_passenger_changed(passenger_info, passenger_info, {})
                self.process_bind_car_event(vehicle.logic, True)

    def process_bind_car_event(self, lvehicle, is_bind=True):
        if lvehicle and lvehicle.is_valid():
            if is_bind:
                ope_func = lvehicle.regist_event
            else:
                ope_func = lvehicle.unregist_event
            ope_func('E_SPEED_CHANGED', self.on_car_speed_changed)
            ope_func('E_SWITCH_VEHICLE_SEAT', self.on_car_passenger_changed)

    def show_chongci_ui(self, is_chongci):
        if self.cur_drive_ope_sel == uoc.DRIVE_OPE_FORWARD:
            if is_chongci:
                self._on_first_layer_lock()
            else:
                self._on_first_layer_unlock()
        elif self.cur_drive_ope_sel == uoc.DRIVE_OPE_BUTTON:
            if is_chongci:
                self._on_second_layer_lock()
            else:
                self._on_second_layer_unlock()

    def lock_drive_ui(self):
        if self.cur_drive_ope_sel == uoc.DRIVE_OPE_FORWARD:
            self._on_first_layer_lock()
        elif self.cur_drive_ope_sel == uoc.DRIVE_OPE_BUTTON:
            self._on_second_layer_lock()
        else:
            ui = global_data.ui_mgr.get_ui('MoveRockerUI')
            ui.set_run_locker(True)
        if self.player:
            self.player.send_event('E_MOVE_FORWARD')

    def get_is_lock(self):
        if self.cur_drive_ope_sel in [uoc.DRIVE_OPE_FORWARD, uoc.DRIVE_OPE_BUTTON]:
            return self._is_lock
        else:
            ui = global_data.ui_mgr.get_ui('MoveRockerUI')
            if ui:
                return ui.get_is_run_lock()
            return False

    def on_car_speed_changed(self, speed_info):
        cur_speed, max_speed = speed_info
        self.cur_speed = round(abs(cur_speed), 1)

    def get_next_free_seat(self, cur_seat_name):
        occupy_seat_list = []
        for p_id, seat_name in six.iteritems(self.passenger_info):
            if not isinstance(seat_name, str):
                continue
            occupy_seat_list.append(seat_name)

        if len(occupy_seat_list) == len(self.seat_list):
            return None
        else:
            if cur_seat_name not in self.seat_list:
                return None
            index = self.seat_list.index(cur_seat_name)
            start_index = index
            seat_len = len(self.seat_list)
            for idx in range(seat_len):
                new_idx = (idx + start_index) % seat_len
                poss_seat_name = self.seat_list[new_idx]
                if poss_seat_name not in occupy_seat_list:
                    return poss_seat_name

            return None

    def on_set_up_vehicle_ui(self, vehicle_ui_template):
        if not self.vehicle_ui_node:
            ccb_vehicle = global_data.uisystem.load_template_create(vehicle_ui_template)
            self.panel.nd_vehicle_mount.GetParent().AddChild('nd_vehicle', ccb_vehicle)
            ccb_vehicle.setAnchorPoint(self.panel.nd_vehicle_mount.getAnchorPoint())
            ccb_vehicle.setPosition(self.panel.nd_vehicle_mount.getPosition())
            ccb_vehicle.setScale(self.panel.nd_vehicle_mount.getScale())
            self.vehicle_ui_node = ccb_vehicle

    def on_car_passenger_changed(self, passenger_info, old_passenger, driver_info):
        if self.cur_vehicle and self.cur_vehicle.logic:
            driver_id = self.cur_vehicle.logic.sd.ref_driver_id
            is_driver = driver_id == global_data.player.id
            self.on_check_driver_car(is_driver)
            if not is_driver:
                self.cancel_speed_lock()

    def set_associated_ui_visible(self, ui_list, is_show):
        for ui_name in ui_list:
            ui_inst = global_data.ui_mgr.get_ui(ui_name)
            if ui_inst:
                if is_show:
                    ui_inst.add_show_count('DriveUI')
                else:
                    ui_inst.add_hide_count('DriveUI')

    def on_drag_drive_layer(self, layer, touch):
        cur_wpos = touch.getLocation()
        cur_lpos = self.panel.btn_speed.getParent().convertToNodeSpace(cur_wpos)
        start_wpos = touch.getStartLocation()
        start_lpos = self.panel.btn_speed.getParent().convertToNodeSpace(start_wpos)
        y_delta = cur_lpos.y - start_lpos.y
        new_y = self.btn_start_pos.y + y_delta
        pos = self.panel.layer_valid.getPosition()
        sz = self.panel.layer_valid.getContentSize()
        max_y = pos.y + sz.height * 0.5
        min_y = pos.y - sz.height * 0.5
        new_y = min(max(new_y, min_y), max_y)
        self.panel.btn_speed.SetPosition(self.panel.btn_speed.getPosition().x, new_y)
        cur_btn_pos = self.panel.btn_speed.getParent().convertToWorldSpace(self.panel.btn_speed.getPosition())
        if self.panel.nd_speed_lock.IsPointIn(cur_btn_pos):
            self._move_acc_lock()
        elif self.panel.nd_normal.IsPointIn(cur_btn_pos):
            self._move_forward()
        elif self.panel.btn_speed_start.IsPointIn(cur_btn_pos):
            self._move_no_force()
        elif self.panel.back.IsPointIn(cur_btn_pos):
            self._move_back()
        else:
            self._move_no_force()

    def _move_acc_lock(self):
        if self.player:
            if self.player:
                self.player.send_event('E_MOVE_FORWARD')
                self.panel.img_lock_hint.SetDisplayFrameByPath('', self.LOCK_IMG_PIC)
                self.panel.img_lock_hint.setVisible(True)
                self.panel.txt_lock_hint.SetColor('#DB')
                self.panel.go_forward.setVisible(True)
                self.panel.go_backward.setVisible(False)

    def _move_forward(self):
        if self.player:
            self.player.send_event('E_MOVE_FORWARD')
            self.panel.txt_lock_hint.SetColor('#SD')
            self.panel.img_lock_hint.setVisible(True)
            self.panel.go_forward.setVisible(True)
            self.panel.go_backward.setVisible(False)
            self.panel.img_lock_hint.SetDisplayFrameByPath('', self.UNLOCK_IMG_PIC)

    def _move_back(self):
        if self.player:
            self.player.send_event('E_MOVE_BACK')
            self.panel.img_lock_hint.setVisible(False)
            self.panel.txt_lock_hint.SetColor('#SD')
            self.panel.go_forward.setVisible(False)
            self.panel.go_backward.setVisible(True)
            self.panel.img_lock_hint.SetDisplayFrameByPath('', self.UNLOCK_IMG_PIC)

    def _move_no_force(self):
        if self.player:
            self.player.send_event('E_MOVE_NO_FORCE')
            self.panel.img_lock_hint.setVisible(False)
            self.panel.txt_lock_hint.SetColor('#SD')
            self.panel.go_forward.setVisible(False)
            self.panel.go_backward.setVisible(False)
            self.panel.img_lock_hint.SetDisplayFrameByPath('', self.UNLOCK_IMG_PIC)

    @unclaim_shortcut_functionality(drive_movement_shortcut_names, 'DriveUIOne')
    def on_end_drive_layer(self, layer, touch):
        cur_lpos = self.panel.btn_speed.getPosition()
        cur_btn_pos = self.panel.btn_speed.getParent().convertToWorldSpace(cur_lpos)
        if self.panel.nd_speed_lock.IsPointIn(cur_btn_pos):
            self._move_acc_lock()
            self._on_first_layer_lock()
        else:
            self._move_no_force()
            self._on_first_layer_unlock()

    def _on_first_layer_lock(self):
        self._is_lock = True
        old_x, _ = self.panel.btn_speed.GetPosition()
        wpos = self.panel.img_speed_bar.ConvertToWorldSpacePercentage(0, 100)
        lpos = self.panel.btn_speed.getParent().convertToNodeSpace(wpos)
        self.panel.btn_speed.SetPosition(old_x, lpos.y - 17)
        self.panel.btn_speed.SetSelect(True)
        self.panel.img_lock_hint.setVisible(False)
        self.panel.speed_lock.setVisible(True)
        self.panel.btn_speed.SetFrames('', [self.BTN_SPEED_NORMAL_PIC, self.BTN_SPEED_LOCK_PIC, self.BTN_SPEED_NORMAL_PIC], False, None)
        return

    def _on_first_layer_unlock(self, exclude_btn_speed=False):
        self._is_lock = False
        if not exclude_btn_speed:
            old_pos = self.panel.btn_speed_start.getPosition()
            self.panel.btn_speed.setPosition(old_pos)
            self.panel.btn_speed.SetSelect(False)
        self.panel.img_lock_hint.setVisible(False)
        self.panel.speed_lock.setVisible(False)

    @claim_shortcut_functionality(drive_movement_shortcut_names, 'DriveUIOne')
    def on_begin_drive_layer(self, layer, touch, is_mock=False):
        from logic.gutils.move_utils import can_move
        if not can_move():
            return False
        else:
            self.panel.btn_speed.SetSelect(True)
            self.panel.speed_lock.setVisible(False)
            if not self.panel.btn_speed.IsPointIn(touch.getLocation()):
                self.panel.btn_speed.setPosition(self.panel.btn_speed_start.getPosition())
            self.btn_start_pos = self.panel.btn_speed.getPosition()
            self.panel.btn_speed.SetFrames('', [self.BTN_SPEED_NORMAL_PIC, self.BTN_SPEED_SEL_PIC, self.BTN_SPEED_NORMAL_PIC], False, None)
            if not is_mock:
                global_data.emgr.on_touch_drive_ui_event.emit(touch)
            return True

    def on_begin_brake_btn(self, btn, touch):
        if self.player:
            self.player.send_event('E_MOVE_BRAKE_START')
            self.cancel_speed_lock()
        return True

    def cancel_speed_lock(self):
        old_pos = self.panel.btn_speed_start.getPosition()
        self.panel.btn_speed.setPosition(old_pos)
        self.panel.speed_lock.setVisible(False)
        self.panel.img_lock_hint.setVisible(True)
        self.switch_speed_lock_state(False)
        self.panel.go_backward.setVisible(False)
        self.panel.go_forward.setVisible(False)

    def on_end_brake_btn(self, btn, touch):
        if self.player:
            self.player.send_event('E_MOVE_BRAKE_END')

    def on_click_get_off_btn(self, btn, touch):
        if self.player:
            self.player.send_event('E_TRY_LEAVE_VEHICLE')
        if self.player:
            self.player.send_event('E_TRY_LEAVE_MECHA')

    def on_switch_transform(self, btn, touch):
        if self.cur_vehicle and self.cur_vehicle.logic:
            self.cur_vehicle.logic.send_event('E_TRY_TRANSFORM')

    def on_begin_horn_btn(self, btn, touch):
        if self.player:
            self.player.send_event('E_VEHICLE_HORN')
        return True

    def on_end_horn_btn(self, btn, touch):
        pass

    def on_click_switch_seat_btn(self, btn, touch):
        if not self.panel.change_seat.isVisible():
            self.panel.change_seat.setVisible(True)
            self.panel.btn_seat.SetSelect(True)
        else:
            self.panel.change_seat.setVisible(False)
            self.panel.btn_seat.SetSelect(False)

    def on_click_seat_btn_4(self, btn, touch):
        self.click_seat_btn(4)

    def on_click_seat_btn_3(self, btn, touch):
        self.click_seat_btn(3)

    def on_click_seat_btn_2(self, btn, touch):
        self.click_seat_btn(2)

    def on_click_seat_btn_1(self, btn, touch):
        self.click_seat_btn(1)

    def click_seat_btn(self, index):
        if self.player:
            self.player.send_event('E_TRY_CHANGE_SEAT', (index - 1) % len(self.seat_list))

    def on_exit_forward_ope_mode(self, is_driver):
        if is_driver and self.player:
            self.player.send_event('E_MOVE_NO_FORCE')

    def init_buttons_ope_parameters(self):
        self.is_in_speed_acc_lock = False
        min_y = self.panel.nd_drag_zone.ConvertToWorldSpacePercentage(50, 0)
        max_y = self.panel.nd_drag_zone.ConvertToWorldSpacePercentage(50, 100)
        self.forward_max_y = self.panel.btn_forward.getParent().convertToNodeSpace(max_y).y
        self.forward_min_y = self.panel.btn_forward.getParent().convertToNodeSpace(min_y).y
        self._on_bar_left_turn_dir = 0
        self.last_rocker_turn_time = 0
        self.max_turn_offset = 0

    def update_rocker_center_pos(self):
        self.rocker_center_pos = self.panel.layer_turn_bar.ConvertToWorldSpacePercentage(50, 50)
        self.rocker_old_center_lpos = self.panel.btn_turn.getPosition()

    @claim_shortcut_functionality((DRIVE_MOVE_FOWARD,), 'DriveUITwo', prerequisites=drive_movement_shortcut_names)
    def on_begin_btn_forward(self, btn, touch, is_mock=False):
        from logic.gutils.move_utils import can_move
        if not can_move():
            return False
        else:
            if self.player:
                self.player.send_event('E_MOVE_FORWARD')
            self.panel.nd_speed_acc_lock.setVisible(True)
            self.panel.bar_speedup.setVisible(True)
            self.panel.nd_locked.setVisible(False)
            self.panel.btn_forward.SetFrames('', [self.BTN_FORWARD_NORMAL_PIC, self.BTN_FORWARD_SEL_PIC, self.BTN_FORWARD_NORMAL_PIC], False, None)
            self.panel.bar_speedup.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/drive/bar_forward_nml.png')
            if self.panel.layer_drive_2.isVisible():
                lpos = self.panel.convertToNodeSpace(btn.ConvertToWorldSpacePercentage(50, 50))
                self.play_touch_effect(None, 'fire_click', lpos, btn.getScale())
            if not is_mock:
                global_data.emgr.on_touch_drive_ui_event.emit(touch)
            return True

    @claim_shortcut_functionality((DRIVE_MOVE_BACKWARD,), 'DriveUITwo', prerequisites=drive_movement_shortcut_names)
    def on_begin_btn_back(self, btn, touch, is_mock=False):
        from logic.gutils.move_utils import can_move
        if not can_move():
            return False
        else:
            if self.is_in_speed_acc_lock:
                self.switch_speed_lock_state(False)
            if self.player:
                self.player.send_event('E_MOVE_BACK')
            if self.panel.layer_drive_2.isVisible():
                lpos = self.panel.convertToNodeSpace(btn.ConvertToWorldSpacePercentage(50, 50))
                self.play_touch_effect(None, 'fire_click', lpos, btn.getScale())
            if not is_mock:
                global_data.emgr.on_touch_drive_ui_event.emit(touch)
            return True

    @unclaim_shortcut_functionality((DRIVE_MOVE_FOWARD,), 'DriveUITwo')
    def on_end_btn_forward(self, btn, touch):
        wpos = touch.getLocation()
        cur_y = self.panel.btn_forward.getPosition().y
        if cur_y > self.forward_max_y - 10:
            self.switch_speed_lock_state(True)
            self.panel.btn_forward.SetFrames('', [self.BTN_FORWARD_NORMAL_PIC, self.BTN_FORWARD_LOCK_PIC, self.BTN_FORWARD_NORMAL_PIC], False, None)
        else:
            self.switch_speed_lock_state(False)
        self.panel.nd_speed_acc_lock.setVisible(False)
        self.panel.bar_speedup.setVisible(False)
        if not self.is_in_speed_acc_lock:
            if self.player:
                self.player.send_event('E_MOVE_NO_FORCE')
        return

    def _on_second_layer_lock(self):
        self.switch_speed_lock_state(True)
        self.panel.btn_forward.SetFrames('', [self.BTN_FORWARD_NORMAL_PIC, self.BTN_FORWARD_LOCK_PIC, self.BTN_FORWARD_NORMAL_PIC], False, None)
        self.panel.nd_speed_acc_lock.setVisible(False)
        self.panel.bar_speedup.setVisible(False)
        return

    def _on_second_layer_unlock(self):
        self.switch_speed_lock_state(False)
        self.panel.btn_forward.SetFrames('', [self.BTN_FORWARD_NORMAL_PIC, self.BTN_FORWARD_SEL_PIC, self.BTN_FORWARD_NORMAL_PIC], False, None)
        self.panel.nd_speed_acc_lock.setVisible(False)
        self.panel.bar_speedup.setVisible(False)
        return

    def on_drag_btn_forward(self, btn, touch):
        s_pos = touch.getStartLocation()
        wpos = touch.getLocation()
        lpos = self.panel.btn_forward.getParent().convertToNodeSpace(wpos)
        s_lpos = self.panel.btn_forward.getParent().convertToNodeSpace(s_pos)
        new_y = self.forward_min_y + lpos.y - s_lpos.y
        new_y = int(min(max(self.forward_min_y, new_y), self.forward_max_y))
        if new_y > self.forward_max_y - 10:
            self.panel.bar_speedup.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/drive/bar_forward_sel.png')
            self.panel.btn_forward.SetFrames('', [self.BTN_FORWARD_NORMAL_PIC, self.BTN_FORWARD_LOCK_PIC, self.BTN_FORWARD_NORMAL_PIC], False, None)
        else:
            self.panel.bar_speedup.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/drive/bar_forward_nml.png')
            self.panel.btn_forward.SetFrames('', [self.BTN_FORWARD_NORMAL_PIC, self.BTN_FORWARD_SEL_PIC, self.BTN_FORWARD_NORMAL_PIC], False, None)
        self.panel.btn_forward.setPosition(self.panel.btn_forward.getPosition().x, new_y)
        return

    def switch_speed_lock_state(self, is_lock):
        self.is_in_speed_acc_lock = is_lock
        self.panel.nd_locked.setVisible(is_lock)
        if is_lock:
            pic_path = 'gui/ui_res_2/battle/drive/bar_forward_sel.png'
        else:
            pic_path = 'gui/ui_res_2/battle/drive/bar_forward_nml.png'
        self._is_lock = is_lock
        self.panel.btn_forward.ReConfPosition()
        self.panel.bar_speedup.SetDisplayFrameByPath('', pic_path)

    @unclaim_shortcut_functionality((DRIVE_MOVE_BACKWARD,), 'DriveUITwo')
    def on_end_btn_back(self, btn, touch):
        if self.player:
            self.player.send_event('E_MOVE_NO_FORCE')

    def _record_time_on_begin(self, btn):
        btn._start_time = self.get_cur_time()
        btn._last_time = btn._start_time
        return True

    def _record_cur_time(self, btn, touch):
        btn._cur_time = self.get_cur_time()
        return True

    def get_cur_time(self):
        from logic.gcommon import time_utility as tutil
        return tutil.get_time()

    def on_exit_button_ope_mode(self):
        self.set_cur_vehicle_offset(0)
        self.enable_camera_follow(False)

    def on_switch_car_ope(self, new_ope):
        if new_ope == self.cur_drive_ope_sel:
            return
        if self.cur_drive_ope_sel == uoc.DRIVE_OPE_FORWARD:
            self.on_exit_forward_ope_mode(self.is_driver)
        elif self.cur_drive_ope_sel == uoc.DRIVE_OPE_BUTTON:
            self.on_exit_button_ope_mode()
        else:
            self.on_exit_button_ope_mode()
        self.cur_drive_ope_sel = new_ope
        self.on_check_driver_car(self.is_driver)
        self._is_lock = False
        self.reset_keyboard_ctrl()

    def on_check_driver_car(self, is_driver=True):
        self.is_driver = is_driver
        if is_driver:
            if self.cur_drive_ope_sel == uoc.DRIVE_OPE_FORWARD:
                self.panel.layer_drive.setVisible(True)
                self.panel.layer_drive_2.setVisible(False)
                self.set_associated_ui_visible(['MoveRockerUI'], False)
            elif self.cur_drive_ope_sel == uoc.DRIVE_OPE_BUTTON:
                self.panel.layer_drive.setVisible(False)
                self.panel.layer_drive_2.setVisible(True)
                self.set_associated_ui_visible(['MoveRockerUI'], False)
            else:
                self.panel.layer_drive.setVisible(False)
                self.panel.layer_drive_2.setVisible(False)
                self.set_associated_ui_visible(['MoveRockerUI'], True)
        else:
            self.panel.layer_drive.setVisible(False)
            self.panel.layer_drive_2.setVisible(False)
            self.set_associated_ui_visible(['MoveRockerUI'], False)
        if self.cur_vehicle and self.cur_vehicle.logic:
            enable_turn = self.cur_drive_ope_sel != uoc.DRIVE_OPE_FORWARD
            self.cur_vehicle.logic.send_event('E_ENABLE_TARGET_YAW_OFFSET', enable_turn)
            if not enable_turn:
                self.cur_vehicle.logic.send_event('E_ENABLE_VEHICLE_CAMERA_FOLLOW', enable_turn)

    def on_touch_bottom_begin(self, *args):
        self.enable_camera_follow(False)
        self._is_in_touch_bottom = True
        return True

    def on_touch_bottom_end(self, *args):
        self._is_in_touch_bottom = False

    def enable_camera_follow(self, enable):
        if self.cur_drive_ope_sel == uoc.DRIVE_OPE_BUTTON and self.is_driver:
            if self.cur_vehicle and self.cur_vehicle.logic:
                self.cur_vehicle.logic.send_event('E_ENABLE_VEHICLE_CAMERA_FOLLOW', enable)

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import VEHICLE_MODE
        self.cur_camera_state_type = state
        if self.is_driver:
            if self.cur_camera_state_type != VEHICLE_MODE:
                self.enable_camera_follow(False)

    def init_keyboard_control_parameters(self):
        self.is_open_up_keyctrl = True
        import game
        self._keystate = {game.VK_W: 0,game.VK_S: 0,
           game.VK_A: 0,
           game.VK_D: 0
           }
        self._key_to_shortcut_name = {game.VK_W: DRIVE_MOVE_FOWARD,
           game.VK_S: DRIVE_MOVE_BACKWARD,
           game.VK_A: DRIVE_MOVE_LEFT,
           game.VK_D: DRIVE_MOVE_RIGHT
           }

    def reset_keyboard_ctrl(self):
        import game
        for key in self._keystate:
            if self._keystate[key]:
                self.on_keyboard_ctrl_change(key, game.MSG_KEY_UP)

    def on_keyboard_ctrl_change(self, key, msg_type, skip_claim_shortcut_logic=False):
        if not self.is_open_up_keyctrl:
            return
        else:
            import game
            if msg_type == game.MSG_KEY_UP:
                state = 0
            else:
                state = 1
            if self._keystate.get(key, None) != state:
                key_get_handled_down_msg = [
                 None]
                self.on_open_key_ctrl_for_drive_ui(key, key_get_handled_down_msg, skip_claim_shortcut_logic)
                if msg_type == game.MSG_KEY_UP:
                    self._keystate[key] = 0
                else:
                    self._keystate[key] = 1
                if key_get_handled_down_msg[0] is not None:
                    if self.cur_drive_ope_sel == uoc.DRIVE_OPE_FORWARD:
                        if key_get_handled_down_msg[0] in (game.VK_W, game.VK_S):
                            self._on_first_layer_unlock(exclude_btn_speed=True)
                    elif self.cur_drive_ope_sel == uoc.DRIVE_OPE_BUTTON:
                        if key_get_handled_down_msg[0] in (game.VK_W, game.VK_S):
                            self._on_second_layer_unlock()
            return

    NEED_TRANSFORM_HOTKEYS = {game.VK_W: hot_key_def.MOVE_FORWARD,
       game.VK_S: hot_key_def.MOVE_BACKWARD,
       game.VK_A: hot_key_def.MOVE_LEFT,
       game.VK_D: hot_key_def.MOVE_RIGHT
       }

    def _drive_ui_key_transform(self, vk_code):
        if vk_code in self.NEED_TRANSFORM_HOTKEYS:
            hotkey_name = self.NEED_TRANSFORM_HOTKEYS[vk_code]
            cur_vk_name_list = hot_key_utils.get_hotkey_binding(hotkey_name)
            cur_vk_code_list = hot_key_utils.vk_name_list_to_vk_code_list(cur_vk_name_list)
            if len(cur_vk_code_list) == 1:
                return cur_vk_code_list[0]
        return vk_code

    def on_open_key_ctrl_for_drive_ui(self, changed_key, out_key_get_handled_down_msg, skip_claim_shortcut_logic=False):
        import game
        cur_lpos = self.panel.btn_speed.getPosition()
        if changed_key in [game.VK_W, game.VK_S]:
            is_w_down = game_hook.is_key_down(self._drive_ui_key_transform(game.VK_W))
            is_s_down = game_hook.is_key_down(self._drive_ui_key_transform(game.VK_S))
            is_changed_key_down = game_hook.is_key_down(self._drive_ui_key_transform(changed_key))
            skip_following = False
            if global_data.is_pc_mode:
                shortcut_name = self._key_to_shortcut_name.get(changed_key, None)
                if shortcut_name is not None:
                    if is_changed_key_down:
                        if not skip_claim_shortcut_logic:
                            if not try_claim_shortcut_functionality((shortcut_name,), 'DriveUIKeyboard', prerequisites=drive_movement_shortcut_names):
                                skip_following = True
                    else:
                        if not is_all_shortcut_functionality_claimed((shortcut_name,), 'DriveUIKeyboard'):
                            skip_following = True
                        try_unclaim_shortcut_functionality((shortcut_name,), 'DriveUIKeyboard')
            if not skip_following:
                if is_changed_key_down:
                    out_key_get_handled_down_msg[0] = changed_key
                if is_w_down and is_s_down:
                    old_pos = self.panel.btn_speed_start.getPosition()
                    self.panel.btn_speed.setPosition(old_pos)
                    self._move_no_force()
                    self.panel.btn_forward.SetSelect(False)
                    self.panel.btn_back.SetSelect(False)
                elif is_w_down:
                    wpos = self.panel.normal.ConvertToWorldSpacePercentage(50, 50)
                    lpos = self.panel.btn_speed.getParent().convertToNodeSpace(wpos)
                    self.panel.btn_speed.SetPosition(cur_lpos.x, lpos.y)
                    self._move_forward()
                    self.panel.btn_forward.SetSelect(True)
                    self.panel.btn_back.SetSelect(False)
                elif is_s_down:
                    wpos = self.panel.back.ConvertToWorldSpacePercentage(50, 50)
                    lpos = self.panel.btn_speed.getParent().convertToNodeSpace(wpos)
                    self.panel.btn_speed.SetPosition(cur_lpos.x, lpos.y)
                    self._move_back()
                    self.panel.btn_forward.SetSelect(False)
                    self.panel.btn_back.SetSelect(True)
                else:
                    old_pos = self.panel.btn_speed_start.getPosition()
                    self.panel.btn_speed.setPosition(old_pos)
                    self._move_no_force()
                    self.panel.btn_forward.SetSelect(False)
                    self.panel.btn_back.SetSelect(False)
        if changed_key in [game.VK_A, game.VK_D]:
            if self.cur_drive_ope_sel == uoc.DRIVE_OPE_FORWARD:
                return
            if changed_key == game.VK_A:
                if game_hook.is_key_down(self._drive_ui_key_transform(game.VK_A)) and not self._keystate[game.VK_A]:
                    do = True
                    if global_data.is_pc_mode and not skip_claim_shortcut_logic:
                        shortcut_name = self._key_to_shortcut_name.get(game.VK_A, None)
                        if shortcut_name is not None:
                            if not try_claim_shortcut_functionality((shortcut_name,), 'DriveUIKeyboard', prerequisites=drive_movement_shortcut_names):
                                do = False
                    if do:
                        self.panel.btn_left.SetSelect(True)
                        self._move_left_begin()
                        out_key_get_handled_down_msg[0] = game.VK_A
                        return
                else:
                    do = True
                    if global_data.is_pc_mode:
                        shortcut_name = self._key_to_shortcut_name.get(game.VK_A, None)
                        if shortcut_name is not None:
                            if not is_all_shortcut_functionality_claimed((shortcut_name,), 'DriveUIKeyboard'):
                                do = False
                            try_unclaim_shortcut_functionality((shortcut_name,), 'DriveUIKeyboard')
                    if do:
                        self.panel.btn_left.SetSelect(False)
                        self._move_left_end()
            if changed_key == game.VK_D:
                if game_hook.is_key_down(self._drive_ui_key_transform(game.VK_D)) and not self._keystate[game.VK_D]:
                    do = True
                    if global_data.is_pc_mode and not skip_claim_shortcut_logic:
                        shortcut_name = self._key_to_shortcut_name.get(game.VK_D, None)
                        if shortcut_name is not None:
                            if not try_claim_shortcut_functionality((shortcut_name,), 'DriveUIKeyboard', prerequisites=drive_movement_shortcut_names):
                                do = False
                    if do:
                        self.panel.btn_right.SetSelect(True)
                        self._move_right_begin()
                        out_key_get_handled_down_msg[0] = game.VK_D
                        return
                else:
                    do = True
                    if global_data.is_pc_mode:
                        shortcut_name = self._key_to_shortcut_name.get(game.VK_D, None)
                        if shortcut_name is not None:
                            if not is_all_shortcut_functionality_claimed((shortcut_name,), 'DriveUIKeyboard'):
                                do = False
                            try_unclaim_shortcut_functionality((shortcut_name,), 'DriveUIKeyboard')
                    if do:
                        self.panel.btn_right.SetSelect(False)
                        self._move_right_end()
        return

    def on_item_data_changed(self, item_data):
        pass

    def on_begin_btn_turn(self, btn, touch):
        pt = touch.getLocation()
        rocker_utils.set_rocker_center_pos(pt, self.rocker_center_pos, self.panel.btn_turn, self.rocker_spawn_radius)
        offset = self.get_cur_offset_from_touch(pt)
        self.set_cur_vehicle_offset(offset)
        self.update_show_dir_from_touch(pt)
        return True

    def on_drag_btn_turn(self, btn, touch):
        pt = touch.getLocation()
        self.panel.btn_turn.setPosition(self.panel.btn_turn.getParent().convertToNodeSpace(pt))
        rocker_utils.set_rocker_center_pos(pt, self.rocker_center_pos, self.panel.btn_turn, self.rocker_spawn_radius)
        self.update_show_dir_from_touch(pt)
        offset = self.get_cur_offset_from_touch(pt)
        self.set_cur_vehicle_offset(offset)

    def on_end_btn_turn(self, btn, touch):
        self.panel.btn_turn.setPosition(self.rocker_old_center_lpos)
        self.panel.btn_left.SetSelect(False)
        self.panel.btn_right.SetSelect(False)
        self._on_bar_left_turn_dir = None
        self.set_cur_vehicle_offset(0)
        return

    def _move_left_begin(self):

        def update_offset(pass_time):
            percent = min(max(0.0, pass_time / self.full_speed_ope_turn_time), 1.0)
            self.set_cur_vehicle_offset(-1 * max(self.max_turn_offset * percent, self.min_ope_turn_offset))

        self.panel.layer_turn_bar.stopAllActions()
        self.panel.layer_turn_bar.TimerAction(update_offset, self.full_speed_ope_turn_time, callback=lambda : update_offset(1.0))
        self.set_cur_vehicle_offset(-1 * self.min_ope_turn_offset)
        if self.panel.layer_drive_2.isVisible():
            lpos = self.panel.convertToNodeSpace(self.panel.btn_left.getParent().convertToWorldSpace(self.panel.btn_left.getPosition()))
            self.play_touch_effect(None, 'fire_click', lpos, self.panel.btn_left.getScale())
        return True

    def _move_left_end(self):
        self.panel.layer_turn_bar.stopAllActions()

        def delay_callback():
            if not game_hook.is_key_down(self._drive_ui_key_transform(game.VK_D)):
                self.set_cur_vehicle_offset(0)

        self.panel.layer_turn_bar.SetTimeOut(0.06, delay_callback, tag=DriveUI.DELAY_TURN_TAG)

    @claim_shortcut_functionality((DRIVE_MOVE_LEFT,), 'DriveUITwo', prerequisites=drive_movement_shortcut_names)
    def on_begin_btn_left(self, *args):
        from logic.gutils.move_utils import can_move
        if not can_move():
            return False
        self._move_left_begin()
        return True

    @unclaim_shortcut_functionality((DRIVE_MOVE_LEFT,), 'DriveUITwo')
    def on_end_btn_left(self, *args):
        self._move_left_end()

    def _move_right_begin(self):

        def update_offset(pass_time):
            percent = min(max(0.0, pass_time / self.full_speed_ope_turn_time), 1.0)
            self.set_cur_vehicle_offset(max(self.max_turn_offset * percent, self.min_ope_turn_offset))

        self.panel.layer_turn_bar.stopAllActions()
        self.panel.layer_turn_bar.TimerAction(update_offset, self.full_speed_ope_turn_time, callback=lambda : update_offset(1.0))
        self.set_cur_vehicle_offset(self.min_ope_turn_offset)
        if self.panel.layer_drive_2.isVisible():
            lpos = self.panel.convertToNodeSpace(self.panel.btn_right.getParent().convertToWorldSpace(self.panel.btn_right.getPosition()))
            self.play_touch_effect(None, 'fire_click', lpos, self.panel.btn_right.getScale())
        return

    def _move_right_end(self):
        self.panel.layer_turn_bar.stopAllActions()

        def delay_callback():
            if not game_hook.is_key_down(self._drive_ui_key_transform(game.VK_A)):
                self.set_cur_vehicle_offset(0)

        self.panel.layer_turn_bar.SetTimeOut(0.06, delay_callback, tag=DriveUI.DELAY_TURN_TAG)

    @claim_shortcut_functionality((DRIVE_MOVE_RIGHT,), 'DriveUITwo', prerequisites=drive_movement_shortcut_names)
    def on_begin_btn_right(self, *args):
        from logic.gutils.move_utils import can_move
        if not can_move():
            return False
        self._move_right_begin()
        return True

    @unclaim_shortcut_functionality((DRIVE_MOVE_RIGHT,), 'DriveUITwo')
    def on_end_btn_right(self, *args):
        self._move_right_end()

    def set_cur_vehicle_offset(self, offset):
        if self.cur_vehicle and self.cur_vehicle.logic:
            self.cur_vehicle.logic.send_event('E_SET_TARGET_YAW_OFFSET', offset)
            if not self._is_in_touch_bottom:
                self.enable_camera_follow(True)

    def get_cur_offset_from_touch(self, touch_wpos):
        raw_percent = float(touch_wpos.x - self.rocker_center_pos.x) / self.rocker_spawn_radius
        percent_val = min(abs(raw_percent), 1.0)
        percent = percent_val if raw_percent > 0 else percent_val * -1
        MAX_OFFSET = 0.785
        return MAX_OFFSET * percent

    def update_show_dir_from_touch(self, touch_wpos):
        if touch_wpos.x - self.rocker_center_pos.x < 0:
            self.panel.btn_right.SetSelect(False)
            self.panel.btn_left.SetSelect(True)
        else:
            self.panel.btn_left.SetSelect(False)
            self.panel.btn_right.SetSelect(True)

    def on_begin_speed_up(self, layer, touch):
        if self.is_in_speed_acc_lock:
            self.switch_speed_lock_state(False)
        self.panel.btn_forward.SetSelect(True)
        return True

    def on_end_speed_up(self, layer, touch):
        if not self.is_in_speed_acc_lock:
            if self.player:
                self.player.send_event('E_MOVE_NO_FORCE')
        self.panel.btn_forward.SetSelect(False)

    def on_button_ope_change(self, new_ope):
        self._button_ope = new_ope
        self.check_button_ope_position()

    def check_button_ope_position(self):
        from logic.gcommon.common_const import ui_operation_const as uoc
        if self._button_ope == uoc.DRIVE_OPE_BUTTON_MOVE_RIGHT:
            self.panel.layer_turn_bar.SetPosition(0, 0)
            self.panel.layer_turn_bar.setAnchorPoint(ccp(0, 0))
            self.panel.speed.SetPosition('100%', 0)
            self.panel.speed.setAnchorPoint(ccp(1, 0))
        elif self._button_ope == uoc.DRIVE_OPE_BUTTON_MOVE_LEFT:
            self.panel.layer_turn_bar.SetPosition('100%', 0)
            self.panel.layer_turn_bar.setAnchorPoint(ccp(1, 0))
            self.panel.speed.SetPosition(0, 0)
            self.panel.speed.setAnchorPoint(ccp(0, 0))

    def on_hot_key_state_opened(self):
        self.refresh_drive_ope()

    def on_hot_key_state_closed(self):
        self.refresh_drive_ope()

    def refresh_drive_ope(self):
        if not global_data.is_pc_mode:
            return
        if not global_data.player:
            return
        drive_ope_sel = global_data.player.get_setting_2(uoc.DRIVE_OPE_KEY)
        self.on_switch_car_ope(drive_ope_sel)

    def on_received_begin_command(self, move_vec):
        self.touch_mock.setTouchStartPos(None)
        self.touch_mock.setTouchPos(None)
        if self.cur_drive_ope_sel == uoc.DRIVE_OPE_BUTTON:
            val_tan30 = 0.57
            if abs(move_vec.x) + abs(move_vec.y) > 10:
                if abs(move_vec.x) < 0.01 or abs(move_vec.y / move_vec.x) > val_tan30:
                    if move_vec.y > 0:
                        self.touch_mock_trigger = self.panel.btn_forward
                    else:
                        self.touch_mock_trigger = self.panel.btn_back
        elif self.cur_drive_ope_sel == uoc.DRIVE_OPE_FORWARD:
            self.touch_mock_trigger = self.panel.layer_drive
        else:
            self.touch_mock_trigger = None
        if self.touch_mock_trigger:
            ret = self.touch_mock_trigger.OnBegin(self.touch_mock, is_mock=True)
            if self.touch_mock_trigger.SetSelect and ret:
                self.touch_mock_trigger.SetSelect(True)
            return ret
        else:
            return

    def on_received_move_command(self, move_vec):
        self.touch_mock.setTouchPos(move_vec)
        if self.cur_drive_ope_sel in [uoc.DRIVE_OPE_BUTTON, uoc.DRIVE_OPE_FORWARD]:
            if self.touch_mock_trigger:
                self.touch_mock_trigger.OnDrag(self.touch_mock)

    def on_received_end_command(self):
        if self.cur_drive_ope_sel in [uoc.DRIVE_OPE_BUTTON, uoc.DRIVE_OPE_FORWARD]:
            if self.touch_mock_trigger:
                if self.touch_mock_trigger.SetSelect:
                    self.touch_mock_trigger.SetSelect(False)
                self.touch_mock_trigger.OnEnd(self.touch_mock)

    def get_move_direction(self):
        if self.cur_drive_ope_sel in [uoc.DRIVE_OPE_BUTTON, uoc.DRIVE_OPE_FORWARD]:
            if self.cur_drive_ope_sel == uoc.DRIVE_OPE_BUTTON:
                if self.panel.btn_back.GetSelect():
                    return -1
                if self.panel.btn_forward.GetSelect():
                    return 1
            elif self.cur_drive_ope_sel == uoc.DRIVE_OPE_FORWARD:
                return None
        return None