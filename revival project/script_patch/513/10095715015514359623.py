# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/AttachableDriveUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import world
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
from logic.client.const import game_mode_const
from logic.gutils.guide_utils import get_change_ui_data_for_guide_ui
ICON_RES = [
 'gui/ui_res_2/battle/attack/drive_blood_prog',
 'gui/ui_res_2/battle/attack/drive_blood_bar']
from common.const import uiconst

class AttachableDriveUI(BasePanel):
    PANEL_CONFIG_NAME = 'capsule/capsule_skateboard'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    MAX_SEAT_NUM = 4
    UI_ACTION_EVENT = {'btn_getoff_skateboard.OnClick': 'on_click_get_off_btn'
       }
    ASSOCIATE_UI_LIST = []
    HOT_KEY_FUNC_MAP_SHOW = {'get_off_skateboard_or_vehicle': {'node': 'temp_pc'}}

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})
        self.panel.btn_getoff_skateboard.setVisible(not global_data.is_pc_mode)

    def init_event(self):
        if global_data.game_mode and not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_EXERCISE):
            global_data.emgr.on_skate_hp_changed += self.on_skate_hp_changed
        self.set_associated_ui_visible(self.ASSOCIATE_UI_LIST, False)

    def on_finalize_panel(self):
        self.set_associated_ui_visible(self.ASSOCIATE_UI_LIST, True)
        self.on_player_setted(None)
        self.destroy_widget('custom_ui_com')
        return

    def init_parameters(self):
        self.max_health = 100
        self.cur_health = 100
        self.player = None
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        if player:
            self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted
        ignore_hp = global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_EXERCISE)
        if not ignore_hp and player:
            hp = player.ev_g_attachable_hp()
            max_hp = player.ev_g_attachable_max_hp()
            self.on_skate_hp_changed((hp, max_hp))
        else:
            self.on_skate_hp_changed((100, 100))
        return

    def on_player_setted(self, player):
        self.player = player

    def on_set_attachable(self, vehicle):
        if self.cur_vehicle:
            self.process_bind_attachable_event(self.cur_vehicle.logic, is_bind=False)
        if vehicle and vehicle.logic:
            LOGIC_GET_VALUE = vehicle.logic.get_value
            self.max_health = LOGIC_GET_VALUE('G_MAX_HP')
            if self.panel:
                self.process_bind_attachable_event(vehicle.logic, is_bind=True)

    def process_bind_attachable_event(self, lvehicle, is_bind=True):
        if lvehicle and lvehicle.is_valid():
            if is_bind:
                ope_func = lvehicle.regist_event
            else:
                ope_func = lvehicle.unregist_event

    def set_associated_ui_visible(self, ui_list, is_show):
        posture_control_ui = global_data.ui_mgr.get_ui('PostureControlUI')
        if posture_control_ui:
            posture_control_ui.btn_roll.setVisible(is_show)
            posture_control_ui.btn_squat.setVisible(is_show)
        for ui_name in ui_list:
            ui_inst = global_data.ui_mgr.get_ui(ui_name)
            if ui_inst:
                if is_show:
                    ui_inst.add_show_count(self.__class__.__name__)
                else:
                    ui_inst.add_hide_count(self.__class__.__name__)

    def on_car_begin_fly(self):
        if self.panel:
            self.panel.btn_go.setVisible(False)
            self.panel.get_off.setVisible(False)

    def on_click_get_off_btn(self, btn, touch):
        if self.player:
            if self.player.ev_g_is_jump():
                return
            self.player.send_event('E_LEAVE_ATTACHABLE_ENTITY')
        self.close()

    def on_skate_hp_changed(self, hp_info):
        hp, max_hp = hp_info
        percent = hp * 100.0 / max_hp
        percentage_range = (62.52, 88.13)
        rate = (percentage_range[1] - percentage_range[0]) * 1.0 / 100
        blood_res = self.get_uires_by_percent(percent, ICON_RES[0])
        self.panel.progress_skateboard.SetProgressTexture(blood_res)
        bar_res = self.get_uires_by_percent(percent, ICON_RES[1])
        self.panel.skateboard_bar.SetDisplayFrameByPath('', bar_res)
        self.panel.progress_skateboard.setPercentage(percent * rate + percentage_range[0])
        self.panel.lab_hp.SetString(ui_utils.get_ratio_txt(hp, max_hp))

    def get_uires_by_percent(self, percent, original_res):
        if percent > 25:
            return ''.join([original_res, '.png'])
        return ''.join([original_res, '_red', '.png'])

    def set_btn_getoff_skateboard_visible(self, visible):
        self.panel.btn_getoff_skateboard.setVisible(visible)

    def set_btn_getoff_skateboard_enable(self, enable):
        self.panel.btn_getoff_skateboard.SetEnable(enable)
        self.panel.btn_getoff_skateboard.img_ban.setVisible(not enable)

    def on_change_ui_custom_data(self):
        ui = global_data.ui_mgr.get_ui('GuideUI')
        if ui:
            param = self.change_ui_data()
            ui.on_change_ui_inform_guide_mixed(param)

    def change_ui_data(self):
        need_to_adjust_scale_type_nodes = (('btn_getoff_skateboard', 'nd_skateboard_tips', None), )
        return get_change_ui_data_for_guide_ui(need_to_adjust_scale_type_nodes, self.panel)