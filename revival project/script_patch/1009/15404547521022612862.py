# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/KizunaAIChargeWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gutils.mall_utils import is_pc_global_pay, is_steam_pay, get_goods_item_reward_id, buy_num_limite_by_day, buy_num_limit_by_all, limite_pay, get_pc_charge_price_str, get_charge_price_str, adjust_price
from logic.gutils.template_utils import init_tempate_mall_i_item, get_left_info
from logic.gutils.item_utils import get_lobby_item_name
from logic.gcommon.const import SHOP_PAYMENT_KIZUNA_AI_LOTTERY_TICKET
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.activity_utils import get_left_time
from logic.gcommon.common_const.activity_const import ACTIVITY_KIZUNA_AI_GIFT
from logic.client.path_utils import KIZUNA_AI_CHARGE_ITEM_PIC_PATH_0, KIZUNA_AI_CHARGE_ITEM_PIC_PATH_1, KIZUNA_AI_CHARGE_ITEM_PIC_PATH_2
from common.utils.timer import CLOCK
from common.cfg import confmgr
import cc
GOODS_ID_LIST = [
 '690325101', '690325102', '690325103']

class KizunaAIChargeWidget(object):

    def on_init_panel(self, panel):
        self.panel = panel
        self.is_pc_global_pay = is_pc_global_pay()
        self.ordered_jelly_goods_info_lst = None
        if global_data.lobby_mall_data and global_data.player:
            self.ordered_jelly_goods_info_lst = global_data.lobby_mall_data.get_activity_sale_info_list('KIZUNA_AI_GOODS')
        self.timer = None
        self.process_event(True)
        self.init_widget()
        self.refresh_all_info()
        self.register_timer()
        action_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.DelayTime.create(3.0),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]
        self.panel.runAction(cc.Sequence.create(action_list))
        global_data.player.call_server_method('attend_activity', (ACTIVITY_KIZUNA_AI_GIFT,))
        return

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'update_charge_info': self.refresh_all_info,
           'buy_good_success': self.refresh_all_info
           }
        if flag:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_reward_list(self, nd_list, goods_id):
        multiply = get_text_by_id(602012)
        reward_id = get_goods_item_reward_id(goods_id)
        reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list')
        nd_list.SetInitCount(len(reward_list))
        for index, (item_no, item_count) in enumerate(reward_list):
            reward_item = nd_list.GetItem(index)
            init_tempate_mall_i_item(reward_item.nd_item, item_no, 1)
            reward_item.lab_name.SetString(get_lobby_item_name(item_no))
            reward_item.lab_num.SetString(multiply + str(item_count))

            @reward_item.nd_item.btn_choose.unique_callback()
            def OnClick(btn, touch, item_id=item_no):
                wpos = touch.getLocation()
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, directly_world_pos=wpos)
                return

    def play_charge_item_anim(self, charge_item, is_special):
        show_anim, loop_anim = ('show', 'loop')
        if is_special:
            show_anim, loop_anim = ('show_02', 'loop_02')
        action_list = [cc.CallFunc.create(lambda : charge_item.PlayAnimation(show_anim)),
         cc.DelayTime.create(2.5),
         cc.CallFunc.create(lambda : charge_item.PlayAnimation(loop_anim))]
        charge_item.runAction(cc.Sequence.create(action_list))

    def init_widget(self):
        goods_id = '690325101'
        charge_item = self.panel.charge_list.GetItem(0)
        charge_item.setLocalZOrder(2)
        charge_item.nd_gift_common.setVisible(True)
        charge_item.nd_gift_special.setVisible(False)
        charge_item.lab_title_1.SetString(608526)
        self.play_charge_item_anim(charge_item, False)
        charge_item = charge_item.nd_gift_common
        charge_item.img_item_common.SetDisplayFrameByPath('', KIZUNA_AI_CHARGE_ITEM_PIC_PATH_0)
        self.init_reward_list(charge_item.list_item_1, goods_id)
        charge_item.list_item_2.SetInitCount(1)
        reward_item = charge_item.list_item_2.GetItem(0)
        init_tempate_mall_i_item(reward_item.nd_item, SHOP_PAYMENT_KIZUNA_AI_LOTTERY_TICKET, 1)

        @reward_item.nd_item.btn_choose.unique_callback()
        def OnClick(btn, touch):
            wpos = touch.getLocation()
            global_data.emgr.show_item_desc_ui_event.emit(SHOP_PAYMENT_KIZUNA_AI_LOTTERY_TICKET, None, directly_world_pos=wpos)
            return

        reward_item.lab_name.setVisible(False)
        reward_item.lab_num.setVisible(False)
        reward_item.lab_name_special.setVisible(True)
        reward_item.lab_name_special.SetString(608536)
        goods_id = '690325102'
        charge_item = self.panel.charge_list.GetItem(1)
        charge_item.setLocalZOrder(1)
        charge_item.nd_gift_common.setVisible(False)
        charge_item.nd_gift_special.setVisible(True)
        charge_item.lab_title_2.SetString(608527)
        self.play_charge_item_anim(charge_item, True)
        charge_item = charge_item.nd_gift_special
        charge_item.img_item_special.SetDisplayFrameByPath('', KIZUNA_AI_CHARGE_ITEM_PIC_PATH_1)
        charge_item.pnl_main_special.lab_text1.SetString(608532)
        charge_item.pnl_main_special.lab_text2.SetString(608533)
        self.init_reward_list(charge_item.list_item_3, goods_id)
        goods_id = '690325103'
        charge_item = self.panel.charge_list.GetItem(2)
        charge_item.nd_gift_common.setVisible(False)
        charge_item.nd_gift_special.setVisible(True)
        charge_item.lab_title_2.SetString(608528)
        self.play_charge_item_anim(charge_item, True)
        charge_item = charge_item.nd_gift_special
        charge_item.img_item_special.SetDisplayFrameByPath('', KIZUNA_AI_CHARGE_ITEM_PIC_PATH_2)
        charge_item.pnl_main_special.lab_text1.SetString(608534)
        charge_item.pnl_main_special.lab_text2.SetString(608535)
        self.init_reward_list(charge_item.list_item_3, goods_id)

    def _refresh_limit_buy_text(self, nd_lab, goods_id):
        _, _, num_info = buy_num_limite_by_day(goods_id)
        text = ''
        if num_info:
            left_num, max_num = num_info
            text += get_text_by_id(607205).format(left_num, max_num)
        _, _, num_info = buy_num_limit_by_all(goods_id)
        if num_info:
            left_num, max_num = num_info
            if text:
                text += ' '
            text += get_text_by_id(608419).format(left_num, max_num)
        nd_lab.SetString(text)

    def _set_buy_btn_enable(self, btn_buy, enable):
        btn_buy.SetEnable(enable)
        btn_buy.vx_button.setVisible(enable)

    def _refresh_charge_item_btn_buy_info(self, btn_buy, nd_lab, goods_id, index):
        has_limited = limite_pay(goods_id)
        if has_limited:
            self._set_buy_btn_enable(btn_buy, False)
            nd_lab.SetString(12014)
        elif self.ordered_jelly_goods_info_lst:
            jelly_goods_id, goods_info = self.ordered_jelly_goods_info_lst[index]
            if not goods_info:
                self._set_buy_btn_enable(btn_buy, False)
                nd_lab.SetString('******')
            else:
                self._set_buy_btn_enable(btn_buy, True)
                if is_pc_global_pay() or is_steam_pay():
                    price_txt = get_pc_charge_price_str(goods_info)
                else:
                    price_txt = get_charge_price_str(jelly_goods_id)
                nd_lab.SetString(adjust_price(price_txt))

                @btn_buy.unique_callback()
                def OnClick(*args):
                    if get_left_time(ACTIVITY_KIZUNA_AI_GIFT) <= 0:
                        self._set_buy_btn_enable(btn_buy, False)
                        nd_lab.SetString('******')
                        return
                    if is_pc_global_pay():
                        from logic.gutils.jump_to_ui_utils import jump_to_web_charge
                        jump_to_web_charge()
                    else:
                        global_data.player and global_data.player.pay_order(jelly_goods_id)

        else:
            self._set_buy_btn_enable(btn_buy, False)
            nd_lab.SetString('******')

    def refresh_all_info(self, *args):
        for index in range(3):
            goods_id = GOODS_ID_LIST[index]
            charge_item = self.panel.charge_list.GetItem(index)
            if index == 0:
                charge_item = charge_item.nd_gift_common
                lab_limit = charge_item.lab_limit_common
                btn_buy = charge_item.btn_buy_common
                lab_price = charge_item.btn_buy_common.lab_price_common
            else:
                charge_item = charge_item.nd_gift_special
                lab_limit = charge_item.lab_limit_special
                btn_buy = charge_item.btn_buy_special
                lab_price = charge_item.btn_buy_special.lab_price_special
            self._refresh_limit_buy_text(lab_limit, goods_id)
            self._refresh_charge_item_btn_buy_info(btn_buy, lab_price, goods_id, index)

    def _update_left_time(self):
        left_time_delta = get_left_time(ACTIVITY_KIZUNA_AI_GIFT)
        is_ending, left_text, left_time, left_unit = get_left_info(left_time_delta)
        if not is_ending:
            day_txt = get_text_by_id(left_text) + ': {0} '.format(left_time) + get_text_by_id(left_unit)
        else:
            day_txt = get_text_by_id(left_text)
        self.panel.lab_time.SetString(day_txt)

    def register_timer(self):
        self.unregister_timer()
        self.timer = global_data.game_mgr.register_logic_timer(self._update_left_time, interval=1.0, times=-1, mode=CLOCK)

    def unregister_timer(self):
        if self.timer:
            global_data.game_mgr.unregister_logic_timer(self.timer)
            self.timer = None
        return

    def on_finalize_panel(self):
        self.panel.stopAllActions()
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('loop')
        for index in range(3):
            charge_item = self.panel.charge_list.GetItem(index)
            charge_item.StopAnimation('show')
            charge_item.StopAnimation('loop')
            charge_item.StopAnimation('show_02')
            charge_item.StopAnimation('loop_02')
            charge_item.stopAllActions()

        self.unregister_timer()
        self.panel = None
        self.process_event(False)
        return

    def set_show(self, show):
        self.panel.setVisible(show)