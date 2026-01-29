# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySpringGiftTickets.py
from __future__ import absolute_import
from six.moves import range
from logic.gutils import mall_utils
from logic.gutils.activity_utils import get_left_time
from logic.gutils.template_utils import get_left_info, init_common_reward_list
from logic.comsys.activity.ActivityTemplate import ActivityBase
DISCOUNT_lST = [
 '-66%', '-55%', '-25%', ' -25%']
NAME_ID_LST = [400311, 400312, 400313, 400314]

class ActivitySpringGiftTickets(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivitySpringGiftTickets, self).__init__(dlg, activity_type)
        self._ordered_jelly_goods_info_lst = None
        self._price_widget = None
        self._init_parameters()
        self._init_event()
        return

    def _init_parameters(self):
        if global_data.lobby_mall_data and global_data.player:
            self._ordered_jelly_goods_info_lst = global_data.lobby_mall_data.get_activity_sale_info_list('SPRING_GIFT_TICKETS_GOODS')

    def on_init_panel(self):
        from logic.gcommon import time_utility
        from logic.comsys.archive.archive_manager import ArchiveManager
        archive_data = ArchiveManager().get_archive_data('activity_setting')
        from logic.gcommon.time_utility import get_server_time
        now_day_time = time_utility.get_time_string('%d', ts=get_server_time())
        archive_data.set_field(str(self._activity_type), now_day_time)
        archive_data.save()
        from logic.gutils.activity_utils import get_activity_open_time
        start_str, end_str = get_activity_open_time(self._activity_type)
        if start_str and end_str and self.panel.lab_time:
            self.panel.lab_time.SetString('{0} - {1}'.format(start_str, end_str))
        if self.panel.lab_time_down:
            left_time_delta = get_left_time(self._activity_type)
            is_ending, left_text, left_time, left_unit = get_left_info(left_time_delta)
            if not is_ending:
                day_txt = get_text_by_id(left_text) + '<size=35> {0} </size>'.format(left_time) + get_text_by_id(left_unit)
            else:
                day_txt = get_text_by_id(left_text)
            self.panel.lab_time_down.SetString(day_txt)
        self._init_price_widget()
        self._init_goods_show()
        self._update_goods_show()

    def _init_goods_show(self):
        for name_idx in range(len(NAME_ID_LST)):
            item_widget = getattr(self.panel, 'temp_content_0%d' % (name_idx + 1))
            item_widget.lab_title.SetString(NAME_ID_LST[name_idx])

        goods_cnt = len(self._ordered_jelly_goods_info_lst)
        for idx in range(goods_cnt):
            item_widget = getattr(self.panel, 'temp_content_0%d' % (idx + 1))
            jelly_goods_id, _ = self._ordered_jelly_goods_info_lst[idx]
            item_widget.nd_tag.lab_tag1.SetString(str(DISCOUNT_lST[idx]))

            @item_widget.btn_buy_common.unique_callback()
            def OnClick(btn, touch, goods_id=jelly_goods_id):
                if mall_utils.is_pc_global_pay():
                    from logic.gutils.jump_to_ui_utils import jump_to_web_charge
                    jump_to_web_charge()
                else:
                    global_data.player and global_data.player.pay_order(goods_id)

    def _update_goods_show(self):
        goods_cnt = len(self._ordered_jelly_goods_info_lst)
        for idx in range(goods_cnt):
            item_widget = getattr(self.panel, 'temp_content_0%d' % (idx + 1))
            jelly_goods_id, goods_info = self._ordered_jelly_goods_info_lst[idx]
            game_goods_id = global_data.player.get_goods_info(jelly_goods_id).get('cShopGoodsId')
            reward_id = mall_utils.get_goods_item_reward_id(game_goods_id)
            init_common_reward_list(item_widget.list_item, reward_id)
            item_widget.img_product.SetDisplayFrameByPath('', mall_utils.get_goods_pic_path(game_goods_id))
            limit_buy, num_info, limit_txt_id = mall_utils.get_limit_info(game_goods_id)
            if limit_buy:
                left_num, max_num = num_info
                if left_num:
                    text_show = str(left_num) + '/' + str(max_num)
                else:
                    text_show = '<color=0xffb3b3ff>{}</color>'.format(left_num) + '/' + str(max_num)
                item_widget.lab_num.SetString(text_show)
                item_widget.lab_limit.SetString(limit_txt_id)
                self._set_enable_buy(item_widget, left_num > 0)
            has_limited = mall_utils.limite_pay(game_goods_id)
            if has_limited:
                self._set_enable_buy(item_widget, False)
                item_widget.lab_price_common.SetString(12121)
            elif not goods_info:
                self._set_enable_buy(item_widget, False)
                item_widget.lab_price_common.SetString('******')
            else:
                self._set_enable_buy(item_widget, True)
                if mall_utils.is_pc_global_pay() or mall_utils.is_steam_pay():
                    price_txt = mall_utils.get_pc_charge_price_str(goods_info)
                else:
                    price_txt = mall_utils.get_charge_price_str(jelly_goods_id)
                item_widget.lab_price_common.SetString(mall_utils.adjust_price(str(price_txt)))

    def _set_enable_buy(self, widget, enable):
        widget.btn_buy_common.SetEnable(enable)
        widget.btn_buy_common.setVisible(enable)
        widget.btn_bar_2.setVisible(not enable)

    def refresh_panel(self):
        if self._ordered_jelly_goods_info_lst is None:
            if global_data.lobby_mall_data and global_data.player:
                self._ordered_jelly_goods_info_lst = global_data.lobby_mall_data.get_activity_sale_info_list('SPRING_GIFT_TICKETS_GOODS')
                self._update_goods_show()
        return

    def set_show(self, show, is_init=False):
        super(ActivitySpringGiftTickets, self).set_show(show, is_init)
        self.panel.stopAllActions()
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('loop')
        import cc
        action_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]
        self.panel.runAction(cc.Sequence.create(action_list))

    def _init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        event_mgr = global_data.emgr
        e_event = {'update_charge_info': self._update_goods_show,
           'buy_good_success': self._buy_good_success
           }
        if is_bind:
            event_mgr.bind_events(e_event)
        else:
            event_mgr.unbind_events(e_event)

    def _init_price_widget--- This code section failed: ---

 168       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'panel'
           6  LOAD_ATTR             1  'list_price'
           9  POP_JUMP_IF_FALSE   114  'to 114'

 169      12  LOAD_CONST            1  ''
          15  LOAD_CONST            2  ('SHOP_PAYMENT_YUANBAO', 'SHOP_PAYMENT_ITEM_VALUABLE_CATTLE_COIN', 'SHOP_PAYMENT_ITEM_SPRING_COUPON')
          18  IMPORT_NAME           2  'logic.gcommon.const'
          21  IMPORT_FROM           3  'SHOP_PAYMENT_YUANBAO'
          24  STORE_FAST            1  'SHOP_PAYMENT_YUANBAO'
          27  IMPORT_FROM           4  'SHOP_PAYMENT_ITEM_VALUABLE_CATTLE_COIN'
          30  STORE_FAST            2  'SHOP_PAYMENT_ITEM_VALUABLE_CATTLE_COIN'
          33  IMPORT_FROM           5  'SHOP_PAYMENT_ITEM_SPRING_COUPON'
          36  STORE_FAST            3  'SHOP_PAYMENT_ITEM_SPRING_COUPON'
          39  POP_TOP          

 170      40  LOAD_CONST            1  ''
          43  LOAD_CONST            3  ('PriceUIWidget',)
          46  IMPORT_NAME           6  'logic.comsys.mall_ui.PriceUIWidget'
          49  IMPORT_FROM           7  'PriceUIWidget'
          52  STORE_FAST            4  'PriceUIWidget'
          55  POP_TOP          

 171      56  LOAD_FAST             4  'PriceUIWidget'
          59  LOAD_FAST             4  'PriceUIWidget'
          62  LOAD_CONST            0  ''
          65  LOAD_CONST            5  'list_money_node'
          68  LOAD_FAST             0  'self'
          71  LOAD_ATTR             0  'panel'
          74  LOAD_ATTR             1  'list_price'
          77  CALL_FUNCTION_513   513 
          80  LOAD_FAST             0  'self'
          83  STORE_ATTR            9  '_price_widget'

 172      86  LOAD_FAST             0  'self'
          89  LOAD_ATTR             9  '_price_widget'
          92  LOAD_ATTR            10  'show_money_types'
          95  LOAD_FAST             2  'SHOP_PAYMENT_ITEM_VALUABLE_CATTLE_COIN'
          98  LOAD_FAST             3  'SHOP_PAYMENT_ITEM_SPRING_COUPON'
         101  LOAD_FAST             1  'SHOP_PAYMENT_YUANBAO'
         104  BUILD_LIST_3          3 
         107  CALL_FUNCTION_1       1 
         110  POP_TOP          
         111  JUMP_FORWARD          0  'to 114'
       114_0  COME_FROM                '111'
         114  LOAD_CONST            0  ''
         117  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_513' instruction at offset 77

    def _buy_good_success(self, *args):
        global_data.emgr.refresh_activity_redpoint.emit()
        self._update_goods_show()

    def on_finalize_panel(self):
        if self._price_widget:
            self._price_widget.destroy()
            self._price_widget = None
        self.process_event(False)
        return