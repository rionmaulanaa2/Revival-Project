# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewLianLianKan.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gutils.activity_utils import can_exchange
from logic.gutils.mall_utils import item_can_use_by_item_no
from logic.gutils.jump_to_ui_utils import jump_to_item_book_page
from logic.gutils.task_utils import get_task_fresh_type, get_task_name, get_total_prog, get_jump_conf, get_raw_left_open_time, get_children_task
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_name, exec_jump_to_ui_info, get_lobby_item_type
from logic.gcommon.item.lobby_item_type import ITEM_TYPE_SKIN
from common.cfg import confmgr
from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED
import cc
from logic.gcommon.time_utility import get_simply_time, get_time_string
from common.utils.timer import CLOCK
from logic.gcommon.common_const.activity_const import SUMMER_COCONUT_COLUMN
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.template_utils import init_tempate_mall_i_item
VER_LINE = 0
HOR_LINE = 1
LEAN_LINE = 2

class ActivityNewLianLianKan(ActivityTemplate):

    def on_init_panel(self):
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self.ui_data = self.activity_conf.get('cUiData')
        all_unlock_reward_id = str(self.ui_data['gift_list'][-1])
        self.ultimate_reward = confmgr.get('common_reward_data', all_unlock_reward_id, 'reward_list')[0][0]
        self.chip_item_id = self.ui_data['chip_item_id']
        self.update_task_list()
        self.panel.list_item.SetInitCount(SUMMER_COCONUT_COLUMN * SUMMER_COCONUT_COLUMN)
        self.panel.list_item_vertical.SetInitCount(SUMMER_COCONUT_COLUMN)
        self.panel.list_item_horizontal.SetInitCount(SUMMER_COCONUT_COLUMN + 1)
        self.reward_item_state = [ ITEM_UNGAIN for i in range(SUMMER_COCONUT_COLUMN * 2 + 1) ]
        self.cup_count = global_data.player.get_item_num_by_no(self.chip_item_id)
        self.allow_click = bool(self.cup_count)
        self.xian_01_init_pos = self.panel.vx_xian_01.GetPosition()
        self.xian_02_init_pos = self.panel.vx_xian_02.GetPosition()
        self.is_skin = get_lobby_item_type(self.ultimate_reward) in ITEM_TYPE_SKIN
        self.panel.lab_name.SetString(get_lobby_item_name(self.ultimate_reward))
        global_data.llk = self
        if self.panel.btn_question:

            @self.panel.btn_question.callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(self.activity_conf['cNameTextID']), get_text_by_id(self.activity_conf['cDescTextID']))

        @self.panel.btn_exchange.callback()
        def OnClick(btn, touch):
            ultimate_reward_gain = item_can_use_by_item_no(self.ultimate_reward)[0]
            if ultimate_reward_gain:
                from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                groceries_buy_confirmUI(str(self.ui_data['exchange_goods_id']))
            else:
                global_data.game_mgr.show_tip(get_text_by_id(610845))

        if self.panel.btn_look:

            @self.panel.btn_look.callback()
            def OnClick(btn, touch):
                jump_to_item_book_page('1', self.ultimate_reward)

        self.update_final_reward()
        self.init_exchange_item()
        self.update_cup_count()
        for idx in range(SUMMER_COCONUT_COLUMN * SUMMER_COCONUT_COLUMN):
            item = self.panel.list_item.GetItem(idx)
            if not item:
                continue
            item.btn_click.EnableCustomState(True)
            item.btn_click.BindMethod('OnClick', lambda btn, touch, i=idx: self.on_click_item_by_idx(i))

        self.update_list_item()
        locked_cell = global_data.player.locked_coconut_map
        for i in range(SUMMER_COCONUT_COLUMN):
            for j in range(SUMMER_COCONUT_COLUMN):
                if i * SUMMER_COCONUT_COLUMN + j in locked_cell:
                    break
            else:
                self.connect_line(HOR_LINE, i)

            for j in range(SUMMER_COCONUT_COLUMN):
                if i + j * SUMMER_COCONUT_COLUMN in locked_cell:
                    break
            else:
                self.connect_line(VER_LINE, i)

        for i in (0, 5, 10, 15):
            if i in locked_cell:
                break
        else:
            self.connect_line(LEAN_LINE, 0)

        reward_list = self.activity_conf.get('cUiData', {}).get('gift_list', [])
        for idx in range(SUMMER_COCONUT_COLUMN * 2 + 1):
            if len(reward_list) > idx:
                reward_btn = self.get_reward_btn(idx)
                if not reward_btn:
                    continue
                reward_item, num = confmgr.get('common_reward_data', str(reward_list[idx]), 'reward_list')[0]
                init_tempate_mall_i_item(reward_btn.temp_item, reward_item, num, show_rare_degree=False, show_tips=False)
                reward_btn.temp_item.btn_choose.BindMethod('OnClick', lambda btn, touch, i=idx, item_id=reward_item, item_num=num: self.on_click_reward(btn, touch, i, item_id, item_num))

        self.update_reward()
        self.play_show_animation()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_time, interval=1, mode=CLOCK)

    def get_reward_btn(self, idx):
        if idx < SUMMER_COCONUT_COLUMN:
            return self.panel.list_item_vertical.GetItem(idx)
        if idx <= SUMMER_COCONUT_COLUMN * 2:
            return self.panel.list_item_horizontal.GetItem(idx - SUMMER_COCONUT_COLUMN)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_new_cell_unlock': self.on_cell_unlocked,
           'receive_coconut_reward': self.receive_reward,
           'on_lobby_bag_item_changed_event': self.on_item_received,
           'receive_task_reward_succ_event': self.update_task_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_exchange_item(self):
        init_tempate_mall_i_item(self.panel.temp_item.temp_item, self.ultimate_reward, 1, show_rare_degree=False, show_tips=True)
        init_tempate_mall_i_item(self.panel.temp_item2.temp_item, self.ui_data['exchange_item_id'], 1, show_rare_degree=False, show_tips=True)
        init_tempate_mall_i_item(self.panel.temp_fragment.temp_item, self.chip_item_id, self.ui_data['cost_count'], show_rare_degree=False, show_tips=True)
        init_tempate_mall_i_item(self.panel.temp_reward.temp_item, self.ui_data['exchange_item_id'], 1, show_rare_degree=False, show_tips=True)

    def update_final_reward(self):
        ultimate_reward_gain = item_can_use_by_item_no(self.ultimate_reward)[0]
        if not self.is_skin:
            self.panel.nd_normal.setVisible(not ultimate_reward_gain)
            self.panel.nd_exchange.setVisible(ultimate_reward_gain)
        else:
            self.panel.nd_exchange.setVisible(True)
            self.panel.nd_normal.setVisible(False)
            if ultimate_reward_gain:
                self.panel.lab_type.SetString(get_text_by_id(83133))
            else:
                self.panel.lab_type.SetString(get_text_by_id(80953))
        self.update_exchange_rp()

    def update_task_list(self, *args):
        task_id = self.activity_conf.get('cTask')
        children_task_list = []
        fixed_task_list = get_children_task(task_id)
        random_refresh_type = get_task_fresh_type(str(self.ui_data['random_task_id']))
        random_task_list = global_data.player.get_random_children_tasks(random_refresh_type, str(self.ui_data['random_task_id']))
        if random_task_list is None:
            log_error('ActivityLianLiankan has no random children tasks!')
            random_task_list = []
        if fixed_task_list is None:
            return
        else:
            fixed_task_list = fixed_task_list + random_task_list
            for child_task in fixed_task_list:
                task_state = STATE_SELECTED
                if global_data.player.is_task_finished(child_task):
                    if global_data.player.has_unreceived_task_reward(child_task):
                        task_state = STATE_NORMAL
                    else:
                        task_state = STATE_DISABLED
                children_task_list.append((task_state, child_task))

            children_task_list.sort()
            self.panel.list_task.SetInitCount(len(children_task_list))
            for idx, (task_state, child_task) in enumerate(children_task_list):
                item = self.panel.list_task.GetItem(idx)
                item.lab_task.SetString(get_task_name(child_task))
                if global_data.player.is_task_finished(child_task):
                    prog_text_color = '<color=0XFBDEA2FF>%s</color>'
                else:
                    prog_text_color = '<color=0XED3147FF>%s</color>'
                item.lab_schedule.SetString((prog_text_color + '/%s') % (global_data.player.get_task_prog(child_task), get_total_prog(child_task)))
                text_id_list = (80930, 604027, 906669, 906672)
                text_id = text_id_list[task_state]
                btn_enable = task_state == STATE_NORMAL
                jump_conf = None
                if task_state == STATE_SELECTED:
                    jump_conf = get_jump_conf(child_task)
                    if jump_conf:
                        text_id = jump_conf.get('unreach_text', None) or text_id_list[-1]
                        btn_enable = True
                item.lab_state.SetString(text_id)
                item.btn_click.SetEnable(btn_enable)
                item.btn_click._updateCurState(task_state)

                @item.btn_click.callback()
                def OnClick(btn, touch, child_task=child_task, task_state=task_state, jump_conf=jump_conf):
                    if task_state == STATE_NORMAL:
                        global_data.player.receive_task_reward(child_task)
                    elif task_state == STATE_SELECTED:
                        exec_jump_to_ui_info(jump_conf)

            global_data.emgr.refresh_activity_redpoint.emit()
            return

    def update_list_item(self):
        for idx in range(SUMMER_COCONUT_COLUMN * SUMMER_COCONUT_COLUMN):
            item = self.panel.list_item.GetItem(idx)
            if not item:
                continue
            btn = item.btn_click
            btn_state = self.get_item_state(idx)
            btn.SetEnable(btn_state == STATE_NORMAL)
            if btn_state == STATE_NORMAL:
                item.PlayAnimation('loop')
            else:
                item.StopAnimation('loop')
                item.vx_saoguang.setVisible(False)
            btn._updateCurState(btn_state)

    def update_reward(self):
        for idx in range(SUMMER_COCONUT_COLUMN * 2 + 1):
            reward_btn = self.get_reward_btn(idx)
            if not reward_btn:
                continue
            state = global_data.player.coconut_map_reward_dict.get(str(idx), ITEM_UNGAIN)
            if state == self.reward_item_state[idx]:
                continue
            if state == ITEM_UNRECEIVED:
                reward_btn.PlayAnimation('click')
            else:
                if self.reward_item_state[idx] == ITEM_UNRECEIVED:
                    reward_btn.RecoverAnimationNodeState('click')
                    reward_btn.StopAnimation('click')
                    reward_btn.vx_mask_01.setVisible(False)
                if state == ITEM_RECEIVED:
                    reward_btn.PlayAnimation('display')
            self.reward_item_state[idx] = state

    def receive_reward(self, idxs):
        if type(idxs) not in (list, tuple):
            idxs = [
             idxs]
        for idx in idxs:
            if idx > SUMMER_COCONUT_COLUMN * 2:
                continue
            reward_btn = self.get_reward_btn(idx)
            reward_btn.RecoverAnimationNodeState('click')
            reward_btn.StopAnimation('click')
            reward_btn.vx_mask_01.setVisible(False)
            reward_btn.PlayAnimation('display')
            self.reward_item_state[idx] = ITEM_RECEIVED

        global_data.emgr.refresh_activity_redpoint.emit()

    def on_item_received(self):
        self.update_cup_count()
        self.update_reward()
        self.update_final_reward()
        self.update_exchange_rp()

    def update_cup_count(self):
        self.cup_count = global_data.player.get_item_num_by_no(self.chip_item_id)
        self.allow_click = bool(self.cup_count)
        if self.panel.lab_chance_number:
            self.panel.lab_chance_number.SetString(str(self.cup_count))
        self.update_list_item()
        global_data.emgr.refresh_activity_redpoint.emit()

    def update_exchange_rp(self):
        img_red = getattr(self.panel.btn_exchange, 'img_red', None)
        if img_red:
            img_red.setVisible(self.show_exchange_rp(self._activity_type))
        return

    def connect_line(self, dir, idx, play_anim=False):
        if dir == VER_LINE:
            step = SUMMER_COCONUT_COLUMN
            start_idx = idx
            img_name = 'img_5'
            self.panel.vx_xian_01.SetPosition(self.xian_01_init_pos[0] - 90 * (SUMMER_COCONUT_COLUMN - idx - 1), self.xian_01_init_pos[1])
            anim_name_1 = 'appear_01'
        elif dir == HOR_LINE:
            step = 1
            start_idx = idx * SUMMER_COCONUT_COLUMN
            img_name = 'img_3'
            self.panel.vx_xian_02.SetPosition(self.xian_02_init_pos[0], self.xian_02_init_pos[1] - 90 * idx)
            anim_name_1 = 'appear_02'
        else:
            step = SUMMER_COCONUT_COLUMN + 1
            start_idx = 0
            img_name = 'img_4'
            anim_name_1 = 'appear_03'
        if play_anim:
            self.panel.runAction(cc.Sequence.create([
             cc.CallFunc.create(lambda : self.panel.PlayAnimation(anim_name_1))]))

    def get_item_state(self, idx):
        btn_state = STATE_NORMAL
        if idx not in global_data.player.locked_coconut_map:
            btn_state = STATE_SELECTED
        elif self.cup_count == 0:
            btn_state = STATE_DISABLED
        return btn_state

    def play_show_animation(self):
        act = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show'))]
        for item in self.panel.list_task.GetAllItem():
            item.nd_vx.setVisible(False)
            act.append(cc.CallFunc.create(lambda item=item: item.PlayAnimation('show')))
            act.append(cc.DelayTime.create(0.03))

        self.panel.runAction(cc.Sequence.create(act))

    def on_click_item_by_idx(self, idx):
        if not self.allow_click:
            return
        if self.get_item_state(idx) != STATE_NORMAL:
            return
        self.allow_click = False
        global_data.player.unlock_coconut_map(int(idx / SUMMER_COCONUT_COLUMN), int(idx % SUMMER_COCONUT_COLUMN))

    def on_click_reward(self, btn, touch, reward_id, item_id, item_num):
        if global_data.player.receive_coconut_reward(reward_id):
            return
        else:
            x, y = btn.GetPosition()
            w, h = btn.GetContentSize()
            x += w * 0.5
            wpos = btn.ConvertToWorldSpace(x, y)
            extra_info = {'show_jump': True}
            global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos, extra_info=extra_info, item_num=item_num)
            return

    def on_cell_unlocked(self, idx):
        if idx >= self.panel.list_item.GetItemCount():
            return
        else:
            item = self.panel.list_item.GetItem(idx)
            if item is None:
                return
            item.StopAnimation('loop')
            item.vx_saoguang.setVisible(False)
            item.PlayAnimation('click')
            self.allow_click = bool(self.cup_count)
            self.update_cup_count()
            self.update_reward()
            row_start = idx - idx % SUMMER_COCONUT_COLUMN
            col_start = idx % SUMMER_COCONUT_COLUMN
            lean_start = 0 if idx in (0, 5, 10, 15) else None
            row_complete = True
            col_complete = True
            lean_complete = lean_start is not None
            for i in range(SUMMER_COCONUT_COLUMN):
                if row_complete and row_start + i in global_data.player.locked_coconut_map:
                    row_complete = False
                if col_complete and col_start + i * SUMMER_COCONUT_COLUMN in global_data.player.locked_coconut_map:
                    col_complete = False
                if lean_complete and lean_start + i * (SUMMER_COCONUT_COLUMN + 1) in global_data.player.locked_coconut_map:
                    lean_complete = False

            if row_complete:
                self.connect_line(HOR_LINE, idx / SUMMER_COCONUT_COLUMN, True)
            if col_complete:
                self.connect_line(VER_LINE, idx % SUMMER_COCONUT_COLUMN, True)
            if lean_complete:
                self.connect_line(LEAN_LINE, 0, True)
            global_data.emgr.refresh_activity_redpoint.emit()
            return

    def refresh_time(self):
        task_id = self.activity_conf.get('cTask')
        task_left_time = get_raw_left_open_time(task_id)

    @staticmethod
    def show_task_rp(activity_id):
        from logic.gutils.activity_utils import can_receive_task_reward
        activity_conf = confmgr.get('c_activity_config', activity_id)
        task_id = activity_conf.get('cTask')
        random_task_id = str(activity_conf['cUiData'].get('random_task_id', 0))
        random_refresh_type = get_task_fresh_type(random_task_id)
        random_task_list = global_data.player.get_random_children_tasks(random_refresh_type, random_task_id)
        if not random_task_list:
            random_task_list = []
        for random_task in random_task_list:
            if can_receive_task_reward(random_task):
                return True

        return can_receive_task_reward(task_id)

    @staticmethod
    def show_exchange_rp(activity_id):
        activity_conf = confmgr.get('c_activity_config', activity_id)
        ui_data = activity_conf['cUiData']
        all_unlock_reward_id = str(ui_data['gift_list'][-1])
        ultimate_reward = confmgr.get('common_reward_data', all_unlock_reward_id, 'reward_list')[0][0]
        ultimate_reward_gain = item_can_use_by_item_no(ultimate_reward)[0]
        if not ultimate_reward_gain:
            return False
        from logic.gutils.mall_utils import get_mall_item_price
        coin_count = global_data.player.get_item_num_by_no(ui_data['chip_item_id'])
        if 'exchange_goods_id' not in ui_data:
            return False
        exchange_goods_cost = get_mall_item_price(str(ui_data['exchange_goods_id']), pick_list=('item', ))
        if not exchange_goods_cost:
            return False
        exchange_goods_cost = exchange_goods_cost[0]['real_price']
        return coin_count >= exchange_goods_cost

    @staticmethod
    def show_tab_rp(activity_id):
        if ActivityNewLianLianKan.show_task_rp(activity_id):
            return True
        else:
            if global_data.player:
                is_reward_receive = global_data.player.check_reward_can_receive()
                if is_reward_receive:
                    return True
            activity_conf = confmgr.get('c_activity_config', activity_id)
            ui_data = activity_conf['cUiData']
            all_unlock_reward_id = str(ui_data['gift_list'][-1])
            ultimate_reward = confmgr.get('common_reward_data', all_unlock_reward_id, 'reward_list')[0][0]
            ultimate_reward_gain = item_can_use_by_item_no(ultimate_reward)[0]
            if ultimate_reward_gain:
                return ActivityNewLianLianKan.show_exchange_rp(activity_id)
            ui_data = activity_conf['cUiData']
            return bool(global_data.player.get_item_num_by_no(ui_data['chip_item_id']))

    def on_finalize_panel(self):
        super(ActivityNewLianLianKan, self).on_finalize_panel()
        global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = None
        return