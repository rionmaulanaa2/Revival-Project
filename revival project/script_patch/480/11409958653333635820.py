# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleGiveUpUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT

class BattleGiveUpUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/open_battle_surrender'
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_ACTION_EVENT = {'temp_btn_1.btn_common.OnClick': 'on_vote_agree',
       'temp_btn_2.btn_common.OnClick': 'on_vote_disagree'
       }
    HOT_KEY_FUNC_MAP = {'surrender_yes': 'on_vote_agree',
       'surrender_no': 'on_vote_disagree'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'surrender_yes': {'node': 'temp_btn_1.temp_pc'},'surrender_no': {'node': 'temp_btn_2.temp_pc'}}

    def on_init_panel(self):
        self.init_parameters()
        self.init_event(True)
        self.init_panel()
        self.panel.PlayAnimation('appear')

    def on_finalize_panel(self):
        self.init_event(False)

    def init_parameters(self):
        self.has_no_surrender = False
        self.is_self_voted = False

    def init_panel(self):
        pass

    def refresh_ui(self, votes, left_time):
        if not (self.panel and self.panel.isValid()):
            return
        else:
            self.panel.list_btn.SetInitCount(len(votes))
            self.panel.prog.SetPercentageWithAni(100, left_time, end_cb=self.end_send_cd)
            self_voted = False
            no_choose = []
            surrender = []
            no_surrender = []
            for player_id, info in six.iteritems(votes):
                idx, flag = info
                is_choose = flag is not None
                is_surrender = flag is True
                condition = (is_choose, is_surrender)
                if not is_choose:
                    no_choose.append(condition)
                elif is_surrender:
                    surrender.append(condition)
                else:
                    no_surrender.append(condition)
                if global_data.player and not self_voted and is_choose:
                    self_voted = player_id == global_data.player.id

            conditions = surrender + no_surrender + no_choose
            for index, nd in enumerate(self.panel.list_btn.GetAllItem()):
                w, h = nd.GetContentSize()
                count = len(conditions)
                nd.SetContentSize(224 / count, h)
                if index < count:
                    is_choose, is_surrender = conditions[index]
                    nd.SetEnable(False)
                    nd.SetShowEnable(False)
                    if not (is_choose and not is_surrender):
                        nd.SetSelect(is_choose)

            self.panel.list_btn.RefreshItemPos()
            if self_voted and not self.panel.IsPlayingAnimation('fold'):
                self.panel.PlayAnimation('fold')
                self.is_self_voted = True
            if no_surrender and not no_choose:
                self.has_no_surrender = True
                self.end_send_cd()
            elif no_choose:
                self.has_no_surrender = True
            else:
                self.has_no_surrender = False
            return

    def end_send_cd(self):
        if not (self.panel and self.panel.isValid()):
            return
        self.panel.StopAnimation('disappear')
        self.panel.PlayAnimation('disappear')
        self.panel.SetTimeOut(self.panel.GetAnimationMaxRunTime('disappear'), lambda : self.close())
        if self.has_no_surrender:
            global_data.game_mgr.show_tip(get_text_by_id(634290))

    def init_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_vote_agree(self, *args, **kargs):
        bat = global_data.battle
        if not bat:
            return
        if self.is_self_voted:
            return False
        bat.vote_surrender(True)

    def on_vote_disagree(self, *args, **kargs):
        bat = global_data.battle
        if not bat:
            return
        if self.is_self_voted:
            return False
        bat.vote_surrender(False)