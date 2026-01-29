# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/ChangeName.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from common.const.uiconst import NORMAL_LAYER_ZORDER, NORMAL_LAYER_ZORDER_3

class ChangeName(WindowSmallBase):
    PANEL_CONFIG_NAME = 'common/change_name'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'panel'

    def on_init_panel(self, *args, **kargs):
        super(ChangeName, self).on_init_panel()
        import logic.comsys.common_ui.InputBox as InputBox

        def send_cb(*args, **kwargs):
            if not self.panel:
                return
            else:
                self.panel.panel.confirm.btn_common_big.OnClick(None)
                return

        self._input_box = InputBox.InputBox(self.panel.panel.inputbox, placeholder=get_text_by_id(2145), send_callback=send_cb)
        self._input_box.set_rise_widget(self.panel)
        from logic.gcommon.item.item_const import ITEM_NO_RENAME_CARD
        card_num = global_data.player.get_item_num_by_no(ITEM_NO_RENAME_CARD)
        self.panel.lab_cost.SetString('%s: %d/%d' % (get_text_by_id(80827), 1, card_num))

        @self.panel.panel.confirm.btn_common_big.callback()
        def OnClick(*args):
            text = self._input_box.get_text()
            if not text:
                return
            if not ui_utils.check_nick_name(text):
                return
            global_data.player.req_change_name(text)

        @self.panel.panel.img_window_bg.btn_close.callback()
        def OnClick(*args):
            self.close()

        global_data.emgr.player_change_name_sucess += self.close

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        global_data.emgr.player_change_name_sucess -= self.close
        return


class ChangeRemarkName(WindowSmallBase):
    PANEL_CONFIG_NAME = 'common/change_name'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    TEMPLATE_NODE_NAME = 'panel'
    GLOBAL_EVENT = {}

    def on_init_panel(self, uid, u_name=None, *args, **kargs):
        super(ChangeRemarkName, self).on_init_panel()
        self.panel.panel.lab_title.SetString(get_text_by_id(610880))
        self.panel.lab_desc.SetString(get_text_by_id(610880))
        self.panel.lab_cost.setVisible(False)
        import logic.comsys.common_ui.InputBox as InputBox

        def send_cb(*args, **kwargs):
            if not self.panel:
                return
            else:
                self.panel.panel.confirm.btn_common_big.OnClick(None)
                return

        self._input_box = InputBox.InputBox(self.panel.panel.inputbox, placeholder=u_name or get_text_by_id(610881), send_callback=send_cb)
        self._input_box.set_rise_widget(self.panel)
        cur_remark = global_data.player._frds_remark.get(int(uid), None)
        if cur_remark:
            self._input_box.set_text(cur_remark)

        @self.panel.panel.confirm.btn_common_big.callback()
        def OnClick(btn, touch):
            text = self._input_box.get_text()
            if not text:
                global_data.player.remark_friend(uid, '')
                self.close()
                return
            if not ui_utils.check_nick_name(text):
                return
            global_data.player.remark_friend(uid, text)
            self.close()

        @self.panel.panel.img_window_bg.btn_close.callback()
        def OnClick(*args):
            self.close()

        global_data.emgr.player_change_name_sucess += self.close
        return

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        global_data.emgr.player_change_name_sucess -= self.close
        return


class ChangeIntimacyName(WindowSmallBase):
    PANEL_CONFIG_NAME = 'common/change_name'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'panel'
    GLOBAL_EVENT = {}

    def on_init_panel(self, uid, *args, **kargs):
        super(ChangeIntimacyName, self).on_init_panel()
        self.panel.panel.lab_title.SetString(get_text_by_id(81201))
        self.panel.lab_desc.SetString(get_text_by_id(81201))
        self.panel.lab_cost.setVisible(False)
        import logic.comsys.common_ui.InputBox as InputBox

        def send_cb(*args, **kwargs):
            if not self.panel:
                return
            else:
                self.panel.panel.confirm.btn_common_big.OnClick(None)
                return

        self._input_box = InputBox.InputBox(self.panel.panel.inputbox, placeholder=get_text_by_id(2145), send_callback=send_cb)
        self._input_box.set_rise_widget(self.panel)

        @self.panel.panel.confirm.btn_common_big.callback()
        def OnClick(btn, touch):
            text = self._input_box.get_text()
            if not text:
                return
            if not ui_utils.check_intimacy_name(text):
                return
            global_data.player.change_intimacy_name(uid, text)
            self.close()

        @self.panel.panel.img_window_bg.btn_close.callback()
        def OnClick(*args):
            self.close()

        global_data.emgr.player_change_name_sucess += self.close

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        global_data.emgr.player_change_name_sucess -= self.close
        return


class ChangeMotto(WindowSmallBase):
    PANEL_CONFIG_NAME = 'common/change_motto'
    TEMPLATE_NODE_NAME = 'panel'
    DLG_ZORDER = NORMAL_LAYER_ZORDER

    def on_init_panel(self, *args, **kargs):
        super(ChangeMotto, self).on_init_panel()
        import logic.comsys.common_ui.InputBox as InputBox
        self._send_callback = kargs.get('send_callback', None)
        placeholder = kargs.get('placeholder', '')
        self._real_input_callback = kargs.get('input_callback', None)
        self._max_length = kargs.get('max_length', None)
        self._init_text = kargs.get('init_text', '')
        self._input_box = InputBox.InputBox(self.panel.panel.inputbox, placeholder=placeholder, input_callback=self._real_input_callback, max_length=self._max_length)
        self._input_box.set_rise_widget(self.panel)
        self._input_box.set_text(self._init_text)

        @self.panel.panel.confirm.btn_common_big.callback()
        def OnClick(*args):
            text = self._input_box.get_text()
            if self._send_callback:
                self._send_callback(text)
            self.close()

        @self.panel.panel.img_window_bg.btn_close.callback()
        def OnClick(*args):
            self.close()

        global_data.emgr.player_change_name_sucess += self.close
        return

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        global_data.emgr.player_change_name_sucess -= self.close
        return


class ChangeNameV2(WindowSmallBase):
    PANEL_CONFIG_NAME = 'setting/setting_highlight/i_rename'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    TEMPLATE_NODE_NAME = 'panel'

    def on_init_panel(self, *args, **kargs):
        super(ChangeNameV2, self).on_init_panel()
        self._send_callback = kargs.get('send_callback', None)
        lab_title_txt = kargs.get('lab_title', 3123)
        self.panel.panel.lab_title.SetString(lab_title_txt)
        btn_txt = kargs.get('btn_txt', 19001)
        if isinstance(btn_txt, int):
            btn_txt = get_text_by_id(btn_txt)
        self.panel.panel.confirm.btn_common_big.SetText(btn_txt)
        lab_subtitle_txt = kargs.get('lab_sub_title', 3124)
        self.panel.lab_subtitle.SetString(lab_subtitle_txt)
        import logic.comsys.common_ui.InputBox as InputBox
        self._input_box = InputBox.InputBox(self.panel.panel.inputbox, max_length=20)
        self._input_box.set_rise_widget(self.panel)

        @self.panel.panel.confirm.btn_common_big.callback()
        def OnClick(btn, touch):
            text = self._input_box.get_text()
            if not text:
                return
            from logic.gcommon.common_utils.text_utils import check_review_words
            flag, msg = check_review_words(text)
            if not flag:
                global_data.game_mgr.show_tip(get_text_by_id(3146))
                return
            if self._send_callback:
                self._send_callback(msg)
            self.close()

        return


class ChangeRoomPlayerName(WindowSmallBase):
    PANEL_CONFIG_NAME = 'common/change_name'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'panel'

    def on_init_panel(self, *args, **kargs):
        super(ChangeRoomPlayerName, self).on_init_panel()
        self.target_uid = kargs.get('target_uid', None)
        self.init_input_widget()
        self.init_btns()
        self.panel.lab_cost.setVisible(False)
        return

    def init_input_widget(self):
        import logic.comsys.common_ui.InputBox as InputBox

        def send_cb(*args, **kwargs):
            if not self.panel:
                return
            else:
                self.panel.panel.confirm.btn_common_big.OnClick(None)
                return

        self._input_box = InputBox.InputBox(self.panel.panel.inputbox, placeholder=get_text_by_id(2145), send_callback=send_cb)
        self._input_box.set_rise_widget(self.panel)

    def init_btns(self):

        @self.panel.panel.confirm.btn_common_big.callback()
        def OnClick(*args):
            text = self._input_box.get_text()
            if not text:
                return
            if not ui_utils.check_nick_name(text):
                return
            if not self.target_uid:
                return
            global_data.player.req_set_char_name_in_room(self.target_uid, text)
            self.close()

        @self.panel.panel.img_window_bg.btn_close.callback()
        def OnClick(*args):
            self.close()

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        return


class ChangeRoomTeamName(WindowSmallBase):
    PANEL_CONFIG_NAME = 'room/change_teamname'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'panel'

    def on_init_panel(self, *args, **kwargs):
        super(ChangeRoomTeamName, self).on_init_panel()
        self.team_idx = kwargs.get('team_idx', 0)
        self.init_input_widget()
        self.init_btns()

    def init_input_widget(self):
        import logic.comsys.common_ui.InputBox as InputBox

        def send_cb(*args, **kwargs):
            if not self.panel:
                return
            else:
                self.panel.panel.confirm.btn_common_big.OnClick(None)
                return

        self._input_box = InputBox.InputBox(self.panel.panel.inputbox, placeholder=get_text_by_id(2145), send_callback=send_cb)
        self._input_box.set_rise_widget(self.panel)

    def init_btns(self):

        @self.panel.panel.confirm.btn_common_big.callback()
        def OnClick(*args):
            text = self._input_box.get_text()
            if not text:
                return
            if not ui_utils.check_nick_name(text):
                return
            if not self.team_idx:
                return
            global_data.player.set_competition_team_name(self.team_idx, text)
            self.close()

        @self.panel.panel.img_window_bg.btn_close.callback()
        def OnClick(*args):
            self.close()

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        return