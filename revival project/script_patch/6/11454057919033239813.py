# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90128.py
_reload_all = True
version = '194199663'
from .pve_monster_status_config import *
cover = {'90128': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_JUMP_1: set([MC_JUMP_3, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_MELEE, MC_IMMOBILIZE, MC_MONSTER_AIMTURN, MC_HIT]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_MELEE, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
             MC_TURN: set([MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_RUN]),
             MC_MONSTER_MELEE: set([MC_MOVE, MC_RUN]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_MONSTER_MELEE, MC_IMMOBILIZE, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN]),
             MC_RUN: set([MC_JUMP_1, MC_TURN, MC_MOVE, MC_STAND]),
             MC_HIT: set([MC_MONSTER_MELEE]),
             MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_MELEE, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_HIT])
             }
   }
forbid = {'90128': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_MONSTER_AIMTURN]),
             MC_JUMP_2: set([MC_MECHA_BOARDING, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_MONSTER_AIMTURN]),
             MC_JUMP_1: set([MC_JUMP_2, MC_MECHA_BOARDING, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD]),
             MC_MONSTER_AIMTURN: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MOVE, MC_RUN]),
             MC_MOVE: set([MC_JUMP_2, MC_MECHA_BOARDING, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MOVE]),
             MC_MONSTER_MELEE: set([MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_HIT]),
             MC_FROZEN: set([MC_DEAD]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN]),
             MC_RUN: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN]),
             MC_HIT: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD])
             }
   }
behavior = {'90128': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 2.5,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_born_02_shader.sfx','born_anim': 'born'},'action_state': 'MonsterBorn'},MC_MONSTER_MELEE: {'custom_param': {'hit_range': [10, 10, 13],'atk_anim_rate': 1.0,'pre_anim_dur': 0.4,'pre_anim': 'melee','aim_turn': True,'pre_anim_rate': 1.0,'bac_anim_dur': 0.7,'skill_id': 9010851,'bac_anim': '','atk_anim_dur': 0.2,'bac_anim_rate': 1.2,'atk_anim': ''},'action_state': 'MonsterMelee'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_IMMOBILIZE: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_DEAD: {'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9001_blast'), ('monster_select', 'monster9001')),'time': 0.0}],'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 0,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'max_aim_dur': 1.2,'aim_right_anim': 'walk_f','aim_speed': 3.14,'aim_left_anim_rate': 2.0,'aim_left_anim': 'walk_f','aim_right_anim_rate': 2.0},'action_state': 'MonsterAimTurn'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9003_run'), ('monster_select', 'monster9003')),'time': 0.0}],'custom_param': {'dynamic_speed_rate': 2,'move_acc': 30,'walk_speed': 11,'brake_acc': -30},'action_state': 'MonsterWalk'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_RUN: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 3,'move_acc': 30,'run_speed': 15,'walk_speed': 11,'brake_acc': -30},'action_state': 'MonsterRun'},MC_HIT: {'custom_param': {'hit_anim_duration': [1, 1],'hit_anim': ['hit', 'hit'],'hit_thresh': 300},'action_state': 'Hit'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]