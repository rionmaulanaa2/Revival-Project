# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/TurntableWidget.py
from __future__ import absolute_import
from .ActivityWidgetBase import ActivityWidgetBase
from time import time
from logic.comsys.reward.ReceiveRewardUI import ReceiveRewardUI
from random import randint

def gen_interval(interval):
    a, b = (1, 1)
    while 1:
        yield a * interval
        a, b = b, a + b


class TurntableWidget(ActivityWidgetBase):

    def on_init_panel(self):
        self._reward_reason = self.extra_conf.get('reward_reason', 0)
        self._timer = 0
        self._order_item = self.extra_conf.get('order_item', [])
        self._init_interval = self.extra_conf.get('init_interval', 0.1)
        self._gen_interval = gen_interval(self.extra_conf.get('step_interval', 0.05))
        self._max_interval = self.extra_conf.get('max_interval', 0.8)
        self._interval = 0.1
        self._next_t = 0
        self._cur_item_idx = 0
        self._final_idx = None
        self._final_item = None
        self._pass_num = 0
        self._pass_target_num = len(self._order_item) * self.extra_conf.get('round', 3)
        self._wait_stop = False
        self._choose_cb = None
        self._pass_cb = None
        self._stop_cb = None
        return

    def on_finalize_panel(self):
        self.stop()
        self._choose_cb = None
        self._pass_cb = None
        self._stop_cb = None
        self._item_order = None
        self._gen_interval = None
        return

    def start_turn_animation(self):
        self._cur_item_idx = randint(0, len(self._order_item) - 1)
        self._next_t = 0
        self._interval = self._init_interval
        self._pass_num = 0
        from common.utils.timer import LOGIC
        self.stop()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.tick, interval=1, mode=LOGIC)
        self._wait_stop = False
        from logic.comsys.common_ui.ScreenLockerUI import ScreenLockerUI
        ScreenLockerUI(None, False)
        if self._reward_reason:
            judge_func = lambda reason: reason == self._reward_reason
            ReceiveRewardUI.register_reason_handler(self._reward_reason, judge_func, ReceiveRewardUI.REWARD_TIPS_APPEND_DICT)
        return

    def set_final_item(self, idx, item):
        self._final_idx = idx
        self._final_item = item

    def stop(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def tick(self):
        now = time()
        if now > self._next_t:
            if self._wait_stop:
                self.stop()
                global_data.emgr.show_cache_specific_reward.emit(self._reward_reason)
                if self._reward_reason:
                    ReceiveRewardUI.unregister_reason_handler(self._reward_reason)
                global_data.ui_mgr.close_ui('ScreenLockerUI')
                self._stop_cb and self._stop_cb(self._final_idx, self._final_item)
                return
            self._cur_item_idx = (self._cur_item_idx + 1) % len(self._order_item)
            item = self._order_item[self._cur_item_idx]
            if self._final_item and self._pass_num > self._pass_target_num:
                self._interval = min(self._interval + next(self._gen_interval), self._max_interval)
                if self._interval >= self._max_interval:
                    if self._final_idx is None:
                        item = self._final_item
                    if item is self._final_item:
                        self._wait_stop = True
                        self._next_t = now + 0.3
                        item.PlayAnimation('chosen')
                        self._choose_cb and self._choose_cb(item)
                        return
            if item.HasAnimation('pass'):
                item.PlayAnimation('pass')
            self._pass_cb and self._pass_cb(item)
            self._pass_num += 1
            self._next_t = now + self._interval
        return

    def set_choose_callback(self, cb):
        self._choose_cb = cb

    def set_pass_callback(self, cb):
        self._pass_cb = cb

    def set_stop_callback(self, cb):
        self._stop_cb = cb