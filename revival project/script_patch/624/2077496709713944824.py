# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/career/CareerBadgeMedalInfoUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.gutils import career_utils
from logic.gcommon import time_utility
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.luck_score_const import LUCKY_DOG_TIMES_CAREER_BADGE_ID

class CareerBadgeMedalInfoUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'life/medal_details'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_window'
    TITLE_TEXT_ID = 910024

    def on_init_panel(self, *args, **kwargs):
        super(CareerBadgeMedalInfoUI, self).on_init_panel()

    def on_finalize_panel(self):
        super(CareerBadgeMedalInfoUI, self).on_finalize_panel()

    def refresh_badge(self, sub_branch, lv):
        self._refresh_badge(self.panel, sub_branch, lv)

    def _refresh_badge(self, node, sub_branch, lv):
        badge_item = node.temp_medal
        career_utils.refresh_badge_medal_item(badge_item, sub_branch, lv)
        lab_medal_desc = node.lab_medal_desc
        node.lab_medal_name.SetString(career_utils.get_badge_name_text(sub_branch))
        lab_medal_desc.SetString(career_utils.get_badge_desc_text_by_lv(sub_branch, lv))
        got, ts = career_utils.has_got_badge(sub_branch, lv)
        node.lab_time.setVisible(got)
        if got:
            fmt_text = get_text_by_id(910025)
            time_text = time_utility.get_server_time_str_from_ts(ts, format='%Y.%m.%d')
            txt = fmt_text.format(time_text)
            node.lab_time.SetString(txt)
        if sub_branch == LUCKY_DOG_TIMES_CAREER_BADGE_ID and not got:
            lab_medal_desc.SetString(get_text_by_id(634772))