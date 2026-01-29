# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySignShare.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.activity.widget import widget
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name
from logic.gutils.client_utils import post_ui_method
MAX_SIGN_CNT = 3
MAX_SHARE_CNT = 3

@widget('AsyncTaskListWidget', 'DescribeWidget')
class ActivitySignShare(ActivityBase):

    def on_init_panel(self):
        super(ActivitySignShare, self).on_init_panel()
        conf = confmgr.get('c_activity_config', self._activity_type)
        self._task_info_list = conf.get('cUiData', {}).get('task_info', [])
        self.__process_event(True)
        self._init_tasks()
        self._on_update_task()

    def __process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self._on_update_task,
           'receive_task_reward_succ_event': self._on_update_task,
           'receive_task_prog_reward_succ_event': self._on_update_task
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _init_tasks(self):
        sign_task_id = self._task_info_list[0]
        sign_reward_list = task_utils.get_task_reward_list(sign_task_id)
        item_id = sign_reward_list[0][0]
        sign_reward_name = get_lobby_item_name(item_id)
        self.panel.nd_sign.lab_emotion.SetString(sign_reward_name)
        self.panel.lab_sign_03.SetString(sign_reward_name)
        self.panel.lab_sign_01.SetString(get_text_by_id(907154).format(MAX_SIGN_CNT))
        share_task_id = self._task_info_list[1]
        share_reward_list = task_utils.get_task_reward_list(share_task_id)
        item_id = share_reward_list[0][0]
        share_reward_name = get_lobby_item_name(item_id)
        self.panel.nd_share.lab_action.SetString(share_reward_name)
        self.panel.lab_share_03.SetString(share_reward_name)
        self.panel.lab_share_01.SetString(get_text_by_id(907155).format(MAX_SHARE_CNT))

        @self.panel.btn_click_01.unique_callback()
        def OnClick(btn, touch, _task_id=sign_task_id, *args):
            prog = global_data.player.get_task_prog(_task_id)
            max_prog = task_utils.get_total_prog(_task_id)
            if prog >= max_prog and not bool(global_data.player.has_receive_reward(_task_id)):
                global_data.player.receive_task_reward(_task_id)

        @self.panel.btn_click_02.unique_callback()
        def OnClick(btn, touch, _task_id=share_task_id, *args):
            prog = global_data.player.get_task_prog(_task_id)
            max_prog = task_utils.get_total_prog(_task_id)
            if prog >= max_prog and not bool(global_data.player.has_receive_reward(_task_id)):
                global_data.player.receive_task_reward(_task_id)

    def set_widget_done(self, item_widget, is_done):
        item_widget.img_love_01.setVisible(not is_done)
        item_widget.img_love_02.setVisible(is_done)

    @post_ui_method
    def _on_update_task(self, *args):
        sign_task_id = self._task_info_list[0]
        prog = global_data.player.get_task_prog(sign_task_id)
        max_prog = task_utils.get_total_prog(sign_task_id)
        sign_total_cnt = min(max_prog, MAX_SIGN_CNT)
        sign_done_cnt = min(prog, MAX_SIGN_CNT)
        if sign_done_cnt >= sign_total_cnt and bool(global_data.player.has_receive_reward(sign_task_id)):
            self.panel.nd_signed_complete.setVisible(True)
            self.panel.nd_signed.setVisible(False)
            self.panel.nd_sign.temp_red.setVisible(False)
        else:
            self.panel.nd_signed_complete.setVisible(False)
            self.panel.nd_signed.setVisible(True)
            self.panel.nd_sign.temp_red.setVisible(sign_done_cnt >= sign_total_cnt)
            sub_sign_list = self.panel.list_heart_01
            sub_sign_list.SetInitCount(0)
            sub_sign_list.SetInitCount(sign_total_cnt)
            for i in range(sign_total_cnt):
                item_widget = sub_sign_list.GetItem(i)
                if i < sign_done_cnt:
                    self.set_widget_done(item_widget, True)
                else:
                    self.set_widget_done(item_widget, False)

        share_task_id = self._task_info_list[1]
        prog = global_data.player.get_task_prog(share_task_id)
        max_prog = task_utils.get_total_prog(share_task_id)
        share_total_cnt = min(max_prog, MAX_SHARE_CNT)
        share_done_cnt = min(prog, MAX_SHARE_CNT)
        if share_done_cnt >= share_total_cnt and bool(global_data.player.has_receive_reward(share_task_id)):
            self.panel.nd_shared_complete.setVisible(True)
            self.panel.nd_shared.setVisible(False)
            self.panel.nd_share.temp_red.setVisible(False)
        else:
            self.panel.nd_shared_complete.setVisible(False)
            self.panel.nd_shared.setVisible(True)
            self.panel.nd_share.temp_red.setVisible(share_done_cnt >= share_total_cnt)
            sub_share_list = self.panel.list_heart_02
            sub_share_list.SetInitCount(0)
            sub_share_list.SetInitCount(share_total_cnt)
            for i in range(share_total_cnt):
                item_widget = sub_share_list.GetItem(i)
                if i < share_done_cnt:
                    self.set_widget_done(item_widget, True)
                else:
                    self.set_widget_done(item_widget, False)

    def on_finalize_panel(self):
        self.__process_event(False)
        super(ActivitySignShare, self).on_finalize_panel()