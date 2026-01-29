# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/veteran/PCVeteranUI.py
from __future__ import absolute_import
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const import uiconst
from logic.gcommon.const import SERVER_SEA_STEAM, SERVER_EA_STEAM
import logic.comsys.common_ui.InputBox as InputBox

class PCVeteranUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/tips_return_pc'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {'btn_cancel.btn_common_big.OnClick': 'close',
       'btn_go.btn_common_big.OnClick': 'confirm',
       'nd_content.btn_mode.OnClick': 'on_click_mode',
       'nd_content.mode_list.nd_close.OnClick': 'close_mode_list'
       }
    GLOBAL_EVENT = {}

    def on_init_panel(self, *args):
        self.server_host = 0
        self.server_list = global_data.player.get_steam_host_list()
        self.server_text = {SERVER_SEA_STEAM: 120010,
           SERVER_EA_STEAM: 120011
           }
        self._lock = False
        self.init_widget()

    def on_finalize_panel(self):
        pass

    def init_widget(self):
        self.panel.list_content.SetInitCount(1)
        item = self.panel.list_content.GetItem(0)
        item.lab_describe.formatText()
        size = item.lab_describe.GetTextContentSize()
        item.SetContentSize(size.width, size.height + 20)
        item.RecursionReConfPosition()
        self.panel.list_content.GetContainer()._refreshItemPos()
        self.panel.list_content.SetInitCount(1)
        opt_list = self.panel.nd_content.mode_list.option_list
        opt_list.SetInitCount(len(self.server_list))
        for i, host_num in enumerate(self.server_list):
            item = opt_list.GetItem(i)
            item.button.SetText(self.server_text.get(host_num, str(host_num)))
            item.button.BindMethod('OnClick', lambda b, t, host=host_num: self.select_server(host))

        self.input_box = InputBox.InputBox(self.panel.input_box, max_length=20, placeholder=906558)
        self.check_has_bind()

    def select_server(self, host_num):
        self.server_host = host_num
        self.panel.nd_content.btn_mode.SetText(self.server_text.get(host_num, str(host_num)))
        self.close_mode_list()

    def confirm(self, *args):
        veteran_info = global_data.player.get_steam_return_info()
        if not veteran_info:
            self.confirm_name()
        else:
            ui = global_data.ui_mgr.show_ui('PCVeteranSuccessUI', 'logic.comsys.veteran')
            ui and ui.set_confirm_info(veteran_info)
            global_data.player.request_return_to_steam_again()

    def confirm_name(self, *args):
        if self._lock:
            return
        host = self.server_host
        if not host:
            return
        uid = self.input_box.get_text()
        try:
            uid = int(uid)
        except:
            global_data.game_mgr.show_tip(get_text_by_id(906549))
            return

        if not global_data.player.query_steam_char_name(host, uid):
            global_data.game_mgr.show_tip(get_text_by_id(15815))
            return
        self._lock = True
        global_data.ui_mgr.show_ui('PCVeteranConfirmUI', 'logic.comsys.veteran')

    def on_click_mode(self, *args):
        self.panel.nd_content.mode_list.setVisible(True)

    def close_mode_list(self, *args):
        self.panel.nd_content.mode_list.setVisible(False)

    def unlock(self):
        self._lock = False

    def check_has_bind(self):
        veteran_info = global_data.player.get_steam_return_info()
        if veteran_info:
            self.input_box.set_text(str(veteran_info.get('uid', 0)))
            self.input_box.enable_input(False)
            self.select_server(int(veteran_info.get('host', 0)))
            self.panel.nd_content.btn_mode.SetEnable(False)
            self.panel.btn_go.btn_common_big.SetEnable(False)
            self.panel.btn_go.btn_common_big.SetText(81024)
            global_data.player.request_return_to_steam_again()