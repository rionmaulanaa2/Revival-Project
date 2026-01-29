# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComBackpackData.py
from __future__ import absolute_import
import six_ex
import six
from ..UnitCom import UnitCom
from ... import const
from ...item import item_const as iconst
from ...item import item_utility as iutil
import json
from logic.gcommon.cdata.status_config import ST_SWIM, ST_PARACHUTE
NOT_THROW_ITEM_STATE = [
 ST_SWIM, ST_PARACHUTE]

class ComBackpackData(UnitCom):
    BIND_EVENT = {'E_PICK_UP_OTHERS': 'pick_up_others',
       'E_PICK_UP_WEAPON': 'pick_up_weapon',
       'G_PICK_UP_WEAPON': 'pick_up_weapon',
       'E_PICK_UP_CLOTHING': 'pick_up_clothing',
       'G_PICK_UP_CLOTHING': 'pick_up_clothing',
       'E_PICK_UP_SUCC': 'pick_up_succ',
       'E_THROW_ITEM': 'on_throw_item',
       'G_THROW_ITEM': 'on_throw_item',
       'G_WEAPON_DATA': 'get_weapon_data',
       'G_CLOTHING_DATA_BY_POS': 'get_clothing_data',
       'G_ALL_WEAPONS': 'get_weapons',
       'G_CLOTHING': 'get_clothing',
       'G_OTHERS': 'get_others',
       'G_PICK_SUCC': 'get_pick_succ',
       'G_ITEM_DATA': 'get_item_data',
       'G_ITME_LIST_BY_ID': 'get_item_list_by_id',
       'G_ITEM_COUNT': 'get_item_count',
       'G_ALL_ITEM_COUNT': 'get_all_item_count',
       'G_ITEM_COUNT_BY_ENTITY_ID': 'get_item_count_by_entity_id',
       'G_CAPACITY': 'get_capacity',
       'E_MOD_ITME_COUNT': 'mod_item_count',
       'E_SWITCH_WEAPON': 'switch_weapon',
       'E_WPBAR_SWITCH_CUR': 'on_switch_cur',
       'G_PACK_ITEMS': 'pack_items',
       'E_WEAPON_BULLET_CHG': 'weapon_bullet_change',
       'E_DO_CLEAR_BACKPACK': 'clear_backpack',
       'E_DO_CLEAR_WEAPON': 'clear_weapon',
       'E_DO_CLEAR_CLOTHING': 'clear_clothing',
       'E_DO_CLEAR_OTHERS': 'clear_others',
       'E_DO_CLEAR_BACKPACK_WITH_LIMITED_LIST': 'clear_backpack_with_limited_list',
       'G_BACKPACK_DICT': 'get_client_dict',
       'G_BACKPACK_LOG_DICT': 'get_log_dict',
       'G_WEAPON_PUT_POS': 'get_weapon_put_pos',
       'G_FASHION': 'get_fashion',
       'G_MECHA_DICT': 'get_mecha_dict',
       'G_HAS_MECHA': 'has_mecha',
       'G_MECHA_FASHION': 'get_mecha_fashion',
       'G_ITEM_FASHION': 'get_item_fashion',
       'G_MECHA_SFX': 'get_mecha_sfx',
       'G_GLIDE_EFFECT': 'get_glide_effect',
       'G_MECHA_CUSTOM_SKIN': 'get_mecha_custom_skin',
       'G_ROLE_VOICE': 'get_role_voice',
       'G_WEAPON_PUT_POS_BY_REPLACE_SAME': 'get_weapon_put_pos_by_replace_same',
       'G_MECHA_POSE': 'get_mecha_pose',
       'G_CAN_THROW_ITEM': 'get_can_throw_item'
       }
    PICK_SUCC_MAX_NUM = 5

    def __init__(self):
        super(ComBackpackData, self).__init__()
        self.total_capacity = 0
        self.weapons = {}
        self.weapon_in_hand = const.PART_WEAPON_POS_MAIN1
        self.clothing = {}
        self.others = {}
        self.pick_succ = []
        self.fashion = {}
        self.mecha_dict = {}
        self.item_fashion = {}
        self.role_voice = []
        self.glide_effect = None
        self.glide_effect_visibility = 0
        return

    def reset(self):
        weapon_keys = six_ex.keys(self.weapons)
        for key in weapon_keys:
            self.on_throw_item(const.BACKPACK_PART_WEAPON, key)

        other_keys = six_ex.keys(self.others)
        for key in other_keys:
            self.on_throw_item(const.BACKPACK_PART_OTHERS, key)

        self.owner = None
        self.weapon_in_hand = const.PART_WEAPON_POS_MAIN1
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComBackpackData, self).init_from_dict(unit_obj, bdict)
        self.total_capacity = bdict.get('total_capacity', 20)
        self.weapons = bdict.get('weapons', {})
        self.others = bdict.get('others', {})
        self.clothing = bdict.get('clothing', {})
        self.fashion = bdict.get('fashion', {})
        self.mecha_dict = bdict.get('mecha_dict', {})
        self.item_fashion = bdict.get('item_fashion', {})
        self.role_voice = bdict.get('role_voice', [])
        self._is_puppet_com = self.is_unit_obj_type('LPuppet')
        self.glide_effect = bdict.get('glide_effect', None)
        self.glide_effect_visibility = bdict.get('glide_effect_visibility', const.GEV_ALL)
        return

    def get_client_dict(self):
        cdict = {'total_capacity': self.total_capacity,
           'weapons': self.weapons,
           'clothing': self.clothing,
           'others': self.others,
           'fashion': self.fashion,
           'mecha_dict': self.mecha_dict,
           'item_fashion': self.item_fashion,
           'role_voice': self.role_voice,
           'glide_effect': self.glide_effect,
           'glide_effect_visibility': self.glide_effect_visibility
           }
        return cdict

    def get_log_dict(self):
        ldict = {'weapons': self.weapons,
           'clothing': self.clothing
           }
        return json.dumps(ldict, default=lambda obj: str(obj))

    def get_capacity(self):
        return (
         self.total_capacity, len(self.others))

    def on_throw_item(self, backpack_part, key):
        item_data = None
        item_pos = -1
        if backpack_part == const.BACKPACK_PART_OTHERS:
            item_data = self.others.get(key, None)
            if item_data is not None:
                del self.others[key]
                self.send_event('E_ITEM_DATA_CHANGED', item_data)
        elif backpack_part == const.BACKPACK_PART_CLOTHING:
            item_data = self.clothing.get(key, None)
            if item_data is not None:
                del self.clothing[key]
                self.send_event('E_CLOTHING_CHANGED', key)
        elif backpack_part == const.BACKPACK_PART_WEAPON:
            item_data = self.weapons.get(key, None)
            if item_data is not None:
                del self.weapons[key]
                self.send_event('E_WEAPON_DATA_DELETED', key)
                self.send_event('E_WEAPON_DATA_CHANGED', key)
                self.send_event('E_WEAPON_DATA_DELETED_SUCCESS', key)
        return item_data

    def get_weapon_put_pos(self, item_data, put_pos):
        item_id = item_data.get('item_id')
        cur_put_pos = -1
        if not iutil.is_gun(item_id):
            return cur_put_pos
        else:
            if put_pos < 0:
                if self.weapons.get(const.PART_WEAPON_POS_MAIN1, None) == None:
                    cur_put_pos = const.PART_WEAPON_POS_MAIN1
                elif self.weapons.get(const.PART_WEAPON_POS_MAIN2, None) == None:
                    cur_put_pos = const.PART_WEAPON_POS_MAIN2
                elif self.weapons.get(const.PART_WEAPON_POS_MAIN3, None) == None:
                    cur_put_pos = const.PART_WEAPON_POS_MAIN3
                else:
                    cur_put_pos = self.weapon_in_hand
            else:
                cur_put_pos = put_pos
            return cur_put_pos

    def get_weapon_put_pos_by_replace_same(self, weapon_data, check_empty_pos):
        if check_empty_pos and len(self.weapons) < len(const.MAIN_WEAPON_LIST):
            weapon_pos = self.get_weapon_put_pos(weapon_data, -1)
            if weapon_pos != const.PART_WEAPON_POS_MAIN_DF:
                return weapon_pos
        item_id = weapon_data.get('item_id')
        for pos, item_data in six.iteritems(self.weapons):
            this_item_id = item_data.get('item_id')
            if not iutil.is_same_type_weapon(item_id, this_item_id):
                continue
            if iutil.get_backpack_item_level(item_id) > iutil.get_backpack_item_level(this_item_id):
                return pos

        for pos, item_data in six.iteritems(self.weapons):
            this_item_id = item_data.get('item_id')
            if not iutil.is_same_type_weapon(item_id, this_item_id):
                continue
            if iutil.get_backpack_item_level(item_id, 0) == iutil.get_backpack_item_level(this_item_id, -1):
                return pos

        return -1

    def pick_up_weapon(self, item_data, put_pos, switch=True):
        throw_item_data = None
        cur_put_pos = self.get_weapon_put_pos(item_data, put_pos)
        if cur_put_pos > 0:
            throw_item_data = self.weapons.get(cur_put_pos, None)
            self.weapons[cur_put_pos] = item_data
            self.send_event('E_WEAPON_DATA_CHANGED', cur_put_pos)
        self.send_event('E_ON_PICK_UP_WEAPON', cur_put_pos, throw_item_data is not None, switch)
        return (
         const.BACKPACK_PART_WEAPON, cur_put_pos, throw_item_data)

    def pick_up_others(self, item_data):
        entity_id = item_data.get('entity_id', 0)
        self.others[entity_id] = item_data
        self.send_event('E_ITEM_DATA_CHANGED', item_data)
        return (
         const.BACKPACK_PART_OTHERS, 1, None)

    def pick_up_succ(self, entity_id, item_id=None, auto_use=False):
        self.pick_succ.append(entity_id)
        if len(self.pick_succ) > self.PICK_SUCC_MAX_NUM:
            self.pick_succ.pop(0)
        if item_id and auto_use:
            self.send_event('E_PICK_UP_SOUND', item_id)

    def get_pick_succ(self):
        return self.pick_succ

    def pick_up_clothing(self, item_dict):
        item_no = item_dict['item_id']
        dress_pos = iutil.get_clothing_dress_pos(item_no)
        if dress_pos is None:
            return (None, 0, None)
        else:
            pos_list = iconst.CLOTHING_LOGIC_PARTS.get(dress_pos, (dress_pos,))
            replace_item_list = []
            replace_pos_list = []
            for replace_pos in pos_list:
                old_item = self.clothing.get(replace_pos, None)
                if old_item:
                    replace_item_list.append(old_item)
                    replace_pos_list.append(replace_pos)
                    del self.clothing[replace_pos]

            self.clothing[dress_pos] = item_dict
            self.send_event('E_CLOTHING_CHANGED', dress_pos)
            for replace_pos in replace_pos_list:
                if replace_pos is not dress_pos:
                    self.send_event('E_CLOTHING_CHANGED', replace_pos)

            return (
             const.BACKPACK_PART_CLOTHING, dress_pos, replace_item_list)

    def switch_weapon_in_hand(self, switch_pos):
        if switch_pos == self.weapon_in_hand:
            return
        else:
            if self.weapons.get(switch_pos, None) is None:
                return
            self.weapon_in_hand = switch_pos
            return self.weapons.get(switch_pos)

    def mod_item_count(self, backpack_part, item_entity_id, count):
        item_data, item_pos = self.get_item_data(backpack_part, item_entity_id)
        if item_data is None:
            return
        else:
            item_data['count'] += count
            item_data['refresh'] = False
            self.send_event('E_ITEM_DATA_CHANGED', item_data)
            item_data['refresh'] = True
            return

    def switch_weapon(self, pos1, pos2):
        weapon_data1 = self.get_weapon_data(pos1)
        weapon_data2 = self.get_weapon_data(pos2)
        self.weapons[pos1] = weapon_data2
        self.weapons[pos2] = weapon_data1
        if pos1 == self.weapon_in_hand and weapon_data1 is not None:
            self.weapon_in_hand = pos2
        elif pos2 == self.weapon_in_hand and weapon_data2 is not None:
            self.weapon_in_hand = pos1
        if not weapon_data2:
            del self.weapons[pos1]
        elif not weapon_data1:
            del self.weapons[pos2]
        self.send_event('E_WEAPON_DATA_SWITCHED', pos1, pos2)
        return

    def pack_items(self):
        all_items = {}
        for pos, info in six_ex.items(self.weapons):
            if pos == const.PART_WEAPON_POS_MAIN_DF:
                continue
            elif info is not None:
                if info['item_id'] in iconst.VIRTUAL_WEAPONS:
                    continue
                all_items[info['entity_id']] = info

        for dress_pos, item_dict in six_ex.items(self.clothing):
            if dress_pos in iconst.CLOTHING_OFF_PARTS and item_dict is not None:
                all_items[item_dict['entity_id']] = item_dict

        for pos, info in six_ex.items(self.others):
            if info is not None:
                all_items[info['entity_id']] = info

        self.ev_g_ai_pack_items(all_items)
        return all_items

    def weapon_bullet_change(self, weapon_pos, cur_bullet_cnt):
        wp = self.ev_g_wpbar_get_by_pos(weapon_pos)
        if not wp:
            return
        wp.set_bullet_num(cur_bullet_cnt)
        if self._is_puppet_com and global_data.cam_lplayer is not self.unit_obj:
            return
        self.send_event('E_WEAPON_DATA_CHANGED', weapon_pos)
        self.send_event('E_CUR_BULLET_NUM_CHG', weapon_pos)

    def clear_backpack(self):
        for pos in six_ex.keys(self.weapons):
            del self.weapons[pos]
            self.send_event('E_WEAPON_DATA_CHANGED', pos)

        for pos in six_ex.keys(self.clothing):
            del self.clothing[pos]
            self.send_event('E_CLOTHING_CHANGED', pos)

        for pos in six_ex.keys(self.others):
            item_data = self.others[pos]
            del self.others[pos]
            self.send_event('E_ITEM_DATA_CHANGED', item_data)

    def clear_weapon(self):
        for pos in six_ex.keys(self.weapons):
            del self.weapons[pos]
            self.send_event('E_WEAPON_DATA_CHANGED', pos)

    def clear_clothing(self):
        for pos in six_ex.keys(self.clothing):
            del self.clothing[pos]
            self.send_event('E_CLOTHING_CHANGED', pos)

    def clear_others(self):
        for pos in six_ex.keys(self.others):
            item_data = self.others[pos]
            del self.others[pos]
            self.send_event('E_ITEM_DATA_CHANGED', item_data)

    def clear_backpack_with_limited_list(self, limited_list):
        for pos in six_ex.keys(self.weapons):
            if self.weapons[pos]['item_id'] not in limited_list:
                del self.weapons[pos]
                self.send_event('E_WEAPON_DATA_CHANGED', pos)

        for pos in six_ex.keys(self.clothing):
            if self.clothing[pos]['item_id'] not in limited_list:
                del self.clothing[pos]
                self.send_event('E_CLOTHING_CHANGED', pos)

        for pos in six_ex.keys(self.others):
            item_data = self.others[pos]
            if item_data['item_id'] not in limited_list:
                del self.others[pos]
                self.send_event('E_ITEM_DATA_CHANGED', item_data)

    def get_weapon_data(self, weapon_pos):
        return self.weapons.get(weapon_pos, None)

    def get_weapons(self):
        return self.weapons

    def get_clothing_data(self, dress_pos):
        return self.clothing.get(dress_pos, None)

    def get_clothing(self):
        return self.clothing

    def get_fashion(self):
        if not G_IS_CLIENT:
            return self.fashion
        else:
            from ext_package.ext_decorator import get_default_fashion
            return get_default_fashion(self, self.fashion)

    def get_others(self):
        return self.others

    def get_item_data(self, backpack_part, eid):
        item_data = None
        item_pos = -1
        if backpack_part == const.BACKPACK_PART_OTHERS:
            item_data = self.others.get(eid, None)
            item_pos = eid
        elif backpack_part == const.BACKPACK_PART_CLOTHING:
            for dress_pos, item_dict in six.iteritems(self.clothing):
                if item_dict and item_dict.get('entity_id', 0) == eid:
                    item_data = item_dict
                    item_pos = dress_pos
                    break

        elif backpack_part == const.BACKPACK_PART_WEAPON:
            for pos in six_ex.keys(self.weapons):
                weapon_data = self.weapons.get(pos, None)
                if weapon_data is not None and weapon_data.get('entity_id', 0) == eid:
                    item_data = self.weapons[pos]
                    item_pos = pos
                    break

        return (
         item_data, item_pos)

    def get_item_count(self, item_id):
        if G_IS_CLIENT:
            from logic.gcommon.item.item_const import ITEM_NO_MEOW_COIN
            if item_id and ITEM_NO_MEOW_COIN == int(item_id) and global_data.cam_lplayer:
                bag_num, _ = global_data.cam_lplayer.ev_g_meow_bag_info()
                return bag_num
        count = 0
        for entity_id, info in six_ex.items(self.others):
            if info.get('item_id') == item_id:
                count += info.get('count')

        return count

    def get_all_item_count(self):
        count_data = {}
        for entity_id, info in six_ex.items(self.others):
            item_id = info.get('item_id')
            count_data[item_id] = count_data.get(item_id, 0) + info.get('count', 0)

        return count_data

    def get_item_count_by_entity_id(self, entity_id):
        count = 0
        info = self.others.get(entity_id)
        if info:
            count = info.get('count')
        return count

    def get_item_list_by_id(self, item_id):
        item_list = []
        for entity_id, info in six_ex.items(self.others):
            if info.get('item_id') == item_id:
                item_list.append(info)

        return item_list

    def on_switch_cur(self, cur_pos):
        self.switch_weapon_in_hand(cur_pos)

    def get_mecha_dict(self):
        return self.mecha_dict

    def has_mecha(self, mecha_id):
        return mecha_id in self.mecha_dict

    def get_mecha_fashion(self, mecha_id):
        return self.mecha_dict.get(mecha_id, {}).get('fashion', {})

    def get_mecha_sfx(self, mecha_id):
        return self.mecha_dict.get(mecha_id, {}).get('sfx', None)

    def get_glide_effect(self, check_visibility=True):
        from logic.gcommon.const import GEV_ONLY_ME, GEV_ONLY_FRIEND, GEV_ALL
        if not check_visibility or self.glide_effect_visibility == GEV_ALL:
            return self.glide_effect
        from logic.gcommon.item.item_const import DEFAULT_GLIDE_EFFECT
        if self.glide_effect_visibility == GEV_ONLY_ME:
            if self.sd.ref_is_avatar:
                return self.glide_effect
        elif self.glide_effect_visibility == GEV_ONLY_FRIEND:
            if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate(self.ev_g_camp_id()):
                return self.glide_effect
        return DEFAULT_GLIDE_EFFECT

    def get_mecha_custom_skin(self, mecha_id):
        return self.mecha_dict.get(mecha_id, {}).get('custom_skin', {})

    def get_mecha_pose(self, mecha_id):
        return self.mecha_dict.get(mecha_id, {}).get('pose', {})

    def get_can_throw_item(self):
        if self.ev_g_is_in_any_state(NOT_THROW_ITEM_STATE):
            global_data.emgr.battle_show_message_event.emit(get_text_local_content(18135))
            return False
        if self.ev_g_gulag_status():
            global_data.emgr.battle_show_message_event.emit(get_text_local_content(18135))
            return False
        return True

    def get_item_fashion(self, item_id):
        return self.item_fashion.get(item_id, {})

    def get_role_voice(self):
        return self.role_voice