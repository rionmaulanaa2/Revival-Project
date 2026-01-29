# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202311/ActivityBindCSWZH5.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from common.cfg import confmgr
from logic.gutils.common_ui_utils import show_game_rule
from logic.gutils.global_data_utils import get_global_data
from logic.gutils import activity_utils
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, ITEM_RECEIVED, ITEM_UNGAIN, ITEM_UNRECEIVED
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import jump_to_ui_utils
from logic.gutils import live_utils
import json

class ActivityBindCSWZH5(ActivityTemplate):

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_resp_cswz_jimu_url': self.on_open_url
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        super(ActivityBindCSWZH5, self).init_parameters()

    def on_init_panel(self):
        super(ActivityBindCSWZH5, self).on_init_panel()
        self.init_btn_jump_h5()

    def init_btn_jump_h5(self):
        btn_go = self.panel.btn_go

        @btn_go.unique_callback()
        def OnClick(btn, touch):
            global_data.player.pull_cswz_jimu_url()

    def on_open_url(self, url):
        if url:
            import game3d
            game3d.open_url(url)