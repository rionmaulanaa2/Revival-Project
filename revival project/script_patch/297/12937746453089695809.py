# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/newbie_stage_config.py
_reload_all = True
if G_IS_NA_PROJECT:
    from .na_newbie_stage_config import *
else:
    DataDict = {'BarrierConfig': {'Content': {201: {'barrier_height': 1.0,
                                           'barrier_left_bottom': [
                                                                 -10608, 290, 5324],
                                           'barrier_right_top': [
                                                               -8915, 898, 8530]
                                           },
                                     202: {'barrier_height': 100.0,
                                           'barrier_left_bottom': [
                                                                 -17062, 110, 15419],
                                           'barrier_right_top': [
                                                               -14886, 110, 19365]
                                           },
                                     203: {'barrier_center': [
                                                            5751, -121, -597],
                                           'barrier_scale': [
                                                           17, 20, 17]
                                           },
                                     204: {'barrier_center': [
                                                            17002, 426, -2708],
                                           'barrier_scale': [
                                                           75, 20, 75]
                                           }
                                     },
                         'Name': '\xe5\x85\xb3\xe5\x8d\xa1\xe8\xbe\xb9\xe7\x95\x8c\xe9\x85\x8d\xe7\xbd\xae',
                         'QuickLink': 1
                         },
       'BornPointConfig': {'Content': {201: {'born_point': [
                                                          -9525, 290, 8060],
                                             'human_yaw': -2.71
                                             },
                                       202: {'born_point': [
                                                          -15964, 122, 16036],
                                             'human_yaw': 0.0
                                             },
                                       203: {'born_point': [
                                                          5188, 183, -284],
                                             'human_yaw': 0.345604
                                             },
                                       204: {'born_point': [
                                                          16925, 390, -2800],
                                             'human_yaw': 1.57
                                             }
                                       },
                           'Name': '\xe5\x85\xb3\xe5\x8d\xa1\xe5\x87\xba\xe7\x94\x9f\xe7\x82\xb9\xe9\x85\x8d\xe7\xbd\xae',
                           'QuickLink': 1
                           },
       'DoorConfig': {'Content': {202: {'door_init_data': [{'npc_id': 1,'faction_id': 2,'init_max_hp': 30000,'reborn_timestamp': None,'position': [-15970.4296875, 193.68447875976562, 16208.669921875],'hp': 30000,'max_hp': 30000}, {'npc_id': 2,'faction_id': 2,'init_max_hp': 30000,'reborn_timestamp': None,'position': [-16413.068359375, 185.87742614746094, 16057.75],'hp': 30000,'max_hp': 30000}, {'npc_id': 3,'faction_id': 2,'init_max_hp': 30000,'reborn_timestamp': None,'position': [-15529.931640625, 185.87744140625, 16057.75],'hp': 30000,'max_hp': 30000}],'group_born_data': {1: [-15965.5, 132.0, 21224.5, 455.0, 1, {}],2: [-15970.0, 123.0, 16055.5, 455.0, 0, {}]}}},'Name': '\xe5\x85\xb3\xe5\x8d\xa1\xe9\x97\xa8\xe9\x85\x8d\xe7\xbd\xae',
                      'QuickLink': 1
                      },
       'StageFour': {'Content': {100: {'Interface': 'empty_guide_holder',
                                       'Next': [
                                              101]
                                       },
                                 101: {'Args': [
                                              'GuideIntroStepsUI', 'logic.comsys.guide_ui'],
                                       'Event': [
                                               'E_GUIDE_CLOSE_INTRO_STEPS', 'guide_close_intro_steps'],
                                       'Interface': 'show_intro_steps',
                                       'Next': [
                                              102],
                                       'NextShowMainUI': [
                                                        'MoveRockerUI', 'BattleInfoUI', 'BattleInfoMessageVisibleUI', 'FrontSightUI', 'WeaponBarSelectUI', 'FireRockerUI', 'BulletReloadUI', 'PostureControlUI', 'PickUI', 'DrugUI', 'SmallMapUI', 'FightLeftShotUI', 'FightReadyTipsUI'],
                                       'Prior': 100
                                       },
                                 102: {'Args': [
                                              5232, 5],
                                       'Interface': 'show_riko_tips',
                                       'Next': [
                                              103, 104]
                                       },
                                 103: {'Args': 1011,
                                       'Interface': 'pick_up_weapon'
                                       },
                                 104: {'Args': [
                                              5298, 5],
                                       'Interface': 'show_riko_tips',
                                       'Next': [
                                              200],
                                       'Prior': 101
                                       },
                                 200: {'Interface': 'empty_guide_holder',
                                       'Next': [
                                              201, 202, 203, 204, 205]
                                       },
                                 201: {'Args': [
                                              5233, 7],
                                       'Interface': 'show_riko_tips'
                                       },
                                 202: {'Args': [
                                              [
                                               17021, 390, -2800], 2, 'temp_locate', 'keep'],
                                       'Interface': 'show_locate'
                                       },
                                 203: {'Args': [
                                              [
                                               17021, 390, -2800], 'effect/fx/guide/guide_end.sfx'],
                                       'Interface': 'show_sfx'
                                       },
                                 204: {'Args': [[{'item_id': 10543,'count': 1,'position': [17022, 398, -2800],'count': 1,'position': [17021, 398, -2801]}, {'item_id': 9912,'count': 1,'position': [17021, 398, -2802]}, {'item_id': 9914,'count': 1,'position': [17023, 398, -2800]}, {'item_id': 9916,'count': 1,'position': [17022, 398, -2801]}]],'Event': [
                                               'E_GUIDE_PICKED_SPECIFIC_ITEMS', 'guide_pick_specific_items'],
                                       'Interface': 'create_items',
                                       'Next': [
                                              300],
                                       'Prior': 200
                                       },
                                 205: {'Args': [
                                              True, 5511],
                                       'Interface': 'show_side_tip_ui'
                                       },
                                 300: {'Interface': 'empty_guide_holder',
                                       'Next': [
                                              301, 302, 303, 304, 305]
                                       },
                                 301: {'Args': [
                                              5234, 5],
                                       'Interface': 'show_riko_tips'
                                       },
                                 302: {'Args': [
                                              [
                                               17002, 426, -2708], 2, 'temp_locate', 'keep'],
                                       'Interface': 'show_locate'
                                       },
                                 303: {'Args': [
                                              [
                                               17002, 426, -2708], 'effect/fx/guide/guide_end.sfx'],
                                       'Interface': 'show_sfx'
                                       },
                                 304: {'Args': [[{'item_id': 10544,'count': 1,'position': [17002, 431, -2708]}]],'Event': [
                                               'E_GUIDE_PICKED_SPECIFIC_ITEMS', 'guide_pick_specific_items'],
                                       'Interface': 'create_items',
                                       'Next': [
                                              400],
                                       'Prior': 300
                                       },
                                 305: {'Args': [
                                              True, 5512],
                                       'Interface': 'show_side_tip_ui'
                                       },
                                 400: {'Interface': 'empty_guide_holder',
                                       'Next': [
                                              401, 402, 403, 404]
                                       },
                                 401: {'Args': [
                                              [
                                               16988, 442, -2829], 2, 'temp_locate', 'keep'],
                                       'Interface': 'show_locate'
                                       },
                                 402: {'Args': [
                                              [
                                               16988, 442, -2829], 'effect/fx/guide/guide_end.sfx'],
                                       'Interface': 'show_sfx'
                                       },
                                 403: {'Args': [
                                              6002, [16989, 443, -2827], {16543: 1,10022: 1,16603: 1,16513: 1}],
                                       'Interface': 'create_pick_item',
                                       'Next': [
                                              500],
                                       'Prior': 400
                                       },
                                 404: {'Args': [
                                              5235, 6],
                                       'Interface': 'show_riko_tips'
                                       },
                                 500: {'Args': [
                                              [
                                               17474, 378, -2661]],
                                       'Interface': 'change_player_head',
                                       'Next': [
                                              501, 502, 503, 504, 505]
                                       },
                                 501: {'Args': [
                                              5236, 5],
                                       'Interface': 'show_riko_tips'
                                       },
                                 502: {'Args': [
                                              [
                                               17474, 378, -2661], 2, 'temp_locate', 'keep'],
                                       'Interface': 'show_locate'
                                       },
                                 503: {'Args': [
                                              [
                                               17474, 378, -2661], 'effect/fx/guide/guide_end.sfx'],
                                       'Interface': 'show_sfx'
                                       },
                                 504: {'Args': [
                                              [
                                               17474, 378, -2661], 3],
                                       'Interface': 'check_move_pos',
                                       'Next': [
                                              600],
                                       'Prior': 500
                                       },
                                 505: {'Args': [
                                              True, 5502],
                                       'Interface': 'show_side_tip_ui'
                                       },
                                 600: {'Interface': 'empty_guide_holder',
                                       'Next': [
                                              601, 602, 603, 604, 605],
                                       'NextShowMainUI': [
                                                        'HpInfoUI', 'BattleSignalInfoUI', 'BattleFightCapacity']
                                       },
                                 601: {'Args': [
                                              5237, 6, 0, 0, 5621],
                                       'Event': [
                                               'E_AIM_TARGET', 'guide_shoot_show'],
                                       'Interface': 'show_riko_tips'
                                       },
                                 602: {'Args': [
                                              [
                                               17628, 378, -2663], 'effect/fx/guide/guide_end.sfx'],
                                       'Interface': 'show_sfx'
                                       },
                                 603: {'Args': [
                                              [
                                               17628, 378, -2663], 2, 'temp_locate', 'keep'],
                                       'Interface': 'show_locate'
                                       },
                                 604: {'Args': [
                                              0, [17628, 378, -2663], 200],
                                       'Event': [
                                               'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                       'Interface': 'create_robot',
                                       'Next': [
                                              700],
                                       'NextShowMainUI': [
                                                        'PickUI', 'DrugUI'],
                                       'Prior': 600
                                       },
                                 605: {'Args': [
                                              True, 5503],
                                       'Interface': 'show_side_tip_ui'
                                       },
                                 700: {'Interface': 'empty_guide_holder',
                                       'Next': [
                                              701, 702, 703, 704, 705, 706, 707, 708, 709]
                                       },
                                 701: {'Args': [
                                              99],
                                       'Interface': 'update_alive_num'
                                       },
                                 702: {'Args': [
                                              2, 2, 10, 2, [18677, -2680, 2250.0], [20197, -2555, 1560.0], 1],
                                       'Interface': 'refresh_poison_circle'
                                       },
                                 703: {'Args': [
                                              [
                                               17628, 378, -2663], 'effect/fx/guide/guide_end.sfx'],
                                       'Interface': 'show_sfx'
                                       },
                                 704: {'Args': [
                                              [
                                               17628, 379, -2663], 2, 'temp_locate', 'keep'],
                                       'Interface': 'show_locate'
                                       },
                                 705: {'Args': [
                                              5238, 5],
                                       'Interface': 'show_riko_tips'
                                       },
                                 706: {'Args': [
                                              6000, [17629, 383, -2664], {10233: 1}],
                                       'Event': [
                                               'E_GUIDE_PICK_END', 'finish_guide'],
                                       'Interface': 'create_pick_item',
                                       'Next': [
                                              900],
                                       'Prior': 700
                                       },
                                 707: {'Args': [
                                              'nd_step_5', 'show_5'],
                                       'Interface': 'show_pick_animation'
                                       },
                                 708: {'Args': [
                                              [
                                               17629, 378, -2664], 2],
                                       'Interface': 'check_move_pos'
                                       },
                                 709: {'Args': [
                                              True, 5513],
                                       'Interface': 'show_side_tip_ui'
                                       },
                                 900: {'Interface': 'empty_guide_holder',
                                       'Next': [
                                              901, 902, 903, 904, 905, 906, 907, 908]
                                       },
                                 901: {'Args': [
                                              2, 3, 10, 1],
                                       'Interface': 'reduce_poison_circle'
                                       },
                                 902: {'Args': [
                                              16],
                                       'Interface': 'update_alive_num'
                                       },
                                 903: {'Args': [
                                              [
                                               5731, 5241, 5242], 7],
                                       'Interface': 'show_multi_human_tips'
                                       },
                                 904: {'Args': [
                                              [
                                               18799, 378, -2683], 5, 'temp_locate', 'keep'],
                                       'Interface': 'show_locate'
                                       },
                                 905: {'Args': [
                                              [
                                               18799, 378, -2683], 'effect/fx/guide/guide_end.sfx'],
                                       'Interface': 'show_sfx'
                                       },
                                 906: {'Args': [
                                              10, 1, [20197, 382, -2555], 120],
                                       'Interface': 'tick_avatar_signal'
                                       },
                                 907: {'Args': [
                                              [
                                               18799, 378, -2683], 5],
                                       'Interface': 'check_move_pos',
                                       'Next': [
                                              1000],
                                       'Prior': 900
                                       },
                                 908: {'Args': [
                                              True, 5514],
                                       'Interface': 'show_side_tip_ui'
                                       },
                                 1000: {'Args': [
                                               3],
                                        'Interface': 'lock_move',
                                        'Next': [
                                               1001, 1002]
                                        },
                                 1001: {'Args': [
                                               'nd_signal_tips', 'show_signal_tips'],
                                        'Interface': 'show_nd_animation'
                                        },
                                 1002: {'Args': [
                                               5243, 5],
                                        'Interface': 'show_riko_tips',
                                        'Next': [
                                               1100],
                                        'Prior': 1000
                                        },
                                 1100: {'Args': [
                                               5302, 5],
                                        'Interface': 'show_riko_tips',
                                        'Next': [
                                               1101, 1102, 1103, 1104, 1105, 1106, 1107]
                                        },
                                 1101: {'Args': [
                                               'nd_hpmp_tips', 'show_hpmp_tips'],
                                        'Interface': 'show_nd_animation'
                                        },
                                 1102: {'Args': [
                                               5303, 5],
                                        'Interface': 'show_riko_tips'
                                        },
                                 1103: {'Args': [
                                               0.2],
                                        'Interface': 'reduce_avatar_signal'
                                        },
                                 1104: {'Args': [[{'item_id': 1612,'count': 1}]],'Interface': 'get_other_items'
                                        },
                                 1105: {'Args': [
                                               'temp_use_tips', 'show_3'],
                                        'Interface': 'show_nd_animation'
                                        },
                                 1106: {'Args': [
                                               5205, 100],
                                        'Event': [
                                                'E_GUIDE_FULL_SIGNAL', 'guide_signal_full_recover'],
                                        'Interface': 'show_use_drug_tip',
                                        'Next': [
                                               1200],
                                        'Prior': 1100
                                        },
                                 1107: {'Args': [
                                               True, 5515],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                 1200: {'Interface': 'empty_guide_holder',
                                        'Next': [
                                               1201, 1202, 1203, 1204],
                                        'NextShowMainUI': [
                                                         'MechaUI', 'MechaControlMain', 'MechaHpInfoUI']
                                        },
                                 1201: {'Args': [
                                               5244, 5],
                                        'Interface': 'show_riko_tips'
                                        },
                                 1202: {'Args': [
                                               'nd_step_13', 'show_13'],
                                        'Event': [
                                                'E_GUIDE_MECHA_UI_SHOW', 'guide_mecha_ui_show'],
                                        'Interface': 'show_nd_animation'
                                        },
                                 1203: {'Event': [
                                                'E_ON_JOIN_MECHA', 'guide_call_mecha_end'],
                                        'Interface': 'mecha_progress',
                                        'Next': [
                                               1300],
                                        'Prior': 1200
                                        },
                                 1204: {'Args': [
                                               True, 5510],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                 1300: {'Args': [
                                               5245, 7],
                                        'Interface': 'show_riko_tips',
                                        'Next': [
                                               1301, 1302, 1303, 1304, 1305, 1306]
                                        },
                                 1301: {'Interface': 'enter_ace_stage'
                                        },
                                 1302: {'Args': [
                                               [
                                                18837, 378, -2742], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate'
                                        },
                                 1303: {'Args': [
                                               [
                                                18837, 378, -2742], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_sfx'
                                        },
                                 1304: {'Args': [
                                               0, {'mecha_type': 8001,'hp': 1500,'pos': [18837, 378, -2742],'shoot': 1,'shoot_delay': 6,'shoot_interval': 5}],
                                        'Interface': 'create_robot_mecha_by_type'
                                        },
                                 1305: {'Event': [
                                                'E_GUIDE_PLAYER_DAMAGE', 'guide_on_player_damage'],
                                        'Interface': 'destroy_mecha'
                                        },
                                 1306: {'Event': [
                                                'E_ON_HUMAN_COM_RECOVERED', 'on_recovered_human_com'],
                                        'Interface': 'after_mecha_die',
                                        'Next': [
                                               1400],
                                        'Prior': 1300
                                        },
                                 1400: {'Interface': 'empty_guide_holder',
                                        'Next': [
                                               1401, 1402],
                                        'NextShowMainUI': [
                                                         'MoveRockerUI', 'BattleInfoUI', 'WeaponBarSelectUI', 'FireRockerUI', 'BulletReloadUI', 'PostureControlUI', 'HpInfoUI', 'SmallMapUI', 'BattleSignalInfoUI']
                                        },
                                 1401: {'Args': [
                                               5730, 7],
                                        'Interface': 'show_mecha_call_disable_tips'
                                        },
                                 1402: {'Args': [
                                               5246, 7],
                                        'Interface': 'show_riko_tips',
                                        'Next': [
                                               1500],
                                        'Prior': 1400
                                        },
                                 1500: {'Interface': 'empty_guide_holder',
                                        'Next': [
                                               1501, 1502, 1503, 1504, 1505, 1506, 1507]
                                        },
                                 1501: {'Args': [
                                               4],
                                        'Interface': 'update_alive_num'
                                        },
                                 1502: {'Args': [
                                               3],
                                        'Interface': 'statistic_kill_robot',
                                        'Next': [
                                               1600],
                                        'Prior': 1500
                                        },
                                 1503: {'Args': [
                                               0, [19044, 383, -2601], 200, 1, '13', 1, 1],
                                        'Event': [
                                                'E_AIM_TARGET', 'guide_shoot_show'],
                                        'Interface': 'create_robot'
                                        },
                                 1504: {'Args': [
                                               0, [18962, 378, -2563], 200, 0, '11', 1, 1],
                                        'Interface': 'create_robot'
                                        },
                                 1505: {'Args': [
                                               5247, 5],
                                        'Interface': 'show_riko_tips'
                                        },
                                 1506: {'Event': [
                                                'E_GUIDE_TOP_FIVE_WIDGET_DESTROY', 'on_top_five_widget_destroy'],
                                        'Interface': 'delay_show_tip_ui'
                                        },
                                 1507: {'Args': [
                                               True, 5517],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                 1600: {'Interface': 'empty_guide_holder',
                                        'Next': [
                                               1601],
                                        'Prior': 1507
                                        },
                                 1601: {'Args': [
                                               5249, 5],
                                        'Interface': 'show_riko_tips',
                                        'Next': [
                                               1603, 1604],
                                        'Prior': 1600
                                        },
                                 1603: {'Args': [],'Interface': 'clear_poison_circle'
                                        },
                                 1604: {'Args': 1604,
                                        'Interface': 'create_end_ui',
                                        'Prior': 1601
                                        }
                                 },
                     'Name': '\xe6\x96\xb0\xe6\x89\x8b\xe5\x85\xb3\xe5\x8d\xa1-4',
                     'QuickLink': 1
                     },
       'StageHuman': {'Content': {100: {'Interface': 'empty_guide_holder',
                                        'Next': [
                                               101, 102, 103]
                                        },
                                  101: {'Args': [
                                               5170, 5170, 4],
                                        'Interface': 'show_human_tips',
                                        'Next': [
                                               200],
                                        'NextShowMainUI': [
                                                         'MoveRockerUI'],
                                        'PCNextShowMainUI': [
                                                           'SceneInteractionUI']
                                        },
                                  102: {'Args': 10012,
                                        'Interface': 'pick_up_weapon'
                                        },
                                  103: {'Interface': 'do_nothing_guide',
                                        'PCArgs': [
                                                 [
                                                  'summon_call_mecha', 'switch_battle_bag'], True],
                                        'PCInterface': 'block_pc_hot_key'
                                        },
                                  200: {'Args': [
                                               5171, 920830, 0],
                                        'Interface': 'show_human_tips',
                                        'Next': [
                                               201, 202, 203, 204, 205, 206, 207],
                                        'Prior': 101
                                        },
                                  201: {'Args': [
                                               5171, 920830, 4],
                                        'Interface': 'show_human_tips'
                                        },
                                  202: {'Args': [
                                               'nd_step_2', 'show_2'],
                                        'Interface': 'show_nd_animation'
                                        },
                                  203: {'Args': [
                                               'temp_move_tips'],
                                        'Interface': 'show_drag_layer',
                                        'PCInterface': 'do_nothing_guide'
                                        },
                                  204: {'Args': [
                                               [
                                                -9576.001953, 290.220032, 7763.281738], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_sfx'
                                        },
                                  205: {'Args': [
                                               [
                                                -9576.001953, 290.220032, 7763.281738], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate'
                                        },
                                  206: {'Args': [
                                               [
                                                -9576.001953, 290.220032, 7763.281738], 1],
                                        'Interface': 'check_move_pos',
                                        'Next': [
                                               300],
                                        'NextShowMainUI': [
                                                         'FrontSightUI', 'WeaponBarSelectUI', 'FireRockerUI', 'BulletReloadUI', 'PostureControlUI'],
                                        'PCNextShowMainUI': [
                                                           'WeaponBarSelectUI'],
                                        'Prior': 200
                                        },
                                  207: {'Args': [
                                               True, 5526],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  300: {'Args': [
                                               5172, 920832, 0],
                                        'Event': [
                                                'E_AIM_TARGET', 'guide_shoot_show'],
                                        'Interface': 'show_human_tips',
                                        'Next': [
                                               301, 302, 303, 304, 305, 306],
                                        'Prior': 206
                                        },
                                  301: {'Args': [
                                               5172, 920832, 6],
                                        'Event': [
                                                'E_AIM_TARGET', 'guide_shoot_show'],
                                        'Interface': 'show_human_tips'
                                        },
                                  302: {'Args': [
                                               'nd_step_3', 'show_3'],
                                        'Interface': 'show_nd_animation',
                                        'InterfaceType': 2
                                        },
                                  303: {'Args': [
                                               [
                                                -9630.237305, 290.220032, 7452.56543], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_sfx'
                                        },
                                  304: {'Args': [
                                               [
                                                -9630.237305, 290.220032, 7452.56543], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate'
                                        },
                                  305: {'Args': [
                                               0, [-9630.237305, 290.220032, 7452.56543], 200],
                                        'Event': [
                                                'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                        'Interface': 'create_robot',
                                        'Next': [
                                               400],
                                        'NextShowMainUI': [
                                                         'PickUI', 'DrugUI'],
                                        'PCNextShowMainUI': [
                                                           'PickUI', 'DrugUI'],
                                        'Prior': 300
                                        },
                                  306: {'Args': [
                                               True, 5527],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  400: {'Args': [
                                               5173, 5173, 0],
                                        'Interface': 'show_human_tips',
                                        'Next': [
                                               401, 402, 403, 404, 405, 406],
                                        'Prior': 305
                                        },
                                  401: {'Args': [
                                               5173, 5173, 6],
                                        'Interface': 'show_human_tips'
                                        },
                                  402: {'Args': [
                                               [
                                                -9676.547852, 292.220032, 7379.949219], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_sfx'
                                        },
                                  403: {'Args': [
                                               [
                                                -9676.547852, 292.220032, 7379.949219], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate'
                                        },
                                  404: {'Args': [[{'item_id': 10232,'count': 1,'position': [-9676.547852, 295.220032, 7379.9492199]}]],'Event': [
                                                'E_GUIDE_PICKED_SPECIFIC_ITEMS', 'guide_pick_specific_items'],
                                        'Interface': 'create_items',
                                        'Next': [
                                               501, 502],
                                        'Prior': 400
                                        },
                                  405: {'Args': [
                                               True, 5528],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  406: {'Interface': 'do_nothing_guide',
                                        'PCArgs': [
                                                 920850, 5, 'pick_thing'],
                                        'PCInterface': 'show_temp_tips_pc'
                                        },
                                  501: {'Args': [
                                               'nd_weapon_1', 'weapon_1'],
                                        'Event': [
                                                'E_TRY_SWITCH', 'guide_switch_end_by_guide_id'],
                                        'Interface': 'show_nd_animation',
                                        'Next': [
                                               601],
                                        'NextShowMainUI': [
                                                         'FightLeftShotUI', 'HpInfoUI', 'FightReadyTipsUI'],
                                        'PCArgs': [
                                                 'nd_step_6_1', 'show_6_1'],
                                        'PCNextShowMainUI': [
                                                           'HpInfoUI', 'FightReadyTipsUI'],
                                        'Prior': 404
                                        },
                                  502: {'Args': [
                                               True, 5529],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  601: {'Args': [
                                               5174, 920834, 0],
                                        'Interface': 'show_human_tips',
                                        'Next': [
                                               602, 603, 604, 605, 606, 607, 608, 609, 610, 611],
                                        'Prior': 501
                                        },
                                  602: {'Args': [
                                               5174, 920834, 6],
                                        'Interface': 'show_human_tips'
                                        },
                                  603: {'Event': [
                                                'E_SUCCESS_AIM', 'guide_try_aim_success']
                                        },
                                  604: {'Args': [
                                               'nd_step_7', 'show_7'],
                                        'Interface': 'show_nd_animation',
                                        'PCInterface': 'do_nothing_guide'
                                        },
                                  605: {'Args': [
                                               'temp_move_tips'],
                                        'Interface': 'show_drag_layer',
                                        'InterfaceType': 2,
                                        'PCInterface': 'do_nothing_guide'
                                        },
                                  606: {'Args': [
                                               'nd_step_8', 'show_8'],
                                        'Interface': 'show_nd_animation',
                                        'InterfaceType': 2,
                                        'PCInterface': 'do_nothing_guide'
                                        },
                                  607: {'Args': [
                                               0, [-9907.066406, 283.126251, 7200.416992], 200],
                                        'Event': [
                                                'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                        'Interface': 'create_robot_aim',
                                        'Next': [
                                               700],
                                        'Prior': 601
                                        },
                                  608: {'Event': [
                                                'E_QUIT_AIM', 'guide_quit_aim_success']
                                        },
                                  609: {'Args': [
                                               [
                                                -9907.066406, 283.126251, 7200.416992], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_sfx'
                                        },
                                  610: {'Args': [
                                               [
                                                -9907.066406, 283.126251, 7200.416992], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate'
                                        },
                                  611: {'Args': [
                                               True, 5527],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  700: {'Args': [
                                               5175, 5175, 0],
                                        'Interface': 'show_human_tips',
                                        'Next': [
                                               701, 702, 703, 704],
                                        'Prior': 607
                                        },
                                  701: {'Args': [
                                               5205, 100],
                                        'Event': [
                                                'E_GUIDE_USE_END', 'guide_use_end'],
                                        'Interface': 'show_use_drug_tip',
                                        'Next': [
                                               800],
                                        'PCArgs': [
                                                 920851, 100, 'use_cur_item'],
                                        'Prior': 700
                                        },
                                  702: {'Args': [
                                               5175, 5175, 6],
                                        'Interface': 'show_human_tips'
                                        },
                                  703: {'Args': [[{'item_id': 1612,'count': 1}]],'Interface': 'get_other_items'
                                        },
                                  704: {'Args': [
                                               True, 5531],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  800: {'Args': [
                                               5176, 5176, 0],
                                        'Interface': 'show_human_tips',
                                        'Next': [
                                               801, 804, 805, 806, 807, 808, 809, 810, 811],
                                        'Prior': 701
                                        },
                                  801: {'Args': [
                                               5176, 5176, 6],
                                        'Interface': 'show_human_tips'
                                        },
                                  802: {'Args': 10523,
                                        'Interface': 'pick_up_weapon'
                                        },
                                  803: {'Args': [
                                               'nd_weapon_2', 'weapon_2'],
                                        'Event': [
                                                'E_TRY_SWITCH', 'guide_switch_end_by_guide_id'],
                                        'Interface': 'show_nd_animation',
                                        'PCArgs': [
                                                 'nd_step_6_2', 'show_6_2']
                                        },
                                  804: {'Args': [
                                               False],
                                        'Interface': 'enable_human_fire'
                                        },
                                  805: {'Args': [
                                               0, {'mecha_type': 8001,'hp': 2021,'pos': [-9922.699219, 284.945923, 7021.270996]}],
                                        'Event': [
                                                'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                        'Interface': 'create_robot_mecha_by_type',
                                        'Next': [
                                               900],
                                        'Prior': 800
                                        },
                                  806: {'Args': [
                                               [
                                                -9922.699219, 284.945923, 7021.270996], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate'
                                        },
                                  807: {'Args': [
                                               [
                                                -9922.699219, 284.945923, 7021.270996], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_sfx'
                                        },
                                  808: {'Args': [
                                               True, 5532],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  809: {'Event': [
                                                'E_GUIDE_ROBOT_MECHA_HP_LOWER', 'on_guide_robot_mecha_lower_hp']
                                        },
                                  810: {'Event': [
                                                'E_TRY_SWITCH', 'on_guide_try_switch']
                                        },
                                  811: {'Args': [
                                               'nd_weapon_2', 'weapon_2'],
                                        'Interface': 'hide_switch_gun_tip',
                                        'PCArgs': [
                                                 'nd_step_6_2', 'show_6_2']
                                        },
                                  900: {'Args': [
                                               5177, 5177, 0],
                                        'Interface': 'show_human_tips',
                                        'Next': [
                                               901, 902, 903, 904, 905, 906, 907, 908, 909],
                                        'Prior': 805
                                        },
                                  901: {'Args': [
                                               5178, 5178, 5],
                                        'Interface': 'show_human_tips'
                                        },
                                  902: {'Args': [
                                               [
                                                -9922.699219, 284.945923, 7021.270996], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_sfx'
                                        },
                                  903: {'Args': [
                                               [
                                                -9922.699219, 284.945923, 7021.270996], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate'
                                        },
                                  904: {'Args': [
                                               5206, 5206, 5],
                                        'Interface': 'show_temp_tips'
                                        },
                                  905: {'Args': [
                                               False],
                                        'Interface': 'enable_human_fire'
                                        },
                                  906: {'Args': [[{'item_id': 10534,'count': 1,'position': [-9927.699219, 287.945923, 7021.270996]}]],'Event': [
                                                'E_GUIDE_PICK_WEAPON', 'guide_pick_weapon'],
                                        'Interface': 'create_items',
                                        'Next': [
                                               1001, 1002],
                                        'Prior': 900
                                        },
                                  907: {'Args': [
                                               False],
                                        'Interface': 'process_auto_pick'
                                        },
                                  908: {'Args': [
                                               True, 5533],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  909: {'Interface': 'do_nothing_guide',
                                        'PCArgs': [
                                                 920833, 5],
                                        'PCInterface': 'show_temp_tips_pc'
                                        },
                                  1001: {'Args': [
                                                'nd_weapon_3', 'weapon_3'],
                                         'Event': [
                                                 'E_TRY_SWITCH', 'guide_switch_end_by_guide_id'],
                                         'Interface': 'show_nd_animation',
                                         'Next': [
                                                1100],
                                         'PCArgs': [
                                                  'nd_step_6_3', 'show_6_3'],
                                         'Prior': 906
                                         },
                                  1002: {'Args': [
                                                True, 5529],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  1100: {'Args': [
                                                5292, 5292, 0],
                                         'Interface': 'show_human_tips',
                                         'Next': [
                                                1101, 1102, 1103, 1104, 1105],
                                         'Prior': 1001
                                         },
                                  1101: {'Args': [
                                                [
                                                 -9942.338867, 285.262695, 6552.431641], 'effect/fx/guide/guide_end.sfx'],
                                         'Interface': 'show_sfx'
                                         },
                                  1102: {'Args': [
                                                [
                                                 -9942.338867, 285.262695, 6552.431641], 2, 'temp_locate', 'keep'],
                                         'Interface': 'show_locate'
                                         },
                                  1103: {'Args': [
                                                0, {'mecha_type': 8001,'hp': 1800,'pos': [-9942.338867, 285.262695, 6552.431641]}],
                                         'Event': [
                                                 'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                         'Interface': 'create_robot_mecha_by_type',
                                         'InterfaceType': 1,
                                         'Next': [
                                                1201],
                                         'Prior': 1100
                                         },
                                  1104: {'Args': [
                                                5292, 5292, 6],
                                         'Interface': 'show_human_tips'
                                         },
                                  1105: {'Args': [
                                                True, 5532],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  1201: {'Args': [
                                                5179, 5179, 5],
                                         'Interface': 'show_human_tips',
                                         'Next': 1301,
                                         'Prior': 1103
                                         },
                                  1301: {'Args': 1301,
                                         'Interface': 'create_end_ui',
                                         'Prior': 1201
                                         }
                                  },
                      'Name': '\xe6\x96\xb0\xe6\x89\x8b\xe5\x85\xb3\xe5\x8d\xa1-1',
                      'QuickLink': 1
                      },
       'StageHumanHandler': {'Content': {'robot_mecha_lower_hp': {'handler_params': 1800
                                                                  },
                                         'robot_mecha_lower_hp_tip_param': {'handler_params': {'pc': ['nd_step_6_2', 'show_6_2'],'mobile': ['nd_weapon_2', 'weapon_2']}},'robot_mecha_lower_hp_weapon_id': {'handler_params': 10523
                                                                            }
                                         },
                             'Name': '\xe7\xac\xac\xe4\xb8\x80\xe5\x85\xb3\xe5\xbc\x95\xe5\xaf\xbc\xe5\x8f\x82\xe6\x95\xb0\xe9\x85\x8d\xe7\xbd\xae',
                             'QuickLink': 1
                             },
       'StageMecha': {'Content': {100: {'Interface': 'empty_guide_holder',
                                        'Next': [
                                               102, 103, 107, 201, 202, 204, 205],
                                        'NextShowMainUI': [
                                                         'MoveRockerUI', 'PickUI', 'WeaponBarSelectUI', 'DrugUI', 'FireRockerUI', 'FightLeftShotUI', 'HpInfoUI', 'FightReadyTipsUI', 'FrontSightUI', 'BulletReloadUI', 'PostureControlUI', 'MechaUI'],
                                        'PCNextShowMainUI': [
                                                           'PickUI', 'WeaponBarSelectUI', 'DrugUI', 'HpInfoUI', 'FightReadyTipsUI', 'SceneInteractionUI', 'MechaUI']
                                        },
                                  101: {'Args': [
                                               [
                                                5180, 5181], 5],
                                        'Interface': 'show_multi_human_tips'
                                        },
                                  102: {'Interface': 'create_death_door_col'
                                        },
                                  103: {'Args': [{10: 10033,1: 10013,2: 10023,3: 10523}],'Interface': 'pick_up_weapons'
                                        },
                                  104: {'Args': {'ui_name': 'DeathWeaponChooseBtn','ui_path': 'logic.comsys.battle.Death'},'Event': [
                                                'E_GUIDE_CLOSE_WEAPON_CHOOSE', 'guide_close_weapon_choose'],
                                        'Interface': 'create_common_ui'
                                        },
                                  105: {'Args': [
                                               'nd_weapon_entry', ''],
                                        'Interface': 'show_nd_animation',
                                        'PCArgs': [
                                                 920852, 'tdm_open_weapon'],
                                        'PCInterface': 'show_select_weapon_tip_pc'
                                        },
                                  106: {'Args': [
                                               True, 5535],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  107: {'Interface': 'do_nothing_guide',
                                        'PCArgs': [
                                                 [
                                                  'switch_battle_bag'], True],
                                        'PCInterface': 'block_pc_hot_key'
                                        },
                                  201: {'Args': [
                                               [
                                                5180, 5182], 5],
                                        'Interface': 'show_multi_human_tips'
                                        },
                                  202: {'Args': [
                                               'nd_step_13', 'show_13'],
                                        'Event': [
                                                'E_GUIDE_MECHA_UI_SHOW', 'guide_mecha_ui_show'],
                                        'Interface': 'show_nd_animation',
                                        'PCArgs': [
                                                 920839, 'summon_call_mecha'],
                                        'PCInterface': 'show_summon_mecha_tip_pc'
                                        },
                                  203: {'Interface': 'trigger_death_door'
                                        },
                                  204: {'Event': [
                                                'E_ON_JOIN_MECHA', 'guide_call_mecha_end'],
                                        'Interface': 'mecha_progress',
                                        'Next': [
                                               203, 301, 302, 303, 304, 305, 306, 307, 308, 309],
                                        'NextShowMainUI': [
                                                         'MechaControlMain', 'MechaHpInfoUI'],
                                        'PCNextShowMainUI': [
                                                           'MechaControlMain', 'MechaHpInfoUI'],
                                        'Prior': 100
                                        },
                                  205: {'Args': [
                                               True, 5536],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  301: {'Args': [
                                               [
                                                5183, 5184], 5],
                                        'Interface': 'show_multi_human_tips'
                                        },
                                  302: {'Args': [
                                               [
                                                -16166.185547, 112.5, 16711.101562], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_sfx'
                                        },
                                  303: {'Args': [
                                               [
                                                -16166.185547, 112.5, 16711.101562], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate'
                                        },
                                  304: {'Args': [
                                               'nd_move_skill', 'move_skill'],
                                        'Interface': 'show_nd_animation',
                                        'PCArgs': [
                                                 920854, 'mecha_rush'],
                                        'PCInterface': 'show_move_skill_tip_pc'
                                        },
                                  305: {'Args': [
                                               [
                                                -16166.185547, 112.5, 16711.101562], 2],
                                        'Interface': 'check_move_pos',
                                        'Next': [
                                               401, 402, 403, 404, 405, 406],
                                        'Prior': 204
                                        },
                                  306: {'Args': [
                                               False, False],
                                        'Interface': 'set_state_change_ui_visible_flag'
                                        },
                                  307: {'Args': [
                                               True, 5526],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  308: {'Interface': 'do_nothing_guide',
                                        'PCArgs': [
                                                 [
                                                  'summon_call_mecha'], True],
                                        'PCInterface': 'block_pc_hot_key'
                                        },
                                  309: {'Event': [
                                                'E_GUIDE_JOIN_MECHA_END_2', 'register_mecha_dash_event']
                                        },
                                  401: {'Args': [
                                               5185, 920841, 5],
                                        'Interface': 'show_human_tips'
                                        },
                                  402: {'Args': [
                                               'nd_step_16', 'show_16'],
                                        'Interface': 'show_nd_animation',
                                        'PCArgs': [
                                                 920842, 5, 'mecha_sub'],
                                        'PCInterface': 'show_temp_tips_pc'
                                        },
                                  403: {'Args': [
                                               0, {'mecha_type': 8001,'hp': 1000,'pos': [-16039, 113.556381, 17188],'shoot': True}],
                                        'Event': [
                                                'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                        'Interface': 'create_robot_mecha_by_type',
                                        'Next': [
                                               501, 502, 503, 504, 505, 506, 507, 602, 604],
                                        'Prior': 305
                                        },
                                  404: {'Args': [
                                               [
                                                -16039, 113.556381, 17188], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_sfx'
                                        },
                                  405: {'Args': [
                                               [
                                                -16039, 113.556381, 17188], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate'
                                        },
                                  406: {'Args': [
                                               True, 5537],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  501: {'Args': [
                                               5187, 920843, 5],
                                        'Interface': 'show_human_tips'
                                        },
                                  502: {'Args': [
                                               'nd_step_17', 'show_17'],
                                        'Interface': 'show_nd_animation',
                                        'PCArgs': [
                                                 'nd_step_secondary', 'show_secondary']
                                        },
                                  503: {'Args': [
                                               0, {'mecha_type': 8005,'hp': 1000,'pos': [-15898, 113.556381, 17078],'shoot': False}],
                                        'Event': [
                                                'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                        'Interface': 'create_robot_mecha_by_type',
                                        'Next': [
                                               701, 702, 703, 704, 705, 706, 707, 708, 709, 710],
                                        'NextShowMainUI': [
                                                         'StateChangeUI'],
                                        'PCNextShowMainUI': [
                                                           'StateChangeUI'],
                                        'Prior': 403
                                        },
                                  504: {'Args': [
                                               [
                                                -15898, 113.556381, 17078], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_sfx'
                                        },
                                  505: {'Args': [
                                               [
                                                -15898, 113.556381, 17078], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate'
                                        },
                                  506: {'Args': 1,
                                        'Interface': 'set_death_top_score'
                                        },
                                  507: {'Args': [
                                               True, 5538],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  601: {'Args': [
                                               5186, 5186, 0],
                                        'Interface': 'show_human_tips'
                                        },
                                  602: {'Args': {'ui_name': 'DeathTopScoreUI','ui_path': 'logic.comsys.battle.Death'},'Interface': 'create_common_ui'
                                        },
                                  603: {'Args': [
                                               5057, 3],
                                        'Interface': 'show_death_rule_tips'
                                        },
                                  604: {'Args': 2,
                                        'Interface': 'set_death_top_score'
                                        },
                                  701: {'Args': [
                                               [
                                                5188, 5189], 5],
                                        'Interface': 'show_multi_human_tips',
                                        'PCArgs': [
                                                 [
                                                  920845, 920855], 5, [None, 'summon_call_mecha']],
                                        'PCInterface': 'show_multi_human_tips_pc'
                                        },
                                  702: {'Args': [
                                               'nd_getoff_mech', 'getoff_mech'],
                                        'Interface': 'show_nd_animation',
                                        'PCArgs': [
                                                 920856, 'summon_call_mecha'],
                                        'PCInterface': 'show_get_off_mecha_tip_pc'
                                        },
                                  703: {'Args': [
                                               0, [-15741.381836, 113.076385, 16987.486328], [[-15708.255859, 113.076385, 16992.101562], [-15702.776367, 117.101006, 17024.4375], [-15746.143555, 117.101006, 17023.753906]], 200],
                                        'Event': [
                                                'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                        'Interface': 'create_robot_move',
                                        'Next': [
                                               801, 802, 803, 804, 805],
                                        'Prior': 503
                                        },
                                  704: {'Args': [
                                               True, False],
                                        'Interface': 'set_state_change_ui_visible'
                                        },
                                  705: {'Args': [
                                               True],
                                        'Interface': 'set_no_mecha_damage'
                                        },
                                  706: {'Args': [
                                               [
                                                -15741.795898, 117.101006, 17023.792969], 3],
                                        'Interface': 'delay_show_locate_and_sfx'
                                        },
                                  707: {'Event': [
                                                'E_ON_LEAVE_MECHA_START', 'guide_leave_mecha_end']
                                        },
                                  708: {'Args': [
                                               True, False],
                                        'Interface': 'set_state_change_ui_visible_flag'
                                        },
                                  709: {'Args': [
                                               True, 5539],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  710: {'Interface': 'do_nothing_guide',
                                        'PCArgs': [
                                                 [
                                                  'summon_call_mecha'], False],
                                        'PCInterface': 'block_pc_hot_key'
                                        },
                                  801: {'Args': [
                                               5190, 5190, 5],
                                        'Interface': 'show_human_tips'
                                        },
                                  802: {'Args': [
                                               'nd_step_13', 'show_13'],
                                        'Event': [
                                                'E_ON_JOIN_MECHA_START', 'guide_call_mecha_end'],
                                        'Interface': 'show_nd_animation',
                                        'Next': [
                                               901, 902, 903],
                                        'NextShowMainUI': [
                                                         'FightStateUI'],
                                        'PCArgs': [
                                                 920853, 'summon_call_mecha'],
                                        'PCInterface': 'show_summon_mecha_tip_pc',
                                        'PCNextShowMainUI': [
                                                           'FightStateUI'],
                                        'Prior': 703
                                        },
                                  803: {'Args': [
                                               False, True],
                                        'Interface': 'set_state_change_ui_visible'
                                        },
                                  804: {'Args': 3,
                                        'Interface': 'set_death_top_score'
                                        },
                                  805: {'Args': [
                                               True, 5540],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  901: {'Args': [
                                               5191, 5191, 3],
                                        'Interface': 'show_human_tips',
                                        'Next': [
                                               1101, 1102, 1103, 1104, 1105, 1106, 1107, 1002],
                                        'Prior': 802
                                        },
                                  902: {'Args': 99112,
                                        'Interface': 'send_firefox_core_module'
                                        },
                                  903: {'Args': [
                                               False],
                                        'Interface': 'set_no_mecha_damage'
                                        },
                                  1001: {'Args': [
                                                5192, 5192, 0],
                                         'Interface': 'show_human_tips',
                                         'NextShowMainUI': [
                                                          'FightStateUI'],
                                         'PCNextShowMainUI': [
                                                            'FightStateUI']
                                         },
                                  1002: {'Args': 99112,
                                         'Interface': 'active_firefox_core_module'
                                         },
                                  1101: {'Args': [
                                                5193, 5193, 5],
                                         'Interface': 'show_human_tips'
                                         },
                                  1102: {'Args': [
                                                'nd_step_17', 'show_17'],
                                         'Interface': 'show_nd_animation',
                                         'PCArgs': [
                                                  'nd_step_secondary', 'show_secondary']
                                         },
                                  1103: {'Args': [
                                                0, {'mecha_type': 8005,'hp': 1800,'pos': [-16017, 112.556396, 17041],'need_agent': True}],
                                         'Event': [
                                                 'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                         'Interface': 'create_robot_mecha_by_type',
                                         'Next': [
                                                1201, 1202, 1203, 1205, 1206],
                                         'Prior': 901
                                         },
                                  1104: {'Args': [
                                                [
                                                 -16017, 112.556396, 17041], 'effect/fx/guide/guide_end.sfx'],
                                         'Interface': 'show_sfx'
                                         },
                                  1105: {'Args': [
                                                [
                                                 -16017, 112.556396, 17041], 2, 'temp_locate', 'keep'],
                                         'Interface': 'show_locate'
                                         },
                                  1106: {'Args': [
                                                True, 5532],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  1107: {'Args': [
                                                True],
                                         'Interface': 'set_robot_eject_flag'
                                         },
                                  1201: {'Args': [
                                                [
                                                 5194, 5194], 5],
                                         'Interface': 'show_multi_human_tips'
                                         },
                                  1202: {'Args': 4,
                                         'Event': [
                                                 'E_GUIDE_ROBOT_DEAD', 'guide_robot_dead'],
                                         'Interface': 'set_death_top_score',
                                         'Next': [
                                                1301, 1302, 1303],
                                         'Prior': 1103
                                         },
                                  1203: {'Interface': 'show_robot_flag_ui'
                                         },
                                  1204: {'Args': [
                                                [
                                                 -16202.412109, 115.195343, 16759.449219], 5],
                                         'Interface': 'delay_show_locate_and_sfx'
                                         },
                                  1205: {'Args': [
                                                True, 5541],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  1206: {'Args': [
                                                False],
                                         'Interface': 'set_no_mecha_damage'
                                         },
                                  1301: {'Args': [
                                                5195, 5195, 5],
                                         'Interface': 'show_human_tips',
                                         'Next': 1401,
                                         'Prior': 1202
                                         },
                                  1302: {'Args': 5,
                                         'Interface': 'set_death_top_score'
                                         },
                                  1303: {'Interface': 'remove_locate_ui'
                                         },
                                  1401: {'Args': 1401,
                                         'Interface': 'create_end_ui',
                                         'Prior': 1301
                                         }
                                  },
                      'Name': '\xe6\x96\xb0\xe6\x89\x8b\xe5\x85\xb3\xe5\x8d\xa1-2',
                      'QuickLink': 1
                      },
       'StageMechaHandler': {'Content': {'ai_parachute_dir': {'handler_params': [
                                                                               -16393, 115, 16562]
                                                              },
                                         'ai_parachute_spd': {'handler_params': 100
                                                              },
                                         'eject_robot_guide_id': {'handler_params': 1202
                                                                  },
                                         'eject_robot_start_pos': {'handler_params': [
                                                                                    -16017, 112.556396, 17041]
                                                                   }
                                         },
                             'Name': '\xe7\xac\xac\xe4\xba\x8c\xe5\x85\xb3\xe5\xbc\x95\xe5\xaf\xbc\xe5\x8f\x82\xe6\x95\xb0\xe9\x85\x8d\xe7\xbd\xae',
                             'QuickLink': 1
                             },
       'StageThird': {'Content': {100: {'Interface': 'empty_guide_holder',
                                        'Next': [
                                               101, 102, 103],
                                        'NextShowMainUI': [
                                                         'BattleInfoUI', 'MoveRockerUI', 'FrontSightUI', 'WeaponBarSelectUI', 'FireRockerUI', 'BulletReloadUI', 'PostureControlUI', 'PickUI', 'DrugUI', 'FightLeftShotUI', 'HpInfoUI', 'FightReadyTipsUI', 'SceneInteractionUI', 'MechaControlMain'],
                                        'PCNextShowMainUI': [
                                                           'BattleInfoUI', 'FrontSightUI', 'WeaponBarSelectUI', 'BattleControlUIPC', 'PickUI', 'DrugUI', 'HpInfoUI', 'FightReadyTipsUI', 'SceneInteractionUI', 'MechaControlMain', 'BulletReloadProgressUI']
                                        },
                                  101: {'Args': [
                                               5211, 5],
                                        'Interface': 'show_human_tips',
                                        'Next': [
                                               201, 202, 203, 204, 205],
                                        'PCInterface': 'show_human_tips_pc',
                                        'Prior': 100
                                        },
                                  102: {'Args': [{10: 10232}],'Interface': 'equip_weapons'
                                        },
                                  103: {'Interface': 'do_nothing_guide',
                                        'PCArgs': [
                                                 [
                                                  'summon_call_mecha', 'switch_battle_bag'], True],
                                        'PCInterface': 'block_pc_hot_key'
                                        },
                                  201: {'Args': [
                                               5212, 5],
                                        'Interface': 'show_human_tips'
                                        },
                                  202: {'Args': [[{'item_id': 1666,'count': 1,'position': [5304, 191, -115]}]],'Event': [
                                                'E_GUIDE_ITEM_PICKED', 'on_guide_pick_item_event'],
                                        'Interface': 'create_items',
                                        'Next': [
                                               301, 302, 303],
                                        'Prior': 101
                                        },
                                  203: {'Args': [
                                               [
                                                5304, 183, -115], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_target_sfx'
                                        },
                                  204: {'Args': [
                                               [
                                                5304, 183, -115], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate_ui'
                                        },
                                  205: {'Args': [
                                               True, 5500],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  301: {'Args': [
                                               5213, 5],
                                        'Interface': 'do_nothing_guide',
                                        'PCArgs': [
                                                 5603, 5],
                                        'PCInterface': 'do_nothing_guide'
                                        },
                                  302: {'Args': [
                                               5213, 100],
                                        'Event': [
                                                'E_GUIDE_ITEM_USE_END', 'on_guide_item_use_end'],
                                        'Interface': 'show_use_drug_tip',
                                        'Next': [
                                               401, 402, 403, 404],
                                        'PCArgs': [
                                                 5463, 100, 'use_cur_item'],
                                        'Prior': 202
                                        },
                                  303: {'Args': [
                                               True, 5501],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  401: {'Args': [
                                               5214, 5],
                                        'Interface': 'show_human_tips',
                                        'Next': [
                                               501, 502, 503, 504, 505],
                                        'PCInterface': 'show_human_tips_pc',
                                        'Prior': 302
                                        },
                                  402: {'Args': [
                                               'nd_jump_tips', 'show_jump'],
                                        'Interface': 'show_nd_animation',
                                        'PCArgs': [
                                                 5464, 5, 'human_jump'],
                                        'PCInterface': 'show_little_tips_pc'
                                        },
                                  403: {'Args': [
                                               False],
                                        'Interface': 'show_attachable_ui',
                                        'PCArgs': [
                                                 'btn_skate_off', False],
                                        'PCInterface': 'set_control_btn_visible'
                                        },
                                  404: {'Interface': 'do_nothing_guide',
                                        'PCArgs': [
                                                 [
                                                  'get_off_skateboard_or_vehicle'], True],
                                        'PCInterface': 'block_pc_hot_key'
                                        },
                                  501: {'Args': [
                                               5215, 5],
                                        'Interface': 'show_human_tips',
                                        'PCInterface': 'show_human_tips_pc'
                                        },
                                  502: {'Args': [
                                               [
                                                6070, 40, -216], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_target_sfx'
                                        },
                                  503: {'Args': [
                                               [
                                                6070, 40, -216], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate_ui'
                                        },
                                  504: {'Args': [
                                               [
                                                6070, 40, -216], 4],
                                        'Interface': 'check_reach_target',
                                        'Next': [
                                               601, 602, 603, 604, 605, 606, 607],
                                        'Prior': 401
                                        },
                                  505: {'Args': [
                                               True, 5502],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  601: {'Args': [
                                               5216, 5],
                                        'Interface': 'show_human_tips',
                                        'PCInterface': 'show_human_tips_pc'
                                        },
                                  602: {'Args': {'role_id': 12,'position': [6614, 112, -744],'max_hp': 100,'shoot': True},'Event': [
                                                'E_GUIDE_ROBOT_DEAD', 'on_guide_robot_die'],
                                        'Interface': 'create_robot',
                                        'Next': [
                                               701, 702, 703, 704, 705, 706],
                                        'Prior': 504
                                        },
                                  603: {'Args': 10,
                                        'Interface': 'delay_remind_attack'
                                        },
                                  604: {'Event': [
                                                'E_SUCCESS_AIM', 'on_guide_hide_delay_attack_tip']
                                        },
                                  605: {'Event': [
                                                'E_QUIT_AIM', 'on_guide_hide_delay_attack_tip']
                                        },
                                  606: {'Args': [
                                               True, 5503],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  607: {'Interface': 'do_nothing_guide',
                                        'PCArgs': [
                                                 5605, 5],
                                        'PCInterface': 'show_little_tips_pc'
                                        },
                                  701: {'Args': [
                                               5217, 5],
                                        'Interface': 'show_human_tips',
                                        'PCArgs': [
                                                 5465, 5, 'get_off_skateboard_or_vehicle'],
                                        'PCInterface': 'show_human_tips_pc'
                                        },
                                  702: {'Args': [
                                               [
                                                6503, 123, -888], 'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_target_sfx'
                                        },
                                  703: {'Args': [
                                               [
                                                6503, 123, -888], 2, 'temp_locate', 'keep'],
                                        'Interface': 'show_locate_ui'
                                        },
                                  704: {'Args': [
                                               [
                                                6503, 123, -888], 4],
                                        'Interface': 'check_reach_target',
                                        'Next': [
                                               801, 802, 803, 804, 805, 806],
                                        'Prior': 602
                                        },
                                  705: {'Args': [
                                               True, 5502],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  706: {'Interface': 'do_nothing_guide',
                                        'PCArgs': [
                                                 5465, 5, 'get_off_skateboard_or_vehicle'],
                                        'PCInterface': 'show_little_tips_pc'
                                        },
                                  801: {'Args': [
                                               5296, 5],
                                        'Interface': 'show_human_tips',
                                        'PCInterface': 'do_nothing_guide'
                                        },
                                  802: {'Args': [
                                               True],
                                        'Interface': 'show_attachable_ui',
                                        'PCArgs': [
                                                 'btn_skate_off', True],
                                        'PCInterface': 'set_control_btn_visible'
                                        },
                                  803: {'Event': [
                                                'E_GUIDE_TRY_DETACH_END', 'on_guide_leave_skateboard'],
                                        'Next': [
                                               901, 902, 903, 904, 905, 906],
                                        'Prior': 704
                                        },
                                  804: {'Args': [
                                               'nd_skateboard_tips', 'show_skateboard'],
                                        'Interface': 'show_nd_animation',
                                        'PCArgs': [
                                                 5607, 5],
                                        'PCInterface': 'show_little_tips_pc'
                                        },
                                  805: {'Args': [
                                               True, 5504],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  806: {'Interface': 'do_nothing_guide',
                                        'PCArgs': [
                                                 [
                                                  'get_off_skateboard_or_vehicle'], False],
                                        'PCInterface': 'block_pc_hot_key'
                                        },
                                  901: {'Args': [
                                               5218, 5],
                                        'Interface': 'show_human_tips',
                                        'PCArgs': [
                                                 5468, 5, 'get_on_skateboard_or_vehicle'],
                                        'PCInterface': 'show_human_tips_pc'
                                        },
                                  902: {'Event': [
                                                'E_ENTER_SKATE_INTERACTION_ZONE', 'on_guide_enter_skate_zone']
                                        },
                                  903: {'Event': [
                                                'E_LEAVE_SKATE_INTERACTION_ZONE', 'on_guide_leave_skate_zone']
                                        },
                                  904: {'Event': [
                                                'E_SUCCESS_BOARD', 'on_guide_success_board'],
                                        'Next': [
                                               7001, 7002, 7003, 7004],
                                        'Prior': 803
                                        },
                                  905: {'Args': [
                                               'effect/fx/guide/guide_end.sfx'],
                                        'Interface': 'show_skateboard_sfx'
                                        },
                                  906: {'Args': [
                                               True, 5542],
                                        'Interface': 'show_side_tip_ui'
                                        },
                                  1001: {'Args': [
                                                5219, 5],
                                         'Interface': 'show_human_tips',
                                         'PCInterface': 'show_human_tips_pc'
                                         },
                                  1002: {'Args': [[{'item_id': 1667,'count': 1,'position': [6551, 188, -1110]}]],'Event': [
                                                 'E_GUIDE_ITEM_PICKED', 'on_guide_pick_item_event'],
                                         'Interface': 'create_items',
                                         'Next': [
                                                1101, 1102, 1103],
                                         'Prior': 7001
                                         },
                                  1003: {'Args': [
                                                [
                                                 6551, 183, -1110], 'effect/fx/guide/guide_end.sfx'],
                                         'Interface': 'show_target_sfx'
                                         },
                                  1004: {'Args': [
                                                [
                                                 6551, 183, -1110], 2, 'temp_locate', 'keep'],
                                         'Interface': 'show_locate_ui'
                                         },
                                  1005: {'Args': [
                                                True, 5505],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  1101: {'Args': [
                                                5220, 7],
                                         'Interface': 'show_human_tips',
                                         'PCArgs': [
                                                  5469, 7, 'use_cur_item'],
                                         'PCInterface': 'show_human_tips_pc'
                                         },
                                  1102: {'Args': [
                                                5284, 100],
                                         'Event': [
                                                 'E_GUIDE_JOIN_MECHA_END', 'on_guide_join_mecha_end'],
                                         'Interface': 'show_use_drug_tip',
                                         'Next': [
                                                1201, 1202, 1203, 1204],
                                         'Prior': 1002
                                         },
                                  1103: {'Args': [
                                                True, 5506],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  1201: {'Args': [
                                                5221, 5],
                                         'Interface': 'show_human_tips',
                                         'Next': [
                                                1301, 1302],
                                         'PCInterface': 'show_human_tips_pc',
                                         'Prior': 1102
                                         },
                                  1202: {'Args': [
                                                False],
                                         'Interface': 'show_get_off_chicken_btn',
                                         'PCArgs': [
                                                  'car_off', False],
                                         'PCInterface': 'set_control_btn_visible'
                                         },
                                  1203: {'Args': [
                                                False],
                                         'Interface': 'show_chicken_transform_btn',
                                         'PCArgs': [
                                                  'car_transform', False],
                                         'PCInterface': 'set_control_btn_visible'
                                         },
                                  1204: {'Interface': 'do_nothing_guide',
                                         'PCArgs': [
                                                  [
                                                   'get_off_skateboard_or_vehicle', 'car_transform'], True],
                                         'PCInterface': 'block_pc_hot_key'
                                         },
                                  1301: {'Args': [
                                                5297, 5],
                                         'Interface': 'show_human_tips',
                                         'Next': [
                                                1401, 1402, 1403, 1404, 1405, 1406],
                                         'PCArgs': [
                                                  5611, 5],
                                         'PCInterface': 'show_human_tips_pc',
                                         'Prior': 1201
                                         },
                                  1302: {'Args': [
                                                5198],
                                         'Interface': 'show_chicken_firerocker_tips',
                                         'PCInterface': 'do_nothing_guide'
                                         },
                                  1401: {'Args': [
                                                5222, 5],
                                         'Interface': 'show_human_tips',
                                         'PCArgs': [
                                                  5470, 5, 'car_transform'],
                                         'PCInterface': 'show_human_tips_pc'
                                         },
                                  1402: {'Args': [
                                                5285],
                                         'Interface': 'show_chicken_transform_tips',
                                         'PCInterface': 'do_nothing_guide'
                                         },
                                  1403: {'Event': [
                                                 'E_GUIDE_TRANSFORM_2_VEHICLE', 'on_guide_transform_2_vehicle'],
                                         'Next': [
                                                1501, 1502, 1503, 1504],
                                         'Prior': 1301
                                         },
                                  1404: {'Args': [
                                                True],
                                         'Interface': 'show_chicken_transform_btn',
                                         'PCArgs': [
                                                  'car_transform', True],
                                         'PCInterface': 'set_control_btn_visible'
                                         },
                                  1405: {'Args': [
                                                True, 5507],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  1406: {'Interface': 'do_nothing_guide',
                                         'PCArgs': [
                                                  [
                                                   'car_transform'], False],
                                         'PCInterface': 'block_pc_hot_key'
                                         },
                                  1501: {'Args': 3,
                                         'Interface': 'wait_guide_handler',
                                         'Next': [
                                                1601, 1602, 1603, 1604, 1605, 1606],
                                         'Prior': 1403
                                         },
                                  1502: {'Args': [
                                                False],
                                         'Interface': 'show_chicken_transform_btn',
                                         'PCArgs': [
                                                  'car_transform', False],
                                         'PCInterface': 'set_control_btn_visible'
                                         },
                                  1503: {'Args': [
                                                False],
                                         'Interface': 'show_chicken_speed_btn',
                                         'PCArgs': [
                                                  'car_rush', False],
                                         'PCInterface': 'set_control_btn_visible'
                                         },
                                  1504: {'Interface': 'do_nothing_guide',
                                         'PCArgs': [
                                                  [
                                                   'car_rush', 'car_transform'], True],
                                         'PCInterface': 'block_pc_hot_key'
                                         },
                                  1601: {'Args': [
                                                5223, 5],
                                         'Interface': 'show_human_tips',
                                         'PCArgs': [
                                                  5471, 5, 'car_rush'],
                                         'PCInterface': 'show_human_tips_pc'
                                         },
                                  1602: {'Args': [
                                                'nd_boost_tips', 'show_boost'],
                                         'Interface': 'show_nd_animation',
                                         'PCArgs': [
                                                  5472, 5, 'car_rush'],
                                         'PCInterface': 'show_little_tips_pc'
                                         },
                                  1603: {'Event': [
                                                 'E_GUIDE_CHICKEN_DASH', 'on_guide_chicken_dash'],
                                         'Next': [
                                                1701, 1702, 1703, 1704, 1705, 1707, 1708, 1709, 1710, 1711],
                                         'Prior': 1501
                                         },
                                  1604: {'Args': [
                                                True],
                                         'Interface': 'show_chicken_speed_btn',
                                         'PCArgs': [
                                                  'car_rush', True],
                                         'PCInterface': 'set_control_btn_visible'
                                         },
                                  1605: {'Args': [
                                                True, 5508],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  1606: {'PCArgs': [
                                                  [
                                                   'car_rush'], False],
                                         'PCInterface': 'block_pc_hot_key'
                                         },
                                  1701: {'Args': [
                                                5224, 5],
                                         'Interface': 'show_human_tips',
                                         'PCInterface': 'show_human_tips_pc'
                                         },
                                  1702: {'Args': [
                                                [
                                                 5375, 185, -54], 'effect/fx/guide/guide_end.sfx'],
                                         'Interface': 'show_target_sfx'
                                         },
                                  1703: {'Args': [
                                                [
                                                 5375, 185, -54], 2, 'temp_locate', 'keep'],
                                         'Interface': 'show_locate_ui'
                                         },
                                  1704: {'Args': [
                                                [
                                                 5375, 185, -54], 4],
                                         'Interface': 'check_reach_target',
                                         'Next': [
                                                1801, 1802, 1803, 1804, 1805, 1806, 1807, 1808, 1809],
                                         'Prior': 1603
                                         },
                                  1705: {'Args': [
                                                True],
                                         'Interface': 'show_chicken_transform_btn',
                                         'PCArgs': [
                                                  'car_transform', True],
                                         'PCInterface': 'set_control_btn_visible'
                                         },
                                  1706: {'Args': 10,
                                         'Interface': 'delay_remind_transform'
                                         },
                                  1707: {'Event': [
                                                 'E_GUIDE_TRANSFORM_2_NORMAL', 'on_guide_hide_delay_trans_tip']
                                         },
                                  1708: {'Args': [
                                                True, 5502],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  1709: {'Interface': 'do_nothing_guide',
                                         'PCArgs': [
                                                  [
                                                   'car_transform'], False],
                                         'PCInterface': 'block_pc_hot_key'
                                         },
                                  1710: {'Interface': 'check_block'
                                         },
                                  1711: {'Interface': 'register_chicken_block_check'
                                         },
                                  1801: {'Args': [
                                                5225, 5],
                                         'Interface': 'show_human_tips',
                                         'PCArgs': [
                                                  5473, 5, 'get_off_skateboard_or_vehicle'],
                                         'PCInterface': 'show_human_tips_pc'
                                         },
                                  1802: {'Args': [
                                                [
                                                 5002, 186, -1222], 'effect/fx/guide/guide_end.sfx'],
                                         'Interface': 'show_target_sfx'
                                         },
                                  1803: {'Args': [
                                                [
                                                 5002, 186, -1222], 2, 'temp_locate', 'keep'],
                                         'Interface': 'show_locate_ui'
                                         },
                                  1804: {'Args': [
                                                True],
                                         'Interface': 'show_get_off_chicken_btn',
                                         'PCArgs': [
                                                  'car_off', True],
                                         'PCInterface': 'set_control_btn_visible'
                                         },
                                  1805: {'Args': [
                                                'nd_drive_off_tips', 'show_drive_off'],
                                         'Interface': 'show_nd_animation',
                                         'PCArgs': [
                                                  5474, 5, 'get_off_skateboard_or_vehicle'],
                                         'PCInterface': 'show_little_tips_pc'
                                         },
                                  1806: {'Interface': 'check_human_in_water',
                                         'PCInterface': 'do_nothing_guide'
                                         },
                                  1807: {'Event': [
                                                 'E_GUIDE_LEAVE_CHICKEN', 'on_guide_leave_chicken'],
                                         'Next': [
                                                1901, 1902, 1903, 1904, 1905, 1906, 1907],
                                         'Prior': 1704
                                         },
                                  1808: {'Args': [
                                                True, 5543],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  1809: {'PCArgs': [
                                                  [
                                                   'get_off_skateboard_or_vehicle'], False],
                                         'PCInterface': 'block_pc_hot_key'
                                         },
                                  1901: {'Args': [
                                                5226, 5],
                                         'Interface': 'show_human_tips',
                                         'PCArgs': [
                                                  5475, 5, 'get_on_skateboard_or_vehicle'],
                                         'PCInterface': 'show_human_tips_pc'
                                         },
                                  1902: {'Event': [
                                                 'E_ENTER_MECHA_INTERACTION_ZONE', 'on_guide_enter_mecha_zone']
                                         },
                                  1903: {'Event': [
                                                 'E_LEAVE_MECHA_INTERACTION_ZONE', 'on_guide_leave_mecha_zone']
                                         },
                                  1904: {'Event': [
                                                 'E_GUIDE_JOIN_MECHA_END', 'on_guide_join_mecha_end_no_card'],
                                         'Next': [
                                                8001, 8002, 8003, 8004],
                                         'Prior': 1807
                                         },
                                  1905: {'Args': [
                                                True, 5544],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  1906: {'PCArgs': [
                                                  5476, 5, 'get_on_skateboard_or_vehicle'],
                                         'PCInterface': 'show_little_tips_pc'
                                         },
                                  1907: {'Args': [
                                                'effect/fx/guide/guide_end.sfx'],
                                         'Interface': 'show_chicken_sfx'
                                         },
                                  2001: {'Args': [
                                                5227, 5],
                                         'Interface': 'show_human_tips',
                                         'PCInterface': 'show_human_tips_pc'
                                         },
                                  2002: {'Args': [
                                                6021, {'npc_id': 1,'position': [5304, 183, -115]}],
                                         'Interface': 'create_building'
                                         },
                                  2003: {'Args': [
                                                [
                                                 5304, 183, -112], 'effect/fx/guide/guide_end.sfx'],
                                         'Interface': 'show_target_sfx'
                                         },
                                  2004: {'Args': [
                                                [
                                                 5304, 183, -112], 2, 'temp_locate', 'keep'],
                                         'Interface': 'show_locate_ui'
                                         },
                                  2005: {'Event': [
                                                 'E_GUIDE_SUPER_JUMP_END', 'on_guide_super_jump_end'],
                                         'Next': 2101,
                                         'Prior': 8001
                                         },
                                  2006: {'Args': [
                                                True, 5509],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  2101: {'Args': [
                                                5228, 5],
                                         'Interface': 'show_human_tips',
                                         'Next': [
                                                2201, 2202, 2203, 2204, 2205, 2206, 2207],
                                         'NextShowMainUI': [
                                                          'MechaUI', 'MechaHpInfoUI'],
                                         'PCInterface': 'show_human_tips_pc',
                                         'Prior': 2005
                                         },
                                  2201: {'Args': [
                                                5229, 5],
                                         'Interface': 'show_human_tips',
                                         'PCArgs': [
                                                  5477, 5, 'summon_call_mecha'],
                                         'PCInterface': 'show_human_tips_pc'
                                         },
                                  2202: {'Interface': 'clear_call_mecha_cd'
                                         },
                                  2203: {'Args': [
                                                'nd_step_13', 'show_13'],
                                         'Event': [
                                                 'E_ON_JOIN_MECHA_START', 'on_guide_join_mecha_start'],
                                         'Interface': 'show_nd_animation',
                                         'Next': [
                                                2301, 2302, 2303, 2304, 2305, 2306, 2307, 2308, 2309],
                                         'PCArgs': [
                                                  920839, 'summon_call_mecha'],
                                         'PCInterface': 'show_summon_mecha_tip',
                                         'Prior': 2101
                                         },
                                  2204: {'Args': [
                                                True, 5510],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  2205: {'Event': [
                                                 'E_WATER_EVENT', 'on_guide_water_status_change']
                                         },
                                  2206: {'Interface': 'init_mecha_call_btn_ban_status'
                                         },
                                  2207: {'Interface': 'do_nothing_guide',
                                         'PCArgs': [
                                                  [
                                                   'summon_call_mecha'], False],
                                         'PCInterface': 'block_pc_hot_key'
                                         },
                                  2301: {'Args': [
                                                5230, 100],
                                         'Interface': 'show_human_tips',
                                         'PCInterface': 'show_human_tips_pc'
                                         },
                                  2302: {'Args': [
                                                [
                                                 5943, -120, -577], 'effect/fx/guide/guide_end.sfx'],
                                         'Interface': 'show_target_sfx'
                                         },
                                  2303: {'Args': [
                                                [
                                                 5943, -120, -577], 2, 'temp_locate', 'keep'],
                                         'Interface': 'show_locate_ui'
                                         },
                                  2304: {'Args': [
                                                [
                                                 5943, -120, -577], 4],
                                         'Interface': 'check_reach_target',
                                         'Next': 2401,
                                         'Prior': 2203
                                         },
                                  2305: {'Event': [
                                                 'E_GUIDE_MECHA_STATE_CHANGE', 'on_guide_mecha_change_state']
                                         },
                                  2306: {'Event': [
                                                 'E_GUIDE_MECHA_STATE_CHANGE', 'on_guide_mecha_change_show_tips']
                                         },
                                  2307: {'Args': [
                                                True, 5502],
                                         'Interface': 'show_side_tip_ui'
                                         },
                                  2308: {'Interface': 'do_nothing_guide',
                                         'PCArgs': [
                                                  [
                                                   'summon_call_mecha'], True],
                                         'PCInterface': 'block_pc_hot_key'
                                         },
                                  2309: {'Interface': 'regist_mecha_diving_delay_riko_tip'
                                         },
                                  2401: {'Args': [
                                                5231, 5],
                                         'Interface': 'show_human_tips',
                                         'Next': 2501,
                                         'PCInterface': 'show_human_tips_pc',
                                         'Prior': 2304
                                         },
                                  2501: {'Args': 2501,
                                         'Interface': 'create_end_ui',
                                         'Prior': 2401
                                         },
                                  7001: {'Args': 1,
                                         'Interface': 'wait_guide_handler',
                                         'Next': [
                                                1001, 1002, 1003, 1004, 1005],
                                         'Prior': 904
                                         },
                                  7002: {'Args': [
                                                False],
                                         'Interface': 'enable_rocker_move'
                                         },
                                  7003: {'Args': [
                                                False],
                                         'Interface': 'enable_screen_touch'
                                         },
                                  7004: {'Args': [
                                                [
                                                 6551, 183, -1110]],
                                         'Interface': 'turn_dir_by_target_pos'
                                         },
                                  8001: {'Args': 1,
                                         'Interface': 'wait_guide_handler',
                                         'Next': [
                                                2001, 2002, 2003, 2004, 2005, 2006],
                                         'Prior': 1904
                                         },
                                  8002: {'Args': [
                                                False],
                                         'Interface': 'enable_rocker_move'
                                         },
                                  8003: {'Args': [
                                                False],
                                         'Interface': 'enable_screen_touch'
                                         },
                                  8004: {'Args': [
                                                [
                                                 5304, 183, -115]],
                                         'Interface': 'turn_dir_by_target_pos'
                                         }
                                  },
                      'Name': '\xe6\x96\xb0\xe6\x89\x8b\xe5\x85\xb3\xe5\x8d\xa1-3',
                      'QuickLink': 1
                      },
       'StageThirdEndHandler': {'Content': {'on_guide_chicken_dash': {'handler_params': 1603
                                                                      },
                                            'on_guide_item_use_end': {'handler_params': {1666: 302,1667: 1102}},'on_guide_join_mecha_end': {'handler_params': 1102
                                                                        },
                                            'on_guide_join_mecha_end_no_card': {'handler_params': 1904
                                                                                },
                                            'on_guide_join_mecha_start': {'handler_params': 2203
                                                                          },
                                            'on_guide_leave_chicken': {'handler_params': 1807
                                                                       },
                                            'on_guide_leave_skateboard': {'handler_params': 803
                                                                          },
                                            'on_guide_success_board': {'handler_params': 904
                                                                       },
                                            'on_guide_super_jump_end': {'handler_params': 2005
                                                                        },
                                            'on_guide_transform_2_vehicle': {'handler_params': 1403
                                                                             }
                                            },
                                'Name': '\xe7\xac\xac\xe4\xb8\x89\xe5\x85\xb3\xe7\xbb\x93\xe6\x9d\x9f\xe5\xbc\x95\xe5\xaf\xbc\xe5\x8f\x82\xe6\x95\xb0\xe9\x85\x8d\xe7\xbd\xae',
                                'QuickLink': 1
                                },
       'ViewRangeConfig': {'Content': {201: {'view_range': 1000.0
                                             },
                                       202: {'view_range': 500.0
                                             },
                                       203: {'view_range': 500.0
                                             },
                                       204: {'view_range': 500.0
                                             }
                                       },
                           'Name': '\xe5\x8a\xa0\xe8\xbd\xbd\xe8\x8c\x83\xe5\x9b\xb4\xe9\x85\x8d\xe7\xbd\xae',
                           'QuickLink': 1
                           },
       'WeaponDamage': {'Content': {1011: {'human_head_hit': 37,
                                           'human_other_hit': 15,
                                           'mecha_head_hit': 16,
                                           'mecha_other_hit': 13
                                           },
                                    1663: {'human_head_hit': 30,
                                           'human_other_hit': 12,
                                           'mecha_head_hit': 11,
                                           'mecha_other_hit': 9
                                           },
                                    6015: {'human_head_hit': 150,
                                           'human_other_hit': 60,
                                           'mecha_head_hit': 72,
                                           'mecha_other_hit': 60
                                           },
                                    8203: {'human_head_hit': 50,
                                           'human_other_hit': 20,
                                           'mecha_head_hit': 24,
                                           'mecha_other_hit': 20
                                           },
                                    8204: {'human_head_hit': 25000,
                                           'human_other_hit': 10000,
                                           'mecha_head_hit': 12000,
                                           'mecha_other_hit': 10000
                                           },
                                    8205: {'human_head_hit': 200,
                                           'human_other_hit': 80,
                                           'mecha_head_hit': 480,
                                           'mecha_other_hit': 400
                                           },
                                    8206: {'human_head_hit': 25000,
                                           'human_other_hit': 10000,
                                           'mecha_head_hit': 0,
                                           'mecha_other_hit': 0
                                           },
                                    8992: {'human_head_hit': 60,
                                           'human_other_hit': 24,
                                           'mecha_head_hit': 26,
                                           'mecha_other_hit': 22
                                           },
                                    8993: {'human_head_hit': 100,
                                           'human_other_hit': 40,
                                           'mecha_head_hit': 180,
                                           'mecha_other_hit': 150
                                           },
                                    8994: {'human_head_hit': 75,
                                           'human_other_hit': 30,
                                           'mecha_head_hit': 90,
                                           'mecha_other_hit': 75
                                           },
                                    8995: {'human_head_hit': 175,
                                           'human_other_hit': 70,
                                           'mecha_head_hit': 420,
                                           'mecha_other_hit': 350
                                           },
                                    10010: {'human_head_hit': 71,
                                            'human_other_hit': 32,
                                            'mecha_head_hit': 39,
                                            'mecha_other_hit': 32
                                            },
                                    10011: {'human_head_hit': 75,
                                            'human_other_hit': 34,
                                            'mecha_head_hit': 41,
                                            'mecha_other_hit': 34
                                            },
                                    10012: {'human_head_hit': 77,
                                            'human_other_hit': 35,
                                            'mecha_head_hit': 42,
                                            'mecha_other_hit': 35
                                            },
                                    10013: {'human_head_hit': 78,
                                            'human_other_hit': 36,
                                            'mecha_head_hit': 43,
                                            'mecha_other_hit': 36
                                            },
                                    10015: {'human_head_hit': 82,
                                            'human_other_hit': 37,
                                            'mecha_head_hit': 45,
                                            'mecha_other_hit': 37
                                            },
                                    10021: {'human_head_hit': 138,
                                            'human_other_hit': 51,
                                            'mecha_head_hit': 58,
                                            'mecha_other_hit': 49
                                            },
                                    10022: {'human_head_hit': 144,
                                            'human_other_hit': 53,
                                            'mecha_head_hit': 61,
                                            'mecha_other_hit': 51
                                            },
                                    10023: {'human_head_hit': 149,
                                            'human_other_hit': 55,
                                            'mecha_head_hit': 63,
                                            'mecha_other_hit': 53
                                            },
                                    10213: {'human_head_hit': 450,
                                            'human_other_hit': 180,
                                            'mecha_head_hit': 388,
                                            'mecha_other_hit': 324
                                            },
                                    10214: {'human_head_hit': 500,
                                            'human_other_hit': 200,
                                            'mecha_head_hit': 456,
                                            'mecha_other_hit': 380
                                            },
                                    10215: {'human_head_hit': 550,
                                            'human_other_hit': 220,
                                            'mecha_head_hit': 501,
                                            'mecha_other_hit': 418
                                            },
                                    10231: {'human_head_hit': 190,
                                            'human_other_hit': 76,
                                            'mecha_head_hit': 164,
                                            'mecha_other_hit': 136
                                            },
                                    10232: {'human_head_hit': 195,
                                            'human_other_hit': 78,
                                            'mecha_head_hit': 168,
                                            'mecha_other_hit': 140
                                            },
                                    10233: {'human_head_hit': 200,
                                            'human_other_hit': 80,
                                            'mecha_head_hit': 172,
                                            'mecha_other_hit': 144
                                            },
                                    10313: {'human_head_hit': 55,
                                            'human_other_hit': 22,
                                            'mecha_head_hit': 38,
                                            'mecha_other_hit': 31
                                            },
                                    10314: {'human_head_hit': 62,
                                            'human_other_hit': 25,
                                            'mecha_head_hit': 43,
                                            'mecha_other_hit': 36
                                            },
                                    10414: {'human_head_hit': 102,
                                            'human_other_hit': 41,
                                            'mecha_head_hit': 39,
                                            'mecha_other_hit': 32
                                            },
                                    10521: {'human_head_hit': 137,
                                            'human_other_hit': 55,
                                            'mecha_head_hit': 480,
                                            'mecha_other_hit': 400
                                            },
                                    10522: {'human_head_hit': 142,
                                            'human_other_hit': 57,
                                            'mecha_head_hit': 504,
                                            'mecha_other_hit': 420
                                            },
                                    10523: {'human_head_hit': 150,
                                            'human_other_hit': 60,
                                            'mecha_head_hit': 540,
                                            'mecha_other_hit': 450
                                            },
                                    10525: {'human_head_hit': 155,
                                            'human_other_hit': 62,
                                            'mecha_head_hit': 564,
                                            'mecha_other_hit': 470
                                            },
                                    10533: {'human_head_hit': 75,
                                            'human_other_hit': 30,
                                            'mecha_head_hit': 252,
                                            'mecha_other_hit': 210
                                            },
                                    10534: {'human_head_hit': 100,
                                            'human_other_hit': 40,
                                            'mecha_head_hit': 360,
                                            'mecha_other_hit': 300
                                            },
                                    10542: {'human_head_hit': 225,
                                            'human_other_hit': 90,
                                            'mecha_head_hit': 696,
                                            'mecha_other_hit': 580
                                            },
                                    10543: {'human_head_hit': 237,
                                            'human_other_hit': 95,
                                            'mecha_head_hit': 816,
                                            'mecha_other_hit': 680
                                            },
                                    10544: {'human_head_hit': 250,
                                            'human_other_hit': 100,
                                            'mecha_head_hit': 912,
                                            'mecha_other_hit': 760
                                            },
                                    10545: {'human_head_hit': 225,
                                            'human_other_hit': 90,
                                            'mecha_head_hit': 648,
                                            'mecha_other_hit': 540
                                            },
                                    10552: {'human_head_hit': 102,
                                            'human_other_hit': 68,
                                            'mecha_head_hit': 408,
                                            'mecha_other_hit': 340
                                            },
                                    10553: {'human_head_hit': 105,
                                            'human_other_hit': 70,
                                            'mecha_head_hit': 420,
                                            'mecha_other_hit': 350
                                            },
                                    10554: {'human_head_hit': 108,
                                            'human_other_hit': 72,
                                            'mecha_head_hit': 432,
                                            'mecha_other_hit': 360
                                            },
                                    10573: {'human_head_hit': 157,
                                            'human_other_hit': 63,
                                            'mecha_head_hit': 504,
                                            'mecha_other_hit': 420
                                            },
                                    10574: {'human_head_hit': 162,
                                            'human_other_hit': 65,
                                            'mecha_head_hit': 546,
                                            'mecha_other_hit': 455
                                            },
                                    10611: {'human_head_hit': 65,
                                            'human_other_hit': 26,
                                            'mecha_head_hit': 187,
                                            'mecha_other_hit': 156
                                            },
                                    10612: {'human_head_hit': 70,
                                            'human_other_hit': 28,
                                            'mecha_head_hit': 201,
                                            'mecha_other_hit': 168
                                            },
                                    10613: {'human_head_hit': 75,
                                            'human_other_hit': 30,
                                            'mecha_head_hit': 216,
                                            'mecha_other_hit': 180
                                            },
                                    10615: {'human_head_hit': 80,
                                            'human_other_hit': 32,
                                            'mecha_head_hit': 230,
                                            'mecha_other_hit': 192
                                            },
                                    10623: {'human_head_hit': 37,
                                            'human_other_hit': 15,
                                            'mecha_head_hit': 108,
                                            'mecha_other_hit': 90
                                            },
                                    10624: {'human_head_hit': 42,
                                            'human_other_hit': 17,
                                            'mecha_head_hit': 122,
                                            'mecha_other_hit': 102
                                            },
                                    10631: {'human_head_hit': 162,
                                            'human_other_hit': 65,
                                            'mecha_head_hit': 358,
                                            'mecha_other_hit': 299
                                            },
                                    10652: {'human_head_hit': 52,
                                            'human_other_hit': 21,
                                            'mecha_head_hit': 25,
                                            'mecha_other_hit': 21
                                            },
                                    10653: {'human_head_hit': 50,
                                            'human_other_hit': 20,
                                            'mecha_head_hit': 24,
                                            'mecha_other_hit': 20
                                            },
                                    10654: {'human_head_hit': 57,
                                            'human_other_hit': 23,
                                            'mecha_head_hit': 27,
                                            'mecha_other_hit': 23
                                            },
                                    105522: {'human_head_hit': 102,
                                             'human_other_hit': 68,
                                             'mecha_head_hit': 408,
                                             'mecha_other_hit': 340
                                             },
                                    105523: {'human_head_hit': 102,
                                             'human_other_hit': 68,
                                             'mecha_head_hit': 408,
                                             'mecha_other_hit': 340
                                             },
                                    105532: {'human_head_hit': 105,
                                             'human_other_hit': 70,
                                             'mecha_head_hit': 420,
                                             'mecha_other_hit': 350
                                             },
                                    105533: {'human_head_hit': 105,
                                             'human_other_hit': 70,
                                             'mecha_head_hit': 420,
                                             'mecha_other_hit': 350
                                             },
                                    105542: {'human_head_hit': 108,
                                             'human_other_hit': 72,
                                             'mecha_head_hit': 432,
                                             'mecha_other_hit': 360
                                             },
                                    105543: {'human_head_hit': 108,
                                             'human_other_hit': 72,
                                             'mecha_head_hit': 432,
                                             'mecha_other_hit': 360
                                             },
                                    105611: {'human_head_hit': 87,
                                             'human_other_hit': 35,
                                             'mecha_head_hit': 504,
                                             'mecha_other_hit': 420
                                             },
                                    105621: {'human_head_hit': 92,
                                             'human_other_hit': 37,
                                             'mecha_head_hit': 540,
                                             'mecha_other_hit': 450
                                             },
                                    105631: {'human_head_hit': 100,
                                             'human_other_hit': 40,
                                             'mecha_head_hit': 576,
                                             'mecha_other_hit': 480
                                             },
                                    106231: {'human_head_hit': 57,
                                             'human_other_hit': 23,
                                             'mecha_head_hit': 110,
                                             'mecha_other_hit': 92
                                             },
                                    106241: {'human_head_hit': 62,
                                             'human_other_hit': 25,
                                             'mecha_head_hit': 120,
                                             'mecha_other_hit': 100
                                             },
                                    800101: {'human_head_hit': 65,
                                             'human_other_hit': 26,
                                             'mecha_head_hit': 69,
                                             'mecha_other_hit': 58
                                             },
                                    800102: {'human_head_hit': 25,
                                             'human_other_hit': 25,
                                             'mecha_head_hit': 125,
                                             'mecha_other_hit': 125
                                             },
                                    800103: {'human_head_hit': 23,
                                             'human_other_hit': 23,
                                             'mecha_head_hit': 112,
                                             'mecha_other_hit': 112
                                             },
                                    800201: {'human_head_hit': 140,
                                             'human_other_hit': 56,
                                             'mecha_head_hit': 270,
                                             'mecha_other_hit': 225
                                             },
                                    800301: {'human_head_hit': 145,
                                             'human_other_hit': 58,
                                             'mecha_head_hit': 235,
                                             'mecha_other_hit': 196
                                             },
                                    800302: {'human_head_hit': 250,
                                             'human_other_hit': 100,
                                             'mecha_head_hit': 480,
                                             'mecha_other_hit': 400
                                             },
                                    800303: {'human_head_hit': 250,
                                             'human_other_hit': 100,
                                             'mecha_head_hit': 510,
                                             'mecha_other_hit': 425
                                             },
                                    800304: {'human_head_hit': 250,
                                             'human_other_hit': 100,
                                             'mecha_head_hit': 510,
                                             'mecha_other_hit': 425
                                             },
                                    800401: {'human_head_hit': 90,
                                             'human_other_hit': 36,
                                             'mecha_head_hit': 264,
                                             'mecha_other_hit': 220
                                             },
                                    800402: {'human_head_hit': 45,
                                             'human_other_hit': 18,
                                             'mecha_head_hit': 86,
                                             'mecha_other_hit': 72
                                             },
                                    800403: {'human_head_hit': 90,
                                             'human_other_hit': 36,
                                             'mecha_head_hit': 264,
                                             'mecha_other_hit': 220
                                             },
                                    800404: {'human_head_hit': 45,
                                             'human_other_hit': 18,
                                             'mecha_head_hit': 86,
                                             'mecha_other_hit': 72
                                             },
                                    800411: {'human_head_hit': 275,
                                             'human_other_hit': 110,
                                             'mecha_head_hit': 720,
                                             'mecha_other_hit': 600
                                             },
                                    800412: {'human_head_hit': 275,
                                             'human_other_hit': 110,
                                             'mecha_head_hit': 720,
                                             'mecha_other_hit': 600
                                             },
                                    800501: {'human_head_hit': 110,
                                             'human_other_hit': 44,
                                             'mecha_head_hit': 258,
                                             'mecha_other_hit': 215
                                             },
                                    800502: {'human_head_hit': 300,
                                             'human_other_hit': 120,
                                             'mecha_head_hit': 792,
                                             'mecha_other_hit': 660
                                             },
                                    800503: {'human_head_hit': 220,
                                             'human_other_hit': 88,
                                             'mecha_head_hit': 792,
                                             'mecha_other_hit': 660
                                             },
                                    800504: {'human_head_hit': 200,
                                             'human_other_hit': 80,
                                             'mecha_head_hit': 624,
                                             'mecha_other_hit': 520
                                             },
                                    800601: {'human_head_hit': 52,
                                             'human_other_hit': 21,
                                             'mecha_head_hit': 106,
                                             'mecha_other_hit': 89
                                             },
                                    800602: {'human_head_hit': 250,
                                             'human_other_hit': 100,
                                             'mecha_head_hit': 600,
                                             'mecha_other_hit': 500
                                             },
                                    800603: {'human_head_hit': 55,
                                             'human_other_hit': 22,
                                             'mecha_head_hit': 110,
                                             'mecha_other_hit': 92
                                             },
                                    800701: {'human_head_hit': 175,
                                             'human_other_hit': 70,
                                             'mecha_head_hit': 302,
                                             'mecha_other_hit': 252
                                             },
                                    800702: {'human_head_hit': 225,
                                             'human_other_hit': 90,
                                             'mecha_head_hit': 432,
                                             'mecha_other_hit': 360
                                             },
                                    800703: {'human_head_hit': 250,
                                             'human_other_hit': 100,
                                             'mecha_head_hit': 504,
                                             'mecha_other_hit': 420
                                             },
                                    800704: {'human_head_hit': 300,
                                             'human_other_hit': 120,
                                             'mecha_head_hit': 648,
                                             'mecha_other_hit': 540
                                             },
                                    800705: {'human_head_hit': 337,
                                             'human_other_hit': 135,
                                             'mecha_head_hit': 810,
                                             'mecha_other_hit': 675
                                             },
                                    800706: {'human_head_hit': 387,
                                             'human_other_hit': 155,
                                             'mecha_head_hit': 948,
                                             'mecha_other_hit': 790
                                             },
                                    800707: {'human_head_hit': 185,
                                             'human_other_hit': 74,
                                             'mecha_head_hit': 355,
                                             'mecha_other_hit': 296
                                             },
                                    800801: {'human_head_hit': 87,
                                             'human_other_hit': 35,
                                             'mecha_head_hit': 168,
                                             'mecha_other_hit': 140
                                             },
                                    800802: {'human_head_hit': 100,
                                             'human_other_hit': 40,
                                             'mecha_head_hit': 96,
                                             'mecha_other_hit': 80
                                             },
                                    800803: {'human_head_hit': 87,
                                             'human_other_hit': 35,
                                             'mecha_head_hit': 168,
                                             'mecha_other_hit': 140
                                             },
                                    800804: {'human_head_hit': 87,
                                             'human_other_hit': 35,
                                             'mecha_head_hit': 168,
                                             'mecha_other_hit': 140
                                             },
                                    800805: {'human_head_hit': 87,
                                             'human_other_hit': 35,
                                             'mecha_head_hit': 168,
                                             'mecha_other_hit': 140
                                             },
                                    800901: {'human_head_hit': 92,
                                             'human_other_hit': 37,
                                             'mecha_head_hit': 104,
                                             'mecha_other_hit': 87
                                             },
                                    800902: {'human_head_hit': 42,
                                             'human_other_hit': 17,
                                             'mecha_head_hit': 40,
                                             'mecha_other_hit': 34
                                             },
                                    800903: {'human_head_hit': 125,
                                             'human_other_hit': 50,
                                             'mecha_head_hit': 336,
                                             'mecha_other_hit': 280
                                             },
                                    800904: {'human_head_hit': 37,
                                             'human_other_hit': 15,
                                             'mecha_head_hit': 36,
                                             'mecha_other_hit': 30
                                             },
                                    800905: {'human_head_hit': 37,
                                             'human_other_hit': 15,
                                             'mecha_head_hit': 27,
                                             'mecha_other_hit': 22
                                             },
                                    800906: {'human_head_hit': 62,
                                             'human_other_hit': 25,
                                             'mecha_head_hit': 150,
                                             'mecha_other_hit': 125
                                             },
                                    800907: {'human_head_hit': 37,
                                             'human_other_hit': 15,
                                             'mecha_head_hit': 54,
                                             'mecha_other_hit': 45
                                             },
                                    800908: {'human_head_hit': 30,
                                             'human_other_hit': 12,
                                             'mecha_head_hit': 28,
                                             'mecha_other_hit': 24
                                             },
                                    801001: {'human_head_hit': 50,
                                             'human_other_hit': 20,
                                             'mecha_head_hit': 36,
                                             'mecha_other_hit': 30
                                             },
                                    801002: {'human_head_hit': 50,
                                             'human_other_hit': 20,
                                             'mecha_head_hit': 36,
                                             'mecha_other_hit': 30
                                             },
                                    801003: {'human_head_hit': 50,
                                             'human_other_hit': 20,
                                             'mecha_head_hit': 36,
                                             'mecha_other_hit': 30
                                             },
                                    801004: {'human_head_hit': 150,
                                             'human_other_hit': 60,
                                             'mecha_head_hit': 360,
                                             'mecha_other_hit': 300
                                             },
                                    801005: {'human_head_hit': 150,
                                             'human_other_hit': 60,
                                             'mecha_head_hit': 360,
                                             'mecha_other_hit': 300
                                             },
                                    801006: {'human_head_hit': 150,
                                             'human_other_hit': 60,
                                             'mecha_head_hit': 360,
                                             'mecha_other_hit': 300
                                             },
                                    801007: {'human_head_hit': 150,
                                             'human_other_hit': 60,
                                             'mecha_head_hit': 360,
                                             'mecha_other_hit': 300
                                             },
                                    801008: {'human_head_hit': 75,
                                             'human_other_hit': 30,
                                             'mecha_head_hit': 201,
                                             'mecha_other_hit': 168
                                             },
                                    801009: {'human_head_hit': 75,
                                             'human_other_hit': 30,
                                             'mecha_head_hit': 201,
                                             'mecha_other_hit': 168
                                             },
                                    801010: {'human_head_hit': 75,
                                             'human_other_hit': 30,
                                             'mecha_head_hit': 201,
                                             'mecha_other_hit': 168
                                             },
                                    801011: {'human_head_hit': 75,
                                             'human_other_hit': 30,
                                             'mecha_head_hit': 201,
                                             'mecha_other_hit': 168
                                             },
                                    801201: {'human_head_hit': 137,
                                             'human_other_hit': 55,
                                             'mecha_head_hit': 264,
                                             'mecha_other_hit': 220
                                             },
                                    801202: {'human_head_hit': 300,
                                             'human_other_hit': 120,
                                             'mecha_head_hit': 600,
                                             'mecha_other_hit': 500
                                             },
                                    801203: {'human_head_hit': 60,
                                             'human_other_hit': 24,
                                             'mecha_head_hit': 120,
                                             'mecha_other_hit': 100
                                             },
                                    801301: {'human_head_hit': 125,
                                             'human_other_hit': 50,
                                             'mecha_head_hit': 180,
                                             'mecha_other_hit': 150
                                             },
                                    801302: {'human_head_hit': 225,
                                             'human_other_hit': 90,
                                             'mecha_head_hit': 486,
                                             'mecha_other_hit': 405
                                             },
                                    801303: {'human_head_hit': 300,
                                             'human_other_hit': 120,
                                             'mecha_head_hit': 672,
                                             'mecha_other_hit': 560
                                             },
                                    801304: {'human_head_hit': 100,
                                             'human_other_hit': 40,
                                             'mecha_head_hit': 168,
                                             'mecha_other_hit': 140
                                             },
                                    801305: {'human_head_hit': 25,
                                             'human_other_hit': 10,
                                             'mecha_head_hit': 64,
                                             'mecha_other_hit': 54
                                             },
                                    801306: {'human_head_hit': 125,
                                             'human_other_hit': 50,
                                             'mecha_head_hit': 194,
                                             'mecha_other_hit': 162
                                             },
                                    801307: {'human_head_hit': 225,
                                             'human_other_hit': 90,
                                             'mecha_head_hit': 524,
                                             'mecha_other_hit': 437
                                             },
                                    801308: {'human_head_hit': 300,
                                             'human_other_hit': 120,
                                             'mecha_head_hit': 725,
                                             'mecha_other_hit': 604
                                             },
                                    801401: {'human_head_hit': 50,
                                             'human_other_hit': 20,
                                             'mecha_head_hit': 43,
                                             'mecha_other_hit': 36
                                             },
                                    801501: {'human_head_hit': 150,
                                             'human_other_hit': 60,
                                             'mecha_head_hit': 172,
                                             'mecha_other_hit': 144
                                             },
                                    801502: {'human_head_hit': 200,
                                             'human_other_hit': 80,
                                             'mecha_head_hit': 564,
                                             'mecha_other_hit': 470
                                             },
                                    890301: {'human_head_hit': 150,
                                             'human_other_hit': 60,
                                             'mecha_head_hit': 216,
                                             'mecha_other_hit': 180
                                             },
                                    890401: {'human_head_hit': 30,
                                             'human_other_hit': 12,
                                             'mecha_head_hit': 93,
                                             'mecha_other_hit': 78
                                             },
                                    890501: {'human_head_hit': 80,
                                             'human_other_hit': 32,
                                             'mecha_head_hit': 245,
                                             'mecha_other_hit': 204
                                             }
                                    },
                        'Name': '\xe6\x96\xb0\xe6\x89\x8b\xe5\x85\xb3\xe5\x8d\xa1\xe6\xad\xa6\xe5\x99\xa8\xe4\xbc\xa4\xe5\xae\xb3',
                        'QuickLink': 1
                        }
       }

    def GetData():
        return DataDict


    def GetBarrierConfig():
        return GetData()['BarrierConfig']['Content']


    def GetStageThird():
        return GetData()['StageThird']['Content']


    def GetBornPointConfig():
        return GetData()['BornPointConfig']['Content']


    def GetStageThirdEndHandler():
        return GetData()['StageThirdEndHandler']['Content']


    def GetStageFour():
        return GetData()['StageFour']['Content']


    def GetDoorConfig():
        return GetData()['DoorConfig']['Content']


    def GetStageHumanHandler():
        return GetData()['StageHumanHandler']['Content']


    def GetViewRangeConfig():
        return GetData()['ViewRangeConfig']['Content']


    def GetStageMechaHandler():
        return GetData()['StageMechaHandler']['Content']


    def GetWeaponDamage():
        return GetData()['WeaponDamage']['Content']


    def GetStageMecha():
        return GetData()['StageMecha']['Content']


    def GetStageHuman():
        return GetData()['StageHuman']['Content']