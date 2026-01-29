# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGranbelmDiscount.py
from __future__ import absolute_import
import six
from logic.gutils import item_utils
from logic.gutils import template_utils
from logic.gutils import mall_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
from logic.gutils.jump_to_ui_utils import jump_to_mall

class ActivityGranbelmDiscount(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityGranbelmDiscount, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.ui_data = conf.get('cUiData', {})

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self.on_init_panel()

    def on_init_panel(self):
        start_str, end_str = activity_utils.get_activity_open_time(self._activity_type)
        if start_str and end_str:
            self.panel.lab_time.SetString(get_text_by_id(604006).format(start_str, end_str))
        btn = self.panel.nd_go.temp_go.btn_major

        @btn.unique_callback()
        def OnClick(btn, touch, *args):
            if not global_data.player.has_item_by_no(16):
                jump_to_mall('16')
            elif not global_data.player.has_item_by_no(101008014):
                jump_to_mall('101008014')
            elif not global_data.player.has_item_by_no(15):
                jump_to_mall('15')
            else:
                jump_to_mall('16')

        goods_node_info = self.ui_data.get('goods_node', {})
        for goods_id, node_name in six.iteritems(goods_node_info):
            nd_node = getattr(self.panel.nd_content, node_name)
            self.set_goods_info(goods_id, nd_node)

            @nd_node.btn_buy.unique_callback()
            def OnClick(btn, touch, gid=goods_id):
                if mall_utils.item_has_owned_by_goods_id(gid):
                    global_data.game_mgr.show_tip(get_text_by_id(607216))
                else:
                    role_or_skin_buy_confirmUI(gid)

        self.panel.PlayAnimation('loop')
        self.panel.PlayAnimation('loop2')

    def set_goods_info(self, goods_id, nd_node):
        from logic.gutils import mall_utils
        temp_price = nd_node.temp_price
        prices = mall_utils.get_mall_item_price(str(goods_id))
        for i, price_info in enumerate(prices):
            if temp_price:
                template_utils.init_price_template(price_info, temp_price)
                break