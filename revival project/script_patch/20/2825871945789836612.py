# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAnnivMilaBow.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityCollect import ActivityCollect
from logic.gcommon.item import item_const as iconst
from logic.gcommon.common_const import activity_const
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import task_utils
from logic.gutils import mall_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_DAY_SECONDS, ONE_HOUR_SECONS
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
from logic.client.const import mall_const
GOODS_ID_SKIN_PRINCESS_MILA = '690116220'

class ActivityAnnivMilaBow(ActivityCollect):

    def on_init_panel(self):
        super(ActivityAnnivMilaBow, self).on_init_panel()
        skin_name = item_utils.get_lobby_item_name(iconst.ITEM_NO_SKIN_PRINCESS_MILA)
        self.panel.img_name.SetString(skin_name)
        self.refresh_bow_cnt()
        self.init_btn_go()

        @self.panel.btn_role.unique_callback()
        def OnClick(btn, touch):
            jump_to_display_detail_by_item_no(iconst.ITEM_NO_SKIN_PRINCESS_MILA)

        @self.panel.btn_go.unique_callback()
        def OnClick(btn, touch):
            ui = global_data.ui_mgr.get_ui('ActivityAnnivMainUI')
            ui.try_select_tab(activity_const.ACTIVITY_ANNIV_MILA_BOW_EXCHANGE)
            page_tab_widget = ui.get_page_tab_widget()
            if page_tab_widget:
                cur_page_widget = page_tab_widget.get_cur_view_page_widget()
                if cur_page_widget:
                    if getattr(cur_page_widget, 'highlight_item_by_goods_id'):
                        cur_page_widget.highlight_item_by_goods_id(goods_id=GOODS_ID_SKIN_PRINCESS_MILA)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'on_lobby_bag_item_changed_event': self.refresh_bow_cnt
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_bow_cnt(self):
        ui = global_data.ui_mgr.get_ui('ActivityAnnivMainUI')
        page_tab_widget = ui.get_page_tab_widget()
        if page_tab_widget:
            cur_view_sub_page_widget = page_tab_widget.get_cur_view_sub_page_widget()
            if cur_view_sub_page_widget:
                cur_view_sub_page_widget.refresh_bow_cnt()

    def set_show(self, show, is_init=False):
        super(ActivityAnnivMilaBow, self).set_show(show, is_init)
        self.panel.PlayAnimation('show')

    def show_list(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        parent_task = task_list[0]
        children_tasks = task_utils.get_children_task(parent_task)
        children_tasks = self.reorder_task_list(children_tasks)
        self._children_tasks = children_tasks

        def callback--- This code section failed: ---

  95       0  LOAD_GLOBAL           0  'task_utils'
           3  LOAD_ATTR             1  'get_raw_left_open_time'
           6  LOAD_DEREF            0  'parent_task'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            0  'left_time'

  96      15  STORE_FAST            1  'close_left_time'
          18  COMPARE_OP            4  '>'
          21  POP_JUMP_IF_FALSE   122  'to 122'

  97      24  LOAD_FAST             0  'left_time'
          27  LOAD_GLOBAL           2  'ONE_HOUR_SECONS'
          30  COMPARE_OP            4  '>'
          33  POP_JUMP_IF_FALSE    79  'to 79'

  98      36  LOAD_DEREF            1  'self'
          39  LOAD_ATTR             3  'panel'
          42  LOAD_ATTR             4  'lab_time'
          45  LOAD_ATTR             5  'SetString'

  99      48  LOAD_GLOBAL           6  'get_text_by_id'
          51  LOAD_CONST            2  607014
          54  CALL_FUNCTION_1       1 
          57  LOAD_ATTR             7  'format'
          60  LOAD_GLOBAL           8  'get_readable_time_day_hour_minitue'
          63  LOAD_FAST             0  'left_time'
          66  CALL_FUNCTION_1       1 
          69  CALL_FUNCTION_1       1 
          72  CALL_FUNCTION_1       1 
          75  POP_TOP          
          76  JUMP_ABSOLUTE       153  'to 153'

 101      79  LOAD_DEREF            1  'self'
          82  LOAD_ATTR             3  'panel'
          85  LOAD_ATTR             4  'lab_time'
          88  LOAD_ATTR             5  'SetString'
          91  LOAD_GLOBAL           6  'get_text_by_id'
          94  LOAD_CONST            2  607014
          97  CALL_FUNCTION_1       1 
         100  LOAD_ATTR             7  'format'
         103  LOAD_GLOBAL           9  'get_readable_time'
         106  LOAD_FAST             0  'left_time'
         109  CALL_FUNCTION_1       1 
         112  CALL_FUNCTION_1       1 
         115  CALL_FUNCTION_1       1 
         118  POP_TOP          
         119  JUMP_FORWARD         31  'to 153'

 103     122  LOAD_CONST            1  ''
         125  STORE_FAST            1  'close_left_time'

 104     128  LOAD_DEREF            1  'self'
         131  LOAD_ATTR             3  'panel'
         134  LOAD_ATTR             4  'lab_time'
         137  LOAD_ATTR             5  'SetString'
         140  LOAD_GLOBAL           9  'get_readable_time'
         143  LOAD_FAST             1  'close_left_time'
         146  CALL_FUNCTION_1       1 
         149  CALL_FUNCTION_1       1 
         152  POP_TOP          
       153_0  COME_FROM                '119'

Parse error at or near `STORE_FAST' instruction at offset 15

        self._timer_cb[0] = callback
        callback()
        sub_act_list = self.panel.act_list
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(children_tasks))
        ui_data = conf.get('cUiData', {})
        for i, task_id in enumerate(children_tasks):
            item_widget = sub_act_list.GetItem(i)
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            if ui_data.get('lab_name_color'):
                color = int(ui_data.get('lab_name_color'), 16)
                item_widget.lab_name.SetColor(color)
            if ui_data.get('lab_num_color'):
                color = int(ui_data.get('lab_num_color'), 16)
                item_widget.lab_num.SetColor(color)
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)

        self.refresh_list()

    def init_btn_go(self):
        if mall_utils.item_has_owned_by_item_no(iconst.ITEM_NO_SKIN_PRINCESS_MILA):
            self.panel.btn_go.setVisible(False)
            return
        self.panel.btn_go.setVisible(True)
        prices = mall_utils.get_mall_item_price(GOODS_ID_SKIN_PRINCESS_MILA)
        if len(prices) > 0:
            prices[0].update({'goods_payment': SHOP_PAYMENT_YUANBAO
               })
        template_utils.splice_price(self.panel.btn_go.temp_price, prices, color=mall_const.NO_RED_DARK_PRICE_COLOR)