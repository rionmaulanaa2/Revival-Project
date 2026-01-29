# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/ChargeWidget.py
from __future__ import absolute_import
from logic.gutils import mall_utils
from logic.gutils import jump_to_ui_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc

class ChargeWidget(object):
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_back_btn'
       }
    UP_MAX_NUM = 4

    def on_init_panel(self, panel):
        self.panel = panel
        self.is_pc_global_pay = mall_utils.is_pc_global_pay()
        self.init_event()
        self.init_widget()
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time('ChargeUINew', self.__class__.__name__)

    def init_event(self):
        global_data.emgr.update_charge_info += self.init_charge_list
        global_data.emgr.pay_order_succ_event += self.init_charge_list

    def on_finalize_panel(self):
        self.panel = None
        global_data.emgr.update_charge_info -= self.init_charge_list
        global_data.emgr.pay_order_succ_event -= self.init_charge_list
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time('ChargeUINew', self.__class__.__name__)
        return

    def set_show(self, show):
        self.panel.setVisible(show)

    def init_widget(self):
        if self.is_pc_global_pay:
            self.panel.lab_charge_tips.setVisible(self.is_pc_global_pay)

            @self.panel.temp_charge.btn_common.unique_callback()
            def OnClick(btn, touch):
                jump_to_ui_utils.jump_to_web_charge()

        if not self.is_pc_global_pay:
            self.init_tips_widget()
        ac_list = [
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(lambda : self.init_charge_list())]
        self.panel.runAction(cc.Sequence.create(ac_list))
        nd_tips_charge = self.panel.nd_tips_charge
        if nd_tips_charge:
            from logic.gcommon.time_utility import get_server_time
            cur_time = get_server_time()
            show_charge_tip = 1671033600 <= cur_time <= 1672866000
            self.panel.nd_tips_charge.setVisible(show_charge_tip)
            if show_charge_tip:
                self.panel.lab_tips_charge.SetString(610327 if cur_time < 1672243200 else 610329)

    def init_tips_widget(self):
        if not self.panel.hint:
            return
        self.panel.hint.setVisible(G_IS_NA_USER)
        self.panel.nd_tips_cn.setVisible(not G_IS_NA_USER)

        @self.panel.nd_tips_cn.btn_recharge_tips.unique_callback()
        def OnClick(*args):
            dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(82015, 82014)

    def init_charge_list(self):
        if not self.panel or not global_data.lobby_mall_data:
            return
        import copy
        charge_info_list = global_data.lobby_mall_data.get_charge_info()
        if not charge_info_list:
            global_data.lobby_mall_data.request_charge_info()
            return
        if self.is_pc_global_pay:
            for index, pay_item_data in enumerate(charge_info_list):
                key = pay_item_data['goodsid']
                nd = getattr(self.panel, 'diamond_quantity%d' % (index + 1))
                if nd:
                    yuanbao = pay_item_data['pay_yuanbao'] + pay_item_data['free_yuanbao']
                    nd.SetString(''.join([str(yuanbao), get_text_local_content(12010)]))

        else:
            all_num = len(charge_info_list)
            charge_list_up = self.panel.charge_list_up
            charge_list_up.SetInitCount(min(all_num, self.UP_MAX_NUM))
            all_items_up = charge_list_up.GetAllItem()
            charge_list_down = self.panel.charge_list_down
            charge_list_down.SetInitCount(max(all_num - self.UP_MAX_NUM, 0))
            all_items_down = charge_list_down.GetAllItem()
            for index, pay_item_data in enumerate(charge_info_list):
                if index < self.UP_MAX_NUM:
                    item_widget = all_items_up[index]
                else:
                    item_widget = all_items_down[index - self.UP_MAX_NUM]
                template_path = 'charge/i_charge_item_{}'.format(index + 2)
                widget_name = item_widget.item.GetName()
                p = item_widget.item.GetParent()
                item_widget.item.Destroy()
                global_data.uisystem.load_template_create(template_path, parent=p, root=item_widget, name=widget_name)
                item_widget.item.SetPositionWithCustomConf('50%5', '50%')
                item_widget.item.PlayAnimation('loop')
                key = pay_item_data['goodsid']
                if mall_utils.is_steam_pay():
                    price_txt = mall_utils.get_pc_charge_price_str(pay_item_data)
                else:
                    price_txt = mall_utils.get_charge_price_str(key)
                item_widget.price.SetString(mall_utils.adjust_price(str(price_txt)))
                yuanbao = pay_item_data['pay_yuanbao'] + pay_item_data['free_yuanbao']
                item_widget.diamond_quantity.SetString(''.join([str(yuanbao), get_text_local_content(12010)]))

                @item_widget.btn_bar.unique_callback()
                def OnClick(btn, touch, product_id=key):
                    if global_data.player:
                        global_data.player.pay_order(product_id)
                    else:
                        global_data.game_mgr.show_tip(get_text_by_id(258))

                if G_IS_NA_PROJECT:
                    self.init_na_rebate_tag_ui(item_widget, key)
                else:
                    self.init_not_na_rebate_tag_ui(item_widget, key)

    def set_rebate_tag_ui_visible(self, item_widget, visible=False):
        item_widget.nd_tag_na.setVisible(visible)
        item_widget.nd_tag_na.lab_tag_down.setVisible(visible)
        item_widget.nd_tag_na.lab_return.setVisible(visible)
        item_widget.bar_tag.setVisible(visible)
        item_widget.bar_tag.lab_tag_cn_up.setVisible(visible)
        item_widget.bar_tag.lab_tag_cn_down.setVisible(visible)
        item_widget.bar_tag.lab_tag_return.setVisible(visible)
        item_widget.bar_tag.lab_return.setVisible(visible)
        item_widget.img_recharge_bar.setVisible(False)

    def init_na_rebate_tag_ui(self, item_widget, key):
        self.set_rebate_tag_ui_visible(item_widget)
        if global_data.player:
            is_first = not global_data.player.has_pay_goodsid(key)
            goods_info = global_data.player.get_goods_info(key)
            if goods_info:
                free_yuanbao = goods_info.get('free', None)
                first_free_yuanbao = goods_info.get('first_free', None)
                first_free_rate = goods_info.get('first_free_rate', None)
                if is_first:
                    if first_free_rate:
                        item_widget.nd_tag_na.setVisible(True)
                        item_widget.nd_tag_na.lab_tag_down.setVisible(True)
                        show_first_free_rate_text_id = None
                        if first_free_rate == 1.0:
                            show_first_free_rate_text_id = 12176
                        elif first_free_rate == 0.5:
                            show_first_free_rate_text_id = 12177
                        if show_first_free_rate_text_id is not None:
                            item_widget.nd_tag_na.lab_tag_down.SetString(show_first_free_rate_text_id)
                    elif first_free_yuanbao:
                        item_widget.nd_tag_na.setVisible(True)
                        item_widget.nd_tag_na.lab_return.setVisible(True)
                        item_widget.nd_tag_na.lab_return.SetString(str(first_free_yuanbao))
                show_free_yuanbao = first_free_yuanbao if is_first else free_yuanbao
                if show_free_yuanbao:
                    item_widget.lab_recharge.SetString(get_text_by_id(12153, {'num': show_free_yuanbao}))
                    item_widget.img_recharge_bar.setVisible(True)
        return

    def init_not_na_rebate_tag_ui(self, item_widget, key):
        item_widget.nd_tag_na.setVisible(False)
        self.set_rebate_tag_ui_visible(item_widget)
        is_first = not global_data.player.has_pay_goodsid(key)
        if global_data.player:
            goods_info = global_data.player.get_goods_info(key)
            if goods_info:
                item_widget.bar_tag.setVisible(is_first)
                free_yuanbao = goods_info.get('free', None)
                first_free_yuanbao = goods_info.get('first_free', None)
                first_free_rate = goods_info.get('first_free_rate', None)
                if first_free_yuanbao is not None and first_free_rate is not None and is_first:
                    item_widget.bar_tag.lab_tag_cn_up.setVisible(True)
                    item_widget.bar_tag.lab_tag_cn_down.setVisible(True)
                    show_first_free_rate_text_id = None
                    if first_free_rate == 1.0:
                        show_first_free_rate_text_id = 12154
                    elif first_free_rate == 0.5:
                        show_first_free_rate_text_id = 12157
                    if show_first_free_rate_text_id is not None:
                        item_widget.bar_tag.lab_tag_cn_up.SetString(get_text_by_id(12152))
                        item_widget.bar_tag.lab_tag_cn_down.SetString(get_text_by_id(show_first_free_rate_text_id))
                    else:
                        item_widget.bar_tag.lab_tag_cn_up.setVisible(False)
                        item_widget.bar_tag.lab_tag_cn_down.SetString(False)
                show_free_yuanbao = first_free_yuanbao if is_first else free_yuanbao
                if show_free_yuanbao:
                    item_widget.lab_recharge.SetString(get_text_by_id(12153, {'num': show_free_yuanbao}))
                    item_widget.img_recharge_bar.setVisible(True)
        return