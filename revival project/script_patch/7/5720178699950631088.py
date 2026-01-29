# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/NewbieThirdLocalBattleServer.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from logic.entities.LocalBattleServer import LocalBattleServer, merge_sync_handler_dict
from common.cfg import confmgr
from logic.client.const.game_mode_const import NEWBIE_STAGE_THIRD_BATTLE_TYPE
from logic.gcommon import time_utility as tutil
from data.newbie_stage_config import GetBornPointConfig
from mobile.common.IdManager import IdManager
import math3d
import collision
from logic.gcommon.const import BACKPACK_PART_OTHERS, PART_WEAPON_POS_MAIN_DF
from logic.gcommon.common_const import mecha_const
from logic.gutils.newbie_stage_utils import get_npc_mecha_trans_init_dict_by_type, get_npc_building_init_dict_by_type, get_self_mecha_init_dict_by_type, get_newbie_stage_local_damage, get_npc_robot_init_dict_by_role_type
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_utils.math3d_utils import tp_to_v3d, v3d_to_tp
from logic.gcommon.common_utils import idx_utils
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, TERRAIN_MASK, REGION_SCENE_GROUP
from common.utils.timer import CLOCK
from logic.gcommon.common_const import vehicle_const

class NewbieThirdLocalBattleServer(LocalBattleServer):
    SYNC_BATTLE_HANDLER = merge_sync_handler_dict(LocalBattleServer.SYNC_BATTLE_HANDLER, {'pick_obj': '_lbs_pick_obj',
       'item_use_try': '_lbs_item_use_try',
       'item_use_do': '_lbs_item_use_do',
       'item_use_cancel': '_lbs_item_use_cancel',
       'on_wpbar_switch': '_lbs_on_wpbar_switch',
       'create_mecha': '_lbs_create_mecha',
       'try_join_mecha': '_lbs_try_join_mecha',
       'try_leave_mecha': '_lbs_try_leave_mecha',
       'try_recall': '_lbs_try_recall',
       'reloaded': '_lbs_reloaded',
       'do_shoot': '_lbs_do_shoot',
       'try_attach': '_lbs_try_attach',
       'try_detach': '_lbs_try_detach',
       'try_mecha_transform': '_lbs_try_mecha_transform',
       'do_skill': '_lbs_do_skill',
       'try_use_jump_building': '_lbs_try_use_jump_building',
       'change_vehicle_data': '_lbs_change_vehicle_data',
       'vehicle_syn_transform': '_lbs_vehicle_syn_transform'
       })
    ITEM_USE_HANDLER = {1666: 'on_use_skateboard_card',
       1667: 'on_use_chicken_card'
       }
    DO_SKILL_HANDLER = {850151: 'on_chicken_dash'
       }
    MAX_ROBOT_SHOOT_BREAK = 25

    def init_from_dict(self, bdict):
        super(NewbieThirdLocalBattleServer, self).init_from_dict(bdict)
        self.battle_type = NEWBIE_STAGE_THIRD_BATTLE_TYPE
        self.items_on_ground = {}
        self.skateboard_pos_on_ground = []
        self.chicken_pos_on_ground = []
        self.robots_in_battle = {}
        self.robot_shoot_break = 0
        self.robot_shoot_timer = None
        self.robot_is_alive = True
        self.super_jump_end_timer = None
        self.disable_join_vehicle = False
        return

    def destroy(self):
        self.stop_robot_shoot()
        self.stop_super_jump_end()
        super(NewbieThirdLocalBattleServer, self).destroy()

    def get_client_dict(self):
        battle_config = confmgr.get('battle_config')
        map_config = confmgr.get('map_config')
        battle_info = battle_config[str(self.battle_type)]
        map_id = battle_info['iMapID']
        cdict = {'battle_type': self.battle_type,
           'battle_data': battle_info,
           'map_data': map_config[str(map_id)],
           'map_id': map_id,
           'player_num': 99,
           'prepare_timestamp': tutil.time(),
           'view_position': GetBornPointConfig().get(self.battle_type, {}).get('born_point', [0, 290, 0]),
           'view_range': 1000
           }
        return cdict

    def get_player_init_dict(self):
        from logic.gcommon.common_const.skill_const import SKILL_ROLL
        info = {'position': GetBornPointConfig().get(self.battle_type, {}).get('born_point', [0, 290, 0]),
           'role_id': global_data.player.get_role(),
           'skills': {SKILL_ROLL: {'last_cast_time': 0,'inc_mp': 10.0,'mp': 150.0,'left_cast_cnt': 999999}},'mp_attr': {'human_yaw': GetBornPointConfig().get(self.battle_type, {}).get('human_yaw', 0)
                       },
           'mecha_dict': {8001: {'fashion': {'0': 201800100},'custom_skin': {},'sfx': 203800000},8005: {'fashion': {'0': 201800500},'custom_skin': {},'sfx': 203800000},8006: {'fashion': {'0': 201800600},'custom_skin': {},'sfx': 203800000}},'recall_cd_type': mecha_const.RECALL_CD_TYPE_GETMECHA,
           'fashion': {'0': int('20100{}00'.format(global_data.player.get_role()))}}
        return info

    def on_quit_battle(self, *args):
        self.destroy_robots_in_battle()
        if global_data.player:
            global_data.player.quit_new_local_battle()

    def destroy_robots_in_battle(self):
        if not self.local_battle:
            return
        for robot_id in six_ex.keys(self.robots_in_battle):
            self.local_battle.destroy_entity(robot_id)

        self.robots_in_battle = {}

    def create_items(self, guide_id, item_list):
        for item_info in item_list:
            item_obj = self._lbs_add_entity('Item', item_info)
            self.items_on_ground[item_obj.id] = {'item_obj': item_obj,'guide_id': guide_id}

    def create_building(self, building_type, extra_dict):
        extra_dict.update({'birthtime': tutil.get_server_time()
           })
        building_init_dict = get_npc_building_init_dict_by_type(building_type, extra_dict)
        self._lbs_add_entity('Building', building_init_dict)

    def create_robot(self, guide_id, robot_dict):
        role_id = robot_dict.get('role_id', 12)
        pos = robot_dict.get('position', [])
        max_hp = robot_dict.get('max_hp', 200)
        shoot = robot_dict.get('shoot', False)
        init_dict = get_npc_robot_init_dict_by_role_type(role_id, pos, max_hp)
        robot = self._lbs_add_entity('Puppet', init_dict)
        item_data = {'item_id': 10011,'entity_id': IdManager.genid(),'count': 1}
        robot.logic.send_event('E_PICK_UP_WEAPON', item_data, -1)
        robot.logic.send_event('E_SWITCHING', 1)
        wp = robot.logic.ev_g_wpbar_cur_weapon()
        bullet_cap = wp.get_bullet_cap()
        wp.set_bullet_num(bullet_cap)
        robot.logic.send_event('E_FORCE_AGENT')
        robot.logic.send_event('E_SET_CONTROL_TARGET', None, {'from_on_land': 1,'use_phys': 1})
        self.robots_in_battle[robot.id] = guide_id
        if shoot:
            self.start_robot_shoot(robot)
        self.robot_is_alive = True
        return

    def get_one_robot(self):
        for robot_id, _ in six.iteritems(self.robots_in_battle):
            robot = EntityManager.getentity(robot_id)
            if robot:
                return robot

        return None

    def get_skateboard_pos_on_ground(self):
        return self.skateboard_pos_on_ground

    def get_chicken_pos_on_ground(self):
        return self.chicken_pos_on_ground

    def _lbs_pick_obj(self, item_entity_id, package_part=None, put_pos=-1, house_entity_id=None, parent_eid=None, throw_pos=None, area_id=-1):
        if not self.items_on_ground:
            return
        else:
            item_eid = IdManager.str2id(item_entity_id)
            item_obj = self.items_on_ground.get(item_eid, {}).get('item_obj', None)
            guide_id = self.items_on_ground.get(item_eid, {}).get('guide_id', None)
            if not item_obj or not item_obj.logic:
                return
            item_data = item_obj.logic.ev_g_pick_data()
            if not item_data:
                return
            item_id = item_data.get('item_id')
            pick_item_data = {'item_id': item_id,
               'entity_id': item_eid,
               'count': item_data.get('count', 1)
               }
            self._lbs_send_event('E_PICK_UP_OTHERS', pick_item_data)
            if item_eid in self.items_on_ground:
                del self.items_on_ground[item_eid]
            global_data.player.new_local_battle.destroy_entity(item_eid)
            self._lbs_send_event('E_GUIDE_ITEM_PICKED', guide_id, item_id)
            return

    def _lbs_item_use_try(self, item_id):
        self._lbs_send_event('E_ITEMUSE_TRY_RET', item_id, 1)

    def _lbs_item_use_cancel(self, item_id):
        self._lbs_send_event('E_ITEMUSE_CANCEL_RES', item_id)

    def _lbs_item_use_do(self, item_id, area_id=-1, extra_data=None):
        func_name = self.ITEM_USE_HANDLER.get(int(item_id))
        if not func_name:
            return
        func_obj = getattr(self, func_name)
        if not func_obj or not callable(func_obj):
            return
        func_obj(item_id)
        self._lbs_send_event('E_GUIDE_ITEM_USE_END', item_id)
        self._lbs_send_event('E_ITEMUSE_ON', item_id)
        item_list = global_data.player.logic.ev_g_itme_list_by_id(item_id)
        if not item_list:
            return
        for info in item_list:
            self._lbs_send_event('E_THROW_ITEM', BACKPACK_PART_OTHERS, info['entity_id'])

    def _lbs_try_attach(self, entity_id):
        global_data.player.new_local_battle.destroy_entity(entity_id)
        self.attach_skateboard()

    def _lbs_try_detach(self, entity_id, lst_pos, lst_rotation):
        self.robot_is_alive = False
        if not global_data.player or not global_data.player.logic:
            return
        broken = False
        atch_data = global_data.player.logic.ev_g_do_detach(entity_id, broken)
        if not atch_data:
            return
        attach_data = {'npc_id': atch_data.get('npc_id'),
           'atch_id': atch_data.get('atch_id'),
           'fashion': atch_data.get('fashion'),
           'hp': atch_data.get('hp'),
           'init_max_hp': atch_data.get('init_max_hp'),
           'max_hp': atch_data.get('max_hp'),
           'position': lst_pos,
           'rot': lst_rotation
           }
        self.skateboard_pos_on_ground = lst_pos
        self._lbs_send_event('E_GUIDE_TRY_DETACH_END')
        self._lbs_add_entity('Attachable', attach_data)

    def _lbs_create_mecha(self, mecha_id, pos, yaw=0, *args):
        self.disable_join_vehicle = True
        extra_dict = {'creator': global_data.player.id,
           'position': pos,
           'born_time': tutil.get_server_time(),
           'mp_attr': {'human_yaw': global_data.player.logic.ev_g_yaw()
                       }
           }
        init_dict = get_self_mecha_init_dict_by_type(mecha_id, extra_dict)
        mecha_obj = self._lbs_add_entity('Mecha', init_dict)
        seat = mecha_obj.logic.ev_g_driver_seat()
        self._lbs_try_join_mecha(mecha_obj.id, seat, False)
        self._lbs_send_event('E_RECALL_SUCESS', True)

    def _lbs_try_join_mecha(self, mecha_eid, seat, is_begin):
        mecha_obj = EntityManager.getentity(mecha_eid)
        if not mecha_obj:
            return
        mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        mecha_id = mecha_obj.logic.ev_g_mecha_id()
        mecha_type = mecha_conf.get(str(mecha_id)).get('mecha_type')
        if mecha_type == mecha_const.MECHA_TYPE_VEHICLE and self.disable_join_vehicle:
            return
        mecha_obj.logic.send_event('E_ADD_PASSENGER', global_data.player.id, 'seat_1')
        self._lbs_send_event('E_ON_JOIN_MECHA_START', mecha_eid, int(mecha_type), tutil.get_server_time(), mecha_obj.is_share(), {}, seat)
        if mecha_type == mecha_const.MECHA_TYPE_VEHICLE:
            self._lbs_send_event('E_GUIDE_JOIN_MECHA_END')
            self._lbs_send_event('E_GUIDE_REGIST_MECHA_DIVING_EVENT', mecha_obj.logic, True)
            self.clear_mecha_call_cd()
            self.recover_chicken_cam()
        else:
            self._lbs_send_event('E_GUIDE_REGIST_MECHA_DIVING_SHOW_TIP_EVENT', mecha_obj.logic, True)

    def _lbs_try_leave_mecha(self, off_point, delay_time):
        if not global_data.player or not global_data.player.logic:
            return
        is_chicken = False
        mecha_eid = global_data.player.logic.ev_g_ctrl_mecha()
        if not mecha_eid:
            control_target = global_data.player.logic.ev_g_control_target()
            if control_target and control_target.logic and control_target.logic.ev_g_is_mechatran():
                mecha_eid = control_target.id
                is_chicken = True
        mecha_obj = EntityManager.getentity(mecha_eid)
        if not mecha_obj:
            return
        mecha_obj.logic.send_event('E_REMOVE_PASSENGER', global_data.player.id)
        is_die = False
        if not off_point:
            position = mecha_obj.logic.get_value('G_POSITION')
            off_point = (position.x, position.y + 50, position.z)
        self._lbs_send_event('E_ON_LEAVE_MECHA_START', off_point, tutil.get_server_time(), is_die, mecha_obj.is_share())
        last_pos = global_data.player.logic.ev_g_last_weapon_pos()
        if not last_pos:
            last_pos = PART_WEAPON_POS_MAIN_DF
        self._lbs_send_event('E_SWITCHING', last_pos)
        if is_chicken:
            pos_on_ground_vec = mecha_obj.logic.get_value('G_POSITION')
            self.chicken_pos_on_ground = [pos_on_ground_vec.x, pos_on_ground_vec.y, pos_on_ground_vec.z]
            self._lbs_send_event('E_GUIDE_LEAVE_CHICKEN')
            self._lbs_send_event('E_GUIDE_REGIST_MECHA_DIVING_EVENT', mecha_obj.logic, False)
            self.clear_mecha_call_cd()

    def _lbs_try_mecha_transform(self, pattern):
        from logic.gcommon.common_const.mecha_const import MECHA_PATTERN_NORMAL, MECHA_PATTERN_VEHICLE
        evt = {MECHA_PATTERN_NORMAL: 'E_TRANSFORM_2_NORMAL',
           MECHA_PATTERN_VEHICLE: 'E_TRANSFORM_2_VEHICLE'
           }.get(pattern, None)
        if not evt:
            return
        else:
            control_target = global_data.player.logic.ev_g_control_target()
            if control_target and control_target.logic:
                control_target.logic.send_event(evt)
                control_target.logic.send_event('E_CHANGE_PATTERN', pattern)
                if pattern == MECHA_PATTERN_VEHICLE:
                    v3d_lin_spd = math3d.vector(0, 0, 0)
                    v3d_agl_spd = math3d.vector(0, 0, 0)
                    enable = True
                    new_player_id = global_data.player.id
                    control_target.logic.send_event('E_VEHICLE_ENABLE_PHYSX', enable, new_player_id, v3d_lin_spd, v3d_agl_spd)
            if pattern == MECHA_PATTERN_VEHICLE:
                self._lbs_send_event('E_GUIDE_TRANSFORM_2_VEHICLE')
            else:
                self._lbs_send_event('E_GUIDE_TRANSFORM_2_NORMAL')
            return

    def _lbs_do_skill(self, skill_id, skill_args=()):
        func_name = self.DO_SKILL_HANDLER.get(int(skill_id))
        if not func_name:
            return
        func_obj = getattr(self, func_name)
        if not func_obj or not callable(func_obj):
            return
        func_obj(skill_id, skill_args)

    def _lbs_try_use_jump_building(self, building_eid):
        if not global_data.player or not global_data.player.logic:
            return
        lplayer = global_data.player.logic
        building = EntityManager.getentity(IdManager.str2id(building_eid))
        if not building or not building.logic:
            return
        player_pos = lplayer.ev_g_position()
        building_pos = building.logic.ev_g_position()
        distance = (player_pos - building_pos).length
        if distance > 200:
            return
        building_no = building.logic.ev_g_building_no()
        building_args = confmgr.get('c_building_data', str(building_no), default={}).get('Args', {})
        jump_args = {}
        control_target = lplayer.ev_g_control_target()
        if not control_target or not control_target.logic:
            return
        ct_logic_name = control_target.logic.__class__.__name__
        if ct_logic_name == 'LAvatar':
            jump_args = building_args.get('avatar', {})
            attachable_id = global_data.player.logic.ev_g_attachable_entity_id()
            if attachable_id and 'skate' in building_args:
                jump_args = building_args.get('skate', {})
        elif ct_logic_name == 'LMecha':
            jump_args = building_args.get('mecha', {})
        elif ct_logic_name == 'LMechaTrans':
            jump_args = building_args.get('vehicle', {})
        control_target.logic.send_event('E_SUPER_JUMP', jump_args)
        self.start_super_jump_end()

    def _lbs_do_shoot(self, start=None, end=None, aim=None, scene_pellet=0, target_dict=None, scene_dict=None, shoot_mask=0, ext_dict=None, wp_pos=None, t_use=0):
        if not target_dict:
            return
        else:
            cur_weapon = global_data.player.logic.ev_g_wpbar_cur_weapon()
            weapon_id = None
            if cur_weapon:
                weapon_id = cur_weapon.get_item_id()
            else:
                if ext_dict:
                    weapon_id = ext_dict.get('bullet_type', None)
                if not weapon_id:
                    return
            for target_id, shoot_info in six.iteritems(target_dict):
                entity = EntityManager.getentity(target_id)
                if not entity or not entity.logic:
                    continue
                is_mecha_target = entity.logic.ev_g_in_mecha('Mecha')
                dmg_parts = {}
                damage = 0
                parts = shoot_info.get('parts', {})
                for part in parts:
                    dmg = get_newbie_stage_local_damage(weapon_id, is_mecha_target, part)
                    dmg_parts[part] = (1, dmg)
                    damage += dmg

                v3d_from = tp_to_v3d(start)
                v3d_target = tp_to_v3d(end)
                list_from = (v3d_from.x, v3d_from.y, v3d_from.z)
                list_target = (v3d_target.x, v3d_target.y, v3d_target.z)
                if damage <= 0:
                    return
                args = (weapon_id, dmg_parts, 0, list_target, list_from, global_data.player.id, None)
                method_name = idx_utils.s_method_2_idx('on_hit_shoot')
                entity.logic.send_event('E_DO_SYNC_METHOD', method_name, args)
                hp = entity.logic.ev_g_hp()
                if hp is None or hp <= 0:
                    return
                entity.logic.ev_g_damage(damage)
                new_hp = entity.logic.ev_g_hp()
                if new_hp is None or new_hp <= 0:
                    entity.logic.send_event('T_DEATH', global_data.player.id)
                if new_hp is None or new_hp <= 0:
                    ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
                    ui and ui._handle_death_event(battle_const.FIGHT_EVENT_DEATH)
                if new_hp is None or new_hp <= 0:
                    self._lbs_send_event('E_GUIDE_ROBOT_DEAD', self.robots_in_battle.get(target_id))
                    self.stop_robot_shoot()

            return

    def _lbs_on_wpbar_switch(self, cur_pos):
        if cur_pos == 0 and self.robot_is_alive:
            return
        self._lbs_send_event('E_SWITCHING', cur_pos)

    def _lbs_reloaded(self, reload_num, wp_pos=None, t_use=0):
        if wp_pos is None:
            wp_pos = global_data.player.logic.ev_g_wpbar_cur_weapon_pos()
        control_target = global_data.player.logic.ev_g_control_target()
        if not control_target or not control_target.logic:
            return
        else:
            wp = control_target.logic.ev_g_wpbar_cur_weapon()
            if not wp:
                return
            control_target.logic.send_event('E_WEAPON_BULLET_CHG', wp_pos, wp.get_bullet_cap())
            return

    def _lbs_change_vehicle_data(self, vehicle_info):
        method_name = idx_utils.s_method_2_idx('change_vehicle_data')
        self._lbs_send_event('E_DO_SYNC_METHOD', method_name, (vehicle_info,))

    def _lbs_vehicle_syn_transform(self, v_id, trans_info):
        if 'l_spd' in trans_info:
            trans_info.pop('l_spd')
        if 'a_spd' in trans_info:
            trans_info.pop('a_spd')
        info = {'change_type': vehicle_const.CH_VEHICLE_SPEED,'data': trans_info['speed'],
           'vid': v_id
           }
        method_name = idx_utils.s_method_2_idx('vehicle_syn_transform')
        self._lbs_send_event('E_DO_SYNC_METHOD', method_name, (v_id, trans_info))
        method_name = idx_utils.s_method_2_idx('change_vehicle_data')
        self._lbs_send_event('E_DO_SYNC_METHOD', method_name, (info,))

    def check_send_pick_item_event(self, guide_id, item_id):
        self._lbs_send_event('E_GUIDE_PICK_ITEM_EVENT', guide_id, item_id)

    def on_use_skateboard_card(self, item_id, *args):
        self.attach_skateboard()

    def attach_skateboard(self):
        attatch_data = {'npc_id': 6008,
           'entity_id': IdManager.genid(),
           'fashion': {u'0': 208200100},'hp': 300,
           'atch_id': 6008,
           'init_max_hp': 300,
           'max_hp': 300,
           'rot': [
                 0, 0, 0, 0]
           }
        if not global_data.player or not global_data.player.logic:
            return
        global_data.player.logic.ev_g_do_attach(attatch_data)

    def on_use_chicken_card(self, item_id, *args):
        if not global_data.player or not global_data.player.logic:
            return
        lplayer = global_data.player.logic
        default_mecha_id = 8501
        default_mecha_fashion = {'0': 208200200}
        player_pos_vec = lplayer.ev_g_position()
        mecha_pos_list = [player_pos_vec.x, player_pos_vec.y, player_pos_vec.z]
        extra_dict = {'creator': lplayer.id,
           'auto_join': True,
           'trans_pattern': mecha_const.MECHA_PATTERN_NORMAL,
           'shapeshift': mecha_const.VEHICLE_STATE_HUMAN,
           'mp_attr': {'mileage': 0,'arm_hit': 1.0,'foot_hit': 1.0,'head_hit': 1.5,'body_hit': 1.0,'item_num': 0,'human_yaw': lplayer.ev_g_yaw() or 0},'mecha_fashion': lplayer.ev_g_item_fashion(default_mecha_id) or default_mecha_fashion,
           'born_time': tutil.get_time(),
           'position': mecha_pos_list
           }
        mecha_init_dict = get_npc_mecha_trans_init_dict_by_type(default_mecha_id, extra_dict)
        self._lbs_add_entity('MechaTrans', mecha_init_dict)

    def on_chicken_dash(self, skill_id, skill_args):
        control_target = global_data.player.logic.ev_g_control_target()
        if control_target and control_target.logic:
            control_target.logic.send_event('E_MOD_SKILL_LEFT_CNT', skill_id, 1)
        self._lbs_send_event('E_GUIDE_CHICKEN_DASH')

    def start_robot_shoot(self, robot):
        if robot and not self.robot_shoot_timer:
            self.robot_shoot_timer = global_data.game_mgr.register_logic_timer(lambda shooter=robot: self.robot_shoot(shooter), interval=0.2, mode=CLOCK)
            self.robot_shoot_break = 0

    def robot_shoot(self, robot):
        if not robot or not robot.logic or not robot.logic.is_valid():
            return
        else:
            if self.robot_shoot_break > self.MAX_ROBOT_SHOOT_BREAK:
                self.robot_shoot_break = 0
            if self.robot_shoot_break == 0:
                robot.logic.send_event('E_GUN_ATTACK')
                robot.logic.send_event('E_ATTACK_START')
            self.robot_shoot_break += 1
            if self.robot_shoot_break >= 2:
                robot.logic.send_event('E_ATTACK_END')
                return
            wp = robot.logic.ev_g_wpbar_cur_weapon()
            if wp is None:
                return
            wp.set_bullet_num(20)
            if robot.logic.sd.ref_aim_target is None:
                control_target = global_data.player.logic.ev_g_control_target()
                robot.logic.send_event('E_ATK_TARGET', control_target.logic)
            from_pos = robot.logic.ev_g_position()
            to_pos = global_data.player.logic.ev_g_position()
            from_pos = from_pos + math3d.vector(0, 20, 0)
            to_pos = to_pos + math3d.vector(0, 20, 0)
            if self.is_hit(from_pos, to_pos):
                return
            robot.logic.send_event('E_CTRL_FACE_TO', to_pos)
            tpl_from_pos = v3d_to_tp(from_pos)
            tpl_to_pos = v3d_to_tp(to_pos)
            damage = get_newbie_stage_local_damage(10011, False, 1)
            print(damage)
            dmg_parts = {1: (
                 1, damage)
               }
            args = (
             10011, dmg_parts, 0, tpl_to_pos, tpl_from_pos, robot.id)
            method_name = idx_utils.s_method_2_idx('on_hit_shoot')
            self._lbs_send_event('E_DO_SYNC_METHOD', method_name, args)
            self.player_take_damage(damage)
            return

    def stop_robot_shoot(self):
        if self.robot_shoot_timer:
            global_data.game_mgr.unregister_logic_timer(self.robot_shoot_timer)
            self.robot_shoot_timer = None
        return

    def is_hit(self, start_pos, end_pos):
        hit_by_ray = global_data.game_mgr.scene.scene_col.hit_by_ray
        ret = hit_by_ray(start_pos, end_pos, 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, True)
        if ret and ret[0]:
            return True
        return False

    def player_take_damage(self, damage):
        mecha = global_data.player.logic.ev_g_bind_mecha_entity()
        if mecha:
            shield = mecha.logic.ev_g_shield()
            hp = mecha.logic.ev_g_hp()
            max_hp = mecha.logic.ev_g_max_hp()
            new_shield = 0 if damage >= shield else shield - damage
            mecha.logic.send_event('E_SET_SHIELD', new_shield)
            left_damage = damage - shield
            new_hp = hp - left_damage if left_damage > 0 else hp
            if new_hp >= max_hp * 0.3 and left_damage > 0:
                mecha.logic.ev_g_damage(damage)
        else:
            hp = global_data.player.logic.ev_g_hp()
            max_hp = global_data.player.logic.ev_g_max_hp()
            new_hp = hp - damage
            if new_hp >= max_hp * 0.3:
                print('player take damage ', damage)
                global_data.player.logic.ev_g_damage(damage)

    def start_super_jump_end(self):
        self.super_jump_end_timer = global_data.game_mgr.register_logic_timer(self.super_jump_end, times=1, interval=5, mode=CLOCK)

    def super_jump_end(self):
        if self:
            self._lbs_send_event('E_GUIDE_SUPER_JUMP_END')

    def stop_super_jump_end(self):
        if self.super_jump_end_timer:
            global_data.game_mgr.unregister_logic_timer(self.super_jump_end_timer)
            self.super_jump_end_timer = None
        return

    def clear_mecha_call_cd(self):
        ui = global_data.ui_mgr.get_ui('MechaUI')
        if ui:
            ui.clear_mecha_cd_timer()
            ui.on_add_mecha_progress(100)
            ui.get_mecha_count_down = 0
            ui.get_mecha_count_down_progress = 0

    def recover_chicken_cam(self):
        control_target = global_data.player.logic.ev_g_control_target()
        if not control_target or not control_target.logic:
            return
        new_yaw = control_target.logic.ev_g_yaw()
        global_data.emgr.fireEvent('camera_set_yaw_event', new_yaw)
        global_data.emgr.fireEvent('camera_set_pitch_event', 0)