# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/BegChatUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
import common.const.uiconst
from common.const import uiconst
from common.cfg import confmgr

class BegChatUI(BasePanel):
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    SEND_CD = 5.0
    PANEL_CONFIG_NAME = 'battle/fight_chat_down'
    UI_ACTION_EVENT = {'bg_layer.OnBegin': 'on_bg_layer_begin'
       }

    def on_init_panel(self, *args, **kargs):
        self._is_chat_open = False
        self.update_cur_quick_list()

    def on_finalize_panel(self):
        pass

    def chat_open(self):
        self.panel.setVisible(True)

    def chat_close(self):
        self.panel.setVisible(False)
        global_data.emgr.show_sos_btn_event.emit()

    def update_cur_quick_list(self):
        beg_text_list = self.get_show_beg_text_list()
        self.panel.lv_chat_list.SetInitCount(len(beg_text_list))
        for idx, (shortcut_id, tid) in enumerate(beg_text_list):
            ui_item = self.panel.lv_chat_list.GetItem(idx)
            self.init_quick_item(ui_item, tid, shortcut_id)

    def init_quick_item(self, ui_item, text_id, shortcut_id):
        ui_item.lab_content.SetString(text_id)

        @ui_item.btn_chat.unique_callback()
        def OnClick(btn, touch, shortcut_id=shortcut_id):
            self.chat_close()
            if not global_data.player:
                return
            tid = self.get_tid_by_shortcut_id(shortcut_id)
            voice_trigger_type = self.get_voice_trigger_type_by_shortcut_id(shortcut_id)
            pity_msg = {}
            if tid:
                pity_msg['text_id'] = tid
            if voice_trigger_type:
                pity_msg['voice_trigger_type'] = voice_trigger_type
            if pity_msg and global_data.cam_lplayer:
                global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', 'send_pity_msg', (pity_msg,), True)
                global_data.cam_lplayer.send_event('E_SHOW_PITY_MSG', pity_msg)

    def on_bg_layer_begin(self, btn, touch):
        self.chat_close()

    def get_show_beg_text_list(self):
        conf = confmgr.get('down_quick_chat', '0')
        return [ (shortcut_id, conf[str(shortcut_id)]['ui_text_id']) for shortcut_id in conf['pity_text_order']
               ]

    def get_tid_by_shortcut_id(self, shortcut_id):
        role_id = global_data.player.get_role()
        text_id = confmgr.get('down_quick_chat', str(role_id), str(shortcut_id), 'text_id', default=None)
        if text_id:
            return text_id
        else:
            return confmgr.get('down_quick_chat', '0', str(shortcut_id), 'text_id', default=None)

    def get_voice_trigger_type_by_shortcut_id(self, shortcut_id):
        conf = None
        if global_data.player:
            role_id = global_data.player.get_role()
            conf = confmgr.get('down_quick_chat', str(role_id), default=None)
        if conf is None:
            conf = confmgr.get('down_quick_chat', '0')
        shortcut_conf = conf.get(str(shortcut_id))
        if not shortcut_conf:
            return
        else:
            return shortcut_conf.get('trigger_type')