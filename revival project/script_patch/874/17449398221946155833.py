# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impLocalBattleServer.py
from __future__ import absolute_import
import six
from logic.gcommon.const import BACKPACK_PART_OTHERS
import logic.gcommon.common_utils.idx_utils as idx_utils
from logic.gcommon.item.item_use_var_name_data import BANDAGE_ID
from logic.gcommon.item.item_utility import is_weapon
from logic.gcommon.common_const import mecha_const as mconst
from common.cfg import confmgr
from mobile.common.EntityFactory import EntityFactory
from mobile.common.IdManager import IdManager
import time
from logic.gcommon.common_const.battle_const import COMBAT_STATE_NONE, FIGHT_EVENT_DEATH, FIGHT_EVENT_MECHA_DEATH
from mobile.common.EntityManager import EntityManager
import collision
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE
from data.c_guide_data import get_init_guide_pos, get_local_damage, get_local_mecha_second_weapon_damage
from common.utils.time_utils import get_time
from logic.gcommon.time_utility import get_server_time
from logic.gcommon.common_utils.math3d_utils import tp_to_v3d
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, NEWBIE_STAGE_MECHA_BATTLE, NEWBIE_STAGE_HUMAN_BATTLE
from common.utils.timer import CLOCK
from logic.comsys.guide_ui.GuideSetting import GuideSetting
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int
from logic.gcommon.common_utils.math3d_utils import v3d_to_tp
from data.newbie_stage_config import GetBornPointConfig, GetWeaponDamage, GetViewRangeConfig, GetStageMechaHandler, GetStageHumanHandler
from logic.gcommon.common_const import ai_const
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gutils.item_utils import is_weapon_full
BARRIER_POLY = [
 math3d.vector(1, 0, 0),
 math3d.vector(0, 0, 1),
 math3d.vector(-1, 0, 0),
 math3d.vector(0, 0, -1)]

class impLocalBattleServer(object):
    rpc_to_handle = {'loaded_battle': '_lbs_loaded_battle',
       'quit_battle': '_lbs_quit_battle',
       'sync_battle': '_lbs_sync_battle',
       'sync_battle_time': '_lbs_sync_battle_time'
       }
    sync_battle_handle = {'pick_obj': '_lbs_pick_obj',
       'item_use_try': '_lbs_item_use_try',
       'item_use_do': '_lbs_item_use_do',
       'item_use_cancel': '_lbs_item_use_cancel',
       'on_wpbar_switch': '_lbs_on_wpbar_switch',
       'create_mecha': '_lbs_create_mecha',
       'try_join_mecha': '_lbs_try_join_mecha',
       'try_leave_mecha': '_lbs_try_leave_mecha',
       'try_recall': '_lbs_try_recall',
       'move_sync_all': '_lbs_move_sync_all',
       'reloaded': '_lbs_reloaded',
       'do_shoot': '_lbs_do_shoot',
       'do_skill': '_lbs_do_skill'
       }
    MECHA_RECALL_CD = 10

    def _init_localbattleserver_from_dict(self, bdict):
        self.local_aoi_id = 0
        self.local_barriers = []
        self._local_battle_data = None
        self.local_mecha = None
        self.local_battle = None
        self.local_robot = None
        self.local_robot_ai_timer = None
        self.local_robot_reload = 0
        self.local_pick_item = None
        self.local_items = {}
        self.local_picked_item_ids = set()
        self.local_robot_ai_timer_logic = None
        self.local_robot_ai_timer_delay = None
        self.local_robot_skill_hurt = -1
        self.local_robot_shoot_break = 0
        self._min_x = None
        self._max_x = None
        self._min_z = None
        self._max_z = None
        self.local_robot_mecha = None
        self.local_monster = None
        self.local_npc_mecha = None
        self.local_npc_mecha_driver = None
        self.need_eject_driver = False
        self.local_robot_mecha_shoot_timer = None
        self.local_robot_mecha_shoot_flag = True
        self.local_robot_mecha_shield_timer = None
        self.local_robot_mecha_shoot_break = 0
        self._assessment_tid = None
        self._no_mecha_damage_flag = False
        self.robot_move_points = []
        self.local_robot_move_timer = None
        return

    def set_assessment_tid(self, tid):
        self._assessment_tid = tid

    def get_assessment_tid(self):
        return self._assessment_tid

    def set_no_mecha_damage_flag(self, flag):
        self._no_mecha_damage_flag = flag

    def _destroy_localbattleserver(self):
        self.local_battle = None
        self.local_robot = None
        self.local_robot_mecha = None
        self.local_npc_mecha = None
        self.local_npc_mecha_driver = None
        self.need_eject_driver = False
        self.local_pick_item = None
        self.local_items = None
        self.local_picked_item_ids = None
        if self.local_robot_mecha_shield_timer:
            global_data.game_mgr.unregister_logic_timer(self.local_robot_mecha_shield_timer)
            self.local_robot_mecha_shield_timer = None
        return

    def get_available_npc_human(self):
        if self.local_robot:
            return self.local_robot[0]
        if self.local_npc_mecha_driver:
            return self.local_npc_mecha_driver[0]

    def get_available_npc_mecha(self):
        if self.local_robot_mecha:
            return self.local_robot_mecha[0]
        if self.local_npc_mecha:
            return self.local_npc_mecha[0]

    def get_local_robot_position(self):
        if self.local_robot[0] and self.local_robot[0].logic:
            pos_vec = self.local_robot[0].logic.ev_g_position()
            return [
             pos_vec.x, pos_vec.y, pos_vec.z]
        return []

    def get_local_npc_mecha_driver_position(self):
        if self.local_npc_mecha_driver[0] and self.local_npc_mecha_driver[0].logic:
            pos_vec = self.local_npc_mecha_driver[0].logic.ev_g_position()
            return [
             pos_vec.x, pos_vec.y, pos_vec.z]
        return []

    def try_start_local_battle(self, battle_type):
        if self.in_local_battle():
            self._start_local_battle(battle_type)
        elif battle_type in [NEWBIE_STAGE_HUMAN_BATTLE, NEWBIE_STAGE_MECHA_BATTLE]:
            self.call_server_method('try_start_local_battle', (battle_type,))
        else:
            self._start_local_battle(battle_type)

    @rpc_method(CLIENT_STUB, (Int('battle_type'),))
    def do_start_local_battle(self, battle_type):
        self._start_local_battle(battle_type)

    def _start_local_battle(self, battle_type):
        self.save_local_battle_data('_lbs_in_battle', 1)
        self.save_local_battle_data('_lbs_battle_type', battle_type)
        self._create_local_battle(battle_type)
        global_data.sound_mgr.delay_stop_music()

    def is_creator_local_battle(self):
        return False

    def get_lbs_battle_type(self):
        info = self._get_local_battle_data()
        return info.get('_lbs_battle_type')

    def has_finish_guide(self):
        info = self._get_local_battle_data()
        return info.get('_lbs_finish_guide', None)

    def _create_local_battle(self, battle_type):
        battle_config = confmgr.get('battle_config')
        map_config = confmgr.get('map_config')
        battle_info = battle_config[str(battle_type)]
        map_id = battle_info['iMapID']
        bdict = {'battle_type': battle_type,
           'battle_data': battle_info,
           'map_data': map_config[str(map_id)],
           'map_id': map_id,
           'player_num': 99,
           'prepare_timestamp': time.time() + 1000,
           'view_position': self.get_player_init_pos(battle_type),
           'view_range': GetViewRangeConfig().get(battle_type, {}).get('view_range', 500)
           }
        if self.local_battle:
            self.local_battle.destroy()
            self.local_battle = None
        battle = EntityFactory.instance().create_entity('LocalBattle', IdManager.genid())
        self.local_battle = battle
        battle.init_from_dict(bdict)
        return

    def get_local_battle(self):
        return self.local_battle

    def get_local_battle_init_dict(self):
        from logic.gcommon.common_const.skill_const import SKILL_ROLL
        if not global_data.battle:
            return
        battle_type = global_data.battle.get_battle_tid()
        info = {'position': self.get_player_init_pos(battle_type),
           'role_id': self.get_role(),
           'role_list': self.get_role_list(),
           'skills': {SKILL_ROLL: {'last_cast_time': 0,'inc_mp': 10.0,'mp': 150.0,'left_cast_cnt': 999999}},'group_id': 2,
           'faction_id': 2,
           'mp_attr': {'human_yaw': GetBornPointConfig().get(battle_type, {}).get('human_yaw', 0)
                       },
           'fashion': {'0': int('20100{}00'.format(global_data.player.get_role()))}}
        return info

    def get_local_aoi_id(self):
        self.local_aoi_id += 1
        return self.local_aoi_id

    def join_local_battle(self):
        self._lbs_create_death_doors()

    def clear_local_barrier(self):
        if self.local_barriers:
            for _, barrier in enumerate(self.local_barriers):
                global_data.game_mgr.scene.scene_col.remove_object(barrier)

            self.local_barriers = []
        if self.logic:
            mecha_id = self.logic.ev_g_ctrl_mecha()
            if mecha_id:
                mecha_obj = EntityManager.getentity(mecha_id)
                if mecha_obj:
                    self._lbs_send_event('E_GUIDE_POS_CHECK', mecha_obj.logic, False)

    def quit_local_battle(self):
        self._no_mecha_damage_flag = False
        self.clear_local_barrier()
        self._lbs_destroy_robot()
        if self.local_battle:
            self.local_battle.destroy()
            self.local_battle = None
        if self.lobby:
            self.lobby.init_from_dict({'is_login': False,'combat_state': COMBAT_STATE_NONE,'from_newbie_stage': True})
        return

    def _get_local_battle_data(self):
        try:
            if self._local_battle_data is None:
                self._local_battle_data = GuideSetting().local_battle_data
            return self._local_battle_data
        except:
            return GuideSetting().local_battle_data

        return

    def get_local_pos(self):
        info = self._get_local_battle_data()
        local_lbs_pos = info.get('_lbs_pos', None)
        if local_lbs_pos is None:
            return get_init_guide_pos(101)
        else:
            return local_lbs_pos

    def get_player_init_pos(self, battle_type):
        return GetBornPointConfig().get(battle_type, {}).get('born_point', [])

    def get_lbs_step(self):
        info = self._get_local_battle_data()
        return info.get('_lbs_step', None)

    def save_local_battle_data(self, key, value):
        info = self._get_local_battle_data()
        info[key] = value
        GuideSetting().local_battle_data = info

    def get_remote_battle_data(self):
        info = self._get_local_battle_data()
        return info.get('_lbs_remote_battle', None)

    def get_death_battle_data(self):
        info = self._get_local_battle_data()
        return info.get('_lbs_death_battle', None)

    def save_remote_battle_data(self, data):
        self.save_local_battle_data('_lbs_remote_battle', data)

    def save_death_battle_data(self, data):
        self.save_local_battle_data('_lbs_death_battle', data)

    def clear_local_battle_data(self):
        info = self._get_local_battle_data()
        battle_type = info.get('_lbs_battle_type', None)
        if battle_type and global_data.player and global_data.player.server:
            global_data.player.server.call_server_method('finish_local_battle', (battle_type, True), None, True)
        keys = [
         '_lbs_battle_type', '_lbs_in_battle', '_lbs_step', '_lbs_pos']
        for key in keys:
            if key in info:
                del info[key]

        GuideSetting().local_battle_data = info
        return

    def read_guide_data(self, name):
        info = self._get_local_battle_data()
        return info.get(name, None)

    def write_guide_data(self, name, value):
        self.save_local_battle_data(name, value)

    def handle_local_battle_rpc(self, method_name, params):
        handle_name = impLocalBattleServer.rpc_to_handle.get(method_name, None)
        if handle_name is None:
            return
        else:
            if isinstance(handle_name, str):
                handle_func = getattr(self, handle_name, None)
                if handle_func is None:
                    return
                handle_func(*params)
            return

    def _lbs_sync_battle(self, method_pack):
        if self.local_battle is None:
            return
        else:
            for sync_id, sync_method_pack in method_pack:
                for method_name, param in sync_method_pack:
                    method_name = idx_utils.s_idx_2_method_name(method_name)
                    handle_name = impLocalBattleServer.sync_battle_handle.get(method_name, None)
                    if handle_name is None:
                        continue
                    handle_func = getattr(self, handle_name, None)
                    if handle_func is None:
                        continue
                    handle_func(*param)

            return

    def _call_local_battle_rpc_method(self, method_name, params):
        method = getattr(self.local_battle, method_name, None)
        method(params)
        return

    def _lbs_send_event(self, evt, *args):
        if self.logic:
            self.logic.send_event(evt, *args)

    def _lbs_get_value(self, evt):
        if self.logic:
            return self.logic.get_value(evt)

    def _lbs_loaded_battle(self, *args):
        params = {'entity_id': self.id,
           'entity_aoi_id': self.get_local_aoi_id(),
           'entity_dict': self.get_local_battle_init_dict()
           }
        self.join_local_battle()
        if self.local_battle.entity_in_battle(self.id):
            return
        self._call_local_battle_rpc_method('add_entity', params)

    def _lbs_quit_battle(self, *_):
        self.quit_local_battle()
        self.clear_local_battle_data()

    def _call_rpc_method(self, method_name, params):
        method = getattr(self, method_name, None)
        method(params)
        return

    def _lbs_sync_battle_time(self, f_send, last_rtt):
        params = {'f_send': f_send,
           'f_stamp': f_send,
           'game_ver': 0
           }
        self._call_rpc_method('on_sync_battle_time', params)

    def _lbs_move_sync_all(self, timestamp, idx, lst_pos, lst_vel, acc, *args):
        pass

    def _lbs_save_pos(self):
        pos = self._lbs_get_value('G_POSITION')
        self.save_local_battle_data('_lbs_pos', (pos.x, pos.y, pos.z))

    def _lbs_reloaded(self, reload_num, wp_pos=None, t_use=0):
        if wp_pos is None:
            wp_pos = self._lbs_get_value('G_WPBAR_CUR_WEAPON_POS')
        mecha = self.logic.ev_g_bind_mecha_entity()
        if mecha:
            wp = mecha.logic.ev_g_wpbar_cur_weapon()
            mecha.logic.send_event('E_WEAPON_BULLET_CHG', wp_pos, wp.get_bullet_cap())
        else:
            wp = self._lbs_get_value('G_WPBAR_CUR_WEAPON')
            self._lbs_send_event('E_WEAPON_BULLET_CHG', wp_pos, wp.get_bullet_cap())
        return

    def _lbs_item_use_try(self, item_no):
        self._lbs_send_event('E_ITEMUSE_TRY_RET', item_no, 1)

    def _lbs_item_use_do(self, item_id, *_):
        if item_id == BANDAGE_ID:
            item_list = self.logic.ev_g_itme_list_by_id(item_id)
            if item_list:
                for info in item_list:
                    self._lbs_send_event('E_THROW_ITEM', BACKPACK_PART_OTHERS, info['entity_id'])

                self._lbs_send_event('E_ITEMUSE_ON', item_id)
                max_hp = self._lbs_get_value('G_MAX_HP')
                self._lbs_send_event('S_HP', max_hp)
                self._lbs_send_event('E_GUIDE_USE_END')

    def _lbs_item_use_cancel(self, item_id):
        self._lbs_send_event('E_ITEMUSE_CANCEL_RES', item_id)

    def _lbs_on_wpbar_switch(self, cur_pos):
        if cur_pos == 0:
            return
        self._lbs_send_event('E_SWITCHING', cur_pos)

    def _lbs_add_entity(self, entity_type, init_dict):
        entity_obj = EntityFactory.instance().create_entity(entity_type, IdManager.genid())
        entity_obj.init_from_dict(init_dict)
        params = {'entity_id': entity_obj.id,
           'entity_aoi_id': self.get_local_aoi_id(),
           'entity_dict': init_dict
           }
        self._call_local_battle_rpc_method('add_entity', params)
        return entity_obj

    def _lbs_create_death_doors(self):
        if not global_data.battle:
            return

    def _lbs_create_mecha_imp(self, mecha_type, pos):
        mecha_init_dict = {'mecha_id': mecha_type,
           'npc_id': mecha_type,
           'creator': self.id,
           'mecha_robot': False,
           'position': pos,
           'max_shield': confmgr.get('mecha_conf', 'ShieldConfig', 'Content', str(mecha_type), 'max_shield'),
           'seats': confmgr.get('mecha_conf', 'MechaConfig', 'Content', str(mecha_type), 'seats'),
           'init_max_hp': 2650,
           'shield': 600.0,
           'repair_energy': 60.0,
           'attachment_config': {9920: 1028,9912: 1008,9913: 1009,9914: 1002,9915: 1003,9916: 1005,9917: 1006,9918: 1025,
                                 9919: 1026},
           'weapons': {1: {'count': 1,'iBolted': 1,'iBulletNum': 80,'item_type': 0,'attachment': {},'item_id': 800101},2: {'item_id': 800102,'item_type': 0,'iBulletNum': 0,'attachment': {},'count': 1}},'wp_bar_cur_pos': 1,
           'trans_pattern': 1,
           'max_shield': 600.0,
           'max_hp': 2650,
           'hp': 2650,
           'skills': {800151: {'last_cast_time': 0,'inc_mp': 30.0,'mp': 100.0,'left_cast_cnt': 999999},800152: {'last_cast_time': 0,'inc_mp': 10.0,'mp': 80.0,'left_cast_cnt': 999999},800153: {'last_cast_time': 0,'inc_mp': 10.0,'mp': 80.0,'left_cast_cnt': 999999}},'module_config': (
                           (1011, 9908), (1030, 9908), (1031, 9909), (1012, 9911), (1010, 9911)),
           'all_valid_state': set([160, 128, 130, 132, 101, 105, 106, 107, 108, 109, 110, 111, 113, 114, 122, 123, 159]),
           'mp_attr': {'human_yaw': global_data.player.logic.ev_g_yaw()
                       }
           }
        mecha_obj = self._lbs_add_entity('Mecha', mecha_init_dict)
        seat = mecha_obj.logic.ev_g_driver_seat()
        self._lbs_send_event('E_ON_JOIN_MECHA_START', mecha_obj.id, 1, get_time(), False, None, seat)
        mecha_obj.logic.send_event('E_ADD_PASSENGER', self.id, seat)
        self._lbs_send_event('E_GUIDE_POS_CHECK', mecha_obj.logic, True)
        self._lbs_send_event('E_RECALL_SUCESS', True)
        self._lbs_send_event('E_STATE_CHANGE_CD', mconst.RECALL_CD_TYPE_NORMAL, self.MECHA_RECALL_CD, self.MECHA_RECALL_CD)
        ui = global_data.ui_mgr.get_ui('PostureControlUI')
        if ui:
            ui.panel.setVisible(False)
        self._lbs_send_event('E_GUIDE_JOIN_MECHA_END_2', mecha_obj.id)
        return mecha_obj

    def _lbs_create_mecha(self, mecha_type, pos, yaw=0, *args):
        if self.local_mecha is not None:
            return
        else:
            mecha_type = 8001
            mecha_obj = self._lbs_create_mecha_imp(mecha_type, pos)
            self.local_mecha = [mecha_type, mecha_obj]
            return

    def _lbs_destroy_mecha(self):
        if self.local_mecha:
            m_pos = self._lbs_get_value('G_POSITION')
            self._lbs_try_leave_mecha(m_pos, None, True)
            self.local_battle.destroy_entity(self.local_mecha[1].id)
            self.local_mecha = None
        return

    def _lbs_try_join_mecha(self, mecha_id, seat, is_begin):
        mecha_obj = EntityManager.getentity(mecha_id)
        if not mecha_obj:
            return
        self._lbs_send_event('E_ON_JOIN_MECHA_START', mecha_id, 1, get_time(), False)
        self._lbs_send_event('E_GUIDE_POS_CHECK', mecha_obj.logic, True)

    def _lbs_try_leave_mecha(self, pos, delay_time, is_destroy=False):
        mecha_id = self.logic.ev_g_ctrl_mecha()
        self._lbs_send_event('E_ON_LEAVE_MECHA_START', pos, get_server_time(), False, False)
        self._lbs_send_event('E_STATE_CHANGE_CD', mconst.RECALL_CD_TYPE_NORMAL, self.MECHA_RECALL_CD, self.MECHA_RECALL_CD)
        not is_destroy and self._lbs_send_event('E_SWITCHING', PART_WEAPON_POS_MAIN1)
        if mecha_id:
            mecha_obj = EntityManager.getentity(mecha_id)
            mecha_obj.logic.send_event('E_REMOVE_PASSENGER', self.id)
            self._lbs_send_event('E_GUIDE_POS_CHECK', mecha_obj.logic, False)
            global_data.game_mgr.register_logic_timer(lambda m_id=mecha_id: self.delay_destroy_self_mecha(m_id), times=1, interval=3, mode=CLOCK)
            ui = global_data.ui_mgr.get_ui('PostureControlUI')
            if ui:
                ui.panel.setVisible(True)

    def _lbs_try_recall(self, pos, yaw=0):
        if self.local_mecha is None:
            return
        else:
            mecha_obj = self._lbs_create_mecha_imp(self.local_mecha[0], pos)
            return

    def _lbs_create_mecha_charger(self, npc_id, pos):
        charger_init_dict = {'npc_id': npc_id,
           'position': pos
           }
        charger = self._lbs_add_entity('Charger', charger_init_dict)
        self.local_battle.record_mecha_charger(charger.id)
        return charger

    def _lbs_create_robot(self, guide_id, interval, pos, max_hp, shoot):
        if self.local_robot:
            return
        else:
            robot_init_dict = {'max_hp': max_hp,
               'is_robot': True,
               'char_name': 'guide_robot',
               'weapons': {},'position': pos,
               'parachute_mecha_id': 8002,
               'faction_id': 1,
               'aim_y': 1.0,
               'role_id': '11'
               }
            robot = self._lbs_add_entity('Puppet', robot_init_dict)
            item_data = {'item_id': 10011,'entity_id': IdManager.genid(),'count': 1}
            robot.logic.send_event('E_PICK_UP_WEAPON', item_data, -1)
            robot.logic.send_event('E_SWITCHING', 1)
            wp = robot.logic.ev_g_wpbar_cur_weapon()
            bullet_cap = wp.get_bullet_cap()
            wp.set_bullet_num(bullet_cap)
            robot.logic.send_event('E_FORCE_AGENT')
            robot.logic.send_event('E_SET_CONTROL_TARGET', None, {'from_on_land': 1,'use_phys': 1})
            self.local_robot = [robot, guide_id, interval]
            if shoot:
                self._lbs_resume_robot()
            return

    def _lbs_move_robot_to(self, next_pos_list):
        self.robot_move_points = list(next_pos_list)
        point_cnt = len(next_pos_list)
        com_remote_robot_move = self.local_robot[0].logic._coms.get('ComRemoteRobotMove', None)
        if com_remote_robot_move:
            if hasattr(com_remote_robot_move, 'exec_block_move'):

                def empty_func(*args):
                    pass

                com_remote_robot_move.exec_block_move = empty_func

        def move_to_next():
            if len(self.robot_move_points) <= 0:
                return
            pos_vec = math3d.vector(*self.robot_move_points[0])
            self.robot_move_points.pop(0)
            self.local_robot[0].logic.send_event('E_CTRL_MOVE_TO', pos_vec)

        self.local_robot_move_timer = global_data.game_mgr.register_logic_timer(move_to_next, interval=0.5, mode=CLOCK, times=point_cnt)
        return

    def _lbs_create_robot_mecha(self, guide_id, interval, pos, max_hp, shoot):
        if self.local_robot_mecha:
            return
        else:
            robot_init_dict = {'max_hp': max_hp,
               'is_robot': True,
               'char_name': 'guide_robot',
               'weapons': {},'position': pos,
               'parachute_mecha_id': 8002,
               'faction_id': 1,
               'aim_y': 1.0,
               'role_id': '11'
               }
            robot = self._lbs_add_entity('Puppet', robot_init_dict)
            mecha_init_dict = {'init_max_hp': 2700,
               'shield': 500.0,
               'last_action': (None, None),
               'creator': robot.id,
               'mecha_sfx': None,
               'mv_state': -1,
               'share': False,
               'repair_energy': 60.0,
               'cur_fuel': 100.0,
               'driver_id': robot.id,
               'suspended': False,
               'seats': ('seat_1', ),
               'broken_times': 0,
               'born_time': 1559460064.397052,
               'passenger_dict': {robot.id: 'seat_1'},'npc_id': 8001,
               'idx_pool': {1: 19},'trans_pattern': 1,
               'shoot_mode': 1,
               'weapons': {1: {'count': 1,'iBolted': 1,'iBulletNum': 80,'item_type': 0,'attachment': {},'item_id': 800101},2: {'item_id': 800102,'item_type': 0,'iBulletNum': 0,'attachment': {},'count': 1}},'faction_id': 1,
               'max_shield': 500.0,
               'max_hp': 2700,
               'hp': 2700,
               'immobilize_value': 0,
               'mp_attr': {'head_hit': 1.2,'body_hit': 1.0,'mileage': 0,'arm_hit': 1.0,'item_num': 0,'foot_hit': 1.0},'mecha_fashion': {'0': 201800100},'mecha_robot': True,
               'auto_join': False,
               'wp_bar_last_pos': 0,
               'wp_bar_cur_gun_pos': 2,
               'rage': 0,
               'skills': {800152: {'cost_fuel': 10,'cost_fuel_type': 1,'last_cast_time': 0,'outer_shield_lasting_time': 4,'outer_shield_hp': 300,
                                   'speed_up_buff_id': 397,'effect_buff_id': 396,'inc_mp': 10,'mp': 100,
                                   'speed_up_lasting_time': 3,'outer_shield_buff_id': 372,'max_mp': 100},
                          800153: {'last_cast_time': 0,'cost_fuel': 20,'cost_fuel_type': 1},800151: {'last_cast_time': 0,'inc_mp': 10,'max_mp': 100,'mp': 100}},
               'missile_lock': None,
               'mecha_id': 8001,
               't_rage_last': 0,
               'wp_bar_cur_pos': 2,
               'mp_explosive': {},'shapeshift': False,
               'set_st': 'set([])',
               'position': pos,
               'fuel_regtime': 0
               }
            mecha_obj = self._lbs_add_entity('Mecha', mecha_init_dict)
            seat = mecha_obj.logic.ev_g_driver_seat()
            mecha_obj.logic.send_event('E_ADD_PASSENGER', robot.id, seat)
            mecha_obj.logic.send_event('E_FORCE_AGENT')
            self.local_robot_mecha = [
             mecha_obj, robot, guide_id, interval]
            if shoot:
                self._lbs_resume_robot()
            return

    def _lbs_create_robot_mecha_by_type(self, guide_id, interval, mecha_dict):
        if self.local_robot_mecha:
            return
        robot_init_dict = {'max_hp': 200,'is_robot': True,
           'char_name': 'guide_robot',
           'weapons': {},'position': mecha_dict.get('pos'),
           'parachute_mecha_id': 8002,
           'faction_id': 1,
           'aim_y': 1.0,
           'role_id': '11'
           }
        robot = self._lbs_add_entity('Puppet', robot_init_dict)
        robot_id = robot.id
        from logic.gutils.newbie_stage_utils import get_npc_mecha_init_dict_by_type
        mecha_init_dict = get_npc_mecha_init_dict_by_type(mecha_dict.get('mecha_type'), robot_id, mecha_dict.get('pos'), mecha_dict.get('hp'), mecha_dict.get('shield'))
        mecha_obj = self._lbs_add_entity('Mecha', mecha_init_dict)
        seat = mecha_obj.logic.ev_g_driver_seat()
        mecha_obj.logic.send_event('E_ADD_PASSENGER', robot_id, seat)
        mecha_obj.logic.send_event('E_FORCE_AGENT')
        self.local_robot_mecha = [
         mecha_obj, robot, guide_id, interval]
        shoot = mecha_dict.get('shoot', False)
        if shoot:
            self._lbs_start_robot_mecha_shoot()

    def _lbs_create_npc_mecha_by_type(self, guide_id, interval, mecha_dict):
        if self.local_npc_mecha or self.local_npc_mecha_driver:
            return
        from logic.gutils.newbie_stage_utils import get_npc_mecha_init_dict_by_type, get_npc_robot_init_dict_by_role_type
        robot_init_dict = get_npc_robot_init_dict_by_role_type(11, mecha_dict.get('pos'))
        robot = self._lbs_add_entity('Puppet', robot_init_dict)
        mecha_init_dict = get_npc_mecha_init_dict_by_type(mecha_dict.get('mecha_type'), robot.id, mecha_dict.get('pos'), mecha_dict.get('hp'), mecha_dict.get('shield'))
        mecha = self._lbs_add_entity('Mecha', mecha_init_dict)
        seat = mecha.logic.ev_g_driver_seat()
        mecha.logic.send_event('E_ADD_PASSENGER', robot.id, seat)
        mecha.logic.send_event('E_FORCE_AGENT')
        self.local_npc_mecha = [
         mecha, guide_id, interval]
        self.local_npc_mecha_driver = [robot, 1202, interval]

    def _lbs_create_robot_eject(self, guide_id, interval, pos, hp):
        if self.local_npc_mecha_driver:
            return
        else:
            from logic.gutils.newbie_stage_utils import get_npc_robot_init_dict_by_role_type
            robot_init_dict = get_npc_robot_init_dict_by_role_type(11, pos)
            robot = self._lbs_add_entity('Puppet', robot_init_dict)
            robot.logic.send_event('E_FORCE_AGENT')
            para_target_pos = GetStageMechaHandler().get('ai_parachute_dir', {}).get('handler_params', [-16393, 115, 16562])
            data = {'para_type': 1,'shake_yaw': False,'para_target_id': None,'eject_reason': 3,'para_target_pos': para_target_pos}
            robot.logic.send_event('E_CTRL_EJECT', data)
            robot.logic.regist_event('E_AFTER_EJECT_PARACHUTE', self.on_guide_npc_mecha_driver_drop)
            self.local_npc_mecha_driver = [
             robot, guide_id, interval]
            return

    def _lbs_create_monster(self, guide_id, interval, pos, max_hp, shoot):
        if self.local_monster:
            return
        monster_init_dict = {'init_max_hp': max_hp,'mp_attr': {'head_hit': 5.0,'body_hit': 1.0,'mileage': 0,'arm_hit': 2.0,'item_num': 0,'foot_hit': 2.0},'hp': max_hp,
           'npc_id': 9007,
           'max_hp': max_hp,
           'position': pos,
           'faction_id': 1,
           'max_shield': 0
           }
        monster = self._lbs_add_entity('Monster', monster_init_dict)
        monster.logic.send_event('E_FORCE_AGENT')
        self.local_monster = [
         monster, guide_id, interval]
        if shoot:
            self._lbs_resume_robot()

    def local_robot_one_shoot(self):
        self._lbs_local_robot_shoot()
        self.local_robot_ai_timer_logic = None
        return

    def _lbs_resume_robot_delay(self):
        self.local_robot_ai_timer_delay = global_data.game_mgr.register_logic_timer(self.resume_robot_delay, interval=3, mode=CLOCK, times=1)

    def resume_robot_delay(self):
        self._lbs_resume_robot()
        self.local_robot_ai_timer_delay = None
        return

    def _lbs_destroy_robot(self):
        if self.local_robot:
            self.local_battle.destroy_entity(self.local_robot[0].id)
            self.local_robot = None
        if self.local_robot_mecha:
            self.local_battle.destroy_entity(self.local_robot_mecha[0].id)
            self.local_robot_mecha = None
        if self.local_monster:
            self.local_battle.destroy_entity(self.local_monster[0].id)
            self.local_monster = None
        if self.local_npc_mecha:
            self.local_battle.destroy_entity(self.local_npc_mecha[0].id)
            self.local_npc_mecha = None
        if self.local_npc_mecha_driver:
            self.local_battle.destroy_entity(self.local_npc_mecha_driver[0].id)
            self.local_npc_mecha_driver = None
        if self.local_robot_ai_timer:
            global_data.game_mgr.unregister_logic_timer(self.local_robot_ai_timer)
            self.local_robot_ai_timer = None
        if self.local_robot_ai_timer_logic:
            global_data.game_mgr.unregister_logic_timer(self.local_robot_ai_timer_logic)
            self.local_robot_ai_timer_logic = None
        if self.local_robot_ai_timer_delay:
            global_data.game_mgr.unregister_logic_timer(self.local_robot_ai_timer_delay)
            self.local_robot_ai_timer_delay = None
        if self.local_robot_mecha_shoot_timer:
            global_data.game_mgr.unregister_logic_timer(self.local_robot_mecha_shoot_timer)
            self.local_robot_mecha_shoot_timer = None
        if self.local_robot_move_timer:
            global_data.game_mgr.unregister_logic_timer(self.local_robot_move_timer)
            self.local_robot_move_timer = None
        return

    def _lbs_destroy_robot_mecha(self):
        if self.local_robot_mecha:
            self.local_battle.destroy_entity(self.local_robot_mecha[0].id)
            self.local_battle.destroy_entity(self.local_robot_mecha[1].id)
            self.local_robot_mecha = None
            if self.local_robot_mecha_shoot_timer:
                global_data.game_mgr.unregister_logic_timer(self.local_robot_mecha_shoot_timer)
                self.local_robot_mecha_shoot_timer = None
        return

    def _lbs_destroy_npc_mecha(self):
        if self.local_npc_mecha:
            self.local_battle.destroy_entity(self.local_npc_mecha[0].id)
            self.local_npc_mecha = None
            self.local_npc_mecha_driver[0].logic.send_event('E_FORCE_AGENT')
            pos_vec = self.local_npc_mecha_driver[0].logic.ev_g_position()
            para_target_pos = GetStageMechaHandler().get('on_guide_npc_mecha_driver_parachute', {}).get('handler_params', [-16330.076172, 111.450447, 16568.083984])
            data = {'para_type': 1,'shake_yaw': False,'para_target_id': None,'eject_reason': 3,'para_target_pos': para_target_pos
               }
            self.local_npc_mecha_driver[0].logic.send_event('E_CTRL_EJECT', data)
            self.local_npc_mecha_driver[0].logic.regist_event('E_AFTER_EJECT_PARACHUTE', self.on_guide_npc_mecha_driver_drop)
        return

    def _lbs_pause_robot(self):
        if self.local_robot_ai_timer:
            global_data.game_mgr.unregister_logic_timer(self.local_robot_ai_timer)
            self.local_robot_ai_timer = None
        return

    def _lbs_resume_robot(self):
        if (self.local_robot or self.local_robot_mecha or self.local_monster) and self.local_robot_ai_timer is None:
            self._lbs_local_robot_shoot()
            self.local_robot_ai_timer = global_data.game_mgr.register_logic_timer(self._lbs_local_robot_shoot, interval=0.2, mode=CLOCK)
            self.local_robot_shoot_break = 0
        return

    def _lbs_start_robot_mecha_shoot(self):
        if self.local_robot_mecha and not self.local_robot_mecha_shoot_timer:
            self.local_robot_mecha_shoot_break = 0
            self.local_robot_mecha_shoot_timer = global_data.game_mgr.register_logic_timer(self.robot_mecha_shoot, interval=0.1, mode=CLOCK)

    def robot_mecha_shoot(self):
        if self.local_robot_mecha:
            mecha = self.local_robot_mecha[0]
            robot = self.local_robot_mecha[1]
            if self.local_robot_mecha_shoot_break > 25:
                self.local_robot_mecha_shoot_break = 0
            self.local_robot_mecha_shoot_break += 1
            if self.local_robot_mecha_shoot_break == 2:
                mecha and mecha.logic and mecha.logic.send_event('E_CTRL_ACTION_STOP', ai_const.CTRL_ACTION_MAIN)
                return
            if self.local_robot_mecha_shoot_break == 1:
                wp = mecha.logic.ev_g_wpbar_cur_weapon()
                if wp is None:
                    return
                wp.set_bullet_num(20)
                if mecha.logic.sd.ref_aim_target is None:
                    target = self.logic.ev_g_bind_mecha_entity()
                    if target:
                        mecha.logic.send_event('E_ATK_TARGET', target.logic)
                    else:
                        mecha.logic.send_event('E_ATK_TARGET', self.logic)
                t_pos = mecha.logic.ev_g_position()
                m_pos = self._lbs_get_value('G_POSITION')
                start_pos = t_pos + math3d.vector(0, 20, 0)
                end_pos = m_pos + math3d.vector(0, 20, 0)
                if self._lbs_is_hit(start_pos, end_pos):
                    return
                lst_from = (
                 t_pos.x, t_pos.y, t_pos.z)
                parameters = (800102, 20, 0, robot.id, lst_from, None, None)
                method_name = idx_utils.s_method_2_idx('on_hit_bomb')
                self._lbs_send_event('E_DO_SYNC_METHOD', method_name, parameters)
                mecha.logic.send_event('E_CTRL_ACTION_START', ai_const.CTRL_ACTION_MAIN, self.id, (end_pos.x, end_pos.y, end_pos.z), False)
                mecha.logic.send_event('E_CTRL_FACE_TO', end_pos)
                self._lbs_player_damage()
        return

    def _lbs_create_pick_item(self, guide_id, item_no, pos, sub_items):
        item_init_dict = {'item_id': item_no,'count': 1,
           'position': pos
           }
        all_item = {}
        for sub_item_no, cnt in six.iteritems(sub_items):
            eid = IdManager.genid()
            all_item[eid] = {'item_id': sub_item_no,'count': cnt}

        if all_item:
            item_init_dict['all_item'] = all_item
        pick_item = self._lbs_add_entity('Item', item_init_dict)
        self.local_pick_item = [pick_item, guide_id]

    def _lbs_destroy_item(self):
        if self.local_pick_item:
            self.local_battle.destroy_entity(self.local_pick_item[0].id)
            self.local_pick_item = None
        return

    def _lbs_create_items(self, guide_id, item_list):
        for item_info in item_list:
            item_obj = self._lbs_add_entity('Item', item_info)
            self.local_items[item_obj.id] = {'item_obj': item_obj,'guide_id': guide_id}

    def _lbs_destroy_items(self):
        if self.local_items:
            for item_eid, _ in six.iteritems(self.local_items):
                self.local_battle.destroy_entity(item_eid)

            self.local_items = {}

    def delay_exec_destroy_ai(self, opt):
        if opt == 1:
            if not self.local_robot:
                return
            p1, p2 = self.local_robot[-2], self.local_robot[-1]
        elif opt == 2:
            if self.local_robot_mecha is None:
                return
            p1, p2 = self.local_robot_mecha[-2], self.local_robot_mecha[-1]
        elif opt == 3:
            p1, p2 = self.local_monster[-2], self.local_monster[-1]
        elif opt == 4:
            p1, p2 = self.local_npc_mecha[-2], self.local_npc_mecha[-1]
        elif opt == 5:
            p1, p2 = self.local_npc_mecha_driver[-2], self.local_npc_mecha_driver[-1]
        else:
            return
        if self.local_robot_mecha:
            self._lbs_destroy_robot_mecha()
        else:
            self._lbs_destroy_robot()
        self.logic.send_event('E_GUIDE_ROBOT_DEAD', p1, p2)
        return

    def _lbs_robot_damage(self, damage):
        if self.local_robot:
            robot = self.local_robot[0]
            if robot.logic.ev_g_hp() > 0:
                robot.logic.ev_g_damage(damage)
                if robot.logic.ev_g_hp() <= 0:
                    robot.logic.send_event('T_DEATH', self.id)
                    self._lbs_pause_robot()
                    global_data.game_mgr.register_logic_timer(lambda : self.delay_exec_destroy_ai(1), interval=2.0, mode=CLOCK, times=1)
                    ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
                    if ui:
                        ui._handle_death_event(FIGHT_EVENT_DEATH)
        if self.local_robot_mecha:
            mecha = self.local_robot_mecha[0]
            shield = mecha.logic.ev_g_shield()
            if shield > 0:
                mecha.logic.send_event('E_SET_SHIELD', shield - damage)
            elif mecha.logic.ev_g_hp() > 0:
                mecha_hp = mecha.logic.ev_g_hp()
                lower_hp = GetStageHumanHandler().get('robot_mecha_lower_hp', {}).get('handler_params', 200)
                if mecha_hp < lower_hp:
                    self._lbs_send_event('E_GUIDE_ROBOT_MECHA_HP_LOWER')
                mecha.logic.ev_g_damage(damage)
                if mecha.logic.ev_g_hp() <= 0:
                    self._lbs_pause_robot()
                    if self.local_robot_mecha[1]:
                        self.local_battle.destroy_entity(self.local_robot_mecha[1].id)
                    global_data.game_mgr.register_logic_timer(lambda : self.delay_exec_destroy_ai(2), interval=2.0, mode=CLOCK, times=1)
                    if self.need_eject_driver:
                        self.need_eject_driver = False
                        self.set_no_mecha_damage_flag(True)
                        eject_robot_guide_id = GetStageMechaHandler().get('eject_robot_guide_id', {}).get('handler_params', 1202)
                        eject_robot_start_pos = GetStageMechaHandler().get('eject_robot_start_pos', {}).get('handler_params', [-16017, 112.556396, 17041])
                        self._lbs_create_robot_eject(eject_robot_guide_id, 0, eject_robot_start_pos, 200)
                    ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
                    if ui:
                        ui._handle_death_event(FIGHT_EVENT_MECHA_DEATH)
        if self.local_monster:
            monster = self.local_monster[0]
            if monster.logic.ev_g_hp() > 0:
                monster.logic.ev_g_damage(damage)
                if monster.logic.ev_g_hp() <= 0:
                    global_data.game_mgr.register_logic_timer(lambda : self.delay_exec_destroy_ai(3), interval=2.0, mode=CLOCK, times=1)
                    ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
                    if ui:
                        ui._handle_death_event(FIGHT_EVENT_DEATH)
        if self.local_npc_mecha:
            mecha = self.local_npc_mecha[0]
            shield = mecha.logic.ev_g_shield()
            if shield > 0:
                mecha.logic.send_event('E_SET_SHIELD', shield - damage)
            elif mecha.logic.ev_g_hp() > 0:
                mecha.logic.ev_g_damage(damage)
                if mecha.logic.ev_g_hp() <= 0:
                    self._lbs_pause_robot()
                    global_data.game_mgr.register_logic_timer(lambda : self.delay_exec_destroy_ai(4), interval=0.033, mode=CLOCK, times=1)
                    ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
                    if ui:
                        ui._handle_death_event(FIGHT_EVENT_MECHA_DEATH)
        if self.local_npc_mecha_driver:
            driver = self.local_npc_mecha_driver[0]
            if driver.logic.ev_g_hp() > 0:
                driver.logic.ev_g_damage(damage)
                if driver.logic.ev_g_hp() <= 0:
                    self._lbs_pause_robot()
                    global_data.game_mgr.register_logic_timer(lambda : self.delay_exec_destroy_ai(5), interval=0.1, mode=CLOCK, times=1)
                    ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
                    if ui:
                        ui._handle_death_event(FIGHT_EVENT_DEATH)

    def _lbs_do_shoot(self, start=None, end=None, aim=None, scene_pellet=0, target_dict=None, scene_dict=None, shoot_mask=0, ext_dict=None, wp_pos=None, t_use=0):
        if target_dict:
            for target_id in target_dict:
                if ext_dict:
                    bullet_type = ext_dict.get('bullet_type', None)
                else:
                    bullet_type = None
                target_obj = EntityManager.getentity(target_id)
                dmg_parts = {}
                damage = 0
                if not global_data.battle:
                    return
                battle_type = global_data.battle.get_battle_tid()
                is_in_mecha = False
                if target_obj:
                    is_in_mecha = target_obj.logic.ev_g_in_mecha('Mecha')
                for part in target_dict[target_id]['parts']:
                    if battle_type in [NEWBIE_STAGE_HUMAN_BATTLE, NEWBIE_STAGE_MECHA_BATTLE]:
                        if bullet_type == 800101 and self._no_mecha_damage_flag:
                            num = 0
                        else:
                            num = self.get_newbie_stage_local_damge(bullet_type, is_in_mecha, part)
                    else:
                        num = get_local_damage(bullet_type, part)
                    dmg_parts[part] = (1, num)
                    damage += num

                start_pos = tp_to_v3d(start)
                end_pos = tp_to_v3d(end)
                st_target = (end_pos.x, end_pos.y, end_pos.z)
                lst_from = (start_pos.x, start_pos.y, start_pos.z)
                parameters = (ext_dict['bullet_type'], dmg_parts, 0, st_target, lst_from, global_data.player.id)
                method_name = idx_utils.s_method_2_idx('on_hit_shoot')
                if target_obj:
                    target_obj.logic.send_event('E_DO_SYNC_METHOD', method_name, parameters)
                self._lbs_robot_damage(damage)

        return

    def _monster_explosive(self, owner, info):
        target_id = info.get('target', None)
        if target_id is None:
            return
        else:
            if target_id == owner.id:
                return
            target = self.local_battle.get_entity(target_id)
            if target is None:
                return
            damage = get_local_mecha_second_weapon_damage()
            parameters = (890501, damage, 0, owner.id, info['pos'], None)
            method_name = idx_utils.s_method_2_idx('on_hit_bomb')
            target.logic.send_event('E_DO_SYNC_METHOD', method_name, parameters)
            return

    def _player_explosive(self, owner, info):
        info = info.get('item')
        if not info:
            return
        else:
            is_mecha = False
            if self.local_robot:
                target = self.local_robot[0]
            elif self.local_robot_mecha:
                target = self.local_robot_mecha[0]
                is_mecha = True
            elif self.local_monster:
                target = self.local_monster[0]
            elif self.local_npc_mecha:
                target = self.local_npc_mecha[0]
                is_mecha = True
            elif self.local_npc_mecha_driver and not self.local_npc_mecha:
                target = self.local_npc_mecha_driver[0]
            else:
                return
            t_pos = target.logic.ev_g_position()
            pos_tpl = info.get('position')
            if not pos_tpl:
                return
            pos = math3d.vector(*pos_tpl)
            dist = t_pos - pos
            if dist.length < 10 * NEOX_UNIT_SCALE:
                bomb_id = owner.logic.ev_g_wpbar_cur_weapon().get_item_id()
                if not global_data.battle:
                    return
                battle_type = global_data.battle.get_battle_tid()
                if battle_type in [NEWBIE_STAGE_HUMAN_BATTLE, NEWBIE_STAGE_MECHA_BATTLE]:
                    if self.logic.ev_g_in_mecha('Mecha'):
                        if self._no_mecha_damage_flag:
                            damage = 0
                        else:
                            damage = self.get_newbie_stage_local_damge(800102, is_mecha, 0)
                    else:
                        damage = self.get_newbie_stage_local_damge(bomb_id, is_mecha, 0)
                else:
                    damage = get_local_mecha_second_weapon_damage()
                parameters = (bomb_id, damage, 0, global_data.player.id, info['position'], None)
                method_name = idx_utils.s_method_2_idx('on_hit_bomb')
                target.logic.send_event('E_DO_SYNC_METHOD', method_name, parameters)
                self._lbs_robot_damage(damage)
                if self.local_robot_skill_hurt >= 0:
                    self.local_robot_skill_hurt += damage
            return

    def _lbs_update_explosive_item_info(self, explosion_info):
        if not self.local_battle:
            return
        if explosion_info:
            for uniq_key in explosion_info:
                _, item_info = global_data.emgr.scene_find_throw_item_event.emit(uniq_key)[0]
                if item_info:
                    owner_id = item_info['owner_id']
                    owner = self.local_battle.get_entity(owner_id)
                    if owner and owner.logic:
                        if owner.logic.is_monster():
                            self._monster_explosive(owner, explosion_info[uniq_key])
                        else:
                            self._player_explosive(owner, explosion_info[uniq_key])

    def _lbs_pick_obj(self, item_entity_id, package_part=None, put_pos=-1, house_entity_id=None, parent_eid=None, throw_pos=None, area_id=-1):
        if self.local_pick_item:
            pick_item = self.local_pick_item[0]
            conf = pick_item.logic.ev_g_pick_data()
            item_id = IdManager.str2id(item_entity_id)
            if item_id in conf['all_item']:
                info = conf['all_item'][item_id]
                item_data = {'item_id': info['item_id'],'entity_id': item_id,'count': info['count']}
                if is_weapon(info['item_id']):
                    iMagSize = confmgr.get('firearm_config', str(info['item_id']))['iMagSize']
                    item_data['iBulletNum'] = iMagSize
                    self._lbs_send_event('E_PICK_UP_WEAPON', item_data, -1)
                else:
                    self._lbs_send_event('E_PICK_UP_OTHERS', item_data)
                pick_item.logic.send_event('E_REMOVE_CHILD_ITEM', item_id)
                conf = pick_item.logic.ev_g_pick_data()
                if not conf['all_item']:
                    self._lbs_send_event('E_GUIDE_PICK_END', self.local_pick_item[1])
        if self.local_items:
            item_eid = IdManager.str2id(item_entity_id)
            item_obj = self.local_items.get(item_eid, {}).get('item_obj')
            guide_id = self.local_items.get(item_eid, {}).get('guide_id')
            if not item_obj or not item_obj.logic:
                return
            item_data = item_obj.logic.ev_g_pick_data()
            if not item_data:
                return
            item_id = item_data.get('item_id')
            if is_weapon(item_id):
                from logic.gcommon import const
                if put_pos >= 0 or not global_data.player.get_setting(uoc.WEAPON_PICK_DIRECTLY_REPLACE_KEY) and put_pos < 0 and is_weapon_full(self.logic):
                    if put_pos < 0:
                        put_pos = self.logic.ev_g_wpbar_cur_weapon_pos()
                    if put_pos in [const.PART_WEAPON_POS_MAIN1, const.PART_WEAPON_POS_MAIN2, const.PART_WEAPON_POS_MAIN3]:
                        throw_weapon_data = self.logic.ev_g_weapon_data(put_pos)
                        throw_pos_vec = self.logic.ev_g_position()
                        new_weapon_data = {'item_id': throw_weapon_data.get('item_id'),
                           'count': 1,
                           'position': [
                                      throw_pos_vec.x, throw_pos_vec.y, throw_pos_vec.z]
                           }
                        item_obj = self._lbs_add_entity('Item', new_weapon_data)
                        self.local_items[item_obj.id] = {'item_obj': item_obj,'guide_id': -1}
                    iMagSize = confmgr.get('firearm_config', str(item_id), default={}).get('iMagSize', 0)
                    weapon_data = {'item_id': item_id,
                       'entity_id': item_eid,
                       'count': item_data.get('count'),
                       'iBulletNum': iMagSize
                       }
                    self._lbs_send_event('E_PICK_UP_WEAPON', weapon_data, put_pos)
                    self._lbs_send_event('E_GUIDE_PICK_WEAPON', guide_id, item_id)
                    self.local_picked_item_ids.add(item_id)
                    self.check_send_specific_items_event(guide_id, [10232])
                    if item_eid in self.local_items:
                        del self.local_items[item_eid]
                    self.local_battle.destroy_entity(item_eid)
                else:
                    if self.logic.ev_g_weapon_data(const.PART_WEAPON_POS_MAIN1) == None:
                        real_put_pos = const.PART_WEAPON_POS_MAIN1
                    elif self.logic.ev_g_weapon_data(const.PART_WEAPON_POS_MAIN2) == None:
                        real_put_pos = const.PART_WEAPON_POS_MAIN2
                    elif self.logic.ev_g_weapon_data(const.PART_WEAPON_POS_MAIN3) == None:
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
                        self._lbs_send_event('E_PICK_UP_WEAPON', weapon_data, put_pos)
                        self._lbs_send_event('E_GUIDE_PICK_WEAPON', guide_id, item_id)
                        self.local_picked_item_ids.add(item_id)
                        self.check_send_specific_items_event(guide_id, [10232])
                        if item_eid in self.local_items:
                            del self.local_items[item_eid]
                        self.local_battle.destroy_entity(item_eid)
            else:
                other_item_data = {'item_id': item_id,
                   'entity_id': item_eid,
                   'count': item_data.get('count')
                   }
                self._lbs_send_event('E_PICK_UP_OTHERS', other_item_data)
                self._lbs_send_event('E_GUIDE_PICK_OTHER_ITEM', guide_id, item_id)
                self.local_picked_item_ids.add(item_id)
                self.check_send_specific_items_event(guide_id, [10232])
                if item_eid in self.local_items:
                    del self.local_items[item_eid]
                self.local_battle.destroy_entity(item_eid)
        return

    def _lbs_do_skill(self, skill_id, *args):
        if int(skill_id) == 800152:
            if self.local_robot_mecha_shield_timer is None:
                self._add_firefox_outer_shield()
                self.local_robot_mecha_shield_timer = global_data.game_mgr.register_logic_timer(self._del_firefox_outer_shield, 4, times=1, mode=CLOCK)
        return

    def _add_firefox_outer_shield(self):
        if not global_data.player or not global_data.player.logic:
            return
        mecha = global_data.player.logic.ev_g_control_target()
        mecha and mecha.logic and mecha.logic.send_event('E_OUTER_SHIELD_HP_CHANGED', 300)

    def _del_firefox_outer_shield(self):
        self.local_robot_mecha_shield_timer = None
        if not global_data.player or not global_data.player.logic:
            return
        else:
            mecha = global_data.player.logic.ev_g_control_target()
            mecha and mecha.logic and mecha.logic.send_event('E_OUTER_SHIELD_HP_CHANGED', 0)
            return

    def _lbs_local_robot_shoot(self):
        if self.local_robot_shoot_break > 25:
            self.local_robot_shoot_break = 0
        if self.local_robot_shoot_break == 0:
            self._lbs_local_robot_attack(True)
        self.local_robot_shoot_break += 1
        if self.local_robot_shoot_break > 2:
            self._lbs_local_robot_attack(False)
            return
        else:
            if self.local_robot:
                robot = self.local_robot[0]
                wp = robot.logic.ev_g_wpbar_cur_weapon()
                if wp is None:
                    return
                num = wp.get_bullet_num()
                if num <= 0:
                    if self.local_robot_reload == 0:
                        robot.logic.send_event('E_TRY_RELOAD')
                        self.local_robot_reload += 0.2
                    else:
                        self.local_robot_reload += 0.2
                        if self.local_robot_reload > 3:
                            self.local_robot_reload = 0
                            wp = robot.logic.ev_g_wpbar_cur_weapon()
                            bullet_cap = wp.get_bullet_cap()
                            wp.set_bullet_num(bullet_cap)
                    return
                wp.set_bullet_num(num - 1)
                if robot.logic.sd.ref_aim_target is None:
                    mecha = self.logic.ev_g_bind_mecha_entity()
                    if mecha:
                        robot.logic.send_event('E_ATK_TARGET', mecha.logic)
                    else:
                        robot.logic.send_event('E_ATK_TARGET', self.logic)
                t_pos = robot.logic.ev_g_position()
                m_pos = self._lbs_get_value('G_POSITION')
                start_pos = t_pos + math3d.vector(0, 20, 0)
                end_pos = m_pos + math3d.vector(0, 20, 0)
                if self._lbs_is_hit(start_pos, end_pos):
                    return
                st_target = v3d_to_tp(start_pos)
                lst_from = v3d_to_tp(t_pos)
                dmg_parts = {1: (1, 20)
                   }
                parameters = (
                 10011, dmg_parts, 0, st_target, lst_from, robot.id)
                method_name = idx_utils.s_method_2_idx('on_hit_shoot')
                self._lbs_send_event('E_DO_SYNC_METHOD', method_name, parameters)
                robot.logic.send_event('E_CTRL_FACE_TO', end_pos)
                self._lbs_player_damage()
            if self.local_robot_mecha:
                mecha = self.local_robot_mecha[0]
                wp = mecha.logic.ev_g_wpbar_cur_weapon()
                if wp is None:
                    return
                num = wp.get_bullet_num()
                if num <= 0:
                    if self.local_robot_reload == 0:
                        mecha.logic.send_event('E_TRY_RELOAD')
                        self.local_robot_reload += 0.2
                    else:
                        self.local_robot_reload += 0.2
                        if self.local_robot_reload > 3:
                            self.local_robot_reload = 0
                            wp = mecha.logic.ev_g_wpbar_cur_weapon()
                            bullet_cap = wp.get_bullet_cap()
                            wp.set_bullet_num(bullet_cap)
                    return
                wp.set_bullet_num(num - 1)
                if mecha.logic.sd.ref_aim_target is None:
                    t = self.logic.ev_g_bind_mecha_entity()
                    if t:
                        mecha.logic.send_event('E_ATK_TARGET', t.logic)
                    else:
                        mecha.logic.send_event('E_ATK_TARGET', self.logic)
                t_pos = mecha.logic.ev_g_position()
                m_pos = self._lbs_get_value('G_POSITION')
                start_pos = t_pos + math3d.vector(0, 20, 0)
                end_pos = m_pos + math3d.vector(0, 20, 0)
                if self._lbs_is_hit(start_pos, end_pos):
                    return
                mecha.logic.send_event('E_CTRL_ACTION_START', 1, self.id, (end_pos.x, end_pos.y, end_pos.z), False)
                mecha.logic.send_event('E_CTRL_FACE_TO', end_pos)
                self._lbs_player_damage()
            if self.local_monster:
                monster = self.local_monster[0]
                t_pos = monster.logic.ev_g_position()
                if not monster.logic.ev_g_is_agent():
                    monster.logic.send_event('E_TRY_AGENT', v3d_to_tp(t_pos))
                if monster.logic.sd.ref_aim_target is None:
                    t = self.logic.ev_g_bind_mecha_entity()
                    if t:
                        monster.logic.send_event('E_ATK_TARGET', t.logic)
                    else:
                        monster.logic.send_event('E_ATK_TARGET', self.logic)
                m_pos = self._lbs_get_value('G_POSITION')
                start_pos = t_pos + math3d.vector(0, 20, 0)
                end_pos = m_pos + math3d.vector(0, 20, 0)
                if self._lbs_is_hit(start_pos, end_pos):
                    return
                st_target = v3d_to_tp(start_pos)
                lst_from = v3d_to_tp(t_pos)
                dmg_parts = {1: (1, 20)
                   }
                parameters = (
                 10011, dmg_parts, 0, st_target, lst_from, monster.id)
                method_name = idx_utils.s_method_2_idx('on_hit_shoot')
                self._lbs_send_event('E_DO_SYNC_METHOD', method_name, parameters)
                monster.logic.send_event('E_MONSTER_CAST_GRENADE', self.id, self._cast_pos())
                monster.logic.send_event('E_CTRL_FACE_TO', end_pos)
                self._lbs_player_damage()
            return

    def _cast_pos(self):
        mecha = self.logic.ev_g_bind_mecha_entity()
        if mecha:
            pos = mecha.logic.ev_g_position()
            return [
             pos.x, pos.y + NEOX_UNIT_SCALE * 3, pos.z]
        else:
            pos = self.logic.ev_g_position()
            return [
             pos.x, pos.y + NEOX_UNIT_SCALE * 1.35, pos.z]

    def _lbs_player_damage(self):
        mecha = self.logic.ev_g_bind_mecha_entity()
        if mecha:
            shield = mecha.logic.ev_g_shield()
            if shield > 0:
                mecha.logic.send_event('E_SET_SHIELD', shield - 20)
            elif mecha.logic.ev_g_hp() * 1.2 > mecha.logic.ev_g_max_hp():
                mecha.logic.ev_g_damage(20)
        elif self._lbs_get_value('G_HP') > self._lbs_get_value('G_MAX_HP') * 0.9:
            self.logic.ev_g_damage(7)
        self._lbs_send_event('E_GUIDE_PLAYER_DAMAGE')

    def _lbs_local_robot_attack(self, is_attack):
        if self.local_robot:
            robot = self.local_robot[0]
            if robot and robot.logic and robot.logic.is_valid():
                if is_attack:
                    robot.logic.send_event('E_GUN_ATTACK')
                    robot.logic.send_event('E_ATTACK_START')
                else:
                    robot.logic.send_event('E_ATTACK_END')

    def _lbs_is_hit(self, start_pos, end_pos):
        hit_by_ray = global_data.game_mgr.scene.scene_col.hit_by_ray
        ret = hit_by_ray(start_pos, end_pos, 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, True)
        if ret and ret[0]:
            return True
        return False

    def get_newbie_stage_local_damge(self, weapon_id, is_mecha, part=0):
        info = GetWeaponDamage().get(weapon_id, None)
        if info:
            if is_mecha:
                if part == 0:
                    return info['mecha_head_hit']
                else:
                    return info['mecha_other_hit']

            elif part == 0:
                return info['human_head_hit']
            else:
                return info['human_other_hit']

        return 40

    def check_send_specific_items_event(self, guide_id, item_list=None):
        if not item_list:
            return
        for item_id in item_list:
            if item_id not in self.local_picked_item_ids:
                return

        self._lbs_send_event('E_GUIDE_PICKED_SPECIFIC_ITEMS', guide_id)

    def delay_destroy_self_mecha(self, mecha_id):
        if not global_data.player or not self.local_battle:
            return
        self.local_battle.destroy_entity(mecha_id)

    def on_guide_npc_mecha_driver_drop(self, *args):
        self.set_no_mecha_damage_flag(False)
        if not global_data.player:
            return
        if not self.local_npc_mecha_driver or not self.local_npc_mecha_driver[0]:
            return
        driver = self.local_npc_mecha_driver[0]
        if not driver.logic:
            return
        parachute_hor_spd = GetStageMechaHandler().get('ai_parachute_spd', {}).get('handler_params', 100)
        driver.logic.send_event('E_SET_PARACHUTE_MAX_SPD', parachute_hor_spd)
        driver.logic.regist_event('E_LAND', self.on_guide_npc_mecha_driver_landed)

    def on_guide_npc_mecha_driver_landed(self, *args):
        self.set_no_mecha_damage_flag(False)
        if not global_data.player:
            return
        if not self.local_npc_mecha_driver or not self.local_npc_mecha_driver[0]:
            return
        driver = self.local_npc_mecha_driver[0]
        if not driver.logic:
            return
        global_data.game_mgr.register_logic_timer(self.delay_create_sfx_on_ground, interval=0.2, times=1, mode=CLOCK)
        driver.logic.send_event('E_MOVE_ROCK', math3d.vector(0, 0, 0), False)

    def delay_create_sfx_on_ground(self):
        if not global_data.player:
            return
        if not self.local_npc_mecha_driver or not self.local_npc_mecha_driver[0]:
            return
        driver = self.local_npc_mecha_driver[0]
        if not driver.logic:
            return
        pos_vec = driver.logic.ev_g_position()
        if not pos_vec:
            return
        global_data.sfx_mgr.create_sfx_in_scene('effect/fx/guide/guide_end.sfx', pos_vec)
        pos_lst = [pos_vec.x, pos_vec.y, pos_vec.z]
        ui = global_data.ui_mgr.get_ui('GuideUI')
        if not ui:
            return
        ui.show_locate(pos_lst, 2, 'temp_locate', 'keep')