# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/9016.py
from __future__ import absolute_import
_reload_all = True
version = '171803523'
from .mecha_status_config import *
cover = {'9016': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
            MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
            MC_JUMP_1: set([MC_JUMP_3, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
            MC_SHOOT: set([]),
            MC_MECHA_BOARDING: set([]),
            MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_SHOOT, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
            MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_IMMOBILIZE, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
            MC_SECOND_WEAPON_ATTACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_IMMOBILIZE, MC_SHOOT, MC_MOVE, MC_STAND, MC_RUN]),
            MC_TURN: set([MC_STAND]),
            MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_RUN]),
            MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_IMMOBILIZE, MC_SHOOT, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
            MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_RUN]),
            MC_RUN: set([MC_JUMP_1, MC_TURN, MC_MOVE, MC_STAND]),
            MC_HIT: set([]),
            MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT])
            }
   }
forbid = {'9016': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD]),
            MC_JUMP_2: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD]),
            MC_JUMP_1: set([MC_JUMP_2, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK]),
            MC_SHOOT: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_SHOOT, MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK]),
            MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_SHOOT, MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
            MC_DEAD: set([]),
            MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_FROZEN, MC_SHOOT, MC_DEAD]),
            MC_SECOND_WEAPON_ATTACK: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD]),
            MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MOVE, MC_RUN]),
            MC_MOVE: set([MC_JUMP_2, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_MOVE]),
            MC_FROZEN: set([MC_DEAD]),
            MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK]),
            MC_RUN: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_SHOOT, MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK]),
            MC_HIT: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK]),
            MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_FROZEN, MC_SHOOT, MC_DEAD])
            }
   }
behavior = {'9016': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'action_param': (0, ['born', 'lower', 1]),'custom_param': {'anim_duration': 3},'action_state': 'Born'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_IMMOBILIZE: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_SHOOT: {'action_param': (0, ['attack', 'lower', 1, {'loop': True}]),'sound_param': [{'sound_name': ('Play_weapon_fire', ('gun', 'ak47'), ('gun_option', 'single')),'time': 0.0}],'custom_param': {'shoot_anim': ('attack', 'lower', 1)},'action_state': 'WeaponFire'},MC_DEAD: {'action_param': (0, ['die', 'lower', 1]),'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9001_blast'), ('monster_select', 'monster9001')),'time': 0.0}],'action_state': 'Die'},MC_BEAT_BACK: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_SECOND_WEAPON_ATTACK: {'sound_param': [{'sound_name': ('Play_weapon_fire', ('gun', 'rpg'), ('gun_option', 'single')),'time': 1.8}, {'sound_name': ('Play_weapon_fire', ('gun', 'rpg'), ('gun_option', 'single')),'time': 2.8}, {'sound_name': ('Play_weapon_fire', ('gun', 'rpg'), ('gun_option', 'single')),'time': 3.8}],'custom_param': {'post_time': 1.0,'pre_time': 1.8,'post_anim': 'skill_fire_02','cast_anim': 'skill_fire_01','pre_anim': 'skill_ready','cast_time': 1},'action_state': 'CastSkill'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MOVE: {'action_param': (0, ['move_f', 'lower', 1, {'loop': True}]),'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9003_run'), ('monster_select', 'monster9003')),'time': 0.0}],'custom_param': {'move_acc': 15,'walk_speed': 5,'brake_acc': -30},'action_state': 'Walk'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_RUN: {'action_param': (0, ['move_f', 'lower', 1, {'loop': True}]),'custom_param': {'move_acc': 15,'run_speed': 7,'walk_speed': 5,'brake_acc': -30},'action_state': 'Run'},MC_HIT: {'custom_param': {'hit_anim_duration': (1, 1),'hit_anim': ('hit', 'hit'),'hit_thresh': 300},'action_state': 'Hit'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]