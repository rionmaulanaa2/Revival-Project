# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityFairyland/ActivityFairylandLianliankan.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gutils.mall_utils import item_can_use_by_item_no
from logic.gutils.jump_to_ui_utils import jump_to_item_book_page
from logic.gutils.task_utils import get_task_fresh_type, get_task_name, get_total_prog, get_jump_conf, get_raw_left_open_time
from logic.gutils.item_utils import get_lobby_item_name
from common.cfg import confmgr
from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED
import cc
from logic.gcommon.time_utility import get_simply_time, get_time_string
from common.utils.timer import CLOCK
from logic.gcommon.common_const.activity_const import SUMMER_COCONUT_COLUMN
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.template_utils import init_tempate_mall_i_item
TOTEM_NAGA_ID = '208106504'
VER_LINE = 0
HOR_LINE = 1
LEAN_LINE = 2
CUP_ITEM_ID = 50104019

class ActivityFairylandLianliankan(ActivityTemplate):

    def on_init_panel(self):
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self.panel.lab_reward_name.SetString(get_lobby_item_name(TOTEM_NAGA_ID))
        self.panel.lab_valid_time.SetString(get_time_string(fmt='%Y.%m.%d', ts=self.activity_conf['cBeginTime']) + '-' + get_time_string(fmt='%m.%d', ts=self.activity_conf['cEndTime']))
        self.update_task_list()
        self.panel.list_item.SetInitCount(SUMMER_COCONUT_COLUMN * SUMMER_COCONUT_COLUMN)
        self.panel.list_item_vertical.SetInitCount(SUMMER_COCONUT_COLUMN)
        self.panel.list_item_horizontal.SetInitCount(SUMMER_COCONUT_COLUMN + 1)
        self.reward_btn_list = self.panel.list_item_vertical.GetAllItem() + self.panel.list_item_horizontal.GetAllItem()
        self.reward_item_state = [ ITEM_UNGAIN for i in range(len(self.reward_btn_list)) ]
        self.cup_count = global_data.player.get_item_num_by_no(CUP_ITEM_ID)
        self.allow_click = bool(self.cup_count)
        global_data.llk = self

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cDescTextID']))

        @self.panel.btn_look.callback()
        def OnClick(btn, touch):
            jump_to_item_book_page('1', TOTEM_NAGA_ID)

        self.update_final_reward()
        self.update_cup_count()
        for idx, item in enumerate(self.panel.list_item.GetAllItem()):
            item.btn_click.EnableCustomState(True)
            item.btn_click.BindMethod('OnClick', lambda btn, touch, i=idx: self.on_click_item_by_idx(i))

        self.update_list_item()
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

        reward_list = self.activity_conf.get('cUiData', {}).get('gift_list', [])
        for idx, reward_btn in enumerate(self.reward_btn_list):
            if len(reward_list) > idx:
                reward_item, num = confmgr.get('common_reward_data', str(reward_list[idx]), 'reward_list')[0]
                init_tempate_mall_i_item(reward_btn.temp_item, reward_item, num, show_tips=False)
                reward_btn.temp_item.btn_choose.BindMethod('OnClick', lambda btn, touch, i=idx, item_id=reward_item, item_num=num: self.on_click_reward(btn, i, item_id, item_num))

        self.update_reward()
        self.play_show_animation()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_time, interval=1, mode=CLOCK)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_new_cell_unlock': self.on_cell_unlocked,
           'receive_coconut_reward': self.receive_reward,
           'on_lobby_bag_item_changed_event': self.on_item_received,
           'receive_task_reward_succ_event': self.update_task_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_final_reward(self):
        totem_nage_gain = item_can_use_by_item_no(TOTEM_NAGA_ID)[0]
        self.panel.lab_type.SetString(get_text_by_id(906668 if totem_nage_gain else 906662))

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
                children_task_list.append((child_task, task_state))

            children_task_list.sort()
            self.panel.list_task.SetInitCount(len(children_task_list))
            for idx, child_task in enumerate(children_task_list):
                item = self.panel.list_task.GetItem(idx)
                item.lab_task.SetString(get_task_name(child_task[0]))
                item.lab_schedule.SetString('%s/%s' % (global_data.player.get_task_prog(child_task[0]), get_total_prog(child_task[0])))
                text_id_list = (80930, 604027, 906669)
                item.btn_click.SetText(text_id_list[child_task[1]])
                item.btn_click.SetEnable(child_task[1] == STATE_NORMAL)
                item.btn_click._updateCurState(child_task[1])

                @item.btn_click.callback()
                def OnClick(btn, touch, task_info=child_task):
                    if task_info[1] == STATE_NORMAL:
                        global_data.player.receive_task_reward(task_info[0])

            global_data.emgr.refresh_activity_redpoint.emit()
            return

    def update_list_item(self):
        for idx, item in enumerate(self.panel.list_item.GetAllItem()):
            btn = item.btn_click
            btn_state = self.get_item_state(idx)
            btn.SetEnable(btn_state == STATE_NORMAL)
            if btn_state == STATE_NORMAL:
                item.PlayAnimation('loop')
            else:
                item.StopAnimation('loop')
                item.vx_saoguang.setVisible(False)
            btn._updateCurState(btn_state)

    def update_reward(self):
        for idx, reward_btn in enumerate(self.reward_btn_list):
            state = global_data.player.coconut_map_reward_dict.get(str(idx), ITEM_UNGAIN)
            if state == self.reward_item_state[idx]:
                continue
            if state == ITEM_UNRECEIVED:
                reward_btn.PlayAnimation('click')
            else:
                if self.reward_item_state[idx] == ITEM_UNRECEIVED:
                    reward_btn.RecoverAnimationNodeState('click')
                    reward_btn.StopAnimation('click')
                    reward_btn.vx_mask_01.setVisible(False)
                if state == ITEM_RECEIVED:
                    reward_btn.PlayAnimation('display')
            self.reward_item_state[idx] = state

    def receive_reward(self, idx):
        if idx > len(self.reward_btn_list):
            return
        self.reward_btn_list[idx].RecoverAnimationNodeState('click')
        self.reward_btn_list[idx].StopAnimation('click')
        self.reward_btn_list[idx].vx_mask_01.setVisible(False)
        self.reward_btn_list[idx].PlayAnimation('display')
        self.reward_item_state[idx] = ITEM_RECEIVED

    def on_item_received(self):
        self.update_cup_count()
        self.update_reward()
        self.update_final_reward()

    def update_cup_count(self):
        self.cup_count = global_data.player.get_item_num_by_no(CUP_ITEM_ID)
        self.allow_click = bool(self.cup_count)
        self.panel.lab_num.SetString(get_text_by_id(906663, (str(self.cup_count),)))
        self.update_list_item()

    def connect_line(self, dir, idx, play_anim=False):
        if dir == VER_LINE:
            step = 4
            start_idx = idx
            img_name = 'img_5'
            self.panel.vx_xian_01.SetPosition('50%' + str(-270 + 90 * idx), '50%0')
            anim_name_1 = 'appear_01'
        elif dir == HOR_LINE:
            step = 1
            start_idx = idx * 4
            img_name = 'img_3'
            self.panel.vx_xian_02.SetPosition('50%-43', '50%' + str(49 - 90 * idx))
            anim_name_1 = 'appear_02'
        else:
            step = 5
            start_idx = 0
            img_name = 'img_4'
            anim_name_1 = 'appear_03'

        def show_line(idx=start_idx):
            for i in range(3):
                item = self.panel.list_item.GetItem(idx)
                nd_img = getattr(item, img_name)
                nd_img.setVisible(True)
                idx += step

        if play_anim:
            self.panel.runAction(cc.Sequence.create([
             cc.CallFunc.create(lambda : self.panel.PlayAnimation(anim_name_1)),
             cc.DelayTime.create(0.17),
             cc.CallFunc.create(show_line)]))
        else:
            show_line()

    def get_item_state(self, idx):
        btn_state = STATE_NORMAL
        if idx not in global_data.player.locked_coconut_map:
            btn_state = STATE_SELECTED
        elif self.cup_count == 0:
            btn_state = STATE_DISABLED
        return btn_state

    def play_show_animation(self):
        act = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show'))]
        for item in self.panel.list_task.GetAllItem():
            item.nd_vx.setVisible(False)
            act.append(cc.CallFunc.create(lambda item=item: item.PlayAnimation('show')))
            act.append(cc.DelayTime.create(0.03))

        self.panel.runAction(cc.Sequence.create(act))

    def on_click_item_by_idx(self, idx):
        if not self.allow_click:
            return
        if self.get_item_state(idx) != STATE_NORMAL:
            return
        self.allow_click = False
        global_data.player.unlock_coconut_map(int(idx / 4), int(idx % 4))

    def on_click_reward(self, btn, reward_id, item_id, item_num):
        if global_data.player.receive_coconut_reward(reward_id):
            return
        else:
            x, y = btn.GetPosition()
            w, _ = btn.GetContentSize()
            x += w * 0.5
            wpos = btn.ConvertToWorldSpace(x, y)
            extra_info = {'show_jump': True}
            global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos, extra_info=extra_info, item_num=item_num)
            return

    def on_cell_unlocked(self, idx):
        if idx >= self.panel.list_item.GetItemCount():
            return
        else:
            item = self.panel.list_item.GetItem(idx)
            item.StopAnimation('loop')
            item.PlayAnimation('click')
            self.allow_click = bool(self.cup_count)
            self.update_cup_count()
            self.update_reward()
            row_start = idx - idx % 4
            col_start = idx % 4
            lean_start = 0 if idx in (0, 5, 10, 15) else None
            row_complete = True
            col_complete = True
            lean_complete = lean_start is not None
            for i in range(4):
                if row_complete and row_start + i in global_data.player.locked_coconut_map:
                    row_complete = False
                if col_complete and col_start + i * 4 in global_data.player.locked_coconut_map:
                    col_complete = False
                if lean_complete and lean_start + i * 5 in global_data.player.locked_coconut_map:
                    lean_complete = False

            if row_complete:
                self.connect_line(HOR_LINE, idx / 4, True)
            if col_complete:
                self.connect_line(VER_LINE, idx % 4, True)
            if lean_complete:
                self.connect_line(LEAN_LINE, 0, True)
            return

    def refresh_time(self):
        task_id = self.activity_conf.get('cTask')
        task_left_time = get_raw_left_open_time(task_id)
        self.panel.lab_time.SetString(get_text_by_id(906607).format(get_simply_time(task_left_time)))

    def on_finalize_panel(self):
        super(ActivityFairylandLianliankan, self).on_finalize_panel()
        global_data.game_mgr.get_logic_timer().unregister(self._timer)