# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90127.py
_reload_all = True
version = '194199659'
from .pve_monster_status_config import *
cover = {'90127': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_JUMP_1: set([MC_JUMP_3, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_MONSTER_SUICIDE, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_IMMOBILIZE, MC_HIT]),
             MC_TURN: set([MC_STAND]),
             MC_MONSTER_SUICIDE: set([MC_TURN, MC_STAND]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_IMMOBILIZE, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN]),
             MC_RUN: set([MC_JUMP_1, MC_TURN, MC_MOVE, MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_RUN]),
             MC_HIT: set([]),
             MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_HIT])
             }
   }
forbid = {'90127': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_MONSTER_SUICIDE, MC_DEAD]),
             MC_JUMP_2: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_MONSTER_SUICIDE, MC_DEAD]),
             MC_JUMP_1: set([MC_JUMP_2, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_MONSTER_SUICIDE, MC_DEAD, MC_BEAT_BACK]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_MONSTER_SUICIDE, MC_DEAD, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_FROZEN, MC_MONSTER_SUICIDE, MC_DEAD]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_MONSTER_SUICIDE, MC_DEAD, MC_BEAT_BACK, MC_MOVE, MC_RUN]),
             MC_MONSTER_SUICIDE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MOVE, MC_RUN, MC_HIT]),
             MC_FROZEN: set([MC_MONSTER_SUICIDE, MC_DEAD]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_MONSTER_SUICIDE, MC_DEAD, MC_BEAT_BACK]),
             MC_RUN: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_MONSTER_SUICIDE, MC_DEAD, MC_BEAT_BACK]),
             MC_MOVE: set([MC_JUMP_2, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_MONSTER_SUICIDE, MC_DEAD, MC_BEAT_BACK, MC_MOVE]),
             MC_HIT: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_MONSTER_SUICIDE, MC_DEAD, MC_BEAT_BACK]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_FROZEN, MC_MONSTER_SUICIDE, MC_DEAD])
             }
   }
behavior = {'90127': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 2.5,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_born_02_shader.sfx','born_anim': 'born'},'action_state': 'MonsterBorn'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_IMMOBILIZE: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_MONSTER_SUICIDE: {'custom_param': {'pre_anim_dur': 1.6,'skill_id': 9010751,'pre_anim_rate': 1.15,'pre_anim': 'skill_ready'},'action_state': 'MonsterSuicide'},MC_DEAD: {'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9001_blast'), ('monster_select', 'monster9001')),'time': 0.0}],'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 0,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9003_run'), ('monster_select', 'monster9003')),'time': 0.0}],'custom_param': {'dynamic_speed_rate': 2,'move_acc': 30,'walk_speed': 12,'brake_acc': -30},'action_state': 'MonsterWalk'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_RUN: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 4,'move_acc': 30,'run_speed': 16,'walk_speed': 12,'brake_acc': -30},'action_state': 'MonsterRun'},MC_HIT: {'custom_param': {'hit_anim_duration': [1, 1],'hit_anim': ['hit', 'hit'],'hit_thresh': 300},'action_state': 'Hit'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]