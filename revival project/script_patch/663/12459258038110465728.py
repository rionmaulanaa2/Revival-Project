# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/ChargeLackTip.py
from __future__ import absolute_import
import copy
from common.const.uiconst import SECOND_CONFIRM_LAYER
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.gutils.jump_to_ui_utils import jump_to_charge
from logic.gutils.mall_utils import is_steam_pay, get_pc_charge_price_str, get_charge_price_str, adjust_price
from logic.gutils.salog import SALog

class ChargeLackTip(WindowSmallBase):
    PANEL_CONFIG_NAME = 'charge/i_charge_lack_tips'
    TEMPLATE_NODE_NAME = 'temp_window'
    DLG_ZORDER = SECOND_CONFIRM_LAYER
    UI_ACTION_EVENT = {'btn_buy.OnClick': 'on_buy',
       'btn_go.OnClick': 'on_go'
       }
    GLOBAL_EVENT = {'update_charge_info': 'init_recommand_charge'
       }

    def on_init_panel(self, lack_num, *args, **kargs):
        super(ChargeLackTip, self).on_init_panel()
        self.lack_num = lack_num
        self.recommand_product_id = None
        self.init_recommand_charge()
        self.panel.temp_window.lab_title.SetString(get_text_by_id(610016, [self.lack_num]))
        return

    def on_buy(self, *args):
        if not self.recommand_product_id:
            return
        global_data.player.pay_order(self.recommand_product_id)
        self.close()

    def on_go(self, *args):
        jump_to_charge(tab_idx=0)
        self.close()

    def init_recommand_charge(self):
        item_widget = self.panel.temp_charge
        if not global_data.lobby_mall_data:
            return
        else:
            charge_info_list = global_data.lobby_mall_data.get_charge_info()
            if not charge_info_list:
                global_data.lobby_mall_data.request_charge_info()
                item_widget.setVisible(False)
                self.panel.btn_buy.SetEnable(False)
                return
            item_widget.setVisible(True)
            self.panel.btn_buy.SetEnable(True)
            recommand_charge_info = None
            cur_yuanbao = 0
            info_idx = 0
            for idx, charge_info in enumerate(charge_info_list):
                _, _, _, _, free_yuanbao = self.get_free_yuanbao(charge_info['goodsid'])
                yuanbao = charge_info['pay_yuanbao'] + charge_info['free_yuanbao'] + free_yuanbao
                if recommand_charge_info is None or cur_yuanbao < yuanbao <= self.lack_num or cur_yuanbao > yuanbao >= self.lack_num or yuanbao >= self.lack_num > cur_yuanbao:
                    recommand_charge_info = charge_info
                    cur_yuanbao = yuanbao
                    info_idx = idx

            cur_yuanbao = recommand_charge_info['pay_yuanbao'] + recommand_charge_info['free_yuanbao']
            cur_template_path = 'charge/i_charge_item_{}'.format(info_idx + 2)
            widget_name = item_widget.item.GetName()
            p = item_widget.item.GetParent()
            item_widget.item.Destroy()
            global_data.uisystem.load_template_create(cur_template_path, parent=p, root=item_widget, name=widget_name)
            item_widget.item.SetPositionWithCustomConf('50%5', '50%')
            item_widget.item.PlayAnimation('loop')
            key = recommand_charge_info['goodsid']
            self.recommand_product_id = key
            if is_steam_pay():
                price_txt = get_pc_charge_price_str(recommand_charge_info)
            else:
                price_txt = get_charge_price_str(key)
            item_widget.price.SetString(adjust_price(str(price_txt)))
            item_widget.diamond_quantity.SetString(''.join([str(cur_yuanbao), get_text_local_content(12010)]))
            if G_IS_NA_PROJECT:
                self.init_na_rebate_tag_ui(item_widget, key)
            else:
                self.init_not_na_rebate_tag_ui(item_widget, key)
            SALog.get_instance().write(SALog.LACK_CURRENCY, {'bid': self.recommand_product_id})
            return

    def init_na_rebate_tag_ui(self, item_widget, key):
        self.set_rebate_tag_ui_visible(item_widget)
        is_first, free_yuanbao, first_free_yuanbao, first_free_rate, total_free_yuanbao = self.get_free_yuanbao(key)
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
        if total_free_yuanbao:
            item_widget.lab_recharge.SetString(get_text_by_id(12153, {'num': total_free_yuanbao}))
            item_widget.img_recharge_bar.setVisible(True)
        return

    def init_not_na_rebate_tag_ui(self, item_widget, key):
        item_widget.nd_tag_na.setVisible(False)
        self.set_rebate_tag_ui_visible(item_widget)
        is_first, free_yuanbao, first_free_yuanbao, first_free_rate, total_free_yuanbao = self.get_free_yuanbao(key)
        item_widget.bar_tag.setVisible(is_first)
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
        if total_free_yuanbao:
            item_widget.lab_recharge.SetString(get_text_by_id(12153, {'num': total_free_yuanbao}))
            item_widget.img_recharge_bar.setVisible(True)
        return

    def get_free_yuanbao(self, key):
        is_first = not global_data.player.has_pay_goodsid(key)
        free_yuanbao = None
        first_free_yuanbao = None
        first_free_rate = None
        total_free_yuanbao = None
        if global_data.player:
            goods_info = global_data.player.get_goods_info(key)
            if goods_info:
                free_yuanbao = goods_info.get('free', None)
                first_free_yuanbao = goods_info.get('first_free', None)
                first_free_rate = goods_info.get('first_free_rate', None)
                total_free_yuanbao = first_free_yuanbao if is_first else free_yuanbao
        return (
         is_first, free_yuanbao, first_free_yuanbao, first_free_rate, total_free_yuanbao)

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