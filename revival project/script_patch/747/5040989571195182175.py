# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityChristmas/ActivityChristmasShare.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.activity.widget.GlobalAchievementWidget import GlobalAchievementWidget
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils

class ChristmasGlobalShare(GlobalAchievementWidget):

    def refresh_reward_content--- This code section failed: ---

  15       0  LOAD_GLOBAL           0  'len'
           3  LOAD_FAST             0  'self'
           6  LOAD_ATTR             1  'children_ids'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            2  'n'

  16      15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'panel'
          21  LOAD_ATTR             3  'list_reward'
          24  LOAD_ATTR             4  'SetInitCount'
          27  LOAD_FAST             2  'n'
          30  CALL_FUNCTION_1       1 
          33  POP_TOP          

  17      34  SETUP_LOOP          331  'to 368'
          37  LOAD_GLOBAL           5  'range'
          40  LOAD_FAST             2  'n'
          43  CALL_FUNCTION_1       1 
          46  GET_ITER         
          47  FOR_ITER            317  'to 367'
          50  STORE_FAST            3  'i'

  18      53  LOAD_FAST             0  'self'
          56  LOAD_ATTR             1  'children_ids'
          59  LOAD_FAST             3  'i'
          62  BINARY_SUBSCR    
          63  STORE_FAST            4  'achieve_id'

  19      66  LOAD_GLOBAL           6  'confmgr'
          69  LOAD_ATTR             7  'get'
          72  LOAD_CONST            1  'global_achieve_data'
          75  LOAD_FAST             4  'achieve_id'
          78  LOAD_CONST            2  'iRewardID'
          81  LOAD_CONST            3  'default'
          84  LOAD_CONST            4  ''
          87  CALL_FUNCTION_259   259 
          90  STORE_FAST            5  'reward_id'

  20      93  LOAD_CONST            4  ''
          96  LOAD_CONST            5  ('ITEM_UNRECEIVED', 'ITEM_RECEIVED', 'ITEM_UNGAIN')
          99  IMPORT_NAME           8  'logic.gcommon.item.item_const'
         102  IMPORT_FROM           9  'ITEM_UNRECEIVED'
         105  STORE_FAST            6  'ITEM_UNRECEIVED'
         108  IMPORT_FROM          10  'ITEM_RECEIVED'
         111  STORE_FAST            7  'ITEM_RECEIVED'
         114  IMPORT_FROM          11  'ITEM_UNGAIN'
         117  STORE_FAST            8  'ITEM_UNGAIN'
         120  POP_TOP          

  21     121  LOAD_GLOBAL          12  'global_data'
         124  LOAD_ATTR            13  'player'
         127  LOAD_ATTR            14  'get_gl_reward_receive_state'
         130  LOAD_FAST             4  'achieve_id'
         133  CALL_FUNCTION_1       1 
         136  STORE_FAST            9  'status'

  22     139  LOAD_FAST             0  'self'
         142  LOAD_ATTR             2  'panel'
         145  LOAD_ATTR             3  'list_reward'
         148  LOAD_ATTR            15  'GetItem'
         151  LOAD_FAST             3  'i'
         154  CALL_FUNCTION_1       1 
         157  STORE_FAST           10  'item'

  23     160  LOAD_FAST             9  'status'
         163  LOAD_FAST             6  'ITEM_UNRECEIVED'
         166  COMPARE_OP            2  '=='
         169  POP_JUMP_IF_FALSE   193  'to 193'

  24     172  LOAD_GLOBAL          16  'False'
         175  STORE_FAST           11  'show_tips'

  25     178  LOAD_FAST             4  'achieve_id'
         181  LOAD_LAMBDA              '<code_object <lambda>>'
         184  MAKE_FUNCTION_1       1 
         187  STORE_FAST           12  'callback'
         190  JUMP_FORWARD         12  'to 205'

  27     193  LOAD_GLOBAL          17  'True'
         196  STORE_FAST           11  'show_tips'

  28     199  LOAD_CONST            0  ''
         202  STORE_FAST           12  'callback'
       205_0  COME_FROM                '190'

  30     205  LOAD_GLOBAL          19  'template_utils'
         208  LOAD_ATTR            20  'init_common_reward_item'
         211  LOAD_FAST            10  'item'
         214  LOAD_FAST             5  'reward_id'
         217  LOAD_FAST            11  'show_tips'
         220  LOAD_FAST            12  'callback'
         223  CALL_FUNCTION_4       4 
         226  POP_TOP          

  32     227  LOAD_GLOBAL          12  'global_data'
         230  LOAD_ATTR            13  'player'
         233  LOAD_ATTR            14  'get_gl_reward_receive_state'
         236  LOAD_FAST             4  'achieve_id'
         239  CALL_FUNCTION_1       1 
         242  STORE_FAST            9  'status'

  33     245  LOAD_FAST             9  'status'
         248  LOAD_FAST             8  'ITEM_UNGAIN'
         251  COMPARE_OP            2  '=='
         254  POP_JUMP_IF_FALSE   260  'to 260'

  34     257  CONTINUE             47  'to 47'

  35     260  LOAD_FAST             9  'status'
         263  LOAD_FAST             6  'ITEM_UNRECEIVED'
         266  COMPARE_OP            2  '=='
         269  POP_JUMP_IF_FALSE   288  'to 288'

  36     272  LOAD_FAST            10  'item'
         275  LOAD_ATTR            21  'PlayAnimation'
         278  LOAD_CONST            7  'get_tips'
         281  CALL_FUNCTION_1       1 
         284  POP_TOP          
         285  JUMP_BACK            47  'to 47'

  37     288  LOAD_FAST             9  'status'
         291  LOAD_FAST             7  'ITEM_RECEIVED'
         294  COMPARE_OP            2  '=='
         297  POP_JUMP_IF_FALSE    47  'to 47'

  38     300  LOAD_FAST            10  'item'
         303  LOAD_ATTR            22  'StopAnimation'
         306  LOAD_CONST            7  'get_tips'
         309  CALL_FUNCTION_1       1 
         312  POP_TOP          

  39     313  LOAD_FAST            10  'item'
         316  LOAD_ATTR            23  'nd_get_tips'
         319  LOAD_ATTR            24  'setVisible'
         322  LOAD_GLOBAL          16  'False'
         325  CALL_FUNCTION_1       1 
         328  POP_TOP          

  40     329  LOAD_FAST            10  'item'
         332  LOAD_ATTR            25  'nd_get'
         335  LOAD_ATTR            24  'setVisible'
         338  LOAD_GLOBAL          17  'True'
         341  CALL_FUNCTION_1       1 
         344  POP_TOP          

  41     345  LOAD_FAST            10  'item'
         348  LOAD_ATTR            26  'nd_lock'
         351  LOAD_ATTR            24  'setVisible'
         354  LOAD_GLOBAL          17  'True'
         357  CALL_FUNCTION_1       1 
         360  POP_TOP          
         361  JUMP_BACK            47  'to 47'
         364  JUMP_BACK            47  'to 47'
         367  POP_BLOCK        
       368_0  COME_FROM                '34'
         368  LOAD_CONST            0  ''
         371  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 367

    def update_progress(self):
        percent = min(100, self.local_num * 2.875e-05 + 3.75)
        self.panel.prog_number_1.SetPercentage(percent)
        num_percent = int(self.local_num * 100.0 / self.share_prog[-1])
        num_percent = min(100, max(1, num_percent))
        self.panel.lab_progress_number_2.SetString('%d%%' % num_percent)


class ActivityChristmasShare(ActivityBase):

    def on_init_panel(self):
        super(ActivityChristmasShare, self).on_init_panel()
        self.ui_data = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        self._parent_achieve_id = self.ui_data.get('global_achieve_id')[0]
        self.widget_map = {}
        self.init_task_list()
        self.init_global_achieve_widget()
        self.init_countdown_widget()

        @self.panel.btn_go.callback()
        def OnClick(*args):
            from logic.gutils.jump_to_ui_utils import jump_to_lottery
            jump_to_lottery('33')

    def on_finalize_panel(self):
        for widget in six_ex.values(self.widget_map):
            widget.on_finalize_panel()

        self.widget_map = None
        return

    def init_task_list(self):
        from logic.comsys.activity.widget.TaskListWidget import TaskListWidget
        self.widget_map['task_list'] = TaskListWidget(self.panel, self._activity_type)

    def init_global_achieve_widget(self):
        extra_info = {'sim_interval': 60
           }
        self.widget_map['global_achieve'] = ChristmasGlobalShare(self.panel.item_progress, self._activity_type, extra_info)

    def init_countdown_widget(self):
        from logic.comsys.activity.widget.CountdownWidget import CountdownWidget
        self.widget_map['countdown'] = CountdownWidget(self.panel.lab_time, self._activity_type)