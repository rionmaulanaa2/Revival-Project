# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90105.py
_reload_all = True
version = '196717277'
from .pve_monster_status_config import *
cover = {'90105': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MONSTER_SCOUT, MC_RUN, MC_STAND, MC_MOVE]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MONSTER_SCOUT, MC_RUN, MC_STAND, MC_MOVE]),
             MC_JUMP_1: set([MC_TURN, MC_MONSTER_SCOUT, MC_RUN, MC_STAND, MC_MOVE]),
             MC_MECHA_BOARDING: set([MC_MONSTER_HIT]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_RUN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_3, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_TURN, MC_MONSTER_SCOUT, MC_RUN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_TOSS]),
             MC_MONSTER_SNIPE: set([MC_MONSTER_SCOUT, MC_RUN, MC_MOVE]),
             MC_MONSTER_FOCUS_SWAG: set([MC_MONSTER_SCOUT, MC_RUN, MC_MOVE]),
             MC_TURN: set([MC_MONSTER_SCOUT, MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_MONSTER_SCOUT, MC_RUN, MC_STAND]),
             MC_MONSTER_SCOUT: set([MC_RUN, MC_MOVE]),
             MC_MONSTER_RANGE: set([MC_MONSTER_SCOUT, MC_RUN, MC_MOVE]),
             MC_RUN: set([MC_JUMP_3, MC_TURN, MC_MONSTER_SCOUT, MC_STAND, MC_MOVE]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MONSTER_SCOUT, MC_RUN, MC_MOVE]),
             MC_MONSTER_POWER_RANGE: set([MC_MONSTER_SCOUT, MC_RUN, MC_MOVE]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_RUN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_IMMOBILIZE: set([MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS]),
             MC_MONSTER_HIT: set([MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_RUN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_TOSS]),
             MC_MONSTER_TOSS: set([MC_MONSTER_SCOUT, MC_RUN, MC_MOVE]),
             MC_MONSTER_ROAR: set([MC_RUN, MC_MOVE])
             }
   }
forbid = {'90105': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_RUN, MC_FROZEN, MC_STAND, MC_MOVE, MC_IMMOBILIZE]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_FOCUS_SWAG, MC_FROZEN]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_SNIPE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MONSTER_FOCUS_SWAG: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_RUN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MONSTER_SCOUT: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MONSTER_RANGE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_RUN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_MONSTER_POWER_RANGE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_FOCUS_SWAG, MC_FROZEN]),
             MC_MONSTER_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN, MC_IMMOBILIZE]),
             MC_MONSTER_TOSS: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_ROAR: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_SCOUT, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_TOSS, MC_IMMOBILIZE])
             }
   }
behavior = {'90105': {MC_JUMP_3: {'action_param': (0, ['idle_01', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle_01', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle_01', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 1.0,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_born_02_shader.sfx','born_anim': 'trans_01'},'action_state': 'MonsterBorn'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 3.5,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'die_01'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['hit_01', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'max_aim_dur': 1.5,'aim_right_anim': 'turn_right','aim_speed': 4.8,'aim_left_anim_rate': 3.5,'aim_left_anim': 'turn_left','aim_right_anim_rate': 3.5},'action_state': 'MonsterAimTurn'},MC_MONSTER_SNIPE: {'custom_param': {'pre_link_sfx_socket': 'part_point1','atk_anim_rate': 1.0,'pre_anim_dur': 2.0,'pre_anim': 'idle_01','pre_sfx_rate': 1.0,'fire_socket': 'part_point1','bac_anim_dur': 0,'skill_id': 9010555,'max_aim_dur': 1.5,'pre_sfx_scale': 1.0,'bac_anim_rate': 1.0,'aim_right_anim': 'turn_right','pre_sfx_res': 'effect/fx/monster/pve/pve_kaihuo_yellow.sfx','aim_right_anim_rate': 4.0,'pre_link_sfx_rate': 1.0,'wp_list': [9010503],'aim_left_anim_rate': 4.0,'pre_anim_rate': 1.0,'aim_left_anim': 'turn_left','bac_anim': '','pre_sfx_socket': 'part_point1','pre_link_sfx_res': 'effect/fx/mecha/8008/8008_aux_aim.sfx','atk_anim_dur': 1.0,'pre_link_sfx_scale': 1.0,'wp_pos': 1,'atk_anim': 'attack_05','aim_speed': 6.28},'action_state': 'MonsterSnipe'},MC_MONSTER_FOCUS_SWAG: {'action_state': 'MonsterFocusSwag'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_ROAR: {'custom_param': {'skill_id': 9010558,'anim_dur': 1.2,'anim_rate': 1.0,'anim_name': 'alert'},'action_state': 'MonsterRoar'},MC_MONSTER_SCOUT: {'custom_param': {'skill_id': 9010554,'anim_dur': 2.4,'anim_rate': 1.0,'anim_name': 'idle_special_01'},'action_state': 'MonsterScout'},MC_RUN: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 3.5,'move_acc': 80,'run_speed': 20,'walk_speed': 16,'brake_acc': -80},'action_state': 'MonsterRun'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['idle_01', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_POWER_RANGE: {'custom_param': {'bac_anim_dur_list': [0, 0],'skill_id': 9010552,'fire_count': 1,'max_aim_dur': 1.5,'aim_right_anim': 'turn_right','bac_anim_rate_list': [1, 1],'wp_pos': 1,'pre_anim_dur_list': [0.4, 0],'pre_anim_rate_list': [2.0, 2.0],'pre_anim_name_list': ['idle_01'],'wp_list': [9010502],'atk_anim_rate_list': [2.0, 2.0],'atk_anim_name_list': ['attack_05'],'fire_socket_list': ['fx_kaihuo1'],'aim_right_anim_rate': 3.0,'aim_left_anim_rate': 3.0,'bac_anim_name_list': ['', ''],'atk_anim_dur_list': [0.8, 0],'aim_left_anim': 'turn_left','aim_speed': 3.28},'action_state': 'MonsterRange'},MC_MONSTER_RANGE: {'custom_param': {'bac_anim_dur_list': [0, 0, 0, 0],'skill_id': 9010551,'fire_count': 4,'max_aim_dur': 1.5,'aim_right_anim': 'turn_right','bac_anim_rate_list': [1, 1, 1, 1],'wp_pos': 1,'pre_anim_dur_list': [1.0, 0, 0, 0],'pre_anim_rate_list': [1.0, 2.0, 2.0, 2.0],'pre_anim_name_list': ['attack_ready', 'idle_01', 'idle_01', 'idle_01'],'wp_list': [9010501],'atk_anim_rate_list': [2.0, 2.0, 2.0, 2.0],'atk_anim_name_list': ['attack_01', 'attack_03', 'attack_02', 'attack_04'],'fire_socket_list': ['fx_kaihuo1', 'fx_kaihuo3', 'fx_kaihuo2', 'fx_kaihuo4'],'aim_right_anim_rate': 3.0,'aim_left_anim_rate': 3.0,'bac_anim_name_list': ['', '', '', ''],'atk_anim_dur_list': [0.5, 0.5, 0.5, 0.5],'aim_left_anim': 'turn_left','aim_speed': 3.28},'action_state': 'MonsterRange'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 3,'move_acc': 80,'walk_speed': 16,'brake_acc': -80},'action_state': 'MonsterWalk'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 1.0,'hit_anim': 'hit_01','hit_anim_dur': 0.2},'action_state': 'MonsterHit'},MC_MONSTER_TOSS: {'custom_param': {'bac_anim_dur_list': [0, 0, 0, 0],'fire_count': 1,'bac_anim_rate_list': [1, 1, 1, 1],'atk_anim_name_list': ['attack_01', 'attack_03', 'attack_02', 'attack_04'],'skill_id': 9010557,'pre_anim_name_list': ['attack_ready', 'attack_ready', 'attack_ready', 'attack_ready'],'max_aim_dur': 1.5,'pre_anim_dur_list': [1.0, 0, 0, 0],'atk_anim_rate_list': [1.0, 2.0, 2.0, 2.0],'min_angle': 45.0,'aim_right_anim': 'turn_right','aim_right_anim_rate': 3.0,'wp_list': [9010502],'aim_left_anim_rate': 3.0,'atk_anim_dur_list': [0.5, 0.5, 0.5, 0.5],'aim_left_anim': 'turn_left','yaw_seq': [-20.0, -10.0, 0.0, 10.0, 20.0],'max_angle': 75.0,'max_dis': 90.0,'fire_socket_list': ['fx_buff', 'fx_kaihuo3', 'fx_kaihuo2', 'fx_kaihuo4'],'wp_pos': 1,'pre_anim_rate_list': [1.0, 1.0, 1.0, 1.0],'bac_anim_name_list': ['', '', '', ''],'aim_speed': 3.28},'action_state': 'MonsterToss'},MC_IMMOBILIZE: {'action_param': (0, ['hit_01', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]