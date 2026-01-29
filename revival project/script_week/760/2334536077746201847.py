# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/NewLoopSeasonUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
import logic.gutils.season_utils as season_utils
from common.const import uiconst
import time
from logic.gutils.advance_utils import create_black_canvas

class NewLoopSeasonUI(BasePanel):
    PANEL_CONFIG_NAME = 'season/season_fg'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_close.OnClick': 'try_close'
       }
    UI_OPEN_SOUND = 'season_logo'

    def on_init_panel(self, *args):
        self._open_ts = time.time()
        self.hide_main_ui()
        from logic.gutils.battle_pass_utils import get_now_season
        now_season = get_now_season()
        s_start_dtime, s_end_dtime = season_utils.get_season_datetime(now_season)
        self.panel.lab_title.SetString(get_text_by_id(83617))
        self.panel.lab_date_left.SetString('{}.{}'.format(s_start_dtime.year, s_start_dtime.month))
        self.panel.lab_date_right.SetString('{}.{}'.format(s_end_dtime.year, s_end_dtime.month))
        self.panel.PlayAnimation('show')

    def on_finalize_panel(self):
        self.show_main_ui()

    def try_close(self, *args):
        if time.time() - self._open_ts < 2:
            return
        self.close()