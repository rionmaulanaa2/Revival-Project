# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/pve/ComPveSetting.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gutils.pve_utils import is_pve_multi_player_team

class ComPveSetting(UnitCom):
    BIND_EVENT = {'E_OPEN_MAIN_SETTING': 'on_open_main_setting'
       }

    def __init__(self):
        super(ComPveSetting, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComPveSetting, self).init_from_dict(unit_obj, bdict)

    def on_open_main_setting(self, ui):
        if not global_data.battle:
            return
        win_ret = global_data.battle.get_pve_win_ret()
        if not is_pve_multi_player_team() and not win_ret:
            ui.set_btn_exit_text_id(465)