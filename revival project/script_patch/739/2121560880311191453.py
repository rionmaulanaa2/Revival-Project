# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/ActivitySummerLianLiankan.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gutils.activity_utils import can_exchange
from logic.gutils.mall_utils import item_can_use_by_item_no
from logic.gutils.jump_to_ui_utils import jump_to_item_book_page
from logic.gutils.task_utils import get_task_fresh_type, get_task_name, get_total_prog, get_jump_conf, get_raw_left_open_time, get_children_task
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_name, exec_jump_to_ui_info
from common.cfg import confmgr
from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED
import cc
from logic.gcommon.time_utility import get_simply_time, get_time_string
from common.utils.timer import CLOCK
from logic.gcommon.common_const.activity_const import BRAND_CNT
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_use_parms, get_lobby_item_name
MAX_LEVEL_COUNT = 3
BTN_LEVEL_TEXT = [610733, 610734, 610735]

class ActivitySummerLianLiankan(ActivityTemplate):
    NEXT_LEVEL_TAG = 20220314

    def on_init_panel(self):
        self.show_brand_level = global_data.player.brand_level
        self.check_if_is_all_open()
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self.ui_data = self.activity_conf.get('cUiData')
        self.prog_color_nml = self.ui_data.get('prog_color_nml', None)
        self.prog_color_fin = self.ui_data.get('prog_color_fin', None)
        reward_list = self.ui_data['gift_list']
        self.ultimate_reward = reward_list[-1]
        self.chip_item_id = self.ui_data['chip_item_id']
        self.update_task_list()
        self.panel.list_item.SetInitCount(16)
        self.reward_btn_list = [ self.panel.list_reward.GetItem(i) for i in range(self.panel.list_reward.GetItemCount()) ]
        self.cup_count = global_data.player.get_item_num_by_no(self.chip_item_id)
        self.allow_click = bool(self.cup_count)
        self.panel.lab_tips.SetString(get_text_by_id(610772, (self.ui_data['btn_pass'],)))
        self.update_final_reward()
        self.update_cup_count()
        for idx, item in enumerate(self.panel.list_item.GetAllItem()):
            item.btn_click.EnableCustomState(True)
            item.btn_click.BindMethod('OnClick', lambda btn, touch, i=idx: self.on_click_item_by_idx(i))

        for idx, reward_btn in enumerate(self.reward_btn_list):
            if len(reward_list) > idx:
                reward_item, num = confmgr.get('common_reward_data', str(reward_list[idx]), 'reward_list')[0]
                if reward_btn.lab_quantity:
                    reward_btn.lab_quantity.setVisible(num > 1)
                    reward_btn.lab_quantity.SetString(str(num))
                img = reward_btn.item
                reward_btn.lab_pass.SetString(BTN_LEVEL_TEXT[idx])
                item_path = get_lobby_item_pic_by_item_no(reward_item)
                img.SetDisplayFrameByPath('', item_path)
                reward_btn.btn_click.BindMethod('OnClick', lambda btn, touch, i=idx + 1, item_id=reward_item, item_num=num: self.on_click_reward(btn, i, item_id, item_num))

        self.update_reward()
        self.play_show_animation()
        self.init_btn()
        self.update_brand_level_show()
        return

    def update_brand_level_show(self):
        self.panel.lab_days.SetString(BTN_LEVEL_TEXT[self.show_brand_level - 1])
        self.update_list_item()
        self.panel.btn_left.SetEnable(self.show_brand_level > 1)
        self.panel.btn_right.SetEnable(self.show_brand_level < 3)
        self.update_btn_share()

    def update_btn_share(self):
        if not self.panel.btn_share:
            return
        self.panel.btn_share.setVisible(bool(self._is_all_level_passed))

    def check_if_is_all_open(self):
        state = global_data.player.core_reward_st.get(str(MAX_LEVEL_COUNT))
        self._is_all_level_passed = state in [ITEM_RECEIVED, ITEM_UNRECEIVED]

    def init_btn(self):
        self.panel.btn_left.BindMethod('OnClick', self.on_click_btn_left)
        self.panel.btn_right.BindMethod('OnClick', self.on_click_btn_right)
        if self.panel.btn_question:

            @self.panel.btn_question.callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(self.activity_conf['cNameTextID']), get_text_by_id(self.activity_conf['cDescTextID']))

        @self.panel.btn_exchange.callback()
        def OnClick(btn, touch):
            if self._is_all_level_passed:
                from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                groceries_buy_confirmUI(str(self.ui_data['exchange_goods_id']))
            else:
                global_data.game_mgr.show_tip(get_text_by_id(610771))

        if self.panel.btn_share:
            self.panel.btn_share.BindMethod('OnClick', self.on_click_btn_share)

        @self.panel.btn_see.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
            reward_item, num = confmgr.get('common_reward_data', str(self.ultimate_reward), 'reward_list')[0]
            jump_to_display_detail_by_item_no(reward_item)

    def on_click_btn_left(self, btn, touch):
        self.show_brand_level = self.show_brand_level - 1
        self.panel.stopActionByTag(self.NEXT_LEVEL_TAG)
        self.update_brand_level_show()

    def on_click_btn_right(self, btn, touch):
        self.show_brand_level = self.show_brand_level + 1
        self.panel.stopActionByTag(self.NEXT_LEVEL_TAG)
        self.update_brand_level_show()

    def on_click_btn_share(self, btn, touch):
        from logic.gutils.activity_utils import goto_share
        share_pic = self.ui_data['share_pic']
        goto_share(share_pic=share_pic, hide_logo=not bool(share_pic))

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'open_brand_succ_event': self.on_cell_unlocked,
           'on_lobby_bag_item_changed_event': self.on_item_received,
           'receive_task_reward_succ_event': self.update_task_list_with_check,
           'task_prog_changed': self.update_task_list_with_check,
           'receive_brand_core_reward_succ': self.received_cord_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_final_reward(self):
        reward_item, num = confmgr.get('common_reward_data', str(self.ultimate_reward), 'reward_list')[0]
        self.panel.lab_name.SetString(get_lobby_item_name(reward_item))
        self.update_exchange_rp()

    def update_task_list_with_check(self, *args):
        self.update_task_list()
        global_data.emgr.refresh_activity_redpoint.emit()

    def get_all_children_task(self):
        if not global_data.player:
            return []
        player = global_data.player
        fixed_children_tasks = get_children_task(self.ui_data.get('fixed_task_id', '')) or []
        random_task_id = self.ui_data.get('random_task_id', '')
        random_refresh_type = get_task_fresh_type(random_task_id)
        random_children_tasks = player.get_random_children_tasks(random_refresh_type, random_task_id) or []
        children_tasks = fixed_children_tasks + random_children_tasks
        return children_tasks

    def update_task_list(self, *args):
        task_list = self.get_all_children_task()
        if task_list is None:
            return
        else:
            children_task_list = []
            for child_task in task_list:
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
                task_prog = global_data.player.get_task_prog(child_task)
                total_prog = get_total_prog(child_task)
                is_done = task_state != STATE_SELECTED
                prog_text = '%s/%s'
                if self.prog_color_fin:
                    if self.prog_color_nml and task_prog < total_prog:
                        prog_text = '<color={}>%s</color><color={}>/%s</color>'.format(self.prog_color_nml, self.prog_color_fin)
                    else:
                        prog_text = '<color={}>%s/%s</color>'.format(self.prog_color_fin)
                item.lab_schedule.SetString(prog_text % (task_prog, total_prog))
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
                item.lab_state.SetColor(5239038 if task_state == STATE_DISABLED else 2364167)
                item.btn_click.SetEnable(btn_enable)
                item.btn_click._updateCurState(task_state)

                @item.btn_click.callback()
                def OnClick(btn, touch, child_task=child_task, task_state=task_state, jump_conf=jump_conf):
                    if task_state == STATE_NORMAL:
                        global_data.player.receive_task_reward(child_task)
                    elif task_state == STATE_SELECTED:
                        exec_jump_to_ui_info(jump_conf)

            return

    def update_list_item(self):
        for idx, item in enumerate(self.panel.list_item.GetAllItem()):
            btn = item.btn_click
            pass_idx = global_data.player.core_brand_record.get(str(self.show_brand_level), None)
            btn.SetFrames('', [
             self.ui_data['btn_nml'],
             self.ui_data['btn_pass'] if pass_idx == idx else self.ui_data['btn_err'],
             self.ui_data['btn_sel']])
            btn_state = self.get_item_state(idx)
            btn.SetEnable(btn_state == STATE_NORMAL)
            item.icon_exchange.setVisible(btn_state == STATE_NORMAL)
            btn._updateCurState(btn_state)

        return

    def update_reward(self):
        for idx, reward_btn in enumerate(self.reward_btn_list):
            state = global_data.player.core_reward_st.get(str(idx + 1), ITEM_UNGAIN)
            reward_btn.nd_lock.setVisible(state == ITEM_UNGAIN)
            reward_btn.StopAnimation('get_tips')
            reward_btn.nd_get_tips.setVisible(state == ITEM_UNRECEIVED)

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
        elif self.panel.lab_chance:
            self.panel.lab_chance.SetString(get_text_by_id(633756, (str(self.cup_count),)))
        self.update_list_item()

    def update_exchange_rp(self):
        img_red = getattr(self.panel, 'img_red', None)
        img_red and img_red.setVisible(ActivitySummerLianLiankan.show_exchange_rp(self.ui_data))
        return

    def get_item_state(self, idx):
        unlock_item_list = global_data.player.open_brand_by_level.get(str(self.show_brand_level), [])
        if self.show_brand_level > global_data.player.brand_level:
            return STATE_DISABLED
        if idx not in unlock_item_list:
            btn_state = STATE_NORMAL if self.allow_click else STATE_DISABLED
        elif idx in unlock_item_list:
            btn_state = STATE_SELECTED
        else:
            btn_state = STATE_NORMAL
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
        core_reward_st = global_data.player.core_reward_st.get(str(self.show_brand_level), None)
        if core_reward_st and (core_reward_st == ITEM_RECEIVED or core_reward_st == ITEM_UNRECEIVED):
            return
        else:
            if self.show_brand_level != global_data.player.brand_level:
                global_data.game_mgr.show_tip(get_text_by_id(610770))
                return
            if not self.allow_click:
                return
            if self.get_item_state(idx) != STATE_NORMAL:
                return
            self.allow_click = False
            global_data.player.try_open_brand(self.show_brand_level, int(idx / BRAND_CNT), int(idx % BRAND_CNT))
            return

    def on_click_reward(self, btn, level, item_id, item_num):
        if global_data.player.receive_brand_core_reward(level):
            return
        else:
            x, y = btn.GetPosition()
            wpos = btn.ConvertToWorldSpace(x, y)
            global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos, extra_info=None, item_num=item_num)
            return

    def on_cell_unlocked(self, level, row, column, open_core_reward):
        if open_core_reward and level <= 0:
            log_error('on_cell_unlocked failed ', level, row, column, open_core_reward)
        if self.show_brand_level != level:
            self.show_brand_level = level
            self.update_brand_level_show()
        idx = row * BRAND_CNT + column
        if idx >= self.panel.list_item.GetItemCount():
            return
        item = self.panel.list_item.GetItem(idx)
        item.PlayAnimation('click')
        item.btn_click.SetFrames('', [
         self.ui_data['btn_nml'],
         self.ui_data['btn_pass'] if open_core_reward else self.ui_data['btn_err'],
         self.ui_data['btn_sel']])
        item.btn_click.SetSelect(True)
        self.allow_click = bool(self.cup_count)
        self.update_reward()
        if open_core_reward:
            self.check_if_is_all_open()
            self.show_kv_anim(level)
            if self._is_all_level_passed:
                self.update_btn_share()
        else:
            self.update_cup_count()
        global_data.emgr.refresh_activity_redpoint.emit()

    def received_cord_reward(self, level):
        self.update_reward()
        global_data.emgr.refresh_activity_redpoint.emit()

    def show_kv_anim(self, target_kv):
        if target_kv != self.show_brand_level:
            return
        global_data.game_mgr.show_tip(get_text_by_id(610773))

        def to_next_level():
            if str(self.show_brand_level) != str(MAX_LEVEL_COUNT):
                self.show_brand_level += 1
                self.update_brand_level_show()

        self.panel.SetTimeOut(2.0, to_next_level, tag=self.NEXT_LEVEL_TAG)

    @staticmethod
    def show_exchange_rp--- This code section failed: ---

 394       0  LOAD_GLOBAL           0  'False'
           3  STORE_FAST            1  '_is_all_level_passed'

 395       6  LOAD_GLOBAL           1  'global_data'
           9  LOAD_ATTR             2  'player'
          12  LOAD_ATTR             3  'core_reward_st'
          15  LOAD_ATTR             4  'get'
          18  LOAD_GLOBAL           5  'str'
          21  LOAD_GLOBAL           6  'MAX_LEVEL_COUNT'
          24  CALL_FUNCTION_1       1 
          27  CALL_FUNCTION_1       1 
          30  STORE_FAST            2  'state'

 396      33  LOAD_FAST             2  'state'
          36  LOAD_GLOBAL           7  'ITEM_RECEIVED'
          39  LOAD_GLOBAL           8  'ITEM_UNRECEIVED'
          42  BUILD_LIST_2          2 
          45  COMPARE_OP            6  'in'
          48  POP_JUMP_IF_FALSE    60  'to 60'

 397      51  LOAD_GLOBAL           9  'True'
          54  STORE_FAST            1  '_is_all_level_passed'
          57  JUMP_FORWARD          0  'to 60'
        60_0  COME_FROM                '57'

 398      60  LOAD_FAST             1  '_is_all_level_passed'
          63  POP_JUMP_IF_TRUE     70  'to 70'

 399      66  LOAD_GLOBAL           0  'False'
          69  RETURN_END_IF    
        70_0  COME_FROM                '63'

 401      70  LOAD_CONST            1  ''
          73  LOAD_CONST            2  ('get_mall_item_price',)
          76  IMPORT_NAME          10  'logic.gutils.mall_utils'
          79  IMPORT_FROM          11  'get_mall_item_price'
          82  STORE_FAST            3  'get_mall_item_price'
          85  POP_TOP          

 402      86  LOAD_GLOBAL           1  'global_data'
          89  LOAD_ATTR             2  'player'
          92  LOAD_ATTR            12  'get_item_num_by_no'
          95  LOAD_ATTR             3  'core_reward_st'
          98  BINARY_SUBSCR    
          99  CALL_FUNCTION_1       1 
         102  STORE_FAST            4  'coin_count'

 403     105  LOAD_FAST             3  'get_mall_item_price'
         108  LOAD_GLOBAL           5  'str'
         111  LOAD_GLOBAL           4  'get'
         114  BINARY_SUBSCR    
         115  CALL_FUNCTION_1       1 
         118  LOAD_CONST            5  'pick_list'
         121  LOAD_CONST            8  ('item',)
         124  CALL_FUNCTION_257   257 
         127  STORE_FAST            5  'exchange_goods_cost'

 404     130  LOAD_FAST             5  'exchange_goods_cost'
         133  POP_JUMP_IF_TRUE    140  'to 140'

 405     136  LOAD_GLOBAL           0  'False'
         139  RETURN_END_IF    
       140_0  COME_FROM                '133'

 406     140  LOAD_FAST             5  'exchange_goods_cost'
         143  LOAD_CONST            1  ''
         146  BINARY_SUBSCR    
         147  LOAD_CONST            7  'real_price'
         150  BINARY_SUBSCR    
         151  STORE_FAST            5  'exchange_goods_cost'

 407     154  LOAD_FAST             4  'coin_count'
         157  LOAD_FAST             5  'exchange_goods_cost'
         160  COMPARE_OP            5  '>='
         163  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_SUBSCR' instruction at offset 98

    @staticmethod
    def show_tab_rp(activity_id):
        activity_conf = confmgr.get('c_activity_config', str(activity_id))
        ui_data = activity_conf['cUiData']
        from logic.gutils.activity_utils import can_receive_task_reward
        fixed_task_id = ui_data.get('fixed_task_id', '')
        if fixed_task_id and can_receive_task_reward(fixed_task_id):
            return True
        else:
            random_task_id = ui_data.get('random_task_id', '')
            if random_task_id and can_receive_task_reward(random_task_id):
                return True
            for level, st in six.iteritems(global_data.player.core_reward_st):
                if st == ITEM_UNRECEIVED:
                    return True

            _is_all_level_passed = False
            state = global_data.player.core_reward_st.get(str(MAX_LEVEL_COUNT))
            if state in [ITEM_RECEIVED, ITEM_UNRECEIVED]:
                _is_all_level_passed = True
            if _is_all_level_passed:
                return ActivitySummerLianLiankan.show_exchange_rp(ui_data)
            return bool(global_data.player.get_item_num_by_no(ui_data['chip_item_id']))