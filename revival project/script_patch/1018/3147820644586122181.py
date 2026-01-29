# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDataAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.share.ComDataBase import ComDataBase
from ..system import ComSystemMgr

class ComDataAppearance(ComDataBase):
    BIND_EVENT = {'E_HUMAN_MODEL_LOADED': 'on_model_loaded',
       'E_SWITCH_MODEL': 'on_switch_model'
       }

    def __init__(self):
        super(ComDataAppearance, self).__init__(False)
        self.model = None
        self.force_sync_once = False
        return

    def get_share_data_name(self):
        return 'ref_appearance'

    def init_from_dict(self, unit_obj, bdict):
        self.model = None
        super(ComDataAppearance, self).init_from_dict(unit_obj, bdict)
        return

    def _do_cache(self):
        self.model = None
        return

    def _do_destroy(self):
        self.model = None
        return

    def on_model_loaded(self, model, userdata):
        self.model = model
        self.model.world_rotation_matrix = self.sd.ref_rotatedata.rotation_mat
        self.activate_ecs()

    def on_switch_model(self, model):
        self.model = model
        self.model.world_rotation_matrix = self.sd.ref_rotatedata.rotation_mat