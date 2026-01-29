# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGranbelmGift.py
from __future__ import absolute_import
from logic.gutils import task_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import template_utils
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils import item_utils
import logic.gcommon.const as gconst
import logic.gcommon.time_utility as tutil
from cocosui import cc, ccui, ccs
from logic.gutils import mall_utils
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
from logic.client.const.mall_const import DARK_PRICE_COLOR, DEF_PRICE_COLOR
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityGranbelmGift(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityGranbelmGift, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            log_error('[ERROR] activity [%s] task has no children task', activity_type)
            return
        self._parent_task_id = task_list[0]
        children_task_list = task_utils.get_children_task(self._parent_task_id)
        if len(children_task_list) < 3:
            log_error('[ERROR] activity [%s] children_task_list[%s] not enough.', activity_type, children_task_list)
            return
        self._gift_task_first = children_task_list[1]
        self._gift_task_second = children_task_list[0]
        self._gift_task_second_limit = children_task_list[2]
        self.select_idx = 0
        if global_data.lobby_mall_data and global_data.player:
            self.goods_info_1 = global_data.lobby_mall_data.get_activity_sale_info('GRANBELM_1_GOODS')
            self.goods_info_30 = global_data.lobby_mall_data.get_activity_sale_info('GRANBELM_30_GOODS')

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        pass

    def on_init_panel(self):
        self.panel.StopAnimation('choose1')
        self.panel.StopAnimation('choose2')
        self.panel.StopAnimation('loop1')
        self.panel.StopAnimation('loop2')
        self.panel.RecoverAnimationNodeState('choose1')
        self.panel.RecoverAnimationNodeState('choose2')
        self.panel.RecoverAnimationNodeState('loop1')
        self.panel.RecoverAnimationNodeState('loop2')
        self.panel.RecordAnimationNodeState('choose1')
        self.panel.RecordAnimationNodeState('choose2')
        self.panel.RecordAnimationNodeState('loop1')
        self.panel.RecordAnimationNodeState('loop2')
        self.panel.PlayAnimation('show')
        conf = confmgr.get('c_activity_config', self._activity_type)
        start_date = tutil.get_date_str('%Y.%m.%d', conf.get('cBeginTime', 0))
        finish_date = tutil.get_date_str('%m.%d', conf.get('cEndTime', 0))
        self.panel.lab_time.SetString(get_text_by_id(604006).format(start_date, finish_date))
        self.panel.lab_tips.SetString(get_text_by_id(607207))
        self._update_gift_task_first_ui()
        self._update_gift_task_second_ui()
        self.panel.lab_preview.setVisible(True)
        self.panel.nd_preview.setVisible(False)

        @self.panel.btn_tips.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(conf.get('cNameTextID', '')), get_text_by_id(conf.get('cRuleTextID', '')))
            x, y = btn.GetPosition()
            wpos = btn.GetParent().ConvertToWorldSpace(x, y)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
            template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

    def _on_update_task_progress(self, task_id):
        if task_id == self._gift_task_first:
            self._update_gift_task_first_ui()
        else:
            self._update_gift_task_second_ui()

    def _get_task_goods_id(self, task_id):
        arg = task_utils.get_task_arg(task_id)
        goods_id = str(arg.get('goods_id', 0))
        return goods_id

    def _update_gift_task_first_ui(self):
        total_prog = task_utils.get_total_prog(self._gift_task_first)
        cur_prog = global_data.player.get_task_prog(self._gift_task_first)
        day_left_prog = total_prog - cur_prog
        self.panel.nd_gift_1.btn_gift_1.lab_tips_1.SetString(get_text_by_id(608419).format(day_left_prog, total_prog))
        self.panel.nd_gift_1.btn_gift_choose_1.lab_tips_1.SetString(get_text_by_id(608419).format(day_left_prog, total_prog))
        goods_id = self._get_task_goods_id(self._gift_task_first)
        self.panel.lab_name_1.SetString(get_text_by_id(607209))
        self.panel.nd_gift_1.btn_buy_1.lab_origin_1.SetString(get_text_by_id(608421))
        if self.goods_info_30:
            if mall_utils.is_pc_global_pay() or mall_utils.is_steam_pay():
                price_txt = mall_utils.get_pc_charge_price_str(self.goods_info_30)
            else:
                price_txt = mall_utils.get_charge_price_str(self.goods_info_30['goodsid'])
        else:
            price_txt = '******'
        self.panel.nd_gift_1.btn_buy_1.lab_price_1.SetString(mall_utils.adjust_price(str(price_txt)))
        if day_left_prog > 0 and self.goods_info_30:
            self.panel.btn_buy_1.SetEnable(True)

            @self.panel.btn_buy_1.unique_callback()
            def OnClick(btn, touch, *args):
                if mall_utils.is_pc_global_pay():
                    from logic.gutils.jump_to_ui_utils import jump_to_web_charge
                    jump_to_web_charge()
                else:
                    global_data.player and global_data.player.pay_order(self.goods_info_30['goodsid'])

        else:
            self.panel.btn_buy_1.SetEnable(False)

        @self.panel.btn_gift_1.unique_callback()
        def OnClick(btn, touch):
            if self.select_idx == 1:
                return
            self.select_idx = 1
            self.panel.lab_preview.setVisible(False)
            self.panel.nd_preview.setVisible(True)
            self.panel.StopAnimation('loop2')
            self.panel.StopAnimation('choose2')
            self.panel.RecoverAnimationNodeState('choose2')
            self.panel.RecoverAnimationNodeState('choose1')
            self.panel.RecoverAnimationNodeState('loop1')
            self.panel.PlayAnimation('choose1')
            self.panel.PlayAnimation('loop1')
            self._update_goods_preview(goods_id)

    def _update_gift_task_second_ui(self):
        total_prog = task_utils.get_total_prog(self._gift_task_second)
        cur_prog = global_data.player.get_task_prog(self._gift_task_second)
        day_left_prog = total_prog - cur_prog
        self.panel.nd_gift_2.btn_gift_2.lab_tips_2.SetString(get_text_by_id(607205).format(day_left_prog, total_prog))
        self.panel.nd_gift_2.btn_gift_choose_2.lab_tips_2.SetString(get_text_by_id(607205).format(day_left_prog, total_prog))
        goods_id = self._get_task_goods_id(self._gift_task_second)
        self.panel.lab_name_2.SetString(get_text_by_id(607208))
        self.panel.nd_gift_2.btn_buy_2.lab_origin_2.SetString(get_text_by_id(608420))
        total_prog = task_utils.get_total_prog(self._gift_task_second_limit)
        cur_prog = global_data.player.get_task_prog(self._gift_task_second_limit)
        total_left_prog = total_prog - cur_prog
        self.panel.nd_gift_2.btn_gift_2.nd_num.lab_last.SetString(get_text_by_id(607206).format(total_left_prog))
        self.panel.nd_gift_2.btn_gift_choose_2.nd_num.lab_last.SetString(get_text_by_id(607206).format(total_left_prog))
        if self.goods_info_1:
            if mall_utils.is_pc_global_pay() or mall_utils.is_steam_pay():
                price_txt = mall_utils.get_pc_charge_price_str(self.goods_info_1)
            else:
                price_txt = mall_utils.get_charge_price_str(self.goods_info_1['goodsid'])
        else:
            price_txt = '******'
        self.panel.nd_gift_2.btn_buy_2.lab_price_2.SetString(mall_utils.adjust_price(str(price_txt)))
        if day_left_prog > 0 and total_left_prog > 0 and self.goods_info_1:
            self.panel.btn_buy_2.SetEnable(True)

            @self.panel.btn_buy_2.unique_callback()
            def OnClick(btn, touch):
                if mall_utils.is_pc_global_pay():
                    from logic.gutils.jump_to_ui_utils import jump_to_web_charge
                    jump_to_web_charge()
                else:
                    global_data.player and global_data.player.pay_order(self.goods_info_1['goodsid'])

        else:
            self.panel.btn_buy_2.SetEnable(False)

        @self.panel.btn_gift_2.unique_callback()
        def OnClick(btn, touch):
            if self.select_idx == 2:
                return
            self.select_idx = 2
            self.panel.lab_preview.setVisible(False)
            self.panel.nd_preview.setVisible(True)
            self.panel.StopAnimation('loop1')
            self.panel.StopAnimation('choose1')
            self.panel.RecoverAnimationNodeState('choose1')
            self.panel.RecoverAnimationNodeState('choose2')
            self.panel.RecoverAnimationNodeState('loop2')
            self.panel.PlayAnimation('choose2')
            self.panel.PlayAnimation('loop2')
            self._update_goods_preview(goods_id)

    def _update_goods_preview(self, goods_id):
        self.panel.nd_preview.lab_name.SetString(mall_utils.get_goods_name(goods_id))
        list_item = self.panel.nd_preview.list_item
        reward_id = mall_utils.get_goods_item_reward_id(goods_id)
        if reward_id <= 0:
            list_item and list_item.setVisible(False)
            return
        list_item.setVisible(True)
        template_utils.init_common_reward_list(list_item, reward_id)