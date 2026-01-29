# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MotorcycleTransUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
from logic.gcommon.common_const import mecha_const as mconst
import logic.gcommon.cdata.status_config as status_config
import logic.gcommon.cdata.mecha_status_config as mecha_status_config
from logic.client.const import game_mode_const
import cc
import math3d
from logic.client.const import game_mode_const
from logic.gutils.guide_utils import get_change_ui_data_for_guide_ui
ICON_RES = [
 'gui/ui_res_2/battle/attack/drive_blood_prog',
 'gui/ui_res_2/battle/attack/drive_blood_bar']
SKILL_SPEED_UP = 410851
RECOVER_RATE = 0.05
from common.const import uiconst

class MotorcycleTransUI(BasePanel):
    PANEL_CONFIG_NAME = 'drive/drive_vehicle_btn'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    HOT_KEY_CHECK_VISIBLE = True
    UI_ACTION_EVENT = {'get_off.OnClick': 'on_get_off',
       'speed_up.OnClick': '_on_speed_up',
       'switch.OnClick': 'on_switch_seat'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'car_rush': {'node': 'speed_up.temp_pc'},'switch_seat': {'node': 'switch.temp_pc'},'get_off_skateboard_or_vehicle': {'node': ['get_off.temp_pc']}}
    ASSOCIATE_UI_LIST = [
     'PostureControlUI', 'ThrowRockerUI']

    def on_init_panel(self):
        self.init_parameters()
        self.set_associated_ui_visible(MotorcycleTransUI.ASSOCIATE_UI_LIST, False)
        self.init_custom_com()
        if global_data.is_pc_mode:
            self.panel.get_off.setVisible(False)
            self.panel.speed_up.setVisible(False)
            self.panel.switch.setVisible(False)
        else:
            self.panel.get_off.setVisible(True)
            self.panel.speed_up.setVisible(self.seat_index == 0)
            self.panel.switch.setVisible(True)
        if not global_data.is_pc_mode:
            self.check_show_nd_guide()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_parameters(self):
        import world
        self.player = None
        self._cur_mecha = None
        self.seat_index = -1
        self._can_acclerate = True
        scn = world.get_active_scene()
        player = scn.get_player()
        self._recover = RECOVER_RATE
        emgr = global_data.emgr
        if player:
            self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted
        return

    def on_player_setted(self, player):
        self.player = player
        if self.player:
            cur_control_target = self.player.ev_g_control_target()
            if cur_control_target and cur_control_target.logic and cur_control_target.logic.is_valid():
                self._set_mecha(cur_control_target)

    def _set_mecha(self, mecha):
        if self._cur_mecha:
            self.process_bind_mecha_event(self._cur_mecha.logic, is_bind=False)
        self._cur_mecha = mecha
        if mecha and mecha.logic:
            self.seat_index = mecha.logic.ev_g_passenger_seat_index(self.player.id)
            vehicle_type = mecha.logic.ev_g_vehicle_type()
            from data import vehicle_data
            vehicle_conf = vehicle_data.data.get(str(vehicle_type), {})
            self.process_bind_mecha_event(mecha.logic, True)
            pattern = mecha.logic.ev_g_pattern()
            ignore_hp = global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_EXERCISE)
            if not ignore_hp:
                self._on_mecha_health_changed()
            else:
                self._set_mecha_health_ignored()
            self._init_skill()

    def on_finalize_panel(self):
        self._set_mecha(None)
        self.on_player_setted(None)
        self.set_associated_ui_visible(MotorcycleTransUI.ASSOCIATE_UI_LIST, True)
        self.destroy_widget('custom_ui_com')
        return

    def set_associated_ui_visible(self, ui_list, is_show):
        for ui_name in ui_list:
            ui_inst = global_data.ui_mgr.get_ui(ui_name)
            if ui_inst:
                if is_show:
                    ui_inst.add_show_count(self.__class__.__name__)
                else:
                    ui_inst.add_hide_count(self.__class__.__name__)

    def process_bind_mecha_event(self, lmecha, is_bind=True):
        if lmecha and lmecha.is_valid():
            if is_bind:
                ope_func = lmecha.regist_event
            else:
                ope_func = lmecha.unregist_event
            if global_data.game_mode and not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_EXERCISE):
                ope_func('E_HEALTH_HP_CHANGE', self._on_mecha_health_changed)
            ope_func('E_ENERGY_CHANGE', self._on_energy_change)
            ope_func('E_ADD_SKILL', self._on_add_skill)
            ope_func('E_CHANGE_PASSENGER', self.change_passenger)

    def change_passenger(self, passenger_id, seat_name):
        if passenger_id != self.player.id:
            return
        self.seat_index = self._cur_mecha.logic.ev_g_passenger_seat_index(self.player.id)
        if global_data.is_pc_mode:
            self.panel.speed_up.setVisible(False)
        else:
            self.panel.speed_up.setVisible(self.seat_index == 0)

    def _on_mecha_health_changed(self, *args):
        if self._cur_mecha and self._cur_mecha.logic:
            percentage_range = (62.52, 88.13)
            rate = (percentage_range[1] - percentage_range[0]) * 1.0 / 100
            percent = self._cur_mecha.logic.ev_g_health_percent() * 100
            blood_res = self.get_uires_by_percent(percent, ICON_RES[0])
            self.panel.hp_progress.SetProgressTexture(blood_res)
            bar_res = self.get_uires_by_percent(percent, ICON_RES[1])
            self.panel.bar.SetDisplayFrameByPath('', bar_res)
            self.panel.hp_progress.SetPercentage(percent * rate + percentage_range[0])
            hp = self._cur_mecha.logic.share_data.ref_hp
            max_hp = self._cur_mecha.logic.ev_g_max_hp()
            self.panel.lab_hp.SetString(ui_utils.get_ratio_txt(hp, max_hp))

    def _set_mecha_health_ignored(self):
        if self._cur_mecha and self._cur_mecha.logic:
            percentage_range = (62.52, 88.13)
            rate = (percentage_range[1] - percentage_range[0]) * 1.0 / 100
            percent = self._cur_mecha.logic.ev_g_health_percent() * 100
            blood_res = self.get_uires_by_percent(percent, ICON_RES[0])
            self.panel.hp_progress.SetProgressTexture(blood_res)
            bar_res = self.get_uires_by_percent(percent, ICON_RES[1])
            self.panel.bar.SetDisplayFrameByPath('', bar_res)
            self.panel.hp_progress.SetPercentage(percent * rate + percentage_range[0])

    def get_uires_by_percent(self, percent, original_res):
        if percent > 25:
            return ''.join([original_res, '.png'])
        return ''.join([original_res, '_red', '.png'])

    def _on_mecha_speed_changed(self, speed_info):
        cur_speed, max_speed = speed_info
        self.panel.lab_speed.SetString('%s' % int(cur_speed))

    def on_get_off(self, *args):
        if self.player:
            self.player.send_event('E_TRY_LEAVE_MECHA')
            if self.player.ev_g_get_state(status_config.ST_HELP):
                self.player.send_event('E_CANCEL_RESCUE')

    def _on_speed_up(self, *args):
        if self._cur_mecha and self._cur_mecha.logic:
            self._cur_mecha.logic.send_event('E_BEGIN_OR_END_VEHICLE_DASH')

    def on_switch_seat(self, *args):
        if not self.player:
            return
        self.player.send_event('E_CHANGE_SEAT')

    def _init_skill(self):
        logic_unit = self._cur_mecha.logic
        if logic_unit:
            percent = logic_unit.ev_g_energy(SKILL_SPEED_UP)
            recover = logic_unit.ev_g_energy_recover(SKILL_SPEED_UP)
            if recover != 0:
                self._recover = recover
            self._on_energy_change(SKILL_SPEED_UP, percent)

    def _on_add_skill(self, skill_id, skill_data=None):
        if skill_id == SKILL_SPEED_UP:
            self._init_skill()

    def _on_energy_change(self, key, percent):
        if key != SKILL_SPEED_UP:
            return
        label, progress = self.panel.lab_acc, self.panel.progress_acc
        self.panel.nd_acc.setVisible(percent < 1 and percent != 0)
        left_time = (1 - percent) / self._recover
        now_progress = (1 - percent) * 100
        progress.SetPercentage(now_progress)
        if left_time <= 0:
            left_time = 0
        label.SetString('%.1f' % left_time)

    def check_show_nd_guide(self):
        self.hide_nd_guide()
        if not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            return
        if not global_data.player or not global_data.player.logic:
            return
        if global_data.player.logic.ev_g_spectate_target():
            return
        battle_times = global_data.player.get_total_cnt()
        if battle_times > 1:
            return
        control_target = global_data.player.logic.ev_g_control_target()
        if not (control_target and control_target.logic and control_target.logic.ev_g_is_mechatran()):
            return
        if control_target.logic.ev_g_pattern() == mconst.MECHA_PATTERN_VEHICLE:
            return
        is_first_joining = global_data.player.logic.ev_g_is_first_joining_veh_mecha()
        if not is_first_joining:
            return
        global_data.player.logic.send_event('E_SET_IS_FIRST_JOINING_VEH_MECHA', False)
        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(15.0),
         cc.CallFunc.create(lambda : self.show_nd_guide()),
         cc.DelayTime.create(3.0),
         cc.CallFunc.create(lambda : self.hide_nd_guide())]))

    def hide_nd_guide(self):
        self.panel.nd_guide.setVisible(False)
        if self.panel.IsPlayingAnimation('change'):
            self.panel.StopAnimation('change')

    def show_nd_guide(self):
        if not self.player:
            return
        if global_data.player.in_local_battle():
            return
        control_target = self.player.ev_g_control_target()
        if not (control_target and control_target.logic and control_target.logic.ev_g_is_mechatran()):
            return
        if control_target.logic.ev_g_pattern() == mconst.MECHA_PATTERN_VEHICLE:
            return
        self.panel.nd_guide.setVisible(True)
        if not self.panel.IsPlayingAnimation('change'):
            self.panel.PlayAnimation('change')

    def set_btn_get_off_visible(self, visible):
        self.panel.get_off.setVisible(visible)

    def set_btn_get_off_enable(self, enable):
        self.panel.get_off.SetEnable(enable)
        self.panel.get_off.img_ban.setVisible(not enable)

    def on_change_ui_custom_data(self):
        ui = global_data.ui_mgr.get_ui('GuideUI')
        if ui:
            param = self.change_ui_data()
            ui.on_change_ui_inform_guide_mixed(param)

    def change_ui_data(self):
        need_to_adjust_scale_type_nodes = (
         ('speed_up', 'nd_boost_tips', None), ('get_off', 'nd_drive_off_tips', None),
         ('switch', 'nd_deformation_tips', None))
        return get_change_ui_data_for_guide_ui(need_to_adjust_scale_type_nodes, self.panel)