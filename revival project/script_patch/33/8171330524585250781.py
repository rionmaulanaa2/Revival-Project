# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity7DShare.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.effect.ui_effect import set_gray
from logic.gutils import task_utils, item_utils, jump_to_ui_utils
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.share.ShareTipsWidget import ShareTipsWidget
from common.cfg import confmgr
import math
UNAVAILABLE_PIC_PATH = 'gui/ui_res_2/activity/activity_new_domestic/share_7days/pnl_sevendays_%d.png'
AVAILABLE_PIC_PATH = 'gui/ui_res_2/activity/activity_new_domestic/share_7days/pnl_sevendays_gold.png'

class Activity7DShare(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(Activity7DShare, self).__init__(dlg, activity_type)
        self._left_time_timer = None
        return

    def on_init_panel(self):
        self.panel.PlayAnimation('show1')
        self.panel.SetTimeOut(self.panel.GetAnimationMaxRunTime('show1'), lambda : self.panel.PlayAnimation('loop'))
        self.process_event(True)
        if not global_data.player.is_today_shared():
            self._share_tips_widget = ShareTipsWidget(self, self.panel, self.panel.btn_share, tips_text_id=607242, custom_check_func=lambda : not global_data.player.is_today_shared() if global_data.player else None)
        else:
            self._share_tips_widget = None
        self.refresh_reward_data()

        @self.panel.btn_share.btn.unique_callback()
        def OnClick(*args):

            def inform_cb():
                if global_data.player:
                    global_data.player.share()
                    global_data.game_mgr.show_tip(get_text_by_id(2177))

            jump_to_ui_utils.jump_to_share(share_inform_func=inform_cb)

        return

    def refresh_reward_data(self):
        task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        task_conf = task_utils.get_task_conf_by_id(task_id)
        self.panel.list_items.DeleteAllSubItem()
        total_prog = task_conf.get('total_prog', 7)
        if global_data.player.is_today_shared():
            if self._share_tips_widget:
                self._share_tips_widget.on_success_share()
        task_cur_prog = global_data.player.get_task_prog(task_id)
        prog_rewards = task_conf.get('prog_rewards', [])
        for i in range(total_prog - 1, -1, -1):
            prog, reward_id = prog_rewards[i]
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            item_no, count = reward_list[0]
            if global_data.player.has_receive_prog_reward(task_id, prog):
                self._init_unavailable_reward_node(self.panel.list_items, i, item_no, count, has_received=True)
            elif global_data.player.is_prog_reward_receivable(task_id, prog):
                self._init_available_reward_node(self.panel.list_items, i, item_no, count, task_id)
            else:
                self._init_unavailable_reward_node(self.panel.list_items, i, item_no, count, has_received=False)

        self.panel.list_items.RefreshItemPos()
        self.panel.lab_text2_num.SetString(str(task_cur_prog))
        self._refresh_left_time()

    def _init_unavailable_reward_node(self, nd_list, index, item_no, count, has_received=True):
        temp_path = 'activity/activity_new_domestic/i_share_7days_item'
        temp_conf = global_data.uisystem.load_template(temp_path)
        nd_item = nd_list.AddItem(temp_conf, 0)
        path = item_utils.get_lobby_item_pic_by_item_no(item_no)
        name = item_utils.get_lobby_item_name(item_no)
        nd_item.img_item.SetDisplayFrameByPath('', path)
        nd_item.lab_item_name.SetString(name)
        if count == 1:
            nd_item.lab_num.setVisible(False)
        else:
            nd_item.lab_num.SetString(str(count))
        nd_item.btn_1.SetEnable(False)
        if has_received:
            set_gray(nd_item.img_item, True)
            nd_item.img_get.setVisible(True)
        else:
            nd_item.PlayAnimation('loop')
        day = index + 1
        nd_item.lab_days.SetString(str(day))
        pic = UNAVAILABLE_PIC_PATH % (day,)
        nd_item.btn_1.SetFrames('', [pic, pic, pic], True, None)

        @nd_item.nd_item.unique_callback()
        def OnClick(btn, touch, *args):
            global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=touch.getLocation())
            return

        return

    def _init_available_reward_node(self, nd_list, index, item_no, count, task_id):
        temp_path = 'activity/activity_new_domestic/i_share_7days_item_2'
        temp_conf = global_data.uisystem.load_template(temp_path)
        nd_item = nd_list.AddItem(temp_conf, 0)
        nd_item.setLocalZOrder(1)
        path = item_utils.get_lobby_item_pic_by_item_no(item_no)
        name = item_utils.get_lobby_item_name(item_no)
        nd_item.img_item.SetDisplayFrameByPath('', path)
        nd_item.lab_item_name.SetString(name)
        if count == 1:
            nd_item.lab_num.setVisible(False)
        else:
            nd_item.lab_num.SetString(str(count))
        day = index + 1
        nd_item.lab_days.SetString(str(day))
        nd_item.PlayAnimation('loop2')

        @nd_item.btn_2.unique_callback()
        def OnClick(btn, touch, *args):
            global_data.player.receive_task_prog_reward(task_id, day)

    def _refresh_left_time(self):
        if self._left_time_timer:
            global_data.game_mgr.unregister_logic_timer(self._left_time_timer)
        from common.utils.timer import RELEASE, CLOCK

        def _update_left_time():
            now_stamp = tutil.get_server_time()
            close_time = global_data.player.activity_closetime_data.get(self._activity_type, now_stamp)
            left_time = close_time - now_stamp
            if left_time <= 0:
                left_time = 0
            unit_lab = self.panel.lab_text_1
            if left_time > tutil.ONE_DAY_SECONDS:
                left_day = int(math.ceil(left_time / tutil.ONE_DAY_SECONDS))
                self.panel.lab_text1_num.SetString(str(left_day))
                unit_lab.SetString(get_text_by_id(556684).format(''))
            elif left_time > tutil.ONE_HOUR_SECONS:
                left_hour = int(math.ceil(left_time / tutil.ONE_HOUR_SECONS))
                self.panel.lab_text1_num.SetString(str(left_hour))
                unit_lab.SetString(get_text_by_id(81049).format(''))
            else:
                left_minute = int(math.ceil(left_time / tutil.ONE_MINUTE_SECONDS))
                self.panel.lab_text1_num.SetString(str(left_minute))
                unit_lab.SetString(get_text_by_id(165).format(''))
            if left_time <= 0:
                self._left_time_timer = None
                return RELEASE
            else:
                return

        _update_left_time()
        self._left_time_timer = global_data.game_mgr.register_logic_timer(_update_left_time, interval=1, times=-1, mode=CLOCK)

    def on_finalize_panel(self):
        if self._share_tips_widget:
            self._share_tips_widget.destroy()
        self._share_tips_widget = None
        self.process_event(False)
        if self._left_time_timer:
            global_data.game_mgr.unregister_logic_timer(self._left_time_timer)
            self._left_time_timer = None
        return

    def set_show(self, show, is_init=False):
        self.panel.setVisible(show)

    def init_event(self):
        pass

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'receive_task_prog_reward_succ_event': self.task_prog_changed,
           'task_prog_changed': self.task_prog_changed,
           'player_first_success_share_event': self.success_share
           }
        if flag:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        pass

    def task_prog_changed(self, *args):
        global_data.emgr.refresh_activity_redpoint.emit()
        self.refresh_reward_data()

    def success_share(self):
        if self._share_tips_widget:
            self._share_tips_widget.on_success_share()