# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MechaDeath/MechaDeathEndStatisticsUI.py
from __future__ import absolute_import
import six
from logic.comsys.battle.Death.DeathEndStatisticsUI import DeathStatisticsUI
from logic.comsys.battle.Settle.GenericSettleWidgets import SettleNameWidget
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_belong_no
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
from logic.gcommon.common_const.battle_const import PLAY_TYPE_MECHA_DEATH
from logic.gcommon.common_const import statistics_const as stat_const

class MechaDeathStatisticsUI(DeathStatisticsUI):
    PANEL_CONFIG_NAME = 'battle_tdm2/end_statistics_tdm2'

    def on_finish_settle_scene_camera(self):
        self.panel.StopAnimation('next')
        self.panel.PlayAnimation('show')
        self.name_widget.reset_position_and_show(False)

    def init_name_widgets(self):
        eid_list, name_str_list, uid_list, mvp_list, mecha_id_list = (
         list(), list(), list(), list(), list())
        if not self._is_ob_settle():
            eid_list.append(self._get_self_eid())
            name_str_list.append(self._get_self_name())
            uid_list.append(self._get_self_uid())
            mvp_list.append(self._settle_dict.get('mvp', False))
            mecha_fashion_id = self._settle_dict.get('mecha_fashion', {}).get(FASHION_POS_SUIT, 201800100)
            mecha_item_id = get_lobby_item_belong_no(mecha_fashion_id)
            mecha_id_list.append(mecha_lobby_id_2_battle_id(mecha_item_id))
        for eid, info in six.iteritems(self.teammate_info):
            eid_list.append(eid)
            uid_list.append(info.get('uid', None))
            mvp_list.append(info.get('mvp', False))
            name_str_list.append(info.get('char_name', ''))
            mecha_fashion_id = info.get('mecha_fashion', {}).get(FASHION_POS_SUIT, 201800100)
            mecha_item_id = get_lobby_item_belong_no(mecha_fashion_id)
            mecha_id_list.append(mecha_item_id)

        self.name_widget = SettleNameWidget(eid_list, name_str_list, uid_list, mvp_list, not self.win_ending and not self.draw_ending, mecha_id_list, is_ob=self._is_ob_settle())
        return

    def init_achievement(self):
        settle_dict = self._settle_dict
        self.panel.temp_achieve.setTouchEnabled(False)
        self._achieve_nds = []
        first_nd = None
        is_mvp = settle_dict.get('mvp', False)
        if is_mvp and not self._is_ob_settle():
            import cc
            if self.win_ending or self.draw_ending:
                template_path = 'end/i_statistics_mvp' if 1 else 'end/i_statistics_defeated_mvp'
                mvp_conf = global_data.uisystem.load_template(template_path)
                nd_mvp = self.panel.temp_achieve.AddItem(mvp_conf)
                mvp_count = global_data.player.get_achieve_stat(PLAY_TYPE_MECHA_DEATH, stat_const.GET_MVP)
                self.panel.PlayAnimation('next')
                nd_mvp.lab_times.SetString(str(mvp_count))
                self._achieve_nds.append(nd_mvp)
                first_nd = first_nd or nd_mvp
        self._cur_achieve_idx = 0
        if len(self._achieve_nds) <= 1:
            self.panel.nd_achieve.btn_left.setVisible(False)
            self.panel.nd_achieve.btn_right.setVisible(False)
        elif first_nd:
            self._achieve_nds.append(first_nd)
        if self._achieve_nds:
            nd_achieve = self._achieve_nds[0]
            nd_achieve.PlayAnimation('show')
            global_data.sound_mgr.play_ui_sound('mvp_open')
        else:
            self.on_click_base_layer(None, None)
            return

        @self.panel.nd_achieve.btn_left.unique_callback()
        def OnBegin(btn, touch):
            if self._cur_achieve_idx == 0:
                self._cur_achieve_idx = len(self._achieve_nds) - 1
            else:
                self._cur_achieve_idx -= 1
            self._show_achievement_by_idx(self._cur_achieve_idx)
            return True

        @self.panel.nd_achieve.btn_right.unique_callback()
        def OnBegin(btn, touch):
            if self._cur_achieve_idx >= len(self._achieve_nds) - 1:
                self._cur_achieve_idx = 0
            else:
                self._cur_achieve_idx += 1
            self._show_achievement_by_idx(self._cur_achieve_idx)
            return True

        return