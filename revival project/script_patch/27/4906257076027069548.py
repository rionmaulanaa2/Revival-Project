# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBreakableCollision.py
from __future__ import absolute_import
from .ComObjCollision import ComObjCollision

class ComBreakableCollision(ComObjCollision):

    def init_from_dict(self, unit, bdict):
        super(ComBreakableCollision, self).init_from_dict(unit, bdict)

    def on_model_load_complete(self, model):
        super(ComBreakableCollision, self).on_model_load_complete(model)
        global_data.emgr.scene_add_break_obj_event.emit(self._col_obj.cid, self.unit_obj)

    def on_model_destroy(self):
        if self._col_obj:
            global_data.emgr.scene_remove_break_obj_event.emit(self._col_obj.cid)