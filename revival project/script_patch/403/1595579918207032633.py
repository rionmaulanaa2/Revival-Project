# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/BattleMvpUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import SMALL_MAP_ZORDER
from common.uisys.basepanel import BasePanel
from common.const import uiconst

class BattleMvpUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_tdm/fight_mvp_tdm'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    TAG = 220927

    def on_init_panel(self, *args, **kwargs):
        self.panel.RecordAnimationNodeState('show')
        self.panel.RecordAnimationNodeState('disappear')
        self.play_animation()
        from logic.client.const import game_mode_const
        game_mode_to_ani = {tuple(game_mode_const.GAME_MODE_DEATHS): 'tdm',
           game_mode_const.GAME_MODE_GVG: 'gvg',
           game_mode_const.GAME_MODE_FFA: 'ffa',
           game_mode_const.GAME_MODE_IMPROVISE: '3v3',
           game_mode_const.GAME_MODE_DUEL: 'gvg'
           }
        if global_data.is_pc_mode:
            game_mode_to_ani.update({tuple(game_mode_const.GAME_MODE_SURVIVALS): 'normal_pc'
               })
        for mode_types, mode_ani in six.iteritems(game_mode_to_ani):
            if global_data.game_mode.is_mode_type(mode_types):
                self.panel.PlayAnimation(mode_ani)
                break

    def play_animation(self):
        self.panel.PlayAnimation('show')

    def restart_show(self):
        self.panel.StopAnimation('disappear')
        self.panel.stopActionByTag(self.TAG)
        self.panel.RecoverAnimationNodeState('disappear')
        self.panel.PlayAnimation('show')

    def delay_close(self):
        self.panel.PlayAnimation('disappear')
        self.panel.DelayCallWithTag(1.2, self.close, tag=self.TAG)

    def on_finalize_panel(self):
        pass