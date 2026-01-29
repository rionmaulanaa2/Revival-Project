# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComClientSynchronizer.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.utility import dummy_cb
from logic.gcommon.time_utility import get_time, time
from mobile.common.EntityManager import EntityManager
from ..proto.client import call as nca_method
import logic.gcommon.common_utils.idx_utils as idx_utils
import logic.gcommon.common_utils.bcast_utils as bcast_utils
import six
SYNC_CLIENT_SNAPSHOT_ITVL = 2
MAX_LOSE_MONITOR_CNT = 20
MID_LOSE_MONITOR_CNT = 10

class ComClientSynchronizer(UnitCom):
    BIND_EVENT = {'G_ENABLE_SYNC': 'is_sync_enable',
       'E_ENABLE_SYNC': 'enable',
       'E_DO_SYNC_METHOD': 'do_sync_method',
       'E_BCAST_OFFLINE_MONITOR': 'bcast_offline_monitor',
       'E_ON_LOSE_CONNECT': 'on_lose_connect',
       'E_ON_AOI_ID_CHANGED': 'on_aoi_id_changed'
       }

    def __init__(self):
        super(ComClientSynchronizer, self).__init__()
        self._sync_method = dummy_cb
        self._sync_method_misty = dummy_cb
        self._enable_sync = False
        self._is_avatar = False
        self._bcast_monitor = []
        self._last_mileage_time = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComClientSynchronizer, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_sync_method = self.do_sync_method
        battle = self.battle
        aoi_id = battle.get_entity_aoi_id(unit_obj.id)
        if aoi_id is not None and aoi_id > 0:
            self._sync_id = aoi_id
        else:
            self._sync_id = str(unit_obj.id)
        self._sync_method = battle.sync_logic_entity
        self._sync_method_misty = battle.sync_logic_entity_misty
        self._is_avatar = bdict.get('is_avatar', False)
        if bdict.get('enable_sync', False):
            self.enable(True)
        return

    def on_aoi_id_changed(self):
        battle = self.battle
        if not battle:
            return
        else:
            aoi_id = battle.get_entity_aoi_id(self.unit_obj.id)
            if aoi_id is not None and aoi_id > 0:
                self._sync_id = aoi_id
            else:
                self._sync_id = str(self.unit_obj.id)
            return

    def destroy(self):
        if self.sd.ref_sync_method:
            self.sd.ref_sync_method = None
        self.enable(False)
        self._sync_method = dummy_cb
        self._sync_method_misty = dummy_cb
        self._bcast_monitor = []
        super(ComClientSynchronizer, self).destroy()
        return

    def cache(self):
        self.sd.ref_sync_method = None
        self.enable(False)
        self._sync_method = dummy_cb
        self._sync_method_misty = dummy_cb
        self._bcast_monitor = []
        super(ComClientSynchronizer, self).cache()
        return

    def bcast_offline_monitor(self, offline_monitor, offline_id, offline_ename):
        if offline_monitor:
            self._bcast_monitor.append((offline_id, offline_ename))
        else:
            for idx, _id in enumerate(self._bcast_monitor):
                if _id == offline_id:
                    del self._bcast_monitor[idx]
                    break

        if len(self._bcast_monitor) > MAX_LOSE_MONITOR_CNT:
            self._bcast_monitor = self._bcast_monitor[-MID_LOSE_MONITOR_CNT:]

    def on_lose_connect(self):
        for _id, offline_ename in self._bcast_monitor:
            self.send_event(offline_ename)

        self._bcast_monitor = []

    def set_interval(self, interval):
        pass

    def enable(self, enable):
        if self._enable_sync == enable:
            return
        self._enable_sync = enable
        self.reset()
        if enable:
            self.regist_event('E_CALL_SYNC_METHOD', self.call_sync_method)
            self.regist_event('E_CALL_SYNC_METHOD_MISTY', self.call_sync_method_misty)
        else:
            self.unregist_event('E_CALL_SYNC_METHOD', self.call_sync_method)
            self.unregist_event('E_CALL_SYNC_METHOD_MISTY', self.call_sync_method_misty)

    def is_sync_enable(self):
        return self._enable_sync

    def call_sync_method(self, method_name, parameters, immediate=False, include_self=False, broadcast=True, exclude=(), merge=None):
        method_name = idx_utils.s_method_2_idx(method_name)
        self._sync_method(self._sync_id, method_name, parameters)

    def call_sync_method_misty(self, method_name, parameters):
        method_name = idx_utils.s_method_2_idx(method_name)
        self._sync_method_misty(self._sync_id, method_name, parameters)

    def do_sync_method(self, method_name, parameters):
        nca_method(method_name, self, parameters)