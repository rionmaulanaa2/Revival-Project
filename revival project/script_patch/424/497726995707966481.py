# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGAGCExchange.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityExchangeNew import ActivityExchangeNew
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_EXCHANGED, BTN_ST_EXCHANGE
from logic.gutils.new_template_utils import update_task_list_btn
from logic.comsys.activity.ActivityExchange import ActivityExchange
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import task_utils, mall_utils, jump_to_ui_utils, activity_utils, item_utils

class ActivityGAGCExchange(ActivityExchangeNew):

    def __init__(self, dlg, activity_type):
        super(ActivityGAGCExchange, self).__init__(dlg, activity_type)
        self.goods_id = '201800771'

    def on_init_panel(self):
        super(ActivityGAGCExchange, self).on_init_panel()
        start_str, end_str = activity_utils.get_activity_open_time(self._activity_type)
        self.panel.lab_time.SetString('{}-{}'.format(start_str, end_str))
        self.panel.act_list_common.setVisible(False)
        self.panel.act_list.setVisible(True)
        self.panel.lab_mecha.SetString(get_text_by_id(610077))

        @self.panel.btn_watch.unique_callback()
        def OnClick(*args):
            self.on_click_watch_btn()

    def refresh_list(self):
        super(ActivityGAGCExchange, self).refresh_list()
        self.init_exchange_list_item()

    def set_show(self, show, is_init=False):
        super(ActivityGAGCExchange, self).set_show(show, is_init)
        if show:
            self.panel.PlayAnimation('show')
            try:
                parent_panel = self.panel.GetParent()
                grand_parent_panel = parent_panel.GetParent()
                grand_parent_panel.temp_activity_top.sub_page_widget_610080.PlayAnimation('show')
            except:
                pass

    def on_click_watch_btn(self, *args):
        jump_to_ui_utils.jump_to_display_detail_by_item_no(self.goods_id, {'skin_list': True})

    def init_exchange_list_item(self):
        children_tasks = task_utils.get_children_task(self.parent_task_id)
        self.panel.list_item.SetInitCount(len(children_tasks))
        for idx, task_id in enumerate(children_tasks):
            item_widget = self.panel.list_item.GetItem(idx)
            extra_params = task_utils.get_task_arg(task_id)
            goods_id = str(extra_params.get('goodsid', ''))
            if not goods_id:
                self.panel.list_item.setVisible(False)
                return
            target_item_no = mall_utils.get_goods_item_no(goods_id)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id)
            if num_info:
                left_num, max_num = num_info
                item_widget.lab_num.SetString('{}/{}'.format(left_num, max_num))
            else:
                item_widget.lab_num.SetString('')
            template_utils.init_tempate_mall_i_item(item_widget.temp_item, target_item_no, show_tips=True)