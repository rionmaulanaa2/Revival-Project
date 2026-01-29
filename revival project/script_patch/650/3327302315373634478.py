# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaModuleBuff.py
from __future__ import absolute_import
from __future__ import print_function
import six
from ..UnitCom import UnitCom

class ComMechaModuleBuff(UnitCom):
    BIND_EVENT = {'E_MECHA_MODULE_EFFECT_ACTIVATE': '_module_efx_activate',
       'E_MECHA_MODULE_EFFECT_DEACTIVATE': '_module_efx_deactivate',
       'G_MECHA_MODULE_EFFECTIVE_DATA_RO': '_get_effective_data_ro'
       }

    def __init__(self):
        super(ComMechaModuleBuff, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaModuleBuff, self).init_from_dict(unit_obj, bdict)
        self._module_buff_in_effect = {}
        module_buff_in_effect = bdict.get('module_buff_data', {})
        for card_id, buff_params in six.iteritems(module_buff_in_effect):
            self._module_efx_activate(card_id, buff_params)

    def _get_effective_data_ro(self):
        return self._module_buff_in_effect

    def _is_ctrled_by_avatar(self):
        return self.sd.ref_driver_id and global_data.player and self.sd.ref_driver_id == global_data.player.id

    def _get_driver_l(self):
        if not self.sd.ref_driver_id:
            return None
        else:
            from mobile.common.EntityManager import EntityManager
            ent = EntityManager.getentity(self.sd.ref_driver_id)
            if ent and ent.logic:
                return ent.logic
            return None
            return None

    @staticmethod
    def to_event_data(data_in_comp):
        start_ts = data_in_comp.get('add_time', 0)
        duration = data_in_comp.get('duration', 0)
        duration_changeable = data_in_comp.get('duration_changeable', False)
        if not duration_changeable:
            duration_for_event = duration
        else:
            duration_for_event = -1
        return (
         start_ts, duration_for_event)

    def _module_efx_activate(self, card_id, buff_params):
        driver_l = self._get_driver_l()
        if driver_l is not None:
            cur_module_config = driver_l.ev_g_mecha_all_installed_module()
            from logic.gutils.mecha_module_utils import get_module_card_slot
            slot = get_module_card_slot(card_id)
            if slot in cur_module_config:
                _, slot_item_id = cur_module_config[slot]
                _, card_lv = driver_l.ev_g_module_item_slot_lv(slot_item_id)
            else:
                card_lv = None
        else:
            card_lv = None
        if card_lv is None:
            if global_data.is_inner_server:
                print('can not get card lv', card_id)
            return
        else:
            buff_id = buff_params.get('buff_id')
            duration = buff_params.get('duration', 0)
            duration_changeable = buff_params.get('duration_changeable', False)
            if not duration_changeable and duration <= 0:
                return
            self._module_buff_in_effect[card_id] = (
             card_lv, buff_params)
            if self._is_ctrled_by_avatar():
                start_ts, duration_for_event = self.to_event_data(buff_params)
                global_data.emgr.battle_mecha_module_effective_change.emit(card_id, card_lv, True, start_ts, duration_for_event)
            return

    def _module_efx_deactivate(self, card_id):
        if card_id in self._module_buff_in_effect:
            del self._module_buff_in_effect[card_id]
        if self._is_ctrled_by_avatar():
            global_data.emgr.battle_mecha_module_effective_change.emit(card_id, -1, False, -1, -1)