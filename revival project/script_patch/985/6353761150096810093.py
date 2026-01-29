# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/8005.py
_reload_all = True
version = '200246617'
from .mecha_status_config import *
cover = {'8005': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_STAND, MC_SUPER_JUMP, MC_HELP, MC_TURN]),
            MC_JUMP_2: set([MC_JUMP_1, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_STAND, MC_SUPER_JUMP, MC_HELP, MC_TURN]),
            MC_JUMP_1: set([MC_CELEBRATE, MC_RUN, MC_MOVE, MC_STAND, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_MECHA_BOARDING: set([MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SHOOT, MC_RELOAD, MC_STAND, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_CELEBRATE: set([MC_STAND]),
            MC_RUN: set([MC_CELEBRATE, MC_MOVE, MC_STAND, MC_HELP, MC_TURN]),
            MC_HELP: set([MC_CELEBRATE, MC_SHOOT, MC_RELOAD, MC_USE_ITEM]),
            MC_SHOOT: set([MC_CELEBRATE, MC_USE_ITEM, MC_HELP]),
            MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_STAND, MC_SUPER_JUMP, MC_DASH, MC_TRANSFORM, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_RELOAD: set([MC_CELEBRATE, MC_SHOOT, MC_USE_ITEM, MC_HELP]),
            MC_SECOND_WEAPON_ATTACK: set([MC_CELEBRATE, MC_RELOAD, MC_USE_ITEM, MC_HELP]),
            MC_MOVE: set([MC_JUMP_3, MC_CELEBRATE, MC_RUN, MC_STAND, MC_HELP, MC_TURN]),
            MC_STAND: set([MC_JUMP_3, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_TURN]),
            MC_SUPER_JUMP: set([MC_JUMP_3, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SECOND_WEAPON_ATTACK, MC_STAND, MC_DASH, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_DASH: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SHOOT, MC_RELOAD, MC_STAND, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_DRIVER_LEAVING: set([MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SHOOT, MC_RELOAD, MC_STAND, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_TRANSFORM: set([MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SHOOT, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_STAND, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_USE_ITEM: set([MC_CELEBRATE, MC_SHOOT, MC_RELOAD, MC_HELP]),
            MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_STAND, MC_SUPER_JUMP, MC_DASH, MC_TRANSFORM, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_STAND, MC_SUPER_JUMP, MC_DASH, MC_USE_ITEM, MC_HELP, MC_TURN]),
            MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_STAND, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_USE_ITEM, MC_FROZEN, MC_HELP, MC_TURN]),
            MC_TURN: set([MC_CELEBRATE, MC_STAND])
            },
   '8005_trans': {MC_SHOOT: set([MC_USE_ITEM]),
                  MC_DEAD: set([MC_TRANSFORM, MC_USE_ITEM, MC_FROZEN, MC_IMMOBILIZE, MC_SHOOT, MC_RELOAD, MC_TURN, MC_STAND, MC_SHOOT_MODE, MC_DRIVER_LEAVING]),
                  MC_TRANSFORM: set([MC_USE_ITEM, MC_SHOOT, MC_RELOAD, MC_TURN, MC_STAND]),
                  MC_SHOOT_MODE: set([]),
                  MC_TURN: set([MC_STAND]),
                  MC_DRIVER_LEAVING: set([MC_USE_ITEM, MC_SHOOT, MC_RELOAD, MC_TURN, MC_STAND, MC_SHOOT_MODE]),
                  MC_USE_ITEM: set([MC_RELOAD]),
                  MC_FROZEN: set([MC_TRANSFORM, MC_USE_ITEM, MC_IMMOBILIZE, MC_SHOOT, MC_RELOAD, MC_TURN, MC_STAND, MC_SHOOT_MODE]),
                  MC_STAND: set([MC_TURN]),
                  MC_RELOAD: set([MC_USE_ITEM, MC_SHOOT]),
                  MC_IMMOBILIZE: set([MC_USE_ITEM, MC_SHOOT, MC_RELOAD, MC_TURN, MC_STAND, MC_SHOOT_MODE])
                  }
   }
forbid = {'8005': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_IMMOBILIZE, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_CELEBRATE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_CELEBRATE, MC_RUN, MC_MOVE, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_USE_ITEM, MC_FROZEN, MC_HELP, MC_DEAD, MC_TURN]),
            MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_SHOOT, MC_BEAT_BACK, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_HELP: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_SHOOT: set([MC_MECHA_BOARDING, MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_RELOAD: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_SECOND_WEAPON_ATTACK: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_SUPER_JUMP: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_DASH: set([MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_DRIVER_LEAVING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_TRANSFORM: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_FROZEN, MC_DEAD]),
            MC_USE_ITEM: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_FROZEN: set([MC_MECHA_BOARDING, MC_DRIVER_LEAVING, MC_DEAD]),
            MC_IMMOBILIZE: set([MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD]),
            MC_DEAD: set([]),
            MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_RUN, MC_MOVE, MC_BEAT_BACK, MC_SECOND_WEAPON_ATTACK, MC_IMMOBILIZE, MC_SUPER_JUMP, MC_DASH, MC_DRIVER_LEAVING, MC_TRANSFORM, MC_FROZEN, MC_DEAD])
            },
   '8005_trans': {MC_SHOOT: set([MC_TRANSFORM, MC_FROZEN, MC_DEAD, MC_RELOAD, MC_SHOOT_MODE, MC_DRIVER_LEAVING]),
                  MC_DEAD: set([]),
                  MC_TRANSFORM: set([MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_SHOOT_MODE, MC_DRIVER_LEAVING]),
                  MC_SHOOT_MODE: set([MC_TRANSFORM, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_DRIVER_LEAVING]),
                  MC_TURN: set([MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_DRIVER_LEAVING]),
                  MC_DRIVER_LEAVING: set([MC_TRANSFORM, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD]),
                  MC_USE_ITEM: set([MC_TRANSFORM, MC_FROZEN, MC_IMMOBILIZE, MC_SHOOT, MC_DEAD, MC_DRIVER_LEAVING]),
                  MC_FROZEN: set([MC_DEAD, MC_DRIVER_LEAVING]),
                  MC_STAND: set([MC_TRANSFORM, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_DRIVER_LEAVING]),
                  MC_RELOAD: set([MC_TRANSFORM, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_SHOOT_MODE, MC_DRIVER_LEAVING]),
                  MC_IMMOBILIZE: set([MC_TRANSFORM, MC_FROZEN, MC_DEAD, MC_DRIVER_LEAVING])
                  }
   }
behavior = {'8005_trans': {MC_TRANSFORM: {'action_param': (0, ['transform', 'lower', 1]),'sound_param': [{'sound_name': ('m_8005_to_mecha', 'nf'),'time': 0.0}],'custom_param': {'timer_rate': 1.25,'camera_state': '28','anim_time': 2.6,'weapon_id': 800503,'break_time': 1,'action_switch': {'action5': 163},'twist_x_bone': ('biped_bone49', 'biped_bone49'),'twist_y_bone': ('biped spine01', 'biped spine01'),'upbody_bone': 'biped spine01','trans_id': '8005'},'action_state': 'Transform','target_state': (1.1, 'ALL')},MC_USE_ITEM: {'action_param': (0, ['transform_idle', 'lower', 1, {'loop': True}]),'action_state': 'UseItem'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_IMMOBILIZE: {'action_param': (0, ['transform_idle', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_SHOOT: {'custom_param': {'sync_yaw': True,'fire_on_release': True,'weapon_pos': 3,'show_track': {'radius': {'800503': 162,'800504': 162},'enable_area_outline': 1},'anim_time': 1,'hold_time': 0.8,'shoot_anim': ('transform_shoot', 'upper', 1)},'action_state': 'WeaponFire'},MC_DEAD: {'action_param': (0, ['transform_idle', 'lower', 1]),'sound_param': [{'sound_name': ('m_8005_die', 'nf'),'time': 0.0}],'action_state': 'Die'},MC_RELOAD: {'action_param': (0, ['transform_reload', 'upper', 1]),'sound_param': [{'sound_name': ('m_8005_cannon_reload', 'nf'),'time': 0.0}],'custom_param': {'anim_duration': 2.6,'weapon_pos': 3},'action_state': 'Reload'},MC_TURN: {'action_param': (0, ['transform_idle', 'upper', 1]),'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': True,'limit_twist_yaw': False,'twist_yaw_offset': 0,'twist_pitch_offset': 10},'action_state': 'Turn'},MC_STAND: {'action_param': (0, ['transform_idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_SHOOT_MODE: {'custom_param': {'show_track': {0: {'show_weapon_id': 800503,'radius': {'800503': 195,'800504': 195},'enable_area_outline': 1},1: {'show_weapon_id': 800503,'radius': {'800503': 195,'800504': 195},'enable_area_outline': 1}},'weapon_pos': 3,'change_conf': {0: {'iMode': 3,'iControl': 2},1: {'iMode': 1,'iControl': 1}}},'action_state': 'ShootModeChange'},MC_DRIVER_LEAVING: {'sound_param': [{'sound_name': ('m_8005_off', 'nf'),'time': 0.0}],'custom_param': {'action_param': {'default': (0, ['unmount', 'lower', 1]),'share_celebrate': (1.5, ['idle', 'lower', 1]),'share': (0, ['unmount', 'lower', 1])},'eject_time': 0.4},'action_state': 'UnMount'}},'8005': {MC_JUMP_3: {'action_param': (0, ['jump_03', 'lower', 1, {'blend_time': 0}]),'sound_param': [{'sound_visible': 1,'sound_name': ('m_8005_jump_down', 'nf'),'time': 0.0}],'custom_param': {'onground_sfx_time': 0.01,'anim_duration': 1,'recover_trigger_speed': 35,'onground_sfx_type': 'middle','recover_max_delta_speed': 80,'max_recover_time': 0.7,'min_recover_time': 0.3},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['jump_02', 'lower', 1, {'loop': False}]),'sound_param': [{'sound_visible': 1,'sound_name': ('Play_mecha', ('mecha_action', 'm_falling_normal_loop')),'is_loop': 1,'time': 0.0}, {'sound_visible': 1,'sound_name': ('Play_mecha', ('mecha_action', 'm_falling_normal_end')),'time': -1}, {'command_type': 0,'sound_name': ('Play_mecha', ('mecha_action', 'm_falling_normal_loop')),'time': -1}],'custom_param': {'h_offset_speed': 7.9,'quick_jump_time': 0.35,'h_offset_acc': 20.0,'gravity': 80.0,'can_quick_jump': True},'action_state': 'Fall','max_speed': 50},MC_JUMP_1: {'action_param': (0, ['jump_01', 'lower', 1]),'custom_param': {'h_offset_speed': 10.0,'skill_id': 800553,'hover_ability': False,'reinforced_val': 15.0,'h_offset_acc': 20.0,'jump_speed': 32.0,'h_speed_ratio': 0.8,'anim_duration': 0.667,'advanced_glide_vertical_speed': 20.0,'gravity': 44.2},'action_state': 'JumpUp','sound_param': [{'sound_visible': 1,'sound_name': ('m_8005_jump', 'nf'),'time': 0.0}]},MC_MECHA_BOARDING: {'sound_param': [{'sound_name': ('m_8005_on', 'nf'),'time': 0.0}],'custom_param': {'action_param': {'default': (0, ['mount', 'lower', 1]),'share': (0, ['mount', 'lower', 1])},'anim_duration': 2.567,'hide_time': 1.2,'slerp_start_time': 0.1},'action_state': 'Mount'},MC_CELEBRATE: {'action_state': 'MechaCelebrate'},MC_RUN: {'state_camera': {'free_cam_breakable': False,'cam': '48'},'action_state': 'Run','custom_param': {'dynamic_speed_rate': 0,'move_acc': 30,'run_speed': 10.5,'walk_speed': 6.2,'brake_acc': -40},'max_speed': 16,'action_param': (0, ['run', 'lower', 4, {'ignore_sufix': True,'loop': True}])},MC_MOVE: {'action_param': (0, ['move', 'lower', 6, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0,'move_acc': 30,'walk_speed': 6.2,'brake_acc': -40},'action_state': 'Walk','max_speed': 16},MC_SHOOT: {'custom_param': {'shoot_anim': ('shoot', 'upper', 1),'weapon_pos': 1},'action_state': 'WeaponFire'},MC_BEAT_BACK: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 15,'gravity': 50,'min_h_speed': 25,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack','max_speed': 55},MC_RELOAD: {'action_param': (0, ['reload', 'upper', 1]),'sound_param': [{'sound_name': ('m_8005_reload', 'nf'),'time': 0.0}],'custom_param': {'anim_duration': 2.6},'action_state': 'Reload'},MC_SECOND_WEAPON_ATTACK: {'sound_param': [{'sound_name': ('m_8005_aim', 'nf'),'time': 0}],'target_state': (0.7, ('MC_TRANSFORM', 'MC_RELOAD', 'MC_SHOOT')),'custom_param': {'skill_id': 800551,'post_time': 1.3,'pre_anim': 'shockwave_01','pre_time': 0.5,'shoot_move_anim': 'shockwave_move','post_anim': 'shockwave_03','hold_anim': 'shockwave_02','post_break_time': 0.3},'action_state': 'AccumulateShoot'},MC_IMMOBILIZE: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_SUPER_JUMP: {'action_param': (0, ['jump_01', 'lower', 1]),'sound_param': [{'sound_visible': 1,'sound_name': ('Play_props', ('props_option', 'mecha_launcher')),'time': 0.0}],'custom_param': {'h_offset_speed': 10.0,'h_offset_dec': 0,'h_offset_acc': 10.0,'anim_duration': 0.667,'jump_gravity': 45},'action_state': 'SuperJumpUp8005'},MC_DASH: {'state_camera': {'cam': '49'},'action_state': 'RocketJump','sound_param': {'run_state': [{'sound_visible': 2,'sound_name': ('m_8005_sprint_normal', 'nf'),'time': 0.0}, {'sound_name': ('m_8005_sprint_end', 'nf'),'time': -1}],'touch_state': [{'sound_name': ('m_8005_aim', 'nf'),'time': 0}]},'custom_param': {'jump_gravity': 100,'max_dist': 60,'break_time': 0.3,'on_ground_anim': 'roketjump_03','base_jump_height': 15,'hold_move_anim': 'shockwave_move','fall_anim': 'roketjump_02','skill_id': 800552,'recover_time': 1,'onground_sfx_type': 'large','hold_stand_anim': 'shockwave_02','break_states': ('MC_MOVE', 'MC_SHOOT', 'MC_SECOND_WEAPON_ATTACK', 'MC_JUMP_1'),'onground_sfx_time': 0.03},'max_speed': 200,'action_param': (0, ['roketjump_01', 'lower', 1])},MC_DRIVER_LEAVING: {'sound_param': [{'sound_name': ('m_8005_off', 'nf'),'time': 0.0}],'custom_param': {'action_param': {'default': (0, ['unmount', 'lower', 1]),'share_celebrate': (1.5, ['idle', 'lower', 1]),'share': (0, ['unmount', 'lower', 1])},'eject_time': 0.4},'action_state': 'UnMount'},MC_TRANSFORM: {'action_param': (0, ['tobear_transform', 'lower', 1]),'sound_param': [{'sound_name': ('m_8005_to_cannon', 'nf'),'time': 0.0}],'custom_param': {'timer_rate': 1.75,'camera_state': '27','anim_time': 2.1,'weapon_id': 800551,'break_time': 1,'twist_x_bone': ('biped spine', 'biped head'),'twist_y_bone': ('biped spine', 'biped head'),'upbody_bone': 'biped spine','break_states': ('MC_MOVE', 'MC_RUN'),'trans_id': '8005_trans'},'action_state': 'Transform','target_state': (1.1, 'ALL')},MC_USE_ITEM: {'action_state': 'UseItem'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_HELP: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Help'},MC_DEAD: {'action_param': (0, ['die', 'lower', 1]),'sound_param': [{'sound_name': ('m_8005_die', 'nf'),'time': 0.0}],'action_state': 'Die'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': True,'turn_left': 'turnleft_90','anim_duration': 1,'turn_right': 'turnright_90'},'action_state': 'Turn'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]