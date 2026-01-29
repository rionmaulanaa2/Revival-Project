# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/ChatReply.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst
from cocosui import cc, ccui, ccs
from logic.client.const import emote_const
from common.cfg import confmgr
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gutils.mall_utils import item_has_owned_by_item_no
from logic.gutils.item_utils import get_lobby_item_left_time
from logic.gcommon import time_utility as tutil
from logic.gcommon.item.item_const import DEFAULT_EMOTE_PACK
from logic.gutils.chat_utils import check_has_split_emote, filter_split_emote, get_all_split_emote
NUM_PER_PAGE = 39
NUM_PER_BIG_PAGE = 8
TURN_FACTOR = 0.1
from common.const import uiconst

class ChatReply(BasePanel):
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CUSTOM
    PANEL_CONFIG_NAME = 'chat/chat_reply'

    def on_init_panel(self, *args, **kargs):
        super(ChatReply, self).on_init_panel()
        self.close_callback = None
        self._input_box = None

        @self.panel.nd_close.callback()
        def OnClick(*args):
            self.panel.SetTimeOut(0.001, self.close)

        reply_text_list = confmgr.get('lobby_team_quick_chat', 'content', default=[])
        self.panel.list_item.SetInitCount(len(reply_text_list))
        for idx, text_id in enumerate(reply_text_list):
            text_id = int(text_id)
            item = self.panel.list_item.GetItem(idx)
            item.lab_content.SetString(text_id)
            item.BindMethod('OnClick', lambda btn, touch, txt=text_id: self.on_click_text(txt))

        return

    def on_click_text(self, text_id):
        self._input_box.set_text(get_text_by_id(text_id))

    def set_input_box(self, input_box):
        self._input_box = input_box

    def get_bg_height(self):
        pos = self.panel.img_bg.getPosition()
        return self.panel.img_bg.getContentSize().height + pos.y

    def set_close_callback(self, callback):
        self.close_callback = callback

    def on_finalize_panel(self):
        if self.close_callback:
            self.close_callback()
        super(ChatReply, self).on_finalize_panel()