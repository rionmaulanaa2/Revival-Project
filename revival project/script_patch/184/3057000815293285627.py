# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90331.py
_reload_all = True
version = '199331346'
from .pve_monster_status_config import *
cover = {'90331': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_RUN, MC_MOVE, MC_STAND]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_RUN, MC_MOVE, MC_STAND]),
             MC_JUMP_1: set([MC_TURN, MC_RUN, MC_MOVE, MC_STAND]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_DASH, MC_RUN, MC_FROZEN, MC_MONSTER_RAISE_SHIELD, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MOVE, MC_IMMOBILIZE, MC_STAND]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_MONSTER_RAISE_SHIELD, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_MOVE, MC_STAND]),
             MC_TURN: set([MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_STAND]),
             MC_MONSTER_RANGE: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_MOVE, MC_STAND]),
             MC_RUN: set([MC_JUMP_3, MC_TURN, MC_MOVE, MC_STAND]),
             MC_MONSTER_RAISE_SHIELD: set([MC_JUMP_3, MC_RUN]),
             MC_MONSTER_POWER_RANGE: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_MOVE, MC_STAND]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_DASH, MC_RUN, MC_MONSTER_RAISE_SHIELD, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MOVE, MC_IMMOBILIZE, MC_STAND]),
             MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_MONSTER_RAISE_SHIELD, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE]),
             MC_MONSTER_DASH: set([MC_TURN, MC_RUN, MC_MOVE, MC_STAND]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_RUN, MC_MOVE])
             }
   }
forbid = {'90331': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_RAISE_SHIELD, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_RAISE_SHIELD, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_RAISE_SHIELD, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_DASH, MC_RUN, MC_FROZEN, MC_MONSTER_RAISE_SHIELD, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MOVE, MC_IMMOBILIZE, MC_STAND]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASH, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_RUN, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_MOVE, MC_IMMOBILIZE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_MONSTER_RANGE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_FROZEN, MC_MONSTER_RAISE_SHIELD, MC_MONSTER_POWER_RANGE, MC_IMMOBILIZE]),
             MC_RUN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_FROZEN, MC_MONSTER_RAISE_SHIELD, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_MONSTER_RAISE_SHIELD: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASH, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_MONSTER_POWER_RANGE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_FROZEN, MC_MONSTER_RAISE_SHIELD, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_MONSTER_DASH: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_RAISE_SHIELD, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_FROZEN, MC_MONSTER_POWER_RANGE, MC_MONSTER_RANGE, MC_IMMOBILIZE])
             }
   }
behavior = {'90331': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 3.0,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_born_02_shader.sfx','born_anim': 'mount'},'action_state': 'MonsterBorn'},MC_DEAD: {'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9001_blast'), ('monster_select', 'monster9001')),'time': 0.0}],'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 0,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'max_aim_dur': 1.2,'aim_right_anim': 'turnright_90','aim_speed': 3.14,'aim_left_anim_rate': 1.0,'aim_left_anim': 'turnleft_90','aim_right_anim_rate': 1.0},'action_state': 'MonsterAimTurn'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_DASH: {'custom_param': {'dash_speed_list': [1800.0],'skill_id': 9033154,'dash_type': 1,'end_aoe_skill_ids': [],'bac_anim_list': ['dash_03'],'bac_anim_dur_list': [1.4],'dash_anim_list': ['dash_02'],'bac_anim_rate_list': [1.2],'pre_anim_dur_list': [0.4],'dash_count': 1,'pre_anim_rate_list': [0.6],'begin_aoe_skill_ids': [],'pre_anim_list': ['dash_01'],'aim_turn': True,'col_info': [90.0, 103.5],'dash_anim_rate_list': [1.0],'dash_form': 2,'is_draw_col': True,'dash_dur_list': [0.5]},'action_state': 'MonsterDash'},MC_RUN: {'action_param': (0, ['run', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0,'move_acc': 30,'run_speed': 15,'walk_speed': 11,'brake_acc': -30},'action_state': 'MonsterRun'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_MONSTER_RAISE_SHIELD: {'custom_param': {'pre_anim_dur': 0.1,'pre_anim': 'shd_start','aim_turn': False,'pre_anim_rate': 1.0,'bac_anim_dur': 0.533,'skill_id': 9033153,'bac_anim': 'shd_end','shield_sfx_socket': 'fx_dun','max_shield_time': 15,'shield_col_size': [1.0, 4.2, 4.8],'bac_anim_rate': 1.0,'shield_sfx_res': 'effect/fx/monster/pve_three/pve_three_dun.sfx'},'action_state': 'MonsterRaiseShield'},MC_MONSTER_POWER_RANGE: {'custom_param': {'bac_anim_dur_list': [0.0, 0.0, 1.4],'skill_id': 9033152,'fire_count': 3,'max_aim_dur': 0.8,'aim_right_anim': 'turnright_90','bac_anim_rate_list': [1.0, 1.0, 1.0],'wp_pos': 1,'pre_anim_dur_list': [0.8, 0.0, 0.0],'pre_anim_rate_list': [1.0, 1.0, 1.0],'pre_anim_name_list': ['shoot_idle', 'shoot_idle', 'shoot_idle'],'wp_list': [9033102],'atk_anim_rate_list': [1.0, 1.0, 1.0],'atk_anim_name_list': ['shoot', 'shoot', 'shoot'],'fire_socket_list': ['fx_kaihuo', 'fx_kaihuo', 'fx_kaihuo'],'aim_right_anim_rate': 1.3,'aim_left_anim_rate': 1.3,'bac_anim_name_list': ['', '', 'reload'],'atk_anim_dur_list': [0.4, 0.4, 0.4],'aim_left_anim': 'turnleft_90','aim_speed': 5},'action_state': 'MonsterRange'},MC_MONSTER_RANGE: {'custom_param': {'bac_anim_dur_list': [1.5],'skill_id': 9033151,'fire_count': 1,'max_aim_dur': 1.2,'aim_right_anim': 'turnright_90','bac_anim_rate_list': [1.0],'wp_pos': 1,'pre_anim_dur_list': [0.3],'pre_anim_rate_list': [0.5],'pre_anim_name_list': ['pan_start'],'wp_list': [9033101],'atk_anim_rate_list': [1.0],'atk_anim_name_list': ['pan_fire_pinjie'],'fire_socket_list': ['fx_kaihuo'],'aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'bac_anim_name_list': [''],'atk_anim_dur_list': [0.5],'aim_left_anim': 'turnleft_90','aim_speed': 3.14},'action_state': 'MonsterRange'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0,'move_acc': 30,'walk_speed': 11,'brake_acc': -30},'action_state': 'MonsterWalk'},MC_IMMOBILIZE: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]