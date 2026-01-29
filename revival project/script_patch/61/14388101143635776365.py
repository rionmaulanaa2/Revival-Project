# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/c_guide_data.py
_reload_all = True
DataDict = {'DeathGuide': {'Content': {'death_guide_choose_weapon': {'guilde_handler_params': [
                                                                                    5056, 5]
                                                            },
                              'death_guide_play_rule': {'guilde_handler_params': [
                                                                                5057, 3, 5058, 5]
                                                        },
                              'death_guide_revive': {'guilde_handler_params': [
                                                                             5056, 5]
                                                     }
                              },
                  'Name': '\xe6\xad\xbb\xe6\x96\x97\xe6\x96\xb0\xe6\x89\x8b\xe6\x8c\x87\xe5\xbc\x95',
                  'QuickLink': 1
                  },
   'LobbyGuide': {'Content': {'battle_duel_finish': {'guide_check_handler': 'check_is_not_newbee_guide',
                                                     'guide_handler_params': {'ui_list': {'LobbyDuelModeConfirmUI': {'temp_func': 'save_guide_key_with_end'}}},'guide_key': 'battle_duel',
                                                     'guide_order': 2,
                                                     'is_last_one': 1
                                                     },
                              'battle_duel_start': {'guide_check_handler': 'check_is_not_newbee_guide',
                                                    'guide_handler_params': {'ui_list': {'MatchMode': {'temp_func': 'show_guide_duel_panel'}}},'guide_key': 'battle_duel',
                                                    'guide_order': 1,
                                                    'ui_delay_show_t': 1
                                                    },
                              'battle_flag_guide_finish': {'guide_check_handler': 'check_need_battle_flag_guide',
                                                           'guide_handler_params': {'ui_list': {'PlayerBattleFlagWidget': {'temp_func': 'save_guide_key_with_end'}}},'guide_key': 'battle_flag',
                                                           'guide_order': 4,
                                                           'is_last_one': 1
                                                           },
                              'battle_flag_guide_lobby': {'guide_check_handler': 'check_need_battle_flag_guide',
                                                          'guide_handler_params': {'ui_list': {'LobbyUI': {'temp_func': 'show_top_guide_temp','template_path': 'common/i_guide_right_below','parent': 'btn_head','layer': 18,'text': 82218}}},'guide_key': 'battle_flag',
                                                          'guide_order': 1
                                                          },
                              'battle_flag_guide_page': {'guide_check_handler': 'check_need_battle_flag_guide',
                                                         'guide_handler_params': {'ui_list': {'PlayerInfoUI': {'temp_func': 'show_top_guide_temp','text': 82218,'template_path': 'common/i_guide_right_below','parent': {'func': 'get_battle_flag_page_guide_parent_node'},'layer': 21}}},'guide_key': 'battle_flag',
                                                         'guide_order': 2
                                                         },
                              'battle_flag_guide_setting': {'guide_check_handler': 'check_need_battle_flag_guide',
                                                            'guide_handler_params': {'ui_list': {'PlayerInfoUI': {'page': 'PlayerBattleFlagWidget','temp_func': 'show_top_guide_temp','text': 82218,'parent': 'btn_set','layer': 21}}},'guide_key': 'battle_flag',
                                                            'guide_order': 3
                                                            },
                              'inscr_guide_1_finish': {'guide_check_handler': 'check_need_inscr_guide_1',
                                                       'guide_handler_params': {'ui_list': {'': {'temp_func': 'save_guide_key_with_end'}}},'guide_key': 'inscr_1',
                                                       'guide_order': 4,
                                                       'is_last_one': 1,
                                                       'post_guide_conf': {'delay': 2.0,'to': 'inscr_guide_bag'
                                                                           },
                                                       'priority': 2
                                                       },
                              'inscr_guide_bag': {'guide_check_handler': 'check_need_inscr_guide_3',
                                                  'guide_handler_params': {'ui_list': {'InscriptionMainUI': {'temp_func': 'show_top_guide_temp','text': 81856,'template_path': 'common/i_guide_right_below','parent': {'func': 'get_inscr_list_btn'},'layer': 21,'enable_vis_tick': 1}}},'guide_key': 'inscr_3',
                                                  'guide_order': 1,
                                                  'pre_guide': 'inscr_guide_1_finish',
                                                  'priority': 2,
                                                  'ui_delay_show_t': 2
                                                  },
                              'inscr_guide_bag_choose': {'guide_check_handler': 'check_need_inscr_guide_3',
                                                         'guide_handler_params': {'ui_list': {'InscriptionMainUI': {'page': 'MechaInscriptionBagWidget','temp_func': 'show_top_guide_temp','text': 81857,'template_path': 'guide/inscription/inscription_guide3','parent': 'list_inscription','layer': 21,'ignore_wpos': 1}}},'guide_key': 'inscr_3',
                                                         'guide_order': 2,
                                                         'priority': 2
                                                         },
                              'inscr_guide_bag_finish': {'guide_check_handler': 'check_need_inscr_guide_3',
                                                         'guide_handler_params': {'ui_list': {'': {'temp_func': 'save_guide_key_with_end'}}},'guide_key': 'inscr_3',
                                                         'guide_order': 3,
                                                         'is_last_one': 1,
                                                         'priority': 2
                                                         },
                              'inscr_guide_choose_tech': {'guide_check_handler': 'check_need_inscr_guide_1',
                                                          'guide_handler_params': {'ui_list': {'InscriptionMainUI': {'page': 'MechaReconstructWidget','temp_func': 'show_top_guide_temp','layer': 21,'text': 81852,'template_path': 'guide/inscription/inscription_guide1','parent': 'nd_add','ignore_wpos': 1}}},'guide_key': 'inscr_1',
                                                          'guide_order': 3,
                                                          'is_trigger_by_hand': 1,
                                                          'priority': 2
                                                          },
                              'inscr_guide_left_arm': {'guide_check_handler': 'check_need_inscr_guide_1',
                                                       'guide_handler_params': {'ui_list': {'InscriptionMainUI': {'page': 'MechaReconstructWidget','temp_func': 'show_top_guide_temp','text': 81851,'template_path': 'common/i_guide_right_top','parent': 'guide_1','dis_click_action': {'nd_1.temp_1.nd_btn.OnClick': [['active_guide_with_finish', 'inscr_guide_choose_tech']],'_else_.OnEnd': [['active_guide_with_finish', 'inscr_guide_choose_recommend0']]}}}},'guide_key': 'inscr_1',
                                                       'guide_order': 2,
                                                       'is_trigger_by_hand': 1,
                                                       'priority': 2
                                                       },
                              'inscr_guide_lobby': {'guide_check_handler': 'check_need_inscr_guide_1',
                                                    'guide_handler_params': {'ui_list': {'LobbyUI': {'temp_func': 'show_top_guide_temp','parent': 'temp_tech','text': 81850}}},'guide_key': 'inscr_1',
                                                    'guide_order': 1,
                                                    'is_trigger_by_hand': 1,
                                                    'priority': 2
                                                    },
                              'lottery_activity_guide_choose': {'guide_check_handler': 'check_need_lottery_activity_guide',
                                                                'guide_handler_params': {'ui_list': {'LotteryActivityChooseUI': {'temp_func': 'show_top_guide_temp','parent': 'nd_title','template': 'common/i_guide_right_top','pos_offset': (30, 75),'text': 12144}}},'guide_key': 'lottery_activity',
                                                                'guide_order': 2
                                                                },
                              'lottery_activity_guide_finish': {'guide_check_handler': 'check_need_lottery_activity_guide',
                                                                'guide_handler_params': {'ui_list': {'LotteryExchangeMallUI': {'temp_func': 'save_guide_key','on_close': 1}}},'guide_key': 'lottery_activity',
                                                                'guide_order': 4
                                                                },
                              'lottery_activity_guide_main': {'guide_check_handler': 'check_need_lottery_activity_guide',
                                                              'guide_handler_params': {'ui_list': {'LotteryMainUI': {'temp_func': 'show_top_guide_temp','parent': 'btn_activity','template': 'common/i_guide_right_below','text': 12143}}},'guide_key': 'lottery_activity',
                                                              'guide_order': 1
                                                              },
                              'lottery_activity_guide_price': {'guide_check_handler': 'check_need_lottery_activity_guide',
                                                               'guide_handler_params': {'ui_list': {'LotteryExchangeMallUI': {'temp_func': 'show_top_guide_temp','parent': 'list_price','template': 'common/i_guide_left_below','pos_offset': (20, 10),'text': 12145}}},'guide_key': 'lottery_activity',
                                                               'guide_order': 3
                                                               },
                              'skin_define_choose': {'guide_check_handler': 'check_need_skin_define_guide',
                                                     'guide_handler_params': {'ui_list': {'MechaDisplay': {'temp_func': 'show_right_top_guide_temp_in_mecha_choose','text': 860142}}},'guide_key': 'skin_define',
                                                     'guide_order': 1
                                                     },
                              'skin_define_end': {'guide_check_handler': 'check_need_skin_define_guide',
                                                  'guide_handler_params': {'ui_list': {'SkinDefineUI': {'temp_func': 'save_guide_key','on_close': 1}}},'guide_key': 'skin_define',
                                                  'guide_order': 3
                                                  },
                              'skin_define_enter': {'guide_check_handler': 'check_need_skin_define_guide',
                                                    'guide_handler_params': {'func': 'show_top_guide_temp_active_by_node','text': 860141,'template_path': 'common/i_guide_left_top'},'guide_key': 'skin_define',
                                                    'guide_order': 2
                                                    },
                              'xingyuan_guide_finish': {'guide_check_handler': 'check_need_xingyuan_guide',
                                                        'guide_handler_params': {'ui_list': {'RoleSkinDefineUI': {'temp_func': 'save_guide_key'}}},'guide_key': 'xingyuan',
                                                        'guide_order': 4,
                                                        'priority': 1
                                                        },
                              'xingyuan_guide_lobby': {'guide_check_handler': 'check_need_xingyuan_guide',
                                                       'guide_handler_params': {'ui_list': {'LobbyUI': {'temp_func': 'show_top_guide_temp','parent': 'temp_role','text': 860103}}},'guide_key': 'xingyuan',
                                                       'guide_order': 1,
                                                       'priority': 1
                                                       },
                              'xingyuan_guide_rolechoose': {'guide_check_handler': 'check_need_xingyuan_guide',
                                                            'guide_handler_params': {'ui_list': {'RoleChooseUI': {'temp_func': 'show_right_top_guide_temp_in_role_choose','text': 860104}}},'guide_key': 'xingyuan',
                                                            'guide_order': 2,
                                                            'priority': 1
                                                            },
                              'xingyuan_guide_roleinfo': {'guide_check_handler': 'check_need_xingyuan_guide',
                                                          'guide_handler_params': {'func': 'show_top_guide_temp_active_by_node','text': 860105,'template_path': 'common/i_guide_left_top'},'guide_key': 'xingyuan',
                                                          'guide_order': 3,
                                                          'priority': 1
                                                          }
                              },
                  'Name': '\xe5\xa4\xa7\xe5\x8e\x85\xe5\xbc\x95\xe5\xaf\xbc',
                  'QuickLink': 1
                  },
   'LocalGuide': {'Content': {101: {'Args': [
                                           5001, 5001, 3],
                                    'InitData': {'pos': [3712, 290, 7476]},'Interface': 'show_human_tips',
                                    'Next': [
                                           201, 202, 203, 204, 205, 206],
                                    'NextShowMainUI': [
                                                     'MoveRockerUI', 'BattleRightTopUI']
                                    },
                              201: {'Args': [
                                           'nd_step_2', 'show_2'],
                                    'Interface': 'show_nd_animation'
                                    },
                              202: {'Args': [
                                           'temp_move_tips'],
                                    'Interface': 'show_drag_layer'
                                    },
                              203: {'Args': [
                                           [
                                            3579, 290, 7415], 'effect/fx/guide/guide_end.sfx'],
                                    'Interface': 'show_sfx'
                                    },
                              204: {'Args': [
                                           [
                                            3579, 290, 7415], 2, 'temp_locate', 'keep'],
                                    'Interface': 'show_locate'
                                    },
                              205: {'Args': [
                                           [
                                            3579, 290, 7415], 1],
                                    'Interface': 'check_move_pos',
                                    'Next': [
                                           301, 302, 303, 304, 305, 306, 307],
                                    'NextShowMainUI': [
                                                     'FrontSightUI', 'WeaponBarSelectUI', 'FireRockerUI', 'BulletReloadUI', 'PostureControlUI'],
                                    'Prior': 101
                                    },
                              206: {'Args': [
                                           5002, 920830, 5],
                                    'Interface': 'show_human_tips'
                                    },
                              301: {'Args': 10012,
                                    'Event': [
                                            'E_AIM_TARGET', 'guide_shoot_show'],
                                    'Interface': 'pick_up_weapon'
                                    },
                              302: {'Args': [
                                           'nd_step_3', 'show_3'],
                                    'Interface': 'show_nd_animation',
                                    'InterfaceType': 2
                                    },
                              303: {'Args': [
                                           [
                                            3226, 290, 7473], 'effect/fx/guide/guide_end.sfx'],
                                    'Interface': 'show_sfx'
                                    },
                              304: {'Args': [
                                           [
                                            3226, 290, 7473], 2, 'temp_locate', 'keep'],
                                    'Interface': 'show_locate'
                                    },
                              305: {'Args': [
                                           0, [3226, 290, 7473], 200],
                                    'Event': [
                                            'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                    'InitData': {'weapons': 10012},'Interface': 'create_robot',
                                    'Next': [
                                           401, 402, 403, 404, 405, 406],
                                    'NextShowMainUI': [
                                                     'PickUI'],
                                    'Prior': 205
                                    },
                              306: {'Args': [
                                           'nd_auto_frame', 'show_auto'],
                                    'Interface': 'show_nd_animation',
                                    'InterfaceType': 2
                                    },
                              307: {'Args': [
                                           5003, 5169, 5],
                                    'Interface': 'show_human_tips'
                                    },
                              401: {'Args': [
                                           6000, [3226, 290, 7473], {10231: 1}],
                                    'Event': [
                                            'E_GUIDE_PICK_END', 'finish_guide'],
                                    'InitData': {'weapons': [10012, 10231]},'Interface': 'create_pick_item',
                                    'Next': [
                                           501, 502],
                                    'Prior': 305
                                    },
                              402: {'Args': [
                                           [
                                            3226, 290, 7473], 'effect/fx/guide/guide_end.sfx'],
                                    'Interface': 'show_sfx'
                                    },
                              403: {'Args': [
                                           [
                                            3226, 290, 7473], 1, 'temp_locate', 'keep'],
                                    'Interface': 'show_locate'
                                    },
                              404: {'Args': [
                                           'nd_step_5', 'show_5'],
                                    'Interface': 'show_nd_animation',
                                    'InterfaceType': 2
                                    },
                              405: {'Args': [
                                           'nd_step_5_1', 'show_5_1'],
                                    'Interface': 'show_nd_animation',
                                    'InterfaceType': 2
                                    },
                              406: {'Args': [
                                           5004, 5004, 5],
                                    'Event': [
                                            'E_GUIDE_PICK_SHOW', 'guide_pick_show'],
                                    'Interface': 'show_human_tips'
                                    },
                              501: {'Args': [
                                           'nd_weapon_1', 'weapon_1'],
                                    'Event': [
                                            'E_TRY_SWITCH', 'guide_switch_end'],
                                    'InitData': {'weapons': [10231, 10012]},'Interface': 'show_nd_animation',
                                    'Next': [
                                           601, 602, 603, 604, 605, 606, 607, 608, 609],
                                    'NextShowMainUI': [
                                                     'FightLeftShotUI', 'HpInfoUI', 'FightReadyTipsUI'],
                                    'Prior': 401
                                    },
                              502: {'Args': 10231,
                                    'Interface': 'check_cur_weapon',
                                    'InterfaceType': 1
                                    },
                              601: {'Args': [
                                           5008, 5008, 5],
                                    'Interface': 'show_human_tips'
                                    },
                              602: {'Event': [
                                            'E_SUCCESS_AIM', 'guide_try_aim_success']
                                    },
                              603: {'Event': [
                                            'E_QUIT_AIM', 'guide_quit_aim_success']
                                    },
                              604: {'Args': [
                                           'nd_step_7', 'show_7'],
                                    'Interface': 'show_nd_animation'
                                    },
                              605: {'Args': [
                                           'temp_move_tips'],
                                    'Interface': 'show_drag_layer',
                                    'InterfaceType': 2
                                    },
                              606: {'Args': [
                                           'nd_step_8', 'show_8'],
                                    'Interface': 'show_nd_animation',
                                    'InterfaceType': 2
                                    },
                              607: {'Args': [
                                           [
                                            2920, 292, 7282], 'effect/fx/guide/guide_end.sfx'],
                                    'Interface': 'show_sfx'
                                    },
                              608: {'Args': [
                                           [
                                            2920, 292, 7282], 2, 'temp_locate', 'keep'],
                                    'Interface': 'show_locate'
                                    },
                              609: {'Args': [
                                           0, [2920, 292, 7282], 200],
                                    'Event': [
                                            'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                    'InitData': {'weapons': [10012, 10231]},'Interface': 'create_robot_aim',
                                    'Next': [
                                           901, 902, 903],
                                    'NextShowMainUI': [
                                                     'MechaUI', 'BattleInfoUI', 'MechaChargeUI', 'MechaControlMain', 'MechaHpInfoUI', 'MechaCockpitUI'],
                                    'Prior': 501
                                    },
                              701: {'Args': [
                                           'temp_use_tips', 'show'],
                                    'Event': [
                                            'E_GUIDE_USE_END', 'guide_use_end'],
                                    'InitData': {'weapons': [1011, 10231],'mecha_progress': 100},'Interface': 'show_drag_layer',
                                    'Next': [
                                           901, 902, 903],
                                    'NextShowMainUI': [
                                                     'MechaUI', 'BattleInfoUI', 'MechaChargeUI', 'MechaControlMain', 'MechaHpInfoUI', 'MechaCockpitUI'],
                                    'Prior': 609
                                    },
                              702: {'Interface': 'guide_quit_aim',
                                    'InterfaceType': 1
                                    },
                              703: {'Args': [
                                           5009, 5009, 5],
                                    'Interface': 'show_human_tips'
                                    },
                              801: {'Args': [
                                           [
                                            2903, 290, 7665], 'effect/fx/guide/guide_end.sfx'],
                                    'Interface': 'show_sfx'
                                    },
                              802: {'Args': [
                                           [
                                            2903, 290, 7665], 2, 'temp_locate', 'keep'],
                                    'Interface': 'show_locate'
                                    },
                              803: {'Args': [
                                           5010, 5010, 5],
                                    'Interface': 'show_human_tips'
                                    },
                              804: {'Args': [
                                           'nd_step_13', 'show_13_charging'],
                                    'Interface': 'show_nd_animation',
                                    'InterfaceType': 2
                                    },
                              805: {'Args': [
                                           9907, [2903, 290, 7665]],
                                    'Event': [
                                            'E_GUIDE_CHARGER_END', 'guide_charger_end'],
                                    'InitData': {'weapons': [1011, 10231],'mecha_progress': 100},'Interface': 'mecha_charger',
                                    'Next': [
                                           901, 902, 903],
                                    'Prior': 701
                                    },
                              806: {'Interface': 'check_mecha_charger',
                                    'InterfaceType': 1
                                    },
                              901: {'Args': [
                                           'nd_step_13', 'show_13'],
                                    'Event': [
                                            'E_GUIDE_MECHA_UI_SHOW', 'guide_mecha_ui_show'],
                                    'Interface': 'show_nd_animation'
                                    },
                              902: {'Event': [
                                            'E_ON_JOIN_MECHA_START', 'guide_call_mecha_end'],
                                    'InitData': {'weapons': [10012, 10231],'mecha': 8001},'Interface': 'mecha_progress',
                                    'Next': [
                                           1101, 1102, 1103, 1104, 1105],
                                    'Prior': 609
                                    },
                              903: {'Args': [
                                           5012, 5012, 5],
                                    'Interface': 'show_human_tips'
                                    },
                              1101: {'Args': [
                                            5013, 5013, 5],
                                     'Interface': 'show_human_tips'
                                     },
                              1102: {'Args': [
                                            'nd_step_16', 'show_16'],
                                     'Interface': 'show_nd_animation'
                                     },
                              1103: {'Args': [
                                            [
                                             2988, 289, 7368], 'effect/fx/guide/guide_end.sfx'],
                                     'Interface': 'show_sfx'
                                     },
                              1104: {'Args': [
                                            [
                                             2988, 289, 7368], 2, 'temp_locate', 'keep'],
                                     'Interface': 'show_locate'
                                     },
                              1105: {'Args': [
                                            0, [2988, 289, 7368], 200],
                                     'Event': [
                                             'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                     'InitData': {'weapons': [10012, 10231],'mecha': 8001},'Interface': 'create_robot_fire',
                                     'Next': [
                                            1201, 1202, 1203, 1204, 1205, 1206],
                                     'Prior': 902
                                     },
                              1201: {'Args': [
                                            5015, 5015, 5],
                                     'Interface': 'show_human_tips'
                                     },
                              1202: {'Args': [
                                            'nd_step_17', 'show_17'],
                                     'Interface': 'show_nd_animation'
                                     },
                              1203: {'Args': [
                                            [
                                             2800, 290, 7436], 'effect/fx/guide/guide_end.sfx'],
                                     'Interface': 'show_sfx'
                                     },
                              1204: {'Args': [
                                            [
                                             2800, 290, 7436], 2, 'temp_locate', 'keep'],
                                     'Interface': 'show_locate'
                                     },
                              1205: {'Args': [
                                            0, [2800, 290, 7436], 200],
                                     'Event': [
                                             'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead_skill'],
                                     'Interface': 'create_robot_skill',
                                     'Prior': 1105
                                     },
                              1206: {'Interface': 'mecha_recovery',
                                     'InterfaceType': 1
                                     }
                              },
                  'Name': '\xe6\x9c\xac\xe5\x9c\xb0\xe6\x96\xb0\xe6\x89\x8b\xe6\x8c\x87\xe5\xbc\x95',
                  'QuickLink': 1
                  },
   'LocalGuideDamage': {'Content': {1101: {'head_hit': 45,
                                           'other_hit': 20
                                           },
                                    8999: {'head_hit': 45,
                                           'other_hit': 20
                                           },
                                    10231: {'head_hit': 70,
                                            'other_hit': 40
                                            },
                                    800251: {'head_hit': 200,
                                             'other_hit': 200
                                             }
                                    },
                        'Name': '\xe6\x9c\xac\xe5\x9c\xb0\xe4\xbc\xa4\xe5\xae\xb3\xe9\x85\x8d\xe7\xbd\xae',
                        'QuickLink': 1
                        },
   'LocalGuideParams': {'Content': {'barrier_pos': {'var_val': [
                                                              2974, 290, 7501]
                                                    },
                                    'barrier_range': {'var_val': 100
                                                      },
                                    'barrier_size': {'var_val': [
                                                               300, 50, 1]
                                                     },
                                    'charge_rate': {'var_val': 40
                                                    },
                                    'mecha_second_weapon_damage': {'var_val': 70
                                                                   }
                                    },
                        'Name': '\xe9\x80\x9a\xe7\x94\xa8\xe5\x8f\x82\xe6\x95\xb0\xe9\x85\x8d\xe7\xbd\xae',
                        'QuickLink': 1
                        },
   'LocalHandler': {'Content': {'guide_call_mecha_end': {'handler_params': 902
                                                         },
                                'guide_charger_end': {'handler_params': 805
                                                      },
                                'guide_quit_aim_success': {'handler_params': [
                                                                            604, [605, 606]]
                                                           },
                                'guide_switch_show': {'handler_params': 501
                                                      },
                                'guide_try_aim_success': {'handler_params': [
                                                                           604, [605, 606]]
                                                          },
                                'guide_use_end': {'handler_params': 701
                                                  }
                                },
                    'Name': '\xe6\x9c\xac\xe5\x9c\xb0\xe6\x96\xb0\xe6\x89\x8b\xe6\x8c\x87\xe5\xbc\x95Handler',
                    'QuickLink': 1
                    },
   'QTEGuide': {'Content': {100: {'Args': [
                                         101, 102],
                                  'InitData': {'pos': [3601, 290, 7458],'yaw': -1.5},'Interface': 'on_sub_guide_progress'
                                  },
                            101: {'Args': [
                                         100],
                                  'Interface': 'save_guide_progress'
                                  },
                            102: {'Args': [
                                         5434, 3],
                                  'Interface': 'show_human_tips',
                                  'Next': 200
                                  },
                            200: {'Args': [
                                         201, 202, 203, 204, 205, 206, 207, 208, 209],
                                  'InitData': {'pos': [3601, 290, 7458],'yaw': -1.8},'Interface': 'on_sub_guide_progress',
                                  'PCArgs': [
                                           201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
                                  },
                            201: {'Args': [
                                         200],
                                  'Interface': 'save_guide_progress'
                                  },
                            202: {'Args': [
                                         'MoveRockerUI', 'BattleRightTopUI', 'BattleInfoUI', 'BattleLeftBottomUI'],
                                  'Interface': 'show_ui'
                                  },
                            203: {'Args': [
                                         5435, 5],
                                  'Interface': 'show_human_tips',
                                  'PCArgs': [
                                           5452, 5]
                                  },
                            204: {'Args': [
                                         'nd_step_2', 'show_2'],
                                  'Interface': 'play_guide_ui_animation'
                                  },
                            205: {'Args': [
                                         'temp_move_tips'],
                                  'Interface': 'show_guide_ui_nd'
                                  },
                            206: {'Args': [
                                         [
                                          3601, 291, 7458], [3519, 291, 7500], 'effect/fx/guide/guide_vfx.sfx'],
                                  'Interface': 'show_route'
                                  },
                            207: {'Args': [
                                         [
                                          3519, 290, 7500], 'effect/fx/guide/guide_end.sfx'],
                                  'Interface': 'show_sfx'
                                  },
                            208: {'Args': [
                                         [
                                          3519, 290, 7500], 2, 'temp_locate', 'keep'],
                                  'Interface': 'show_locate'
                                  },
                            209: {'Args': [
                                         [
                                          3519, 290, 7500], 1],
                                  'Interface': 'check_move_pos',
                                  'Next': 300
                                  },
                            210: {'Interface': 'disable_hotkey',
                                  'PCArgs': [
                                           'HUMAN_SQUAT', 'HUMAN_JUMP', 'HUMAN_ROLL', 'SWITCH_BATTLE_BAG', 'SWITCH_PC_MODE', 'SUMMON_CALL_MECHA']
                                  },
                            300: {'Args': [
                                         301, 302, 303, 304, 305, 306, 307, 308, 309],
                                  'InitData': {'pos': [3519, 290, 7443],'yaw': -1.38,'show_ui': ['MoveRockerUI', 'BattleRightTopUI', 'BattleInfoUI', 'BattleLeftBottomUI'],'pre_steps': [209]},'Interface': 'on_sub_guide_progress',
                                  'PCArgs': [
                                           301, 302, 303, 304, 305, 306, 307, 308, 309, 310]
                                  },
                            301: {'Args': [
                                         300],
                                  'Interface': 'save_guide_progress'
                                  },
                            302: {'Args': [
                                         5436, 10],
                                  'Interface': 'show_human_tips',
                                  'PCArgs': [
                                           5445, 10]
                                  },
                            303: {'Args': [
                                         'FrontSightUI', 'WeaponBarSelectUI', 'BattleHitFeedBack', 'FireRockerUI', 'BulletReloadUI', 'PostureControlUI'],
                                  'Interface': 'show_ui'
                                  },
                            304: {'Args': [
                                         'PostureControlUI', ['nd_squat', 'nd_roll'], False],
                                  'Interface': 'set_ui_nd_visibility'
                                  },
                            305: {'Args': [
                                         10012],
                                  'Interface': 'give_weapon'
                                  },
                            306: {'Args': [
                                         'nd_step_3', 'show_3'],
                                  'Event': [
                                          'E_AIM_TARGET', 'guide_shoot_show'],
                                  'Interface': 'shoot_tips_on_aim'
                                  },
                            307: {'Args': [
                                         [
                                          3339, 292, 7458], 'effect/fx/guide/guide_end.sfx'],
                                  'Interface': 'show_sfx'
                                  },
                            308: {'Args': [
                                         [
                                          3339, 292, 7458], 2, 'temp_locate', 'keep'],
                                  'Interface': 'show_locate'
                                  },
                            309: {'Args': [{'hp': 200,'max_hp': 200,'init_max_hp': 200,'is_fight': False,'npc_id': 9001,'position': [3339, 292, 7458],'faction_id': None}],'Event': [
                                          'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                  'Interface': 'create_monster',
                                  'Next': 400
                                  },
                            310: {'Interface': 'enable_hotkey',
                                  'PCArgs': [
                                           'HUMAN_JUMP']
                                  },
                            400: {'Args': [
                                         401, 402, 403, 404, 405],
                                  'InitData': {'pos': [3519, 290, 7443],'yaw': -1.38,'show_ui': ['MoveRockerUI', 'BattleRightTopUI', 'BattleInfoUI', 'BattleLeftBottomUI', 'FrontSightUI', 'WeaponBarSelectUI', 'BattleHitFeedBack', 'FireRockerUI', 'BulletReloadUI', 'PostureControlUI'],'weapon': 10012,'pre_steps': [209, 304, 310]},'Interface': 'on_sub_guide_progress'
                                  },
                            401: {'Args': [
                                         400],
                                  'Interface': 'save_guide_progress'
                                  },
                            402: {'Args': [
                                         5437, 5],
                                  'Interface': 'show_human_tips',
                                  'PCArgs': [
                                           5446, 5]
                                  },
                            403: {'Args': [
                                         [
                                          3226, 290, 7473], 'effect/fx/guide/guide_end.sfx'],
                                  'Interface': 'show_sfx'
                                  },
                            404: {'Args': [
                                         [
                                          3226, 290, 7473], 2, 'temp_locate', 'keep'],
                                  'Interface': 'show_locate'
                                  },
                            405: {'Args': [
                                         [
                                          3226, 290, 7473], 1],
                                  'Interface': 'check_move_pos',
                                  'Next': 500
                                  },
                            500: {'Args': [
                                         501, 502],
                                  'Interface': 'on_sub_guide_progress'
                                  },
                            501: {'Args': [],'Interface': 'camera_push_forward'
                                  },
                            502: {'Args': [
                                         'video/qte_hotsteel_show.mp4'],
                                  'Interface': 'play_video',
                                  'Next': 510
                                  },
                            510: {'Args': [
                                         511, 512, 514],
                                  'Interface': 'on_sub_guide_progress',
                                  'PCArgs': [
                                           511, 512, 513, 514]
                                  },
                            511: {'Args': [
                                         [
                                          2779, 290, 7415], 1.89, 1200, 300],
                                  'Interface': 'create_ai_mecha'
                                  },
                            512: {'Args': [
                                         'PostureControlUI', ['nd_roll'], True],
                                  'Interface': 'set_ui_nd_visibility'
                                  },
                            513: {'Interface': 'disable_mouse_keyboard',
                                  'PCArgs': []},
                            514: {'Args': [
                                         [
                                          3226, 290, 7473], -1.68],
                                  'Event': [
                                          'E_QTE_VIDEO_FINISH', 'on_qte_video_finish'],
                                  'Interface': 'adjust_pos_yaw',
                                  'Next': 600
                                  },
                            600: {'Args': [
                                         601, 603],
                                  'InitData': {'pos': [3226, 290, 7473],'yaw': -1.68,'show_ui': ['MoveRockerUI', 'BattleRightTopUI', 'BattleInfoUI', 'BattleLeftBottomUI', 'FrontSightUI', 'WeaponBarSelectUI', 'BattleHitFeedBack', 'FireRockerUI', 'BulletReloadUI', 'PostureControlUI'],'weapon': 10012,'pre_steps': [209, 310, 511]},'Interface': 'on_sub_guide_progress',
                                  'PCArgs': [
                                           601, 602, 603]
                                  },
                            601: {'Args': [
                                         600],
                                  'Interface': 'save_guide_progress'
                                  },
                            602: {'Interface': 'disable_mouse_ctrl',
                                  'PCArgs': []},
                            603: {'Args': [
                                         'FightLeftShotUI', 'HpInfoUI', 'FightReadyTipsUI'],
                                  'Interface': 'show_ui',
                                  'Next': 610,
                                  'PCArgs': [
                                           'FightLeftShotUI', 'HpInfoUI', 'FightReadyTipsUI', 'BattleControlUIPC']
                                  },
                            610: {'Args': [
                                         611, 612],
                                  'Interface': 'on_sub_guide_progress'
                                  },
                            611: {'Args': [
                                         5438, 'step_1', 0],
                                  'Interface': 'qte_guide_step',
                                  'PCArgs': [
                                           5447, 'step_1', 0]
                                  },
                            612: {'Event': [
                                          'E_MOVE_ROCK', 'on_rocker_move_left'],
                                  'Interface': 'rocker_move_left',
                                  'Next': 620
                                  },
                            620: {'Args': [
                                         621, 622, 623],
                                  'Interface': 'on_sub_guide_progress',
                                  'PCArgs': [
                                           621, 622, 623]
                                  },
                            621: {'Args': [
                                         5439, 'step_2', 0.4],
                                  'Interface': 'qte_guide_step',
                                  'PCArgs': [
                                           5451, 'step_2', 0.4]
                                  },
                            622: {'Args': [
                                         0.4, 0.3, 0.1],
                                  'Event': [
                                          'E_CLICK_ROLL', 'on_click_roll'],
                                  'Interface': 'click_roll_btn',
                                  'Next': 630
                                  },
                            623: {'Args': [
                                         511],
                                  'Interface': 'ai_mecha_fire'
                                  },
                            624: {'Interface': 'enable_hotkey',
                                  'PCArgs': [
                                           'HUMAN_ROLL']
                                  },
                            630: {'Args': [
                                         631],
                                  'Interface': 'on_sub_guide_progress'
                                  },
                            631: {'Args': [
                                         1.0, 0.1],
                                  'Interface': 'ai_mecha_fire_finish',
                                  'Next': 700
                                  },
                            700: {'Args': [
                                         701, 703, 704, 705, 706, 707],
                                  'InitData': {'pos': [3223, 290, 7369],'yaw': -1.58,'show_ui': ['MoveRockerUI', 'BattleRightTopUI', 'BattleInfoUI', 'BattleLeftBottomUI', 'FrontSightUI', 'WeaponBarSelectUI', 'BattleHitFeedBack', 'FireRockerUI', 'BulletReloadUI', 'PostureControlUI', 'FightLeftShotUI', 'HpInfoUI', 'FightReadyTipsUI'],'weapon': 10012,'pre_steps': [209, 310, 511, 624]},'Interface': 'on_sub_guide_progress',
                                  'PCArgs': [
                                           701, 702, 703, 704, 705, 706, 707, 708]
                                  },
                            701: {'Args': [
                                         700],
                                  'Interface': 'save_guide_progress'
                                  },
                            702: {'Interface': 'resume_mouse_ctrl',
                                  'PCArgs': []},
                            703: {'Interface': 'resume_bullet_tick'
                                  },
                            704: {'Args': [
                                         5440, 15],
                                  'Interface': 'show_human_tips',
                                  'PCArgs': [
                                           5440, 15]
                                  },
                            705: {'Args': [
                                         'MechaUI', 'BattleInfoUI', 'MechaChargeUI', 'MechaControlMain', 'MechaHpInfoUI', 'MechaCockpitUI', 'MechaFuelUI'],
                                  'Interface': 'show_ui'
                                  },
                            706: {'Args': [
                                         'nd_step_13', 'show_13'],
                                  'Interface': 'play_guide_ui_animation'
                                  },
                            707: {'Event': [
                                          'E_CLICK_SUMMON_MECHA', 'on_click_summon'],
                                  'Interface': 'check_summon_mecha',
                                  'Next': 800
                                  },
                            708: {'Interface': 'enable_hotkey',
                                  'PCArgs': [
                                           'SUMMON_CALL_MECHA']
                                  },
                            800: {'Args': [
                                         801],
                                  'Interface': 'on_sub_guide_progress'
                                  },
                            801: {'Args': [{'11': 'video/qte_firefox_show.mp4','12': 'video/qte_arthur_show.mp4'}],'Interface': 'play_mecha_show_video',
                                  'Next': 810
                                  },
                            810: {'Args': [
                                         811, 812, 815],
                                  'Interface': 'on_sub_guide_progress',
                                  'PCArgs': [
                                           811, 812, 813, 814, 815]
                                  },
                            811: {'Event': [
                                          'E_GUIDE_MECHA_STATE_CHANGE', 'hide_leave_mecha'],
                                  'Interface': 'dummy_func'
                                  },
                            812: {'Args': [{'11': 8001,'12': 8002}, [3223, 290, 7369], -1.58],'Interface': 'summon_mecha'
                                  },
                            813: {'Interface': 'disable_hotkey',
                                  'PCArgs': [
                                           'SUMMON_CALL_MECHA']
                                  },
                            814: {'Interface': 'disable_mouse_keyboard',
                                  'PCArgs': []},
                            815: {'Event': [
                                          'E_QTE_VIDEO_FINISH', 'on_qte_video_finish'],
                                  'Interface': 'dummy_func',
                                  'Next': 900
                                  },
                            900: {'Args': [
                                         901, 902, 903, 904, 905, 906, 907],
                                  'InitData': {'pos': [3223, 290, 7369],'yaw': -1.58,'show_ui': ['MoveRockerUI', 'BattleRightTopUI', 'BattleInfoUI', 'BattleLeftBottomUI', 'FrontSightUI', 'WeaponBarSelectUI', 'BattleHitFeedBack', 'FireRockerUI', 'BulletReloadUI', 'PostureControlUI', 'FightLeftShotUI', 'HpInfoUI', 'FightReadyTipsUI', 'MechaUI', 'BattleInfoUI', 'MechaChargeUI', 'MechaControlMain', 'MechaHpInfoUI', 'MechaCockpitUI', 'MechaFuelUI'],'weapon': 10012,'pre_steps': [209, 310, 511, 624, 811, 812, 813]},'Interface': 'on_sub_guide_progress',
                                  'PCArgs': [
                                           901, 902, 903, 904, 905, 906, 907, 908]
                                  },
                            901: {'Args': [
                                         900],
                                  'Interface': 'save_guide_progress'
                                  },
                            902: {'Args': [
                                         5441, 5],
                                  'Interface': 'show_human_tips',
                                  'PCArgs': [
                                           5441, 5]
                                  },
                            903: {'Args': [
                                         511, 6, 'temp_locate', 'keep'],
                                  'Interface': 'show_mecha_locate'
                                  },
                            904: {'Interface': 'hide_sub_weapon_btn'
                                  },
                            905: {'Args': [
                                         'nd_step_16', 'show_16'],
                                  'Interface': 'play_guide_ui_animation'
                                  },
                            906: {'Event': [
                                          'E_GUIDE_MECHA_AGONY', 'on_guide_mecha_agony'],
                                  'Interface': 'check_guide_mecha_agony',
                                  'Next': 1000
                                  },
                            907: {'Args': [
                                         511],
                                  'Interface': 'qte_mecha_shoot'
                                  },
                            908: {'Interface': 'disable_hotkey',
                                  'PCArgs': [
                                           'MECHA_SUB']
                                  },
                            1000: {'Args': [
                                          1001, 1002, 1003],
                                   'Interface': 'on_sub_guide_progress',
                                   'PCArgs': [
                                            1001, 1002, 1003, 1004, 1005, 1006]
                                   },
                            1001: {'Interface': 'show_ui'
                                   },
                            1002: {'Args': [
                                          5442, 'step_3'],
                                   'Interface': 'qte_guide_step',
                                   'PCArgs': [
                                            5448, 'step_3']
                                   },
                            1003: {'Interface': 'check_sub_weapon_click',
                                   'Next': 1100
                                   },
                            1004: {'Interface': 'disable_camera_yaw',
                                   'PCArgs': []},
                            1005: {'Interface': 'disable_keyboard_and_mouse_left',
                                   'PCArgs': []},
                            1006: {'Interface': 'enable_hotkey',
                                   'PCArgs': [
                                            'MECHA_SUB']
                                   },
                            1100: {'Args': [
                                          1101],
                                   'Interface': 'on_sub_guide_progress'
                                   },
                            1101: {'Args': [{'11': 'video/qte_firefox_execute.mp4','12': 'video/qte_arthur_execute.mp4'}],'Interface': 'play_execute_video',
                                   'Next': 1200
                                   },
                            1200: {'Args': [
                                          1201, 1202, 1203],
                                   'Interface': 'on_sub_guide_progress',
                                   'PCArgs': [
                                            1201, 1202, 1204, 1203]
                                   },
                            1201: {'Interface': 'save_qte_guide_finish'
                                   },
                            1202: {'Interface': 'open_create_role_ui'
                                   },
                            1203: {'Interface': 'quit_qte_battle'
                                   },
                            1204: {'Interface': 'enable_hotkey',
                                   'PCArgs': [
                                            'HUMAN_SQUAT', 'HUMAN_JUMP', 'HUMAN_ROLL', 'SWITCH_BATTLE_BAG', 'SWITCH_PC_MODE', 'SUMMON_CALL_MECHA', 'MECHA_SUB']
                                   }
                            },
                'Name': 'QTE\xe6\x96\xb0\xe6\x89\x8b\xe6\x8c\x87\xe5\xbc\x95',
                'QuickLink': 1
                },
   'RemoteGuide': {'Content': {'remote_ace_time': {'guilde_handler_params': [
                                                                           5402, 5]
                                                   },
                               'remote_binder': {'guilde_handler_params': [
                                                                         5414, 3.5]
                                                 },
                               'remote_board_water': {'guilde_handler_params': [
                                                                              1044, 5]
                                                      },
                               'remote_call_mecha': {'guilde_handler_params': [
                                                                             1025, 5]
                                                     },
                               'remote_carrier': {'guilde_handler_params': [
                                                                          1019, 5]
                                                  },
                               'remote_destroy_mecha': {'guilde_handler_params': [
                                                                                1036, 5]
                                                        },
                               'remote_froze_weapon': {'guilde_handler_params': [
                                                                               5413, 3.5]
                                                       },
                               'remote_guide_collect': {'guilde_handler_params': [
                                                                                5023, 5]
                                                        },
                               'remote_guide_entity': {'guilde_handler_params': {1: [
                                                                                   2, 5026, 5],
                                                                                 2: [
                                                                                   2, 5027, 5],
                                                                                 3: [
                                                                                   2, 5036, 5]
                                                                                 }
                                                       },
                               'remote_guide_escape': {'guilde_handler_params': [
                                                                               5024, 5]
                                                       },
                               'remote_guide_mecha': {'guilde_handler_params': [
                                                                              80116, 5]
                                                      },
                               'remote_guide_parachute': {'guilde_handler_params': [
                                                                                  5021, 5022, 3, 4]
                                                          },
                               'remote_helmet': {'guilde_handler_params': [
                                                                         1038, 5]
                                                 },
                               'remote_mecha_accelerator': {'guilde_handler_params': [
                                                                                    5410, 3.5]
                                                            },
                               'remote_mecha_die_accelerator': {'guilde_handler_params': [
                                                                                        5411, 3.5]
                                                                },
                               'remote_mecha_dun': {'guilde_handler_params': [
                                                                            1045, 5]
                                                    },
                               'remote_mecha_energy': {'guilde_handler_params': [
                                                                               5400, 5]
                                                       },
                               'remote_mecha_stamina_60': {'guilde_handler_params': [
                                                                                   5403, 5]
                                                           },
                               'remote_mecha_thunder': {'guilde_handler_params': [
                                                                                5412, 3.5]
                                                        },
                               'remote_module_guide': {'guilde_handler_params': [
                                                                               5300, 5]
                                                       },
                               'remote_shield': {'guilde_handler_params': [
                                                                         1014, 5]
                                                 },
                               'remote_signal_60': {'guilde_handler_params': [
                                                                            5415, 3.5]
                                                    },
                               'remote_signal_85': {'guilde_handler_params': [
                                                                            5405, 5]
                                                    },
                               'remote_stamina_85': {'guilde_handler_params': [
                                                                             5404, 5]
                                                     },
                               'remote_weapon_missile': {'guilde_handler_params': [
                                                                                 1022, 5]
                                                         }
                               },
                   'Name': '\xe5\xb1\x80\xe5\x86\x85\xe6\x96\xb0\xe6\x89\x8b\xe6\x8c\x87\xe5\xbc\x95',
                   'QuickLink': 1
                   },
   'SpecialGuide': {'Content': {'special_call_mecha': {'guilde_handler_params': [
                                                                               862002, 5]
                                                       },
                                'special_double_click': {'guilde_handler_params': [
                                                                                 1013, 5]
                                                         }
                                },
                    'Name': '\xe7\x89\xb9\xe6\xae\x8a\xe6\x96\xb0\xe6\x89\x8b\xe6\x8c\x87\xe5\xbc\x95',
                    'QuickLink': 1
                    }
   }

def GetData():
    return DataDict


def GetQTEGuide():
    return GetData()['QTEGuide']['Content']


def GetRemoteGuide():
    return GetData()['RemoteGuide']['Content']


def GetLocalHandler():
    return GetData()['LocalHandler']['Content']


def GetDeathGuide():
    return GetData()['DeathGuide']['Content']


def GetLocalGuideParams():
    return GetData()['LocalGuideParams']['Content']


def GetLocalGuide():
    return GetData()['LocalGuide']['Content']


def GetLocalGuideDamage():
    return GetData()['LocalGuideDamage']['Content']


def GetSpecialGuide():
    return GetData()['SpecialGuide']['Content']


def GetLobbyGuide():
    return GetData()['LobbyGuide']['Content']


def get_init_guide_pos(guide_id):
    return GetLocalGuide()[guide_id].get('InitData', {}).get('pos', None)


def get_init_guide_data(guide_id):
    return GetLocalGuide()[guide_id].get('InitData', None)


def get_handler_params(key):
    return GetLocalHandler()[key]['handler_params']


def get_charge_rate():
    return GetLocalGuideParams()['charge_rate']['var_val']


def get_local_damage(weapon_id, part):
    info = GetLocalGuideDamage().get(weapon_id, None)
    if info:
        if part == 0:
            return info['head_hit']
        else:
            return info['other_hit']

    return 20


def get_local_mecha_second_weapon_cd():
    return GetLocalGuideParams()['mecha_second_weapon_cd']['var_val']


def get_local_mecha_second_weapon_damage():
    return GetLocalGuideParams()['mecha_second_weapon_damage']['var_val']


def get_remote_guide_params--- This code section failed: ---

1168       0  LOAD_CONST            1  -1
           3  LOAD_CONST            2  ('battle_utils',)
           6  IMPORT_NAME           0  'logic.gcommon.common_utils'
           9  IMPORT_FROM           1  'battle_utils'
          12  STORE_FAST            1  'battle_utils'
          15  POP_TOP          

1169      16  POP_TOP          
          17  PRINT_ITEM_TO    
          18  PRINT_ITEM_TO    
          19  COMPARE_OP            2  '=='
          22  POP_JUMP_IF_FALSE    69  'to 69'
          25  LOAD_FAST             1  'battle_utils'
          28  LOAD_ATTR             2  'is_signal_logic'
          31  CALL_FUNCTION_0       0 
          34  UNARY_NOT        
        35_0  COME_FROM                '22'
          35  POP_JUMP_IF_FALSE    69  'to 69'

1170      38  LOAD_GLOBAL           3  'GetRemoteGuide'
          41  CALL_FUNCTION_0       0 
          44  LOAD_FAST             0  'handler_name'
          47  BINARY_SUBSCR    
          48  LOAD_CONST            4  'guilde_handler_params'
          51  BINARY_SUBSCR    
          52  STORE_FAST            2  'guilde_handler_params'

1171      55  LOAD_CONST            5  5515
          58  LOAD_FAST             2  'guilde_handler_params'
          61  LOAD_CONST            6  1
          64  BINARY_SUBSCR    
          65  BUILD_LIST_2          2 
          68  RETURN_END_IF    
        69_0  COME_FROM                '35'

1172      69  LOAD_GLOBAL           3  'GetRemoteGuide'
          72  CALL_FUNCTION_0       0 
          75  LOAD_FAST             0  'handler_name'
          78  BINARY_SUBSCR    
          79  LOAD_CONST            4  'guilde_handler_params'
          82  BINARY_SUBSCR    
          83  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 16


def get_death_guide_params(handler_name):
    return GetDeathGuide()[handler_name]['guilde_handler_params']


def get_special_guide_params(handler_name):
    return GetSpecialGuide()[handler_name]['guilde_handler_params']


def get_qte_local_damage(weapon_id, part):
    return get_local_damage(weapon_id, part)


def get_qte_step_init_data(step_id):
    return GetQTEGuide()[step_id].get('InitData', {})