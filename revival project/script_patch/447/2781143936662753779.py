# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/guide_utils.py
from __future__ import absolute_import
import six
from logic.comsys.guide_ui.GuideSetting import GuideSetting
from cocosui import cc
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN

def check_need_xingyuan_guide():
    from logic.gutils.bond_utils import need_bond_guided
    if GuideSetting()._create_login:
        return False
    if need_bond_guided():
        return False
    return True


def check_need_battle_flag_guide():
    return False
    if not global_data.new_sys_open_mgr:
        return False
    from logic.gutils.career_utils import get_owned_badge_ids
    from logic.gcommon.common_const.new_system_prompt_data import SYSTEM_BATTLE_FLAG
    has_badge = len(get_owned_badge_ids()) > 0
    if global_data.new_sys_open_mgr.meet_lv_condition(SYSTEM_BATTLE_FLAG) and has_badge:
        return True
    return False


def check_need_lottery_activity_guide():
    return True


def check_need_inscr_guide_1():
    return True


def check_need_inscr_guide_2():
    return True


def check_need_inscr_guide_3():
    return True


def check_is_not_newbee_guide():
    if GuideSetting()._create_login:
        return False
    return True


def get_inscr_list_btn():
    ui = global_data.ui_mgr.get_ui('InscriptionMainUI')
    if ui:
        return ui.get_inscr_list_tab_btn()
    else:
        return None


def get_battle_flag_page_guide_parent_node():
    ui = global_data.ui_mgr.get_ui('PlayerInfoUI')
    if ui:
        return ui.get_battle_flag_page_tab_btn()
    else:
        return None


def check_need_skin_define_guide():
    if not global_data.player.mecha_custom_skin_open():
        return False
    if GuideSetting()._create_login:
        return False
    mecha_num = len(global_data.player.get_items_by_type(L_ITEM_TYPE_MECHA))
    mecha_skin_num = len(global_data.player.get_items_by_type(L_ITEM_TYPE_MECHA_SKIN))
    if mecha_skin_num <= mecha_num:
        return False
    if global_data.achi_mgr.get_cur_user_archive_data('skin_define'):
        return False
    return True


def get_name_string_path(nd, ctrl_path):
    try:
        ctrlnamelist = ctrl_path.split('.')
        ctrl = nd
        for name in ctrlnamelist:
            ctrl = getattr(ctrl, name)

        return ctrl
    except Exception as e:
        log_error('get_name_path failed for ctrl path', ctrl_path, e)


def resolve_guide_node_name(nd, node_name):
    if type(node_name) is dict:
        node_name_dict = node_name
        list_name = node_name_dict.get('list')
        func_name = node_name_dict.get('func')
        if list_name:
            list_nd = resolve_guide_node_name(nd, list_name)
            index = node_name_dict.get('index')
            if list_nd is not None and index is not None:
                return list_nd.GetItem(index)
            else:
                return

        elif func_name:
            from logic.gutils import guide_utils
            func = getattr(guide_utils, func_name)
            if func:
                return func()
            log_error('unsupport name dict', node_name_dict)
        else:
            log_error('unsupport name dict', node_name_dict)
    else:
        return get_name_string_path(nd, node_name)
    return


def parse_guide_click_action(start_nd, click_action):
    if not click_action:
        return
    parsed_click_action = {}
    for ctrl_path, action_conf in six.iteritems(click_action):
        ctrlnamelist = ctrl_path.rsplit('.', 1)
        event_name = ctrlnamelist[1]
        com_path = ctrlnamelist[0]
        if com_path == '_else_':
            parsed_click_action.setdefault(com_path, {})
            parsed_click_action[com_path].update({event_name: action_conf})
        else:
            nd = resolve_guide_node_name(start_nd, com_path)
            if nd:
                parsed_click_action.setdefault(nd, {})
                parsed_click_action[nd].update({event_name: action_conf})

    return parsed_click_action


def get_guide_conf_nd(ui_inst, ui_name, ui_guide_dict, name_key='parent'):
    parent_name = ui_guide_dict.get(name_key)
    page_name = ui_guide_dict.get('page')
    if parent_name:
        if page_name:
            page_inst = ui_inst.get_sub_page(page_name)
            start_nd = page_inst.panel
        else:
            start_nd = ui_inst.panel
        nd = resolve_guide_node_name(start_nd, parent_name)
        return nd
    else:
        return None


def active_guide_with_finish(from_guide_name, action_func_list):
    global_data.lobby_guide_mgr.deactivate_guide_by_name(from_guide_name)
    guide_name = action_func_list[1]
    if global_data.lobby_guide_mgr.check_can_activate_by_guide_name(guide_name):
        global_data.lobby_guide_mgr.on_notify_check_guide(guide_name)


def show_top_guide_temp--- This code section failed: ---

 154       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('template_utils',)
           6  IMPORT_NAME           0  'logic.gutils'
           9  IMPORT_FROM           1  'template_utils'
          12  STORE_FAST            4  'template_utils'
          15  POP_TOP          

 155      16  LOAD_GLOBAL           2  'global_data'
          19  LOAD_ATTR             3  'ui_mgr'
          22  LOAD_ATTR             4  'get_ui'
          25  LOAD_FAST             2  'ui_name'
          28  CALL_FUNCTION_1       1 
          31  STORE_FAST            5  'ui_inst'

 156      34  LOAD_FAST             5  'ui_inst'
          37  POP_JUMP_IF_TRUE     44  'to 44'

 157      40  LOAD_CONST            0  ''
          43  RETURN_END_IF    
        44_0  COME_FROM                '37'

 158      44  LOAD_FAST             3  'ui_guide_dict'
          47  LOAD_ATTR             5  'get'
          50  LOAD_CONST            3  'page'
          53  CALL_FUNCTION_1       1 
          56  STORE_FAST            6  'page_name'

 159      59  LOAD_FAST             6  'page_name'
          62  POP_JUMP_IF_FALSE    93  'to 93'

 160      65  LOAD_FAST             5  'ui_inst'
          68  LOAD_ATTR             6  'get_sub_page'
          71  LOAD_FAST             6  'page_name'
          74  CALL_FUNCTION_1       1 
          77  STORE_FAST            7  'page'

 161      80  LOAD_FAST             7  'page'
          83  POP_JUMP_IF_TRUE     93  'to 93'

 162      86  LOAD_CONST            0  ''
          89  RETURN_END_IF    
        90_0  COME_FROM                '83'
          90  JUMP_FORWARD          0  'to 93'
        93_0  COME_FROM                '90'

 164      93  LOAD_GLOBAL           7  'get_guide_conf_nd'
          96  LOAD_FAST             5  'ui_inst'
          99  LOAD_FAST             2  'ui_name'
         102  LOAD_FAST             3  'ui_guide_dict'
         105  CALL_FUNCTION_3       3 
         108  STORE_FAST            8  'parent_nd'

 165     111  LOAD_FAST             3  'ui_guide_dict'
         114  LOAD_ATTR             5  'get'
         117  LOAD_CONST            4  'text'
         120  CALL_FUNCTION_1       1 
         123  STORE_FAST            9  'text'

 166     126  LOAD_FAST             3  'ui_guide_dict'
         129  LOAD_ATTR             5  'get'
         132  LOAD_CONST            5  'template_path'
         135  LOAD_CONST            0  ''
         138  CALL_FUNCTION_2       2 
         141  STORE_FAST           10  'temp_path'

 167     144  LOAD_FAST             3  'ui_guide_dict'
         147  LOAD_ATTR             5  'get'
         150  LOAD_CONST            6  'pos_offset'
         153  LOAD_CONST           25  (0, 0)
         156  CALL_FUNCTION_2       2 
         159  STORE_FAST           11  'pos_offset'

 168     162  LOAD_FAST             3  'ui_guide_dict'
         165  LOAD_ATTR             5  'get'
         168  LOAD_CONST            7  'is_force'
         171  LOAD_CONST            1  ''
         174  CALL_FUNCTION_2       2 
         177  STORE_FAST           12  'is_force'

 169     180  LOAD_FAST             3  'ui_guide_dict'
         183  LOAD_ATTR             5  'get'
         186  LOAD_CONST            8  'parent'
         189  CALL_FUNCTION_1       1 
         192  STORE_FAST           13  'parent_name'

 170     195  LOAD_FAST             3  'ui_guide_dict'
         198  LOAD_ATTR             5  'get'
         201  LOAD_CONST            9  'click_action'
         204  BUILD_MAP_0           0 
         207  CALL_FUNCTION_2       2 
         210  STORE_FAST           14  'click_action'

 171     213  LOAD_FAST             3  'ui_guide_dict'
         216  LOAD_ATTR             5  'get'
         219  LOAD_CONST           10  'ignore_wpos'
         222  CALL_FUNCTION_1       1 
         225  STORE_FAST           15  'ignore_wpos'

 172     228  LOAD_FAST             3  'ui_guide_dict'
         231  LOAD_ATTR             5  'get'
         234  LOAD_CONST           11  'enable_vis_tick'
         237  CALL_FUNCTION_1       1 
         240  STORE_FAST           16  'enable_vis_tick'

 173     243  LOAD_CONST            0  ''
         246  STORE_DEREF           0  'ui_item'

 174     249  LOAD_FAST            14  'click_action'
         252  POP_JUMP_IF_FALSE   356  'to 356'

 175     255  LOAD_FAST             6  'page_name'
         258  POP_JUMP_IF_FALSE   288  'to 288'

 176     261  LOAD_FAST             5  'ui_inst'
         264  LOAD_ATTR             6  'get_sub_page'
         267  LOAD_FAST             6  'page_name'
         270  CALL_FUNCTION_1       1 
         273  STORE_FAST           17  'page_inst'

 177     276  LOAD_FAST            17  'page_inst'
         279  LOAD_ATTR             9  'panel'
         282  STORE_FAST           18  'start_nd'
         285  JUMP_FORWARD          9  'to 297'

 179     288  LOAD_FAST             5  'ui_inst'
         291  LOAD_ATTR             9  'panel'
         294  STORE_FAST           18  'start_nd'
       297_0  COME_FROM                '285'

 180     297  LOAD_GLOBAL          10  'parse_guide_click_action'
         300  LOAD_FAST            18  'start_nd'
         303  LOAD_FAST            14  'click_action'
         306  CALL_FUNCTION_2       2 
         309  STORE_FAST           19  'parsed_click_action'

 181     312  LOAD_CONST            1  ''
         315  LOAD_CONST           12  ('GuideHelperUI',)
         318  IMPORT_NAME          11  'logic.comsys.guide_ui.GuideHelperUI'
         321  IMPORT_FROM          12  'GuideHelperUI'
         324  STORE_FAST           20  'GuideHelperUI'
         327  POP_TOP          

 182     328  LOAD_FAST            20  'GuideHelperUI'
         331  CALL_FUNCTION_0       0 
         334  STORE_FAST           21  'mask_ui'

 183     337  LOAD_FAST            21  'mask_ui'
         340  LOAD_ATTR            13  'set_click_action_list'
         343  LOAD_FAST             0  'guide_name'
         346  LOAD_FAST            19  'parsed_click_action'
         349  CALL_FUNCTION_2       2 
         352  POP_TOP          
         353  JUMP_FORWARD          0  'to 356'
       356_0  COME_FROM                '353'

 185     356  LOAD_FAST             8  'parent_nd'
         359  STORE_DEREF           1  'nd'

 186     362  LOAD_FAST            12  'is_force'
         365  POP_JUMP_IF_FALSE   392  'to 392'

 187     368  LOAD_GLOBAL           7  'get_guide_conf_nd'
         371  LOAD_FAST             5  'ui_inst'
         374  LOAD_FAST             2  'ui_name'
         377  LOAD_FAST             3  'ui_guide_dict'
         380  LOAD_CONST           13  'force_nd'
         383  CALL_FUNCTION_4       4 
         386  STORE_FAST           22  'force_nd'
         389  JUMP_FORWARD          6  'to 398'

 189     392  LOAD_CONST            0  ''
         395  STORE_FAST           22  'force_nd'
       398_0  COME_FROM                '389'

 190     398  LOAD_DEREF            1  'nd'
         401  POP_JUMP_IF_FALSE   670  'to 670'

 191     404  LOAD_FAST            15  'ignore_wpos'
         407  POP_JUMP_IF_TRUE    471  'to 471'

 192     410  LOAD_DEREF            1  'nd'
         413  LOAD_ATTR            14  'ConvertToWorldSpacePercentage'
         416  LOAD_CONST           14  50
         419  LOAD_CONST           14  50
         422  CALL_FUNCTION_2       2 
         425  STORE_FAST           23  'wpos'

 193     428  LOAD_GLOBAL          15  'cc'
         431  LOAD_ATTR            16  'Vec2'
         434  LOAD_FAST            23  'wpos'
         437  LOAD_ATTR            17  'x'
         440  LOAD_FAST            11  'pos_offset'
         443  LOAD_CONST            1  ''
         446  BINARY_SUBSCR    
         447  BINARY_ADD       
         448  LOAD_FAST            23  'wpos'
         451  LOAD_ATTR            18  'y'
         454  LOAD_FAST            11  'pos_offset'
         457  LOAD_CONST           15  1
         460  BINARY_SUBSCR    
         461  BINARY_ADD       
         462  CALL_FUNCTION_2       2 
         465  STORE_FAST           23  'wpos'
         468  JUMP_FORWARD          6  'to 477'

 195     471  LOAD_CONST            0  ''
         474  STORE_FAST           23  'wpos'
       477_0  COME_FROM                '468'

 196     477  LOAD_FAST             3  'ui_guide_dict'
         480  LOAD_ATTR             5  'get'
         483  LOAD_CONST           16  'layer'
         486  LOAD_CONST            0  ''
         489  CALL_FUNCTION_2       2 
         492  STORE_FAST           24  'z_layer'

 197     495  LOAD_GLOBAL          19  'False'
         498  STORE_FAST           25  'simple_tag'

 198     501  LOAD_FAST            24  'z_layer'
         504  POP_JUMP_IF_FALSE   516  'to 516'

 199     507  LOAD_GLOBAL          20  'True'
         510  STORE_FAST           25  'simple_tag'
         513  JUMP_FORWARD          0  'to 516'
       516_0  COME_FROM                '513'

 200     516  LOAD_FAST            10  'temp_path'
         519  POP_JUMP_IF_FALSE   576  'to 576'

 201     522  LOAD_FAST             4  'template_utils'
         525  LOAD_ATTR            21  'init_guide_temp'
         528  LOAD_DEREF            1  'nd'
         531  LOAD_FAST            23  'wpos'
         534  LOAD_CONST           17  'text_id'
         537  LOAD_FAST             9  'text'
         540  LOAD_CONST           18  'name'
         543  LOAD_CONST           19  'temp_path'
         546  LOAD_FAST            10  'temp_path'
         549  LOAD_CONST           20  'simple_tag'
         552  LOAD_FAST            25  'simple_tag'
         555  LOAD_CONST           16  'layer'
         558  LOAD_FAST            24  'z_layer'
         561  LOAD_CONST           21  'ass_parent_ui'
         564  LOAD_FAST             5  'ui_inst'
         567  CALL_FUNCTION_1538  1538 
         570  STORE_DEREF           0  'ui_item'
         573  JUMP_FORWARD         45  'to 621'

 203     576  LOAD_FAST             4  'template_utils'
         579  LOAD_ATTR            21  'init_guide_temp'
         582  LOAD_DEREF            1  'nd'
         585  LOAD_FAST            23  'wpos'
         588  LOAD_CONST           17  'text_id'
         591  LOAD_FAST             9  'text'
         594  LOAD_CONST           18  'name'
         597  LOAD_CONST           20  'simple_tag'
         600  LOAD_FAST            25  'simple_tag'
         603  LOAD_CONST           16  'layer'
         606  LOAD_FAST            24  'z_layer'
         609  LOAD_CONST           21  'ass_parent_ui'
         612  LOAD_FAST             5  'ui_inst'
         615  CALL_FUNCTION_1282  1282 
         618  STORE_DEREF           0  'ui_item'
       621_0  COME_FROM                '573'

 205     621  LOAD_FAST            24  'z_layer'
         624  POP_JUMP_IF_FALSE   652  'to 652'

 206     627  LOAD_GLOBAL           2  'global_data'
         630  LOAD_ATTR            22  'lobby_guide_mgr'
         633  LOAD_ATTR            23  'save_guide_node'
         636  LOAD_FAST             0  'guide_name'
         639  LOAD_FAST             2  'ui_name'
         642  LOAD_DEREF            0  'ui_item'
         645  CALL_FUNCTION_3       3 
         648  POP_TOP          
         649  JUMP_FORWARD          0  'to 652'
       652_0  COME_FROM                '649'

 208     652  LOAD_FAST            22  'force_nd'
         655  POP_JUMP_IF_TRUE    670  'to 670'

 209     658  LOAD_DEREF            1  'nd'
         661  STORE_FAST           22  'force_nd'
         664  JUMP_ABSOLUTE       670  'to 670'
         667  JUMP_FORWARD          0  'to 670'
       670_0  COME_FROM                '667'

 210     670  LOAD_CONST           22  201030
         673  STORE_FAST           26  'VIS_TAG'

 211     676  LOAD_FAST            16  'enable_vis_tick'
         679  POP_JUMP_IF_FALSE   791  'to 791'
         682  LOAD_DEREF            0  'ui_item'
       685_0  COME_FROM                '679'
         685  POP_JUMP_IF_FALSE   791  'to 791'

 212     688  LOAD_CLOSURE          1  'nd'
         691  LOAD_CLOSURE          0  'ui_item'
         697  LOAD_CONST               '<code_object check_vis>'
         700  MAKE_CLOSURE_0        0 
         703  STORE_FAST           27  'check_vis'

 216     706  LOAD_DEREF            0  'ui_item'
         709  LOAD_ATTR            24  'runAction'
         712  LOAD_GLOBAL          15  'cc'
         715  LOAD_ATTR            25  'RepeatForever'
         718  LOAD_ATTR            26  'create'

 217     721  LOAD_GLOBAL          15  'cc'
         724  LOAD_ATTR            27  'Sequence'
         727  LOAD_ATTR            26  'create'

 219     730  LOAD_GLOBAL          15  'cc'
         733  LOAD_ATTR            28  'DelayTime'
         736  LOAD_ATTR            26  'create'
         739  LOAD_CONST           24  0.03
         742  CALL_FUNCTION_1       1 

 220     745  LOAD_GLOBAL          15  'cc'
         748  LOAD_ATTR            29  'CallFunc'
         751  LOAD_ATTR            26  'create'
         754  LOAD_FAST            27  'check_vis'
         757  CALL_FUNCTION_1       1 
         760  BUILD_LIST_2          2 
         763  CALL_FUNCTION_1       1 
         766  CALL_FUNCTION_1       1 
         769  CALL_FUNCTION_1       1 
         772  STORE_FAST           28  'act'

 224     775  LOAD_FAST            28  'act'
         778  LOAD_ATTR            30  'setTag'
         781  LOAD_FAST            26  'VIS_TAG'
         784  CALL_FUNCTION_1       1 
         787  POP_TOP          
         788  JUMP_FORWARD          0  'to 791'
       791_0  COME_FROM                '788'

 226     791  LOAD_FAST            13  'parent_name'
         794  POP_JUMP_IF_TRUE    800  'to 800'

 227     797  JUMP_FORWARD          0  'to 800'
       800_0  COME_FROM                '797'

 228     800  LOAD_FAST            12  'is_force'
         803  POP_JUMP_IF_FALSE   865  'to 865'
         806  LOAD_FAST            22  'force_nd'
       809_0  COME_FROM                '803'
         809  POP_JUMP_IF_FALSE   865  'to 865'

 229     812  LOAD_CONST            1  ''
         815  LOAD_CONST           12  ('GuideHelperUI',)
         818  IMPORT_NAME          11  'logic.comsys.guide_ui.GuideHelperUI'
         821  IMPORT_FROM          12  'GuideHelperUI'
         824  STORE_FAST           20  'GuideHelperUI'
         827  POP_TOP          

 230     828  LOAD_FAST            20  'GuideHelperUI'
         831  CALL_FUNCTION_0       0 
         834  STORE_FAST           21  'mask_ui'

 231     837  LOAD_FAST            21  'mask_ui'
         840  POP_JUMP_IF_FALSE   865  'to 865'

 232     843  LOAD_FAST            21  'mask_ui'
         846  LOAD_ATTR            31  'set_touch_area_list'
         849  LOAD_FAST            22  'force_nd'
         852  BUILD_LIST_1          1 
         855  CALL_FUNCTION_1       1 
         858  POP_TOP          
         859  JUMP_ABSOLUTE       865  'to 865'
         862  JUMP_FORWARD          0  'to 865'
       865_0  COME_FROM                '862'
         865  LOAD_CONST            0  ''
         868  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1538' instruction at offset 567


def show_top_guide_temp_finish(guide_name, guide_key, ui_name, ui_guide_dict):
    ui_inst = global_data.ui_mgr.get_ui(ui_name)
    z_layer = ui_guide_dict.get('layer', None)
    enable_vis_tick = ui_guide_dict.get('enable_vis_tick')
    if z_layer:
        nd_guide = global_data.lobby_guide_mgr.saved_guide_nd_dict.get(guide_name, {}).get(ui_name, None)
        if nd_guide:
            name = nd_guide.__class__.__name__
            if ui_inst:
                ui_inst.remove_associate_vis_ui(str(name))
            global_data.lobby_guide_mgr.saved_guide_nd_dict.get(guide_name, {}).pop(ui_name)
            global_data.ui_mgr.close_ui(str(name))
    is_force = ui_guide_dict.get('is_force', 0)
    click_action = ui_guide_dict.get('click_action', {})
    if is_force or click_action:
        global_data.ui_mgr.close_ui('GuideHelperUI')
    if not ui_inst:
        return
    else:
        page_name = ui_guide_dict.get('page')
        if page_name:
            page = ui_inst.get_sub_page(page_name)
            if not page:
                return
        nd = get_guide_conf_nd(ui_inst, ui_name, ui_guide_dict)
        text = ui_guide_dict.get('text')
        if nd:
            nd_guide = getattr(nd, guide_name)
            if nd_guide:
                if enable_vis_tick:
                    nd_guide.stopAllActions()
                nd_guide.setVisible(False)
                return
        return


def show_top_guide_temp_refresh(guide_name, guide_key, ui_name, ui_guide_dict):
    from logic.gutils import template_utils
    ui_inst = global_data.ui_mgr.get_ui(ui_name)
    if not ui_inst:
        return
    else:
        page_name = ui_guide_dict.get('page')
        if page_name:
            page = ui_inst.get_sub_page(page_name)
            if not page:
                return
        z_layer = ui_guide_dict.get('layer', None)
        if z_layer:
            nd_guide = global_data.lobby_guide_mgr.saved_guide_nd_dict.get(guide_name, {}).get(ui_name, None)
            if nd_guide:
                nd = get_guide_conf_nd(ui_inst, ui_name, ui_guide_dict)
                pos_offset = ui_guide_dict.get('pos_offset', (0, 0))
                if nd:
                    wpos = nd.ConvertToWorldSpacePercentage(50, 50)
                    wpos = cc.Vec2(wpos.x + pos_offset[0], wpos.y + pos_offset[1])
                    template_utils.set_node_position_in_screen(nd_guide, nd, wpos)
        return


def show_top_guide_temp_active_by_node(node, guide_name, guide_key, guide_dict, **kwargs):
    from logic.gutils import template_utils
    text = guide_dict.get('text')
    template_path = guide_dict.get('template_path')
    if node:
        wpos = node.ConvertToWorldSpacePercentage(50, 50)
        if template_path:
            kw = {'temp_path': template_path}
        else:
            kw = {}
        ui_item = template_utils.init_guide_temp(node, wpos, text_id=text, name=guide_name, **kw)


def show_top_guide_temp_active_by_node_finish(node, guide_name, guide_key, guide_dict, **kwargs):
    text = guide_dict.get('text')
    if node:
        nd_guide = getattr(node, guide_name)
        if nd_guide:
            nd_guide.setVisible(False)


def show_right_top_guide_temp_in_role_choose(guide_name, guide_key, ui_name, ui_guide_dict):
    from logic.gutils import template_utils
    from common.cfg import confmgr
    ui_inst = global_data.ui_mgr.get_ui(ui_name)
    if not ui_inst:
        return
    else:
        selected_role_id = None
        role_config = confmgr.get('role_info', 'RoleProfile', 'Content')
        for role_id, info in six.iteritems(role_config):
            role_id = int(role_id)
            if global_data.player.get_item_by_no(role_id):
                selected_role_id = role_id
                break

        if selected_role_id:
            nd = ui_inst.guide_get_role_to_ui_item(selected_role_id)
            if not nd:
                log_error('show_right_top_guide_temp_in_role_choose failed to find role nd!')
                return
            text = ui_guide_dict.get('text')
            if nd:
                nd.setLocalZOrder(1)
                wpos = nd.ConvertToWorldSpacePercentage(50, 50)
                ui_item = template_utils.init_guide_temp(nd, wpos, text_id=text, name=guide_name)
                if ui_item:
                    ui_item.setLocalZOrder(1)
        return


def show_right_top_guide_temp_in_role_choose_finish(guide_name, guide_key, ui_name, ui_guide_dict):
    from common.cfg import confmgr
    ui_inst = global_data.ui_mgr.get_ui(ui_name)
    if not ui_inst:
        return
    role_config = confmgr.get('role_info', 'RoleProfile', 'Content')
    for role_id, info in six.iteritems(role_config):
        role_id = int(role_id)
        if global_data.player.get_item_by_no(role_id):
            selected_role_id = role_id
            nd = ui_inst.guide_get_role_to_ui_item(selected_role_id)
            if not nd:
                continue
            nd_guide = getattr(nd, guide_name)
            if nd_guide:
                nd_guide.setVisible(False)


def show_right_top_guide_temp_in_mecha_choose(guide_name, guide_key, ui_name, ui_guide_dict):
    from logic.gutils import template_utils
    from common.cfg import confmgr
    ui_inst = global_data.ui_mgr.get_ui(ui_name)
    if not ui_inst:
        return
    selected_mecha_id = 8001
    nd = ui_inst.guide_get_mecha_to_ui_item(selected_mecha_id)
    if not nd:
        log_error('show_right_top_guide_temp_in_mecha_choose failed to find mecha nd!')
        return
    text = ui_guide_dict.get('text')
    if nd:
        nd.setLocalZOrder(100)
        wpos = nd.ConvertToWorldSpacePercentage(50, 50)
        ui_item = template_utils.init_guide_temp(nd, wpos, text_id=text, name=guide_name)
        if ui_item:
            ui_item.setLocalZOrder(100)


def show_right_top_guide_temp_in_mecha_choose_finish(guide_name, guide_key, ui_name, ui_guide_dict):
    from common.cfg import confmgr
    ui_inst = global_data.ui_mgr.get_ui(ui_name)
    if not ui_inst:
        return
    selected_mecha_id = 8001
    nd = ui_inst.guide_get_mecha_to_ui_item(selected_mecha_id)
    if not nd:
        return
    nd_guide = getattr(nd, guide_name)
    if nd_guide:
        nd_guide.setVisible(False)


def save_guide_key(guide_name, guide_key, ui_name, ui_guide_dict):
    global_data.player and global_data.player.add_read_lobby_guide(guide_key)


def save_guide_key_finish(guide_name, guide_key, ui_name, ui_guide_dict):
    pass


def save_guide_key_with_end(guide_name, guide_key, ui_name, ui_guide_dict):
    save_guide_key(guide_name, guide_key, ui_name, ui_guide_dict)


def save_guide_key_with_end_finish(guide_name, guide_key, ui_name, ui_guide_dict):
    pass


def none(*args):
    pass


def none_finish(*args):
    pass


def get_newbie_assessment_guide_key(step):
    key = 'showed_newbie_assessment_guide_' + str(step)
    return key


def newbie_assessment_guide_checked(step):
    key = get_newbie_assessment_guide_key(step)
    return global_data.achi_mgr.get_cur_user_archive_data(key, default=0) == 1


def check_show_newbie_assessment_guide--- This code section failed: ---

 418       0  LOAD_FAST             1  'check_prev_step'
           3  POP_JUMP_IF_FALSE    26  'to 26'

 419       6  LOAD_GLOBAL           0  'newbie_assessment_guide_checked'
           9  LOAD_GLOBAL           1  'False'
          12  BINARY_SUBTRACT  
          13  CALL_FUNCTION_1       1 
          16  POP_JUMP_IF_TRUE     26  'to 26'

 420      19  LOAD_GLOBAL           1  'False'
          22  RETURN_END_IF    
        23_0  COME_FROM                '16'
          23  JUMP_FORWARD          0  'to 26'
        26_0  COME_FROM                '23'

 422      26  LOAD_FAST             4  'create_only'
          29  POP_JUMP_IF_FALSE    67  'to 67'

 423      32  LOAD_CONST            2  ''
          35  LOAD_CONST            3  ('GuideSetting',)
          38  IMPORT_NAME           2  'logic.comsys.guide_ui.GuideSetting'
          41  IMPORT_FROM           3  'GuideSetting'
          44  STORE_FAST            5  'GuideSetting'
          47  POP_TOP          

 424      48  LOAD_FAST             5  'GuideSetting'
          51  CALL_FUNCTION_0       0 
          54  LOAD_ATTR             4  '_create_login'
          57  POP_JUMP_IF_TRUE     67  'to 67'

 425      60  LOAD_GLOBAL           1  'False'
          63  RETURN_END_IF    
        64_0  COME_FROM                '57'
          64  JUMP_FORWARD          0  'to 67'
        67_0  COME_FROM                '64'

 427      67  LOAD_FAST             3  'check_task'
          70  POP_JUMP_IF_FALSE   125  'to 125'

 428      73  LOAD_GLOBAL           5  'global_data'
          76  LOAD_ATTR             6  'player'
          79  LOAD_ATTR             7  'get_newbie_parent_task_id'
          82  CALL_FUNCTION_0       0 
          85  STORE_FAST            6  'parent_task_id'

 429      88  LOAD_GLOBAL           5  'global_data'
          91  LOAD_ATTR             6  'player'
          94  LOAD_ATTR             8  'get_task_prog'
          97  LOAD_FAST             6  'parent_task_id'
         100  CALL_FUNCTION_1       1 
         103  LOAD_CONST            2  ''
         106  COMPARE_OP            4  '>'
         109  STORE_FAST            7  'has_finish_one'

 430     112  LOAD_FAST             7  'has_finish_one'
         115  POP_JUMP_IF_FALSE   125  'to 125'

 431     118  LOAD_GLOBAL           1  'False'
         121  RETURN_END_IF    
       122_0  COME_FROM                '115'
         122  JUMP_FORWARD          0  'to 125'
       125_0  COME_FROM                '122'

 433     125  LOAD_GLOBAL           0  'newbie_assessment_guide_checked'
         128  LOAD_FAST             0  'step'
         131  CALL_FUNCTION_1       1 
         134  STORE_FAST            8  'has_record'

 434     137  LOAD_FAST             8  'has_record'
         140  POP_JUMP_IF_FALSE   147  'to 147'

 435     143  LOAD_GLOBAL           1  'False'
         146  RETURN_END_IF    
       147_0  COME_FROM                '140'

 436     147  LOAD_FAST             2  'record'
         150  POP_JUMP_IF_FALSE   187  'to 187'

 437     153  LOAD_GLOBAL           9  'get_newbie_assessment_guide_key'
         156  LOAD_FAST             0  'step'
         159  CALL_FUNCTION_1       1 
         162  STORE_FAST            9  'key'

 438     165  LOAD_GLOBAL           5  'global_data'
         168  LOAD_ATTR            10  'achi_mgr'
         171  LOAD_ATTR            11  'set_cur_user_archive_data'
         174  LOAD_FAST             9  'key'
         177  LOAD_CONST            1  1
         180  CALL_FUNCTION_2       2 
         183  POP_TOP          
         184  JUMP_FORWARD          0  'to 187'
       187_0  COME_FROM                '184'

 439     187  LOAD_GLOBAL          12  'True'
         190  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_1' instruction at offset 13


def get_change_ui_data_for_guide_ui(need_to_adjust_scale_type_nodes, panel):
    scale_type_adjust_list = []
    pos_type_adjust_list = []
    for source_nd_name, target_nd_name, target_scale_nd_name in need_to_adjust_scale_type_nodes:
        nd = get_name_string_path(panel, source_nd_name)
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        scale = nd.getScale()
        scale_type_adjust_list.append((w_pos, scale, target_nd_name, target_scale_nd_name))

    ret_dict = {'scale_type': scale_type_adjust_list,
       'pos_type': pos_type_adjust_list
       }
    return ret_dict


def is_quality_level_initial():
    from logic.gcommon.common_const.ui_operation_const import QUALITY_LEVEL_KEY
    return global_data.player and global_data.player.has_setting_2(QUALITY_LEVEL_KEY)


def show_guide_duel_panel(*args):
    from common.uisys.basepanel import BasePanel
    from common.const.uiconst import BG_ZORDER, NORMAL_LAYER_ZORDER_1, UI_VKB_NO_EFFECT

    class BattleDuelGuideUI(BasePanel):
        PANEL_CONFIG_NAME = 'battle_duel/guide_battle_duel'
        DLG_ZORDER = NORMAL_LAYER_ZORDER_1
        UI_VKB_TYPE = UI_VKB_NO_EFFECT
        UI_ACTION_EVENT = {'nd_touch.OnClick': 'on_click_nd_touch'
           }

        def on_init_panel(self, *args):
            self.panel.PlayAnimation('show_step_1')

        def on_click_nd_touch(self, *args):
            self.close()

    BattleDuelGuideUI()


def show_guide_duel_panel_finish(*args):
    global_data.ui_mgr.close_ui('BattleDuelGuideUI')