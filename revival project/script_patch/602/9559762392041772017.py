# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90215.py
_reload_all = True
version = '196717335'
from .pve_monster_status_config import *
cover = {'90215': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_TURN, MC_STAND]),
             MC_JUMP_2: set([MC_JUMP_1, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_TURN, MC_STAND]),
             MC_JUMP_1: set([MC_RUN, MC_MOVE, MC_TURN, MC_STAND]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_FROZEN, MC_MOVE, MC_MONSTER_ROAR, MC_BEAT_BACK, MC_TURN, MC_IMMOBILIZE, MC_STAND, MC_MONSTER_RANGE, MC_MONSTER_DASH]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_RUN, MC_MOVE, MC_MONSTER_ROAR, MC_TURN, MC_IMMOBILIZE, MC_STAND, MC_MONSTER_RANGE, MC_MONSTER_DASH]),
             MC_TURN: set([MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_RUN, MC_TURN, MC_STAND]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_MONSTER_ROAR, MC_BEAT_BACK, MC_TURN, MC_IMMOBILIZE, MC_STAND, MC_MONSTER_RANGE, MC_MONSTER_DASH]),
             MC_STAND: set([MC_JUMP_3, MC_RUN, MC_MOVE, MC_TURN]),
             MC_MONSTER_RANGE: set([MC_RUN, MC_MOVE, MC_MONSTER_ROAR, MC_TURN, MC_STAND]),
             MC_RUN: set([MC_MOVE, MC_TURN, MC_STAND]),
             MC_IMMOBILIZE: set([MC_MONSTER_ROAR, MC_BEAT_BACK, MC_MONSTER_RANGE, MC_MONSTER_DASH]),
             MC_MONSTER_ROAR: set([MC_RUN, MC_MOVE, MC_TURN, MC_STAND]),
             MC_MONSTER_DASH: set([MC_RUN, MC_MOVE, MC_TURN, MC_STAND])
             }
   }
forbid = {'90215': {MC_JUMP_3: set([MC_FROZEN, MC_MONSTER_ROAR, MC_DEAD, MC_IMMOBILIZE, MC_MONSTER_RANGE, MC_MONSTER_DASH]),
             MC_JUMP_2: set([MC_JUMP_3, MC_FROZEN, MC_MONSTER_ROAR, MC_DEAD, MC_IMMOBILIZE, MC_MONSTER_RANGE, MC_MONSTER_DASH]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_FROZEN, MC_MONSTER_ROAR, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_MONSTER_RANGE, MC_MONSTER_DASH]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_RUN, MC_FROZEN, MC_MOVE, MC_DEAD, MC_BEAT_BACK, MC_TURN, MC_IMMOBILIZE, MC_STAND]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_FROZEN, MC_MOVE, MC_MONSTER_ROAR, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_MONSTER_RANGE, MC_MONSTER_DASH]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_MONSTER_ROAR, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_MONSTER_RANGE, MC_MONSTER_DASH]),
             MC_FROZEN: set([MC_DEAD]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_MONSTER_ROAR, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_MONSTER_RANGE, MC_MONSTER_DASH]),
             MC_MONSTER_RANGE: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_MONSTER_DASH]),
             MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_MONSTER_ROAR, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_MONSTER_RANGE, MC_MONSTER_DASH]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD]),
             MC_MONSTER_ROAR: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_MONSTER_RANGE, MC_MONSTER_DASH]),
             MC_MONSTER_DASH: set([MC_MECHA_BOARDING, MC_FROZEN, MC_MONSTER_ROAR, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_MONSTER_DASH])
             }
   }
behavior = {'90215': {MC_JUMP_3: {'action_param': (0, ['fly', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['fly', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['fly', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_rate': 2.0,'born_anim_dur': 2.0,'born_anim': 'flybiteattack'},'action_state': 'MonsterBorn'},MC_RUN: {'action_param': (0, ['fly', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0,'move_acc': 10,'run_speed': 15,'walk_speed': 12,'brake_acc': -10},'action_state': 'MonsterRun'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0,'move_acc': 10,'walk_speed': 12,'brake_acc': -10},'action_state': 'MonsterWalk'},MC_MONSTER_ROAR: {'custom_param': {'skill_id': 9021552,'anim_dur': 2.0,'anim_rate': 1.0,'anim_name': 'flytaunt'},'action_state': 'MonsterRoar'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'die_anim': 'deathhittheground'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['flygethit', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_IMMOBILIZE: {'action_param': (0, ['flygethit', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_STAND: {'action_param': (0, ['fly', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_RANGE: {'custom_param': {'bac_anim_dur_list': [0.2],'skill_id': 9021551,'fire_count': 1,'max_aim_dur': 1.5,'aim_right_anim': 'fly','bac_anim_rate_list': [1.0],'wp_pos': 1,'pre_anim_dur_list': [1.1],'pre_anim_rate_list': [1.8],'pre_anim_name_list': ['flyspitready'],'wp_list': [9021501],'atk_anim_rate_list': [1.2],'atk_anim_name_list': ['flystingerattack'],'fire_socket_list': ['fx_tail'],'aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'bac_anim_name_list': [''],'atk_anim_dur_list': [0.5],'aim_left_anim': 'fly','aim_speed': 3.14},'action_state': 'MonsterRange'},MC_MONSTER_DASH: {'custom_param': {'dash_speed_list': [330],'skill_id': 9021553,'dash_type': 1,'end_aoe_skill_ids': [],'bac_anim_list': [''],'bac_anim_dur_list': [0.1],'dash_anim_list': [''],'bac_anim_rate_list': [1.0],'pre_anim_dur_list': [0.2],'dash_count': 1,'pre_anim_rate_list': [1.0],'begin_aoe_skill_ids': [],'pre_anim_list': ['flyspitattack'],'aim_turn': False,'col_info': [5, 5],'dash_anim_rate_list': [1.0],'dash_form': 2,'is_draw_col': False,'dash_dur_list': [0.3]},'action_state': 'MonsterDash'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]