# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSyncAIClient.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
import collision
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE
import time

class ComSyncAIClient(UnitCom):
    BIND_EVENT = {'E_BEGIN_AGENT_AI': 'init_ai_data',
       'E_END_AGENT_AI': 'clear_ai_data',
       'E_SYNC_AI_DATA': 'sync_ai_data',
       'E_SET_AI_DATA': 'set_ai_data',
       'G_ENEMY_POS': 'get_enemy_pos',
       'G_ATTACK_POS': 'get_attack_pos',
       'E_TRY_SERVER_ACTION': 'call_server_ai_action',
       'E_SYNC_AGENT_DATA': 'sync_agent_data',
       'E_SYNC_STATE_DATA': 'sync_state_data',
       'G_SYNC_AI_PARAM': 'get_sync_ai_param'
       }

    def __init__(self, need_update=False):
        super(ComSyncAIClient, self).__init__(need_update)
        self.state_name = None
        self.sync_data = {}
        self.agent_data = {}
        self.wait_time = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComSyncAIClient, self).init_from_dict(unit_obj, bdict)
        info = bdict.get('ai_state_machine', None)
        if info:
            self.state_name = info['state_name']
            if info['sync_data']:
                self.sync_data = info['sync_data']
        return

    def init_ai_data(self):
        pass

    def clear_ai_data(self):
        self.state_name = None
        self.sync_data = {}
        self.agent_data = {}
        return

    def sync_ai_data(self, state_name, sync_data):
        if state_name != self.state_name:
            self.send_event('E_CLEAR_MOVE_QUEUE')
        self.state_name = state_name
        if sync_data:
            self.sync_data = sync_data
        else:
            self.sync_data = {}

    def get_sync_ai_param(self):
        if self.unit_obj.is_monster():
            return
        else:
            now = time.time()
            if now - self.wait_time <= 0.5:
                return
            self.wait_time = now
            info = []
            if self.state_name == 'CombatState' or self.state_name and self.state_name.startswith('MechaCombatState'):
                enemy_id = self.sync_data.get('enemy_id', None)
                enemy = EntityManager.getentity(enemy_id) if enemy_id else None
                if enemy and not self.can_shoot_enemy(enemy):
                    info.append([0, enemy.id])
            if self.state_name and self.state_name.startswith('MechaCombatState'):
                info.append([1, self.ev_g_fuel(), self.ev_g_max_fuel()])
            return info

    def set_ai_data(self, k, v):
        if self.sync_data.get(k, None) != v:
            self.sync_data[k] = v
        return

    def get_enemy_pos(self):
        if self.sync_data is None:
            return
        else:
            enemy_id = self.sync_data.get('enemy_id', None)
            if enemy_id == self.unit_obj.id:
                return
            enemy = EntityManager.getentity(enemy_id) if enemy_id else None
            enemy = enemy.logic.ev_g_control_target() if enemy and enemy.logic and enemy.logic.ev_g_is_in_mecha() else enemy
            if enemy and enemy.logic:
                return enemy.logic.ev_g_model_position()
            return

    def get_attack_pos(self):
        if self.sync_data is None:
            return
        else:
            enemy_id = self.sync_data.get('enemy_id', None)
            enemy = EntityManager.getentity(enemy_id) if enemy_id else None
            enemy = enemy.logic.ev_g_control_target() if enemy and enemy.logic.ev_g_is_in_mecha() else enemy
            if enemy:
                model = enemy.logic.ev_g_model()
                if not model or not model.bounding_box:
                    return
                m_height = model.bounding_box.y * 0.5
                m_pos = model.world_position
                return math3d.vector(m_pos.x, m_pos.y + m_height, m_pos.z)
            return

    def call_server_ai_action(self, evt, *args):
        player = global_data.player
        if player:
            self.send_event('E_CALL_SYNC_METHOD', 'call_ai_action', (evt, args, player.id))

    def sync_agent_data(self, key, value):
        if self.agent_data.get(key, None) != value:
            self.agent_data[key] = value
            self.call_server_ai_action('E_SYNC_AGENT_DATA', key, value)
        return

    def sync_state_data(self, key, value):
        self.call_server_ai_action('E_SYNC_STATE_DATA', key, value)

    def can_shoot(self, start_pos, end_pos):
        scn = world.get_active_scene()
        if not scn:
            return False
        ret = scn.scene_col.hit_by_ray(start_pos, end_pos, 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, True)
        if ret and ret[0]:
            return False
        return True

    def can_shoot_enemy(self, enemy):
        is_mecha = enemy.logic.ev_g_is_in_mecha()
        o_pos = self.ev_g_position()
        if o_pos is None:
            return False
        else:
            if is_mecha:
                start_pos = math3d.vector(o_pos.x, o_pos.y + NEOX_UNIT_SCALE * 4.8, o_pos.z)
            else:
                start_pos = math3d.vector(o_pos.x, o_pos.y + NEOX_UNIT_SCALE * 1.8, o_pos.z)
            can_shoot = self.can_shoot
            mecha = enemy.logic.ev_g_control_target()
            if is_mecha and mecha:
                e_pos = mecha.logic.ev_g_position()
                if e_pos is None:
                    return False
                end_pos = math3d.vector(e_pos.x, e_pos.y + NEOX_UNIT_SCALE * 3, e_pos.z)
                if can_shoot(start_pos, end_pos):
                    return (start_pos, end_pos)
                end_pos = math3d.vector(e_pos.x, e_pos.y + NEOX_UNIT_SCALE * 4.5, e_pos.z)
                if can_shoot(start_pos, end_pos):
                    return True
                face = e_pos - o_pos
                face.y = 0
                if face.is_zero:
                    return False
                face.normalize()
                l_face = math3d.vector(face.z, 0, -face.x)
                end_pos = e_pos + l_face * NEOX_UNIT_SCALE
                end_pos.y += NEOX_UNIT_SCALE * 3
                if can_shoot(start_pos, end_pos):
                    return True
                r_face = math3d.vector(-face.z, 0, face.x)
                end_pos = e_pos + r_face * NEOX_UNIT_SCALE
                end_pos.y += NEOX_UNIT_SCALE * 3
                if can_shoot(start_pos, end_pos):
                    return True
            else:
                e_pos = enemy.logic.ev_g_position()
                if e_pos is None:
                    return False
                end_pos = math3d.vector(e_pos.x, e_pos.y + NEOX_UNIT_SCALE * 1.35, e_pos.z)
                if can_shoot(start_pos, end_pos):
                    return True
                end_pos = math3d.vector(e_pos.x, e_pos.y + NEOX_UNIT_SCALE * 1.7, e_pos.z)
                if can_shoot(start_pos, end_pos):
                    return True
            return False