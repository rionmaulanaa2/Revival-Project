# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90312.py
_reload_all = True
version = '198762506'
from .pve_monster_status_config import *
cover = {'90312': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_JUMP_1: set([MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_MECHA_BOARDING: set([MC_MONSTER_HIT]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MONSTER_AIMTURN: set([MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_TURN: set([MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_STAND]),
             MC_MONSTER_RANGE: set([MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_RUN: set([MC_TURN, MC_MOVE, MC_STAND]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN]),
             MC_MONSTER_POWER_RANGE: set([MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MONSTER_HIT: set([MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_TOSS]),
             MC_MONSTER_TOSS: set([MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_IMMOBILIZE: set([MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS])
             }
   }
forbid = {'90312': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_FROZEN, MC_STAND, MC_IMMOBILIZE]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_MONSTER_AIMTURN: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MOVE, MC_RUN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MONSTER_RANGE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MONSTER_POWER_RANGE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_MONSTER_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN, MC_IMMOBILIZE]),
             MC_MONSTER_TOSS: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN])
             }
   }
behavior = {'90312': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 1.0,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve_three/pve_three_birth_shader.sfx','born_anim': 'idle'},'action_state': 'MonsterBorn'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 0,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'stand_die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['hit', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'max_aim_dur': 1.3,'aim_right_anim': 'turnright_90','aim_speed': 3.14,'aim_left_anim_rate': 1.0,'aim_left_anim': 'turnleft_90','aim_right_anim_rate': 1.0},'action_state': 'MonsterAimTurn'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'move_acc': 1000,'dynamic_speed_rate': 0.7,'brake_acc': -1000,'walk_speed': 11},'action_state': 'MonsterWalk'},MC_RUN: {'action_param': (0, ['stand_run_f', 'lower', 1, {'loop': True}]),'custom_param': {'move_acc': 1000,'run_speed': 16,'dynamic_speed_rate': 0.1,'brake_acc': -1000,'walk_speed': 11},'action_state': 'MonsterRun'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_POWER_RANGE: {'custom_param': {'bac_anim_dur_list': [0.0, 0.0, 0.0],'skill_id': 9031255,'fire_count': 3,'max_aim_dur': 1.3,'aim_right_anim': 'turnright_90','bac_anim_rate_list': [1.0, 1.0, 1.0],'wp_pos': 1,'pre_anim_dur_list': [0.6, 0.0, 0.0],'pre_anim_rate_list': [1.0, 1.0, 1.0],'pre_anim_name_list': ['stand_shoot', '', ''],'wp_list': [9031201],'atk_anim_rate_list': [1.0, 1.0, 1.0],'atk_anim_name_list': ['stand_fire', 'stand_fire', 'stand_fire'],'fire_socket_list': ['fx_kaihuo', 'fx_kaihuo', 'fx_kaihuo'],'aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'bac_anim_name_list': ['', '', ''],'atk_anim_dur_list': [0.2, 0.2, 0.2],'aim_left_anim': 'turnleft_90','aim_speed': 3.14},'action_state': 'MonsterRange'},MC_MONSTER_RANGE: {'custom_param': {'bac_anim_dur_list': [0.0, 0.0, 0.0],'fire_count': 3,'bac_anim_rate_list': [1.0, 1.0, 1.0],'move_speed': 120.0,'stand_anim': 'idle','atk_anim_name_list': ['stand_fire', 'stand_fire', 'stand_fire'],'move_start_ts': 0.2,'move_anim_rate': 1.0,'skill_id': 9031251,'pre_anim_name_list': ['stand_shoot', '', ''],'max_aim_dur': 1.3,'pre_anim_dur_list': [0.6, 0.0, 0.0],'atk_anim_rate_list': [1.0, 1.0, 1.0],'stand_anim_rate': 1.0,'aim_right_anim': 'turnright_90','move_anim': 'walk_f','aim_right_anim_rate': 1.0,'atk_anim_dur_list': [0.2, 0.2, 0.2],'wp_list': [9031201],'aim_left_anim_rate': 1.0,'move_end_ts': 3.0,'aim_left_anim': 'turnleft_90','fire_socket_list': ['fx_kaihuo', 'fx_kaihuo', 'fx_kaihuo'],'wp_pos': 1,'pre_anim_rate_list': [1.0, 1.0, 1.0],'move_anim_loop': True,'bac_anim_name_list': ['', '', ''],'aim_speed': 3.14},'action_state': 'MonsterRange'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 1.0,'hit_anim': 'hit','hit_anim_dur': 0.9},'action_state': 'MonsterHit'},MC_MONSTER_TOSS: {'custom_param': {'bac_anim_dur_list': [1.0],'fire_count': 1,'bac_anim_rate_list': [1],'atk_anim_name_list': [''],'skill_id': 9031252,'pre_anim_name_list': ['skill1'],'max_aim_dur': 1.3,'pre_anim_dur_list': [0.6],'atk_anim_rate_list': [1.0],'min_angle': 40.0,'aim_right_anim': 'turnright_90','aim_right_anim_rate': 1.0,'wp_list': [9031202],'aim_left_anim_rate': 1.0,'atk_anim_dur_list': [0.3],'aim_left_anim': 'turnleft_90','yaw_seq': [0],'max_angle': 80.0,'max_dis': 60.0,'fire_socket_list': ['fx_toss'],'wp_pos': 1,'pre_anim_rate_list': [1.0],'bac_anim_name_list': [''],'aim_speed': 3.14},'action_state': 'MonsterToss'},MC_IMMOBILIZE: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]