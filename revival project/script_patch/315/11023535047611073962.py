# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/trigger_gift_utils.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.common_utils.local_text import get_text_by_id, get_cur_text_lang, LANG_CN, LANG_ZHTW
from common.cfg import confmgr
from logic.gutils import mall_utils
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN
from logic.gcommon.common_const import shop_const
from logic.comsys.charge_ui.LeftTimeCountDownWidget import LeftTimeCountDownWidget
from logic.gcommon import time_utility as tutil
INTRO_TYPE_2_TEXT = {'A': 608300,
   'B': 608301,
   'C': 608302,
   'D': 608303,
   'E': 608304,
   'F': 608305,
   'G': 608306
   }

def get_gift_recommend_type(intro_level):
    if intro_level in shop_const.TRIGGER_GIFT_SKIN_RECOMMEND_TYPES:
        return shop_const.TRIGGER_GIFT_RECOMMEND_TYPE_SKIN
    return shop_const.TRIGGER_GIFT_RECOMMEND_TYPE_OTHER_ITEMS


def get_gift_intro_text--- This code section failed: ---

  33       0  LOAD_FAST             0  'intro_params'
           3  POP_JUMP_IF_TRUE     10  'to 10'

  34       6  LOAD_CONST            0  ''
           9  RETURN_END_IF    
        10_0  COME_FROM                '3'

  35      10  RETURN_VALUE     
          11  RETURN_VALUE     
          12  RETURN_VALUE     
          13  BINARY_SUBSCR    
          14  STORE_FAST            2  'intro_type'

  36      17  LOAD_FAST             1  'skin_goods_id'
          20  POP_JUMP_IF_FALSE    66  'to 66'
          23  LOAD_FAST             2  'intro_type'
          26  LOAD_CONST            2  'B'
          29  COMPARE_OP            2  '=='
        32_0  COME_FROM                '20'
          32  POP_JUMP_IF_FALSE    66  'to 66'

  37      35  LOAD_GLOBAL           1  'mall_utils'
          38  LOAD_ATTR             2  'get_goods_belong_item_name'
          41  LOAD_FAST             1  'skin_goods_id'
          44  CALL_FUNCTION_1       1 
          47  STORE_FAST            3  'belong_item_name'

  38      50  LOAD_FAST             0  'intro_params'
          53  LOAD_ATTR             3  'append'
          56  LOAD_FAST             3  'belong_item_name'
          59  CALL_FUNCTION_1       1 
          62  POP_TOP          
          63  JUMP_FORWARD          0  'to 66'
        66_0  COME_FROM                '63'

  39      66  LOAD_GLOBAL           4  'INTRO_TYPE_2_TEXT'
          69  LOAD_ATTR             5  'get'
          72  LOAD_FAST             2  'intro_type'
          75  CALL_FUNCTION_1       1 
          78  STORE_FAST            4  'text_id'

  40      81  LOAD_FAST             4  'text_id'
          84  POP_JUMP_IF_TRUE     91  'to 91'

  41      87  LOAD_CONST            0  ''
          90  RETURN_END_IF    
        91_0  COME_FROM                '84'

  42      91  LOAD_GLOBAL           6  'len'
          94  LOAD_FAST             0  'intro_params'
          97  CALL_FUNCTION_1       1 
         100  LOAD_CONST            3  1
         103  COMPARE_OP            2  '=='
         106  POP_JUMP_IF_FALSE   119  'to 119'

  43     109  LOAD_GLOBAL           7  'get_text_by_id'
         112  LOAD_FAST             4  'text_id'
         115  CALL_FUNCTION_1       1 
         118  RETURN_END_IF    
       119_0  COME_FROM                '106'

  44     119  LOAD_GLOBAL           6  'len'
         122  LOAD_FAST             0  'intro_params'
         125  CALL_FUNCTION_1       1 
         128  LOAD_CONST            3  1
         131  COMPARE_OP            4  '>'
         134  POP_JUMP_IF_FALSE   157  'to 157'

  45     137  LOAD_GLOBAL           7  'get_text_by_id'
         140  LOAD_FAST             4  'text_id'
         143  CALL_FUNCTION_1       1 
         146  LOAD_ATTR             8  'format'
         149  LOAD_ATTR             3  'append'
         152  SLICE+1          
         153  CALL_FUNCTION_VAR_0     0 
         156  RETURN_END_IF    
       157_0  COME_FROM                '134'
         157  LOAD_CONST            0  ''
         160  RETURN_VALUE     

Parse error at or near `RETURN_VALUE' instruction at offset 10


def get_skin_goods_id(goods_list):
    for goods_id in goods_list:
        item_no = mall_utils.get_goods_item_no(goods_id)
        lobby_i_type = item_utils.get_lobby_item_type(item_no)
        if lobby_i_type in [L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN]:
            return goods_id

    return None


def get_role_display_img_path(fashion_id):
    role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
    img_path = role_skin_config.get(str(fashion_id), {}).get('img_role')
    return img_path


def get_mecha_display_img_path(fashion_id):
    mecha_skin_config = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
    img_path = mecha_skin_config.get(str(fashion_id), {}).get('img_path')
    return img_path


def is_valid_discount_value(discount_value):
    return 0 < shop_const.TRIGGER_GIFT_MIN_DISCOUNT <= discount_value <= 1


def get_gift_discount_text--- This code section failed: ---

  77       0  LOAD_GLOBAL           0  'is_valid_discount_value'
           3  LOAD_FAST             0  'discount_value'
           6  CALL_FUNCTION_1       1 
           9  POP_JUMP_IF_FALSE   118  'to 118'

  78      12  LOAD_FAST             1  'lang_choice'
          15  LOAD_GLOBAL           1  'LANG_CN'
          18  LOAD_GLOBAL           2  'LANG_ZHTW'
          21  BUILD_LIST_2          2 
          24  COMPARE_OP            6  'in'
          27  POP_JUMP_IF_FALSE    91  'to 91'

  79      30  LOAD_CONST            1  '%.1f'
          33  LOAD_CONST            2  10
          36  BINARY_MULTIPLY  
          37  BINARY_MODULO    
          38  STORE_FAST            2  'discount_value_text'

  80      41  LOAD_FAST             2  'discount_value_text'
          44  LOAD_ATTR             3  'endswith'
          47  LOAD_CONST            3  '.0'
          50  CALL_FUNCTION_1       1 
          53  POP_JUMP_IF_FALSE    78  'to 78'

  81      56  LOAD_GLOBAL           4  'str'
          59  LOAD_GLOBAL           5  'int'
          62  LOAD_GLOBAL           2  'LANG_ZHTW'
          65  BINARY_MULTIPLY  
          66  CALL_FUNCTION_1       1 
          69  CALL_FUNCTION_1       1 
          72  STORE_FAST            2  'discount_value_text'
          75  JUMP_FORWARD          0  'to 78'
        78_0  COME_FROM                '75'

  82      78  LOAD_CONST            4  '{}'
          81  LOAD_ATTR             6  'format'
          84  LOAD_FAST             2  'discount_value_text'
          87  CALL_FUNCTION_1       1 
          90  RETURN_END_IF    
        91_0  COME_FROM                '27'

  84      91  LOAD_CONST            5  '{}%'
          94  LOAD_ATTR             6  'format'
          97  LOAD_CONST            6  100
         100  LOAD_GLOBAL           5  'int'
         103  LOAD_GLOBAL           6  'format'
         106  BINARY_MULTIPLY  
         107  CALL_FUNCTION_1       1 
         110  BINARY_SUBTRACT  
         111  CALL_FUNCTION_1       1 
         114  RETURN_VALUE     
         115  JUMP_FORWARD          0  'to 118'
       118_0  COME_FROM                '115'

  85     118  LOAD_CONST            7  ''
         121  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_MODULO' instruction at offset 37


def format_discount_ui_text(discount_value, panel, show_discount_cn=False):
    lang_choice = get_cur_text_lang()
    discount_text = get_gift_discount_text(discount_value, lang_choice)
    print('format_discount_ui_text', discount_text)
    if discount_text:
        if lang_choice in [LANG_CN, LANG_ZHTW]:
            if show_discount_cn:
                panel.lab_discount_cn.SetString(get_text_by_id(608311).format(discount_text))
            else:
                panel.lab_discount_cn.SetString(discount_text)
            panel.lab_discount_cn.setVisible(True)
            panel.lab_discount_en.setVisible(False)
        else:
            panel.lab_discount_en.SetString(discount_text)
            panel.lab_discount_en.setVisible(True)
            panel.lab_discount_cn.setVisible(False)
    else:
        panel.lab_discount_en.setVisible(False)
        panel.lab_discount_cn.setVisible(False)


def get_discount_text_with_lang--- This code section failed: ---

 109       0  LOAD_FAST             1  'lang_choice'
           3  LOAD_GLOBAL           0  'LANG_CN'
           6  LOAD_GLOBAL           1  'LANG_ZHTW'
           9  BUILD_LIST_2          2 
          12  COMPARE_OP            6  'in'
          15  POP_JUMP_IF_FALSE    53  'to 53'

 110      18  LOAD_CONST            1  '{:g}'
          21  LOAD_ATTR             2  'format'
          24  LOAD_ATTR             2  'format'
          27  BINARY_MULTIPLY  
          28  CALL_FUNCTION_1       1 
          31  STORE_FAST            2  'discount_str'

 111      34  LOAD_GLOBAL           3  'get_text_by_id'
          37  LOAD_CONST            3  608311
          40  CALL_FUNCTION_1       1 
          43  LOAD_ATTR             2  'format'
          46  LOAD_FAST             2  'discount_str'
          49  CALL_FUNCTION_1       1 
          52  RETURN_END_IF    
        53_0  COME_FROM                '15'

 113      53  LOAD_GLOBAL           3  'get_text_by_id'
          56  LOAD_CONST            3  608311
          59  CALL_FUNCTION_1       1 
          62  LOAD_ATTR             2  'format'
          65  LOAD_CONST            4  100
          68  LOAD_GLOBAL           4  'int'
          71  LOAD_GLOBAL           4  'int'
          74  BINARY_MULTIPLY  
          75  CALL_FUNCTION_1       1 
          78  BINARY_SUBTRACT  
          79  CALL_FUNCTION_1       1 
          82  RETURN_VALUE     

Parse error at or near `BINARY_MULTIPLY' instruction at offset 27


def get_gift_ui_animation_names(is_skin_ui, is_open, item_type=None, item_num=1):
    if is_skin_ui:
        if item_type == L_ITEM_TYPE_MECHA_SKIN and item_num == 1:
            if is_open:
                return ['appear2', 'loop']
            return 'disappear2'
        if item_type == L_ITEM_TYPE_MECHA_SKIN and item_num > 1:
            if is_open:
                return ['appear2', 'appear_item', 'loop']
            return 'disappear2'
        if item_type == L_ITEM_TYPE_ROLE_SKIN and item_num == 1:
            if is_open:
                return ['appear', 'loop']
            return 'disappear1'
        if item_type == L_ITEM_TYPE_ROLE_SKIN and item_num > 1:
            if is_open:
                return ['appear', 'appear_item', 'loop']
            return 'disappear1'
    else:
        if is_open:
            return ['appear', 'loop']
        return 'disappear'


def init_template_lobby_btn_gifts--- This code section failed: ---

 142       0  LOAD_FAST             1  'gift_info'
           3  LOAD_ATTR             0  'get'
           6  LOAD_CONST            1  'show_discount'
           9  LOAD_CONST            0  ''
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            2  'show_discount'

 143      18  LOAD_FAST             2  'show_discount'
          21  LOAD_CONST            0  ''
          24  COMPARE_OP            9  'is-not'
          27  POP_JUMP_IF_FALSE    49  'to 49'

 144      30  LOAD_GLOBAL           2  'format_discount_ui_text'
          33  LOAD_FAST             2  'show_discount'
          36  LOAD_FAST             2  'show_discount'
          39  LOAD_GLOBAL           3  'True'
          42  CALL_FUNCTION_258   258 
          45  POP_TOP          
          46  JUMP_FORWARD         28  'to 77'

 146      49  LOAD_GLOBAL           2  'format_discount_ui_text'
          52  LOAD_FAST             1  'gift_info'
          55  LOAD_ATTR             0  'get'
          58  LOAD_CONST            3  'discount'
          61  LOAD_CONST            4  ''
          64  CALL_FUNCTION_2       2 
          67  CALL_FUNCTION_2       2 
          70  LOAD_GLOBAL           3  'True'
          73  CALL_FUNCTION_258   258 
          76  POP_TOP          
        77_0  COME_FROM                '46'

 147      77  LOAD_FAST             1  'gift_info'
          80  LOAD_ATTR             0  'get'
          83  LOAD_CONST            5  'cash_only'
          86  LOAD_CONST            4  ''
          89  CALL_FUNCTION_2       2 
          92  STORE_FAST            3  'cash_only'

 148      95  LOAD_FAST             3  'cash_only'
          98  POP_JUMP_IF_FALSE   120  'to 120'

 149     101  LOAD_FAST             0  'temp_item_ui'
         104  LOAD_ATTR             4  'lab_gifts_name'
         107  LOAD_ATTR             5  'SetString'
         110  LOAD_CONST            6  12131
         113  CALL_FUNCTION_1       1 
         116  POP_TOP          
         117  JUMP_FORWARD         16  'to 136'

 151     120  LOAD_FAST             0  'temp_item_ui'
         123  LOAD_ATTR             4  'lab_gifts_name'
         126  LOAD_ATTR             5  'SetString'
         129  LOAD_CONST            7  608310
         132  CALL_FUNCTION_1       1 
         135  POP_TOP          
       136_0  COME_FROM                '117'

 152     136  LOAD_FAST             0  'temp_item_ui'
         139  LOAD_ATTR             6  'PlayAnimation'
         142  LOAD_CONST            8  'show_charge'
         145  CALL_FUNCTION_1       1 
         148  POP_TOP          

 153     149  LOAD_FAST             0  'temp_item_ui'
         152  LOAD_ATTR             6  'PlayAnimation'
         155  LOAD_CONST            9  'loop_charge'
         158  CALL_FUNCTION_1       1 
         161  POP_TOP          

 154     162  LOAD_GLOBAL           7  'LeftTimeCountDownWidget'
         165  LOAD_FAST             0  'temp_item_ui'
         168  LOAD_FAST             0  'temp_item_ui'
         171  LOAD_ATTR             8  'nd_time'
         174  LOAD_ATTR             9  'lab_time'
         177  LOAD_LAMBDA              '<code_object <lambda>>'
         180  MAKE_FUNCTION_0       0 
         183  CALL_FUNCTION_3       3 
         186  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_258' instruction at offset 42


def init_template_lobby_btn_battle_pass(temp_item_ui, gift_info):
    temp_item_ui.PlayAnimation('show')
    return LeftTimeCountDownWidget(temp_item_ui, temp_item_ui.nd_time.lab_time, lambda timestamp: get_text_by_id(607014).format(tutil.get_delta_time_str(timestamp)))