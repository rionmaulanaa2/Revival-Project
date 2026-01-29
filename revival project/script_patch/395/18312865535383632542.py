# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySpringSuperSale.py
from __future__ import absolute_import
from logic.gutils import mall_utils
from logic.gutils.activity_utils import get_left_time
from logic.gcommon.time_utility import get_day_hour_minute_second
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.activity.widget import widget
from logic.comsys.activity.ActivityTemplate import ActivityBase
ORIGIN_PRICE = 60

@widget('DescribeWidget')
class ActivitySpringSuperSale(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivitySpringSuperSale, self).__init__(dlg, activity_type)
        ui_data = confmgr.get('c_activity_config', self._activity_type, default={}).get('cUiData', {})
        self._game_goods_id = ui_data.get('goods_id_list')[0]
        self._jelly_goods_name = ui_data.get('jelly_goods_name')
        self._init_parameters()
        self._init_event()

    def _init_parameters(self):
        self._jelly_goods_info = global_data.lobby_mall_data.get_activity_sale_info(self._jelly_goods_name)

    def on_init_panel(self):
        left_time = get_left_time(self._activity_type)
        day, _, _, _ = get_day_hour_minute_second(left_time)
        self.panel.lab_time_tip.SetString(get_text_by_id(601186).format(day))
        self._init_title()
        self._init_goods_show()
        self._update_goods_show()

    def _init_goods_show(self):

        @self.panel.btn_buy.unique_callback()
        def OnClick(btn, touch):
            if mall_utils.is_pc_global_pay():
                from logic.gutils.jump_to_ui_utils import jump_to_web_charge
                jump_to_web_charge()
            elif self._jelly_goods_info:
                global_data.player and global_data.player.pay_order(self._jelly_goods_info['goodsid'])

        @self.panel.btn_search.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
            jump_to_display_detail_by_item_no(mall_utils.get_goods_item_no(self._game_goods_id), {'skin_list': 1})

    def _update_goods_show(self):
        has_limited = mall_utils.limite_pay(self._game_goods_id)
        if has_limited or not self._jelly_goods_info:
            self.panel.btn_buy.SetEnable(False)
            self.panel.lab_buy.setVisible(False)
            self.panel.btn_buy.SetText(12014)
            self.panel.btn_buy.temp_price.setVisible(False)
        else:
            self.panel.btn_buy.SetEnable(True)
            self.panel.lab_buy.setVisible(True)
            self.panel.btn_buy.SetText('')
            self.panel.btn_buy.temp_price.setVisible(True)
        if self._jelly_goods_info:
            if mall_utils.is_pc_global_pay() or mall_utils.is_steam_pay():
                price_txt = mall_utils.get_pc_charge_price_str(self._jelly_goods_info)
                price_val = self._jelly_goods_info.get('price')
            else:
                price_txt = mall_utils.get_charge_price_str(self._jelly_goods_info['goodsid'])
                price_val = mall_utils.get_charge_price_val(self._jelly_goods_info['goodsid'])
            adjusted_price = mall_utils.adjust_price(str(price_txt))
            origin_price_val = ''
            try:
                price_val_str = str(price_val)
                price_val_str = price_val_str.replace(',', '')
                start_index = 0
                for i, ch in enumerate(price_val_str):
                    start_index = i
                    if ch.isdigit():
                        break

                price_val_str = price_val_str[start_index:]
                origin_price_val = int(eval(str(price_val_str)) / 0.1)
            except:
                origin_price_val = ''
                log_error('ActivitySpringSuperSale - calculate origin price val fail - price_val:', price_val)

            self.panel.btn_buy.temp_price.img_price.setVisible(False)
            self.panel.btn_buy.temp_price.lab_price.SetString(adjusted_price)
            self.panel.btn_buy.temp_price.lab_price_before.SetString(str(origin_price_val))
        else:
            self.panel.btn_buy.temp_price.img_price.setVisible(False)
            self.panel.btn_buy.temp_price.lab_price.SetString('')
            self.panel.btn_buy.temp_price.lab_price_before.SetString('')

    def refresh_panel(self):
        pass

    def set_show(self, show, is_init=False):
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        self.panel.PlayAnimation('right')
        super(ActivitySpringSuperSale, self).set_show(show, is_init)

    def _init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        event_mgr = global_data.emgr
        e_event = {'update_charge_info': self._update_goods_show,
           'buy_good_success': self._update_goods_show
           }
        if is_bind:
            event_mgr.bind_events(e_event)
        else:
            event_mgr.unbind_events(e_event)

    def _init_title(self):
        from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN
        language = get_cur_text_lang()
        self.panel.img_title.setVisible(language == LANG_CN)
        self.panel.lab_title_en.setVisible(language != LANG_CN)

    def on_finalize_panel(self):
        self.process_event(False)