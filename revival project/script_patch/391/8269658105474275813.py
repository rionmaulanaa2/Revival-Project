# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ZombieFFA/ZombieFFAPriceUIWidget.py
from __future__ import absolute_import
from logic.gcommon import const
from logic.gutils import item_utils

class ZombieFFAPriceUIWidget(object):

    def __init__(self, parent, list_money_node):
        self.parent = parent
        self.panel = parent.panel
        self.list_money = list_money_node

    def init_parameter(self):
        self.money_types = []
        self.money_info = {}
        self.money_to_widget = {}

    def on_finalize_panel(self):
        self.parent = None
        self.panel = None
        self.list_money = None
        return

    def destroy(self):
        self.on_finalize_panel()

    def update_money_info(self, money_info):
        self.money_info = money_info
        self._on_update_money_info()

    def _on_update_money_info(self):
        self.list_money.SetInitCount(len(self.money_info))
        for idx, money_item_no in enumerate(self.money_info):
            money_nd = self.list_money.GetItem(idx)
            money_count = self.money_info[money_item_no].get('count', 0)
            money_color = self.money_info[money_item_no].get('color')
            money_icon = item_utils.get_money_icon(money_item_no)
            money_nd.txt_price.SetString(str(money_count))
            money_color and money_nd.txt_price.SetColor(money_color)
            money_nd.price_icon.SetDisplayFrameByPath('', money_icon)
            money_nd.PlayAnimation('change')

        self.list_money.ChildResizeAndPosition()