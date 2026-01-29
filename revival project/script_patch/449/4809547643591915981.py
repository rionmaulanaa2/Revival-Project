# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMonsterMarkView.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.component.client.ComBaseMarkView import ComBaseMarkView
import world
import math3d

class ComMonsterMarkView(ComBaseMarkView):
    BIND_EVENT = dict(ComBaseMarkView.BIND_EVENT)
    BIND_EVENT.update({'E_HEALTH_HP_EMPTY': 'on_death'
       })

    def _is_cam_player(self, entity_id):
        return global_data.cam_lplayer and entity_id == global_data.cam_lplayer.id

    def _on_model_loaded(self, model):
        super(ComMonsterMarkView, self)._on_model_loaded(model)
        self.creat_marks()

    def get_mark_position(self):
        model = self.ev_g_model()
        pos = model.get_socket_matrix('xuetiao', world.SPACE_TYPE_LOCAL).translation
        pos.y = pos.y * model.scale.y
        return pos

    def on_death(self, *args, **kargs):
        self.clear_marks()