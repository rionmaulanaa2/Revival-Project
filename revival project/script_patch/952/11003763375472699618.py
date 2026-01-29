# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/TVMissileLauncherUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
from logic.gcommon.common_const import mecha_const as mconst
import logic.gcommon.cdata.status_config as status_config
import cc
import math3d
from logic.client.const import game_mode_const
from common.const import uiconst
ICON_RES = [
 'gui/ui_res_2/battle/attack/drive_blood_prog',
 'gui/ui_res_2/battle/attack/drive_blood_bar']

class TVMissileLauncherUI(BasePanel):
    PANEL_CONFIG_NAME = 'drive/drive_tv_missile_btn'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    HOT_KEY_CHECK_VISIBLE = True
    UI_ACTION_EVENT = {'get_off.OnClick': 'on_get_off'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'get_off_skateboard_or_vehicle': {'node': ['get_off.temp_pc']}}
    ASSOCIATE_UI_LIST = [
     'PostureControlUI', 'ThrowRockerUI']

    def on_init_panel(self):
        self.init_parameters()
        self.set_associated_ui_visible(TVMissileLauncherUI.ASSOCIATE_UI_LIST, False)
        self.init_custom_com()
        if global_data.is_pc_mode:
            self.panel.get_off.setVisible(False)
        else:
            self.panel.get_off.setVisible(True)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_parameters(self):
        self.lplayer = None
        self.cur_lmecha = None
        return

    def set_player(self, lplayer):
        self.lplayer = lplayer

    def set_mecha(self, lmecha):
        if self.cur_lmecha:
            self.process_bind_mecha_event(self.cur_lmecha, is_bind=False)
        self.cur_lmecha = lmecha
        if lmecha:
            self.process_bind_mecha_event(lmecha, True)
            ignore_hp = global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_EXERCISE)
            if not ignore_hp:
                self._on_mecha_health_changed()
            else:
                self._set_mecha_health_ignored()

    def on_finalize_panel(self):
        self.set_player(None)
        self.set_mecha(None)
        self.set_associated_ui_visible(TVMissileLauncherUI.ASSOCIATE_UI_LIST, True)
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

    def _on_mecha_health_changed(self, *args):
        if self.cur_lmecha.is_valid():
            percentage_range = (62.52, 88.13)
            rate = (percentage_range[1] - percentage_range[0]) * 1.0 / 100
            percent = self.cur_lmecha.ev_g_health_percent() * 100
            blood_res = self.get_uires_by_percent(percent, ICON_RES[0])
            self.panel.hp_progress.SetProgressTexture(blood_res)
            bar_res = self.get_uires_by_percent(percent, ICON_RES[1])
            self.panel.bar.SetDisplayFrameByPath('', bar_res)
            self.panel.hp_progress.SetPercentage(percent * rate + percentage_range[0])
            hp = self.cur_lmecha.share_data.ref_hp
            max_hp = self.cur_lmecha.ev_g_max_hp()
            self.panel.lab_hp.SetString(ui_utils.get_ratio_txt(hp, max_hp))

    def _set_mecha_health_ignored(self):
        if self.cur_lmecha.is_valid():
            percentage_range = (62.52, 88.13)
            rate = (percentage_range[1] - percentage_range[0]) * 1.0 / 100
            percent = self.cur_lmecha.ev_g_health_percent() * 100
            blood_res = self.get_uires_by_percent(percent, ICON_RES[0])
            self.panel.hp_progress.SetProgressTexture(blood_res)
            bar_res = self.get_uires_by_percent(percent, ICON_RES[1])
            self.panel.bar.SetDisplayFrameByPath('', bar_res)
            self.panel.hp_progress.SetPercentage(percent * rate + percentage_range[0])

    def get_uires_by_percent(self, percent, original_res):
        if percent > 25:
            return ''.join([original_res, '.png'])
        return ''.join([original_res, '_red', '.png'])

    def on_get_off(self, *args):
        if self.lplayer.is_valid():
            model = self.lplayer.ev_g_model()
            if model:
                pos = model.world_position
                pos -= model.world_rotation_matrix.forward * 2
                pos = (pos.x, pos.y, pos.z)
                self.lplayer.send_event('E_CALL_SYNC_METHOD', 'try_leave_tvml', (pos,), True)

    def set_btn_get_off_visible(self, visible):
        self.panel.get_off.setVisible(visible)

    def set_btn_get_off_enable(self, enable):
        self.panel.get_off.SetEnable(enable)
        self.panel.get_off.img_ban.setVisible(not enable)