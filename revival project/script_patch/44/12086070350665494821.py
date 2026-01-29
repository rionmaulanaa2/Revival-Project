# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartPickableModelManager.py
from __future__ import absolute_import
from common.framework import Singleton

class PartPickableModelManager(Singleton):
    ALIAS_NAME = 'pickable_model_mgr'

    def init(self):
        self.model_to_id = {}
        self.process_event(True)

    def on_finalize(self):
        self.process_event(False)
        self.model_to_id = {}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_add_pickable_model_event': self.on_add_model,
           'scene_del_pickable_model_event': self.on_del_model
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_add_model(self, model, ids, spawn_id):
        if not (model and model.valid):
            return
        self.model_to_id[str(model)] = ids

    def on_del_model(self, model, spawn_id):
        if not (model and model.valid):
            return
        if model in self.model_to_id:
            del self.model_to_id[str(model)]

    def get_model_entity_id(self, model):
        if not (model and model.valid):
            return []
        return self.model_to_id.get(str(model))