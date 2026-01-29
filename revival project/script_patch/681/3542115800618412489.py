# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Clone/CloneEndStatisticsUI.py
from __future__ import absolute_import
import six
from logic.comsys.battle.Death.DeathEndStatisticsUI import DeathStatisticsUI
from logic.comsys.battle.Settle.GenericSettleWidgets import SettleNameWidget
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gutils import dress_utils

class CloneStatisticsUI(DeathStatisticsUI):
    PANEL_CONFIG_NAME = 'battle_clone/end_statistics_clone'

    def on_init_panel(self, group_num, settle_dict, reward, teammate_num, teaminfo, enemy_info, achievenment):
        self.padding_mecha_fashion(settle_dict, teaminfo)
        super(CloneStatisticsUI, self).on_init_panel(group_num, settle_dict, reward, teammate_num, teaminfo, enemy_info, achievenment)

    def padding_mecha_fashion(self, settle_dict, teaminfo):

        def padding(data):
            fashion_data = data.get('mecha_fashion', {})
            if not fashion_data:
                fashion_data[FASHION_POS_SUIT] = default_mecha_clothing

        battle = global_data.battle
        if not battle:
            return
        self.mecha_id = battle.get_my_group_use_mecha()
        default_mecha_clothing = dress_utils.battle_id_to_mecha_lobby_id(self.mecha_id)
        padding(settle_dict)
        for teammate_data in six.itervalues(teaminfo):
            padding(teammate_data)

    def on_finish_settle_scene_camera(self):
        self.panel.StopAnimation('next')
        self.panel.PlayAnimation('show')
        self.name_widget.reset_position_and_show(False)

    def init_name_widgets(self):
        eid_list, name_str_list, uid_list, mvp_list, mecha_id_list, priv_settings_list = (
         list(), list(), list(), list(), list(), list())
        if not self._is_ob_settle():
            eid_list.append(self._get_self_eid())
            name_str_list.append(self._get_self_name())
            uid_list.append(self._get_self_uid())
            mvp_list.append(self._settle_dict.get('mvp', False))
            priv_settings_list.append(self._get_self_priv_settings())
        mecha_id_list.append(self.mecha_id)
        for eid, info in six.iteritems(self.teammate_info):
            eid_list.append(eid)
            mvp_list.append(info.get('mvp', False))
            name_str_list.append(info.get('char_name', ''))
            uid_list.append(info.get('uid', None))
            mecha_id_list.append(self.mecha_id)
            priv_settings_list.append(info.get('priv_settings', {}))

        extra_data = {'priv_settings_list': priv_settings_list
           }
        self.name_widget = SettleNameWidget(eid_list, name_str_list, uid_list, mvp_list, not self.win_ending and not self.draw_ending, mecha_id_list, is_ob=self._is_ob_settle(), extra_info=extra_data)
        return

    def init_achievement(self):
        self.on_click_base_layer(None, None)
        return