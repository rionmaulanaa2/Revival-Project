# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityHalfPriceArtCollectionSingleLottery.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gutils.activity_utils import get_left_time

class ActivityHalfPriceArtCollectionSingleLottery(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityHalfPriceArtCollectionSingleLottery, self).__init__(dlg, activity_type)
        self.life_timer = 0

    def on_init_panel(self):
        self.init_widgets()
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('btn_loop')
        if global_data.player:
            global_data.player.call_server_method('client_sa_log', ('Monthlycard', {'oper': 'open_act'}))

        @self.panel.btn_go.unique_callback()
        def OnClick(*args):
            self.on_click_btn_go()

    def on_finalize_panel(self):
        self.unregister_timer()

    def on_click_btn_go(self, *args):
        from logic.gutils import mall_utils
        from logic.gutils.jump_to_ui_utils import jump_to_lottery, jump_to_charge
        if global_data.player and global_data.player.has_yueka():
            lottery_ids = mall_utils.get_all_valid_art_lottery_id()
            lottery_id = None
            if lottery_ids:
                lottery_id = lottery_ids[-1]
            jump_to_lottery(lottery_id=lottery_id)
            global_data.player.call_server_method('client_sa_log', ('Monthlycard', {'oper': 'click_go'}))
        else:
            from logic.comsys.charge_ui.ChargeUINew import ACTIVITY_YUEKA_NEW_TYPE
            jump_to_charge(ACTIVITY_YUEKA_NEW_TYPE)
        return

    def init_widgets(self):
        self.refresh_time()
        self.register_timer()

    def refresh_time(self):
        if not self.panel or not self.panel.lab_time:
            return
        lab_time = self.panel.lab_time
        left_time = get_left_time(self._activity_type)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                lab_time.SetString(get_text_by_id(610105).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                lab_time.SetString(get_text_by_id(610105).format(get_readable_time(left_time)))
        else:
            close_left_time = 0
            lab_time.SetString(get_readable_time(close_left_time))

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self.life_timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_time, interval=5, mode=CLOCK)

    def unregister_timer(self):
        if self.life_timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self.life_timer)
        self.life_timer = 0