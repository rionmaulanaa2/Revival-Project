# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90209.py
_reload_all = True
version = '196717331'
from .pve_monster_status_config import *
cover = {'90209': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_RUN, MC_STAND]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_RUN, MC_STAND]),
             MC_JUMP_1: set([MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_RUN, MC_STAND]),
             MC_MECHA_BOARDING: set([MC_MONSTER_AIMTURN, MC_MONSTER_SCOUT, MC_MONSTER_HIT]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_MONSTER_AIMTURN: set([MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_RUN, MC_STAND]),
             MC_MONSTER_POWER_MELEE: set([MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_RUN, MC_STAND]),
             MC_TURN: set([MC_MONSTER_AIMTURN, MC_MONSTER_SCOUT, MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_SCOUT, MC_RUN, MC_STAND]),
             MC_MONSTER_SCOUT: set([MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_MONSTER_MELEE: set([MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_RUN, MC_STAND]),
             MC_RUN: set([MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_STAND]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_RUN]),
             MC_MONSTER_RANGE: set([MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_RUN, MC_STAND]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_HIT: set([MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MOVE, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_RUN, MC_STAND, MC_MONSTER_RANGE]),
             MC_IMMOBILIZE: set([MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_POWER_MELEE, MC_MONSTER_SCOUT, MC_MONSTER_MELEE, MC_MONSTER_RANGE, MC_MONSTER_HIT])
             }
   }
forbid = {'90209': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_POWER_MELEE, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_POWER_MELEE, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_TURN, MC_MOVE, MC_MONSTER_MELEE, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_RANGE, MC_IMMOBILIZE]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_POWER_MELEE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MOVE, MC_MONSTER_MELEE, MC_RUN, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_SCOUT: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_MELEE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_RANGE: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_POWER_MELEE, MC_MONSTER_MELEE, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_MONSTER_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN, MC_IMMOBILIZE]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN])
             }
   }
behavior = {'90209': {MC_JUMP_3: {'action_param': (0, ['', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_rate': 1.0,'born_anim_dur': 1.5,'born_anim': 'born'},'action_state': 'MonsterBorn'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'die_anim': 'death'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['gethitfront', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'skill_id': 9020952,'max_aim_dur': 1.2,'aim_right_anim': 'turn90right','aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'aim_left_anim': 'turn90left','aim_speed': 3.14},'action_state': 'MonsterAimTurn'},MC_MONSTER_POWER_MELEE: {'custom_param': {'hit_range': [10.0, 10.0, 20.0],'atk_anim_rate': 1.0,'pre_anim_dur': 0.13,'pre_anim': 'jumpbiteattack','aim_turn': True,'pre_anim_rate': 0.8,'move_end_ts': 1.1,'bac_anim_dur': 0.4,'skill_id': 9020956,'bac_anim': '','atk_anim_dur': 0.63,'bac_anim_rate': 1.0,'move_start_ts': 0.1,'move_speed': 280.0,'atk_anim': ''},'action_state': 'MonsterMelee'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 1.0,'move_acc': 3000,'walk_speed': 13,'brake_acc': -3000},'action_state': 'MonsterWalk'},MC_MONSTER_SCOUT: {'custom_param': {'skill_id': 9020954,'anim_dur': 8.0,'anim_rate': 1.0,'anim_name': 'idlelookaround'},'action_state': 'MonsterScout'},MC_MONSTER_MELEE: {'custom_param': {'hit_range': [10.0, 10.0, 20.0],'atk_anim_rate': 1.0,'pre_anim_dur': 0.27,'pre_anim': 'claws2hitcomboattack','aim_turn': True,'pre_anim_rate': 0.8,'move_end_ts': 1.2,'bac_anim_dur': 0.3,'skill_id': 9020955,'bac_anim': '','atk_anim_dur': 0.73,'bac_anim_rate': 1.0,'move_start_ts': 0.27,'move_speed': 120.0,'atk_anim': ''},'action_state': 'MonsterMelee'},MC_RUN: {'action_param': (0, ['run', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.1,'move_acc': 3000,'run_speed': 18,'walk_speed': 13,'brake_acc': -3000},'action_state': 'MonsterRun'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['idlebreathe', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_RANGE: {'custom_param': {'bac_anim_dur_list': [0.1],'skill_id': 9020951,'fire_count': 1,'max_aim_dur': 1.2,'aim_right_anim': 'turn90right','bac_anim_rate_list': [1.0],'wp_pos': 1,'pre_anim_dur_list': [0.4],'pre_anim_rate_list': [0.45],'pre_anim_name_list': ['spitattack'],'wp_list': [9020901],'atk_anim_rate_list': [1.0],'atk_anim_name_list': [''],'fire_socket_list': ['fx_mouse'],'aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'bac_anim_name_list': [''],'atk_anim_dur_list': [0.3],'aim_left_anim': 'turn90left','aim_speed': 3.14},'action_state': 'MonsterRange'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 1.0,'hit_anim': 'gethitfront','hit_anim_dur': 0.6},'action_state': 'MonsterHit'},MC_IMMOBILIZE: {'action_param': (0, ['gethitfront', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]