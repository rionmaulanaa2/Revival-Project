# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/ActivitySummerConcertWarmup.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name, exec_jump_to_ui_info
from common.cfg import confmgr
from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED
import cc
from common.utils.timer import CLOCK
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_use_parms, get_lobby_item_name
from logic.gutils import activity_utils
from logic.comsys.activity.widget.GlobalAchievementWidget import GlobalAchievementWidget
from logic.comsys.activity.ActivityCollectNew import ActivityCollectNew
from common.const.uiconst import NORMAL_LAYER_ZORDER_3
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils import template_utils
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from logic.gcommon import time_utility as tutil
from logic.gutils.new_template_utils import update_task_list_btn

class PickStarTarget(object):

    def __init__(self, parent, parent_target, sub_target_list, task_finish_time):
        self.parent_target = parent_target
        self.sub_target_list = sub_target_list
        self.task_finish_time = task_finish_time
        self.panel = global_data.uisystem.load_template_create('activity/activity_202208/music/i_music_page_1', parent=parent)
        self.choose_callback = None
        self.on_init_panel()
        return

    def init_btn(self):
        if self.panel.btn_question:

            @self.panel.btn_question.callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(83191), get_text_by_id(83193))

    def set_choose_callback(self, callback):
        self.choose_callback = callback

    def on_init_panel(self):
        self._cur_touch_index = None
        self.touch_count = len(self.sub_target_list)
        for i in range(self.touch_count):
            touch_nd = getattr(self.panel, 'nd_touch_%d' % i)

            @touch_nd.callback()
            def OnClick(btn, touch, touch_idx=i):
                self.on_click_touch_nd(btn, touch, touch_idx)

        @self.panel.btn_pick.callback()
        def OnClick(btn, touch):
            cur_time = tutil.get_server_time()
            if self.task_finish_time < cur_time:
                global_data.game_mgr.show_tip(get_text_by_id(83195))
                return
            else:
                if self._cur_touch_index is None:
                    return
                sub_target = self.sub_target_list[self._cur_touch_index]
                if global_data.player:
                    global_data.player.choose_global_achive(self.parent_target, sub_target)
                if self.choose_callback:
                    self.choose_callback()
                return

        self.init_btn()
        return

    def on_click_touch_nd(self, btn, touch, touch_idx):
        if touch_idx == self._cur_touch_index:
            return
        self.set_choose_node(self._cur_touch_index, False)
        self._cur_touch_index = touch_idx
        self.set_choose_node(self._cur_touch_index, True)

    def set_choose_node(self, touch_idx, is_choose):
        if touch_idx is None:
            return
        else:
            tips_nd = getattr(self.panel, 'nd_tips_%d' % touch_idx)
            if tips_nd:
                tips_nd.setVisible(is_choose)
            img_nd = getattr(self.panel, 'img_team_%d' % touch_idx)
            if not img_nd:
                return
            if not is_choose:
                img_path = 'gui/ui_res_2/activity/activity_202208/music/page_1/btn_concert_%d_0.png' % touch_idx
                img_nd.SetDisplayFrameByPath('', img_path)
            else:
                img_path = 'gui/ui_res_2/activity/activity_202208/music/page_1/btn_concert_%d_2.png' % touch_idx
                img_nd.SetDisplayFrameByPath('', img_path)
            return

    def destroy(self):
        self.choose_callback = None
        self.parent_target = None
        self.sub_target_list = []
        if self.panel:
            self.panel.Destroy()
            self.panel = None
        return


class StarGlobalHeatValue(GlobalAchievementWidget):

    def on_init_panel(self):
        self.achieve_name = self.extra_conf.get('achieve_name', '')
        super(StarGlobalHeatValue, self).on_init_panel()

    def init_parameters(self):
        self.children_ids = confmgr.get('c_activity_config', self.activity_id, 'cUiData', 'global_achieve_id', default=[])
        first_id = self.children_ids[0]
        self.parent_id = str(confmgr.get('global_achieve_data', first_id, 'cParentID', default=first_id))
        if not self.achieve_name:
            self.achieve_name = confmgr.get('global_achieve_data', first_id, 'cGStatName', default='share')
        self.share_prog = [ confmgr.get('global_achieve_data', aid, 'iCondValue') for aid in self.children_ids ]
        self.server_num = 0
        self.local_num = 0
        self.increase_num = 0
        self._times = 0
        self._timer = None
        self._is_first_open = True
        return

    def refresh_reward_content(self, *args):
        pass

    def update_progress(self):
        if self.local_num is not None:
            if global_data.player:
                global_data.player.set_simulate_cache(self.achieve_name, self.local_num)
        self.panel.lab_value.SetString(str(self.local_num))
        return


class HeatValueRankPanel(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202208/music/open_music_rank'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    GLOBAL_EVENT = {'message_update_global_reward_receive': 'refresh_reward_content'
       }

    def on_init_panel(self):
        super(HeatValueRankPanel, self).on_init_panel()
        self.parent_id = None
        self.achive_name_dict = {}
        self.reward_list = []
        self.task_finish_time = 0

        @self.panel.btn_close.callback()
        def OnClick(btn, touch):
            self.close()

        return

    def set_rank_achive(self, parent_id, achive_name_dic, reward_list, task_finish_time):
        self.parent_id = parent_id
        self.achive_name_dict = achive_name_dic
        self.reward_list = reward_list
        self.task_finish_time = task_finish_time
        self.children_achieves = sorted(activity_utils.get_child_achieves_from_parent(self.parent_id))
        self.my_chose_achive_id = global_data.player.get_chose_sub_of_global_achive(self.parent_id)
        self.on_update_parent_achive()

    def on_update_parent_achive(self):
        global_stat_data = global_data.player or None if 1 else global_data.player.get_global_stat_data()
        if global_stat_data is None:
            return
        else:
            self.achive_nums = {}
            if self.task_finish_time > tutil.get_server_time():
                chose_a_name = confmgr.get('global_achieve_data', str(self.my_chose_achive_id), 'cGStatName', default='share')
                chose_a_num = global_stat_data.get(self.parent_id, {}).get(chose_a_name, 0)
                diff = chose_a_num - global_data.player.get_simulate_cache(chose_a_name)
            else:
                diff = 0
            for aid in self.children_achieves:
                a_name = confmgr.get('global_achieve_data', str(aid), 'cGStatName', default='share')
                a_num = global_stat_data.get(self.parent_id, {}).get(a_name, 0)
                self.achive_nums[aid] = max(a_num - diff, 0)

            rank_list = []
            achive_ids = sorted(six_ex.keys(self.achive_nums), key=lambda x: [self.achive_nums[x], x], reverse=True)
            for a_id in achive_ids:
                rank_list.append([a_id, self.achive_name_dict.get(str(a_id), ''), self.achive_nums[a_id], a_id == self.my_chose_achive_id])

            self.set_rank_content(rank_list, achive_ids)
            return

    def set_rank_content(self, all_rank_data, rank_child_achive_ids):
        self.all_rank_data = all_rank_data
        self.rank_child_achive_ids = rank_child_achive_ids
        if not self.reward_list:
            log_error('reward_list is not setted!', self.reward_list)
            return
        self.panel.list_item.SetInitCount(len(all_rank_data))
        all_items = self.panel.list_item.GetAllItem()
        for i, ui_item in enumerate(all_items):
            rank_data = all_rank_data[i]
            self.init_rank_item(ui_item, rank_data, i)

        self.refresh_reward_content()

    def init_rank_item(self, rank_ui_item, rank_data, index):
        rank_ui_item.lab_rank.SetString(str(index + 1))
        rank_ui_item.lab_team.SetString(rank_data[1])
        rank_ui_item.lab_integral.SetString(str(rank_data[2]))
        rank_ui_item.bar_mine.setVisible(rank_data[3])

    def on_finalize_panel(self):
        pass

    def refresh_reward_content(self, *args):
        from common.cfg import confmgr
        from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN

        def init_reward_item(item, achieve_id, item_no, item_num):
            if achieve_id != self.my_chose_achive_id:
                status = ITEM_UNGAIN
            else:
                status = global_data.player.get_gl_reward_receive_state(achieve_id)
            if status == ITEM_UNRECEIVED:
                show_tips = False
                callback = lambda achieve_id=achieve_id: global_data.player.try_get_global_achieve(achieve_id)
            else:
                show_tips = True
                callback = None
            init_tempate_mall_i_item(item, item_no, item_num, show_tips=show_tips, callback=callback)
            if self.task_finish_time > tutil.get_server_time():
                status = ITEM_UNGAIN
            if status == ITEM_UNGAIN:
                pass
            elif status == ITEM_UNRECEIVED:
                item.PlayAnimation('get_tips')
            elif status == ITEM_RECEIVED:
                item.StopAnimation('get_tips')
                item.nd_get_tips.setVisible(False)
                item.nd_get.setVisible(True)
                item.nd_lock.setVisible(True)
            return

        n = len(self.reward_list)
        for i in range(n):
            reward_id = self.reward_list[i]
            achieve_id = self.rank_child_achive_ids[i]
            nd_list = self.panel.list_item.GetItem(i).list_reward
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            if not reward_conf:
                nd_list.DeleteAllSubItem()
                log_error('reward_id is not exist in common_reward_data', reward_id)
                return
            reward_list = reward_conf.get('reward_list', [])
            reward_count = len(reward_list)
            nd_list.SetInitCount(reward_count)
            for idx in range(reward_count):
                item_no, item_num = reward_list[idx]
                reward_item = nd_list.GetItem(idx)
                init_reward_item(reward_item, achieve_id, item_no, item_num)

        if self.my_chose_achive_id is not None:
            status = global_data.player.get_gl_reward_receive_state(self.my_chose_achive_id)
            if self.task_finish_time < tutil.get_server_time():
                self.panel.temp_btn_1.setVisible(True)
                self.panel.lab_tips.setVisible(False)
                if status == ITEM_UNRECEIVED:
                    self.panel.temp_btn_1.btn_common.SetText(80930)
                    self.panel.temp_btn_1.btn_common.SetEnable(True)

                    @self.panel.temp_btn_1.btn_common.callback()
                    def OnClick(btn, touch):
                        global_data.player.try_get_global_achieve(self.my_chose_achive_id)

                else:
                    self.panel.temp_btn_1.btn_common.SetText(80866)
                    self.panel.temp_btn_1.btn_common.SetEnable(False)
            else:
                self.panel.temp_btn_1.setVisible(False)
                self.panel.lab_tips.setVisible(True)
        return


class ActivitySummerConcertWarmup(ActivityCollectNew):

    def __init__(self, dlg, activity_type):
        super(ActivityCollectNew, self).__init__(dlg, activity_type)
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self.ui_data = self.activity_conf.get('cUiData')
        self.fixed_task_id = self.ui_data.get('task_id')
        self.random_task_id = None
        return

    def on_init_panel(self):
        children_ids = self.ui_data.get('global_achieve_id', [])
        first_id = children_ids[0]
        self.parent_achieve_id = str(confmgr.get('global_achieve_data', first_id, 'cParentID', default=first_id))
        self.widget_map = {}
        self.children_achieves = sorted(activity_utils.get_child_achieves_from_parent(self.parent_achieve_id))
        self.my_chose_achive_id = global_data.player.get_chose_sub_of_global_achive(self.parent_achieve_id)
        self.pick_target_ui = None
        self.task_finish_time = self.ui_data.get('task_finish_time', 0)
        self.achive_name = ''
        if self.my_chose_achive_id is None:
            self.pick_target_ui = PickStarTarget(self.panel.GetParent(), self.parent_achieve_id, self.children_achieves, self.task_finish_time)
            self.pick_target_ui.set_choose_callback(self.on_finish_choose)
        else:
            self.update_img_team()
        self.init_countdown_widget()
        self.act_list = self.panel.act_list
        self.show_list()
        self.panel.btn_rank.temp_red.setVisible(ActivitySummerConcertWarmup.show_rank_reward_rp(self._activity_type))

        @self.panel.btn_rank.callback()
        def OnClick(btn, touch):
            team_name = self.ui_data.get('team_name', {})
            rank_rewards = self.ui_data.get('rank_rewards', [])
            task_finish_time = self.ui_data.get('task_finish_time', 0)
            ui = HeatValueRankPanel()
            ui.set_rank_achive(self.parent_achieve_id, team_name, rank_rewards, task_finish_time)

        self.init_btn()
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')
        if self.panel.HasAnimation('loop'):
            self.panel.PlayAnimation('loop')
        return

    def on_finish_choose(self):
        self.my_chose_achive_id = global_data.player.get_chose_sub_of_global_achive(self.parent_achieve_id)
        if self.pick_target_ui:
            self.pick_target_ui.destroy()
            self.pick_target_ui = None
        self.update_img_team()
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')
        if self.panel.HasAnimation('loop'):
            self.panel.PlayAnimation('loop')
        return

    def update_img_team(self):
        if self.my_chose_achive_id in self.children_achieves:
            index = self.children_achieves.index(self.my_chose_achive_id)
            img_path = 'gui/ui_res_2/activity/activity_202208/music/page_2/img_concer_driver_%s.png' % index
            self.panel.img_team.SetDisplayFrameByPath('', img_path)
        self.achive_name = confmgr.get('global_achieve_data', str(self.my_chose_achive_id), 'cGStatName', default='share')
        self.init_global_achieve_widget()

    def init_global_achieve_widget(self):
        extra_info = {'need_sim': True if self.task_finish_time > tutil.get_server_time() else False,
           'sim_interval': 60,
           'achieve_name': self.achive_name
           }
        self.widget_map['global_achieve'] = StarGlobalHeatValue(self.panel.bar_value, self._activity_type, extra_info)

    def init_countdown_widget(self):
        from logic.comsys.activity.widget.CountdownWidget import CountdownWidget
        self.widget_map['countdown'] = CountdownWidget(self.panel.lab_tips_time, self._activity_type)

    def refresh_list(self):
        player = global_data.player
        if not player:
            return
        if not self.act_list:
            log_error('Activity %s dont indicate task list node!', self.__class__.__name__)
            return
        for idx, task_id in enumerate(self._children_tasks):
            item_widget = self.act_list.GetItem(idx).temp_common
            total_times = task_utils.get_total_prog(task_id)
            cur_times = player.get_task_prog(task_id)
            self._set_item_widget_lab_num(item_widget, total_times, cur_times)
            update_task_list_btn(item_widget.nd_task.temp_btn_get, self.get_receive_btn_status(task_id))

            @item_widget.nd_task.temp_btn_get.btn_common.unique_callback()
            def OnClick(btn, touch, _task_id=task_id):
                self.on_click_receive_btn(_task_id)

    def get_receive_btn_status(self, task_id):
        from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_GO, BTN_ST_OVERDUE
        task_finish_time = self.ui_data.get('task_finish_time')
        cur_time = tutil.get_server_time()
        if cur_time > task_finish_time:
            return BTN_ST_OVERDUE
        status = global_data.player.get_task_reward_status(task_id)
        if status == ITEM_RECEIVED:
            return BTN_ST_RECEIVED
        if status == ITEM_UNGAIN:
            jump_conf = task_utils.get_jump_conf(task_id)
            if jump_conf:
                return BTN_ST_GO
            else:
                return BTN_ST_ONGOING

        elif status == ITEM_UNRECEIVED:
            return BTN_ST_CAN_RECEIVE

    def init_btn(self):
        if self.panel.btn_question:

            @self.panel.btn_question.callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(self.activity_conf['cNameTextID']), get_text_by_id(self.activity_conf['cRuleTextID']))

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'message_update_global_reward_receive': self.refresh_red_point,
           'task_prog_changed': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    @staticmethod
    def show_choose_rp(activity_id):
        activity_conf = confmgr.get('c_activity_config', activity_id)
        ui_data = activity_conf.get('cUiData')
        task_finish_time = ui_data.get('task_finish_time')
        cur_time = tutil.get_server_time()
        if task_finish_time < cur_time:
            return False
        else:
            children_ids = ui_data.get('global_achieve_id', [])
            first_id = children_ids[0]
            parent_achieve_id = str(confmgr.get('global_achieve_data', first_id, 'cParentID', default=first_id))
            my_chose_achive_id = global_data.player.get_chose_sub_of_global_achive(parent_achieve_id)
            return my_chose_achive_id is None

    @staticmethod
    def show_task_rp(activity_id):
        from logic.gutils.activity_utils import can_receive_task_reward
        activity_conf = confmgr.get('c_activity_config', activity_id)
        ui_data = activity_conf.get('cUiData')
        task_id = ui_data.get('task_id')
        show = can_receive_task_reward(task_id)
        return show

    @staticmethod
    def show_rank_reward_rp(activity_id):
        if not global_data.player:
            return False
        else:
            activity_conf = confmgr.get('c_activity_config', activity_id)
            ui_data = activity_conf.get('cUiData')
            children_ids = ui_data.get('global_achieve_id', [])
            first_id = children_ids[0]
            parent_achieve_id = str(confmgr.get('global_achieve_data', first_id, 'cParentID', default=first_id))
            my_chose_achive_id = global_data.player.get_chose_sub_of_global_achive(parent_achieve_id)
            task_finish_time = ui_data.get('task_finish_time')
            cur_time = tutil.get_server_time()
            if cur_time > task_finish_time and my_chose_achive_id is not None:
                status = global_data.player.get_gl_reward_receive_state(my_chose_achive_id)
                if status == ITEM_UNRECEIVED:
                    return True
            return False

    @staticmethod
    def show_tab_rp(activity_id):
        if ActivitySummerConcertWarmup.show_choose_rp(activity_id):
            return True
        if ActivitySummerConcertWarmup.show_task_rp(activity_id):
            return True
        if ActivitySummerConcertWarmup.show_rank_reward_rp(activity_id):
            return True
        return False

    def on_finalize_panel(self):
        super(ActivitySummerConcertWarmup, self).on_finalize_panel()
        if self.pick_target_ui:
            self.pick_target_ui.destroy()
            self.pick_target_ui = None
        for widget in six_ex.values(self.widget_map):
            widget.on_finalize_panel()

        self.widget_map = None
        return

    def refresh_red_point(self):
        self.panel.btn_rank.temp_red.setVisible(ActivitySummerConcertWarmup.show_rank_reward_rp(self._activity_type))
        global_data.emgr.refresh_activity_redpoint.emit()