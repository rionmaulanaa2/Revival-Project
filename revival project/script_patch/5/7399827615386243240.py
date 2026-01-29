# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/KothEndWinUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
import cc
from common.const import uiconst

class KothEndWinUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_win_koth'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_details.OnClick': '_on_show_details',
       'btn_next.OnClick': '_on_click_btn_exit'
       }

    def on_init_panel(self, settle_dict, finished_cb=None):
        self.settle_dict = settle_dict
        self.finished_cb = finished_cb
        round_points = settle_dict.get('round_points', {})
        camp_scores = {}
        for turn, data in six.iteritems(round_points):
            turn = int(turn)
            for camp, score in six.iteritems(data):
                camp = int(camp)
                if camp not in camp_scores:
                    camp_scores[camp] = 0
                camp_scores[camp] += score

        score_node = [
         self.panel.nd_score.nd_blue.lab_camp_score,
         self.panel.nd_score.nd_red.lab_camp_score,
         self.panel.nd_score.nd_purple.lab_camp_score]
        for camp, score in six.iteritems(camp_scores):
            camp = int(camp)
            side = global_data.king_battle_data.get_side_by_faction_id(camp)
            score_node[side].SetString(str(score))

        rank = settle_dict.get('rank')
        if rank == 1:
            global_data.emgr.play_virtual_anchor_voice.emit('vo6_1')
        end_time = self.panel.GetAnimationMaxRunTime('end')
        rank_ani = ['appear_first', 'appear_second', 'appear_third']
        appear_rank_time = self.panel.GetAnimationMaxRunTime(rank_ani[rank - 1])
        com_ac_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('end')),
         cc.DelayTime.create(end_time),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation(rank_ani[rank - 1])),
         cc.DelayTime.create(appear_rank_time),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('appear_score'))]
        self.panel.stopAllActions()
        self.panel.runAction(cc.Sequence.create(com_ac_list))

    def _on_show_details(self, *args):
        ui = global_data.ui_mgr.show_ui('KothEndWithRankUI', 'logic.comsys.battle.Settle')
        ui.set_rank_info(self.settle_dict)

    def _on_click_btn_exit(self, *args):
        self.close()
        self.finished_cb and self.finished_cb()

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('KothEndWithRankUI')