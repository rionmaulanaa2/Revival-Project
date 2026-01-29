# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90122.py
_reload_all = True
version = '196717301'
from .pve_monster_status_config import *
cover = {'90122': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_TURN, MC_MONSTER_SCOUT, MC_STAND]),
             MC_JUMP_2: set([MC_JUMP_1, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_TURN, MC_MONSTER_SCOUT, MC_STAND]),
             MC_JUMP_1: set([MC_RUN, MC_MOVE, MC_TURN, MC_MONSTER_SCOUT, MC_STAND]),
             MC_MECHA_BOARDING: set([MC_MONSTER_SCOUT]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_FROZEN, MC_MOVE, MC_IMMOBILIZE, MC_BEAT_BACK, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_STAND, MC_MONSTER_RANGE]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_RUN, MC_MOVE, MC_IMMOBILIZE, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_STAND, MC_MONSTER_RANGE]),
             MC_TURN: set([MC_MONSTER_SCOUT, MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_RUN, MC_TURN, MC_MONSTER_SCOUT, MC_STAND]),
             MC_MONSTER_ROAR: set([MC_RUN, MC_MOVE, MC_TURN, MC_STAND]),
             MC_MONSTER_RANGE: set([MC_MONSTER_SCOUT]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_IMMOBILIZE, MC_BEAT_BACK, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_STAND, MC_MONSTER_RANGE]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_TURN, MC_MONSTER_SCOUT]),
             MC_MONSTER_SCOUT: set([MC_RUN, MC_MOVE, MC_TURN, MC_STAND]),
             MC_RUN: set([MC_MOVE, MC_TURN, MC_MONSTER_SCOUT, MC_STAND]),
             MC_IMMOBILIZE: set([MC_BEAT_BACK, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_RANGE])
             }
   }
forbid = {'90122': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_MONSTER_RANGE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_MONSTER_RANGE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_RANGE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_RUN, MC_FROZEN, MC_MOVE, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_TURN, MC_MONSTER_ROAR, MC_STAND]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_FROZEN, MC_MOVE, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_ROAR, MC_MONSTER_RANGE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_ROAR]),
             MC_MONSTER_ROAR: set([MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_SCOUT, MC_MONSTER_RANGE]),
             MC_MONSTER_RANGE: set([MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_ROAR]),
             MC_FROZEN: set([MC_DEAD]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_ROAR, MC_MONSTER_RANGE]),
             MC_MONSTER_SCOUT: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_ROAR, MC_MONSTER_RANGE]),
             MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_ROAR]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD])
             }
   }
behavior = {'90122': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 2.7,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_born_02_shader.sfx','born_anim': 'born'},'action_state': 'MonsterBorn'},MC_RUN: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.2,'move_acc': 3000,'run_speed': 35,'walk_speed': 28,'brake_acc': -3000},'action_state': 'MonsterRun'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.2,'move_acc': 3000,'walk_speed': 28,'brake_acc': -3000},'action_state': 'MonsterWalk'},MC_IMMOBILIZE: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 0,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_ROAR: {'custom_param': {'skill_id': 9011358,'anim_dur': 1.0,'anim_rate': 1.0,'anim_name': 'alert'},'action_state': 'MonsterRoar'},MC_MONSTER_SCOUT: {'action_param': (0, ['seek', 'lower', 1]),'custom_param': {'skill_id': 9010202,'anim_dur': 3.6,'anim_rate': 1.0,'anim_name': 'seek'},'action_state': 'MonsterScout'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_RANGE: {'custom_param': {'bac_anim_dur_list': [0.5],'skill_id': 9010251,'fire_count': 1,'max_aim_dur': 0.6,'wp_pos': 1,'pre_anim_dur_list': [0.6],'pre_anim_rate_list': [1.5],'pre_anim_name_list': ['attack_01'],'wp_list': [9010201],'atk_anim_rate_list': [1.6],'atk_anim_name_list': [''],'fire_socket_list': ['fx_kaihuo'],'bac_anim_name_list': ['attack_2'],'atk_anim_dur_list': [0.4],'bac_anim_rate_list': [1.2],'aim_speed': 5},'action_state': 'MonsterRange'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]