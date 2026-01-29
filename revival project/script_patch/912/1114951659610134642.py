# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/AirshipDriveUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
import world
from common.const.uiconst import BASE_LAYER_ZORDER
from common.const import uiconst

class AirshipDriveUI(BasePanel):
    PANEL_CONFIG_NAME = 'capsule/capsule_airship'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    MAX_SEAT_NUM = 4
    UI_ACTION_EVENT = {'get_off.OnClick': 'on_click_get_off_btn',
       'btn_go.OnClick': 'on_click_go_btn',
       'btn_parachute.OnClick': 'on_click_parachute_btn'
       }
    ASSOCIATE_UI_LIST = [
     'FireRockerUI', 'MoveRockerUI', 'ThrowRockerUI', 'FrontSightUI', 'SceneInteractionUI', 'FightLeftShotUI', 'WeaponBarSelectUI', 'PickUI', 'StateChangeUI']

    def on_init_panel(self):
        self.init_car_parameter()
        self.init_parameters()
        self.init_event()

    def init_event(self):
        self.set_associated_ui_visible(AirshipDriveUI.ASSOCIATE_UI_LIST, False)

    def on_finalize_panel(self):
        self.set_associated_ui_visible(AirshipDriveUI.ASSOCIATE_UI_LIST, True)
        if self.cur_vehicle:
            self.process_bind_car_event(self.cur_vehicle.logic, is_bind=False)
        self.on_player_setted(None)
        return

    def init_parameters(self):
        self.player = None
        self.is_player_first_setted = False
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        if player:
            self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted
        return

    def on_player_setted(self, player):
        self.unbind_join_vehicle_event(self.player)
        self.player = player
        if self.player:
            if not self.is_player_first_setted:
                self.is_player_first_setted = True
            self.bind_join_vehicle_event(self.player)
            cur_control_target = self.player.ev_g_control_target()
            self.on_switch_control_target(cur_control_target.id, None)
            if player.ev_g_in_carrier_or_plane():
                self.on_car_fly()
        return

    def bind_join_vehicle_event(self, target):
        return
        if target and target.is_valid():
            target.regist_event('E_ON_CONTROL_TARGET_CHANGE', self.on_switch_control_target)

    def unbind_join_vehicle_event(self, target):
        return
        print('unbind_join_vehicle_event')
        if target and target.is_valid():
            target.unregist_event('E_ON_CONTROL_TARGET_CHANGE', self.on_switch_control_target)

    def on_switch_control_target(self, target_id, _, *args):
        from mobile.common.EntityManager import EntityManager
        target = EntityManager.getentity(target_id)
        if target and target.logic and target.logic.is_valid():
            if target.__class__.__name__ == 'Airship':
                self.show()
                self.on_set_car(target)
            else:
                if self.panel:
                    self.hide()
                self.on_set_car(None)
        return

    def init_car_parameter(self):
        self.max_car_health = 100
        self.cur_car_health = 100
        self.cur_vehicle = None
        return

    def _update_get_off_and_go_btn(self, vehicle):
        if not vehicle:
            self.panel.get_off.setVisible(False)
            self.panel.btn_go.setVisible(False)
            return
        from logic.gcommon.common_const import vehicle_const
        LOGIC_GET_VALUE = vehicle.logic.get_value
        status = LOGIC_GET_VALUE('G_AIRSHIP_STATUS')
        if vehicle_const.STATUS_STOP == status:
            self.panel.get_off.setVisible(True)
            self.panel.btn_go.setVisible(True)
        else:
            self.panel.get_off.setVisible(False)
            self.panel.btn_go.setVisible(False)

    def _update_drive_ship_btn(self, vehicle):
        if not vehicle:
            self.panel.btn_go.setVisible(False)
            return
        LOGIC_GET_VALUE = vehicle.logic.get_value
        driver_id = LOGIC_GET_VALUE('G_DRIVER')
        if self.player.id == driver_id:
            self.panel.btn_go.setVisible(True)
        else:
            self.panel.btn_go.setVisible(False)

    def on_set_car(self, vehicle):
        if self.cur_vehicle:
            self.process_bind_car_event(self.cur_vehicle.logic, is_bind=False)
        self.cur_vehicle = vehicle
        self._update_drive_ship_btn(vehicle)
        self._update_get_off_and_go_btn(vehicle)
        if vehicle and vehicle.logic:
            LOGIC_GET_VALUE = vehicle.logic.get_value
            self.max_car_health = LOGIC_GET_VALUE('G_MAX_HP')
            cur_hp = LOGIC_GET_VALUE('G_HP')
            speed = LOGIC_GET_VALUE('G_SPEED')
            if self.panel:
                self.on_car_health_changed(cur_hp)
                self.on_car_speed_changed(speed)
                self.process_bind_car_event(vehicle.logic, True)

    def process_bind_car_event(self, lvehicle, is_bind=True):
        if lvehicle and lvehicle.is_valid():
            if is_bind:
                ope_func = lvehicle.regist_event
            else:
                ope_func = lvehicle.unregist_event
            ope_func('E_HEALTH_HP_CHANGE', self.on_car_health_changed)
            ope_func('E_AIRSHIP_FLY', self.on_car_fly)
            ope_func('E_AIRSHIP_BEGIN_FLY', self.on_car_begin_fly)
            ope_func('E_SPEED', self.on_car_speed_changed)

    def set_associated_ui_visible(self, ui_list, is_show):
        for ui_name in ui_list:
            ui_inst = global_data.ui_mgr.get_ui(ui_name)
            if ui_inst:
                if is_show:
                    ui_inst.add_show_count('AirshipDriveUI')
                else:
                    ui_inst.add_hide_count('AirshipDriveUI')

    def on_car_speed_changed(self, speed):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        speed = speed / NEOX_UNIT_SCALE * 3.6
        speed = int(speed)
        from logic.gcommon.common_utils.local_text import get_text_by_id
        text = str(speed) + get_text_by_id(19040)
        self.panel.lab_speed.SetString(text)

    def on_car_health_changed(self, cur_hp, *arg):
        percent = cur_hp / self.max_car_health
        percent = min(percent, 1)
        percent = max(percent, 0)
        percent *= 100
        self.panel.progress_airship_red.SetPercentage(100 - percent)

    def on_car_fly(self):
        if self.panel:
            self.panel.btn_go.setVisible(False)
            self.panel.get_off.setVisible(False)
            self.panel.btn_parachute.setVisible(True)

    def on_car_begin_fly(self):
        if self.panel:
            self.panel.btn_go.setVisible(False)
            self.panel.get_off.setVisible(False)

    def on_click_get_off_btn(self, btn, touch):
        if self.player:
            self.player.send_event('E_TRY_LEAVE_VEHICLE')
        self.close()

    def on_click_go_btn(self, btn, touch):
        move_target_position = self.cur_vehicle.logic.ev_g_move_target_position()
        if not move_target_position:
            global_data.emgr.scene_show_big_map_event.emit(True)
            return
        if self.player:
            self.player.send_event('E_VEHICLE_LAUNCH', self.cur_vehicle.id, (move_target_position.x, move_target_position.z))

    def on_click_parachute_btn(self, btn, touch):
        if self.player:
            self.player.send_event('E_TRY_LEAVE_VEHICLE')
        self.close()