# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/season/TierDetailUI.py
from __future__ import absolute_import
import math
from cocosui import cc
from common import utilities
from logic.gutils import template_utils
from logic.gutils import season_utils
from logic.gutils import item_utils
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class TierDetailUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'season/tier_details'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {}

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)

    def on_init_panel(self, *args, **kwargs):
        super(TierDetailUI, self).on_init_panel()
        template_utils.init_common_panel(self.panel.temp_bg, 15027, None)
        self.init_event()
        self.panel.PlayAnimation('appear')
        self.show_list()
        return

    def show_list(self):
        from logic.gcommon.cdata import dan_data
        list_reward = self.panel.list_reward
        custom_conf = []
        dan_list = season_utils.get_dan_list()
        templateName, templateInfo = list_reward.GetTemplateSetting()
        for i, dan in enumerate(dan_list):
            custom_conf.append({'template': templateName,'template_info': {'temp_tier': {'template_info': {'temp_tier': {'ccbFile': season_utils.get_dan_template(dan)}}}}})

        list_reward.SetCustomizeConf(custom_conf)
        list_reward.SetInitCount(len(dan_list))
        top_dan = [
         dan_data.LEGEND, dan_data.ALPHA]
        for i, dan in enumerate(dan_list):
            widget_item = list_reward.GetItem(i)
            template_utils.init_tier_common(widget_item.temp_tier, dan, 0, show_stage='glow', hide_nd_star=True)
            widget_item.lab_tier_name.SetString(season_utils.get_dan_lv_name(dan))
            if dan in top_dan:
                widget_item.lab_describe.SetString('')
            else:
                widget_item.lab_describe.SetString(get_text_by_id(608010, [dan_data.get_lv_num(dan)]))

    def on_close(self, *args):
        self.close()