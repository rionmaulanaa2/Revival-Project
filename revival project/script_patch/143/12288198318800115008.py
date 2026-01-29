# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/human_attr_config.py
_reload_all = True
data = {'iHp': {'cKey': 'iHp',
           'cType': 'VAR_INT',
           'iPercent': 1,
           'cInit': '200',
           'iSyncType': 0,
           'cDesc': '\xe8\xa1\x80\xe9\x87\x8f'
           },
   'iStamina': {'cKey': 'iStamina',
                'cType': 'VAR_INT',
                'iPercent': 1,
                'cInit': '100',
                'iSyncType': 0,
                'cDesc': '\xe4\xbd\x93\xe5\x8a\x9b'
                },
   'iBaseMoveSpd': {'cKey': 'iBaseMoveSpd',
                    'cType': 'VAR_INT',
                    'iPercent': 1,
                    'cInit': '10',
                    'iSyncType': 0,
                    'cDesc': '\xe5\x88\x9d\xe5\xa7\x8b\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6'
                    },
   'iJumpHeight': {'cKey': 'iJumpHeight',
                   'cType': 'VAR_INT',
                   'iPercent': 1,
                   'cInit': '10',
                   'iSyncType': 0,
                   'cDesc': '\xe8\xb7\xb3\xe8\xb7\x83\xe9\xab\x98\xe5\xba\xa6'
                   },
   'iBaseCapacity': {'cKey': 'iBaseCapacity',
                     'cType': 'VAR_INT',
                     'iPercent': 1,
                     'cInit': '20',
                     'iSyncType': 0,
                     'cDesc': '\xe5\x88\x9d\xe5\xa7\x8b\xe8\xb4\x9f\xe9\x87\x8d'
                     },
   'fXHeadHit': {'cKey': 'fXHeadHit',
                 'cType': 'VAR_FLOAT',
                 'iPercent': 1,
                 'cInit': '2.5',
                 'iSyncType': 0,
                 'cDesc': '\xe5\xa4\xb4\xe9\x83\xa8\xe4\xbc\xa4\xe5\xae\xb3\xe5\x80\x8d\xe6\x95\xb0'
                 },
   'fXBodyHit': {'cKey': 'fXBodyHit',
                 'cType': 'VAR_FLOAT',
                 'iPercent': 1,
                 'cInit': '1.00',
                 'iSyncType': 0,
                 'cDesc': '\xe8\xba\xab\xe4\xbd\x93\xe4\xbc\xa4\xe5\xae\xb3\xe5\x80\x8d\xe6\x95\xb0'
                 },
   'fXLimbHit': {'cKey': 'fXLimbHit',
                 'cType': 'VAR_FLOAT',
                 'iPercent': 1,
                 'cInit': '1.00',
                 'iSyncType': 0,
                 'cDesc': '\xe5\x9b\x9b\xe8\x82\xa2\xe4\xbc\xa4\xe5\xae\xb3\xe5\x80\x8d\xe6\x95\xb0'
                 },
   'fHealTime': {'cKey': 'fHealTime',
                 'cType': 'VAR_FLOAT',
                 'iPercent': 1,
                 'cInit': '15',
                 'iSyncType': 0,
                 'cDesc': '\xe8\x84\xb1\xe6\x88\x98\xe6\x81\xa2\xe5\xa4\x8d\xe6\x97\xb6\xe9\x97\xb4'
                 },
   'fHealInterval': {'cKey': 'fHealInterval',
                     'cType': 'VAR_FLOAT',
                     'iPercent': 1,
                     'cInit': '0.5',
                     'iSyncType': 0,
                     'cDesc': '\xe8\xa1\x80\xe9\x87\x8f\xe6\x81\xa2\xe5\xa4\x8d\xe9\x97\xb4\xe9\x9a\x94'
                     },
   'iHealHp': {'cKey': 'iHealHp',
               'cType': 'VAR_INT',
               'iPercent': 1,
               'cInit': '10',
               'iSyncType': 0,
               'cDesc': '\xe8\xa1\x80\xe9\x87\x8f\xe6\x81\xa2\xe5\xa4\x8d\xe9\x87\x8f'
               },
   'fHealTimeFactor': {'cKey': 'fHealTimeFactor',
                       'cType': 'VAR_FLOAT',
                       'iPercent': 1,
                       'cInit': '0',
                       'iSyncType': 0,
                       'cDesc': '\xe8\x84\xb1\xe6\x88\x98\xe8\xa1\x80\xe9\x87\x8f\xe6\x81\xa2\xe5\xa4\x8d\xe6\x97\xb6\xe9\x97\xb4\xe5\x8a\xa0\xe6\x88\x90'
                       },
   'iHealHpFactor': {'cKey': 'iHealHpFactor',
                     'cType': 'VAR_FLOAT',
                     'iPercent': 1,
                     'cInit': '0',
                     'iSyncType': 0,
                     'cDesc': '\xe8\x84\xb1\xe6\x88\x98\xe8\xa1\x80\xe9\x87\x8f\xe6\x81\xa2\xe5\xa4\x8d\xe9\x87\x8f\xe5\x8a\xa0\xe6\x88\x90'
                     },
   'fDmgReduce': {'cKey': 'fDmgReduce',
                  'cType': 'VAR_FLOAT',
                  'iPercent': 1,
                  'cInit': '0',
                  'iSyncType': 0,
                  'cDesc': '\xe4\xbc\xa4\xe5\xae\xb3\xe5\x87\x8f\xe5\x85\x8d'
                  },
   'fMeleeReduce': {'cKey': 'fMeleeReduce',
                    'cType': 'VAR_FLOAT',
                    'iPercent': 1,
                    'cInit': '0',
                    'iSyncType': 0,
                    'cDesc': '\xe8\xbf\x91\xe6\x88\x98\xe4\xbc\xa4\xe5\xae\xb3\xe5\x87\x8f\xe5\x85\x8d'
                    },
   'mpSpecDmgReduce': {'cKey': 'mpSpecDmgReduce',
                       'cType': 'VAR_FLOAT',
                       'iPercent': 1,
                       'cInit': '0',
                       'iSyncType': 0,
                       'cDesc': '\xe7\x89\xb9\xe6\xae\x8a\xe4\xbc\xa4\xe5\xae\xb3\xe5\x87\x8f\xe5\x85\x8d'
                       },
   'mpPartDmgReduce': {'cKey': 'mpPartDmgReduce',
                       'cType': 'VAR_FLOAT',
                       'iPercent': 1,
                       'cInit': '0',
                       'iSyncType': 0,
                       'cDesc': '\xe9\x83\xa8\xe4\xbd\x8d\xe4\xbc\xa4\xe5\xae\xb3\xe5\x87\x8f\xe5\x85\x8d'
                       },
   'fSpdRate': {'cKey': 'fSpdRate',
                'cType': 'VAR_FLOAT',
                'iPercent': 1,
                'cInit': '0',
                'iSyncType': 0,
                'cDesc': '\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                },
   'fMechaReduce': {'cKey': 'fMechaReduce',
                    'cType': 'VAR_FLOAT',
                    'iPercent': 1,
                    'cInit': '0',
                    'iSyncType': 0,
                    'cDesc': '\xe6\x9c\xba\xe7\x94\xb2\xe5\x87\x8f\xe4\xbc\xa4'
                    },
   'human_speed_up_factor': {'cKey': 'human_speed_up_factor',
                             'cType': 'VAR_FLOAT',
                             'iPercent': 1,
                             'cInit': '0',
                             'iSyncType': 0,
                             'cDesc': '\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                             },
   'roll_cost_factor': {'cKey': 'roll_cost_factor',
                        'cType': 'VAR_FLOAT',
                        'iPercent': 1,
                        'cInit': '0',
                        'iSyncType': 1,
                        'cDesc': '\xe7\xbf\xbb\xe6\xbb\x9a\xe6\xb6\x88\xe8\x80\x97\xe5\x8a\xa0\xe6\x88\x90'
                        },
   'roll_inc_up': {'cKey': 'roll_inc_up',
                   'cType': 'VAR_FLOAT',
                   'iPercent': 1,
                   'cInit': '0',
                   'iSyncType': 1,
                   'cDesc': '\xe7\xbf\xbb\xe6\xbb\x9a\xe6\xaf\x8f\xe7\xa7\x92\xe6\x81\xa2\xe5\xa4\x8d\xe5\x8a\xa0\xe6\x88\x90'
                   },
   'load_switch_gun_force_walk': {'cKey': 'load_switch_gun_force_walk',
                                  'cType': 'VAR_INT',
                                  'iPercent': 1,
                                  'cInit': '1',
                                  'iSyncType': 1,
                                  'cDesc': '\xe6\x8d\xa2\xe5\xad\x90\xe5\xbc\xb9\xe5\x88\x87\xe6\x9e\xaa\xe8\xb7\x91\xe6\xad\xa5\xe7\x8a\xb6\xe6\x80\x81\xe5\x88\x99\xe5\xbc\xba\xe5\x88\xb6\xe8\xa1\x8c\xe8\xb5\xb0'
                                  },
   'box_check_dis_factor': {'cKey': 'box_check_dis_factor',
                            'cType': 'VAR_FLOAT',
                            'iPercent': 1,
                            'cInit': '0',
                            'iSyncType': 1,
                            'cDesc': '\xe7\x9b\x92\xe5\xad\x90\xe6\x8e\xa2\xe6\xb5\x8b\xe8\xb7\x9d\xe7\xa6\xbb\xe5\x8a\xa0\xe6\x88\x90'
                            },
   'item_type_sing_time_factor_9': {'cKey': 'item_type_sing_time_factor_9',
                                    'cType': 'VAR_FLOAT',
                                    'iPercent': 1,
                                    'cInit': '0',
                                    'iSyncType': 1,
                                    'cDesc': '\xe7\x89\xa9\xe5\x93\x81\xe7\xb1\xbb\xe5\x9e\x8b9\xe4\xbd\xbf\xe7\x94\xa8\xe7\x89\xa9\xe5\x93\x81\xe6\x97\xb6\xe9\x97\xb4\xe5\x8a\xa0\xe6\x88\x90'
                                    },
   'weapon_take_time_factor': {'cKey': 'weapon_take_time_factor',
                               'cType': 'VAR_FLOAT',
                               'iPercent': 1,
                               'cInit': '0',
                               'iSyncType': 1,
                               'cDesc': '\xe4\xba\xba\xe7\x89\xa9\xe6\xad\xa6\xe5\x99\xa8\xe6\x8b\xbf\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4\xe5\x8a\xa0\xe6\x88\x90'
                               },
   'weapon_reload_speed_factor_human_all': {'cKey': 'weapon_reload_speed_factor_human_all',
                                            'cType': 'VAR_FLOAT',
                                            'iPercent': 1,
                                            'cInit': '0',
                                            'iSyncType': 1,
                                            'cDesc': '\xe4\xba\xba\xe7\x89\xa9\xe6\x89\x80\xe6\x9c\x89\xe6\xad\xa6\xe5\x99\xa8\xe7\xb1\xbb\xe5\x9e\x8b\xe7\x9a\x84\xe6\x8d\xa2\xe5\xbc\xb9\xe6\x97\xb6\xe9\x97\xb4\xe5\x8a\xa0\xe6\x88\x90'
                                            },
   'weapon_reload_speed_factor_6': {'cKey': 'weapon_reload_speed_factor_6',
                                    'cType': 'VAR_FLOAT',
                                    'iPercent': 1,
                                    'cInit': '0',
                                    'iSyncType': 1,
                                    'cDesc': '\xe6\xad\xa6\xe5\x99\xa8\xe7\xb1\xbb\xe5\x9e\x8b6\xe6\x8d\xa2\xe5\xbc\xb9\xe6\x97\xb6\xe9\x97\xb4\xe5\x8a\xa0\xe6\x88\x90'
                                    },
   'weapon_reload_speed_factor_12': {'cKey': 'weapon_reload_speed_factor_12',
                                     'cType': 'VAR_FLOAT',
                                     'iPercent': 1,
                                     'cInit': '0',
                                     'iSyncType': 1,
                                     'cDesc': '\xe6\xad\xa6\xe5\x99\xa8\xe7\xb1\xbb\xe5\x9e\x8b12\xe6\x8d\xa2\xe5\xbc\xb9\xe6\x97\xb6\xe9\x97\xb4\xe5\x8a\xa0\xe6\x88\x90'
                                     },
   'weapon_reload_speed_factor_14': {'cKey': 'weapon_reload_speed_factor_14',
                                     'cType': 'VAR_FLOAT',
                                     'iPercent': 1,
                                     'cInit': '0',
                                     'iSyncType': 1,
                                     'cDesc': '\xe6\xad\xa6\xe5\x99\xa8\xe7\xb1\xbb\xe5\x9e\x8b14\xe6\x8d\xa2\xe5\xbc\xb9\xe6\x97\xb6\xe9\x97\xb4\xe5\x8a\xa0\xe6\x88\x90'
                                     },
   'parachute_acc_factor': {'cKey': 'parachute_acc_factor',
                            'cType': 'VAR_FLOAT',
                            'iPercent': 1,
                            'cInit': '0',
                            'iSyncType': 1,
                            'cDesc': '\xe4\xba\xba\xe7\x89\xa9\xe8\xb7\xb3\xe4\xbc\x9e\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                            },
   'parachute_max_spd_factor': {'cKey': 'parachute_max_spd_factor',
                                'cType': 'VAR_FLOAT',
                                'iPercent': 1,
                                'cInit': '0',
                                'iSyncType': 1,
                                'cDesc': '\xe4\xba\xba\xe7\x89\xa9\xe8\xb7\xb3\xe4\xbc\x9e\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                                },
   'human_cure_item_add_factor': {'cKey': 'human_cure_item_add_factor',
                                  'cType': 'VAR_FLOAT',
                                  'iPercent': 1,
                                  'cInit': '0',
                                  'iSyncType': 1,
                                  'cDesc': '\xe4\xba\xba\xe7\x89\xa9\xe5\x9b\x9e\xe8\xa1\x80\xe9\x81\x93\xe5\x85\xb7\xe5\x8a\xa0\xe6\x88\x90'
                                  },
   'fDriverLevelStarPointFactor': {'cKey': 'fDriverLevelStarPointFactor',
                                   'cType': 'VAR_FLOAT',
                                   'iPercent': 1,
                                   'cInit': '1.00',
                                   'iSyncType': 1,
                                   'cDesc': '\xe9\xa9\xbe\xe9\xa9\xb6\xe5\x91\x98ACE\xe5\x8b\x8b\xe7\xab\xa0\xe5\x8d\x87\xe7\xba\xa7\xe5\x8a\xa0\xe6\x88\x90'
                                   },
   'fRollReloadSpeedFactor': {'cKey': 'fRollReloadSpeedFactor',
                              'cType': 'VAR_FLOAT',
                              'iPercent': 1,
                              'cInit': '0',
                              'iSyncType': 1,
                              'cDesc': '\xe9\xa9\xbe\xe9\xa9\xb6\xe5\x91\x98\xe6\xbb\x9a\xe5\x8a\xa8\xe6\x97\xb6\xe4\xb8\x8a\xe5\xbc\xb9\xe9\x80\x9f\xe7\x8e\x87'
                              },
   'iFataShieldRecoverLife': {'cKey': 'iFataShieldRecoverLife',
                              'cType': 'VAR_INT',
                              'iPercent': 1,
                              'cInit': '0',
                              'iSyncType': 0,
                              'cDesc': '\xe6\x9c\xab\xe6\x97\xa5\xe6\x8a\xa4\xe6\x89\x8b\xe5\xa2\x9e\xe5\x8a\xa0\xe8\xa1\x80\xe9\x87\x8f'
                              },
   'iFataShieldRecoverPerTime': {'cKey': 'iFataShieldRecoverPerTime',
                                 'cType': 'VAR_INT',
                                 'iPercent': 1,
                                 'cInit': '0',
                                 'iSyncType': 0,
                                 'cDesc': '\xe6\x9c\xab\xe6\x97\xa5\xe6\x8a\xa4\xe6\x89\x8b\xe6\xaf\x8f\xe6\xac\xa1\xe5\xa2\x9e\xe5\x8a\xa0\xe8\xa1\x80\xe9\x87\x8f'
                                 },
   'iFataShieldRecoverInterval': {'cKey': 'iFataShieldRecoverInterval',
                                  'cType': 'VAR_INT',
                                  'iPercent': 1,
                                  'cInit': '0',
                                  'iSyncType': 0,
                                  'cDesc': '\xe6\x9c\xab\xe6\x97\xa5\xe6\x8a\xa4\xe6\x89\x8b\xe5\x9b\x9e\xe8\xa1\x80\xe8\xa7\xa6\xe5\x8f\x91\xe9\x97\xb4\xe9\x9a\x94'
                                  },
   'iFataShieldRecoverCD': {'cKey': 'iFataShieldRecoverCD',
                            'cType': 'VAR_INT',
                            'iPercent': 1,
                            'cInit': '0',
                            'iSyncType': 0,
                            'cDesc': '\xe6\x9c\xab\xe6\x97\xa5\xe6\x8a\xa4\xe6\x89\x8bCD\xe6\x97\xb6\xe9\x97\xb4'
                            },
   'iFataShieldTriggerMinLife': {'cKey': 'iFataShieldTriggerMinLife',
                                 'cType': 'VAR_INT',
                                 'iPercent': 1,
                                 'cInit': '0',
                                 'iSyncType': 0,
                                 'cDesc': '\xe6\x9c\xab\xe6\x97\xa5\xe6\x8a\xa4\xe6\x89\x8b\xe8\xa7\xa6\xe5\x8f\x91\xe8\xa1\x80\xe9\x87\x8f'
                                 },
   'fReduceHurtOfPoison': {'cKey': 'fReduceHurtOfPoison',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '0',
                           'iSyncType': 0,
                           'cDesc': '\xe4\xba\xba\xe7\x89\xa9\xe6\x94\xb6\xe5\x88\xb0\xe6\xaf\x92\xe5\x9c\x88\xe4\xbc\xa4\xe5\xae\xb3\xe5\x87\x8f\xe5\x85\x8d\xe6\xaf\x94\xe4\xbe\x8b'
                           },
   'fReduceHurtOfMonster': {'cKey': 'fReduceHurtOfMonster',
                            'cType': 'VAR_FLOAT',
                            'iPercent': 1,
                            'cInit': '0',
                            'iSyncType': 0,
                            'cDesc': '\xe4\xba\xba\xe7\x89\xa9\xe6\x94\xb6\xe5\x88\xb0\xe9\x87\x8e\xe6\x80\xaa\xe4\xbc\xa4\xe5\xae\xb3\xe5\x87\x8f\xe5\x85\x8d\xe6\xaf\x94\xe4\xbe\x8b'
                            },
   'fExtraJumpFactor': {'cKey': 'fExtraJumpFactor',
                        'cType': 'VAR_FLOAT',
                        'iPercent': 1,
                        'cInit': '0',
                        'iSyncType': 1,
                        'cDesc': '\xe4\xba\xba\xe7\x89\xa9\xe9\xa2\x9d\xe5\xa4\x96\xe8\xb7\xb3\xe8\xb7\x83\xe6\xac\xa1\xe6\x95\xb0\xe7\x9a\x84\xe8\xb7\xb3\xe8\xb7\x83\xe5\xb9\x85\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                        },
   'fExtraRushDistFactor': {'cKey': 'fExtraRushDistFactor',
                            'cType': 'VAR_FLOAT',
                            'iPercent': 1,
                            'cInit': '0',
                            'iSyncType': 1,
                            'cDesc': '\xe4\xba\xba\xe7\x89\xa9\xe9\xa2\x9d\xe5\xa4\x96\xe5\x86\xb2\xe5\x88\xba\xe6\xac\xa1\xe6\x95\xb0\xe7\x9a\x84\xe5\xb9\x85\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                            },
   'fGiftMechaEnemyDebuffDurationAddFactor': {'cKey': 'fGiftMechaEnemyDebuffDurationAddFactor',
                                              'cType': 'VAR_FLOAT',
                                              'iPercent': 1,
                                              'cInit': '0',
                                              'iSyncType': 0,
                                              'cDesc': '\xe5\xa4\xa9\xe8\xb5\x8b-\xe6\x9c\xba\xe7\x94\xb2\xe7\xbb\x99\xe6\x95\x8c\xe4\xba\xba\xe5\x8a\xa0\xe7\x9a\x84\xe8\xb4\x9f\xe9\x9d\xa2BUFF\xe5\xbb\xb6\xe6\x97\xb6\xe5\x8a\xa0\xe6\x88\x90'
                                              },
   'fGiftMechaFightFactorAddOnHurt': {'cKey': 'fGiftMechaFightFactorAddOnHurt',
                                      'cType': 'VAR_FLOAT',
                                      'iPercent': 1,
                                      'cInit': '0',
                                      'iSyncType': 0,
                                      'cDesc': '\xe6\x9c\xba\xe7\x94\xb2\xe5\xa4\xa9\xe8\xb5\x8b-\xe6\x8d\x9f\xe5\xa4\xb1\xe8\x80\x90\xe4\xb9\x85\xe6\x97\xb6\xe6\x88\x98\xe5\x8a\x9b\xe7\xb3\xbb\xe6\x95\xb0\xe5\x8a\xa0\xe6\x88\x90'
                                      },
   'fGiftMechaFightFactorPercentOnHurt': {'cKey': 'fGiftMechaFightFactorPercentOnHurt',
                                          'cType': 'VAR_FLOAT',
                                          'iPercent': 1,
                                          'cInit': '0',
                                          'iSyncType': 0,
                                          'cDesc': '\xe6\x9c\xba\xe7\x94\xb2\xe5\xa4\xa9\xe8\xb5\x8b-\xe6\x8d\x9f\xe5\xa4\xb1\xe8\x80\x90\xe4\xb9\x85\xe6\x97\xb6\xe6\x88\x98\xe5\x8a\x9b\xe5\x8a\xa0\xe6\x88\x90\xe8\x80\x90\xe4\xb9\x85\xe7\x99\xbe\xe5\x88\x86\xe6\xaf\x94'
                                          },
   'iCostRatioFactor': {'cKey': 'iCostRatioFactor',
                        'cType': 'VAR_FLOAT',
                        'iPercent': 1,
                        'cInit': '0',
                        'iSyncType': 1,
                        'cDesc': '\xe8\x80\x97\xe5\xbc\xb9\xe7\xb3\xbb\xe6\x95\xb0'
                        },
   'item_sing_time_factor': {'cKey': 'item_sing_time_factor',
                             'cType': 'VAR_FLOAT',
                             'iPercent': 1,
                             'cInit': '0',
                             'iSyncType': 1,
                             'cDesc': '\xe4\xbd\xbf\xe7\x94\xa8\xe7\x89\xa9\xe5\x93\x81\xe5\x90\x9f\xe5\x94\xb1\xe6\x97\xb6\xe9\x97\xb4\xe5\x8a\xa0\xe6\x88\x90'
                             },
   'item_type_sing_time_factor_6': {'cKey': 'item_type_sing_time_factor_6',
                                    'cType': 'VAR_FLOAT',
                                    'iPercent': 1,
                                    'cInit': '0',
                                    'iSyncType': 1,
                                    'cDesc': '\xe7\x89\xa9\xe5\x93\x81\xe7\xb1\xbb\xe5\x9e\x8b6\xe4\xbd\xbf\xe7\x94\xa8\xe7\x89\xa9\xe5\x93\x81\xe6\x97\xb6\xe9\x97\xb4\xe5\x8a\xa0\xe6\x88\x90'
                                    },
   'rescue_time_factor': {'cKey': 'rescue_time_factor',
                          'cType': 'VAR_FLOAT',
                          'iPercent': 1,
                          'cInit': '0',
                          'iSyncType': 1,
                          'cDesc': '\xe6\x95\x91\xe6\x8f\xb4\xe6\x97\xb6\xe9\x97\xb4\xe5\x8a\xa0\xe6\x88\x90'
                          },
   'recall_mecha_time_factor': {'cKey': 'recall_mecha_time_factor',
                                'cType': 'VAR_FLOAT',
                                'iPercent': 1,
                                'cInit': '0',
                                'iSyncType': 0,
                                'cDesc': '\xe9\x87\x8d\xe7\x94\x9f\xe5\x8f\xac\xe5\x94\xa4\xe6\x9c\xba\xe7\x94\xb2\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                                },
   'call_mecha_time_factor': {'cKey': 'call_mecha_time_factor',
                              'cType': 'VAR_FLOAT',
                              'iPercent': 1,
                              'cInit': '0',
                              'iSyncType': 0,
                              'cDesc': '\xe9\xa6\x96\xe6\xac\xa1\xe5\x8f\xac\xe5\x94\xa4\xe6\x9c\xba\xe7\x94\xb2\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                              },
   'recall_mecha_on_leave_time_factor': {'cKey': 'recall_mecha_on_leave_time_factor',
                                         'cType': 'VAR_FLOAT',
                                         'iPercent': 1,
                                         'cInit': '0',
                                         'iSyncType': 0,
                                         'cDesc': '\xe4\xb8\xbb\xe5\x8a\xa8\xe7\xa6\xbb\xe5\xbc\x80\xe5\x90\x8e\xe5\x8f\xac\xe5\x94\xa4\xe6\x9c\xba\xe7\x94\xb2\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                                         },
   'listen_range_factor': {'cKey': 'listen_range_factor',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '0',
                           'iSyncType': 1,
                           'cDesc': '\xe5\xa3\xb0\xe9\x9f\xb3\xe4\xbe\xa6\xe5\x90\xac\xe8\x8c\x83\xe5\x9b\xb4\xe5\x8a\xa0\xe6\x88\x90\xef\xbc\x88\xe6\x94\xbe\xe5\x9c\xa8\xe4\xba\xba\xe8\xbf\x99\xe9\x87\x8c\xe4\xbd\xbf\xe7\x94\xa8\xe6\xaf\x94\xe8\xbe\x83\xe6\x96\xb9\xe4\xbe\xbf\xef\xbc\x89'
                           },
   'eject_height_factor': {'cKey': 'eject_height_factor',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '1',
                           'iSyncType': 1,
                           'cDesc': '\xe6\x9c\xba\xe7\x94\xb2\xe7\x88\x86\xe7\x82\xb8\xe5\x90\x8e\xe5\xbc\xb9\xe5\xb0\x84\xe9\xab\x98\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                           },
   'fGiftAddMechaHurtAllWeapon': {'cKey': 'fGiftAddMechaHurtAllWeapon',
                                  'cType': 'VAR_FLOAT',
                                  'iPercent': 1,
                                  'cInit': '0',
                                  'iSyncType': 0,
                                  'cDesc': '\xe4\xba\xba\xe7\x89\xa9\xe5\xa4\xa9\xe8\xb5\x8b-\xe6\x89\x80\xe6\x9c\x89\xe6\xad\xa6\xe5\x99\xa8\xe7\xbb\x99\xe6\x9c\xba\xe7\x94\xb2\xe4\xbc\xa4\xe5\xae\xb3\xe5\x8a\xa0\xe6\x88\x90'
                                  },
   'fGiftReduceMechaHurtToHuman': {'cKey': 'fGiftReduceMechaHurtToHuman',
                                   'cType': 'VAR_FLOAT',
                                   'iPercent': 1,
                                   'cInit': '0',
                                   'iSyncType': 0,
                                   'cDesc': '\xe4\xba\xba\xe7\x89\xa9\xe5\xa4\xa9\xe8\xb5\x8b-\xe5\x87\x8f\xe5\xb0\x91\xe6\x9c\xba\xe7\x94\xb2\xe7\xbb\x99\xe4\xba\xba\xe7\x89\xa9\xe4\xbc\xa4\xe5\xae\xb3'
                                   },
   'iSignal': {'cKey': 'iSignal',
               'cType': 'VAR_INT',
               'iPercent': 1,
               'cInit': '200',
               'iSyncType': 0,
               'cDesc': '\xe4\xbf\xa1\xe5\x8f\xb7\xe5\x80\xbc\xe5\x88\x9d\xe5\xa7\x8b\xe5\x80\xbc'
               },
   'fSignalBelowToExtraHurt': {'cKey': 'fSignalBelowToExtraHurt',
                               'cType': 'VAR_FLOAT',
                               'iPercent': 1,
                               'cInit': '0.75',
                               'iSyncType': 0,
                               'cDesc': '\xe4\xbf\xa1\xe5\x8f\xb7\xe9\x87\x8f\xe5\xb0\x8f\xe4\xba\x8e\xe8\xaf\xa5\xe5\x80\xbc\xe6\x97\xb6\xe9\x80\xa0\xe6\x88\x90\xe9\xa2\x9d\xe5\xa4\x96\xe4\xbc\xa4\xe5\xae\xb3'
                               },
   'fSignalExtraHurtFactor': {'cKey': 'fSignalExtraHurtFactor',
                              'cType': 'VAR_FLOAT',
                              'iPercent': 1,
                              'cInit': '0.67',
                              'iSyncType': 0,
                              'cDesc': '\xe4\xbf\xa1\xe5\x8f\xb7\xe9\x87\x8f\xe9\x80\xa0\xe6\x88\x90\xe9\xa2\x9d\xe5\xa4\x96\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe8\xae\xa1\xe7\xae\x97\xe7\xb3\xbb\xe6\x95\xb0'
                              },
   'iDropMechaModuleOnDie': {'cKey': 'iDropMechaModuleOnDie',
                             'cType': 'VAR_INT',
                             'iPercent': 1,
                             'cInit': '1',
                             'iSyncType': 0,
                             'cDesc': '\xe6\xad\xbb\xe4\xba\xa1\xe6\x97\xb6\xe6\x98\xaf\xe5\x90\xa6\xe6\x8e\x89\xe8\x90\xbd\xe6\xa8\xa1\xe7\xbb\x84'
                             },
   'eject_speed_factor': {'cKey': 'eject_speed_factor',
                          'cType': 'VAR_FLOAT',
                          'iPercent': 1,
                          'cInit': '0',
                          'iSyncType': 1,
                          'cDesc': '\xe6\x9c\xba\xe7\x94\xb2\xe7\x88\x86\xe7\x82\xb8\xe5\x90\x8e\xe5\xbc\xb9\xe5\xb0\x84\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                          },
   'iShowTailEffectOnMechaDie': {'cKey': 'iShowTailEffectOnMechaDie',
                                 'cType': 'VAR_INT',
                                 'iPercent': 1,
                                 'cInit': '1',
                                 'iSyncType': 2,
                                 'cDesc': '\xe6\x9c\xba\xe7\x94\xb2\xe7\x88\x86\xe7\x82\xb8\xe5\x90\x8e\xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xbe\xe7\xa4\xba\xe6\x8b\x96\xe5\xb0\xbe\xe7\x89\xb9\xe6\x95\x88'
                                 },
   'iSignalRevive': {'cKey': 'iSignalRevive',
                     'cType': 'VAR_INT',
                     'iPercent': 1,
                     'cInit': '80',
                     'iSyncType': 0,
                     'cDesc': '\xe5\xa4\x8d\xe6\xb4\xbb\xe6\x97\xb6\xe4\xbf\xa1\xe5\x8f\xb7\xe9\x87\x8f\xe5\x88\x9d\xe5\xa7\x8b\xe5\x80\xbc'
                     },
   'iHealSignal': {'cKey': 'iHealSignal',
                   'cType': 'VAR_INT',
                   'iPercent': 1,
                   'cInit': '10',
                   'iSyncType': 0,
                   'cDesc': '\xe4\xbf\xa1\xe5\x8f\xb7\xe5\x80\xbc\xe6\x81\xa2\xe5\xa4\x8d\xe9\x87\x8f'
                   },
   'iHealSignalTime': {'cKey': 'iHealSignalTime',
                       'cType': 'VAR_FLOAT',
                       'iPercent': 1,
                       'cInit': '15',
                       'iSyncType': 0,
                       'cDesc': '\xe4\xbf\xa1\xe5\x8f\xb7\xe5\x80\xbc\xe6\x81\xa2\xe5\xa4\x8d\xe6\x97\xb6\xe9\x97\xb4'
                       },
   'iHealSignalInterval': {'cKey': 'iHealSignalInterval',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '1',
                           'iSyncType': 0,
                           'cDesc': '\xe4\xbf\xa1\xe5\x8f\xb7\xe5\x80\xbc\xe6\x81\xa2\xe5\xa4\x8d\xe9\x97\xb4\xe9\x9a\x94'
                           },
   'fBeRescueTimeReduceFactor': {'cKey': 'fBeRescueTimeReduceFactor',
                                 'cType': 'VAR_FLOAT',
                                 'iPercent': 1,
                                 'cInit': '0',
                                 'iSyncType': 0,
                                 'cDesc': '\xe8\xa2\xab\xe9\x98\x9f\xe5\x8f\x8b\xe6\x95\x91\xe6\x8f\xb4\xe6\x97\xb6\xe6\x95\x91\xe6\x8f\xb4\xe6\x97\xb6\xe9\x97\xb4\xe5\x87\x8f\xe5\xb0\x91\xe7\xb3\xbb\xe6\x95\xb0'
                                 },
   'fParachuteHoriSpeedupFactor': {'cKey': 'fParachuteHoriSpeedupFactor',
                                   'cType': 'VAR_FLOAT',
                                   'iPercent': 1,
                                   'cInit': '0',
                                   'iSyncType': 1,
                                   'cDesc': '\xe7\xbb\x84\xe9\x98\x9f\xe8\xb7\xb3\xe4\xbc\x9e\xe6\x97\xb6\xe6\xa8\xaa\xe5\x90\x91\xe9\xa3\x9e\xe8\xa1\x8c\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe9\x80\x9f\xe7\xb3\xbb\xe6\x95\xb0'
                                   },
   'mecha_weapon_add_factor_by_dis_dis': {'cKey': 'mecha_weapon_add_factor_by_dis_dis',
                                          'cType': 'VAR_FLOAT',
                                          'iPercent': 1,
                                          'cInit': '0',
                                          'iSyncType': 0,
                                          'cDesc': '\xe5\xa4\xa9\xe8\xb5\x8b-\xe6\x9c\xba\xe7\x94\xb2\xe4\xb8\xbb\xe6\xad\xa6\xe5\x99\xa8\xe6\x8c\x89\xe8\xb7\x9d\xe7\xa6\xbb\xe5\xa2\x9e\xe4\xbc\xa4\xe8\xb7\x9d\xe7\xa6\xbb'
                                          },
   'mecha_weapon_add_factor_by_dis_add': {'cKey': 'mecha_weapon_add_factor_by_dis_add',
                                          'cType': 'VAR_FLOAT',
                                          'iPercent': 1,
                                          'cInit': '0',
                                          'iSyncType': 0,
                                          'cDesc': '\xe5\xa4\xa9\xe8\xb5\x8b-\xe6\x9c\xba\xe7\x94\xb2\xe4\xb8\xbb\xe6\xad\xa6\xe5\x99\xa8\xe6\x8c\x89\xe8\xb7\x9d\xe7\xa6\xbb\xe5\xa2\x9e\xe4\xbc\xa4\xe5\x9b\xa0\xe5\xad\x90'
                                          },
   'fGiftReduceSameSexHurtFactor': {'cKey': 'fGiftReduceSameSexHurtFactor',
                                    'cType': 'VAR_FLOAT',
                                    'iPercent': 1,
                                    'cInit': '0',
                                    'iSyncType': 0,
                                    'cDesc': '\xe5\xa4\xa9\xe8\xb5\x8b-\xe6\x9d\xa5\xe8\x87\xaa\xe7\x9b\xb8\xe5\x90\x8c\xe6\x80\xa7\xe5\x88\xab\xe8\xa7\x92\xe8\x89\xb2\xe7\x9a\x84\xe4\xbc\xa4\xe5\xae\xb3\xe9\x99\x8d\xe4\xbd\x8e\xe5\x9b\xa0\xe5\xad\x90'
                                    },
   'fGiftAddOpSexHurtFactor': {'cKey': 'fGiftAddOpSexHurtFactor',
                               'cType': 'VAR_FLOAT',
                               'iPercent': 1,
                               'cInit': '0',
                               'iSyncType': 0,
                               'cDesc': '\xe5\xa4\xa9\xe8\xb5\x8b-\xe5\xaf\xb9\xe7\x9b\xb8\xe5\x8f\x8d\xe6\x80\xa7\xe5\x88\xab\xe9\x80\xa0\xe6\x88\x90\xe7\x9a\x84\xe4\xbc\xa4\xe5\xae\xb3\xe5\xa2\x9e\xe5\x8a\xa0\xe5\x9b\xa0\xe5\xad\x90'
                               },
   'fAddRifleToMechaDmg': {'cKey': 'fAddRifleToMechaDmg',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '0',
                           'iSyncType': 0,
                           'cDesc': '\xe6\xad\xa5\xe6\x9e\xaa\xe5\xaf\xb9\xe6\x9c\xba\xe7\x94\xb2\xe4\xbc\xa4\xe5\xae\xb3\xe6\x8f\x90\xe5\x8d\x87'
                           },
   'fAddFullHealthDmg': {'cKey': 'fAddFullHealthDmg',
                         'cType': 'VAR_FLOAT',
                         'iPercent': 1,
                         'cInit': '0',
                         'iSyncType': 0,
                         'cDesc': '\xe6\xbb\xa1\xe8\xa1\x80\xe6\xbb\xa1\xe7\x94\xb2\xe4\xbc\xa4\xe5\xae\xb3\xe6\x8f\x90\xe5\x8d\x87'
                         },
   'fAddToMechaDmg': {'cKey': 'fAddToMechaDmg',
                      'cType': 'VAR_FLOAT',
                      'iPercent': 1,
                      'cInit': '0',
                      'iSyncType': 0,
                      'cDesc': '\xe5\xaf\xb9\xe6\x9c\xba\xe7\x94\xb2\xe4\xbc\xa4\xe5\xae\xb3\xe6\x8f\x90\xe5\x8d\x87'
                      },
   'blood_packet_cd_add': {'cKey': 'blood_packet_cd_add',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '0',
                           'iSyncType': 0,
                           'cDesc': '\xe8\xa1\x80\xe5\x8c\x85CD\xe5\x8a\xa0\xe6\x88\x90'
                           },
   'blood_packet_cd_add_sec': {'cKey': 'blood_packet_cd_add_sec',
                               'cType': 'VAR_FLOAT',
                               'iPercent': 1,
                               'cInit': '0',
                               'iSyncType': 0,
                               'cDesc': '\xe8\xa1\x80\xe5\x8c\x85CD\xe7\xa7\x92\xe6\x95\xb0\xe5\x8a\xa0\xe6\x88\x90'
                               },
   'human_common_weapon_spread_factor': {'cKey': 'human_common_weapon_spread_factor',
                                         'cType': 'VAR_FLOAT',
                                         'iPercent': 1,
                                         'cInit': '0',
                                         'iSyncType': 0,
                                         'cDesc': '\xe4\xba\xba\xe7\x89\xa9\xe6\x99\xae\xe9\x80\x9a\xe6\xad\xa6\xe5\x99\xa8\xe6\x95\xa3\xe5\xb0\x84\xe5\x80\xbc\xef\xbc\x88\xe4\xb8\x8d\xe5\xbd\xb1\xe5\x93\x8d\xe9\x95\xad\xe5\xb0\x84\xe6\x9e\xaa\xe7\xad\x89\xe7\x89\xb9\xe6\xae\x8a\xe6\xad\xa6\xe5\x99\xa8\xef\xbc\x89'
                                         },
   'boom_robot_charge_range_factor': {'cKey': 'boom_robot_charge_range_factor',
                                      'cType': 'VAR_FLOAT',
                                      'iPercent': 1,
                                      'cInit': '0',
                                      'iSyncType': 1,
                                      'cDesc': '\xe5\xa5\x87\xe5\xa5\x87\xe5\xa8\x9c\xe5\xa4\xa9\xe8\xb5\x8b\xef\xbc\x8c\xe8\x87\xaa\xe8\xb5\xb0\xe9\x9b\xb7\xe8\xbf\xbd\xe8\xb8\xaa\xe8\xb7\x9d\xe7\xa6\xbb\xe6\x8f\x90\xe5\x8d\x87'
                                      },
   'boom_robot_charge_spd_factor': {'cKey': 'boom_robot_charge_spd_factor',
                                    'cType': 'VAR_FLOAT',
                                    'iPercent': 1,
                                    'cInit': '0',
                                    'iSyncType': 1,
                                    'cDesc': '\xe5\xa5\x87\xe5\xa5\x87\xe5\xa8\x9c\xe5\xa4\xa9\xe8\xb5\x8b\xef\xbc\x8c\xe8\x87\xaa\xe8\xb5\xb0\xe9\x9b\xb7\xe8\xbf\xbd\xe8\xb8\xaa\xe9\x80\x9f\xe5\xba\xa6\xe6\x8f\x90\xe5\x8d\x87'
                                    },
   'mecha_weapon_add_factor_by_height_add': {'cKey': 'mecha_weapon_add_factor_by_height_add',
                                             'cType': 'VAR_FLOAT',
                                             'iPercent': 1,
                                             'cInit': '0',
                                             'iSyncType': 0,
                                             'cDesc': '\xe7\xbb\xb4\xe5\xa6\xae\xe8\x8e\x8e\xe5\xa4\xa9\xe8\xb5\x8b\xef\xbc\x8c\xe9\xab\x98\xe5\xba\xa6\xe5\xb7\xae\xe5\xa2\x9e\xe5\x8a\xa0\xe6\xad\xa6\xe5\x99\xa8\xe4\xbc\xa4\xe5\xae\xb3'
                                             },
   'mecha_weapon_add_factor_by_height_height': {'cKey': 'mecha_weapon_add_factor_by_height_height',
                                                'cType': 'VAR_FLOAT',
                                                'iPercent': 1,
                                                'cInit': '0',
                                                'iSyncType': 0,
                                                'cDesc': '\xe7\xbb\xb4\xe5\xa6\xae\xe8\x8e\x8e\xe5\xa4\xa9\xe8\xb5\x8b\xef\xbc\x8c\xe9\xab\x98\xe5\xba\xa6\xe5\xb7\xae\xe5\xa2\x9e\xe5\x8a\xa0\xe6\xad\xa6\xe5\x99\xa8\xe4\xbc\xa4\xe5\xae\xb3\xef\xbc\x88\xe8\xb7\x9d\xe7\xa6\xbb\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x89'
                                                },
   'mecha_weapon_add_factor_by_height_max_height': {'cKey': 'mecha_weapon_add_factor_by_height_max_height',
                                                    'cType': 'VAR_FLOAT',
                                                    'iPercent': 1,
                                                    'cInit': '0',
                                                    'iSyncType': 0,
                                                    'cDesc': '\xe7\xbb\xb4\xe5\xa6\xae\xe8\x8e\x8e\xe5\xa4\xa9\xe8\xb5\x8b\xef\xbc\x8c\xe9\xab\x98\xe5\xba\xa6\xe5\xb7\xae\xe5\xa2\x9e\xe5\x8a\xa0\xe6\xad\xa6\xe5\x99\xa8\xe4\xbc\xa4\xe5\xae\xb3\xef\xbc\x88\xe6\x9c\x80\xe5\xa4\xa7\xe8\xb7\x9d\xe7\xa6\xbb\xef\xbc\x89'
                                                    },
   'mecha_call_inc_rate': {'cKey': 'mecha_call_inc_rate',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '0',
                           'iSyncType': 0,
                           'cDesc': '\xe6\xac\xa7\xe7\x8f\x80\xe5\xa4\xa9\xe8\xb5\x8b\xef\xbc\x8c\xe5\xa2\x9e\xe5\x8a\xa0\xe6\x9c\xba\xe7\x94\xb2\xe5\x8f\xac\xe5\x94\xa4\xe9\x80\x9f\xe5\xba\xa6'
                           },
   'pick_range_factor': {'cKey': 'pick_range_factor',
                         'cType': 'VAR_FLOAT',
                         'iPercent': 1,
                         'cInit': '0',
                         'iSyncType': 1,
                         'cDesc': '\xe6\x8b\xbe\xe5\x8f\x96\xe8\x8c\x83\xe5\x9b\xb4\xe5\x8a\xa0\xe6\x88\x90'
                         },
   'mecha_last_shoot_dmg_factor': {'cKey': 'mecha_last_shoot_dmg_factor',
                                   'cType': 'VAR_FLOAT',
                                   'iPercent': 1,
                                   'cInit': '0',
                                   'iSyncType': 0,
                                   'cDesc': '\xe6\x9c\x80\xe5\x90\x8e\xe4\xb8\x80\xe5\x8f\x91\xe5\xad\x90\xe5\xbc\xb9\xe4\xbc\xa4\xe5\xae\xb3\xe5\x8a\xa0\xe6\x88\x90'
                                   },
   'affect_radius_add': {'cKey': 'affect_radius_add',
                         'cType': 'VAR_FLOAT',
                         'iPercent': 0,
                         'cInit': '0',
                         'iSyncType': 1,
                         'cDesc': '\xe7\x88\x86\xe7\x82\xb8\xe7\x89\xa9\xe5\xbd\xb1\xe5\x93\x8d\xe8\x8c\x83\xe5\x9b\xb4\xe5\x8a\xa0\xe6\x88\x90',
                         'fExtremum': 5
                         },
   'affect_radius_factor': {'cKey': 'affect_radius_factor',
                            'cType': 'VAR_FLOAT',
                            'iPercent': 1,
                            'cInit': '0',
                            'iSyncType': 1,
                            'cDesc': '\xe7\x88\x86\xe7\x82\xb8\xe7\x89\xa9\xe5\xbd\xb1\xe5\x93\x8d\xe8\x8c\x83\xe5\x9b\xb4\xe5\x8a\xa0\xe6\x88\x90',
                            'fExtremum': 2
                            },
   'col_radius': {'cKey': 'col_radius',
                  'cType': 'VAR_FLOAT',
                  'iPercent': 1,
                  'cInit': '0',
                  'iSyncType': 1,
                  'cDesc': '\xe7\x88\x86\xe7\x82\xb8\xe7\x89\xa9\xe7\xa2\xb0\xe6\x92\x9e\xe4\xbd\x93\xe5\xa4\xa7\xe5\xb0\x8f\xe5\x8a\xa0\xe6\x88\x90'
                  },
   'base_power_add': {'cKey': 'base_power_add',
                      'cType': 'VAR_INT',
                      'iPercent': 0,
                      'cInit': '0',
                      'iSyncType': 0,
                      'cDesc': '\xe5\x9f\xba\xe7\xa1\x80\xe4\xbc\xa4\xe5\xae\xb3\xe5\xa2\x9e\xe9\x87\x8f'
                      },
   'base_power_factor': {'cKey': 'base_power_factor',
                         'cType': 'VAR_FLOAT',
                         'iPercent': 1,
                         'cInit': '0',
                         'iSyncType': 0,
                         'cDesc': '\xe5\x9f\xba\xe7\xa1\x80\xe4\xbc\xa4\xe5\xae\xb3\xe5\x8a\xa0\xe6\x88\x90',
                         'fExtremum': 3
                         },
   'shield_dmg_factor': {'cKey': 'shield_dmg_factor',
                         'cType': 'VAR_FLOAT',
                         'iPercent': 1,
                         'cInit': '0',
                         'iSyncType': 0,
                         'cDesc': '\xe6\x8a\xa4\xe7\x9b\xbe\xe4\xbc\xa4\xe5\xae\xb3\xe5\x8a\xa0\xe6\x88\x90'
                         },
   'max_hp_factor': {'cKey': 'max_hp_factor',
                     'cType': 'VAR_FLOAT',
                     'iPercent': 1,
                     'cInit': '0',
                     'iSyncType': 0,
                     'cDesc': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\xa1\x80\xe9\x87\x8f\xe5\x8a\xa0\xe6\x88\x90'
                     },
   'speed_up_factor': {'cKey': 'speed_up_factor',
                       'cType': 'VAR_FLOAT',
                       'iPercent': 1,
                       'cInit': '0',
                       'iSyncType': 1,
                       'cDesc': '\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                       },
   'dist_damage_factor': {'cKey': 'dist_damage_factor',
                          'cType': 'VAR_FLOAT',
                          'iPercent': 1,
                          'cInit': '0',
                          'iSyncType': 0,
                          'cDesc': '\xe4\xbc\xa4\xe5\xae\xb3\xe8\xae\xa1\xe7\xae\x97\xe7\x9a\x84\xe8\xa1\xb0\xe5\x87\x8f\xe8\xb7\x9d\xe7\xa6\xbb\xe5\x8a\xa0\xe6\x88\x90\xef\xbc\x8c\xe7\x88\x86\xe7\x82\xb8\xe8\xb7\x9d\xe7\xa6\xbb\xef\xbc\x88\xe7\x9b\xb8\xe5\xaf\xb9\xe7\x88\x86\xe7\x82\xb8\xe7\x82\xb9\xef\xbc\x89'
                          },
   'max_hp_add': {'cKey': 'max_hp_add',
                  'cType': 'VAR_INT',
                  'iPercent': 1,
                  'cInit': '0',
                  'iSyncType': 0,
                  'cDesc': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\xa1\x80\xe9\x87\x8f\xe5\x9b\xba\xe5\xae\x9a\xe5\x8a\xa0\xe6\x88\x90'
                  },
   'dist_shoot_damage_factor': {'cKey': 'dist_shoot_damage_factor',
                                'cType': 'VAR_FLOAT',
                                'iPercent': 1,
                                'cInit': '0',
                                'iSyncType': 0,
                                'cDesc': '\xe4\xbc\xa4\xe5\xae\xb3\xe8\xae\xa1\xe7\xae\x97\xe7\x9a\x84\xe8\xa1\xb0\xe5\x87\x8f\xe8\xb7\x9d\xe7\xa6\xbb\xe5\x8a\xa0\xe6\x88\x90\xef\xbc\x8c\xe5\xb0\x84\xe5\x87\xbb\xe8\xb7\x9d\xe7\xa6\xbb\xef\xbc\x88\xe7\x9b\xb8\xe5\xaf\xb9\xe5\xb0\x84\xe5\x87\xba\xe7\x82\xb9\xef\xbc\x89'
                                },
   'reload_speed_factor': {'cKey': 'reload_speed_factor',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '0',
                           'iSyncType': 1,
                           'cDesc': '\xe6\x8d\xa2\xe5\xbc\xb9\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                           },
   'reload_speed_factor_pos_1': {'cKey': 'reload_speed_factor_pos_1',
                                 'cType': 'VAR_FLOAT',
                                 'iPercent': 1,
                                 'cInit': '0',
                                 'iSyncType': 1,
                                 'cDesc': '\xe6\x8d\xa2\xe5\xbc\xb9\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                                 },
   'reload_speed_factor_pos_2': {'cKey': 'reload_speed_factor_pos_2',
                                 'cType': 'VAR_FLOAT',
                                 'iPercent': 1,
                                 'cInit': '0',
                                 'iSyncType': 1,
                                 'cDesc': '\xe6\x8d\xa2\xe5\xbc\xb9\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                                 },
   'reload_speed_factor_pos_3': {'cKey': 'reload_speed_factor_pos_3',
                                 'cType': 'VAR_FLOAT',
                                 'iPercent': 1,
                                 'cInit': '0',
                                 'iSyncType': 1,
                                 'cDesc': '\xe6\x8d\xa2\xe5\xbc\xb9\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                                 },
   'reload_speed_factor_pos_4': {'cKey': 'reload_speed_factor_pos_4',
                                 'cType': 'VAR_FLOAT',
                                 'iPercent': 1,
                                 'cInit': '0',
                                 'iSyncType': 1,
                                 'cDesc': '\xe6\x8d\xa2\xe5\xbc\xb9\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                                 },
   'reload_speed_factor_pos_5': {'cKey': 'reload_speed_factor_pos_5',
                                 'cType': 'VAR_FLOAT',
                                 'iPercent': 1,
                                 'cInit': '0',
                                 'iSyncType': 1,
                                 'cDesc': '\xe6\x8d\xa2\xe5\xbc\xb9\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                                 },
   'reload_speed_factor_pos_6': {'cKey': 'reload_speed_factor_pos_6',
                                 'cType': 'VAR_FLOAT',
                                 'iPercent': 1,
                                 'cInit': '0',
                                 'iSyncType': 1,
                                 'cDesc': '\xe6\x8d\xa2\xe5\xbc\xb9\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                                 },
   'fShootSpeedFactor': {'cKey': 'fShootSpeedFactor',
                         'cType': 'VAR_FLOAT',
                         'iPercent': 1,
                         'cInit': '0',
                         'iSyncType': 1,
                         'cDesc': '\xe5\xb0\x84\xe9\x80\x9f\xe5\x8a\xa0\xe6\x88\x90'
                         },
   'fShootSpeedFactor_pos_1': {'cKey': 'fShootSpeedFactor_pos_1',
                               'cType': 'VAR_FLOAT',
                               'iPercent': 1,
                               'cInit': '0',
                               'iSyncType': 1,
                               'cDesc': '\xe4\xb8\xbb\xe6\xad\xa6\xe5\x99\xa8\xe5\xb0\x84\xe5\x87\xbb\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                               },
   'fShootSpeedFactor_pos_2': {'cKey': 'fShootSpeedFactor_pos_2',
                               'cType': 'VAR_FLOAT',
                               'iPercent': 1,
                               'cInit': '0',
                               'iSyncType': 1,
                               'cDesc': '\xe5\x89\xaf\xe6\xad\xa6\xe5\x99\xa8\xe5\xb0\x84\xe5\x87\xbb\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                               },
   'spread_factor': {'cKey': 'spread_factor',
                     'cType': 'VAR_FLOAT',
                     'iPercent': 1,
                     'cInit': '0',
                     'iSyncType': 1,
                     'cDesc': '\xe6\x95\xa3\xe5\xb0\x84\xe8\x8c\x83\xe5\x9b\xb4\xe5\x8a\xa0\xe6\x88\x90'
                     },
   'spread_factor_pos_1': {'cKey': 'spread_factor_pos_1',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '0',
                           'iSyncType': 1,
                           'cDesc': '\xe4\xb8\xbb\xe6\xad\xa6\xe5\x99\xa8\xe6\x95\xa3\xe5\xb0\x84\xe8\x8c\x83\xe5\x9b\xb4\xe5\x8a\xa0\xe6\x88\x90'
                           },
   'spread_factor_pos_2': {'cKey': 'spread_factor_pos_2',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '0',
                           'iSyncType': 1,
                           'cDesc': '2\xe5\x8f\xb7\xe4\xbd\x8d\xe6\x95\xa3\xe5\xb0\x84\xe8\x8c\x83\xe5\x9b\xb4\xe5\x8a\xa0\xe6\x88\x90'
                           },
   'spread_max_factor': {'cKey': 'spread_max_factor',
                         'cType': 'VAR_FLOAT',
                         'iPercent': 1,
                         'cInit': '0',
                         'iSyncType': 1,
                         'cDesc': '\xe6\x95\xa3\xe5\xb8\x83\xe9\x80\x92\xe5\xa2\x9e\xe4\xb8\x8a\xe9\x99\x90\xe5\x8a\xa0\xe6\x88\x90'
                         },
   'spread_inc_factor': {'cKey': 'spread_inc_factor',
                         'cType': 'VAR_FLOAT',
                         'iPercent': 1,
                         'cInit': '0',
                         'iSyncType': 1,
                         'cDesc': '\xef\xbc\x88\xe8\x85\xb0\xe5\xb0\x84\xef\xbc\x89\xe6\x95\xa3\xe5\xb0\x84\xe9\x80\x92\xe5\xa2\x9e\xe5\x8a\xa0\xe6\x88\x90'
                         },
   'throw_speed_add_rate': {'cKey': 'throw_speed_add_rate',
                            'cType': 'VAR_FLOAT',
                            'iPercent': 1,
                            'cInit': '0',
                            'iSyncType': 1,
                            'cDesc': '\xe6\x8a\x95\xe6\x8e\xb7\xe7\x89\xa9\xe9\xa3\x9e\xe8\xa1\x8c\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                            },
   'attr_vampire_factor': {'cKey': 'attr_vampire_factor',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '0',
                           'iSyncType': 0,
                           'cDesc': '\xe4\xbc\xa4\xe5\xae\xb3\xe5\x90\xb8\xe8\xa1\x80\xe7\xb3\xbb\xe6\x95\xb0'
                           },
   'accumulate_init_energy_ratio': {'cKey': 'accumulate_init_energy_ratio',
                                    'cType': 'VAR_FLOAT',
                                    'iPercent': 1,
                                    'cInit': '0',
                                    'iSyncType': 1,
                                    'cDesc': '\xe8\x93\x84\xe5\x8a\x9b\xe6\x9e\xaa\xe5\x88\x9d\xe5\xa7\x8b\xe8\x93\x84\xe5\x8a\x9b\xe5\x80\xbc'
                                    },
   'footstep_sound_dis_factor': {'cKey': 'footstep_sound_dis_factor',
                                 'cType': 'VAR_FLOAT',
                                 'iPercent': 1,
                                 'cInit': '0',
                                 'iSyncType': 2,
                                 'cDesc': '\xe8\x84\x9a\xe6\xad\xa5\xe5\xa3\xb0\xe9\x9f\xb3\xe8\xb7\x9d\xe7\xa6\xbb\xe5\x8a\xa0\xe6\x88\x90'
                                 },
   'controlled_time_factor': {'cKey': 'controlled_time_factor',
                              'cType': 'VAR_FLOAT',
                              'iPercent': 1,
                              'cInit': '0',
                              'iSyncType': 0,
                              'cDesc': '\xe5\x8f\x97\xe6\x8e\xa7\xe6\x97\xb6\xe9\x97\xb4\xe5\x8a\xa0\xe6\x88\x90'
                              },
   'cure_factor': {'cKey': 'cure_factor',
                   'cType': 'VAR_FLOAT',
                   'iPercent': 1,
                   'cInit': '0',
                   'iSyncType': 0,
                   'cDesc': '\xe6\xb2\xbb\xe7\x96\x97\xe6\x95\x88\xe6\x9e\x9c\xe5\x8a\xa0\xe6\x88\x90'
                   },
   'crit_prate': {'cKey': 'crit_prate',
                  'cType': 'VAR_FLOAT',
                  'iPercent': 1,
                  'cInit': '0',
                  'iSyncType': 0,
                  'cDesc': '\xe6\x9a\xb4\xe5\x87\xbb\xe5\x80\x8d\xe7\x8e\x87'
                  },
   'skill_recover_factor': {'cKey': 'skill_recover_factor',
                            'cType': 'VAR_FLOAT',
                            'iPercent': 1,
                            'cInit': '0',
                            'iSyncType': 1,
                            'cDesc': '\xe6\x8a\x80\xe8\x83\xbd\xe6\x81\xa2\xe5\xa4\x8d\xe9\x80\x9f\xe5\xba\xa6',
                            'fExtremum': 3
                            },
   'skill_cd_add': {'cKey': 'skill_cd_add',
                    'cType': 'VAR_FLOAT',
                    'iPercent': 1,
                    'cInit': '0',
                    'iSyncType': 1,
                    'cDesc': '\xe6\x8a\x80\xe8\x83\xbdCD\xe5\x8a\xa0\xe6\x88\x90'
                    },
   'skill_hit_recover_factor': {'cKey': 'skill_hit_recover_factor',
                                'cType': 'VAR_FLOAT',
                                'iPercent': 1,
                                'cInit': '0',
                                'iSyncType': 1,
                                'cDesc': '\xe5\x91\xbd\xe4\xb8\xad\xe4\xb9\x8b\xe5\x90\x8e\xe6\x8a\x80\xe8\x83\xbd\xe6\x81\xa2\xe5\xa4\x8d\xe9\x80\x9f\xe5\xba\xa6'
                                },
   'hip_jump_factor': {'cKey': 'hip_jump_factor',
                       'cType': 'VAR_FLOAT',
                       'iPercent': 1,
                       'cInit': '0',
                       'iSyncType': 1,
                       'cDesc': 'HIP,\xe8\xb7\xb3\xe8\xb7\x83'
                       },
   'hip_stand_stop_factor': {'cKey': 'hip_stand_stop_factor',
                             'cType': 'VAR_FLOAT',
                             'iPercent': 1,
                             'cInit': '0',
                             'iSyncType': 1,
                             'cDesc': 'HIP,\xe7\xab\x99\xe7\xab\x8b,\xe9\x9d\x99\xe6\xad\xa2'
                             },
   'hip_stand_move_factor': {'cKey': 'hip_stand_move_factor',
                             'cType': 'VAR_FLOAT',
                             'iPercent': 1,
                             'cInit': '0',
                             'iSyncType': 1,
                             'cDesc': 'HIP,\xe7\xab\x99\xe7\xab\x8b,\xe7\xa7\xbb\xe5\x8a\xa8'
                             },
   'attr_vampire_factor_human': {'cKey': 'attr_vampire_factor_human',
                                 'cType': 'VAR_FLOAT',
                                 'iPercent': 1,
                                 'cInit': '0',
                                 'iSyncType': 0,
                                 'cDesc': '\xe4\xbc\xa4\xe5\xae\xb3\xe5\x90\xb8\xe8\xa1\x80\xe7\xb3\xbb\xe6\x95\xb0,\xe4\xb8\x93\xe5\xaf\xb9\xe4\xba\xba'
                                 },
   'attr_vampire_factor_mecha': {'cKey': 'attr_vampire_factor_mecha',
                                 'cType': 'VAR_FLOAT',
                                 'iPercent': 1,
                                 'cInit': '0',
                                 'iSyncType': 0,
                                 'cDesc': '\xe4\xbc\xa4\xe5\xae\xb3\xe5\x90\xb8\xe8\xa1\x80\xe7\xb3\xbb\xe6\x95\xb0,\xe4\xb8\x93\xe5\xaf\xb9\xe6\x9c\xba\xe7\x94\xb2'
                                 },
   'weapon_heat_dec_factor': {'cKey': 'weapon_heat_dec_factor',
                              'cType': 'VAR_FLOAT',
                              'iPercent': 1,
                              'cInit': '0',
                              'iSyncType': 1,
                              'cDesc': '\xe6\xad\xa6\xe5\x99\xa8\xe6\x95\xa3\xe7\x83\xad\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                              },
   'super_jump_vspeed_add': {'cKey': 'super_jump_vspeed_add',
                             'cType': 'VAR_FLOAT',
                             'iPercent': 1,
                             'cInit': '0',
                             'iSyncType': 0,
                             'cDesc': '\xe5\xbc\xb9\xe8\xb7\xb3\xe5\x8f\xb0\xe5\x9e\x82\xe7\x9b\xb4\xe5\x88\x9d\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90'
                             },
   'accumulate_gun_factor': {'cKey': 'accumulate_gun_factor',
                             'cType': 'VAR_FLOAT',
                             'iPercent': 1,
                             'cInit': '0',
                             'iSyncType': 1,
                             'cDesc': '\xe6\xad\xa6\xe5\x99\xa8\xe8\x93\x84\xe5\x8a\x9b\xe9\x80\x9f\xe5\xba\xa6\xe5\x8a\xa0\xe6\x88\x90',
                             'fExtremum': 1
                             },
   'weapon_interval_factor': {'cKey': 'weapon_interval_factor',
                              'cType': 'VAR_FLOAT',
                              'iPercent': 1,
                              'cInit': '0',
                              'iSyncType': 1,
                              'cDesc': '\xe6\xad\xa6\xe5\x99\xa8\xe5\xbc\x80\xe7\x81\xab\xe9\x97\xb4\xe9\x9a\x94\xe5\x8a\xa0\xe6\x88\x90',
                              'fExtremum': 1
                              },
   'weak_hit_factor': {'cKey': 'weak_hit_factor',
                       'cType': 'VAR_FLOAT',
                       'iPercent': 1,
                       'cInit': '0',
                       'iSyncType': 1,
                       'cDesc': '\xe5\xbc\xb1\xe7\x82\xb9\xe9\xa2\x9d\xe5\xa4\x96\xe5\xa2\x9e\xe4\xbc\xa4'
                       },
   'armor_factor': {'cKey': 'armor_factor',
                    'cType': 'VAR_FLOAT',
                    'iPercent': 1,
                    'cInit': '0',
                    'iSyncType': 1,
                    'cDesc': '\xe6\x8a\xa4\xe7\x94\xb2\xe5\x8f\x98\xe5\x8c\x96\xe6\xaf\x94\xe4\xbe\x8b'
                    },
   'armor_add': {'cKey': 'armor_add',
                 'cType': 'VAR_FLOAT',
                 'iPercent': 1,
                 'cInit': '0',
                 'iSyncType': 1,
                 'cDesc': '\xe6\x8a\xa4\xe7\x94\xb2\xe5\x8f\x98\xe5\x8c\x96\xe5\x8a\xa0\xe5\x87\x8f'
                 },
   'armor_pierce_factor': {'cKey': 'armor_pierce_factor',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '0',
                           'iSyncType': 1,
                           'cDesc': '\xe6\x8a\xa4\xe7\x94\xb2\xe7\xa9\xbf\xe9\x80\x8f\xe7\xb3\xbb\xe6\x95\xb0'
                           },
   'crit_prate_pos_1': {'cKey': 'crit_prate_pos_1',
                        'cType': 'VAR_FLOAT',
                        'iPercent': 1,
                        'cInit': '0',
                        'iSyncType': 0,
                        'cDesc': '\xe4\xb8\xbb\xe6\xad\xa6\xe5\x99\xa8\xe6\x9a\xb4\xe5\x87\xbb\xe6\xa6\x82\xe7\x8e\x87'
                        },
   'crit_prate_pos_2': {'cKey': 'crit_prate_pos_2',
                        'cType': 'VAR_FLOAT',
                        'iPercent': 1,
                        'cInit': '0',
                        'iSyncType': 0,
                        'cDesc': '\xe5\x89\xaf\xe6\xad\xa6\xe5\x99\xa8\xe6\x9a\xb4\xe5\x87\xbb\xe6\xa6\x82\xe7\x8e\x87'
                        },
   'crit_dmg_add_factor': {'cKey': 'crit_dmg_add_factor',
                           'cType': 'VAR_FLOAT',
                           'iPercent': 1,
                           'cInit': '0',
                           'iSyncType': 0,
                           'cDesc': '\xe6\x9a\xb4\xe5\x87\xbb\xe4\xbc\xa4\xe5\xae\xb3\xe5\x80\x8d\xe7\x8e\x87\xe5\x8a\xa0\xe6\x88\x90'
                           },
   'recover_limit_factor': {'cKey': 'recover_limit_factor',
                            'cType': 'VAR_FLOAT',
                            'iPercent': 1,
                            'cInit': '0',
                            'iSyncType': 0,
                            'cDesc': '\xe6\x81\xa2\xe5\xa4\x8d\xe8\xa1\x80\xe9\x87\x8f\xe4\xb8\x8a\xe9\x99\x90\xe7\xb3\xbb\xe6\x95\xb0'
                            }
   }
import six
MP_TYPE = {'VAR_INT': int,
   'VAR_FLOAT': float
   }
attr_dict = {}
attr_sync_dict = {}
for key, val in six.iteritems(data):
    type_name = val['cType']
    attr_dict[key] = MP_TYPE[type_name](val['cInit'])
    attr_sync_dict[key] = val['iSyncType']

def has_define_attr(attr_name):
    return attr_name in attr_sync_dict


def get_attr_sync_type--- This code section failed: ---

1315       0  LOAD_GLOBAL           0  'attr_sync_dict'
           3  LOAD_ATTR             1  'get'
           6  LOAD_ATTR             1  'get'
           9  CALL_FUNCTION_2       2 
          12  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9


def get_init_attr_val(key, default=0):
    if key not in attr_dict:
        return default
    return attr_dict[key]


def get_attr_extremum(key):
    if key not in data:
        return None
    else:
        return data[key].get('fExtremum', None)


def get_init_attr--- This code section failed: ---

1332       0  BUILD_MAP_0           0 
           3  STORE_FAST            1  'd'

1333       6  LOAD_FAST             1  'd'
           9  LOAD_ATTR             0  'update'
          12  LOAD_GLOBAL           1  'attr_dict'
          15  CALL_FUNCTION_1       1 
          18  POP_TOP          

1335      19  LOAD_CONST            1  ''
          22  LOAD_FAST             1  'd'
          25  LOAD_CONST            2  'human_yaw'
          28  STORE_SUBSCR     

1337      29  LOAD_FAST             1  'd'
          32  LOAD_FAST             3  'mp_attr'
          35  STORE_SUBSCR     

1338      36  LOAD_FAST             1  'd'
          39  LOAD_ATTR             2  'get'
          42  LOAD_CONST            4  'iHp'
          45  LOAD_CONST            5  100
          48  CALL_FUNCTION_2       2 
          51  CALL_FUNCTION_6       6 
          54  STORE_SUBSCR     

1339      55  LOAD_FAST             1  'd'
          58  LOAD_ATTR             2  'get'
          61  LOAD_CONST            4  'iHp'
          64  LOAD_CONST            5  100
          67  CALL_FUNCTION_2       2 
          70  CALL_FUNCTION_7       7 
          73  STORE_SUBSCR     

1340      74  LOAD_FAST             1  'd'
          77  LOAD_ATTR             2  'get'
          80  LOAD_CONST            8  'iSignal'
          83  LOAD_CONST            5  100
          86  CALL_FUNCTION_2       2 
          89  CALL_FUNCTION_9       9 
          92  STORE_SUBSCR     

1341      93  LOAD_FAST             1  'd'
          96  LOAD_ATTR             2  'get'
          99  LOAD_CONST            8  'iSignal'
         102  LOAD_CONST            5  100
         105  CALL_FUNCTION_2       2 
         108  CALL_FUNCTION_10     10 
         111  STORE_SUBSCR     

1342     112  LOAD_FAST             1  'd'
         115  LOAD_ATTR             2  'get'
         118  LOAD_CONST           11  'iSignalRevive'
         121  LOAD_CONST           12  20
         124  CALL_FUNCTION_2       2 
         127  CALL_FUNCTION_13     13 
         130  STORE_SUBSCR     

1344     131  LOAD_FAST             1  'd'
         134  LOAD_ATTR             2  'get'
         137  LOAD_CONST           14  'iHealSignal'
         140  LOAD_CONST            1  ''
         143  CALL_FUNCTION_2       2 
         146  CALL_FUNCTION_15     15 
         149  STORE_SUBSCR     

1345     150  LOAD_FAST             1  'd'
         153  LOAD_ATTR             2  'get'
         156  LOAD_CONST           16  'iHealSignalTime'
         159  LOAD_CONST            1  ''
         162  CALL_FUNCTION_2       2 
         165  CALL_FUNCTION_17     17 
         168  STORE_SUBSCR     

1346     169  LOAD_FAST             1  'd'
         172  LOAD_ATTR             2  'get'
         175  LOAD_CONST           18  'iHealSignalInterval'
         178  LOAD_CONST            1  ''
         181  CALL_FUNCTION_2       2 
         184  CALL_FUNCTION_19     19 
         187  STORE_SUBSCR     

1349     188  LOAD_FAST             1  'd'
         191  LOAD_ATTR             2  'get'
         194  LOAD_CONST           20  'iHealHp'
         197  LOAD_CONST            1  ''
         200  CALL_FUNCTION_2       2 
         203  CALL_FUNCTION_21     21 
         206  STORE_SUBSCR     

1350     207  LOAD_FAST             1  'd'
         210  LOAD_ATTR             2  'get'
         213  LOAD_CONST           22  'fHealTime'
         216  LOAD_CONST            1  ''
         219  CALL_FUNCTION_2       2 
         222  CALL_FUNCTION_23     23 
         225  STORE_SUBSCR     

1351     226  LOAD_FAST             1  'd'
         229  LOAD_ATTR             2  'get'
         232  LOAD_CONST           24  'fHealInterval'
         235  LOAD_CONST            1  ''
         238  CALL_FUNCTION_2       2 
         241  CALL_FUNCTION_25     25 
         244  STORE_SUBSCR     

1353     245  LOAD_FAST             1  'd'
         248  LOAD_ATTR             2  'get'
         251  LOAD_CONST           26  'iStamina'
         254  LOAD_CONST            5  100
         257  CALL_FUNCTION_2       2 
         260  CALL_FUNCTION_27     27 
         263  STORE_SUBSCR     

1354     264  LOAD_CONST            1  ''
         267  LOAD_CONST           28  'vit'
         270  STORE_SUBSCR     

1355     271  LOAD_FAST             1  'd'
         274  LOAD_ATTR             2  'get'
         277  LOAD_CONST           29  'iBaseCapacity'
         280  LOAD_CONST            5  100
         283  CALL_FUNCTION_2       2 
         286  CALL_FUNCTION_30     30 
         289  STORE_SUBSCR     

1358     290  LOAD_CONST            4  'iHp'
         293  LOAD_CONST           20  'iHealHp'
         296  LOAD_CONST           22  'fHealTime'
         299  LOAD_CONST           24  'fHealInterval'
         302  LOAD_CONST           26  'iStamina'
         305  LOAD_CONST           29  'iBaseCapacity'
         308  BUILD_LIST_6          6 
         311  STORE_FAST            2  'exclude_keys'

1359     314  STORE_FAST            3  'mp_attr'
         317  BINARY_SUBSCR    
         318  STORE_FAST            3  'mp_attr'

1360     321  SETUP_LOOP           36  'to 360'
         324  LOAD_FAST             2  'exclude_keys'
         327  GET_ITER         
         328  FOR_ITER             28  'to 359'
         331  STORE_FAST            4  'k'

1361     334  LOAD_FAST             4  'k'
         337  LOAD_FAST             3  'mp_attr'
         340  COMPARE_OP            6  'in'
         343  POP_JUMP_IF_FALSE   328  'to 328'

1362     346  LOAD_FAST             3  'mp_attr'
         349  LOAD_FAST             4  'k'
         352  DELETE_SUBSCR    
         353  JUMP_BACK           328  'to 328'
         356  JUMP_BACK           328  'to 328'
         359  POP_BLOCK        
       360_0  COME_FROM                '321'

Parse error at or near `STORE_SUBSCR' instruction at offset 35