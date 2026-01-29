# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVETeamPassDetailInfoUI.py
from __future__ import absolute_import
from logic.comsys.battle.pve.PVEPassDetailInfoUIBase import PVEPassDetailInfoUIBase, PVE_DETAIL_PROP_ICON_PATH
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc
import six_ex
import time
PROG_PASS_ATTRIBUTE_INFO = {'total_damage': {'title': 635540,'icon': 'dam_pct','max_name': 'group_damage'}}
NORMAL_PASS_ATTRIBUTE_INFO = {'total_damage': {'title': 635543,'icon': 'dam','is_percent': False,'is_decimals': False},'pve_rescue': {'title': 635541,'icon': 'er','is_percent': False,'is_decimals': False},'mecha_dead': {'title': 635542,'icon': 'kia','is_percent': False,'is_decimals': False},'kill_monster': {'title': 635544,'icon': 'mob','is_percent': False,'is_decimals': False}}

class PVETeamPassDetailInfoUI(PVEPassDetailInfoUIBase):

    def show_player_name(self, name):
        is_quit = self.pass_info.get('fail_quit', False)
        name = '{}({})'.format(name, get_text_by_id(635589)) if is_quit else name
        self.panel.lab_name.SetString(name)

    def init_prop_list(self):
        self.list_info_team.SetInitCount(2)
        self.team_template = self.list_info_team.GetItem(0)
        self.team_template.lab_title.SetString(get_text_by_id(635554))
        template_bottom = self.list_info_team.GetItem(1)
        template_bottom.list_info_prog.DeleteAllSubItem()
        template_bottom.lab_title.SetString(get_text_by_id(444))
        self.normal_priority_list = template_bottom.list_info

    def init_priority_list_widget(self):
        self.nd_data.setVisible(False)
        self.nd_data_team.setVisible(True)
        self.init_prop_list()

    def _update_top_prop_info(self):
        self._update_team_property_prog()
        self._update_team_property_normal()

    def _update_team_property_prog(self):
        list_info = self.team_template.list_info_prog
        list_info.DeleteAllSubItem()
        for priority_name, info in six_ex.items(PROG_PASS_ATTRIBUTE_INFO):
            item = list_info.AddTemplateItem()
            item.lab_title.SetString(get_text_by_id(info.get('title')))
            item.icon.SetDisplayFrameByPath('', PVE_DETAIL_PROP_ICON_PATH.format(info.get('icon')))
            lab_data = item.lab_data
            init_num = int(self.pass_info.get(priority_name))
            max_num = self.pass_info.get(info.get('max_name'))
            if max_num:
                percent = float(init_num) / max_num * 100 if 1 else 0
                lab_data.SetString('{:.1f}%'.format(percent))
                bar_prog = item.bar_prog
                bar_prog.prog_normal.SetPercentage(percent)

    def _update_team_property_normal(self):
        list_info = self.team_template.list_info
        list_info.DeleteAllSubItem()
        for priority_name, info in six_ex.items(NORMAL_PASS_ATTRIBUTE_INFO):
            item = list_info.AddTemplateItem()
            item.lab_title.setString(get_text_by_id(info.get('title')))
            item.icon.SetDisplayFrameByPath('', PVE_DETAIL_PROP_ICON_PATH.format(info.get('icon')))
            lab_data = item.lab_data
            init_num = self.pass_info.get(priority_name, 0)
            is_percent = info.get('is_percent')
            if is_percent:
                lab_data.SetString('{}%'.format(int(init_num * 100)))
            elif info.get('is_decimals'):
                lab_data.SetString('%.1f' % init_num)
            else:
                lab_data.SetString(str(int(init_num)))