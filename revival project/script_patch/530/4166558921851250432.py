# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/red_packet/RedPacketSendSettingUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils.red_packet_utils import init_red_packet_cover_item, get_red_packet_info, get_red_packet_bless_list, get_red_packet_bless_info, get_open_packet_cover_list, init_small_red_packet_cover_item, get_user_setting_red_packet_cover, set_user_setting_red_packet_cover, CUR_ID_TO_PAYMENT_ID
from logic.gcommon.common_const.red_packet_const import RED_PACKET_DAY_CREATE_MAX_COUNT
from common.const.uiconst import UI_VKB_CLOSE
from logic.gutils.template_utils import init_price_template
from logic.gutils.mall_utils import get_mall_item_price, get_lobby_item_name
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gutils.mall_utils import check_payment
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
from logic.gcommon.common_const import chat_const
MIN_EXTRA_COST = 1
HANDING_FEE = 0.01
NUM_SCROLL_LIST_MAX_COUNT = 2

class RedPacketSendSettingUI(BasePanel):
    PANEL_CONFIG_NAME = 'chat/red_packet/open_red_packet_send'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn'
       }
    GLOBAL_EVENT = {'change_red_packet_cover_succeed': 'refresh_choose_red_packet_cover',
       'buy_good_success': 'refresh_owner_red_packet_cover_list'
       }
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, red_packet_type, channel, **kwargs):
        self.regist_main_ui()
        self.channel = channel
        self.send_red_packet_type = red_packet_type
        self.select_money_num = 0
        self.select_packet_num = 0
        self.select_bless_id = 1
        self.real_money_num = 0
        self.real_price_info = {}
        self.bless_idx_list = []
        self.packet_item_info = get_red_packet_info(self.send_red_packet_type)
        self.choose_cover_item = None
        self.choose_cover_item_no = get_user_setting_red_packet_cover()
        self.init_left_red_packet_cover()
        self.init_send_red_packet_info()
        self.init_sub_red_packet_cover()
        self.init_price_widget()
        return

    def init_left_red_packet_cover(self):
        init_red_packet_cover_item(self.panel.temp_item, self.choose_cover_item_no, True)

    def init_send_red_packet_info(self):
        if not self.packet_item_info:
            return
        self.bless_idx_list = get_red_packet_bless_list()
        self.money_list = self.packet_item_info.get('money_list')
        self.num_list = self.packet_item_info.get('num_list')
        if self.channel == 2:
            self.num_list = [
             10]
        self.panel.nd_wish.lab_wish.SetString(int(self.bless_idx_list[0]))
        bless_list = self.panel.nd_wish.choose_list
        bless_list.nd_close.BindMethod('OnClick', lambda btn, touch: self.on_click_change_choose_list(self.panel.nd_wish.btn_list.icon_arrow, bless_list))
        bless_list.option_list.BindMethod('OnCreateItem', lambda lv, idx, item: self.on_create_list_item(self.bless_idx_list[idx], item, click_cb=self.refresh_bless_text))
        bless_list.option_list.SetInitCount(len(self.bless_idx_list))
        bless_list.option_list.scroll_Load()
        self.panel.nd_wish.btn_list.BindMethod('OnClick', lambda btn, touch: self.on_click_change_choose_list(self.panel.nd_wish.btn_list.icon_arrow, bless_list))
        self.panel.nd_total.lab_number.SetString(str(self.money_list[0]))
        money_item_list = self.panel.nd_total.choose_list
        money_item_list.nd_close.BindMethod('OnClick', lambda btn, touch: self.on_click_change_choose_list(self.panel.nd_total.btn_list.icon_arrow, money_item_list))
        money_item_list.option_list.BindMethod('OnCreateItem', lambda lv, idx, item: self.on_create_list_item(str(self.money_list[idx]), item, click_cb=self.refresh_cost_money))
        money_item_list.option_list.SetInitCount(len(self.money_list))
        money_item_list.option_list.scroll_Load()
        self.panel.nd_total.btn_list.BindMethod('OnClick', lambda btn, touch: self.on_click_change_choose_list(self.panel.nd_total.btn_list.icon_arrow, money_item_list))
        self.panel.nd_number.lab_number.SetString(str(self.num_list[0]))
        num_item_list = self.panel.nd_number.choose_list
        choose_list_size = len(self.num_list) if len(self.num_list) <= NUM_SCROLL_LIST_MAX_COUNT else NUM_SCROLL_LIST_MAX_COUNT
        num_item_list.SetContentSize(434, 4 + 55 * choose_list_size)
        num_item_list.nd_close.BindMethod('OnClick', lambda btn, touch: self.on_click_change_choose_list(self.panel.nd_number.btn_list.icon_arrow, num_item_list))
        num_item_list.option_list.BindMethod('OnCreateItem', lambda lv, idx, item: self.on_create_list_item(str(self.num_list[idx]), item, click_cb=self.refresh_red_packet_num))
        num_item_list.option_list.SetInitCount(len(self.num_list))
        num_item_list.option_list.scroll_Load()
        self.refresh_choose_list_size(num_item_list)
        self.panel.nd_number.btn_list.BindMethod('OnClick', lambda btn, touch: self.on_click_change_choose_list(self.panel.nd_number.btn_list.icon_arrow, num_item_list))
        self.refresh_cost_money(str(self.money_list[0]), is_init=True)
        self.refresh_red_packet_num(str(self.money_list[0]), is_init=True)
        lab_remain = 0
        max_count = RED_PACKET_DAY_CREATE_MAX_COUNT
        if global_data.player:
            max_count = global_data.player.get_red_packet_day_create_limit_count()
            lab_remain = max_count - global_data.player.get_red_packet_day_create_count()
        self.panel.lab_remain.SetString('<color=01C7DFFF>{}</color>/<color=363B51FF>{}</color>'.format(lab_remain, max_count))
        self.panel.btn_send.BindMethod('OnClick', lambda btn, touch: self.on_click_send())
        self.panel.lab_cost.SetString(get_text_by_id(634409).format(get_lobby_item_name(self.packet_item_info.get('cur_id', 50101001))))

    def init_price_widget--- This code section failed: ---

 115       0  LOAD_GLOBAL           0  'PriceUIWidget'
           3  LOAD_GLOBAL           1  'panel'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  'panel'
          12  LOAD_ATTR             2  'list_money'
          15  CALL_FUNCTION_257   257 
          18  LOAD_FAST             0  'self'
          21  STORE_ATTR            3  'price_top_widget'

 116      24  LOAD_FAST             0  'self'
          27  LOAD_ATTR             3  'price_top_widget'
          30  LOAD_ATTR             4  'show_money_types'
          33  LOAD_GLOBAL           5  'CUR_ID_TO_PAYMENT_ID'
          36  LOAD_ATTR             6  'get'
          39  LOAD_FAST             0  'self'
          42  LOAD_ATTR             7  'packet_item_info'
          45  LOAD_ATTR             6  'get'
          48  LOAD_CONST            2  'cur_id'
          51  LOAD_CONST            3  50101001
          54  CALL_FUNCTION_2       2 
          57  LOAD_GLOBAL           8  'SHOP_PAYMENT_YUANBAO'
          60  CALL_FUNCTION_2       2 
          63  BUILD_LIST_1          1 
          66  CALL_FUNCTION_1       1 
          69  POP_TOP          

Parse error at or near `CALL_FUNCTION_257' instruction at offset 15

    def init_sub_red_packet_cover(self):
        self.open_red_packet_cover_list = get_open_packet_cover_list()
        self.owner_red_packet_cover_list = []
        self.refresh_owner_red_packet_cover_list()
        self.panel.temp_btn_more.btn_common_big.BindMethod('OnClick', lambda btn, touch: self.on_click_show_more())

    def on_create_list_item(self, text, item, click_cb=None):
        item.button.SetText(text)

        @item.button.unique_callback()
        def OnClick(btn, touch):
            if click_cb:
                click_cb(text)

    def refresh_choose_red_packet_cover(self, item_no):
        if not self.panel:
            return
        self.choose_cover_item_no = item_no
        self.refresh_left_red_packet_cover(item_no)
        self.refresh_owner_red_packet_cover_list(True)

    def refresh_owner_red_packet_cover_list(self, force=False):
        if not self.panel:
            return
        old_num = len(self.owner_red_packet_cover_list)
        for i in range(len(self.open_red_packet_cover_list)):
            item_no = self.open_red_packet_cover_list[i]
            if item_no in self.owner_red_packet_cover_list:
                continue
            if global_data.player and global_data.player.has_item_by_no(int(item_no)):
                self.owner_red_packet_cover_list.append(item_no)

        new_num = len(self.owner_red_packet_cover_list)
        if old_num != new_num or force == True:
            self.panel.list_item.SetInitCount(new_num)
            for i in range(new_num):
                item = self.panel.list_item.GetItem(i)
                init_small_red_packet_cover_item(item, self.owner_red_packet_cover_list[i])
                if self.owner_red_packet_cover_list[i] == str(self.choose_cover_item_no):
                    self.choose_cover_item = item
                    self.choose_cover_item.btn_choose.SetSelect(True)
                else:
                    item.btn_choose.SetSelect(False)
                item.btn_choose.BindMethod('OnClick', lambda btn, touch, item=item, idx=i: self.on_click_choose_red_packet(idx, item))

    def refresh_left_red_packet_cover(self, item_num):
        init_red_packet_cover_item(self.panel.temp_item, item_num, True)

    def refresh_choose_list_size(self, widget, max_height=None):
        old_size = widget.bar.getContentSize()
        old_list_size = widget.option_list.getContentSize()
        extra_height = old_size.height - old_list_size.height
        width, _ = widget.option_list.GetContentSize()
        _, height = widget.option_list.GetContainer().GetContentSize()
        if max_height:
            height = min(height, max_height)
        widget.option_list.SetContentSize(width, height)
        widget.bar.SetContentSize(old_size.width, height + extra_height)
        widget.SetContentSize(widget.GetContentSize()[0], height)
        widget.option_list.ReConfPosition()
        widget.bar.ReConfPosition()

    def refresh_bless_text(self, text_id):
        self.panel.temp_item.lab_wish.SetString(text_id)
        self.panel.nd_wish.lab_wish.SetString(text_id)
        self.select_bless_id = self.bless_idx_list.index(text_id) + 1
        self.on_click_change_choose_list(self.panel.nd_wish.btn_list.icon_arrow, self.panel.nd_wish.choose_list)

    def refresh_red_packet_num(self, num, is_init=False):
        self.select_packet_num = num
        self.panel.nd_number.lab_number.SetString(num)
        if not is_init:
            self.on_click_change_choose_list(self.panel.nd_number.btn_list.icon_arrow, self.panel.nd_number.choose_list)

    def refresh_cost_money(self, money_num, is_init=False):
        self.select_money_num = money_num
        self.panel.nd_total.lab_number.SetString(money_num)
        goods_count = int(int(money_num) / 10)
        price_info = get_mall_item_price(str(self.packet_item_info.get('goods_id', 700500011)), goods_count)
        if not price_info:
            return
        price_info = price_info[0]
        handing_fee = price_info['real_price'] * HANDING_FEE
        if handing_fee <= MIN_EXTRA_COST:
            handing_fee = MIN_EXTRA_COST
        handing_fee = int(handing_fee)
        price_info['real_price'] += handing_fee
        price_info['original_price'] += handing_fee
        init_price_template(price_info, self.panel.temp_price, color=DARK_PRICE_COLOR)
        self.real_money_num = money_num
        self.real_price_info = price_info
        if not is_init:
            self.on_click_change_choose_list(self.panel.nd_total.btn_list.icon_arrow, self.panel.nd_total.choose_list)

    def on_click_change_choose_list(self, arrow, list):
        list_visible = not list.isVisible()
        if list_visible:
            arrow.setRotation(0)
        else:
            arrow.setRotation(180)
        list.setVisible(list_visible)

    def on_click_choose_red_packet(self, idx, item):
        if self.choose_cover_item:
            self.choose_cover_item.btn_choose.SetSelect(False)
        self.choose_cover_item = item
        self.choose_cover_item_no = self.owner_red_packet_cover_list[idx]
        self.choose_cover_item.btn_choose.SetSelect(True)
        self.refresh_left_red_packet_cover(self.choose_cover_item_no)
        set_user_setting_red_packet_cover(self.choose_cover_item_no)

    def on_click_send(self):
        if not check_payment(self.real_price_info['goods_payment'], self.real_price_info['real_price']):
            return
        if not global_data.player:
            return
        if self.channel == chat_const.CHAT_BATTLE_WORLD:
            from logic.client.const import game_mode_const
            if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CONCERT):
                global_data.player.gen_concert_red_packet(self.send_red_packet_type, self.select_money_num, self.select_packet_num, get_user_setting_red_packet_cover(), self.select_bless_id)
        else:
            global_data.player.gen_red_packet(self.channel, self.send_red_packet_type, self.select_money_num, self.select_packet_num, get_user_setting_red_packet_cover(), self.select_bless_id)
        global_data.emgr.send_red_packet_succeed.emit()
        self.close()

    def on_click_show_more(self):
        global_data.ui_mgr.show_ui('RedPacketCoverChangeUI', 'logic.comsys.red_packet')

    def on_click_close_btn(self, *args):
        self.close()

    def on_finalize_panel(self):
        self.unregist_main_ui()
        if self.price_top_widget:
            self.price_top_widget.destroy()
            self.price_top_widget = None
        return

    def set_skin_list_vis(self, vis):
        self.panel.nd_skin_list.setVisible(vis)

    def set_remain_unusable(self, usable):
        self.panel.nd_remain.setVisible(usable)