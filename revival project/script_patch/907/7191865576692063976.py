# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/ItemSkinBuyConfirmUI.py
from __future__ import absolute_import
from logic.comsys.mall_ui.RoleAndSkinBuyConfirmUI import RoleAndSkinBuyConfirmUI
from logic.gutils import mall_utils
from logic.comsys.common_ui.JapanShoppingTips import show_with_japan_shopping_tips

@show_with_japan_shopping_tips
class ItemSkinBuyConfirmUI(RoleAndSkinBuyConfirmUI):
    PANEL_CONFIG_NAME = 'mall/buy_confirm_weapen'

    def set_module_info(self, goods_id):
        pass

    def set_item_info(self, goods_id):
        path = mall_utils.get_detail_pic(goods_id)
        can_view = bool(path)
        self.panel.img_gun.setVisible(can_view)
        can_view and self.panel.img_gun.SetDisplayFrameByPath('', path)
        self.panel.lab_name.SetString(mall_utils.get_goods_name(goods_id))
        self.panel.lab_describe.SetString(mall_utils.get_goods_decs(goods_id))
        access_txt = mall_utils.get_item_access(goods_id)
        self.panel.nd_other_unlock.setVisible(bool(access_txt))
        access_txt and self.panel.lab_other_unlock.SetString(access_txt)

    def init_view(self):
        pass

    def adjuest_buy_btn(self):
        pass