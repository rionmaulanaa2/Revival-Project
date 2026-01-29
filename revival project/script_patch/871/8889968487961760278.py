# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/get_on_mecha_utils.py
from __future__ import absolute_import

def ComWeaponController_init(owner, com):
    owner.get_com('ComBackpackData').on_init_complete()


HUMAN_COMPONENT_LIST = {'Avatar': [
            {'component': 'ComAimHelper'
               },
            {'component': 'ComPositionChecker'
               },
            {'component': 'ComWeaponController',
               'init_func': ComWeaponController_init
               }],
   'Puppet': [
            {'component': 'ComWeaponController',
               'init_func': ComWeaponController_init
               }],
   'Common': []}

def ComMoveSyncSender2_init(owner, com):
    import logic.gcommon.common_const.sync_const as sync_const
    trigger_lst = [
     sync_const.SYNC_TRIGGER_NAME_EULER]
    com.set_enable_sync_trigger(trigger_lst)


def ComMoveSyncReceiver2_init(owner, com):
    import logic.gcommon.common_const.sync_const as sync_const


def ComHumanDriverGhost_getter(owner):
    pos = owner.ev_g_position()
    return {'position': (pos.x, pos.y, pos.z)}


def ComMechaStaticCollision_getter(owner):
    from logic.gcommon.common_const.collision_const import MECHA_STAND_WIDTH, MECHA_STAND_HEIGHT
    return {'capsule_size': (MECHA_STAND_WIDTH, MECHA_STAND_HEIGHT)}


def ComDriver_getter(owner):
    return {'mecha_id': owner.share_data.ref_mecha_id}


MECHA_COMPONENT_LIST = {'Avatar': [
            {'component': 'ComCharacter'
               },
            {'component': 'com_character_ctrl.ComDriver',
               'bdict_getter': ComDriver_getter
               },
            {'component': 'ComMoveSyncSender2',
               'init_func': ComMoveSyncSender2_init
               },
            {'component': 'ComPositionChecker'
               }],
   'Puppet': [
            {'component': 'ComMechaStaticCollision',
               'bdict_getter': ComMechaStaticCollision_getter
               },
            {'component': 'ComInterpolater'
               },
            {'component': 'ComMoveSyncReceiver2',
               'init_func': ComMoveSyncReceiver2_init
               },
            {'component': 'ComHumanDriverGhost',
               'bdict_getter': ComHumanDriverGhost_getter
               }],
   'Robot_Add': [
               {'component': 'ComCharacter'
                  }],
   'Robot_Del': [
               {'component': 'ComMechaStaticCollision'
                  }],
   'AI_Agent': [
              {'component': 'ComCharacter'
                 },
              {'component': 'com_character_ctrl.ComDriver',
                 'bdict_getter': ComDriver_getter
                 },
              {'component': 'ComMoveSyncSender2',
                 'init_func': ComMoveSyncSender2_init
                 },
              {'component': 'ComPositionChecker'
                 },
              {'component': 'com_ai_ctrl.ComRemoteControl'
                 }],
   'AI_Receiver': [
                 {'component': 'ComInterpolater'
                    },
                 {'component': 'ComMoveSyncReceiver2',
                    'init_func': ComMoveSyncReceiver2_init
                    },
                 {'component': 'ComHumanDriverGhost',
                    'bdict_getter': ComHumanDriverGhost_getter
                    }],
   'Common_Agent': [
                  {'component': 'ComMoveSyncSender2',
                     'init_func': ComMoveSyncSender2_init
                     }],
   'Common_Receiver': [
                     {'component': 'ComInterpolater'
                        },
                     {'component': 'ComMoveSyncReceiver2',
                        'init_func': ComMoveSyncReceiver2_init
                        }]
   }

def get_mecha_component(type_key, new=False):
    com_list = MECHA_COMPONENT_LIST[type_key]
    return com_list


def on_join_mecha_8005(self):
    from mobile.common.EntityManager import EntityManager
    driver = EntityManager.getentity(self.sd.ref_driver_id)
    if driver and driver.logic:
        driver.logic.send_event('E_SEAT_ON_MECHA', True, self.unit_obj.id)