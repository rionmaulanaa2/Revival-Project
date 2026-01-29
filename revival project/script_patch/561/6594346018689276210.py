# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanApplyJoinUI.py
from __future__ import absolute_import
import common.const.uiconst
import cc
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.gcommon.common_utils.ui_gameplay_utils import check_clan_name
from common.cfg import confmgr
import logic.comsys.common_ui.InputBox as InputBox
from logic.gcommon.common_utils.text_utils import check_review_words

class ClanApplyJoinUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'crew/open_crew_apply'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'panel'

    def on_init_panel(self, *args, **kargs):
        super(ClanApplyJoinUI, self).on_init_panel()
        self.init_conf()
        self.init_inputbox()
        self.init_text()
        self.init_button()
        self.init_parameters()

    def init_conf(self):
        self.avt_request_limit = confmgr.get('clan_data', 'avt_request_limit')

    def init_inputbox(self):
        self.temp_inputbox = InputBox.InputBox(self.panel.pnl_bg.temp_inputbox, max_length=self.avt_request_limit, input_callback=self.input_cb, placeholder=get_text_by_id(0), start_input_cb=self.start_input_cb, need_sp_length_func=True)
        self.temp_inputbox.set_rise_widget(self.panel)
        self.temp_inputbox._input_box.setTextVerticalAlignment(cc.TEXTVALIGNMENT_TOP)

    def init_text(self):
        self.panel.pnl_bg.lab_num_limit.SetString('%s/%s' % ('0', str(self.avt_request_limit)))

    def init_parameters(self):
        self.clan_id_list = []
        self.apply_cb = None
        return

    def init_button(self):

        @self.panel.pnl_bg.temp_btn_2.btn_common.callback()
        def OnClick(*args):
            request_data = {}
            request_content = self.temp_inputbox.get_text()
            if not request_content:
                request_content = get_text_by_id(358)
            input_text_len = self.temp_inputbox.get_text_len(request_content)
            request_data['request_content'] = request_content
            if input_text_len > self.avt_request_limit:
                global_data.game_mgr.show_tip(get_text_by_id(82192), True)
                return
            if not request_content:
                request_content = ''
            else:
                flag, request_content = check_review_words(request_content)
                if not flag:
                    global_data.game_mgr.show_tip(get_text_by_id(10045), True)
                    return
            if global_data.player:
                global_data.player.request_join_clan(self.clan_id_list, request_data)
            if self.apply_cb:
                self.apply_cb()
            self.close()

        @self.panel.callback()
        def OnClick(*args):
            if not self.temp_inputbox.get_text():
                self.pnl_bg.temp_inputbox.lab_default.setVisible(True)

        @self.panel.pnl_bg.btn_close.callback()
        def OnClick(*args):
            if self.apply_cb:
                self.apply_cb()
            self.close()

        @self.panel.pnl_bg.temp_btn_1.btn_common.callback()
        def OnClick(*args):
            if self.apply_cb:
                self.apply_cb()
            self.close()

        global_data.emgr.clan_mod_name += self.close

    def input_cb(self, text):
        self.change_limit_num(text)

    def start_input_cb(self):
        self.hide_note()

    def hide_note(self):
        self.pnl_bg.temp_inputbox.lab_default.setVisible(False)

    def change_limit_num(self, text):
        input_text_len = self.temp_inputbox.get_text_len(text)
        str_text_len = str(input_text_len)
        if input_text_len > self.avt_request_limit:
            str_text_len = '#SR' + str_text_len + '#n'
        self.panel.pnl_bg.lab_num_limit.SetString('%s/%s' % (str_text_len, str(self.avt_request_limit)))

    def set_clan_id_list(self, clan_id_list):
        self.clan_id_list = clan_id_list

    def set_apply_cb(self, cb):
        self.apply_cb = cb

    def on_finalize_panel(self):
        if self.temp_inputbox:
            self.temp_inputbox.destroy()
            self.temp_inputbox = None
        self.clan_id_list = []
        global_data.emgr.clan_mod_name -= self.close
        return