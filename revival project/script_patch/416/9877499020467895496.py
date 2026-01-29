# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathEnemyBaseUI.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
from common.const import uiconst
TICK_HIDE_TAG = 221216

class DeathEnemyBaseUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_tips/tdm_tips/i_tdm_tips_near_enemy_base'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self):
        pass

    def on_finalize_panel(self):
        pass

    def SetInfo(self, info):
        self.panel.lab_2.SetString(''.join([get_text_by_id(81783), str(int(info * 100)), '%']))

    def do_show_panel(self):
        self.stopActionByTag(TICK_HIDE_TAG)
        if not self.panel.isVisible():
            self.panel.PlayAnimation('show')
        super(DeathEnemyBaseUI, self).do_show_panel()

    def do_hide_panel(self):
        self.stopActionByTag(TICK_HIDE_TAG)
        if not self.panel.isVisible():
            super(DeathEnemyBaseUI, self).do_hide_panel()
            return
        max_time = self.panel.GetAnimationMaxRunTime('disappear')

        def _hide():
            super(DeathEnemyBaseUI, self).do_hide_panel()

        self.panel.DelayCallWithTag(max_time, _hide, TICK_HIDE_TAG)
        self.panel.PlayAnimation('disappear')