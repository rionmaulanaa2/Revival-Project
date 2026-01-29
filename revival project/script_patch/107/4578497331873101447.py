# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90162.py
_reload_all = True
version = '196717324'
from .pve_monster_status_config import *
cover = {'90162': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_JUMP_2: set([MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_JUMP_1: set([MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_MONSTER_LINK, MC_FROZEN, MC_IMMOBILIZE, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_MONSTER_LASER, MC_RUN]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_MONSTER_LINK, MC_IMMOBILIZE, MC_TURN, MC_MOVE, MC_STAND, MC_MONSTER_LASER, MC_RUN]),
             MC_TURN: set([MC_MECHA_BOARDING, MC_STAND]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_MONSTER_LINK, MC_BEAT_BACK, MC_MONSTER_LASER]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_MONSTER_LINK, MC_IMMOBILIZE, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_MONSTER_LASER, MC_RUN]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN]),
             MC_MONSTER_LASER: set([MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_RUN: set([MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_STAND, MC_RUN]),
             MC_MONSTER_LINK: set([MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_STAND, MC_RUN])
             }
   }
forbid = {'90162': {MC_JUMP_3: set([MC_MONSTER_LINK, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_MONSTER_LASER]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MONSTER_LINK, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_MONSTER_LASER]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MONSTER_LINK, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_LASER]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_FROZEN, MC_DEAD]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_LINK, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MOVE, MC_MONSTER_LASER, MC_RUN]),
             MC_IMMOBILIZE: set([MC_FROZEN, MC_DEAD]),
             MC_FROZEN: set([MC_DEAD]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_MONSTER_LINK, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_LASER]),
             MC_MONSTER_LASER: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK]),
             MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_LINK, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_LASER]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MONSTER_LINK, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_LASER]),
             MC_MONSTER_LINK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK])
             }
   }
behavior = {'90162': {MC_JUMP_3: {'action_param': (0, ['idle_tower', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle_tower', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle_tower', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 1.3,'born_anim_rate': 2.0,'sfx_path': '','born_anim': 'tower_build'},'action_state': 'MonsterBorn'},MC_MONSTER_LINK: {'custom_param': {'link_anim': 'tower_shield','pre_anim_dur': 1.0,'pre_anim': 'tower_attack','link_anim_rate': 1.0,'target_socket': 'fx_box','link_sfx_scale': 1.5,'link_sfx_res': 'effect/fx/monster/pve/pve_cureline.sfx','end_sfx_res': 'effect/fx/monster/pve/pve_cureline.sfx','skill_id': 9016252,'link_socket': 'fx_kaihuo','end_sfx_scale': 1.1},'action_state': 'MonsterLink'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_IMMOBILIZE: {'action_param': (0, ['idle_tower', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 0,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'idle_tower'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['idle_tower', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MOVE: {'action_param': (0, ['idle_tower', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 2,'move_acc': 1000,'walk_speed': 100,'brake_acc': -1000},'action_state': 'MonsterWalk'},MC_STAND: {'action_param': (0, ['idle_tower', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_MONSTER_LASER: {'custom_param': {'int_anim_dur': 1.06,'max_laser_dis': 100,'atk_anim_rate': 1.0,'pre_anim_dur': 1.0,'pre_anim': 'tower_attack','bac_anim_rate': 1.0,'atk_socket': 'fx_kaihuo','bac_anim_dur': 1.43,'skill_id': 9016251,'face_to': False,'pre_sfx_scale': 1.0,'atk_sfx_res': 'effect/fx/monster/pve/pve_laser.sfx','max_atk_dur': 5.0,'int_anim_rate': 1.0,'end_socket': 'fx_kaihuo','height_offset': 100.0,'atk_sfx_scale': 1.0,'hit_interval': 0.5,'pre_anim_rate': 1.0,'int_anim': 'idle_tower','end_sfx_res': 'effect/fx/monster/pve/pve_laser_end.sfx','bac_anim': 'idle_tower','pre_sfx_res': '','pre_track_ratio': 0.5,'atk_track_ratio': 0.03,'pre_socket': 'fx_kaihuo','atk_anim': 'tower_shield','end_sfx_scale': 1.0},'action_state': 'MonsterLaser'},MC_RUN: {'action_param': (0, ['idle_tower', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.5,'move_acc': 1000,'run_speed': 100,'walk_speed': 100,'brake_acc': -1000},'action_state': 'MonsterRun'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]