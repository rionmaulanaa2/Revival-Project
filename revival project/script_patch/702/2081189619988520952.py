# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/8001.py
_reload_all = True
version = '202130469'
from .mecha_status_config import *
cover = {'8001': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_SUPER_JUMP, MC_TURN, MC_HELP, MC_STAND, MC_RUN, MC_MOVE]),
            MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_SUPER_JUMP, MC_TURN, MC_HELP, MC_STAND, MC_RUN, MC_MOVE]),
            MC_JUMP_1: set([MC_CELEBRATE, MC_TURN, MC_HELP, MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE]),
            MC_SHOOT: set([MC_CELEBRATE, MC_HELP, MC_USE_ITEM]),
            MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_CELEBRATE, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_SUPER_JUMP, MC_TURN, MC_HELP, MC_USE_ITEM, MC_FROZEN, MC_STAND, MC_RUN, MC_IMMOBILIZE, MC_MOVE, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_CELEBRATE: set([MC_STAND]),
            MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_CELEBRATE, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_SUPER_JUMP, MC_TURN, MC_HELP, MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE, MC_DASH]),
            MC_RELOAD: set([MC_SHOOT, MC_CELEBRATE, MC_HELP, MC_USE_ITEM]),
            MC_SECOND_WEAPON_ATTACK: set([MC_SHOOT, MC_CELEBRATE, MC_RELOAD, MC_HELP, MC_USE_ITEM]),
            MC_TURN: set([MC_CELEBRATE, MC_STAND]),
            MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_CELEBRATE, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_SUPER_JUMP, MC_TURN, MC_HELP, MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE, MC_DASH, MC_MECHA_BOARDING]),
            MC_USE_ITEM: set([MC_SHOOT, MC_CELEBRATE, MC_RELOAD, MC_HELP]),
            MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_CELEBRATE, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_SUPER_JUMP, MC_TURN, MC_HELP, MC_USE_ITEM, MC_STAND, MC_RUN, MC_IMMOBILIZE, MC_MOVE, MC_DASH]),
            MC_STAND: set([MC_JUMP_3, MC_CELEBRATE, MC_TURN, MC_RUN, MC_MOVE]),
            MC_RUN: set([MC_CELEBRATE, MC_TURN, MC_HELP, MC_STAND, MC_MOVE]),
            MC_SUPER_JUMP: set([MC_JUMP_3, MC_CELEBRATE, MC_TURN, MC_HELP, MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE, MC_DASH]),
            MC_MOVE: set([MC_JUMP_3, MC_CELEBRATE, MC_TURN, MC_HELP, MC_STAND, MC_RUN]),
            MC_DASH: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_CELEBRATE, MC_RELOAD, MC_SUPER_JUMP, MC_TURN, MC_HELP, MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE]),
            MC_HELP: set([MC_SHOOT, MC_CELEBRATE, MC_RELOAD, MC_USE_ITEM]),
            MC_DRIVER_LEAVING: set([MC_SHOOT, MC_CELEBRATE, MC_RELOAD, MC_TURN, MC_HELP, MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE]),
            MC_MECHA_BOARDING: set([MC_SHOOT, MC_CELEBRATE, MC_RELOAD, MC_TURN, MC_HELP, MC_USE_ITEM, MC_STAND, MC_RUN, MC_MOVE])
            }
   }
forbid = {'8001': {MC_JUMP_3: set([MC_DEAD, MC_CELEBRATE, MC_FROZEN, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_JUMP_2: set([MC_JUMP_3, MC_DEAD, MC_CELEBRATE, MC_FROZEN, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_DEAD, MC_BEAT_BACK, MC_SUPER_JUMP, MC_FROZEN, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_SHOOT: set([MC_DEAD, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_FROZEN, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_DEAD: set([]),
            MC_CELEBRATE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_DEAD, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_SUPER_JUMP, MC_TURN, MC_HELP, MC_USE_ITEM, MC_FROZEN, MC_RUN, MC_IMMOBILIZE, MC_MOVE, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_BEAT_BACK: set([MC_DEAD, MC_FROZEN, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_RELOAD: set([MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_FROZEN, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_SECOND_WEAPON_ATTACK: set([MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_SUPER_JUMP, MC_FROZEN, MC_RUN, MC_IMMOBILIZE, MC_MOVE, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_IMMOBILIZE: set([MC_DEAD, MC_FROZEN, MC_DRIVER_LEAVING]),
            MC_USE_ITEM: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_SUPER_JUMP, MC_FROZEN, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_FROZEN: set([MC_DEAD, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_SUPER_JUMP, MC_FROZEN, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_SHOOT, MC_DEAD, MC_BEAT_BACK, MC_RELOAD, MC_SUPER_JUMP, MC_FROZEN, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_SUPER_JUMP: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_SUPER_JUMP, MC_FROZEN, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_DASH: set([MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_FROZEN, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_HELP: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_SUPER_JUMP, MC_FROZEN, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING, MC_MECHA_BOARDING]),
            MC_DRIVER_LEAVING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_SUPER_JUMP, MC_FROZEN, MC_IMMOBILIZE, MC_DASH, MC_MECHA_BOARDING]),
            MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_SUPER_JUMP, MC_FROZEN, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING])
            }
   }
behavior = {'8001': {MC_JUMP_3: {'action_param': (0, ['jump_03', 'lower', 1]),'sound_param': [{'sound_visible': 1,'sound_name': ('m_8001_jump_down', 'nf'),'time': 0.0}],'custom_param': {'horizontal_speed_to_on_ground_duration_rate': 35,'min_on_ground_duration': 0.3,'anim_duration': 1.733,'on_ground_duration_to_sfx_type_threshold': [0.1, 1.0],'show_on_ground_sfx_time': 0.06,'max_on_ground_duration': 0.5,'horizontal_brake_speed': 15,'min_trigger_on_ground_fall_duration': 0.13,'fall_duration_to_on_ground_duration_rate': 0.8,'max_horizontal_brake_duration': 0.8,'min_trigger_on_ground_horizontal_speed': 20},'action_state': 'OnGroundPure'},MC_JUMP_2: {'action_param': (0, ['jump_02', 'lower', 1, {'loop': False}]),'sound_param': [{'sound_visible': 1,'sound_name': ('Play_mecha', ('mecha_action', 'm_falling_normal_loop')),'is_loop': 1,'time': 0.0}, {'sound_visible': 1,'sound_name': ('Play_mecha', ('mecha_action', 'm_falling_normal_end')),'time': -1}, {'command_type': 0,'sound_name': ('Play_mecha', ('mecha_action', 'm_falling_normal_loop')),'time': -1}],'custom_param': {'h_offset_speed': 7.7,'h_offset_acc': 20.0,'coyote_duration': 0.35,'h_offset_dec': 0,'max_h_offset_dec_duration': -1,'fall_gravity': 90.0},'action_state': 'FallPure','max_speed': 50},MC_JUMP_1: {'sound_param': {'jump': [{'sound_visible': 1,'sound_name': ('m_8001_jump', 'nf'),'time': 0.0}]},'custom_param': {'h_offset_speed': 10.0,'skill_id': 800153,'btn_up_punishment_height': 2,'h_offset_dec': 0,'h_offset_acc': 22.0,'anim_name': 'jump_01','jump_speed': 33.0,'h_speed_ratio': 0.85,'anim_duration': 0.433,'jump_gravity': 61.25},'action_state': 'JumpUp8001'},MC_SHOOT: {'custom_param': {'slow_down_speed': 3.5,'shoot_anim': ('shoot', 'upper', 7),'weapon_pos': 1},'action_state': 'WeaponFire8001'},MC_DEAD: {'action_param': (0, ['die', 'lower', 1]),'sound_param': [{'sound_name': ('m_8001_die', 'nf'),'time': 0.0}],'custom_param': {'back_deacc': 20},'action_state': 'Die'},MC_CELEBRATE: {'action_state': 'MechaCelebrate'},MC_BEAT_BACK: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 15,'gravity': 50,'min_h_speed': 25,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_RELOAD: {'action_param': (0, ['reload', 'upper', 1]),'sound_param': [{'sound_name': ('m_8001_reload', 'nf'),'time': 0.0}],'custom_param': {'anim_duration': 2.0},'action_state': 'Reload'},MC_SECOND_WEAPON_ATTACK: {'action_param': (0, ['missile_01', 'upper', 1]),'custom_param': {'skill_id': 800151,'anim_part': 'upper','post_anim': ('missile_03', 0.23),'weapon_pos': 2,'blend_dir': 1,'shoot_anim': ('missile_02', 0.3)},'action_state': 'SequenceShoot'},MC_SUPER_JUMP: {'action_param': (0, ['jump_01', 'lower', 1]),'sound_param': [{'sound_visible': 1,'sound_name': ('Play_props', ('props_option', 'mecha_launcher')),'time': 0.0}],'custom_param': {'h_offset_speed': 10.0,'h_offset_acc': 10.0,'h_speed_ratio': 1.0,'jump_gravity': 45,'h_offset_dec': 0.0,'max_h_offset_dec_duration': -1,'anim_duration': 0.667},'action_state': 'SuperJumpUpPure'},MC_TURN: {'sound_param': [{'sound_name': ('m_8001_turn', 'nf'),'time': 0.0}],'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': True,'turn_left': 'turnleft_90','anim_duration': 1,'turn_right': 'turnright_90'},'action_state': 'Turn'},MC_HELP: {'action_param': (0, ['standby_combat', 'lower', 1, {'loop': True}]),'action_state': 'Help'},MC_USE_ITEM: {'action_state': 'UseItem'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['standby_combat', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_RUN: {'state_camera': {'free_cam_breakable': False,'cam': '43'},'action_state': 'Run','custom_param': {'dynamic_speed_rate': 0.1,'move_acc': 30,'run_speed': 9.24,'walk_speed': 6.5,'brake_acc': -40},'max_speed': 12,'action_param': (0, ['run', 'lower', 4, {'ignore_sufix': True,'loop': True}])},MC_IMMOBILIZE: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_MOVE: {'action_param': (0, ['move', 'lower', 6, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.8,'move_acc': 30,'walk_speed': 6.5,'brake_acc': -40},'action_state': 'Walk','max_speed': 12},MC_DASH: {'state_camera': {'delay_camera_param': {'recover_time': 0.2,'speed': 0.4,'last_time': 0.6}},'action_state': 'Dash8001','sound_param': [{'sound_visible': 2,'sound_name': ('m_8001_sprint_normal', 'nf'),'condition': 'air','time': 0.0}, {'sound_visible': 2,'sound_name': ('m_8001_sprint_normal', 'nf'),'condition': 'land','time': 0.0}, {'sound_name': ('m_8001_sprint_end', 'nf'),'condition': 'land','time': -1}, {'sound_name': ('m_8001_sprint_end', 'nf'),'condition': 'air','time': -1}],'custom_param': {'air_dash_brake_time': 0.3,'skill_id': 800152,'dash_anim_air': 'thrust_air','dash_anim': 'thrust','dash_speed': 70,'dash_param': {'land': {'brake_begin': 0.55,'stop': 0.75,'acc_end': 0.25,'end': 0.933,'acc_begin': 0},'air': {'brake_begin': 0.4,'end': 0.53,'acc_end': 0.126,'acc_begin': 0}},'air_dash_brake_val': 120,'multi_dir': True},'max_speed': 200},MC_DRIVER_LEAVING: {'sound_param': [{'sound_name': ('m_8001_off', 'nf'),'time': 0.0}],'custom_param': {'action_param': {'default': (0, ['unmount', 'lower', 1]),'share_celebrate': (1.5, ['idle', 'lower', 1]),'share': (0, ['unmount', 'lower', 1])},'eject_time': 0.4},'action_state': 'UnMount'},MC_MECHA_BOARDING: {'sound_param': [{'sound_name': ('m_8001_on', 'nf'),'time': 0.0}],'custom_param': {'action_param': {'default': (0, ['mount', 'lower', 1]),'share': (0, ['mount', 'lower', 1])},'anim_duration': 4,'hide_time': 2,'pre_mount_trk_info': {'trk_time': 0.15,'dis': [0, 0, -50]},'slerp_start_time': 0.1},'action_state': 'Mount'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]