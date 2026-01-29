# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/8008.py
from __future__ import absolute_import
_reload_all = True
version = '140375262'
from .mecha_status_config import *
cover = {'8008': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_RUN, MC_TURN, MC_MOVE, MC_BEAT_BACK, MC_STAND, MC_SUPER_JUMP, MC_HELP]),
            MC_JUMP_2: set([MC_JUMP_1, MC_RUN, MC_TURN, MC_MOVE, MC_BEAT_BACK, MC_STAND, MC_SUPER_JUMP, MC_HELP]),
            MC_JUMP_1: set([MC_JUMP_2, MC_CELEBRATE, MC_RUN, MC_TURN, MC_MOVE, MC_STAND, MC_USE_ITEM, MC_HELP]),
            MC_MECHA_BOARDING: set([MC_CELEBRATE, MC_PHOTON_ATTACK, MC_PHOTON_RELOAD, MC_RUN, MC_TURN, MC_MOVE, MC_SHOOT, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_STAND, MC_USE_ITEM, MC_HELP, MC_PHOTON_SHIELD]),
            MC_CELEBRATE: set([MC_STAND]),
            MC_PHOTON_ATTACK: set([MC_CELEBRATE, MC_PHOTON_RELOAD]),
            MC_PHOTON_RELOAD: set([]),
            MC_RUN: set([MC_CELEBRATE, MC_TURN, MC_MOVE, MC_STAND, MC_HELP]),
            MC_EXECUTE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_CELEBRATE, MC_PHOTON_ATTACK, MC_PHOTON_RELOAD, MC_RUN, MC_TURN, MC_MOVE, MC_CAST_SKILL, MC_SHOOT, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_STAND, MC_DRIVER_LEAVING, MC_USE_ITEM, MC_FROZEN, MC_HELP, MC_PHOTON_SHIELD]),
            MC_HELP: set([MC_CELEBRATE, MC_SHOOT, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_USE_ITEM]),
            MC_CAST_SKILL: set([MC_CELEBRATE, MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_USE_ITEM, MC_HELP]),
            MC_SHOOT: set([MC_CELEBRATE, MC_USE_ITEM, MC_HELP]),
            MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_CELEBRATE, MC_PHOTON_ATTACK, MC_PHOTON_RELOAD, MC_RUN, MC_TURN, MC_MOVE, MC_CAST_SKILL, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_STAND, MC_SUPER_JUMP, MC_USE_ITEM, MC_HELP, MC_PHOTON_SHIELD]),
            MC_RELOAD: set([MC_CELEBRATE, MC_SHOOT, MC_USE_ITEM, MC_HELP]),
            MC_SECOND_WEAPON_ATTACK: set([MC_CELEBRATE, MC_PHOTON_ATTACK, MC_PHOTON_RELOAD, MC_USE_ITEM, MC_HELP]),
            MC_MOVE: set([MC_JUMP_3, MC_CELEBRATE, MC_RUN, MC_TURN, MC_STAND, MC_HELP]),
            MC_STAND: set([MC_JUMP_3, MC_CELEBRATE, MC_RUN, MC_TURN, MC_MOVE]),
            MC_SUPER_JUMP: set([MC_JUMP_3, MC_CELEBRATE, MC_RUN, MC_TURN, MC_MOVE, MC_CAST_SKILL, MC_STAND, MC_USE_ITEM, MC_HELP]),
            MC_DRIVER_LEAVING: set([MC_CELEBRATE, MC_PHOTON_ATTACK, MC_PHOTON_RELOAD, MC_RUN, MC_TURN, MC_MOVE, MC_SHOOT, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_STAND, MC_USE_ITEM, MC_HELP, MC_PHOTON_SHIELD]),
            MC_USE_ITEM: set([MC_CELEBRATE, MC_SHOOT, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_HELP]),
            MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_CELEBRATE, MC_PHOTON_ATTACK, MC_RUN, MC_TURN, MC_MOVE, MC_CAST_SKILL, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_STAND, MC_SUPER_JUMP, MC_USE_ITEM, MC_HELP, MC_PHOTON_SHIELD]),
            MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_CELEBRATE, MC_PHOTON_ATTACK, MC_PHOTON_RELOAD, MC_RUN, MC_TURN, MC_MOVE, MC_CAST_SKILL, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_STAND, MC_SUPER_JUMP, MC_USE_ITEM, MC_HELP, MC_PHOTON_SHIELD]),
            MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_CELEBRATE, MC_PHOTON_ATTACK, MC_PHOTON_RELOAD, MC_RUN, MC_TURN, MC_MOVE, MC_CAST_SKILL, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_STAND, MC_SUPER_JUMP, MC_DRIVER_LEAVING, MC_USE_ITEM, MC_FROZEN, MC_HELP, MC_PHOTON_SHIELD]),
            MC_TURN: set([MC_CELEBRATE, MC_STAND]),
            MC_PHOTON_SHIELD: set([MC_CELEBRATE, MC_USE_ITEM, MC_HELP])
            }
   }
forbid = {'8008': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_CELEBRATE, MC_CAST_SKILL, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_CELEBRATE, MC_CAST_SKILL, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_JUMP_1: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_CAST_SKILL, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_CAST_SKILL, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_CELEBRATE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_PHOTON_ATTACK, MC_PHOTON_RELOAD, MC_RUN, MC_TURN, MC_MOVE, MC_CAST_SKILL, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DRIVER_LEAVING, MC_USE_ITEM, MC_FROZEN, MC_HELP, MC_DEAD, MC_EXECUTE, MC_PHOTON_SHIELD]),
            MC_PHOTON_ATTACK: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_PHOTON_RELOAD: set([MC_MECHA_BOARDING, MC_PHOTON_ATTACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_DEAD, MC_EXECUTE]),
            MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_RELOAD, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_EXECUTE: set([MC_BEAT_BACK, MC_SUPER_JUMP, MC_DEAD]),
            MC_HELP: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_CAST_SKILL, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE, MC_PHOTON_SHIELD]),
            MC_CAST_SKILL: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_SHOOT: set([MC_MECHA_BOARDING, MC_CAST_SKILL, MC_RELOAD, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_RELOAD: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_SECOND_WEAPON_ATTACK: set([MC_MECHA_BOARDING, MC_CAST_SKILL, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_SUPER_JUMP: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_DRIVER_LEAVING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_CAST_SKILL, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_USE_ITEM: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_CAST_SKILL, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE, MC_PHOTON_SHIELD]),
            MC_FROZEN: set([MC_MECHA_BOARDING, MC_DRIVER_LEAVING, MC_DEAD, MC_EXECUTE]),
            MC_IMMOBILIZE: set([MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_DEAD: set([MC_EXECUTE]),
            MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE]),
            MC_PHOTON_SHIELD: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD, MC_EXECUTE])
            }
   }
behavior = {'8008': {MC_JUMP_3: {'action_param': (0, ['jump_04', 'lower', 1]),'sound_param': [{'sound_visible': 1,'sound_name': ('m_8008_jump_down_normal', 'nf'),'time': 0.0}],'custom_param': {'skill_id': 800851,'min_recover_time': 0.3,'recover_trigger_speed': 35.0,'recover_max_delta_speed': 80.0,'max_recover_time': 0.7,'onground_sfx_time': 0.05,'onground_sfx_type': 'large','anim_duration': 1,'anim_expected_duration': 0.5},'action_state': 'OnGround8008'},MC_JUMP_2: {'action_param': (0, ['jump_03', 'lower', 1, {'loop': False}]),'sound_param': [{'sound_visible': 1,'sound_name': ('Play_mecha', ('mecha_action', 'm_falling_normal_loop')),'is_loop': 1,'time': 0.0}, {'sound_visible': 1,'sound_name': ('Play_mecha', ('mecha_action', 'm_falling_normal_end')),'time': -1}, {'command_type': 0,'sound_name': ('Play_mecha', ('mecha_action', 'm_falling_normal_loop')),'time': -1}],'custom_param': {'h_offset_speed': 8,'skill_id': 800851,'h_offset_acc': 16,'gravity': 60},'action_state': 'Fall8008','max_speed': 50},MC_JUMP_1: {'action_param': (0, ['jump_01', 'lower', 1]),'sound_param': {'post': [{'sound_name': ('m_8008_air_release', 'nf'),'time': 0.0}],'loop': [{'sound_visible': 2,'sound_name': ('m_8008_jump', 'nf'),'time': 0.0}, {'sound_name': ('m_8008_jump_loop', 'nf'),'is_loop': 1,'time': 0.0}, {'sound_visible': 0,'command_type': 0,'sound_name': ('m_8008_jump_loop', 'nf'),'time': -1}]},'custom_param': {'h_offset_acc': 25,'jump_speed': 14.8,'h_offset_dec_duration': 1.0,'max_height': 2450,'max_h_speed': 10.2,'post_anim_name': 'jump_02','h_offset_speed': 8.5,'skill_id': 800851,'max_brake_acc_time': 1,'post_anim_duration': 0.36,'h_speed_ratio': 0.8,'post_anim_rate': 1.9,'loop_anim_name': 'jump_01'},'action_state': 'JetJump8008'},MC_MECHA_BOARDING: {'sound_param': [{'sound_name': ('m_8008_on', 'nf'),'time': 0.0}],'custom_param': {'action_param': {'default': (0, ['mount', 'lower', 1]),'share': (0, ['mount', 'lower', 1])},'anim_duration': 2.333,'hide_time': 1,'slerp_start_time': 0.1},'action_state': 'Mount'},MC_CELEBRATE: {'action_state': 'MechaCelebrate'},MC_PHOTON_ATTACK: {'sound_param': [{'sound_name': ('m_8008_weapon3_fire', 'nf'),'time': 0.5}],'custom_param': {'total_time': 1,'skill_id': 800853,'anim': 'laser_backpack','laser_time': 0.5,'up_bone': {'exit': (('biped root', 0), ('biped spine', 1)),'enter': (('biped root', 0), ('biped_bone13', 1), ('biped_bone16', 1))}},'action_state': 'PhotonAttack'},MC_PHOTON_RELOAD: {'custom_param': {'total_time': 0.94,'anim': 'reload_tower','up_bone': {'exit': (('biped root', 0), ('biped spine', 1)),'enter': (('biped root', 0), ('biped_bone13', 1), ('biped_bone16', 1))}},'action_state': 'PhotonReload'},MC_RUN: {'state_camera': {'free_cam_breakable': False,'cam': '48'},'action_state': 'Run','custom_param': {'dynamic_speed_rate': 0,'move_acc': 30,'run_speed': 9.5,'walk_speed': 7,'brake_acc': -40},'max_speed': 12,'action_param': (0, ['run', 'lower', 4, {'ignore_sufix': True,'loop': True}])},MC_MOVE: {'action_param': (0, ['move', 'lower', 6, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0,'move_acc': 30,'walk_speed': 7,'brake_acc': -40},'action_state': 'Walk','max_speed': 10},MC_CAST_SKILL: {'sound_param': [{'sound_visible': 1,'command_type': 1,'sound_name': ('m_8008_sprint_normal', 'nf'),'time': 0.0}, {'command_type': 1,'sound_name': ('m_8008_shield_on', 'nf'),'time': 0.0}],'custom_param': {'skill_id': 800855,'hard_state': ('MC_TURN', 'MC_JUMP_1', 'MC_DASH', 'MC_SHOOT', 'MC_MOVE'),'hard_time': 0.5,'skill_anim': 'build_shield','anim_time': 1.2,'cast_time': 0.2,'ignore_reload_anim': True},'action_state': 'CommonCastSkill','max_speed': 60},MC_SHOOT: {'action_param': (0, ['shoot_idle', 'upper', 1, {'blend_time': 0.1}]),'custom_param': {'slow_down_on_shoot': False,'use_up_anim_states': ['MC_STAND', 'MC_HOVER'],'hold_time': 0.5,'shoot_anim': ('shoot', 'upper', 1),'weapon_pos': 1},'action_state': 'WeaponFire'},MC_BEAT_BACK: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 15,'gravity': 50,'min_h_speed': 25,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_RELOAD: {'action_param': (0, ['reload', 'upper', 1]),'sound_param': [{'sound_name': ('m_8008_reload', 'nf'),'time': 0.0}],'custom_param': {'anim_duration': 2.6},'action_state': 'Reload'},MC_SECOND_WEAPON_ATTACK: {'sound_param': {'touch_state': [{'sound_visible': 1,'sound_name': ('m_8008_weapon1_ready', 'nf'),'time': -1}]},'custom_param': {'skill_id': 800802,'post_time': 0.76,'aim_anim': 'throw_02','pre_time': 0.33,'post_anim': 'throw_04','hold_anim': 'throw_02','post_break_time': 1.5,'up_bone': {'exit': (('biped root', 0), ('biped spine', 1)),'enter': (('biped root', 0), ('biped_bone13', 1), ('biped_bone16', 1))},'pre_anim': 'throw_01','show_track': True,'exit_default_anim': 'idle_tower','fire_interval': 0.5,'aim_time': 2,'hold_time': 1,'fire_anim': 'throw_03','replace_stand': False,'fire_time': 1},'action_state': 'AccumulateSkill_M8'},MC_IMMOBILIZE: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_SUPER_JUMP: {'state_camera': {'cam': '49'},'action_state': 'SuperJumpUp','sound_param': [{'sound_visible': 1,'sound_name': ('Play_props', ('props_option', 'mecha_launcher')),'time': 0.0}],'custom_param': {'h_scale': 6,'anim_duration': 0.667,'h_max_speed': 60,'gravity': 50,'jump_speed': 58},'action_param': (0, ['jump_01', 'lower', 1])},MC_DRIVER_LEAVING: {'sound_param': [{'sound_name': ('m_8008_off', 'nf'),'time': 0.0}],'custom_param': {'action_param': {'default': (0, ['unmount', 'lower', 1]),'share_celebrate': (1.5, ['idle', 'lower', 1]),'share': (0, ['unmount', 'lower', 1])},'eject_time': 0.4},'action_state': 'UnMount'},MC_USE_ITEM: {'action_state': 'UseItem'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_HELP: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Help'},MC_DEAD: {'action_param': (0, ['die', 'lower', 1]),'sound_param': [{'sound_name': ('m_8008_die', 'nf'),'time': 0.0}],'action_state': 'Die'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': True,'turn_left': 'turnleft_90','anim_duration': 1,'turn_right': 'turnright_90'},'action_state': 'Turn'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]