# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/PreviewEmoteList.py
from __future__ import absolute_import
import common.utilities
from common.cfg import confmgr
from common.const import uiconst
from common.utils.cocos_utils import ccp
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
import logic.gcommon.const as const
from logic.gcommon.common_utils.local_text import get_text_by_id
from cocosui import cc, ccui, ccs

class PreviewEmoteList(BasePanel):
    PANEL_CONFIG_NAME = 'charge/charge_month_emote'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_bg.btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self, *args, **kargs):
        self.emote_key = kargs.get('emote_key', '')
        self._emote_dict = confmgr.get('emote', 'emote')
        self._emote_list = confmgr.get('emote', 'emote_list', self.emote_key, default=[])
        self._all_emotes_info = confmgr.get('chat_all_emotes', default={})
        self.show_emote_list()

    def on_click_close_btn(self, *args):
        self.close()

    def on_login_reconnect(self, *args):
        self.close()

    def show_emote_list(self):
        count = len(self._emote_list)
        self.panel.emote_list.SetInitCount(count)
        for i, no in enumerate(self._emote_list):
            item = self.panel.emote_list.GetItem(i)
            s = self._emote_dict[str(no)]
            begin = s.find('=')
            end = s.find(',')
            filename = s[begin + 1:end] + '0000.png'
            item.img_item.setSpriteFrame(filename)
            item.lab_name.SetColor('#DK')
            item.lab_name.SetString(get_text_by_id(self._all_emotes_info.get(str(no), {}).get('iTxtId')))