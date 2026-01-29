# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/gvg/GVGTopScoreJudgeUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import SMALL_MAP_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
from logic.gutils import role_head_utils
from logic.comsys.effect import ui_effect
from logic.client.const import game_mode_const
import math
from common.const import uiconst
from logic.gutils import mecha_utils
from .GVGTopScoreUI import GVGTopScoreUI
from logic.client.const import game_mode_const

class MechaHpWidget(object):

    def __init__(self, hp_mech_progress):
        self.mecha_in_danger = False
        self.set_unit_params(hp_mech_progress, mecha_utils.get_mecha_blood_unit_count())

    def destroy(self):
        pass

    def update_mecha_health(self, hp_mech_progress, mecha):
        if not (mecha and mecha.logic):
            return
        mecha = mecha.logic
        Value = mecha.get_value
        hp_max = Value('G_MAX_HP')
        hp = Value('G_HP')
        if hp > hp_max:
            hp = hp_max
        shield = Value('G_SHIELD')
        shield_max = Value('G_MAX_SHIELD')
        outer_shield = Value('G_OUTER_SHIELD') or 0
        temporary_shield = Value('G_SUM_TEMPORARY_SHIELD') or 0
        other_shield = outer_shield + temporary_shield
        if shield > shield_max:
            shield = shield_max
        mecha_in_danger = hp < hp_max * 0.25
        if self.mecha_in_danger ^ mecha_in_danger:
            hp_mech_progress.SetUniformTexture('_TexWhite', 'gui/ui_res_2/battle/mech_main/hp_mech_25.png')
        else:
            hp_mech_progress.SetUniformTexture('_TexWhite', 'gui/ui_res_2/battle/mech_main/hp_mech_100.png')
        self.mecha_in_danger = mecha_in_danger
        self.set_ratio_params(hp_mech_progress, hp, shield, hp_max + shield_max + other_shield - hp - shield)
        self.set_progress_params(hp_mech_progress, hp, shield, other_shield)

    def set_unit_params(self, nd, unit, scalar=0.5, gap_unit=None):
        programState = nd.getGLProgramState()
        programState.setUniformFloat('_Xinterval', unit / 2)
        programState.setUniformFloat('_Yinterval', 0)
        programState.setUniformFloat('_Scalar', scalar)
        if gap_unit is not None:
            programState.setUniformFloat('_Emptyinterval', gap_unit)
        return

    def set_progress_params(self, nd, hp, shield, other_shield):
        programState = nd.getGLProgramState()
        programState.setUniformFloat('_XBlood', hp)
        programState.setUniformFloat('_YBlood', shield)
        programState.setUniformFloat('_ZBlood', other_shield)

    def set_ratio_params(self, nd, max_hp, max_shield, other_shield, ratio=0.5):
        programState = nd.getGLProgramState()
        programState.setUniformFloat('_X', max_hp)
        programState.setUniformFloat('_Y', max_shield)
        programState.setUniformFloat('_Z', other_shield)


class GVGTopScoreJudgeUI(GVGTopScoreUI):
    PANEL_CONFIG_NAME = 'observe/2v2_all_player_tab'

    def init_panel(self):
        super(GVGTopScoreJudgeUI, self).init_panel()
        self.set_names()
        self.init_hp_widget()
        self.start_tick()

    def update_battle_data(self):
        super(GVGTopScoreJudgeUI, self).update_battle_data()
        self.set_names()

    def on_finalize_panel(self):
        super(GVGTopScoreJudgeUI, self).on_finalize_panel()
        for eid, widget in six.iteritems(self._hp_widget_dict):
            widget and widget.destroy()

        self._hp_widget_dict = {}

    def set_names(self):
        bat = self.get_battle()
        eid_to_group_id = bat.eid_to_group_id
        group_data = bat.group_data
        for list_nd in self.mecha_list_nd:
            all_items = list_nd.GetAllItem()
            for item in all_items:
                item.lab_player.SetString('')

        for eid in self.eids:
            group_id = eid_to_group_id[eid]
            name = group_data[group_id][eid]['char_name']
            list_nd = self.get_list_node(eid)
            head_index = self.get_list_node_index(eid)
            item_widget = list_nd.GetItem(head_index)
            if item_widget:
                item_widget.lab_player.SetString(name)

        team_names = bat.get_competition_team_names()
        self.panel.lab_blue_team.SetString(team_names.get(bat.my_group, ''))
        self.panel.lab_red_team.SetString(team_names.get(bat.other_group, ''))
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
            if not team_names.get(bat.my_group, '') and not team_names.get(bat.other_group, ''):
                self.panel.nd_words.setVisible(False)

    def start_tick(self):
        import cc
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.update_team_status),
         cc.DelayTime.create(1.0)])))

    def init_hp_widget(self):
        self._hp_widget_dict = {}
        for eid in self.eids:
            index = self.eid_to_index.get(eid, 0)
            lst_nd = self.get_list_node(eid)
            temp_nd = lst_nd.GetItem(index)
            self._hp_widget_dict[eid] = MechaHpWidget(temp_nd.hp_mech_progress)

    def update_team_status(self):
        if not (global_data.battle and global_data.player):
            return
        for eid in self.eids:
            index = self.eid_to_index.get(eid, 0)
            lst_nd = self.get_list_node(eid)
            temp_nd = lst_nd.GetItem(index)
            hp_widget = self._hp_widget_dict.get(eid)
            from mobile.common.EntityManager import EntityManager
            puppet = EntityManager.getentity(eid)
            if hp_widget and puppet and puppet.logic:
                mecha = puppet.logic.ev_g_control_target()
                hp_widget.update_mecha_health(temp_nd.hp_mech_progress, mecha)