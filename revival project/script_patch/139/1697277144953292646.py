# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90311.py
_reload_all = True
version = '199328622'
from .pve_monster_status_config import *
cover = {'90311': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_TURN, MC_STAND, MC_RUN, MC_MOVE]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_STAND, MC_RUN, MC_MOVE]),
             MC_JUMP_1: set([MC_MONSTER_POWER_MELEE, MC_TURN, MC_STAND, MC_RUN, MC_MOVE]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_FROZEN, MC_STAND, MC_RUN, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_IMMOBILIZE]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_3, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_STAND, MC_RUN, MC_MOVE]),
             MC_MONSTER_POWER_MELEE: set([MC_JUMP_3, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_STAND, MC_RUN, MC_MOVE]),
             MC_TURN: set([MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_RUN]),
             MC_MONSTER_MELEE: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_RUN, MC_MOVE]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_STAND, MC_RUN, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_RUN, MC_MOVE]),
             MC_RUN: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_MOVE]),
             MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_MONSTER_MELEE]),
             MC_MONSTER_HIT: set([MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_STAND, MC_RUN, MC_MOVE, MC_IMMOBILIZE]),
             MC_MONSTER_DASH: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_RUN, MC_MOVE])
             }
   }
forbid = {'90311': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_FROZEN, MC_IMMOBILIZE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_FROZEN, MC_STAND, MC_RUN, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_POWER_MELEE, MC_FROZEN]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_POWER_MELEE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_FROZEN, MC_RUN, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_MELEE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_RUN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_POWER_MELEE, MC_FROZEN, MC_MONSTER_HIT]),
             MC_MONSTER_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_MONSTER_DASH: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE])
             }
   }
behavior = {'90311': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 3,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve_three/pve_three_birth_shader.sfx','born_anim': 'act_show'},'action_state': 'MonsterBorn'},MC_DEAD: {'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9001_blast'), ('monster_select', 'monster9001')),'time': 0.0}],'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'max_aim_dur': 1.2,'aim_right_anim': 'turn_right','aim_speed': 3.14,'aim_left_anim_rate': 2.0,'aim_left_anim': 'turn_left','aim_right_anim_rate': 2.0},'action_state': 'MonsterAimTurn'},MC_MONSTER_POWER_MELEE: {'custom_param': {'hit_range': [12.0, 12.0, 24.0],'atk_anim_rate': 1.0,'pre_anim_dur': 0.4,'pre_anim': 'melee_2','aim_turn': True,'pre_anim_rate': 0.7,'move_end_ts': 0.7,'bac_anim_dur': 0.45,'skill_id': 9031152,'bac_anim': '','atk_anim_dur': 0.15,'bac_anim_rate': 1.0,'move_start_ts': 0.65,'move_speed': 1380.0,'atk_anim': ''},'action_state': 'MonsterMelee'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_DASH: {'custom_param': {'dash_speed_list': [1000.0],'skill_id': 9031155,'dash_type': 1,'end_aoe_skill_ids': [],'bac_anim_list': ['dash_03'],'bac_anim_dur_list': [1.5],'dash_anim_list': ['dash_02'],'bac_anim_rate_list': [1.0],'pre_anim_dur_list': [0.7],'dash_count': 1,'pre_anim_rate_list': [0.6],'begin_aoe_skill_ids': [],'pre_anim_list': ['dash_01'],'aim_turn': True,'col_info': [55.0, 55.0],'dash_anim_rate_list': [1.0],'dash_form': 2,'is_draw_col': True,'dash_dur_list': [0.6]},'action_state': 'MonsterDash'},MC_MONSTER_MELEE: {'custom_param': {'hit_range': [10, 10, 18.0],'skill_id': 9031151,'bac_anim': '','atk_anim_dur': 0.2,'atk_anim_rate': 1.0,'move_start_ts': 0.55,'pre_anim_dur': 0.3,'bac_anim_rate': 1.0,'move_speed': 1480.0,'pre_anim': 'melee_1','aim_turn': True,'pre_anim_rate': 0.6,'move_end_ts': 0.6,'atk_anim': '','is_draw_col': False,'bac_anim_dur': 0.6},'action_state': 'MonsterMelee'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_RUN: {'action_param': (0, ['run_front', 'lower', 1, {'loop': True}]),'custom_param': {'move_acc': 3000.0,'run_speed': 15,'dynamic_speed_rate': 0.0,'brake_acc': -3000.0,'walk_speed': 11},'action_state': 'MonsterRun'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9003_run'), ('monster_select', 'monster9003')),'time': 0.0}],'custom_param': {'move_acc': 3000.0,'dynamic_speed_rate': 0.0,'brake_acc': -3000.0,'walk_speed': 11},'action_state': 'MonsterWalk'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 1.0,'hit_anim': 'die_shock','hit_anim_dur': 0.3},'action_state': 'MonsterHit'},MC_IMMOBILIZE: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]