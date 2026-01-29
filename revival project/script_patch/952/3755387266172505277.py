# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityHelpDiscount.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils.share_utils import share_wx_mini_program
from logic.gcommon import time_utility as tutil
from logic.client.const import mall_const
from logic.gutils import mall_utils
from logic.gutils import template_utils
import logic.gcommon.const as gconst
from logic.gutils import task_utils
from logic.gutils import activity_utils
from common.platform.dctool import interface
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error
import math
SIGN_KEY = '3d95d926-ba78-42d1-b3a9-a5cdbd6c0e06'
DISCOUNT_BG = ['gui/ui_res_2/activity/activity_202101/activity_bargain/bar_price_overbargain.png',
 'gui/ui_res_2/activity/activity_202101/activity_bargain/bar_price_uncurrent.png',
 'gui/ui_res_2/activity/activity_202101/activity_bargain/bar_price_current.png']
NUM_COLOR = [13684944, 1248270, 1248270]

class ActivityHelpDiscount(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityHelpDiscount, self).__init__(dlg, activity_type)
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.user_name = 'gh_008877576790'
        self.mini_program_path = self.get_mini_program_path()
        self.mini_program_type = '0'
        self.process_event(True)

    def init_parameters(self):
        self.goods_id = None
        self._timer = 0
        self._timer_cb = {}
        self.last_discount = 0
        return

    def on_init_panel(self):
        self.panel.PlayAnimation('show')
        self.show_end = False
        animation_time = self.panel.GetAnimationMaxRunTime('show')

        def finished_show():
            self.show_end = True
            self.panel.PlayAnimation('loop')

        self.panel.SetTimeOut(animation_time, finished_show)
        progress_node = self.panel.progress_bar
        if hasattr(progress_node, 'SetPercentage') and progress_node.SetPercentage:
            progress_node.SetPercentage(0)
        else:
            progress_node.SetPercent(0)
        self.init_parameters()
        self.refresh_discount()
        self.init_btns()

        @self.panel.btn_help.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

        @self.panel.btn_detail.unique_callback()
        def OnClick(btn, touch, *args):
            if self.goods_id:
                mall_utils.mall_switch_detail(self.goods_id)

        self.register_timer()
        self._timer_cb[0] = lambda : self.refresh_time()
        self.refresh_time()

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
        del_keys = []
        for key, cb in six.iteritems(self._timer_cb):
            result = cb()
            if result == -1:
                del_keys.append(key)

        for key in del_keys:
            del self._timer_cb[key]

    def get_left_time(self):
        player = global_data.player
        if not player:
            return (-1, -1)
        return player.get_help_discount_left_time()

    def refresh_time(self):
        start_left_time, end_left_time = self.get_left_time()
        if end_left_time > 0:
            self.panel.lab_day_last.SetString(get_text_by_id(607014).format(tutil.get_simply_time(end_left_time)))
        else:
            self.panel.lab_day_last.SetString(607926)
            self.refresh_discount()
            return -1

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_spring_discount_info_event': self.refresh_discount,
           'player_item_update_event': self.refresh_discount
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def get_mini_program_path(self):
        player = global_data.player
        if not player:
            return ''
        role_id = player.uid
        server_id = global_data.channel._hostnum
        input_params = {'gameuid': str(role_id),
           'hostnum': str(server_id)
           }
        url_params_str = six.moves.urllib.parse.urlencode(input_params)
        return 'pages/login/login?%s' % url_params_str

    def init_btns(self):

        @self.panel.btn_buy_2.unique_callback()
        def OnClick(btn, touch):
            if global_data.is_pc_mode:
                global_data.game_mgr.show_tip(get_text_by_id(607929))
            else:
                print('ActivityHelpDiscount====================mini_program_path========', self.mini_program_path)
                share_wx_mini_program(self.user_name, self.mini_program_path, self.mini_program_type)
                global_data.player.call_server_method('client_sa_log', ('SpringDiscount', {'oper': 'share'}))

    def get_price_num(self):
        if not self.goods_id:
            return (-1, gconst.SHOP_ITEM_YUANBAO)
        price_info = mall_utils.get_mall_item_price(self.goods_id)
        if not price_info:
            return (-1, gconst.SHOP_ITEM_YUANBAO)
        return (price_info[0].get('original_price', -1), price_info[0].get('goods_payment', gconst.SHOP_ITEM_YUANBAO))

    def refresh_price(self, show_price):
        if show_price < 0:
            return
        price = str(show_price)
        for i in range(3):
            show = i < len(price)
            index = i + 1
            num_nd = getattr(self.panel.nd_num, 'img_num_%d' % index)
            num_nd_cj = getattr(num_nd, 'vx_num_%d_cj' % index)
            vx_num_nd = getattr(self.panel.vx_nd_num_shine, 'img_num_%d' % index)
            num_nd.setVisible(show)
            num_nd_cj.setVisible(show)
            vx_num_nd.setVisible(show)
            if show:
                path = 'gui/ui_res_2/activity/activity_202101/activity_bargain/tet_springbargaining_%s.png' % price[i]
                num_nd.SetDisplayFrameByPath('', path)
                num_nd_cj.SetMaskFrameByPath('', path)
                vx_num_nd.SetDisplayFrameByPath('', path)

    def buy_goods(self, discount):
        if not self.goods_id:
            return
        price_num, goods_payment = self.get_price_num()
        price = math.ceil(price_num * 1.0 * discount / 100)

        def _pay():
            global_data.player.buy_goods(self.goods_id, 1, goods_payment)

        if not mall_utils.check_payment(goods_payment, price, cb=_pay):
            return
        _pay()

    def refresh_discount(self):
        player = global_data.player
        if not player:
            return
        else:
            spring_discount_info = player.get_spring_discount_info()
            goods_ids = six_ex.keys(spring_discount_info)
            if not goods_ids:
                return
            self.goods_id = str(goods_ids[0])
            is_owned = mall_utils.item_has_owned_by_goods_id(self.goods_id)
            self.panel.temp_price.setVisible(not is_owned)
            discount = spring_discount_info[goods_ids[0]]
            if self.show_end:
                if self.last_discount != discount:
                    self.panel.PlayAnimation('kan')
            self.last_discount = discount
            prices = mall_utils.get_mall_item_price(self.goods_id)
            if not prices:
                return
            original_price = prices[0]['original_price']
            show_price = int(math.ceil(original_price * 1.0 * discount / 100))
            prices[0]['original_price'] = show_price
            template_utils.splice_price(self.panel.temp_price, prices, color=mall_const.DARK_PRICE_COLOR, skew=0)
            cur_nd = None
            for i in range(9):
                nd = getattr(self.panel, 'temp_node_%d' % (i + 1))
                each_discount = 10 - i
                if i == 0:
                    nd.lab_node_num.SetString(607924)
                else:
                    nd.lab_node_num.SetString(get_text_by_id(608311).format(str(each_discount)))
                if each_discount * 10 == discount:
                    state = 2
                elif each_discount * 10 < discount:
                    state = 1
                else:
                    state = 0
                nd.img_node.SetDisplayFrameByPath('', DISCOUNT_BG[state])
                nd.lab_node_num.SetColor(NUM_COLOR[state])
                if state == 2:
                    nd.img_node.setRotation(90 - 20 * i)
                    nd.vx_particular.setVisible(True)
                    cur_nd = nd
                else:
                    nd.img_node.setRotation(0)
                    nd.vx_particular.setVisible(False)

            def _show_node_ani(cur_nd=cur_nd):
                if cur_nd:
                    cur_nd.PlayAnimation('appear')

            percent = 25 + 50 * (100 - discount) * 1.0 / 80
            progress_node = self.panel.progress_bar
            if hasattr(progress_node, 'SetPercentage') and progress_node.SetPercentage:
                progress_node.SetPercentageWithAni(percent, duration_sec=0.3, end_cb=_show_node_ani)
            else:
                progress_node.SetPercent(percent, time=0.3, end_cb=_show_node_ani)
            if discount == 100:
                self.panel.lab_price_tips.SetString(607913)
            elif discount == 20:
                self.panel.lab_price_tips.SetString(607915)
            else:
                self.panel.lab_price_tips.SetString(get_text_by_id(607914).format(num=original_price - show_price, count=(discount - 20) / 10))
            self.refresh_price(show_price)
            self.panel.btn_buy_1.SetTextOffset({'x': '50%32','y': '50%'})
            self.panel.btn_buy_1.SetText(12017)
            start_left_time, end_left_time = self.get_left_time()
            if discount == 20 or is_owned or end_left_time < 0:
                self.panel.btn_buy_1.img_btn_light.setVisible(False)
                self.panel.btn_buy_2.setVisible(False)
                self.panel.btn_buy_1.SetPosition(*self.panel.btn_buy_1_empty.GetPosition())
                if is_owned:
                    self.panel.btn_buy_1.SetEnable(False)
                    self.panel.btn_buy_1.SetTextOffset({'x': '50%','y': '50%'})
                    self.panel.btn_buy_1.SetText(12136)
                else:
                    self.panel.btn_buy_1.SetEnable(True)

                    @self.panel.btn_buy_1.unique_callback()
                    def OnClick(btn, touch, discount=discount):
                        self.buy_goods(discount)

            else:
                self.panel.btn_buy_1.img_btn_light.setVisible(True)
                self.panel.btn_buy_2.setVisible(True)
                self.panel.btn_buy_1.SetPosition('50%113', '50%-314')

                @self.panel.btn_buy_1.unique_callback()
                def OnClick(btn, touch, discount=discount):
                    from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

                    def callback(discount=discount):
                        self.buy_goods(discount)

                    SecondConfirmDlg2().confirm(content=get_text_by_id(607925).format(num=show_price, discount=original_price - show_price), confirm_callback=callback)

            return