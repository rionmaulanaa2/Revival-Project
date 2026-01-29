# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryCNValentineWidget.py
from __future__ import absolute_import
from .LotteryCommonTurntableWidget import LotteryCommonTurntableWidget
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
from common.utils.timer import CLOCK
from logic.client.const.mall_const import REDCILFF_PRICE_COLOR, DARK_PRICE_COLOR, USE_TEMPLATE_COLOR
import cc
import copy
from logic.gutils.task_utils import get_task_reward
import common.cfg.confmgr as confmgr
from logic.gutils.item_utils import get_lobby_item_type
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_LOTTERY_TICKET, L_ITEM_TYPE_HEAD
SHOW_TIP_KEY = 'lottery_turntable_tip_{}'

class LotteryCNValentineWidget(LotteryCommonTurntableWidget):

    def refresh_task_reward_status(self, task_id):
        if 'bind_task_id' in self.data:
            if task_id != self.data['bind_task_id']:
                return
            task_reward_status = global_data.player.get_task_reward_status(self.data['bind_task_id'])
            self.panel.lab_btn_bones_name.SetString(self.text_id_map[task_reward_status])
            self.panel.btn_reward.red_point.setVisible(task_reward_status == ITEM_UNRECEIVED)
            self.panel.btn_reward.img_got_mask.setVisible(task_reward_status == ITEM_RECEIVED)
            if task_reward_status == ITEM_UNRECEIVED:
                self.panel.PlayAnimation('bones_get')
            else:
                self.panel.StopAnimation('bones_get')
                self.panel.RecoverAnimationNodeState('bones_get')
        if 'exclusive_gift' in self.data:
            task_list = self.data['exclusive_gift'].get('task_list', [])
            self.panel.btn_bones.red_point.setVisible(False)
            for task_id in task_list:
                task_reward_status = global_data.player.get_task_reward_status(task_id)
                if task_reward_status == ITEM_UNRECEIVED:
                    self.panel.btn_bones.red_point.setVisible(True)
                    return

        else:
            self.panel.btn_bones.setVisible(False)
            self.panel.nd_tips.setVisible(False)

    def _set_task_reward_tips_visible(self, flag, from_timer=False):
        self.panel.nd_tips.setVisible(flag)
        if flag:
            self.panel.PlayAnimation('tips_show')
            self.panel.PlayAnimation('tips_loop')
        else:
            self.panel.StopAnimation('tips_show')
            self.panel.StopAnimation('tips_loop')
            if not from_timer:
                global_data.game_mgr.unregister_logic_timer(self.task_reward_tips_timer)
            self.task_reward_tips_timer = None
        return

    def init_parameters(self):
        super(LotteryCNValentineWidget, self).init_parameters()
        self.task_reward_tips_timer = None
        self.price_color = copy.deepcopy(USE_TEMPLATE_COLOR)
        self.text_id_map = {ITEM_UNGAIN: self.data.get('extra_data', {}).get('left_top_text_id', 609866),
           ITEM_UNRECEIVED: 81708,
           ITEM_RECEIVED: 80866
           }
        self.show_tip_key = SHOW_TIP_KEY.format(self.lottery_id)
        return

    def init_panel(self):
        super(LotteryCNValentineWidget, self).init_panel()
        if self.panel.btn_question:

            @global_unique_click(self.panel.btn_question)
            def OnClick(btn, touch):
                dlg = GameRuleDescUI()
                title, content = self.data.get('rule_desc', [608080, 608081])
                dlg.set_lottery_rule(title, content)

        self.panel.RecordAnimationNodeState('bones_get')
        if 'bind_task_id' in self.data:
            self.refresh_task_reward_status(self.data['bind_task_id'])

            @global_unique_click(self.panel.btn_reward)
            def OnClick(btn, touch):
                self.panel.nd_tips.setVisible(False)
                global_data.achi_mgr.set_cur_user_archive_data(self.show_tip_key, 0)
                task_id = self.data['bind_task_id']
                task_reward_status = global_data.player.get_task_reward_status(task_id)
                if task_reward_status == ITEM_UNRECEIVED:
                    global_data.player.receive_task_reward(task_id)
                    self.panel.btn_reward.red_point.setVisible(False)
                else:
                    reward_list = confmgr.get('common_reward_data', str(get_task_reward(task_id)), 'reward_list', default=None)
                    reward_item, num = reward_list[0]
                    bind_item_no = self.data.get('extra_data', {}).get('btn_reward_bind_item_no')
                    if bind_item_no and reward_item == bind_item_no:
                        dlg = GameRuleDescUI()
                        title_text_id = self.data.get('extra_data', {}).get('btn_reward_title_text_id')
                        content_text_id = self.data.get('extra_data', {}).get('btn_reward_content_text_id')
                        dlg.set_show_rule(title_text_id, content_text_id)
                        dlg.set_node_pos(btn.getPosition(), cc.Vec2(-0.1, 1.1))
                    else:
                        global_data.emgr.show_item_desc_ui_event.emit(reward_item, None, btn.getPosition(), item_num=num)
                return

            show_tip = global_data.achi_mgr.get_cur_user_archive_data(self.show_tip_key, default=1)
            self.panel.nd_tips.setVisible(bool(show_tip))
            if show_tip:
                self.panel.runAction(cc.Sequence.create([
                 cc.DelayTime.create(30),
                 cc.CallFunc.create(lambda : self.panel.nd_tips.setVisible(False))]))
        if 'exclusive_gift' in self.data:
            self.refresh_task_reward_status(None)

            @global_unique_click(self.panel.btn_bones)
            def OnClick(btn, touch):
                self.panel.nd_tips.setVisible(False)
                global_data.achi_mgr.set_cur_user_archive_data(self.show_tip_key, 0)
                from logic.comsys.lottery.LotteryExclusiveGiftUI import LotteryExclusiveGiftUI
                gift_template = self.data['exclusive_gift'].get('gift_template', '')
                LotteryExclusiveGiftUI(None, self.data['exclusive_gift'], gift_template=gift_template)
                return

            show_tip = global_data.achi_mgr.get_cur_user_archive_data(self.show_tip_key, default=1)
            self.panel.nd_tips.setVisible(bool(show_tip))
            if show_tip:
                self.panel.runAction(cc.Sequence.create([
                 cc.DelayTime.create(30),
                 cc.CallFunc.create(lambda : self.panel.nd_tips.setVisible(False))]))
        else:
            self.panel.btn_bones.setVisible(False)
            self.panel.nd_tips.setVisible(False)
        return

    def get_event_conf(self):
        econf = super(LotteryCNValentineWidget, self).get_event_conf()
        econf.update({'buy_good_success': self.refresh_bind_task_red_point,
           'receive_task_reward_succ_event': self.refresh_task_reward_status
           })
        return econf

    def on_finalize_panel(self):
        super(LotteryCNValentineWidget, self).on_finalize_panel()
        self.price_color = None
        if self.task_reward_tips_timer:
            global_data.game_mgr.unregister_logic_timer(self.task_reward_tips_timer)
            self.task_reward_tips_timer = None
        return

    def refresh_bind_task_red_point(self, *args):
        if 'bind_task_id' in self.data:
            self.refresh_task_reward_status(self.data['bind_task_id'])