# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/GiftBoxItemLotteryUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_CLOSE
from logic.comsys.charge_ui.LeftTimeCountDownWidget import LeftTimeCountDownWidget
from logic.gcommon import time_utility as tutil
from logic.gutils import trigger_gift_utils
from logic.gutils import template_utils
from logic.gutils import mall_utils
import logic.gcommon.const as gconst
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gcommon.common_utils.local_text import get_text_by_id, get_cur_text_lang, LANG_CN, LANG_EN
from logic.gutils.fly_out_animation import FlyOutMotion
import cc
from logic.gutils.reward_item_ui_utils import refresh_item_info, play_item_appear_to_idle_animation
from logic.client.const import mall_const
from common.cfg import confmgr
from logic.gutils import jump_to_ui_utils

class GiftBoxItemLotteryUI(BasePanel):
    PANEL_CONFIG_NAME = 'charge/charge_gift_box_new'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CLOSE
    DELAY_CLOSE_TAG = 31415926
    FLY_OUT_ANIM_TAG = 31415927
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': '_on_click_close_btn',
       'btn_buy.OnClick': '_on_click_buy'
       }

    def on_init_panel(self, gift_info, **kwargs):
        self.init_parameters(gift_info)
        self.init_widget()
        self.bind_event(True)

    def init_parameters(self, gift_info):
        self._gift_info = gift_info
        self._goods_list = self._gift_info.get('goods_list', [])
        self._cash_only = self._gift_info.get('cash_only', 0)
        chance_gift_no = self._gift_info.get('chance_gift_no', None)
        if self._cash_only:
            self._goods_func_str_or_goods_list = self.get_goods_func_str_or_goods_list(chance_gift_no)
            if not self._goods_func_str_or_goods_list:
                log_error('chance gift sdk func failed!', self._goods_list[0], self._goods_func_str_or_goods_list)
        else:
            self._goods_func_str_or_goods_list = ''
        self._wait_for_charge_result = None
        self._cash_goods_info = None
        self.is_pc_global_pay = mall_utils.is_pc_global_pay()
        _item_list = []
        for i, goods_id in enumerate(self._goods_list):
            item_type = mall_utils.get_goods_item_item_type(goods_id)
            if item_type in [mall_const.LOTTERY_TYPE, mall_const.REWARD_TYPE]:
                reward_id = mall_utils.get_goods_item_reward_id(goods_id)
                buy_reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
                _item_list.extend(buy_reward_list)
            else:
                _item_list.append([mall_utils.get_goods_item_no(goods_id), mall_utils.get_goods_num(goods_id)])

        self._item_list = _item_list
        self._left_time_widget = None
        self._closing = False
        self._fly_node = self.panel.nd_content_big
        self._fly_src_wpos = self._fly_node.getParent().convertToWorldSpace(cc.Vec2(*self._fly_node.GetPosition()))
        self._fly_ref_node_wpos = self._fly_src_wpos
        self._item_animation_index = -1
        if self._cash_only:
            self.panel.nd_title.setVisible(False)
            self.panel.nd_title_6.setVisible(True)
            self.panel.img_time_bar.setVisible(False)
            self.panel.lab_tips.SetString(609645)
            self.panel.temp_price.setVisible(False)
            if len(self._goods_list) != 1:
                log_error('ERROR!!!when in cash only mode, good list should be of length 1, ', self._goods_list)
        else:
            self.panel.lab_tips.SetString(self.get_gift_tip_text_id(chance_gift_no))
        return

    def get_goods_func_str_or_goods_list(self, chance_gift_no):
        conf = confmgr.get('chance_gift', default={})
        if not conf or not chance_gift_no:
            return ''
        gift_info = conf.get(str(chance_gift_no), {})
        return gift_info.get('goods_func_str', '')

    def get_gift_tip_text_id(self, chance_gift_no):
        conf = confmgr.get('chance_gift', default={})
        if not conf or not chance_gift_no:
            return 12182
        gift_info = conf.get(str(chance_gift_no))
        if gift_info:
            tip_text_id = gift_info.get('tip_text_id')
            if tip_text_id:
                return tip_text_id
        return 12182

    def bind_event(self, bind):
        e_conf = {'buy_good_fail': self.buy_good_fail,
           'buy_good_success': self.refresh_goods_reward
           }
        if bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def on_finalize_panel(self):
        super(GiftBoxItemLotteryUI, self).on_finalize_panel()
        self.bind_event(False)
        self._gift_info = None
        if self._left_time_widget:
            self._left_time_widget.destroy()
            self._left_time_widget = None
        return

    def init_widget(self):
        self._init_left_time_widget()
        self._init_ui_text()
        self._init_gift_goods_items()
        for animation_name in trigger_gift_utils.get_gift_ui_animation_names(False, True):
            self.panel.PlayAnimation(animation_name)

        self._play_item_color_animation()

    def _init_left_time_widget(self):
        expire_time = self._gift_info.get('expire_time', 0)
        if expire_time > tutil.get_server_time():
            self._left_time_widget = LeftTimeCountDownWidget(self.panel, self.panel.lab_time, lambda timestamp: tutil.get_delta_time_str(timestamp))
            self._left_time_widget.begin_count_down_time(expire_time, self._time_up_callback, use_big_interval=False)

    def _init_ui_text(self):
        show_discount = self._gift_info.get('show_discount', None)
        if show_discount is not None:
            discount_text = trigger_gift_utils.get_gift_discount_text(show_discount, get_cur_text_lang())
        else:
            discount_text = trigger_gift_utils.get_gift_discount_text(self._gift_info.get('discount', 0), get_cur_text_lang())
        lab_discount = self._cash_only or self.panel.nd_title.lab_discount if 1 else self.panel.nd_title_6.lab_discount
        if discount_text:
            lab_discount.SetString(discount_text)
            lab_discount.setVisible(True)
        else:
            lab_discount.setVisible(False)
        return

    def _init_gift_goods_items(self):
        if not self._item_list:
            return
        if len(self._item_list) <= 3:
            self.panel.list_item_1.setVisible(True)
            self.panel.list_item_2.setVisible(False)
            list_item = self.panel.list_item_1
        else:
            self.panel.list_item_1.setVisible(False)
            self.panel.list_item_2.setVisible(True)
            list_item = self.panel.list_item_2
        list_item.DeleteAllSubItem()
        list_item.SetInitCount(len(self._item_list))
        for i, item_info in enumerate(self._item_list):
            item_no, item_num = item_info
            ui_item = list_item.GetItem(i)
            template_utils.init_tempate_mall_i_item(ui_item.temp_reward, item_no, item_num=item_num, show_tips=True)

        if not self._cash_only:
            price_info = {'original_price': self.get_total_original_price(),'discount_price': self._gift_info.get('discount_price', 0),
               'goods_payment': gconst.SHOP_PAYMENT_YUANBAO
               }
            COLOR = [
             '#SW', '#SR', '#BC']
            template_utils.init_price_template(price_info, self.panel.temp_price, color=COLOR)
        else:
            self.panel.lab_price.setVisible(True)
            if type(self._goods_func_str_or_goods_list) in [str, six.text_type]:
                func_str = self._goods_func_str_or_goods_list
                goods_info = getattr(global_data.lobby_mall_data, func_str)()
            else:
                good_list = self._goods_func_str_or_goods_list
                goods_info = global_data.lobby_mall_data.get_activity_sale_info(good_list)
            self._cash_goods_info = goods_info
            if not goods_info:
                self.panel.btn_buy.SetEnable(False)
                self.panel.lab_price.SetString('******')
            else:
                self.panel.btn_buy.SetEnable(True)
                if self.is_pc_global_pay or mall_utils.is_steam_pay():
                    price_txt = mall_utils.get_pc_charge_price_str(goods_info)
                else:
                    key = goods_info['goodsid']
                    price_txt = mall_utils.get_charge_price_str(key)
                self.panel.lab_price.SetString(mall_utils.adjust_price(str(price_txt)))

    def get_total_original_price(self):
        price_list = []
        goods_list = self._gift_info.get('goods_list')
        for i, goods_id in enumerate(goods_list):
            prices = mall_utils.get_mall_item_price(goods_id, pick_list=('yuanbao', ))
            if prices:
                price_list.append(prices[0])

        pay_prices = mall_utils.get_mall_item_real_pay_price(price_list)
        total_prices = template_utils.merge_goods_prices(pay_prices)
        if total_prices:
            total_price = total_prices[0]
            original_price = total_price.get('original_price', 0)
        else:
            original_price = int(self._gift_info.get('discount_price', 0) / self._gift_info.get('discount', 1.0))
        return original_price

    def get_ui_item_list(self):
        if len(self._item_list) <= 3:
            return self.panel.list_item_1
        else:
            return self.panel.list_item_2

    def _time_up_callback(self):
        if global_data.player:
            global_data.player.on_trigger_gift_expire(self._gift_info.get('id'))
        self.close()

    def _on_click_buy(self, btn, touch):
        if not self._cash_only:
            discount_price = self._gift_info.get('discount_price', 0)
            if mall_utils.check_payment(gconst.SHOP_PAYMENT_YUANBAO, discount_price, pay_tip=True):
                if global_data.player:
                    global_data.player.buy_chance_gift(self._gift_info.get('id'))
            elif global_data.player:
                gift_id = self._gift_info.get('id')
                from logic.gcommon.common_const.shop_const import LOG_GIFT_STATE_CHARGE
                global_data.player.call_server_method('chance_gift_log', (gift_id, LOG_GIFT_STATE_CHARGE))
        else:
            _goods_info = self._cash_goods_info
            self._wait_for_charge_result = True
            if self.is_pc_global_pay:
                jump_to_ui_utils.jump_to_web_charge()
            elif _goods_info:
                global_data.player and global_data.player.pay_order(_goods_info['goodsid'])

    def _on_confirm_close(self):
        if not self._gift_info:
            self.close()
            return
        if self._gift_info.get('expire_time', 0) > tutil.get_server_time():
            global_data.emgr.lobby_add_giftbox_entry.emit(self._gift_info)
        else:
            self._time_up_callback()
        self._try_close()

    def _on_click_close_btn(self, *args):
        if not self._cash_only:
            left_time_stamp = self._gift_info.get('expire_time') - tutil.get_server_time()
            left_time_str = tutil.get_readable_time(left_time_stamp)
            SecondConfirmDlg2().confirm(content=get_text_by_id(608308).format(left_time_str), confirm_callback=self._on_confirm_close)
        else:
            self._on_confirm_close()

    def _try_close(self):
        if not self.is_valid():
            return
        if self._closing:
            return
        self._closing = True
        for animation_name in trigger_gift_utils.get_gift_ui_animation_names(False, True):
            self.panel.StopAnimation(animation_name)

        dst_wpos, motion = self._get_fly_animation_params()
        if dst_wpos and motion:
            close_animation_name = trigger_gift_utils.get_gift_ui_animation_names(False, False)
            self.panel.PlayAnimation(close_animation_name)
            delay_close_time = self.panel.GetAnimationMaxRunTime(close_animation_name)
            self._play_fly_animation(self._fly_src_wpos, dst_wpos, motion)

            def cb():
                self.close()

            self.DelayCallWithTag(delay_close_time, cb, self.DELAY_CLOSE_TAG)
        else:
            self.close()

    def on_click_close_btn(self):
        self._try_close()

    def _play_fly_animation(self, src_wpos, dst_wpos, motion):
        import time
        start_t = time.time()

        def update_motion(_, prev_t=[
 start_t]):
            cur_time = time.time()
            delta = cur_time - prev_t[0]
            motion.update(delta)
            node = self._fly_node
            wpos = motion.get_pos()
            lpos = node.getParent().convertToNodeSpace(wpos)
            node.setPosition(lpos)
            prev_t[0] = cur_time

        self.panel.StopTimerActionByTag(self.FLY_OUT_ANIM_TAG)
        duration = motion.get_max_time()
        self.panel.TimerActionByTag(self.FLY_OUT_ANIM_TAG, update_motion, duration)

    def _get_fly_animation_params(self):
        ui = global_data.ui_mgr.get_ui('LobbyUI')
        if ui is not None:
            ref_dst_wpos = cc.Vec2(ui.get_trigger_gift_cocos_wpos())
            diff_vec = cc.Vec2(ref_dst_wpos)
            diff_vec.subtract(self._fly_ref_node_wpos)
            dst_wpos = cc.Vec2(self._fly_src_wpos)
            dst_wpos.add(diff_vec)
            motion = FlyOutMotion(self._fly_src_wpos, dst_wpos)
            return (
             dst_wpos, motion)
        else:
            return (None, None)
            return

    def _play_item_color_animation(self):

        def show_animation():
            if self._item_animation_index == 0 and len(self._item_list) == 1:
                return
            self._item_animation_index = (self._item_animation_index + 1) % len(self._item_list)
            item_no, item_num = self._item_list[self._item_animation_index]
            ui_item_list = self.get_ui_item_list()
            ui_item = ui_item_list.GetItem(self._item_animation_index)
            play_item_appear_to_idle_animation(ui_item, item_no, item_num, show_animation, callback_advance_rate=0.8)

        show_animation()

    def buy_good_fail(self):
        if self._wait_for_charge_result is None:
            return
        else:
            show_discount = self._gift_info.get('show_discount', None) or self._gift_info.get('discount', 0)
            fail_ui = global_data.ui_mgr.show_ui('ChargeGiftBoxFailUI', 'logic.comsys.common_ui')
            if type(self._goods_func_str_or_goods_list) in [str, six.text_type]:
                func_str = self._goods_func_str_or_goods_list
                goods_info = getattr(global_data.lobby_mall_data, func_str)()
            else:
                good_list = self._goods_func_str_or_goods_list
                goods_info = global_data.lobby_mall_data.get_activity_sale_info(good_list)
            fail_ui.show_panel(self._goods_list[0], '', int(-100 * (1.0 - show_discount)), goods_info=goods_info)
            self._wait_for_charge_result = None
            return

    def refresh_goods_reward(self):
        self._wait_for_charge_result = None
        return