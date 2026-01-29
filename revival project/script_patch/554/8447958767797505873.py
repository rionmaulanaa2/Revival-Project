# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAnnivExchange.py
from __future__ import absolute_import
import six_ex
from six.moves import zip
from six.moves import range
from functools import cmp_to_key
from logic.comsys.activity.ActivityExchange import ActivityExchange
from logic.gutils import activity_utils
from logic.gutils import mall_utils
from logic.gutils import task_utils
from logic.gutils import item_utils
from logic.gutils import template_utils
from common.cfg import confmgr
import logic.gcommon.const as gconst
from logic.gcommon.item import item_const as iconst
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2, NormalConfirmUI2
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.const import SHOP_ITEM_YUANBAO
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
from logic.client.const import mall_const
ICON_PLUS = 'gui/ui_res_2/activity/activity_resource/icon_plus_task.png'
ICON_ARROW = 'gui/ui_res_2/activity/activity_resource/icon_arrow_task.png'
GOODS_ID_LIST_MILA_SKIN_XINGYUAN = [
 '690116221', '690116225']
GOODS_ID_SKIN_PRINCESS_MILA = '690116220'
BOW_CNT_INTERVAL_LIST = [
 65, 40, 20, 0]
AVAILABLE_GOODS_ID_LIST = [690116216, 690116218, 690116219, 690116220]

class ActivityAnnivExchange(ActivityExchange):

    def on_init_panel(self):
        super(ActivityAnnivExchange, self).on_init_panel()
        skin_name = item_utils.get_lobby_item_name(iconst.ITEM_NO_SKIN_PRINCESS_MILA)
        self.panel.img_name.SetString(skin_name)
        self.refresh_bow_cnt()
        self.init_price_widget()
        self.init_btn_go()

        @self.panel.btn_role.unique_callback()
        def OnClick(btn, touch):
            jump_to_display_detail_by_item_no(iconst.ITEM_NO_SKIN_PRINCESS_MILA)

        @self.panel.btn_go.unique_callback()
        def OnClick(btn, touch):
            self.highlight_item_by_goods_id(goods_id=GOODS_ID_SKIN_PRINCESS_MILA)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.buy_good_success,
           'on_lobby_bag_item_changed_event': self.refresh_bow_cnt
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def set_show(self, show, is_init=False):
        super(ActivityAnnivExchange, self).set_show(show, is_init)
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
            extra_params = task_utils.get_task_arg(task_id_a)
            goods_id_a = str(extra_params.get('goodsid', ''))
            sort_id_a = int(extra_params.get('sort_id', 999))
            extra_params = task_utils.get_task_arg(task_id_b)
            goods_id_b = str(extra_params.get('goodsid', ''))
            sort_id_b = int(extra_params.get('sort_id', 999))
            left_num_a, max_num = (1, 0)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id_a)
            if num_info:
                left_num_a, max_num = num_info
                if mall_utils.item_has_owned_by_goods_id(goods_id_a):
                    left_num_a = 0
            left_num_b, max_num = (1, 0)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id_b)
            if num_info:
                left_num_b, max_num = num_info
                if mall_utils.item_has_owned_by_goods_id(goods_id_b):
                    left_num_b = 0
            enough_a = left_num_a > 0
            enough_b = left_num_b > 0
            if enough_a != enough_b:
                if enough_a:
                    return -1
                if enough_b:
                    return 1
            if enough_a == enough_b:
                if not enough_a:
                    return six_ex.compare(int(task_id_a), int(task_id_b))
                else:
                    return six_ex.compare(sort_id_a, sort_id_b)

            return six_ex.compare(int(task_id_a), int(task_id_b))

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list

    def show_list(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        parent_task = task_list[0]
        children_tasks = task_utils.get_children_task(parent_task)
        children_tasks = self.reorder_task_list(children_tasks)
        self._children_tasks = children_tasks
        sub_act_list = self.panel.act_list
        sub_act_list.SetTemplate('activity/i_task_exchange')
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(children_tasks))
        ui_data = conf.get('cUiData', {})
        for i, task_id in enumerate(children_tasks):
            item_widget = sub_act_list.GetItem(i)
            extra_params = task_utils.get_task_arg(task_id)
            goods_id = str(extra_params.get('goodsid', ''))
            if not goods_id:
                continue
            prices_list = mall_utils.get_mall_item_price_list(goods_id)
            if not prices_list:
                continue
            target_item_no = mall_utils.get_goods_item_no(goods_id)
            target_item_num = mall_utils.get_goods_num(goods_id)
            if len(prices_list) == 4:
                cost_item_no_a = prices_list[0]
                cost_item_no_b = prices_list[2]
                template_utils.init_tempate_mall_i_item(item_widget.temp_fragment, cost_item_no_a, show_tips=True)
                template_utils.init_tempate_mall_i_item(item_widget.temp_reward, cost_item_no_b, show_tips=True)
                template_utils.init_tempate_mall_i_item(item_widget.temp_reward_2, target_item_no, target_item_num, show_tips=True)
                if goods_id in GOODS_ID_LIST_MILA_SKIN_XINGYUAN:
                    item_widget.temp_reward_2.nd_xingyuan.setVisible(True)
                else:
                    item_widget.temp_reward_2.nd_xingyuan.setVisible(False)
                item_widget.img_arrow_1.SetDisplayFrameByPath('', ICON_PLUS)
                item_widget.img_arrow_2.SetDisplayFrameByPath('', ICON_ARROW)
                item_widget.img_arrow_1.setVisible(True)
                item_widget.img_arrow_2.setVisible(True)
                item_widget.temp_fragment.setVisible(True)
                item_widget.temp_reward.setVisible(True)
                item_widget.temp_reward_2.setVisible(True)
            elif len(prices_list) == 2:
                cost_item_no = prices_list[0]
                template_utils.init_tempate_mall_i_item(item_widget.temp_fragment, cost_item_no, show_tips=True)
                template_utils.init_tempate_mall_i_item(item_widget.temp_reward, target_item_no, target_item_num, show_tips=True)
                if goods_id in GOODS_ID_LIST_MILA_SKIN_XINGYUAN:
                    item_widget.temp_reward.nd_xingyuan.setVisible(True)
                else:
                    item_widget.temp_reward.nd_xingyuan.setVisible(False)
                item_widget.img_arrow_1.SetDisplayFrameByPath('', ICON_ARROW)
                item_widget.img_arrow_1.setVisible(True)
                item_widget.img_arrow_2.setVisible(False)
                item_widget.temp_fragment.setVisible(True)
                item_widget.temp_reward.setVisible(True)
                item_widget.temp_reward_2.setVisible(False)
            else:
                log_error('ActivityAnnivExchange unsupport price_list!')
                return
            do_remind = [
             global_data.player.has_exchange_reminder(goods_id)]

            @item_widget.btn_tick.unique_callback()
            def OnClick(btn, touch, do_remind=do_remind, goods_id=goods_id):
                do_remind[0] = not do_remind[0]
                btn.SetSelect(do_remind[0])
                global_data.player.add_exchange_reminder(goods_id, do_remind[0])

            item_widget.btn_tick.SetSelect(do_remind[0])
            if ui_data.get('lab_tips_color'):
                color = int(ui_data.get('lab_tips_color'), 16)
                item_widget.lab_tips.SetColor(color)
            if ui_data.get('lab_num_color'):
                color = int(ui_data.get('lab_num_color'), 16)
                item_widget.lab_num.SetColor(color)

        self.refresh_list()

    def refresh_list(self):
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i)
            extra_params = task_utils.get_task_arg(task_id)
            if not extra_params:
                continue
            goods_id = str(extra_params.get('goodsid', ''))
            if not goods_id:
                continue
            prices_list = mall_utils.get_mall_item_price_list(goods_id)
            if not prices_list:
                continue
            limit_left_num = 1
            left_num, max_num = (0, 0)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id)
            if num_info:
                left_num, max_num = num_info
                if mall_utils.item_has_owned_by_goods_id(goods_id):
                    left_num = 0
                limit_left_num = left_num
                item_widget.lab_num.SetString(get_text_by_id(607018).format(left_num, max_num))
            else:
                item_widget.lab_num.SetString('')
            if len(prices_list) == 4:
                cost_item_no_a = prices_list[0]
                cost_item_no_b = prices_list[2]
                cost_item_amount_a = global_data.player.get_item_num_by_no(int(cost_item_no_a))
                cost_item_amount_b = global_data.player.get_item_num_by_no(int(cost_item_no_b))
                cost_item_num_a = prices_list[1]
                cost_item_num_b = prices_list[3]
                cost_str_a = self.get_cost_str(cost_item_amount_a, cost_item_num_a)
                cost_str_b = self.get_cost_str(cost_item_amount_b, cost_item_num_b)
                item_widget.temp_fragment.lab_quantity.SetString(cost_str_a)
                item_widget.temp_reward.lab_quantity.SetString(cost_str_b)
                item_widget.temp_fragment.lab_quantity.setVisible(True)
                item_widget.temp_reward.lab_quantity.setVisible(True)
            elif len(prices_list) == 2:
                cost_item_no = prices_list[0]
                cost_item_amount = global_data.player.get_item_num_by_no(int(cost_item_no))
                cost_item_num = prices_list[1]
                cost_str = self.get_cost_str(cost_item_amount, cost_item_num)
                item_widget.temp_fragment.lab_quantity.SetString(cost_str)
                item_widget.temp_fragment.lab_quantity.setVisible(True)
            btn = item_widget.temp_btn_get.btn_common

            def check_btn(btn=btn, left_num=left_num, goods_id=goods_id, max_num=max_num):
                if limit_left_num <= 0:
                    item_widget.nd_get.setVisible(True)
                    btn.setVisible(False)
                    return
                btn.setVisible(True)
                item_widget.nd_get.setVisible(False)
                enable = left_num > 0 and mall_utils.check_item_money_list(prices_list)
                if mall_utils.item_has_owned_by_goods_id(goods_id):
                    enable = False
                btn.SetEnable(enable)

            @btn.unique_callback()
            def OnClick(btn, touch, goods_id=goods_id, left_num=left_num):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                self.hide_highlight_effect()
                if mall_utils.item_has_owned_by_goods_id(goods_id):
                    global_data.game_mgr.show_tip(get_text_by_id(607175))
                    return
                if goods_id in GOODS_ID_LIST_MILA_SKIN_XINGYUAN and not mall_utils.item_has_owned_by_item_no(iconst.ITEM_NO_SKIN_PRINCESS_MILA):
                    NormalConfirmUI2(content=get_text_by_id(609205))
                else:
                    self.do_exchange(goods_id, left_num)

            check_btn()

    def get_cost_str(self, have_cnt, need_cnt):
        if have_cnt >= need_cnt:
            return '#DB{0}#n'.format(need_cnt)
        else:
            return '#SR{0}#n'.format(need_cnt)

    def refresh_bow_cnt(self):
        ui = global_data.ui_mgr.get_ui('ActivityAnnivMainUI')
        page_tab_widget = ui.get_page_tab_widget()
        if page_tab_widget:
            cur_view_sub_page_widget = page_tab_widget.get_cur_view_sub_page_widget()
            if cur_view_sub_page_widget:
                cur_view_sub_page_widget.refresh_bow_cnt()

    def do_exchange(self, goods_id, _left_num):
        price_list = mall_utils.get_mall_item_price_list(goods_id)
        item_consumed_count = len(price_list)
        item_consumed_count /= 2
        yuanbao_consumed_cnt = 0
        bow_consumed_cnt = 0
        for i in range(item_consumed_count):
            item_no = price_list[i * 2]
            if item_no == SHOP_ITEM_YUANBAO:
                num = global_data.player.get_item_money(item_no)
                yuanbao_consumed_cnt = price_list[i * 2 + 1]
                from logic.gutils.mall_utils import check_yuanbao
                if not check_yuanbao(yuanbao_consumed_cnt):
                    return

        for i in range(item_consumed_count):
            item_no = price_list[i * 2]
            if item_no != SHOP_ITEM_YUANBAO:
                num = global_data.player.get_item_money(item_no)
                bow_consumed_cnt = price_list[i * 2 + 1]
                if num < price_list[i * 2 + 1]:
                    global_data.game_mgr.show_tip(get_text_by_id(607180))
                    return

        left_num = 0
        _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id)
        if num_info:
            left_num, _ = num_info
        from logic.comsys.mall_ui import BuyConfirmUIInterface
        if not activity_utils.is_activity_in_limit_time(self._activity_type):
            return
        if left_num > 1:
            BuyConfirmUIInterface.groceries_buy_confirmUI(goods_id)
        else:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            dlg = SecondConfirmDlg2()

            def on_confirm():
                dlg.close()
                global_data.player.buy_goods(goods_id, 1, gconst.SHOP_PAYMENT_ITEM)

            name = mall_utils.get_goods_name(goods_id)
            c = ''
            if yuanbao_consumed_cnt == 0:
                c = get_text_by_id(609199).format(x=bow_consumed_cnt, z=name)
            elif bow_consumed_cnt == 0:
                c = get_text_by_id(609198).format(x=yuanbao_consumed_cnt, z=name)
            else:
                c = get_text_by_id(609195).format(x=yuanbao_consumed_cnt, y=bow_consumed_cnt, z=name)
            dlg.confirm(content=c, confirm_callback=on_confirm)

    def highlight_item_by_goods_id(self, goods_id=None):
        self.hide_highlight_effect()
        if goods_id is None:
            goods_id = self.get_available_goods_id_by_bow_cnt()
        idx = self.get_index_in_list_by_goods_id(goods_id)
        self.show_highlight_effect(idx)
        return

    def show_highlight_effect(self, idx):
        sub_act_list = self.panel.act_list
        if sub_act_list is None:
            return
        else:
            if idx < 0 or idx >= sub_act_list.GetItemCount():
                return
            sub_act_list.LocatePosByItem(idx)
            item = sub_act_list.GetItem(idx)
            item.img_light.setVisible(True)
            item.PlayAnimation('light')
            return

    def hide_highlight_effect(self):
        if not self.panel.act_list:
            return
        item_list = self.panel.act_list.GetAllItem()
        for item in item_list:
            if item.IsPlayingAnimation('light'):
                item.StopAnimation('light')
            item.img_light.setVisible(False)

    def get_index_in_list_by_goods_id(self, goods_id):
        for idx, task_id in enumerate(self._children_tasks):
            extra_params = task_utils.get_task_arg(task_id)
            if not extra_params:
                continue
            cur_goods_id = str(extra_params.get('goodsid', ''))
            if not cur_goods_id:
                continue
            if str(goods_id) != str(cur_goods_id):
                continue
            return idx

    def get_available_goods_id_by_bow_cnt(self):
        cur_bow_cnt = global_data.player.get_item_num_by_no(iconst.ITEM_NO_MILA_BOW)
        for bow_cnt, goods_id in zip(BOW_CNT_INTERVAL_LIST, AVAILABLE_GOODS_ID_LIST):
            if cur_bow_cnt >= bow_cnt:
                return goods_id

        return AVAILABLE_GOODS_ID_LIST[0]

    def init_price_widget(self):
        self.price_widget = PriceUIWidget(self.panel, call_back=None, list_money_node=self.panel.list_price)
        self.price_widget.show_money_types([SHOP_PAYMENT_YUANBAO])
        return

    def init_btn_go(self):
        if mall_utils.item_has_owned_by_item_no(iconst.ITEM_NO_SKIN_PRINCESS_MILA):
            self.panel.btn_go.setVisible(False)
            return
        self.panel.btn_go.setVisible(True)
        prices = mall_utils.get_mall_item_price(GOODS_ID_SKIN_PRINCESS_MILA)
        if len(prices) > 0:
            prices[0].update({'goods_payment': SHOP_PAYMENT_YUANBAO
               })
        template_utils.splice_price(self.panel.btn_go.temp_price, prices, color=mall_const.NO_RED_DARK_PRICE_COLOR)