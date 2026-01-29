# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewbieBondMechaGift.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityCollectNew import ActivityCollectNew
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gutils.new_template_utils import update_task_list_btn
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import task_utils
from common.utils.timer import CLOCK, RELEASE
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_INACTIVE, BTN_ST_OVERDUE
from logic.gutils import mall_utils
import os
from logic.gcommon.time_utility import get_server_time
from logic.comsys.activity.ActivityNewReturnMechaGift import ActivityNewReturnMechaGift
from logic.gcommon.common_const.activity_const import ACTIVITY_EXCLUSIVE_MECHA

class ActivityNewbieBondMechaGift(ActivityNewReturnMechaGift):
    CHOOSE_MECHA_TEXT = 860250
    MECHA_DISPLAY_PATH = 'gui/ui_res_2/battle_mech_call_pic'
    UI_ACTION_EVENT = {}

    def __init__(self, dlg, activity_type):
        super(ActivityNewbieBondMechaGift, self).__init__(dlg, activity_type)
        self.ask_timer = None
        self.tmp_idx = None
        self.t = 0
        self.callback_flag = 0
        self.ignore_bind = False
        return

    def on_init_panel(self):
        super(ActivityNewbieBondMechaGift, self).on_init_panel()

    def start_ask_timer(self):
        self.ask_timer = global_data.game_mgr.register_logic_timer(self.ask_webinfo, interval=3, times=-1, mode=CLOCK)

    def stop_ask_timer(self):
        global_data.game_mgr.unregister_logic_timer(self.ask_timer)

    def on_finalize_panel(self):
        super(ActivityNewbieBondMechaGift, self).on_finalize_panel()
        global_data.game_mgr.unregister_logic_timer(self.ask_timer)

    def init_mecha_choose(self):
        super(ActivityNewbieBondMechaGift, self).init_mecha_choose()

    def process_event(self, is_bind):
        super(ActivityNewbieBondMechaGift, self).process_event(is_bind)