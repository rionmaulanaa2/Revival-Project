# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202201/ActivitySpringFestivalPuzzle.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.comsys.activity.widget import widget
from logic.gutils.mall_utils import item_can_use_by_item_no
from logic.gutils.activity_utils import get_left_time
from logic.gutils.jump_to_ui_utils import jump_to_item_book_page
from logic.gutils.task_utils import get_task_fresh_type, get_task_name, get_task_reward, get_total_prog, get_jump_conf, get_raw_left_open_time
from logic.gutils.item_utils import get_item_pic_by_item_no
from common.cfg import confmgr
from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED
import cc
from logic.gcommon.time_utility import get_simply_time, get_time_string
from common.utils.timer import CLOCK
from logic.gcommon.common_const.activity_const import PUZZLE_ROW_CNT, PUZZLE_COLUMN_CNT
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.template_utils import init_tempate_mall_i_item, init_common_reward_list
from logic.gutils.mall_utils import get_mall_item_price

@widget('AsyncTaskListWidget')
class ActivitySpringFestivalPuzzle(ActivityTemplate):

    def on_init_panel(self):
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self.ui_data = self.activity_conf.get('cUiData', {})
        self.unlocked_cover_list = global_data.player.opened_puzzle_data
        self.key_count = 0
        self.allow_click = False
        self.update_key_count()
        self.cover_count = PUZZLE_ROW_CNT * PUZZLE_COLUMN_CNT
        self.panel.temp_cover.SetInitCount(self.cover_count)
        coin_pic_path = 'gui/ui_res_2/icon/icon_%s.png' % str(self.ui_data['coin_id'])
        self.panel.icon_puzzle.SetDisplayFrameByPath('', coin_pic_path)
        for idx, item in enumerate(self.panel.temp_cover.GetAllItem()):
            item.img_item.BindMethod('OnClick', lambda btn, touch, i=idx: self.on_click_item_by_idx(i))
            item.lab_num_unlock.SetString(str(self.ui_data['cover_cost']))
            item.icon_puzzle.SetDisplayFrameByPath('', coin_pic_path)

        self.update_cover_list()
        if self.panel.btn_exchange:

            @self.panel.btn_exchange.callback()
            def OnClick(btn, touch):
                from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                groceries_buy_confirmUI(str(self.ui_data['exchange_goods_id']))

        if self.ui_data.get('exchange_goods_id', None):
            exchange_goods_cost = get_mall_item_price(str(self.ui_data['exchange_goods_id']), pick_list=('item', ))[0]['real_price']
            init_tempate_mall_i_item(self.panel.temp_fragment, self.ui_data['coin_id'], exchange_goods_cost, show_tips=True)
            init_tempate_mall_i_item(self.panel.temp_reward, self.ui_data['exchange_item_id'], 1, show_tips=True)

        @self.panel.btn_show.callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_item_book_page
            jump_to_item_book_page('8', self.ui_data['all_reward_id'])

        self.on_item_update()
        if self.panel.btn_lottery:

            @self.panel.btn_lottery.callback()
            def OnClick(btn, touch):
                from logic.gutils.jump_to_ui_utils import jump_to_lottery
                jump_to_lottery('38')

        if self.panel.btn_question:

            @self.panel.btn_question.callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cDescTextID']))

        act = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop_01'))]
        all_unlocked = self.check_all_unlocked()
        self.panel.nd_exchange and self.panel.nd_exchange.setVisible(all_unlocked)
        self.panel.bar_tips.setVisible(not all_unlocked)
        if all_unlocked:
            act.extend([
             cc.DelayTime.create(5),
             cc.CallFunc.create(lambda : self.panel.bar_reward_tips.setVisible(False))])
        self.panel.runAction(cc.Sequence.create(act))
        self.panel.btn_lottery and self.panel.btn_lottery.setVisible(all_unlocked)
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_time, interval=1, mode=CLOCK)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_open_puzzle': self.on_cover_unlocked,
           'player_item_update_event_with_id': self.on_item_update
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_item_update(self, item_no=None, **args):
        if item_no == self.ui_data['all_reward_id'] or global_data.player.get_item_num_by_no(self.ui_data['all_reward_id']):
            self.panel.lab_type.SetString(12136)
        if item_no == self.ui_data['coin_id']:
            self.update_key_count()

    def update_cover_list(self):
        for idx, item in enumerate(self.panel.temp_cover.GetAllItem()):
            not_unlocked = idx not in self.unlocked_cover_list
            item.img_item.setVisible(not_unlocked)
            item.lab_num_unlock.setVisible(not_unlocked)

    def check_all_unlocked(self):
        self.unlocked_cover_list = global_data.player.opened_puzzle_data
        return len(self.unlocked_cover_list) >= self.panel.temp_cover.GetItemCount()

    def update_key_count(self, *args):
        self.key_count = global_data.player.get_item_num_by_no(self.ui_data['coin_id'])
        self.allow_click = self.key_count >= self.ui_data['cover_cost']
        self.panel.lab_coin_num.SetString(get_text_by_id(81860, {'num': str(self.key_count)}))
        img_red = getattr(self.panel.btn_exchange, 'img_red', None)
        if img_red:
            img_red.setVisible(self.show_exchange_rp(self._activity_type))
        global_data.emgr.refresh_activity_redpoint.emit()
        return

    def on_click_item_by_idx(self, idx):
        if not self.allow_click:
            return
        if idx in self.unlocked_cover_list:
            return
        self.allow_click = False
        global_data.player.open_puzzle(int(idx / PUZZLE_COLUMN_CNT), int(idx % PUZZLE_COLUMN_CNT))

    def on_cover_unlocked(self, idx):
        from logic.comsys.common_ui.ScreenLockerUI import ScreenLockerUI
        if idx >= self.panel.temp_cover.GetItemCount():
            return
        item = self.panel.temp_cover.GetItem(idx)
        item.lab_num_unlock.setVisible(False)
        act = [
         cc.CallFunc.create(lambda : ScreenLockerUI(None, False)),
         cc.CallFunc.create(lambda : item.PlayAnimation('show_01')),
         cc.DelayTime.create(item.GetAnimationMaxRunTime('show_01'))]
        if self.check_all_unlocked():
            act.extend([
             cc.DelayTime.create(item.GetAnimationMaxRunTime('click')),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('full_show')),
             cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('full_show'))])
        reason = 'OPEN_PUZZLE-' + str(int(idx / PUZZLE_COLUMN_CNT)) + '-' + str(int(idx % PUZZLE_COLUMN_CNT))
        act.extend([
         cc.CallFunc.create(lambda : global_data.emgr.show_cache_specific_reward.emit(reason)),
         cc.CallFunc.create(lambda : global_data.emgr.show_cache_specific_reward.emit('OPEN_ALL_PUZZLE')),
         cc.CallFunc.create(lambda : global_data.ui_mgr.close_ui('ScreenLockerUI'))])
        if self.check_all_unlocked():
            act.extend([
             cc.DelayTime.create(5),
             cc.CallFunc.create(lambda : self.panel.bar_reward_tips.setVisible(False))])
            self.panel.btn_lottery and self.panel.btn_lottery.setVisible(True)
        self.panel.runAction(cc.Sequence.create(act))
        self.update_key_count()

    def refresh_time(self):
        task_left_time = get_left_time(self._activity_type)
        self.panel.lab_time.SetString(get_text_by_id(906607).format(get_simply_time(task_left_time)))

    def on_finalize_panel(self):
        super(ActivitySpringFestivalPuzzle, self).on_finalize_panel()
        global_data.game_mgr.get_logic_timer().unregister(self._timer)

    @staticmethod
    def show_task_rp(activity_id):
        from logic.gutils.activity_utils import can_receive_task_reward
        activity_conf = confmgr.get('c_activity_config', activity_id)
        ui_data = activity_conf['cUiData']
        if not ui_data:
            return False
        show = can_receive_task_reward(activity_conf['cTask']) or can_receive_task_reward(ui_data['daily_random'])
        return show

    @staticmethod
    def show_exchange_rp(activity_id):
        activity_conf = confmgr.get('c_activity_config', activity_id)
        ui_data = activity_conf['cUiData']
        coin_count = global_data.player.get_item_num_by_no(ui_data['coin_id'])
        exchange_goods_cost = get_mall_item_price(str(ui_data['exchange_goods_id']), pick_list=('item', ))
        if not exchange_goods_cost:
            return False
        exchange_goods_cost = exchange_goods_cost[0]['real_price']
        return coin_count >= exchange_goods_cost

    @staticmethod
    def show_tab_rp(activity_id):
        if ActivitySpringFestivalPuzzle.show_task_rp(activity_id):
            return True
        else:
            puzzle_finish = len(global_data.player.opened_puzzle_data) >= PUZZLE_COLUMN_CNT * PUZZLE_ROW_CNT
            if puzzle_finish:
                return ActivitySpringFestivalPuzzle.show_exchange_rp(activity_id)
            activity_conf = confmgr.get('c_activity_config', activity_id)
            ui_data = activity_conf['cUiData']
            return bool(global_data.player.get_item_num_by_no(ui_data['coin_id']))