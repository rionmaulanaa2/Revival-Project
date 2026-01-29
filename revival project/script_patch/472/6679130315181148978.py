# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/9011.py
from __future__ import absolute_import
_reload_all = True
version = '171803505'
from .mecha_status_config import *
cover = {'9011': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
            MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
            MC_JUMP_1: set([MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
            MC_SHOOT: set([]),
            MC_MECHA_BOARDING: set([MC_HIT]),
            MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_SHOOT, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
            MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_SHOOT, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
            MC_TURN: set([MC_STAND]),
            MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_RUN]),
            MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_IMMOBILIZE, MC_SHOOT, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT]),
            MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN]),
            MC_RUN: set([MC_TURN, MC_MOVE, MC_STAND]),
            MC_HIT: set([]),
            MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT])
            }
   }
forbid = {'9011': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD]),
            MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD]),
            MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK]),
            MC_SHOOT: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK]),
            MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_SHOOT, MC_DEAD, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
            MC_DEAD: set([]),
            MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD]),
            MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MOVE, MC_RUN]),
            MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK]),
            MC_FROZEN: set([MC_MECHA_BOARDING, MC_DEAD]),
            MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK]),
            MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK]),
            MC_HIT: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK]),
            MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_FROZEN, MC_SHOOT, MC_DEAD])
            }
   }
behavior = {'9011': {MC_JUMP_3: {'action_param': (0, ['stand', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['stand', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['stand', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'action_param': (0, ['born', 'lower', 1]),'custom_param': {'anim_duration': 2},'action_state': 'Born'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_IMMOBILIZE: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_SHOOT: {'action_param': (0, ['attack_02', 'upper', 1]),'custom_param': {'weapon_type': 890401,'cast_time': (0.2, 0.95),'fire_socket': ('fx_spark_kaihuo_02', 'fx_spark_kaihuo_01'),'fire_sound_param': ('Play_weapon_fire', (('gun', 'monster9006_fire'), ('gun_option', 'single'))),'min_cast_interval': 2.5},'action_state': 'CastGrenade'},MC_DEAD: {'action_param': (0, ['die', 'lower', 1]),'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9006_blast'), ('monster_select', 'monster9006')),'time': 0.0}],'action_state': 'Die'},MC_BEAT_BACK: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MOVE: {'action_param': (0, ['run', 'lower', 1, {'loop': True}]),'custom_param': {'move_acc': 15,'walk_speed': 7,'brake_acc': -30},'action_state': 'Walk'},MC_STAND: {'action_param': (0, ['stand', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_RUN: {'action_param': (0, ['run', 'lower', 1, {'loop': True}]),'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9001_turn_back'), ('monster_select', 'monster9001')),'time': 0.0}],'custom_param': {'move_acc': 15,'run_speed': 10,'walk_speed': 7,'brake_acc': -30},'action_state': 'Run'},MC_HIT: {'custom_param': {'hit_anim_duration': (1, 1),'hit_anim': ('hit', 'hit'),'hit_thresh': 300},'action_state': 'Hit'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]