# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202203/ActivityJointLightningBP.py
from __future__ import absolute_import
import six
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils, mall_utils, jump_to_ui_utils, activity_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc
from logic.gcommon import time_utility as tutil
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN

class ActivityJointLightningBP(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityJointLightningBP, self).__init__(dlg, activity_type)
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.children_task_list = task_utils.get_children_task(self.task_id)
        self._timer = 0
        self._timer_cb = {}
        self.goods_id = '20617404'
        self.goods_info = None
        self.is_pc_global_pay = mall_utils.is_pc_global_pay()
        if global_data.lobby_mall_data and global_data.player:
            self.goods_info = global_data.lobby_mall_data.get_activity_sale_info('SUMMER_DISCOUNT_CHARGE_GOODS')
            if self.goods_info:
                key = self.goods_info['goodsid']
                goods_id = global_data.player.get_goods_info(key).get('cShopGoodsId')
                if goods_id:
                    self.goods_id = goods_id
        return

    def on_init_panel(self):
        if not self.is_unlock_rebate():
            self.register_timer()
        self.init_time_widget()
        self.init_btn_get()
        self.init_btn_goto()
        self.init_anim()
        self.init_btn_vx()
        self.process_event(True)
        self.update_widget()

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.update_widget,
           'task_prog_changed': self.update_widget,
           'buy_good_success': self.update_widget
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

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

    def refresh_time(self):
        lab_time = self.panel.nd_content.bar_time.lan_countdown
        left_time = activity_utils.get_left_time(self._activity_type)
        if left_time > 0:
            if left_time > tutil.ONE_HOUR_SECONS:
                lab_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time_day_hour_minitue(left_time)))
            else:
                lab_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time(left_time)))
        else:
            close_left_time = 0
            lab_time.SetString(tutil.get_readable_time(close_left_time))
        if left_time < tutil.ONE_DAY_SECONDS:
            lab_time.SetColor(16776557)
        else:
            lab_time.SetColor(16777215)

    def init_anim(self):
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

        @self.panel.nd_content.character_red.nd_touch.unique_callback()
        def OnClick(btn, touch):
            self.on_click_anim()

    def init_time_widget(self):
        player = global_data.player
        if not player:
            return
        if self.is_unlock_rebate():
            self.unregister_timer()
            lab_time = self.panel.nd_content.bar_time.lan_countdown
            left_count = 0
            for task_id in self.children_task_list:
                reward_status = player.get_task_reward_status(task_id)
                if reward_status != ITEM_RECEIVED:
                    left_count += 1

            lab_time.SetString(get_text_by_id(609712).format(left_count))
        else:
            self._timer_cb[0] = lambda : self.refresh_time()
            self.refresh_time()

    def init_btn_get(self):
        self.panel.nd_content.lab_price.setVisible(not self.is_unlock_rebate())
        if self.is_unlock_rebate():
            self.init_btn_rebate()
        else:
            self.init_btn_buy()

        @self.panel.nd_content.btn_buy.unique_callback()
        def OnClick(btn, touch):
            if self.is_unlock_rebate():
                self.on_click_btn_rebate()
            else:
                self.on_click_btn_buy()

    def init_btn_buy(self):
        btn_buy = self.panel.nd_content.btn_buy
        if not self.goods_info:
            btn_buy.SetEnable(False)
            btn_buy.SetText('******')
            return
        if self.is_pc_global_pay or mall_utils.is_steam_pay():
            price_txt = mall_utils.get_pc_charge_price_str(self.goods_info)
        else:
            price_txt = mall_utils.get_charge_price_str(self.goods_info['goodsid'])
        btn_buy.SetEnable(True)
        btn_buy.SetText(mall_utils.adjust_price(str(price_txt)))

    def init_btn_rebate(self):
        btn_rebate = self.panel.nd_content.btn_buy
        can_receive = global_data.player.has_unreceived_task_reward(self.task_id)
        btn_rebate.SetEnable(can_receive)
        if can_receive:
            btn_rebate.SetText(604030)
        else:
            btn_rebate.SetText(604029)

    def init_btn_goto(self):
        self.panel.nd_content.lab_name.SetString(mall_utils.get_goods_name(self.goods_id))

        @self.panel.nd_content.btn_search.unique_callback()
        def OnClick(btn, touch):
            self.on_click_btn_goto()

    def init_btn_vx(self):
        can_receive = global_data.player.has_unreceived_task_reward(self.task_id)
        can_buy = not self.is_unlock_rebate() and self.goods_info
        if can_receive or can_buy:
            self.panel.PlayAnimation('loop_btn_buy')
            self.panel.vx_hx_lighteffect.sweeplight.setVisible(True)
            self.panel.nd_content.btn_buy.vx_btn_buy_sweep1.setVisible(True)
        else:
            self.panel.StopAnimation('loop_btn_buy')
            self.panel.vx_hx_lighteffect.sweeplight.setVisible(False)
            self.panel.nd_content.btn_buy.vx_btn_buy_sweep1.setVisible(False)

    def on_click_btn_buy(self, *args):
        if self.is_pc_global_pay:
            jump_to_ui_utils.jump_to_web_charge()
        elif self.goods_info:
            global_data.player and global_data.player.pay_order(self.goods_info['goodsid'])

    def on_click_btn_rebate(self, *args):
        player = global_data.player
        if not player:
            return
        player.receive_all_task_reward(self.task_id)
        self.panel.nd_content.btn_buy.SetEnable(False)
        self.panel.nd_content.btn_buy.SetText(604029)

    def on_click_btn_goto(self, *args):
        jump_to_ui_utils.jump_to_display_detail_by_goods_id(self.goods_id, {'role_info_ui': True})

    def on_click_anim(self, *args):
        pass

    def is_unlock_rebate(self):
        player = global_data.player
        if not player:
            return False
        bought_num = player.buy_num_all_dict.get(self.goods_id, 0)
        return bought_num > 0

    def update_widget(self, *args):
        is_unlock = self.is_unlock_rebate()
        if is_unlock:
            self.panel.nd_content.txt_discount.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202203/joint_lightning/txt_joint_lightning_sale48.png')
        else:
            self.panel.nd_content.txt_discount.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202203/joint_lightning/txt_joint_lightning_sale.png')
        self.init_time_widget()
        self.init_btn_get()
        self.init_btn_vx()