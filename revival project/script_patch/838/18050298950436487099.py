# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKizunaAISupportGroup.py
from __future__ import absolute_import
import six
from six.moves import range
from functools import cmp_to_key
from logic.comsys.activity.ActivityCollect import ActivityCollect
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gcommon.const import SHOP_PAYMENT_KIZUNA_AI_CHEER_LIGHT_CARD, SHOP_PAYMENT_ITEM_KIZUNA_AI_CHEER_LIGHT_CARD
from logic.gutils.template_utils import splice_price
from logic.gutils.mall_utils import get_mall_item_price
from logic.gutils.task_utils import get_jump_conf, get_total_prog
from logic.gutils.activity_utils import is_activity_in_limit_time
from logic.gutils.item_utils import exec_jump_to_ui_info
from common.cfg import confmgr
import cc
KIZUNA_AI_SHARE_TASK_ID = '1411612'
KIZUNA_AI_EMOTE_GOODS_ID = '50400044'
EMOTE_KEY = 'kizunaai'
SPECIAL_EMOTE_ITEM_ID = 30800109
SPECIAL_EMOTE_TASK_ID = '1411615'
PIC0 = 'gui/ui_res_2/common/button/btn_secondary_middle.png'
PIC1 = 'gui/ui_res_2/common/button/btn_secondary_major.png'
PIC2 = 'gui/ui_res_2/common/button/btn_secondary_useless.png'

class ActivityKizunaAISupportGroup(ActivityCollect):

    def _get_anim_action(self, item, anim_name):
        return cc.CallFunc.create(lambda : item.PlayAnimation(anim_name) and item.setVisible(True))

    def play_show_animation(self):
        self.panel.PlayAnimation('show')
        count = self.panel.act_list.GetItemCount()
        for i in range(count):
            item = self.panel.act_list.GetItem(i)
            item.setVisible(False)

        action_list = []
        action_list.append(cc.DelayTime.create(0.05))
        passed_time = 0.05
        for i in range(count):
            item = self.panel.act_list.GetItem(i)
            action_list.append(self._get_anim_action(item, 'show'))
            if i != count - 1:
                action_list.append(cc.DelayTime.create(0.1))
                passed_time += 0.1

        left_time = self.panel.GetAnimationMaxRunTime('show') - passed_time
        if left_time < 0:
            left_time = 0.03
        action_list.extend([
         cc.DelayTime.create(left_time),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('continue'))])
        self.panel.runAction(cc.Sequence.create(action_list))

    def on_init_panel(self):
        super(ActivityKizunaAISupportGroup, self).on_init_panel()
        self.init_emote_list()
        self.refresh_item_info()
        global_data.player.call_server_method('attend_activity', (self._activity_type,))
        global_data.ui_mgr.get_ui('ActivityKizunaAIMainUI').panel.nd_shadow.setVisible(True)
        self.play_show_animation()

    def init_parameters(self):
        super(ActivityKizunaAISupportGroup, self).init_parameters()
        self.emote_price_info = get_mall_item_price(KIZUNA_AI_EMOTE_GOODS_ID)[0]
        self.emote_item_list = confmgr.get('preview_12002521')['turntable_goods_info']
        self.emote_own_count = 0
        self.common_emote_count = len(self.emote_item_list)

    def init_event(self):
        super(ActivityKizunaAISupportGroup, self).init_event()

        @self.panel.btn_start.unique_callback()
        def OnClick(*args):
            from logic.comsys.common_ui.ScreenLockerUI import ScreenLockerUI
            ScreenLockerUI(None, False)
            global_data.player.buy_goods(KIZUNA_AI_EMOTE_GOODS_ID, 1, self.emote_price_info['goods_payment'])
            return

        conf = confmgr.get('c_activity_config', self._activity_type)

        @self.panel.btn_help.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(int(conf['cNameTextID']), int(conf['cDescTextID']))

    def init_emote_list(self):
        emote_conf = confmgr.get('chat_all_emotes').get_conf()
        emote_text_map = dict()
        for values in six.itervalues(emote_conf):
            if values.get('iItemId', None):
                emote_text_map[str(values['iItemId'])] = values['iTxtId']

        nd_list = self.panel.list_emote
        for index, (item_id, item_count) in enumerate(self.emote_item_list):
            item = nd_list.GetItem(index)
            item.lab_reward.SetString(emote_text_map[item_id])

        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.refresh_item_info,
           'receive_task_reward_succ_event': self._on_update_reward,
           'receive_lottery_result': self.on_receive_lottery_result
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        super(ActivityKizunaAISupportGroup, self).on_finalize_panel()
        parent = global_data.ui_mgr.get_ui('ActivityKizunaAIMainUI')
        parent and parent.panel.nd_shadow.setVisible(False)

    def refresh_cheer_light_card_count(self):
        nd_remain = self.panel.lab_remain.temp_price
        remain_card_count = global_data.player.get_item_num_by_no(SHOP_PAYMENT_KIZUNA_AI_CHEER_LIGHT_CARD)
        price_info = {'goods_payment': SHOP_PAYMENT_ITEM_KIZUNA_AI_CHEER_LIGHT_CARD,
           'original_price': remain_card_count,
           'real_price': remain_card_count
           }
        splice_price(nd_remain, [price_info], is_or=False, color=DARK_PRICE_COLOR)
        nd_price = self.panel.btn_start.temp_price
        splice_price(nd_price, [self.emote_price_info], is_or=False, color=DARK_PRICE_COLOR)
        self.panel.btn_start.SetEnable(remain_card_count >= self.emote_price_info['real_price'] and self.emote_own_count < self.common_emote_count)

    def on_receive_lottery_result(self, item_list, origin_list, extra_data):
        global_data.ui_mgr.close_ui('ScreenLockerUI')
        global_data.emgr.receive_award_succ_event_from_lottery.emit(item_list, origin_list)

    def refresh_emote_own_state(self):
        nd_list = self.panel.list_emote
        own_count = 0
        for index, (item_id, item_count) in enumerate(self.emote_item_list):
            item = nd_list.GetItem(index)
            own = global_data.player.get_item_num_by_no(int(item_id)) > 0
            item.pnl_get.setVisible(own)
            if own:
                own_count += 1

        if global_data.player.get_item_num_by_no(SPECIAL_EMOTE_ITEM_ID) > 0:
            self.panel.temp_emote_rare.pnl_get.setVisible(True)
            own_count += 1
        elif own_count == self.common_emote_count:
            global_data.player.receive_task_reward(SPECIAL_EMOTE_TASK_ID)
        self.emote_own_count = own_count

    def refresh_item_info(self):
        self.refresh_emote_own_state()
        self.refresh_cheer_light_card_count()

    def check_special_emote_task_prog(self, task_id):
        if task_id == SPECIAL_EMOTE_TASK_ID:
            if self.emote_own_count >= self.common_emote_count:
                global_data.player.receive_task_reward(SPECIAL_EMOTE_TASK_ID)
        elif task_id == KIZUNA_AI_SHARE_TASK_ID:
            self._on_update_reward()

    def _set_item_widget_lab_num(self, item_widget, total_times, cur_times):
        if cur_times == total_times:
            item_widget.lab_num.SetString('<color=0x73bb0cff>{0}</color><color=0x7982acff>/{1}</color>'.format(cur_times, total_times))
        else:
            item_widget.lab_num.SetString('{0}/{1}'.format(cur_times, total_times))

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
            can_receive_reward_a = global_data.player.is_task_reward_receivable(task_id_a)
            can_receive_reward_b = global_data.player.is_task_reward_receivable(task_id_b)
            if can_receive_reward_a or can_receive_reward_b:
                if can_receive_reward_a:
                    return -1
                if can_receive_reward_b:
                    return 1
                return 0
            has_rewarded_a = global_data.player.has_receive_reward(task_id_a)
            has_rewarded_b = global_data.player.has_receive_reward(task_id_b)
            if has_rewarded_a != has_rewarded_b:
                if has_rewarded_a:
                    return 1
                if has_rewarded_b:
                    return -1
            return 0

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list

    def refresh_list(self):
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i)
            total_times = get_total_prog(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            self._set_item_widget_lab_num(item_widget, total_times, cur_times)
            btn = item_widget.temp_btn_get.btn_common
            item_widget.nd_get.setVisible(False)

            def check_btn(btn=btn, task_id=task_id):
                has_rewarded = global_data.player.has_receive_reward(task_id)
                if has_rewarded:
                    item_widget.nd_get.setVisible(True)
                    btn.setVisible(False)
                elif cur_times < total_times:
                    btn.setVisible(True)
                    jump_conf = get_jump_conf(task_id)
                    if jump_conf:
                        btn.SetText(80284)
                        btn.SetTextColor('#SK', '#SK', '#SK')
                        btn.SetFrames('', [PIC0, PIC0, PIC2], False, None)
                        btn.SetEnable(True)
                    else:
                        btn.SetTextColor('#SK', '#SK', '#SK')
                        btn.SetEnable(False)
                        btn.SetText(604030)
                else:
                    btn.SetTextColor('#SK', '#SK', '#SK')
                    btn.SetFrames('', [PIC1, PIC1, PIC2], False, None)
                    btn.setVisible(True)
                    btn.SetEnable(True)
                    btn.SetText(604030)
                return

            @btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not is_activity_in_limit_time(self._activity_type):
                    return
                _total_times = get_total_prog(task_id)
                _cur_times = global_data.player.get_task_prog(task_id)
                jump_conf = get_jump_conf(task_id)
                if _cur_times < _total_times:
                    exec_jump_to_ui_info(jump_conf)
                else:
                    global_data.player.receive_task_reward(task_id)
                    btn.SetText(80866)
                    btn.SetEnable(False)

            check_btn()