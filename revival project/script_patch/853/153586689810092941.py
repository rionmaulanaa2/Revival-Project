# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityShare.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gutils import template_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import task_utils
from common.utils.timer import CLOCK
from logic.gcommon.time_utility import get_simply_time, ONE_DAY_SECONDS

class ActivityShare(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityShare, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()
        self._register_timer()

    def on_finalize_panel(self):
        self.process_event(False)
        self._unregister_timer()

    def init_parameters(self):
        self._parent_task = None
        self._timer = None
        self._timer_cb = {}
        self._left_seconds = 0
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._refresh_btn
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self.on_init_panel()

    def _register_timer(self):
        self._unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def _unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = None
        self._timer_cb = {}
        return

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def on_init_panel(self):
        from logic.gutils import task_utils
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        reward_id = ''
        if conf['cTask']:
            task_list = activity_utils.parse_task_list(conf['cTask'])
            if len(task_list) <= 0:
                return
            self._parent_task = task_list[0]
            tmp_reward_id = task_utils.get_task_reward(self._parent_task)
            if tmp_reward_id:
                reward_id = str(tmp_reward_id) if 1 else reward_id
            if reward_id:
                template_utils.init_common_reward_list(self.panel.list_reward, reward_id)
            return self._parent_task or None

        def callback--- This code section failed: ---

  85       0  LOAD_DEREF            0  'task_utils'
           3  LOAD_ATTR             0  'get_raw_left_open_time'
           6  LOAD_DEREF            1  'self'
           9  LOAD_ATTR             1  '_parent_task'
          12  CALL_FUNCTION_1       1 
          15  STORE_FAST            0  'left_time'

  86      18  STORE_FAST            1  'close_left_time'
          21  COMPARE_OP            4  '>'
          24  POP_JUMP_IF_FALSE    70  'to 70'

  87      27  LOAD_DEREF            1  'self'
          30  LOAD_ATTR             2  'panel'
          33  LOAD_ATTR             3  'lab_time'
          36  LOAD_ATTR             4  'SetString'
          39  LOAD_GLOBAL           5  'get_text_by_id'
          42  LOAD_CONST            2  607014
          45  CALL_FUNCTION_1       1 
          48  LOAD_ATTR             6  'format'
          51  LOAD_GLOBAL           7  'get_simply_time'
          54  LOAD_FAST             0  'left_time'
          57  CALL_FUNCTION_1       1 
          60  CALL_FUNCTION_1       1 
          63  CALL_FUNCTION_1       1 
          66  POP_TOP          
          67  JUMP_FORWARD         71  'to 141'

  89      70  LOAD_GLOBAL           8  'ONE_DAY_SECONDS'
          73  LOAD_FAST             0  'left_time'
          76  BINARY_ADD       
          77  STORE_FAST            1  'close_left_time'

  90      80  LOAD_FAST             1  'close_left_time'
          83  LOAD_CONST            1  ''
          86  COMPARE_OP            1  '<='
          89  POP_JUMP_IF_FALSE   101  'to 101'
          92  LOAD_CONST            1  ''
          95  STORE_FAST            1  'close_left_time'
          98  JUMP_FORWARD          0  'to 101'
       101_0  COME_FROM                '98'

  91     101  LOAD_DEREF            1  'self'
         104  LOAD_ATTR             2  'panel'
         107  LOAD_ATTR             3  'lab_time'
         110  LOAD_ATTR             4  'SetString'
         113  LOAD_GLOBAL           5  'get_text_by_id'
         116  LOAD_CONST            3  607130
         119  CALL_FUNCTION_1       1 
         122  LOAD_ATTR             6  'format'
         125  LOAD_GLOBAL           7  'get_simply_time'
         128  LOAD_FAST             1  'close_left_time'
         131  CALL_FUNCTION_1       1 
         134  CALL_FUNCTION_1       1 
         137  CALL_FUNCTION_1       1 
         140  POP_TOP          
       141_0  COME_FROM                '67'

Parse error at or near `STORE_FAST' instruction at offset 18

        self._timer_cb[0] = callback
        callback()
        self._refresh_btn(self._parent_task)

    def _refresh_btn(self, task_id, *args):
        if task_id != self._parent_task:
            return
        cur_param_index = 0
        activity_type = self._activity_type
        func_list = confmgr.get('c_activity_config', activity_type, 'arrCondition', default=[])
        nRet = 0
        text_id = 0
        for idx in range(len(func_list)):
            nRet, text_id = self.exec_custom_condition(idx)
            cur_param_index = idx
            if nRet >= 1:
                break

        btn = self.panel.btn_get

        @btn.unique_callback()
        def OnClick(btn, touch):
            if nRet:
                self.exec_custom_func(cur_param_index)
            else:
                self.exec_custom_func(cur_param_index + 1)

        activity_utils.set_btn_text(btn, nRet, text_id)
        global_data.player.read_activity_list(self._activity_type)