# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallDisplayCompetitionListWidget.py
from __future__ import absolute_import
from logic.comsys.mall_ui.MallDisplayFragmentListWidget import MallDisplayFragmentListWidget
from logic.client.const import mall_const
COM_TIP_ARCHIVE_DATA_KEY = 'mall_competition_show_tip'

class MallDisplayCompetitionListWidget(MallDisplayFragmentListWidget):
    TIPS_KEY = COM_TIP_ARCHIVE_DATA_KEY
    TIPS_TID = 931015
    TABLE_NAME = 'mall_summer_competition_config'
    TABLE_ERROR_MSG = '15.\xe5\x95\x86\xe5\x9f\x8e\xe8\xa1\xa8-\xe8\xb5\x9b\xe4\xba\x8b\xe5\x85\x91\xe6\x8d\xa2\xe5\x95\x86\xe5\xba\x97\xe8\xa1\xa8   \xe7\x83\x82\xe4\xba\x86\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81'
    SETTING_KEY = mall_const.SETTING_NEW_COMPETITION_GOODS

    @staticmethod
    def show_red_point(tip_archive_data_key=COM_TIP_ARCHIVE_DATA_KEY, conf_name='mall_summer_competition_config', setting_key=mall_const.SETTING_NEW_FRAGMENT_GOODS):
        return MallDisplayFragmentListWidget.show_red_point(tip_archive_data_key, conf_name, setting_key)

    def set_show(self, show):
        super(MallDisplayCompetitionListWidget, self).set_show(show)
        if show:
            self.check_req_global_buy_info()

    def init_shop_rule(self):

        @self.panel.btn_button.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(931014, 931015)

    def is_item_has_bought(self, goods_id):
        from logic.gutils.mall_utils import get_limit_info, limite_pay
        limit_buy = limite_pay(goods_id)
        return limit_buy

    def cb_create_item(self, index, item_widget):
        super(MallDisplayCompetitionListWidget, self).cb_create_item(index, item_widget)
        is_special = False
        if index < len(self.special_goods_items):
            goods_id = self.special_goods_items[index]
            is_special = True
        elif index - len(self.special_goods_items) < len(self.goods_items):
            goods_id = self.goods_items[index - len(self.special_goods_items)]
        else:
            goods_id = None
        goods_id = str(goods_id)
        from logic.gutils.mall_utils import get_limit_info, limite_pay
        limit_buy = limite_pay(goods_id)
        if limit_buy:
            item_widget.nd_sold_out.setVisible(limit_buy)
        return

    def check_req_global_buy_info(self):
        from common.cfg import confmgr
        import time
        global_limit_list = []
        for goods_list in [self.special_goods_items, self.goods_items]:
            for goods_id in goods_list:
                goods_conf = confmgr.get('mall_config', str(goods_id), default={})
                global_buy_limit = goods_conf.get('global_buy_limit', None)
                if global_buy_limit:
                    global_limit_list.append(goods_id)

        if global_limit_list:
            last_req_global_buy_info_time = global_data.last_req_global_buy_info_time or 0
            cur_time = time.time()
            if cur_time - last_req_global_buy_info_time > 10:
                global_data.player.req_global_buy_info(global_limit_list)
                global_data.last_req_global_buy_info_time = cur_time
        return

    def get_buy_ui(self):
        from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
        return groceries_buy_confirmUI(self.select_goods_id)