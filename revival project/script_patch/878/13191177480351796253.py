# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/local_battle_npc_utils.py
from __future__ import absolute_import
import six
import six_ex
import logic.gcommon.common_utils.idx_utils as idx_utils
from logic.gcommon.common_const.battle_const import COMBAT_STATE_NONE, FIGHT_EVENT_DEATH, FIGHT_EVENT_MECHA_DEATH
from mobile.common.EntityManager import EntityManager
from common.utils.timer import CLOCK
from logic.gcommon.common_utils.math3d_utils import v3d_to_tp
from logic.gcommon.common_const import ai_const
from logic.gcommon import time_utility as tutil
from mobile.common.IdManager import IdManager
import math3d
from common.cfg import confmgr
from logic.gcommon.item.item_utility import is_weapon
from logic.gcommon.item.item_const import SCENEBOX_ST_OPENED
from logic.gutils import item_utils

class NPCMgr(object):

    def __init__(self, lbs, local_battle):
        self._server = lbs
        self._local_battle = local_battle
        self._local_npcs = {}

    def destroy_npc(self, npc_id):
        if npc_id not in self._local_npcs:
            return
        np_entity = EntityManager.getentity(npc_id)
        if np_entity:
            self._local_battle.destroy_entity(npc_id)
            del self._local_npcs[npc_id]

    def destroy_all_npc(self):
        npc_ids = six_ex.keys(self._local_npcs)
        for npc_id in npc_ids:
            self.destroy_npc(npc_id)

    def tick(self):
        pass

    def lbs_send_event(self, evt, *args):
        self._server._lbs_send_event(evt, *args)

    def lbs_add_entity(self, entity_type, init_dict):
        return self._server._lbs_add_entity(entity_type, init_dict)

    def lbs_get_value(self, event):
        return self._server._lbs_get_value(event)

    def lbs_is_hit(self, start_pos, end_pos):
        return self._server._lbs_is_hit(start_pos, end_pos)

    def lbs_player_damage(self):
        self._server._lbs_player_damage()

    def get_all_npc_ids(self):
        return six_ex.keys(self._local_npcs)


class FightNPCMgrBase(NPCMgr):

    def __init__(self, lbs, local_battle):
        super(FightNPCMgrBase, self).__init__(lbs, local_battle)
        self._last_tick_time = None
        self._local_ai_timer = None
        self._allow_attack = True
        return

    def resume_attack(self):
        self._allow_attack = True
        self.tick()
        if not self._local_ai_timer:
            self._local_ai_timer = global_data.game_mgr.register_logic_timer(self.tick, interval=0.2, mode=CLOCK)

    def pause_attack(self):
        self._allow_attack = False
        if self._local_ai_timer:
            global_data.game_mgr.unregister_logic_timer(self._local_ai_timer)
            self._local_ai_timer = None
        return

    def delay_exec_destroy_ai(self, opt, ai_data):
        self.lbs_send_event('E_GUIDE_ROBOT_DEAD', ai_data['guide_id'], ai_data['interval'])
        self.destroy_npc(ai_data['id'])

    def on_hurt(self, npc_id, damage):
        pass

    def destroy_all_npc(self):
        super(FightNPCMgrBase, self).destroy_all_npc()
        self.pause_attack()

    def is_allow_attack(self):
        return self._allow_attack


class RobotMechaMgr(FightNPCMgrBase):

    def __init__(self, lbs, local_battle):
        super(RobotMechaMgr, self).__init__(lbs, local_battle)
        self._shoot_delay_timer = None
        return

    def add_robot_mecha(self, guide_id, interval, mecha_dict):
        robot_init_dict = {'max_hp': 200,
           'is_robot': True,
           'char_name': 'guide_robot',
           'weapons': {},'position': mecha_dict.get('pos'),
           'parachute_mecha_id': 8002,
           'faction_id': 1,
           'aim_y': 1.0,
           'role_id': '11'
           }
        robot = self.lbs_add_entity('Puppet', robot_init_dict)
        robot_id = robot.id
        from logic.gutils.newbie_stage_utils import get_npc_mecha_init_dict_by_type
        mecha_init_dict = get_npc_mecha_init_dict_by_type(mecha_dict.get('mecha_type'), robot_id, mecha_dict.get('pos'), mecha_dict.get('hp'), mecha_dict.get('shield'))
        mecha_obj = self.lbs_add_entity('Mecha', mecha_init_dict)
        seat = mecha_obj.logic.ev_g_driver_seat()
        mecha_obj.logic.send_event('E_ADD_PASSENGER', robot_id, seat)
        mecha_obj.logic.send_event('E_FORCE_AGENT')
        shoot = mecha_dict.get('shoot', False)
        self._local_npcs[mecha_obj.id] = {'guide_id': guide_id,
           'interval': interval,
           'shoot': shoot,
           'driver_id': robot.id,
           'id': mecha_obj.id,
           'shoot_interval': mecha_dict.get('shoot_interval', 0),
           'shoot_delay': mecha_dict.get('shoot_delay', 0),
           'created_time': tutil.get_time()
           }
        if shoot:
            self.resume_attack()

    def tick(self):
        timestamp = tutil.get_time()
        if not self.is_allow_attack():
            return
        self._last_tick_time = timestamp
        for mecha_id in self._local_npcs:
            mecha = EntityManager.getentity(mecha_id)
            robot_data = self._local_npcs[mecha_id]
            robot = EntityManager.getentity(robot_data.get('driver_id'))
            shoot = robot_data.get('shoot', False)
            if mecha and robot and shoot:
                self.do_shoot(mecha, robot, robot_data)

    def do_shoot(self, mecha, robot, robot_data):
        local_robot_last_shoot = robot_data.get('local_robot_last_shoot', 0)
        shoot_interval = robot_data.get('shoot_interval', 0)
        shoot_delay = robot_data.get('shoot_delay', 0)
        created_time = robot_data.get('created_time', 0)
        if shoot_delay > 0 and tutil.get_time() - created_time < shoot_delay:
            return
        else:
            if local_robot_last_shoot and 0 < tutil.get_time() - local_robot_last_shoot < shoot_interval:
                mecha and mecha.logic and mecha.logic.send_event('E_CTRL_ACTION_STOP', ai_const.CTRL_ACTION_MAIN)
                return
            wp = mecha.logic.ev_g_wpbar_cur_weapon()
            if wp is None:
                return
            wp.set_bullet_num(20)
            if mecha.logic.sd.ref_aim_target is None:
                target = global_data.player.logic.ev_g_bind_mecha_entity()
                in_mecha = global_data.player.logic.ev_g_in_mecha('Mecha')
                if in_mecha and target:
                    mecha.logic.send_event('E_ATK_TARGET', target.logic)
                else:
                    mecha.logic.send_event('E_ATK_TARGET', global_data.player.logic)
            t_pos = mecha.logic.ev_g_position()
            m_pos = self.lbs_get_value('G_POSITION')
            start_pos = t_pos + math3d.vector(0, 20, 0)
            end_pos = m_pos + math3d.vector(0, 20, 0)
            if self.lbs_is_hit(start_pos, end_pos):
                return
            robot_data['local_robot_last_shoot'] = tutil.get_time()
            lst_from = (
             t_pos.x, t_pos.y, t_pos.z)
            parameters = (800102, 20, 0, robot.id, lst_from, None, None)
            method_name = idx_utils.s_method_2_idx('on_hit_bomb')
            self.lbs_send_event('E_DO_SYNC_METHOD', method_name, parameters)
            mecha.logic.send_event('E_CTRL_ACTION_START', ai_const.CTRL_ACTION_MAIN, global_data.player.id, (end_pos.x, end_pos.y, end_pos.z), False)
            mecha.logic.send_event('E_CTRL_FACE_TO', end_pos)
            self.lbs_player_damage()
            return

    def on_hurt(self, robot_id, damage):
        if robot_id not in self._local_npcs:
            return
        mecha = EntityManager.getentity(robot_id)
        data = self._local_npcs[robot_id]
        if mecha:
            shield = mecha.logic.ev_g_shield()
            if shield > 0:
                mecha.logic.send_event('E_SET_SHIELD', shield - damage)
            elif mecha.logic.ev_g_hp() > 0:
                mecha.logic.ev_g_damage(damage)
                if mecha.logic.ev_g_hp() <= 0:
                    self.pause_attack()
                    if data.get('driver_id'):
                        self._destroy_robot(data['driver_id'])
                    self.delay_exec_destroy_ai(2, data)
                    ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
                    if ui:
                        ui._handle_death_event(FIGHT_EVENT_MECHA_DEATH)
            shoot_delay = data.get('shoot_delay', 0)
            if shoot_delay > 0:
                data['shoot_delay'] = 0

    def _destroy_robot(self, robot_id):
        robot = EntityManager.getentity(robot_id)
        if robot:
            self._local_battle.destroy_entity(robot.id)

    def destroy_all_npc(self):
        super(RobotMechaMgr, self).destroy_all_npc()
        if self._shoot_delay_timer:
            global_data.game_mgr.unregister_logic_timer(self._shoot_delay_timer)
            self._shoot_delay_timer = None
        return


class RobotMgr(FightNPCMgrBase):

    def __init__(self, lbs, local_battle):
        super(RobotMgr, self).__init__(lbs, local_battle)

    def tick(self):
        timestamp = tutil.get_time()
        if not self.is_allow_attack():
            return
        self._last_tick_time = timestamp
        for robot_id in self._local_npcs:
            robot_data = self._local_npcs[robot_id]
            robot = EntityManager.getentity(robot_id)
            shoot = robot_data.get('shoot', False)
            if robot and shoot:
                self.do_shoot(robot, robot_data)

    def add_robot(self, guide_id, interval, pos, max_hp, shoot, role_id, eagle_flag):
        robot_init_dict = {'max_hp': max_hp,'is_robot': True,
           'char_name': 'guide_robot',
           'weapons': {},'position': pos,
           'parachute_mecha_id': 8002,
           'faction_id': 1,
           'aim_y': 1.0,
           'role_id': role_id,
           'fashion': {'0': int('20100{}00'.format(role_id))}}
        robot = self.lbs_add_entity('Puppet', robot_init_dict)
        item_data = {'item_id': 10011,'entity_id': IdManager.genid(),'count': 1}
        robot.logic.send_event('E_PICK_UP_WEAPON', item_data, -1)
        robot.logic.send_event('E_SWITCHING', 1)
        wp = robot.logic.ev_g_wpbar_cur_weapon()
        bullet_cap = wp.get_bullet_cap()
        wp.set_bullet_num(bullet_cap)
        robot.logic.send_event('E_FORCE_AGENT')
        robot.logic.send_event('E_SET_CONTROL_TARGET', None, {'from_on_land': 1,'use_phys': 1})
        self._local_npcs[robot.id] = {'guide_id': guide_id,'interval': interval,'shoot': shoot,'id': robot.id}
        if eagle_flag:
            robot.logic.send_event('E_ADD_EAGLE_FLAG', robot.id, 'gift', False)
        if shoot:
            self.resume_attack()
        return

    def do_shoot(self, robot, robot_data):
        shoot_break = robot_data.get('shoot_break', 0)
        if shoot_break > 25:
            shoot_break = 0
        if shoot_break == 0:
            self.change_robot_attack(robot, True)
        shoot_break += 1
        robot_data['shoot_break'] = shoot_break
        if shoot_break > 2:
            self.change_robot_attack(robot, False)
            return
        else:
            if not robot:
                return
            wp = robot.logic.ev_g_wpbar_cur_weapon()
            if wp is None:
                return
            num = wp.get_bullet_num()
            local_robot_reload = robot_data.get('local_robot_reload', 0)
            if num <= 0:
                if local_robot_reload == 0:
                    robot.logic.send_event('E_TRY_RELOAD')
                    local_robot_reload += 0.2
                else:
                    local_robot_reload += 0.2
                    if local_robot_reload > 3:
                        local_robot_reload = 0
                        wp = robot.logic.ev_g_wpbar_cur_weapon()
                        bullet_cap = wp.get_bullet_cap()
                        wp.set_bullet_num(bullet_cap)
                robot_data['local_robot_reload'] = local_robot_reload
                return
            wp.set_bullet_num(num - 1)
            if robot.logic.sd.ref_aim_target is None:
                mecha = global_data.player.logic.ev_g_bind_mecha_entity()
                in_mecha = global_data.player.logic.ev_g_in_mecha('Mecha')
                if in_mecha and mecha:
                    robot.logic.send_event('E_ATK_TARGET', mecha.logic)
                else:
                    robot.logic.send_event('E_ATK_TARGET', global_data.player.logic)
            t_pos = robot.logic.ev_g_position()
            m_pos = self.lbs_get_value('G_POSITION')
            start_pos = t_pos + math3d.vector(0, 20, 0)
            end_pos = m_pos + math3d.vector(0, 20, 0)
            if self.lbs_is_hit(start_pos, end_pos):
                return
            st_target = v3d_to_tp(start_pos)
            lst_from = v3d_to_tp(t_pos)
            dmg_parts = {1: (1, 20)
               }
            parameters = (
             10011, dmg_parts, 0, st_target, lst_from, robot.id)
            method_name = idx_utils.s_method_2_idx('on_hit_shoot')
            self.lbs_send_event('E_DO_SYNC_METHOD', method_name, parameters)
            robot.logic.send_event('E_CTRL_FACE_TO', end_pos)
            self.lbs_player_damage()
            return

    def change_robot_attack(self, robot, is_attack):
        if robot and robot.logic and robot.logic.is_valid():
            if is_attack:
                robot.logic.send_event('E_GUN_ATTACK')
                robot.logic.send_event('E_ATTACK_START')
            else:
                robot.logic.send_event('E_ATTACK_END')

    def on_hurt(self, robot_id, damage):
        if robot_id not in self._local_npcs:
            return
        data = self._local_npcs[robot_id]
        robot = EntityManager.getentity(robot_id)
        if robot and robot.logic.ev_g_hp() > 0:
            robot.logic.ev_g_damage(damage)
            if robot.logic.ev_g_hp() <= 0:
                robot.logic.send_event('T_DEATH', global_data.player.id)
                self.delay_exec_destroy_ai(1, data)
                self.destroy_npc(robot_id)
                ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
                if ui:
                    ui._handle_death_event(FIGHT_EVENT_DEATH)


class ItemNPCMgr(NPCMgr):

    def __init__(self, lbs, local_battle):
        super(ItemNPCMgr, self).__init__(lbs, local_battle)
        self._local_picked_items = {}
        self._local_target_pick_items = {}
        self._box_sub_item_2_id = {}

    def add_items(self, guide_id, item_list):
        for item_info in item_list:
            item_id = item_info['item_id']
            count = item_info.get('count', 1)
            item_obj = self.lbs_add_entity('Item', item_info)
            self._local_npcs[item_obj.id] = {'item_obj': item_obj,
               'guide_id': guide_id,
               'item_id': item_id,
               'count': count
               }
            self._local_target_pick_items.setdefault(item_id, 0)
            self._local_target_pick_items[item_id] += count

    def add_box_item(self, guide_id, item_no, pos, sub_items):
        item_init_dict = {'item_id': item_no,
           'count': 1,
           'position': pos
           }
        all_item = {}
        for sub_item_no, cnt in six.iteritems(sub_items):
            eid = IdManager.genid()
            all_item[eid] = {'item_id': sub_item_no,'count': cnt}

        if all_item:
            item_init_dict['all_item'] = all_item
        pick_item = self.lbs_add_entity('Item', item_init_dict)
        for eid in six.iterkeys(all_item):
            self._box_sub_item_2_id[eid] = pick_item.id

        self._local_npcs[pick_item.id] = {'item_obj': pick_item,'guide_id': guide_id,'is_box': True,'item_id': item_no}

    def destroy_item(self):
        npc_ids = six_ex.keys(self._local_npcs)
        for npc_id in npc_ids:
            item_data = self._local_npcs[npc_id]
            if item_data.get('is_box', False):
                continue
            self.destroy_npc(npc_id)

    def destroy_box_item(self):
        npc_ids = six_ex.keys(self._local_npcs)
        for npc_id in npc_ids:
            item_data = self._local_npcs[npc_id]
            if item_data.get('is_box', False):
                self.destroy_npc(npc_id)

    def destroy_all_npc(self):
        super(ItemNPCMgr, self).destroy_all_npc()
        self._local_picked_items = {}
        self._local_target_pick_items = {}
        self._box_sub_item_2_id = {}

    def pick_item(self, item_entity_id, package_part=None, put_pos=-1, house_entity_id=None, parent_eid=None, throw_pos=None, area_id=-1):
        item_eid = IdManager.str2id(item_entity_id)
        if item_eid in self._box_sub_item_2_id:
            box_id = self._box_sub_item_2_id[item_eid]
            pick_item = EntityManager.getentity(box_id)
            pick_item_data = self._local_npcs.get(box_id, None)
            if not pick_item or not pick_item_data:
                return
            self.pick_box_item(item_entity_id, package_part, put_pos, house_entity_id, parent_eid, throw_pos, area_id)
        else:
            pick_item_data = self._local_npcs.get(item_eid, None)
            if not pick_item_data:
                return
            pick_item = EntityManager.getentity(item_eid)
            if not pick_item:
                return
            self.pick_normal_item(item_entity_id, package_part, put_pos, house_entity_id, parent_eid, throw_pos, area_id)
        return

    def pick_normal_item(self, item_entity_id, package_part=None, put_pos=-1, house_entity_id=None, parent_eid=None, throw_pos=None, area_id=-1):
        lplayer = global_data.player.logic
        pick_item_data = self._local_npcs.get(item_entity_id, None)
        item_eid = IdManager.str2id(item_entity_id)
        item_obj = pick_item_data.get('item_obj')
        guide_id = pick_item_data.get('guide_id')
        if not item_obj or not item_obj.logic:
            return
        else:
            item_data = item_obj.logic.ev_g_pick_data()
            if not item_data:
                return
            item_id = item_data.get('item_id')
            self._local_picked_items.setdefault(item_id, 0)
            if is_weapon(item_id):
                from logic.gcommon import const
                if put_pos >= 0:
                    if put_pos in [const.PART_WEAPON_POS_MAIN1, const.PART_WEAPON_POS_MAIN2, const.PART_WEAPON_POS_MAIN3]:
                        throw_weapon_data = global_data.player.logic.ev_g_weapon_data(put_pos)
                        throw_pos_vec = global_data.player.logic.ev_g_position()
                        new_weapon_data = {'item_id': throw_weapon_data.get('item_id'),
                           'count': 1,
                           'position': [
                                      throw_pos_vec.x, throw_pos_vec.y, throw_pos_vec.z]
                           }
                        item_obj = self.lbs_add_entity('Item', new_weapon_data)
                        self._local_npcs[item_obj.id] = {'item_obj': item_obj,'guide_id': -1}
                    iMagSize = confmgr.get('firearm_config', str(item_id), default={}).get('iMagSize', 0)
                    weapon_data = {'item_id': item_id,
                       'entity_id': item_eid,
                       'count': item_data.get('count'),
                       'iBulletNum': iMagSize
                       }
                    self.lbs_send_event('E_PICK_UP_WEAPON', weapon_data, put_pos)
                    self.lbs_send_event('E_GUIDE_PICK_WEAPON', guide_id, item_id)
                    self._local_picked_items[item_id] += item_data.get('count', 1)
                    self.check_send_specific_items_event(guide_id, self._local_target_pick_items)
                    self.destroy_npc(item_eid)
                else:
                    if lplayer.ev_g_weapon_data(const.PART_WEAPON_POS_MAIN1) == None:
                        real_put_pos = const.PART_WEAPON_POS_MAIN1
                    elif lplayer.ev_g_weapon_data(const.PART_WEAPON_POS_MAIN2) == None:
                        real_put_pos = const.PART_WEAPON_POS_MAIN2
                    elif lplayer.ev_g_weapon_data(const.PART_WEAPON_POS_MAIN3) == None:
                        real_put_pos = const.PART_WEAPON_POS_MAIN3
                    else:
                        real_put_pos = -1
                    if real_put_pos != -1:
                        iMagSize = confmgr.get('firearm_config', str(item_id), default={}).get('iMagSize', 0)
                        weapon_data = {'item_id': item_id,
                           'entity_id': item_eid,
                           'count': item_data.get('count'),
                           'iBulletNum': iMagSize
                           }
                        self.lbs_send_event('E_PICK_UP_WEAPON', weapon_data, put_pos)
                        self.lbs_send_event('E_GUIDE_PICK_WEAPON', guide_id, item_id)
                        self._local_picked_items[item_id] += item_data.get('count', 1)
                        self.check_send_specific_items_event(guide_id, self._local_target_pick_items)
                        self.destroy_npc(item_eid)
                cur_wp_pos = lplayer.share_data.ref_wp_bar_cur_pos
                weapons = lplayer.ev_g_all_weapons() or {}
                if cur_wp_pos == const.PART_WEAPON_POS_MAIN_DF and lplayer.ev_g_weapon_data(const.PART_WEAPON_POS_MAIN1) and len(weapons) == 2:
                    lplayer.send_event('E_SWITCHING', const.PART_WEAPON_POS_MAIN1)
            else:
                other_item_data = {'item_id': item_id,
                   'entity_id': item_eid,
                   'count': item_data.get('count')
                   }
                self.lbs_send_event('E_PICK_UP_OTHERS', other_item_data)
                self.lbs_send_event('E_GUIDE_PICK_OTHER_ITEM', guide_id, item_id)
                self._local_picked_items[item_id] += item_data.get('count', 1)
                self.check_send_specific_items_event(guide_id, self._local_target_pick_items)
                self.destroy_npc(item_eid)
            return

    def pick_box_item(self, item_entity_id, package_part=None, put_pos=-1, house_entity_id=None, parent_eid=None, throw_pos=None, area_id=-1):
        lplayer = global_data.player.logic
        item_id = IdManager.str2id(item_entity_id)
        box_id = self._box_sub_item_2_id.get(item_id)
        pick_item_data = self._local_npcs.get(box_id, None)
        pick_item = EntityManager.getentity(box_id)
        if not pick_item or not pick_item_data:
            return
        else:
            conf = pick_item.logic.ev_g_pick_data()
            if item_id in conf['all_item']:
                info = conf['all_item'][item_id]
                item_data = {'item_id': info['item_id'],'entity_id': item_id,'count': info['count']}
                if is_weapon(info['item_id']):
                    iMagSize = confmgr.get('firearm_config', str(info['item_id']))['iMagSize']
                    item_data['iBulletNum'] = iMagSize
                    put_pos = lplayer.ev_g_weapon_put_pos_by_replace_same(item_data, True) or -1
                    self.lbs_send_event('E_PICK_UP_WEAPON', item_data, put_pos)
                else:
                    self.lbs_send_event('E_PICK_UP_OTHERS', item_data)
                pick_item.logic.send_event('E_REMOVE_CHILD_ITEM', item_id)
                if item_id in self._box_sub_item_2_id:
                    del self._box_sub_item_2_id[item_id]
                conf = pick_item.logic.ev_g_pick_data()
                if not conf['all_item']:
                    self.lbs_send_event('E_GUIDE_PICK_END', pick_item_data.get('guide_id', 0))
                    if pick_item_data.get('item_id', 0) > 0 and item_utils.is_scene_box(pick_item_data.get('item_id', 0)):
                        pick_item.logic.send_event('E_SCENE_BOX_STAT_CHANGE', SCENEBOX_ST_OPENED)
                    else:
                        self.destroy_npc(box_id)
            return

    def check_send_specific_items_event(self, guide_id, target_item_dict=None):
        if not target_item_dict:
            return
        for item_id in target_item_dict:
            if target_item_dict[item_id] != self._local_picked_items.get(item_id, -1):
                return

        self._local_picked_items = {}
        self._local_target_pick_items = {}
        self.lbs_send_event('E_GUIDE_PICKED_SPECIFIC_ITEMS', guide_id)


class LocalBattleNPCMgr(object):

    def __init__(self, lbs, local_battle):
        self._server = lbs
        self._local_battle = local_battle
        self._robot_mgr = RobotMgr(lbs, local_battle)
        self._robot_mecha_mgr = RobotMechaMgr(lbs, local_battle)
        self._item_mgr = ItemNPCMgr(lbs, local_battle)

    def add_robot_mecha(self, guide_id, interval, mecha_dict):
        self._robot_mecha_mgr.add_robot_mecha(guide_id, interval, mecha_dict)

    def add_robot(self, guide_id, interval, pos, max_hp, shoot, role_id, eagle_flag):
        self._robot_mgr.add_robot(guide_id, interval, pos, max_hp, shoot, role_id, eagle_flag)

    def on_npc_hurt(self, npc_id, damage):
        self._robot_mgr.on_hurt(npc_id, damage)
        self._robot_mecha_mgr.on_hurt(npc_id, damage)

    def add_items(self, guide_id, item_list):
        self._item_mgr.add_items(guide_id, item_list)

    def add_box_item(self, guide_id, item_no, pos, sub_items):
        self._item_mgr.add_box_item(guide_id, item_no, pos, sub_items)

    def destroy_item(self):
        self._item_mgr.destroy_item()

    def destroy_box_item(self):
        self._item_mgr.destroy_box_item()

    def pick_item(self, item_entity_id, package_part=None, put_pos=-1, house_entity_id=None, parent_eid=None, throw_pos=None, area_id=-1):
        self._item_mgr.pick_item(item_entity_id, package_part, put_pos, house_entity_id, parent_eid, throw_pos, area_id)

    def destroy_all(self):
        self._robot_mgr.destroy_all_npc()
        self._robot_mecha_mgr.destroy_all_npc()
        self._item_mgr.destroy_all_npc()

    def get_all_attack_npc_ids(self):
        npc_ids = []
        npc_ids.extend(self._robot_mgr.get_all_npc_ids())
        npc_ids.extend(self._robot_mecha_mgr.get_all_npc_ids())
        return npc_ids