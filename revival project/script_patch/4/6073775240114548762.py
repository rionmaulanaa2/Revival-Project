# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90227.py
_reload_all = True
version = '196708195'
from .pve_monster_status_config import *
cover = {'90227': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_JUMP_1: set([MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_MOVE, MC_FROZEN, MC_STAND, MC_RUN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_3, MC_TURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_MOVE, MC_STAND, MC_RUN]),
             MC_MONSTER_SPURT: set([MC_MOVE, MC_RUN]),
             MC_TURN: set([MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_RUN]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_MOVE, MC_STAND, MC_RUN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_SWEEP: set([MC_MOVE, MC_RUN]),
             MC_RUN: set([MC_JUMP_3, MC_TURN, MC_MOVE, MC_STAND]),
             MC_MONSTER_HIT: set([MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_STAND]),
             MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_MONSTER_HIT]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN])
             }
   }
forbid = {'90227': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_FROZEN, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_FROZEN, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_FROZEN, MC_IMMOBILIZE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_TURN, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_MOVE, MC_FROZEN, MC_STAND, MC_RUN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_SPURT: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SWEEP, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_MOVE, MC_FROZEN, MC_RUN, MC_IMMOBILIZE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_FROZEN, MC_IMMOBILIZE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_MONSTER_SWEEP: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_RUN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_FROZEN, MC_IMMOBILIZE]),
             MC_MONSTER_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_FROZEN, MC_IMMOBILIZE]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_SPURT, MC_MONSTER_SWEEP, MC_FROZEN, MC_IMMOBILIZE])
             }
   }
behavior = {'90227': {MC_JUMP_3: {'action_param': (0, ['base_idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['base_idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['base_idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 2.5,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve_two/pve_two_birth_shader.sfx','born_anim': 'base_idle'},'action_state': 'MonsterBorn'},MC_DEAD: {'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9001_blast'), ('monster_select', 'monster9001')),'time': 0.0}],'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 1.2,'sfx_path': 'effect/fx/monster/pve_two/pve_two_death_shader.sfx','die_anim': 'base_die_stand_hit_from_front'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['base_idle', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_AIMTURN: {'custom_param': {'skill_id': 9022752,'max_aim_dur': 1.8,'aim_right_anim': 'base_move_turn_right90','aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'aim_left_anim': 'base_move_turn_left90','aim_speed': 3.14},'action_state': 'MonsterAimTurn'},MC_MONSTER_SPURT: {'custom_param': {'hit_sfx_rate': 1.0,'atk_anim_rate': 0.7,'pre_anim_dur': 1.5,'pre_anim': 'attack_skill_jingjie_prepare','bac_anim_rate': 1.0,'atk_socket': 'fx_fire','hit_sfx_scale': 2.0,'bac_anim_dur': 0,'skill_id': 9022753,'start_angle': -70.0,'atk_sfx_rate': 1.0,'atk_sfx_res': 'effect/fx/monster/pve_two/pve_jiguang_start.sfx','end_socket': 'fx_fire','height_offset': 95.0,'atk_sfx_scale': 0.05,'pre_anim_rate': 1.0,'end_sfx_res': 'effect/fx/monster/pve_two/pve_jiguang_end.sfx','bac_anim': '','end_sfx_rate': 1.0,'atk_anim_dur': 1.1,'end_angle': -2.0,'atk_anim': 'attack_skill_oneshoot','hit_sfx_res': 'effect/fx/monster/pve_two/pve_jiguang_hit.sfx','end_sfx_scale': 0.5,'max_spurt_dis': 200},'action_state': 'MonsterSpurt'},MC_MONSTER_SWEEP: {'custom_param': {'height_offset': 0.0,'skill_id': 9022751,'bac_anim': '','max_sweep_dis': 200.0,'hit_sfx_rate': 1.0,'atk_anim_rate': 0.38,'atk_anim_dur': 1.1,'start_angle': -50.0,'atk_sfx_scale': 0.5,'pre_anim_dur': 1.5,'atk_sfx_res': 'effect/fx/monster/pve_two/pve_jiguang_start.sfx','atk_sfx_rate': 1.0,'end_angle': 50.0,'pre_anim': 'attack_skill_jingjie_prepare','bac_anim_rate': 1.0,'pre_anim_rate': 1.0,'atk_socket': 'fx_fire','atk_anim': 'attack_skill_oneshoot','hit_sfx_scale': 2.0,'bac_anim_dur': 0,'hit_sfx_res': 'effect/fx/monster/pve_two/pve_jiguang_hit.sfx'},'action_state': 'MonsterSweep'},MC_MOVE: {'action_param': (0, ['base_idle', 'lower', 1, {'loop': True}]),'sound_param': [{'sound_name': ('Play_monster', ('monster_action', 'monster9003_run'), ('monster_select', 'monster9003')),'time': 0.0}],'custom_param': {'dynamic_speed_rate': 2,'move_acc': 30,'walk_speed': 11,'brake_acc': -30},'action_state': 'MonsterWalk'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['base_idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_RUN: {'action_param': (0, ['base_idle', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 3,'move_acc': 30,'run_speed': 15,'walk_speed': 11,'brake_acc': -30},'action_state': 'MonsterRun'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 1.0,'hit_anim': 'beaten_lighthit','hit_anim_dur': 0.2},'action_state': 'MonsterHit'},MC_IMMOBILIZE: {'action_param': (0, ['shake', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]