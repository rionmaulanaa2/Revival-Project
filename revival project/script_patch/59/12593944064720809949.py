# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/pve_rank_utils.py
from __future__ import absolute_import

def get_config_pve_rank_data(c_rank_type):
    from logic.gcommon.common_const import rank_pve_const
    from logic.comsys.battle.pve.rank.PVERankDataObj import PVERankDataObj
    data_obj = PVERankDataObj(c_rank_type)
    rank_config = rank_pve_const.data.get(data_obj.to_server(), None)
    return rank_config


def show_role_tips(title, content):
    from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
    dlg = GameRuleDescUI()
    dlg.set_show_rule(get_text_local_content(title), get_text_local_content(content))