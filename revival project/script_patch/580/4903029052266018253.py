# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90007.py
_reload_all = True
version = '196719466'
from .pve_monster_status_config import *
cover = {'90007': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_STAND]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_STAND]),
             MC_JUMP_1: set([MC_TURN, MC_STAND]),
             MC_MECHA_BOARDING: set([]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_MOVE, MC_IMMOBILIZE, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_ROAR, MC_STAND, MC_RUN]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MOVE, MC_IMMOBILIZE, MC_MONSTER_AIMTURN, MC_TURN, MC_STAND, MC_RUN]),
             MC_MONSTER_AIMTURN: set([MC_MOVE, MC_TURN, MC_STAND, MC_RUN]),
             MC_TURN: set([MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_STAND, MC_RUN]),
             MC_MONSTER_ROAR: set([MC_MOVE, MC_MONSTER_AIMTURN, MC_TURN, MC_STAND, MC_RUN]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_MOVE, MC_IMMOBILIZE, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_ROAR, MC_STAND, MC_RUN]),
             MC_STAND: set([MC_JUMP_3, MC_MOVE, MC_TURN, MC_RUN]),
             MC_RUN: set([MC_MOVE, MC_TURN, MC_STAND]),
             MC_MONSTER_ESCAPE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_MOVE, MC_IMMOBILIZE, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_ROAR, MC_STAND, MC_RUN]),
             MC_IMMOBILIZE: set([MC_BEAT_BACK])
             }
   }
forbid = {'90007': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_MONSTER_ESCAPE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_MONSTER_ESCAPE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_ESCAPE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_FROZEN, MC_MOVE, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_TURN, MC_MONSTER_ROAR, MC_STAND, MC_RUN, MC_MONSTER_ESCAPE]),
             MC_DEAD: set([MC_MONSTER_ESCAPE]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD, MC_MONSTER_ROAR, MC_MONSTER_ESCAPE]),
             MC_MONSTER_AIMTURN: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_ROAR, MC_MONSTER_ESCAPE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_MOVE, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_RUN, MC_MONSTER_ESCAPE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_ESCAPE]),
             MC_MONSTER_ROAR: set([MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_ESCAPE]),
             MC_FROZEN: set([MC_DEAD, MC_MONSTER_ESCAPE]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_ESCAPE]),
             MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_FROZEN, MC_IMMOBILIZE, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_AIMTURN, MC_MONSTER_ROAR, MC_MONSTER_ESCAPE]),
             MC_MONSTER_ESCAPE: set([MC_DEAD]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_FROZEN, MC_DEAD, MC_MONSTER_ESCAPE])
             }
   }
behavior = {'90007': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 0.5,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_born_02_shader.sfx','born_anim': 'idle'},'action_state': 'MonsterBorn'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_MOVE: {'action_param': (0, ['move', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.0,'move_acc': 3000,'walk_speed': 24,'brake_acc': -3000},'action_state': 'MonsterWalk'},MC_IMMOBILIZE: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'},MC_DEAD: {'custom_param': {'sfx_path': 'effect/fx/monster/pve/pve_017_guangzhu.sfx','tip_text_2': 83583,'die_anim_rate': 1.0,'sfx_delay': 0.0,'tip_text': 83582,'die_anim': 'guard','tip_type': 5},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_AIMTURN: {'custom_param': {'skill_id': 9000753,'max_aim_dur': 1.1,'aim_right_anim': 'turnright_90','aim_right_anim_rate': 1.0,'aim_left_anim_rate': 1.0,'aim_left_anim': 'turnleft_90','aim_speed': 3.6},'action_state': 'MonsterAimTurn'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_ROAR: {'custom_param': {'skill_id': 9000751,'anim_dur': 1.6,'anim_rate': 1.0,'anim_name': 'panic'},'action_state': 'MonsterRoar'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_RUN: {'action_param': (0, ['move', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.3,'move_acc': 3000,'run_speed': 30,'walk_speed': 24,'brake_acc': -3000},'action_state': 'MonsterRun'},MC_MONSTER_ESCAPE: {'custom_param': {'escape_anim': 'escape','escape_anim_rate': 1.0,'tip_type': 2,'tip_text': 83584},'action_state': 'MonsterEscape'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]