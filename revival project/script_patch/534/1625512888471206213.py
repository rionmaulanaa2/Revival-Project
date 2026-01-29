# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90323.py
_reload_all = True
version = '198958113'
from .pve_monster_status_config import *
cover = {'90323': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_JUMP_1: set([MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_LINK_HEAL, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_IMMOBILIZE, MC_MONSTER_AIMTURN, MC_MONSTER_LINK_HEAL]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_3, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_MONSTER_LINK_HEAL: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_AIMTURN, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_TURN: set([MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_RUN]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_IMMOBILIZE, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_LINK_HEAL, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MOVE, MC_RUN]),
             MC_RUN: set([MC_JUMP_3, MC_TURN, MC_MOVE, MC_STAND]),
             MC_IMMOBILIZE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_LINK_HEAL])
             }
   }
forbid = {'90323': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_LINK_HEAL]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_MONSTER_AIMTURN, MC_MONSTER_LINK_HEAL]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_LINK_HEAL]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_LINK_HEAL, MC_TURN, MC_MOVE, MC_STAND, MC_RUN]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD]),
             MC_MONSTER_AIMTURN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_LINK_HEAL]),
             MC_MONSTER_LINK_HEAL: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_LINK_HEAL, MC_MOVE, MC_RUN]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_LINK_HEAL]),
             MC_FROZEN: set([MC_DEAD]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_LINK_HEAL]),
             MC_RUN: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_LINK_HEAL]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD])
             }
   }
behavior = {'90323': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 1.0,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_born_02_shader.sfx','born_anim': 'trans_01'},'action_state': 'MonsterBorn'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_IMMOBILIZE: {'action_param': (0, ['hit', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_DEAD: {'custom_param': {'die_anim_rate': 1.0,'sfx_delay': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'die'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['hit', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'max_aim_dur': 1.2,'aim_right_anim': 'rotate_right','aim_speed': 3.14,'aim_left_anim_rate': 2.0,'aim_left_anim': 'rotate_left','aim_right_anim_rate': 2.0},'action_state': 'MonsterAimTurn'},MC_MONSTER_LINK_HEAL: {'custom_param': {'max_heal_time': 5.0,'heal_anim_dur': 0,'pre_anim_dur': 0.3,'pre_anim': 'attack_01_1','pre_anim_rate': 1.0,'heal_anim': 'attack_01_2','bac_anim_dur': 0.3,'skill_id': 9032351,'bac_anim': 'attack_01_3','heal_anim_rate': 1.0,'max_heal_dist': 1040,'bac_anim_rate': 1.0,'heal_sfx_res': 'effect/fx/monster/pve/pve_cureline.sfx','cast_skill_socket': 'fx_attack_01_2','min_heal_dist': 65.0},'action_state': 'MonsterLinkHeal'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 1.1,'move_acc': 3000,'walk_speed': 11,'brake_acc': -3000},'action_state': 'MonsterWalk'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_RUN: {'action_param': (0, ['run', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.4,'move_acc': 3000,'run_speed': 15,'walk_speed': 11,'brake_acc': -3000},'action_state': 'MonsterRun'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]