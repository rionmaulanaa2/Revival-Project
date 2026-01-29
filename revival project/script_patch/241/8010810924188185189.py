# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/intimacy/IntimacyHistoricalEventUI.py
import time
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from logic.gutils import role_head_utils
from logic.gutils.role_head_utils import PlayerInfoManager
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from common.const.property_const import U_ID, C_NAME
from logic.gcommon.const import INTIMACY_NAME_MAP, IDX_INTIMACY_LV, IDX_INTIMACY_TYPE, IDX_INTIMACY_NAME, INTIMACY_MEMORY_EVENT_BUILT, ALL_INTIMACY_MEMORY_EVENTS, INTIMACY_HISTORICAL_EVENT_KEY, INTIMACY_MEMORY_EVENT_RELATION_DAY, INTIMACY_MEMORY_SPECIAL_RELATION_EVENTS
from logic.gutils.intimacy_utils import init_intimacy_event_bar, init_intimacy_event_frame, init_intimacy_pic
from logic.gcommon import time_utility as tutil
from logic.comsys.share.IntimacyHistoricalEventShareCreator import IntimacyHistoricalEventShareCreator
from common.utils.cocos_utils import ccp
TEMPLATE_LIST = [
 'friend/i_intimacy_historical_event_line1',
 'friend/i_intimacy_historical_event_line2',
 'friend/i_intimacy_historical_event_line3',
 'friend/i_intimacy_historical_event_line4']

def get_data_list--- This code section failed: ---

  27       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'intimacy_memory_data'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            1  'intimacy_memory_conf'

  28      15  BUILD_MAP_0           0 
          18  STORE_FAST            2  'intimacy_event_data_dict'

  29      21  LOAD_GLOBAL           2  'str'
          24  LOAD_FAST             1  'intimacy_memory_conf'
          27  LOAD_ATTR             1  'get'
          30  LOAD_GLOBAL           3  'INTIMACY_MEMORY_EVENT_RELATION_DAY'
          33  CALL_FUNCTION_1       1 
          36  LOAD_ATTR             1  'get'
          39  LOAD_CONST            2  'priority'
          42  CALL_FUNCTION_1       1 
          45  CALL_FUNCTION_1       1 
          48  STORE_FAST            3  'realation_day_priority'

  31      51  STORE_FAST            3  'realation_day_priority'
          54  BINARY_SUBSCR    
          55  STORE_FAST            4  'build_time'

  32      58  LOAD_GLOBAL           4  'int'
          61  LOAD_GLOBAL           5  'tutil'
          64  LOAD_ATTR             6  'get_day_start_timestamp'
          67  LOAD_FAST             4  'build_time'
          70  CALL_FUNCTION_1       1 
          73  CALL_FUNCTION_1       1 
          76  STORE_DEREF           0  'intimacy_begin_timestamp'

  33      79  BUILD_MAP_1           1 
          82  LOAD_GLOBAL           4  'int'
          85  LOAD_FAST             4  'build_time'
          88  CALL_FUNCTION_1       1 
          91  LOAD_CONST            4  'time'
          94  STORE_MAP        
          95  LOAD_FAST             0  'data'
          98  LOAD_GLOBAL           7  'INTIMACY_MEMORY_EVENT_BUILT'
         101  STORE_SUBSCR     

  35     102  SETUP_LOOP          389  'to 494'
         105  LOAD_GLOBAL           8  'enumerate'
         108  LOAD_FAST             0  'data'
         111  CALL_FUNCTION_1       1 
         114  GET_ITER         
         115  FOR_ITER            375  'to 493'
         118  UNPACK_SEQUENCE_2     2 
         121  STORE_FAST            5  'i'
         124  STORE_FAST            6  'event_name'

  36     127  LOAD_FAST             6  'event_name'
         130  LOAD_GLOBAL           9  'ALL_INTIMACY_MEMORY_EVENTS'
         133  COMPARE_OP            6  'in'
         136  POP_JUMP_IF_FALSE   115  'to 115'

  37     139  LOAD_FAST             1  'intimacy_memory_conf'
         142  LOAD_ATTR             1  'get'
         145  LOAD_FAST             6  'event_name'
         148  CALL_FUNCTION_1       1 
         151  STORE_FAST            7  'conf'

  38     154  LOAD_GLOBAL           2  'str'
         157  LOAD_FAST             7  'conf'
         160  LOAD_ATTR             1  'get'
         163  LOAD_CONST            2  'priority'
         166  CALL_FUNCTION_1       1 
         169  CALL_FUNCTION_1       1 
         172  STORE_FAST            8  'sort_id'

  39     175  SETUP_LOOP          312  'to 490'
         178  LOAD_GLOBAL           8  'enumerate'
         181  LOAD_FAST             0  'data'
         184  LOAD_FAST             6  'event_name'
         187  BINARY_SUBSCR    
         188  CALL_FUNCTION_1       1 
         191  GET_ITER         
         192  FOR_ITER            291  'to 486'
         195  UNPACK_SEQUENCE_2     2 
         198  STORE_FAST            9  'j'
         201  STORE_FAST           10  'event_value'

  40     204  LOAD_FAST             0  'data'
         207  LOAD_FAST             6  'event_name'
         210  BINARY_SUBSCR    
         211  LOAD_FAST            10  'event_value'
         214  BINARY_SUBSCR    
         215  STORE_FAST           11  'timestamp'

  41     218  LOAD_GLOBAL          10  'type'
         221  LOAD_FAST            11  'timestamp'
         224  CALL_FUNCTION_1       1 
         227  LOAD_GLOBAL           4  'int'
         230  COMPARE_OP            2  '=='
         233  POP_JUMP_IF_FALSE   192  'to 192'
         236  LOAD_FAST            10  'event_value'
         239  LOAD_CONST            5  'total_times'
         242  COMPARE_OP            3  '!='
       245_0  COME_FROM                '233'
         245  POP_JUMP_IF_FALSE   192  'to 192'

  43     248  LOAD_GLOBAL           5  'tutil'
         251  LOAD_ATTR            11  'get_date_str'
         254  LOAD_CONST            6  '%Y.%m.%d'
         257  LOAD_FAST            11  'timestamp'
         260  CALL_FUNCTION_2       2 
         263  STORE_FAST           12  'date_time'

  45     266  LOAD_FAST             2  'intimacy_event_data_dict'
         269  LOAD_ATTR             1  'get'
         272  LOAD_FAST            12  'date_time'
         275  CALL_FUNCTION_1       1 
         278  LOAD_CONST            0  ''
         281  COMPARE_OP            8  'is'
         284  POP_JUMP_IF_FALSE   300  'to 300'

  46     287  BUILD_MAP_0           0 
         290  LOAD_FAST             2  'intimacy_event_data_dict'
         293  LOAD_FAST            12  'date_time'
         296  STORE_SUBSCR     
         297  JUMP_FORWARD          0  'to 300'
       300_0  COME_FROM                '297'

  47     300  LOAD_FAST             2  'intimacy_event_data_dict'
         303  LOAD_FAST            12  'date_time'
         306  BINARY_SUBSCR    
         307  STORE_FAST           13  'event_data'

  48     310  LOAD_FAST            13  'event_data'
         313  LOAD_ATTR             1  'get'
         316  LOAD_FAST             8  'sort_id'
         319  CALL_FUNCTION_1       1 
         322  STORE_FAST           14  'intimacy_event_data'

  49     325  LOAD_FAST            14  'intimacy_event_data'
         328  POP_JUMP_IF_FALSE   396  'to 396'

  51     331  LOAD_FAST            10  'event_value'
         334  LOAD_CONST            4  'time'
         337  COMPARE_OP            3  '!='
         340  POP_JUMP_IF_FALSE   396  'to 396'
         343  LOAD_FAST            14  'intimacy_event_data'
         346  LOAD_CONST            7  1
         349  BINARY_SUBSCR    
         350  LOAD_CONST            4  'time'
         353  COMPARE_OP            3  '!='
       356_0  COME_FROM                '340'
       356_1  COME_FROM                '328'
         356  POP_JUMP_IF_FALSE   396  'to 396'

  52     359  LOAD_GLOBAL           4  'int'
         362  LOAD_FAST            10  'event_value'
         365  CALL_FUNCTION_1       1 
         368  LOAD_GLOBAL           4  'int'
         371  LOAD_FAST            14  'intimacy_event_data'
         374  LOAD_CONST            7  1
         377  BINARY_SUBSCR    
         378  CALL_FUNCTION_1       1 
         381  COMPARE_OP            1  '<='
         384  POP_JUMP_IF_FALSE   396  'to 396'

  53     387  CONTINUE            192  'to 192'
         390  JUMP_ABSOLUTE       396  'to 396'
         393  JUMP_FORWARD          0  'to 396'
       396_0  COME_FROM                '393'

  54     396  LOAD_FAST             6  'event_name'
         399  LOAD_FAST            10  'event_value'
         402  BUILD_LIST_2          2 
         405  LOAD_FAST            13  'event_data'
         408  LOAD_FAST             8  'sort_id'
         411  STORE_SUBSCR     

  56     412  LOAD_FAST             3  'realation_day_priority'
         415  LOAD_FAST            13  'event_data'
         418  COMPARE_OP            7  'not-in'
         421  POP_JUMP_IF_FALSE   483  'to 483'

  58     424  LOAD_GLOBAL           5  'tutil'
         427  LOAD_ATTR             6  'get_day_start_timestamp'
         430  LOAD_FAST            11  'timestamp'
         433  CALL_FUNCTION_1       1 
         436  STORE_FAST           15  'date_timestamp'

  59     439  LOAD_GLOBAL           5  'tutil'
         442  LOAD_ATTR            13  'get_delta_days'
         445  LOAD_FAST            15  'date_timestamp'
         448  LOAD_DEREF            0  'intimacy_begin_timestamp'
         451  CALL_FUNCTION_2       2 
         454  LOAD_CONST            7  1
         457  BINARY_ADD       
         458  STORE_FAST           16  'date_time_value'

  60     461  LOAD_GLOBAL           3  'INTIMACY_MEMORY_EVENT_RELATION_DAY'
         464  LOAD_FAST            16  'date_time_value'
         467  BUILD_LIST_2          2 
         470  LOAD_FAST            13  'event_data'
         473  LOAD_FAST             3  'realation_day_priority'
         476  STORE_SUBSCR     
         477  JUMP_ABSOLUTE       483  'to 483'
         480  JUMP_BACK           192  'to 192'
         483  JUMP_BACK           192  'to 192'
         486  POP_BLOCK        
       487_0  COME_FROM                '175'
         487  JUMP_BACK           115  'to 115'
         490  JUMP_BACK           115  'to 115'
         493  POP_BLOCK        
       494_0  COME_FROM                '102'

  62     494  LOAD_CLOSURE          0  'intimacy_begin_timestamp'
         500  LOAD_CONST               '<code_object check_relation_date>'
         503  MAKE_CLOSURE_0        0 
         506  STORE_FAST           17  'check_relation_date'

  77     509  LOAD_DEREF            0  'intimacy_begin_timestamp'
         512  POP_JUMP_IF_FALSE  1035  'to 1035'

  78     515  SETUP_LOOP          517  'to 1035'
         518  LOAD_GLOBAL          14  'INTIMACY_MEMORY_SPECIAL_RELATION_EVENTS'
         521  GET_ITER         
         522  FOR_ITER            506  'to 1031'
         525  STORE_FAST            6  'event_name'

  79     528  LOAD_FAST             1  'intimacy_memory_conf'
         531  LOAD_ATTR             1  'get'
         534  LOAD_FAST             6  'event_name'
         537  CALL_FUNCTION_1       1 
         540  STORE_FAST           18  'relation_conf'

  80     543  LOAD_GLOBAL           2  'str'
         546  LOAD_FAST            18  'relation_conf'
         549  LOAD_ATTR             1  'get'
         552  LOAD_CONST            2  'priority'
         555  CALL_FUNCTION_1       1 
         558  CALL_FUNCTION_1       1 
         561  STORE_FAST            8  'sort_id'

  81     564  LOAD_FAST            18  'relation_conf'
         567  LOAD_ATTR             1  'get'
         570  LOAD_CONST            9  'trigger_data'
         573  LOAD_CONST            0  ''
         576  CALL_FUNCTION_2       2 
         579  STORE_FAST           19  'fixed_relation_time'

  82     582  LOAD_FAST            19  'fixed_relation_time'
         585  POP_JUMP_IF_FALSE   785  'to 785'

  84     588  SETUP_LOOP          194  'to 785'
         591  LOAD_FAST            19  'fixed_relation_time'
         594  GET_ITER         
         595  FOR_ITER            183  'to 781'
         598  STORE_FAST           20  'relation_time'

  85     601  LOAD_FAST            17  'check_relation_date'
         604  LOAD_FAST            20  'relation_time'
         607  LOAD_GLOBAL          15  'False'
         610  CALL_FUNCTION_2       2 
         613  STORE_FAST           21  'date_time_value_list'

  86     616  LOAD_GLOBAL          16  'len'
         619  LOAD_FAST            21  'date_time_value_list'
         622  CALL_FUNCTION_1       1 
         625  LOAD_CONST           10  ''
         628  COMPARE_OP            4  '>'
         631  POP_JUMP_IF_FALSE   595  'to 595'

  87     634  LOAD_FAST            21  'date_time_value_list'
         637  LOAD_CONST           10  ''
         640  BINARY_SUBSCR    
         641  STORE_FAST           16  'date_time_value'

  88     644  LOAD_DEREF            0  'intimacy_begin_timestamp'
         647  LOAD_FAST            16  'date_time_value'
         650  LOAD_CONST            7  1
         653  BINARY_SUBTRACT  
         654  LOAD_GLOBAL           5  'tutil'
         657  LOAD_ATTR            17  'ONE_DAY_SECONDS'
         660  BINARY_MULTIPLY  
         661  BINARY_ADD       
         662  STORE_FAST           22  'relation_timestamp'

  89     665  LOAD_GLOBAL           5  'tutil'
         668  LOAD_ATTR            11  'get_date_str'
         671  LOAD_CONST            6  '%Y.%m.%d'
         674  LOAD_FAST            22  'relation_timestamp'
         677  CALL_FUNCTION_2       2 
         680  STORE_FAST           12  'date_time'

  90     683  LOAD_FAST             2  'intimacy_event_data_dict'
         686  LOAD_ATTR             1  'get'
         689  LOAD_FAST            12  'date_time'
         692  CALL_FUNCTION_1       1 
         695  LOAD_CONST            0  ''
         698  COMPARE_OP            8  'is'
         701  POP_JUMP_IF_FALSE   717  'to 717'

  91     704  BUILD_MAP_0           0 
         707  LOAD_FAST             2  'intimacy_event_data_dict'
         710  LOAD_FAST            12  'date_time'
         713  STORE_SUBSCR     
         714  JUMP_FORWARD         38  'to 755'

  94     717  LOAD_FAST             2  'intimacy_event_data_dict'
         720  LOAD_FAST            12  'date_time'
         723  BINARY_SUBSCR    
         724  STORE_FAST           13  'event_data'

  95     727  LOAD_FAST            13  'event_data'
         730  LOAD_ATTR             1  'get'
         733  LOAD_FAST             3  'realation_day_priority'
         736  CALL_FUNCTION_1       1 
         739  POP_JUMP_IF_FALSE   755  'to 755'

  96     742  LOAD_CONST            0  ''
         745  LOAD_FAST            13  'event_data'
         748  LOAD_FAST             3  'realation_day_priority'
         751  STORE_SUBSCR     
         752  JUMP_FORWARD          0  'to 755'
       755_0  COME_FROM                '752'
       755_1  COME_FROM                '714'

  97     755  LOAD_FAST             6  'event_name'
         758  LOAD_FAST            16  'date_time_value'
         761  BUILD_LIST_2          2 
         764  LOAD_FAST             2  'intimacy_event_data_dict'
         767  LOAD_FAST            12  'date_time'
         770  BINARY_SUBSCR    
         771  LOAD_FAST             8  'sort_id'
         774  STORE_SUBSCR     
         775  JUMP_BACK           595  'to 595'
         778  JUMP_BACK           595  'to 595'
         781  POP_BLOCK        
       782_0  COME_FROM                '588'
         782  JUMP_FORWARD          0  'to 785'
       785_0  COME_FROM                '588'

  99     785  LOAD_FAST            18  'relation_conf'
         788  LOAD_ATTR             1  'get'
         791  LOAD_CONST           11  'extra_data'
         794  LOAD_CONST            0  ''
         797  CALL_FUNCTION_2       2 
         800  STORE_FAST           23  'loop_relation_time'

 100     803  LOAD_FAST            23  'loop_relation_time'
         806  POP_JUMP_IF_FALSE   522  'to 522'

 102     809  LOAD_FAST            17  'check_relation_date'
         812  LOAD_FAST            23  'loop_relation_time'
         815  LOAD_GLOBAL          18  'True'
         818  CALL_FUNCTION_2       2 
         821  STORE_FAST           21  'date_time_value_list'

 103     824  LOAD_GLOBAL          16  'len'
         827  LOAD_FAST            21  'date_time_value_list'
         830  CALL_FUNCTION_1       1 
         833  LOAD_CONST           10  ''
         836  COMPARE_OP            4  '>'
         839  POP_JUMP_IF_FALSE  1028  'to 1028'

 104     842  SETUP_LOOP          180  'to 1025'
         845  LOAD_FAST            21  'date_time_value_list'
         848  GET_ITER         
         849  FOR_ITER            169  'to 1021'
         852  STORE_FAST           16  'date_time_value'

 105     855  LOAD_DEREF            0  'intimacy_begin_timestamp'
         858  LOAD_FAST            16  'date_time_value'
         861  LOAD_CONST            7  1
         864  BINARY_SUBTRACT  
         865  LOAD_GLOBAL           5  'tutil'
         868  LOAD_ATTR            17  'ONE_DAY_SECONDS'
         871  BINARY_MULTIPLY  
         872  BINARY_ADD       
         873  STORE_FAST           22  'relation_timestamp'

 106     876  LOAD_GLOBAL           5  'tutil'
         879  LOAD_ATTR            11  'get_date_str'
         882  LOAD_CONST            6  '%Y.%m.%d'
         885  LOAD_FAST            22  'relation_timestamp'
         888  CALL_FUNCTION_2       2 
         891  STORE_FAST           12  'date_time'

 107     894  LOAD_FAST             2  'intimacy_event_data_dict'
         897  LOAD_ATTR             1  'get'
         900  LOAD_FAST            12  'date_time'
         903  CALL_FUNCTION_1       1 
         906  LOAD_CONST            0  ''
         909  COMPARE_OP            8  'is'
         912  POP_JUMP_IF_FALSE   928  'to 928'

 108     915  BUILD_MAP_0           0 
         918  LOAD_FAST             2  'intimacy_event_data_dict'
         921  LOAD_FAST            12  'date_time'
         924  STORE_SUBSCR     
         925  JUMP_FORWARD         38  'to 966'

 111     928  LOAD_FAST             2  'intimacy_event_data_dict'
         931  LOAD_FAST            12  'date_time'
         934  BINARY_SUBSCR    
         935  STORE_FAST           13  'event_data'

 112     938  LOAD_FAST            13  'event_data'
         941  LOAD_ATTR             1  'get'
         944  LOAD_FAST             3  'realation_day_priority'
         947  CALL_FUNCTION_1       1 
         950  POP_JUMP_IF_FALSE   966  'to 966'

 113     953  LOAD_CONST            0  ''
         956  LOAD_FAST            13  'event_data'
         959  LOAD_FAST             3  'realation_day_priority'
         962  STORE_SUBSCR     
         963  JUMP_FORWARD          0  'to 966'
       966_0  COME_FROM                '963'
       966_1  COME_FROM                '925'

 114     966  LOAD_FAST            16  'date_time_value'
         969  LOAD_CONST           12  365
         972  BINARY_MODULO    
         973  LOAD_CONST           10  ''
         976  COMPARE_OP            2  '=='
         979  POP_JUMP_IF_FALSE   992  'to 992'
         982  LOAD_FAST            16  'date_time_value'
         985  LOAD_CONST           12  365
         988  BINARY_FLOOR_DIVIDE
         989  JUMP_FORWARD          3  'to 995'
         992  LOAD_FAST            16  'date_time_value'
       995_0  COME_FROM                '989'
         995  STORE_FAST           16  'date_time_value'

 115     998  LOAD_FAST             6  'event_name'
        1001  LOAD_FAST            16  'date_time_value'
        1004  BUILD_LIST_2          2 
        1007  LOAD_FAST             2  'intimacy_event_data_dict'
        1010  LOAD_FAST            12  'date_time'
        1013  BINARY_SUBSCR    
        1014  LOAD_FAST             8  'sort_id'
        1017  STORE_SUBSCR     
        1018  JUMP_BACK           849  'to 849'
        1021  POP_BLOCK        
      1022_0  COME_FROM                '842'
        1022  JUMP_ABSOLUTE      1028  'to 1028'
        1025  JUMP_BACK           522  'to 522'
        1028  JUMP_BACK           522  'to 522'
        1031  POP_BLOCK        
      1032_0  COME_FROM                '515'
        1032  JUMP_FORWARD          0  'to 1035'
      1035_0  COME_FROM                '515'

 116    1035  LOAD_FAST             2  'intimacy_event_data_dict'
        1038  RETURN_VALUE     

Parse error at or near `STORE_FAST' instruction at offset 51


class IntimacyHistoricalEventUI(BasePanel):
    PANEL_CONFIG_NAME = 'friend/i_intimacy_historical_event'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_content.btn_close.OnClick': 'on_click_close_ui'
       }

    def on_click_close_ui(self, *args):
        self.close()

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()

    def init_parameters(self):
        self._uid = None
        self._friend_info = None
        self._intimacy_info = None
        self._friend_list = global_data.message_data.get_friends()
        self._intimacy_event_data_dict = {}
        self._event_list = None
        self._screen_capture_helper = None
        self._share_content = None
        self._intimacy_name = None
        return

    def on_finalize_panel(self):
        self._uid = None
        self._friend_info = None
        self._intimacy_info = None
        self._friend_list = None
        self._archive_data = None
        self._intimacy_event_data_dict = None
        self._event_list = None
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
        self._screen_capture_helper = None
        self._share_content = None
        self._intimacy_name = None
        return

    def set_data(self, uid, data):
        self._uid = uid
        self._archive_data = global_data.achi_mgr.get_general_archive_data()
        self._friend_info = self._friend_list.get(uid, None)
        self._intimacy_info = global_data.player.intimacy_data.get(str(uid))
        if self._friend_info is None:
            return
        else:
            if self._intimacy_info is None:
                return
            self._intimacy_type = self._intimacy_info[IDX_INTIMACY_TYPE]
            self._intimacy_name = self._intimacy_info[IDX_INTIMACY_NAME]
            if self._intimacy_name is None:
                self._intimacy_name = get_text_by_id(INTIMACY_NAME_MAP[self._intimacy_type])
            self._intimacy_event_data_dict = get_data_list(data)
            self.update_panel()
            del data[INTIMACY_MEMORY_EVENT_BUILT]
            self._archive_data.set_field(INTIMACY_HISTORICAL_EVENT_KEY.format(str(uid)), self._intimacy_event_data_dict)
            global_data.emgr.message_on_intimacy_event.emit(global_data.player.uid, self._uid)
            global_data.emgr.on_intimacy_event_set_data.emit()
            return

    def update_panel(self):
        self._update_event_list()
        self._update_intimacy_data()

    def _update_event_list(self):
        self._event_list = self.panel.nd_content.list_event
        self._event_list.RecycleAllItem()
        index = 0
        date_time_list = []
        for date_time in sorted(self._intimacy_event_data_dict.keys()):
            template_index = index % len(TEMPLATE_LIST)
            template_path = TEMPLATE_LIST[template_index]
            template_conf = global_data.uisystem.load_template(template_path)
            item = self._event_list.AddItem(template_conf)
            self._init_event_list_item(item, date_time, self._intimacy_event_data_dict[date_time])
            index += 1
            date_time_list.append(date_time)
            if index == len(self._intimacy_event_data_dict):
                item.nd_line.img_line.setVisible(False)

    def _init_event_list_item(self, item, date_time, intimacy_event_data):
        temp_event_item = item.temp_event
        list_lab = temp_event_item.nd_position.list_lab
        temp_event_item.lab_date.SetString(date_time)
        highest_intimacy_event_data = None
        sorted_keys = sorted(map(int, intimacy_event_data.keys()))
        for sort_id in sorted_keys:
            lab_item = list_lab.AddTemplateItem()
            event_data = intimacy_event_data[str(sort_id)]
            self._init_event_list_lab_item(lab_item, event_data)
            if event_data[0] != INTIMACY_MEMORY_EVENT_RELATION_DAY:
                highest_intimacy_event_data = event_data

        width, height = list_lab.GetContentSize()
        if len(intimacy_event_data) <= 3:
            list_lab.SetContentSize(width, 2 + 44 * len(intimacy_event_data))
        else:
            list_lab.LocatePosByItem(len(intimacy_event_data) - 1)
        temp_event_item.btn_share.BindMethod('OnClick', lambda btn, touch: callable(intimacy_event_cb) and intimacy_event_cb())

        def intimacy_event_cb():
            if not self._screen_capture_helper:
                from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
                self._screen_capture_helper = ScreenFrameHelper()
            self._share_content = IntimacyHistoricalEventShareCreator()
            self._share_content.create(intimacy_event_data=highest_intimacy_event_data, intimacy_info=self._intimacy_info, friend_info=self._friend_info, date_time=date_time)
            self._screen_capture_helper.set_custom_share_content(self._share_content)
            self._screen_capture_helper.take_screen_shot([self.__class__.__name__], self.panel)

        cache_data_list = self._archive_data.get_field(INTIMACY_HISTORICAL_EVENT_KEY.format(str(self._uid)), {})
        if not cache_data_list:
            item.img_new.setVisible(False)
            return
        else:
            cache_intimacy_event_data = cache_data_list.get(date_time)
            if cache_intimacy_event_data is None:
                item.img_new.setVisible(True)
            elif intimacy_event_data != cache_intimacy_event_data:
                item.img_new.setVisible(True)
            else:
                item.img_new.setVisible(False)
            return

    def _init_event_list_lab_item(self, lab_item, intimacy_event_data):
        event_name = intimacy_event_data[0]
        init_intimacy_event_bar(lab_item.bar_color, self._intimacy_type, event_name)
        text_id = confmgr.get('intimacy_memory_data', event_name, 'text_id')
        value_num = str(intimacy_event_data[1])
        lab_item.lab_event.SetString(get_text_by_id(text_id).format(value_num, time=value_num, rela=self._intimacy_name, lv=value_num))

    def _update_intimacy_data(self):
        nd = self.panel.nd_content
        frame_color = nd.frame_color
        intimacy_info = self._intimacy_info
        friend_info = self._friend_info
        player = global_data.player
        frame_color.lab_relationship.SetString(str(self._intimacy_name))
        init_intimacy_event_frame(frame_color, self._intimacy_type)
        init_intimacy_pic(frame_color.icon_relationship, self._intimacy_type)
        frame_color.lab_level.SetString('Lv.{}'.format(str(intimacy_info[IDX_INTIMACY_LV])))
        player_info_manager = PlayerInfoManager()
        others_head = nd.temp_head_others

        @others_head.callback()
        def OnClick(btn, touch):
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            ui.refresh_by_uid(int(friend_info[U_ID]))
            ui.set_position(touch.getLocation())
            ui.need_close_history_ui = True

        update_head_info = global_data.message_data.get_role_head_info(self._uid)
        frame = update_head_info.get('head_frame', None)
        photo = update_head_info.get('head_photo', None)
        if frame and photo:
            friend_info['head_frame'] = frame
            friend_info['head_photo'] = photo
        player_info_manager.add_head_item_auto(others_head, self._uid, 0, friend_info)
        friend_name = str(friend_info[C_NAME])
        others_head.lab_playername.SetString(friend_name)
        head_frame = player.get_head_frame()
        head_photo = player.get_head_photo()
        my_head = nd.temp_head_mine
        role_head_utils.init_role_head(my_head, head_frame, head_photo)
        my_head.lab_playername.SetString(player.get_name())
        return