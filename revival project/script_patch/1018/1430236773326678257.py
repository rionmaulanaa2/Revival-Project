# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/hot_key_utils.py
from __future__ import absolute_import
import game3d
import six_ex
from six.moves import range
import six
import game
import time
from logic.client.const import hotkey_const
from logic.vscene.parts.ctrl.VirtualCodeComplement import MOUSE_BUTTON_BACK, MOUSE_BUTTON_FORWARD
key_down_time = {}

def hot_key_func_to_hot_key(hot_key_func_name):
    import logic.vscene.parts.ctrl.GamePyHook as game_hook
    hot_key_spec = get_hotkey_binding(hot_key_func_name)
    if hot_key_spec:
        if hot_key_spec == game_hook.PC_HOTKEY_CUSTOM_UNBIND_VK_CODE_LIST:
            return game_hook.PC_HOTKEY_CUSTOM_CACHE_UNBIND_INT_VAL
        if len(hot_key_spec) == 1:
            hot_key_spec = hot_key_spec[0]
        else:
            return vk_name_list_to_vk_code_list(hot_key_spec)
    if type(hot_key_spec) in [list, tuple]:
        try:
            hot_key_lst = []
            for hot_key_name in hot_key_spec:
                if hot_key_name is None:
                    continue
                hot_key = None
                if hasattr(game_hook, hot_key_name):
                    hot_key = getattr(game_hook, hot_key_name)
                elif hasattr(game, hot_key_name):
                    hot_key = getattr(game, hot_key_name)
                if hot_key:
                    hot_key_lst.append(hot_key)

            return hot_key_lst
        except:
            return

    else:
        hot_key_name = hot_key_spec
        return game_hook.get_vk_code(hot_key_name)
    return


def hot_key_func_to_hot_key_name_spec_from_cfg(hot_key_func_name):
    from common.cfg import confmgr
    hot_key_conf = confmgr.get('c_hot_key_config')
    hot_key_name = hot_key_conf.get(hot_key_func_name, {}).get('cHotKeyDef', '')
    return hot_key_name


def get_hot_key_fun_desc(hot_key_func_name):
    from common.cfg import confmgr
    hot_key_conf = confmgr.get('c_hot_key_config')
    from logic.gcommon.common_utils.local_text import get_text_by_id
    return get_text_by_id(hot_key_conf.get(hot_key_func_name, {}).get('cHotKeyFuncDesc', ''))


def get_hot_key_display_name(hot_key_name):
    from common.cfg import confmgr
    from logic.gcommon.common_utils.local_text import get_text_by_id
    key_conf = confmgr.get('c_key_name_config', str(hot_key_name), default={})
    nameId = key_conf.get('cKeyName', 0)
    if not nameId:
        nameText = key_conf.get('cKeyNameText', None)
        if nameText is not None:
            return nameText
        return get_text_by_id(920505, {'key': get_hot_key_short_display_name(hot_key_name)})
    else:
        return get_text_by_id(nameId)


def get_hot_key_value_display_name(hot_key_value):
    from logic.client.const.key_const import hot_key_value_to_hot_key_name
    hot_key_name = hot_key_value_to_hot_key_name(hot_key_value)
    if hot_key_name:
        return get_hot_key_display_name(hot_key_name)
    log_error('get_hot_key_value_display_name: %d not found', hot_key_value)
    return ''


def get_hot_key_short_display_name--- This code section failed: ---

  98       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'logic.vscene.parts.ctrl.GamePyHook'
           9  LOAD_ATTR             1  'vscene'
          12  LOAD_ATTR             2  'parts'
          15  LOAD_ATTR             3  'ctrl'
          18  LOAD_ATTR             4  'GamePyHook'
          21  STORE_FAST            1  'game_hook'

  99      24  LOAD_FAST             0  'vk_name_str'
          27  LOAD_FAST             1  'game_hook'
          30  LOAD_ATTR             5  'PC_HOTKEY_CUSTOM_CACHE_UNBIND_STR_VAL'
          33  COMPARE_OP            2  '=='
          36  POP_JUMP_IF_FALSE    43  'to 43'

 100      39  LOAD_CONST            2  ''
          42  RETURN_END_IF    
        43_0  COME_FROM                '36'

 102      43  LOAD_CONST            1  ''
          46  LOAD_CONST            3  ('confmgr',)
          49  IMPORT_NAME           6  'common.cfg'
          52  IMPORT_FROM           7  'confmgr'
          55  STORE_FAST            2  'confmgr'
          58  POP_TOP          

 103      59  LOAD_CONST            1  ''
          62  LOAD_CONST            4  ('get_text_by_id',)
          65  IMPORT_NAME           8  'logic.gcommon.common_utils.local_text'
          68  IMPORT_FROM           9  'get_text_by_id'
          71  STORE_FAST            3  'get_text_by_id'
          74  POP_TOP          

 104      75  LOAD_FAST             2  'confmgr'
          78  LOAD_ATTR            10  'get'
          81  LOAD_CONST            5  'c_key_name_config'
          84  LOAD_GLOBAL          11  'str'
          87  LOAD_FAST             0  'vk_name_str'
          90  CALL_FUNCTION_1       1 
          93  LOAD_CONST            6  'default'
          96  BUILD_MAP_0           0 
          99  CALL_FUNCTION_258   258 
         102  STORE_FAST            4  'key_conf'

 105     105  LOAD_FAST             4  'key_conf'
         108  LOAD_ATTR            10  'get'
         111  LOAD_CONST            7  'cKeyName'
         114  LOAD_CONST            1  ''
         117  CALL_FUNCTION_2       2 
         120  STORE_FAST            5  'nameId'

 106     123  LOAD_FAST             5  'nameId'
         126  POP_JUMP_IF_FALSE   139  'to 139'

 107     129  LOAD_FAST             3  'get_text_by_id'
         132  LOAD_FAST             5  'nameId'
         135  CALL_FUNCTION_1       1 
         138  RETURN_END_IF    
       139_0  COME_FROM                '126'

 109     139  LOAD_FAST             4  'key_conf'
         142  LOAD_ATTR            10  'get'
         145  LOAD_CONST            8  'cKeyNameText'
         148  LOAD_CONST            0  ''
         151  CALL_FUNCTION_2       2 
         154  STORE_FAST            6  'nameText'

 110     157  LOAD_FAST             6  'nameText'
         160  LOAD_CONST            0  ''
         163  COMPARE_OP            9  'is-not'
         166  POP_JUMP_IF_FALSE   173  'to 173'

 111     169  LOAD_FAST             6  'nameText'
         172  RETURN_END_IF    
       173_0  COME_FROM                '166'

 112     173  LOAD_FAST             0  'vk_name_str'
         176  LOAD_ATTR            13  'startswith'
         179  LOAD_CONST            9  'VK_'
         182  CALL_FUNCTION_1       1 
         185  POP_JUMP_IF_FALSE   199  'to 199'

 113     188  POP_JUMP_IF_FALSE    10  'to 10'
         191  SLICE+1          
         192  STORE_FAST            7  'hot_key_display_name'

 114     195  LOAD_FAST             7  'hot_key_display_name'
         198  RETURN_END_IF    
       199_0  COME_FROM                '188'
       199_1  COME_FROM                '185'

 116     199  LOAD_GLOBAL          14  'log_error'
         202  LOAD_CONST           11  'Unsupported hot key'
         205  LOAD_FAST             0  'vk_name_str'
         208  CALL_FUNCTION_2       2 
         211  POP_TOP          

 117     212  LOAD_FAST             0  'vk_name_str'
         215  RETURN_VALUE     
         216  LOAD_CONST            0  ''
         219  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 188


def get_hot_key_short_display_name_ex(hot_key_func_name):
    hot_key_name_spec = hot_key_func_to_hot_key_name_spec_from_cfg(hot_key_func_name)
    return get_hot_key_short_display_name_ex_raw(hot_key_name_spec)


def vk_name_to_vk_code(vk_name):
    import logic.vscene.parts.ctrl.GamePyHook as game_hook
    if vk_name == game_hook.PC_HOTKEY_CUSTOM_CACHE_UNBIND_STR_VAL:
        return game_hook.PC_HOTKEY_CUSTOM_CACHE_UNBIND_INT_VAL
    else:
        return getattr(game, vk_name, None)


def vk_name_list_to_vk_code_list(vk_name_list):
    if vk_name_list is None:
        return
    else:
        if len(vk_name_list) == 0:
            return []
        ret = []
        for vk_name in vk_name_list:
            vk_code = vk_name_to_vk_code(vk_name)
            if vk_code is None:
                continue
            ret.append(vk_code)

        return ret


def vk_code_list_to_vk_name_list(vk_code_list):
    if vk_code_list is None:
        return
    else:
        if len(vk_code_list) == 0:
            return []
        import logic.vscene.parts.ctrl.GamePyHook as game_hook
        ret = []
        for vk_code in vk_code_list:
            vk_name = game_hook.vk_code_to_vk_name(vk_code)
            if not vk_name:
                continue
            ret.append(vk_name)

        return ret


def get_hot_key_short_display_name_ex_raw--- This code section failed: ---

 163       0  LOAD_GLOBAL           0  'isinstance'
           3  LOAD_FAST             0  'vk_name_list'
           6  LOAD_GLOBAL           1  'six'
           9  LOAD_ATTR             2  'string_types'
          12  CALL_FUNCTION_2       2 
          15  POP_JUMP_IF_FALSE    28  'to 28'

 164      18  LOAD_GLOBAL           3  'get_hot_key_short_display_name'
          21  LOAD_FAST             0  'vk_name_list'
          24  CALL_FUNCTION_1       1 
          27  RETURN_END_IF    
        28_0  COME_FROM                '15'

 165      28  LOAD_GLOBAL           0  'isinstance'
          31  LOAD_FAST             0  'vk_name_list'
          34  LOAD_GLOBAL           4  'list'
          37  LOAD_GLOBAL           5  'tuple'
          40  BUILD_TUPLE_2         2 
          43  CALL_FUNCTION_2       2 
          46  POP_JUMP_IF_FALSE   141  'to 141'

 166      49  LOAD_GLOBAL           6  'len'
          52  LOAD_FAST             0  'vk_name_list'
          55  CALL_FUNCTION_1       1 
          58  LOAD_CONST            1  ''
          61  COMPARE_OP            2  '=='
          64  POP_JUMP_IF_FALSE    71  'to 71'

 167      67  LOAD_CONST            2  ''
          70  RETURN_END_IF    
        71_0  COME_FROM                '64'

 168      71  LOAD_GLOBAL           6  'len'
          74  LOAD_FAST             0  'vk_name_list'
          77  CALL_FUNCTION_1       1 
          80  LOAD_CONST            3  1
          83  COMPARE_OP            2  '=='
          86  POP_JUMP_IF_FALSE   100  'to 100'

 169      89  LOAD_GLOBAL           3  'get_hot_key_short_display_name'
          92  LOAD_GLOBAL           1  'six'
          95  BINARY_SUBSCR    
          96  CALL_FUNCTION_1       1 
          99  RETURN_END_IF    
       100_0  COME_FROM                '86'

 171     100  LOAD_CONST            4  '+'
         103  LOAD_ATTR             7  'join'
         106  BUILD_LIST_0          0 
         109  LOAD_FAST             0  'vk_name_list'
         112  GET_ITER         
         113  FOR_ITER             18  'to 134'
         116  STORE_FAST            1  'i'
         119  LOAD_GLOBAL           3  'get_hot_key_short_display_name'
         122  LOAD_FAST             1  'i'
         125  CALL_FUNCTION_1       1 
         128  LIST_APPEND           2  ''
         131  JUMP_BACK           113  'to 113'
         134  CALL_FUNCTION_1       1 
         137  RETURN_VALUE     
         138  JUMP_FORWARD          4  'to 145'

 173     141  LOAD_CONST            2  ''
         144  RETURN_VALUE     
       145_0  COME_FROM                '138'

Parse error at or near `CALL_FUNCTION_1' instruction at offset 96


def set_hot_key_common_tip_multiple_version(temp_list_node, multiple_hot_key_func_name, force_set=False):
    if multiple_hot_key_func_name is None:
        multiple_hot_key_func_name = []
    temp_list_node.SetInitCount(len(multiple_hot_key_func_name))
    for idx in range(len(multiple_hot_key_func_name)):
        hotkey_func_name = multiple_hot_key_func_name[idx]
        temp_node = temp_list_node.GetItem(idx)
        set_hot_key_common_tip(temp_node, hotkey_func_name, update_root_node_size=True, force_set=force_set)

    temp_list_node.RefreshItemPos()
    return


def set_hot_key_common_tip(temp_node, hot_key_func_name, vk_name_str_or_list=None, update_root_node_size=False, force_set=False):
    if vk_name_str_or_list is None:
        vk_name_str_or_list = get_hotkey_binding(hot_key_func_name)
    set_hot_key_common_tip_core(temp_node, vk_name_str_or_list, update_root_node_size, force_set=force_set)
    return


def get_vk_icon_path--- This code section failed: ---

 200       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('confmgr',)
           6  IMPORT_NAME           0  'common.cfg'
           9  IMPORT_FROM           1  'confmgr'
          12  STORE_FAST            1  'confmgr'
          15  POP_TOP          

 201      16  LOAD_FAST             1  'confmgr'
          19  LOAD_ATTR             2  'get'
          22  LOAD_CONST            3  'c_key_name_config'
          25  LOAD_CONST            4  'cKeyIconPath'
          28  LOAD_CONST            5  'default'
          31  LOAD_CONST            6  ''
          34  CALL_FUNCTION_259   259 
          37  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_259' instruction at offset 34


def set_hot_key_common_tip_core--- This code section failed: ---

 209       0  LOAD_FAST             3  'force_set'
           3  UNARY_NOT        
           4  POP_JUMP_IF_FALSE    45  'to 45'
           7  LOAD_GLOBAL           0  'global_data'
          10  LOAD_ATTR             1  'is_pc_mode'
          13  JUMP_IF_FALSE_OR_POP    37  'to 37'
          16  LOAD_GLOBAL           0  'global_data'
          19  LOAD_ATTR             2  'pc_ctrl_mgr'
          22  JUMP_IF_FALSE_OR_POP    37  'to 37'
          25  LOAD_GLOBAL           0  'global_data'
          28  LOAD_ATTR             2  'pc_ctrl_mgr'
          31  LOAD_ATTR             3  'is_pc_control_enable'
          34  CALL_FUNCTION_0       0 
        37_0  COME_FROM                '22'
        37_1  COME_FROM                '13'
          37  UNARY_NOT        
        38_0  COME_FROM                '4'
          38  POP_JUMP_IF_FALSE    45  'to 45'

 210      41  LOAD_CONST            0  ''
          44  RETURN_END_IF    
        45_0  COME_FROM                '38'

 215      45  LOAD_GLOBAL           4  'getattr'
          48  LOAD_GLOBAL           1  'is_pc_mode'
          51  CALL_FUNCTION_2       2 
          54  STORE_FAST            4  'temp_list_node'

 218      57  LOAD_GLOBAL           5  'isinstance'
          60  LOAD_FAST             1  'vk_name_str_or_list'
          63  LOAD_GLOBAL           6  'list'
          66  LOAD_GLOBAL           7  'tuple'
          69  BUILD_TUPLE_2         2 
          72  CALL_FUNCTION_2       2 
          75  POP_JUMP_IF_FALSE   112  'to 112'

 219      78  LOAD_GLOBAL           8  'len'
          81  LOAD_FAST             1  'vk_name_str_or_list'
          84  CALL_FUNCTION_1       1 
          87  LOAD_CONST            2  1
          90  COMPARE_OP            2  '=='
          93  POP_JUMP_IF_FALSE   112  'to 112'

 220      96  LOAD_FAST             1  'vk_name_str_or_list'
          99  LOAD_CONST            3  ''
         102  BINARY_SUBSCR    
         103  STORE_FAST            1  'vk_name_str_or_list'
         106  JUMP_ABSOLUTE       112  'to 112'
         109  JUMP_FORWARD          0  'to 112'
       112_0  COME_FROM                '109'

 222     112  LOAD_CONST            3  ''
         115  LOAD_CONST            4  ('confmgr',)
         118  IMPORT_NAME           9  'common.cfg'
         121  IMPORT_FROM          10  'confmgr'
         124  STORE_FAST            5  'confmgr'
         127  POP_TOP          

 223     128  LOAD_CONST            3  ''
         131  LOAD_CONST            5  ('get_text_by_id',)
         134  IMPORT_NAME          11  'logic.gcommon.common_utils.local_text'
         137  IMPORT_FROM          12  'get_text_by_id'
         140  STORE_FAST            6  'get_text_by_id'
         143  POP_TOP          

 225     144  LOAD_GLOBAL           5  'isinstance'
         147  LOAD_FAST             1  'vk_name_str_or_list'
         150  LOAD_GLOBAL          13  'six'
         153  LOAD_ATTR            14  'string_types'
         156  CALL_FUNCTION_2       2 
         159  POP_JUMP_IF_FALSE   456  'to 456'

 226     162  LOAD_FAST             1  'vk_name_str_or_list'
         165  STORE_FAST            7  'vk_name_str'

 228     168  LOAD_FAST             4  'temp_list_node'
         171  LOAD_ATTR            15  'SetInitCount'
         174  LOAD_CONST            2  1
         177  CALL_FUNCTION_1       1 
         180  POP_TOP          

 229     181  LOAD_FAST             4  'temp_list_node'
         184  LOAD_ATTR            16  'GetItem'
         187  LOAD_CONST            3  ''
         190  CALL_FUNCTION_1       1 
         193  STORE_FAST            8  'node'

 232     196  LOAD_GLOBAL          17  'is_hot_key_unset_raw'
         199  LOAD_FAST             7  'vk_name_str'
         202  CALL_FUNCTION_1       1 
         205  POP_JUMP_IF_TRUE    331  'to 331'

 233     208  LOAD_FAST             5  'confmgr'
         211  LOAD_ATTR            18  'get'
         214  LOAD_CONST            6  'c_key_name_config'
         217  LOAD_FAST             7  'vk_name_str'
         220  LOAD_CONST            7  'default'
         223  BUILD_MAP_0           0 
         226  CALL_FUNCTION_258   258 
         229  STORE_FAST            9  'key_conf'

 234     232  LOAD_FAST             9  'key_conf'
         235  LOAD_ATTR            18  'get'
         238  LOAD_CONST            8  'cKeyIconPath'
         241  LOAD_CONST            9  ''
         244  CALL_FUNCTION_2       2 
         247  STORE_FAST           10  'icon_path'

 235     250  LOAD_GLOBAL          19  'bool'
         253  LOAD_FAST            10  'icon_path'
         256  CALL_FUNCTION_1       1 
         259  STORE_FAST           11  'is_show_icon'

 237     262  LOAD_FAST            11  'is_show_icon'
         265  POP_JUMP_IF_FALSE   290  'to 290'

 238     268  LOAD_FAST             8  'node'
         271  LOAD_ATTR            20  'img_pc'
         274  LOAD_ATTR            21  'SetDisplayFrameByPath'
         277  LOAD_CONST            9  ''
         280  LOAD_FAST            10  'icon_path'
         283  CALL_FUNCTION_2       2 
         286  POP_TOP          
         287  JUMP_ABSOLUTE       375  'to 375'

 240     290  LOAD_FAST             8  'node'
         293  LOAD_ATTR            22  'lab_pc'
         296  LOAD_ATTR            23  'SetString'
         299  LOAD_GLOBAL          24  'get_hot_key_short_display_name'
         302  LOAD_FAST             7  'vk_name_str'
         305  CALL_FUNCTION_1       1 
         308  CALL_FUNCTION_1       1 
         311  POP_TOP          

 241     312  LOAD_FAST             8  'node'
         315  LOAD_ATTR            22  'lab_pc'
         318  LOAD_ATTR            25  'SetColor'
         321  LOAD_CONST           10  '#SK'
         324  CALL_FUNCTION_1       1 
         327  POP_TOP          
         328  JUMP_FORWARD         44  'to 375'

 243     331  LOAD_GLOBAL          26  'False'
         334  STORE_FAST           11  'is_show_icon'

 244     337  LOAD_FAST             8  'node'
         340  LOAD_ATTR            22  'lab_pc'
         343  LOAD_ATTR            23  'SetString'
         346  LOAD_FAST             6  'get_text_by_id'
         349  LOAD_CONST           11  920709
         352  CALL_FUNCTION_1       1 
         355  CALL_FUNCTION_1       1 
         358  POP_TOP          

 245     359  LOAD_FAST             8  'node'
         362  LOAD_ATTR            22  'lab_pc'
         365  LOAD_ATTR            25  'SetColor'
         368  LOAD_CONST           12  '#BR'
         371  CALL_FUNCTION_1       1 
         374  POP_TOP          
       375_0  COME_FROM                '328'

 247     375  LOAD_FAST             8  'node'
         378  LOAD_ATTR            20  'img_pc'
         381  LOAD_ATTR            27  'setVisible'
         384  LOAD_FAST            11  'is_show_icon'
         387  CALL_FUNCTION_1       1 
         390  POP_TOP          

 248     391  LOAD_FAST             8  'node'
         394  LOAD_ATTR            22  'lab_pc'
         397  LOAD_ATTR            27  'setVisible'
         400  LOAD_FAST            11  'is_show_icon'
         403  UNARY_NOT        
         404  CALL_FUNCTION_1       1 
         407  POP_TOP          

 250     408  LOAD_GLOBAL          28  'update_pc_tip_item_node_width'
         411  LOAD_FAST             8  'node'
         414  LOAD_FAST            11  'is_show_icon'
         417  CALL_FUNCTION_2       2 
         420  POP_TOP          

 251     421  LOAD_FAST             4  'temp_list_node'
         424  LOAD_ATTR            29  'RefreshItemPos'
         427  CALL_FUNCTION_0       0 
         430  POP_TOP          

 252     431  LOAD_FAST             2  'update_root_node_size'
         434  POP_JUMP_IF_FALSE  1058  'to 1058'

 253     437  LOAD_GLOBAL          30  'align_node_width_with_target'
         440  LOAD_FAST             0  'temp_node'
         443  LOAD_FAST             4  'temp_list_node'
         446  CALL_FUNCTION_2       2 
         449  POP_TOP          
         450  JUMP_ABSOLUTE      1058  'to 1058'
         453  JUMP_FORWARD        602  'to 1058'

 254     456  LOAD_GLOBAL           5  'isinstance'
         459  LOAD_FAST             1  'vk_name_str_or_list'
         462  LOAD_GLOBAL           6  'list'
         465  LOAD_GLOBAL           7  'tuple'
         468  BUILD_TUPLE_2         2 
         471  CALL_FUNCTION_2       2 
         474  POP_JUMP_IF_FALSE  1048  'to 1048'

 255     477  LOAD_FAST             1  'vk_name_str_or_list'
         480  STORE_FAST           12  'vk_name_str_list'

 257     483  BUILD_LIST_0          0 
         486  STORE_FAST           13  'all_items'

 258     489  LOAD_CONST            9  ''
         492  STORE_FAST           14  'txt_cache'

 259     495  LOAD_CONST            0  ''
         498  STORE_FAST           15  'last_type'

 260     501  SETUP_LOOP          309  'to 813'
         504  LOAD_GLOBAL          32  'enumerate'
         507  LOAD_FAST            12  'vk_name_str_list'
         510  CALL_FUNCTION_1       1 
         513  GET_ITER         
         514  FOR_ITER            295  'to 812'
         517  UNPACK_SEQUENCE_2     2 
         520  STORE_FAST           16  'i'
         523  STORE_FAST           17  'vk_name'

 261     526  LOAD_FAST             5  'confmgr'
         529  LOAD_ATTR            18  'get'
         532  LOAD_CONST            6  'c_key_name_config'
         535  LOAD_FAST            17  'vk_name'
         538  LOAD_CONST            7  'default'
         541  BUILD_MAP_0           0 
         544  CALL_FUNCTION_258   258 
         547  STORE_FAST            9  'key_conf'

 262     550  LOAD_FAST             9  'key_conf'
         553  LOAD_ATTR            18  'get'
         556  LOAD_CONST            8  'cKeyIconPath'
         559  LOAD_CONST            9  ''
         562  CALL_FUNCTION_2       2 
         565  STORE_FAST           10  'icon_path'

 263     568  LOAD_GLOBAL          19  'bool'
         571  LOAD_FAST            10  'icon_path'
         574  CALL_FUNCTION_1       1 
         577  STORE_FAST           11  'is_show_icon'

 266     580  LOAD_FAST            11  'is_show_icon'
         583  POP_JUMP_IF_FALSE   660  'to 660'

 267     586  LOAD_FAST            14  'txt_cache'
         589  POP_JUMP_IF_FALSE   631  'to 631'

 268     592  LOAD_CONST           13  '%s+'
         595  LOAD_FAST            14  'txt_cache'
         598  BINARY_MODULO    
         599  STORE_FAST           14  'txt_cache'

 269     602  LOAD_FAST            13  'all_items'
         605  LOAD_ATTR            33  'append'
         608  BUILD_MAP_1           1 
         611  LOAD_FAST            14  'txt_cache'
         614  LOAD_CONST           14  'txt'
         617  STORE_MAP        
         618  CALL_FUNCTION_1       1 
         621  POP_TOP          

 270     622  LOAD_CONST            9  ''
         625  STORE_FAST           14  'txt_cache'
         628  JUMP_FORWARD          0  'to 631'
       631_0  COME_FROM                '628'

 271     631  LOAD_FAST            13  'all_items'
         634  LOAD_ATTR            33  'append'
         637  BUILD_MAP_1           1 
         640  LOAD_FAST            10  'icon_path'
         643  LOAD_CONST           15  'icon'
         646  STORE_MAP        
         647  CALL_FUNCTION_1       1 
         650  POP_TOP          

 273     651  LOAD_CONST           15  'icon'
         654  STORE_FAST           15  'last_type'
         657  JUMP_FORWARD         95  'to 755'

 275     660  LOAD_FAST            15  'last_type'
         663  POP_JUMP_IF_TRUE    681  'to 681'

 276     666  LOAD_GLOBAL          24  'get_hot_key_short_display_name'
         669  LOAD_FAST            17  'vk_name'
         672  CALL_FUNCTION_1       1 
         675  STORE_FAST           14  'txt_cache'
         678  JUMP_FORWARD         68  'to 749'

 277     681  LOAD_FAST            15  'last_type'
         684  LOAD_CONST           14  'txt'
         687  COMPARE_OP            2  '=='
         690  POP_JUMP_IF_FALSE   718  'to 718'

 278     693  LOAD_CONST           16  '%s+%s'
         696  LOAD_FAST            14  'txt_cache'
         699  LOAD_GLOBAL          24  'get_hot_key_short_display_name'
         702  LOAD_FAST            17  'vk_name'
         705  CALL_FUNCTION_1       1 
         708  BUILD_TUPLE_2         2 
         711  BINARY_MODULO    
         712  STORE_FAST           14  'txt_cache'
         715  JUMP_FORWARD         31  'to 749'

 279     718  LOAD_FAST            15  'last_type'
         721  LOAD_CONST           15  'icon'
         724  COMPARE_OP            2  '=='
         727  POP_JUMP_IF_FALSE   749  'to 749'

 280     730  LOAD_CONST           17  '+%s'
         733  LOAD_GLOBAL          24  'get_hot_key_short_display_name'
         736  LOAD_FAST            17  'vk_name'
         739  CALL_FUNCTION_1       1 
         742  BINARY_MODULO    
         743  STORE_FAST           14  'txt_cache'
         746  JUMP_FORWARD          0  'to 749'
       749_0  COME_FROM                '746'
       749_1  COME_FROM                '715'
       749_2  COME_FROM                '678'

 282     749  LOAD_CONST           14  'txt'
         752  STORE_FAST           15  'last_type'
       755_0  COME_FROM                '657'

 284     755  LOAD_FAST            16  'i'
         758  LOAD_GLOBAL           8  'len'
         761  LOAD_FAST            12  'vk_name_str_list'
         764  CALL_FUNCTION_1       1 
         767  LOAD_CONST            2  1
         770  BINARY_SUBTRACT  
         771  COMPARE_OP            2  '=='
         774  POP_JUMP_IF_FALSE   514  'to 514'

 285     777  LOAD_FAST            14  'txt_cache'
         780  POP_JUMP_IF_FALSE   809  'to 809'

 286     783  LOAD_FAST            13  'all_items'
         786  LOAD_ATTR            33  'append'
         789  BUILD_MAP_1           1 
         792  LOAD_FAST            14  'txt_cache'
         795  LOAD_CONST           14  'txt'
         798  STORE_MAP        
         799  CALL_FUNCTION_1       1 
         802  POP_TOP          
         803  JUMP_ABSOLUTE       809  'to 809'
         806  JUMP_BACK           514  'to 514'
         809  JUMP_BACK           514  'to 514'
         812  POP_BLOCK        
       813_0  COME_FROM                '501'

 288     813  LOAD_FAST             4  'temp_list_node'
         816  LOAD_ATTR            15  'SetInitCount'
         819  LOAD_GLOBAL           8  'len'
         822  LOAD_FAST            13  'all_items'
         825  CALL_FUNCTION_1       1 
         828  CALL_FUNCTION_1       1 
         831  POP_TOP          

 289     832  SETUP_LOOP          178  'to 1013'
         835  LOAD_GLOBAL          32  'enumerate'
         838  LOAD_FAST             4  'temp_list_node'
         841  LOAD_ATTR            34  'GetAllItem'
         844  CALL_FUNCTION_0       0 
         847  CALL_FUNCTION_1       1 
         850  GET_ITER         
         851  FOR_ITER            158  'to 1012'
         854  UNPACK_SEQUENCE_2     2 
         857  STORE_FAST           16  'i'
         860  STORE_FAST            8  'node'

 290     863  LOAD_FAST            13  'all_items'
         866  LOAD_FAST            16  'i'
         869  BINARY_SUBSCR    
         870  STORE_FAST           18  'info'

 292     873  LOAD_CONST           15  'icon'
         876  LOAD_FAST            18  'info'
         879  COMPARE_OP            6  'in'
         882  STORE_FAST           11  'is_show_icon'

 293     885  LOAD_FAST            11  'is_show_icon'
         888  POP_JUMP_IF_FALSE   922  'to 922'

 294     891  LOAD_FAST             8  'node'
         894  LOAD_ATTR            20  'img_pc'
         897  LOAD_ATTR            21  'SetDisplayFrameByPath'
         900  LOAD_CONST            9  ''
         903  LOAD_FAST            18  'info'
         906  LOAD_ATTR            18  'get'
         909  LOAD_CONST           15  'icon'
         912  CALL_FUNCTION_1       1 
         915  CALL_FUNCTION_2       2 
         918  POP_TOP          
         919  JUMP_FORWARD         41  'to 963'

 296     922  LOAD_FAST             8  'node'
         925  LOAD_ATTR            22  'lab_pc'
         928  LOAD_ATTR            23  'SetString'
         931  LOAD_FAST            18  'info'
         934  LOAD_ATTR            18  'get'
         937  LOAD_CONST           14  'txt'
         940  CALL_FUNCTION_1       1 
         943  CALL_FUNCTION_1       1 
         946  POP_TOP          

 297     947  LOAD_FAST             8  'node'
         950  LOAD_ATTR            22  'lab_pc'
         953  LOAD_ATTR            25  'SetColor'
         956  LOAD_CONST           10  '#SK'
         959  CALL_FUNCTION_1       1 
         962  POP_TOP          
       963_0  COME_FROM                '919'

 298     963  LOAD_FAST             8  'node'
         966  LOAD_ATTR            20  'img_pc'
         969  LOAD_ATTR            27  'setVisible'
         972  LOAD_FAST            11  'is_show_icon'
         975  CALL_FUNCTION_1       1 
         978  POP_TOP          

 299     979  LOAD_FAST             8  'node'
         982  LOAD_ATTR            22  'lab_pc'
         985  LOAD_ATTR            27  'setVisible'
         988  LOAD_FAST            11  'is_show_icon'
         991  UNARY_NOT        
         992  CALL_FUNCTION_1       1 
         995  POP_TOP          

 301     996  LOAD_GLOBAL          28  'update_pc_tip_item_node_width'
         999  LOAD_FAST             8  'node'
        1002  LOAD_FAST            11  'is_show_icon'
        1005  CALL_FUNCTION_2       2 
        1008  POP_TOP          
        1009  JUMP_BACK           851  'to 851'
        1012  POP_BLOCK        
      1013_0  COME_FROM                '832'

 302    1013  LOAD_FAST             4  'temp_list_node'
        1016  LOAD_ATTR            29  'RefreshItemPos'
        1019  CALL_FUNCTION_0       0 
        1022  POP_TOP          

 303    1023  LOAD_FAST             2  'update_root_node_size'
        1026  POP_JUMP_IF_FALSE  1058  'to 1058'

 304    1029  LOAD_GLOBAL          30  'align_node_width_with_target'
        1032  LOAD_FAST             0  'temp_node'
        1035  LOAD_FAST             4  'temp_list_node'
        1038  CALL_FUNCTION_2       2 
        1041  POP_TOP          
        1042  JUMP_ABSOLUTE      1058  'to 1058'
        1045  JUMP_FORWARD         10  'to 1058'

 306    1048  LOAD_GLOBAL          35  'zero_node_width'
        1051  LOAD_FAST             0  'temp_node'
        1054  CALL_FUNCTION_1       1 
        1057  POP_TOP          
      1058_0  COME_FROM                '1045'
      1058_1  COME_FROM                '453'
        1058  LOAD_CONST            0  ''
        1061  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 51


def update_pc_tip_item_node_width(node, is_show_icon):
    _, h = node.GetContentSize()
    if is_show_icon:
        w, _ = node.img_pc.GetContentSize()
        node.SetContentSize(w, h)
    else:
        w, _ = node.img_bar.GetContentSize()
        node.SetContentSize(w, h)
    node.RecursionReConfPosition()


def align_node_width_with_target(aligned_node, target_node, offset=-30):
    _, h = aligned_node.GetContentSize()
    w, _ = target_node.GetContentSize()
    aligned_node.SetContentSize(w + offset, h)
    aligned_node.RecursionReConfPosition()


def zero_node_width(node):
    _, h = node.GetContentSize()
    node.SetContentSize(0, h)


def is_hotkey_down(hotkey_name):
    vk_name_list = get_hotkey_binding(hotkey_name)
    vk_code_list = vk_name_list_to_vk_code_list(vk_name_list)
    if vk_code_list is None:
        return False
    else:
        import logic.vscene.parts.ctrl.GamePyHook as game_hook
        for vk_code in vk_code_list:
            if is_mouse_btn(vk_code):
                if not global_data.mouse_mgr:
                    return False
                if not global_data.mouse_mgr.get_mouse_state(vk_code):
                    return False
            elif not game_hook.is_key_down(vk_code):
                return False
        else:
            return True

        return


def is_hotkey_up(hotkey_name):
    vk_name_list = get_hotkey_binding(hotkey_name)
    vk_code_list = vk_name_list_to_vk_code_list(vk_name_list)
    if vk_code_list is None:
        return True
    else:
        import logic.vscene.parts.ctrl.GamePyHook as game_hook
        for vk_code in vk_code_list:
            if is_mouse_btn(vk_code):
                if global_data.mouse_mgr.get_mouse_state(vk_code):
                    return False
            elif game_hook.is_key_down(vk_code):
                return False
        else:
            return True

        return


def get_hotkey_families(hotkey_name):
    from logic.client.const import hotkey_const
    for families in hotkey_const.HOTKET_FAMILIES_CATALOG:
        if hotkey_name in families:
            return families
    else:
        return set()


def is_hotkey_configurable(hotkey_name):
    from common.cfg import confmgr
    return confmgr.get('c_hot_key_config', str(hotkey_name), 'configurable', default=False)


def can_config_combination(hotkey_name):
    from logic.client.const import hotkey_const
    return is_hotkey_configurable(hotkey_name) and hotkey_name not in hotkey_const.COMBINATION_BLACKLIST


def is_two_category_conflict(question, against):
    for exception_couple_set in hotkey_const.EXCEPTION_NON_CONFLICT_CATALOG:
        if question in exception_couple_set and against in exception_couple_set:
            return False

    return question in hotkey_const.GENERAL_CONFLICT_SET and against in hotkey_const.GENERAL_CONFLICT_SET


def get_config_category(hotkey_name):
    from common.cfg import confmgr
    return confmgr.get('c_hot_key_config', str(hotkey_name), 'config_category', default=None)


def get_conflict_category(hotkey_name):
    from common.cfg import confmgr
    return confmgr.get('c_hot_key_config', str(hotkey_name), 'confict_category', default=None)


def get_hotkey_binding_vk_code_list(hotkey_name):
    vk_name_list = get_hotkey_binding(hotkey_name)
    return vk_name_list_to_vk_code_list(vk_name_list)


def get_conflict_hotkeys(hotkey_name, vk_code_list, conflict_against_vk_code_list_provider=None):
    import logic.vscene.parts.ctrl.GamePyHook as game_hook
    if not vk_code_list or vk_code_list == game_hook.PC_HOTKEY_CUSTOM_UNBIND_VK_CODE_LIST:
        return []
    else:
        catetory = get_conflict_category(hotkey_name)
        if catetory is None:
            return []
        conflict_hotkeys = set()
        for cat in get_conflict_catalog():
            if cat == catetory:
                continue
            if not is_two_category_conflict(cat, catetory):
                continue
            if not callable(conflict_against_vk_code_list_provider):
                conflict_against_vk_code_list_provider = get_hotkey_binding_vk_code_list
            for _hotkey_name in get_configurable_hotkeys_by_conflict(cat):
                against_vk_code_list = conflict_against_vk_code_list_provider(_hotkey_name)
                if not against_vk_code_list or against_vk_code_list == game_hook.PC_HOTKEY_CUSTOM_UNBIND_VK_CODE_LIST:
                    continue
                if against_vk_code_list == vk_code_list:
                    conflict_hotkeys.add(_hotkey_name)

        return list(conflict_hotkeys)


COMBIME_START_KEYS = {game.VK_LALT, game.VK_RALT, game.VK_LCTRL, game.VK_RCTRL, game.VK_LSHIFT, game.VK_RSHIFT}

def is_combine_start_key(vk_code):
    return vk_code in COMBIME_START_KEYS


def is_hot_key_unset(hotkey_name):
    vk_name_list = get_hotkey_binding(hotkey_name)
    if len(vk_name_list) == 1 and is_hot_key_unset_raw(vk_name_list[0]):
        return True
    else:
        return False


def is_hot_key_unset_raw(vk_name):
    import logic.vscene.parts.ctrl.GamePyHook as game_hook
    return vk_name == game_hook.PC_HOTKEY_CUSTOM_CACHE_UNBIND_STR_VAL


def is_hot_key_unset_raw_by_code(vk_code):
    import logic.vscene.parts.ctrl.GamePyHook as game_hook
    return vk_code == game_hook.PC_HOTKEY_CUSTOM_CACHE_UNBIND_INT_VAL


def is_hotkey_binding_out_of_sync_with_server():
    if not global_data.player:
        return False
    from logic.gcommon.common_const import ui_operation_const as uoc
    return global_data.player.is_setting_out_of_sync_2(uoc.PC_CUSTOM_HOTKEY_USER_CACHE_KEY)


def sync_hotkey_binding_to_server():
    if not global_data.player:
        return
    from logic.gcommon.common_const import ui_operation_const as uoc
    return global_data.player.sync_setting_to_server_2(uoc.PC_CUSTOM_HOTKEY_USER_CACHE_KEY)


def _read_hotkey_binding_from_user_setting(hotkey_name):
    if not global_data.player:
        return
    else:
        from logic.gcommon.common_const import ui_operation_const as uoc
        custom_override_cache = global_data.player.get_setting_2(uoc.PC_CUSTOM_HOTKEY_USER_CACHE_KEY)
        vk_code_list = custom_override_cache.get(hotkey_name, None)
        if vk_code_list is not None:
            if isinstance(vk_code_list, int):
                vk_name_list = vk_code_list_to_vk_name_list([vk_code_list])
                return vk_name_list
            if isinstance(vk_code_list, (tuple, list)):
                for vk_code in vk_code_list:
                    if not isinstance(vk_code, int):
                        log_error('Corrupted custom_override_cache', hotkey_name, vk_code_list)
                        break
                else:
                    vk_name_list = vk_code_list_to_vk_name_list(vk_code_list)
                    return vk_name_list

            else:
                log_error('Corrupted custom_override_cache', hotkey_name, vk_code_list)
        return


def get_hotkey_binding(hotkey_name):
    vk_name_list = _read_hotkey_binding_from_user_setting(hotkey_name)
    if vk_name_list is not None:
        return vk_name_list
    else:
        vk_name_list = hot_key_func_to_hot_key_name_spec_from_cfg(hotkey_name)
        if isinstance(vk_name_list, six.string_types):
            if vk_name_list == '':
                vk_name_list = []
            else:
                vk_name_list = [
                 vk_name_list]
        return vk_name_list


def restore_all_hotkey_bindings():
    if not global_data.player:
        return
    from logic.gcommon.common_const import ui_operation_const as uoc
    custom_override_cache = global_data.player.get_setting_2(uoc.PC_CUSTOM_HOTKEY_USER_CACHE_KEY)
    affected_hotkey_names = six_ex.keys(custom_override_cache)
    custom_override_cache = {}
    global_data.player.write_setting_2(uoc.PC_CUSTOM_HOTKEY_USER_CACHE_KEY, custom_override_cache, sync_to_server=False)
    if affected_hotkey_names:
        reregister_all_key_bindings()


def is_unbind(vk_code_list):
    import logic.vscene.parts.ctrl.GamePyHook as game_hook
    return vk_code_list == game_hook.PC_HOTKEY_CUSTOM_UNBIND_VK_CODE_LIST


def unbind_hotkey(hotkey_name, trigger_reregister):
    import logic.vscene.parts.ctrl.GamePyHook as game_hook
    bind_hotkey(hotkey_name, game_hook.PC_HOTKEY_CUSTOM_UNBIND_VK_CODE_LIST, trigger_reregister)


def bind_hotkey(hotkey_name, vk_code_list, trigger_reregister):
    families = get_hotkey_families(hotkey_name)
    if families:
        for _hotkey_name in families:
            bind_hotkey_single(_hotkey_name, vk_code_list, trigger_reregister)

    else:
        bind_hotkey_single(hotkey_name, vk_code_list, trigger_reregister)


def _write_hotkey_binding_to_user_setting(hotkey_name, vk_code_list):
    if not global_data.player:
        return False
    from logic.gcommon.common_const import ui_operation_const as uoc
    custom_override_cache = global_data.player.get_setting_2(uoc.PC_CUSTOM_HOTKEY_USER_CACHE_KEY)
    custom_override_cache[hotkey_name] = vk_code_list
    global_data.player.write_setting_2(uoc.PC_CUSTOM_HOTKEY_USER_CACHE_KEY, custom_override_cache, sync_to_server=False)
    return True


def bind_hotkey_single(hotkey_name, vk_code_list, trigger_reregister):
    if not hotkey_name:
        return
    if not vk_code_list or not isinstance(vk_code_list, list):
        return
    old = _read_hotkey_binding_from_user_setting(hotkey_name)
    ok = _write_hotkey_binding_to_user_setting(hotkey_name, vk_code_list)
    if ok:
        if old != vk_code_list:
            if trigger_reregister:
                reregister_all_key_bindings()


def reregister_all_key_bindings():
    if global_data.pc_ctrl_mgr:
        global_data.pc_ctrl_mgr.hot_key_conf_refresh()


def get_sorted_hotkey_catalog():
    from data import hot_key_config_catalog_def
    return hot_key_config_catalog_def.SORTED_CATALOG


def get_conflict_catalog():
    from data import hot_key_conflict_catalog_def
    return hot_key_conflict_catalog_def.CATALOG


def get_hotkey_category_name(key_category):
    from common.cfg import confmgr
    from logic.gcommon.common_utils.local_text import get_text_by_id
    name_id = confmgr.get('hot_key_config_catalog_cfg', str(key_category), 'name_id', default=None)
    if name_id is None:
        return ''
    else:
        return get_text_by_id(name_id)
        return


def get_hotkey_category_icon_path(key_category):
    from common.cfg import confmgr
    return confmgr.get('hot_key_config_catalog_cfg', str(key_category), 'icon_path', default='')


MOUSE_VK_CODES = {
 game.MOUSE_BUTTON_LEFT, game.MOUSE_BUTTON_RIGHT, game.MOUSE_BUTTON_MIDDLE, MOUSE_BUTTON_BACK, MOUSE_BUTTON_FORWARD}
MOUSE_VK_NAME = {'MOUSE_BUTTON_LEFT', 'MOUSE_BUTTON_RIGHT', 'MOUSE_BUTTON_MIDDLE', 'MOUSE_BUTTON_BACK', 'MOUSE_BUTTON_FORWARD'}

def has_mouse_btn_only(hotkey_name):
    vk_name_list = get_hotkey_binding(hotkey_name)
    return has_mouse_btn_only_raw(vk_name_list)


def has_mouse_btn_only_raw--- This code section failed: ---

 628       0  LOAD_GLOBAL           0  'len'
           3  LOAD_FAST             0  'vk_name_list'
           6  CALL_FUNCTION_1       1 
           9  LOAD_CONST            1  1
          12  COMPARE_OP            2  '=='
          15  POP_JUMP_IF_FALSE    42  'to 42'
          18  POP_JUMP_IF_FALSE     2  'to 2'
          21  BINARY_SUBSCR    
          22  LOAD_GLOBAL           1  'MOUSE_VK_NAME'
          25  COMPARE_OP            6  'in'
        28_0  COME_FROM                '15'
          28  POP_JUMP_IF_FALSE    42  'to 42'

 629      31  LOAD_GLOBAL           2  'True'
          34  LOAD_GLOBAL           2  'True'
          37  BINARY_SUBSCR    
          38  BUILD_TUPLE_2         2 
          41  RETURN_END_IF    
        42_0  COME_FROM                '28'

 631      42  LOAD_GLOBAL           3  'False'
          45  LOAD_CONST            0  ''
          48  BUILD_TUPLE_2         2 
          51  RETURN_VALUE     
          52  LOAD_CONST            0  ''
          55  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 18


def is_mouse_btn(vk_code):
    return vk_code in MOUSE_VK_CODES


def get_configurable_hotkeys(key_category):
    from data import hot_key_config_catalog
    return hot_key_config_catalog.CATALOG_DICT.get(str(key_category), [])


def get_configurable_hotkeys_by_conflict(conflict_cat):
    from data import hot_key_config_catalog
    return hot_key_config_catalog.CONFLICT_CATALOG_DICT.get(conflict_cat, [])


def get_hot_key_extra_arg(hot_key_name, arg_key, default=None):
    from common.cfg import confmgr
    return confmgr.get('c_hot_key_config', str(hot_key_name), 'cExtraArgs', arg_key, default=default)


def get_cur_need_implement_hot_key_funcs():
    need_imp_names = []
    from common.cfg import confmgr
    hot_key_conf = confmgr.get('c_hot_key_config')
    for hot_key_func_name, conf in six.iteritems(hot_key_conf):
        cHotKeyImp = conf.get('cHotKeyImp')
        if cHotKeyImp not in ('ui_imp', ):
            need_imp_names.append(hot_key_func_name)

    return need_imp_names


def is_keyboard_hot_key(hot_key_in):
    hot_key = hot_key_fix(hot_key_in)
    is_combine_key = is_combined_hot_key(hot_key)
    if is_combine_key:
        last_keycode = hot_key[-1]
    else:
        last_keycode = hot_key
    if not is_mouse_btn(last_keycode):
        return True
    return False


def hot_key_fix--- This code section failed: ---

 676       0  LOAD_GLOBAL           0  'type'
           3  LOAD_FAST             0  'hot_key'
           6  CALL_FUNCTION_1       1 
           9  LOAD_GLOBAL           1  'list'
          12  COMPARE_OP            2  '=='
          15  POP_JUMP_IF_FALSE    41  'to 41'
          18  LOAD_GLOBAL           2  'len'
          21  LOAD_FAST             0  'hot_key'
          24  CALL_FUNCTION_1       1 
          27  LOAD_CONST            1  1
          30  COMPARE_OP            2  '=='
        33_0  COME_FROM                '15'
          33  POP_JUMP_IF_FALSE    41  'to 41'

 677      36  POP_JUMP_IF_FALSE     2  'to 2'
          39  BINARY_SUBSCR    
          40  RETURN_END_IF    
        41_0  COME_FROM                '36'
        41_1  COME_FROM                '33'

 678      41  LOAD_FAST             0  'hot_key'
          44  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 36


def is_combined_hot_key(hot_key):
    return type(hot_key) == list and len(hot_key) > 1


def ui_switch_func(ui_name, ui_path, *args):
    from logic.client.const import game_mode_const
    from logic.gcommon.const import NEWBIE_STAGE_HUMAN_BATTLE, NEWBIE_STAGE_MECHA_BATTLE
    if global_data.player.in_local_battle():
        if global_data.player.logic:
            battle_tid = global_data.battle.get_battle_tid()
            if battle_tid == game_mode_const.QTE_LOCAL_BATTLE_TYPE:
                global_data.player.logic.send_event('E_LOCAL_BATTLE_ESC')
            elif battle_tid in (NEWBIE_STAGE_HUMAN_BATTLE, NEWBIE_STAGE_MECHA_BATTLE):
                global_data.player.logic.send_event('E_LOCAL_BATTLE_ESC_1_2')
            elif battle_tid == game_mode_const.NEWBIE_STAGE_THIRD_BATTLE_TYPE:
                global_data.player.logic.send_event('E_LOCAL_BATTLE_ESC_3')
            elif battle_tid == game_mode_const.NEWBIE_STAGE_FOURTH_BATTLE_TYPE:
                global_data.player.logic.send_event('E_LOCAL_BATTLE_ESC_4')
        return
    if not global_data.ui_mgr.get_ui(ui_name):
        can_open_settings = True
        if global_data.player and global_data.player.logic:
            if global_data.player.logic.sd.ref_in_aim:
                can_open_settings = False
        if can_open_settings:
            global_data.ui_mgr.show_ui(ui_name, ui_path)
    else:
        global_data.ui_mgr.close_ui(ui_name)


def check_has_player():
    if global_data.player:
        return True
    else:
        return False


def check_has_player_logic():
    if not (global_data.player and global_data.player.logic):
        return False
    return True


def check_player_in_normal_parachute_state():
    from logic.gcommon.common_utils.parachute_utils import STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_LAND
    normal_list = [
     STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_LAND]
    return check_player_in_parachute_state(normal_list)


def check_player_in_land_state():
    from logic.gcommon.common_utils.parachute_utils import STAGE_LAND
    normal_list = [
     STAGE_LAND]
    return check_player_in_parachute_state(normal_list)


def check_player_in_land_or_island_state():
    from logic.gcommon.common_utils.parachute_utils import STAGE_LAND, STAGE_ISLAND
    normal_list = [
     STAGE_LAND, STAGE_ISLAND]
    return check_player_in_parachute_state(normal_list)


def check_player_in_parachute_state(correct_state_list):
    if not check_has_player_logic():
        return False
    cur_stage = global_data.player.logic.share_data.ref_parachute_stage
    if cur_stage not in correct_state_list:
        return False
    return True


def switch_battle_bag_or_scoredetails_checker():
    if not global_data.game_mode:
        return False
    else:
        from logic.client.const import game_mode_const
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            return check_player_in_normal_parachute_state()
        if not global_data.player:
            return False
        if not global_data.player.is_in_battle():
            return False
        player = global_data.player.logic
        if player:
            if player.ev_g_death() or player.ev_g_defeated():
                return False
            if global_data.player.logic.ev_g_is_in_spectate():
                return False
        if global_data.ui_mgr.get_ui('MainSettingUI'):
            return False
        if global_data.ui_mgr.get_ui('MechaSummonUI'):
            return False
        if global_data.ui_mgr.get_ui('BigMapUI'):
            return False
        if global_data.ui_mgr.get_ui('DeathChooseWeaponUI'):
            return False
        return True


def switch_battle_bag():
    from logic.client.const.game_mode_const import GAME_MODE_SURVIVALS, GAME_MODE_PVES
    ui_inst = None
    if global_data.game_mode and global_data.game_mode.is_mode_type(GAME_MODE_SURVIVALS):
        ui_inst = global_data.ui_mgr.get_ui('BagUI')
    elif global_data.game_mode and global_data.game_mode.is_mode_type(GAME_MODE_PVES):
        switch_pve_info_ui()
        return
    if ui_inst:
        if ui_inst.is_appeared():
            ui_inst.disappear()
            global_data.sound_mgr.play_ui_sound('equipment_ui_close')
        else:
            ui_inst.appear()
            global_data.sound_mgr.play_ui_sound('equipment_ui_open')
    return


def switch_pve_info_ui():
    if global_data.battle and global_data.battle.is_settled():
        global_data.ui_mgr.close_ui('PVEInfoUI')
        return
    ui_inst = global_data.ui_mgr.get_ui('PVEInfoUI')
    if not ui_inst:
        global_data.ui_mgr.show_ui('PVEInfoUI', 'logic.comsys.control_ui')
        global_data.sound_mgr.play_ui_sound('equipment_ui_open')
    elif ui_inst.is_appeared():
        ui_inst.disappear()
        global_data.sound_mgr.play_ui_sound('equipment_ui_close')
    else:
        ui_inst.appear()
        global_data.sound_mgr.play_ui_sound('equipment_ui_open')


def switch_scavenge_battle_bag():
    from logic.client.const import game_mode_const
    if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SCAVENGE):
        ui_inst = global_data.ui_mgr.get_ui('BagUI')
        if ui_inst:
            if ui_inst.is_appeared():
                ui_inst.disappear()
                global_data.sound_mgr.play_ui_sound('equipment_ui_close')
            else:
                ui_inst.appear()
                global_data.sound_mgr.play_ui_sound('equipment_ui_open')


def switch_scoredetails(keycode, msg):
    from logic.client.const import game_mode_const
    if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DEATH, game_mode_const.GAME_MODE_SNIPE, game_mode_const.GAME_MODE_HUMAN_DEATH, game_mode_const.GAME_MODE_SCAVENGE, game_mode_const.GAME_MODE_RANDOM_DEATH)):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('DeathScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('DeathScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('DeathScoreDetailsUI', 'logic.comsys.battle.Death')
    elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL)):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('GVGScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('GVGScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('GVGScoreDetailsUI', 'logic.comsys.battle.gvg')
    elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_FFA):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('FFAScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('FFAScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('FFAScoreDetailsUI', 'logic.comsys.battle.ffa')
    elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CLONE):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('CloneScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('CloneScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('CloneScoreDetailsUI', 'logic.comsys.battle.Clone')
    elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_IMPROVISE):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('ImproviseScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('ImproviseScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('ImproviseScoreDetailsUI', 'logic.comsys.battle.Improvise')
    elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_MECHA_DEATH, game_mode_const.GAME_MODE_GOOSE_BEAR)):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('MechaDeathScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('MechaDeathScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('MechaDeathScoreDetailsUI', 'logic.comsys.battle.MechaDeath')
    elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_ZOMBIE_FFA):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('ZombieFFAScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('ZombieFFAScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('ZombieFFAScoreDetailsUI', 'logic.comsys.battle.ZombieFFA')
    elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_ARMRACE):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('ArmRaceScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('ArmRaceScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('ArmRaceScoreDetailsUI', 'logic.comsys.battle.ArmRace')
    elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CONTROL):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('OccupyScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('OccupyScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('OccupyScoreDetailsUI', 'logic.comsys.battle.Occupy')
    elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_FLAG, game_mode_const.GAME_MODE_FLAG2)):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('FlagScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('FlagScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('FlagScoreDetailsUI', 'logic.comsys.battle.Flag')
    elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CROWN):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('CrownScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('CrownScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('CrownScoreDetailsUI', 'logic.comsys.battle.Crown')
    elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_CRYSTAL, game_mode_const.GAME_MODE_ADCRYSTAL)):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('CrystalScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('CrystalScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('CrystalScoreDetailsUI', 'logic.comsys.battle.Crystal')
    elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_MUTIOCCUPY):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('MutiOccupyScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('MutiOccupyScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('MutiOccupyScoreDetailsUI', 'logic.comsys.battle.MutiOccupy')
    elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_TRAIN):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('TrainScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('TrainScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('TrainScoreDetailsUI', 'logic.comsys.battle.Train')
    elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_ASSAULT):
        if msg == game.MSG_KEY_DOWN:
            ui_inst = global_data.ui_mgr.get_ui('AssaultScoreDetailsUI')
            if ui_inst:
                global_data.ui_mgr.close_ui('AssaultScoreDetailsUI')
            else:
                global_data.ui_mgr.show_ui('AssaultScoreDetailsUI', 'logic.comsys.battle.Assault')


def move_checker():
    if global_data.battle and global_data.battle.is_settled() and not global_data.battle.is_in_settle_celebrate_stage():
        return False
    if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_death():
        return False
    return True


def move_forward(keycode, msg):
    if is_down_msg(msg):
        if not move_checker():
            return
    if not global_data.moveKeyboardMgr:
        return
    if msg == game.MSG_KEY_UP and global_data.moveKeyboardMgr.is_move_locked():
        vk_add_down_time = key_down_time.get(game.VK_ADD, 0)
        vk_w_down_time = key_down_time.get(game.VK_W, 0)
        if vk_add_down_time > vk_w_down_time:
            return
    global_data.moveKeyboardMgr.process_input(game.VK_W, msg)
    if msg == game.MSG_KEY_DOWN:
        key_down_time[game.VK_W] = time.time()
        global_data.moveKeyboardMgr.stop_move_lock()


def move_backward(keycode, msg):
    if is_down_msg(msg):
        if not move_checker():
            return
    if not global_data.moveKeyboardMgr:
        return
    global_data.moveKeyboardMgr.process_input(game.VK_S, msg)
    if msg == game.MSG_KEY_DOWN:
        global_data.moveKeyboardMgr.stop_move_lock()


def move_left(keycode, msg):
    if is_down_msg(msg):
        if not move_checker():
            return
    if not global_data.moveKeyboardMgr:
        return
    global_data.moveKeyboardMgr.process_input(game.VK_A, msg)
    if msg == game.MSG_KEY_DOWN:
        global_data.moveKeyboardMgr.stop_move_lock()


def move_right(keycode, msg):
    if is_down_msg(msg):
        if not move_checker():
            return
    if not global_data.moveKeyboardMgr:
        return
    global_data.moveKeyboardMgr.process_input(game.VK_D, msg)
    if msg == game.MSG_KEY_DOWN:
        global_data.moveKeyboardMgr.stop_move_lock()


def lock_move_rocker_checker():
    from logic.vscene.parts.ctrl.ShortcutFunctionalityMutex import is_any_shortcut_functionality_claimed_by_others, not_front_movement_shortcut_names, drive_movement_shortcut_names
    if is_any_shortcut_functionality_claimed_by_others(not_front_movement_shortcut_names + drive_movement_shortcut_names, 'lock_move_rocker_keyboard'):
        return False
    if global_data.is_judge_ob:
        return False
    ui = global_data.ui_mgr.get_ui('MoveRockerUI')
    if ui:
        if ui.get_is_run_lock():
            return False
    if not global_data.player:
        return False
    if not global_data.player.is_in_battle():
        return False
    if global_data.player.logic:
        control_target = global_data.player.logic.ev_g_control_target()
        if control_target and control_target.logic and control_target.logic.ev_g_is_mechatran():
            from logic.gcommon.common_const import mecha_const
            if control_target.logic.ev_g_pattern() == mecha_const.MECHA_PATTERN_VEHICLE:
                return False
    from logic.gutils.move_utils import can_move
    if not can_move():
        return False
    return True


def lock_move_rocker(keycode, msg):
    if not global_data.moveKeyboardMgr:
        return False
    if global_data.is_judge_ob:
        return False
    global_data.moveKeyboardMgr.toggle_move_rocker_lock_shortcut_wrapper(keycode, msg)
    if msg == game.MSG_KEY_DOWN:
        key_down_time[game.VK_ADD] = time.time()


def try_to_run(keycode, msg):
    if global_data.moveKeyboardMgr:
        global_data.moveKeyboardMgr.start_acc_process_input(keycode, msg)


def switch_pc_mode():
    if not global_data.player:
        return
    none_before = not global_data.pc_ctrl_mgr
    if none_before:
        from logic.vscene.parts.ctrl.PCCtrlManager import PCCtrlManager
        PCCtrlManager()
    if not global_data.pc_ctrl_mgr.get_pc_control_switch_enabled():
        return
    if none_before:
        global_data.pc_ctrl_mgr.enable_PC_control(True)
    else:
        global_data.pc_ctrl_mgr.enable_PC_control(not global_data.pc_ctrl_mgr.is_pc_control_enable())


def use_car_transform(msg, keycode):
    if global_data.mecha and global_data.mecha.__class__.__name__ == 'MechaTrans' and global_data.mecha.logic:
        global_data.mecha.logic.send_event('E_TRY_TRANSFORM')


def use_car_rush(msg, keycode):
    from logic.gutils.move_utils import can_move
    if not can_move():
        return
    from logic.gcommon.common_const import mecha_const as mconst
    if global_data.mecha:
        if global_data.mecha.__class__.__name__ == 'MechaTrans':
            if global_data.mecha.logic:
                pattern = global_data.mecha.logic.ev_g_pattern()
                if pattern == mconst.MECHA_TYPE_VEHICLE:
                    global_data.mecha.logic.send_event('E_TRY_VEHICLE_DASH')
        elif global_data.mecha.__class__.__name__ == 'Motorcycle':
            if global_data.mecha.logic:
                if global_data.mecha.logic.sd.ref_avatar_seat_idx != 0:
                    return
            global_data.mecha.logic.send_event('E_BEGIN_OR_END_VEHICLE_DASH')


def get_off_vehicle_or_skateboard(msg, keycode):
    if global_data.player and global_data.player.logic:
        if global_data.player.logic.ev_g_in_mecha('MechaTrans') or global_data.player.logic.ev_g_in_mecha('Motorcycle'):
            global_data.player.logic.send_event('E_TRY_LEAVE_MECHA')
        lplayer = global_data.player.logic
        if lplayer.sd.ref_controlling_tv_missile_launcher:
            ui = global_data.ui_mgr.get_ui('TVMissileLauncherUI')
            ui and ui.on_get_off()
        entity_id = lplayer.ev_g_attachable_entity_id()
        if not entity_id:
            return
        if lplayer.ev_g_is_jump():
            return
        lplayer.send_event('E_LEAVE_ATTACHABLE_ENTITY')


def interact_with_pet(*args):
    if global_data.player_pet and global_data.player_pet.logic:
        ui = global_data.ui_mgr.get_ui('PetInteractUI')
        if ui:
            global_data.ui_mgr.close_ui('PetInteractUI')
        else:
            global_data.ui_mgr.show_ui('PetInteractUI', 'logic.comsys.pet')


def on_switch_seat(*args):
    if not global_data.player or not global_data.player.logic:
        return
    global_data.player.logic.send_event('E_CHANGE_SEAT')


def on_reload(*args):
    if not global_data.player or not global_data.player.logic:
        return
    if not global_data.mecha or not global_data.mecha.logic:
        return
    seat_idx = global_data.mecha.logic.sd.ref_avatar_seat_idx
    if seat_idx == 2:
        global_data.emgr.pc_hotkey_try_reload.emit()
    else:
        global_data.mecha.logic.send_event('E_CLICK_RELOAD_UI')


from logic.gutils.lobby_jump_utils import lobby_jump

def human_jump(msg, keycode):
    if global_data.player and not global_data.player.is_in_battle() and global_data.lobby_player:
        lobby_jump()
        return
    from logic.gutils.climb_utils import on_begin_jump_btn_exc
    if global_data.cam_lctarget and global_data.cam_lctarget.__class__.__name__ == 'LAvatar':
        on_begin_jump_btn_exc()


def human_squat(msg, keycode):
    import logic.gutils.character_ctrl_utils as character_ctrl_utils
    if global_data.player and global_data.player.logic:
        lplayer = global_data.player.logic
        if not lplayer:
            return
        if lplayer.ev_g_is_stand():
            character_ctrl_utils.try_stand_to_squat(lplayer)
        elif lplayer.ev_g_is_crouch():
            character_ctrl_utils.try_squat_to_stand(lplayer)


def human_roll(msg, keycode):
    from logic.gutils.move_utils import can_roll
    from logic.gcommon.common_const.skill_const import SKILL_ROLL
    from logic.gcommon.cdata import status_config
    if not global_data.player:
        return
    player = global_data.player.logic
    if not player:
        return
    if not can_roll():
        return
    if not player.ev_g_can_cast_skill(SKILL_ROLL):
        return
    if not player.ev_g_is_equip_rush_bone():
        player.send_event('E_CLICK_ROLL')
        if not player.ev_g_status_check_pass(status_config.ST_ROLL):
            return
        player.send_event('E_CTRL_ROLL')
    else:
        player.send_event('E_CTRL_RUSH')


def try_switch_gun_mode(msg, keycode):
    if global_data.player and global_data.player.logic:
        cur_weapon = global_data.player.logic.ev_g_wpbar_cur_weapon()
        if cur_weapon and cur_weapon.is_multi_wp():
            global_data.player.logic.send_event('E_SWITCH_WEAPON_MODE')


def human_reload(msg, keycode):
    from logic.gcommon.cdata import status_config
    from logic.gcommon import const
    if global_data.cam_lplayer:
        lplayer = global_data.cam_lplayer
    else:
        lplayer = None
    if not lplayer:
        return
    else:
        if not lplayer.ev_g_status_check_pass(status_config.ST_RELOAD):
            return
        weapon_pos = lplayer.ev_g_wpbar_cur_weapon_pos()
        if weapon_pos in const.MAIN_WEAPON_LIST:
            weapon_data = lplayer.ev_g_wpbar_get_by_pos(weapon_pos)
            if weapon_data is None:
                weapon_data = None if 1 else weapon_data.get_data()
                return weapon_data or None
            cur_bullet_num = weapon_data.get('iBulletNum', 0)
            wp = lplayer.ev_g_wpbar_get_by_pos(weapon_pos)
            if wp:
                max_bullet = wp.get_bullet_cap()
                if cur_bullet_num != max_bullet:
                    lplayer.send_event('E_TRY_RELOAD')
        return


def use_cur_item(msg, keycode):
    drug_ui = global_data.ui_mgr.get_ui('DrugUIPC')
    if not drug_ui:
        return
    drug_ui.keyboard_use_cur_item()


def toggle_keyboard_run_switch(keycode, msg):
    if global_data.moveKeyboardMgr:
        global_data.moveKeyboardMgr.set_run_switch_state(not global_data.moveKeyboardMgr.get_run_switch_state())
        global_data.moveKeyboardMgr.process_input(keycode, game.MSG_KEY_DOWN)


def human_fire(keycode, msg):
    from logic.vscene.parts.keyboard.HumanFireKeyboardMgr import HumanFireKeyboardMgr
    inst = HumanFireKeyboardMgr()
    inst.process_input(keycode, msg)


def fullscreen_switch_func():
    if not global_data.pc_ctrl_mgr:
        return
    global_data.pc_ctrl_mgr.request_fullscreen(not global_data.pc_ctrl_mgr.is_fullscreen(), req_from_setting_ui=False, persistent=True)


def exit_game():
    import game3d
    game3d.exit()


def paste_text():
    import game3d
    clipboard_text = game3d.get_clipboard_text()
    if clipboard_text:
        global_data.emgr.pc_paste_text.emit(clipboard_text)


def toggle_pc_hotkey_hint():
    if not global_data.pc_ctrl_mgr:
        return
    global_data.pc_ctrl_mgr.set_pc_hotkey_hint_switch(not global_data.pc_ctrl_mgr.get_pc_hotkey_hint_switch(), persistent=True)


def get_ui_mouse_scroll_sensitivity--- This code section failed: ---

1306       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('confmgr',)
           6  IMPORT_NAME           0  'common.cfg'
           9  IMPORT_FROM           1  'confmgr'
          12  STORE_FAST            1  'confmgr'
          15  POP_TOP          

1307      16  LOAD_FAST             1  'confmgr'
          19  LOAD_ATTR             2  'get'
          22  LOAD_CONST            3  'c_hot_key_parameter'
          25  LOAD_CONST            4  'ui_scroll_sensitivity_dict'
          28  LOAD_CONST            5  'default'
          31  LOAD_CONST            0  ''
          34  CALL_FUNCTION_259   259 
          37  STORE_FAST            2  's'

1308      40  LOAD_FAST             2  's'
          43  POP_JUMP_IF_TRUE     71  'to 71'

1309      46  LOAD_FAST             1  'confmgr'
          49  LOAD_ATTR             2  'get'
          52  LOAD_CONST            3  'c_hot_key_parameter'
          55  LOAD_CONST            4  'ui_scroll_sensitivity_dict'
          58  LOAD_CONST            6  'Default'
          61  LOAD_CONST            5  'default'
          64  LOAD_CONST            7  200
          67  CALL_FUNCTION_259   259 
          70  RETURN_END_IF    
        71_0  COME_FROM                '43'

1311      71  LOAD_FAST             2  's'
          74  RETURN_VALUE     
          75  LOAD_CONST            0  ''
          78  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_259' instruction at offset 34


def is_down_msg(msg):
    is_down = msg in [game.MSG_KEY_DOWN, game.MSG_MOUSE_DOWN]
    return is_down


def is_up_msg(msg):
    return not is_down_msg(msg)


def switch_judge_camera():
    from logic.gutils.judge_utils import is_ob
    if not is_ob():
        return
    if global_data.ui_mgr.get_ui('JudgeObserveUINew'):
        ui = global_data.ui_mgr.get_ui('JudgeObserveUINew')
        if ui:
            ui.try_free_camera()
    elif global_data.ui_mgr.get_ui('JudgeObserveUINewPC'):
        ui = global_data.ui_mgr.get_ui('JudgeObserveUINew')
        if ui:
            ui.try_free_camera()
    elif not bool(global_data.is_in_judge_camera):
        if global_data.cam_lplayer:
            global_data.emgr.try_switch_judge_camera_event.emit(not bool(global_data.is_in_judge_camera))
    else:
        global_data.emgr.try_switch_judge_camera_event.emit(not bool(global_data.is_in_judge_camera))


def judge_north_team():
    import math3d
    if not global_data.is_judge_ob:
        return
    if not global_data.player:
        return
    pid = global_data.player.logic.ev_g_spectate_target_id()
    from logic.gutils.judge_utils import get_ob_nearest_team_in_direction, try_switch_ob_target
    target_pid = get_ob_nearest_team_in_direction(pid, math3d.vector(0, 0, 1))
    if target_pid:
        try_switch_ob_target(target_pid)


def judge_south_team():
    if not global_data.is_judge_ob:
        return
    import math3d
    if not global_data.is_judge_ob:
        return
    if not global_data.player:
        return
    pid = global_data.player.logic.ev_g_spectate_target_id()
    from logic.gutils.judge_utils import get_ob_nearest_team_in_direction, try_switch_ob_target
    target_pid = get_ob_nearest_team_in_direction(pid, math3d.vector(0, 0, -1))
    if target_pid:
        try_switch_ob_target(target_pid)


def judge_west_team():
    if not global_data.is_judge_ob:
        return
    import math3d
    if not global_data.is_judge_ob:
        return
    if not global_data.player:
        return
    pid = global_data.player.logic.ev_g_spectate_target_id()
    from logic.gutils.judge_utils import get_ob_nearest_team_in_direction, try_switch_ob_target
    target_pid = get_ob_nearest_team_in_direction(pid, math3d.vector(-1, 0, 0))
    if target_pid:
        try_switch_ob_target(target_pid)


def judge_east_team():
    if not global_data.is_judge_ob:
        return
    if not global_data.is_judge_ob:
        return
    import math3d
    if not global_data.is_judge_ob:
        return
    if not global_data.player:
        return
    pid = global_data.player.logic.ev_g_spectate_target_id()
    from logic.gutils.judge_utils import get_ob_nearest_team_in_direction, try_switch_ob_target
    target_pid = get_ob_nearest_team_in_direction(pid, math3d.vector(1, 0, 0))
    if target_pid:
        try_switch_ob_target(target_pid)


def judge_previous_teammate--- This code section failed: ---

1402       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'is_judge_ob'
           6  POP_JUMP_IF_TRUE     13  'to 13'

1403       9  LOAD_GLOBAL           2  'False'
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

1404      13  LOAD_GLOBAL           0  'global_data'
          16  LOAD_ATTR             3  'player'
          19  POP_JUMP_IF_TRUE     26  'to 26'

1405      22  LOAD_GLOBAL           2  'False'
          25  RETURN_END_IF    
        26_0  COME_FROM                '19'

1406      26  LOAD_GLOBAL           0  'global_data'
          29  LOAD_ATTR             3  'player'
          32  LOAD_ATTR             4  'logic'
          35  LOAD_ATTR             5  'ev_g_spectate_target_id'
          38  CALL_FUNCTION_0       0 
          41  STORE_FAST            0  'pid'

1407      44  LOAD_CONST            1  ''
          47  LOAD_CONST            2  ('judge_switch_to_another_teammate', 'try_switch_ob_target')
          50  IMPORT_NAME           6  'logic.gutils.judge_utils'
          53  IMPORT_FROM           7  'judge_switch_to_another_teammate'
          56  STORE_FAST            1  'judge_switch_to_another_teammate'
          59  IMPORT_FROM           8  'try_switch_ob_target'
          62  STORE_FAST            2  'try_switch_ob_target'
          65  POP_TOP          

1408      66  LOAD_FAST             1  'judge_switch_to_another_teammate'
          69  LOAD_FAST             3  'target_pid'
          72  CALL_FUNCTION_2       2 
          75  STORE_FAST            3  'target_pid'

1409      78  LOAD_FAST             3  'target_pid'
          81  POP_JUMP_IF_FALSE    97  'to 97'

1410      84  LOAD_FAST             2  'try_switch_ob_target'
          87  LOAD_FAST             3  'target_pid'
          90  CALL_FUNCTION_1       1 
          93  POP_TOP          
          94  JUMP_FORWARD          0  'to 97'
        97_0  COME_FROM                '94'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 72


def judge_next_teammate--- This code section failed: ---

1413       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'is_judge_ob'
           6  POP_JUMP_IF_TRUE     13  'to 13'

1414       9  LOAD_GLOBAL           2  'False'
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

1415      13  LOAD_GLOBAL           0  'global_data'
          16  LOAD_ATTR             3  'player'
          19  POP_JUMP_IF_TRUE     26  'to 26'

1416      22  LOAD_GLOBAL           2  'False'
          25  RETURN_END_IF    
        26_0  COME_FROM                '19'

1417      26  LOAD_GLOBAL           0  'global_data'
          29  LOAD_ATTR             3  'player'
          32  LOAD_ATTR             4  'logic'
          35  LOAD_ATTR             5  'ev_g_spectate_target_id'
          38  CALL_FUNCTION_0       0 
          41  STORE_FAST            0  'pid'

1418      44  LOAD_CONST            1  ''
          47  LOAD_CONST            2  ('judge_switch_to_another_teammate', 'try_switch_ob_target')
          50  IMPORT_NAME           6  'logic.gutils.judge_utils'
          53  IMPORT_FROM           7  'judge_switch_to_another_teammate'
          56  STORE_FAST            1  'judge_switch_to_another_teammate'
          59  IMPORT_FROM           8  'try_switch_ob_target'
          62  STORE_FAST            2  'try_switch_ob_target'
          65  POP_TOP          

1419      66  LOAD_FAST             1  'judge_switch_to_another_teammate'
          69  LOAD_FAST             3  'target_pid'
          72  CALL_FUNCTION_2       2 
          75  STORE_FAST            3  'target_pid'

1420      78  LOAD_FAST             3  'target_pid'
          81  POP_JUMP_IF_FALSE    97  'to 97'

1421      84  LOAD_FAST             2  'try_switch_ob_target'
          87  LOAD_FAST             3  'target_pid'
          90  CALL_FUNCTION_1       1 
          93  POP_TOP          
          94  JUMP_FORWARD          0  'to 97'
        97_0  COME_FROM                '94'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 72


def judge_hide_details():
    if not global_data.is_judge_ob:
        return False
    global_data.judge_need_hide_details = not global_data.judge_need_hide_details
    global_data.emgr.judge_need_hide_details_event.emit()


def judge_kick_out_player_func():
    if not global_data.player:
        return
    from logic.gutils import judge_utils
    if not judge_utils.is_ob():
        return
    ob_target_id = judge_utils.get_ob_target_id()
    global_data.player.call_server_method('ob_kick_out_player', (ob_target_id,))


def get_cur_key_name_by_func_code(hot_key_func_code):
    from common.cfg import confmgr
    from logic.gcommon.common_utils.local_text import get_text_by_id
    hot_key_name_list = []
    if isinstance(hot_key_func_code, list):
        for func_code in hot_key_func_code:
            hot_key_name_list.extend(get_hotkey_binding(func_code))

    elif isinstance(hot_key_func_code, str):
        hot_key_name_list = get_hotkey_binding(hot_key_func_code)
    display_name_list = []
    if hot_key_name_list:
        for key_name in hot_key_name_list:
            key_conf = confmgr.get('c_key_name_config', str(key_name), default={})
            key_name_text_id = key_conf.get('cKeyName', 0)
            if not key_name_text_id:
                key_name_text = key_conf.get('cKeyNameText', None)
                if key_name_text is not None:
                    display_name_list.append(key_name_text)
                else:
                    display_name_list.append(get_hot_key_short_display_name(key_name))
            else:
                display_name_list.append(get_text_by_id(key_name_text_id))

        return ','.join(display_name_list)
    else:
        return ''
        return


def get_google_play_pc_input_sdk_key_map():
    mouse_btn_2_code = {game.MOUSE_BUTTON_LEFT: 10,
       game.MOUSE_BUTTON_RIGHT: 1,
       game.MOUSE_BUTTON_MIDDLE: 2
       }
    import json
    map_dict = {'input_version': '1.0.0'}
    key_map_dict = {}
    hotkey_catalog = get_sorted_hotkey_catalog()
    map_dict['groups'] = hotkey_catalog
    action_dict = {}
    for ordinal, cat in enumerate(hotkey_catalog):
        hotkey_names = get_configurable_hotkeys(cat)
        key_map_dict[cat] = {'gname': get_hotkey_category_name(cat),'actions': hotkey_names}
        for hotkey_idx, hotkey_name in enumerate(hotkey_names):
            desc = get_hot_key_fun_desc(hotkey_name)
            configurable = is_hotkey_configurable(hotkey_name)
            vk_name_list = get_hotkey_binding(hotkey_name)
            vk_code_list = vk_name_list_to_vk_code_list(vk_name_list)
            is_mouse = any([ vk_code in mouse_btn_2_code for vk_code in vk_code_list ])
            if is_mouse:
                vk_code_list = [ mouse_btn_2_code[vk_code] for vk_code in vk_code_list if vk_code in mouse_btn_2_code ]
            configurable = False
            action_dict[hotkey_name] = {'name': desc,'configurable': configurable,'vk_code_list': vk_code_list,'is_mouse': is_mouse}

    map_dict['group_dict'] = key_map_dict
    map_dict['action_dict'] = action_dict
    map_dict_str = json.dumps(map_dict)
    return map_dict_str


def test():
    from logic.gutils.hot_key_utils import get_sorted_hotkey_catalog, get_configurable_hotkeys, get_hot_key_fun_desc, is_hotkey_configurable, get_hotkey_binding, get_hotkey_category_name, vk_name_list_to_vk_code_list
    import json
    map_dict = {'input_version': '1.0.0'}
    key_map_dict = {}
    hotkey_catalog = get_sorted_hotkey_catalog()
    map_dict['groups'] = hotkey_catalog
    action_dict = {}
    for ordinal, cat in enumerate(hotkey_catalog):
        if ordinal > 0:
            continue
        hotkey_names = get_configurable_hotkeys(cat)
        key_map_dict[cat] = {'gname': get_hotkey_category_name(cat),'actions': hotkey_names}
        for hotkey_idx, hotkey_name in enumerate(hotkey_names):
            desc = get_hot_key_fun_desc(hotkey_name)
            configurable = is_hotkey_configurable(hotkey_name)
            vk_name_list = get_hotkey_binding(hotkey_name)
            vk_code_list = vk_name_list_to_vk_code_list(vk_name_list)
            action_dict[hotkey_name] = {'name': desc,'configurable': configurable,'vk_code_list': vk_code_list}

    map_dict['group_dict'] = key_map_dict
    map_dict['action_dict'] = action_dict
    map_dict_str = json.dumps(map_dict)
    import game3d
    game3d.update_google_input_sdk_mapping(map_dict_str)
    return map_dict_str