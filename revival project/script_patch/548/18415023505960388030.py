# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90101.py
_reload_all = True
version = '196717268'
from .pve_monster_status_config import *
cover = {'90101': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_RUN, MC_STAND, MC_MOVE, MC_MONSTER_STUN]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_RUN, MC_STAND, MC_MOVE, MC_MONSTER_STUN]),
             MC_JUMP_1: set([MC_TURN, MC_RUN, MC_STAND, MC_MOVE]),
             MC_MONSTER_HIT: set([MC_TURN, MC_RUN, MC_STAND, MC_MOVE]),
             MC_MECHA_BOARDING: set([MC_MONSTER_HIT]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_RANGE, MC_MOVE, MC_IMMOBILIZE]),
             MC_MONSTER_DASHATK: set([MC_RUN, MC_MOVE]),
             MC_MONSTER_POWER_MELEE: set([MC_RUN, MC_MOVE]),
             MC_TURN: set([MC_STAND]),
             MC_MONSTER_DASH: set([MC_RUN, MC_MOVE]),
             MC_MONSTER_ROAR: set([]),
             MC_MONSTER_MELEE: set([MC_RUN, MC_MOVE]),
             MC_RUN: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_MOVE]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_RUN, MC_MOVE]),
             MC_MONSTER_RANGE: set([]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_IMMOBILIZE: set([MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_STUN]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_STAND]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_3, MC_MONSTER_DASHATK, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_RANGE, MC_MOVE]),
             MC_MONSTER_STUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_HIT])
             }
   }
forbid = {'90101': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MONSTER_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_RUN, MC_FROZEN, MC_STAND, MC_MOVE, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_DASHATK, MC_MONSTER_DASH, MC_FROZEN]),
             MC_MONSTER_DASHATK: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MONSTER_POWER_MELEE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_RUN, MC_FROZEN, MC_MONSTER_RANGE, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MONSTER_DASH: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MONSTER_ROAR: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MONSTER_MELEE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_RUN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MONSTER_RANGE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_FROZEN: set([MC_DEAD]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_DASHATK, MC_MONSTER_DASH, MC_FROZEN]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_DASHATK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_DASH, MC_MONSTER_ROAR, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_STUN]),
             MC_MONSTER_STUN: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_IMMOBILIZE])
             }
   }
behavior = {'90101': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 3.0,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_born_02_shader.sfx','born_anim': 'attack_03'},'action_state': 'MonsterBorn'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 2.2,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['hit', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_DASHATK: {'custom_param': {'skill_id': 9010153,'max_rush_duration': 1.7,'miss_anim_duration': 1.5,'pre_anim': 'charge_start','miss_anim_rate': 1.0,'miss_anim': 'charge_atk01','aim_turn': True,'tick_interval': 0.03,'rush_anim_rate': 1.4,'max_rush_speed': 430,'begin_aoe_skill_id': 9010155,'rush_anim': 'charge_mid','col_info': [20, 50],'air_dash_end_speed': 30,'pre_anim_rate': 1.0,'is_draw_col': False,'dash_stepheight': 3.0,'end_aoe_skill_id': 9010156,'pre_anim_duration': 1.2,'end_brake_time': 1.5},'action_state': 'MonsterDashAtk'},MC_MONSTER_AIMTURN: {'custom_param': {'skill_id': 9010159,'max_aim_dur': 1.8,'aim_right_anim': 'turn_right','aim_right_anim_rate': 1.8,'aim_left_anim_rate': 1.8,'aim_left_anim': 'turn_left','aim_speed': 3.6},'action_state': 'MonsterAimTurn'},MC_MONSTER_POWER_MELEE: {'custom_param': {'hit_range': [11.0, 11.0, 37.0],'atk_anim_rate': 2.6,'pre_anim_dur': 1.1,'pre_anim': 'attack_01','aim_turn': True,'pre_anim_rate': 1.1,'move_end_ts': 1.2,'bac_anim_dur': 0.7,'skill_id': 9010152,'bac_anim': '','atk_anim_dur': 0.4,'bac_anim_rate': 1.5,'move_start_ts': 0.95,'move_speed': 290.0,'atk_anim': ''},'action_state': 'MonsterMelee'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_DASH: {'custom_param': {'dash_speed_list': [650.0],'skill_id': 9010160,'dash_type': 1,'end_aoe_skill_ids': [9010156],'bac_anim_list': ['charge_atk01'],'bac_anim_dur_list': [1.5],'dash_anim_list': ['charge_mid'],'bac_anim_rate_list': [1.0],'pre_anim_dur_list': [1.25],'dash_count': 1,'pre_anim_rate_list': [1.0],'begin_aoe_skill_ids': [],'pre_anim_list': ['charge_start'],'aim_turn': True,'col_info': [40, 60],'dash_anim_rate_list': [1.4],'dash_form': 2,'is_draw_col': False,'dash_dur_list': [1.1]},'action_state': 'MonsterDash'},MC_MONSTER_ROAR: {'custom_param': {'skill_id': 9010154,'anim_dur': 2.9,'anim_rate': 1.0,'anim_name': 'attack_03'},'action_state': 'MonsterRoar'},MC_MONSTER_MELEE: {'custom_param': {'hit_range': [11.0, 11.0, 30.0],'atk_anim_rate': 2.6,'pre_anim_dur': 0.6,'pre_anim': 'attack_02','aim_turn': True,'pre_anim_rate': 1.1,'move_end_ts': 0.6,'bac_anim_dur': 0.7,'skill_id': 9010151,'bac_anim': '','atk_anim_dur': 0.5,'bac_anim_rate': 1.8,'move_start_ts': 0.2,'move_speed': 120.0,'atk_anim': ''},'action_state': 'MonsterMelee'},MC_RUN: {'action_param': (0, ['run', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.3,'move_acc': 1000,'run_speed': 21,'walk_speed': 16,'brake_acc': -1000},'action_state': 'MonsterRun'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_RANGE: {'custom_param': {'bac_anim_dur_list': [0, 0.5],'skill_id': 9010157,'fire_count': 2,'max_aim_dur': 1.2,'wp_pos': 1,'pre_anim_dur_list': [1.0, 0],'pre_anim_rate_list': [1.0, 1.0],'pre_anim_name_list': ['remote_atk_start', ''],'wp_list': [9010103, 9010103],'atk_anim_rate_list': [1.0, 1.0],'atk_anim_name_list': ['remote_atk_shoot', 'remote_atk_shoot'],'fire_socket_list': ['fx_kaihuo', 'fx_kaihuo'],'bac_anim_name_list': ['', 'remote_atk_end'],'atk_anim_dur_list': [0.5, 0.5],'bac_anim_rate_list': [1.0, 1.0],'aim_speed': 5},'action_state': 'MonsterRange'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.9,'move_acc': 1000,'walk_speed': 16,'brake_acc': -1000},'action_state': 'MonsterWalk'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 1.0,'hit_anim': 'hit','hit_anim_dur': 0.7},'action_state': 'MonsterHit'},MC_IMMOBILIZE: {'action_param': (0, ['hit', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_MONSTER_STUN: {'custom_param': {'stun_anim': 'beaten_loop','pre_anim': 'beaten_start','bac_anim': 'beaten_end','bac_anim_rate': 1.0,'pre_anim_rate': 1.0,'pre_anim_dur': 1.06,'stun_anim_rate': 1.0,'bac_anim_dur': 1.46},'action_state': 'MonsterStun'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]