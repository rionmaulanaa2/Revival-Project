# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/8504.py
from __future__ import absolute_import
_reload_all = True
from .mecha_status_config import *
cover = {'8504_trans': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_STAND, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_HELP]),
                  MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_STAND, MC_TRANSFORM, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_HELP]),
                  MC_JUMP_1: set([MC_TURN, MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE, MC_HELP]),
                  MC_SHOOT: set([MC_USE_ITEM, MC_HELP]),
                  MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_TURN, MC_IMMOBILIZE, MC_USE_ITEM, MC_FROZEN, MC_STAND, MC_TRANSFORM, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_HELP]),
                  MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_RELOAD, MC_TURN, MC_USE_ITEM, MC_STAND, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_HELP]),
                  MC_RELOAD: set([MC_SHOOT, MC_USE_ITEM, MC_HELP]),
                  MC_TURN: set([MC_STAND]),
                  MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_RUN]),
                  MC_USE_ITEM: set([MC_SHOOT, MC_RELOAD, MC_HELP]),
                  MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_TURN, MC_IMMOBILIZE, MC_USE_ITEM, MC_STAND, MC_TRANSFORM, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_HELP]),
                  MC_STAND: set([MC_JUMP_3, MC_TURN, MC_RUN, MC_MOVE]),
                  MC_TRANSFORM: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_RELOAD, MC_TURN, MC_USE_ITEM, MC_STAND, MC_HELP]),
                  MC_RUN: set([MC_TURN, MC_STAND, MC_MOVE]),
                  MC_SUPER_JUMP: set([MC_JUMP_3, MC_TURN, MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE, MC_HELP]),
                  MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_TURN, MC_USE_ITEM, MC_STAND, MC_RUN, MC_SUPER_JUMP, MC_MOVE, MC_HELP]),
                  MC_HELP: set([MC_SHOOT, MC_RELOAD, MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE])
                  },
   '8504': {MC_DEAD: set([MC_TRANSFORM, MC_TURN, MC_USE_ITEM, MC_FROZEN, MC_STAND]),
            MC_TRANSFORM: set([MC_TURN, MC_USE_ITEM, MC_STAND, MC_DASH]),
            MC_TURN: set([]),
            MC_USE_ITEM: set([]),
            MC_FROZEN: set([]),
            MC_STAND: set([MC_TURN, MC_DASH]),
            MC_DASH: set([MC_STAND])
            }
   }
forbid = {'8504_trans': {MC_JUMP_3: set([MC_DEAD, MC_IMMOBILIZE, MC_FROZEN, MC_TRANSFORM]),
                  MC_JUMP_2: set([MC_JUMP_3, MC_DEAD, MC_IMMOBILIZE, MC_FROZEN]),
                  MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_FROZEN, MC_TRANSFORM, MC_SUPER_JUMP]),
                  MC_SHOOT: set([MC_DEAD, MC_BEAT_BACK, MC_RELOAD, MC_IMMOBILIZE, MC_FROZEN, MC_TRANSFORM]),
                  MC_DEAD: set([]),
                  MC_BEAT_BACK: set([MC_DEAD, MC_IMMOBILIZE, MC_FROZEN, MC_TRANSFORM]),
                  MC_RELOAD: set([MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_FROZEN, MC_TRANSFORM]),
                  MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_FROZEN, MC_TRANSFORM, MC_RUN, MC_SUPER_JUMP, MC_MOVE]),
                  MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_FROZEN, MC_SUPER_JUMP, MC_HELP]),
                  MC_USE_ITEM: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_FROZEN, MC_TRANSFORM, MC_SUPER_JUMP]),
                  MC_FROZEN: set([MC_DEAD]),
                  MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_FROZEN, MC_TRANSFORM, MC_SUPER_JUMP]),
                  MC_TRANSFORM: set([MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_FROZEN, MC_SUPER_JUMP]),
                  MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_DEAD, MC_BEAT_BACK, MC_RELOAD, MC_IMMOBILIZE, MC_FROZEN, MC_SUPER_JUMP, MC_HELP]),
                  MC_SUPER_JUMP: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_FROZEN, MC_TRANSFORM]),
                  MC_IMMOBILIZE: set([MC_DEAD, MC_FROZEN, MC_TRANSFORM]),
                  MC_HELP: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_IMMOBILIZE, MC_FROZEN, MC_TRANSFORM, MC_SUPER_JUMP])
                  },
   '8504': {MC_DEAD: set([]),
            MC_TRANSFORM: set([MC_DEAD, MC_FROZEN]),
            MC_TURN: set([MC_DEAD, MC_FROZEN]),
            MC_USE_ITEM: set([MC_DEAD, MC_TRANSFORM, MC_FROZEN]),
            MC_FROZEN: set([MC_DEAD, MC_TRANSFORM, MC_TURN, MC_USE_ITEM, MC_STAND, MC_DASH]),
            MC_STAND: set([MC_DEAD, MC_TRANSFORM, MC_FROZEN]),
            MC_DASH: set([MC_DEAD, MC_FROZEN])
            }
   }
behavior = {'8504': {MC_TRANSFORM: {'action_param': (0, ['transform', 'lower', 1]),'custom_param': {'anim_time': 0.6,'trans_id': '8504_trans'},'action_state': 'Transform'},MC_DASH: {'custom_param': {'skill_id': 850151,'dash_duration': 5.0},'action_state': 'DashVehicle'},MC_STAND: {'action_param': (0, ['vehicle_idle', 'lower', 1, {'loop': True}]),'action_state': 'StandVehicle'},MC_DEAD: {'action_param': (0, ['vehicle_idle', 'lower', 1]),'action_state': 'Die'},MC_USE_ITEM: {'action_state': 'UseItem'}},'8504_trans': {MC_JUMP_3: {'action_param': (0, ['jump_03', 'lower', 1]),'sound_param': [{'sound_visible': 1,'sound_name': ('Play_mecha_run_material', ('mecha_step_action', 'mecha_jump_down')),'time': 0.0}],'custom_param': {'anim_duration': 0.67,'recover_trigger_speed': 36,'recover_max_delta_speed': 50},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['jump_02', 'lower', 1, {'loop': True}]),'custom_param': {'h_offset_speed': 11,'h_offset_acc': 20,'gravity': 78},'action_state': 'Fall','max_speed': 50},MC_JUMP_1: {'action_param': (0, ['jump_01', 'lower', 1]),'sound_param': [{'sound_visible': 1,'sound_name': ('Play_mecha', ('mecha_action', 'mecha8501_jump')),'time': 0.0}],'custom_param': {'h_offset_speed': 11,'skill_id': 850152,'h_offset_acc': 20,'jump_speed': 30,'h_speed_ratio': 0.8,'gravity': 75,'anim_duration': 1},'action_state': 'JumpUp'},MC_SHOOT: {'custom_param': {'shoot_anim': ('shoot_frozen', 'upper', 1),'weapon_pos': 1},'action_state': 'WeaponFire'},MC_DEAD: {'action_param': (0, ['idle', 'lower', 1]),'action_state': 'Die'},MC_BEAT_BACK: {'action_param': (0, ['jump_02', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 15,'gravity': 50,'min_h_speed': 25,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_RELOAD: {'action_param': (0, ['reload', 'upper', 1]),'sound_param': [{'sound_name': ('Play_mecha', ('mecha_action', 'mecha8501_reload')),'time': 0.0}],'custom_param': {'anim_duration': 1.0},'action_state': 'Reload'},MC_TURN: {'custom_param': {'enable_twist_pitch': False,'enable_twist_yaw': False,'anim_duration': 1},'action_state': 'Turn'},MC_IMMOBILIZE: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_USE_ITEM: {'action_param': (0, ['idle', 'upper', 1, {'loop': True}]),'action_state': 'UseItem'},MC_RUN: {'action_param': (0, ['run', 'lower', 4, {'ignore_sufix': True,'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.1,'move_acc': 30,'run_speed': 11,'walk_speed': 7,'brake_acc': -40},'action_state': 'Run','max_speed': 16},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_TRANSFORM: {'action_param': (0, ['transform_back', 'lower', 1]),'custom_param': {'timer_rate': 1.2,'anim_time': 0.6,'trans_id': '8504'},'action_state': 'Transform'},MC_SUPER_JUMP: {'action_param': (0, ['jump_01', 'lower', 1]),'sound_param': [{'sound_visible': 1,'sound_name': ('Play_props', ('props_option', 'mecha_launcher')),'time': 0.0}],'custom_param': {'h_scale': 6,'anim_duration': 1,'h_max_speed': 60,'gravity': 60,'jump_speed': 80},'action_state': 'SuperJumpUp'},MC_MOVE: {'action_param': (0, ['move', 'lower', 6, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.8,'move_acc': 30,'walk_speed': 7,'brake_acc': -40},'action_state': 'Walk'},MC_HELP: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Help'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]