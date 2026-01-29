# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/GroceriesBuyConfirmUI.py
from __future__ import absolute_import
import logic.gcommon.const as gconst
from common.const.uiconst import DIALOG_LAYER_BAN_ZORDER
from common.const import uiconst
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from logic.gcommon.item import item_const
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.client.const import mall_const
from common.cfg import confmgr
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.comsys.common_ui.JapanShoppingTips import show_with_japan_shopping_tips
from logic.gcommon.common_utils.local_text import get_text_by_id

@show_with_japan_shopping_tips
class GroceriesBuyConfirmUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'mall/buy_confirm_groceries'
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {}

    def on_init_panel(self, goods_id, need_show=item_const.ITEM_SHOW_TYPE_NONE, pick_list=None, init_quantity=1, force_change_init_quantity=False, fixed_price_info=None, confirm_buy_func=None):
        super(GroceriesBuyConfirmUI, self).on_init_panel()
        self.goods_id = goods_id
        self.pick_list = pick_list or []
        self.item_widgets = {}
        self.need_show = need_show
        self._fixed_price_info = fixed_price_info
        self._confirm_buy_func = confirm_buy_func
        self.init_widget(init_quantity, force_change_init_quantity)
        self.init_event()

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.on_close
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.destroy_widget('item_num_btn_widget')
        self.process_event(False)

    def init_widget(self, init_quantity=1, force_change_init_quantity=False):
        self.set_item_info()
        self.init_item_num(init_quantity, force_change_init_quantity)
        self.init_gift_list()

    def init_item_num(self, init_quantity=1, force_change_init_quantity=False):
        mall_conf = confmgr.get('mall_config', self.goods_id, default={})
        all_max_num = mall_utils.get_goods_limit_num_all(self.goods_id)
        if all_max_num == 1:
            max_num = 1
        else:
            self.panel.temp_quantity.setVisible(True)
            max_buy_num_per_day = mall_conf.get('max_buy_num_per_day')
            max_buy_num_per_week = mall_utils.get_goods_max_buy_num_per_week(self.goods_id)
            season_max_num = mall_conf.get('max_buy_num_per_season', None)
            times_max_num = mall_conf.get('num_times', None)
            if season_max_num:
                _, _, num_info = mall_utils.buy_num_limite_by_season(self.goods_id)
                max_num = season_max_num
            elif max_buy_num_per_day:
                _, _, num_info = mall_utils.buy_num_limite_by_day(self.goods_id)
                max_num = max_buy_num_per_day
            elif max_buy_num_per_week:
                _, _, num_info = mall_utils.buy_num_limite_by_week(self.goods_id)
                max_num = max_buy_num_per_week
            elif all_max_num:
                _, _, num_info = mall_utils.buy_num_limit_by_all(self.goods_id)
                max_num = all_max_num
            else:
                max_num = times_max_num
                num_info = None
            if num_info:
                left_num, _ = num_info
                if times_max_num is None:
                    times_max_num = min(left_num, max_num)
                max_num = min(times_max_num, left_num)
            max_num = 99999 if max_num is None else max(1, max_num)
            prices = mall_utils.get_mall_item_price(self.goods_id, pick_list=self.pick_list)
            if prices:
                money_limit_num = 1
                for price_info in prices:
                    goods_payment = price_info.get('goods_payment')
                    real_price = price_info.get('real_price')
                    if real_price == 0:
                        continue
                    my_money_num = mall_utils.get_my_money(goods_payment)
                    limit_num = int(my_money_num / real_price)
                    money_limit_num = max(money_limit_num, limit_num)

                max_num = min(money_limit_num, max_num)
        if not force_change_init_quantity:
            init_quantity = min(init_quantity, max_num)
        self.item_num_btn_widget = ItemNumBtnWidget(self.panel.temp_quantity)
        self.item_num_btn_widget.init_item({'quantity': max_num}, self.set_total_price, init_quantity=init_quantity)
        return

    def set_total_price(self, *args):
        _, num = args
        self.panel.temp_quantity.lab_num.SetString(str(num))
        if self._fixed_price_info:
            prices = self._fixed_price_info
        else:
            prices = mall_utils.get_mall_item_price(self.goods_id, num, pick_list=self.pick_list)
        if not prices:
            return
        for i, node in enumerate([self.panel.temp_btn_buy1, self.panel.temp_btn_buy2]):
            if not node:
                continue
            if i < len(prices):
                node.setVisible(True)
                price_info = prices[i]
                goods_payment = price_info.get('goods_payment')
                real_price = price_info.get('real_price')
                if len(prices) > 1 and i == 0:
                    color = mall_const.DEF_PRICE_COLOR
                else:
                    color = mall_const.DARK_PRICE_COLOR
                template_utils.init_price_template(price_info, node.temp_price, color=color)

                @node.btn_common.unique_callback()
                def OnClick(btn, touch, goods_payment=goods_payment, real_price=real_price):
                    from logic.gutils import item_utils
                    unowned_open_item_nos = mall_utils.get_goods_id_unowned_open_item_nos(self.goods_id)
                    if unowned_open_item_nos:
                        name_text = item_utils.get_lobby_item_name(unowned_open_item_nos[0])
                        global_data.game_mgr.show_tip(get_text_by_id(81606, {'skin_name': name_text}))
                        return
                    limit = mall_utils.limite_pay(self.goods_id)
                    if limit:
                        return

                    def _pay():
                        if self._confirm_buy_func:
                            self._confirm_buy_func(self.goods_id)
                        else:
                            global_data.player.buy_goods(self.goods_id, num, goods_payment, need_show=self.need_show)
                        global_data.player.sa_log_anniversary_gift_state_buy(self.goods_id)

                    def after_yueka--- This code section failed: ---

 160       0  LOAD_GLOBAL           0  'False'
           3  POP_JUMP_IF_FALSE   182  'to 182'
           6  LOAD_GLOBAL           1  'mall_utils'
           9  LOAD_ATTR             2  'get_payment_item_no'
          12  LOAD_DEREF            1  'goods_payment'
          15  CALL_FUNCTION_1       1 
          18  LOAD_GLOBAL           3  'gconst'
          21  LOAD_ATTR             4  'SHOP_PAYMENT_PIECE5'
          24  COMPARE_OP            2  '=='
        27_0  COME_FROM                '3'
          27  POP_JUMP_IF_FALSE   182  'to 182'

 161      30  LOAD_DEREF            2  'self'
          33  LOAD_ATTR             5  '_get_real_price'
          36  CALL_FUNCTION_0       0 
          39  STORE_DEREF           0  'yuanbao_real_price'

 162      42  LOAD_GLOBAL           1  'mall_utils'
          45  LOAD_ATTR             6  'check_payment'
          48  LOAD_DEREF            1  'goods_payment'
          51  LOAD_DEREF            3  'real_price'
          54  LOAD_GLOBAL           0  'False'
          57  LOAD_CONST            1  'cb'
          60  LOAD_DEREF            4  '_pay'
          63  CALL_FUNCTION_259   259 
          66  POP_JUMP_IF_FALSE    80  'to 80'

 163      69  LOAD_DEREF            4  '_pay'
          72  CALL_FUNCTION_0       0 
          75  POP_TOP          

 164      76  LOAD_CONST            0  ''
          79  RETURN_END_IF    
        80_0  COME_FROM                '66'

 166      80  LOAD_CLOSURE          0  'yuanbao_real_price'
          83  LOAD_CLOSURE          2  'self'
          89  LOAD_CONST               '<code_object _yuanbao_pay>'
          92  MAKE_CLOSURE_0        0 
          95  STORE_FAST            0  '_yuanbao_pay'

 175      98  LOAD_GLOBAL           7  'get_text_local_content'
         101  LOAD_CONST            3  12122
         104  CALL_FUNCTION_1       1 
         107  LOAD_ATTR             8  'format'
         110  LOAD_CONST            4  'img1'

 176     113  LOAD_CONST            5  '<color=0XFFFFFFFF><img ="gui/ui_res_2/icon/icon_exchange.png",scale=0.0></color>'
         116  LOAD_CONST            6  'img2'

 177     119  LOAD_CONST            7  '<color=0XFFFFFFFF><img ="gui/ui_res_2/icon/icon_crystal.png",scale=0.0></color>'
         122  LOAD_CONST            8  'num'

 178     125  LOAD_DEREF            0  'yuanbao_real_price'
         128  CALL_FUNCTION_768   768 
         131  STORE_FAST            1  'content_text'

 180     134  LOAD_CONST            9  ''
         137  LOAD_CONST           10  ('SecondConfirmDlg2',)
         140  IMPORT_NAME           9  'logic.comsys.common_ui.NormalConfirmUI'
         143  IMPORT_FROM          10  'SecondConfirmDlg2'
         146  STORE_FAST            2  'SecondConfirmDlg2'
         149  POP_TOP          

 181     150  LOAD_FAST             2  'SecondConfirmDlg2'
         153  CALL_FUNCTION_0       0 
         156  LOAD_ATTR            11  'confirm'
         159  LOAD_CONST           11  'content'

 182     162  LOAD_FAST             1  'content_text'
         165  LOAD_CONST           12  'confirm_callback'

 183     168  LOAD_CONST           13  'unique_key'

 184     171  LOAD_CONST           14  'use_yuanbao'
         174  CALL_FUNCTION_768   768 
         177  POP_TOP          

 186     178  LOAD_CONST            0  ''
         181  RETURN_END_IF    
       182_0  COME_FROM                '27'

 188     182  LOAD_GLOBAL           1  'mall_utils'
         185  LOAD_ATTR             6  'check_payment'
         188  LOAD_DEREF            1  'goods_payment'
         191  LOAD_DEREF            3  'real_price'
         194  LOAD_CONST            1  'cb'
         197  LOAD_DEREF            4  '_pay'
         200  CALL_FUNCTION_258   258 
         203  POP_JUMP_IF_TRUE    210  'to 210'

 189     206  LOAD_CONST            0  ''
         209  RETURN_END_IF    
       210_0  COME_FROM                '203'

 190     210  LOAD_CONST            9  ''
         213  LOAD_CONST           15  ('goods_buy_need_confirm',)
         216  IMPORT_NAME          12  'logic.gutils.mall_buy_confirm_func'
         219  IMPORT_FROM          13  'goods_buy_need_confirm'
         222  STORE_FAST            3  'goods_buy_need_confirm'
         225  POP_TOP          

 191     226  LOAD_FAST             3  'goods_buy_need_confirm'
         229  LOAD_DEREF            2  'self'
         232  LOAD_ATTR            14  'goods_id'
         235  LOAD_CONST           16  'call_back'
         238  LOAD_DEREF            4  '_pay'
         241  CALL_FUNCTION_257   257 
         244  POP_JUMP_IF_FALSE   251  'to 251'

 192     247  LOAD_CONST            0  ''
         250  RETURN_END_IF    
       251_0  COME_FROM                '244'

 193     251  LOAD_DEREF            4  '_pay'
         254  CALL_FUNCTION_0       0 
         257  POP_TOP          

Parse error at or near `CALL_FUNCTION_768' instruction at offset 174

                    mall_utils.check_yueka_discount_notice(self.goods_id, lambda : after_yueka())

            else:
                node.setVisible(False)

    def set_item_info(self):
        self.panel.img_item.SetDisplayFrameByPath('', mall_utils.get_goods_pic_path(self.goods_id))
        if self.panel.icon_try:
            template_utils.init_mall_item_try_icon(self.panel.icon_try, self.goods_id)
        self.panel.lab_name.SetString(mall_utils.get_goods_name(self.goods_id))
        self.panel.lab_describe.SetString(mall_utils.get_goods_decs(self.goods_id))
        if not self.panel.lab_limit:
            return
        else:
            _, season_limit, season_num_info = mall_utils.buy_num_limite_by_season(self.goods_id)
            _, day_limit, day_num_info = mall_utils.buy_num_limite_by_day(self.goods_id)
            _, week_limit, week_num_info = mall_utils.buy_num_limite_by_week(self.goods_id)
            _, all_limit, all_num_info = mall_utils.buy_num_limit_by_all(self.goods_id)
            lab_limit = self.panel.lab_limit
            if season_num_info:
                num_info = season_num_info
                lab_limit and lab_limit.SetString(608049)
            elif day_num_info:
                num_info = day_num_info
                lab_limit and lab_limit.SetString(81062)
            elif week_num_info:
                num_info = week_num_info
                lab_limit and lab_limit.SetString(81449)
            elif all_num_info:
                num_info = all_num_info
                lab_limit and lab_limit.SetString(81371)
            else:
                lab_limit and lab_limit.setVisible(False)
                num_info = None
            if num_info:
                left_num, max_num = num_info
                color = '#SS' if left_num else '#SR'
                self.panel.lab_num.SetString(''.join([color, str(left_num), '#n', '/', str(max_num)]))
                for node in [self.panel.temp_btn_buy1, self.panel.temp_btn_buy1]:
                    node and node.btn_common.SetEnable(left_num > 0)

            lab_limit_total = self.panel.lab_limit_total
            lab_limit_total.setVisible(bool(all_num_info))
            if all_num_info:
                left_num, max_num = all_num_info
                lab_limit_total and lab_limit_total.SetString(get_text_by_id(608419).format(left_num, max_num))
            item_no = mall_utils.get_goods_item_no(self.goods_id)
            use_params = confmgr.get('lobby_item', str(item_no), default={}).get('use_params', {})
            self.panel.btn_preview.setVisible(bool(use_params.get('need_preview', 0) or use_params.get('need_probability', 0)))

            @self.panel.btn_preview.unique_callback()
            def OnClick(btn, touch, item_no=item_no, *args):
                wpos = touch.getLocation()
                global_data.emgr.show_item_desc_ui_event.emit(item_no, wpos)

            return

    def init_gift_list(self):
        reward_id = mall_utils.get_goods_item_reward_id(self.goods_id)
        list_gift = self.panel.list_gift
        if reward_id <= 0:
            list_gift and list_gift.setVisible(False)
            return
        self.panel.list_gift.setVisible(True)
        template_utils.init_common_reward_list(self.panel.list_gift, reward_id)

    def on_close(self, *args):
        self.close()

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