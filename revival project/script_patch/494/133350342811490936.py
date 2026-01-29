# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVESinglePassDetailInfoUI.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc
import six_ex
import time
from logic.comsys.battle.pve.PVEPassDetailInfoUIBase import PVEPassDetailInfoUIBase
PASS_PRIORITY_INFO = {'hp': {'title': 409,'icon': 'durability','up_name': 'up_hp','max_name': 'max_hp'},'shield': {'title': 410,'icon': 'shield','up_name': 'up_shield','max_name': 'max_shield'},'atk': {'title': 408,'icon': 'atk','up_name': 'up_atk','max_name': 'max_atk'},'speed': {'title': 415,'icon': 'speed','up_name': '','max_name': 'max_speed'}}

class PVESinglePassDetailInfoUI(PVEPassDetailInfoUIBase):

    def init_priority_list_widget(self):
        self.nd_data.setVisible(True)
        self.nd_data_team.setVisible(False)
        self.normal_priority_list = self.panel.list_info

    def _update_top_prop_info(self):
        from logic.comsys.battle.pve.PVEMainUIWidgetUI.PVEMechaInfoWidget import PRIORITY_ICON_PATH
        list_info = self.panel.list_info_2
        list_info.DeleteAllSubItem()
        for priority_name, info in six_ex.items(PASS_PRIORITY_INFO):
            item = list_info.AddTemplateItem()
            item.lab_title.SetString(get_text_by_id(info.get('title')))
            item.icon.SetDisplayFrameByPath('', PRIORITY_ICON_PATH.format(info.get('icon')))
            lab_data = item.lab_data
            init_num = int(self.mecha_conf.get(priority_name))
            lab_data.SetString(str(init_num))
            bar_prog = item.bar_prog
            max_num = self.mecha_conf.get(info.get('max_name'))
            bar_prog.prog_normal.SetPercentage(float(init_num) / max_num * 100)