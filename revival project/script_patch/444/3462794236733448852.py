# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/Concert/LodObject.py
from __future__ import absolute_import
from six.moves import range
import game3d
from logic.gcommon.const import NEOX_UNIT_SCALE
MAX_LOD_LEVEL = 4

class LodObject(object):
    LOD_UPDATE_INTERVAL = 0.5

    def __init__(self):
        self._model = None
        self._start_lod_level = 0
        self._cur_lod_level = 0
        self._to_lod_level = 0
        self._lod_update_last_time = 0
        self._lod_dist_list = []
        self._load_mesh_task = None
        self._cur_res_path = None
        self._last_res_path = None
        self._need_update = False
        self._lod_config = None
        return

    def set_lod_model(self, model, sub_mesh_path, curl_lod_levl, lod_config):
        self._model = model
        start_lod_level, lod_dist_list = self.calc_lod_dist(lod_config)
        self._start_lod_level = start_lod_level
        self._lod_dist_list = lod_dist_list
        self._last_res_path = sub_mesh_path
        self._cur_res_path = sub_mesh_path
        self._lod_config = lod_config
        self._model.lod_config = lod_dist_list
        self._model.lod_callback = self.update_lod
        self._cur_lod_level = curl_lod_levl

    def calc_lod_dist(self, lod_config):
        for level in range(MAX_LOD_LEVEL):
            key = 'lod_' + str(level)
            dist = lod_config[key][0]
            if dist >= 0:
                start_lod_level = level
                break

        lod_dist_list = []
        for level in range(start_lod_level, MAX_LOD_LEVEL):
            key = 'lod_' + str(level)
            dist = lod_config[key][0] * NEOX_UNIT_SCALE
            lod_dist_list.append(dist)

        supply_len = 3 - len(lod_dist_list)
        supply_len = max(supply_len, 0)
        for _ in range(supply_len):
            lod_dist_list.append(-1)

        lod_dist_list = tuple(lod_dist_list)
        return (
         start_lod_level, lod_dist_list)

    def clear_lod_model(self):
        self._model = None
        return

    def update_lod(self, lod_level):
        if lod_level >= len(self._lod_dist_list) or self._lod_dist_list[lod_level] < 0:
            return
        self._to_lod_level = lod_level
        if not self._need_update:
            self._need_update = True

    def update_cur_lod(self):
        if self._cur_lod_level == self._to_lod_level:
            return
        self._cur_lod_level = self._to_lod_level
        self.load_lod_model()

    def tick(self):
        if self._model and self._need_update:
            now = global_data.game_time
            if now - self._lod_update_last_time > self.LOD_UPDATE_INTERVAL:
                self.update_cur_lod()
                self._lod_update_last_time = now
                self._need_update = False

    def load_lod_model(self):
        lod_name = self.get_lod_level_name()
        res_path = self.get_res_path()
        index = res_path.find('empty.gim')
        res_path = res_path[0:index] + lod_name + '.gim'
        if self._cur_res_path:
            self._last_res_path = self._cur_res_path
        self._cur_res_path = res_path
        self._load_mesh_task = global_data.model_mgr.create_mesh_async(self._load_mesh_task, res_path, self._model, self.on_load_mesh_completed, self.on_before_add_new_mesh, game3d.ASYNC_ULTIMATE_HIGH)

    def get_res_path(self):
        pass

    def get_lod_level_name(self):
        lod_level = self._start_lod_level + self._cur_lod_level
        lod_key = 'lod_' + str(lod_level)
        lod_name = self._lod_config[lod_key][1]
        if lod_name == 'l4':
            lod_name = 'l3'
        return lod_name

    def on_before_add_new_mesh(self, model):
        if self._last_res_path:
            model.remove_mesh(self._last_res_path)
            self._last_res_path = None
        return

    def on_load_mesh_completed(self, model):
        pass

    def destroy(self):
        self.clear_lod_model()