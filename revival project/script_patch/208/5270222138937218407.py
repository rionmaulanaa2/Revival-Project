# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/NewbieFourLocalBattleServer.py
from __future__ import absolute_import
import logic.gcommon.common_utils.idx_utils as idx_utils
from logic.gcommon.common_const import mecha_const as mconst
from logic.gcommon.common_const.battle_const import COMBAT_STATE_NONE
from mobile.common.EntityManager import EntityManager
from common.utils.time_utils import get_time
from logic.gcommon.common_utils.math3d_utils import tp_to_v3d
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN_DF
from logic.comsys.guide_ui.GuideSetting import GuideSetting
from data.newbie_stage_config import GetBarrierConfig, GetDoorConfig, GetBornPointConfig, GetWeaponDamage
from logic.entities.LocalBattleServer import LocalBattleServer, merge_sync_handler_dict
from common.cfg import confmgr
from logic.client.const.game_mode_const import NEWBIE_STAGE_FOURTH_BATTLE_TYPE
from logic.gcommon import time_utility as tutil
from data.newbie_stage_config import GetBornPointConfig
from mobile.common.IdManager import IdManager
import math3d
from logic.gcommon.const import BACKPACK_PART_OTHERS
from logic.gcommon.common_utils.local_battle_npc_utils import LocalBattleNPCMgr
from logic.gutils.newbie_stage_utils import get_self_mecha_init_dict_by_type
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE

class NewbieFourLocalBattleServer(LocalBattleServer):
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
       'try_detach': '_lbs_try_detach'
       })
    ITEM_USE_HANDLER = {1666: 'on_use_skateboard_card',
       1612: 'on_use_blood_packet'
       }
    MECHA_RECALL_CD = 10

    def __init__(self, entityid):
        super(LocalBattleServer, self).__init__(entityid)
        self.battle_type = NEWBIE_STAGE_FOURTH_BATTLE_TYPE
        self._npc_mgr = None
        self.local_mecha = None
        return

    def init_from_dict(self, bdict):
        super(NewbieFourLocalBattleServer, self).init_from_dict(bdict)
        self.battle_type = bdict.get('battle_type', NEWBIE_STAGE_FOURTH_BATTLE_TYPE)

    def on_set_local_battle(self):
        self._npc_mgr = LocalBattleNPCMgr(self, self.get_local_battle())

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
           'max_signal': 100,
           'max_hp': 200,
           'signal_reduce_rate': 1,
           'fashion': {'0': int('20100{}00'.format(global_data.player.get_role()))}}
        return info

    def _lbs_create_items(self, guide_id, item_list):
        self._npc_mgr.add_items(guide_id, item_list)

    def destroy_items(self):
        self._npc_mgr.destroy_item()

    def _lbs_create_mecha(self, mecha_id, pos, yaw=0, *args):
        if self.local_mecha is not None:
            return
        else:
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
            self._lbs_send_event('E_STATE_CHANGE_CD', mconst.RECALL_CD_TYPE_NORMAL, self.MECHA_RECALL_CD, self.MECHA_RECALL_CD)
            ui = global_data.ui_mgr.get_ui('PostureControlUI')
            if ui:
                ui.panel.setVisible(False)
            self.local_mecha = [
             mecha_id, mecha_obj]
            return

    def _lbs_try_join_mecha(self, mecha_eid, seat, is_begin):
        mecha_obj = EntityManager.getentity(mecha_eid)
        if not mecha_obj:
            return
        mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        mecha_id = mecha_obj.logic.ev_g_mecha_id()
        mecha_type = mecha_conf.get(str(mecha_id)).get('mecha_type')
        seat = mecha_obj.logic.ev_g_driver_seat()
        mecha_obj.logic.send_event('E_ADD_PASSENGER', global_data.player.id, seat)
        self._lbs_send_event('E_ON_JOIN_MECHA_START', mecha_eid, int(mecha_type), tutil.get_server_time(), mecha_obj.is_share(), {}, seat)
        if mecha_type == mconst.MECHA_TYPE_VEHICLE:
            self._lbs_send_event('E_GUIDE_JOIN_MECHA_END')
            self._lbs_send_event('E_GUIDE_REGIST_MECHA_DIVING_EVENT', mecha_obj.logic, True)
            self.clear_mecha_call_cd()

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
            self._lbs_send_event('E_GUIDE_LEAVE_CHICKEN')
            self._lbs_send_event('E_GUIDE_REGIST_MECHA_DIVING_EVENT', mecha_obj.logic, False)
            self.clear_mecha_call_cd()
        ui = global_data.ui_mgr.get_ui('PostureControlUI')
        if ui:
            ui.panel.setVisible(True)
        global_data.game_mgr.register_logic_timer(lambda m_id=mecha_eid: self.delay_destroy_self_mecha(m_id), times=1, interval=2, mode=CLOCK)

    def clear_mecha_call_cd(self):
        ui = global_data.ui_mgr.get_ui('MechaUI')
        if ui:
            ui.clear_mecha_cd_timer()
            ui.on_add_mecha_progress(100)
            ui.get_mecha_count_down = 0
            ui.get_mecha_count_down_progress = 0

    def _lbs_try_recall(self, pos, yaw=0):
        if self.local_mecha is None:
            return
        else:
            self._lbs_create_mecha(self.local_mecha[0], pos)
            return

    def delay_destroy_self_mecha(self, mecha_id):
        if not global_data.player or not self.local_battle:
            return
        else:
            self.local_battle.destroy_entity(mecha_id)
            self.local_mecha = None
            return

    def _lbs_pick_obj(self, item_entity_id, package_part=None, put_pos=-1, house_entity_id=None, parent_eid=None, throw_pos=None, area_id=-1):
        self._npc_mgr.pick_item(item_entity_id, package_part, put_pos, house_entity_id, parent_eid, throw_pos, area_id)

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

    def _lbs_try_attach(self, entity_id):
        global_data.player.new_local_battle.destroy_entity(entity_id)
        self.attach_skateboard()

    def _lbs_try_detach(self, entity_id, lst_pos, lst_rotation):
        if not global_data.player or not global_data.player.logic:
            return
        broken = False
        atch_data = global_data.player.logic.ev_g_do_detach(entity_id, broken)
        if not atch_data:
            return
        attach_data = {'npc_id': atch_data.get('npc_id'),'atch_id': atch_data.get('atch_id'),
           'fashion': atch_data.get('fashion'),
           'hp': atch_data.get('hp'),
           'init_max_hp': atch_data.get('init_max_hp'),
           'max_hp': atch_data.get('max_hp'),
           'position': lst_pos,
           'rot': lst_rotation
           }
        self._lbs_add_entity('Attachable', attach_data)

    def _lbs_on_wpbar_switch(self, cur_pos):
        if cur_pos == 0:
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

    def _lbs_do_shoot(self, start=None, end=None, aim=None, scene_pellet=0, target_dict=None, scene_dict=None, shoot_mask=0, ext_dict=None, wp_pos=None, t_use=0):
        if target_dict:
            for target_id in target_dict:
                if ext_dict:
                    bullet_type = ext_dict.get('bullet_type', None)
                else:
                    cur_weapon = global_data.player.logic.ev_g_wpbar_cur_weapon()
                    bullet_type = cur_weapon.get_item_id()
                target_obj = EntityManager.getentity(target_id)
                dmg_parts = {}
                damage = 0
                is_in_mecha = False
                if target_obj:
                    is_in_mecha = target_obj.logic.ev_g_in_mecha('Mecha')
                for part in target_dict[target_id]['parts']:
                    num = self.get_newbie_stage_local_damge(bullet_type, is_in_mecha, part)
                    dmg_parts[part] = (1, num)
                    damage += num

                start_pos = tp_to_v3d(start)
                end_pos = tp_to_v3d(end)
                st_target = (end_pos.x, end_pos.y, end_pos.z)
                lst_from = (start_pos.x, start_pos.y, start_pos.z)
                parameters = (bullet_type, dmg_parts, 0, st_target, lst_from, global_data.player.id)
                method_name = idx_utils.s_method_2_idx('on_hit_shoot')
                if target_obj:
                    target_obj.logic.send_event('E_DO_SYNC_METHOD', method_name, parameters)
                self._lbs_robot_damage(target_obj, damage)

        return

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

    def on_use_skateboard_card(self, item_id, *args):
        self.attach_skateboard()
        self._lbs_send_event('E_ITEMUSE_ON', item_id)
        item_list = global_data.player.logic.ev_g_itme_list_by_id(item_id)
        if not item_list:
            return
        for info in item_list:
            self._lbs_send_event('E_THROW_ITEM', BACKPACK_PART_OTHERS, info['entity_id'])

    def on_use_blood_packet(self, item_id, *args):
        item_list = global_data.player.logic.ev_g_itme_list_by_id(item_id)
        if item_list:
            for info in item_list:
                self._lbs_send_event('E_THROW_ITEM', BACKPACK_PART_OTHERS, info['entity_id'])

            self._lbs_send_event('E_ITEMUSE_ON', item_id)
            max_hp = self._lbs_get_value('G_MAX_HP')
            self._lbs_send_event('S_HP', max_hp)
            max_signal = self._lbs_get_value('G_MAX_SIGNAL')
            self._lbs_send_event('SET_SIGNAL', max_signal)
            self._lbs_send_event('E_GUIDE_USE_END')

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

    def _lbs_create_pick_item(self, guide_id, item_no, pos, sub_items):
        self._npc_mgr.add_box_item(guide_id, item_no, pos, sub_items)

    def _lbs_destroy_item(self):
        self._npc_mgr.destroy_item()

    def _lbs_start_poison_circle(self, guide_id, state, refresh_time, last_time):
        global_data.emgr.scene_start_poison_circle_event.emit(state, refresh_time, last_time)

    def _lbs_refresh_poison_circle(self, guide_id, state, refresh_time, last_time, level, poison_point, safe_point, reduce_type):
        global_data.emgr.scene_refresh_poison_circle_event.emit(state, refresh_time, last_time, level, poison_point, safe_point, reduce_type)
        global_data.emgr.scene_reset_poison_level.emit(level)

    def _lbs_reduce_poison_circle(self, guide_id, state, refresh_time, last_time, reduce_type):
        global_data.emgr.scene_reduce_poison_circle_event.emit(state, refresh_time, last_time, reduce_type)
        global_data.sound_mgr.play_ui_sound('remind')

    def _lbs_clear_poison(self):
        global_data.ui_mgr.close_ui('BattleSignalInfoUI')
        global_data.emgr.scene_clear_poison_circle_event.emit()

    def _lbs_enter_ace_stage(self):
        from logic.gcommon.common_const import battle_const
        message = [{'i_type': battle_const.MAIN_MECHA_RECALL_INFO}, {'i_type': battle_const.MAIN_ACE_TIME}]
        message_type = [
         battle_const.MAIN_NODE_COMMON_INFO, battle_const.MAIN_NODE_COMMON_INFO]
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, True)
        global_data.emgr.battle_into_ace_stage_event.emit()

    def _lbs_create_robot_mecha_by_type(self, guide_id, interval, mecha_dict):
        self._npc_mgr.add_robot_mecha(guide_id, interval, mecha_dict)

    def _lbs_player_damage(self):
        mecha = global_data.player.logic.ev_g_ctrl_mecha_obj()
        if mecha:
            shield = mecha.logic.ev_g_shield()
            if shield > 0:
                mecha.logic.send_event('E_SET_SHIELD', shield - 100)
            elif mecha.logic.ev_g_hp() * 1.2 > mecha.logic.ev_g_max_hp():
                mecha.logic.ev_g_damage(50)
        elif self._lbs_get_value('G_HP') > self._lbs_get_value('G_MAX_HP') * 0.2:
            global_data.player.logic.ev_g_damage(2)
        self._lbs_send_event('E_GUIDE_PLAYER_DAMAGE')

    def _lbs_create_robot(self, guide_id, interval, pos, max_hp, shoot, role_id, eagle_flag):
        self._npc_mgr.add_robot(guide_id, interval, pos, max_hp, shoot, role_id, eagle_flag)

    def _lbs_robot_damage(self, target_obj, damage):
        if not target_obj or damage <= 0:
            return
        npc_id = target_obj.id
        self._npc_mgr.on_npc_hurt(npc_id, damage)

    def _lbs_destroy_robot(self):
        self._npc_mgr.destroy_all()

    def on_quit_battle(self, *args):
        self.quit_local_battle()
        self.clear_local_battle_data()

    def quit_local_battle(self):
        self._lbs_destroy_robot()
        if self.local_battle:
            self.local_battle.destroy()
            self.local_battle = None
        lobby = global_data.player.get_lobby()
        if lobby:
            lobby.init_from_dict({'is_login': False,'combat_state': COMBAT_STATE_NONE,'from_newbie_stage': True})
        return

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

    def has_finish_guide(self):
        info = self._get_local_battle_data()
        return info.get('_lbs_finish_guide', None)

    def lbs_update_explosive_item_info(self, explosion_info):
        if explosion_info:
            for uniq_key in explosion_info:
                _, item_info = global_data.emgr.scene_find_throw_item_event.emit(uniq_key)[0]
                if item_info:
                    owner_id = item_info['owner_id']
                    owner = self.local_battle.get_entity(owner_id)
                    if owner and owner.logic and owner.logic.ev_g_is_avatar():
                        self._player_explosive(owner, explosion_info[uniq_key])

    def _player_explosive(self, owner, info):
        info = info.get('item')
        if not info:
            return
        else:
            pos_tpl = info.get('position')
            if not pos_tpl:
                return
            pos = math3d.vector(*pos_tpl)
            target_list = []
            for npc_id in self._npc_mgr.get_all_attack_npc_ids():
                entity = self.local_battle.get_entity(npc_id)
                if not entity:
                    continue
                t_pos = entity.logic.ev_g_position()
                dist = t_pos - pos
                if dist.length < 10 * NEOX_UNIT_SCALE:
                    target_list.append(entity)

            for target in target_list:
                bomb_id = owner.logic.ev_g_wpbar_cur_weapon().get_item_id()
                is_mecha = target and target.logic and target.logic.__class__.__name__ == 'LMechaRobot'
                if global_data.player.logic.ev_g_in_mecha('Mecha'):
                    damage = self.get_newbie_stage_local_damge(800102, is_mecha, 0)
                else:
                    damage = self.get_newbie_stage_local_damge(bomb_id, is_mecha, 0)
                parameters = (
                 bomb_id, damage, 0, global_data.player.id, info['position'], None)
                method_name = idx_utils.s_method_2_idx('on_hit_bomb')
                target.logic.send_event('E_DO_SYNC_METHOD', method_name, parameters)
                self._lbs_robot_damage(target, damage)

            return