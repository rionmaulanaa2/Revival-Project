# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/target_com_utils.py
from __future__ import absolute_import
import six
ACTION_DEL = 1
ACTION_EVENT_ON = 2
ACTION_EVENT_OFF = 3
COND_FIT = 10
COND_NON_FIT = 11
KEY_COMMON = 'common'
KEY_CONTROLLER = 'ctrl'
KEY_NON_CONTROLLER = 'no_ctrl'
KEY_USE_PHYS = 'use_phys'

def get_event_config(target_type, mp_com_config):
    mp_res = {ACTION_DEL: [],ACTION_EVENT_ON: [],ACTION_EVENT_OFF: []}
    d = config.get(target_type)
    for key, mp in six.iteritems(d):
        if key != KEY_COMMON and not mp_com_config.get(key, None):
            continue
        for action, lst in six.iteritems(mp):
            mp_res[action].extend(lst)

    return mp_res


config = {'human': {KEY_COMMON: {ACTION_EVENT_ON: [
                                          'ComHumanAppearance', 'ComHumanIKController']
                          },
             KEY_CONTROLLER: {ACTION_EVENT_ON: [
                                              'ComMoveSyncSender2', 'ComCharacter', 'ComHumanDriver']
                              },
             KEY_NON_CONTROLLER: {ACTION_EVENT_ON: [
                                                  'ComHumanDriverGhost', 'ComMoveSyncReceiver2', 'ComCharacterCollision'],
                                  ACTION_DEL: ('ComCharacter', 'ComHumanDriver')
                                  }
             },
   'lose': {KEY_COMMON: {ACTION_EVENT_OFF: [
                                          'ComHumanAppearance', 'ComHumanIKController']
                         },
            KEY_CONTROLLER: {ACTION_DEL: [
                                        'ComMoveSyncSender2', 'ComCharacter', 'ComHumanDriver']
                             },
            KEY_NON_CONTROLLER: {ACTION_DEL: [
                                            'ComHumanDriverGhost', 'ComMoveSyncReceiver2', 'ComCharacterCollision']
                                 }
            },
   'robot': {KEY_COMMON: {ACTION_EVENT_ON: [
                                          'ComHumanAppearance', 'ComHumanIKController']
                          },
             KEY_NON_CONTROLLER: {ACTION_DEL: [
                                             'ComMoveSyncReceiver2', 'ComHumanDriverGhost', 'ComCharacterCollision'],
                                  ACTION_EVENT_ON: [
                                                  'ComCharacter', 'ComHumanDriver', 'ComMoveSyncReceiver', 'ComWaterHuman', 'ComMoveSyncSender2', ('com_parachute', 'ComParachuteDriver')]
                                  }
             }
   }