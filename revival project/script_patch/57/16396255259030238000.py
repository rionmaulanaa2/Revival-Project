# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/GroceriesBothBuyConfirmUI.py
from __future__ import absolute_import
from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
from logic.comsys.common_ui.JapanShoppingTips import show_with_japan_shopping_tips

@show_with_japan_shopping_tips
class GroceriesBothBuyConfirmUI(GroceriesBuyConfirmUI):
    PANEL_CONFIG_NAME = 'mall/buy_confirm_groceries_both'