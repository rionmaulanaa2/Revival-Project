# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanTaskBase.py
from __future__ import absolute_import
import six
from six.moves import range
from functools import cmp_to_key
from logic.comsys.task.CommonTaskWidget import CommonTaskWidget
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gcommon.cdata import clan_point_reward_conf
from logic.gutils.new_template_utils import VitalityBoxReward

class ClanTaskBase(CommonTaskWidget):

    def __init__(self, parent, panel, task_type, auto_sort=True, dlg=None):
        super(ClanTaskBase, self).__init__(parent, panel, task_type, False)
        if dlg:
            self.nd_content = dlg
        self.day_vitality_box_widgets = {}
        self.week_vitality_box_widgets = {}

    def on_init_panel(self):
        self.init_task_event()
        self._init_get_all()
        self.panel.PlayAnimation('show')

    def destroy(self):
        super(ClanTaskBase, self).destroy()
        global_data.emgr.player_info_update_event -= self.on_refresh_content
        global_data.emgr.clan_task_day_reward -= self.on_refresh_content
        global_data.emgr.clan_task_week_reward -= self.on_refresh_content

    def init_task_event(self):
        global_data.emgr.player_info_update_event += self.on_refresh_content
        global_data.emgr.clan_task_day_reward += self.on_refresh_content
        global_data.emgr.clan_task_week_reward += self.on_refresh_content

    def init_widget(self, need_hide=True):
        super(ClanTaskBase, self).init_widget(need_hide)
        self.on_refresh_content()

    def on_refresh_content(self, *args):
        self._on_task_update()
        self.init_task_content()
        self.init_day_vitality()
        self.init_week_vitality()

    def init_day_vitality(self):
        new_point = global_data.player.get_day_clan_point()
        if self.nd_content:
            self.nd_content.nd_today.lab_liveness.SetString(str(new_point))

    def init_week_vitality(self):
        max_vitality_level = clan_point_reward_conf.get_week_vitality_count()
        for lv in range(1, max_vitality_level + 1):
            vitality_point = clan_point_reward_conf.get_week_reward_point(lv)
            nd_reward = getattr(self.nd_content, 'nd_reward_' + str(lv))
            if not nd_reward:
                continue
            box_widget = self.week_vitality_box_widgets.get(lv, None)
            if not box_widget:
                box_widget = VitalityBoxReward(nd_reward, lv, self.on_click_week_vitality)
                nd_reward.lab_liveness.SetString(str(vitality_point))
                self.week_vitality_box_widgets[lv] = box_widget
            box_widget.update_vitality_point(vitality_point)
            reward_st = global_data.player.get_week_clan_reward_st(lv)
            box_widget.update_reward_status(reward_st, show_get_img=False)

        self._on_update_week_vitality()
        return

    def on_click_week_vitality(self, btn, touch, lv):
        reward_st = global_data.player.get_week_clan_reward_st(lv)
        if reward_st == ITEM_UNRECEIVED:
            global_data.player.receive_week_clan_point_reward(lv)
        elif reward_st == ITEM_RECEIVED:
            global_data.game_mgr.show_tip(get_text_by_id(602011))
        else:
            x, y = btn.GetPosition()
            wpos = btn.GetParent().ConvertToWorldSpace(x, y)
            reward_id = clan_point_reward_conf.get_week_reward_id(lv)
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            global_data.emgr.show_reward_preview_event.emit(reward_list, wpos)
        return True

    def _on_update_week_vitality(self, *args):
        new_point = global_data.player.get_week_clan_point()
        if self.nd_content:
            self.nd_content.nd_week_liveness.lab_liveness.SetString(str(new_point))

    def get_task_ids(self, extra_data=None):
        task_ids = []
        for task_id, conf in six.iteritems(confmgr.get('task/clan_task_data')):
            if not conf.get('need_hide', 0):
                task_ids.append(task_id)

        return task_ids

    def init_task_content(self):
        from logic.gutils import clan_utils
        player = global_data.player
        if not player:
            return
        if not self.ui_view_list:
            return
        self.task_ids = clan_utils.get_clan_task_ids()
        self.task_ids.sort(key=cmp_to_key(task_utils.sort_task_func))
        self.task_dict = {}
        self.ui_view_list.DeleteAllSubItem()
        index = 0
        self.sview_content_height = 0
        sview_height = self.ui_view_list.getContentSize().height
        while self.sview_content_height < sview_height and index < len(self.task_ids):
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

    def _init_get_all(self):

        @self.panel.temp_get_all.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            can_receive_task = self._get_all_receivable_tasks()
            for task_id in can_receive_task:
                global_data.player.receive_task_reward(task_id)

            can_receivable_lv_lst = self._get_week_receivable_lv()
            for lv in can_receivable_lv_lst:
                global_data.player.receive_week_clan_point_reward(lv)

    def _on_task_update(self, *args):
        can_receive_task = self._get_all_receivable_tasks()
        can_receivable_lv_lst = self._get_week_receivable_lv()
        can_receive = True if can_receive_task or can_receivable_lv_lst else False
        self.panel.temp_get_all.setVisible(can_receive)
        self.panel.pnl_get_all.setVisible(can_receive)

    def _get_week_receivable_lv(self):
        max_vitality_level = clan_point_reward_conf.get_week_vitality_count()
        can_receivable_lv_lst = []
        for lv in range(1, max_vitality_level + 1):
            reward_st = global_data.player.get_week_clan_reward_st(lv)
            if reward_st == ITEM_UNRECEIVED:
                can_receivable_lv_lst.append(lv)

        return can_receivable_lv_lst

    def _get_all_receivable_tasks(self):
        if not self.task_ids:
            from logic.gutils import clan_utils
            self.task_ids = clan_utils.get_clan_task_ids()
        can_receive_task = []
        for task_id in self.task_ids:
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                can_receive_task.append(task_id)

        return can_receive_task