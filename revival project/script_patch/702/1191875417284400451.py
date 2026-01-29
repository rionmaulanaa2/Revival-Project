# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/9015.py
from __future__ import absolute_import
_reload_all = True
version = '171803520'
from .mecha_status_config import *
cover = {'9015': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
            MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
            MC_JUMP_1: set([MC_JUMP_3, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
            MC_SHOOT: set([]),
            MC_MECHA_BOARDING: set([]),
            MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_SWORD_CORE, MC_TURN, MC_MOVE, MC_FROZEN, MC_STAND, MC_RUN, MC_HIT, MC_IMMOBILIZE]),
            MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT, MC_IMMOBILIZE]),
            MC_SECOND_WEAPON_ATTACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_MOVE, MC_STAND, MC_RUN, MC_IMMOBILIZE]),
            MC_SWORD_CORE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT, MC_IMMOBILIZE]),
            MC_TURN: set([MC_STAND]),
            MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_RUN]),
            MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_SWORD_CORE, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT, MC_IMMOBILIZE]),
            MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_RUN]),
            MC_RUN: set([MC_JUMP_1, MC_TURN, MC_MOVE, MC_STAND]),
            MC_HIT: set([]),
            MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN, MC_HIT])
            }
   }
forbid = {'9015': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_SWORD_CORE, MC_FROZEN, MC_IMMOBILIZE]),
            MC_JUMP_2: set([MC_MECHA_BOARDING, MC_DEAD, MC_SWORD_CORE, MC_FROZEN, MC_IMMOBILIZE]),
            MC_JUMP_1: set([MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_SWORD_CORE, MC_FROZEN, MC_IMMOBILIZE]),
            MC_SHOOT: set([MC_SHOOT, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_SWORD_CORE, MC_FROZEN, MC_IMMOBILIZE]),
            MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_SWORD_CORE, MC_TURN, MC_MOVE, MC_FROZEN, MC_STAND, MC_RUN, MC_HIT, MC_IMMOBILIZE]),
            MC_DEAD: set([]),
            MC_BEAT_BACK: set([MC_SHOOT, MC_MECHA_BOARDING, MC_DEAD, MC_SWORD_CORE, MC_FROZEN]),
            MC_SECOND_WEAPON_ATTACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_SWORD_CORE, MC_FROZEN]),
            MC_SWORD_CORE: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN]),
            MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_SWORD_CORE, MC_MOVE, MC_FROZEN, MC_RUN, MC_IMMOBILIZE]),
            MC_MOVE: set([MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_SWORD_CORE, MC_MOVE, MC_FROZEN, MC_IMMOBILIZE]),
            MC_FROZEN: set([MC_DEAD]),
            MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_SWORD_CORE, MC_FROZEN, MC_IMMOBILIZE]),
            MC_RUN: set([MC_JUMP_3, MC_SHOOT, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_SWORD_CORE, MC_FROZEN, MC_IMMOBILIZE]),
            MC_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_SWORD_CORE, MC_FROZEN, MC_IMMOBILIZE]),
            MC_IMMOBILIZE: set([MC_SHOOT, MC_MECHA_BOARDING, MC_DEAD, MC_SWORD_CORE, MC_FROZEN])
            }
   }
behavior = {'9015': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_SHOOT: {'action_param': (0, ['attack', 'lower', 1, {'loop': True}]),'sound_param': [{'sound_name': ('Play_weapon_fire', ('gun', 'monster9007_fire'), ('gun_option', 'single')),'time': 0.0}],'custom_param': {'shoot_anim': ('attack', 'lower', 1)},'action_state': 'WeaponFire'},MC_MECHA_BOARDING: {'action_param': (0, ['born', 'lower', 1]),'custom_param': {'anim_duration': 3},'action_state': 'Born'},MC_DEAD: {'action_param': (0, ['die', 'lower', 1]),'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9007_blast'), ('monster_select', 'monster9007')),'time': 0.0}],'action_state': 'Die'},MC_BEAT_BACK: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_SECOND_WEAPON_ATTACK: {'custom_param': {'pre_anim': 'fire_attack_01','post_anim': 'fire_attack_03','pre_sound_param': ('Play_weapon_fire', (('gun', 'monster9007_fire'), ('gun_option', 'xuli'))),'fire_sound_param': ('Play_weapon_fire', (('gun', 'monster9007_fire'), ('gun_option', 'single'))),'weapon_type': 890501,'pre_time': 1.5,'cast_time': 0.3,'fire_socket': 'fx_kaihuo1','cast_anim': 'fire_attack_02','post_time': 0.8},'action_state': 'AccumulateCastGrenade'},MC_SWORD_CORE: {'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9007_frantic'), ('monster_select', 'monster9007')),'time': 0.0}, {'command_type': 0,'sound_name': 'monster9007_frantic','time': -1}],'custom_param': {'speed_scale': 2.0,'cast_time': 2.8,'cast_anim': 'skill_02'},'action_state': 'CastSkillClient'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MOVE: {'action_param': (0, ['move_f', 'lower', 1, {'loop': True}]),'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9007_run'), ('monster_select', 'monster9007')),'time': 0.0}],'custom_param': {'move_acc': 15,'walk_speed': 5,'brake_acc': -30},'action_state': 'Walk'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_RUN: {'action_param': (0, ['move_f', 'lower', 1, {'loop': True}]),'custom_param': {'move_acc': 15,'run_speed': 7,'walk_speed': 5,'brake_acc': -30},'action_state': 'Run'},MC_HIT: {'custom_param': {'hit_anim_duration': (1, 1),'hit_anim': ('hit', 'hit'),'hit_thresh': 300},'action_state': 'Hit'},MC_IMMOBILIZE: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]