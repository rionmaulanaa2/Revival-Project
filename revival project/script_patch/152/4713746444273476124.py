# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/BreakableAggregation.py
from __future__ import absolute_import
import math3d
from .NPC import FullCacheableNPC
from logic.gutils.scene_utils import is_break_obj, recycle_affiliate_break_models

class BreakableAggregation(FullCacheableNPC):

    def init_from_dict(self, bdict):
        self._data = {}
        for break_id, params in bdict.get('break_info', []):
            if not params or len(params) < 2:
                continue
            if not is_break_obj(break_id):
                continue
            if not (global_data.game_mode and global_data.game_mode.is_pve()):
                bpoint = math3d.vector(*params[0])
                if self.recycle_models(break_id, bpoint):
                    continue
                self.break_models(break_id, params)

    @classmethod
    def recycle_models(self, model_name, center_pos):
        scn = global_data.battle.get_scene()
        if scn:
            old_model = scn.get_model(model_name)
            recycle_affiliate_break_models(scn, model_name, center_pos)
            if old_model:
                world_pos = old_model.world_position
                old_model.destroy()
                if not (global_data.game_mode and global_data.game_mode.is_pve()):
                    scn.del_model_in_cache(model_name, world_pos)
                scn.add_filter_model_name(model_name)
                if hasattr(scn, 'enable_indices_by_name'):
                    scn.enable_indices_by_name(model_name, False)

    @classmethod
    def break_models(self, bid, params):
        bpoint = params[0]
        bnormal = params[1]
        if bid and bpoint and bnormal:
            break_item_info = {'model_col_name': bid,'point': math3d.vector(*bpoint),
               'normal': math3d.vector(*bnormal),
               'power': None,
               'break_type': None
               }
            global_data.emgr.scene_add_break_objs.emit([break_item_info], False)
        return