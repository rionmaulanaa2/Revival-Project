# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Crown/CrownTopCounterUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.const.uiconst import SMALL_MAP_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility
import math
from common.const import uiconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.battle.Crown.CrownGuideUI import CrownGuideUI
CROWN_NUM_TO_POWER_NAME = {0: 17290,
   1: 17291,
   2: 17292,
   3: 17293
   }

class CrownTopCounterUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_king/king_top_collection'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.init_panel()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_panel(self):
        self.panel.bar_collection.setVisible(True)
        self.panel.bar_tips.setVisible(False)

    def init_event(self):
        self.process_event(True)

    def init_parameters(self):
        self.crown_count = 0
        self.cfg_data = global_data.game_mode.get_cfg_data('play_data')
        self.observed_player_id = None
        self.crown_list = []
        self.become_king_crown_count = self.cfg_data.get('become_king_crown_count', 0)
        self.king_identity_duration = self.cfg_data.get('king_identity_duration', 0)
        self.crown_born = False
        for idx in range(self.become_king_crown_count):
            getattr(self.panel, 'temp_icon_{}'.format(idx))
            self.crown_list.append(getattr(self.panel, 'temp_icon_{}'.format(idx)))
            self.crown_list[idx].btn_icon.SetEnable(False)

        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_king_alive_time': self.update_king_alive_time,
           'update_crown_count': self.update_crown_count,
           'on_crown_born': self.on_crown_born,
           'on_crown_death': self.on_crown_death,
           'scene_observed_player_setted_event': self.on_switch_observe_target,
           'become_pre_king': self.on_become_pre_king,
           'no_more_pre_king': self.on_no_more_pre_king
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_crown_count(self, count):
        if global_data.player:
            for idx in range(self.become_king_crown_count):
                self.crown_list[idx].vx_icon.setVisible(idx + 1 <= count)
                if idx + 1 <= count and idx + 1 > self.crown_count:
                    self.crown_list[idx].PlayAnimation('king')

            self.panel.lab_identity.SetString(get_text_by_id(CROWN_NUM_TO_POWER_NAME[count]))
        self.crown_count = count

    def on_crown_born(self, king_id, king_faction):
        if global_data.cam_lplayer and global_data.cam_lplayer.id == king_id:
            self.crown_born = True
            self.panel.bar_collection.setVisible(False)
            self.panel.bar_tips.setVisible(True)
            self.panel.bar_tips.lab_tips.setString(get_text_by_id(17340))
            global_data.game_mgr.show_tip(get_text_by_id(17340) + '\xef\xbc\x8c' + get_text_by_id(83482))

    def on_crown_death(self, king_id, king_faction):
        if global_data.cam_lplayer and global_data.cam_lplayer.id == king_id:
            self.crown_born = False
            self.panel.bar_collection.setVisible(True)
            self.panel.bar_tips.setVisible(False)

    def update_king_alive_time(self, remain_time):

        def update_time(pass_time):
            if self.panel.lab_count:
                self.panel.lab_count.SetString('{}s'.format(int(remain_time - pass_time)))

        update_time(0)
        self.panel.lab_count.StopTimerAction()
        self.panel.lab_count.TimerAction(update_time, remain_time, callback=None, interval=1.0)
        return

    def update_ui_state(self, state):
        self.panel.setVisible(state)

    def on_switch_observe_target(self, observe_target):
        from logic.gutils import judge_utils
        if not observe_target or not global_data.battle or not judge_utils.is_ob():
            return
        else:
            self.panel.bar_collection.setVisible(True)
            self.panel.bar_tips.setVisible(False)
            group_king_id = global_data.battle.get_group_king_id()
            for group_id, king_id in six.iteritems(group_king_id):
                if observe_target.id == king_id:
                    self.on_crown_born(king_id, group_id)
                    return

            crown_count = global_data.battle.get_soul_crown_count(observe_target.id)
            if crown_count is not None:
                self.update_crown_count(crown_count)
                return
            return

    def on_become_pre_king(self, remain_time):
        if not self.crown_born:
            self.panel.bar_collection.setVisible(False)
            self.panel.bar_tips.setVisible(True)
            self.update_pre_king_time(remain_time)
            self.panel.bar_tips.lab_tips.setString(get_text_by_id(83481))

    def on_no_more_pre_king(self):
        if not self.crown_born:
            self.panel.bar_collection.setVisible(True)
            self.panel.bar_tips.setVisible(False)
            self.panel.bar_tips.lab_tips.setString(get_text_by_id(17340))

    def update_pre_king_time(self, remain_time):

        def update_time(pass_time):
            if self.panel.lab_count:
                self.panel.lab_count.SetString('{}s'.format(int(remain_time - pass_time)))

        update_time(0)
        self.panel.lab_count.StopTimerAction()
        self.panel.lab_count.TimerAction(update_time, remain_time, callback=None, interval=1.0)
        return