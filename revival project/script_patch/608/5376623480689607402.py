# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAgentCapsuleGhost.py
from __future__ import absolute_import
from ..UnitCom import UnitCom

class ComAgentCapsuleGhost(UnitCom):
    BIND_EVENT = {'E_AGENT_COIN_CHANGED': ('_on_agent_coin_changed', -1),
       'E_GET_CAPSULE': ('_on_get_capsule', -1),
       'G_AGENT_COIN': '_get_agent_coin',
       'G_CUR_CAPSULE': '_on_cur_capsule'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComAgentCapsuleGhost, self).init_from_dict(unit_obj, bdict)
        self._coin = bdict.get('coin', 0)
        self._cur_capsule = bdict.get('cur_capsule', None)
        return

    def _on_agent_coin_changed(self, coin_cnt, reason=None):
        delta = coin_cnt - self._coin
        self._coin = coin_cnt
        if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
            from logic.gcommon import const
            if delta > 0:
                if reason == const.SYS_ADD_COIN:
                    global_data.emgr.sys_award_coin_event.emit(delta)
                else:
                    global_data.emgr.agent_coin_get_event.emit(delta, reason)

    def _on_get_capsule(self, capsule_id):
        self._cur_capsule = capsule_id

    def _on_cur_capsule(self):
        return self._cur_capsule

    def _get_agent_coin(self):
        return self._coin