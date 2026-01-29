# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/gvg/GVGScoreMsgUI.py
from __future__ import absolute_import
import six_ex
import six
from common.const.uiconst import BASE_LAYER_ZORDER_1
from common.uisys.basepanel import BasePanel
from logic.client.const import game_mode_const
from common.const import uiconst

class GVGScoreMsgUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_tips/gvg_tips/gvg_score_tips'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self):
        self.init_parameters()
        self.process_event(True)
        self.init_panel()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_panel(self):
        self.hide()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_score_msg': self.update_score_msg
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        bat = global_data.battle
        self.my_group = bat.my_group
        self.other_group = bat.other_group
        self.eid_to_index = bat.eid_to_index
        self.eid_to_group_id = bat.eid_to_group_id

    def update_score_msg(self, left_player_dict):
        self.hide()
        my_group_num = left_player_dict.get(self.my_group, 0)
        other_group_num = left_player_dict.get(self.other_group, 0)
        ani_name = None
        if my_group_num == 2 and other_group_num == 1:
            ani_name = 'show_2v1'
        elif my_group_num == 1 and other_group_num == 2:
            ani_name = 'show_1v2'
        elif my_group_num == 1 and other_group_num == 1:
            ani_name = 'show_1v1'
        if global_data.gvg_battle_data and ani_name:
            mecha_use_dict = global_data.gvg_battle_data.mecha_use_dict
            my_group_left_num = {}
            other_group_left_num = {}
            for eid, die_num in six.iteritems(mecha_use_dict):
                left_num = game_mode_const.GVG_MECHA_NUM - die_num
                if left_num <= 0:
                    continue
                index = self.eid_to_index.get(eid, 0)
                if self.my_group == self.eid_to_group_id.get(eid):
                    my_group_left_num[index] = left_num
                else:
                    other_group_left_num[index] = left_num
                self.set_mecha_num_txt('left', my_group_num, my_group_left_num)
                self.set_mecha_num_txt('right', other_group_num, other_group_left_num)

            self.panel.PlayAnimation(ani_name)
            self.show()
            delay = self.panel.GetAnimationMaxRunTime(ani_name)
            self.panel.SetTimeOut(delay, lambda : self.hide())
        return

    def set_mecha_num_txt(self, nd_key, player_num, mecha_num):
        nd_name = '%s_%d' % (nd_key, player_num)
        nd = getattr(self.panel, nd_name)
        if not nd:
            return
        mecha_indexs = six_ex.keys(mecha_num)
        mecha_indexs.sort()
        for i, index in enumerate(mecha_indexs):
            lab_nd_name = 'lab_%s_%d' % (nd_key, i + 1)
            lab_nd = getattr(nd, lab_nd_name)
            lab_nd and lab_nd.SetString(str(mecha_num[index]))