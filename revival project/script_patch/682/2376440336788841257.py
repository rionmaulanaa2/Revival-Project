# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90221.py
_reload_all = True
version = '196717342'
from .pve_monster_status_config import *
cover = {'90221': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_RUN, MC_STAND, MC_MOVE]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_RUN, MC_STAND, MC_MOVE]),
             MC_JUMP_1: set([MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_RUN, MC_STAND, MC_MOVE]),
             MC_MECHA_BOARDING: set([MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_HIT]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_RANGE, MC_MOVE, MC_IMMOBILIZE]),
             MC_MONSTER_AIMTURN: set([MC_TURN, MC_RUN, MC_STAND, MC_MOVE]),
             MC_MONSTER_POWER_MELEE: set([MC_TURN, MC_MONSTER_AIMTURN, MC_RUN, MC_STAND, MC_MOVE]),
             MC_TURN: set([MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_RUN, MC_STAND]),
             MC_MONSTER_MELEE: set([MC_TURN, MC_MONSTER_AIMTURN, MC_RUN, MC_STAND, MC_MOVE]),
             MC_RUN: set([MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_STAND, MC_MOVE]),
             MC_MONSTER_SUMMON: set([MC_TURN, MC_MONSTER_AIMTURN, MC_RUN, MC_STAND, MC_MOVE]),
             MC_MONSTER_RANGE: set([MC_TURN, MC_MONSTER_AIMTURN, MC_RUN, MC_STAND, MC_MOVE]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_IMMOBILIZE: set([MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_MONSTER_RANGE, MC_MONSTER_HIT]),
             MC_MONSTER_HIT: set([MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_RANGE, MC_MOVE]),
             MC_MONSTER_ROAR: set([MC_TURN, MC_MONSTER_AIMTURN, MC_RUN, MC_STAND, MC_MOVE]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_RUN, MC_MOVE])
             }
   }
forbid = {'90221': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_TURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_MELEE, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_RANGE, MC_MOVE, MC_IMMOBILIZE]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_POWER_MELEE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_SUMMON, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_MELEE, MC_RUN, MC_FROZEN, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_MELEE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_SUMMON: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_RANGE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_MONSTER_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_SUMMON, MC_FROZEN, MC_IMMOBILIZE]),
             MC_MONSTER_ROAR: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_SUMMON, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE])
             }
   }
behavior = {'90221': {MC_JUMP_3: {'action_param': (0, ['', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_rate': 1.2,'born_anim_dur': 3.1,'born_anim': 'attack_skill_beiji'},'action_state': 'MonsterBorn'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.2,'die_anim': 'base_die_stand_hit_from_front'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['base_idle_fight', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_AIMTURN: {'custom_param': {'skill_id': 9022155,'max_aim_dur': 1.2,'aim_right_anim': 'base_move_turn_right90','aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'aim_left_anim': 'base_move_turn_left90','aim_speed': 3.14},'action_state': 'MonsterAimTurn'},MC_MONSTER_POWER_MELEE: {'custom_param': {'hit_range': [15.0, 15.0, 31.0],'atk_anim_rate': 1.0,'pre_anim_dur': 1.3,'pre_anim': 'attack_super_hebaozhan','aim_turn': True,'pre_anim_rate': 1.5,'move_end_ts': 1.3,'bac_anim_dur': 1.7,'skill_id': 9022154,'bac_anim': '','atk_anim_dur': 0.2,'bac_anim_rate': 1.0,'move_start_ts': 1.1,'move_speed': 1000.0,'atk_anim': ''},'action_state': 'MonsterMelee'},MC_MONSTER_SUMMON: {'custom_param': {'sum_anim_name_list': [''],'skill_id': 9022151,'fire_count': 1,'max_aim_dur': 1.2,'aim_right_anim': 'base_move_turn_right90','bac_anim_dur_list': [1.0],'bac_anim_rate_list': [1.0],'pre_anim_dur_list': [1.8],'pre_anim_rate_list': [1.0],'pre_anim_name_list': ['attack_skill_shengchan'],'bac_anim_name_list': [''],'fire_socket_list': ['ps_egg1'],'aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'sum_anim_dur_list': [5.0],'sum_anim_rate_list': [1.0],'aim_left_anim': 'base_move_turn_left90','aim_speed': 3.14},'action_state': 'MonsterSummon'},MC_MONSTER_ROAR: {'custom_param': {'skill_id': 9022156,'anim_dur': 4.7,'anim_rate': 1.2,'anim_name': 'attack_special_1'},'action_state': 'MonsterRoar'},MC_MONSTER_MELEE: {'custom_param': {'hit_range': [15.0, 15.0, 26.0],'atk_anim_rate': 1.0,'pre_anim_dur': 1.1,'pre_anim': 'attack_skill_xulichuo','aim_turn': True,'pre_anim_rate': 1.4,'move_end_ts': 1.1,'bac_anim_dur': 1.7,'skill_id': 9022153,'bac_anim': '','atk_anim_dur': 0.2,'bac_anim_rate': 1.0,'move_start_ts': 0.1,'move_speed': 340.0,'atk_anim': ''},'action_state': 'MonsterMelee'},MC_RUN: {'action_param': (0, ['run', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.1,'move_acc': 3000,'run_speed': 16,'walk_speed': 13,'brake_acc': -3000},'action_state': 'MonsterRun'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['base_idle_fight', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_RANGE: {'custom_param': {'bac_anim_dur_list': [0.0, 0.0, 1.0],'skill_id': 9022152,'fire_count': 3,'max_aim_dur': 1.2,'aim_right_anim': 'base_move_turn_right90','bac_anim_rate_list': [1.0, 1.0, 1.0],'wp_pos': 1,'pre_anim_dur_list': [0.65, 0.2, 0.25],'pre_anim_rate_list': [1.0, 1.0, 1.0],'pre_anim_name_list': ['attack_skill_pentu', '', ''],'wp_list': [9022101],'atk_anim_rate_list': [1.0, 1.0, 1.0],'atk_anim_name_list': ['', '', ''],'fire_socket_list': ['fx_tail', 'fx_tail', 'fx_tail'],'aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'bac_anim_name_list': ['', '', ''],'atk_anim_dur_list': [0.3, 0.2, 0.2],'aim_left_anim': 'base_move_turn_left90','aim_speed': 3.14},'action_state': 'MonsterRange'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 1.0,'move_acc': 3000,'walk_speed': 13,'brake_acc': -3000},'action_state': 'MonsterWalk'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 1.0,'hit_anim': 'beaten_land_center_heavy','hit_anim_dur': 1.3},'action_state': 'MonsterHit'},MC_IMMOBILIZE: {'action_param': (0, ['attack_skill_beiji', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]