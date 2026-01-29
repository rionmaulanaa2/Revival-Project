# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewSkin.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.template_utils import init_price_view
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gutils.item_utils import get_lobby_item_name
from logic.gutils import jump_to_ui_utils
from logic.gcommon import time_utility as tutil
from logic.gutils.mall_utils import is_valid_goods
money_icon_scale = 0.8

class ActivityNewSkin(ActivityBase):

    def on_init_panel(self):
        self._item_id = [
         201801034, 201800132]
        self.set_item_content(201801034, self.panel.lab_mech_name_1, self.panel.temp_price_1, self.panel.img_mech_name_1.btn_look)
        self.set_item_content(201800132, self.panel.lab_mech_name_2, self.panel.temp_price_2, self.panel.img_mech_name_2.btn_look)
        self.set_item_content(208105611, self.panel.lab_weapon)
        self.set_package_content()
        self.play_animation()
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_lobby_bag_item_changed_event': self.set_package_content
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def set_item_content(self, item_id, nd_lab, nd_price=None, nd_jump=None):
        goods_id = str(item_id)
        nd_lab.SetString(get_lobby_item_name(item_id))
        if nd_price:
            init_price_view(nd_price, goods_id, DARK_PRICE_COLOR, money_icon_scale=money_icon_scale)
        if nd_jump:

            @nd_jump.callback()
            def OnClick(btn, touch, item_id=item_id):
                jump_to_ui_utils.jump_to_display_detail_by_item_no(item_id, {'skin_list': 1})

    def set_package_content(self):
        goods_id = str(50600070)
        init_price_view(self.panel.temp_price, goods_id, DARK_PRICE_COLOR, money_icon_scale=money_icon_scale)
        self.panel.lab_discount_num.SetString('40%')
        if not is_valid_goods(goods_id):
            self.panel.btn_buy.SetEnable(False)
            self.panel.img_buy.SetDisplayFrameByPath('', 'gui/ui_res_2/common/button/btn_special_useless.png')
        else:
            self.panel.btn_buy.SetEnable(True)
            self.panel.img_buy.SetDisplayFrameByPath('', 'gui/ui_res_2/common/button/btn_special_major.png')

            @self.panel.btn_buy.callback()
            def OnClick(btn, touch, goods_id=goods_id):
                from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                groceries_buy_confirmUI(goods_id)

        conf = confmgr.get('c_activity_config', self._activity_type)
        now = int(tutil.time())
        end_time = conf.get('cEndTime', now)
        left_day = max(end_time - now, 0) / tutil.ONE_DAY_SECONDS
        s = get_text_by_id(82116).format(left_day) if left_day > 0 else get_text_by_id(81398)
        self.panel.lab_discount_days.SetString(s)

    def play_animation(self):
        self.panel.PlayAnimation('show')
        delay = self.panel.GetAnimationMaxRunTime('show')
        self.panel.DelayCall(delay, lambda *args: self.panel.PlayAnimation('loop1') and 0)
        self.panel.DelayCall(delay, lambda *args: self.panel.PlayAnimation('loop2') and 0)