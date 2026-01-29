# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/NewChatPigeon.py
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
from logic.gcommon.const import PRIV_SHOW_COLORFUL_FONT
from logic.gcommon.cdata.privilege_data import COLOR_FONT
from logic.gcommon.common_const.chat_const import PIGEON_NORMAL
DEFAULT_FONTSIZE = 24
from common.const import uiconst

class NewChatPigeon(BasePanel):
    DLG_ZORDER = common.const.uiconst.TOP_MSG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'common/speaker_tips'
    UI_TYPE = common.const.uiconst.UI_TYPE_MESSAGE

    def on_init_panel(self, *args, **kargs):
        self._clip_size = self.panel.nd_clip.getContentSize()
        self._pigoen_msg = global_data.message_data.get_pigoen_data()
        self._timer = global_data.game_mgr.register_logic_timer(self.check_tick, interval=1, times=-1, mode=timer.CLOCK)
        self.hide()
        self._is_showing_msg = False
        self.pass_time = 0
        self._pigeon_type = PIGEON_NORMAL

        @self.panel.nd_click.callback()
        def OnClick(*args):
            from logic.gutils.jump_to_ui_utils import jump_to_lobby_chat
            from logic.comsys.chat.MainChat import UI_PIGEON_INDEX
            return jump_to_lobby_chat(UI_PIGEON_INDEX)

    def add_msg(self):
        self._is_showing_msg = True
        data = self._pigoen_msg[0]
        del self._pigoen_msg[0]
        self._pigeon_type = data.get('pigeon_type', PIGEON_NORMAL)
        if not data.get('not_show_pigoen', False):
            self.show()
            self.panel.PlayAnimation('show')
            sender_info = data.get('sender_info', None)
            if sender_info:
                priv_data = sender_info.get('privilege', {})
                priv_settings = priv_data.get('priv_settings', {})
                priv_colorful_font = priv_data.get('priv_colorful_font', False)
                if priv_colorful_font and priv_settings.get(PRIV_SHOW_COLORFUL_FONT, False):
                    self.panel.lab_speaker.SetColor(COLOR_FONT)
                else:
                    self.panel.lab_speaker.SetColor(16777215)
                self.panel.lab_name.SetString('[%s]:' % sender_info[C_NAME])
                self.panel.lab_speaker.SetString(get_server_text(data['msg']))
            else:
                self.panel.lab_name.SetString('')
                self.panel.lab_speaker.SetString(get_server_text(data['msg']))
            self.panel.lab_speaker.formatText()
            self.panel.lab_name.SetPosition(401, '50%')
            name_text_size = self.panel.lab_name.getTextContentSize()
            msg_text_size = self.panel.lab_speaker.getTextContentSize()
            text_width = name_text_size.width + msg_text_size.width
            len_off = text_width - self._clip_size.width
            if len_off < 0:
                x_off = -self._clip_size.width
                time = self._clip_size.width / 70.0
            else:
                x_off = -text_width
                time = text_width / 70.0
            if time > 0:
                self.panel.lab_name.runAction(cc.Sequence.create([cc.MoveBy.create(time, cc.Vec2(x_off, 0))]))
                self.pass_time -= time
        else:
            self.pass_time = 0
        global_data.emgr.show_top_chat_pigeon.emit(True, data)
        return

    def end_last_msg(self):
        self.panel.PlayAnimation('disappear')
        delay = self.panel.GetAnimationMaxRunTime('disappear')
        global_data.emgr.show_top_chat_pigeon.emit(False, {'pigeon_type': self._pigeon_type})

        def _hide():
            self.hide()
            self._is_showing_msg = False
            self.pass_time = 0

        self.panel.lab_speaker.SetTimeOut(delay, _hide)

    def check_tick(self):
        if self._is_showing_msg:
            self.pass_time += 1
        if self._pigoen_msg:
            if self.pass_time >= 1:
                self.end_last_msg()
            elif not self._is_showing_msg:
                self.add_msg()
        elif self.pass_time >= 4:
            self.end_last_msg()

    def on_finalize_panel(self):
        global_data.game_mgr.unregister_logic_timer(self._timer)