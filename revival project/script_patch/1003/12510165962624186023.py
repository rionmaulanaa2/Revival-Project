# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mechatran_appearance/ComPatternTrans.py
from __future__ import absolute_import
from ...UnitCom import UnitCom
from logic.gcommon.common_const import mecha_const as mconst
from mobile.common.EntityManager import EntityManager
import math3d
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import collision_const
from logic.gcommon.item.item_const import FASHION_POS_SUIT
import logic.gcommon.const as gconst

class ComPatternTrans(UnitCom):
    BIND_EVENT = {'E_PATTERN_HANDLE': 'update_pattern',
       'E_VEHICLE_ENABLE_PHYSX': 'update_physx_owner'
       }
    PATTERN_COM_MAP = {mconst.MECHA_PATTERN_NORMAL: {'add': [],'delete': [
                                              'ComVehicleDriver2',
                                              'ComVehicleCollision']
                                     },
       mconst.MECHA_PATTERN_VEHICLE: {'add': [
                                            ('ComVehicleDriver2', 'client'),
                                            ('ComVehicleCollision', 'client')],
                                      'delete': [
                                               'ComCharacter',
                                               'ComDriver',
                                               'ComInput']
                                      }
       }

    def __init__(self):
        super(ComPatternTrans, self).__init__()
        self._pattern = None
        self._data = None
        self._phys_owner = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPatternTrans, self).init_from_dict(unit_obj, bdict)
        pattern = bdict.get('trans_pattern', mconst.MECHA_PATTERN_NORMAL)
        self.skin_id = bdict.get('mecha_fashion', {}).get(FASHION_POS_SUIT)
        self.update_pattern(pattern, bdict)
        self._npc_id = bdict['npc_id']

    def update_pattern(self, pattern, bdict=None, force_update=False):
        if pattern == self._pattern and not force_update:
            return
        else:
            if not bdict:
                bdict = {}
                pos = None
                if pattern == mconst.MECHA_PATTERN_NORMAL:
                    is_valid, pos = self.ev_g_check_transform_pos_valid()
                if not pos:
                    pos = self.ev_g_foot_position()
                if not pos:
                    pos = self.ev_g_position()
                if pos:
                    bdict['position'] = (
                     pos.x, pos.y, pos.z)
                bdict['lin_spd'] = (0, 0, 0)
                bdict['agl_spd'] = (0, 0, 0)
                bdict['phys_owner'] = self._phys_owner
                bdict['npc_id'] = self._npc_id
            self._pattern = pattern
            import copy
            com_map = self.PATTERN_COM_MAP[pattern]
            add_coms = copy.copy(com_map['add'])
            delete_coms = copy.copy(com_map['delete'])
            is_trans_wheel_chair = self.is_wheel_chair()
            is_driver = self.sd.ref_driver_id == global_data.player.id
            if pattern == mconst.MECHA_PATTERN_NORMAL:
                bdict['init_speed'] = self.ev_g_char_walk_direction()
                self.send_event('E_VEHICLE_UNDRIVE_SET', False)
                driver_id = self.sd.ref_driver_id
                driver = EntityManager.getentity(driver_id)
                if driver and driver.logic:
                    driver.logic.send_event('E_VEHICLE_TURN', 0)
                    self.send_event('E_SET_STATIC_COLLISON', not is_driver)
                if is_trans_wheel_chair:
                    delete_coms.append('ComMechaTransWheelchair')
                if is_driver:
                    add_coms.append(('ComMoveSyncSender2', 'client'))
                    add_coms.append(('ComCharacter', 'client'))
                    add_coms.append(('ComDriver', 'client.com_character_ctrl'))
                    add_coms.append(('ComInput', 'client.com_character_ctrl'))
                    delete_coms.append('ComMoveSyncReceiver2')
                    delete_coms.append('ComHumanDriverGhost')
                else:
                    add_coms.append(('ComMoveSyncReceiver2', 'client'))
                    add_coms.append(('ComHumanDriverGhost', 'client'))
                    delete_coms.append('ComMoveSyncSender2')
                    delete_coms.append('ComCharacter')
                    delete_coms.append('ComDriver')
                    delete_coms.append('ComInput')
            elif pattern == mconst.MECHA_PATTERN_VEHICLE:
                bdict['init_speed'] = self.ev_g_char_walk_direction()
                self.send_event('E_VEHICLE_UNDRIVE_SET', True)
                if is_trans_wheel_chair:
                    add_coms.append(('ComMechaTransWheelchair', 'client'))
                delete_coms.append('ComMoveSyncReceiver2')
                delete_coms.append('ComHumanDriverGhost')
                delete_coms.append('ComMoveSyncSender2')
            lst_complete = []
            for cname, ctype in add_coms:
                com = self.unit_obj.get_com(cname)
                if com:
                    self.unit_obj.del_com(cname)
                com = self.unit_obj.add_com(cname, ctype)
                com.init_from_dict(self.unit_obj, bdict)
                lst_complete.append(com)

            for com in lst_complete:
                com.on_init_complete()

            for cname in delete_coms:
                self.unit_obj.del_com(cname)

            self.send_event('E_FOOT_POSITION', math3d.vector(*bdict['position']))
            self.send_event('E_ACTIVE_DRIVER')
            self.send_event('E_FORCE_ACTIVE')
            return

    def update_physx_owner(self, enable, new_player_id, lin_spd, agl_spd):
        self._phys_owner = new_player_id

    def is_wheel_chair(self):
        return self.skin_id == gconst.TRANS_WHEELCHAIR_ITEM_ID