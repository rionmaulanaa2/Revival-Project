# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/SkinGetUseBuyWidget.py
from __future__ import absolute_import
from logic.gutils import items_book_utils
from logic.gutils import item_utils
from logic.gcommon.item import item_const
from logic.gutils import template_utils
from logic.gutils import mall_utils
from logic.comsys.mall_ui.BuyConfirmUIInterface import item_skin_buy_confirmUI

class SkinGetUseBuyWidget(object):

    def __init__(self, parent, buy_btn, use_btn, jump_btn, price_temp, jump_desc):
        self.parent = parent
        self.buy_btn = buy_btn
        self.use_btn = use_btn
        self.jump_btn = jump_btn
        self.price_temp = price_temp
        self.jump_desc = jump_desc
        self.item_no = None
        self.skin_no = None
        self.goods_id = None
        self.init_event()
        return

    def update_target_item_no(self, item_no, skin_no, goods_id):
        self.item_no = item_no
        self.skin_no = skin_no
        self.goods_id = goods_id
        self.refresh_widget()

    def init_event(self):
        if self.buy_btn:
            self.buy_btn.btn_common_big.BindMethod('OnClick', self.on_click_buy_btn)
        if self.use_btn:
            self.use_btn.btn_common_big.BindMethod('OnClick', self.on_click_use_btn)
        if self.jump_btn:
            self.jump_btn.btn_common_big.BindMethod('OnClick', self.on_click_jump_btn)

    def update_buy_widget(self, can_buy):
        if self.buy_btn:
            self.buy_btn.setVisible(can_buy)
        if self.goods_id:
            template_utils.init_price_view(self.price_temp, self.goods_id)

    def update_use_widget(self, can_use):
        if self.use_btn:
            self.use_btn.setVisible(can_use)

    def update_jump_widget(self, can_jump, jump_txt):
        if self.jump_btn:
            enable = item_utils.can_jump_to_ui(self.skin_no) and can_jump
            self.jump_btn.btn_common_big.SetEnable(enable)
            self.jump_btn.btn_common_big.SetText(get_text_by_id(2222 if enable else 80828))
            self.jump_btn.setVisible(can_jump and bool(jump_txt))
        if self.jump_desc:
            self.jump_desc.SetString(jump_txt or '')

    def refresh_widget(self):
        item_can_use, _ = mall_utils.item_can_use_by_item_no(self.skin_no)
        can_buy = bool(self.goods_id) and not item_can_use
        self.update_buy_widget(can_buy)
        item_fashion_no = items_book_utils.get_item_fashion_no(self.item_no)
        can_use = item_can_use and item_fashion_no != int(self.skin_no)
        self.update_use_widget(can_use)
        can_jump = not can_buy and not item_can_use
        jump_txt = item_utils.get_item_access(self.skin_no)
        self.update_jump_widget(can_jump, jump_txt)
        return can_use

    def on_click_buy_btn(self, *args):
        if self.goods_id is None or mall_utils.item_has_owned_by_goods_id(self.goods_id):
            return
        else:
            ui = item_skin_buy_confirmUI(self.goods_id)
            ui.set_buttom_ui_price_nd(self.parent.parent.panel.top.list_money)
            return

    def on_click_use_btn(self, *args):
        if not self.skin_no:
            return
        fashion_dict = {item_const.WEAPON_FASHION_PART_SUIT: self.skin_no}
        global_data.player and global_data.player.try_dress_battle_item_fashion(str(self.item_no), fashion_dict)

    def on_click_jump_btn(self, *args):
        item_utils.jump_to_ui(self.skin_no)

    def destroy(self):
        self.parent = None
        self.buy_btn = None
        self.use_btn = None
        self.jump_btn = None
        self.price_temp = None
        self.jump_desc = None
        return