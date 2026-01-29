# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/CastLogic.py
from __future__ import absolute_import
from .StateBase import StateBase
from logic.gcommon.common_const import monster_const
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import LOW_BODY, UP_BODY
from logic.gcommon.common_const.idx_const import ExploderID
from mobile.common.EntityManager import EntityManager
from common.cfg import confmgr
from math import radians, tan
import common.utils.timer as timer
import math3d
import world
import logic.gcommon.common_utils.bcast_utils as bcast

def on_fire_ray_by_custom_direction(custom_direction, direction, up):
    all_dirs = []
    for data in custom_direction:
        offset = data[0]
        radian = data[1]
        rotation_matrix = math3d.matrix.make_rotation(direction, radian)
        temp_dir = direction + up * rotation_matrix * tan(radians(offset))
        temp_dir.normalize()
        all_dirs.append(temp_dir)

    direction = all_dirs
    return direction


class CastSkill(StateBase):
    BIND_EVENT = {'E_MONSTER_CAST_ACTION': 'on_cast_action'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(CastSkill, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.pre_anim = self.custom_param['pre_anim']
        self.cast_anim = self.custom_param['cast_anim']
        self.post_anim = self.custom_param['post_anim']
        self.pre_time = self.custom_param.get('pre_time', 0)
        self.cast_time = self.custom_param.get('cast_time', 1)
        self.post_time = self.custom_param.get('post_time', 0)
        self.init_sub_state_events()
        self.cast_finished = False

    def init_sub_state_events(self):
        self.register_substate_callback(monster_const.CAST_PRE, 0, self.pre_start)
        self.register_substate_callback(monster_const.CAST_PRE, self.pre_time, self.pre_end)
        self.register_substate_callback(monster_const.CAST_FIRE, 0, self.cast_start)
        self.register_substate_callback(monster_const.CAST_FIRE, self.cast_time, self.cast_end)
        self.register_substate_callback(monster_const.CAST_POST, 0, self.post_start)
        self.register_substate_callback(monster_const.CAST_POST, self.post_time, self.post_end)

    def enter(self, leave_states):
        super(CastSkill, self).enter(leave_states)
        self.send_event('E_CLEAR_SPEED')

    def check_transitions(self):
        if self.cast_finished:
            return MC_STAND

    def on_cast_action(self, stage):
        if not self.is_active:
            self.active_self()
        self.sub_state = None
        self.sub_state = stage
        return

    def pre_start(self):
        self.cast_finished = False
        self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def pre_end(self):
        pass

    def cast_start(self):
        self.send_event('E_POST_ACTION', self.cast_anim, LOW_BODY, 1, blend_time=0)

    def cast_end(self):
        pass

    def post_start(self):
        self.send_event('E_POST_ACTION', self.post_anim, LOW_BODY, 1)

    def post_end(self):
        self.sub_state = None
        self.cast_finished = True
        return


class AccumulateCastGrenade(StateBase):
    ITEM_INDEX = 1
    BIND_EVENT = {'E_MONSTER_CAST_GRENADE': 'on_cast_grenade',
       'E_MONSTER_WILD_ATTACK_BEGIN': 'on_wild_attack_begin',
       'E_MONSTER_WILD_ATTACK_END': 'on_wild_attack_end',
       'E_MONSTER_CAST_SOUND': 'on_cast_sound'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(AccumulateCastGrenade, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.tick_interval = 0.2
        self.weapon_type = self.custom_param['weapon_type']
        self.fire_socket = self.custom_param['fire_socket']
        self.pre_anim = self.custom_param['pre_anim']
        self.cast_anim = self.custom_param['cast_anim']
        self.post_anim = self.custom_param['post_anim']
        self.pre_time = self.custom_param.get('pre_time', 0)
        self.cast_time = self.custom_param.get('cast_time', 1)
        self.post_time = self.custom_param.get('post_time', 0)
        self.pre_sound_param = self.custom_param.get('pre_sound_param', None)
        self.fire_sound_param = self.custom_param.get('fire_sound_param', None)
        self.init_sub_state_events()
        self.cast_finished = False
        self.target_id = None
        self.target_pos = None
        return

    def init_sub_state_events(self):
        self.register_substate_callback(monster_const.CAST_PRE, 0, self.pre_start)
        self.register_substate_callback(monster_const.CAST_PRE, self.pre_time, self.pre_end)
        self.register_substate_callback(monster_const.CAST_FIRE, 0, self.cast_start)
        self.register_substate_callback(monster_const.CAST_FIRE, self.cast_time, self.cast_end)
        self.register_substate_callback(monster_const.CAST_POST, 0, self.post_start)
        self.register_substate_callback(monster_const.CAST_POST, self.post_time, self.post_end)

    def on_cast_grenade(self, target_id, target_pos):
        if self.is_active:
            return
        self.target_id = target_id
        self.target_pos = math3d.vector(*target_pos)
        self.send_event('E_CTRL_FACE_TO', self.target_pos)
        self.active_self()
        if target_id:
            self.send_event('E_CTRL_FOCUS', target_id)

    def update(self, dt):
        super(AccumulateCastGrenade, self).update(dt)

    def enter(self, leave_states):
        super(AccumulateCastGrenade, self).enter(leave_states)
        self.send_event('E_CLEAR_SPEED')
        self.sub_state = None
        self.sub_state = monster_const.CAST_PRE
        self.apply_timscale_to_anim = True
        return

    def check_transitions(self):
        if self.cast_finished:
            return MC_STAND

    def pre_start(self):
        self.cast_finished = False
        self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)
        if self.pre_sound_param:
            self.on_cast_sound(self.sid, self.sub_state)

    def pre_end(self):
        self.sub_state = monster_const.CAST_FIRE

    def cast_start(self):
        self.send_event('E_POST_ACTION', self.cast_anim, LOW_BODY, 1, blend_time=0)
        self.cast_grenade()
        self.send_event('E_CTRL_FOCUS', None)
        return

    def cast_end(self):
        self.sub_state = monster_const.CAST_POST

    def post_start(self):
        self.send_event('E_POST_ACTION', self.post_anim, LOW_BODY, 1)

    def post_end(self):
        self.sub_state = None
        self.cast_finished = True
        return

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)

    def cast_grenade(self):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        fire_socket = self.fire_socket
        mat = model.get_socket_matrix(fire_socket, world.SPACE_TYPE_WORLD)
        start_pos = mat.translation
        up = mat.rotation.up
        target_pos = self.target_pos
        if self.target_id:
            target = EntityManager.getentity(self.target_id)
            if target and target.logic:
                target_pos = target.logic.ev_g_position() + math3d.vector(0, 15, 0)
        direction = target_pos - start_pos
        direction.normalize()
        pellets_conf = confmgr.get('firearm_config', str(self.weapon_type), 'iPellets')
        conf = confmgr.get('firearm_config', str(self.weapon_type), 'cCustomParam') or {}
        custom_direction = conf.get('custom_direction', [])
        if type(pellets_conf) == dict:
            interval = pellets_conf['cd']
            times = len(pellets_conf['bullets'])
            global_data.game_mgr.register_logic_timer(lambda : self.fire_one_bullet(start_pos, direction), interval, times=times, mode=timer.CLOCK)
        elif custom_direction:
            directions = on_fire_ray_by_custom_direction(custom_direction, direction, up)
            for direction in directions:
                self.fire_one_bullet(start_pos, direction)

        else:
            self.fire_one_bullet(start_pos, direction)

    def fire_one_bullet(self, start_pos, direction):
        if not self or not self.is_valid():
            return
        item_kind = confmgr.get('firearm_config', str(self.weapon_type), 'iKind')
        throw_item = {'uniq_key': self.get_uniq_key(),
           'item_itype': self.weapon_type,
           'item_kind': item_kind,
           'position': (
                      start_pos.x, start_pos.y, start_pos.z),
           'dir': (
                 direction.x, direction.y, direction.z)
           }
        self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)
        if self.fire_sound_param:
            self.on_cast_sound(self.sid, self.sub_state)

    def on_wild_attack_begin(self, rate):
        self.set_state_speed_scale(rate)

    def on_wild_attack_end(self):
        self.set_state_speed_scale(1)

    def on_cast_sound(self, sid, stage):
        if sid != self.sid:
            return
        pos = self.ev_g_position()
        if stage == monster_const.CAST_PRE:
            global_data.sound_mgr.play_sound(self.pre_sound_param[0], pos, *self.pre_sound_param[1])
        elif stage == monster_const.CAST_FIRE:
            global_data.sound_mgr.play_sound(self.fire_sound_param[0], pos, *self.fire_sound_param[1])
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_MONSTER_CAST_SOUND, (sid, stage)))


class CastGrenade(StateBase):
    ITEM_INDEX = 1
    BIND_EVENT = {'E_MONSTER_CAST_GRENADE': 'on_cast_grenade',
       'E_MONSTER_CAST_SOUND': 'on_cast_sound'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(CastGrenade, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.tick_interval = 0.2
        self.weapon_type = self.custom_param['weapon_type']
        self.fire_socket = self.custom_param['fire_socket']
        self.fire_socket_number = len(self.fire_socket)
        self.cast_time = self.custom_param['cast_time']
        self.min_cast_interval = self.custom_param.get('min_cast_interval', 0.2)
        self.fire_sound_param = self.custom_param.get('fire_sound_param', None)
        self.target_id = None
        self.target_pos = None
        return

    def enter(self, leave_states):
        super(CastGrenade, self).enter(leave_states)
        for cast_time in self.cast_time:
            self.delay_call(cast_time, self.cast_grenade)

        self.fire_cnt = 0

    def exit(self, enter_states):
        self.send_event('E_CTRL_FOCUS', None)
        super(CastGrenade, self).exit(enter_states)
        return

    def check_transitions(self):
        if self.elapsed_time > self.min_cast_interval:
            self.disable_self()
            return MC_STAND

    def on_cast_grenade(self, target_id, target_pos):
        if self.is_active:
            return
        self.target_id = target_id
        self.target_pos = math3d.vector(*target_pos)
        self.send_event('E_CTRL_FACE_TO', self.target_pos)
        self.active_self()
        if target_id:
            self.send_event('E_CTRL_FOCUS', target_id)

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)

    def cast_grenade(self):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        self.fire_cnt += 1
        fire_socket = self.fire_socket[self.fire_cnt % self.fire_socket_number]
        mat = model.get_socket_matrix(fire_socket, world.SPACE_TYPE_WORLD)
        start_pos = mat.translation
        up = mat.rotation.up
        target_pos = self.target_pos
        if self.target_id:
            target = EntityManager.getentity(self.target_id)
            if target and target.logic:
                target_pos = target.logic.ev_g_position() + math3d.vector(0, 15, 0)
        direction = target_pos - start_pos
        direction.normalize()
        pellets_conf = confmgr.get('firearm_config', str(self.weapon_type), 'iPellets')
        conf = confmgr.get('firearm_config', str(self.weapon_type), 'cCustomParam') or {}
        custom_direction = conf.get('custom_direction', [])
        if type(pellets_conf) == dict:
            interval = pellets_conf['cd']
            times = len(pellets_conf['bullets'])
            global_data.game_mgr.register_logic_timer(lambda : self.fire_one_bullet(start_pos, direction), interval, times=times, mode=timer.CLOCK)
        elif custom_direction:
            directions = on_fire_ray_by_custom_direction(custom_direction, direction, up)
            for direction in directions:
                self.fire_one_bullet(start_pos, direction)

        else:
            self.fire_one_bullet(start_pos, direction)

    def fire_one_bullet(self, start_pos, direction):
        if not self or not self.is_valid():
            return
        item_kind = confmgr.get('firearm_config', str(self.weapon_type), 'iKind')
        throw_item = {'uniq_key': self.get_uniq_key(),
           'item_itype': self.weapon_type,
           'item_kind': item_kind,
           'position': (
                      start_pos.x, start_pos.y, start_pos.z),
           'dir': (
                 direction.x, direction.y, direction.z)
           }
        self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)
        if self.fire_sound_param:
            self.on_cast_sound(self.sid)

    def on_cast_sound(self, sid, *args):
        if sid != self.sid:
            return
        pos = self.ev_g_position()
        global_data.sound_mgr.play_sound(self.fire_sound_param[0], pos, *self.fire_sound_param[1])
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_MONSTER_CAST_SOUND, (sid,)))


class CastSkillClient(StateBase):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(CastSkillClient, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.tick_interval = 0.2
        self.cast_anim = self.custom_param['cast_anim']
        self.cast_time = self.custom_param['cast_time']
        self.speed_scale = self.custom_param.get('speed_scale', 1.0)
        self.cast_finished = False

    def enter(self, leave_states):
        super(CastSkillClient, self).enter(leave_states)
        self.send_event('E_POST_ACTION', self.cast_anim, LOW_BODY, 1, timeScale=self.speed_scale)
        self.send_event('E_CLEAR_SPEED')
        self.delay_call(self.cast_time, self.cast_finish_cb)
        self.cast_finished = False
        self.set_state_speed_scale(self.speed_scale)

    def cast_finish_cb(self):
        self.cast_finished = True

    def check_transitions(self):
        if self.cast_finished:
            self.disable_self()
            return MC_STAND