# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/KothEndWithRankUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.const import uiconst

class KothEndWithRankUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_koth_round_score'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_close.OnClick': '_on_close'
       }

    def on_init_panel(self):
        pass

    def set_rank_info(self, settle_dict):
        round_points = settle_dict.get('round_points', {})
        for turn, data in six.iteritems(round_points):
            turn = int(turn)
            for camp, score in six.iteritems(data):
                camp = int(camp)
                side = global_data.king_battle_data.get_side_by_faction_id(camp)
                node = self.panel.list_team.GetItem(side)
                txt_node = getattr(node, 'lab_round%d' % turn)
                txt_node and txt_node.SetString(str(score))

    def _on_close(self, *args):
        self.close()