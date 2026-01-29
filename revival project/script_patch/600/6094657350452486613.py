# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/90112.py
_reload_all = True
version = '196717286'
from .pve_monster_status_config import *
cover = {'90112': {MC_JUMP_3: set([MC_JUMP_2, MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MONSTER_SCOUT, MC_STAND, MC_RUN, MC_MOVE]),
             MC_JUMP_2: set([MC_JUMP_1, MC_BEAT_BACK, MC_TURN, MC_MONSTER_SCOUT, MC_STAND, MC_RUN, MC_MOVE]),
             MC_JUMP_1: set([MC_TURN, MC_MONSTER_SCOUT, MC_STAND, MC_RUN, MC_MOVE]),
             MC_MECHA_BOARDING: set([MC_MONSTER_HIT]),
             MC_DEAD: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_FROZEN, MC_STAND, MC_RUN, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_BEAT_BACK: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MONSTER_SNIPE, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_STAND, MC_RUN, MC_MOVE, MC_IMMOBILIZE]),
             MC_MONSTER_SNIPE: set([MC_TURN, MC_MONSTER_SCOUT, MC_STAND, MC_RUN, MC_MOVE]),
             MC_MONSTER_FOCUS_SWAG: set([MC_TURN, MC_MONSTER_SCOUT, MC_STAND, MC_RUN, MC_MOVE]),
             MC_TURN: set([MC_MONSTER_SCOUT, MC_STAND]),
             MC_MOVE: set([MC_JUMP_3, MC_TURN, MC_MONSTER_SCOUT, MC_STAND, MC_RUN]),
             MC_MONSTER_SCOUT: set([MC_TURN, MC_STAND, MC_RUN, MC_MOVE]),
             MC_FROZEN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_BEAT_BACK, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_STAND, MC_RUN, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_STAND: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_TURN, MC_MONSTER_SCOUT, MC_RUN, MC_MOVE]),
             MC_RUN: set([MC_TURN, MC_MONSTER_SCOUT, MC_STAND, MC_MOVE]),
             MC_IMMOBILIZE: set([MC_BEAT_BACK, MC_MONSTER_SNIPE, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_MONSTER_HIT]),
             MC_MONSTER_HIT: set([MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_TURN, MC_MONSTER_ROAR, MC_MONSTER_SCOUT, MC_STAND, MC_RUN, MC_MOVE]),
             MC_MONSTER_ROAR: set([MC_TURN, MC_STAND, MC_RUN, MC_MOVE])
             }
   }
forbid = {'90112': {MC_JUMP_3: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_IMMOBILIZE]),
             MC_JUMP_2: set([MC_JUMP_3, MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_IMMOBILIZE]),
             MC_JUMP_1: set([MC_JUMP_3, MC_JUMP_2, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_IMMOBILIZE]),
             MC_MECHA_BOARDING: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_TURN, MC_FROZEN, MC_STAND, MC_RUN, MC_MOVE, MC_IMMOBILIZE]),
             MC_DEAD: set([]),
             MC_BEAT_BACK: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_FOCUS_SWAG, MC_FROZEN]),
             MC_MONSTER_SNIPE: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_FOCUS_SWAG: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_TURN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_RUN, MC_MOVE, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MOVE: set([MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_MONSTER_SCOUT: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_FROZEN: set([MC_DEAD]),
             MC_STAND: set([MC_JUMP_2, MC_JUMP_1, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_RUN: set([MC_JUMP_3, MC_JUMP_2, MC_JUMP_1, MC_MECHA_BOARDING, MC_DEAD, MC_BEAT_BACK, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_ROAR, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE]),
             MC_IMMOBILIZE: set([MC_MECHA_BOARDING, MC_DEAD, MC_MONSTER_FOCUS_SWAG, MC_FROZEN]),
             MC_MONSTER_HIT: set([MC_MECHA_BOARDING, MC_DEAD, MC_FROZEN, MC_IMMOBILIZE]),
             MC_MONSTER_ROAR: set([MC_DEAD, MC_BEAT_BACK, MC_MONSTER_SNIPE, MC_MONSTER_FOCUS_SWAG, MC_MONSTER_SCOUT, MC_FROZEN, MC_MONSTER_HIT, MC_IMMOBILIZE])
             }
   }
behavior = {'90112': {MC_JUMP_3: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36},'action_state': 'OnGround'},MC_JUMP_2: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'gravity': 100},'action_state': 'Fall'},MC_JUMP_1: {'action_param': (0, ['idle', 'lower', 1]),'custom_param': {'anim_duration': 1,'gravity': 57,'jump_speed': 36},'action_state': 'JumpUp'},MC_MECHA_BOARDING: {'custom_param': {'born_anim_dur': 1.9,'born_anim_rate': 1.0,'sfx_path': 'effect/fx/monster/pve/monster_born_02_shader.sfx','born_anim': 'act_pull'},'action_state': 'MonsterBorn'},MC_DEAD: {'custom_param': {'die_anim_rate': 0.9,'sfx_delay': 1.8,'sfx_path': 'effect/fx/monster/pve/monster_dying.sfx','die_anim': 'die_shock'},'action_state': 'MonsterDie'},MC_BEAT_BACK: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'custom_param': {'max_affect_dist': 15,'min_v_speed': 10,'gravity': 50,'min_h_speed': 10,'max_v_speed': 30,'max_h_speed': 50},'action_state': 'BeatBack'},MC_MONSTER_SNIPE: {'custom_param': {'pre_link_sfx_socket': 'fx_firecircle','atk_anim_rate': 1.0,'pre_anim_dur': 1.5,'pre_anim': 'attack_02','fire_socket': 'fx_firecircle','bac_anim_dur': 0,'skill_id': 9011251,'max_aim_dur': 1.0,'bac_anim_rate': 1.0,'aim_right_anim': 'attack_01','aim_right_anim_rate': 1.0,'pre_link_sfx_rate': 1.0,'wp_list': [9011201],'aim_left_anim_rate': 1.0,'pre_anim_rate': 1.0,'aim_left_anim': 'attack_01','bac_anim': '','pre_link_sfx_res': 'effect/fx/monster/pve/pve_ju_xian.sfx','atk_anim_dur': 1.367,'pre_link_sfx_scale': 1.0,'wp_pos': 1,'trace_dur': 1.3,'atk_anim': 'attack_03','aim_speed': 4},'action_state': 'MonsterSnipe'},MC_MONSTER_FOCUS_SWAG: {'action_state': 'MonsterFocusSwag'},MC_TURN: {'custom_param': {'enable_twist_pitch': True,'enable_twist_yaw': False},'action_state': 'Turn'},MC_MONSTER_ROAR: {'custom_param': {'skill_id': 9011254,'anim_dur': 0.6,'anim_rate': 1.0,'anim_name': 'alert'},'action_state': 'MonsterRoar'},MC_MONSTER_SCOUT: {'custom_param': {'skill_id': 9011252,'anim_dur': 2.9,'anim_rate': 1.0,'anim_name': 'act_show'},'action_state': 'MonsterScout'},MC_FROZEN: {'action_state': 'OnFrozen'},MC_STAND: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Stand'},MC_RUN: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.7,'move_acc': 30,'run_speed': 16,'walk_speed': 13,'brake_acc': -30},'action_state': 'MonsterRun'},MC_MOVE: {'action_param': (0, ['walk_f', 'lower', 1, {'loop': True}]),'custom_param': {'dynamic_speed_rate': 0.7,'move_acc': 3000,'walk_speed': 13,'brake_acc': -3000},'action_state': 'MonsterWalk'},MC_MONSTER_HIT: {'custom_param': {'hit_anim_rate': 1.5,'hit_anim': 'get_hit','hit_anim_dur': 1.3},'action_state': 'MonsterHit'},MC_IMMOBILIZE: {'action_param': (0, ['idle', 'lower', 1, {'loop': True}]),'action_state': 'Immobilize'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]