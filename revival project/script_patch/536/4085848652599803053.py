# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/character_anim_const.py
k_air_friction = 0.0
k_linear_damping = 0.7
k_mix_ratio = 1.0
k_stiffness = 1.0
k_simulation_steps = 30
k_air_friction_idle = 1.0
UP_BODY = 1
LOW_BODY = 2
EXTERN_BODY_1 = 3
LOWER_UP_BODY = 4
UP_BODY_SELECT = 11
LOW_BODY_SELECT = 12
LOW_UP_BODY_SELECT = 13
UP_BODY_ENABLE = 'up_body_action'
LOWER_UP_BODY_ENABLE = 'lower_up_body_action'
LOW_BODY_ENABLE = 'low_body_action'
UP_BODY_DIR_TYPE = 'up_body_blend_type'
LOWER_UP_BODY_DIR_TYPE = 'lower_up_body_blend_type'
LOW_BODY_DIR_TYPE = 'low_body_blend_type'
HAIR_DIR_TYPE = 'hair_blend_type'
HAIR_SINGLE_TYPE = 'hair_single_type'
DEFAULT_UP_BODY_BONE = 2
FULL_BODY_BONE = 1
DEFAULT_UP_BODY_CONFIG = (
 ('biped root', 0), ('biped spine', 1))
FULL_BODY_BONE_CONFIG = (('biped root', 1), )
BIND_OBJ_TYPE_SKATE = 1
BIND_OBJ_TYPE_PARACHUTE = 2
DEBUG_PART_DESC = {UP_BODY: 'UP_BODY',
   LOWER_UP_BODY: 'LOWER_UP_BODY',LOW_BODY: 'LOW_BODY',EXTERN_BODY_1: 'EXTERN_BODY_1'}