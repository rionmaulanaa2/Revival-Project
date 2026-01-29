# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202111/ActivitySakuganLinkageTicket.py
from __future__ import absolute_import
import six
from six.moves import range
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import jump_to_ui_utils
import logic.gcommon.time_utility as tutil
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const
from cocosui import cc, ccui, ccs
from common.platform.dctool import interface
from logic.gutils.mall_utils import is_pc_global_pay, is_steam_pay, get_goods_item_reward_id, get_goods_item_task_id, buy_num_limit_by_all, limite_pay, get_pc_charge_price_str, get_charge_price_str, adjust_price
from logic.gutils.template_utils import init_tempate_mall_i_item, get_left_info
from logic.gutils.item_utils import get_lobby_item_name
from logic.gcommon.const import SHOP_PAYMENT_KIZUNA_AI_LOTTERY_TICKET
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import mall_utils

class ActivitySakuganLinkageTicket(ActivityBase):

    def on_init_panel(self):
        self._timer = 0
        self._timer_cb = {}
        self.is_pc_global_pay = is_pc_global_pay()
        from common.cfg import confmgr
        conf = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self._goods_list = conf.get('goods_list', [])
        if global_data.channel.is_steam_channel():
            self._goods_list = conf.get('goods_list_steam', [])
        if G_IS_NA_PROJECT or global_data.channel.is_steam_channel():
            self._goods_func_list = conf.get('goods_func_list_na', [])
        else:
            self._goods_func_list = conf.get('goods_func_list', [])
        self.init_event()
        self.register_timer()
        self.init_widget()
        action_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]
        self.panel.runAction(cc.Sequence.create(action_list))
        if len(self._goods_list) >= 3:
            reward_id = mall_utils.get_goods_item_reward_id(self._goods_list[2])
            if reward_id:
                import common.cfg.confmgr as confmgr
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                if not reward_conf:
                    log_error('reward_id is not exist in common_reward_data', reward_id)
                else:
                    reward_list = reward_conf.get('reward_list', [])
                    reward_count = len(reward_list)
                    for idx in range(reward_count):
                        item_no, item_num = reward_list[idx]
                        reward_item = getattr(self.panel, 'temp_icon_orange_%d' % (idx + 1))
                        if reward_item:
                            reward_item = getattr(reward_item, 'temp_item_1')
                            init_tempate_mall_i_item(reward_item, item_no, item_num, show_tips=True, force_extra_ani=False)

        @self.panel.bar_prize_1.callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_activity, jump_to_lottery
            jump_to_lottery('32')

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.refresh_goods_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.panel and self.panel.stopAllActions()
        self.panel = None
        self.unregister_timer()
        self.process_event(False)
        return

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def get_end_time(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        return conf.get('cEndTime', 0)

    def init_widget(self):

        def callback():
            now_time = tutil.get_server_time()
            expire_ts = self.get_end_time()
            left_time = expire_ts - now_time
            if left_time <= 0:
                self.panel.lab_sakugan_time.SetString(606071)
            else:
                self.panel.lab_sakugan_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time_day_hour_minitue(left_time)))

        self._timer_cb[0] = callback
        callback()
        self.refresh_goods_reward()

    def refresh_goods_reward(self):
        now_time = tutil.get_server_time()
        expire_ts = self.get_end_time()
        left_time = expire_ts - now_time
        goods_func_sid_list = self._goods_func_list
        btns = [self.panel.btn_01, self.panel.btn_02, self.panel.btn_03]
        price_items = [self.panel.temp_price_1, self.panel.temp_price_2, self.panel.temp_price_3]
        lab_limit = [self.panel.lab_label_1, self.panel.lab_label_2, self.panel.lab_label_3]
        for i, func_str in enumerate(goods_func_sid_list):
            goods_lst = goods_func_sid_list[i]
            goods_id = str(self._goods_list[i])
            has_bought = limite_pay(goods_id)
            btn_buy = btns[i]
            lab_price = price_items[i].lab_price
            limit_num_all = mall_utils.get_goods_limit_num_all(goods_id)
            lab_limit[i].SetString(get_text_by_id(82279).format(limit_num_all))
            if has_bought:
                self.panel.StopAnimation('loop_0%d' % (i + 1))
            elif not self.panel.IsPlayingAnimation('loop_0%d' % (i + 1)):
                self.panel.PlayAnimation('loop_0%d' % (i + 1))
            if has_bought:
                btn_buy.SetEnable(False)
                lab_price.setVisible(False)
                btn_buy.SetText(12014)
            elif goods_lst:
                goods_info = global_data.lobby_mall_data.get_activity_sale_info(goods_lst)
                if not goods_info:
                    btn_buy.SetEnable(False)
                    lab_price.setVisible(False)
                    btn_buy.SetText('******')
                    self.panel.StopAnimation('loop_0%d' % (i + 1))
                elif left_time <= 0:
                    btn_buy.SetEnable(False)
                    lab_price.setVisible(False)
                    btn_buy.SetText(81154)
                else:
                    btn_buy.SetEnable(True)
                    lab_price.setVisible(True)
                    btn_buy.SetText('')
                    if self.is_pc_global_pay or is_steam_pay():
                        price_txt = get_pc_charge_price_str(goods_info)
                    else:
                        key = goods_info['goodsid']
                        price_txt = get_charge_price_str(key)
                    lab_price.SetString(adjust_price(str(price_txt)))

                    @btn_buy.unique_callback()
                    def OnClick(btn, touch, _goods_info=goods_info):
                        if self.is_pc_global_pay:
                            jump_to_ui_utils.jump_to_web_charge()
                        elif _goods_info:
                            global_data.player and global_data.player.pay_order(_goods_info['goodsid'])

            else:
                from logic.gutils.mall_utils import get_mall_item_price
                prices = get_mall_item_price(str(goods_id))
                temp_price = price_items[i]
                for i, price_info in enumerate(prices):
                    if temp_price:
                        template_utils.init_price_template(price_info, temp_price)

                temp_price.img_price.setVisible(True)

                @btn_buy.unique_callback()
                def OnClick(btn, touch, goods_id=goods_id):
                    from logic.comsys.mall_ui import BuyConfirmUIInterface
                    import logic.gcommon.const as gconst
                    if not activity_utils.is_activity_in_limit_time(self._activity_type):
                        return
                    has_bought = limite_pay(goods_id)
                    if not has_bought:
                        global_data.player.buy_goods(goods_id, 1, gconst.SHOP_PAYMENT_YUANBAO)