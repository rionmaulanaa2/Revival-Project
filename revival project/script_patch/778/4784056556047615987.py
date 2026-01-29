# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/LimitChargeWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from common.cfg import confmgr
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils import jump_to_ui_utils
import logic.gcommon.time_utility as tutil
from logic.gcommon.common_const import activity_const
from logic.gutils.activity_utils import need_remain_weekly_card_renewal, save_weekly_card_tab_open_time
from cocosui import cc, ccui, ccs

class LimitChargeWidget(object):

    def on_init_panel(self, panel):
        self.panel = panel
        self._timer = 0
        self._timer_cb = {}
        self._weekly_goods_list = [
         '20603500', '20603501']
        self._goods_names = [609044, 609045, 609046]
        self.is_pc_global_pay = mall_utils.is_pc_global_pay()
        self.process_event(True)
        self.register_timer()
        self.init_widget()
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time('ChargeUINew', self.__class__.__name__)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_charge_info': self.refresh_goods,
           'update_weekly_card_info': self.refresh_goods,
           'buy_good_success': self.refresh_goods
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.panel = None
        self.unregister_timer()
        self.process_event(False)
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time('ChargeUINew', self.__class__.__name__)
        return

    def set_show(self, show):
        self.panel.setVisible(show)

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

    def init_widget(self):
        if not (self.panel.charge_list.GetItemCount() > 0 and self.panel.charge_list.IsAllLoaded()):
            self.panel.nd_title.setVisible(False)
        self.panel.charge_list.setTouchEnabled(False)

        def callback():
            left_time = tutil.get_next_utc8_sunday_8(apply_ea=1)
            self.panel.lab_time.SetString(get_text_by_id(607451, [tutil.get_readable_time_day_hour_minitue(left_time)]))

        self._timer_cb[0] = callback
        callback()

        @self.panel.charge_list.callback()
        def OnCreateItem(lv, idx, ui_item):
            if not (self.panel and self.panel.isValid()):
                return
            self.OnChargeCreateItem(lv, idx, ui_item)

        if self.is_pc_global_pay:
            self.panel.charge_list.SetInitCount(1)
        else:
            self.panel.charge_list.SetInitCount(3)

    def OnChargeCreateItem(self, lv, idx, ui_item):
        if idx == 0:
            item_widget = self.panel.charge_list.GetItem(0)
            item_widget.lab_title_2.SetString(self._goods_names[0])
            item_widget.img_item_special.SetDisplayFrameByPath('', 'gui/ui_res_2/charge/icon_gifts_week_1.png')
            item_widget.lab_tips_1.SetString(get_text_by_id(606013, {'num': 10}))
            btn_tips = item_widget.btn_tips

            @btn_tips.unique_callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(607443, 607440)
                x, y = btn_tips.GetPosition()
                wpos = btn_tips.GetParent().ConvertToWorldSpace(x, y)
                dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
                template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

            reward_id = activity_const.WEEKLYCARD_FIRST_BUY_REWARD
            template_utils.init_common_reward_list(item_widget.list_item_2, reward_id)
            reward_id = activity_const.WEEKLYCARD_DAY_REWARD
            template_utils.init_common_reward_list(item_widget.list_item_3, reward_id)
        elif idx == 1:
            item_widget = self.panel.charge_list.GetItem(1)
            item_widget.lab_title_1.SetString(self._goods_names[1])
            item_widget.img_item_common.SetDisplayFrameByPath('', 'gui/ui_res_2/charge/icon_gifts_week_2.png')
            btn_tips_common = item_widget.btn_tips_common
            btn_tips_common.setVisible(True)

            @btn_tips_common.unique_callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(607443, 607441)
                x, y = btn_tips_common.GetPosition()
                wpos = btn_tips_common.GetParent().ConvertToWorldSpace(x, y)
                dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
                template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

            goods_id = self._weekly_goods_list[0]
            reward_id = mall_utils.get_goods_item_reward_id(goods_id)
            template_utils.init_common_reward_list(item_widget.list_item_1, reward_id)
            count = item_widget.list_item_1.GetItemCount()
            _item = item_widget.list_item_1.GetItem(count - 1)
            _item.icon_up.setVisible(True)
            _item.icon_up.lab_prob.setVisible(False)
            _item.icon_up.lab_num.setVisible(True)
            _item.icon_up.lab_num.SetString('+30%')
        elif idx == 2:
            item_widget = self.panel.charge_list.GetItem(2)
            item_widget.lab_title_1.SetString(self._goods_names[2])
            item_widget.img_item_common.SetDisplayFrameByPath('', 'gui/ui_res_2/charge/icon_gifts_week_3.png')
            goods_id = self._weekly_goods_list[1]
            reward_id = mall_utils.get_goods_item_reward_id(goods_id)
            template_utils.init_common_reward_list(item_widget.list_item_1, reward_id)
        if self.panel.charge_list.IsAllLoaded():
            allItem = self.panel.charge_list.GetAllItem()
            for idx, item_widget in enumerate(allItem):
                if idx == 0:
                    item_widget.nd_gift_common.setVisible(False)
                    item_widget.nd_gift_special.setVisible(True)
                elif idx == 1:
                    item_widget.nd_gift_common.setVisible(True)
                    item_widget.nd_gift_special.setVisible(False)
                elif idx == 2:
                    item_widget.nd_gift_common.setVisible(True)
                    item_widget.nd_gift_special.setVisible(False)

            self.refresh_goods()
            if need_remain_weekly_card_renewal():
                save_weekly_card_tab_open_time()
                global_data.player.read_activity_list(activity_const.ACTIVITY_WEEKLYCARD)
            self.show_ani()
            self.panel.PlayAnimation('show')

    def show_ani(self):
        if not self.panel.charge_list.IsAllLoaded():
            return
        acts = []
        count = 3
        if self.is_pc_global_pay:
            count = 1
        for i in range(count):

            def callback(index=i):
                self._show_ani(index)

            acts.append(cc.DelayTime.create(0.05 * i))
            acts.append(cc.CallFunc.create(callback))

        act = cc.Sequence.create(acts)
        self.panel.runAction(act)

    def _show_ani(self, index):
        if not self.panel:
            return
        item_widget = self.panel.charge_list.GetItem(index)
        btn = item_widget.btn_buy_common
        str_type = 'common'
        if index == 0:
            str_type = 'special'
            btn = item_widget.btn_buy_special
        ani_name = 'show_{}'.format(str_type)
        item_widget.PlayAnimation(ani_name)
        max_time = item_widget.GetAnimationMaxRunTime(ani_name)

        def callback(_item_widget=item_widget, _str_type=str_type):
            _item_widget.StopAnimation(ani_name)
            if btn.IsEnable():
                _item_widget.PlayAnimation('loop_{}'.format(_str_type))

        item_widget.SetTimeOut(max_time, callback)

    def refresh_btns(self):
        count = self.panel.charge_list.GetItemCount()
        for i in range(count):
            item_widget = self.panel.charge_list.GetItem(i)
            btn = item_widget.btn_buy_common
            btn_vx = item_widget.btn_vx_common
            str_type = 'common'
            if i == 0:
                str_type = 'special'
                btn = item_widget.btn_buy_special
                btn_vx = item_widget.btn_vx_special
            if not btn.IsEnable():
                btn_vx.setVisible(False)
                item_widget.StopAnimation('loop_{}'.format(str_type))

    def refresh_goods(self):
        if not self.panel.charge_list.IsAllLoaded():
            return
        player = global_data.player
        item_widget = self.panel.charge_list.GetItem(0)
        has_weeklycard = player.has_weeklycard()
        item_widget.btn_buy_special.setVisible(False)
        item_widget.nd_buy_early.setVisible(False)
        goods_info = global_data.lobby_mall_data.get_activity_sale_info('WEEKLY_CARD_GOODS')
        if has_weeklycard:
            now_time = tutil.get_server_time()
            time = player.get_weeklycard_time()
            has_payed = player.get_weeklycard_payed()
            left_time = time - now_time
            item_widget.lab_limit_special.SetString(get_text_by_id(606009, [tutil.get_readable_time_day_hour_minitue(left_time)]))
            can_renewal = False
            if not has_payed:
                can_renewal = True
            has_received = player._weeklycard_daily
            if can_renewal:
                btn_get = item_widget.btn_get
                item_widget.nd_buy_early.setVisible(True)
                item_widget.btn_get.SetEnable(not has_received)
                item_widget.btn_get.lab_get.SetString(80866 if has_received else 80930)
            else:
                btn_get = item_widget.btn_buy_special
                item_widget.btn_buy_special.setVisible(True)
                item_widget.btn_buy_special.SetEnable(not has_received)
                item_widget.lab_price_special.SetString(606011 if has_received else 606010)
            count = item_widget.list_item_2.GetItemCount()
            for i in range(count):
                item = item_widget.list_item_2.GetItem(i)
                item.nd_get.setVisible(has_weeklycard)

            count = item_widget.list_item_3.GetItemCount()
            for i in range(count):
                item = item_widget.list_item_3.GetItem(i)
                item.nd_get.setVisible(has_received)

            @btn_get.unique_callback()
            def OnClick(btn, touch):
                global_data.player and global_data.player.try_get_weeklycard_daily_reward()

            @item_widget.btn_buy.unique_callback()
            def OnClick(btn, touch, _goods_info=goods_info):
                if self.is_pc_global_pay:
                    jump_to_ui_utils.jump_to_web_charge()
                elif _goods_info:
                    global_data.player and global_data.player.pay_order(_goods_info['goodsid'])

        else:
            item_widget.btn_buy_special.setVisible(True)
            item_widget.lab_limit_special.SetString(607428)
            if not goods_info:
                item_widget.btn_buy_special.SetEnable(False)
                item_widget.lab_price_special.SetString('******')
            else:
                item_widget.btn_buy_special.SetEnable(True)
                if self.is_pc_global_pay or mall_utils.is_steam_pay():
                    price_txt = mall_utils.get_pc_charge_price_str(goods_info)
                else:
                    price_txt = mall_utils.get_charge_price_str(goods_info['goodsid'])
                item_widget.lab_price_special.SetString(mall_utils.adjust_price(str(price_txt)))

            @item_widget.btn_buy_special.unique_callback()
            def OnClick(btn, touch, _goods_info=goods_info):
                if self.is_pc_global_pay:
                    jump_to_ui_utils.jump_to_web_charge()
                elif _goods_info:
                    global_data.player and global_data.player.pay_order(_goods_info['goodsid'])

        goods_lists = [
         'WEEKLY_COINS_SPEEDUP_GOODS', 'WEEKLY_MECHA_LEVELUP_GOODS']
        if self.is_pc_global_pay:
            self.refresh_btns()
            return
        for i, goods_list in enumerate(goods_lists):
            item_widget = self.panel.charge_list.GetItem(i + 1)
            goods_id = self._weekly_goods_list[i]
            has_bought = mall_utils.limite_pay(goods_id)
            if has_bought:
                item_widget.btn_buy_common.SetEnable(False)
                left_time = tutil.get_next_utc8_sunday_8(apply_ea=1)
                item_widget.lab_limit_common.SetString(get_text_by_id(607448, [tutil.get_readable_time_day_hour_minitue(left_time)]))
                item_widget.lab_price_common.SetString(12014)
            else:
                item_widget.lab_limit_common.SetString(607428)
                goods_info = global_data.lobby_mall_data.get_activity_sale_info(goods_list)
                if not goods_info:
                    item_widget.btn_buy_common.SetEnable(False)
                    item_widget.lab_price_common.SetString('******')
                else:
                    item_widget.btn_buy_common.SetEnable(True)
                    if self.is_pc_global_pay or mall_utils.is_steam_pay():
                        price_txt = mall_utils.get_pc_charge_price_str(goods_info)
                    else:
                        key = goods_info['goodsid']
                        price_txt = mall_utils.get_charge_price_str(key)
                    item_widget.lab_price_common.SetString(mall_utils.adjust_price(str(price_txt)))

                    @item_widget.btn_buy_common.unique_callback()
                    def OnClick(btn, touch, _goods_info=goods_info):
                        if self.is_pc_global_pay:
                            jump_to_ui_utils.jump_to_web_charge()
                        elif _goods_info:
                            global_data.player and global_data.player.pay_order(_goods_info['goodsid'])

            count = item_widget.list_item_1.GetItemCount()
            for j in range(count):
                item = item_widget.list_item_1.GetItem(j)
                item.nd_get.setVisible(has_bought)

        self.refresh_btns()