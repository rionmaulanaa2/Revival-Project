# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/8019.py
_reload_all = True
version = '195587422'
from .mecha_status_config import *
cover = {'8019': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_STAND, MC_SUPER_JUMP, MC_HELP, MC_TURN]),
            MC_JUMP_2: set([MC_JUMP_1, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_STAND, MC_SUPER_JUMP, MC_HELP, MC_TURN]),
            MC_JUMP_1: set([MC_CELEBRATE, MC_RUN, MC_MOVE, MC_STAND, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_MECHA_BOARDING: set([MC_CELEBRATE, MC_RUN, MC_MOVE, MC_DEFEND, MC_SHOOT, MC_RELOAD, MC_STAND, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_CELEBRATE: set([MC_STAND]),
            MC_RUN: set([MC_CELEBRATE, MC_MOVE, MC_STAND, MC_HELP, MC_TURN]),
            MC_DEFEND: set([MC_CELEBRATE, MC_USE_ITEM, MC_HELP]),
            MC_SHOOT: set([MC_CELEBRATE, MC_USE_ITEM, MC_HELP]),
            MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_STAND, MC_SUPER_JUMP, MC_DASH, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_RELOAD: set([MC_CELEBRATE, MC_SHOOT, MC_USE_ITEM, MC_HELP]),
            MC_SECOND_WEAPON_ATTACK: set([MC_CELEBRATE, MC_SHOOT, MC_RELOAD, MC_USE_ITEM, MC_HELP]),
            MC_MOVE: set([MC_JUMP_3, MC_CELEBRATE, MC_RUN, MC_STAND, MC_HELP, MC_TURN]),
            MC_STAND: set([MC_JUMP_3, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_TURN]),
            MC_SUPER_JUMP: set([MC_JUMP_3, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SECOND_WEAPON_ATTACK, MC_STAND, MC_DASH, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_DASH: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SHOOT, MC_RELOAD, MC_STAND, MC_SUPER_JUMP, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_DRIVER_LEAVING: set([MC_CELEBRATE, MC_RUN, MC_MOVE, MC_DEFEND, MC_SHOOT, MC_RELOAD, MC_STAND, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_USE_ITEM: set([MC_CELEBRATE, MC_SHOOT, MC_RELOAD, MC_HELP]),
            MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_STAND, MC_SUPER_JUMP, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_HELP: set([MC_CELEBRATE, MC_SHOOT, MC_RELOAD, MC_USE_ITEM]),
            MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_DEFEND, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_STAND, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_USE_ITEM, MC_FROZEN, MC_HELP, MC_TURN]),
            MC_TURN: set([MC_CELEBRATE, MC_STAND]),
            MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_STAND, MC_SUPER_JUMP, MC_DASH, MC_USE_ITEM, MC_HELP, MC_TURN])
            }
   }
forbid = {'8019': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_CELEBRATE, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_CELEBRATE, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_CELEBRATE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_DEFEND, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_USE_ITEM, MC_FROZEN, MC_HELP, MC_DEAD, MC_TURN]),
            MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_DEFEND: set([MC_MECHA_BOARDING, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_SHOOT: set([MC_MECHA_BOARDING, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_RELOAD: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_SECOND_WEAPON_ATTACK: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_SUPER_JUMP: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_DASH: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_DRIVER_LEAVING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_FROZEN, MC_DEAD]),
            MC_USE_ITEM: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_FROZEN: set([MC_MECHA_BOARDING, MC_DASH, MC_DRIVER_LEAVING, MC_DEAD]),
            MC_HELP: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_DEAD: set([]),
            MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_IMMOBILIZE: set([MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD])
            }
   }
behavior = {'8019': {MC_JUMP_3: {'action_param': (0, ['jump_03', 'lower', 1, {'blend_time': 0.1}]),'sound_param': [{'sound_visible': 1,'sound_name': ('m_8019_jump_end', 'nf'),'time': 0.0}],'custom_param': {'onground_sfx_time': 0.01,'anim_duration': 1,'recover_trigger_speed': 35,'onground_sfx_type': 'middle','recover_max_delta_speed': 80,'max_recover_time': 0.5,'min_recover_time': 0.3},'action_state': 'OnGround8019'},MC_JUMP_2: {'action_param': (0, ['jump_02', 'lower', 1, {'loop': False}]),'sound_param': [{'sound_visible': 1,'sound_name': ('Play_mecha', ('mecha_action', 'm_falling_normal_loop')),'is_loop': 1,'time': 0.0}, {'sound_visible': 1,'sound_name': ('Play_mecha', ('mecha_action', 'm_falling_normal_end')),'time': -1}, {'command_type': 0,'sound_name': ('Play_mecha', ('mecha_action', 'm_falling_normal_loop')),'time': -1}],'custom_param': {'h_offset_speed': 7.9,'quick_jump_time': 0.35,'h_offset_acc': 20.0,'gravity': 105.0,'can_quick_jump': True},'action_state': 'Fall8019','max_speed': 50},MC_JUMP_1: {'action_param': (0, ['jump_01', 'lower', 1]),'custom_param': {'h_offset_speed': 10.0,'skill_id': 801954,'hover_ability': False,'reinforced_val': 15.0,'h_offset_acc': 20.0,'jump_speed': 38.0,'h_speed_ratio': 0.8,'anim_duration': 0.58,'advanced_glide_vertical_speed': 20.0,'gravity': 60},'action_state': 'JumpUp8019','sound_param': [{'sound_visible': 1,'sound_name': ('m_8019_jump', 'nf'),'time': 0.0}]},MC_MECHA_BOARDING: {'sound_param': [{'sound_name': ('m_8019_on', 'nf'),'time': 0.0}],'custom_param': {'action_param': {'default': (0, ['mount', 'lower', 1]),'share': (0, ['mount', 'lower', 1])},'anim_duration': 4.267,'hide_time': 1.2,'pre_mount_trk_info': {'trk_time': 0.15,'dis': [0, 0, -50]},'slerp_start_time': 0.1},'action_state': 'Mount','state_camera': {'cam': '133'}},MC_CELEBRATE: {'action_state': 'MechaCelebrate'},MC_RUN: {'custom_param': {'dynamic_speed_rate': 0,'move_acc': 30,'run_speed': 9.8,'walk_speed': 7,'brake_acc': -40},'action_state': 'Run8019','max_speed': 12,'state_camera': {'cam': '135'}},MC_MOVE: {'state_camera': {'cam': '134'},'action_state': 'Walk','custom_param': {'dynamic_speed_rate': 0,'move_acc': 30,'walk_speed': 7,'brake_acc': -40},'max_speed': 12,'action_param': (0, ['move', 'lower', 6, {'loop': True}])},MC_DEFEND: {'custom_param': {'skill_id': 801953,'defend_enter_anim_dur': 0.6,'defend_exit_anim_dur': 0.5,'defend_enter_anim': 'shd_start','defend_exit_anim': 'shd_end','defend_anim': 'shd_idle'},'action_state': 'Defend'},MC_SHOOT: {'action_param': (0, ['shoot_idle', 'upper', 1]),'custom_param': {'use_up_anim_states': ['MC_STAND'],'need_keep_fire_time': True,'shoot_anim': ('shoot', 'upper', 7),'shoot_aim_ik': ('aim', ['biped spine', 'biped spine1', 'biped r clavicle', 'biped r upperarm', 'biped r forearm']),'weapon_pos': 1},'action_state': 'WeaponFire8019'},MC_BEAT_BACK: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 15,'gravity': 50,'min_h_speed': 25,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_RELOAD: {'sound_param': [{'sound_name': ('m_8019_reload', 'nf'),'time': 0.0}],'custom_param': {'use_up_anim_states': ['MC_STAND'],'reload_anim_dir': 7,'anim_duration': 2.0,'weapon_pos': 1,'use_up_anim_bone': {'exit': 2,'enter': 1}},'action_state': 'Reload8019'},MC_SECOND_WEAPON_ATTACK: {'sound_param': {'touch_state': [{'sound_name': ('m_8019_weapon1_start', 'nf'),'time': 0.0}]},'custom_param': {'post_time': 2.4,'pre_time': 0.5,'shoot_move_anim': 'pan_loop_idle','hold_anim': 'pan_loop','pre_anim': 'pan_start','pre_anim_rate': 0.7,'weapon_pos': 3,'skill_id': 801951,'post_anim': 'pan_fire_pinjie','post_anim_rate': 1.0,'post_break_time': 0.51},'action_state': 'AccumulateShoot8019','state_camera': {'cam': '137'}},MC_IMMOBILIZE: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'state_camera': {'cam': '133'},'action_state': 'Stand'},MC_SUPER_JUMP: {'state_camera': {'cam': '135'},'action_state': 'SuperJumpUp','sound_param': [{'sound_visible': 1,'sound_name': ('Play_props', ('props_option', 'mecha_launcher')),'time': 0.0}],'custom_param': {'h_scale': 6,'anim_duration': 0.667,'h_max_speed': 60,'gravity': 47,'jump_speed': 60},'action_param': (0, ['jump_02', 'lower', 1])},MC_DASH: {'state_camera': {'cam': '135'},'action_state': 'Dash8019','sound_param': {'run_state': [{'sound_name': ('m_8019_sprint_start', 'nf'),'time': 0.0}, {'sound_visible': 2,'sound_name': ('m_8019_sprint_loop', 'nf'),'is_loop': 1,'time': 0.0}, {'sound_visible': 2,'command_type': 0,'sound_name': ('m_8019_sprint_loop', 'nf'),'time': -1}],'custom_state': [{'sound_name': ('m_8019_sprint_manual_end', 'nf'),'time': -1}]},'custom_param': {'max_rush_duration': 0.7,'hit_skill_id': 801956,'pre_anim': 'dash_01','cam_pitch_sensitivity': 30,'miss_anim_rate': 1.0,'skill_id': 801952,'miss_anim': 'dash_05','tick_interval': 0.03,'break_hit_time': 0.4,'hit_anim_duration': 1.0,'pre_anim_duration': 0.4,'cam_yaw_sensitivity': 40,'range_pitch_angle': [-70, -25],'max_rush_speed': 65,'hit_anim_rate': 1.0,'hit_anim': 'dash_03','pre_anim_rate': 1.3,'air_dash_end_speed': 25,'miss_anim_duration': 0.66,'start_acc_time': 0.35,'range_pitch_speed_ratio': [0.65, 1.0],'attack_skill_id': 801955,'rush_anim': 'dash_02','min_elevation_speed_ratio': 0.65,'end_brake_time': 0.434},'max_speed': 100},MC_DRIVER_LEAVING: {'sound_param': [{'sound_name': ('m_8019_off', 'nf'),'time': 0.0}],'custom_param': {'action_param': {'default': (0, ['unmount', 'lower', 1]),'share_celebrate': (1.5, ['idle', 'lower', 1]),'share': (0, ['unmount', 'lower', 1])},'eject_anim_time': 1.327,'eject_time': 0.4,'anim_time': 1.667,'eject_anim_time_tag': True},'action_state': 'UnMount','state_camera': {'cam': '133'}},MC_USE_ITEM: {'action_state': 'UseItem'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_HELP: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Help'},MC_DEAD: {'action_param': (0, ['die', 'lower', 1]),'sound_param': [{'sound_name': ('m_8019_die', 'nf'),'time': 0.0}],'action_state': 'Die'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': True,'anim_duration': 1},'action_state': 'Turn8019','state_camera': {'cam': '135'}}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]