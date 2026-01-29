# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/ChatPigeon.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import time
import common.const.uiconst
from cocosui import cc, ccui, ccs
from common.const.property_const import *
from common.cfg import confmgr
import common.utils.timer as timer
from common.const.property_const import *
from common.uisys.uielment.CCRichText import CCRichText
from logic.gcommon.common_utils.local_text import get_server_text
DEFAULT_FONTSIZE = 24
from common.const import uiconst

class ChatPigeon(BasePanel):
    DLG_ZORDER = common.const.uiconst.TOP_MSG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'chat/chat_pigeon'
    UI_TYPE = common.const.uiconst.UI_TYPE_MESSAGE

    def on_init_panel(self, *args, **kargs):
        self.panel.nd_root.setVisible(False)
        self._bottom_size = self.panel.img_bg.getContentSize()
        self.item_data = global_data.uisystem.load_template('chat/chat_pigeon_item')
        self._pigoen_msg = global_data.message_data.get_pigoen_data()
        self._timer = global_data.game_mgr.register_logic_timer(self.check_tick, interval=2, times=-1, mode=timer.LOGIC)
        self._show_count = 0
        self._last_msg = None
        self._last_msg_width = 0
        return

    def add_msg(self):
        self._show_count += 1
        self.panel.nd_root.setVisible(True)
        data = self._pigoen_msg[0]
        del self._pigoen_msg[0]
        item_panel = global_data.uisystem.create_item(self.item_data, self.panel.nd_root)
        pos = item_panel.img_icon.getPosition()
        pos = cc.Vec2(pos.x + 10, pos.y + 8)
        sender_info = data.get('sender_info', None)
        if sender_info:
            msg = '[%s]%s' % (sender_info[C_NAME], get_server_text(data['msg']))
            rt_msg = CCRichText.Create(msg, DEFAULT_FONTSIZE, cc.Size(1800, 50))
        else:
            rt_msg = CCRichText.Create(get_server_text(data['msg']), DEFAULT_FONTSIZE, cc.Size(1800, 50))
        rt_msg.formatText()
        if len(rt_msg.getLineWidths()) > 1:
            rt_msg = CCRichText.Create(msg, DEFAULT_FONTSIZE, cc.Size(3000, 50))
            rt_msg.formatText()
        rt_msg.setAnchorPoint(cc.Vec2(0.0, 0.0))
        rt_msg.setPosition(pos)
        item_panel.AddChild(None, rt_msg)
        width = rt_msg.getLineWidths()[0] + pos.x
        item_panel.setPosition(cc.Vec2(0 + self._bottom_size.width, 4))
        time = (width + self._bottom_size.width) / 100.0
        act0 = cc.MoveBy.create(time, cc.Vec2(-(width + self._bottom_size.width), 0))

        def callback():
            if item_panel == self._last_msg:
                self._last_msg = None
            item_panel.Destroy()
            self._show_count -= 1
            if self._show_count <= 0:
                self.panel.nd_root.setVisible(False)
            return

        act1 = cc.CallFunc.create(callback)
        act2 = cc.Sequence.create([act0, act1])
        item_panel.runAction(act2)
        self._last_msg = item_panel
        self._last_msg_width = width
        return

    def check_tick(self):
        if self._pigoen_msg:
            if self._last_msg and self._last_msg.getPosition().x + self._last_msg_width < self._bottom_size.width - 100 or not self._last_msg:
                self.add_msg()

    def on_finalize_panel(self):
        global_data.game_mgr.unregister_logic_timer(self._timer)