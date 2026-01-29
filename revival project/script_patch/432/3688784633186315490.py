# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90321.py
_reload_all = True
version = '198970704'
from .pve_monster_status_config import *
cover = {'90321': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_RUN, MC_MOVE, MC_STAND]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MONSTER_ROAR, MC_RUN, MC_MOVE, MC_STAND]),
             MC_JUMP_1: set([MC_TURN, MC_MONSTER_ROAR, MC_RUN, MC_MOVE, MC_STAND]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_BRAMBLE, MC_RUN, MC_MOVE, MC_IMMOBILIZE, MC_STAND]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_AIMTURN, MC_MONSTER_MELEE, MC_MONSTER_BRAMBLE, MC_IMMOBILIZE]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_3, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_MONSTER_BRAMBLE, MC_RUN, MC_MOVE, MC_STAND]),
             MC_TURN: set([MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_STAND]),
             MC_MONSTER_MELEE: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_MOVE, MC_STAND]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_MONSTER_BRAMBLE, MC_RUN, MC_MOVE, MC_IMMOBILIZE, MC_STAND]),
             MC_MONSTER_BRAMBLE: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_MOVE, MC_STAND]),
             MC_RUN: set([MC_JUMP_3, MC_TURN, MC_MOVE, MC_STAND]),
             MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_MELEE, MC_MONSTER_BRAMBLE]),
             MC_MONSTER_ROAR: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_TURN, MC_IMMOBILIZE, MC_STAND]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_RUN, MC_MOVE])
             }
   }
forbid = {'90321': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_BRAMBLE, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_BRAMBLE, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_BRAMBLE, MC_IMMOBILIZE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_BRAMBLE, MC_RUN, MC_MOVE, MC_IMMOBILIZE, MC_STAND]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_ROAR, MC_FROZEN]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_BRAMBLE, MC_RUN, MC_MOVE, MC_IMMOBILIZE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_BRAMBLE, MC_IMMOBILIZE]),
             MC_MONSTER_MELEE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_BRAMBLE, MC_IMMOBILIZE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_MONSTER_BRAMBLE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE]),
             MC_RUN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_BRAMBLE, MC_IMMOBILIZE]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_ROAR, MC_FROZEN]),
             MC_MONSTER_ROAR: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_BRAMBLE, MC_RUN, MC_MOVE]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_BRAMBLE, MC_IMMOBILIZE])
             }
   }
behavior = {'90321': {MC_JUMP_3: {'action_param': (0, ['por1011_03_idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['por1011_03_idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['por1011_03_idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 1.0,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve_three/pve_three_birth_shader.sfx','born_anim': 'por1011_03_trans_01'},'action_state': 'MonsterBorn'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 1.2,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'por1011_03_die_01'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['por1011_03_hit', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'skill_id': 9032153,'max_aim_dur': 1.2,'aim_right_anim': 'por1011_03_rotate_right','aim_speed': 3.14,'aim_left_anim_rate': 1.0,'aim_left_anim': 'por1011_03_rotate_life','aim_right_anim_rate': 1.0},'action_state': 'MonsterAimTurn'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_ROAR: {'custom_param': {'skill_id': 9030452,'anim_dur': 1.8,'anim_rate': 1.3,'anim_name': 'por1011_03_idle_special_01'},'action_state': 'MonsterRoar'},MC_MONSTER_MELEE: {'custom_param': {'hit_range': [12.0, 10.0, 35.0],'skill_id': 9032151,'bac_anim': '','atk_anim_dur': 0.2,'atk_anim_rate': 1.8,'move_start_ts': 0.6,'pre_anim_dur': 0.7,'bac_anim_rate': 1.0,'move_speed': 420.0,'pre_anim': 'por1011_03_attack_02','aim_turn': True,'pre_anim_rate': 1.2,'move_end_ts': 0.9,'atk_anim': '','is_draw_col': False,'bac_anim_dur': 0.4},'action_state': 'MonsterMelee'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_MONSTER_BRAMBLE: {'custom_param': {'hit_range': [14.0, 10.0, 16.0],'skill_id': 9032152,'bac_anim': '','atk_anim_rate': 1.0,'atk_anim_dur': 0.6,'pre_anim_dur': 1.3,'bac_anim_rate': 1.0,'hit_seq': [8.0, 23.0, 39.0],'pre_anim': 'por1011_03_attack_01','aim_turn': True,'hit_interval': 0.02,'pre_anim_rate': 1.0,'max_hit_dis': 120,'is_draw_col': False,'atk_anim': '','bac_anim_dur': 0.4},'action_state': 'MonsterBramble'},MC_RUN: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 2,'move_acc': 30,'run_speed': 19.5,'walk_speed': 13,'brake_acc': -30},'action_state': 'MonsterRun'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 1.1,'move_acc': 30,'walk_speed': 13,'brake_acc': -30},'action_state': 'MonsterWalk'},MC_IMMOBILIZE: {'action_param': (0, ['por1011_03_hit', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_STAND: {'action_param': (0, ['por1011_03_idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]