# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/CustomBattleSettingInfoWidget.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED
from copy import deepcopy
from .SettingWidgetBase import SettingWidgetBase
ENABLE_CONTENT_PATH = 'gui/ui_res_2/room/bar_room_content_2.png'
DISABLE_CONTENT_PATH = 'gui/ui_res_2/room/bar_room_content_3.png'

class CustomBattleSettingInfoWidget(SettingWidgetBase):

    def __init__(self, panel, parent):
        super(CustomBattleSettingInfoWidget, self).__init__(panel, parent)
        self.panel = panel
        self.nd_settings = self.panel
        self._setting_dict = {}
        self.code_2_content_and_btn = {}
        self.double_groups = []
        self.widget_conf = confmgr.get('custom_battle_conf')
        self.init_widget()
        self.enable_buttons(False)
        self.recover_settings()
        self.panel.SetContentSize(923, 1342)

    def init_widget(self):
        list_def_d = self.nd_settings.nd_def.list_item
        list_atk_s = self.nd_settings.nd_atk.list_item
        list_move_d = self.nd_settings.nd_move.list_item
        list_move_s = self.nd_settings.nd_move.list_item2
        list_mode_s = self.nd_settings.nd_mode.list_item
        list_ban_s = self.nd_settings.nd_ban.list_item
        list_other_s = self.nd_settings.nd_others.list_item
        self.code_2_content_and_btn = {1: (
             list_def_d.GetItem(0).bar_choose_1.btn_choose_1, list_def_d.GetItem(0).bar_content_1, list_def_d.GetItem(0).lab_title, list_def_d.GetItem(0).bar_content_1.lab_content_1),
           2: (
             list_def_d.GetItem(0).bar_choose_2.btn_choose_2, list_def_d.GetItem(0).bar_content_2, list_def_d.GetItem(0).lab_title, list_def_d.GetItem(0).bar_content_2.lab_content_2),
           3: (
             list_def_d.GetItem(1).bar_choose_1.btn_choose_1, list_def_d.GetItem(1).bar_content_1, list_def_d.GetItem(1).lab_title, list_def_d.GetItem(1).bar_content_1.lab_content_1),
           4: (
             list_def_d.GetItem(1).bar_choose_2.btn_choose_2, list_def_d.GetItem(1).bar_content_2, list_def_d.GetItem(1).lab_title, list_def_d.GetItem(1).bar_content_2.lab_content_2),
           5: (
             list_def_d.GetItem(2).bar_choose_1.btn_choose_1, list_def_d.GetItem(2).bar_content_1, list_def_d.GetItem(2).lab_title, list_def_d.GetItem(2).bar_content_1.lab_content_1),
           6: (
             list_def_d.GetItem(2).bar_choose_2.btn_choose_2, list_def_d.GetItem(2).bar_content_2, list_def_d.GetItem(2).lab_title, list_def_d.GetItem(2).bar_content_2.lab_content_2),
           7: (
             list_atk_s.GetItem(0).bar_choose_1.btn_choose_1, list_atk_s.GetItem(0).bar_content_1, list_atk_s.GetItem(0).lab_title, list_atk_s.GetItem(0).bar_content_1.lab_content_1),
           8: (
             list_atk_s.GetItem(1).bar_choose_1.btn_choose_1, list_atk_s.GetItem(1).bar_content_1, list_atk_s.GetItem(1).lab_title, list_atk_s.GetItem(1).bar_content_1.lab_content_1),
           9: (
             list_atk_s.GetItem(2).bar_choose_1.btn_choose_1, list_atk_s.GetItem(2).bar_content_1, list_atk_s.GetItem(2).lab_title, list_atk_s.GetItem(2).bar_content_1.lab_content_1),
           10: (
              list_atk_s.GetItem(3).bar_choose_1.btn_choose_1, list_atk_s.GetItem(3).bar_content_1, list_atk_s.GetItem(3).lab_title, list_atk_s.GetItem(3).bar_content_1.lab_content_1),
           11: (
              list_atk_s.GetItem(4).bar_choose_1.btn_choose_1, list_atk_s.GetItem(4).bar_content_1, list_atk_s.GetItem(4).lab_title, list_atk_s.GetItem(4).bar_content_1.lab_content_1),
           12: (
              list_atk_s.GetItem(5).bar_choose_1.btn_choose_1, list_atk_s.GetItem(5).bar_content_1, list_atk_s.GetItem(5).lab_title, list_atk_s.GetItem(5).bar_content_1.lab_content_1),
           13: (
              list_atk_s.GetItem(6).bar_choose_1.btn_choose_1, list_atk_s.GetItem(6).bar_content_1, list_atk_s.GetItem(6).lab_title, list_atk_s.GetItem(6).bar_content_1.lab_content_1),
           14: (
              list_move_d.GetItem(0).bar_choose_1.btn_choose_1, list_move_d.GetItem(0).bar_content_1, list_move_d.GetItem(0).lab_title, list_move_d.GetItem(0).bar_content_1.lab_content_1),
           15: (
              list_move_d.GetItem(0).bar_choose_2.btn_choose_2, list_move_d.GetItem(0).bar_content_2, list_move_d.GetItem(0).lab_title, list_move_d.GetItem(0).bar_content_2.lab_content_2),
           16: (
              list_move_s.GetItem(0).bar_choose_1.btn_choose_1, list_move_s.GetItem(0).bar_content_1, list_move_s.GetItem(0).lab_title, list_move_s.GetItem(0).bar_content_1.lab_content_1),
           17: (
              list_move_s.GetItem(1).bar_choose_1.btn_choose_1, list_move_s.GetItem(1).bar_content_1, list_move_s.GetItem(1).lab_title, list_move_s.GetItem(1).bar_content_1.lab_content_1),
           18: (
              list_move_s.GetItem(2).bar_choose_1.btn_choose_1, list_move_s.GetItem(2).bar_content_1, list_move_s.GetItem(2).lab_title, list_move_s.GetItem(2).bar_content_1.lab_content_1),
           19: (
              list_move_s.GetItem(3).bar_choose_1.btn_choose_1, list_move_s.GetItem(3).bar_content_1, list_move_s.GetItem(3).lab_title, list_move_s.GetItem(3).bar_content_1.lab_content_1),
           20: (
              list_mode_s.GetItem(0).bar_choose_1.btn_choose_1, list_mode_s.GetItem(0).bar_content_1, list_mode_s.GetItem(0).lab_title, list_mode_s.GetItem(0).bar_content_1.lab_content_1),
           21: (
              list_mode_s.GetItem(1).bar_choose_1.btn_choose_1, list_mode_s.GetItem(1).bar_content_1, list_mode_s.GetItem(1).lab_title, list_mode_s.GetItem(1).bar_content_1.lab_content_1),
           22: (
              list_mode_s.GetItem(2).bar_choose_1.btn_choose_1, list_mode_s.GetItem(2).bar_content_1, list_mode_s.GetItem(2).lab_title, list_mode_s.GetItem(2).bar_content_1.lab_content_1),
           23: (
              list_mode_s.GetItem(3).bar_choose_1.btn_choose_1, list_mode_s.GetItem(3).bar_content_1, list_mode_s.GetItem(3).lab_title, list_mode_s.GetItem(3).bar_content_1.lab_content_1),
           24: (
              list_ban_s.GetItem(0).bar_choose_1.btn_choose_1, list_ban_s.GetItem(0).bar_content_1, list_ban_s.GetItem(0).lab_title, list_ban_s.GetItem(0).bar_content_1.lab_content_1),
           25: (
              list_ban_s.GetItem(1).bar_choose_1.btn_choose_1, list_ban_s.GetItem(1).bar_content_1, list_ban_s.GetItem(1).lab_title, list_ban_s.GetItem(1).bar_content_1.lab_content_1),
           26: (
              list_ban_s.GetItem(2).bar_choose_1.btn_choose_1, list_ban_s.GetItem(2).bar_content_1, list_ban_s.GetItem(2).lab_title, list_ban_s.GetItem(2).bar_content_1.lab_content_1),
           27: (
              list_other_s.GetItem(0).bar_choose_1.btn_choose_1, list_other_s.GetItem(0).bar_content_1, list_other_s.GetItem(0).lab_title, list_other_s.GetItem(0).bar_content_1.lab_content_1)
           }
        self.double_groups = [
         (1, 2), (3, 4), (5, 6), (14, 15)]
        for idx, ui_tp in six.iteritems(self.code_2_content_and_btn):
            conf = self.widget_conf.get(str(idx), None)
            if not conf:
                continue
            ui_tp[2].SetString(get_text_by_id(conf.get('NameTextId', 19026)))
            ui_tp[3].SetString(get_text_by_id(conf.get('ExplainTextId', 19026)))

        return

    def set_setting_dict(self, setting_dict):
        self._setting_dict = deepcopy(setting_dict)

    def get_setting_dict(self):
        return self._setting_dict

    def recover_settings(self):
        if global_data.battle:
            setting_dict = global_data.battle.get_customed_battle_dict()
            if setting_dict is not None:
                self.set_setting_dict(setting_dict)
            for idx in six.iterkeys(self.code_2_content_and_btn):
                if idx in self._setting_dict and self._setting_dict.get(idx, 0) > 0:
                    self.recover_enable(idx, True)
                else:
                    self.recover_enable(idx, False)

        return

    def recover_enable(self, idx, is_enable):
        btn = self.code_2_content_and_btn[idx][0]
        content = self.code_2_content_and_btn[idx][1]
        content.SetDisplayFrameByPath('', DISABLE_CONTENT_PATH)
        btn.SetSelect(is_enable)

    def enable_buttons(self, enable):
        for ui_tp in six.itervalues(self.code_2_content_and_btn):
            ui_tp[0].SetEnable(enable)