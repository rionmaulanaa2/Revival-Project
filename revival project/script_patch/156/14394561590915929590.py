# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90232.py
_reload_all = True
version = '196717352'
from .pve_monster_status_config import *
cover = {'90232': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_JUMP_1: set([MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_LAUNCHER]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_IMMOBILIZE, MC_MONSTER_LAUNCHER]),
             MC_MONSTER_AIMTURN: set([MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_OBLIQUE, MC_MONSTER_LAUNCHER]),
             MC_TURN: set([MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_MONSTER_AIMTURN, MC_TURN, MC_RUN, MC_STAND]),
             MC_MONSTER_RANGE: set([MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_RUN: set([MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_STAND]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN]),
             MC_MONSTER_OBLIQUE: set([MC_TURN, MC_MOVE, MC_RUN, MC_STAND]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_LAUNCHER]),
             MC_MONSTER_HIT: set([MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_STAND, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_MONSTER_LAUNCHER]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_MONSTER_LAUNCHER]),
             MC_MONSTER_LAUNCHER: set([MC_TURN, MC_MOVE, MC_RUN, MC_STAND])
             }
   }
forbid = {'90232': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_IMMOBILIZE, MC_MONSTER_LAUNCHER]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_IMMOBILIZE, MC_MONSTER_LAUNCHER]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_IMMOBILIZE, MC_MONSTER_LAUNCHER]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_RUN, MC_FROZEN, MC_STAND, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_DEAD, MC_FROZEN]),
             MC_MONSTER_AIMTURN: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MOVE, MC_RUN, MC_FROZEN, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_LAUNCHER]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_LAUNCHER]),
             MC_MONSTER_RANGE: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_MONSTER_OBLIQUE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_LAUNCHER]),
             MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_LAUNCHER]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_LAUNCHER]),
             MC_MONSTER_OBLIQUE: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE, MC_MONSTER_LAUNCHER]),
             MC_FROZEN: set([MC_DEAD]),
             MC_MONSTER_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN, MC_IMMOBILIZE]),
             MC_IMMOBILIZE: set([MC_DEAD, MC_FROZEN]),
             MC_MONSTER_LAUNCHER: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_FROZEN, MC_MONSTER_OBLIQUE, MC_MONSTER_RANGE, MC_MONSTER_HIT, MC_IMMOBILIZE])
             }
   }
behavior = {'90232': {MC_JUMP_3: {'action_param': (0, ['shixianggui_guard', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['shixianggui_guard', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['shixianggui_guard', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_rate': 1.5,'born_anim_dur': 3.8,'born_anim': 'shixianggui_spawn'},'action_state': 'MonsterBorn'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'die_anim': 'shixianggui_die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['hitback', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'skill_id': 9023252,'max_aim_dur': 1.0,'aim_right_anim': 'shixianggui_walk','aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'aim_left_anim': 'shixianggui_walk','aim_speed': 7.2},'action_state': 'MonsterAimTurn'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.3,'move_acc': 1000,'walk_speed': 11,'brake_acc': -3000},'action_state': 'MonsterWalk'},MC_RUN: {'action_param': (0, ['run', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.1,'move_acc': 1000,'run_speed': 18,'walk_speed': 11,'brake_acc': -3000},'action_state': 'MonsterRun'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['shixianggui_guard', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_OBLIQUE: {'custom_param': {'max_dash_dis': 100,'skill_id': 9023254,'bac_anim': '','idl_anim_dur': 1.5,'atk_anim_rate': 0.7,'atk_anim_dur': 0.5,'pre_anim_dur': 0.9,'aim_turn': True,'idl_anim_rate': 1.0,'bac_anim_rate': 0.8,'pre_anim': 'skill_omni02_pre','end_aoe_skill_id': 9023255,'focus_dis': 2.0,'focus_time': 0.8,'pre_anim_rate': 1.0,'atk_anim': 'skill_omni02_cast','idl_anim': 'skill_omni02_idle','bac_anim_dur': 0.3},'action_state': 'MonsterOblique'},MC_MONSTER_RANGE: {'custom_param': {'bac_anim_dur_list': [0.8],'skill_id': 9023251,'fire_count': 1,'max_aim_dur': 0.8,'wp_pos': 1,'pre_anim_dur_list': [0.7],'pre_anim_rate_list': [0.7],'pre_anim_name_list': ['shixianggui_attack'],'wp_list': [9023201],'atk_anim_rate_list': [0.9],'atk_anim_name_list': [''],'fire_socket_list': ['fx_righthand'],'bac_anim_name_list': [''],'atk_anim_dur_list': [0.2],'bac_anim_rate_list': [1.0],'aim_speed': 5},'action_state': 'MonsterRange'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 1.0,'hit_anim': 'hitback','hit_anim_dur': 0.6},'action_state': 'MonsterHit'},MC_IMMOBILIZE: {'action_param': (0, ['hitback', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_MONSTER_LAUNCHER: {'custom_param': {'bac_anim_dur_list': [1.35],'fire_count': 1,'bac_anim_rate_list': [1.0],'atk_anim_name_list': [''],'skill_id': 9023256,'pre_anim_name_list': ['shixianggui_attack02'],'max_aim_dur': 1.0,'offset_angle': -90.0,'atk_anim_rate_list': [1.0],'aim_right_anim': 'shixianggui_walk','aim_right_anim_rate': 1.0,'pre_anim_dur_list': [1.5],'wp_list': [9023201],'aim_left_anim_rate': 1.0,'atk_anim_dur_list': [0],'aim_left_anim': 'shixianggui_walk','end_aoe_skill_id_list': [9023255],'fire_socket_list': ['fx_dilie_huoquan'],'end_aoe_skill_id_2_list': [9023257],'main_angle': 90.0,'wp_pos': 1,'pre_anim_rate_list': [1.0],'spin_seq': [-96, -108, -120, -132, -144, -158.0, -170.0, -84, -72, -60, -48, -36, -24.0, -12.0, 0.0, 12.0, 24.0, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144, 156, 169.0, 180.0],'bac_anim_name_list': [''],'aim_speed': 7.2},'action_state': 'MonsterLauncher'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]