# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/reward_item_ui_utils.py
from __future__ import absolute_import
import six_ex
import six
from logic.gcommon.item.item_const import RARE_DEGREE_0, RARE_DEGREE_1, RARE_DEGREE_2, RARE_DEGREE_3, RARE_DEGREE_4, RARE_DEGREE_5, RARE_DEGREE_6, RARE_DEGREE_7
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_item_rare_degree
from logic.gutils.custom_ui_utils import get_cut_name
import cc
REWARD_APPEAR_ANIM = {RARE_DEGREE_0: 'appear_common',
   RARE_DEGREE_1: 'appear_green',
   RARE_DEGREE_2: 'appear_blue',
   RARE_DEGREE_3: 'appear_purple',
   RARE_DEGREE_4: 'appear_orange',
   RARE_DEGREE_5: 'appear_ssp',
   RARE_DEGREE_6: 'appear_red',
   RARE_DEGREE_7: 'appear_ssp'
   }
REWARD_IDLE_ANIM = {RARE_DEGREE_1: 'green',
   RARE_DEGREE_2: 'blue',
   RARE_DEGREE_3: 'purple',
   RARE_DEGREE_4: 'orange',
   RARE_DEGREE_5: 'ssp',
   RARE_DEGREE_6: 'red',
   RARE_DEGREE_7: 'ssp'
   }
REWARD_RARE_COLOR = {RARE_DEGREE_0: 'white',
   RARE_DEGREE_1: 'green',
   RARE_DEGREE_2: 'blue',
   RARE_DEGREE_3: 'purple',
   RARE_DEGREE_4: 'orange',
   RARE_DEGREE_5: 'color',
   RARE_DEGREE_6: 'red',
   RARE_DEGREE_7: 'color'
   }

def _get_item_rare_degree(item_no, item_num):
    rare_degree = get_item_rare_degree(item_no, item_num, ignore_imporve=True)
    if rare_degree not in REWARD_RARE_COLOR:
        rare_degree = RARE_DEGREE_0
    return rare_degree


def smash_item_info(nd_item, item_id, item_num, show_tips=False):
    from logic.gutils import template_utils
    nd_item.nd_smash_item.setVisible(True)
    nd_item.nd_smash_item.setScale(1)
    smash_item = getattr(nd_item.temp_reward, 'nd_smash_item')
    if not smash_item:
        return
    template_utils.init_tempate_mall_i_item(smash_item, item_id, item_num=item_num, templatePath=smash_item.GetTemplatePath(), ignore_improve=True, show_tips=show_tips)
    return smash_item


def refresh_item_info--- This code section failed: ---

  69       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('template_utils',)
           6  IMPORT_NAME           0  'logic.gutils'
           9  IMPORT_FROM           1  'template_utils'
          12  STORE_FAST            5  'template_utils'
          15  POP_TOP          

  70      16  LOAD_CONST            1  ''
          19  LOAD_CONST            3  ('get_lobby_item_pic_by_item_no', 'get_lobby_item_use_parms', 'get_lobby_item_type')
          22  IMPORT_NAME           2  'logic.gutils.item_utils'
          25  IMPORT_FROM           3  'get_lobby_item_pic_by_item_no'
          28  STORE_FAST            6  'get_lobby_item_pic_by_item_no'
          31  IMPORT_FROM           4  'get_lobby_item_use_parms'
          34  STORE_FAST            7  'get_lobby_item_use_parms'
          37  IMPORT_FROM           5  'get_lobby_item_type'
          40  STORE_FAST            8  'get_lobby_item_type'
          43  POP_TOP          

  71      44  LOAD_CONST            1  ''
          47  LOAD_CONST            4  ('L_ITEM_TYPE_NEW_MECHA_COMPONENT',)
          50  IMPORT_NAME           6  'logic.gcommon.item.lobby_item_type'
          53  IMPORT_FROM           7  'L_ITEM_TYPE_NEW_MECHA_COMPONENT'
          56  STORE_FAST            9  'L_ITEM_TYPE_NEW_MECHA_COMPONENT'
          59  POP_TOP          

  73      60  LOAD_FAST             8  'get_lobby_item_type'
          63  LOAD_FAST             1  'item_id'
          66  CALL_FUNCTION_1       1 
          69  LOAD_FAST             9  'L_ITEM_TYPE_NEW_MECHA_COMPONENT'
          72  COMPARE_OP            2  '=='
          75  POP_JUMP_IF_FALSE   323  'to 323'

  74      78  LOAD_FAST             0  'nd_item'
          81  LOAD_ATTR             8  'temp_reward'
          84  LOAD_ATTR             9  'setVisible'
          87  LOAD_GLOBAL          10  'False'
          90  CALL_FUNCTION_1       1 
          93  POP_TOP          

  75      94  LOAD_GLOBAL          11  'hasattr'
          97  LOAD_GLOBAL           5  'get_lobby_item_type'
         100  CALL_FUNCTION_2       2 
         103  POP_JUMP_IF_FALSE   131  'to 131'
         106  LOAD_FAST             0  'nd_item'
         109  LOAD_ATTR            12  'complex_item'
       112_0  COME_FROM                '103'
         112  POP_JUMP_IF_FALSE   131  'to 131'

  76     115  LOAD_FAST             0  'nd_item'
         118  LOAD_ATTR            12  'complex_item'
         121  LOAD_ATTR            13  'Destroy'
         124  CALL_FUNCTION_0       0 
         127  POP_TOP          
         128  JUMP_FORWARD          0  'to 131'
       131_0  COME_FROM                '128'

  77     131  LOAD_GLOBAL          14  'global_data'
         134  LOAD_ATTR            15  'uisystem'
         137  LOAD_ATTR            16  'load_template_create'
         140  LOAD_CONST            6  'mech_display/inscription/i_inscription_icon_item'
         143  LOAD_CONST            7  'parent'
         146  LOAD_FAST             0  'nd_item'
         149  LOAD_ATTR             8  'temp_reward'
         152  LOAD_ATTR            17  'GetParent'
         155  CALL_FUNCTION_0       0 
         158  LOAD_CONST            8  'name'
         161  LOAD_CONST            5  'complex_item'
         164  CALL_FUNCTION_513   513 
         167  STORE_FAST           10  'nd'

  78     170  LOAD_CONST            1  ''
         173  LOAD_CONST            9  ('init_component_slot_temp',)
         176  IMPORT_NAME          18  'logic.gutils.inscription_utils'
         179  IMPORT_FROM          19  'init_component_slot_temp'
         182  STORE_FAST           11  'init_component_slot_temp'
         185  POP_TOP          

  79     186  LOAD_FAST            11  'init_component_slot_temp'
         189  LOAD_FAST            10  'nd'
         192  LOAD_FAST             1  'item_id'
         195  CALL_FUNCTION_2       2 
         198  POP_TOP          

  80     199  LOAD_FAST            10  'nd'
         202  LOAD_ATTR            20  'setScale'
         205  LOAD_CONST           10  0.37
         208  CALL_FUNCTION_1       1 
         211  POP_TOP          

  81     212  LOAD_FAST            10  'nd'
         215  LOAD_ATTR            21  'setPosition'
         218  LOAD_FAST             0  'nd_item'
         221  LOAD_ATTR             8  'temp_reward'
         224  LOAD_ATTR            22  'getPosition'
         227  CALL_FUNCTION_0       0 
         230  CALL_FUNCTION_1       1 
         233  POP_TOP          

  82     234  LOAD_FAST            10  'nd'
         237  LOAD_ATTR            23  'setAnchorPoint'
         240  LOAD_FAST             0  'nd_item'
         243  LOAD_ATTR             8  'temp_reward'
         246  LOAD_ATTR            24  'getAnchorPoint'
         249  CALL_FUNCTION_0       0 
         252  CALL_FUNCTION_1       1 
         255  POP_TOP          

  83     256  LOAD_FAST             0  'nd_item'
         259  LOAD_ATTR            25  'nd_purple'
         262  LOAD_ATTR             9  'setVisible'
         265  LOAD_GLOBAL          10  'False'
         268  CALL_FUNCTION_1       1 
         271  POP_TOP          

  84     272  LOAD_FAST             0  'nd_item'
         275  LOAD_ATTR            26  'nd_orange'
         278  LOAD_ATTR             9  'setVisible'
         281  LOAD_GLOBAL          10  'False'
         284  CALL_FUNCTION_1       1 
         287  POP_TOP          

  85     288  LOAD_FAST             0  'nd_item'
         291  LOAD_ATTR            27  'nd_green'
         294  LOAD_ATTR             9  'setVisible'
         297  LOAD_GLOBAL          10  'False'
         300  CALL_FUNCTION_1       1 
         303  POP_TOP          

  86     304  LOAD_FAST             0  'nd_item'
         307  LOAD_ATTR            28  'nd_blue'
         310  LOAD_ATTR             9  'setVisible'
         313  LOAD_GLOBAL          10  'False'
         316  CALL_FUNCTION_1       1 
         319  POP_TOP          
         320  JUMP_FORWARD        169  'to 492'

  88     323  LOAD_FAST             0  'nd_item'
         326  LOAD_ATTR             8  'temp_reward'
         329  LOAD_ATTR             9  'setVisible'
         332  LOAD_GLOBAL          29  'True'
         335  CALL_FUNCTION_1       1 
         338  POP_TOP          

  89     339  LOAD_FAST             0  'nd_item'
         342  LOAD_ATTR            25  'nd_purple'
         345  LOAD_ATTR             9  'setVisible'
         348  LOAD_GLOBAL          29  'True'
         351  CALL_FUNCTION_1       1 
         354  POP_TOP          

  90     355  LOAD_FAST             0  'nd_item'
         358  LOAD_ATTR            26  'nd_orange'
         361  LOAD_ATTR             9  'setVisible'
         364  LOAD_GLOBAL          29  'True'
         367  CALL_FUNCTION_1       1 
         370  POP_TOP          

  91     371  LOAD_FAST             0  'nd_item'
         374  LOAD_ATTR            27  'nd_green'
         377  LOAD_ATTR             9  'setVisible'
         380  LOAD_GLOBAL          29  'True'
         383  CALL_FUNCTION_1       1 
         386  POP_TOP          

  92     387  LOAD_FAST             0  'nd_item'
         390  LOAD_ATTR            28  'nd_blue'
         393  LOAD_ATTR             9  'setVisible'
         396  LOAD_GLOBAL          29  'True'
         399  CALL_FUNCTION_1       1 
         402  POP_TOP          

  93     403  LOAD_GLOBAL          11  'hasattr'
         406  LOAD_GLOBAL           5  'get_lobby_item_type'
         409  CALL_FUNCTION_2       2 
         412  POP_JUMP_IF_FALSE   440  'to 440'
         415  LOAD_FAST             0  'nd_item'
         418  LOAD_ATTR            12  'complex_item'
       421_0  COME_FROM                '412'
         421  POP_JUMP_IF_FALSE   440  'to 440'

  94     424  LOAD_FAST             0  'nd_item'
         427  LOAD_ATTR            12  'complex_item'
         430  LOAD_ATTR            13  'Destroy'
         433  CALL_FUNCTION_0       0 
         436  POP_TOP          
         437  JUMP_FORWARD          0  'to 440'
       440_0  COME_FROM                '437'

  95     440  LOAD_FAST             5  'template_utils'
         443  LOAD_ATTR            30  'init_tempate_mall_i_item'
         446  LOAD_FAST             0  'nd_item'
         449  LOAD_ATTR             8  'temp_reward'
         452  LOAD_FAST             1  'item_id'
         455  LOAD_CONST           11  'item_num'
         458  LOAD_FAST             2  'item_num'
         461  LOAD_CONST           12  'templatePath'
         464  LOAD_FAST             0  'nd_item'
         467  LOAD_ATTR             8  'temp_reward'
         470  LOAD_ATTR            31  'GetTemplatePath'
         473  CALL_FUNCTION_0       0 
         476  LOAD_CONST           13  'ignore_improve'
         479  LOAD_GLOBAL          29  'True'
         482  LOAD_CONST           14  'show_tips'
         485  LOAD_FAST             3  'show_tips'
         488  CALL_FUNCTION_1026  1026 
         491  POP_TOP          
       492_0  COME_FROM                '320'

  96     492  LOAD_GLOBAL          32  'get_lobby_item_name'
         495  LOAD_FAST             1  'item_id'
         498  CALL_FUNCTION_1       1 
         501  STORE_FAST           12  'item_name'

  97     504  LOAD_FAST             0  'nd_item'
         507  LOAD_ATTR            33  'lab_item_name'
         510  LOAD_ATTR            34  'SetString'
         513  LOAD_GLOBAL          35  'get_cut_name'
         516  LOAD_GLOBAL          36  'six'
         519  LOAD_ATTR            37  'text_type'
         522  LOAD_FAST            12  'item_name'
         525  CALL_FUNCTION_1       1 
         528  LOAD_FAST             4  'max_len'
         531  CALL_FUNCTION_2       2 
         534  CALL_FUNCTION_1       1 
         537  POP_TOP          

  98     538  LOAD_FAST             0  'nd_item'
         541  LOAD_ATTR            38  'nd_smash_item'
         544  LOAD_ATTR             9  'setVisible'
         547  LOAD_GLOBAL          10  'False'
         550  CALL_FUNCTION_1       1 
         553  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 100


def play_item_appear_to_idle_animation(nd_item, item_id, item_num, callback=None, need_reset_node=False, callback_advance_rate=1.0, after_smash=False, action_tag_id=None):
    rare_degree = _get_item_rare_degree(item_id, item_num)
    action_list = []
    if need_reset_node:
        for anim_name in six.itervalues(REWARD_IDLE_ANIM):
            nd_item.StopAnimation(anim_name)

        action_list.append(cc.CallFunc.create(lambda : nd_item.setVisible(False)))
        action_list.append(cc.CallFunc.create(lambda : nd_item.PlayAnimation('clean_idle_anim')))
    anim_open_name = REWARD_APPEAR_ANIM[rare_degree]
    action_list.append(cc.CallFunc.create(lambda : nd_item.PlayAnimation(anim_open_name)))
    action_list.append(cc.DelayTime.create(0.03))
    action_list.append(cc.CallFunc.create(lambda : nd_item.setVisible(True)))
    open_duration = nd_item.GetAnimationMaxRunTime(anim_open_name)
    open_duration *= callback_advance_rate
    action_list.append(cc.DelayTime.create(open_duration))
    anim_idle_name = REWARD_IDLE_ANIM.get(rare_degree, None)
    if anim_idle_name:
        action_list.append(cc.CallFunc.create(lambda : nd_item.PlayAnimation(anim_idle_name)))
    if callback and callable(callback):
        if after_smash:
            action_list.append(cc.DelayTime.create(max(0, 1.7 - open_duration)))
        action_list.append(cc.CallFunc.create(callback))
    action = nd_item.runAction(cc.Sequence.create(action_list))
    action_tag_id and action.setTag(action_tag_id)
    return


def play_item_with_smash_animation(nd_item, origin_item_id, origin_item_count, chip_item_id, chip_item_count, callback=None):
    action_list = []
    origin_rare_degree = _get_item_rare_degree(origin_item_id, origin_item_count)
    origin_open_name = REWARD_APPEAR_ANIM[origin_rare_degree]
    action_list.append(cc.CallFunc.create(lambda : nd_item.setVisible(True)))
    action_list.append(cc.CallFunc.create(lambda : nd_item.PlayAnimation(origin_open_name)))
    action_list.append(cc.DelayTime.create(nd_item.GetAnimationMaxRunTime(origin_open_name) + 0.25))
    action_list.append(cc.CallFunc.create(lambda : nd_item.PlayAnimation('smash')))
    action_list.append(cc.DelayTime.create(nd_item.GetAnimationMaxRunTime('smash')))
    action_list.append(cc.CallFunc.create(lambda : smash_item_info(nd_item, chip_item_id, chip_item_count)))
    action_list.append(cc.CallFunc.create(lambda : play_item_appear_to_idle_animation(nd_item, chip_item_id, chip_item_count, callback=lambda : nd_item.PlayAnimation('smash_scale'), need_reset_node=True)))
    if callback and callable(callback):
        action_list.append(cc.CallFunc.create(callback))
    nd_item.runAction(cc.Sequence.create(action_list))


def find_cur_active_probability_up_data(reward_id, probability_up_list):
    probability_up_data = []
    for tab_data_conf in probability_up_list:
        tab_id, tab_data = tab_data_conf
        if tab_id == str(reward_id):
            probability_up_data = tab_data

    cur_time_span_probability_data = None
    from logic.gcommon import time_utility
    cur_time_stamp = time_utility.get_server_time()
    for time_span_prob in probability_up_data:
        start_time, end_time, probability_data, banner_layout = time_span_prob
        if start_time <= cur_time_stamp < end_time:
            cur_time_span_probability_data = list(time_span_prob)
            break

    return cur_time_span_probability_data


def process_lottery_probability_up_data(lottery_table_id, probability_data):
    from common.cfg import confmgr
    sorted_rank_types = sorted(six_ex.keys(probability_data), reverse=True)
    conf_name = 'preview_%s' % str(lottery_table_id)
    conf = confmgr.get(conf_name, default=None)
    probability_dict = {}
    sorted_item_no_list = []
    for rank_type in sorted_rank_types:
        sorted_inner_keys = sorted(six_ex.keys(probability_data[rank_type]), key=lambda x: conf.get(str(x), 1.0))
        probability_dict.update(probability_data[rank_type])
        sorted_item_no_list.extend(sorted_inner_keys)

    return (sorted_item_no_list, probability_dict)