# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/FightData.py
from __future__ import absolute_import
from copy import deepcopy
from logic.gcommon.common_const import battle_const, weapon_const, buff_const, attr_const
from logic.gcommon.const import HIT_PART_BODY
from logic.gcommon.item import item_utility as iutil
KEY_TYPE = 'type'
KEY_PART = 'part'
KEY_PARTS = 'parts'
KEY_BUFF = 'buf'
KEY_BULLET = 'bullet'
KEY_AIM = 'aim'
KEY_MASK = 'mask'
KEY_RAW_ATK = 'atk'
KEY_ATK_ITEM = 'item'
KEY_ATK_START = 'start'
KEY_ATK_TARGET = 'target'
KEY_ATK_PELLET = 'pel'
KEY_ATK_NAME = 'name'
KEY_ATK_ARP = 'arp'
KEY_ATK_BUFF = 'atk_buff'
KEY_ATK_MAT = 'mat'
KEY_ATK_POS = 'pos'
KEY_ATK_SOURCE_POS = 'spos'
KEY_ATK_UID = 'atk_uid'
KEY_ATK_FORCE = 'force'
KEY_ATK_SID = 'skill_id'
KEY_ATK_SDATA = 'skill_data'
KEY_ATK_PASSIVE_SKILL = 'passive_skill'
KEY_ATK_PARTS_FACTOR = 'part_factor'
KEY_ATK_SHIELD_FACTOR = 'shield_factor'
KEY_ATK_SHOW_INFO = 'show_info'
KEY_NON_STAT = 'non_stat'
KEY_ATK_TIME = 'atk_time'
KEY_IMMUNE_ALL_DAMAGE = 'immune_all'
KEY_ATK_CRIT = 'key_atk_crit'
KEY_ATK_POWER_FACTOR = 'key_power_factor'
KEY_ATK_POWER_ADD = 'key_power_add'
KEY_ATK_ITEM_EID = 'item_eid'
KEY_ATK_EARLY_POWER_FACTOR = 'early_power_factor'
KEY_WEAK_HIT_FACTOR = 'weak_hit_factor'
KEY_ARMOR_PIERCE_FACTOR = 'armor_pierce_factor'
WEAK_HIT_STANDARD = 1.1
KEY_SECKILL = 'seckill'
KEY_SECKILL_HIT_HINT = 'seckill_hit_hint'
KEY_MONSTER_SECKILL_PERCENT = 'monster_seckill_percent'
KEY_DAMAGE = 'dmg'
KEY_SHIELD_DAMAGE = 'shield_dmg'
KEY_REAL_DAMAGE = 'real_dmg'
KEY_INNER_DAMAGE = 'inner_dmg'
KEY_DMG_MAP = 'dmg_map'
KEY_EFFECT = 'eft'
KEY_REDUCE = 'rdc'
KEY_ENTITY_TAG = 'tag'
KEY_DIE_OR_BROKEN = 'die_or_broken'
KEY_MECHA_ID = 'mecha_id'
KEY_SKIN_ID = 'skin_id'
FD_MAKER_SOUL = 1
FD_MAKER_MECHA = 2
FD_MAKER_DANMU = 3
FD_MAKER_MONSTER = 4
FD_MAKER_POISON = 5
FD_MAKER_SIGNAL = 6
FD_MAKER_KONGDAO_FALL = 7
FD_MAKER_FIELD = 8
FD_MAKER_TYPES = {'Mecha': FD_MAKER_MECHA,
   'Soul': FD_MAKER_SOUL,
   'SoulDirect': FD_MAKER_SOUL,
   'Monster': FD_MAKER_MONSTER
   }
SYSTEM_FD_MAKER = set([FD_MAKER_POISON, FD_MAKER_MONSTER, FD_MAKER_SIGNAL, FD_MAKER_KONGDAO_FALL])

def is_system_maker(maker_type):
    return maker_type in SYSTEM_FD_MAKER


class FightData(object):
    __slots__ = ('id_trigger', 'id_target', 'type', 'atk_data', 'inj_data', 'maker_type',
                 'target_type', 'trigger_faction')

    def __init__(self):
        super(FightData, self).__init__()
        self.id_trigger = None
        self.maker_type = None
        self.trigger_faction = None
        self.id_target = None
        self.target_type = None
        self.type = None
        self.atk_data = {}
        self.inj_data = {}
        return


def get_ft_data_by_type(i_type, damage, id_trigger=None, id_target=None):
    ft_dat = FightData()
    ft_dat.type = i_type
    ft_dat.id_trigger = id_trigger
    ft_dat.id_target = id_target
    ft_dat.atk_data[KEY_RAW_ATK] = damage
    return ft_dat


def get_building_ft_data(building, damage, target_id, frompos, targetpos):
    dat = FightData()
    dat.type = battle_const.FIGHT_TYPE_SHOOT
    dat.id_trigger = building.get_owner_id()
    dat.id_target = target_id
    dat.atk_data[KEY_RAW_ATK] = damage
    dat.atk_data[KEY_PARTS] = {HIT_PART_BODY: 1}
    dat.atk_data[KEY_ATK_ITEM] = building.get_no()
    dat.atk_data[KEY_ATK_TARGET] = targetpos
    dat.atk_data[KEY_ATK_START] = frompos
    dat.atk_data[KEY_ATK_ARP] = False
    dat.atk_data[KEY_AIM] = battle_const.AIM_MODE_NORMAL
    dat.atk_data[KEY_MASK] = battle_const.SHOOT_MASK_AT_AIM
    return dat


def get_buff_ft_data(id_target, damage, buff_id, buff_data, is_human):
    ft_dat = FightData()
    ft_dat.type = battle_const.FIGHT_TYPE_BUFF
    ft_dat.id_trigger = buff_data.get('creator_id', None)
    ft_dat.id_target = id_target
    ft_dat.atk_data[KEY_RAW_ATK] = damage
    ft_dat.atk_data[KEY_ATK_BUFF] = buff_id
    if ft_dat.id_trigger:
        ft_dat.atk_data[KEY_ATK_NAME] = buff_data['creator_name']
        ft_dat.atk_data[KEY_ATK_ITEM] = buff_data['creator_item']
    ft_dat.maker_type = FD_MAKER_MECHA
    mecha_id = buff_data.get('mecha_id', None)
    if mecha_id > 0:
        ft_dat.atk_data[KEY_MECHA_ID] = mecha_id
    return ft_dat


def get_bomb_ft_data(target, damage, bomb_data, parts, ltrigger):
    ft_dat = FightData()
    ft_dat.id_trigger = bomb_data['owner_id']
    ft_dat.maker_type = bomb_data.get('owner_type', 'Soul')
    ft_dat.type = battle_const.FIGHT_TYPE_BOMB
    ft_dat.id_target = target.id
    ft_dat.target_type = target.__class__.__name__
    ft_dat.atk_data[KEY_RAW_ATK] = damage
    ft_dat.atk_data[KEY_ATK_ITEM] = bomb_data['item_itype']
    ft_dat.atk_data[KEY_ATK_ITEM_EID] = bomb_data.get('item_eid', None)
    ft_dat.atk_data[KEY_ATK_NAME] = bomb_data['owner_name']
    ft_dat.atk_data[KEY_MECHA_ID] = bomb_data.get('mecha_id', None)
    ft_dat.atk_data[KEY_SKIN_ID] = bomb_data.get('skin_id', None)
    ft_dat.atk_data[KEY_ATK_POS] = bomb_data['position']
    ft_dat.atk_data[KEY_ATK_UID] = bomb_data.get('uniq_key', None)
    if 'skill_data' in bomb_data:
        ft_dat.atk_data[KEY_ATK_SDATA] = bomb_data['skill_data']
        ft_dat.atk_data[KEY_ATK_SDATA]['uniq_key'] = ft_dat.atk_data[KEY_ATK_UID]
    if ltrigger:
        ft_dat.atk_data[KEY_ATK_SHIELD_FACTOR] = ltrigger.ev_g_add_attr(attr_const.ATTR_SHIELD_DMG_FACTOR, bomb_data['item_itype']) + bomb_data.get('fShieldFactor', 0)
    ft_dat.atk_data[KEY_ATK_SOURCE_POS] = bomb_data.get('s_position', None)
    explose_time = bomb_data.get('explose_time', 0)
    last_time = bomb_data.get('last_time', 0)
    ft_dat.atk_data[KEY_ATK_TIME] = explose_time - last_time
    if 'sub_idx' in bomb_data:
        ft_dat.atk_data[KEY_ATK_SHOW_INFO] = {'sub_idx': bomb_data['sub_idx']}
    if parts:
        ft_dat.atk_data[KEY_PARTS] = parts
    buff_add_id = bomb_data.get('buff_add', None)
    if buff_add_id:
        buff_cond = bomb_data.get('buff_cond', None)
        buff_enable = False
        if not buff_cond:
            buff_enable = True
        elif buff_cond == buff_const.BUFF_COND_ADD_ON_DAMAGE:
            buff_enable = True if damage > 0 else False
        elif buff_cond == buff_const.BUFF_COND_FIT_TARGET_ID:
            if target.id == bomb_data.get('target', None):
                buff_enable = True
        elif buff_cond == buff_const.BUFF_COND_ADD_GUN_FACTOR_RAD:
            factor_rad = bomb_data.get('calc_damage_factor_rad', {}).get(target.id, 0)
            buff_enable = factor_rad > 0
        if buff_enable:
            buff_list = ft_dat.atk_data.get(KEY_BUFF, [])
            buff_datas = bomb_data.get('buff_datas', {})
            buff_creator_info = {'creator_name': bomb_data['owner_name'],
               'creator_item': bomb_data['item_itype'],
               'creator_id': ft_dat.id_trigger,
               'mecha_id': bomb_data.get('mecha_id', None),
               'trigger_id': bomb_data.get('trigger_id', None)
               }
            custom_buff_data = bomb_data.get('custom_param', {}).get('update_buff_data', {})
            for buff_id in buff_add_id:
                buff_data = buff_datas.get(buff_id, {})
                buff_data.update(bomb_data.get('buff_' + str(buff_id), {}))
                buff_data.update(buff_creator_info)
                custom_data = deepcopy(custom_buff_data.get(str(buff_id), {}))
                battle = None
                if ltrigger:
                    battle = ltrigger.get_battle()
                    battle and hasattr(battle, 'battle_modify_custom_data') and battle.battle_modify_custom_data(custom_data, ltrigger, buff_id)
                buff_data.update(custom_data)
                buff_data.update({'bomb_position': bomb_data.get('position')})
                buff_list.append((buff_id, buff_data))

            ft_dat.atk_data[KEY_BUFF] = buff_list
    skill_id = bomb_data.get('skill_id', None)
    if skill_id:
        ft_dat.atk_data[KEY_ATK_SID] = skill_id
        skill_data = bomb_data.get('skill_data', None)
        if skill_data:
            ft_dat.atk_data[KEY_ATK_SDATA] = skill_data
    return ft_dat


def get_bomb_door_ft_data(target, damage, bomb_data, door_index, ltrigger):
    ft_dat = get_bomb_ft_data(target, damage, bomb_data, None, ltrigger)
    ft_dat.atk_data[KEY_PARTS] = {door_index: 1}
    return ft_dat


def get_broken_ft_data(damage, owner_id, owner_name, item_itype, lst_pos, is_seckill=False):
    ft_dat = FightData()
    ft_dat.id_trigger = owner_id
    ft_dat.type = battle_const.FIGHT_TYPE_X_BOMB
    ft_dat.atk_data[KEY_RAW_ATK] = is_seckill or damage if 1 else 1
    ft_dat.atk_data[KEY_ATK_ITEM] = item_itype
    ft_dat.atk_data[KEY_ATK_NAME] = owner_name
    ft_dat.atk_data[KEY_SECKILL] = is_seckill
    ft_dat.atk_data[KEY_ATK_POS] = lst_pos
    return ft_dat


def get_mecha_broken_ft_data(damage, owner_id, owner_name, item_itype, lst_pos, is_seckill=False):
    ft_dat = get_broken_ft_data(damage, owner_id, owner_name, item_itype, lst_pos, is_seckill)
    ft_dat.type = battle_const.FIGHT_TYPE_BOMB
    return ft_dat


def get_crash_ft_data(damage, crash_type, item_itype, tp3_pos, owner_id=None):
    ft_dat = FightData()
    ft_dat.type = battle_const.FIGHT_TYPE_CRASH
    ft_dat.id_trigger = owner_id
    ft_dat.atk_data[KEY_RAW_ATK] = damage
    ft_dat.atk_data[KEY_ATK_ITEM] = item_itype
    ft_dat.atk_data[KEY_ATK_POS] = tp3_pos
    ft_dat.maker_type = FD_MAKER_SOUL
    if item_itype and iutil.is_mecha(item_itype):
        ft_dat.atk_data[KEY_MECHA_ID] = item_itype
        ft_dat.maker_type = FD_MAKER_MECHA
    ft_dat.atk_data[KEY_TYPE] = crash_type
    return ft_dat


def get_thunder_ft_data(owner_id, owner_name, owner_faction, tp3_pos, id_target, damage, trigger_item_id, mecha_id):
    ft_dat = FightData()
    ft_dat.type = battle_const.FIGHT_TYPE_THUNDER
    ft_dat.id_trigger = owner_id
    ft_dat.trigger_faction = owner_faction
    ft_dat.id_target = id_target
    ft_dat.atk_data[KEY_ATK_NAME] = owner_name
    ft_dat.atk_data[KEY_RAW_ATK] = damage
    ft_dat.atk_data[KEY_ATK_POS] = tp3_pos
    ft_dat.atk_data[KEY_ATK_ITEM] = trigger_item_id
    ft_dat.maker_type = FD_MAKER_MECHA
    if mecha_id > 0:
        ft_dat.atk_data[KEY_MECHA_ID] = mecha_id
    return ft_dat


def get_fall_ft_data--- This code section failed: ---

 322       0  LOAD_GLOBAL           0  'FightData'
           3  CALL_FUNCTION_0       0 
           6  STORE_FAST            1  'ft_dat'

 323       9  LOAD_GLOBAL           1  'battle_const'
          12  LOAD_ATTR             2  'FIGHT_TYPE_KILL'
          15  LOAD_FAST             1  'ft_dat'
          18  STORE_ATTR            3  'type'

 324      21  LOAD_GLOBAL           4  'True'
          24  LOAD_FAST             1  'ft_dat'
          27  LOAD_ATTR             5  'atk_data'
          30  LOAD_GLOBAL           6  'KEY_ATK_FORCE'
          33  STORE_SUBSCR     

 325      34  LOAD_GLOBAL           7  'FD_MAKER_KONGDAO_FALL'
          37  LOAD_FAST             1  'ft_dat'
          40  STORE_ATTR            8  'maker_type'

 326      43  STORE_ATTR            1  'battle_const'
          46  BINARY_ADD       
          47  LOAD_FAST             1  'ft_dat'
          50  LOAD_ATTR             5  'atk_data'
          53  LOAD_GLOBAL           9  'KEY_RAW_ATK'
          56  STORE_SUBSCR     

 327      57  LOAD_FAST             1  'ft_dat'
          60  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_ATTR' instruction at offset 43


def get_field_ft_data(id_target, damage, field_data):
    ft_dat = FightData()
    ft_dat.type = battle_const.FIGHT_TYPE_FIELD
    ft_dat.id_trigger = field_data.get('creator_id', None)
    ft_dat.id_target = id_target
    ft_dat.atk_data[KEY_RAW_ATK] = damage
    if ft_dat.id_trigger:
        ft_dat.atk_data[KEY_ATK_NAME] = field_data.get('creator_name')
        ft_dat.atk_data[KEY_ATK_ITEM] = field_data.get('creator_item')
    ft_dat.maker_type = FD_MAKER_FIELD
    return ft_dat