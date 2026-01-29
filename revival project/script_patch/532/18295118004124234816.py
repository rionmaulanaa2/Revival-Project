# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPromare/ActivityPromareLianliankan.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gutils.mall_utils import item_can_use_by_item_no
from logic.gutils.jump_to_ui_utils import jump_to_item_book_page
from logic.gutils.task_utils import get_task_fresh_type, get_task_name, get_total_prog, get_jump_conf, get_raw_left_open_time
from logic.gutils.item_utils import get_lobby_item_name, exec_jump_to_ui_info, get_lobby_item_type, get_lobby_item_reward_id
from common.cfg import confmgr
from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED
import cc
from logic.gcommon.time_utility import get_simply_time, get_time_string
from common.utils.timer import CLOCK
from logic.gcommon.common_const.activity_const import SUMMER_COCONUT_COLUMN
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.template_utils import init_tempate_mall_i_item, get_reward_list_by_reward_id
from ..ActivityNewLianLianKan import ActivityNewLianLianKan
from logic.gcommon.item.lobby_item_type import L_ITEM_YTPE_VEHICLE_SKIN, L_ITEM_TYPE_GIFTPACKAGE, L_ITME_TYPE_GUNSKIN
VER_LINE = 0
HOR_LINE = 1
LEAN_LINE = 2

class ActivityPromareLianliankan(ActivityNewLianLianKan):

    def on_init_panel(self):
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        ui_data = self.activity_conf.get('cUiData')
        all_unlock_reward_id = str(ui_data['gift_list'][-1])
        self.reward_list = ui_data.get('gift_list', [])
        self.ultimate_reward = confmgr.get('common_reward_data', all_unlock_reward_id, 'reward_list')[0][0]
        self.chip_item_id = ui_data['chip_item_id']
        self.update_task_list()
        self.update_cup_count()
        self.panel.list_item.DeleteAllSubItem()
        self.panel.list_item.BindMethod('OnCreateItem', self.create_connect_item)
        self.panel.list_item.SetInitCount(SUMMER_COCONUT_COLUMN * SUMMER_COCONUT_COLUMN)
        self.panel.list_item.scroll_Load()
        self.reward_item_state = [ ITEM_UNGAIN for i in range(SUMMER_COCONUT_COLUMN * 2 + 1) ]
        self.panel.list_item_vertical.DeleteAllSubItem()
        self.panel.list_item_vertical.BindMethod('OnCreateItem', self.create_reward_ver_item)
        self.panel.list_item_vertical.SetInitCount(SUMMER_COCONUT_COLUMN)
        self.panel.list_item_vertical.scroll_Load()
        self.panel.list_item_horizontal.DeleteAllSubItem()
        self.panel.list_item_horizontal.BindMethod('OnCreateItem', self.create_reward_hor_item)
        self.panel.list_item_horizontal.SetInitCount(SUMMER_COCONUT_COLUMN + 1)
        self.panel.list_item_horizontal.scroll_Load()
        self.cup_count = global_data.player.get_item_num_by_no(self.chip_item_id)
        self.allow_click = bool(self.cup_count)
        self.xian_01_init_pos = self.panel.vx_xian_01.GetPosition()
        self.xian_02_init_pos = self.panel.vx_xian_02.GetPosition()
        global_data.llk = self

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cDescTextID']))

        @self.panel.btn_look.callback()
        def OnClick(btn, touch):
            reward_type = get_lobby_item_type(self.ultimate_reward)
            if reward_type == L_ITEM_YTPE_VEHICLE_SKIN:
                jump_to_item_book_page('2', self.ultimate_reward)
            elif reward_type == L_ITME_TYPE_GUNSKIN:
                jump_to_item_book_page('3', self.ultimate_reward)
            elif reward_type == L_ITEM_TYPE_GIFTPACKAGE:
                dlg = global_data.ui_mgr.show_ui('MultiChosenSingleRewardUI', 'logic.comsys.reward')
                dlg and dlg.set_use_params({'id': None,'item_no': self.ultimate_reward,'quantity': 1}, [], [])
                dlg and dlg.set_btn_use_visible(False)
            return

        self.update_final_reward()
        locked_cell = global_data.player.locked_coconut_map
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

        self.update_reward()
        self.play_show_animation()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_time, interval=1, mode=CLOCK)

    def update_final_reward(self):
        ultimate_reward_gain = not bool(global_data.player.locked_coconut_map)
        self.panel.lab_type.SetString(get_text_by_id(80953 if ultimate_reward_gain else 906662))

    def update_cup_count(self):
        self.cup_count = global_data.player.get_item_num_by_no(self.chip_item_id)
        self.allow_click = bool(self.cup_count)
        self.panel.lab_num.SetString(get_text_by_id(610751, (str(self.cup_count),)))

    def refresh_time(self):
        pass

    def on_item_received(self):
        self.update_cup_count()
        self.update_reward()
        self.update_final_reward()
        self.update_exchange_rp()
        self.update_list_item()

    def update_task_list(self, *args):
        task_id = self.activity_conf.get('cTask')
        random_refresh_type = get_task_fresh_type(task_id)
        children_task_list = []
        random_task_list = global_data.player.get_random_children_tasks(random_refresh_type, task_id)
        if random_task_list is None:
            return
        else:
            for child_task in random_task_list:
                task_state = STATE_SELECTED
                if global_data.player.is_task_finished(child_task):
                    if global_data.player.has_unreceived_task_reward(child_task):
                        task_state = STATE_NORMAL
                    else:
                        task_state = STATE_DISABLED
                children_task_list.append((task_state, child_task))

            children_task_list.sort()
            self.panel.list_task.SetInitCount(len(children_task_list))
            for idx, (task_state, child_task) in enumerate(children_task_list):
                item = self.panel.list_task.GetItem(idx)
                item.lab_task.SetString(get_task_name(child_task))
                cur_prog, total_prog = global_data.player.get_task_prog(child_task), get_total_prog(child_task)
                item.lab_schedule.SetString(('<color=0xDD418Dff>%s</color>/%s' if cur_prog < total_prog else '%s/%s') % (cur_prog, total_prog))
                text_id_list = (80930, 604027, 906669, 906672)
                text_id = text_id_list[task_state]
                btn_enable = task_state == STATE_NORMAL
                jump_conf = None
                if task_state == STATE_SELECTED:
                    jump_conf = get_jump_conf(child_task)
                    if jump_conf:
                        text_id = jump_conf.get('unreach_text', None) or text_id_list[-1]
                        btn_enable = True
                item.btn_click.SetText(text_id)
                item.btn_click.SetEnable(btn_enable)
                item.btn_click._updateCurState(task_state)

                @item.btn_click.callback()
                def OnClick(btn, touch, child_task=child_task, task_state=task_state, jump_conf=jump_conf):
                    if task_state == STATE_NORMAL:
                        global_data.player.receive_task_reward(child_task)
                    elif task_state == STATE_SELECTED:
                        exec_jump_to_ui_info(jump_conf)

            global_data.emgr.refresh_activity_redpoint.emit()
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
            item.PlayAnimation('click')
        else:
            if self.reward_item_state[idx] == ITEM_UNRECEIVED:
                item.RecoverAnimationNodeState('click')
                item.StopAnimation('click')
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
            item.PlayAnimation('click')
        else:
            if self.reward_item_state[idx] == ITEM_UNRECEIVED:
                item.RecoverAnimationNodeState('click')
                item.StopAnimation('click')
                item.vx_mask_01.setVisible(False)
            if state == ITEM_RECEIVED:
                item.PlayAnimation('display')
        self.reward_item_state[idx] = state

    def create_connect_item(self, lv, idx, item):
        btn = item.btn_click
        item.btn_click.EnableCustomState(True)
        item.btn_click.BindMethod('OnClick', lambda btn, touch, i=idx: self.on_click_item_by_idx(i))
        btn_state = self.get_item_state(idx)
        btn.SetEnable(btn_state == STATE_NORMAL)
        if btn_state == STATE_NORMAL:
            item.PlayAnimation('loop')
        else:
            item.StopAnimation('loop')
            item.vx_saoguang.setVisible(False)
        btn._updateCurState(btn_state)