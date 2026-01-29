# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/inscription_utils.py
from __future__ import absolute_import
import six_ex
import six
from common.cfg import confmgr
from logic.gutils import item_utils

def get_component_bag_bg_pic(com_type):
    from logic.gcommon.cdata.mecha_component_data import COMPONENT_ATK, COMPONENT_DEFENSE
    data = {COMPONENT_ATK: 'gui/ui_res_2/mech_display/inscription/frame_warehouse_red.png',COMPONENT_DEFENSE: 'gui/ui_res_2/mech_display/inscription/frame_warehouse_blue.png'
       }
    return data.get(com_type, data[COMPONENT_ATK])


def get_com_type_pic(com_type, suffix=''):
    from logic.gcommon.cdata.mecha_component_data import COMPONENT_ATK, COMPONENT_DEFENSE
    data = {COMPONENT_ATK: COMPONENT_ATK + 1,COMPONENT_DEFENSE: COMPONENT_DEFENSE + 2
       }
    return 'gui/ui_res_2/mech_display/inscription/pnl_icon_bar_%s%s.png' % (data.get(int(com_type), COMPONENT_ATK + 1), suffix)


def get_com_type_item_pic(part, suffix='unlock'):
    from logic.gcommon.cdata.mecha_component_data import part2type
    com_type = part2type(part)
    from logic.gcommon.cdata.mecha_component_data import COMPONENT_ATK, COMPONENT_DEFENSE
    data = {COMPONENT_DEFENSE: 'gui/ui_res_2/item/inscription/pnl_icon_blue_%s.png',
       COMPONENT_ATK: 'gui/ui_res_2/item/inscription/pnl_icon_red_%s.png'
       }
    return data.get(com_type, data[COMPONENT_ATK]) % suffix


def init_component_slot_temp(slot_nd, com_item_no, is_lock=False, unlock_lv=None, com_type=None, show_tips=False, show_full=False, need_name=False):
    if com_type is None:
        if com_item_no is not None:
            from logic.gcommon.cdata.mecha_component_data import get_component_type
            com_type = get_component_type(com_item_no)
    if com_type is None:
        log_error('Empty component slot need com type!!!')
        return
    else:
        if not com_item_no:
            slot_nd.lab_tech_name.setVisible(False)
            slot_nd.loop_full.setVisible(False)
            slot_nd.StopAnimation('loop_full')
            if not is_lock:
                bar_pic = get_com_type_pic(com_type, '_empty')
                slot_nd.nd_empty.setVisible(True)
                slot_nd.nd_empty.img_bar.SetDisplayFrameByPath('', bar_pic)
                slot_nd.nd_normal.setVisible(False)
                slot_nd.nd_lock_1.setVisible(False)
                slot_nd.nd_lock_2.setVisible(False)
            elif unlock_lv is not None:
                bar_pic = get_com_type_pic(com_type, '_lock_2')
                slot_nd.nd_empty.setVisible(False)
                slot_nd.nd_normal.setVisible(False)
                slot_nd.nd_lock_1.setVisible(False)
                slot_nd.nd_lock_2.setVisible(True)
                slot_nd.nd_lock_2.img_bar.SetDisplayFrameByPath('', bar_pic)
                slot_nd.lab_level.SetString(get_text_by_id(81809, {'lv': str(unlock_lv)}))
            else:
                bar_pic = get_com_type_pic(com_type, '_lock')
                slot_nd.nd_empty.setVisible(False)
                slot_nd.nd_normal.setVisible(False)
                slot_nd.nd_lock_1.setVisible(True)
                slot_nd.nd_lock_2.setVisible(False)
                slot_nd.nd_lock_1.img_bar.SetDisplayFrameByPath('', bar_pic)
            return
        from logic.gcommon.item import item_const
        if show_full:
            slot_nd.loop_full.setVisible(True)
            slot_nd.PlayAnimation('loop_full')
        else:
            slot_nd.loop_full.setVisible(False)
            slot_nd.StopAnimation('loop_full')
        if need_name:
            slot_nd.lab_tech_name.setVisible(True)
            slot_nd.lab_tech_name.SetString(item_utils.get_lobby_item_name(com_item_no))
        else:
            slot_nd.lab_tech_name.setVisible(False)
        bar_pic = get_com_type_pic(com_type)
        slot_nd.nd_empty.setVisible(False)
        slot_nd.nd_normal.setVisible(True)
        slot_nd.nd_lock_2.setVisible(False)
        slot_nd.nd_lock_1.setVisible(False)
        slot_nd.nd_normal.img_bar.SetDisplayFrameByPath('', bar_pic)
        pic = item_utils.get_lobby_item_pic_by_item_no(com_item_no)
        slot_nd.img_icon.SetDisplayFrameByPath('', pic)
        if show_tips and com_item_no:

            @slot_nd.nd_btn.callback()
            def OnClick(layer, touch):
                wpos = touch.getLocation()
                from logic.comsys.mecha_display.LobbyItemInscrDescUI import LobbyItemInscrDescUI
                ui = LobbyItemInscrDescUI()
                if ui:
                    ui.show_item_desc_info(com_item_no, None, directly_world_pos=wpos, item_num=None, extra_info={'hide_button': True})
                return

        return


def init_component_detail_temp(slot_detail_nd, component_no, num=1, is_select=False):
    init_component_slot_temp(slot_detail_nd.temp_inscription, component_no)
    slot_detail_nd.lab_name.SetString(item_utils.get_lobby_item_name(component_no))
    if num > 1:
        slot_detail_nd.nd_num.setVisible(True)
        slot_detail_nd.nd_empty.setVisible(False)
        slot_detail_nd.lab_num.SetString(get_text_by_id(81860, {'num': num}))
    elif num <= 0:
        slot_detail_nd.nd_empty.setVisible(True)
        slot_detail_nd.nd_num.setVisible(False)
    else:
        slot_detail_nd.nd_num.setVisible(False)
        slot_detail_nd.nd_empty.setVisible(False)
    inscr_buff_list = get_component_id_buff_list(component_no)
    set_ability_list(slot_detail_nd.list_ability, None, get_inscr_buff_dict_by_buff_list(inscr_buff_list))
    return


def init_component_bag_temp(slot_detail_nd, component_no, num=1, is_select=False):
    from logic.gcommon.cdata.mecha_component_data import get_mecha_component_price, get_com_unlock_lv
    from logic.gcommon.cdata.mecha_component_conf import get_give_com_level
    from logic.gutils.template_utils import splice_price, init_price_template, get_money_rich_text_ex
    from logic.gutils import mall_utils
    init_component_slot_temp(slot_detail_nd.temp_inscription, component_no)
    slot_detail_nd.lab_name.SetString(item_utils.get_lobby_item_name(component_no))
    inscr_buff_list = get_component_id_buff_list(component_no)
    set_ability_list(slot_detail_nd.list_ability, None, get_inscr_buff_dict_by_buff_list(inscr_buff_list))
    has_own = global_data.player.has_owned_component(component_no)
    if has_own:
        slot_detail_nd.nd_lock.setVisible(False)
        slot_detail_nd.nd_buy.setVisible(False)
        slot_detail_nd.nd_have.setVisible(True)
    else:
        slot_detail_nd.nd_have.setVisible(False)
        unlock_lv = get_give_com_level(component_no)
        if unlock_lv is not None and unlock_lv > global_data.player.get_lv():
            slot_detail_nd.nd_lock.setVisible(True)
            slot_detail_nd.nd_buy.setVisible(False)
            slot_detail_nd.nd_lock.lab_level.SetString(get_text_by_id(81872, {'lv': unlock_lv}))
        else:
            slot_detail_nd.nd_buy.setVisible(True)
            slot_detail_nd.nd_lock.setVisible(False)
            price_info = get_component_buy_price(component_no)
            init_price_template(price_info, slot_detail_nd.temp_cost)

            @slot_detail_nd.btn_buy.callback()
            def OnClick(btn, touch):
                if unlock_lv is not None and unlock_lv > global_data.player.get_lv():
                    global_data.game_mgr.show_tip(get_text_by_id(81872, {'lv': unlock_lv}))
                    return
                else:
                    if global_data.player.has_owned_component(component_no):
                        return
                    if not mall_utils.check_payment(price_info['goods_payment'], price_info['real_price'], pay_tip=False):
                        global_data.game_mgr.show_tip(get_text_by_id(81873))
                        return
                    from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                    price_info_list = [price_info]
                    dlg = SecondConfirmDlg2()

                    def on_cancel():
                        dlg.close()

                    def on_confirm():
                        dlg.close()
                        if mall_utils.check_payment(price_info['goods_payment'], price_info['real_price'], pay_tip=False):
                            global_data.player.buy_mecha_component(component_no)

                    price_text = get_money_rich_text_ex(price_info_list)
                    dlg.confirm(content=get_text_by_id(81983, {'cost': price_text,'item_name': item_utils.get_lobby_item_name(component_no)}), cancel_callback=on_cancel, confirm_callback=on_confirm, unique_callback=on_cancel)
                    return

    return


def format_buff_value--- This code section failed: ---

 177       0  LOAD_GLOBAL           0  'type'
           3  LOAD_FAST             0  'buff_value'
           6  CALL_FUNCTION_1       1 
           9  LOAD_GLOBAL           1  'six'
          12  LOAD_ATTR             2  'integer_types'
          15  COMPARE_OP            7  'not-in'
          18  POP_JUMP_IF_FALSE    30  'to 30'

 178      21  LOAD_CONST            1  '%+.1f%%'
          24  LOAD_CONST            2  100
          27  BINARY_MULTIPLY  
          28  BINARY_MODULO    
          29  RETURN_END_IF    
        30_0  COME_FROM                '18'

 180      30  LOAD_GLOBAL           3  'str'
          33  LOAD_FAST             0  'buff_value'
          36  CALL_FUNCTION_1       1 
          39  RETURN_VALUE     

Parse error at or near `BINARY_MODULO' instruction at offset 28


def get_component_id_buff_list(component_no):
    from logic.gcommon.cdata.mecha_component_data import get_inscs_of_component_client
    insc_list = get_inscs_of_component_client(component_no)
    return insc_list


def get_player_component_list_by_type(component_type, inscr_type_list):
    from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_NEW_MECHA_COMPONENT
    if not global_data.player:
        return []
    else:
        from logic.gcommon.cdata.mecha_component_data import get_component_type
        from logic.gcommon.cdata.mecha_component_data import get_inscs_of_component_client
        coms = global_data.player.get_mecha_component_list()
        if component_type is not None:
            valid_items = [ com_id for com_id in coms if get_component_type(com_id) == component_type ]
        else:
            valid_items = coms
        if inscr_type_list:
            inscr_compatible_list = []
            for com_id in valid_items:
                inscr_list = get_inscs_of_component_client(com_id)
                for _, inscr_id, _ in inscr_list:
                    inscr_conf = confmgr.get('inscription_data', str(inscr_id), default={})
                    weightKind = inscr_conf.get('weightKind', 1)
                    if weightKind in inscr_type_list:
                        inscr_compatible_list.append(com_id)
                        break

            valid_items = inscr_compatible_list
        return filter_list_by_plan_for_items(valid_items)


def filter_item_nos_by_inscr_type(item_no_list, inscr_type_list):
    from logic.gcommon.cdata.mecha_component_data import get_inscs_of_component_client
    inscr_compatible_list = []
    for item_no in item_no_list:
        inscr_list = get_inscs_of_component_client(item_no)
        for _, inscr_id, _ in inscr_list:
            inscr_conf = confmgr.get('inscription_data', str(inscr_id), default={})
            weightKind = inscr_conf.get('weightKind', 1)
            if weightKind in inscr_type_list:
                inscr_compatible_list.append(item_no)
                break

    return inscr_compatible_list


def get_player_component_list_by_parts(parts, exclude_item_no_list):
    if not global_data.player:
        return []
    from logic.gcommon.cdata.mecha_component_data import get_component_parts
    item_nos = global_data.player.get_mecha_component_list()
    valid_items = [ item_no for item_no in item_nos if any([ p in parts for p in get_component_parts(item_no) if item_no not in exclude_item_no_list ]) ]
    return filter_list_by_plan_for_items(valid_items)


def get_component_list_inscr_add_dict(item_no_list):
    if not global_data.player:
        return {}
    inscr_buff_list = []
    for item_no in item_no_list:
        inscr_buff_list.extend(get_component_id_buff_list(item_no))

    return get_inscr_buff_dict_by_buff_list(inscr_buff_list)


def get_inscr_buff_dict_by_buff_list(inscr_buff_list):
    import six.moves.collections_abc
    import collections
    inscr_buff_dict = collections.OrderedDict()
    for idx, component_buff_info in enumerate(inscr_buff_list):
        _component_id, inscr_buff_id, buff_value = component_buff_info
        inscr_buff_dict.setdefault(inscr_buff_id, 0)
        inscr_buff_dict[inscr_buff_id] += buff_value

    return inscr_buff_dict


def show_attr_dict_change(old_dict, new_dict):
    attr_change_dict = {}
    attr_base_factor = {}
    import math
    for inscr_id, value in six.iteritems(new_dict):
        attr_base_factor[inscr_id] = math.copysign(1, value)
        if inscr_id not in old_dict:
            attr_change_dict[inscr_id] = value
        else:
            attr_change_dict[inscr_id] = value - old_dict[inscr_id]

    for inscr_id, value in six.iteritems(old_dict):
        if inscr_id not in new_dict:
            attr_base_factor[inscr_id] = math.copysign(1, value)
            attr_change_dict[inscr_id] = -value

    att_change_list = []
    for inscr_id in sorted(six_ex.keys(attr_change_dict)):
        text_id = confmgr.get('inscription_data', str(inscr_id), 'descTid', default='')
        change = attr_change_dict[inscr_id]
        if change != 0:
            att_change_list.append([text_id, change, attr_base_factor[inscr_id]])

    return (att_change_list, attr_base_factor)


def get_component_list_inscr_list(item_no_list):
    if not global_data.player:
        return {}
    inscr_id_list = []
    for component_no in item_no_list:
        inscr_buff_list = get_component_id_buff_list(component_no)
        unit = []
        for idx, component_buff_info in enumerate(inscr_buff_list):
            component_no, inscr_buff_id, buff_value = component_buff_info
            unit.append((component_no, inscr_buff_id))

        inscr_id_list.append(unit)

    return inscr_id_list


def _get_component_item_cost_price(item_cost, num):
    from logic.gutils.mall_utils import get_item_money_type, get_default_money_types
    if item_cost:
        item_no, item_num = item_cost
        price_info = {'original_price': item_num * num,
           'real_price': item_num * num,
           'discount_price': None,
           'goods_payment': get_item_money_type(item_no)
           }
        return price_info
    else:
        return {}
        return


def get_component_buy_price(item_no, item_num=1):
    from logic.gcommon.cdata.mecha_component_data import get_mecha_component_price
    item_cost = get_mecha_component_price(item_no)
    return _get_component_item_cost_price(item_cost, item_num)


def get_merged_item_no_all_list(own_com_list, all_item_no_list=()):
    all_list = all_item_no_list
    own_list = list(own_com_list)
    unown_list = [ item_no for item_no in all_list if item_no not in own_list ]
    return (
     unown_list, own_list)


def filter_list_by_plan(item_no_list):
    return item_no_list


def filter_list_by_plan_for_items(com_ids):
    return com_ids


def get_used_com_item_id_list(mecha_id, page_index):
    page_content = global_data.player.get_mecha_component_page_content_conf(mecha_id, page_index)
    used_item_id_list = []
    for p, item_id_list in six.iteritems(page_content):
        used_item_id_list.extend([ item_id for item_id in item_id_list if item_id is not None ])

    return used_item_id_list


def get_empty_slot_list(mecha_id, page_index):
    from logic.gcommon.const import MECHA_COMPONENT_PART_LIST
    from logic.gcommon.item import item_const
    page_content = global_data.player.get_mecha_component_page_content_conf(mecha_id, page_index)
    empty_slot_dict = {}
    for p in MECHA_COMPONENT_PART_LIST:
        item_id_list = page_content.get(str(p), [None] * item_const.COMPONENT_SLOT_CNT_PER_PART)
        unlock_index_list = global_data.player.get_unlock_slot_idx(p)
        empty_slot_dict[p] = [ slot_idx for slot_idx, item_id in enumerate(item_id_list) if item_id is None and slot_idx in unlock_index_list ]

    return empty_slot_dict


def cal_radar_score(used_item_id_list):
    score_dict = {}
    inscr_id_list = get_component_list_inscr_list(used_item_id_list)
    for inscr_id_list_item in inscr_id_list:
        if len(inscr_id_list_item) == 1:
            factor = 2
        else:
            factor = 1
        for _, inscr_id in inscr_id_list_item:
            inscr_conf = confmgr.get('inscription_data', str(inscr_id), default={})
            weightValue = inscr_conf.get('weightValue', 5)
            weightKind = inscr_conf.get('weightKind', 1)
            score_dict.setdefault(weightKind, 0)
            score_dict[weightKind] += weightValue * factor

    return score_dict


def set_ability_list(list_ability, nd_empty, inscr_buff_sorted_dict):
    if nd_empty:
        if len(inscr_buff_sorted_dict) <= 0:
            nd_empty.setVisible(True)
        else:
            nd_empty.setVisible(False)
    list_ability.SetInitCount(len(inscr_buff_sorted_dict))
    sorted_inscr_list = six_ex.keys(inscr_buff_sorted_dict)
    for idx, inscr_id in enumerate(sorted_inscr_list):
        buff_value = inscr_buff_sorted_dict[sorted_inscr_list[idx]]
        ui_item = list_ability.GetItem(idx)
        ui_item.lab_num.SetString(format_buff_value(buff_value))
        text_id = confmgr.get('inscription_data', str(inscr_id), 'descTid', default='')
        ui_item.lab_content.SetString(text_id)
        ui_item.SetPressEnable(True)

        @ui_item.callback()
        def OnPressed(btn, inscr_id=inscr_id):
            text_id = confmgr.get('inscription_data', str(inscr_id), 'descTid', default='')
            detailTid = confmgr.get('inscription_data', str(inscr_id), 'descDetailTid', default='')
            txt = '#SO%s#n:%s' % (get_text_by_id(text_id), get_text_by_id(detailTid))
            wpos = btn.ConvertToWorldSpace(0, 0)
            import cc
            anchor = cc.Vec2(1, 0.5)
            global_data.emgr.show_item_desc_text_ui_event.emit(txt, wpos, anchor)

        @ui_item.callback()
        def OnEnd(btn, touch):
            global_data.emgr.hide_item_desc_text_ui_event.emit()


def get_inscr_part_name--- This code section failed: ---

 389       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('MECHA_PART_HEAD', 'MECHA_PART_LEFT_ARM', 'MECHA_PART_RIGHT_ARM', 'MECHA_PART_BODY', 'MECHA_PART_PROPELLER', 'MECHA_PART_LOWER_BODY', 'MECHA_COMPONENT_PART_LIST')
           6  IMPORT_NAME           0  'logic.gcommon.const'
           9  IMPORT_FROM           1  'MECHA_PART_HEAD'
          12  STORE_FAST            1  'MECHA_PART_HEAD'
          15  IMPORT_FROM           2  'MECHA_PART_LEFT_ARM'
          18  STORE_FAST            2  'MECHA_PART_LEFT_ARM'
          21  IMPORT_FROM           3  'MECHA_PART_RIGHT_ARM'
          24  STORE_FAST            3  'MECHA_PART_RIGHT_ARM'
          27  IMPORT_FROM           4  'MECHA_PART_BODY'
          30  STORE_FAST            4  'MECHA_PART_BODY'
          33  IMPORT_FROM           5  'MECHA_PART_PROPELLER'
          36  STORE_FAST            5  'MECHA_PART_PROPELLER'
          39  IMPORT_FROM           6  'MECHA_PART_LOWER_BODY'
          42  STORE_FAST            6  'MECHA_PART_LOWER_BODY'
          45  IMPORT_FROM           7  'MECHA_COMPONENT_PART_LIST'
          48  STORE_FAST            7  'MECHA_COMPONENT_PART_LIST'
          51  POP_TOP          

 392      52  BUILD_MAP_6           6 

 393      55  LOAD_CONST            3  81229
          58  LOAD_FAST             1  'MECHA_PART_HEAD'
          61  STORE_MAP        

 394      62  LOAD_CONST            4  868024
          65  LOAD_FAST             2  'MECHA_PART_LEFT_ARM'
          68  STORE_MAP        

 395      69  LOAD_CONST            5  868023
          72  LOAD_FAST             3  'MECHA_PART_RIGHT_ARM'
          75  STORE_MAP        

 396      76  LOAD_CONST            5  868023
          79  LOAD_FAST             4  'MECHA_PART_BODY'
          82  STORE_MAP        

 397      83  LOAD_CONST            6  868025
          86  LOAD_FAST             5  'MECHA_PART_PROPELLER'
          89  STORE_MAP        

 398      90  LOAD_CONST            7  860101
          93  LOAD_FAST             6  'MECHA_PART_LOWER_BODY'
          96  STORE_MAP        
          97  STORE_FAST            8  'name_dic'

 400     100  LOAD_FAST             8  'name_dic'
         103  LOAD_ATTR             8  'get'
         106  LOAD_ATTR             3  'MECHA_PART_RIGHT_ARM'
         109  CALL_FUNCTION_2       2 
         112  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 109


def get_inscr_part_slot_icon(part, suffix):
    from logic.gcommon.cdata.mecha_component_data import part2type
    com_type = part2type(part)
    bar_pic = get_com_type_pic(com_type, suffix)
    return bar_pic


def init_desc_list--- This code section failed: ---

 409       0  LOAD_GLOBAL           0  'len'
           3  LOAD_FAST             1  'inscr_buff_list'
           6  CALL_FUNCTION_1       1 
           9  LOAD_CONST            1  1
          12  COMPARE_OP            1  '<='
          15  POP_JUMP_IF_FALSE    37  'to 37'

 410      18  LOAD_FAST             0  'nd'
          21  LOAD_ATTR             1  'nd_desc_2'
          24  LOAD_ATTR             2  'setVisible'
          27  LOAD_GLOBAL           3  'False'
          30  CALL_FUNCTION_1       1 
          33  POP_TOP          
          34  JUMP_FORWARD         16  'to 53'

 412      37  LOAD_FAST             0  'nd'
          40  LOAD_ATTR             1  'nd_desc_2'
          43  LOAD_ATTR             2  'setVisible'
          46  LOAD_GLOBAL           4  'True'
          49  CALL_FUNCTION_1       1 
          52  POP_TOP          
        53_0  COME_FROM                '34'

 413      53  SETUP_LOOP          214  'to 270'
          56  LOAD_GLOBAL           5  'enumerate'
          59  LOAD_FAST             1  'inscr_buff_list'
          62  CALL_FUNCTION_1       1 
          65  GET_ITER         
          66  FOR_ITER            200  'to 269'
          69  UNPACK_SEQUENCE_2     2 
          72  STORE_FAST            2  'idx'
          75  STORE_FAST            3  'component_buff_info'

 414      78  LOAD_FAST             3  'component_buff_info'
          81  UNPACK_SEQUENCE_3     3 
          84  STORE_FAST            4  '_component_id'
          87  STORE_FAST            5  'inscr_buff_id'
          90  STORE_FAST            6  'buff_value'

 415      93  LOAD_GLOBAL           6  'confmgr'
          96  LOAD_ATTR             7  'get'
          99  LOAD_CONST            2  'inscription_data'
         102  LOAD_GLOBAL           8  'str'
         105  LOAD_FAST             5  'inscr_buff_id'
         108  CALL_FUNCTION_1       1 
         111  LOAD_CONST            3  'descTid'
         114  LOAD_CONST            4  'default'
         117  LOAD_CONST            5  ''
         120  CALL_FUNCTION_259   259 
         123  STORE_FAST            7  'text_id'

 416     126  LOAD_GLOBAL           6  'confmgr'
         129  LOAD_ATTR             7  'get'
         132  LOAD_CONST            2  'inscription_data'
         135  LOAD_GLOBAL           8  'str'
         138  LOAD_FAST             5  'inscr_buff_id'
         141  CALL_FUNCTION_1       1 
         144  LOAD_CONST            6  'descDetailTid'
         147  LOAD_CONST            4  'default'
         150  LOAD_CONST            5  ''
         153  CALL_FUNCTION_259   259 
         156  STORE_FAST            8  'detailTid'

 418     159  LOAD_GLOBAL           9  'getattr'
         162  LOAD_GLOBAL           7  'get'
         165  LOAD_FAST             2  'idx'
         168  LOAD_CONST            1  1
         171  BINARY_ADD       
         172  BINARY_MODULO    
         173  CALL_FUNCTION_2       2 
         176  STORE_FAST            9  'ui_item'

 419     179  LOAD_FAST             9  'ui_item'
         182  POP_JUMP_IF_FALSE    66  'to 66'

 420     185  LOAD_FAST             9  'ui_item'
         188  LOAD_ATTR            10  'temp_stat'
         191  LOAD_ATTR            11  'GetItem'
         194  LOAD_CONST            8  ''
         197  CALL_FUNCTION_1       1 
         200  LOAD_ATTR            12  'lab_content'
         203  LOAD_ATTR            13  'SetString'
         206  LOAD_FAST             7  'text_id'
         209  CALL_FUNCTION_1       1 
         212  POP_TOP          

 421     213  LOAD_FAST             9  'ui_item'
         216  LOAD_ATTR            10  'temp_stat'
         219  LOAD_ATTR            11  'GetItem'
         222  LOAD_CONST            8  ''
         225  CALL_FUNCTION_1       1 
         228  LOAD_ATTR            14  'lab_num'
         231  LOAD_ATTR            13  'SetString'
         234  LOAD_GLOBAL          15  'format_buff_value'
         237  LOAD_FAST             6  'buff_value'
         240  CALL_FUNCTION_1       1 
         243  CALL_FUNCTION_1       1 
         246  POP_TOP          

 422     247  LOAD_FAST             9  'ui_item'
         250  LOAD_ATTR            16  'lab_desc'
         253  LOAD_ATTR            13  'SetString'
         256  LOAD_FAST             8  'detailTid'
         259  CALL_FUNCTION_1       1 
         262  POP_TOP          
         263  JUMP_BACK            66  'to 66'
         266  JUMP_BACK            66  'to 66'
         269  POP_BLOCK        
       270_0  COME_FROM                '53'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 173


def get_com_sort_name(com_item_no):
    from logic.gcommon.cdata.mecha_component_data import get_component_type
    from logic.gcommon.cdata.mecha_component_data import COMPONENT_ATK, COMPONENT_DEFENSE
    com_type = get_component_type(com_item_no)
    data = {COMPONENT_ATK: 81869,COMPONENT_DEFENSE: 81871
       }
    return data.get(com_type, 81869)