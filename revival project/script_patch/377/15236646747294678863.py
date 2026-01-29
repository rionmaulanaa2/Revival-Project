# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/9015.py
_reload_all = True
DataDict = {9015: {'Content': {'MC_BEAT_BACK': {'action_param': (
                                                      0, ['shake', 'lower', 1, {'loop': True}]),
                                       'action_state': 'BeatBack',
                                       'custom_param': {'max_h_speed': 50,
                                                        'min_h_speed': 10,
                                                        'max_v_speed': 30,
                                                        'min_v_speed': 10,
                                                        'max_affect_dist': 15,
                                                        'gravity': 50
                                                        }
                                       },
                      'MC_DEAD': {'action_param': (
                                                 0, ['die', 'lower', 1]),
                                  'action_state': 'Die',
                                  'sound_param': [{'time': 0.0,'sound_name': ('Play_monster', ('monster_action', 'monster9007_blast'), ('monster_select', 'monster9007'))}]},
                      'MC_FROZEN': {'action_state': 'OnFrozen'
                                    },
                      'MC_HIT': {'action_state': 'Hit',
                                 'custom_param': {'hit_thresh': 300,
                                                  'hit_anim': ('hit', 'hit'),
                                                  'hit_anim_duration': (1, 1)
                                                  }
                                 },
                      'MC_IMMOBILIZE': {'action_param': (
                                                       0, ['shake', 'lower', 1, {'loop': True}]),
                                        'action_state': 'Immobilize'
                                        },
                      'MC_JUMP_1': {'action_param': (
                                                   0, ['idle', 'lower', 1]),
                                    'action_state': 'JumpUp',
                                    'custom_param': {'gravity': 57,'jump_speed': 36,'anim_duration': 1}},
                      'MC_JUMP_2': {'action_param': (
                                                   0, ['idle', 'lower', 1, {'loop': True}]),
                                    'action_state': 'Fall',
                                    'custom_param': {'gravity': 100}},
                      'MC_JUMP_3': {'action_param': (
                                                   0, ['idle', 'lower', 1]),
                                    'action_state': 'OnGround',
                                    'custom_param': {'anim_duration': 0.5,'recover_trigger_speed': 36}},
                      'MC_MECHA_BOARDING': {'action_param': (
                                                           0, ['born', 'lower', 1]),
                                            'action_state': 'Born',
                                            'custom_param': {'anim_duration': 3
                                                             }
                                            },
                      'MC_MOVE': {'action_param': (
                                                 0, ['move_f', 'lower', 1, {'loop': True}]),
                                  'action_state': 'Walk',
                                  'custom_param': {'walk_speed': 5,'move_acc': 15,'brake_acc': -30},'sound_param': [{'time': 0.0,'sound_name': ('Play_monster', ('monster_action', 'monster9007_run'), ('monster_select', 'monster9007'))}]},
                      'MC_RUN': {'action_param': (
                                                0, ['move_f', 'lower', 1, {'loop': True}]),
                                 'action_state': 'Run',
                                 'custom_param': {'walk_speed': 5,'run_speed': 7,'move_acc': 15,'brake_acc': -30}},
                      'MC_SECOND_WEAPON_ATTACK': {'action_state': 'AccumulateCastGrenade',
                                                  'custom_param': {'weapon_type': 890501,
                                                                   'fire_socket': 'fx_kaihuo1',
                                                                   'pre_anim': 'fire_attack_01',
                                                                   'cast_anim': 'fire_attack_02',
                                                                   'post_anim': 'fire_attack_03',
                                                                   'pre_time': 1.5,
                                                                   'cast_time': 0.3,
                                                                   'post_time': 0.8,
                                                                   'pre_sound_param': (
                                                                                     'Play_weapon_fire', (('gun', 'monster9007_fire'), ('gun_option', 'xuli'))),
                                                                   'fire_sound_param': (
                                                                                      'Play_weapon_fire', (('gun', 'monster9007_fire'), ('gun_option', 'single')))
                                                                   }
                                                  },
                      'MC_SHOOT': {'action_param': (
                                                  0, ['attack', 'lower', 1, {'loop': True}]),
                                   'action_state': 'WeaponFire',
                                   'custom_param': {'shoot_anim': ('attack', 'lower', 1)},'sound_param': [{'time': 0.0,'sound_name': ('Play_weapon_fire', ('gun', 'monster9007_fire'), ('gun_option', 'single'))}]},
                      'MC_STAND': {'action_param': (
                                                  0, ['idle', 'lower', 1, {'loop': True}]),
                                   'action_state': 'Stand'
                                   },
                      'MC_SWORD_CORE': {'action_state': 'CastSkillClient',
                                        'custom_param': {'cast_anim': 'skill_02',
                                                         'cast_time': 2.8,
                                                         'speed_scale': 2.0
                                                         },
                                        'sound_param': [{'time': 0.0,'sound_name': ('Play_monster', ('monster_action', 'monster9007_frantic'), ('monster_select', 'monster9007'))}, {'time': -1,'command_type': 0,'sound_name': 'monster9007_frantic'}]},
                      'MC_TURN ': {'action_state': 'Turn',
                                   'custom_param': {'enable_twist_yaw': False,
                                                    'enable_twist_pitch': True
                                                    }
                                   }
                      },
          'Name': '\xe7\x8c\x8e\xe9\xad\x94\xe4\xba\xba\xe4\xb8\xad\xe5\x9e\x8b\xe6\x80\xaa\xef\xbc\x882\xe5\x8f\xaa\xef\xbc\x89',
          'QuickLink': 1
          },
   'status': {'Content': {'MC_BEAT_BACK': {'MC_DEAD': 2,
                                           'MC_FROZEN': 2,
                                           'MC_HIT': 1,
                                           'MC_IMMOBILIZE': 2,
                                           'MC_JUMP_1': 1,
                                           'MC_JUMP_2': 2,
                                           'MC_JUMP_3': 2,
                                           'MC_MECHA_BOARDING': 1,
                                           'MC_MOVE': 1,
                                           'MC_RUN': 1,
                                           'MC_SHOOT': 1,
                                           'MC_STAND': 1,
                                           'MC_SWORD_CORE': 1,
                                           'MC_TURN ': 1
                                           },
                          'MC_DEAD': {'MC_BEAT_BACK': 1,
                                      'MC_FROZEN': 1,
                                      'MC_HIT': 1,
                                      'MC_IMMOBILIZE': 1,
                                      'MC_JUMP_1': 1,
                                      'MC_JUMP_2': 1,
                                      'MC_JUMP_3': 1,
                                      'MC_MECHA_BOARDING': 1,
                                      'MC_MOVE': 1,
                                      'MC_RUN': 1,
                                      'MC_SECOND_WEAPON_ATTACK': 1,
                                      'MC_SHOOT': 1,
                                      'MC_STAND': 1,
                                      'MC_SWORD_CORE': 1,
                                      'MC_TURN ': 1
                                      },
                          'MC_FROZEN': {'MC_BEAT_BACK': 1,
                                        'MC_DEAD': 2,
                                        'MC_HIT': 1,
                                        'MC_IMMOBILIZE': 1,
                                        'MC_JUMP_1': 1,
                                        'MC_JUMP_2': 1,
                                        'MC_JUMP_3': 1,
                                        'MC_MECHA_BOARDING': 1,
                                        'MC_MOVE': 1,
                                        'MC_RUN': 1,
                                        'MC_SECOND_WEAPON_ATTACK': 1,
                                        'MC_SHOOT': 1,
                                        'MC_STAND': 1,
                                        'MC_SWORD_CORE': 1,
                                        'MC_TURN ': 1
                                        },
                          'MC_HIT': {'MC_BEAT_BACK': 2,
                                     'MC_DEAD': 2,
                                     'MC_FROZEN': 2,
                                     'MC_IMMOBILIZE': 2,
                                     'MC_MECHA_BOARDING': 1,
                                     'MC_SWORD_CORE': 2
                                     },
                          'MC_IMMOBILIZE': {'MC_BEAT_BACK': 2,
                                            'MC_DEAD': 2,
                                            'MC_FROZEN': 2,
                                            'MC_HIT': 1,
                                            'MC_JUMP_1': 1,
                                            'MC_JUMP_2': 1,
                                            'MC_JUMP_3': 1,
                                            'MC_MECHA_BOARDING': 1,
                                            'MC_MOVE': 1,
                                            'MC_RUN': 1,
                                            'MC_SECOND_WEAPON_ATTACK': 2,
                                            'MC_SHOOT': 1,
                                            'MC_STAND': 1,
                                            'MC_SWORD_CORE': 2,
                                            'MC_TURN ': 1
                                            },
                          'MC_JUMP_1': {'MC_BEAT_BACK': 2,
                                        'MC_DEAD': 2,
                                        'MC_FROZEN': 2,
                                        'MC_IMMOBILIZE': 2,
                                        'MC_JUMP_2': 2,
                                        'MC_JUMP_3': 2,
                                        'MC_MECHA_BOARDING': 1,
                                        'MC_RUN': 2,
                                        'MC_SECOND_WEAPON_ATTACK': 2,
                                        'MC_STAND': 1,
                                        'MC_SWORD_CORE': 2,
                                        'MC_TURN ': 1
                                        },
                          'MC_JUMP_2': {'MC_BEAT_BACK': 2,
                                        'MC_DEAD': 2,
                                        'MC_FROZEN': 2,
                                        'MC_IMMOBILIZE': 2,
                                        'MC_JUMP_1': 1,
                                        'MC_JUMP_3': 2,
                                        'MC_MECHA_BOARDING': 1,
                                        'MC_MOVE': 1,
                                        'MC_SECOND_WEAPON_ATTACK': 2,
                                        'MC_STAND': 1,
                                        'MC_SWORD_CORE': 2,
                                        'MC_TURN ': 1
                                        },
                          'MC_JUMP_3': {'MC_BEAT_BACK': 2,
                                        'MC_DEAD': 2,
                                        'MC_FROZEN': 2,
                                        'MC_IMMOBILIZE': 2,
                                        'MC_JUMP_1': 2,
                                        'MC_MECHA_BOARDING': 1,
                                        'MC_MOVE': 2,
                                        'MC_RUN': 1,
                                        'MC_SECOND_WEAPON_ATTACK': 2,
                                        'MC_STAND': 2,
                                        'MC_SWORD_CORE': 2,
                                        'MC_TURN ': 1
                                        },
                          'MC_MECHA_BOARDING': {'MC_BEAT_BACK': 1,
                                                'MC_DEAD': 2,
                                                'MC_FROZEN': 2,
                                                'MC_HIT': 1,
                                                'MC_IMMOBILIZE': 1,
                                                'MC_JUMP_1': 1,
                                                'MC_JUMP_2': 1,
                                                'MC_JUMP_3': 1,
                                                'MC_MOVE': 1,
                                                'MC_RUN': 1,
                                                'MC_SECOND_WEAPON_ATTACK': 1,
                                                'MC_SHOOT': 1,
                                                'MC_STAND': 2,
                                                'MC_SWORD_CORE': 1,
                                                'MC_TURN ': 1
                                                },
                          'MC_MOVE': {'MC_DEAD': 2,
                                      'MC_FROZEN': 2,
                                      'MC_JUMP_1': 2,
                                      'MC_JUMP_2': 2,
                                      'MC_JUMP_3': 2,
                                      'MC_MECHA_BOARDING': 1,
                                      'MC_MOVE': 1,
                                      'MC_RUN': 2,
                                      'MC_SECOND_WEAPON_ATTACK': 2,
                                      'MC_STAND': 2,
                                      'MC_SWORD_CORE': 2,
                                      'MC_TURN ': 1
                                      },
                          'MC_RUN': {'MC_DEAD': 2,
                                     'MC_FROZEN': 2,
                                     'MC_JUMP_1': 2,
                                     'MC_JUMP_2': 2,
                                     'MC_JUMP_3': 2,
                                     'MC_MECHA_BOARDING': 1,
                                     'MC_MOVE': 2,
                                     'MC_SECOND_WEAPON_ATTACK': 2,
                                     'MC_STAND': 2,
                                     'MC_SWORD_CORE': 2,
                                     'MC_TURN ': 1
                                     },
                          'MC_SECOND_WEAPON_ATTACK': {'MC_BEAT_BACK': 2,
                                                      'MC_DEAD': 2,
                                                      'MC_FROZEN': 2,
                                                      'MC_IMMOBILIZE': 2,
                                                      'MC_JUMP_1': 2,
                                                      'MC_JUMP_2': 2,
                                                      'MC_JUMP_3': 2,
                                                      'MC_MECHA_BOARDING': 1,
                                                      'MC_MOVE': 1,
                                                      'MC_RUN': 1,
                                                      'MC_SHOOT': 1,
                                                      'MC_STAND': 2,
                                                      'MC_SWORD_CORE': 2
                                                      },
                          'MC_SHOOT': {'MC_BEAT_BACK': 1,
                                       'MC_DEAD': 2,
                                       'MC_FROZEN': 2,
                                       'MC_IMMOBILIZE': 1,
                                       'MC_MECHA_BOARDING': 1,
                                       'MC_RUN': 1,
                                       'MC_SECOND_WEAPON_ATTACK': 2,
                                       'MC_SHOOT': 1,
                                       'MC_SWORD_CORE': 2
                                       },
                          'MC_STAND': {'MC_DEAD': 2,
                                       'MC_FROZEN': 2,
                                       'MC_JUMP_1': 2,
                                       'MC_JUMP_2': 2,
                                       'MC_JUMP_3': 2,
                                       'MC_MECHA_BOARDING': 1,
                                       'MC_MOVE': 2,
                                       'MC_RUN': 2,
                                       'MC_SECOND_WEAPON_ATTACK': 2,
                                       'MC_SWORD_CORE': 2,
                                       'MC_TURN ': 2
                                       },
                          'MC_SWORD_CORE': {'MC_BEAT_BACK': 1,
                                            'MC_DEAD': 2,
                                            'MC_FROZEN': 2,
                                            'MC_HIT': 1,
                                            'MC_IMMOBILIZE': 1,
                                            'MC_JUMP_1': 1,
                                            'MC_JUMP_2': 1,
                                            'MC_JUMP_3': 1,
                                            'MC_MECHA_BOARDING': 1,
                                            'MC_MOVE': 1,
                                            'MC_RUN': 1,
                                            'MC_SECOND_WEAPON_ATTACK': 1,
                                            'MC_SHOOT': 1,
                                            'MC_STAND': 1,
                                            'MC_TURN ': 1
                                            },
                          'MC_TURN ': {'MC_DEAD': 2,
                                       'MC_FROZEN': 2,
                                       'MC_JUMP_1': 2,
                                       'MC_JUMP_2': 2,
                                       'MC_JUMP_3': 2,
                                       'MC_MECHA_BOARDING': 1,
                                       'MC_MOVE': 2,
                                       'MC_RUN': 2,
                                       'MC_STAND': 2,
                                       'MC_SWORD_CORE': 2
                                       }
                          },
              'Name': '\xe7\x8a\xb6\xe6\x80\x81\xe8\xbf\x81\xe7\xa7\xbb\xe8\xa1\xa8',
              'QuickLink': 1
              }
   }

def GetData():
    return DataDict


def Getstatus():
    return GetData()['status']['Content']


def Get9015():
    return GetData()['9015']['Content']