# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComExplosiveContainerClient.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from common.cfg import confmgr
import math3d
import logic.gcommon.const as const
from logic.gcommon.common_const.sound_const import ATTACK_WEAPON_8003

class ComExplosiveContainerClient(UnitCom):
    BIND_EVENT = {'G_ALL_ATTACH_EXPLOSIVE': '_get_all_attach_explosive',
       'E_ATTACH_EXPLOSIVE': '_on_attach_explosive',
       'E_DETACH_EXPLOSIVE': '_on_detach_explosive'
       }

    def __init__(self):
        super(ComExplosiveContainerClient, self).__init__()
        self.mp_explosive = {}

    def init_from_dict(self, unit_obj, bdict):
        super(ComExplosiveContainerClient, self).init_from_dict(unit_obj, bdict)
        self.mp_explosive = bdict.get('mp_explosive', {})

    def on_init_complete(self):
        self.send_event('E_INIT_ATTACH_EXPLOSIVE')

    def _get_all_attach_explosive(self):
        return self.mp_explosive

    def _on_attach_explosive(self, item_info):
        uniq_key = item_info['uniq_key']
        if uniq_key in self.mp_explosive:
            return
        else:
            self.mp_explosive[uniq_key] = item_info
            ukey = item_info['uniq_key']
            eobj, einfo = global_data.emgr.scene_find_throw_item_event.emit(ukey)[0]
            if eobj and eobj.logic:
                model = self.ev_g_model()
                if model and model.valid:
                    eobj.logic.send_event('E_ON_ATTACH_EXPLOSIVE', model, item_info, self.unit_obj)
            item_type = item_info.get('item_itype', None)
            if item_type:
                self.play_attach_sound(item_info)
            return

    def _on_detach_explosive(self, uniq_key):
        if uniq_key not in self.mp_explosive:
            return
        item_info = self.mp_explosive.pop(uniq_key)
        self.send_event('E_ON_DETACH_EXPLOSIVE', item_info)

    def play_attach_sound(self, item_info):
        item_type = item_info['item_itype']
        if item_type in ATTACK_WEAPON_8003:
            pos_list = item_info['position']
            pos = math3d.vector(pos_list[0], pos_list[1], pos_list[2])
            global_data.sound_mgr.play_event('m_8003_weapon1_start_hit_3p', pos)