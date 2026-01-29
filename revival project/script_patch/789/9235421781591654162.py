# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/PriceWidget.py
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from common.cfg import confmgr
import six

class PriceWidget(object):

    def __init__(self, panel, activity_type):
        self.panel = panel
        self.price_widget = None
        self._activity_type = activity_type
        self.on_init_panel()
        return

    def on_init_panel(self):
        ui_data = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        self.price_widget = PriceUIWidget(self.panel, call_back=None, list_money_node=self.panel.list_money)
        money_exchange = ui_data.get('money_exchange', {})
        new_money_exchange = {}
        for money_type, goods_id in six.iteritems(money_exchange):
            new_money_exchange[int(money_type)] = goods_id

        self.price_widget.set_exchange_item_dict(new_money_exchange)
        self.price_widget.show_money_types(ui_data.get('money_types', []))
        return

    def on_finalize_panel(self):
        self.panel = None
        if self.price_widget:
            self.price_widget.destroy()
            self.price_widget = None
        return

    def refresh_panel(self):
        pass