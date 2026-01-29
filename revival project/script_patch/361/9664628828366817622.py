# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/pve/ComPveBless.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
from logic.gutils.pve_utils import get_all_elem_type
from logic.gcommon.common_const.pve_const import MECHA_DEFAULT_BLESS

class ComPveBless(UnitCom):
    BIND_EVENT = {'E_CHOOSE_BLESS': '_on_choose_bless',
       'E_REMOVE_BLESS': '_on_remove_bless',
       'E_RANDOM_CHOOSE_BLESS': '_on_random_choose_bless',
       'G_CHOOSED_BLESSES': '_get_choosed_blesses',
       'G_BLESS_LEVEL': '_get_bless_level',
       'E_ON_UPDATE_PVE_ICE': '_on_update_pve_ice',
       'G_PVE_ICE': '_get_pve_ice',
       'E_ON_CONTROL_TARGET_CHANGE': '_on_control_target_change'
       }

    def __init__(self):
        super(ComPveBless, self).__init__()
        self._choosed_blesses = {}
        self._ice_cnt = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComPveBless, self).init_from_dict(unit_obj, bdict)
        self._choosed_blesses = bdict.get('choosed_blesses', {})
        self._ice_cnt = bdict.get('ice_cnt', 0)

    def _get_choosed_blesses(self):
        return self._choosed_blesses

    def _get_bless_level(self, bless_id):
        return self._choosed_blesses.get(bless_id, 0)

    def _on_choose_bless(self, bless_id, add_level, notice=True):
        self._choosed_blesses.setdefault(bless_id, 0)
        self._choosed_blesses[bless_id] += add_level
        if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
            notice and global_data.emgr.pve_update_bless_event.emit(bless_id)
            global_data.emgr.pve_update_elem_list_event.emit(self._choosed_blesses)

    def _on_remove_bless(self, bless_id):
        if bless_id in self._choosed_blesses:
            del self._choosed_blesses[bless_id]
        if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
            global_data.emgr.pve_remove_bless_event.emit(bless_id)
            global_data.emgr.pve_update_elem_list_event.emit(self._choosed_blesses)

    def _on_random_choose_bless(self, bless_id, add_level):
        global_data.emgr.pve_random_choose_bless.emit(bless_id)

    def _on_update_pve_ice(self, ice_cnt):
        self._ice_cnt = ice_cnt
        if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
            global_data.emgr.pve_update_ice_cnt.emit(ice_cnt)

    def _get_pve_ice(self):
        return self._ice_cnt

    def _on_control_target_change(self, *args):
        ctarget = self.sd.ref_ctrl_target
        if not ctarget or not ctarget.logic:
            return
        my_mecha_id = ctarget.logic.ev_g_mecha_id()
        for mecha_id, bless_list in six.iteritems(MECHA_DEFAULT_BLESS):
            for bless in bless_list:
                if mecha_id == my_mecha_id and bless not in self._choosed_blesses:
                    self._on_choose_bless(bless, 1, notice=False)
                elif mecha_id != my_mecha_id and bless in self._choosed_blesses:
                    self._on_remove_bless(bless)