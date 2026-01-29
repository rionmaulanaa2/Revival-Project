# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNile/ActivityBingoLianliankan.py
from __future__ import absolute_import
from six.moves import range
from logic.gutils.task_utils import get_task_fresh_type, get_task_name, get_total_prog, get_jump_conf, get_children_task
from logic.gutils.item_utils import get_lobby_item_name, exec_jump_to_ui_info, get_lobby_item_type, get_lobby_item_reward_id
from common.cfg import confmgr
from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED
import cc
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.template_utils import init_tempate_mall_i_item, get_reward_list_by_reward_id
from logic.comsys.activity.ActivityNile.ActivityBingoLlkLeftRewardWidget import ActivityBingoLlkLeftRewardWidget
from logic.gutils import activity_utils
import six_ex
from logic.gutils import task_utils
from logic.gutils import item_utils
from logic.gcommon.common_const.activity_const import SUMMER_COCONUT_COLUMN
VER_LINE = 0
HOR_LINE = 1
LEAN_LINE = 2
DIRECTIONAL_REWARD_COUNT = 4
from logic.comsys.activity.ActivityTemplate import ActivityTemplate

class ActivityBingoLianliankan(ActivityTemplate):

    def on_init_panel(self):
        self.widget_map = {}
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        ui_data = self.activity_conf.get('cUiData')
        self.SLOT_OPEN_ITEM_NO = ui_data.get('SLOT_OPEN_ITEM_NO', 71600028)
        self.reward_list = ui_data.get('gift_list', [])
        icon_dict = {'1451644': 'gui/ui_res_2/activity/activity_202303/square_lianliankan/icon_square_hp_blue.png',
           '1451638': 'gui/ui_res_2/activity/activity_202303/square_lianliankan/icon_square_helmet_blue.png',
           '1451645': 'gui/ui_res_2/activity/activity_202303/square_lianliankan/icon_square_txt_blue.png',
           '1451640': 'gui/ui_res_2/activity/activity_202303/square_lianliankan/icon_square_date_blue.png',
           '1451643': 'gui/ui_res_2/activity/activity_202303/square_lianliankan/icon_square_txt_blue.png',
           '1451639': 'gui/ui_res_2/activity/activity_202303/square_lianliankan/icon_square_chat_blue.png',
           '1451641': 'gui/ui_res_2/activity/activity_202303/square_lianliankan/icon_square_mecha_blue.png',
           '1451642': 'gui/ui_res_2/activity/activity_202303/square_lianliankan/icon_square_vehicle_blue.png',
           '1451646': 'gui/ui_res_2/activity/activity_202303/square_lianliankan/icon_square_txt_blue.png'
           }
        self._task_icon_dict = ui_data.get('task_icon_dict', icon_dict)
        self.chip_item_id = ui_data['chip_item_id']
        task = self.activity_conf.get('cTask')
        self._cTask = task
        _task_list = get_children_task(task)
        if len(_task_list) != 16:
            if global_data.is_inner_server:
                global_data.uisystem.post_wizard_trace_inner_server('\xe4\xbb\xbb\xe5\x8a\xa1\xe4\xb8\xaa\xe6\x95\xb0\xe6\x9c\x89\xe8\xaf\xaf' + str(_task_list))
        other_task_list = _task_list[0:9]
        login_task_list = _task_list[9:16]
        self._task_list = []
        self._task_list.append(login_task_list[0])
        self._task_list.extend(other_task_list[0:3])
        self._task_list.append(login_task_list[1])
        self._task_list.extend(other_task_list[3:6])
        self._task_list.append(login_task_list[2])
        self._task_list.extend(other_task_list[6:9])
        self._task_list.extend(login_task_list[3:])
        self.other_task_list = other_task_list
        self.login_task_list = login_task_list
        self.left_panel_widget = ActivityBingoLlkLeftRewardWidget(self.panel, self._activity_type)
        self.update_reward_cell_map()
        self.update_cup_count()
        self.panel.list_item.DeleteAllSubItem()
        self.panel.list_item.BindMethod('OnCreateItem', self.create_connect_item)
        self.panel.list_item.SetInitCount(len(self._task_list))
        self.panel.list_item.scroll_Load()
        self.cup_count = global_data.player.get_item_num_by_no(self.chip_item_id)
        self.xian_01_init_pos = self.panel.vx_xian_01.GetPosition()
        self.xian_02_init_pos = self.panel.vx_xian_02.GetPosition()
        global_data.llk = self
        self.init_coconut_rewards()
        self.init_countdown_widget()
        self._update_get_all_reward()

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cDescTextID']))

        self.play_show_animation()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_new_cell_unlock': self.on_cell_unlocked,
           'receive_coconut_reward': self.receive_coconut_reward,
           'on_lobby_bag_item_changed_event': self.on_item_received,
           'receive_task_reward_succ_event': self.receive_task_reward_succ
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        super(ActivityBingoLianliankan, self).on_finalize_panel()
        for widget in six_ex.values(self.widget_map):
            widget.on_finalize_panel()

        self.widget_map = None
        if self.left_panel_widget:
            self.left_panel_widget.on_finalize_panel()
            self.left_panel_widget = None
        global_data.ui_mgr.close_ui('ActivityBingoLianliankanTaskPanelUI')
        return

    def init_countdown_widget(self):
        from logic.gcommon.time_utility import get_day_hour_minute_second

        def text_cb(left_time):
            days, hours, minutes, second = get_day_hour_minute_second(left_time)
            return get_text_by_id(634313, [str(days), '%02.0f' % hours, '%02.0f' % minutes])

        from logic.comsys.activity.widget.CountdownWidget import CountdownWidget
        self.widget_map['countdown'] = CountdownWidget(self.panel.lab_tips_time, self._activity_type, {'txt_cb': text_cb})

    def update_cup_count(self):
        self.cup_count = global_data.player.get_item_num_by_no(self.chip_item_id)
        self.panel.lab_num.SetString(get_text_by_id(610751, (str(self.cup_count),)))

    def on_item_received(self):
        self.update_cup_count()
        self._update_get_all_reward()

    def play_show_animation(self):
        act = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show'))]
        self.panel.runAction(cc.Sequence.create(act))

    def create_connect_item(self, lv, idx, item):
        item.btn_click.EnableCustomState(True)
        item.btn_click.BindMethod('OnClick', lambda btn, touch, i=idx: self.on_click_item_by_idx(i))
        self.update_task_item_by_idx(idx)

    def on_click_item_by_idx(self, idx):
        from logic.comsys.activity.ActivityNile.ActivityBingoLianliankanTaskPanelUI import ActivityBingoLianliankanTaskPanelUI
        _task_panel = ActivityBingoLianliankanTaskPanelUI()
        _task_panel.update_task_id(self, self._task_list[idx])
        reward_btn = self.panel.list_item.GetItem(idx)
        wcenter_pos = reward_btn.ConvertToWorldSpacePercentage(50, 50)
        _task_panel.set_position(self.panel, wcenter_pos)
        _task_panel.show_panel()

    def get_item_state(self, idx):
        status = global_data.player.get_task_reward_status(self._task_list[idx])
        if status == ITEM_UNGAIN:
            return STATE_DISABLED
        if status == ITEM_UNRECEIVED:
            return STATE_NORMAL
        if status == ITEM_RECEIVED:
            return STATE_SELECTED

    def connect_line(self, dir, idx, play_anim=False):
        if dir == VER_LINE:
            step = DIRECTIONAL_REWARD_COUNT
            start_idx = idx
            img_name = 'img_5'
            self.panel.vx_xian_01.SetPosition(self.xian_01_init_pos[0] - 90 * (DIRECTIONAL_REWARD_COUNT - idx - 1), self.xian_01_init_pos[1])
            anim_name_1 = 'appear_01'
        elif dir == HOR_LINE:
            step = 1
            start_idx = idx * DIRECTIONAL_REWARD_COUNT
            img_name = 'img_3'
            self.panel.vx_xian_02.SetPosition(self.xian_02_init_pos[0], self.xian_02_init_pos[1] - 90 * idx)
            anim_name_1 = 'appear_02'
        else:
            step = DIRECTIONAL_REWARD_COUNT + 1
            start_idx = 0
            img_name = 'img_4'
            anim_name_1 = 'appear_03'
        if play_anim:
            self.panel.runAction(cc.Sequence.create([
             cc.CallFunc.create(lambda : self.panel.PlayAnimation(anim_name_1))]))

    def update_reward_cell_map(self):
        self._unrewarded_cell_map = list(range(len(self._task_list)))
        for idx in range(len(self._task_list)):
            task_id = self._task_list[idx]
            has_received = global_data.player.has_receive_reward(task_id)
            if has_received:
                self._unrewarded_cell_map.remove(idx)

        set_unreward_cell_map = set(self._unrewarded_cell_map)
        set_locked_coconut_map = set(global_data.player.locked_coconut_map)
        if set_unreward_cell_map != set_locked_coconut_map:
            if global_data.is_inner_server:
                global_data.uisystem.post_wizard_trace_inner_server('\xe6\x9c\xac\xe7\x95\x8c\xe9\x9d\xa2\xe6\xb2\xa1\xe6\x9c\x89\xe6\x89\x93\xe5\xbc\x80\xe5\xad\x94\xe7\x9a\x84\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x92\x8ccoconut map\xe4\xb9\x8b\xe9\x97\xb4\xe4\xb8\x8d\xe4\xb8\x80\xe8\x87\xb4\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5')
            log_error('\xe6\x9c\xac\xe7\x95\x8c\xe9\x9d\xa2\xe6\xb2\xa1\xe6\x9c\x89\xe6\x89\x93\xe5\xbc\x80\xe5\xad\x94\xe7\x9a\x84\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x92\x8ccoconut map\xe4\xb9\x8b\xe9\x97\xb4\xe4\xb8\x8d\xe4\xb8\x80\xe8\x87\xb4\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5', set_unreward_cell_map, set_locked_coconut_map, self._task_list)
        for idx in set_locked_coconut_map - set_unreward_cell_map:
            global_data.player.unlock_coconut_map(int(idx / DIRECTIONAL_REWARD_COUNT), int(idx % DIRECTIONAL_REWARD_COUNT))

    def on_cell_unlocked(self, idx):
        if idx >= self.panel.list_item.GetItemCount():
            return
        else:
            item = self.panel.list_item.GetItem(idx)
            if item is None:
                return
            item.StopAnimation('loop')
            self.update_cup_count()
            self.update_line_connected_reward()
            row_start = idx - idx % SUMMER_COCONUT_COLUMN
            col_start = idx % SUMMER_COCONUT_COLUMN
            lean_start = 0 if idx in (0, 5, 10, 15) else None
            row_complete = True
            col_complete = True
            lean_complete = lean_start is not None
            for i in range(SUMMER_COCONUT_COLUMN):
                if row_complete and row_start + i in global_data.player.locked_coconut_map:
                    row_complete = False
                if col_complete and col_start + i * SUMMER_COCONUT_COLUMN in global_data.player.locked_coconut_map:
                    col_complete = False
                if lean_complete and lean_start + i * (SUMMER_COCONUT_COLUMN + 1) in global_data.player.locked_coconut_map:
                    lean_complete = False

            if row_complete:
                self.connect_line(HOR_LINE, int(idx / SUMMER_COCONUT_COLUMN), True)
            if col_complete:
                self.connect_line(VER_LINE, int(idx % SUMMER_COCONUT_COLUMN), True)
            if lean_complete:
                self.connect_line(LEAN_LINE, 0, True)
            return

    def update_task_item_by_idx(self, idx):
        item = self.panel.list_item.GetItem(idx)
        if not item:
            return
        btn = item.btn_click
        btn_state = self.get_item_state(idx)
        btn.SetEnable(btn_state == STATE_NORMAL or btn_state == STATE_DISABLED)
        item.nd_got.setVisible(False)
        if btn_state == STATE_NORMAL:
            item.PlayAnimation('loop')
            item.vx_mask_01.setVisible(False)
            item.nd_reward.setVisible(True)
            item.nd_info.setVisible(False)
        elif btn_state == STATE_DISABLED:
            item.StopAnimation('loop')
            item.nd_reward.setVisible(False)
            item.nd_got.setVisible(True)
            item.nd_info.setVisible(True)
        else:
            item.StopAnimation('loop')
            item.vx_mask_01.setVisible(False)
            item.nd_reward.setVisible(False)
            item.nd_info.setVisible(True)
        btn._updateCurState(btn_state)
        task_id = self._task_list[idx]
        if task_id in self.login_task_list:
            item.lab_date.SetString(str(self.login_task_list.index(task_id) + 1))
        else:
            pic = self._task_icon_dict.get(str(task_id), '')
            if pic:
                if btn_state == STATE_SELECTED:
                    pic = pic.replace('_blue.png', '_red.png')
                item.nd_info.icon.SetDisplayFrameByPath('', pic)
            total_times = task_utils.get_total_prog(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            progress_txt = str('%s/%s' % (cur_times, total_times))
            item.lab_prog.SetString(progress_txt)
        if task_id:
            reward_list = task_utils.get_task_reward_list(task_id)
            reward_item_no, item_num = reward_list[0]
            from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_use_parms
            item.nd_reward.item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(reward_item_no))
            item.nd_reward.lab_quantity.SetString(str(item_num))

    def update_task_list_reward(self):
        for idx in range(self.panel.list_item.GetItemCount()):
            self.update_task_item_by_idx(idx)

    def _update_get_all_reward(self):
        if not self.panel.btn_get_all:
            return
        has_unreceived_task_reward = global_data.player.has_unreceived_task_reward(self._cTask)
        self.panel.btn_get_all.setVisible(has_unreceived_task_reward)

        @self.panel.btn_get_all.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            is_reward_receive = global_data.player.check_reward_can_receive()
            has_unreceived_task_reward = global_data.player.has_unreceived_task_reward(self._cTask)
            if has_unreceived_task_reward:
                global_data.player.receive_tasks_reward([self._cTask])

    def init_coconut_rewards(self):
        self.reward_item_state = [ ITEM_UNGAIN for i in range(DIRECTIONAL_REWARD_COUNT * 2 + 1) ]
        self.panel.list_item_vertical.DeleteAllSubItem()
        self.panel.list_item_vertical.BindMethod('OnCreateItem', self.create_reward_ver_item)
        self.panel.list_item_vertical.SetInitCount(DIRECTIONAL_REWARD_COUNT)
        self.panel.list_item_vertical.scroll_Load()
        self.panel.list_item_horizontal.DeleteAllSubItem()
        self.panel.list_item_horizontal.BindMethod('OnCreateItem', self.create_reward_hor_item)
        self.panel.list_item_horizontal.SetInitCount(DIRECTIONAL_REWARD_COUNT + 1)
        self.panel.list_item_horizontal.scroll_Load()
        locked_cell = self._unrewarded_cell_map
        for i in range(4):
            for j in range(4):
                if i * 4 + j in locked_cell:
                    break
            else:
                self.connect_line(HOR_LINE, i)

            for j in range(4):
                if i + j * 4 in locked_cell:
                    break
            else:
                self.connect_line(VER_LINE, i)

        for i in (0, 5, 10, 15):
            if i in locked_cell:
                break
        else:
            self.connect_line(LEAN_LINE, 0)

    def on_click_reward(self, btn, touch, reward_id, item_id, item_num):
        if global_data.player.receive_coconut_reward(reward_id):
            return
        else:
            x, y = btn.GetPosition()
            w, h = btn.GetContentSize()
            x += w * 0.5
            wpos = btn.ConvertToWorldSpace(x, y)
            extra_info = {'show_jump': True}
            global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos, extra_info=extra_info, item_num=item_num)
            return

    def create_reward_ver_item(self, lv, idx, item):
        if len(self.reward_list) > idx:
            reward_info = confmgr.get('common_reward_data', str(self.reward_list[idx]), 'reward_list')
            if not reward_info:
                return
            reward_item, num = reward_info[0]
            init_tempate_mall_i_item(item.temp_item, reward_item, num, show_tips=False)
            item.temp_item.btn_choose.BindMethod('OnClick', lambda btn, touch, i=idx, item_id=reward_item, item_num=num: self.on_click_reward(btn, touch, i, item_id, item_num))
        state = global_data.player.coconut_map_reward_dict.get(str(idx), ITEM_UNGAIN)
        if state == self.reward_item_state[idx]:
            return
        if state == ITEM_UNRECEIVED:
            item.PlayAnimation('get_tips')
        else:
            if self.reward_item_state[idx] == ITEM_UNRECEIVED:
                item.RecoverAnimationNodeState('get_tips')
                item.StopAnimation('get_tips')
                item.vx_mask_01.setVisible(False)
            if state == ITEM_RECEIVED:
                item.PlayAnimation('display')
        self.reward_item_state[idx] = state

    def create_reward_hor_item(self, lv, idx, item):
        idx += SUMMER_COCONUT_COLUMN
        if len(self.reward_list) > idx:
            reward_info = confmgr.get('common_reward_data', str(self.reward_list[idx]), 'reward_list')
            if not reward_info:
                return
            reward_item, num = reward_info[0]
            init_tempate_mall_i_item(item.temp_item, reward_item, num, show_tips=False)
            item.temp_item.btn_choose.BindMethod('OnClick', lambda btn, touch, i=idx, item_id=reward_item, item_num=num: self.on_click_reward(btn, touch, i, item_id, item_num))
        state = global_data.player.coconut_map_reward_dict.get(str(idx), ITEM_UNGAIN)
        if state == self.reward_item_state[idx]:
            return
        if state == ITEM_UNRECEIVED:
            item.PlayAnimation('get_tips')
        else:
            if self.reward_item_state[idx] == ITEM_UNRECEIVED:
                item.RecoverAnimationNodeState('get_tips')
                item.StopAnimation('get_tips')
                item.vx_mask_01.setVisible(False)
            if state == ITEM_RECEIVED:
                item.PlayAnimation('display')
        self.reward_item_state[idx] = state

    def get_reward_btn(self, idx):
        if idx < DIRECTIONAL_REWARD_COUNT:
            return self.panel.list_item_vertical.GetItem(idx)
        if idx <= DIRECTIONAL_REWARD_COUNT * 2:
            return self.panel.list_item_horizontal.GetItem(idx - DIRECTIONAL_REWARD_COUNT)

    def update_line_connected_reward(self):
        for idx in range(SUMMER_COCONUT_COLUMN * 2 + 1):
            self._update_line_connected_reward_helper(idx)

    def _update_line_connected_reward_helper(self, idx):
        reward_btn = self.get_reward_btn(idx)
        if not reward_btn:
            return
        state = global_data.player.coconut_map_reward_dict.get(str(idx), ITEM_UNGAIN)
        if state == self.reward_item_state[idx]:
            return
        if state == ITEM_UNRECEIVED:
            reward_btn.PlayAnimation('get_tips')
        else:
            if self.reward_item_state[idx] == ITEM_UNRECEIVED:
                reward_btn.RecoverAnimationNodeState('get_tips')
                reward_btn.StopAnimation('get_tips')
                reward_btn.vx_mask_01.setVisible(False)
            if state == ITEM_RECEIVED:
                reward_btn.PlayAnimation('display')
        self.reward_item_state[idx] = state

    def receive_task_reward_succ(self, *args):
        for idx in range(DIRECTIONAL_REWARD_COUNT * DIRECTIONAL_REWARD_COUNT):
            self.update_task_item_by_idx(idx)
            status = global_data.player.get_task_reward_status(self._task_list[idx])
            if status == ITEM_RECEIVED:
                row = int(idx / DIRECTIONAL_REWARD_COUNT)
                column = int(idx % DIRECTIONAL_REWARD_COUNT)
                global_data.player.unlock_coconut_map(row, column)
                if global_data.is_inner_server:
                    coconut_id = row * DIRECTIONAL_REWARD_COUNT + column
                    if global_data.player and coconut_id not in global_data.player.opend_coconut_map:
                        if global_data.player.get_item_num_by_no(self.SLOT_OPEN_ITEM_NO) <= 0:
                            global_data.uisystem.post_wizard_trace_inner_server('\xe5\xbd\x93\xe5\x89\x8d\xe9\x9c\x80\xe8\xa6\x81\xe5\xbc\x80\xe5\xad\x94\xef\xbc\x8c\xe4\xbd\x86\xe4\xb8\x80\xe4\xb8\xaa%s\xe9\x83\xbd\xe6\xb2\xa1\xe6\x9c\x89' % self.SLOT_OPEN_ITEM_NO)

        self.update_line_connected_reward()
        widget_type = activity_utils.get_activity_widget_type(self._activity_type)
        self.panel.SetTimeOut(1.0, lambda : global_data.emgr.refresh_activity_redpoint_by_type.emit(widget_type), tag=241023)

    def receive_coconut_reward(self, reward_idx):
        self._update_line_connected_reward_helper(reward_idx)
        widget_type = activity_utils.get_activity_widget_type(self._activity_type)
        self.panel.SetTimeOut(1.0, lambda : global_data.emgr.refresh_activity_redpoint_by_type.emit(widget_type), tag=241023)

    @staticmethod
    def show_tab_rp(activity_type):
        activity_conf = confmgr.get('c_activity_config', activity_type)

        def task_1():
            from logic.gutils.activity_utils import can_receive_task_reward
            task_id = activity_conf.get('cTask')
            random_task_id = str(activity_conf['cUiData'].get('random_task_id', 0))
            final_task_id = str(activity_conf['cUiData'].get('final_reward_task', 0))
            random_refresh_type = get_task_fresh_type(random_task_id)
            random_task_list = global_data.player.get_random_children_tasks(random_refresh_type, random_task_id)
            if not random_task_list:
                random_task_list = []
            for random_task in random_task_list:
                if can_receive_task_reward(random_task):
                    return True

            if can_receive_task_reward(final_task_id):
                return True
            return can_receive_task_reward(task_id)

        if task_1():
            return True
        if global_data.player:
            is_reward_receive = global_data.player.check_reward_can_receive()
            if is_reward_receive:
                return True
        return False