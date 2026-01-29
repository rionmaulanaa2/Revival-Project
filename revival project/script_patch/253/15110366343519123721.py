# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Crystal/CrystalBattleHintUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT, UI_TYPE_MESSAGE
from logic.gutils.judge_utils import get_player_group_id
CRYSTAL_DIE_TEXT_ID_SELF = [
 17330,
 17331,
 17332]
CRYSTAL_DIE_TEXT_ID_OTHER = [
 17327,
 17328,
 17329]

class CrystalBattleHintUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_crystal/crystal_hint_ui'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_MESSAGE
    GLOBAL_EVENT = {'show_crystal_hit_hint_event': 'show_crystal_hit_hint',
       'show_crystal_destroy_hint_event': 'show_crystal_destroy_hint',
       'show_crystal_die_hint_event': 'show_crystal_die_hint',
       'death_begin_count_down_over': 'show_crystal_start_hint'
       }

    def on_init_panel(self, *args, **kwargs):
        self.panel.nd_tip_hit.setVisible(False)
        self.panel.nd_tip_destroy.setVisible(False)
        self.panel.nd_tip_start.setVisible(False)
        self.panel.nd_tip_hit.RecordAnimationNodeState('show')
        self.panel.nd_tip_hit.RecordAnimationNodeState('disappear')
        self.panel.nd_tip_destroy.RecordAnimationNodeState('show')
        self.panel.nd_tip_destroy.RecordAnimationNodeState('disappear')
        self.panel.nd_tip_start.RecordAnimationNodeState('break')
        self.panel.nd_tip_start.RecordAnimationNodeState('break_out')
        self.panel.nd_tip_die_other.RecordAnimationNodeState('show')
        self.panel.nd_tip_die_other.RecordAnimationNodeState('disappear')
        self.panel.nd_tip_die_self.RecordAnimationNodeState('show')
        self.panel.nd_tip_die_self.RecordAnimationNodeState('disappear')

    def show_crystal_hit_hint(self):
        if self.panel.nd_tip_hit.IsPlayingAnimation('show'):
            return
        if self.panel.nd_tip_hit.IsPlayingAnimation('disappear'):
            return
        self.panel.nd_tip_hit.RecoverAnimationNodeState('show')
        self.panel.nd_tip_hit.RecoverAnimationNodeState('disappear')
        self.panel.nd_tip_hit.setVisible(True)
        self.panel.nd_tip_hit.PlayAnimation('show')

        def hide():
            self.panel.nd_tip_hit.PlayAnimation('disappear')

        self.panel.SetTimeOut(3, hide)
        self.panel.nd_tip_start.setVisible(False)

    def show_crystal_destroy_hint(self, crystal_group_id):
        if crystal_group_id == get_player_group_id():
            return
        if self.panel.nd_tip_destroy.IsPlayingAnimation('show'):
            return
        if self.panel.nd_tip_destroy.IsPlayingAnimation('disappear'):
            return
        self.panel.nd_tip_destroy.RecoverAnimationNodeState('show')
        self.panel.nd_tip_destroy.RecoverAnimationNodeState('disappear')
        self.panel.nd_tip_destroy.setVisible(True)
        self.panel.nd_tip_destroy.PlayAnimation('show')

        def hide():
            self.panel.nd_tip_destroy.PlayAnimation('disappear')

        self.panel.SetTimeOut(3, hide)

    def show_crystal_start_hint(self):
        self.panel.nd_tip_start.setVisible(True)
        self.panel.nd_tip_start.PlayAnimation('break')

        def hide():
            self.panel.nd_tip_start.PlayAnimation('break_out')

        self.panel.SetTimeOut(3, hide)

    def show_crystal_die_hint(self, crystal_group_id, crystal_round):
        if crystal_group_id == get_player_group_id():
            self.show_crystal_die_self(crystal_round)
        else:
            self.show_crystal_die_other(crystal_round)

    def show_crystal_die_self(self, crystal_round):
        if self.panel.nd_tip_die_self.IsPlayingAnimation('show'):
            return
        if self.panel.nd_tip_die_self.IsPlayingAnimation('disappear'):
            return
        if crystal_round < 0 or crystal_round >= len(CRYSTAL_DIE_TEXT_ID_SELF):
            return
        text_id = CRYSTAL_DIE_TEXT_ID_SELF[crystal_round]
        self.panel.nd_tip_die_self.lab_1.SetString(text_id)
        self.panel.nd_tip_die_self.RecoverAnimationNodeState('show')
        self.panel.nd_tip_die_self.RecoverAnimationNodeState('disappear')
        self.panel.nd_tip_die_self.setVisible(True)
        self.panel.nd_tip_die_self.PlayAnimation('show')

        def hide():
            self.panel.nd_tip_die_self.PlayAnimation('disappear')

        self.panel.SetTimeOut(3, hide)

    def show_crystal_die_other(self, crystal_round):
        if self.panel.nd_tip_die_other.IsPlayingAnimation('show'):
            return
        if self.panel.nd_tip_die_other.IsPlayingAnimation('disappear'):
            return
        if crystal_round < 0 or crystal_round >= len(CRYSTAL_DIE_TEXT_ID_OTHER):
            return
        text_id = CRYSTAL_DIE_TEXT_ID_OTHER[crystal_round]
        self.panel.nd_tip_die_other.lab_1.SetString(text_id)
        self.panel.nd_tip_die_other.RecoverAnimationNodeState('show')
        self.panel.nd_tip_die_other.RecoverAnimationNodeState('disappear')
        self.panel.nd_tip_die_other.setVisible(True)
        self.panel.nd_tip_die_other.PlayAnimation('show')

        def hide():
            self.panel.nd_tip_die_other.PlayAnimation('disappear')

        self.panel.SetTimeOut(3, hide)