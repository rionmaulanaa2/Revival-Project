# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaMarkView.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.component.client.ComBaseMarkView import ComBaseMarkView
from logic.gcommon.common_const import buff_const as bconst
import math3d

class ComMechaMarkView(ComBaseMarkView):
    BIND_EVENT = dict(ComBaseMarkView.BIND_EVENT)
    BIND_EVENT.update({'E_ON_JOIN_MECHA': '_on_join_mecha',
       'E_ON_LEAVE_MECHA': '_on_leave_mecha',
       'E_SET_MECAH_MODE': ('_on_set_mecha_mode', 100)
       })

    def _is_cam_player(self, entity_id):
        playerid = self.sd.ref_driver_id
        return global_data.cam_lplayer and playerid == global_data.cam_lplayer.id

    def get_mark_position(self):
        return math3d.vector(0, 85, 0)

    def _on_model_loaded(self, model):
        super(ComMechaMarkView, self)._on_model_loaded(model)
        if self.unit_obj.__class__.__name__ == 'LMechaTrans':
            self.creat_marks()

    def _on_set_mecha_mode(self, *args):
        global_data.emgr.battle_afk_invincible_event.emit(self.ev_g_has_buff_by_id(bconst.BUFF_ID_AFK_INVINCIBLE), self.unit_obj.id)

    def _on_join_mecha(self, *args, **kargs):
        self.creat_marks()

    def _on_leave_mecha(self, *args, **kargs):
        self.send_event('E_CLEAR_CAMP')
        self.clear_marks()