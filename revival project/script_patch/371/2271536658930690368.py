# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNile/ActivityTreasurePavilion.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
from logic.gutils.mall_utils import buy_num_limit_by_all, check_payment_by_goods_id
from logic.gutils.template_utils import init_single_price, FrameLoaderTemplate
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import ITEM_SHOW_TYPE_AUTO
from logic.gcommon.time_utility import get_simply_readable_time, get_server_time
from logic.gutils import item_utils, activity_utils
from common.utils.timer import CLOCK
from common.cfg import confmgr
import six_ex

class ActivityTreasurePavilion(ActivityBase):

    def on_init_panel(self):
        self.init_params()
        self.init_ui()
        self.init_ui_event()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success_with_list': self._on_buy_good_success_goods_list,
           'player_item_update_event': self._update_lab_num,
           'receive_task_reward_succ_event': self._update_btn_get_redpoint
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_params(self):
        self._exchange_item = activity_utils.get_activity_conf_ui_data(self._activity_type, 'exchange_item')
        self._goods_id_list = activity_utils.get_activity_conf_ui_data(self._activity_type, 'goods_id_list')
        self._end_task_timestamp = activity_utils.get_activity_conf_ui_data(self._activity_type, 'end_task_timestamp')
        self._end_exchange_timestamp = activity_utils.get_activity_conf_ui_data(self._activity_type, 'end_exchange_timestamp')
        self._remain_time_text_id = None
        self._goods_item_dict = {}
        self._mall_config = confmgr.get('mall_config', default={})
        self._timer = None
        self._frame_loader_template = None
        return

    def init_ui(self):
        self._init_lab_time()
        self._init_goods_list()
        self._update_lab_num()
        self._update_btn_get_redpoint()

    def init_ui_event(self):

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            from .ActivityTreasurePavilionTaskPanelUI import ActivityTreasurePavilionTaskPanelUI
            ActivityTreasurePavilionTaskPanelUI(activity_type=self._activity_type)

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

    def _init_lab_time(self):
        time = get_server_time()
        if time < self._end_task_timestamp:
            self._remain_time = self._end_task_timestamp - time
            self._remain_time_text_id = 635496
            self.panel.btn_get.setVisible(True)
        elif self._end_task_timestamp < time < self._end_exchange_timestamp:
            self._remain_time = self._end_exchange_timestamp - time
            self._remain_time_text_id = 635497
            self.panel.btn_get.setVisible(False)
            global_data.emgr.refresh_activity_redpoint.emit()
        else:
            self.panel.lab_tips_time.SetString('')
            if self._timer:
                global_data.game_mgr.get_logic_timer().unregister(self._timer)
                self._timer = None
            return
        if self._remain_time > 0:
            if not self._timer:
                self._timer = global_data.game_mgr.get_logic_timer().register(func=self._update_lab_time, interval=1, mode=CLOCK)
            self._update_lab_time()
        return

    def _update_lab_time(self):
        if not self._remain_time_text_id:
            return
        else:
            self._remain_time = self._remain_time - 1
            if self._remain_time < 0:
                if self._timer:
                    global_data.game_mgr.get_logic_timer().unregister(self._timer)
                    self._timer = None
                self._init_lab_time()
            time_str = get_simply_readable_time(self._remain_time)
            self.panel.lab_tips_time.SetString(get_text_by_id(self._remain_time_text_id).format(time_str))
            return

    def _init_goods_list(self):
        self._frame_loader_template = FrameLoaderTemplate(self.panel.list_item, len(self._goods_id_list), self._init_goods_item)

    def _init_goods_item(self, item, cur_index):
        goods_id = str(self._goods_id_list[cur_index])
        conf = self._mall_config.get(goods_id, {})
        if not conf:
            log_error('\xe6\x89\xbe\xe4\xb8\x8d\xe5\x88\xb0\xe5\x95\x86\xe5\x93\x81id\xef\xbc\x9a{}\xe3\x80\x82\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa515.\xe5\x95\x86\xe5\x9f\x8e\xe8\xa1\xa8\xe6\x88\x9642.\xe6\xb4\xbb\xe5\x8a\xa8\xe9\x85\x8d\xe7\xbd\xae\xe8\xa1\xa8\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81'.format(goods_id))
            self.panel.list_item.RecycleItem(item)
            return
        self._goods_item_dict[goods_id] = item
        item_no = conf.get('item_no')
        item_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
        item.item.SetDisplayFrameByPath('', item_path)
        item.lab_name.setString(item_utils.get_lobby_item_name(item_no))
        lab_quantity = item.lab_quantity
        item_num = conf.get('num', 0)
        if item_num > 1:
            lab_quantity.setVisible(True)
            lab_quantity.SetString(str(item_num))
        else:
            lab_quantity.setVisible(False)
        temp_level = item.temp_level
        degree_pic = item_utils.get_skin_rare_degree_icon(item_no)
        if degree_pic:
            temp_level.setVisible(True)
            temp_level.bar_level.SetDisplayFrameByPath('', degree_pic)
        else:
            temp_level.setVisible(False)
        color = [
         3746445, '#SR', 3746445]
        init_single_price(item.temp_price, goods_id, color, 'item')
        self._update_goods_state(goods_id)
        btn_bg_item = item.btn_bg_item
        btn_bg_item.EnableCustomState(True)

        @btn_bg_item.unique_callback()
        def OnClick(btn, touch):
            if not check_payment_by_goods_id(goods_id, pay_tip=False):
                global_data.game_mgr.show_tip(get_text_by_id(609936))
            else:
                GroceriesBuyConfirmUI(goods_id=goods_id, need_show=ITEM_SHOW_TYPE_AUTO)

    def _update_goods_state(self, goods_id):
        goods_id = str(goods_id)
        item = self._goods_item_dict.get(goods_id)
        if item and item.isValid():
            sold_out, _, num_info = buy_num_limit_by_all(goods_id)
            limit_num, max_num = num_info
            item.lab_got.setVisible(sold_out)
            item.temp_price.setVisible(not sold_out)
            item.btn_bg_item.SetShowEnable(not sold_out)
            item.lab_times.setString(get_text_by_id(12126).format(max_num - limit_num, max_num))

    def _on_buy_good_success_goods_list(self, goods_list):
        for goods_info in goods_list:
            goods_id = goods_info[0]
            self._update_goods_state(goods_id)

    def _update_lab_num(self):
        item_count = global_data.player.get_item_num_by_no(int(self._exchange_item)) if global_data.player else 0
        self.panel.lab_num.setString(str(item_count))
        for goods_id, item in six_ex.items(self._goods_item_dict):
            if item and item.isValid():
                color = [3746445, '#SR', 3746445]
                init_single_price(item.temp_price, goods_id, color, 'item')

    def _update_btn_get_redpoint(self, *args):
        has_redpoint = activity_utils.get_redpoint_count_by_type(self._activity_type) > 0
        self.panel.img_red.setVisible(has_redpoint)

    def on_finalize_panel(self):
        self.process_event(False)
        if self._frame_loader_template:
            self._frame_loader_template.destroy()
            self._frame_loader_template = None
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = None
        return