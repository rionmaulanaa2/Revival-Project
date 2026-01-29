# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/RoleAndSkinBuyConfirmUI.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from common.const.uiconst import DIALOG_LAYER_BAN_ZORDER
from logic.gutils.mecha_module_utils import init_module_temp_item
from logic.gutils.reinforce_card_utils import get_card_item_no
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import mecha_const
from logic.gutils import mall_utils
from logic.gutils import item_utils
from logic.gutils import template_utils
from logic.gutils import dress_utils
from common.cfg import confmgr
from logic.client.const import mall_const
from logic.gcommon.item import item_const
from logic.gutils import item_utils
import logic.gcommon.const as gconst
from common.utils import timer
import math
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gcommon import time_utility
from logic.gutils.red_packet_utils import init_red_packet_cover_item
from logic.comsys.common_ui.JapanShoppingTips import show_with_japan_shopping_tips
SKIN_TYPE_FOREVER = 0
SKIN_TYPE_7DAYS = 1

@show_with_japan_shopping_tips
class RoleAndSkinBuyConfirmUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'mall/buy_confirm'
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {}

    def on_init_panel(self, goods_id, pick_list=None, fixed_price_info=None, confirm_buy_func=None):
        super(RoleAndSkinBuyConfirmUI, self).on_init_panel()
        self.goods_id = goods_id
        self.pick_list = [] if pick_list is None else pick_list
        self.child_goods_id = None
        self.cur_goods_id = None
        self.discount_item_no = None
        self.skin_type = SKIN_TYPE_FOREVER
        self.refresh_timer_id = None
        self.buy_btn_2_goods_payment = {}
        self.button_ui_price_nd = None
        self.top_price_widget = None
        self._fixed_price_info = fixed_price_info
        self._confirm_buy_func = confirm_buy_func
        self._close_after_successfully_jump = False
        self.init_record()
        self.init_widget()
        self.init_event()
        self.panel.PlayAnimation('appear')
        return

    def init_event(self):
        self.process_event(True)
        self.clear_refresh_timer()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.on_close,
           'second_confirm_event': self._on_second_confirm,
           'pay_order_succ_event': self.on_buy_good_success
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        if self.button_ui_price_nd and self.button_ui_price_nd.isValid():
            self.button_ui_price_nd.setVisible(True)
        self._confirm_buy_func = None
        self.process_event(False)
        self._upload_click_record()
        self.top_price_widget and self.top_price_widget.destroy()
        global_data.emgr.mall_clear_sub_ui_price_widget.emit()
        return

    def on_buy_good_success(self):
        self.refresh_info()

    def init_widget(self):
        self.init_view()
        self.init_buy_type()
        self.refresh_info()
        self.init_price_widget()

    def discount_cb(self, goods_id, discount_item_no):
        self.discount_item_no = discount_item_no
        self.set_total_price(goods_id)

    def init_view(self):
        self.panel.temp_mech_try.setVisible(False)
        self.panel.temp_use_discount.setVisible(False)

    def refresh_info(self):
        if self.skin_type == SKIN_TYPE_FOREVER:
            goods_id = self.goods_id
        else:
            goods_id = self.child_goods_id
        self.set_item_info(self.goods_id)
        self.set_module_info(self.goods_id)
        self.set_skin_info(self.goods_id)
        if not self._fixed_price_info:
            template_utils.show_discount_view(self.panel.temp_use_discount, goods_id, self.discount_cb)
            if mall_utils.get_goods_anniv_discount(str(goods_id)):
                self.panel.temp_use_discount.setVisible(False)
        else:
            self.set_total_price(self.goods_id)

    def init_buy_type(self):
        if self._fixed_price_info:
            self.panel.nd_buy_time.setVisible(False)
            return
        else:
            self.child_goods_id = mall_utils.get_child_goods(self.goods_id)
            if mall_utils.is_max_7day_goods_num(self.goods_id):
                self.child_goods_id = None
            btn_7days_enable = bool(self.child_goods_id)

            @self.panel.btn_forever.callback()
            def OnClick(*args):
                self.skin_type = SKIN_TYPE_FOREVER
                self.panel.btn_forever.SetSelect(True)
                btn_7days_enable and self.panel.btn_7days.SetSelect(False)
                self.show_installment_info()
                self.refresh_info()

            @self.panel.btn_7days.callback()
            def OnClick(*args):
                self.skin_type = SKIN_TYPE_7DAYS
                self.panel.btn_forever.SetSelect(False)
                self.panel.btn_7days.SetSelect(True)
                self.show_installment_info()
                self.refresh_info()

            self.skin_type = SKIN_TYPE_FOREVER
            self.panel.btn_7days.setVisible(btn_7days_enable)
            self.panel.btn_forever.SetSelect(True)
            btn_7days_enable and self.panel.btn_7days.SetSelect(False)
            self.panel.nd_buy_time.setVisible(btn_7days_enable)
            self.show_installment_info()
            return

    def init_price_widget--- This code section failed: ---

 160       0  LOAD_GLOBAL           0  'PriceUIWidget'
           3  LOAD_GLOBAL           1  'panel'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  'panel'
          12  LOAD_ATTR             2  'list_price'
          15  LOAD_CONST            2  'pnl_title'
          18  LOAD_GLOBAL           3  'False'
          21  CALL_FUNCTION_513   513 
          24  LOAD_FAST             0  'self'
          27  STORE_ATTR            4  'top_price_widget'

 161      30  LOAD_FAST             0  'self'
          33  LOAD_ATTR             5  'refresh_price_widget'
          36  CALL_FUNCTION_0       0 
          39  POP_TOP          

 162      40  LOAD_GLOBAL           6  'global_data'
          43  LOAD_ATTR             7  'emgr'
          46  LOAD_ATTR             8  'mall_init_sub_ui_price_widget'
          49  LOAD_ATTR             9  'emit'
          52  CALL_FUNCTION_0       0 
          55  POP_TOP          

Parse error at or near `CALL_FUNCTION_513' instruction at offset 21

    def set_total_price(self, goods_id):
        price_gift_item_dict, min_gift_close_time = mall_utils.get_mall_item_price_gift_item(goods_id)
        if self._fixed_price_info:
            prices = self._fixed_price_info
        else:
            prices = mall_utils.get_mall_item_price(goods_id, pick_list=self.pick_list)
        prices.reverse()
        now_time = time_utility.get_server_time()
        for i, node in enumerate([self.panel.btn_buy_2, self.panel.btn_buy_1]):
            if i < len(prices):
                node.setVisible(True)
                price_info = prices[i]
                goods_payment = price_info.get('goods_payment')
                color = mall_const.DEF_PRICE_COLOR
                self.buy_btn_2_goods_payment[node] = goods_payment
                if i:
                    color = mall_const.MALL_BUY_PRICE_COLOR
                payment_has_gift = goods_payment in price_gift_item_dict
                if hasattr(node, 'nd_cristal_buy_tips') and node.nd_cristal_buy_tips:
                    node.nd_cristal_buy_tips.setVisible(payment_has_gift)
                    if payment_has_gift:
                        node.nd_cristal_buy_tips.SetTimeOut(min_gift_close_time - now_time + 1, lambda : self.set_total_price)
                        gift_item_no = str(price_gift_item_dict[goods_payment])
                        item_no = mall_utils.get_goods_item_no(gift_item_no)

                        def callback(gift_item_no=gift_item_no):
                            mall_utils.mall_switch_detail(gift_item_no)

                        template_utils.init_tempate_mall_i_item(node.nd_cristal_buy_tips.lab_gift.nd_auto_fit.temp_gift_skin, item_no, callback=callback, templatePath='i_item_dark')
                if goods_payment in gconst.CAN_DISCOUNT_PAYMENT and not self._fixed_price_info:
                    mall_utils.refresh_discount_price(price_info, self.discount_item_no)
                real_price = price_info.get('real_price')
                is_advance_price = mall_utils.is_advance_buy_price_currently(price_info)
                if is_advance_price:
                    original_price = price_info.get('original_price')
                    if node == self.panel.btn_buy_2:
                        price_info_org = {'original_price': original_price,'goods_payment': goods_payment}
                        template_utils.init_price_template(price_info_org, node.nd_buy_tips.lab_advance_buy.nd_auto_fit.temp_low_price, color=mall_const.NO_RED_PRICE_COLOR)
                        limit_close_timestamp = price_info.get('limit_close_timestamp')
                        remain_time = limit_close_timestamp - now_time
                        template_utils.show_remain_time_countdown(node.nd_buy_tips, node.nd_buy_tips.lab_time, remain_time, '', cb=lambda : self.set_total_price(goods_id), custom_text=81455)
                    if node.nd_buy_tips:
                        node.nd_buy_tips.setVisible(False)
                elif node.nd_buy_tips:
                    node.nd_buy_tips.setVisible(False)
                template_utils.init_price_template(price_info, node.temp_price, color=color)

                @node.btn_common_big.unique_callback()
                def OnClick(btn, touch, goods_id=goods_id, goods_payment=goods_payment, real_price=real_price, btn_index=i):
                    self.try_buy_goods_with_advance_and_gift_item_check(goods_id, goods_payment, real_price)

                if goods_payment == gconst.SHOP_PAYMENT_GOLD:
                    self.limit_open_gold_pay(node.btn_common_big, goods_id)
            else:
                node.setVisible(False)

        self.adjuest_buy_btn()

    def adjuest_buy_btn(self):
        _, h = self.panel.nd_buy_time.GetContentSize()
        btn_buy_1_show = self.panel.btn_buy_1 and self.panel.btn_buy_1.isVisible()
        w = 530 if btn_buy_1_show else 730
        self.panel.nd_buy_time.SetContentSize(w, h)
        self.panel.nd_buy_time.ResizeAndPosition(include_self=False)
        pos = ('100%-343', '50%-55') if btn_buy_1_show else ('100%-144', '50%-55')
        self.panel.btn_buy_2.SetPosition(*pos)

    def get_advance_buy_tips(self, goods_id, price_info):
        goods_payment = price_info.get('goods_payment')
        limit_close_timestamp = price_info.get('limit_close_timestamp')
        original_price = price_info.get('original_price')
        remain_time = limit_close_timestamp - time_utility.get_server_time()
        if remain_time > 0:
            remain_time_str = mall_utils.get_remain_time_txt(remain_time)
            price_str = template_utils.get_money_rich_text(goods_payment, original_price)
            confirm_text = get_text_by_id(81454, {'time': remain_time_str,'price': price_str,'item_name': mall_utils.get_goods_name(goods_id)
               })
            return confirm_text
        return ''

    def get_buy_gift_item_tips(self, goods_id):
        price_gift_item_dict, _ = mall_utils.get_mall_item_price_gift_item(goods_id)
        if price_gift_item_dict:
            goods_payment_list = six_ex.keys(price_gift_item_dict)
            goods_payment_2 = goods_payment_list[0]
            price_info_2 = self.find_price_info_by_payment(goods_id, goods_payment_2)
            if price_info_2:
                real_price_2 = price_info_2.get('real_price')
                price_str_2 = template_utils.get_money_rich_text(goods_payment_2, real_price_2)
                item_id = price_gift_item_dict[goods_payment_2]
                item_name = item_utils.get_item_name(item_id)
                confirm_text = get_text_by_id(81457, {'price2': price_str_2,'item_name': mall_utils.get_goods_name(goods_id),
                   'gift_name': item_name
                   })
                return confirm_text
        return ''

    def find_price_info_by_payment(self, goods_id, goods_pm):
        if self._fixed_price_info:
            price_list = self._fixed_price_info
        else:
            price_list = mall_utils.get_mall_item_price(goods_id, pick_list=self.pick_list)
        price_index = -1
        for i, temp_price_info in enumerate(price_list):
            if temp_price_info.get('goods_payment', None) == goods_pm:
                price_index = i
                break

        if price_index < 0:
            log_error('try_buy_goods_with_advance_and_gift_item_check fail to find correct goods_payment', goods_id, goods_pm, price_list)
            return
        else:
            price_info = price_list[price_index]
            return price_info

    def try_buy_goods_with_advance_and_gift_item_check(self, goods_id, goods_payment, real_price):
        price_info = self.find_price_info_by_payment(goods_id, goods_payment)
        if not price_info:
            return
        confirm_text_list = []
        is_advance_price = mall_utils.is_advance_buy_price_currently(price_info)
        if is_advance_price:
            confirm_text = self.get_advance_buy_tips(goods_id, price_info)
            confirm_text_list.append(confirm_text)
        price_gift_item_dict, _ = mall_utils.get_mall_item_price_gift_item(goods_id)
        if price_gift_item_dict and goods_payment not in price_gift_item_dict:
            goods_payment_list = six_ex.keys(price_gift_item_dict)
            goods_payment_2 = goods_payment_list[0]
            price_info_2 = self.find_price_info_by_payment(goods_id, goods_payment_2)
            if price_info_2:
                real_price_2 = price_info_2.get('real_price')
                price_str_1 = template_utils.get_money_rich_text(goods_payment, real_price)
                price_str_2 = template_utils.get_money_rich_text(goods_payment_2, real_price_2)
                item_no = mall_utils.get_goods_item_no(str(price_gift_item_dict[goods_payment_2]))
                item_name = item_utils.get_lobby_item_name(item_no)
                confirm_text = get_text_by_id(81456, {'price2': price_str_2,'price1': price_str_1,'item_name': mall_utils.get_goods_name(goods_id),
                   'gift_name': item_name})
                confirm_text_list.append(confirm_text)

        def _buy():
            self.try_buy_goods(goods_id, goods_payment, real_price)

        if confirm_text_list:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            SecondConfirmDlg2().confirm(content='\n'.join(confirm_text_list), confirm_callback=_buy, unique_key='ask_advance_buy_use_gold')
        else:
            _buy()

    def try_buy_goods(self, goods_id, goods_payment, real_price):
        limit = mall_utils.limite_pay(goods_id)
        if limit:
            return
        payment_type = mall_utils.get_payment_type(goods_payment)
        self._add_click_record('payment_%s_buy' % payment_type)

        def _pay():
            discount_item_id = None
            if goods_payment in gconst.CAN_DISCOUNT_PAYMENT:
                discount_item_id = self.discount_item_no
            global_data.player.buy_goods(goods_id, 1, goods_payment, discount_item_id=discount_item_id)
            self._pay_success({goods_payment: real_price})
            global_data.player.sa_log_anniversary_gift_state_buy(goods_id)
            return

        def after_yueka--- This code section failed: ---

 348       0  LOAD_GLOBAL           0  'False'
           3  POP_JUMP_IF_FALSE   185  'to 185'
           6  LOAD_GLOBAL           1  'mall_utils'
           9  LOAD_ATTR             2  'get_payment_item_no'

 349      12  LOAD_DEREF            1  'goods_payment'
          15  CALL_FUNCTION_1       1 
          18  LOAD_GLOBAL           3  'gconst'
          21  LOAD_ATTR             4  'SHOP_PAYMENT_PIECE5'
          24  COMPARE_OP            2  '=='
        27_0  COME_FROM                '3'
          27  POP_JUMP_IF_FALSE   185  'to 185'

 350      30  LOAD_DEREF            2  'self'
          33  LOAD_ATTR             5  '_get_real_price'
          36  CALL_FUNCTION_0       0 
          39  STORE_DEREF           0  'yuanbao_real_price'

 351      42  LOAD_GLOBAL           1  'mall_utils'
          45  LOAD_ATTR             6  'check_payment'
          48  LOAD_DEREF            1  'goods_payment'
          51  LOAD_DEREF            3  'real_price'
          54  LOAD_GLOBAL           0  'False'
          57  LOAD_CONST            1  'cb'
          60  LOAD_DEREF            4  '_pay'
          63  CALL_FUNCTION_259   259 
          66  POP_JUMP_IF_FALSE    80  'to 80'

 352      69  LOAD_DEREF            4  '_pay'
          72  CALL_FUNCTION_0       0 
          75  POP_TOP          

 353      76  LOAD_CONST            0  ''
          79  RETURN_END_IF    
        80_0  COME_FROM                '66'

 355      80  LOAD_CLOSURE          0  'yuanbao_real_price'
          83  LOAD_CLOSURE          2  'self'
          86  LOAD_CLOSURE          5  'goods_id'
          92  LOAD_CONST               '<code_object _yuanbao_pay>'
          95  MAKE_CLOSURE_0        0 
          98  STORE_FAST            0  '_yuanbao_pay'

 365     101  LOAD_GLOBAL           7  'get_text_local_content'
         104  LOAD_CONST            3  12122
         107  CALL_FUNCTION_1       1 
         110  LOAD_ATTR             8  'format'
         113  LOAD_CONST            4  'img1'

 366     116  LOAD_CONST            5  '<color=0XFFFFFFFF><img ="gui/ui_res_2/icon/icon_exchange.png",scale=0.0></color>'
         119  LOAD_CONST            6  'img2'

 367     122  LOAD_CONST            7  '<color=0XFFFFFFFF><img ="gui/ui_res_2/icon/icon_crystal.png",scale=0.0></color>'
         125  LOAD_CONST            8  'num'

 368     128  LOAD_DEREF            0  'yuanbao_real_price'
         131  CALL_FUNCTION_768   768 
         134  STORE_FAST            1  'content_text'

 370     137  LOAD_CONST            9  ''
         140  LOAD_CONST           10  ('SecondConfirmDlg2',)
         143  IMPORT_NAME           9  'logic.comsys.common_ui.NormalConfirmUI'
         146  IMPORT_FROM          10  'SecondConfirmDlg2'
         149  STORE_FAST            2  'SecondConfirmDlg2'
         152  POP_TOP          

 371     153  LOAD_FAST             2  'SecondConfirmDlg2'
         156  CALL_FUNCTION_0       0 
         159  LOAD_ATTR            11  'confirm'
         162  LOAD_CONST           11  'content'

 372     165  LOAD_FAST             1  'content_text'
         168  LOAD_CONST           12  'confirm_callback'

 373     171  LOAD_CONST           13  'unique_key'

 374     174  LOAD_CONST           14  'use_yuanbao'
         177  CALL_FUNCTION_768   768 
         180  POP_TOP          

 377     181  LOAD_CONST            0  ''
         184  RETURN_END_IF    
       185_0  COME_FROM                '27'

 379     185  LOAD_GLOBAL           1  'mall_utils'
         188  LOAD_ATTR             6  'check_payment'
         191  LOAD_DEREF            1  'goods_payment'
         194  LOAD_DEREF            3  'real_price'
         197  LOAD_CONST            1  'cb'
         200  LOAD_DEREF            4  '_pay'
         203  CALL_FUNCTION_258   258 
         206  POP_JUMP_IF_TRUE    213  'to 213'

 380     209  LOAD_CONST            0  ''
         212  RETURN_END_IF    
       213_0  COME_FROM                '206'

 382     213  LOAD_DEREF            4  '_pay'
         216  CALL_FUNCTION_0       0 
         219  POP_TOP          

Parse error at or near `CALL_FUNCTION_768' instruction at offset 177

        if not self._fixed_price_info:
            mall_utils.check_yueka_discount_notice(goods_id, lambda : after_yueka())
        else:
            if not mall_utils.check_payment(goods_payment, real_price, cb=_pay):
                return
            if self._confirm_buy_func and callable(self._confirm_buy_func):
                self._confirm_buy_func(goods_id)
            else:
                _pay()

    def limit_open_gold_pay(self, node, goods_id):
        enable, time = mall_utils.limite_pay_by_goods_payment(gconst.SHOP_PAYMENT_GOLD, goods_id)
        node.SetEnable(enable)
        self.panel.lab_forbidden.setVisible(False)
        self.panel.btn_buy_1.temp_price.setVisible(True)
        if time is None:
            return
        else:
            show_time = time > 0
            self.panel.lab_forbidden.setVisible(show_time)
            self.panel.btn_buy_1.temp_price.setVisible(not show_time)
            time_txt = mall_utils.get_remain_time_txt(time)
            real_price_txt = '<color=0XFFFFFFFF><img ="%s",scale=0.0></color>' % item_utils.get_money_icon(gconst.SHOP_PAYMENT_GOLD)
            self.panel.lab_forbidden.SetString(get_text_by_id(81155).format(time=time_txt, gold=real_price_txt))
            if time > 0:

                def _cb(nd=node):
                    nd.SetEnable(True)
                    self.panel.lab_forbidden.setVisible(False)
                    self.panel.btn_buy_1.temp_price.setVisible(True)

                self.refresh_timer_id = global_data.game_mgr.register_logic_timer(_cb, interval=time, times=1, mode=timer.CLOCK)
            return

    def clear_refresh_timer(self):
        if self.refresh_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.refresh_timer_id)
        self.refresh_timer_id = None
        return

    def get_role_pic(self, goods_id):
        item_no = mall_utils.get_goods_item_no(goods_id)
        pic = mall_utils.get_half_pic_by_item_no(item_no)
        return pic

    def get_mecha_pic(self, goods_id):
        return mall_utils.get_detail_pic(goods_id)

    def set_role_pic(self, node, goods_id):
        path = self.get_role_pic(goods_id)
        node.SetDisplayFrameByPath('', path)

    def set_mecha_pic(self, node, goods_id):
        path = self.get_mecha_pic(goods_id)
        node.SetDisplayFrameByPath('', path)

    def set_red_packet_cover(self, node, goods_id):
        item_no = mall_utils.get_goods_item_no(goods_id)
        init_red_packet_cover_item(node, item_no)

    def set_item_info(self, goods_id):
        is_driver = mall_utils.is_driver(goods_id)
        is_mecha = mall_utils.is_mecha(goods_id)
        is_red_packet = mall_utils.is_red_packet_cover(goods_id)
        path_funcs = [self.set_role_pic, self.set_mecha_pic, self.set_red_packet_cover]
        nodes = [self.panel.img_role, self.panel.img_mech, self.panel.temp_red_packet]
        visibles = [is_driver, is_mecha, is_red_packet]
        for i, node in enumerate(nodes):
            can_view = bool(visibles[i])
            node.setVisible(can_view)
            if can_view:
                path_funcs[i](node, goods_id)

        self.panel.lab_name.SetString(mall_utils.get_goods_name(goods_id))
        self.set_good_describe(goods_id)
        item_no = mall_utils.get_goods_item_no(goods_id)
        str_item_no = str(item_no)
        access_txt = item_utils.get_item_access(str_item_no)
        self.panel.nd_other_unlock.setVisible(bool(access_txt))
        access_txt and self.panel.lab_other_unlock.SetString(access_txt)

        @self.panel.btn_get_way.callback()
        def OnClick(*args):
            if item_utils.can_jump_to_ui(str_item_no):
                item_utils.jump_to_ui(str_item_no)
            if self._close_after_successfully_jump:
                if not self.panel.isVisible():
                    self.close()

    def set_good_describe(self, goods_id):
        import cc
        rule = mall_utils.get_goods_decs(goods_id)
        is_mecha = mall_utils.is_only_mecha(goods_id)
        if not is_mecha:
            size = self.panel.lab_describe.getContentSize()
            w, h = size.width, size.height
            self.panel.lab_describe.SetContentSize(w, 158)
        self.panel.lab_describe.SetInitCount(1)
        text_item = self.panel.lab_describe.GetItem(0)
        text_item.lab_describe.SetString(rule)
        text_item.lab_describe.formatText()
        sz = text_item.lab_describe.getTextContentSize()
        sz.height += 20
        old_sz = text_item.getContentSize()
        text_item.setContentSize(cc.Size(old_sz.width, sz.height))
        text_item.RecursionReConfPosition()
        old_inner_size = self.panel.lab_describe.GetInnerContentSize()
        self.panel.lab_describe.SetInnerContentSize(old_inner_size.width, sz.height)
        self.panel.lab_describe.GetContainer()._refreshItemPos()
        self.panel.lab_describe._refreshItemPos()

    def set_skin_info(self, goods_id):
        item_utils.check_skin_tag(self.panel.nd_kind, None, goods_id)
        pos = ('100%-120', '100%-37') if self.panel.nd_kind and self.panel.nd_kind.isVisible() else ('100%-40',
                                                                                                     '100%-37')
        self.panel.lab_name.SetPosition(*pos)
        return

    def set_module_info(self, goods_id):
        is_mecha = mall_utils.is_only_mecha(goods_id)
        self.panel.nd_module.setVisible(is_mecha)
        if is_mecha:
            macha_lobby_id = mall_utils.get_goods_item_no(goods_id)
            mecha_id = dress_utils.mecha_lobby_id_2_battle_id(macha_lobby_id)
            module_conf = confmgr.get('mecha_default_module_conf', default={}).get(str(mecha_id))
            slot_1 = module_conf.get('slot_pos1')
            slot_2 = module_conf.get('slot_pos2')
            slot_3 = module_conf.get('slot_pos3')
            slot_4 = module_conf.get('slot_pos4')
            card_list = [slot_1[0], slot_2[0], slot_3[0]]
            card_list.extend(slot_4)
            for i in range(len(card_list)):
                module_nd = self.panel.module_list.GetItem(i)
                item_no = get_card_item_no(card_list[i])
                module_nd.img_skill.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
                self.register_module_info_click(module_nd, item_no)

    def show_installment_info(self):
        if mall_utils.is_ticket_permanent_discount(self.goods_id):
            if self.skin_type == SKIN_TYPE_FOREVER:
                if mall_utils.is_max_7day_goods_num(self.goods_id):
                    txt_id = 12106
                else:
                    txt_id = 12104
            else:
                txt_id = 12103
            template_utils.show_installment_info(True, self.panel.temp_mech_try, self.goods_id, txt_id)

    def register_module_info_click(self, module_nd, item_no):
        if item_no:

            @module_nd.unique_callback()
            def OnClick(layer, touch, *args):
                position = touch.getLocation()
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=position)
                return

    def enable_btn_buy_get(self, click_action, text):
        self.panel.btn_buy_1.setVisible(False)
        self.panel.btn_buy_get.setVisible(True)
        self.panel.btn_buy_get.btn_common_big.SetText(text)
        self.refresh_price_widget()

        @self.panel.btn_buy_get.btn_common_big.unique_callback()
        def OnClick(*args):
            click_action()
            self.close()

    def on_close(self, *args):
        self.close()

    def refresh_price_widget(self):
        money_types = []
        for btn in (self.panel.btn_buy_2, self.panel.btn_buy_1):
            if not btn.isVisible() or not self.buy_btn_2_goods_payment.get(btn):
                continue
            good_payment = self.buy_btn_2_goods_payment.get(btn)
            if good_payment:
                money_types.append(good_payment)

        self.top_price_widget.show_money_types(money_types)

    def set_buttom_ui_price_nd(self, nd):
        self.button_ui_price_nd = nd
        if self.button_ui_price_nd.isValid():
            self.button_ui_price_nd.setVisible(False)

    def _add_click_record(self, button_name):
        if not self._need_log:
            return
        self._click_record.append((button_name, int(time_utility.get_server_time())))

    def _on_second_confirm(self, unique_key, flag):
        if not self._need_log:
            return
        button_name = unique_key + '_' + ('yes' if flag else 'no')
        self._add_click_record(button_name)

    def _upload_click_record(self):
        if not self._need_log:
            return
        self._log_info['closed_time'] = int(time_utility.get_server_time())
        self._log_info['detail'] = self._click_record
        global_data.player.sa_log_buy_confirm(self._log_info)

    def _pay_success(self, payment):
        if not self._need_log:
            return
        self._log_info['cost_resource'] = {str(k):v for k, v in six.iteritems(payment)}

    def init_record(self):
        self._need_log = False
        self._log_info = {}
        self._click_record = []
        value_data = {}
        prices = mall_utils.get_mall_item_price(self.goods_id, pick_list=self.pick_list)
        for price_info in prices:
            goods_payment = price_info.get('goods_payment')
            currency = mall_utils.get_payment_item_no(goods_payment)
            real_price = price_info.get('real_price') or price_info.get('original_price')
            value_data[str(currency)] = real_price

        for currency in (gconst.SHOP_ITEM_YUANBAO, gconst.SHOP_PAYMENT_PIECE5):
            if str(currency) not in value_data:
                self._need_log = False

        if not self._need_log:
            return
        self._log_info['item_value'] = value_data
        from logic.gcommon.cdata import dan_data
        from logic.gcommon.const import SHOP_PAYMENT_PIECE5
        player = global_data.player
        self._log_info.update({'opened_time': int(time_utility.get_server_time()),
           'role_level': player.get_lv(),
           'dan': player.get_dan('survival_dan'),
           'dan_lv': player.get_dan_lv(dan_data.DAN_SURVIVAL),
           'battlepasslv': player.battlepass_lv,
           'left_yuanbao': player.get_yuanbao(),
           'left_coupon': player.get_item_num_by_no(SHOP_PAYMENT_PIECE5),
           'left_alpha_coin': player.get_diamond(),
           'left_coin': player.get_gold(),
           'item': {str(self.goods_id): 1}})

    def _get_real_price(self):
        real_price = 0
        prices = mall_utils.get_mall_item_price(self.goods_id, pick_list=('yuanbao', ))
        for price_info in prices:
            goods_payment = price_info.get('goods_payment')
            if mall_utils.get_payment_type(goods_payment) == gconst.SHOP_PAYMENT_YUANBAO:
                if price_info.get('discount_condition', '') == 'yueka':
                    real_price = price_info.get('original_price', 0)
                    if global_data.player.has_yueka():
                        real_price = price_info.get('discount_price', 0)
                else:
                    real_price += price_info.get('real_price', 0)

        return real_price

    def set_close_after_successfully_jump(self, val):
        self._close_after_successfully_jump = val