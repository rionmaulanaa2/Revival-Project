# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryActivityButtonWidget.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.activity_utils import get_lottery_activity_types, get_activity_red_point_count_by_widget_type
from logic.gcommon.common_const.activity_const import WIDGET_LOTTERY_S1
from common.cfg import confmgr

class LotteryActivityButtonWidget(object):

    def __init__(self, parent, panel):
        self.parent = parent
        self.panel = panel
        self.refresh_lottery_activity_btn()
        self.process_event(True)

        @self.panel.btn_activity.unique_callback()
        def OnClick(*args):
            activity_types = get_lottery_activity_types()
            if not activity_types:
                global_data.game_mgr.show_tip(get_text_by_id(12128))
                return
            else:
                from .LotteryActivityChooseUI import LotteryActivityChooseUI
                LotteryActivityChooseUI(None, activity_types)
                return

    @property
    def cur_lottery_id(self):
        return self.parent.cur_lottery_id

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'message_update_global_reward_receive': self.refresh_lottery_activity_btn,
           'receive_task_reward_succ_event': self.refresh_lottery_activity_btn,
           'buy_good_success': self.refresh_lottery_activity_btn
           }
        func = emgr.bind_events if flag else emgr.unbind_events
        func(econf)

    def destroy(self):
        self.panel = None
        self.process_event(False)
        return

    def refresh_lottery_activity_btn(self, *args):
        if not self.refresh_activity_button_visible():
            return
        red_point_count = get_activity_red_point_count_by_widget_type(WIDGET_LOTTERY_S1)
        self.panel.nd_activity.red_point.setVisible(red_point_count > 0)
        if not self.panel.IsPlayingAnimation('loop_activity'):
            self.panel.PlayAnimation('loop_activity')
        if not self.panel.IsPlayingAnimation('show_lighting'):
            self.panel.PlayAnimation('show_lighting')

    def refresh_activity_button_visible(self):
        activity_types = get_lottery_activity_types()
        if not activity_types:
            self.panel.nd_activity.setVisible(False)
            return False
        else:
            lottery_info = confmgr.get('lottery_page_config', str(self.cur_lottery_id), default=None)
            if lottery_info and lottery_info.get('special_type'):
                self.panel.nd_activity.setVisible(True)
                return True
            self.panel.nd_activity.setVisible(False)
            return False
            return