# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/task/DayTaskWidget.py
from __future__ import absolute_import
from six.moves import range
from functools import cmp_to_key
from .CommonTaskWidget import CommonTaskWidget
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER
from common.framework import Functor
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils import task_utils
from logic.gutils.new_template_utils import VitalityBoxReward
from logic.gutils.client_utils import post_ui_method
from logic.comsys.lottery.LotteryTurntableSecondComfirm import LotteryTurntableSecondComfirm

class DayTaskWidget(CommonTaskWidget):

    def __init__(self, parent, panel, task_type):
        super(DayTaskWidget, self).__init__(parent, panel, task_type)
        self.nd_content = self.panel.temp_content
        self.day_vitality_box_widgets = {}
        self.week_vitality_box_widgets = {}
        self.cur_tab_index = 0
        self.cur_widget_list = None
        self.cur_tab_btn = None
        return

    def init_event(self):
        super(DayTaskWidget, self).init_event()
        global_data.emgr.update_day_vitality_event += self._on_update_day_vitality
        global_data.emgr.update_day_vitality_reward_event += self._on_update_day_vitality_reward
        global_data.emgr.update_week_vitality_event += self._on_update_week_vitality
        global_data.emgr.update_week_vitality_reward_event += self._on_update_week_vitality_reward
        global_data.emgr.refresh_day_random_task += self.refresh_day_random_task
        global_data.emgr.update_day_vitality_event += self._refresh_get_all_btn
        global_data.emgr.update_day_vitality_reward_event += self._refresh_get_all_btn
        global_data.emgr.update_week_vitality_event += self._refresh_get_all_btn
        global_data.emgr.update_week_vitality_reward_event += self._refresh_get_all_btn
        global_data.emgr.task_prog_changed += self._refresh_get_all_btn
        global_data.emgr.receive_task_reward_succ_event += self._refresh_get_all_btn

        @self.nd_content.temp_get_all.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            global_data.player and global_data.player.call_server_method('receive_all_day_task_rewards')

    def init_task_type_tab(self):
        self.tab_info = [{'tab_name': 634570}, {'tab_name': 634571}]
        tab_list = self.nd_content.list_tab
        tab_list.SetInitCount(len(self.tab_info))
        all_items = tab_list.GetAllItem()
        for index, widget in enumerate(all_items):
            if not widget:
                continue

            @widget.btn_tab.callback()
            def OnClick(btn, touch, index=index, item=widget):
                if index == 0:
                    task_ids = self.get_task_ids()
                else:
                    task_ids = self.get_random_task_ids()
                if not task_ids or len(task_ids) <= 0:
                    return
                task_ids.sort(key=cmp_to_key(task_utils.sort_task_func))
                self.cur_tab_index = index
                self.init_task_content(task_ids)
                if self.cur_tab_btn:
                    self.cur_tab_btn.SetSelect(False)
                self.cur_tab_btn = btn
                self.cur_tab_btn.SetSelect(True)
                self.update_tab_btn_red_point()

        first_red = self.check_task_tab_red_point(0)
        sec_red = self.check_task_tab_red_point(1)
        item = all_items[0]
        if first_red:
            item = all_items[0]
        elif sec_red:
            item = all_items[1]
        else:
            item = all_items[0]
        item.btn_tab.OnClick(item.btn_tab)

    def get_finish_task_num(self, task_ids):
        if not task_ids:
            return (0, 0)
        has_get = 0
        for task_id in task_ids:
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED or status == ITEM_RECEIVED:
                has_get += 1

        return (
         has_get, len(task_ids))

    def update_tab_btn_red_point(self):
        tab_list = self.nd_content.list_tab
        all_items = tab_list.GetAllItem()
        for index, widget in enumerate(all_items):
            task_ids = []
            if index == 0:
                task_ids = self.get_task_ids()
            else:
                task_ids = self.get_random_task_ids()
            has_get, max_task = self.get_finish_task_num(task_ids)
            info = self.tab_info[index]
            if self.cur_tab_index == index:
                widget.lab_title.SetColor('#SW')
            else:
                widget.lab_title.SetColor(7307174)
            widget.lab_title.SetString(get_text_by_id(info.get('tab_name')).format(has_get, max_task), '')
            is_red = self.check_task_tab_red_point(index)
            if is_red:
                widget.img_red_dot.setVisible(True)
            else:
                widget.img_red_dot.setVisible(False)

    def init_widget(self, need_hide=True):
        super(DayTaskWidget, self).init_widget(need_hide)
        self.init_task_type_tab()
        self.init_day_vitality()
        self.init_week_vitality()
        self._refresh_get_all_btn()

    def _refresh_get_all_btn(self, *args, **kwargs):
        if self.check_red_point():
            self.nd_content.temp_get_all.btn_common_big.SetEnable(True)
            self.nd_content.temp_get_all.setVisible(True)
            self.nd_content.pnl_get_all.setVisible(True)
        else:
            self.nd_content.temp_get_all.btn_common_big.SetEnable(False)
            self.nd_content.temp_get_all.setVisible(False)
            self.nd_content.pnl_get_all.setVisible(False)
        self.update_tab_btn_red_point()

    def _on_reset_day_vitality(self):
        self.init_day_vitality()

    def _on_reset_week_vitality(self):
        self.init_week_vitality()

    def init_day_vitality(self):
        max_vitality_level = task_utils.get_max_day_vitality_level()
        for lv in range(1, max_vitality_level + 1):
            lv_conf = task_utils.get_vitality_conf_by_level(lv)
            vitality_point = lv_conf.get('vitality_point')
            nd_temp = getattr(self.nd_content, 'temp_' + str(lv))
            if nd_temp:
                box_widget = VitalityBoxReward(nd_temp, lv, self.on_click_day_vitality)
                self.day_vitality_box_widgets[lv] = box_widget
                box_widget.update_vitality_point(vitality_point)
                reward_st = global_data.player.get_vitality_reward_status(lv)
                box_widget.update_reward_status(reward_st)

        self._on_update_day_vitality()

    def init_week_vitality(self):
        max_vitality_level = task_utils.get_max_week_vitality_level()
        for lv in range(1, max_vitality_level + 1):
            vitality_point = task_utils.get_week_vitality_point_by_level(lv)
            nd_reward = getattr(self.nd_content, 'nd_reward_' + str(lv))
            if nd_reward:
                box_widget = VitalityBoxReward(nd_reward, lv, self.on_click_week_vitality)
                self.week_vitality_box_widgets[lv] = box_widget
                box_widget.update_vitality_point(vitality_point)
                reward_st = global_data.player.get_week_vitality_reward_status(lv)
                box_widget.update_reward_status(reward_st)

        self._on_update_week_vitality()

    def on_click_day_vitality(self, btn, touch, lv):
        reward_st = global_data.player.get_vitality_reward_status(lv)
        if reward_st == ITEM_UNRECEIVED:
            global_data.player.receive_vitality_reward(lv)
        elif reward_st == ITEM_RECEIVED:
            global_data.game_mgr.show_tip(get_text_by_id(602011))
        else:
            x, y = btn.GetPosition()
            wpos = btn.GetParent().ConvertToWorldSpace(x, y)
            reward_id = task_utils.get_vitality_reward(lv)
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            global_data.emgr.show_reward_preview_event.emit(reward_list, wpos)
        return True

    def on_click_week_vitality(self, btn, touch, lv):
        reward_st = global_data.player.get_week_vitality_reward_status(lv)
        if reward_st == ITEM_UNRECEIVED:
            global_data.player.receive_week_vitality_reward(lv)
        elif reward_st == ITEM_RECEIVED:
            global_data.game_mgr.show_tip(get_text_by_id(602011))
        else:
            x, y = btn.GetPosition()
            wpos = btn.GetParent().ConvertToWorldSpace(x, y)
            reward_id = task_utils.get_week_vitality_reward(lv)
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            global_data.emgr.show_reward_preview_event.emit(reward_list, wpos)
        return True

    @post_ui_method
    def _on_update_day_vitality(self, *args):
        new_lv = global_data.player.get_vitality_lv()
        new_point = global_data.player.get_vitality_point()
        if self.nd_content:
            self.nd_content.nd_today.lab_liveness.SetString(str(new_point))
            max_level = task_utils.get_max_day_vitality_level()
            if new_lv >= max_level:
                self.nd_content.nd_progress.progress_timer.SetPercentage(100)
            else:
                percent = task_utils.get_vitality_prog_percent(new_lv)
                next_lv_percent = task_utils.get_vitality_prog_percent(new_lv + 1)
                next_lv_point = task_utils.get_vitality_point_by_level(new_lv + 1)
                if new_lv >= 1:
                    pre_lv_point = task_utils.get_vitality_point_by_level(new_lv)
                else:
                    pre_lv_point = 0
                extra_percent = (new_point - pre_lv_point) * (next_lv_percent - percent) / (next_lv_point - pre_lv_point)
                self.nd_content.nd_progress.progress_timer.SetPercentage(percent + extra_percent)

    @post_ui_method
    def _on_update_week_vitality(self, *args):
        self._updata_week_vitality_tips()
        new_point = global_data.player.get_week_vitality_point()
        if self.nd_content:
            self.nd_content.nd_week_liveness.lab_liveness.SetString(str(new_point))

    def _on_update_day_vitality_reward(self, lv, *args):
        reward_st = global_data.player.get_vitality_reward_status(lv)
        box_widget = self.day_vitality_box_widgets.get(lv, None)
        if box_widget:
            box_widget.update_reward_status(reward_st)
        return

    def _on_update_week_vitality_reward(self, lv, *args):
        self._updata_week_vitality_tips()
        reward_st = global_data.player.get_week_vitality_reward_status(lv)
        box_widget = self.week_vitality_box_widgets.get(lv, None)
        if box_widget:
            box_widget.update_reward_status(reward_st)
        return

    @post_ui_method
    def _updata_week_vitality_tips(self):
        if global_data.player.get_week_vitality_reward_status(1) == ITEM_UNRECEIVED and global_data.player.get_lv() >= 10:
            self.nd_content.nd_tips_vx.setVisible(True)
            self.nd_content.PlayAnimation('show_tips')
        else:
            self.nd_content.nd_tips_vx.setVisible(False)
            self.nd_content.StopAnimation('show_tips')

    @staticmethod
    def get_changed_day_tasks():
        return global_data.player.get_changed_day_tasks()

    @staticmethod
    def get_random_task_ids():
        return global_data.player.get_random_day_task_ids()

    @staticmethod
    def get_task_ids():
        return global_data.player.get_day_task_ids()

    def refresh_day_random_task(self, *args):
        if self.cur_tab_index == 0:
            return
        task_ids = self.get_random_task_ids()
        self.init_task_content(task_ids)

    def init_task_content(self, task_ids):
        player = global_data.player
        if not player:
            return
        self.task_ids = task_ids
        self.task_dict = {}
        self.ui_view_list.SetInitCount(0)
        index = 0
        self.sview_content_height = 0
        sview_height = self.ui_view_list.getContentSize().height
        while self.sview_content_height <= sview_height and index < len(self.task_ids):
            task_id = self.task_ids[index]
            nd_task_item = self.add_task_data(task_id)
            item_height = nd_task_item.getContentSize().height
            self.sview_content_height += item_height
            index += 1

        self.sview_index = index - 1
        self.add_list_view_check()

    def add_list_view_check(self):

        def scroll_callback(sender, eventType):
            if not self.is_check_sview:
                self.is_check_sview = True
                self.nd_content.SetTimeOut(0.033, self.check_sview)

        self.ui_view_list.addEventListener(scroll_callback)

    def check_sview(self):
        task_num = len(self.task_ids)
        self.sview_index = self.ui_view_list.AutoAddAndRemoveItem_MulCol(self.sview_index, self.task_ids, task_num, self.add_task_data, 300, 300, self.on_del_task_item)
        self.is_check_sview = False

    @staticmethod
    def check_task_tab_red_point--- This code section failed: ---

 329       0  BUILD_LIST_0          0 
           3  STORE_FAST            1  'task_ids'

 330       6  STORE_FAST            1  'task_ids'
           9  COMPARE_OP            2  '=='
          12  POP_JUMP_IF_FALSE    30  'to 30'

 331      15  LOAD_GLOBAL           0  'DayTaskWidget'
          18  LOAD_ATTR             1  'get_task_ids'
          21  CALL_FUNCTION_0       0 
          24  STORE_FAST            1  'task_ids'
          27  JUMP_FORWARD         12  'to 42'

 333      30  LOAD_GLOBAL           0  'DayTaskWidget'
          33  LOAD_ATTR             2  'get_random_task_ids'
          36  CALL_FUNCTION_0       0 
          39  STORE_FAST            1  'task_ids'
        42_0  COME_FROM                '27'

 334      42  SETUP_LOOP           42  'to 87'
          45  LOAD_FAST             1  'task_ids'
          48  GET_ITER         
          49  FOR_ITER             34  'to 86'
          52  STORE_FAST            2  'task_id'

 335      55  LOAD_GLOBAL           3  'global_data'
          58  LOAD_ATTR             4  'player'
          61  LOAD_ATTR             5  'get_task_reward_status'
          64  LOAD_FAST             2  'task_id'
          67  CALL_FUNCTION_1       1 
          70  LOAD_GLOBAL           6  'ITEM_UNRECEIVED'
          73  COMPARE_OP            2  '=='
          76  POP_JUMP_IF_FALSE    49  'to 49'

 336      79  LOAD_GLOBAL           7  'True'
          82  RETURN_END_IF    
        83_0  COME_FROM                '76'
          83  JUMP_BACK            49  'to 49'
          86  POP_BLOCK        
        87_0  COME_FROM                '42'

 337      87  LOAD_GLOBAL           8  'False'
          90  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_FAST' instruction at offset 6

    @staticmethod
    def check_red_point():
        for task_id in DayTaskWidget.get_task_ids():
            if global_data.player.get_task_reward_status(task_id) == ITEM_UNRECEIVED:
                return True

        for task_id in DayTaskWidget.get_random_task_ids():
            if global_data.player.get_task_reward_status(task_id) == ITEM_UNRECEIVED:
                return True

        max_vitality_level = task_utils.get_max_day_vitality_level()
        for lv in range(1, max_vitality_level + 1):
            reward_st = global_data.player.get_vitality_reward_status(lv)
            if reward_st == ITEM_UNRECEIVED:
                return True

        max_vitality_level = task_utils.get_max_week_vitality_level()
        for lv in range(1, max_vitality_level + 1):
            reward_st = global_data.player.get_week_vitality_reward_status(lv)
            if reward_st == ITEM_UNRECEIVED:
                return True

        return False

    def destroy(self):
        global_data.emgr.update_day_vitality_event -= self._on_update_day_vitality
        global_data.emgr.update_day_vitality_reward_event -= self._on_update_day_vitality_reward
        global_data.emgr.update_week_vitality_event -= self._on_update_week_vitality
        global_data.emgr.update_week_vitality_reward_event -= self._on_update_week_vitality_reward
        global_data.emgr.update_day_vitality_event -= self._refresh_get_all_btn
        global_data.emgr.update_day_vitality_reward_event -= self._refresh_get_all_btn
        global_data.emgr.update_week_vitality_event -= self._refresh_get_all_btn
        global_data.emgr.update_week_vitality_reward_event -= self._refresh_get_all_btn
        global_data.emgr.task_prog_changed -= self._refresh_get_all_btn
        global_data.emgr.receive_task_reward_succ_event -= self._refresh_get_all_btn
        global_data.emgr.refresh_day_random_task -= self.refresh_day_random_task
        super(DayTaskWidget, self).destroy()