# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity51HelpDiscount.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils.share_utils import share_wx_mini_program, share_qq_mini_program, is_package_name_been_share_platform_verified
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
MAY_MIN_DISCOUNT = 20
MIN_CUT_MOUNT = 30
MIN_PRICE = 116
MAX_PRICE = 580
MAX_PRICE_DEDUCTION = 464

class Activity51HelpDiscount(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(Activity51HelpDiscount, self).__init__(dlg, activity_type)
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.wx_user_name = 'gh_12644ca919ad'
        self.qq_user_name = '1111400894'
        self.mini_program_path = self.get_mini_program_path()
        self.mini_program_type = '1'
        self._is_appear_share_btn = False
        self.process_event(True)

    def init_parameters(self):
        self.goods_id = None
        self._timer = 0
        self._timer_cb = {}
        self.last_deduction = 0
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

        @self.panel.progress_bar.unique_callback()
        def OnSetPercentage(pr, percent):
            baifenbi = (percent - 25.0) / 50.0
            angle = baifenbi * -180 + 90 + (1.0 - baifenbi) * -10 + 5
            self.panel.img_butterfly.setRotation(angle)

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
                from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_goods_id
                jump_to_display_detail_by_goods_id(self.goods_id, extra_parameter={'skin_list': 1})

        @self.panel.unique_callback()
        def OnClick(btn, touch):
            if self._is_appear_share_btn:
                self.set_share_btn_vis(False)

        self.register_timer()
        self._timer_cb[0] = lambda : self.refresh_time()
        self.refresh_time()

    def get_min_discount(self):
        return MAY_MIN_DISCOUNT

    def set_share_btn_vis(self, vis):
        if vis:
            self._is_appear_share_btn = True
            self.panel.StopAnimation('disappear')
            self.panel.PlayAnimation('appear')
        else:
            self._is_appear_share_btn = False
            self.panel.StopAnimation('appear')
            self.panel.PlayAnimation('disappear')

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=30, mode=CLOCK)

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

    def get_end_time(self):
        conf = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        return conf.get('share_end_time', 0)

    def refresh_time(self):
        end_time = self.get_end_time()
        if end_time:
            server_time = tutil.get_server_time()
            left_time = end_time - server_time
            if left_time > 0:
                self.panel.lab_day_last.SetString(get_text_by_id(607014).format(tutil.get_readable_time_2(left_time)))
            else:
                self.panel.lab_day_last.SetString(607926)
                return -1
        else:
            self.panel.lab_day_last.SetString(607926)
            return -1

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_festival_goods_deduction_info_event': self.refresh_discount,
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

    def get_share_url_param(self):
        player = global_data.player
        if not player:
            return ''
        role_id = player.uid
        server_id = global_data.channel._hostnum
        input_params = {'gameuid': str(role_id),
           'hostnum': str(server_id)
           }
        url_params_str = six.moves.urllib.parse.urlencode(input_params)
        return url_params_str

    def init_btns(self):

        @self.panel.btn_buy_2.unique_callback()
        def OnClick(btn, touch):
            print('Activity51HelpDiscount====================mini_program_path========', self.mini_program_path)
            self.set_share_btn_vis(not self._is_appear_share_btn)

        from logic.client.const.share_const import APP_SHARE_WEIXIN_MINI_PROGRAM, APP_SHARE_MOBILE_QQ, TYPE_MINI_PROGRAM
        from logic.gutils.share_utils import init_platform_list

        def share_cb(share_args):
            global_data.player.call_server_method('client_sa_log', ('FestivalDiscount', {'festival': 'may_festival','oper': 'share'}))
            self.set_share_btn_vis(False)
            import game3d
            platform = share_args.get('platform_enum', None)
            is_verified = is_package_name_been_share_platform_verified(platform)
            url_params_str = self.get_share_url_param()
            if global_data.is_pc_mode or game3d.get_platform() == game3d.PLATFORM_WIN32 or not is_verified:
                if platform == APP_SHARE_WEIXIN_MINI_PROGRAM:
                    url = 'https://smc.163.com/m/kanjia202104/jump/?%s&c=2' % url_params_str
                else:
                    url = 'https://smc.163.com/m/kanjia202104/jump/?%s&c=1' % url_params_str
                game3d.open_url(url)
                return
            else:
                if platform == APP_SHARE_WEIXIN_MINI_PROGRAM:
                    share_wx_mini_program(self.wx_user_name, self.mini_program_path, '0')
                else:
                    if not global_data.feature_mgr.is_support_qq_mini_program():
                        url = 'https://smc.163.com/m/kanjia202104/jump/?%s&c=1' % url_params_str
                        game3d.open_url(url)
                        global_data.game_mgr.show_tip(get_text_by_id(607957))
                        return
                    share_qq_mini_program(self.qq_user_name, self.mini_program_path, 'release')
                return

        plat_enum_list = [
         APP_SHARE_WEIXIN_MINI_PROGRAM, APP_SHARE_MOBILE_QQ]
        plat_list = global_data.share_mgr.get_support_platforms_from_enum(plat_enum_list)
        init_platform_list(self.panel.nd_share_btn, share_cb, share_type=TYPE_MINI_PROGRAM, force_plat_list=plat_list)

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
            vx_num_nd = getattr(self.panel.vx_nd_num_shine, 'img_num_%d' % index)
            num_nd.setVisible(show)
            vx_num_nd.setVisible(show)
            if show:
                path = 'gui/ui_res_2/activity/activity_202104/may/img_nun_%s.png' % price[i]
                num_nd.SetDisplayFrameByPath('', path)
                vx_num_nd.SetDisplayFrameByPath('', path)

    def buy_goods(self, cur_price):
        if not self.goods_id:
            return
        org_price_num, goods_payment = self.get_price_num()

        def _pay():
            global_data.player.buy_goods(self.goods_id, 1, goods_payment)

        if not mall_utils.check_payment(goods_payment, cur_price, cb=_pay):
            return
        _pay()

    def refresh_discount(self):
        player = global_data.player
        if not player:
            return
        deduction_info = player.get_festival_goods_deduction_info()
        goods_ids = six_ex.keys(deduction_info)
        if not goods_ids:
            return
        self.goods_id = str(goods_ids[0])
        is_owned = mall_utils.item_has_owned_by_goods_id(self.goods_id)
        self.panel.temp_price.setVisible(not is_owned)
        prices = mall_utils.get_mall_item_price(self.goods_id)
        if not prices:
            return
        original_price = prices[0]['original_price']
        deduction_price = deduction_info[goods_ids[0]]
        if self.show_end:
            if self.last_deduction != deduction_price:
                if deduction_price != MAX_PRICE_DEDUCTION:
                    self.panel.PlayAnimation('kan')
                else:
                    self.panel.PlayAnimation('kan_02')
        self.last_deduction = deduction_price
        cur_price = original_price - deduction_price
        show_price = cur_price
        min_discount = self.get_min_discount()
        lowest_price = int(math.ceil(original_price * 1.0 * min_discount / 100))
        prices[0]['original_price'] = show_price
        template_utils.splice_price(self.panel.temp_price, prices, color=mall_const.DARK_PRICE_COLOR, skew=0)
        belong_item_name = mall_utils.get_goods_belong_item_name(self.goods_id)
        item_name = mall_utils.get_goods_name(self.goods_id)
        self.panel.lab_skin.SetString(belong_item_name + '\xc2\xb7' + item_name)
        self.panel.nd_left_icon.img_prcie_bar.lab_price.SetString(str(int(math.ceil(original_price))))
        self.panel.nd_right_icon.img_prcie_bar.lab_price.SetString(str(int(math.ceil(lowest_price))))
        percent = 1.0 - float(cur_price - MIN_PRICE) / (MAX_PRICE - MIN_PRICE)
        percent = percent * 50 + 25
        progress_node = self.panel.progress_bar
        if hasattr(progress_node, 'SetPercentage') and progress_node.SetPercentage:
            progress_node.SetPercentageWithAni(percent, duration_sec=0.3)
        else:
            progress_node.SetPercent(percent, time=0.3)
        distance_to_min_price = show_price - lowest_price
        if deduction_price == 0:
            self.panel.lab_price_tips.SetString(607947)
        elif deduction_price == MAX_PRICE_DEDUCTION:
            self.panel.lab_get.setVisible(True)
            self.panel.btn_buy_1.SetFrames('', ['gui/ui_res_2/activity/activity_202104/may/btn_yellow.png', 'gui/ui_res_2/activity/activity_202104/may/btn_yellow.png', 'gui/ui_res_2/activity/activity_202104/may/btn_useless.png'])
        else:
            self.panel.lab_price_tips.SetString(get_text_by_id(607948).format(num=original_price - show_price, remain=show_price - lowest_price))
        if deduction_price == 0:
            self.panel.pnl_share_tips.setVisible(True)
            self.panel.lab_bargain_tips.setVisible(False)
        else:
            self.panel.pnl_share_tips.setVisible(False)
            self.panel.lab_bargain_tips.setVisible(True)
            if distance_to_min_price <= 150:
                need_share_time = int(math.ceil(float(distance_to_min_price) / MIN_CUT_MOUNT))
                self.panel.lab_bargain_tips.SetString(get_text_by_id(607951, (need_share_time,)))
            else:
                self.panel.lab_bargain_tips.SetString(607950)
        self.refresh_price(show_price)
        self.panel.btn_buy_1.SetTextOffset({'x': '50%36','y': '50%10'})
        self.panel.btn_buy_1.SetText(12017)
        end_time = self.get_end_time()
        server_time = tutil.get_server_time()
        end_left_time = end_time - server_time
        if deduction_price == MAX_PRICE_DEDUCTION or is_owned or end_left_time < 0:
            if deduction_price == MAX_PRICE_DEDUCTION:
                self.panel.nd_progress.setVisible(False)
                self.panel.lab_price_tips.setVisible(False)
                self.panel.lab_finish_tips.setVisible(True)
            self.panel.btn_buy_2.setVisible(False)
            self.panel.btn_buy_1.SetPosition(*self.panel.btn_buy_1_empty.GetPosition())
            if is_owned:
                self.panel.lab_price_tips.setVisible(False)
                self.panel.lab_finish_tips.setVisible(True)
                self.panel.lab_finish_tips.SetString(get_text_by_id(607956, {'name': belong_item_name + '\xc2\xb7' + item_name}))
                self.panel.btn_buy_1.SetEnable(False)
                self.panel.btn_buy_1.SetTextOffset({'x': '50%8','y': '50%10'})
                self.panel.btn_buy_1.SetText(12136)
            else:
                self.panel.btn_buy_1.SetEnable(True)

                @self.panel.btn_buy_1.unique_callback()
                def OnClick(btn, touch, price=cur_price):
                    self.buy_goods(price)

        else:
            self.panel.btn_buy_2.setVisible(True)

            @self.panel.btn_buy_1.unique_callback()
            def OnClick(btn, touch, price=cur_price):
                from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

                def callback(price=cur_price):
                    self.buy_goods(price)

                SecondConfirmDlg2().confirm(content=get_text_by_id(607958).format(num=show_price, discount=original_price - show_price), confirm_callback=callback)