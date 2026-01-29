# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/CustomBattleSettingWidget.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED
from copy import deepcopy
import cc
import bisect
from logic.gcommon.common_const.custom_battle_const import CUSTOM_SETTINGS_MEMORY_SUB_GUIDE, CUSTOM_SETTINGS_CHOOSE_GUIDE_TXT, CUSTOM_SETTINGS_SAVE_GUIDE_TXT, CUSTOM_SETTINGS_TIP_TXT_CANNOT_CHANGE
from logic.gutils import template_utils
ENABLE_CONTENT_PATH = 'gui/ui_res_2/room/bar_room_content_2.png'
DISABLE_CONTENT_PATH = 'gui/ui_res_2/room/bar_room_content_3.png'
OFFSET_BUFFER = 50

class CustomBattleSettingWidget(object):

    def __init__(self, node, custom_battle_dict):
        self.panel = node
        self.nd_settings = self.panel.list_setting.GetItem(0)
        self.nd_left_btns = self.panel.list_btn_left
        self._setting_dict = deepcopy(custom_battle_dict)
        self.code_2_content_and_btn = {}
        self.double_groups = []
        self.left_lab_2_pos_and_text = {}
        self.offset_anchors = [-941, -742, -376, -102, 128, 315]
        self.offset_anchors_with_buffer = []
        self.widget_conf = confmgr.get('custom_battle_conf')
        self.need_guide = global_data.achi_mgr.get_cur_user_archive_data(CUSTOM_SETTINGS_MEMORY_SUB_GUIDE, True)
        self.guide_click_choose = None
        self.guide_click_save = None
        self.init_widget()
        self.init_settings()
        self.init_left_tab()
        self.can_change_setting = True
        return

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
        self.left_lab_2_pos_and_text = {self.nd_left_btns.GetItem(0).btn_window_tab: (
                                                       self.offset_anchors[0], 19632),
           self.nd_left_btns.GetItem(1).btn_window_tab: (
                                                       self.offset_anchors[1], 19633),
           self.nd_left_btns.GetItem(2).btn_window_tab: (
                                                       self.offset_anchors[2], 19634),
           self.nd_left_btns.GetItem(3).btn_window_tab: (
                                                       self.offset_anchors[3], 19635),
           self.nd_left_btns.GetItem(4).btn_window_tab: (
                                                       self.offset_anchors[4], 19636),
           self.nd_left_btns.GetItem(5).btn_window_tab: (
                                                       self.offset_anchors[5], 19637)
           }
        for anchor in self.offset_anchors:
            self.offset_anchors_with_buffer.append(anchor + OFFSET_BUFFER)

        for idx, ui_tp in six.iteritems(self.code_2_content_and_btn):
            conf = self.widget_conf.get(str(idx), None)
            if not conf:
                continue
            ui_tp[2].SetString(get_text_by_id(conf.get('NameTextId', 19026)))
            ui_tp[3].SetString(get_text_by_id(conf.get('ExplainTextId', 19026)))

        for lab_btn, info_tp in six.iteritems(self.left_lab_2_pos_and_text):
            lab_btn.SetText(get_text_by_id(info_tp[1]))

        self.recover_settings()
        self.show_custom_battle_click_choose_guide_ui()
        return

    def init_settings(self):
        double_check_idx = []
        for tps in self.double_groups:
            for setting_idx in tps:
                double_check_idx.append(setting_idx)

            self.set_double_setting(tps[0], tps[1])

        for code_idx, ui_tp in six.iteritems(self.code_2_content_and_btn):
            if code_idx not in double_check_idx:
                self.set_single_setting(code_idx)

    def set_double_setting(self, idx1, idx2):
        btn1 = self.code_2_content_and_btn[idx1][0]
        btn2 = self.code_2_content_and_btn[idx2][0]
        c2c_b = self.code_2_content_and_btn

        def set_idx_enable(idx, is_enable, value):
            btn = c2c_b[idx][0]
            content = c2c_b[idx][1]
            if is_enable:
                self._setting_dict[idx] = value
                content.SetDisplayFrameByPath('', ENABLE_CONTENT_PATH)
            elif idx in self._setting_dict:
                self._setting_dict.pop(idx)
                content.SetDisplayFrameByPath('', DISABLE_CONTENT_PATH)
            btn.SetSelect(is_enable)

        @btn1.callback()
        def OnClick(*args):
            if not self.can_change_setting:
                global_data.game_mgr.show_tip(get_text_by_id(CUSTOM_SETTINGS_TIP_TXT_CANNOT_CHANGE))
                return
            if btn1._curState == STATE_SELECTED:
                set_idx_enable(idx1, False, 0)
            else:
                set_idx_enable(idx1, True, 1)
            set_idx_enable(idx2, False, 0)

        @btn2.callback()
        def OnClick(*args):
            if not self.can_change_setting:
                global_data.game_mgr.show_tip(get_text_by_id(CUSTOM_SETTINGS_TIP_TXT_CANNOT_CHANGE))
                return
            if btn2._curState == STATE_SELECTED:
                set_idx_enable(idx2, False, 0)
            else:
                set_idx_enable(idx2, True, 1)
            set_idx_enable(idx1, False, 0)

    def set_single_setting(self, idx1):
        btn1 = self.code_2_content_and_btn[idx1][0]
        c2c_b = self.code_2_content_and_btn

        def set_idx_enable(idx, is_enable, value):
            btn = c2c_b[idx][0]
            content = c2c_b[idx][1]
            if is_enable:
                self._setting_dict[idx] = value
                content.SetDisplayFrameByPath('', ENABLE_CONTENT_PATH)
            elif idx in self._setting_dict:
                self._setting_dict.pop(idx)
                content.SetDisplayFrameByPath('', DISABLE_CONTENT_PATH)
            btn.SetSelect(is_enable)

        @btn1.callback()
        def OnClick(*args):
            if not self.can_change_setting:
                global_data.game_mgr.show_tip(get_text_by_id(CUSTOM_SETTINGS_TIP_TXT_CANNOT_CHANGE))
                return
            if btn1._curState == STATE_SELECTED:
                set_idx_enable(idx1, False, 0)
            else:
                set_idx_enable(idx1, True, 1)

    def set_setting_dict(self, setting_dict):
        self._setting_dict = deepcopy(setting_dict)

    def get_setting_dict(self):
        return self._setting_dict

    def recover_settings(self, setting_dict=None):
        if setting_dict is not None:
            self.set_setting_dict(setting_dict)
        for idx in six.iterkeys(self.code_2_content_and_btn):
            if idx in self._setting_dict and self._setting_dict.get(idx, 0) > 0:
                self.recover_enable(idx, True)
            else:
                self.recover_enable(idx, False)

        return

    def init_left_tab(self):
        for btn, info_tp in six.iteritems(self.left_lab_2_pos_and_text):
            self.init_left_tab_offset(btn, info_tp[0])

        self.set_left_tab_selected(self.nd_left_btns.GetItem(0).btn_window_tab)

        @self.panel.list_setting.callback()
        def OnScrolling(*args):
            pos = self.panel.list_setting.GetContentOffset()
            idx = bisect.bisect_left(self.offset_anchors_with_buffer, pos.y)
            if idx >= len(self.offset_anchors_with_buffer):
                idx = len(self.offset_anchors_with_buffer) - 1
            self.set_left_tab_selected(self.nd_left_btns.GetItem(idx).btn_window_tab)

    def init_left_tab_offset(self, btn, offset):

        @btn.callback()
        def OnClick(*args):
            self.panel.list_setting.SetContentOffset(cc.Vec2(0, offset))
            self.set_left_tab_selected(btn)

    def set_left_tab_selected(self, select_btn):
        for btn in six.iterkeys(self.left_lab_2_pos_and_text):
            if btn == select_btn:
                btn.SetSelect(True)
            else:
                btn.SetSelect(False)

    def recover_enable(self, idx, is_enable):
        btn = self.code_2_content_and_btn[idx][0]
        content = self.code_2_content_and_btn[idx][1]
        if is_enable:
            content.SetDisplayFrameByPath('', ENABLE_CONTENT_PATH)
        else:
            content.SetDisplayFrameByPath('', DISABLE_CONTENT_PATH)
        btn.SetSelect(is_enable)

    def enable_buttons(self, enable):
        self.can_change_setting = enable
        self.panel.temp_btn_1.btn_common_big.SetEnable(enable)
        self.panel.temp_btn_2.btn_common_big.SetEnable(enable)
        if enable:
            self.recover_settings()

    def show_custom_battle_click_choose_guide_ui(self):
        if not self.need_guide:
            return
        else:

            @self.panel.nd_touch.callback()
            def OnClick(*args):
                self.destroy_guide_ui()

            self.guide_click_choose = template_utils.init_guide_temp(self.nd_settings.nd_def.list_item.GetItem(2).bar_choose_1.btn_choose_1, None, CUSTOM_SETTINGS_CHOOSE_GUIDE_TXT, 'custom_battle_guide_2', 'common/i_guide_right_top', 50)
            return

    def show_custom_battle_click_save_guide_ui(self):
        if not self.need_guide:
            return
        else:
            self.guide_click_save = template_utils.init_guide_temp(self.panel.temp_btn_2.btn_common_big, None, CUSTOM_SETTINGS_SAVE_GUIDE_TXT, 'custom_battle_guide_3', 'common/i_guide_left_top', 30)
            self.need_guide = False
            global_data.achi_mgr.set_cur_user_archive_data(CUSTOM_SETTINGS_MEMORY_SUB_GUIDE, False)
            return

    def destroy_guide_ui(self):
        if self.guide_click_choose:
            self.guide_click_choose.removeFromParent()
            self.guide_click_choose = None
            if not self.guide_click_save:
                self.show_custom_battle_click_save_guide_ui()
                return
        if self.guide_click_save:
            self.guide_click_save.removeFromParent()
            self.guide_click_save = None
        return