# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVESuggestReplyUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CUSTOM, UI_TYPE_MESSAGE
from logic.gutils.role_head_utils import init_role_head
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr

class PVESuggestReplyUI(BasePanel):
    PANEL_CONFIG_NAME = 'home_system/open_home_system_reply'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'pnl_bg.btn_close.OnClick': '_on_click_back'
       }

    def on_init_panel(self, sheet_id, suggest_id, *args, **kwargs):
        super(PVESuggestReplyUI, self).on_init_panel()
        self._init_params(sheet_id, suggest_id)
        self._init_ui()
        self.process_events(True)

    def _init_params(self, sheet_id, suggest_id):
        self._sheet_id = sheet_id
        self._suggest_id = suggest_id
        self._conf = confmgr.get('pve_suggest_conf', 'SuggestConf', 'Content', self._suggest_id)
        self._suggest_item = None
        return

    def _init_ui(self):
        self.panel.temp_btn_1.setVisible(False)
        self.panel.lab_title.setString(get_text_by_id(860312))
        self._list_item = self.panel.list_item
        self._init_list_item()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_do_like_pve_suggest': self.on_do_like_pve_suggest
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def _init_list_item(self):
        self.panel.list_item.RecycleAllItem()
        self._init_suggest_item()
        self._init_reply_item()

    def _init_suggest_item(self):
        self._suggest_item = self._list_item.AddItem(global_data.uisystem.load_template('home_system/i_home_system_reply_item'))
        pnl_bg = self._suggest_item.pnl_bg
        list_icon = pnl_bg.lab_like.nd_auto_fit.list_icon
        pnl_bg.lab_time.setVisible(False)
        pnl_bg.bar_praise.setVisible(False)
        pnl_bg.btn_report.setVisible(False)
        list_icon.GetItem(0).setVisible(False)
        pnl_bg.lab_name.setString(get_text_by_id(self._conf.get('suggest_player_name')))
        frame_item_no = self._conf.get('suggest_frame_no')
        photo_no = self._conf.get('suggest_photo_no')
        init_role_head(pnl_bg.temp_head, frame_item_no, photo_no)
        pnl_bg.lab_content.setString(get_text_by_id(self._conf.get('suggest_text_id')))
        self._update_suggest_like()
        like_item = list_icon.GetItem(1)
        btn_icon = like_item.btn_icon
        btn_icon.EnableCustomState(True)

        @btn_icon.callback()
        def OnClick(btn, touch):
            is_like = global_data.player.get_pve_suggest_is_like(self._sheet_id, self._suggest_id)
            if not is_like:
                global_data.player.do_like_pve_suggest(self._sheet_id, self._suggest_id)

    def _init_reply_item(self):
        item = self._list_item.AddItem(global_data.uisystem.load_template('home_system/i_home_system_reply_item2'))
        pnl_bg = item.pnl_bg
        lab_name = pnl_bg.lab_name
        lab_name.nd_auto_fit.setVisible(False)
        pnl_bg.lab_time.setVisible(False)
        pnl_bg.btn_report.setVisible(False)
        pnl_bg.lab_like.setVisible(False)
        lab_name.setString(get_text_by_id(self._conf.get('reply_player_name')))
        frame_item_no = self._conf.get('reply_frame_no')
        photo_no = self._conf.get('reply_photo_no')
        init_role_head(pnl_bg.temp_head, frame_item_no, photo_no)
        pnl_bg.lab_content.setString(get_text_by_id(self._conf.get('reply_text_id')))

    def _update_suggest_like(self):
        pnl_bg = self._suggest_item.pnl_bg
        lab_like = pnl_bg.lab_like
        lab_like.setString(str(global_data.player.get_pve_suggest_like_count(self._suggest_id)))
        list_icon = lab_like.nd_auto_fit.list_icon
        like_item = list_icon.GetItem(1)
        is_like = global_data.player.get_pve_suggest_is_like(self._sheet_id, self._suggest_id)
        like_item.btn_icon.SetSelect(is_like)

    def on_do_like_pve_suggest(self, sheet_id, suggest_id):
        if self._sheet_id == sheet_id and self._suggest_id == suggest_id:
            self._update_suggest_like()

    def _on_click_back(self, *args):
        self.close()

    def on_finalize_panel(self):
        self.process_events(False)
        super(PVESuggestReplyUI, self).on_finalize_panel()
        self._sheet_id = None
        self._suggest_id = None
        self._conf = None
        self._list_item = None
        self._suggest_item = None
        return