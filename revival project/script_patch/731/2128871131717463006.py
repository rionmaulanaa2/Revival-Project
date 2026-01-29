# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/mecha_const.py
from __future__ import absolute_import
_reload_all = True
from logic.gcommon.const import NEOX_UNIT_SCALE
from . import weapon_const
CD_TYPE_COUNTDOWN = 0
CD_TYPE_PROGRESS = 1
KNIGHT_MECHA_ID = 8002
MECHA_TYPE_NONE = 0
MECHA_TYPE_NORMAL = 1
MECHA_TYPE_VEHICLE = 2
MECHA_PATTERN_NORMAL = 1
MECHA_PATTERN_VEHICLE = 2
VEHICLE_STATE_HUMAN = 'trans'
VEHICLE_STATE_VEHICLE = ''
BEAR_STATE_NORMAL = ''
BEAR_STATE_TRANS = 'trans'
TRIO_STATE_M = ''
TRIO_STATE_S = 'S'
TRIO_STATE_R = 'R'
STATE_HUMANOID = 0
STATE_LEVITATE = 1
STATE_INJECT = 2
MECHA_8022_FORM_NORMAL = 1
MECHA_8022_FORM_VEHICLE = 2
MECHA_8032_START_MOVE_FORWARD = 3
MECHA_8032_STOP_MOVE_FORWARD = 4
MECHA_8032_ENTER_SPRINT = 1
MECHA_8032_STOP_SPRINT = 2
MECHA_8032_SHIELD = 803202
VALID_MECHA_STATE = {8501: (
        VEHICLE_STATE_HUMAN, VEHICLE_STATE_VEHICLE),
   8502: (
        VEHICLE_STATE_HUMAN, VEHICLE_STATE_VEHICLE),
   8503: (
        VEHICLE_STATE_HUMAN, VEHICLE_STATE_VEHICLE),
   8504: (
        VEHICLE_STATE_HUMAN, VEHICLE_STATE_VEHICLE),
   8005: (
        BEAR_STATE_NORMAL, BEAR_STATE_TRANS),
   8009: (
        TRIO_STATE_M, TRIO_STATE_S, TRIO_STATE_R)
   }
RECOVER_STATE = {8005: BEAR_STATE_NORMAL
   }
DEFEND_ON = 1
DEFEND_OFF = 0
MECHA_8023_FORM_SNIPE = 'S'
MECHA_8023_FORM_PISTOL = ''
MECHA_8023_STAND = 'stand'
MECHA_8023_MOVE = 'move'
MECHA_8023_RUN = 'run'
MECHA_8023_DASH = 'dash'
MECHA_8023_JUMP_1 = 'jump_1'
MECHA_8023_JUMP_2 = 'jump_2'
TRIGGER_GREANDE_ADD_RANGE_BUFF_ID = 31802302
TRIGGER_C4_ADD_RANGE_BUFF_ID = 31802412
MECHA_8028_FORM_RABBIT = 'rabbit'
MECHA_8028_FORM_FAIRY = 'fairy'
MECHA_8029_FORM_SCOUT = '8029'
MECHA_8029_FORM_HUNT = '8029_S'
MECHA_8032_NORMAL = '8032'
MECHA_8032_SPRINT = '8032_S'
STATE_RIFLE = 1
STATE_SHOTGUN = 2
STATE_RIFLE_VICE = 3
STATE_SHOTGUN_VICE = 4
STATE_SWITCH_RIFLE = 5
STATE_SWITCH_SHOTGUN = 6
STATE_SHOTGUN_RELOAD = 7
STATE_SWITCH_RIFLE_RUN = 8
STATE_SWITCH_SHOTGUN_RUN = 9
STATE_ALL = [
 'rifle_hand', 'shotgun_back', 'rifle_vice_back', 'shotgun_vice_back', 'shotgun_hand', 'rifle_back', 'rifle_hand_l', 'shotgun_hand_l', 'shotgun_vice_hand', 'rifle_vice_hand', 'shotgun_hand_reload']
STATE_VISIBLE = {STATE_RIFLE: [
               [
                'rifle_hand', 'shotgun_back', 'rifle_vice_back', 'shotgun_vice_back'], ['shotgun_change', 'rifle_change', 'shotgun_hand_reload', 'shotgun_hand', 'rifle_back', 'rifle_hand_l', 'shotgun_hand_l', 'shotgun_vice_hand', 'rifle_vice_hand']],
   STATE_SHOTGUN: [
                 [
                  'shotgun_hand', 'rifle_back', 'rifle_vice_back', 'shotgun_vice_back'], ['shotgun_change', 'rifle_change', 'shotgun_hand_reload', 'rifle_hand', 'shotgun_back', 'shotgun_hand_l', 'rifle_hand_l', 'shotgun_vice_hand', 'rifle_vice_hand']],
   STATE_RIFLE_VICE: [
                    [
                     'rifle_hand_l', 'rifle_vice_hand', 'shotgun_vice_back', 'shotgun_back'], ['shotgun_change', 'rifle_change', 'shotgun_hand_reloadrifle_back', 'rifle_hand', 'rifle_vice_back', 'shotgun_hand', 'shotgun_vice_hand', 'shotgun_hand_l']],
   STATE_SHOTGUN_VICE: [
                      [
                       'shotgun_hand_l', 'rifle_vice_hand', 'shotgun_vice_back', 'rifle_back'], ['shotgun_change', 'rifle_change', 'shotgun_hand_reload', 'shotgun_back', 'rifle_vice_back', 'rifle_hand_l', 'shotgun_hand', 'rifle_hand', 'shotgun_vice_hand']],
   STATE_SWITCH_RIFLE: [
                      [
                       'shotgun_back', 'rifle_hand_l', 'rifle_vice_back', 'shotgun_vice_back'], ['shotgun_change', 'rifle_change', 'shotgun_hand_reload', 'rifle_back', 'shotgun_hand_l', 'rifle_hand', 'rifle_vice_hand', 'shotgun_hand', 'shotgun_vice_hand']],
   STATE_SWITCH_SHOTGUN: [
                        [
                         'rifle_back', 'shotgun_hand_l', 'rifle_vice_back', 'shotgun_vice_back'], ['shotgun_change', 'rifle_change', 'shotgun_hand_reload', 'shotgun_back', 'shotgun_hand', 'shotgun_vice_hand', 'rifle_hand_l', 'rifle_hand', 'rifle_vice_hand']],
   STATE_SWITCH_RIFLE_RUN: [
                          [
                           'shotgun_back', 'shotgun_change', 'rifle_vice_back', 'shotgun_vice_back'], ['rifle_change', 'rifle_hand_l', 'shotgun_hand_reload', 'rifle_back', 'shotgun_hand_l', 'rifle_hand', 'rifle_vice_hand', 'shotgun_hand', 'shotgun_vice_hand']],
   STATE_SWITCH_SHOTGUN_RUN: [
                            [
                             'rifle_back', 'rifle_change', 'rifle_vice_back', 'shotgun_vice_back'], ['shotgun_change', 'shotgun_hand_l', 'shotgun_hand_reload', 'shotgun_back', 'shotgun_hand', 'shotgun_vice_hand', 'rifle_hand_l', 'rifle_hand', 'rifle_vice_hand']],
   STATE_SHOTGUN_RELOAD: [
                        [
                         'shotgun_hand_reload', 'rifle_back', 'rifle_vice_back', 'shotgun_vice_back'], ['shotgun_change', 'rifle_change', 'shotgun_hand_l', 'rifle_hand', 'shotgun_back', 'shotgun_hand', 'rifle_hand_l', 'shotgun_vice_hand', 'rifle_vice_hand']]
   }
MECHA_SHOOT_NORMAL = 0
MECHA_SHOOT_QUICK = 1
SHARE_MECHA_FACTOR = 1
SHARE_MECHA_HP_FACTOR = 1
MAX_UP_SPEED = 5 * NEOX_UNIT_SCALE
FALL_GRAVITY = 48 * NEOX_UNIT_SCALE
JET_ACC = -100 * NEOX_UNIT_SCALE
JET_HORI_ACC = 30 * NEOX_UNIT_SCALE
RECOVER_CD = 0.25
ZERO_CD = 0.5
REPAIR_SING = 3.0
REPAIR_HP_PERCENT = 0.15
REPAIR_FULL_ROUND = 3
REPAIR_ROUND_ITVL = 20.0
RECALL_DURATION = 2
MECHA_LEVEL_NEED_EXP = 100
MECHA_MAX_LEVEL = 8
RECALL_CD_TYPE_NORMAL = 1
RECALL_CD_TYPE_DIE = 2
RECALL_CD_TYPE_GETMECHA = 3
RECOVER_CD_TYPE_DISABLE = 4
RECALL_MAXCD_TYPE_GETMECHA = 420
CD_COLLECT_TYPE_HM_DMG = 1
CD_COLLECT_TYPE_HM_DOWN = 2
CD_COLLECT_TYPE_HM_DEAD = 3
CD_COLLECT_TYPE_MC_DMG = 4
CD_COLLECT_TYPE_MC_DESTROY = 5
NENGLIANGTI_CD_RECUDE = 10
MECHA_DAMAGE_CD_REDUCE_TYPE_VALUE = 1
MECHA_DAMAGE_CD_REDUCE_TYPE_FUNC = 2
ATTACHMENT_LEAVE_MECHA = 1
ATTACHMENT_EXPLODE = 2
MAX_MECHA_BODY_CNT = 15
SELF_DESTRUCT = 7
MECHA_BROKEN_WATER_HEIGHT = 4 * NEOX_UNIT_SCALE
MECHA_WATER_BROKEN_TIME = 8
MAX_GRADE = 7
ONE_GRADE_EXP = 100
MODULE_ITEM_COLOR_CONF = {9908: 'red',
   9909: 'blue',
   9910: 'yellow',
   9911: 'sp'
   }
ATTACHMENT_POS_LIST = [
 0, 1]
MODULE_POS_LIST = [0, 1, 2, 3]
MAX_INSTALL_ATTACHMENT_NUM = 2
SP_MODULE_CHOOSE_ITEM_ID = 9911
SP_MODULE_NO_CHOOSE_ITEM_IDS = [99111, 99112]
SP_MODULE_ITEM_ALL_IDS = [9911, 99111, 99112]
SP_MODULE_SLOT = 4
MODULE_ATTACK_SLOT = 1
MODULE_DEFEND_SLOT = 2
MODULE_MOVE_SLOT = 3
MODULE_PLAN_AMOUNT = 2
MODULE_MAX_SLOT_COUNT = 4
MODULE_SP_SLOT_COUNT = 2
MODULE_NORMAL_COUNT = 3
EXERCISE_SP_MODULE_SWITCH_CD = 1
MODULE_CARD_GAIN_VIA_GOT_MECHA = 1
MODULE_CARD_GAIN_VIA_MECHA_PROFICIENCY_REWARD = 2
MODULE_CARD_GAIN_VIA_SHOP_LOTTERY = 3
MODULE_SP_SLOT_ACTIVATE_ITEM_NO = 48000901
MECAH_JUMP_TYPE_DEFAULT = 1
MECHA_JUMP_TYPE_ROCKET = 2
MECHA_JUMP_TYPE_SLASH_JUMP = 3
MECHA_JUMP_TYPE_POISON_JUMP = 4
MECHA_JUMP_TYPE_8034_JUMP = 5
MECHA_JUMP_EXPLOSIVE = {MECAH_JUMP_TYPE_DEFAULT: weapon_const.THROWABLE_JUMP_ITEM_DEFAULT,
   MECHA_JUMP_TYPE_ROCKET: weapon_const.THROWABLE_JUMP_ITEM_ROCKET,
   MECHA_JUMP_TYPE_SLASH_JUMP: weapon_const.THROWABLE_JUMP_ITEM_SLASH_JUMP,
   MECHA_JUMP_TYPE_POISON_JUMP: weapon_const.THROWABLE_JUMP_ITEM_POISON_JUMP,
   MECHA_JUMP_TYPE_8034_JUMP: weapon_const.THROWABLE_JUMP_ITEM_8034_JUMP
   }
MECHA_RUSH_NO_ROCKER = 0
MECHA_RUSH_CAN_ROCKER = 1
MECHA_RUSH_8005 = 2
PHOTON_TOWER_ADD_RANGE_BUFF_ID = 358
PHOTON_TOWER_SECOND_WEAPON_SKILL_ID = 800802
DEFAULT_SOCKET_LIST = [
 'part_point0', 'part_point1', 'part_point2', 'part_point3', 'part_point4', 'part_point5']
MECHA_SOCKET_LIST = ['part_point0', 'part_point1', 'part_point2', 'part_point3', 'part_point4', 'part_point5']
VEHICLE_SOCKET_LIST = ['part_point1']
MONSTER_SOCKET_LIST = ['part_point1']
HUMAN_SOCKET_LIST = ['hit']
HANDY_SHIELD_SOCKET = 'shield'
HANDY_SHIELD_BONE = 'dun_bone_01'
HANDY_SHIELD_MAX_HP = 500
BEACON_8031_Y_OFFSET = 61.1
MECHA_8031_DEFAULT_FASHION = {'1': None,'0': 201803100}
TELPORT_REASON_SKILL = 1
EJECT_REASON_NORMAL = 1
EJECT_REASON_POISON_DAMAGE = 2
EJECT_REASON_OTHERS_DAMAGE = 3
MECHA_12_BUMP_SKILL_ID = 801255
MECHA_12_BALL_STATE_EXTRA_HEIGHT = 23
MECHA_USUAL_USE_MECHA_MAX_SET_NUM = 3
MECHA_TYPE = [
 '', 'spec_burst', 'spec_sustain', 'spec_sinpe', 'spec_strike', 'spec_ranger', 'spec_heavy']
MECHA_TYPE_ID = [12013, 607504, 607505, 607506, 607507, 607508, 607509]
SKIN_RARE_BACKGROUND = {0: 'gui/ui_res_2/mech_display/img_skin_frame_a_bar.png',
   2: 'gui/ui_res_2/mech_display/img_skin_frame_b_bar.png',
   3: 'gui/ui_res_2/mech_display/img_skin_frame_a_bar.png',
   4: 'gui/ui_res_2/mech_display/img_skin_frame_s_bar.png',
   5: 'gui/ui_res_2/mech_display/img_skin_frame_a_bar.png',
   6: 'gui/ui_res_2/mech_display/img_skin_frame_s_bar.png',
   7: 'gui/ui_res_2/mech_display/img_skin_frame_a_bar.png'
   }
MECHA_MODE_BLOOD_SOCKET_POS_OFFSET = {8033: {MECHA_PATTERN_VEHICLE: -45}}
EX_REFINE_UPGRADE_TYPE_COLOR = 0
EX_REFINE_UPGRADE_TYPE_SFX = 1
EX_REFINE_UPGRADE_TYPE_FINAL = 2