# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Flag2/Flag2MarkUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import SMALL_MAP_ZORDER
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
import weakref
import copy
import math
import math3d
import common.utils.timer as timer
from common.const import uiconst
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from logic.comsys.common_ui import CommonInfoUtils
from logic.comsys.battle.Flag2.Flag2MarkWidget import Flag2MarkWidgetUI
from logic.comsys.battle.Flag.FlagBaseMarkWidget import FlagBaseMarkWidgetUI
from common.utils.ui_utils import get_scale

class Flag2MarkUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.init_mark_icon()

    def init_parameters(self):
        self.mark_widgets = []

    def on_finalize_panel(self):
        for tmp_mark_widget in self.mark_widgets:
            tmp_mark_widget.on_finalize()

    def init_mark_icon(self):
        faction_to_flag_base_id = global_data.death_battle_data.faction_to_flag_base_id
        for faction_id, flag_base_id in six.iteritems(faction_to_flag_base_id):
            if not flag_base_id:
                return
            if faction_id == global_data.player.logic.ev_g_group_id():
                self.mark_widgets.append(FlagBaseMarkWidgetUI('flag_base_blue', flag_base_id, self.panel))

        flag_id_dict = global_data.death_battle_data.flag_ent_id_dict
        self.mark_widgets.append(Flag2MarkWidgetUI(flag_id_dict, self.panel))