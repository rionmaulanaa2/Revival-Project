# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/KingCheckStateUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
StateToImgPath = {1: None,
   2: 'gui/ui_res_2/battle_koth/stat/icon_mech.png',
   3: 'gui/ui_res_2/battle_koth/stat/icon_die.png'
   }
from common.const import uiconst

class KingCheckStateUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_koth/stat_main'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self):
        self.init_event()
        self.init_parameters()
        self.init_panel()

    def on_finalize_panel(self):
        pass

    def init_parameters(self):
        self.name = global_data.player.logic.ev_g_char_name()

    def init_panel(self):
        team_list = self.panel.nd_stat.nd_stat_team.list_team
        for i in range(4):
            team_list.GetItem(i).img_team_icon.lab_num.SetString(str(i + 1))

        team_list = self.panel.nd_stat.nd_stat_camp.list_camp
        for i in range(8):
            team_list.GetItem(i).lab_rank.SetString(str(i + 1))

        if global_data.king_battle_data:
            self.update_data(global_data.king_battle_data.get_rank_data())

    def init_event(self):
        emgr = global_data.emgr
        econf = {'update_rank_data': self.update_data
           }
        emgr.bind_events(econf)

    def update_data(self, state_data):
        if state_data is None:
            return
        else:
            team = state_data.get('group', [])
            team_list = self.panel.nd_stat.nd_stat_team.list_team
            member_count = len(team)
            for i in range(4):
                member = team_list.GetItem(i)
                self.set_item_value(member, team[i] if i < member_count else None, i < member_count)

            team = state_data.get('faction', [])
            team_list = self.panel.nd_stat.nd_stat_camp.list_camp
            member_count = len(team)
            for i in range(8):
                member = team_list.GetItem(i)
                self.set_item_value(member, team[i] if i < member_count else None, i < member_count)

            return

    def init_self_diff(self, item, is_self):
        if item.img_self.isVisible() == is_self:
            return
        item.img_self.setVisible(is_self)
        color = '#DW'
        if is_self:
            color = '#DY'
        item.lab_name.SetColor(color)
        item.lab_kill.SetColor(color)
        item.lab_kill_mech.SetColor(color)
        item.lab_die.SetColor(color)
        item.lab_score.SetColor(color)

    def set_item_value(self, member, data, visible):
        if visible:
            soul_id = data[0]
            is_self = data[1] == self.name
            self.init_self_diff(member, is_self)
            member.lab_name.SetString(data[1])
            member_state = data[2]
            if member_state == 1:
                member.img_status.setVisible(False)
            else:
                member.img_status.setVisible(True)
                member.img_status.SetDisplayFrameByPath('', StateToImgPath[member_state])
            member.lab_kill.SetString(str(data[3]))
            member.lab_kill_mech.SetString(str(data[4]))
            member.lab_die.SetString(str(data[5]))
            member.lab_score.SetString(str(data[6]))
            member.setVisible(True)
        else:
            member.setVisible(False)