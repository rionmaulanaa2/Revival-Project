# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/NeutralShopBattle/BattleAceCoinUIPC.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER_1
from logic.gcommon.cdata import driver_lv_data
from logic.gcommon.common_const import battle_const
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from common.const import uiconst
from .BattleAceCoinUI import BattleAceCoinUI

class BattleAceCoinUIPC(BattleAceCoinUI):
    PANEL_CONFIG_NAME = 'battle_s4_shop/fight_ace_coin_pc'