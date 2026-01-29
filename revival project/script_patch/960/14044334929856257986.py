# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/CommonInfoUtils.py
from __future__ import absolute_import
import six
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.client.const import tips_const
PRELOAD_TYPE_NONE = 0
PRELOAD_TYPE_BATTLE = 1
PRELOAD_TYPE_TDM = 2
PRELOAD_TYPE_CHICKEN = 4
PRELOAD_TYPE_TDM_FLAG_BATTLE = 8
PRELOAD_TYPE_TDM_CROWN = 16
PRELOAD_TYPE_TDM_CRYSTAL_BATTLE = 32
PRELOAD_TYPE_TDM_MUTIOCCUPY_BATTLE = 64
PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE = 128
PRELOAD_TYPE_TDM_SCAVENGE_BATTLE = 256
PRELOAD_TYPR_TDM_TRAIN_BATTLE = 512
PRELOAD_TYPE_TDM_FLAG2_BATTLE = 1024
PRELOAD_TYPE_TDM_SNATCHEGG_BATTLE = 2048
PRELOAD_TYPE_PVE = 4096
TEMPLATE_PATH = {battle_const.FALL_RETURN_LEFT_TIMES: (
                                       'battle/i_fight_newmap_backtips', PRELOAD_TYPE_CHICKEN),
   battle_const.MAIN_ENHANCE_INFO: (
                                  'battle_tips/common_tips/i_enhance_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_FIGHT_CAPACITY_UPGRADE: (
                                            'battle_tips/common_tips/fight_point_tips', PRELOAD_TYPE_NONE),
   battle_const.MED_KILL_INFO: (
                              'battle_tips/common_tips/i_kill_tips', PRELOAD_TYPE_BATTLE),
   battle_const.MAIN_KILL_KING: (
                               'battle_tips/common_tips/i_kingofkill_tips', PRELOAD_TYPE_NONE),
   battle_const.MED_R_EQUIPMENT_INFO_OLD: (
                                         'battle_tips/common_tips/i_equipment_tips', PRELOAD_TYPE_CHICKEN),
   battle_const.MED_R_EQUIPMENT_INFO: (
                                     'battle_tips/common_tips/i_equipment_tip_strong', PRELOAD_TYPE_NONE),
   battle_const.MED_R_MODUL_INFO: (
                                 'battle_tips/common_tips/i_equipment_tip_strong', PRELOAD_TYPE_BATTLE),
   battle_const.MED_R_EQUIPMENT_INFO_WEAK: (
                                          'battle_tips/common_tips/i_equipment_tip_weak', PRELOAD_TYPE_NONE),
   battle_const.MED_R_MODUL_INFO_WEAK: (
                                      'battle_tips/common_tips/i_equipment_tip_weak', PRELOAD_TYPE_BATTLE),
   battle_const.MED_R_MECHA_RESET_INFO: (
                                       'battle_tips/common_tips/i_equipment_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_RANK_AWAED: (
                                'battle_tips/common_tips/i_rank_tips', PRELOAD_TYPE_CHICKEN),
   battle_const.MAIN_END_KILL_KING: (
                                   'battle_tips/common_tips/i_lose_kingofkill_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_ACE_TIME: (
                              'battle_tips/common_tips/i_ace_time_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_MECHA_RECALL_INFO: (
                                       'battle_tips/common_tips/i_nomecha_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_SOUND_VISIBLE_INFO: (
                                        'battle_tips/common_tips/i_soundvisible_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_B_SIDE_TEN_POINTS: (
                                            'battle_tips/koth_tips/i_bluepoint_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_R_SIDE_TEN_POINTS: (
                                            'battle_tips/koth_tips/i_redpoint_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_O_SIDE_TEN_POINTS: (
                                            'battle_tips/koth_tips/i_orangepoint_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_LEFT_TIME: (
                                    'battle/i_time_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_OCCUPY: (
                                 'battle_tips/koth_tips/i_koth_occupy_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_OCCUPY_POINT: (
                                       'battle_tips/koth_tips/i_koth_me_occupy_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_DAMAGE_POINT: (
                                       'battle_tips/koth_tips/i_koth_player_point_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_RESCUE_POINT: (
                                       'battle_tips/koth_tips/i_koth_rescue_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_KILL_POINT: (
                                     'battle_tips/koth_tips/i_koth_kill_tips', PRELOAD_TYPE_TDM),
   battle_const.MAIN_KOTH_REVENGE_POINT: (
                                        'battle_tips/koth_tips/i_koth_revenge_tips', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_END_COMBO_KILL_POINT: (
                                               'battle_tips/koth_tips/i_koth_shutdown_kill', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_END_COMBO_KILL_POINT_ALL: (
                                                   'battle_tips/koth_tips/i_koth_shutdown_kill2', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_COMBO_KILL_POINT: (
                                           'battle_tips/koth_tips/i_koth_continue_kill', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_COMBO_KILL_POINT_ALL: (
                                               'battle_tips/koth_tips/i_koth_continue_kill2', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KOTH_KILL_MECHA_POINT: (
                                           'battle_tips/koth_tips/i_koth_kill_mech_tips', PRELOAD_TYPE_TDM),
   battle_const.TDM_BLUE_FIRST_ARRIVE_40_POINT: (
                                               'battle_tips/tdm_tips/i_tdm_bluepoint_tips', PRELOAD_TYPE_TDM),
   battle_const.TDM_RED_FIRST_ARRIVE_40_POINT: (
                                              'battle_tips/tdm_tips/i_tdm_redpoint_tips', PRELOAD_TYPE_TDM),
   battle_const.TDM_ABOUT_TO_GET_MODULE_UPGRADE: (
                                                'battle_tdm/i_module_upgrade_tips', PRELOAD_TYPE_TDM),
   battle_const.TDM_THREE_TIMES_POINT: (
                                      'battle_tips/tdm_tips/i_3times_point_tips', PRELOAD_TYPE_TDM),
   battle_const.FLAG_BATTLE_ACE_BUFF_TIP: (
                                         'battle_tips/tdm_tips/i_3times_flag_point_tips', PRELOAD_TYPE_TDM),
   battle_const.TDM_THREE_TIMES_POINT_NEW: (
                                          'battle_tips/common_tips/i_3times_point_tips_tdm', PRELOAD_TYPE_TDM),
   battle_const.COMMON_AIM_POISON_TIPS: (
                                       'battle_tips/common_tips/i_in_poison_tips', PRELOAD_TYPE_CHICKEN),
   battle_const.MAIN_NODE_PLAYER_LEVEL_UP: (
                                          'battle_tips/common_tips/i_role_level_new', PRELOAD_TYPE_CHICKEN),
   battle_const.TDM_OTHER_KILL_KING: (
                                    'battle_tips/tdm_tips/i_others_mvp_tips', PRELOAD_TYPE_TDM),
   battle_const.TDM_KILL_TIPS: (
                              'battle_tips/tdm_tips/i_achieve_tdm_tips', PRELOAD_TYPE_TDM | PRELOAD_TYPE_CHICKEN | PRELOAD_TYPE_PVE),
   battle_const.TDM_ACHIEVE_TIPS: (
                                 'battle_tips/koth_tips/i_koth_continue_kill2', PRELOAD_TYPE_TDM),
   battle_const.COMMON_OTHER_FIRST_BLOOD: (
                                         'battle_tips/tdm_tips/i_others_first_blood_tips', PRELOAD_TYPE_NONE),
   battle_const.TDM_BLUE_DOOR_DESTROYED: (
                                        'battle_tips/tdm_tips/i_door_break_blue', PRELOAD_TYPE_TDM),
   battle_const.TDM_BLUE_DOOR_RECOVER: (
                                      'battle_tips/tdm_tips/i_door_recover_blue', PRELOAD_TYPE_TDM),
   battle_const.TDM_RED_DOOR_DESTROYED: (
                                       'battle_tips/tdm_tips/i_door_break_red', PRELOAD_TYPE_TDM),
   battle_const.TDM_RED_DOOR_RECOVER: (
                                     'battle_tips/tdm_tips/i_door_recover_red', PRELOAD_TYPE_TDM),
   battle_const.MAIN_WILL_ACE_TIME: (
                                   'battle_tips/common_tips/i_ace_time_predict_tips', PRELOAD_TYPE_NONE),
   battle_const.TDM_COME_HOME: (
                              'battle_tips/tdm_tips/i_lose_point', PRELOAD_TYPE_TDM),
   battle_const.SECOND_ACE_TIME: (
                                'battle_tips/common_tips/i_ace_time2_tips', PRELOAD_TYPE_TDM),
   battle_const.ZOMBIEFFA_ACE_TIME: (
                                   'battle_tips/common_tips/i_ace_time3_tips', PRELOAD_TYPE_NONE),
   battle_const.ZOMBIEFFA_MECHA_EXTINCTION: (
                                           'battle_ffa3/ffa3_kill_broadcast', PRELOAD_TYPE_NONE),
   battle_const.FLAG_BATTLE_ACE_TIME: (
                                     'battle_tips/common_tips/i_ace_time4_tips', PRELOAD_TYPE_TDM),
   battle_const.SECOND_ACE_TIME_NEW: (
                                    'battle_tips/common_tips/i_ace_time2_tips_tdm', PRELOAD_TYPE_TDM),
   battle_const.FFA_BLOODTHIRST_BUFF: (
                                     'battle_tips/ffa_tips/i_ffa_powerup_tips', PRELOAD_TYPE_NONE),
   battle_const.BATTLE_LEFT_TIME: (
                                 'battle_tips/ffa_tips/i_count_30_tips', PRELOAD_TYPE_NONE),
   battle_const.FFA_COUNT_POINT: (
                                'battle_tips/ffa_tips/i_count_point', PRELOAD_TYPE_NONE),
   battle_const.ARMRACE_LEFT_TIME: (
                                  'battle_tips/arms_race_tips/i_count_30_tips', PRELOAD_TYPE_NONE),
   battle_const.ARMRACE_ACE_TIME: (
                                 'battle_tips/arms_race_tips/i_arms_race_acetime_tips', PRELOAD_TYPE_NONE),
   battle_const.ARMRACE_UZI_TIP: (
                                'battle_tips/arms_race_tips/i_arms_race_uzi_tips', PRELOAD_TYPE_NONE),
   battle_const.ARMRACE_LEVEL_UP: (
                                 'battle_tips/arms_race_tips/i_arms_race_levelup_tips', PRELOAD_TYPE_NONE),
   battle_const.ARMRACE_LEVEL_DOWN: (
                                   'battle_tips/arms_race_tips/i_demotion_tips', PRELOAD_TYPE_NONE),
   battle_const.ARMRACE_BLOODTHIRST_BUFF: (
                                         'battle_tips/arms_race_tips/i_arms_race_catchup_tips', PRELOAD_TYPE_NONE),
   battle_const.RANDOM_DEATH_GET_ITEM_TIP: (
                                          'battle_random/random_item_tips', PRELOAD_TYPE_NONE),
   battle_const.RANDOM_DEATH_LOST_ITEM_TIP: (
                                           'battle_random/random_item_dis_tips', PRELOAD_TYPE_NONE),
   battle_const.RANDOM_DEATH_GET_WEAPON_TIP: (
                                            'battle_random/random_weapon_tip', PRELOAD_TYPE_NONE),
   battle_const.GVG_KILL_TIPS: (
                              'battle_tips/gvg_tips/i_gvg_kill_tips', PRELOAD_TYPE_NONE),
   battle_const.GVG_MULTI_KILL_TIPS: (
                                    'battle_tips/gvg_tips/i_gvg_sp_kill_tips', PRELOAD_TYPE_BATTLE),
   battle_const.GRANBELM_PORTAL_REFRESH_TIPS: (
                                             'battle_tips/full_moon/i_portal_tips', PRELOAD_TYPE_NONE),
   battle_const.ONLY_JOIN_ONE_SHARE_MECHA_TIPS: (
                                               'battle_tips/brv2_tips/i_only_one_mecha_tips', PRELOAD_TYPE_NONE),
   battle_const.TEAMMATE_LOCATE_UI: (
                                   'battle/fight_teammate_scene', PRELOAD_TYPE_TDM),
   battle_const.MAIN_NODE_RESCUE_FAILED_REASON: (
                                               'battle_tips/common_tips/i_recruit_tips', PRELOAD_TYPE_CHICKEN),
   battle_const.MAIN_MED_GET_ITEM_INFO: (
                                       'battle_tips/common_tips/i_med_get_item_tip', PRELOAD_TYPE_NONE),
   battle_const.CONCERT_SINGLE_BEAT: (
                                    'activity/activity_202109/kizuna/ai_dacall/i_ai_dacall_game1', PRELOAD_TYPE_NONE),
   battle_const.CONCERT_MULTIPLE_BEAT: (
                                      'activity/activity_202109/kizuna/ai_dacall/i_ai_dacall_game2', PRELOAD_TYPE_NONE),
   battle_const.CONCERT_LONG_BEAT: (
                                  'activity/activity_202109/kizuna/ai_dacall/i_ai_dacall_game3', PRELOAD_TYPE_NONE),
   battle_const.CONCERT_PLAYER_NORMAL_ROUND_REWARD: (
                                                   'activity/activity_202212/music_lottery/i_music_lottery_got_normal', PRELOAD_TYPE_NONE),
   battle_const.CONCERT_PLAYER_FINAL_ROUND_REWARD: (
                                                  'activity/activity_202212/music_lottery/i_music_lottery_got_end', PRELOAD_TYPE_NONE),
   battle_const.CONCERT_RECEIVED_REWARD: (
                                        'activity/activity_202212/music_lottery/i_music_lottery_got_self', PRELOAD_TYPE_NONE),
   tips_const.LOBBY_SUB_CHARM_INFO: (
                                   'common/i_charm_up', PRELOAD_TYPE_NONE),
   battle_const.FLAG_BATTLE_FLAG_BASE_BLUE_LOCATE_UI: (
                                                     'battle_flagsnatch/i_flaghome_mark_blue', PRELOAD_TYPE_TDM_FLAG_BATTLE),
   battle_const.FLAG_BATTLE_FLAG_BASE_RED_LOCATE_UI: (
                                                    'battle_flagsnatch/i_flaghome_mark_red', PRELOAD_TYPE_TDM_FLAG_BATTLE),
   battle_const.FLAG_BATTLE_FLAG_LOCATE_UI: (
                                           'battle_flagsnatch/i_flag_mark', PRELOAD_TYPE_TDM_FLAG_BATTLE),
   battle_const.FLAG_BATTLE_FLAG_PICKED_SELF_TEAM: (
                                                  'battle_flagsnatch/i_get_flag_blue', PRELOAD_TYPE_TDM_FLAG_BATTLE),
   battle_const.FLAG_BATTLE_FLAG_PICKED_OTHER_TEAM: (
                                                   'battle_flagsnatch/i_get_flag_red', PRELOAD_TYPE_TDM_FLAG_BATTLE),
   battle_const.FLAG_BATTLE_FLAG_RECOVER_TO_ORIGIN: (
                                                   'battle_flagsnatch/i_none_flag', PRELOAD_TYPE_TDM_FLAG_BATTLE),
   battle_const.FLAG_BATTLE_FLAG_DROPPED_SELF_TEAM: (
                                                   'battle_flagsnatch/i_throw_flag_blue', PRELOAD_TYPE_TDM_FLAG_BATTLE),
   battle_const.FLAG_BATTLE_FLAG_DROPPED_OTHER_TEAM: (
                                                    'battle_flagsnatch/i_throw_flag_red', PRELOAD_TYPE_TDM_FLAG_BATTLE),
   battle_const.FLAG_BATTLE_FLAG_PLANTED_SELF_TEAM: (
                                                   'battle_flagsnatch/i_win_flag_blue', PRELOAD_TYPE_TDM_FLAG_BATTLE),
   battle_const.FLAG_BATTLE_FLAG_PLANTED_OTHER_TEAM: (
                                                    'battle_flagsnatch/i_win_flag_red', PRELOAD_TYPE_TDM_FLAG_BATTLE),
   battle_const.BOUNTY_CENTER_TIPS: (
                                   'battle_tips/bounty_tips/i_bounty_tips', PRELOAD_TYPE_NONE),
   battle_const.RECRUITMENT_BATTLE_ACCEPT: (
                                          'battle_recruit/i_recruit_accept', PRELOAD_TYPE_NONE),
   battle_const.RECRUITMENT_BATTLE_LEAVE: (
                                         'battle_recruit/i_recruit_leave', PRELOAD_TYPE_NONE),
   battle_const.RECRUITMENT_BATTLE_REJECT: (
                                          'battle_recruit/i_recruit_reject', PRELOAD_TYPE_NONE),
   battle_const.CROWN_BATTLE_CROWN_SELF_LOCATE_UI: (
                                                  'battle_king/i_king_mark_yellow', PRELOAD_TYPE_TDM_CROWN),
   battle_const.CROWN_BATTLE_CROWN_TEAMMATE_LOCATE_UI: (
                                                      'battle_king/i_king_mark_blue', PRELOAD_TYPE_TDM_CROWN),
   battle_const.CROWN_BATTLE_CROWN_OTHER_LOCATE_UI: (
                                                   'battle_king/i_king_mark_red', PRELOAD_TYPE_TDM_CROWN),
   battle_const.CROWN_BATTLE_CROWN_TEAM_BORN_TIPS: (
                                                  'battle_king/i_king_tips_appear_blue', PRELOAD_TYPE_TDM_CROWN),
   battle_const.CROWN_BATTLE_CROWN_TEAM_DIE_TIPS: (
                                                 'battle_king/i_king_tips_kill_blue', PRELOAD_TYPE_TDM_CROWN),
   battle_const.CROWN_BATTLE_CROWN_OTHER_BORN_TIPS: (
                                                   'battle_king/i_king_tips_appear_red', PRELOAD_TYPE_TDM_CROWN),
   battle_const.CROWN_BATTLE_CROWN_OTHER_DIE_TIPS: (
                                                  'battle_king/i_king_tips_kill_red', PRELOAD_TYPE_TDM_CROWN),
   battle_const.FIRE_BATTLE_IMMUNE_TIPS: (
                                        'battle_fire/i_fire_tips_buff', PRELOAD_TYPE_NONE),
   battle_const.FIRE_BATTLE_HAVE_AWARD_TIPS: (
                                            'battle_fire/i_fire_tips_award', PRELOAD_TYPE_NONE),
   battle_const.FIRE_BATTLE_FIRE_STATE_TIPS: (
                                            'battle_fire/i_fire_tips_state', PRELOAD_TYPE_NONE),
   battle_const.CRYSTAL_BATTLE_CRYSTAL_MARK_BLUE: (
                                                 'battle_crystal/i_crystal_mark_blue', PRELOAD_TYPE_TDM_CRYSTAL_BATTLE),
   battle_const.CRYSTAL_BATTLE_CRYSTAL_MARK_RED: (
                                                'battle_crystal/i_crystal_mark_red', PRELOAD_TYPE_TDM_CRYSTAL_BATTLE),
   battle_const.MUTIOCCUPY_BECOME_KING: (
                                       'battle_control/i_control_tips', PRELOAD_TYPE_TDM_MUTIOCCUPY_BATTLE),
   battle_const.MUTIOCCUPY_USE_ITEM: (
                                    'battle_control/i_control_tips2', PRELOAD_TYPE_TDM_MUTIOCCUPY_BATTLE),
   battle_const.MUTIOCCUPY_SELF_OCCUPY_A: (
                                         'battle_control/i_control_tips_blue_a', PRELOAD_TYPE_TDM_MUTIOCCUPY_BATTLE),
   battle_const.MUTIOCCUPY_SELF_OCCUPY_B: (
                                         'battle_control/i_control_tips_blue_b', PRELOAD_TYPE_TDM_MUTIOCCUPY_BATTLE),
   battle_const.MUTIOCCUPY_SELF_OCCUPY_C: (
                                         'battle_control/i_control_tips_blue_c', PRELOAD_TYPE_TDM_MUTIOCCUPY_BATTLE),
   battle_const.MUTIOCCUPY_ENEMY_OCCUPY_A: (
                                          'battle_control/i_control_tips_red_a', PRELOAD_TYPE_TDM_MUTIOCCUPY_BATTLE),
   battle_const.MUTIOCCUPY_ENEMY_OCCUPY_B: (
                                          'battle_control/i_control_tips_red_b', PRELOAD_TYPE_TDM_MUTIOCCUPY_BATTLE),
   battle_const.MUTIOCCUPY_ENEMY_OCCUPY_C: (
                                          'battle_control/i_control_tips_red_c', PRELOAD_TYPE_TDM_MUTIOCCUPY_BATTLE),
   battle_const.TDM_PRE_NOTIFY_ROGUE_GIFT: (
                                          'battle_tips/tdm_tips/i_tdm_rogue_ready', PRELOAD_TYPE_TDM),
   battle_const.TDM_CHOOSE_ROGUE_NOT_IN_BASE: (
                                             'battle_tips/tdm_tips/i_tdm_rogue_unprepared', PRELOAD_TYPE_TDM),
   battle_const.ADCRYSTAL_TIP_ATK_START: (
                                        'battle_crystal/battle_crystal_start_tips_red', PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE),
   battle_const.ADCRYSTAL_TIP_DEF_START: (
                                        'battle_crystal/battle_crystal_start_tips', PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE),
   battle_const.ADCRYSTAL_TIP_SEC_STAGE_ATK: (
                                            'battle_crystal/i_battle_crystal2_tips_stage2_1_red', PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE),
   battle_const.ADCRYSTAL_TIP_SEC_STAGE_DEF: (
                                            'battle_crystal/i_battle_crystal2_tips_stage2_1', PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE),
   battle_const.ADCRYSTAL_TIP_POS_CHANGE_ATK: (
                                             'battle_crystal/i_battle_crystal2_tips_stage2_2_red', PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE),
   battle_const.ADCRYSTAL_TIP_POS_CHANGE_DEF: (
                                             'battle_crystal/i_battle_crystal2_tips_stage2_2', PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE),
   battle_const.ADCRYSTAL_TIP_LOW_HP_BUFF_ATK: (
                                              'battle_crystal/i_battle_crystal2_tips_buff_red', PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE),
   battle_const.ADCRYSTAL_TIP_LOW_HP_BUFF_DEF: (
                                              'battle_crystal/i_battle_crystal2_tips_buff', PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE),
   battle_const.ADCRYSTAL_TIP_LOW_DIE_CNT_BUFF_ATK: (
                                                   'battle_crystal/i_battle_crystal2_tips_buff', PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE),
   battle_const.ADCRYSTAL_TIP_LOW_DIE_CNT_BUFF_DEF: (
                                                   'battle_crystal/i_battle_crystal2_tips_buff_red', PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE),
   battle_const.ADCRYSTAL_TIP_PRE_CRYSTAL_DESTROY_ATK: (
                                                      'battle_crystal/i_battle_crystal2_tips_destory_red', PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE),
   battle_const.ADCRYSTAL_TIP_PRE_CRYSTAL_DESTROY_DEF: (
                                                      'battle_crystal/i_battle_crystal2_tips_destory', PRELOAD_TYPE_TDM_ADCRYSTAL_BATTLE),
   battle_const.SCAVENGE_TIP_GAME_START: (
                                        'battle_pick_up/battle_pick_start_tips', PRELOAD_TYPE_TDM_SCAVENGE_BATTLE),
   battle_const.SCAVENGE_TIP_WEAPON_PICKED_BY_GROUPMATE: (
                                                        'battle_pick_up/battle_pick_got_tips_teammate', PRELOAD_TYPE_TDM_SCAVENGE_BATTLE),
   battle_const.SCAVENGE_TIP_WEAPON_PICKED_BY_ENEMY: (
                                                    'battle_pick_up/battle_pick_got_tips_enemy', PRELOAD_TYPE_TDM_SCAVENGE_BATTLE),
   battle_const.TRAIN_USE_SKILL_PUSH: (
                                     'battle_push_train/i_battle_push_train_tips_skill_enemy', PRELOAD_TYPR_TDM_TRAIN_BATTLE),
   battle_const.TRAIN_USE_SKILL_STOP: (
                                     'battle_push_train/i_battle_push_train_tips_skill_teammate', PRELOAD_TYPR_TDM_TRAIN_BATTLE),
   battle_const.TRAIN_USE_NORMAL_SKILL: (
                                       'battle_push_train/i_battle_push_train_tips_skill_use', PRELOAD_TYPR_TDM_TRAIN_BATTLE),
   battle_const.TRAIN_TIP_ATK_START: (
                                    'battle_push_train/battle_push_train_start_tips_blue', PRELOAD_TYPR_TDM_TRAIN_BATTLE),
   battle_const.TRAIN_TIP_DEF_START: (
                                    'battle_push_train/battle_push_train_start_tips_red', PRELOAD_TYPR_TDM_TRAIN_BATTLE),
   battle_const.TRAIN_CAN_USE_SKILL: (
                                    'battle_push_train/i_battle_push_train_tips_skill', PRELOAD_TYPR_TDM_TRAIN_BATTLE),
   battle_const.TRAIN_ARRIVE_STATION: (
                                     'battle_push_train/i_battle_push_train_tips_route', PRELOAD_TYPR_TDM_TRAIN_BATTLE),
   battle_const.TRAIN_ARRIVE_END: (
                                 'battle_push_train/battle_push_train_tips_arrive', PRELOAD_TYPR_TDM_TRAIN_BATTLE),
   battle_const.TRAIN_USE_ALL_TIME: (
                                   'battle_push_train/battle_push_train_tips_timeout', PRELOAD_TYPR_TDM_TRAIN_BATTLE),
   battle_const.MAGIC_MONSTER_TIP: (
                                  'battle_hunter/i_battle_hunter_monster_tips_1', PRELOAD_TYPE_NONE),
   battle_const.MAGIC_GET_ITEM: (
                               'battle_hunter/i_battle_hunter_item_introduce_1', PRELOAD_TYPE_NONE),
   battle_const.MAGIC_USE_MAGIC: (
                                'battle_hunter/i_battle_hunter_item_tips_green_use', PRELOAD_TYPE_NONE),
   battle_const.MAGIC_ACHIEVE: (
                              'battle_hunter/i_achieve_hunter_tips', PRELOAD_TYPE_NONE),
   battle_const.FLAG2_BATTLE_FLAG_PICKED_SELF_TEAM: (
                                                   'battle_flagsnatch2/battle_flagsnatch2_got_status_1', PRELOAD_TYPE_TDM_FLAG2_BATTLE),
   battle_const.FLAG2_BATTLE_FLAG_PICKED_OTHER_TEAM: (
                                                    'battle_flagsnatch2/battle_flagsnatch2_got_status_2', PRELOAD_TYPE_TDM_FLAG2_BATTLE),
   battle_const.FLAG2_BATTLE_FLAG_PLANTED_SELF_TEAM: (
                                                    'battle_flagsnatch2/battle_flagsnatch2_plant_status_1', PRELOAD_TYPE_TDM_FLAG2_BATTLE),
   battle_const.FLAG2_BATTLE_FLAG_PLANTED_OTHER_TEAM: (
                                                     'battle_flagsnatch2/battle_flagsnatch2_plant_status_2', PRELOAD_TYPE_TDM_FLAG2_BATTLE),
   battle_const.FLAG2_BATTLE_START_TIP: (
                                       'battle_flagsnatch2/battle_flagsnatch2_start', PRELOAD_TYPE_TDM_FLAG2_BATTLE),
   battle_const.FLAG2_BATTLE_FLAG_BASE_BLUE_LOCATE_UI: (
                                                      'battle_flagsnatch/i_flaghome_mark_blue', PRELOAD_TYPE_TDM_FLAG2_BATTLE),
   battle_const.FLAG2_BATTLE_FLAG_BASE_RED_LOCATE_UI: (
                                                     'battle_flagsnatch/i_flaghome_mark_red', PRELOAD_TYPE_TDM_FLAG2_BATTLE),
   battle_const.FLAG2_BATTLE_FLAG_DROPPED_SELF_TEAM: (
                                                    'battle_flagsnatch/i_throw_flag_blue', PRELOAD_TYPE_TDM_FLAG2_BATTLE),
   battle_const.FLAG2_BATTLE_FLAG_DROPPED_OTHER_TEAM: (
                                                     'battle_flagsnatch/i_throw_flag_red', PRELOAD_TYPE_TDM_FLAG2_BATTLE),
   battle_const.FLAG2_BATTLE_FLAG_RECOVER_TO_ORIGIN: (
                                                    'battle_flagsnatch/i_none_flag', PRELOAD_TYPE_TDM_FLAG2_BATTLE),
   battle_const.SNATCHEGG_ROUND_TIP: (
                                    'battle_golden_egg/battle_golden_egg_round_tips', PRELOAD_TYPE_TDM_SNATCHEGG_BATTLE),
   battle_const.OUR_GROUP_PICK_EGG_TIP: (
                                       'battle_golden_egg/i_battle_golden_egg_got_tips_blue', PRELOAD_TYPE_TDM_SNATCHEGG_BATTLE),
   battle_const.OTHER_GROUP_PICK_EGG_TIP: (
                                         'battle_golden_egg/i_battle_golden_egg_got_tips_red', PRELOAD_TYPE_TDM_SNATCHEGG_BATTLE),
   battle_const.OUR_GROUP_DROP_EGG_TIP: (
                                       'battle_golden_egg/i_battle_golden_egg_drop_tips_blue', PRELOAD_TYPE_TDM_SNATCHEGG_BATTLE),
   battle_const.OUR_GROUP_DROP_LAST_EGG_TIP: (
                                            'battle_golden_egg/i_battle_golden_egg_drop_tips', PRELOAD_TYPE_TDM_SNATCHEGG_BATTLE),
   battle_const.OTHER_GROUP_DROP_EGG_TIP: (
                                         'battle_golden_egg/i_battle_golden_egg_drop_tips_red', PRELOAD_TYPE_TDM_SNATCHEGG_BATTLE),
   battle_const.SNATCHEGG_CREATE_EGG_TIP: (
                                         'battle_golden_egg/i_battle_golden_egg_refresh_tips', PRELOAD_TYPE_TDM_SNATCHEGG_BATTLE),
   battle_const.SNATCHEGG_BATTLE_EGG_LOCATE_UI: (
                                               'battle_golden_egg/i_battle_golden_egg_mark', PRELOAD_TYPE_TDM_SNATCHEGG_BATTLE),
   battle_const.DUEL_ROUND_TIP: (
                               'battle_duel/battle_duel_tips_round', PRELOAD_TYPE_NONE),
   battle_const.DUEL_ROUND_TIP2: (
                                'battle_duel/battle_duel_tips_start', PRELOAD_TYPE_NONE),
   battle_const.GOOSEBEAR_MAP_COLLAPSE_TIP: (
                                           'battle_happy_push/i_battle_happy_push_tips_collapse', PRELOAD_TYPE_NONE),
   battle_const.GOOSEBEAR_OVER_GRAVITY_FIRST_TIP: (
                                                 'battle_happy_push/i_battle_happy_push_tips_gravity', PRELOAD_TYPE_NONE),
   battle_const.GOOSEBEAR_OVER_GRAVITY_REFRESH_TIP: (
                                                   'battle_happy_push/i_battle_happy_push_tips_gravity_refresh', PRELOAD_TYPE_NONE),
   battle_const.GOOSEBEAR_GAME_START_TIP: (
                                         'battle_happy_push/i_battle_happy_push_tips_start', PRELOAD_TYPE_NONE),
   battle_const.GOOSEBEAR_PROP_FIRST_TIP: (
                                         'battle_happy_push/i_battle_happy_push_tips_prop_refresh', PRELOAD_TYPE_NONE),
   battle_const.GOOSEBEAR_PROP_REFRESH_TIP: (
                                           'battle_happy_push/i_battle_happy_push_tips_prop_refresh_small', PRELOAD_TYPE_NONE),
   battle_const.GOOSEBEAR_LESS_GRAVITY_FIRST_TIP: (
                                                 'battle_happy_push/i_battle_happy_push_tips_gravity2', PRELOAD_TYPE_NONE),
   battle_const.GOOSEBEAR_LESS_GRAVITY_REFRESH_TIP: (
                                                   'battle_happy_push/i_battle_happy_push_tips_gravity_refresh2', PRELOAD_TYPE_NONE),
   battle_const.ASSAULT_TEAMMATE_PLAYER_TIP: (
                                            'battle_assault/battle_assault_tips_change_blue', PRELOAD_TYPE_NONE),
   battle_const.ASSAULT_ENEMY_PLAYER_TIP: (
                                         'battle_assault/battle_assault_tips_change_red', PRELOAD_TYPE_NONE),
   battle_const.ASSAULT_GAME_START_TIP: (
                                       'battle_assault/battle_assault_tips_start', PRELOAD_TYPE_NONE),
   battle_const.NBOMB_DEVICE_EXPLOSION: (
                                       'battle_bomb/i_battle_bomb_tip_end', PRELOAD_TYPE_NONE),
   battle_const.NBOMB_DEVICE_PLACE_ERROR: (
                                         'battle_bomb/i_battle_bomb_tip_region', PRELOAD_TYPE_NONE),
   battle_const.NBOMB_DEVICE_PLACE_SUCCEED: (
                                           'battle_bomb/i_battle_bomb_tip_start', PRELOAD_TYPE_NONE),
   battle_const.NBOMB_DEVICE_REMOVE: (
                                    'battle_bomb/i_battle_bomb_tip_destroyed', PRELOAD_TYPE_NONE),
   battle_const.NBOMB_DEVICE_BE_HIT: (
                                    'battle_bomb/i_battle_bomb_tip_atked', PRELOAD_TYPE_NONE),
   battle_const.NBOMB_DEVICE_STATUS_ERROR: (
                                          'battle_bomb/i_battle_bomb_tip_region', PRELOAD_TYPE_NONE),
   battle_const.NBOMB_CORE_APPEAR: (
                                  'battle_bomb/i_battle_bomb_tip_core_appear', PRELOAD_TYPE_NONE),
   battle_const.NBOMB_CORE_TRANSFER: (
                                    'battle_bomb/i_battle_bomb_tip_core_appear', PRELOAD_TYPE_NONE),
   battle_const.NBOMB_CORE_COLLECT_COMPLETE: (
                                            'battle_bomb/i_battle_bomb_tip_core_complete', PRELOAD_TYPE_NONE),
   battle_const.NBOMB_CORE_DROP: (
                                'battle_bomb/i_battle_bomb_tip_core_drop', PRELOAD_TYPE_NONE),
   battle_const.NBOMB_CORE_PICKUP: (
                                  'battle_bomb/i_battle_bomb_tip_core_picked', PRELOAD_TYPE_NONE),
   battle_const.COMMON_SURVIVAL_SS_KILL_MESSAGE: (
                                                'battle/i_kill_message_mecha_skin_2', PRELOAD_TYPE_NONE),
   battle_const.COMMON_SURVIVAL_SS_KILL_MESSAGE_PC: (
                                                   'battle/i_kill_message_mecha_skin_2_pc', PRELOAD_TYPE_NONE),
   battle_const.COMMON_SURVIVAL_KILL_MVP_MESSAGE: (
                                                 'battle/i_mvp_kill_message', PRELOAD_TYPE_NONE),
   battle_const.COMMON_SURVIVAL_KILL_MVP_MESSAGE_PC: (
                                                    'battle/i_mvp_kill_message_pc', PRELOAD_TYPE_NONE),
   battle_const.MAIN_KILL_MVP: (
                              'battle_tips/i_kill_mvp', PRELOAD_TYPE_NONE),
   battle_const.DEATH_DOOR_DISAPPEAR: (
                                     'battle_tips/tdm_tips/i_tdm_tips_near_enemy_disappear', PRELOAD_TYPE_TDM),
   battle_const.PVE_LEVEL_PORTAL: (
                                 'battle_tips/pve/i_portal_tips', PRELOAD_TYPE_NONE)
   }
PVE_CACHE_SIZE_DICT = {battle_const.TDM_KILL_TIPS: 3
   }
NON_PC_ONLY_TEMPLATE_PATH = {battle_const.COMMON_SURVIVAL_SS_KILL_MESSAGE: (
                                                'battle/i_kill_message_mecha_skin_2', PRELOAD_TYPE_BATTLE),
   battle_const.COMMON_SURVIVAL_KILL_MVP_MESSAGE: (
                                                 'battle/i_mvp_kill_message', PRELOAD_TYPE_BATTLE)
   }
PC_ONLY_TEMPLATE_PATH = {battle_const.COMMON_SURVIVAL_SS_KILL_MESSAGE_PC: (
                                                   'battle/i_kill_message_mecha_skin_2_pc', PRELOAD_TYPE_BATTLE),
   battle_const.COMMON_SURVIVAL_KILL_MVP_MESSAGE_PC: (
                                                    'battle/i_mvp_kill_message_pc', PRELOAD_TYPE_BATTLE)
   }
VISIBLE_SPECIAL_SETTING = {battle_const.COMMON_AIM_POISON_TIPS: False
   }

def preload_battle_ui(battle_type):
    from logic.gcommon.common_utils.battle_utils import get_play_type_by_battle_id
    from logic.client.const import game_mode_const
    if global_data.is_pc_mode:
        TEMPLATE_PATH.update(PC_ONLY_TEMPLATE_PATH)
    else:
        TEMPLATE_PATH.update(NON_PC_ONLY_TEMPLATE_PATH)
    preload_types = PRELOAD_TYPE_BATTLE
    play_type = get_play_type_by_battle_id(battle_type)
    if play_type in battle_const.PLAY_TYPE_TDMS:
        preload_types |= PRELOAD_TYPE_TDM
    elif play_type in (battle_const.PLAY_TYPE_CHICKEN, battle_const.PLAY_TYPE_HUMAN, battle_const.PLAY_TYPE_CHICKEN_FAST):
        preload_types |= PRELOAD_TYPE_CHICKEN
    game_mode_dict = {game_mode_const.GAME_MODE_FLAG: PRELOAD_TYPE_TDM_FLAG_BATTLE,
       game_mode_const.GAME_MODE_CROWN: PRELOAD_TYPE_TDM_CROWN,
       game_mode_const.GAME_MODE_CRYSTAL: PRELOAD_TYPE_TDM_CRYSTAL_BATTLE,
       game_mode_const.GAME_MODE_TRAIN: PRELOAD_TYPR_TDM_TRAIN_BATTLE,
       game_mode_const.GAME_MODE_FLAG2: PRELOAD_TYPE_TDM_FLAG2_BATTLE
       }
    if global_data.game_mode.is_pve():
        preload_types |= PRELOAD_TYPE_PVE
    for game_mode in six.iterkeys(game_mode_dict):
        if global_data.game_mode.is_mode_type(game_mode):
            preload_types |= game_mode_dict[game_mode]

    preload_json_paths = [ path for itype, (path, ptypes) in six.iteritems(TEMPLATE_PATH) if ptypes & preload_types ]
    global_data.ui_pool.preload_ui(preload_json_paths)
    if global_data.game_mode.is_pve():
        global_data.ui_pool.set_cache_size_dict(PVE_CACHE_SIZE_DICT)
        for itype, num in PVE_CACHE_SIZE_DICT.items():
            tips_path, ptypes = TEMPLATE_PATH.get(itype, ['', 0])
            if ptypes & preload_types:
                num_paths = [tips_path] * (num - 1) if num - 1 > 0 else []
                global_data.ui_pool.preload_ui(num_paths)


def create_ui(itype, parent, repos=True, resize=False):
    data = TEMPLATE_PATH.get(itype)
    if data:
        ui = global_data.ui_pool.create_ui(data[0], parent, repos, resize)
        return ui
    else:
        return None
        return None


def destroy_ui(ui):
    global_data.ui_pool.destroy_ui(ui)


def set_show_num(node, num):
    node.SetString(str(num))


def set_show_lv_num(node, num):
    node.SetString('{0}{1}'.format('LV', str(num)))


def set_show_point_num(node, num):
    node.SetString('{0}{1}{2}'.format('+' if num > 0 else '-', abs(num), get_text_by_id(155)))


def set_show_normal_point_num(node, num):
    node.SetString('{0}{1}'.format(abs(num), get_text_by_id(155)))


def set_show_percent_num(node, num):
    node.SetString('{0}{1}'.format(str(num), '%'))


def set_show_minute_num(node, num):
    node.SetString(get_text_by_id(10256).format(data=num))


def set_fall_return_num(panel, num):
    color = 16188996 if num <= 1 else 16220418
    panel.temp_num.lab_num.SetString(str(num + 1))
    panel.temp_num.lab_num_2.SetString(str(num))
    panel.temp_num.lab_num.SetColor(color)
    panel.temp_num.lab_num_2.SetColor(color)
    panel.temp_num.PlayAnimation('show')