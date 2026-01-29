# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/QuickChatSettingUI.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from common.cfg import confmgr
import copy
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

class QuickChatSettingUI(BasePanel):
    PANEL_CONFIG_NAME = 'setting/setting_tab_9'
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close',
       'btn_cancel.btn_common.OnClick': 'on_click_close',
       'btn_sure.btn_common.OnClick': 'on_click_sure',
       'btn_reserve.btn_common.OnClick': 'on_click_reserve',
       'btn_question.OnClick': 'on_click_question'
       }

    def on_init_panel(self, *args, **kwargs):
        self._shortcut_list = copy.copy(global_data.player.get_setting_2(uoc.SHORTCUT_ORDER))
        if not self._shortcut_list:
            self._shortcut_list = list(range(7))
        self._quick_chat_conf = confmgr.get('team_quick_chat', '0')
        self.selected_info = ()
        self.useable_quick_chat_list = {}
        self.shown_quick_chat_list = ()
        self.is_modified = False
        self.init_parameters()
        self.init_left_list()
        self.init_right_list()

    def init_parameters(self):
        for shortcut_id in self._quick_chat_conf['order']:
            if shortcut_id in self._shortcut_list:
                continue
            shortcut_conf = self._quick_chat_conf[str(shortcut_id)]
            type_tid = shortcut_conf.get('type_tid', None)
            if not type_tid:
                continue
            slist = self.useable_quick_chat_list.setdefault(type_tid, [])
            slist.append(shortcut_id)

        return

    def init_left_list(self):
        if not self._shortcut_list:
            return
        self.panel.left_list.SetInitCount(len(self._shortcut_list))
        for idx, shortcut_id in enumerate(self._shortcut_list):
            item = self.panel.left_list.GetItem(idx)
            shortcut_conf = self._quick_chat_conf.get(str(shortcut_id))
            item.lab_content.SetString(shortcut_conf['text_id'], args={'second': 'n'})
            item.lab_num.SetString(str(idx + 1))
            item.btn_chat.SetSelect(False)
            if not self.selected_info:
                item.btn_chat.lab_content.SetColor(2304360)
                item.btn_chat.lab_num.SetColor(10723795)

            @item.btn_chat.unique_callback()
            def OnClick(btn, touch, idx=idx):
                if self.selected_info and self.selected_info[0] == idx:
                    return
                if self.selected_info:
                    self.selected_info[1].SetSelect(False)
                    self.selected_info[1].lab_content.SetColor(2304360)
                    self.selected_info[1].lab_num.SetColor(10723795)
                btn.SetSelect(True)
                btn.lab_content.SetColor(16777215)
                btn.lab_num.SetColor(16777215)
                self.selected_info = (idx, btn)

            if self.selected_info and self.selected_info[0] == idx:
                item.btn_chat.SetSelect(True)

    def init_right_list(self):
        self.panel.temp_list_table.SetInitCount(len(self.useable_quick_chat_list))
        type_tid_list = sorted(six_ex.keys(self.useable_quick_chat_list))
        for idx, type_tid in enumerate(type_tid_list):
            item = self.panel.temp_list_table.GetItem(idx)
            item.btn_tab.SetText(type_tid)
            item.btn_tab.SetSelect(False)

            @item.btn_tab.unique_callback()
            def OnClick(btn, touch, idx=idx, type_tid=type_tid):
                if self.shown_quick_chat_list and self.shown_quick_chat_list[0] == type_tid:
                    return
                if self.shown_quick_chat_list:
                    self.shown_quick_chat_list[1].SetSelect(False)
                btn.SetSelect(True)
                self.shown_quick_chat_list = (type_tid, btn, idx)
                self.refresh_select_list(type_tid)

        if not self.shown_quick_chat_list:
            self.panel.temp_list_table.GetItem(0).btn_tab.OnClick(None)
        else:
            show_idx = self.shown_quick_chat_list[-1]
            self.panel.temp_list_table.GetItem(show_idx).btn_tab.SetSelect(True)
        return

    def refresh_select_list(self, type_tid):
        shortcut_list = self.useable_quick_chat_list.get(type_tid, [])
        print(shortcut_list)
        self.panel.temp_right_list_01.SetInitCount(len(shortcut_list))
        for idx, shortcut_id in enumerate(shortcut_list):
            item = self.panel.temp_right_list_01.GetItem(idx)
            shortcut_conf = self._quick_chat_conf.get(str(shortcut_id))
            item.lab_content.SetString(shortcut_conf['text_id'], args={'second': 'n'})
            item.lab_num.SetString(str(idx + 1))

            @item.btn_chat.unique_callback()
            def OnBegin(btn, touch):
                btn.SetSelect(True)
                btn.lab_content.SetColor(16777215)
                btn.lab_num.SetColor(16777215)

            @item.btn_chat.unique_callback()
            def OnEnd(btn, touch):
                btn.SetSelect(False)
                btn.lab_content.SetColor(2304360)
                btn.lab_num.SetColor(10723795)

            @item.btn_chat.unique_callback()
            def OnCancel(btn, touch):
                btn.SetSelect(False)
                btn.lab_content.SetColor(2304360)
                btn.lab_num.SetColor(10723795)

            def click_exchange(btn, touch, idx=idx, sid=shortcut_id):
                if not self.selected_info:
                    global_data.game_mgr.show_tip(860179)
                    return
                shortcut_list.pop(idx)
                replaced_idx = self.selected_info[0]
                replaced_shortcut_id = self._shortcut_list[replaced_idx]
                replaced_shortcut_conf = self._quick_chat_conf[str(replaced_shortcut_id)]
                replaced_type_tid = replaced_shortcut_conf['type_tid']
                self.useable_quick_chat_list.setdefault(replaced_type_tid, []).append(replaced_shortcut_id)
                self._shortcut_list[replaced_idx] = sid
                self.is_modified = True
                self.init_left_list()
                self.init_right_list()
                self.refresh_select_list(type_tid)

            item.btn_replace.BindMethod('OnClick', click_exchange)
            item.btn_chat.BindMethod('OnClick', click_exchange)

    def save_settings(self):
        global_data.player.write_setting_2(uoc.SHORTCUT_ORDER, self._shortcut_list, sync_to_server=True)
        global_data.emgr.quick_shortcut_order_change.emit()

    def on_click_close(self, *args):
        if not self.is_modified:
            self.close()
            return

        def confirm_cb():
            self.save_settings()
            self.close()

        SecondConfirmDlg2().confirm(content=2001, confirm_callback=confirm_cb, cancel_callback=self.close)

    def on_click_sure(self, *args):
        self.save_settings()
        self.close()

    def on_click_reserve(self, *args):
        self._shortcut_list = list(range(7))
        self.selected_info = ()
        self.shown_quick_chat_list = ()
        self.useable_quick_chat_list.clear()
        self.is_modified = True
        self.init_parameters()
        self.init_left_list()
        self.init_right_list()

    def on_click_question(self, *args):
        dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
        dlg.set_show_rule(2293, 860181)