# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/MiaomiaoItemGoUseDismountWidget.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gutils import mall_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_LOBBY_SKIN, L_ITEM_TYPE_MUSIC
from logic.gutils import jump_to_ui_utils
from logic.gutils import item_utils

class MiaomiaoItemGoUseDismountWidget(object):

    def __init__(self, parent, go_btn, use_btn, dismount_btn, btn_preview, price_temp):
        self.parent = parent
        self.go_btn = go_btn
        self.use_btn = use_btn
        self.btn_preview = btn_preview
        self.dismount_btn = dismount_btn
        self.price_temp = price_temp
        self.item_no = None
        self.goods_id = None
        self.init_event()
        return

    def update_target_item_no(self, item_no, goods_id):
        self.item_no = item_no
        self.goods_id = goods_id
        self.refresh_widget()

    def init_event(self):
        if self.go_btn:
            self.go_btn.btn_common_big.BindMethod('OnClick', self.on_click_go_btn)
        if self.use_btn:
            self.use_btn.btn_common_big.BindMethod('OnClick', self.on_click_use_btn)
        if self.dismount_btn:
            self.dismount_btn.btn_common_big.BindMethod('OnClick', self.on_click_dismount_btn)
        if self.btn_preview:
            self.btn_preview.BindMethod('OnClick', self.on_click_preview)

    def update_go_widget(self, item_can_goto):
        if self.go_btn:
            self.go_btn.setVisible(item_can_goto)

    def update_use_widget(self, can_use):
        if self.use_btn:
            self.use_btn.setVisible(can_use)

    def update_dismount_widget(self, can_jump):
        if self.dismount_btn:
            self.dismount_btn.setVisible(can_jump)

    def is_default_item(self, item_no):
        from logic.gcommon.item.item_const import DEFAULT_LOBBY_BGM, DEFAULT_LOBBY_SKIN, DEFAULT_LOBBY_SKYBOX
        return int(item_no) in [DEFAULT_LOBBY_BGM, DEFAULT_LOBBY_SKIN, DEFAULT_LOBBY_SKYBOX]

    def get_music_item_no(self):
        from logic.gcommon.item.item_const import DEFAULT_LOBBY_BGM
        cur_bgm_item_no = global_data.player.get_lobby_bgm() or DEFAULT_LOBBY_BGM
        return cur_bgm_item_no

    def refresh_widget(self):
        item_can_use, _ = mall_utils.item_can_use_by_item_no(self.item_no)
        self.update_go_widget(not item_can_use)
        cur_miaomiao_item_no = None
        if global_data.player:
            item_type = item_utils.get_lobby_item_type(self.item_no)
            if item_type == L_ITEM_TYPE_LOBBY_SKIN:
                cur_miaomiao_item_no = global_data.player.get_lobby_skin()
            elif item_type == L_ITEM_TYPE_MUSIC:
                from logic.gcommon.item.item_const import DEFAULT_LOBBY_BGM
                cur_miaomiao_item_no = self.get_music_item_no()
        print('cur_miaomiao_item_no', cur_miaomiao_item_no)
        can_use = item_can_use and str(cur_miaomiao_item_no) != str(self.item_no)
        self.update_use_widget(can_use)
        itme_can_dismount = item_can_use and str(cur_miaomiao_item_no) == str(self.item_no)
        self.update_dismount_widget(itme_can_dismount)
        if itme_can_dismount:
            if self.dismount_btn:
                self.dismount_btn.btn_common_big.SetText(14007)
                self.dismount_btn.btn_common_big.SetEnable(False)
        return can_use

    def on_click_go_btn(self, *args):
        can_buy_in_mall = mall_utils.get_goods_can_buy_in_mall(self.goods_id)
        if self.goods_id and can_buy_in_mall:
            jump_to_ui_utils.jump_to_mall(self.goods_id)
        else:
            from logic.gutils.item_utils import get_lobby_item_name, jump_to_ui
            jump_to_ui(self.item_no)

    def on_click_use_btn(self, *args):
        if not self.item_no:
            return
        item_type = item_utils.get_lobby_item_type(self.item_no)
        if item_type == L_ITEM_TYPE_LOBBY_SKIN:
            global_data.player.change_lobby_skin(self.item_no)
        elif item_type == L_ITEM_TYPE_MUSIC:
            global_data.player.select_lobby_bgm(self.item_no)

    def on_click_dismount_btn(self, *args):
        if not self.item_no:
            return
        item_type = item_utils.get_lobby_item_type(self.item_no)
        if item_type == L_ITEM_TYPE_LOBBY_SKIN:
            global_data.player.change_lobby_skin(0)
        elif item_type == L_ITEM_TYPE_MUSIC:
            from logic.gcommon.item.item_const import DEFAULT_LOBBY_BGM
            global_data.player.select_lobby_bgm(DEFAULT_LOBBY_BGM)

    def on_click_preview(self, *args):
        from logic.gutils.jump_to_ui_utils import jump_to_lobby_skin_preview
        jump_to_lobby_skin_preview(self.item_no, (item_utils.get_lobby_item_type(self.item_no),))

    def destroy(self):
        self.parent = None
        self.buy_btn = None
        self.use_btn = None
        self.jump_btn = None
        self.price_temp = None
        return