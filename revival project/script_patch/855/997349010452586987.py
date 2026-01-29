# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/NewAlphaPlan/AlphaPlanNewbieAttendBase.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc, get_lobby_item_rare_degree_pic_by_item_no, get_item_rare_degree, get_lobby_item_type
from logic.comsys.effect.ui_effect import set_gray
from logic.gcommon.item import lobby_item_type as lbt
REWARD_START_ID = 18000000
LIST_NODE_COUNT = 7
REWARD_CNT = LIST_NODE_COUNT + 1
CIRCLE_PIC_PREFIX = 'gui/ui_res_2/activity/activity_new_domestic/new_sign_in/'
CIRCLE_PIC_INFO_BLUE = (CIRCLE_PIC_PREFIX + 'img_new_eightdays_item_blue.png', CIRCLE_PIC_PREFIX + 'img_new_eightdays_item_blue_02.png')
CIRCLE_PIC_INFO_GREEN = (CIRCLE_PIC_PREFIX + 'img_new_eightdays_item_green_01.png', CIRCLE_PIC_PREFIX + 'img_new_eightdays_item_green_02.png')
CIRCLE_PIC_INFO_PURPLE = (CIRCLE_PIC_PREFIX + 'img_new_eightdays_item_purple.png', CIRCLE_PIC_PREFIX + 'img_new_eightdays_item_purple_02.png')
CIRCLE_PIC_INFO_ORANGE = (CIRCLE_PIC_PREFIX + 'img_new_eightdays_item_gold.png', CIRCLE_PIC_PREFIX + 'img_new_eightdays_item_gold_02.png')
from logic.gcommon.item.item_const import RARE_DEGREE_1, RARE_DEGREE_2, RARE_DEGREE_3, RARE_DEGREE_4
CIRCLE_PIC_INFO_MAP = {RARE_DEGREE_1: CIRCLE_PIC_INFO_GREEN,
   RARE_DEGREE_2: CIRCLE_PIC_INFO_BLUE,
   RARE_DEGREE_3: CIRCLE_PIC_INFO_PURPLE,
   RARE_DEGREE_4: CIRCLE_PIC_INFO_ORANGE
   }

class AlphaPlanNewbieAttendBase:
    DELAY_REWARD_SHOW_INTERVAL = 2
    REWARD_SHOW_INTERVAL_TAG = 31415925
    FPS = 30
    ACTIVITY_TYPE = '53'

    def _init_list_reward(self, list_node, eighth_node, get_btn, hide_ele):
        list_node.SetInitCount(LIST_NODE_COUNT)
        self._reward_node_list = []
        self._reward_node_list.extend(list_node.GetAllItem())
        self._reward_node_list.append(eighth_node)
        self._get_btn = get_btn
        self._ui_item_rare_degree = None
        for ele_node in self._reward_node_list:
            if hide_ele:
                ele_node.setVisible(False)
            ele_node.btn_img_circle.SetEnableTouch(False)
            ele_node.btn_img_circle.EnableCustomState(True)
            ele_node.btn_img_date.SetEnableTouch(False)
            ele_node.btn_img_date.EnableCustomState(True)
            ele_node.btn_lab_name.SetEnableTouch(False)
            ele_node.btn_lab_name.EnableCustomState(True)
            ele_node.RecordAnimationNodeState('show1')
            ele_node.RecordAnimationNodeState('loop')
            ele_node.RecordAnimationNodeState('loop2')

        return

    def _play_reward_show(self, idx, tag=None):
        if idx < 0 or idx >= len(self._reward_node_list):
            return
        else:
            ele_node = self._get_reward_node(idx)
            if not ele_node:
                return
            ele_node.PlayAnimation('show1')
            ele_node.setVisible(True)
            if tag is None:
                tag = self.REWARD_SHOW_INTERVAL_TAG
            self.panel.DelayCallWithTag(self.DELAY_REWARD_SHOW_INTERVAL / self.FPS, self._play_reward_show, tag, idx - 1)
            return

    def _get_reward_node(self, idx):
        if idx < 0 or idx >= len(self._reward_node_list):
            return None
        else:
            return self._reward_node_list[idx]

    def _refresh_list_reward(self):
        history_day = global_data.player.get_history_attend_days()
        has, _ = global_data.player.has_attendable_day_no()
        self._get_btn.SetEnable(has)
        reward_data = confmgr.get('common_reward_data')
        for i, item in enumerate(self._reward_node_list):
            target_day_no = i + 1
            got = global_data.player.is_newbie_day_attended(target_day_no)
            can_get = global_data.player.try_get_newbie_attend_reward(get_reward=False, day_no=target_day_no)
            reward_id = str(REWARD_START_ID + i + 1)
            item_no, item_cnt = reward_data.get(reward_id, {}).get('reward_list', ())[0]
            self._refresh_reward_node(item, target_day_no, item_no, item_cnt, i, got, can_get)

    def _refresh_reward_node(self, node, day_no, item_no, item_cnt, item_idx, got, can_get):
        item = node
        item_type = get_lobby_item_type(item_no)
        show_degree_frame = item_type in [lbt.L_ITEM_TYPE_MECHA, lbt.L_ITEM_TYPE_MECHA_SKIN, lbt.L_ITEM_MECHA_SFX, lbt.L_ITEM_TYPE_ICON]
        pic_path = get_lobby_item_pic_by_item_no(item_no)
        item.item_other.SetDisplayFrameByPath('', pic_path)
        item.img_item_out.SetDisplayFrameByPath('', pic_path)
        item.cut_item_out.SetMaskFrameByPath('', pic_path)
        item.img_frame.SetDisplayFrameByPath('', get_lobby_item_rare_degree_pic_by_item_no(item_no, item_cnt))
        degree = self._get_item_rare_degree(item_idx, item_no, item_cnt)
        circle_pic_info = CIRCLE_PIC_INFO_MAP.get(degree, CIRCLE_PIC_INFO_GREEN)
        normal_circle_pic, gray_circle_pic = circle_pic_info[0], circle_pic_info[1]
        from common.utils.cocos_utils import CCRect
        item.btn_img_circle.SetFrames('', [normal_circle_pic, normal_circle_pic, gray_circle_pic])
        item.img_frame.setVisible(show_degree_frame)
        item.cut_item_out.setVisible(not show_degree_frame)
        name = get_lobby_item_name(item_no)
        item.btn_lab_name.SetText(name)
        if item_cnt > 1:
            num_txt = 'x%s' % item_cnt
        else:
            num_txt = ''
        item.lab_num.SetString(num_txt)
        if item_type == lbt.L_ITEM_TYPE_HEAD_FRAME:
            scale = 0.48
            show_d_bg = True
        else:
            scale = 0.3
            show_d_bg = False
        item.cut_item_out.setScaleX(scale)
        item.cut_item_out.setScaleY(scale)
        item.head_bg.setVisible(show_d_bg)
        if got:
            set_gray(item.img_item_out, True)
            set_gray(item.img_frame, True)
            set_gray(item.item_other, True)
            item.btn_img_circle.SetShowEnable(False)
            item.btn_img_date.SetShowEnable(False)
            item.btn_lab_name.SetShowEnable(False)
            item.img_check.setVisible(True)
            item.btn_img_circle_1.SetDisplayFrameByPath('', gray_circle_pic)
        else:
            set_gray(item.img_item_out, False)
            set_gray(item.img_frame, False)
            set_gray(item.item_other, False)
            item.btn_img_circle.SetSelect(can_get)
            item.btn_img_date.SetSelect(can_get)
            item.btn_lab_name.SetSelect(can_get)
            item.img_check.setVisible(False)
            item.btn_img_circle_1.SetDisplayFrameByPath('', normal_circle_pic)
        item.StopAnimation('loop')
        item.StopAnimation('loop2')
        item.RecoverAnimationNodeState('loop')
        item.RecoverAnimationNodeState('loop2')
        item.RecoverAnimationNodeState('show1')
        if not item.IsPlayingAnimation('show1'):
            item.PlayAnimation('show1')
            item.StopAnimation('show1', finish_ani=True)
        if can_get:
            item.PlayAnimation('loop')
        elif not got:
            item.PlayAnimation('loop2')

        @item.btn_lick.unique_callback()
        def OnClick(btn, touch, day_no=day_no, can_get=can_get, item_no=item_no, item_num=item_cnt):
            if not can_get:
                x, y = btn.GetPosition()
                wpos = btn.ConvertToWorldSpace(x, y)
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, item_num=item_num)
            else:
                global_data.player.try_get_newbie_attend_reward(True, day_no=day_no)
            return

    def _get_item_rare_degree(self, item_idx, item_no, item_cnt):
        if self._ui_item_rare_degree is None:
            conf = confmgr.get('c_activity_config', self.ACTIVITY_TYPE)
            ui_data = conf.get('cUiData', {})
            self._ui_item_rare_degree = ui_data.get('RareCustom', [])
        if item_idx >= len(self._ui_item_rare_degree):
            log_error('AlphaPlanNewbieAttendBase item_idx greater than rare_degree_custom_list')
            return 0
        else:
            return self._ui_item_rare_degree[item_idx]

    def on_click_get_reward(self, *args):
        global_data.player.try_get_newbie_attend_reward(True, day_no=None)
        return

    def _on_update_newbie_attend_reward(self, *args):
        self._refresh_list_reward()
        self._refresh_progress()

    def _refresh_progress(self):
        return
        history_day = global_data.player.get_history_attend_days()
        from logic.gcommon.common_const.activity_const import ALPHA_PLAN_ATTEND_DAYS
        day = min(history_day, ALPHA_PLAN_ATTEND_DAYS)
        day = max(day, 0)
        progress_vals = [
         0, 6, 18, 31, 43, 56, 69, 81, 100]
        progress = 0
        if day >= 0 and day < len(progress_vals):
            progress = progress_vals[day]
        self._progress_node.SetPercent(progress)