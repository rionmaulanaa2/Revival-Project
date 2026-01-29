# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/GameVoiceTextUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
import cc
from common.cfg import confmgr
from common.const import uiconst

class GameVoiceTextUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_human_voice'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.cur_text = ''
        self._play_voice_end = False
        self.move_action = False

    def on_finalize_panel(self):
        pass

    def show_text(self, txt):
        if self.cur_text == txt:
            return
        self._play_voice_end = False
        self.panel.lab_voice.SetString(txt)
        role_id = global_data.player.logic.ev_g_role_id()
        role_data = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id))
        pic_url = role_data.get('icon')
        old_cap = self.panel.img_role.getCapInsets()
        self.panel.img_role.SetDisplayFrameByPath('', pic_url)
        self.panel.img_role.setCapInsets(old_cap)
        lab_voice_width, _ = self.lab_voice.GetContentSize()
        lab_container_width, _ = self.lab_container.GetContentSize()
        if lab_voice_width > lab_container_width:
            fixed_x = lab_container_width - lab_voice_width
            move_time = abs(fixed_x) / 100
            self.move_action = True

            def _move_callback():
                self.move_action = False
                self.try_close()

            self.lab_voice.runAction(cc.Sequence.create([
             cc.DelayTime.create(1.0),
             cc.MoveTo.create(move_time, cc.Vec2(fixed_x, self.lab_voice.getPositionY())),
             cc.CallFunc.create(_move_callback)]))

    def play_voice_end(self):
        self._play_voice_end = True
        self.try_close()

    def try_close(self):
        if not self.move_action and self._play_voice_end:
            self.close()