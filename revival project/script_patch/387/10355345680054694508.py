# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/InteractionGetUseBuyWidget.py
from __future__ import absolute_import
from logic.gutils import item_utils
from logic.gutils import template_utils
from logic.gutils import mall_utils
from logic.client.const import items_book_const

class InteractionGetUseBuyWidget(object):

    def __init__(self, parent, buy_btn, use_btn, jump_btn, price_temp, jump_desc):
        self.parent = parent
        self.buy_btn = buy_btn
        self.use_btn = use_btn
        self.jump_btn = jump_btn
        self.price_temp = price_temp
        self.jump_desc = jump_desc
        self.goods_id = None
        self.state = None
        self.init_event()
        self.init_widget()
        return

    def init_widget(self):
        if self.buy_btn:
            self.buy_btn.setVisible(False)
        if self.use_btn:
            self.use_btn.setVisible(False)
        if self.jump_btn:
            self.jump_btn.setVisible(False)

    def update_target_item_no(self, goods_id, state):
        self.goods_id = goods_id
        self.state = state
        self.refresh_widget()

    def init_event(self):
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
            self.jump_btn.setVisible(can_jump)
        if self.jump_desc:
            self.jump_desc.SetString(jump_txt or '')

    def refresh_widget(self):
        can_use, _ = mall_utils.item_can_use_by_item_no(self.goods_id)
        can_jump = item_utils.can_jump_to_ui(self.goods_id) and not can_use and self.state == items_book_const.INTERACTION_STATE_DISPLAY
        jump_txt = item_utils.get_item_access(self.goods_id)
        self.update_jump_widget(can_jump, jump_txt)
        return can_use

    def on_click_jump_btn(self, *args):
        item_utils.jump_to_ui(self.goods_id)

    def destroy(self):
        self.parent = None
        self.buy_btn = None
        self.use_btn = None
        self.jump_btn = None
        self.price_temp = None
        self.jump_desc = None
        return