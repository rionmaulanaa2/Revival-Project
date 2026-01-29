# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityRedCliff/ActivityRedCliffLianLianKan.py
from __future__ import absolute_import
import six
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

class ActivityRedCliffLianLianKan(ActivityTemplate):
    NEXT_LEVEL_TAG = 20220314

    def on_init_panel(self):
        self.show_brand_level = global_data.player.brand_level
        self.check_if_is_all_open()
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self.ui_data = self.activity_conf.get('cUiData')
        self.ultimate_reward = self.ui_data['ultimate_reward']
        self.chip_item_id = self.ui_data['chip_item_id']
        self.update_task_list()
        self.panel.list_item.SetInitCount(16)
        self.reward_btn_list = [self.panel.btn_clearance_1, self.panel.btn_clearance_2, self.panel.btn_clearance_3]
        self.cup_count = global_data.player.get_item_num_by_no(self.chip_item_id)
        self.allow_click = bool(self.cup_count)
        self.update_final_reward()
        self.init_exchange_item()
        self.update_cup_count()
        for idx, item in enumerate(self.panel.list_item.GetAllItem()):
            item.btn_click.EnableCustomState(True)
            item.btn_click.BindMethod('OnClick', lambda btn, touch, i=idx: self.on_click_item_by_idx(i))

        reward_list = self.activity_conf.get('cUiData', {}).get('gift_list', [])
        for idx, reward_btn in enumerate(self.reward_btn_list):
            if len(reward_list) > idx:
                reward_item, num = confmgr.get('common_reward_data', str(reward_list[idx]), 'reward_list')[0]
                img = getattr(reward_btn, 'img_clearance_%d' % (idx + 1))
                item_path = get_lobby_item_pic_by_item_no(reward_item)
                img.SetDisplayFrameByPath('', item_path)
                reward_btn.BindMethod('OnClick', lambda btn, touch, i=idx + 1, item_id=reward_item, item_num=num: self.on_click_reward(btn, touch, i, item_id, item_num))

        self.update_reward()
        self.play_show_animation()
        self.init_btn()
        self.update_brand_level_show()

    def update_brand_level_show(self, keep_kv_hide=False):
        level_name_dict = {1: 610733,2: 610734,3: 610735}
        self.panel.lab_days.SetString(level_name_dict.get(self.show_brand_level, 610733))
        if (self.show_brand_level < global_data.player.brand_level or self._is_all_level_passed) and not keep_kv_hide:
            self.panel.list_item.setVisible(False)
            self.panel.img_kv.setVisible(True)
            self.panel.img_kv.stopAllActions()
            self.panel.img_kv.setOpacity(255)
            kv_path = 'gui/ui_res_2/activity/activity_202203/hongyadong_open/img_hongyadong_open_kv_%d.png' % self.show_brand_level
            self.panel.img_kv.SetDisplayFrameByPath('', kv_path)
        else:
            self.panel.list_item.setVisible(True)
            self.panel.img_kv.setVisible(False)
            self.update_list_item()
        self.panel.btn_left.SetEnable(self.show_brand_level > 1)
        self.panel.btn_right.SetEnable(self.show_brand_level < 3)
        self.update_btn_share()

    def update_btn_share(self):
        if self._is_all_level_passed:
            self.panel.btn_share.setVisible(True)
        else:
            self.panel.btn_share.setVisible(False)

    def check_if_is_all_open(self):
        state = global_data.player.core_reward_st.get(str(MAX_LEVEL_COUNT))
        if state in [ITEM_RECEIVED, ITEM_UNRECEIVED]:
            self._is_all_level_passed = True
        else:
            self._is_all_level_passed = False

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
        goto_share(share_pic='gui/ui_res_2/activity/activity_202203/hongyadong_open/img_hongyadong_kv_all.png', hide_logo=True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'open_brand_succ_event': self.on_cell_unlocked,
           'on_lobby_bag_item_changed_event': self.on_item_received,
           'receive_task_reward_succ_event': self.update_task_list_with_check,
           'task_prog_changed': self.update_task_list_with_check,
           'receive_brand_core_reward_succ': self.recived_cord_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_exchange_item(self):
        pass

    def update_final_reward(self):
        reward_item, num = confmgr.get('common_reward_data', str(self.ultimate_reward), 'reward_list')[0]
        self.panel.lab_gun_name.SetString(get_lobby_item_name(reward_item))
        self.update_exchange_rp()

    def update_task_list_with_check(self, *args):
        self.update_task_list()
        global_data.emgr.refresh_activity_redpoint.emit()

    def update_task_list(self, *args):
        task_id = str(self.activity_conf.get('cUiData', {}).get('random_task_id'))
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
            self.panel.list_task.SetInitCount(len(children_task_list))
            for idx, (task_state, child_task) in enumerate(children_task_list):
                item = self.panel.list_task.GetItem(idx)
                item.lab_task.SetString(get_task_name(child_task))
                task_prog = global_data.player.get_task_prog(child_task)
                total_prog = get_total_prog(child_task)
                is_done = task_state != STATE_SELECTED
                if is_done:
                    color = 'A2F4FE' if 1 else '24275E'
                    item.lab_schedule.SetString('<color=0X%sFF>%s</color>/%s' % (color, task_prog, total_prog))
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
            btn_state = self.get_item_state(idx)
            btn.SetEnable(btn_state == STATE_NORMAL)
            item.icon_exchange.setVisible(btn_state == STATE_NORMAL)
            btn._updateCurState(btn_state)

    def update_reward(self):
        for idx, reward_btn in enumerate(self.reward_btn_list):
            state = global_data.player.core_reward_st.get(str(idx + 1), ITEM_UNGAIN)
            img_gain = getattr(self.panel, 'img_gain_%d' % (idx + 1))
            if state == ITEM_UNRECEIVED:
                reward_btn.SetSelect(True)
                img_gain.setVisible(False)
            elif state == ITEM_RECEIVED:
                reward_btn.SetSelect(False)
                img_gain.setVisible(True)

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

    def update_exchange_rp(self):
        img_red = getattr(self.panel.nd_exchange, 'img_tips', None)
        if img_red:
            img_red.setVisible(self.show_exchange_rp(self._activity_type))
        return

    def get_item_state(self, idx):
        if self.show_brand_level < global_data.player.brand_level:
            return STATE_DISABLED
        if self.show_brand_level > global_data.player.brand_level:
            return STATE_DISABLED
        if idx not in global_data.player.open_brand:
            btn_state = STATE_NORMAL if self.allow_click else STATE_DISABLED
        elif idx in global_data.player.open_brand:
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
        if self.show_brand_level != global_data.player.brand_level:
            global_data.game_mgr.show_tip(get_text_by_id(610770))
            return
        if not self.allow_click:
            return
        if self.get_item_state(idx) != STATE_NORMAL:
            return
        self.allow_click = False
        global_data.player.try_open_brand(self.show_brand_level, int(idx / BRAND_CNT), int(idx % BRAND_CNT))

    def on_click_reward(self, btn, touch, level, item_id, item_num):
        if global_data.player.receive_brand_core_reward(level):
            return
        else:
            x, y = btn.GetPosition()
            w, h = btn.GetContentSize()
            x -= 6 * w
            y -= 60
            wpos = btn.ConvertToWorldSpace(x, y)
            global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos, extra_info=None, item_num=item_num)
            return

    def on_cell_unlocked(self, level, row, column, open_core_reward):
        if open_core_reward:
            if level <= 0:
                log_error('on_cell_unlocked failed ', level, row, column, open_core_reward)
        if self.show_brand_level != level:
            self.show_brand_level = level
            self.update_brand_level_show(keep_kv_hide=True)
        idx = row * BRAND_CNT + column
        if idx >= self.panel.list_item.GetItemCount():
            return
        item = self.panel.list_item.GetItem(idx)
        item.PlayAnimation('click')
        if open_core_reward:
            new_frames = ['gui/ui_res_2/activity/activity_202203/hongyadong_open/img_brand_hongyadong_open_4.png',
             'gui/ui_res_2/activity/activity_202203/hongyadong_open/img_brand_hongyadong_open_3.png',
             'gui/ui_res_2/activity/activity_202203/hongyadong_open/img_brand_hongyadong_open_1.png']
            item.btn_click.SetFrames('', new_frames)
        else:
            new_frames = [
             'gui/ui_res_2/activity/activity_202203/hongyadong_open/img_brand_hongyadong_open_4.png',
             'gui/ui_res_2/activity/activity_202203/hongyadong_open/img_brand_hongyadong_open_2.png',
             'gui/ui_res_2/activity/activity_202203/hongyadong_open/img_brand_hongyadong_open_1.png']
            item.btn_click.SetFrames('', new_frames)
        item.btn_click.SetSelect(True)
        self.allow_click = bool(self.cup_count)
        self.update_reward()
        if open_core_reward:
            self.check_if_is_all_open()
            self.panel.SetTimeOut(2.0, lambda : self.show_kv_anim(level), self.NEXT_LEVEL_TAG)
            if self._is_all_level_passed:
                self.update_btn_share()
        else:
            self.update_cup_count()
        global_data.emgr.refresh_activity_redpoint.emit()

    def recived_cord_reward(self, level):
        self.update_reward()

    def show_kv_anim(self, target_kv):
        if target_kv != self.show_brand_level:
            return
        global_data.game_mgr.show_tip(get_text_by_id(610773))
        kv_path = 'gui/ui_res_2/activity/activity_202203/hongyadong_open/img_hongyadong_open_kv_%d.png' % self.show_brand_level
        self.panel.img_kv.SetDisplayFrameByPath('', kv_path)
        self.panel.img_kv.setVisible(True)
        self.panel.img_kv.setOpacity(0)
        self.panel.img_kv.SetEnableCascadeOpacityRecursion(True)
        self.panel.list_item.setVisible(False)
        action = cc.FadeIn.create(1.3)
        self.panel.img_kv.runAction(action)

        def to_next_level():
            if str(self.show_brand_level) != str(MAX_LEVEL_COUNT):
                self.show_brand_level += 1
                self.update_brand_level_show()

        self.panel.SetTimeOut(2.0, to_next_level, tag=self.NEXT_LEVEL_TAG)

    @staticmethod
    def show_task_rp(activity_id):
        from logic.gutils.activity_utils import can_receive_task_reward
        activity_conf = confmgr.get('c_activity_config', activity_id)
        task_id = activity_conf.get('cTask')
        show = can_receive_task_reward(task_id)
        return show

    @staticmethod
    def show_exchange_rp(activity_id):
        _is_all_level_passed = False
        state = global_data.player.core_reward_st.get(str(MAX_LEVEL_COUNT))
        if state in [ITEM_RECEIVED, ITEM_UNRECEIVED]:
            _is_all_level_passed = True
        if not _is_all_level_passed:
            return False
        from logic.gutils.mall_utils import get_mall_item_price
        activity_conf = confmgr.get('c_activity_config', activity_id)
        ui_data = activity_conf['cUiData']
        coin_count = global_data.player.get_item_num_by_no(ui_data['chip_item_id'])
        exchange_goods_cost = get_mall_item_price(str(ui_data['exchange_goods_id']), pick_list=('item', ))
        if not exchange_goods_cost:
            return False
        exchange_goods_cost = exchange_goods_cost[0]['real_price']
        return coin_count >= exchange_goods_cost

    @staticmethod
    def show_tab_rp(activity_id):
        if ActivityRedCliffLianLianKan.show_task_rp(activity_id):
            return True
        else:
            activity_conf = confmgr.get('c_activity_config', activity_id)
            ui_data = activity_conf['cUiData']
            for level, st in six.iteritems(global_data.player.core_reward_st):
                if st == ITEM_UNRECEIVED:
                    return True

            _is_all_level_passed = False
            state = global_data.player.core_reward_st.get(str(MAX_LEVEL_COUNT))
            if state in [ITEM_RECEIVED, ITEM_UNRECEIVED]:
                _is_all_level_passed = True
            if _is_all_level_passed:
                return ActivityRedCliffLianLianKan.show_exchange_rp(activity_id)
            ui_data = activity_conf['cUiData']
            return bool(global_data.player.get_item_num_by_no(ui_data['chip_item_id']))

    def on_finalize_panel(self):
        super(ActivityRedCliffLianLianKan, self).on_finalize_panel()