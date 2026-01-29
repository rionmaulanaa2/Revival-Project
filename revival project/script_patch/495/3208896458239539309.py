# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90322.py
_reload_all = True
version = '199327549'
from .pve_monster_status_config import *
cover = {'90322': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MONSTER_SCOUT, MC_RUN, MC_STAND, MC_MOVE]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MONSTER_SCOUT, MC_RUN, MC_STAND, MC_MOVE]),
             MC_JUMP_1: set([MC_TURN, MC_MONSTER_SCOUT, MC_RUN, MC_STAND, MC_MOVE]),
             MC_MONSTER_HIT: set([MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_RUN, MC_STAND, MC_MONSTER_MULTI_RANGE, MC_MOVE]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_MULTI_RANGE, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_MULTI_RANGE, MC_MOVE, MC_IMMOBILIZE]),
             MC_MONSTER_DASHATK: set([MC_TURN, MC_RUN, MC_STAND, MC_MOVE]),
             MC_TURN: set([MC_STAND]),
             MC_MONSTER_ROAR: set([MC_TURN, MC_RUN, MC_STAND, MC_MOVE]),
             MC_MONSTER_SCOUT: set([MC_TURN, MC_RUN, MC_STAND, MC_MOVE]),
             MC_MONSTER_MELEE: set([MC_TURN, MC_RUN, MC_STAND, MC_MOVE]),
             MC_RUN: set([MC_MONSTER_DASHATK, MC_TURN, MC_MONSTER_SCOUT, MC_STAND, MC_MOVE]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_RUN, MC_MONSTER_MULTI_RANGE, MC_MOVE, MC_MONSTER_HIT]),
             MC_MONSTER_MULTI_RANGE: set([]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_MULTI_RANGE, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_IMMOBILIZE: set([MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT]),
             MC_MOVE: set([MC_JUMP_3, MC_MONSTER_DASHATK, MC_TURN, MC_MONSTER_SCOUT, MC_RUN, MC_STAND]),
             MC_MONSTER_AIMTURN: set([MC_MONSTER_DASHATK, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_MULTI_RANGE, MC_MOVE, MC_MONSTER_HIT])
             }
   }
forbid = {'90322': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_IMMOBILIZE]),
             MC_MONSTER_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_RUN, MC_FROZEN, MC_STAND, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_MONSTER_DASHATK: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_RUN, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_ROAR: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_SCOUT: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_MELEE: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_IMMOBILIZE]),
             MC_MONSTER_MULTI_RANGE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_AIMTURN: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_IMMOBILIZE])
             }
   }
behavior = {'90322': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 2.7,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve_three/pve_three_birth_shader.sfx','born_anim': 'born'},'action_state': 'MonsterBorn'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 1.7,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_DASHATK: {'custom_param': {'skill_id': 9032255,'max_rush_duration': 1.0,'miss_anim_duration': 1.8,'pre_anim': 'skill1_1','miss_anim_rate': 1.0,'miss_anim': '','aim_turn': True,'tick_interval': 0.03,'rush_anim_rate': 1.0,'max_rush_speed': 550.0,'rush_anim': '','col_info': [80, 120],'air_dash_end_speed': 30,'pre_anim_rate': 1.0,'is_draw_col': False,'dash_stepheight': 8.0,'pre_anim_duration': 0.2,'end_brake_time': 1.0},'action_state': 'MonsterDashAtk'},MC_MONSTER_AIMTURN: {'custom_param': {'skill_id': 9032252,'max_aim_dur': 1.8,'aim_right_anim': 'turn_right','aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'aim_left_anim': 'turn_left','aim_speed': 3.6},'action_state': 'MonsterAimTurn'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_ROAR: {'custom_param': {'skill_id': 9032254,'anim_dur': 3.0,'anim_rate': 1.0,'anim_name': 'skill'},'action_state': 'MonsterRoar'},MC_MONSTER_SCOUT: {'action_param': (0, ['seek', 'lower', 1]),'custom_param': {'skill_id': 9032253,'anim_dur': 4.8,'anim_rate': 1.0,'anim_name': 'reload'},'action_state': 'MonsterScout'},MC_MONSTER_MELEE: {'custom_param': {'hit_range': [14.0, 14.0, 39],'atk_anim_rate': 2.0,'pre_anim_dur': 0.6,'pre_anim': 'melee','aim_turn': True,'pre_anim_rate': 1.1,'bac_anim_dur': 0.9,'skill_id': 9032256,'bac_anim': '','atk_anim_dur': 0.2,'bac_anim_rate': 1.0,'atk_anim': ''},'action_state': 'MonsterMelee'},MC_RUN: {'action_param': (0, ['run_front', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.5,'move_acc': 3000,'run_speed': 18,'walk_speed': 13,'brake_acc': -3000},'action_state': 'MonsterRun'},MC_FROZEN: {'action_param': (0, ['', 'lower', 1]),'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_MULTI_RANGE: {'custom_param': {'bac_anim_dur_list': [0.0, 0.0, 0.1],'skill_id': 9032251,'fire_count': 3,'max_aim_dur': 2.0,'multi_fire_seq': [['kaihuo_1', 'kaihuo_2'], ['kaihuo_1', 'kaihuo_2'], ['kaihuo_1', 'kaihuo_2']],'atk_anim_name_list': ['attack', 'attack', 'attack'],'bac_anim_rate_list': [1.0, 1.0, 2.0],'pre_anim_dur_list': [0.0, 2.4, 2.4],'pre_anim_rate_list': [1.0, 1.2, 1.2],'pre_anim_name_list': ['attack', 'skill', 'skill'],'wp_list': [9032201, 9032201, 9032201],'atk_anim_rate_list': [1.0, 1.0, 1.0],'socket_list': ['kaihuo_1', 'kaihuo_2', 'kaihuo_2'],'bac_anim_name_list': ['', '', 'hit'],'atk_anim_dur_list': [0.6, 0.6, 0.6],'aim_speed': 3.0},'action_state': 'MonsterMultiRange'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 1.0,'move_acc': 3000,'walk_speed': 13,'brake_acc': -3000},'action_state': 'MonsterWalk'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 1.0,'hit_anim': 'hit_6','hit_anim_dur': 1.5},'action_state': 'MonsterHit'},MC_IMMOBILIZE: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]