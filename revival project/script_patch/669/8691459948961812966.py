# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/koth_shop_utils.py
from __future__ import absolute_import
import six_ex
import six
from logic.gcommon.common_const.shop_const import KING_SHOP_MONEY_UNIT_DIAMOND, KING_SHOP_MONEY_UNIT_GOLD
from logic.gutils import template_utils
from logic.gutils import item_utils
import copy

def get_shop_item_price--- This code section failed: ---

  10       0  LOAD_CONST            1  'gold_consumed'
           3  LOAD_FAST             0  'mall_conf'
           6  COMPARE_OP            6  'in'
           9  POP_JUMP_IF_FALSE    28  'to 28'

  11      12  POP_JUMP_IF_FALSE     1  'to 1'
          15  BINARY_SUBSCR    
          16  STORE_FAST            2  'price'

  12      19  LOAD_GLOBAL           0  'KING_SHOP_MONEY_UNIT_GOLD'
          22  STORE_FAST            3  'goods_payment'
          25  JUMP_FORWARD         13  'to 41'

  14      28  JUMP_FORWARD          2  'to 33'
          31  BINARY_SUBSCR    
          32  STORE_FAST            2  'price'

  15      35  LOAD_GLOBAL           1  'KING_SHOP_MONEY_UNIT_DIAMOND'
          38  STORE_FAST            3  'goods_payment'
        41_0  COME_FROM                '25'

  16      41  LOAD_FAST             2  'price'
          44  LOAD_FAST             1  'count'
          47  BINARY_MULTIPLY  
          48  LOAD_FAST             3  'goods_payment'
          51  BUILD_TUPLE_2         2 
          54  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 12


def check_diamond(consumed, own, pay_tip=False):
    if own < consumed:
        if pay_tip:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            SecondConfirmDlg2().confirm(content=get_text_local_content(12008))
        return False
    return True


def check_gold(consumed, own, pay_tip=False):
    if own < consumed:
        if pay_tip:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            SecondConfirmDlg2().confirm(content=get_text_local_content(12008))
        return False
    return True


def check_payment(consumed, money_info, pay_tip=False):
    from logic.gcommon.common_const.shop_const import KING_SHOP_MONEY_UNIT_GOLD, KING_SHOP_MONEY_UNIT_DIAMOND
    payment_checker = {'diamond_consumed': (
                          check_diamond, KING_SHOP_MONEY_UNIT_DIAMOND),
       'gold_consumed': (
                       check_gold, KING_SHOP_MONEY_UNIT_GOLD)
       }
    is_enough = True
    for currency, cost in six.iteritems(consumed):
        if currency not in six_ex.keys(payment_checker):
            continue
        func, currency_type = payment_checker[currency]
        own_money = money_info.get(currency_type, 0)
        is_enough = is_enough and func(cost, own_money, pay_tip)

    return is_enough


def init_shop_weapon_item(ui_item, goods_data, is_enough=True):
    from logic.gutils import item_utils
    goods_id = goods_data.get('goods_id', None)
    item_no = goods_data.get('item_dict', {}).get('1', {}).get('item_no', None)
    item_type = goods_data.get('item_type', None)
    num = goods_data.get('num', 1)
    sell_pos = goods_data.get('sell_pos', 1)
    diamond_consumed = goods_data.get('diamond_consumed', 500)
    item_name = item_utils.get_item_name(item_no)
    ui_item.lab_name.setString(item_name)
    ui_item.img_weapen.SetDisplayFrameByPath('', item_utils.get_gun_pic_by_item_id(item_no))
    init_shop_money_label(ui_item, goods_data, is_enough)
    return


def init_shop_money_label(ui_item, item_info, is_enough, colors=('#SW', '#SR')):
    from logic.client.const.koth_shop_const import GOLD_PIC, DIAMOND_PIC
    diamond_consumed = item_info.get('diamond_consumed', 0)
    gold_consumed = item_info.get('gold_consumed', 0)
    if diamond_consumed:
        ui_item.img_money.lab_money.SetString(str(diamond_consumed))
        ui_item.img_money.lab_money.SetColor(colors[0] if is_enough else colors[1])
        ui_item.img_money.SetDisplayFrameByPath('', DIAMOND_PIC)
        ui_item.img_money.setVisible(True)
    elif gold_consumed:
        ui_item.img_money.lab_money.SetString(str(gold_consumed))
        ui_item.img_money.lab_money.SetColor(colors[0] if is_enough else colors[1])
        ui_item.img_money.SetDisplayFrameByPath('', GOLD_PIC)
        ui_item.img_money.setVisible(True)
    else:
        ui_item.img_money.lab_money.SetString('')
        ui_item.img_money.setVisible(False)


def init_koth_own_money(ui_item, item_info):
    gold_num = item_info.get(KING_SHOP_MONEY_UNIT_GOLD, 0)
    diamond_num = item_info.get(KING_SHOP_MONEY_UNIT_DIAMOND, 0)
    ui_item.img_coin.lab_coin.setString(str(gold_num))
    ui_item.img_diamond.lab_diamond.setString(str(diamond_num))


def init_koth_own_money2(ui_item, item_info):
    gold_num = item_info.get(KING_SHOP_MONEY_UNIT_GOLD, 0)
    diamond_num = item_info.get(KING_SHOP_MONEY_UNIT_DIAMOND, 0)
    ui_item.lab_currency1.setString(str(gold_num))
    ui_item.lab_currency.setString(str(diamond_num))


def init_mall_item_temp(item_temp, item_dict):
    item_no = item_dict.get('item_no')
    can_upgrade = item_dict.get('can_upgrade', False)
    show_text = item_dict.get('show_text', None)
    if item_no is not None:
        item_temp.btn_item.setVisible(True)
        img_quality = template_utils.get_item_quality_pic(item_no)
        item_temp.img_quality.SetDisplayFrameByPath('', img_quality)
        item_temp.img_item.SetDisplayFrameByPath('', item_utils.get_item_pic_by_item_no(item_no))
        item_temp.img_upgrade.setVisible(can_upgrade)
        item_temp.quantity.setVisible(show_text is not None)
        if show_text:
            item_temp.quantity.SetString(str(show_text))
    else:
        item_temp.btn_item.setVisible(False)
    return


def calc_player_item_upgrade_info(item_no, shop_tab):
    from common.cfg import confmgr
    upgrade_infos = confmgr.get('king_shop_config', 'items_data', str(item_no), default={})
    cur_level = str(upgrade_infos.get('level'))
    cur_goods_id = upgrade_infos.get('goods_id')
    item_infos = confmgr.get('king_shop_config', 'goods_data', str(shop_tab), default={})
    next_level = get_koth_item_next_level(cur_level)
    if not next_level:
        return {'is_full_lv': True}
    else:
        goods_data = item_infos.get(str(cur_goods_id), {})
        goods_item_dict_data = copy.deepcopy(goods_data.get('item_dict', {}).get(str(next_level), {'is_full_lv': True}))
        if goods_item_dict_data.get('item_no'):
            if not goods_item_dict_data.get('is_full_lv'):
                goods_item_dict_data['level'] = int(next_level)
            return goods_item_dict_data
        return None


def get_koth_item_next_level(str_lv):
    return {'1': '2','2': '3','3': None}.get(str_lv, None)


def check_koth_item_can_upgrade():
    pass


def get_cur_shop_lent():
    if global_data.cam_lctarget:
        pos = global_data.cam_lctarget.ev_g_position()
        if global_data.king_battle_data.is_in_camp(pos, global_data.king_battle_data.my_camp_id):
            return get_shop_lent(global_data.king_battle_data.my_camp_id)
        else:
            return get_shop_lent()


def get_shop_lent(faction_id=0):
    from mobile.common.EntityManager import EntityManager
    shop_ls = EntityManager.get_entities_by_type('Shop')
    shop_list = [ shop_ent for _, shop_ent in six.iteritems(shop_ls) if shop_ent.get_faction_id() == faction_id ]
    if shop_list:
        shop_ent = shop_list[0]
        if shop_ent and shop_ent.logic:
            return shop_ent.logic
    return None


def get_goods_id_by_item_id(item_id):
    from common.cfg import confmgr
    item_infos = confmgr.get('king_shop_config', 'items_data', str(item_id), default={})
    goods_id = item_infos.get('goods_id')
    return goods_id