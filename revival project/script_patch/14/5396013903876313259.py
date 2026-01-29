# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartBoxManager.py
from __future__ import absolute_import
from common.cfg import confmgr
from common.framework import Singleton
from mobile.common.EntityManager import EntityManager
from logic.gcommon.item.item_const import SCENEBOX_ST_OPENED

class PartBoxManager(Singleton):
    ALIAS_NAME = 'box_mgr'

    def init(self):
        self.box_info = []
        self.sfx_ids = {}
        self.process_event(True)

    def on_finalize(self):
        self.process_event(False)
        for box in self.box_info:
            if not (box and box()):
                continue
            self.del_sfx(box().id)

        self.box_info = set()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_update_box_info_event': self.on_update_box_info,
           'scene_open_box_event': self.on_open_box
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_update_box_info(self, box_info):
        if self.box_info == box_info:
            return
        add_box = set(box_info) - set(self.box_info)
        del_box = set(self.box_info) - set(box_info)
        for box in add_box:
            if not (box and box()):
                continue
            if not box().model():
                continue
            if self.is_scene_box_open(box().id):
                continue
            conf = confmgr.get('box_res', str(box().data.get('item_id')), default={})
            sfx_path = conf.get('appear_sfx')
            if not sfx_path:
                continue
            self.del_sfx(box().id)
            sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, box().model().world_position)
            self.sfx_ids[box().id] = sfx_id

        for box in del_box:
            if not (box and box()):
                continue
            if not box().model():
                continue
            self.del_sfx(box().id)

        self.box_info = box_info

    def on_open_box(self, entity_id, ref_model, cnf_data):
        if self.is_scene_box_open(entity_id):
            return
        if not (ref_model and ref_model()):
            return
        conf = confmgr.get('box_res', str(cnf_data.get('item_id')), default={})
        sfx_path = conf.get('open_sfx')
        if not sfx_path:
            return
        self.del_sfx(entity_id)
        sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, ref_model().world_position)
        self.sfx_ids[entity_id] = sfx_id

    def del_sfx(self, entity_id):
        if entity_id in self.sfx_ids:
            global_data.sfx_mgr.remove_sfx_by_id(self.sfx_ids[entity_id])

    def is_scene_box_open(self, entity_id):
        return EntityManager.getentity(entity_id).logic.ev_g_scene_box_is_open()