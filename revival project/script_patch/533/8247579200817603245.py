# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewReturn/ActivityNewReturnGift.py
from __future__ import absolute_import
import six
from six.moves import range
import cc
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
from logic.gcommon.time_utility import get_server_time
from logic.comsys.activity.ActivityTemplate import ActivityBase

class ActivityNewReturnGift(ActivityBase):
    LAB_LEFT_TIME_NAME = 'lab_rest_time'

    def __init__(self, dlg, activity_type):
        super(ActivityNewReturnGift, self).__init__(dlg, activity_type)
        self._timer = None
        self._timer_cb = {}
        self._task_id = None
        self._left_time_node = None
        self._before_init_panel()
        return

    def _before_init_panel(self):
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.reward_list = task_utils.get_task_reward_list(self._task_id)
        self.panel.list_items.SetInitCount(len(self.reward_list))
        self._init_reward_lst()

    def on_init_panel(self):
        self._close_time = global_data.player.activity_closetime_data.get(self._activity_type, get_server_time())
        self._process_event(True)
        self._init_ui_event()
        self._left_time_node = getattr(self.panel, self.LAB_LEFT_TIME_NAME) if self.LAB_LEFT_TIME_NAME else None
        if self._left_time_node:
            self._register_timer()
            self._timer_cb[0] = lambda : self._refresh_left_time()
            self._refresh_left_time()
        self._custom_init_panel()
        return

    def set_show(self, show, is_init=False):
        super(ActivityNewReturnGift, self).set_show(show, is_init)
        if not show:
            return
        self.panel.PlayAnimation('show')
        self.panel.SetTimeOut(2, lambda : self.panel.PlayAnimation('loop'))

        def play_item_anim(idx):
            item = self.panel.list_items.GetItem(idx)
            item.setVisible(True)
            item.PlayAnimation('show')
            item.PlayAnimation('loop')

        item_num = self.panel.list_items.GetItemCount()
        act_lst = []
        for idx in range(item_num):
            if idx == 0:
                delay = 0.2 if 1 else 0.04
                act_lst.append(cc.DelayTime.create(delay))
                act_lst.append(cc.CallFunc.create(lambda item_idx=idx: play_item_anim(item_idx)))

        if act_lst:
            self.panel.runAction(cc.Sequence.create(act_lst))

    def _refresh_left_time(self):
        now_time = get_server_time()
        left_time_delta = self._close_time - now_time
        is_ending, left_text, left_time, left_unit = template_utils.get_left_info(left_time_delta)
        if not is_ending:
            day_txt = get_text_by_id(left_text) + str(left_time) + get_text_by_id(left_unit)
        else:
            day_txt = get_text_by_id(left_text)
        self._left_time_node.SetString(day_txt)

    def _init_reward_lst(self, *args):
        for idx, reward_info in enumerate(self.reward_list):
            item_no, item_num = reward_info
            tmp_item = self.panel.list_items.GetItem(idx)
            item_name = get_lobby_item_name(item_no)
            tmp_item.lab_name.SetString(item_name)
            res_path = get_lobby_item_pic_by_item_no(item_no)
            tmp_item.img_item.SetDisplayFrameByPath('', res_path)
            tmp_item.lab_num.SetString('x{}'.format(item_num))

        self._update_receive_state()

    def _update_receive_state(self, *args):
        if not global_data.player:
            pass
        is_received = global_data.player.is_all_received_reward(self._task_id)
        self.panel.btn_get.SetEnable(not is_received)
        txt = 604029 if is_received else 604030
        self.panel.btn_get.SetText(txt)
        all_item = self.panel.list_items.GetAllItem()
        for tmp_item in all_item:
            tmp_item.nd_got.setVisible(is_received)

        global_data.emgr.refresh_activity_redpoint.emit()

    def _init_ui_event(self):

        @self.panel.btn_get.unique_callback()
        def OnClick(*args):
            now_time = get_server_time()
            left_time_delta = self._close_time - now_time
            if left_time_delta <= 0:
                global_data.game_mgr.show_tip(get_text_by_id(607911))
                return
            if not global_data.player or global_data.player.has_receive_reward(self._task_id):
                return
            can_receive = global_data.player.is_task_reward_receivable(self._task_id)
            if can_receive:
                global_data.player.receive_task_reward(self._task_id)

    def _register_timer(self):
        from common.utils.timer import CLOCK
        self._unregister_timer()
        self._timer = global_data.game_mgr.register_logic_timer(self._second_callback, interval=1, times=-1, mode=CLOCK)

    def _unregister_timer(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
        self._timer = None
        self._timer_cb = {}
        return

    def _second_callback(self):
        for timer_key, cb_func in six.iteritems(self._timer_cb):
            cb_func()

    def _process_event(self, is_bind):
        e_conf = {'receive_task_reward_succ_event': self._update_receive_state
           }
        if is_bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def _custom_init_panel(self):
        pass

    def on_finalize_panel(self):
        self._process_event(False)
        self._unregister_timer()