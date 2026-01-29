# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/NewRoleChargeWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from common.cfg import confmgr
from logic.gutils import mall_utils
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import jump_to_ui_utils
import logic.gcommon.time_utility as tutil
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const
from cocosui import cc, ccui, ccs
from common.platform.dctool import interface

class NewRoleChargeWidget(object):

    def on_init_panel(self, panel, parent_ui_cls_name='ChargeUINew'):
        self.panel = panel
        self._timer = 0
        self._timer_cb = {}
        self.is_pc_global_pay = mall_utils.is_pc_global_pay()
        self._goods_list = [
         '20603504', '20603502', '20603503']
        self._na_names = [
         609041, 609042, 609043]
        self._ch_names = [607474, 607475, 607476]
        self._na_icons = [
         'gui/ui_res_2/charge/icon_gifts_new_1.png', 'gui/ui_res_2/charge/icon_gifts_new_2.png', 'gui/ui_res_2/charge/icon_gifts_new_3.png']
        self._ch_icons = ['gui/ui_res_2/charge/icon_gifts_beginner_1.png', 'gui/ui_res_2/charge/icon_gifts_beginner_2.png', 'gui/ui_res_2/charge/icon_gifts_beginner_3.png']
        self._na_tags = [
         607436, 12111]
        self._ch_tags = [81048, 12151]
        self._names = self._ch_names
        self._icons = self._ch_icons
        self._tags = self._ch_tags
        self._parent_ui_cls_name = parent_ui_cls_name
        self.init_event()
        self.register_timer()
        self.init_widget()
        if global_data.ui_lifetime_log_mgr:
            page_name = '{}_{}'.format(self._parent_ui_cls_name, self.__class__.__name__)
            global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time(self._parent_ui_cls_name, page_name)

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.refresh_task_reward,
           'receive_task_reward_succ_event': self.refresh_task_reward,
           'buy_good_success': self.refresh_goods_reward
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
            page_name = '{}_{}'.format(self._parent_ui_cls_name, self.__class__.__name__)
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time(self._parent_ui_cls_name, page_name)
        return

    def set_show(self, show):
        if self.panel:
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

        def callback():
            now_time = tutil.get_server_time()
            expire_ts = global_data.player.get_newbie_gift_expire_ts()
            left_time = expire_ts - now_time
            if left_time <= 0 and activity_utils.has_new_role_12_goods_reward(all_done=True):
                self.panel.lab_time.SetString(607454)
            elif left_time <= 0:
                self.panel.lab_time.SetString(606071)
            else:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time_day_hour_minitue(left_time)))

        self._timer_cb[0] = callback
        callback()
        self.panel.PlayAnimation('show')
        item_widget = self.panel.charge_list.GetItem(0)
        item_widget.nd_gift_common.setVisible(False)
        item_widget.nd_gift_special.setVisible(True)
        item_widget.lab_title_2.SetString(self._names[0])
        item_widget.img_item_special.SetDisplayFrameByPath('', self._icons[0])
        btn_tips = item_widget.btn_tips

        @btn_tips.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(607443, 607439)
            x, y = btn_tips.GetPosition()
            wpos = btn_tips.GetParent().ConvertToWorldSpace(x, y)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
            template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        self.refresh_goods_reward()
        self.show_ani()

    def show_ani(self):
        acts = []
        for i in range(3):

            def callback(index=i):
                self._show_ani(index)

            acts.append(cc.DelayTime.create(0.05 * i))
            acts.append(cc.CallFunc.create(callback))

        act = cc.Sequence.create(acts)
        self.panel.runAction(act)

    def _show_ani(self, index):
        if not self.panel or not self.panel.isValid():
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

    def refresh_goods_reward(self):
        self.refresh_task_reward()
        now_time = tutil.get_server_time()
        expire_ts = global_data.player.get_newbie_gift_expire_ts()
        left_time = expire_ts - now_time
        goods_lists = [
         'NEW_ROLE_12_GOODS', 'NEW_ROLE_30_GOODS']
        icons = [self._icons[1], self._icons[2]]
        for i, goods_list in enumerate(goods_lists):
            item_widget = self.panel.charge_list.GetItem(i + 1)
            item_widget.nd_gift_common.setVisible(True)
            item_widget.nd_gift_special.setVisible(False)
            item_widget.lab_title_1.SetString(self._names[i + 1])
            item_widget.img_item_common.SetDisplayFrameByPath('', icons[i])
            item_widget.nd_tag.setVisible(i != 0)
            if i != 0:
                item_widget.lab_tag1.SetString(self._tags[0])
                item_widget.lab_tag2.SetString(self._tags[1])
            goods_id = self._goods_list[i + 1]
            reward_id = mall_utils.get_goods_item_reward_id(goods_id)
            if i == 1:
                force_extra_ani = True if 1 else False
                template_utils.init_common_reward_list(item_widget.list_item_1, reward_id, force_extra_ani=force_extra_ani)
                has_bought = mall_utils.limite_pay(goods_id)
                item_widget.lab_limit_common.SetString(81172)
                if has_bought:
                    item_widget.btn_buy_common.SetEnable(False)
                    item_widget.lab_price_common.SetString(12014)
                else:
                    goods_info = global_data.lobby_mall_data.get_activity_sale_info(goods_list)
                    if not goods_info:
                        item_widget.btn_buy_common.SetEnable(False)
                        item_widget.lab_price_common.SetString('******')
                    elif left_time <= 0:
                        item_widget.btn_buy_common.SetEnable(False)
                        item_widget.lab_price_common.SetString(81154)
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

    def refresh_task_reward(self, *args):
        item_widget = self.panel.charge_list.GetItem(0)
        goods_id = self._goods_list[0]
        task_id = mall_utils.get_goods_item_task_id(goods_id)
        children_tasks = task_utils.get_children_task(task_id)
        total_prog = task_utils.get_total_prog(task_id)
        cur_prog = global_data.player.get_task_prog(task_id)
        has_bought = mall_utils.limite_pay(goods_id)
        can_receive_task = []
        for i, sub_task_id in enumerate(children_tasks):
            nd_day = getattr(item_widget, 'nd_day_{}'.format(i + 1))
            if not has_bought:
                nd_day.img_choose.setVisible(False)
            else:
                nd_day.img_choose.setVisible(i == cur_prog - 1)
            reward_id = task_utils.get_task_reward(sub_task_id)
            template_utils.init_common_reward_list(nd_day.list_item, reward_id)
            has_rewarded = global_data.player.has_receive_reward(sub_task_id)
            if not has_rewarded:
                can_receive_task.append(sub_task_id)
            count = nd_day.list_item.GetItemCount()
            for j in range(count):
                _item_widget = nd_day.list_item.GetItem(j)
                if i == 0 and j == 0:
                    _item_widget.nd_get.setVisible(has_bought)
                else:
                    _item_widget.nd_get.setVisible(has_rewarded)

        if not has_bought:
            item_widget.lab_limit_special.SetString(81172)
            goods_info = global_data.lobby_mall_data.get_activity_sale_info('NEW_ROLE_6_GOODS')
            if not goods_info:
                item_widget.btn_buy_special.SetEnable(False)
                item_widget.lab_price_special.SetString('******')
            else:
                item_widget.btn_buy_special.SetEnable(True)
                if self.is_pc_global_pay or mall_utils.is_steam_pay():
                    price_txt = mall_utils.get_pc_charge_price_str(goods_info)
                else:
                    key = goods_info['goodsid']
                    price_txt = mall_utils.get_charge_price_str(key)
                item_widget.lab_price_special.SetString(mall_utils.adjust_price(str(price_txt)))

                @item_widget.btn_buy_special.unique_callback()
                def OnClick(btn, touch, _goods_info=goods_info):
                    if self.is_pc_global_pay:
                        jump_to_ui_utils.jump_to_web_charge()
                    elif _goods_info:
                        global_data.player and global_data.player.pay_order(_goods_info['goodsid'])

        else:
            can_receive_count = len(can_receive_task)
            item_widget.lab_limit_special.SetString(get_text_by_id(607411).format(get_text_by_id(556685).format(can_receive_count)))
            if can_receive_task and can_receive_count > total_prog - cur_prog:
                item_widget.btn_buy_special.SetEnable(True)
                item_widget.lab_price_special.SetString(80930)
            else:
                item_widget.btn_buy_special.SetEnable(False)
                item_widget.lab_price_special.SetString(606011)

            @item_widget.btn_buy_special.unique_callback()
            def OnClick(btn, touch):
                for sub_task_id in can_receive_task:
                    global_data.player.receive_task_reward(sub_task_id)

        self.refresh_btns()