# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/SimpleFirstWinUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc, init_lobby_bag_item, get_lobby_item_usage, try_use_lobby_item
from common.cfg import confmgr
from logic.gcommon.item import item_sorter
from logic.gutils import mall_utils
from logic.gutils import item_utils
from data.season_update_config import MONEY_DICT
from common.const import uiconst
from logic.gutils.template_utils import init_tempate_mall_i_item

def stop_first_win_time_lab(lab_tips_time):
    lab_tips_time.StopTimerAction()


def update_first_win_time_lab(lab_tips_time, finish_tid=634671, full_time=False):
    from logic.gcommon import time_utility
    is_transparent = [False]
    if global_data.player:
        next_time = global_data.player.get_next_first_win_reward_time()
        cur_time = time_utility.get_server_time()
        if next_time > cur_time:
            end_time = next_time

            def timer_end():
                if lab_tips_time and not lab_tips_time.IsDestroyed():
                    lab_tips_time.StopTimerAction()
                    lab_tips_time.SetString(finish_tid)

            def update_time(pass_time):
                is_transparent[0] = not is_transparent[0]
                cur_time = time_utility.get_server_time()
                left_time = max(end_time - cur_time, 0)
                day, hour, minute, second = time_utility.get_day_hour_minute_second(left_time)
                if full_time:
                    if hour > 0:
                        text = '%02d:%02d:%02d' % (hour, minute, second)
                    else:
                        text = '%02d:%02d' % (minute, second)
                else:
                    text = '%02d:%02d' % (hour, minute)
                    if is_transparent[0]:
                        text = text.replace(':', '<color=0xFEFFFF4C>:</color>')
                    else:
                        text = text.replace(':', '<color=0xFEFFFFFF>:</color>')
                    text_list = [text]

                    def update_trans--- This code section failed: ---

  55       0  LOAD_DEREF            0  'is_transparent'
           3  LOAD_CONST            1  ''
           6  BINARY_SUBSCR    
           7  UNARY_NOT        
           8  LOAD_DEREF            0  'is_transparent'
          11  LOAD_CONST            1  ''
          14  STORE_SUBSCR     

  56      15  LOAD_DEREF            1  'text_list'
          18  LOAD_CONST            1  ''
          21  BINARY_SUBSCR    
          22  STORE_FAST            0  'text1'

  57      25  LOAD_DEREF            0  'is_transparent'
          28  LOAD_CONST            1  ''
          31  BINARY_SUBSCR    
          32  POP_JUMP_IF_FALSE    56  'to 56'

  58      35  LOAD_FAST             0  'text1'
          38  LOAD_ATTR             0  'replace'
          41  LOAD_CONST            2  ':'
          44  LOAD_CONST            3  '<color=0xFEFFFF4C>:</color>'
          47  CALL_FUNCTION_2       2 
          50  STORE_FAST            0  'text1'
          53  JUMP_FORWARD         18  'to 74'

  60      56  LOAD_FAST             0  'text1'
          59  LOAD_ATTR             0  'replace'
          62  LOAD_CONST            2  ':'
          65  LOAD_CONST            4  '<color=0xFEFFFFFF>:</color>'
          68  CALL_FUNCTION_2       2 
          71  STORE_FAST            0  'text1'
        74_0  COME_FROM                '53'

  62      74  LOAD_DEREF            2  'lab_tips_time'
          77  POP_JUMP_IF_FALSE   122  'to 122'
          80  LOAD_DEREF            2  'lab_tips_time'
          83  LOAD_ATTR             1  'IsDestroyed'
          86  CALL_FUNCTION_0       0 
          89  UNARY_NOT        
        90_0  COME_FROM                '77'
          90  POP_JUMP_IF_FALSE   122  'to 122'

  63      93  LOAD_DEREF            2  'lab_tips_time'
          96  LOAD_ATTR             2  'SetString'
          99  LOAD_GLOBAL           3  'get_text_by_id'
         102  LOAD_CONST            5  83397
         105  BUILD_MAP_1           1 
         108  BUILD_MAP_6           6 
         111  STORE_MAP        
         112  CALL_FUNCTION_2       2 
         115  CALL_FUNCTION_1       1 
         118  POP_TOP          
         119  JUMP_FORWARD          0  'to 122'
       122_0  COME_FROM                '119'

  65     122  LOAD_DEREF            2  'lab_tips_time'
         125  LOAD_ATTR             4  'SetTimeOut'
         128  LOAD_CONST            7  0.5
         131  LOAD_DEREF            3  'update_trans'
         134  CALL_FUNCTION_2       2 
         137  POP_TOP          

Parse error at or near `STORE_MAP' instruction at offset 111

                if lab_tips_time and not lab_tips_time.IsDestroyed():
                    lab_tips_time.SetString(get_text_by_id(83397, {'n': text}))
                if left_time <= 0:
                    timer_end()
                    return

            update_time(0)
            lab_tips_time.StopTimerAction()
            lab_tips_time.TimerAction(update_time, end_time, callback=timer_end, interval=1.0)
        else:
            lab_tips_time.SetString(finish_tid)


class SimpleFirstWinUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202306/first_win/i_first_win'
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = {'btn_close.OnClick': 'OnClickClose'
       }

    def on_init_panel(self, *args):
        self.regist_main_ui()
        self.show_rewards()
        update_first_win_time_lab(self.panel.lab_tips_time, finish_tid=634338, full_time=True)

    def show_rewards(self):
        victory_table = confmgr.get('daily_first_victory_conf', default={})
        reward_list = []
        for key, conf in six.iteritems(victory_table):
            reward_item_no = conf.get('reward_item_no', 0)
            if reward_item_no:
                reward_list.append((key, reward_item_no, conf.get('Value', 0)))

        self.panel.list_reward.SetInitCount(len(reward_list))
        for idx, _ in enumerate(reward_list):
            sub_item = self.panel.list_reward.GetItem(idx)
            key, reward_item_no, item_num = reward_list[idx]
            init_tempate_mall_i_item(sub_item, reward_item_no, item_num=item_num, show_tips=True)

    def OnClickClose(self, btn, touch):
        self.close()