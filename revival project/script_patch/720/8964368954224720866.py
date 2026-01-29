# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90205.py
_reload_all = True
version = '196717328'
from .pve_monster_status_config import *
cover = {'90205': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_TURN, MC_STAND]),
             MC_JUMP_2: set([MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_TURN, MC_STAND]),
             MC_JUMP_1: set([MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_TURN, MC_STAND]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_FROZEN, MC_MOVE, MC_IMMOBILIZE, MC_BEAT_BACK, MC_MONSTER_FLAME, MC_TURN, MC_MONSTER_ROAR, MC_STAND, MC_MONSTER_RANGE]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_IMMOBILIZE, MC_MONSTER_FLAME, MC_TURN, MC_MONSTER_ROAR, MC_STAND, MC_MONSTER_RANGE]),
             MC_MONSTER_FLAME: set([MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_TURN, MC_STAND]),
             MC_TURN: set([MC_MECHA_BOARDING, MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_RUN, MC_TURN, MC_STAND]),
             MC_MONSTER_ROAR: set([MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_TURN, MC_STAND]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_IMMOBILIZE, MC_BEAT_BACK, MC_MONSTER_FLAME, MC_TURN, MC_MONSTER_ROAR, MC_STAND, MC_MONSTER_RANGE]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_TURN]),
             MC_MONSTER_RANGE: set([MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_TURN, MC_STAND]),
             MC_RUN: set([MC_MECHA_BOARDING, MC_MOVE, MC_TURN, MC_STAND]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_FLAME, MC_MONSTER_ROAR, MC_MONSTER_RANGE])
             }
   }
forbid = {'90205': {MC_JUMP_3: set([MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_MONSTER_FLAME, MC_MONSTER_ROAR, MC_MONSTER_RANGE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_MONSTER_FLAME, MC_MONSTER_ROAR, MC_MONSTER_RANGE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_FLAME, MC_MONSTER_ROAR, MC_MONSTER_RANGE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_RUN, MC_FROZEN, MC_MOVE, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_TURN, MC_STAND]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_FROZEN, MC_DEAD]),
             MC_MONSTER_FLAME: set([MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_ROAR, MC_MONSTER_RANGE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_RUN, MC_FROZEN, MC_MOVE, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_FLAME, MC_MONSTER_ROAR, MC_MONSTER_RANGE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_FLAME, MC_MONSTER_ROAR, MC_MONSTER_RANGE]),
             MC_MONSTER_ROAR: set([MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_FLAME, MC_MONSTER_RANGE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_FLAME, MC_MONSTER_ROAR, MC_MONSTER_RANGE]),
             MC_MONSTER_RANGE: set([MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_FLAME, MC_MONSTER_ROAR]),
             MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_FLAME, MC_MONSTER_ROAR, MC_MONSTER_RANGE]),
             MC_IMMOBILIZE: set([MC_FROZEN, MC_DEAD])
             }
   }
behavior = {'90205': {MC_JUMP_3: {'action_param': (0, ['flystationary', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['flystationary', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['flystationary', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_rate': 2.0,'born_anim_dur': 2.0,'born_anim': 'takeoff'},'action_state': 'MonsterBorn'},MC_RUN: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.3,'move_acc': 5,'run_speed': 15,'walk_speed': 12,'brake_acc': -5},'action_state': 'MonsterRun'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_MOVE: {'action_param': (0, ['flystationary', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.3,'move_acc': 5,'walk_speed': 12,'brake_acc': -5},'action_state': 'MonsterWalk'},MC_IMMOBILIZE: {'action_param': (0, ['glidegethit', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.5,'die_anim': 'flystationarygethittofalling'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['glidegethit', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_FLAME: {'custom_param': {'hit_range': [10.0, 15.0, 27.0],'height_offset': -30.0,'bac_anim': None,'atk_anim_dur': 2.2,'atk_anim_rate': 0.7,'skill_id': 9020553,'move_start_ts': 0.3,'pre_anim_dur': 0.4,'move_speed': 80.0,'bac_anim_rate': 1.0,'hit_seq': [0.0, 5.0, 15.0, 5.0, 0.0, -5.0, -15.0, -20.0],'pre_anim': 'flystationaryroaregybreath','aim_turn': False,'forward_offset': 23.0,'pre_anim_rate': 0.6,'move_end_ts': 2.7,'atk_anim': None,'is_draw_col': False,'bac_anim_dur': 0.3,'hit_interval': 0.36},'action_state': 'MonsterFlame'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_ROAR: {'custom_param': {'skill_id': 9020552,'anim_dur': 3.0,'anim_rate': 1.0,'anim_name': 'flystationaryroaregybreath'},'action_state': 'MonsterRoar'},MC_STAND: {'action_param': (0, ['flystationary', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_RANGE: {'custom_param': {'bac_anim_dur_list': [0.2],'skill_id': 9020551,'fire_count': 1,'max_aim_dur': 1.5,'aim_right_anim': 'flystationary','bac_anim_rate_list': [1.0],'wp_pos': 1,'pre_anim_dur_list': [0.45],'pre_anim_rate_list': [0.7],'pre_anim_name_list': ['flystationaryspitenergyball'],'wp_list': [9020501],'atk_anim_rate_list': [0.7],'atk_anim_name_list': [''],'fire_socket_list': ['fx_mouth_fire'],'aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'bac_anim_name_list': [''],'atk_anim_dur_list': [0.1],'aim_left_anim': 'flystationary','aim_speed': 3.14},'action_state': 'MonsterRange'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]