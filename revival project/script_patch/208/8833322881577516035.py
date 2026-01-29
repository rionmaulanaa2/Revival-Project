# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/4108.py
from __future__ import absolute_import
_reload_all = True
from .mecha_status_config import *
cover = {'4108': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_STAND, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_HELP]),
            MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TRANSFORM, MC_TURN, MC_STAND, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_HELP]),
            MC_JUMP_1: set([MC_TURN, MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE, MC_HELP]),
            MC_SHOOT: set([MC_USE_ITEM, MC_HELP]),
            MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_TRANSFORM, MC_TURN, MC_IMMOBILIZE, MC_USE_ITEM, MC_FROZEN, MC_STAND, MC_RIGHT_AIM, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_DASH, MC_HELP]),
            MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_RELOAD, MC_TURN, MC_USE_ITEM, MC_STAND, MC_RIGHT_AIM, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_DASH, MC_HELP]),
            MC_RELOAD: set([MC_SHOOT, MC_USE_ITEM, MC_RIGHT_AIM, MC_HELP]),
            MC_TURN: set([MC_STAND]),
            MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_USE_ITEM, MC_STAND, MC_RUN, MC_HELP]),
            MC_USE_ITEM: set([MC_SHOOT, MC_RELOAD, MC_RIGHT_AIM, MC_HELP]),
            MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_TRANSFORM, MC_TURN, MC_IMMOBILIZE, MC_USE_ITEM, MC_STAND, MC_RIGHT_AIM, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_DASH, MC_HELP]),
            MC_STAND: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_MOVE]),
            MC_TRANSFORM: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_RELOAD, MC_TURN, MC_USE_ITEM, MC_STAND, MC_RIGHT_AIM, MC_HELP]),
            MC_RIGHT_AIM: set([]),
            MC_RUN: set([MC_TURN, MC_USE_ITEM, MC_STAND, MC_MOVE, MC_HELP]),
            MC_SUPER_JUMP: set([MC_JUMP_3, MC_TURN, MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE, MC_HELP]),
            MC_DASH: set([MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE, MC_HELP]),
            MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_TURN, MC_USE_ITEM, MC_STAND, MC_RIGHT_AIM, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_DASH, MC_HELP]),
            MC_HELP: set([MC_SHOOT, MC_RELOAD, MC_USE_ITEM, MC_STAND, MC_RIGHT_AIM, MC_RUN, MC_MOVE, MC_DASH])
            },
   '4108_2': {MC_RELOAD: set([MC_SHOOT]),
              MC_SHOOT: set([]),
              MC_STAND: set([MC_TURN]),
              MC_TURN: set([MC_STAND]),
              MC_RIGHT_AIM: set([])
              },
   '4108_3': {MC_STAND: set([MC_TURN]),
              MC_TURN: set([MC_STAND])
              },
   '4108_1': {MC_RELOAD: set([MC_SHOOT]),
              MC_SHOOT: set([]),
              MC_STAND: set([MC_TURN]),
              MC_TURN: set([MC_STAND])
              }
   }
forbid = {'4108': {MC_JUMP_3: set([MC_DEAD, MC_TRANSFORM, MC_IMMOBILIZE, MC_FROZEN]),
            MC_JUMP_2: set([MC_JUMP_3, MC_DEAD, MC_IMMOBILIZE, MC_FROZEN]),
            MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_DEAD, MC_BEAT_BACK, MC_TRANSFORM, MC_IMMOBILIZE, MC_FROZEN, MC_SUPER_JUMP]),
            MC_SHOOT: set([MC_DEAD, MC_BEAT_BACK, MC_RELOAD, MC_TRANSFORM, MC_IMMOBILIZE, MC_FROZEN]),
            MC_DEAD: set([]),
            MC_BEAT_BACK: set([MC_DEAD, MC_TRANSFORM, MC_IMMOBILIZE, MC_FROZEN]),
            MC_RELOAD: set([MC_DEAD, MC_BEAT_BACK, MC_TRANSFORM, MC_IMMOBILIZE, MC_FROZEN]),
            MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_TRANSFORM, MC_IMMOBILIZE, MC_FROZEN, MC_RUN, MC_SUPER_JUMP, MC_MOVE]),
            MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_FROZEN, MC_SUPER_JUMP, MC_DASH]),
            MC_USE_ITEM: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_TRANSFORM, MC_IMMOBILIZE, MC_FROZEN, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_DASH]),
            MC_FROZEN: set([MC_DEAD]),
            MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_TRANSFORM, MC_IMMOBILIZE, MC_FROZEN, MC_SUPER_JUMP, MC_DASH]),
            MC_TRANSFORM: set([MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_FROZEN, MC_SUPER_JUMP]),
            MC_RIGHT_AIM: set([MC_DEAD, MC_BEAT_BACK, MC_TRANSFORM, MC_IMMOBILIZE, MC_FROZEN]),
            MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_DEAD, MC_BEAT_BACK, MC_RELOAD, MC_IMMOBILIZE, MC_FROZEN, MC_RIGHT_AIM, MC_SUPER_JUMP, MC_DASH]),
            MC_SUPER_JUMP: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_TRANSFORM, MC_IMMOBILIZE, MC_FROZEN]),
            MC_DASH: set([MC_DEAD, MC_BEAT_BACK, MC_TRANSFORM, MC_IMMOBILIZE, MC_FROZEN]),
            MC_IMMOBILIZE: set([MC_DEAD, MC_TRANSFORM, MC_FROZEN]),
            MC_HELP: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_TRANSFORM, MC_IMMOBILIZE, MC_FROZEN, MC_SUPER_JUMP])
            },
   '4108_2': {MC_RELOAD: set([]),
              MC_SHOOT: set([MC_RELOAD]),
              MC_STAND: set([]),
              MC_TURN: set([]),
              MC_RIGHT_AIM: set([MC_RIGHT_AIM])
              },
   '4108_3': {MC_STAND: set([]),
              MC_TURN: set([])
              },
   '4108_1': {MC_RELOAD: set([]),
              MC_SHOOT: set([MC_RELOAD]),
              MC_STAND: set([]),
              MC_TURN: set([])
              }
   }
behavior = {'4108_2': {MC_RELOAD: {'sound_param': [{'sound_name': ['Play_lmg_reload', 'nf'],'time': 0.0}],'custom_param': {'anim_duration': 1.0},'action_state': 'Reload4108Seat'},MC_SHOOT: {'custom_param': {'shoot_anim': ('', 'upper', 1),'weapon_pos': 1},'action_state': 'WeaponFire4108Seat'},MC_STAND: {'state_camera': {'cam': '112'},'action_state': 'SeatStand'},MC_TURN: {'custom_param': {'trans_self': True},'action_state': 'Turn4108Seat'},MC_RIGHT_AIM: {'state_camera': {'cam': '113'},'action_state': 'RightAim4108Seat'}},'4108': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.3,'recover_trigger_speed': 100.0,'onground_sfx_type': 'middle','recover_max_delta_speed': 100.0,'max_recover_time': 0.1,'min_recover_time': 0.05},'action_state': 'OnGround4108'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'h_offset_speed': 7.7,'quick_jump_time': 0.35,'h_offset_acc': 20.0,'gravity': 90.0,'can_quick_jump': True},'action_state': 'Fall4108'},MC_RUN: {'action_param': (0, ['move', 'lower', 4, {'yaw_list': [0, 0, 0, 0],'loop': True}]),'sound_param': {'run_state': [{'sound_visible': 2,'sound_name': ('Play_duorenzaiju', ('duorenzaiju', 'duorenzaiju_idle')),'is_loop': 1,'time': 0}, {'sound_visible': 0,'command_type': 0,'sound_name': ('Play_duorenzaiju', ('duorenzaiju', 'duorenzaiju_idle')),'time': -1}]},'custom_param': {'run_speed': 23,'rotate_speed': 60,'brake_acc': -8,'walk_speed': 7,'move_acc': 7,'dynamic_speed_rate': 0.1},'action_state': 'Run4108'},MC_SHOOT: {'action_state': 'WeaponFire4108'},MC_DEAD: {'sound_param': [{'sound_name': ('m_8014_die', 'nf'),'time': 0.0}],'custom_param': {'die_action': ['die', 'lower', 1, {}],'anim_duration': 1},'action_state': 'Die4108'},MC_RIGHT_AIM: {'action_state': 'RightAim4108'},MC_TURN: {'custom_param': {'rotate_speed': 60},'action_state': 'Turn4108'},MC_MOVE: {'action_param': (0, ['move', 'lower', 4, {'yaw_list': [0, 0, 0, 0],'loop': True}]),'sound_param': {'run_state': [{'sound_visible': 2,'sound_name': ('Play_duorenzaiju', ('duorenzaiju', 'duorenzaiju_idle')),'is_loop': 1,'time': 0}, {'sound_visible': 0,'command_type': 0,'sound_name': ('Play_duorenzaiju', ('duorenzaiju', 'duorenzaiju_idle')),'time': -1}]},'custom_param': {'dynamic_speed_rate': 0.8,'move_acc': 7,'walk_speed': 7,'brake_acc': -8,'rotate_speed': 60},'action_state': 'Walk4108'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand4108'},MC_RELOAD: {'action_state': 'Reload4108'},MC_SUPER_JUMP: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'h_scale': 6,'anim_duration': 0.667,'h_max_speed': 60,'gravity': 45,'jump_speed': 62},'action_state': 'SuperJumpUp'},MC_DASH: {'action_param': (0, ['accelerate', 'lower', 1]),'sound_param': {'run_state': [{'sound_name': ('Play_duorenzaiju', ('duorenzaiju', 'duorenzaiju_boost_start')),'time': 0}, {'sound_visible': 2,'sound_name': ('Play_duorenzaiju', ('duorenzaiju', 'duorenzaiju_boost_loop')),'is_loop': 1,'time': 0}, {'sound_visible': 0,'command_type': 0,'sound_name': ('Play_duorenzaiju', ('duorenzaiju', 'duorenzaiju_boost_loop')),'time': -1}, {'sound_name': ('Play_duorenzaiju', ('duorenzaiju', 'duorenzaiju_boost_end')),'time': -1}]},'custom_param': {'skill_id': 410851,'brake_acc': 25,'walk_speed': 40,'move_acc': 80,'forward_walk_speed': 40,'back_walk_speed': 20,'dash_duration': 3},'action_state': 'DashMotorcycle','max_speed': 50}},'4108_3': {MC_STAND: {'state_camera': {'cam': '114'},'action_state': 'SeatStand'},MC_TURN: {'custom_param': {'forward_driver': True},'action_state': 'Turn4108Seat'}},'4108_1': {MC_RELOAD: {'sound_param': [{'sound_name': ['Play_m249_reload', 'nf'],'time': 0.0}],'custom_param': {'anim_duration': 1.0},'action_state': 'Reload4108Seat','state_camera': {'cam': '111'}},MC_SHOOT: {'custom_param': {'shoot_anim': ('', 'upper', 1),'weapon_pos': 1},'action_state': 'WeaponFire4108Seat'},MC_STAND: {'state_camera': {'cam': '111'},'action_state': 'SeatStand'},MC_TURN: {'custom_param': {'forward_vehicle': True},'action_state': 'Turn4108Seat'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]