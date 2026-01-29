# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90103.py
_reload_all = True
version = '196717274'
from .pve_monster_status_config import *
cover = {'90103': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_STUN]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_STUN]),
             MC_JUMP_1: set([MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_MECHA_BOARDING: set([MC_MONSTER_HIT]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_3, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE]),
             MC_TURN: set([MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_STAND]),
             MC_MONSTER_RANGE: set([MC_MONSTER_AIMTURN, MC_MOVE, MC_RUN]),
             MC_RUN: set([MC_JUMP_3, MC_TURN, MC_MOVE, MC_STAND]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN]),
             MC_MONSTER_POWER_RANGE: set([MC_MONSTER_AIMTURN, MC_MOVE, MC_RUN]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MONSTER_HIT: set([MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE]),
             MC_IMMOBILIZE: set([MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_STUN]),
             MC_MONSTER_STUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE])
             }
   }
forbid = {'90103': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_FROZEN, MC_STAND, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MOVE, MC_RUN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MONSTER_RANGE: set([MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_RUN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MONSTER_POWER_RANGE: set([MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_FROZEN: set([MC_DEAD]),
             MC_MONSTER_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_MONSTER_STUN: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN])
             }
   }
behavior = {'90103': {MC_JUMP_3: {'action_param': (0, ['idle_Peace', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle_Peace', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle_Peace', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 2.0,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_born_02_shader.sfx','born_anim': 'come_On_The_Stage'},'action_state': 'MonsterBorn'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 0.5,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['idle_Peace', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'skill_id': 9010353,'max_aim_dur': 3,'aim_right_anim': 'turn_right','aim_right_anim_rate': 1.5,'aim_left_anim_rate': 1.5,'aim_left_anim': 'turn_left','aim_speed': 2},'action_state': 'MonsterAimTurn'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 1.0,'move_acc': 30,'walk_speed': 12,'brake_acc': -30},'action_state': 'MonsterWalk'},MC_RUN: {'action_param': (0, ['run', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0,'move_acc': 30,'run_speed': 16,'walk_speed': 12,'brake_acc': -30},'action_state': 'MonsterRun'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['idle_Peace', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_POWER_RANGE: {'custom_param': {'bac_anim_dur_list': [0, 0, 0, 0, 0, 0, 0, 0, 1.2],'skill_id': 9010352,'fire_count': 9,'max_aim_dur': 3,'aim_right_anim': 'turn_right','bac_anim_rate_list': [1, 1, 1, 1, 1, 1, 1, 1, 1],'wp_pos': 1,'pre_anim_dur_list': [1.0, 0.8, 0, 0, 0, 0, 0, 0, 0],'pre_anim_rate_list': [2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],'pre_anim_name_list': ['idlePeace_IdleGM', 'Ready_GM', 'idlePeace_IdleGM', 'idlePeace_IdleGM', 'idlePeace_IdleGM', 'idlePeace_IdleGM', 'idlePeace_IdleGM', 'idlePeace_IdleGM', 'idlePeace_IdleGM'],'wp_list': [9010303],'atk_anim_rate_list': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],'atk_anim_name_list': ['Shoot_GM', 'Shoot_GM', 'Shoot_GM', 'Shoot_GM', 'Shoot_GM', 'Shoot_GM', 'Shoot_GM', 'Shoot_GM', 'Shoot_GM'],'fire_socket_list': ['fx_kaihuo1', 'fx_kaihuo1', 'fx_kaihuo2', 'fx_kaihuo3', 'fx_kaihuo4', 'fx_kaihuo1', 'fx_kaihuo2', 'fx_kaihuo3', 'fx_kaihuo4'],'aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'bac_anim_name_list': ['idleGM_IdlePeace', 'idleGM_IdlePeace', 'idleGM_IdlePeace', 'idleGM_IdlePeace', 'idleGM_IdlePeace', 'idleGM_IdlePeace', 'idleGM_IdlePeace', 'idleGM_IdlePeace', 'idleGM_IdlePeace'],'atk_anim_dur_list': [0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],'aim_left_anim': 'turn_left','aim_speed': 2},'action_state': 'MonsterRange'},MC_MONSTER_RANGE: {'custom_param': {'bac_anim_dur_list': [0, 0, 0, 0, 2.167],'skill_id': 9010351,'fire_count': 5,'max_aim_dur': 3,'aim_right_anim': 'turn_right','bac_anim_rate_list': [1.0, 1.0, 1.0, 1.0, 1.0],'wp_pos': 1,'pre_anim_dur_list': [1.867, 0.8, 0, 0, 0],'pre_anim_rate_list': [1.0, 1.0, 1.0, 1.0, 1.0],'pre_anim_name_list': ['idlePeace_IdleHMG', 'Ready_HMG', 'Ready_HMG', 'Ready_HMG', 'Ready_HMG'],'wp_list': [9010301],'atk_anim_rate_list': [1.0, 0.2, 0.2, 0.2, 0.2],'atk_anim_name_list': ['Shoot_HMG', 'Shoot_HMG', 'Shoot_HMG', 'Shoot_HMG', 'Shoot_HMG'],'fire_socket_list': ['fx_kaihuo', 'fx_kaihuo', 'fx_kaihuo', 'fx_kaihuo', 'fx_kaihuo'],'aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'bac_anim_name_list': ['idleHMG_IdlePeace', 'idleHMG_IdlePeace', 'idleHMG_IdlePeace', 'idleHMG_IdlePeace', 'idleHMG_IdlePeace'],'atk_anim_dur_list': [0, 0.2, 0.2, 0.2, 0.2],'aim_left_anim': 'turn_left','aim_speed': 1},'action_state': 'MonsterRange'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 0.5,'hit_anim': 'die','hit_anim_dur': 0.3},'action_state': 'MonsterHit'},MC_IMMOBILIZE: {'action_param': (0, ['idle_Peace', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_MONSTER_STUN: {'custom_param': {'stun_anim': 'beaten_loop','pre_anim': 'beaten_start','bac_anim': 'beaten_end','bac_anim_rate': 1.0,'pre_anim_rate': 1.0,'pre_anim_dur': 0.83,'stun_anim_rate': 1.0,'bac_anim_dur': 0.73},'action_state': 'MonsterStun'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]