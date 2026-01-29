# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewSkin210123.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.mall_utils import is_valid_goods
from logic.gutils.template_utils import init_price_view
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gutils.advance_utils import set_new_mecha_package
money_icon_scale = 0.8

class ActivityNewSkin210123(ActivityBase):

    def on_init_panel(self):
        self.set_package_content()
        self.play_animation()
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_lobby_bag_item_changed_event': self.set_package_content
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def set_package_content(self):
        set_new_mecha_package(self.panel)

    def play_animation(self):
        self.panel.PlayAnimation('show')