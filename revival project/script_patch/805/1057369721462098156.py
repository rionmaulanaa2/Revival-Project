# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_base_appearance/ComLodBase.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
import device_compatibility
from logic.client.const import game_mode_const
from logic.gcommon.common_const import battle_const
from common.utils import pc_platform_utils
MAX_LOD_LEVEL = 4

class ComLodBase(UnitCom):
    LOD_UPDATE_INTERVAL = 0.5

    def __init__(self):
        super(ComLodBase, self).__init__()
        self._lod_config = None
        self._start_lod_level = 0
        self._cur_lod_level = 0
        self._to_lod_level = 0
        self._lod_update_last_time = 0
        self._lod_dist_list = [-1, -1, -1]
        self._lod_config = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComLodBase, self).init_from_dict(unit_obj, bdict)
        self.int_data()

    def int_data(self):
        pass

    def on_humman_model_load(self, model, user_data, *arg):
        pass

    def tick(self, delta):
        now = global_data.game_time
        if now - self._lod_update_last_time > self.LOD_UPDATE_INTERVAL:
            self.update_cur_lod()
            self._lod_update_last_time = now
            self.need_update = False

    def calc_lod_dist(self):
        import game3d
        if global_data.game_mgr.gds:
            quality = global_data.game_mgr.gds.get_actual_quality()
        else:
            quality = 0
        perf_flag = device_compatibility.get_device_perf_flag()
        if self.ev_g_is_avatar():
            camp_flag = 0
        elif global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate(self.unit_obj.ev_g_camp_id()):
            camp_flag = 1
        else:
            camp_flag = 2
        game_mode = global_data.game_mode.get_mode_type() if global_data.game_mode else None
        game_mode_idx = game_mode_const.get_game_mode_index(game_mode)
        if pc_platform_utils.is_pc_hight_quality_simple():
            index = ','.join([str(battle_const.PLAY_TYPE_CHICKEN), str(perf_flag), str(4), str(camp_flag)])
        else:
            index = ','.join([str(game_mode_idx), str(perf_flag), str(quality), str(camp_flag)])
        default_config = {'lod_0': -1,'lod_1': 20,'lod_2': 40,'lod_3': 60}
        quality_lod_config = self._lod_config.get(index, None)
        if quality_lod_config is None:
            subs_index = ','.join([str(battle_const.PLAY_TYPE_DEATH), str(perf_flag), str(quality), str(camp_flag)])
            quality_lod_config = self._lod_config.get(subs_index, default_config)
        for level in range(MAX_LOD_LEVEL):
            key = 'lod_' + str(level)
            dist = quality_lod_config[key]
            if dist >= 0:
                start_lod_level = level
                break

        lod_dist_list = []
        for level in range(start_lod_level, MAX_LOD_LEVEL):
            key = 'lod_' + str(level)
            dist = quality_lod_config[key] * NEOX_UNIT_SCALE
            lod_dist_list.append(dist)

        supply_len = 3 - len(lod_dist_list)
        supply_len = max(supply_len, 0)
        for _ in range(supply_len):
            lod_dist_list.append(-1)

        lod_dist_list = tuple(lod_dist_list)
        return (
         start_lod_level, lod_dist_list)

    def update_lod(self, lod_level):
        if lod_level >= len(self._lod_dist_list) or self._lod_dist_list[lod_level] < 0:
            return
        self._to_lod_level = lod_level
        if not self._need_update:
            self.need_update = True

    def update_cur_lod(self):
        if self._cur_lod_level == self._to_lod_level:
            return
        self._cur_lod_level = self._to_lod_level
        self.load_lod_model()

    def on_display_quality_change(self, quality):
        if self.ev_g_is_avatar():
            return
        model = self.ev_g_model()
        if not model:
            return
        start_lod_level, lod_dist_list = self.calc_lod_dist()
        self._start_lod_level = start_lod_level
        model.lod_config = lod_dist_list
        self._lod_dist_list = lod_dist_list
        self.load_lod_model()