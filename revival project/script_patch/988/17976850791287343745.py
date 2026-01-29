# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityFairyland/ActivityFairylandPuzzle.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gutils.mall_utils import item_can_use_by_item_no
from logic.gutils.activity_utils import get_left_time
from logic.gutils.jump_to_ui_utils import jump_to_item_book_page
from logic.gutils.task_utils import get_task_fresh_type, get_task_name, get_task_reward, get_total_prog, get_jump_conf, get_raw_left_open_time
from logic.gutils.item_utils import get_lobby_item_name
from common.cfg import confmgr
from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED
import cc
from logic.gcommon.time_utility import get_simply_time, get_time_string
from common.utils.timer import CLOCK
from logic.gcommon.common_const.activity_const import PUZZLE_ROW_CNT, PUZZLE_COLUMN_CNT
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.template_utils import init_tempate_mall_i_item, init_common_reward_list

class ActivityFairylandPuzzle(ActivityTemplate):
    TASK_TEMPLATE = 'activity/activity_202108/24_puzzle/i_activity_puzzle_task'

    def on_init_panel(self):
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self.ui_data = self.activity_conf.get('cUiData', {})
        self.unlocked_cover_list = global_data.player.opened_puzzle_data
        self.key_count = 0
        self.allow_click = False
        self.update_key_count()
        self.cover_count = PUZZLE_ROW_CNT * PUZZLE_COLUMN_CNT
        self.panel.temp_cover.SetInitCount(self.cover_count)
        for idx, item in enumerate(self.panel.temp_cover.GetAllItem()):
            item.btn_cover.BindMethod('OnClick', lambda btn, touch, i=idx: self.on_click_item_by_idx(i))
            item.lab_num_unlock.SetString(str(self.ui_data['cover_cost']))

        self.update_cover_list()
        self.task_panel = global_data.uisystem.load_template_create(self.TASK_TEMPLATE, parent=self.panel, name='task_dlg')
        self.task_panel.setVisible(False)
        self.panel.btn_task.BindMethod('OnClick', lambda *args: self.task_panel.setVisible(True))
        self.task_panel.nd_task_list.nd_layer.BindMethod('OnClick', lambda *args: self.task_panel.setVisible(False))
        self.task_panel.act_list.SetInitCount(3)
        self.update_task_dlg()

        @self.panel.btn_exchange.callback()
        def OnClick(btn, touch):
            from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
            groceries_buy_confirmUI(str(self.ui_data['exchange_goods_id']))

        init_tempate_mall_i_item(self.panel.temp_fragment, self.ui_data['coin_id'], 5, show_tips=True)
        init_tempate_mall_i_item(self.panel.temp_reward, self.ui_data['exchange_item_id'], 1, show_tips=True)
        init_tempate_mall_i_item(self.panel.temp_item_single, self.ui_data['single_reward_id'], show_tips=True)
        self.panel.temp_item_single.lab_name.SetString(906666)
        init_tempate_mall_i_item(self.panel.temp_item_all, self.ui_data['all_reward_id'], show_tips=True)
        self.panel.temp_item_all.lab_name.SetString(906667)

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cDescTextID']))

        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop_01'))]))
        all_unlocked = self.check_all_unlocked()
        self.panel.temp_cover.setVisible(not all_unlocked)
        self.panel.img_puzzle_line.setVisible(not all_unlocked)
        self.panel.nd_progress.setVisible(not all_unlocked)
        self.panel.temp_fragment.setVisible(all_unlocked)
        self.panel.temp_reward.setVisible(all_unlocked)
        self.panel.btn_exchange.setVisible(all_unlocked)
        self.panel.img_arrow.setVisible(all_unlocked)
        if not all_unlocked:
            self.update_cover_list()
            self.update_prog()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_time, interval=1, mode=CLOCK)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_open_puzzle': self.on_cover_unlocked,
           'on_lobby_bag_item_changed_event': self.update_key_count,
           'receive_task_reward_succ_event': self.update_task_dlg
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_task_dlg(self, *args):
        task_id = self.activity_conf.get('cTask')
        random_refresh_type = get_task_fresh_type(task_id)
        children_task_list = []
        random_task_list = global_data.player.get_random_children_tasks(random_refresh_type, task_id)
        if random_task_list is None:
            return
        else:
            for child_task in random_task_list:
                task_state = STATE_SELECTED
                if global_data.player.is_task_finished(child_task):
                    if global_data.player.has_unreceived_task_reward(child_task):
                        task_state = STATE_NORMAL
                    else:
                        task_state = STATE_DISABLED
                children_task_list.append((task_state, child_task))

            children_task_list.sort()
            self.panel.btn_task.img_red.setVisible(self.show_task_rp(self._activity_type))
            global_data.emgr.refresh_activity_redpoint.emit()
            for idx, (task_state, child_task) in enumerate(children_task_list):
                item = self.task_panel.act_list.GetItem(idx).temp_common
                item.lab_name.SetString(get_task_name(child_task))
                item.lab_num.SetString('%s/%s' % (global_data.player.get_task_prog(child_task), get_total_prog(child_task)))
                text_id_list = (80930, 604027, 906669)
                item.temp_btn_get.btn_common.SetText(text_id_list[task_state])
                item.temp_btn_get.btn_common.SetEnable(task_state == STATE_NORMAL)
                reward_id = get_task_reward(child_task)
                init_common_reward_list(item.list_reward, reward_id)

                @item.temp_btn_get.btn_common.callback()
                def OnClick(btn, touch, task_id=child_task, state=task_state):
                    if state == STATE_NORMAL:
                        global_data.player.receive_task_reward(task_id)

            return

    def update_cover_list(self):
        if self.check_all_unlocked():
            return
        for idx, item in enumerate(self.panel.temp_cover.GetAllItem()):
            item.setVisible(idx not in self.unlocked_cover_list)

    def update_prog(self):
        prog = int(len(self.unlocked_cover_list) * 100.0 / self.cover_count)
        self.panel.progress_bar.SetPercent(prog)
        if prog in (0, 100):
            self.panel.vx_saojiao.setVisible(False)
            self.panel.StopAnimation('loop_02')
        else:
            self.panel.vx_saojiao.setVisible(True)
            self.panel.vx_saojiao.SetPosition(str(prog + 14) + '%0', '50%0')
            self.panel.PlayAnimation('loop_02')

    def check_all_unlocked(self):
        self.unlocked_cover_list = global_data.player.opened_puzzle_data
        return len(self.unlocked_cover_list) >= self.panel.temp_cover.GetItemCount()

    def update_key_count(self, *args):
        self.key_count = global_data.player.get_item_num_by_no(self.ui_data['coin_id'])
        self.allow_click = self.key_count >= self.ui_data['cover_cost']
        self.panel.lab_num.SetString(str(self.key_count))
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
        if idx >= self.panel.temp_cover.GetItemCount():
            return
        item = self.panel.temp_cover.GetItem(idx)
        act = [
         cc.CallFunc.create(lambda : item.PlayAnimation('click')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('click'))]
        if self.check_all_unlocked():
            act.extend([
             cc.DelayTime.create(item.GetAnimationMaxRunTime('click')),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('full_show'))])
        self.panel.runAction(cc.Sequence.create(act))
        self.update_key_count()
        self.update_prog()

    def refresh_time(self):
        task_left_time = get_left_time(self._activity_type)
        self.panel.lab_time.SetString(get_text_by_id(906607).format(get_simply_time(task_left_time)))

    def on_finalize_panel(self):
        super(ActivityFairylandPuzzle, self).on_finalize_panel()
        global_data.game_mgr.get_logic_timer().unregister(self._timer)

    @staticmethod
    def show_task_rp(activity_id):
        from logic.gutils.activity_utils import can_receive_task_reward
        activity_conf = confmgr.get('c_activity_config', activity_id)
        task_id = activity_conf.get('cTask')
        show = can_receive_task_reward(task_id)
        return show

    @staticmethod
    def show_exchange_rp(activity_id):
        from logic.gutils.mall_utils import get_mall_item_price
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
        if ActivityFairylandPuzzle.show_task_rp(activity_id):
            return True
        else:
            puzzle_finish = len(global_data.player.opened_puzzle_data) >= PUZZLE_COLUMN_CNT * PUZZLE_ROW_CNT
            if puzzle_finish:
                return ActivityFairylandPuzzle.show_exchange_rp(activity_id)
            activity_conf = confmgr.get('c_activity_config', activity_id)
            ui_data = activity_conf['cUiData']
            return bool(global_data.player.get_item_num_by_no(ui_data['coin_id']))