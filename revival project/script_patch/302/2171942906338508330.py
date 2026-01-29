# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryAIConcertWidget.py
from __future__ import absolute_import
from logic.comsys.lottery.LotteryArtCollectionWidget import LotteryArtCollectionWidget
from common.utils.timer import CLOCK

class LotteryAIConcertWidget(LotteryArtCollectionWidget):

    def init_panel(self):
        super(LotteryAIConcertWidget, self).init_panel()
        guarantee_count, max_guarantee_count = global_data.player.get_reward_guarantee_round_data(self.data['table_id'])
        if guarantee_count:
            pass

    def _show_shop(self):
        if not self.panel.mall_box_buy.isVisible():
            self.shop_widget.parent_show()
        else:
            self.preview_widget.parent_show()
        if not self.refresh_nd_tip_visible():
            return
        self.panel.PlayAnimation('tips_show')
        self.panel.PlayAnimation('tips_loop')
        self.tips_anim_timer = global_data.game_mgr.register_logic_timer(self.tips_anim_end_callback, interval=8.0, times=1, mode=CLOCK)

    def tips_anim_end_callback(self):
        self.panel.StopAnimation('tips_loop')
        self.tips_anim_timer = None
        return

    def refresh_nd_tip_visible(self):
        show = True
        if global_data.player.get_task_prog('1421209') >= 50:
            show = False
        elif global_data.player.get_item_num_by_no(201011152) > 0 or global_data.player.get_item_num_by_no(201011100) > 0:
            show = False
        self.panel.nd_tips.setVisible(show)
        return show

    def _on_lottery_open_box_result(self, item_ids):
        super(LotteryAIConcertWidget, self)._on_lottery_open_box_result(item_ids)
        self.refresh_nd_tip_visible()

    def show_reward_pool(self, rare_degree, cur_count):
        pass

    def hide_reward_pool(self):
        pass