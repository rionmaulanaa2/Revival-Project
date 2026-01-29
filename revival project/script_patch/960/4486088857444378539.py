# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAlphaPlanTrain.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from functools import cmp_to_key
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_item_rare_degree
from common.utils.cocos_utils import ccp
TRAIN_UIRES_PREFIX = 'gui/ui_res_2/activity/activity_new_domestic/new_star_plan/'
REWARD_RARENESS_UI_INFO_B = (
 TRAIN_UIRES_PREFIX + 'pnl_alpha_gift_blue.png',
 TRAIN_UIRES_PREFIX + 'pnl_alpha_gift_note_blue.png',
 3708133,
 TRAIN_UIRES_PREFIX + 'pnl_alpha_gift_bluepro2.png')
REWARD_RARENESS_UI_INFO_S = (
 TRAIN_UIRES_PREFIX + 'pnl_alpha_gift_gold.png',
 TRAIN_UIRES_PREFIX + 'pnl_alpha_gift_note_gold.png',
 14124032,
 TRAIN_UIRES_PREFIX + 'pnl_alpha_gift_goldpro2.png')
ICON_B = 'gui/ui_res_2/reward/img_b01.png'
ICON_A = 'gui/ui_res_2/reward/img_a01.png'
ICON_S = 'gui/ui_res_2/reward/img_s01.png'
from logic.gcommon.item.item_const import RARE_DEGREE_2, RARE_DEGREE_3, RARE_DEGREE_4
REWARD_RARENESS_UI_INFO = {RARE_DEGREE_2: REWARD_RARENESS_UI_INFO_B,
   RARE_DEGREE_4: REWARD_RARENESS_UI_INFO_S
   }
REWARD_RARENESS_ICON_INFO = {RARE_DEGREE_2: ICON_B,
   RARE_DEGREE_3: ICON_A,
   RARE_DEGREE_4: ICON_S
   }

class ActivityAlphaPlanTrain(ActivityBase):
    FPS = 30
    DELAY_REWARD_SHOW_TAG = 31415926
    ELE_REWARD_MISSION_ANIM_TAG = 31415926
    MSTATE_COLLAPSED = 1
    MSTATE_EXPANDED = 2
    U_NODE_STATE_IN = 1
    U_NODE_STATE_OUT = 2

    def __init__(self, dlg, activity_type):
        ActivityBase.__init__(self, dlg, activity_type)

    def on_init_panel(self):
        self.is_done = True
        self._init_data()
        self._init_view()
        self._refresh_view(sync_ultimate=False)
        self.init_event()
        from logic.gcommon.common_utils.local_text import get_cur_text_lang_shorthand
        sh = get_cur_text_lang_shorthand()
        if self.panel.HasAnimation(sh):
            self.panel.PlayAnimation(sh)
        if self._init_item_idx + 1 != len(self._task_ids):
            self.panel.PlayAnimation('in')
            in_time = self.panel.GetAnimationMaxRunTime('in')
            self.panel.DelayCallWithTag(in_time, self._on_in_finished, self.DELAY_REWARD_SHOW_TAG)
        else:
            self.panel.PlayAnimation('in')
            self.panel.StopAnimation('in', finish_ani=True)
            self._on_in_finished()
            self._sync_ultimate_node_position()
            self._try_do_u_node_in()
        self.is_done = False

    def on_finalize_panel(self):
        self.is_done = True
        self.process_event(False)
        self._stop_update_list_pos_and_size_timer()
        self._stop_sync_ultimate_pos_timer()
        list_node = self.panel.nd_list
        cnt = list_node.GetItemCount()
        for i in range(cnt):
            item = list_node.GetItem(i)
            self._stop_mission_out(item, i)
            self._stop_mission(item, i)
            item.PlayAnimation('mission_out')
            item.StopAnimation('mission_out', finish_ani=True)

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_task_reward_received
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self._refresh_view()

    def _on_in_finished(self):
        self._play_reward_show()
        list_node = self.panel.nd_list
        list_node.setTouchEnabled(True)

    def _play_reward_show(self):
        list_node = self.panel.nd_list
        cnt = list_node.GetItemCount()
        for i in range(cnt):
            item = list_node.GetItem(i)
            item.PlayAnimation('show1')

    def _init_data(self):
        self._task_ids = self._get_parent_tasks()
        self._u_task_id = self._get_u_task_id()
        self._custom_item_rare_degree = self._get_custom_rare_degree()
        self._player_attend_days = global_data.player.get_history_attend_days()
        list_task_cnt = len(self._task_ids)
        self._init_item_idx = min(list_task_cnt, self._player_attend_days) - 1
        self._update_list_pos_and_size_timer_id = None
        self._update_list_pos_and_size_end_time = 0.0
        self._reward_mission_anim_info = {}
        self._ultimate_node = self.panel.nd_mech
        self._ultimate_visual_node = self.panel.nd_mech_visual
        self._sync_ultimate_pos_timer_id = None
        self._sync_ultimate_pos_end_time = 0.0
        self._u_node_anim_state = self.U_NODE_STATE_OUT
        self.TASK_ORDER_PRIORITY_MAP = {self.UNOBTAINED: 1,
           self.UNFINISHED: 2,
           self.OBTAINED: 3,
           self.LOCKED: 4
           }
        self._nd_list_outside_width = 368
        return

    def _init_view(self):
        self._init_rewards()
        if not self._ultimate_node._user_data_init_position:
            self._ultimate_node._user_data_init_position = self._ultimate_node.GetPosition()
        self._ultimate_node.SetPosition(*self._ultimate_node._user_data_init_position)
        self.panel.PlayAnimation('mech_out')
        self.panel.StopAnimation('mech_out', finish_ani=True)

    def _init_rewards(self):
        task_ids = self._task_ids
        list_node = self.panel.nd_list
        list_node.SetItemSizeGetter(self._list_size_getter)
        list_node.BindMethod('OnScrolling', self._on_list_scrolling)
        list_node.BindMethod('OnScrollToRight', self._on_list_scrolled_to_right)
        list_node.BindMethod('OnScrollBounceRight', self._on_scroll_bounce_right)
        list_task_cnt = len(task_ids)
        cnt = list_task_cnt + 1
        list_node.SetInitCount(cnt)
        if self._init_item_idx >= 0 and self._init_item_idx < list_task_cnt:
            item = list_node.GetItem(self._init_item_idx)
            self._play_mission(item, self._init_item_idx)
            self._stop_mission(item, self._init_item_idx)
            off = list_node.GetContentOffset()
            width = self._get_list_offset_x_until_idx(self._init_item_idx)
            list_node.SetContentOffsetInDuration(ccp(-width, off.y), bound_check=True, over_edge=False)
        list_node.setTouchEnabled(False)
        ultimate_drag_node = self.panel.mech_3

        @ultimate_drag_node.unique_callback()
        def OnBegin(btn, touch):
            return True

        @ultimate_drag_node.unique_callback()
        def OnDrag(btn, touch, list_node=list_node):
            delta = touch.getDelta()
            if list_node.isValid():
                off = list_node.GetContentOffset()
                new_x = off.x + delta.x
                list_node.SetContentOffsetInDuration(ccp(new_x, off.y), bound_check=True, over_edge=False)
                self._on_list_scrolling(list_node)

        @ultimate_drag_node.unique_callback()
        def OnEnd(btn, touch):
            pass

    def _get_list_offset_x_until_idx(self, idx):
        list_node = self.panel.nd_list
        item = list_node.GetItem(idx)
        x, _ = item.GetPosition()
        return x

    def _refresh_u_reward_view(self):
        task_id = self._u_task_id
        reward_info = self._get_reward_item_info(task_id)
        if reward_info is None:
            return
        else:
            item_no, item_num = reward_info
            reward_text_node = self.panel.vx_lab_text
            reward_text_node.SetString(get_lobby_item_name(item_no))
            task_status = self._get_task_status(task_id)
            obtain_btn = self.panel.btn_mech
            if task_status == self.LOCKED:
                btn_text_id = 604033
            elif task_status == self.UNFINISHED:
                btn_text_id = 604027
            elif task_status == self.UNOBTAINED:
                btn_text_id = 604028
            elif task_status == self.OBTAINED:
                btn_text_id = 604029
            else:
                btn_text_id = 604033
            obtain_btn.SetText(btn_text_id)
            obtain_btn.SetEnable(task_status == self.UNOBTAINED)

            @obtain_btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                task_s = self._get_task_status(task_id)
                if task_s != self.UNOBTAINED:
                    return
                global_data.player.receive_task_reward(task_id)

            return

    LOCKED = 1
    UNFINISHED = 2
    UNOBTAINED = 3
    OBTAINED = 4

    def _get_task_status(self, task_id):
        test = False
        if test:
            if '1901002' == task_id:
                return self.LOCKED
            if '1901003' == task_id:
                return self.OBTAINED
            if '1901004' == task_id:
                return self.UNOBTAINED
            if '1901000' == task_id:
                return self.UNOBTAINED
            if '1902000' == task_id:
                return self.LOCKED
            if '1908000' == task_id:
                return self.UNOBTAINED
        if not global_data.player:
            return self.LOCKED
        if task_id in self._task_ids:
            idx = self._task_ids.index(task_id)
            if self._player_attend_days < idx + 1:
                return self.LOCKED
        if task_id == self._u_task_id:
            l = len(self._task_ids)
            if l > 1:
                d_task_id = self._task_ids[l - 1]
                if d_task_id != self._u_task_id:
                    st = self._get_task_status(d_task_id)
                    if st == self.LOCKED:
                        return self.LOCKED
        player = global_data.player
        if not player.is_task_finished(task_id):
            return self.UNFINISHED
        if not player.has_receive_reward(task_id):
            return self.UNOBTAINED
        return self.OBTAINED

    def _list_size_getter(self, idx, item):
        list_node = self.panel.nd_list
        w, h = item.GetContentSize()
        if idx + 1 == list_node.GetItemCount():
            ele_card_w, _ = item.nd_card.GetContentSize()
            v_w, _ = self._ultimate_visual_node.GetContentSize()
            v_w += self._nd_list_outside_width
            return (
             (w - ele_card_w) * 0.5 + v_w, h)
        visual_width_of_expaneded_list = 437
        animating, perc = self._is_mission_animating(idx)
        mission_state = self._get_mission_state(idx)
        if animating:
            act_perc = perc
        else:
            act_perc = 0.0
        if mission_state == self.MSTATE_COLLAPSED:
            act_perc = perc
        else:
            act_perc = 1.0 - perc
        return (
         w + act_perc * visual_width_of_expaneded_list, h)

    def _sync_ultimate_node_position(self):
        list_node = self.panel.nd_list
        cnt = list_node.GetItemCount()
        if cnt < 1:
            return
        dummy_node = list_node.GetItem(cnt - 1)
        _, dummy_node_y = dummy_node.GetPosition()
        visual_node_width, _ = self._list_size_getter(cnt - 1, dummy_node)
        visual_node_width = visual_node_width - self._nd_list_outside_width
        dst_pos_vline_x = self._get_ele_card_visual_left_in_inner(dummy_node) + float(visual_node_width) * 0.5
        wpos = dummy_node.GetParent().ConvertToWorldSpace(dst_pos_vline_x, dummy_node_y)
        px, py = self._ultimate_node.GetPosition()
        wpos_u = self._ultimate_node.GetParent().ConvertToWorldSpace(px, py)
        px, py = self._ultimate_visual_node.GetPosition()
        wpos_uv = self._ultimate_visual_node.GetParent().ConvertToWorldSpace(px, py)
        wpos_x_offset = wpos_u.x - wpos_uv.x
        wpos.x += wpos_x_offset
        _, o_y = self._ultimate_node.GetPosition()
        lpos = self._ultimate_node.GetParent().convertToNodeSpace(wpos)
        self._ultimate_node.SetPosition(lpos.x, o_y)

    def _get_ele_card_visual_left_in_inner(self, ele_node):
        dummy_node = ele_node
        dummy_node_x, _ = dummy_node.GetPosition()
        dummy_node_w, _ = dummy_node.GetContentSize()
        ele_card_w, _ = dummy_node.nd_card.GetContentSize()
        return dummy_node_x + dummy_node_w * 0.5 - ele_card_w * 0.5

    def _on_list_scrolling(self, slist):
        if self.is_done:
            return
        self._init_period_sync_utilmate_pos_check()
        list_node = slist
        viewport_w, _ = slist.GetContentSize()
        off = list_node.GetContentOffset()
        offset_x = off.x
        viewport_right_relative_to_inner_left = viewport_w - offset_x
        cnt = list_node.GetItemCount()
        if cnt >= 1:
            dummy_node = list_node.GetItem(cnt - 1)
            ref_pos_vline_x = self._get_ele_card_visual_left_in_inner(dummy_node)
            if viewport_right_relative_to_inner_left > ref_pos_vline_x:
                self._try_do_u_node_in()
            else:
                self._try_do_u_node_out()

    def _on_scroll_bounce_right(self, slist):
        if self.is_done:
            return
        self._init_period_sync_utilmate_pos_check()

    def _on_list_scrolled_to_right(self, *args):
        if self.is_done:
            return
        self._init_period_sync_utilmate_pos_check()

    def _refresh_view(self, sync_ultimate=True):
        self._refresh_rewards(sync_ultimate=sync_ultimate)
        self._refresh_u_reward_view()

    def _get_reward_item_info(self, task_id):
        reward_id = task_utils.get_task_reward(task_id)
        if not reward_id:
            log_error('no reward_id', task_id)
            return None
        else:
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            if not reward_conf:
                log_error('reward_id is not exist in common_reward_data', task_id, reward_id)
                return None
            reward_list = reward_conf.get('reward_list', [])
            if len(reward_list) <= 0:
                log_error('empty reward_list', task_id, reward_id)
                return None
            item_no, item_num = reward_list[0]
            return (
             item_no, item_num)

    def _refresh_rewards(self, sync_ultimate=True):
        task_ids = self._task_ids
        list_node = self.panel.nd_list
        cnt = list_node.GetItemCount()
        day_text_start_id = 604013
        for i in range(cnt):
            item = list_node.GetItem(i)
            if i >= len(task_ids):
                item.setVisible(False)
                continue
            item.setVisible(True)
            task_id = task_ids[i]
            task_s = self._get_task_status(task_id)
            item.RecordAnimationNodeState('loop2')
            text_id_offset = i % 8
            item.card_day_text.SetString(day_text_start_id + text_id_offset)
            reward_info = self._get_reward_item_info(task_id)
            if reward_info is None:
                continue
            item_no, item_num = reward_info
            item.img_card_item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(item_no))
            if item_no == 208200203:
                s = 0.6
            else:
                s = 0.5
            item.img_card_item.setScaleX(s)
            item.img_card_item.setScaleY(s)
            item.lab.lab_text.SetString(get_lobby_item_name(item_no))
            if item_num > 1:
                text = 'X%s' % item_num
            else:
                text = ''
            item.lab_num.SetString(text)
            if task_s == self.LOCKED:
                v_degree = RARE_DEGREE_2
            else:
                v_degree = RARE_DEGREE_4
            degree = self._custom_item_rare_degree[i]
            rareness_ui_info = REWARD_RARENESS_UI_INFO.get(v_degree, REWARD_RARENESS_UI_INFO_B)
            _card_baseboard, _card_transparency, _card_day_text, _img_card_ingline = rareness_ui_info
            _lab_img_class = REWARD_RARENESS_ICON_INFO.get(degree, ICON_B)
            item.img_card_baseboard.SetDisplayFrameByPath('', _card_baseboard)
            item.card_transparency.SetDisplayFrameByPath('', _card_transparency)
            item.card_day_text.SetOutLineColor(_card_day_text)
            item.lab_img_class.SetDisplayFrameByPath('', _lab_img_class)
            item.lab_img_class_cp.SetMaskFrameByPath('', _lab_img_class)
            item.img_card_ingline.SetProgressTexture(_img_card_ingline)
            progress_pect = float(global_data.player.get_task_prog(task_id)) / task_utils.get_total_prog(task_id)
            item.img_card_ingline.SetPercentage(progress_pect * 100)

            @item.card_baseboard.unique_callback()
            def OnClick(btn, touch, item=item, idx=i, task_id=task_id):
                task_s = self._get_task_status(task_id)
                if task_s == self.LOCKED:
                    return
                src_state = self._get_mission_state(idx)
                animating, perc = self._is_mission_animating(idx)
                if src_state == self.MSTATE_COLLAPSED:
                    if not animating:
                        dst_state = self.MSTATE_EXPANDED
                    else:
                        dst_state = self.MSTATE_COLLAPSED
                elif not animating:
                    dst_state = self.MSTATE_COLLAPSED
                else:
                    dst_state = self.MSTATE_EXPANDED
                if dst_state == self.MSTATE_EXPANDED:
                    self._stop_mission_out(item, idx)
                    self._play_mission(item, idx)
                else:
                    self._stop_mission(item, idx)
                    self._play_mission_out(item, idx)

            @item.nd_item.unique_callback()
            def OnClick(btn, touch, item_no=item_no, item_num=item_num):
                x, y = btn.GetPosition()
                wpos = btn.GetParent().ConvertToWorldSpace(x, y)
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, item_num=item_num)
                return

            self._refresh_reward_task_status(item, task_id, i)

            @item.btn_card.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                task_s = self._get_task_status(task_id)
                if task_s != self.UNOBTAINED:
                    return
                global_data.player.receive_task_reward(task_id)

            children_ids = task_utils.get_children_task(task_id)
            children_ids = sorted(children_ids[:], key=cmp_to_key(self._task_sorter))
            c_cnt = len(children_ids)
            inner_list = item.list
            inner_list.SetInitCount(c_cnt)
            child_got_cnt = 0
            has_obtainable_child = False
            for j in range(c_cnt):
                c_item = inner_list.GetItem(j)
                c_task_id = children_ids[j]
                c_status = self._get_task_status(c_task_id)
                if c_status == self.UNOBTAINED:
                    has_obtainable_child = True
                elif c_status == self.OBTAINED:
                    child_got_cnt += 1
                c_item.text.SetString(task_utils.get_task_name(c_task_id))
                reward_info = self._get_reward_item_info(c_task_id)
                if reward_info is None:
                    continue
                item_no, item_num = reward_info
                item_pic_path = get_lobby_item_pic_by_item_no(item_no)
                c_item.img_item.SetDisplayFrameByPath('', item_pic_path)
                if item_num > 1:
                    text = 'X%s' % item_num
                else:
                    text = ''
                c_item.lab_num.SetString(text)
                cur_pro = global_data.player.get_task_prog(c_task_id)
                total_pro = task_utils.get_total_prog(c_task_id)
                c_item.text_progress.SetString('%s/%s' % (cur_pro, total_pro))
                self._refresh_sub_reward_task_status(c_item, c_task_id, c_status)

                @c_item.btn_go.unique_callback()
                def OnClick(btn, touch, task_id=c_task_id):
                    task_s = self._get_task_status(task_id)
                    if task_s == self.UNOBTAINED:
                        global_data.player.receive_task_reward(task_id)
                    elif task_s == self.UNFINISHED:
                        jump_conf = task_utils.get_jump_conf(task_id)
                        func_name = None
                        if jump_conf:
                            func_name = jump_conf.get('func')
                        from logic.gutils import jump_to_ui_utils
                        if jump_to_ui_utils.is_lobby_jump(func_name):
                            global_data.ui_mgr.close_ui('AlphaPlanMainUI')
                        task_utils.try_do_jump(task_id)
                    return

                @c_item.btn_lab_item.unique_callback()
                def OnClick(btn, touch, item_no=item_no, item_num=item_num):
                    x, y = btn.GetPosition()
                    wpos = btn.ConvertToWorldSpace(x, y)
                    global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, item_num=item_num)
                    return

            item.text_mission_pro.SetString('%s/%s' % (child_got_cnt, c_cnt))
            item.img_red.setVisible(has_obtainable_child)

        if sync_ultimate:
            self._sync_ultimate_node_position()
        return

    def _task_sorter(self, a, b):
        a_s = self._get_task_status(a)
        b_s = self._get_task_status(b)
        if a_s == b_s:
            return six_ex.compare(a, b)
        else:
            a_p = self.TASK_ORDER_PRIORITY_MAP.get(a_s, 99)
            b_p = self.TASK_ORDER_PRIORITY_MAP.get(b_s, 99)
            return six_ex.compare(a_p, b_p)

    def _refresh_reward_task_status(self, item, task_id, item_idx):
        task_s = self._get_task_status(task_id)
        item.StopAnimation('loop2')
        item.RecoverAnimationNodeState('loop2')
        gray = task_s == self.OBTAINED
        from logic.comsys.effect.ui_effect import set_gray
        set_gray(item.img_card_baseboard, gray)
        set_gray(item.img_card_item, gray)
        set_gray(item.card_transparency, gray)
        set_gray(item.card_shadow, gray)
        set_gray(item.card_pin, gray)
        item.btn_card.SetEnable(task_s == self.UNOBTAINED)
        item.img_got.setVisible(gray)
        item.img_got_2.setVisible(gray)
        item.right.setVisible(gray)
        unlocked = task_s != self.LOCKED
        if not unlocked:
            from logic.gcommon.common_utils.local_text import get_text_by_id
            btn_text = get_text_by_id(604034).format(day=item_idx + 1)
        else:
            unfinished = task_s == self.UNFINISHED
            if unfinished:
                btn_text = 604027
            else:
                obtained = task_s == self.OBTAINED
                if obtained:
                    btn_text = 604029
                else:
                    btn_text = 604028
                    item.PlayAnimation('loop2')
        item.btn_card.SetText(btn_text)

    def _refresh_sub_reward_task_status(self, item, task_id, c_status):
        gray = c_status == self.OBTAINED
        item.img_lab_got.setVisible(gray)
        item.img_lab_gotright.setVisible(gray)
        if c_status == self.OBTAINED:
            btn_text_id = 604029
            btn_text_color = 7171437
        elif c_status == self.UNOBTAINED:
            btn_text_id = 604030
            btn_text_color = 15420639
        else:
            jump_conf = task_utils.get_jump_conf(task_id)
            if not jump_conf:
                btn_text_id = 604031
                btn_text_color = 7183100
            else:
                btn_text_id = 80284
                btn_text_color = 929134
        item.text_go.SetColor(btn_text_color)
        item.text_go.SetString(btn_text_id)

    def _refresh_all_day_reward_task_status(self):
        list_node = self.panel.nd_list
        cnt = list_node.GetItemCount()
        for i in range(cnt):
            if i + 1 == cnt:
                continue
            item = list_node.GetItem(i)
            self._refresh_reward_task_status(item, '1901000', i)

    def _get_u_task_id(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        ui_data = conf.get('cUiData', {})
        return ui_data.get('final_task_id', '1908999')

    def _get_parent_tasks(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        ui_data = conf.get('cUiData', {})
        return ui_data.get('task_id', [])

    def _get_custom_rare_degree(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        ui_data = conf.get('cUiData', [])
        return ui_data.get('RareCustom', [])

    def _get_cur_time(self):
        import time
        return time.time()

    def _is_timer_working(self, timer_id):
        return timer_id is not None

    def _start_update_list_pos_and_size_timer(self, duration):
        if not self._update_list_pos_and_size_timer_id:
            from common.utils.timer import CLOCK
            self._update_list_pos_and_size_timer_id = global_data.game_mgr.register_logic_timer(func=self._update_list_pos_and_size_cb, times=-1, mode=CLOCK, interval=0.02)
        now = self._get_cur_time()
        self._update_list_pos_and_size_end_time = now + duration

    def _stop_update_list_pos_and_size_timer(self):
        if self._update_list_pos_and_size_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._update_list_pos_and_size_timer_id)
        self._update_list_pos_and_size_timer_id = None
        return

    def _update_list_pos_and_size_cb(self):
        now = self._get_cur_time()
        if now > self._update_list_pos_and_size_end_time:
            from common.utils.timer import RELEASE
            self._update_list_pos_and_size_timer_id = None
            return RELEASE
        else:
            list_node = self.panel.nd_list
            list_node.RefreshItemPos()
            self._sync_ultimate_node_position()
            return

    def _get_mission_state(self, idx):
        info = self._reward_mission_anim_info.get(idx, None)
        if info is None:
            return self.MSTATE_COLLAPSED
        else:
            return info[3]
            return

    def _is_mission_animating(self, idx):
        info = self._reward_mission_anim_info.get(idx, None)
        if info is None:
            return (False, 0.0)
        else:
            return (
             info[2] >= info[0], min(1.0, max(float(info[2] - info[0]) / (info[1] - info[0]), 0.0)))
            return

    def _play_mission(self, item, idx):
        self._play_mission_core(item, idx, 'mission', self.MSTATE_COLLAPSED, self.MSTATE_EXPANDED)

    def _stop_mission(self, item, idx):
        self._stop_mission_core(item, idx, 'mission', self.MSTATE_EXPANDED)

    def _play_mission_out(self, item, idx):
        self._play_mission_core(item, idx, 'mission_out', self.MSTATE_EXPANDED, self.MSTATE_COLLAPSED)

    def _stop_mission_out(self, item, idx):
        self._stop_mission_core(item, idx, 'mission_out', self.MSTATE_COLLAPSED)

    def _on_mission_anim_end(self, idx, end_anim_type):
        info = self._reward_mission_anim_info.get(idx, None)
        if info:
            info[2] = info[0] - 1
            info[3] = end_anim_type
        return

    def _play_mission_core(self, item, idx, anim_name, start_anim_type, end_anim_type):
        item.PlayAnimation(anim_name)
        anim_time = item.GetAnimationMaxRunTime(anim_name)

        def tick_func(pass_time, idx=idx):
            info = self._reward_mission_anim_info[idx]
            info[2] += pass_time

        def end_cb(idx=idx):
            self._on_mission_anim_end(idx, end_anim_type)

        now = self._get_cur_time()
        info = [now, now + anim_time, now, start_anim_type]
        self._reward_mission_anim_info[idx] = info
        item.TimerActionByTag(self.ELE_REWARD_MISSION_ANIM_TAG, tick_func, anim_time, end_cb, interval=0.02)
        tick_func(0.0, idx)
        self._start_update_list_pos_and_size_timer(anim_time + 0.1)

    def _stop_mission_core(self, item, idx, anim_name, end_anim_type):
        item.StopAnimation(anim_name, finish_ani=True)
        item.StopTimerActionByTag(self.ELE_REWARD_MISSION_ANIM_TAG)
        self._on_mission_anim_end(idx, end_anim_type)
        list_node = self.panel.nd_list
        list_node.RefreshItemPos()
        self._stop_update_list_pos_and_size_timer()

    def _init_period_sync_utilmate_pos_check(self):
        EST_MAX_SETTLE_TIME = 4
        self._start_sync_ultimate_pos_timer(EST_MAX_SETTLE_TIME)

    def _start_sync_ultimate_pos_timer(self, duration):
        if not self._sync_ultimate_pos_timer_id:
            from common.utils.timer import CLOCK
            self._sync_ultimate_pos_timer_id = global_data.game_mgr.register_logic_timer(func=self._sync_ultimate_pos_cb, times=-1, mode=CLOCK, interval=0.02)
        now = self._get_cur_time()
        self._sync_ultimate_pos_end_time = now + duration

    def _stop_sync_ultimate_pos_timer(self):
        if self._sync_ultimate_pos_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._sync_ultimate_pos_timer_id)
        self._sync_ultimate_pos_timer_id = None
        return

    def _sync_ultimate_pos_cb(self):
        now = self._get_cur_time()
        if now > self._sync_ultimate_pos_end_time:
            from common.utils.timer import RELEASE
            self._sync_ultimate_pos_timer_id = None
            return RELEASE
        else:
            self._sync_ultimate_node_position()
            return

    def _try_do_u_node_in(self):
        if self._u_node_anim_state != self.U_NODE_STATE_IN:
            self._play_u_node_in(self.panel)

    def _try_do_u_node_out(self):
        if self._u_node_anim_state != self.U_NODE_STATE_OUT:
            self._play_u_node_out(self.panel)

    def _play_u_node_in(self, anim_node):
        anim_node.StopAnimation('mech_out')
        anim_node.PlayAnimation('mech_in')
        anim_node.PlayAnimation('loop')
        self._u_node_anim_state = self.U_NODE_STATE_IN

    def _play_u_node_out(self, anim_node):
        anim_node.StopAnimation('mech_in')
        anim_node.PlayAnimation('mech_out')
        self._u_node_anim_state = self.U_NODE_STATE_OUT

    def _is_task_id_of_interest(self, task_id):
        return True

    def _on_task_progress_updated(self, task_id, *args):
        if not self._is_task_id_of_interest(task_id):
            return
        self._refresh_view()

    def _on_task_reward_received(self, task_id, *args):
        if not self._is_task_id_of_interest(task_id):
            return
        self._refresh_view()
        global_data.emgr.refresh_activity_redpoint.emit()