# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/career/CareerBadgeProgressUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils import career_utils
from logic.gcommon import time_utility

class CareerBadgeProgressUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'life/life_icon_level_details'
    TEMPLATE_NODE_NAME = 'temp_bg'
    DLG_ZORDER = NORMAL_LAYER_ZORDER

    def on_init_panel(self, *args, **kwargs):
        super(CareerBadgeProgressUI, self).on_init_panel()

    def on_finalize_panel(self):
        super(CareerBadgeProgressUI, self).on_finalize_panel()

    def refresh_badge_list(self, sub_branch):
        cnt = career_utils.get_badge_lv_count(sub_branch)
        self.panel.list_details.SetInitCount(cnt)
        for i in range(cnt):
            lv = i + 1
            item = self.panel.list_details.GetItem(i)
            self._refresh_badge(item, sub_branch, lv)

    def _refresh_badge(self, node, sub_branch, lv):
        badge_item = node.temp_life_icon
        career_utils.refresh_badge_item(badge_item, sub_branch, lv)
        node.lab_name.SetString(career_utils.get_badge_name_text(sub_branch))
        node.lab_content.SetString(career_utils.get_badge_desc_text_by_lv(sub_branch, lv))
        got, ts = career_utils.has_got_badge(sub_branch, lv)
        node.nd_progress.setVisible(not got)
        node.nd_finish.setVisible(got)
        time_text = time_utility.get_server_time_str_from_ts(ts, format='%Y.%m.%d')
        node.lab_finish_time.SetString(time_text)
        max_prog = career_utils.get_badge_max_prog_by_lv(sub_branch, lv)
        if got:
            cur_prog = max_prog
        else:
            cur_prog = career_utils.get_badge_ongoing_max_cur_prog(sub_branch)
            cur_prog = min(cur_prog, max_prog)
        node.lab_progress.SetString('%d/%d' % (cur_prog, max_prog))