# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90226.py
_reload_all = True
version = '196717348'
from .pve_monster_status_config import *
cover = {'90226': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_TURN, MC_STAND, MC_RUN, MC_MOVE]),
             MC_JUMP_2: set([MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_TURN, MC_STAND, MC_RUN, MC_MOVE]),
             MC_JUMP_1: set([MC_MECHA_BOARDING, MC_TURN, MC_STAND, MC_RUN, MC_MOVE]),
             MC_MONSTER_HIT: set([MC_MONSTER_AIMTURN, MC_MONSTER_EVADE, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_MONSTER_SUB_EVADE, MC_STAND, MC_RUN, MC_MOVE]),
             MC_MECHA_BOARDING: set([MC_MONSTER_HIT]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_EVADE, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_STAND, MC_RUN, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_MELEE, MC_STAND, MC_RUN, MC_MOVE, MC_IMMOBILIZE]),
             MC_MONSTER_AIMTURN: set([MC_MECHA_BOARDING, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_STAND, MC_RUN, MC_MOVE]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_EVADE, MC_MONSTER_POWER_MELEE, MC_MONSTER_MELEE, MC_MONSTER_SUB_EVADE, MC_MONSTER_HIT]),
             MC_MONSTER_POWER_MELEE: set([MC_MECHA_BOARDING, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_STAND, MC_RUN, MC_MOVE]),
             MC_TURN: set([MC_MECHA_BOARDING, MC_STAND]),
             MC_MONSTER_DASH: set([MC_MECHA_BOARDING, MC_MONSTER_AIMTURN, MC_TURN, MC_STAND, MC_RUN, MC_MOVE]),
             MC_MONSTER_MELEE: set([MC_MECHA_BOARDING, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_STAND, MC_RUN, MC_MOVE]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_EVADE, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_MONSTER_SUB_EVADE, MC_STAND, MC_RUN, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_RUN, MC_MOVE]),
             MC_RUN: set([MC_MECHA_BOARDING, MC_MONSTER_AIMTURN, MC_TURN, MC_STAND, MC_MOVE]),
             MC_MOVE: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_MONSTER_AIMTURN, MC_TURN, MC_STAND, MC_RUN]),
             MC_MONSTER_SUB_EVADE: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_STAND, MC_RUN, MC_MOVE, MC_IMMOBILIZE]),
             MC_MONSTER_EVADE: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_STAND, MC_RUN, MC_MOVE, MC_IMMOBILIZE])
             }
   }
forbid = {'90226': {MC_JUMP_3: set([MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_EVADE, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_EVADE, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_EVADE, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_IMMOBILIZE]),
             MC_MONSTER_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN, MC_IMMOBILIZE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_EVADE, MC_TURN, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_STAND, MC_RUN, MC_MOVE, MC_IMMOBILIZE]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_DEAD, MC_MONSTER_DASH, MC_FROZEN]),
             MC_MONSTER_AIMTURN: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_EVADE, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_IMMOBILIZE: set([MC_DEAD, MC_MONSTER_DASH, MC_FROZEN]),
             MC_MONSTER_POWER_MELEE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_EVADE, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_EVADE, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_RUN, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_DASH: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_EVADE, MC_MONSTER_POWER_MELEE, MC_MONSTER_MELEE, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_MELEE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_EVADE, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_EVADE, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_EVADE, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_EVADE, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_SUB_EVADE: set([MC_DEAD, MC_MONSTER_EVADE, MC_FROZEN, MC_MONSTER_HIT]),
             MC_MONSTER_EVADE: set([MC_DEAD, MC_MONSTER_SUB_EVADE, MC_FROZEN, MC_MONSTER_HIT])
             }
   }
behavior = {'90226': {MC_JUMP_3: {'action_param': (0, ['base_idle_stand', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['base_idle_stand', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['base_idle_stand', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_rate': 1.0,'born_anim_dur': 1.2,'born_anim': 'attack_shouji_front_medium'},'action_state': 'MonsterBorn'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'die_anim': 'base_die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['attack_shouji_back_heavy', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'max_aim_dur': 1.0,'aim_right_anim': 'walk_f','aim_speed': 5,'aim_left_anim_rate': 1.0,'aim_left_anim': 'walk_f','aim_right_anim_rate': 1.0},'action_state': 'MonsterAimTurn'},MC_MONSTER_EVADE: {'custom_param': {'turn_start_ts': 0.1,'skill_id': 9022654,'bac_anim': '','land_anim_rate': 1.0,'pre_anim_dur': 0.15,'evd_speed': 850,'gravity': 1000,'bac_anim_rate': 1.0,'max_evd_time': 0.35,'pre_anim': 'attack_dodge_left','turn_speed': 12,'land_anim': '','pre_anim_rate': 1.0,'evd_anim_rate': 1.0,'land_anim_dur': 0.0,'evd_anim': '','bac_anim_dur': 0.4},'action_state': 'MonsterEvade'},MC_MONSTER_POWER_MELEE: {'custom_param': {'hit_range': [10.0, 10.0, 14.0],'atk_anim_rate': 1.0,'pre_anim_dur': 0.45,'pre_anim': 'attack_skill_rush_scratch_down','aim_turn': True,'pre_anim_rate': 1.0,'move_end_ts': 0.55,'bac_anim_dur': 0.4,'skill_id': 9022652,'bac_anim': '','atk_anim_dur': 0.15,'bac_anim_rate': 1.0,'move_start_ts': 0.15,'move_speed': 280.0,'atk_anim': ''},'action_state': 'MonsterMelee'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_DASH: {'custom_param': {'dash_speed_list': [450.0],'skill_id': 9022653,'dash_type': 1,'end_aoe_skill_ids': [],'bac_anim_list': [''],'bac_anim_dur_list': [0.55],'dash_anim_list': [''],'bac_anim_rate_list': [1.0],'pre_anim_dur_list': [0.35],'dash_count': 1,'pre_anim_rate_list': [0.7],'begin_aoe_skill_ids': [],'pre_anim_list': ['attack_skill_rush_gnaw'],'aim_turn': True,'col_info': [30.0, 20.0],'dash_anim_rate_list': [1.3],'dash_form': 2,'is_draw_col': False,'dash_dur_list': [0.6]},'action_state': 'MonsterDash'},MC_MONSTER_MELEE: {'custom_param': {'hit_range': [10, 10.0, 12],'atk_anim_rate': 1.0,'pre_anim_dur': 0.35,'pre_anim': 'attack_skill_scratch_up','aim_turn': True,'pre_anim_rate': 1.0,'move_end_ts': 0.4,'bac_anim_dur': 0.4,'skill_id': 9022651,'bac_anim': '','atk_anim_dur': 0.15,'bac_anim_rate': 1.0,'move_start_ts': 0.2,'move_speed': 90.0,'atk_anim': ''},'action_state': 'MonsterMelee'},MC_MONSTER_SUB_EVADE: {'custom_param': {'turn_start_ts': 0.1,'skill_id': 9022655,'bac_anim': '','land_anim_rate': 1.0,'pre_anim_dur': 0.15,'evd_speed': 850,'gravity': 1000,'bac_anim_rate': 1.0,'max_evd_time': 0.35,'pre_anim': 'attack_dodge_right','turn_speed': 12,'land_anim': '','pre_anim_rate': 1.0,'evd_anim_rate': 1.0,'land_anim_dur': 0.0,'evd_anim': '','bac_anim_dur': 0.4},'action_state': 'MonsterEvade'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['base_idle_stand', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_RUN: {'action_param': (0, ['run', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0,'move_acc': 1000,'run_speed': 14,'walk_speed': 8,'brake_acc': -3000},'action_state': 'MonsterRun'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.5,'move_acc': 1000,'walk_speed': 8,'brake_acc': -3000},'action_state': 'MonsterWalk'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 1.0,'hit_anim': 'attack_shouji_back_heavy','hit_anim_dur': 1.6},'action_state': 'MonsterHit'},MC_IMMOBILIZE: {'action_param': (0, ['attack_shouji_back_heavy', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]