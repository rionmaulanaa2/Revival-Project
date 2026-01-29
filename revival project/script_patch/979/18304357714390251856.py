# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90333.py
_reload_all = True
version = '199215541'
from .pve_monster_status_config import *
cover = {'90333': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_JUMP_1: set([MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_MONSTER_HARD_MULTI_RANGE, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_AIMTURN, MC_IMMOBILIZE]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_3, MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_TURN: set([MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_STAND]),
             MC_MONSTER_HARD_MULTI_RANGE: set([MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_RUN: set([MC_JUMP_3, MC_TURN, MC_MOVE, MC_STAND]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN]),
             MC_MONSTER_MULTI_RANGE: set([MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_MONSTER_HARD_MULTI_RANGE, MC_RUN, MC_STAND, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_HIT: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_MONSTER_HARD_MULTI_RANGE, MC_RUN, MC_STAND, MC_MONSTER_MULTI_RANGE, MC_IMMOBILIZE]),
             MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_MONSTER_AIMTURN])
             }
   }
forbid = {'90333': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_HARD_MULTI_RANGE, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_HARD_MULTI_RANGE, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_HARD_MULTI_RANGE, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_MONSTER_HARD_MULTI_RANGE, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_HARD_MULTI_RANGE, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_HARD_MULTI_RANGE, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MOVE, MC_MONSTER_HARD_MULTI_RANGE, MC_RUN, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_HARD_MULTI_RANGE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_RUN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_HARD_MULTI_RANGE, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_MULTI_RANGE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_HARD_MULTI_RANGE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_MONSTER_HIT: set([MC_DEAD, MC_FROZEN]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_HARD_MULTI_RANGE, MC_FROZEN, MC_MONSTER_MULTI_RANGE, MC_MONSTER_HIT])
             }
   }
behavior = {'90333': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 1.0,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_born_02_shader.sfx','born_anim': 'idle'},'action_state': 'MonsterBorn'},MC_DEAD: {'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9001_blast'), ('monster_select', 'monster9001')),'time': 0.0}],'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 0,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['hit_front_00', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'skill_id': 9033352,'max_aim_dur': 1.2,'aim_right_anim': 'idle','aim_speed': 3.14,'aim_left_anim_rate': 1.0,'aim_left_anim': 'idle','aim_right_anim_rate': 1.0},'action_state': 'MonsterAimTurn'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MOVE: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9003_run'), ('monster_select', 'monster9003')),'time': 0.0}],'custom_param': {'dynamic_speed_rate': 2,'move_acc': 30,'walk_speed': 11,'brake_acc': -30},'action_state': 'MonsterWalk'},MC_MONSTER_HARD_MULTI_RANGE: {'custom_param': {'bac_anim_dur_list': [0.0, 0.0, 0.0, 0.4],'skill_id': 9033353,'fire_count': 4,'max_aim_dur': 2.0,'multi_fire_seq': [['fx_kaihuo_1'], ['fx_kaihuo_3'], ['fx_kaihuo_1'], ['fx_kaihuo_3']],'atk_anim_name_list': ['attack_right', 'attack_left', 'attack_right', 'attack_left'],'bac_anim_rate_list': [1.0, 1.0, 1.0, 1.0],'pre_anim_dur_list': [0.7, 0.0, 0.0, 0.0],'pre_anim_rate_list': [1.0, 1.0, 1.0, 1.0],'pre_anim_name_list': ['attack_01_00', 'attack_01_00', 'attack_01_00', 'attack_01_00'],'wp_list': [9033302, 9033302, 9033302, 9033302],'atk_anim_rate_list': [1.5, 1.5, 1.5, 1.5],'socket_list': ['fx_kaihuo_1', 'fx_kaihuo_3', 'fx_kaihuo_1', 'fx_kaihuo_3'],'bac_anim_name_list': ['attack_01_05', 'attack_01_05', 'attack_01_05', 'attack_01_05'],'atk_anim_dur_list': [0.4, 0.4, 0.4, 0.4],'aim_speed': 2.0},'action_state': 'MonsterMultiRange'},MC_RUN: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 3,'move_acc': 30,'run_speed': 15,'walk_speed': 11,'brake_acc': -30},'action_state': 'MonsterRun'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_MULTI_RANGE: {'custom_param': {'bac_anim_dur_list': [0.0, 0.4],'skill_id': 9033351,'fire_count': 2,'max_aim_dur': 2.0,'multi_fire_seq': [['fx_missile_1', 'fx_missile_2', 'fx_missile_5', 'fx_missile_6'], ['fx_missile_3', 'fx_missile_4', 'fx_missile_7', 'fx_missile_8']],'atk_anim_name_list': ['attack_01_04', ''],'bac_anim_rate_list': [1.0, 1.0],'pre_anim_dur_list': [0.5, 0.2],'pre_anim_rate_list': [1.0, 1.0],'pre_anim_name_list': ['attck_ready', 'attack_01_04'],'wp_list': [9033301, 9033301, 9033301, 9033301, 9033301, 9033301, 9033301, 9033301],'atk_anim_rate_list': [1.2, 1.0],'socket_list': ['fx_missile_1', 'fx_missile_2', 'fx_missile_3', 'fx_missile_4', 'fx_missile_5', 'fx_missile_6', 'fx_missile_7', 'fx_missile_8'],'bac_anim_name_list': ['attack_01_05', 'attack_01_05'],'atk_anim_dur_list': [0.9, 0.7],'aim_speed': 2.0},'action_state': 'MonsterMultiRange'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 1.0,'hit_anim': 'hit_front_00','hit_anim_dur': 0.33},'action_state': 'MonsterHit'},MC_IMMOBILIZE: {'action_param': (0, ['hit_front_00', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]