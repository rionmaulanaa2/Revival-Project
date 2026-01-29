# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Breakable.py
from __future__ import absolute_import
from .BaseClientEntity import BaseClientEntity
from common.cfg import confmgr
import math3d
from logic.gutils.scene_utils import is_break_obj, recycle_affiliate_break_models

class Breakable(BaseClientEntity):
    TIME_LIMIT = 2

    @classmethod
    def is_cacheable(self):
        return True

    @classmethod
    def init_from_dict(self, bdict):
        bid = bdict.get('break_id', None)
        parms = bdict.get('param', None)
        age = bdict.get('age', None)
        if not parms or len(parms) < 2:
            return
        else:
            if not bid:
                return
            if not is_break_obj(bid):
                return
            bpoint = parms[0]
            bnormal = parms[1]
            if age >= self.TIME_LIMIT and self.recycle_models(bid, math3d.vector(*bpoint)):
                return
            if bid and bpoint and bnormal:
                break_item_info = {'model_col_name': bid,'point': math3d.vector(*bpoint),
                   'normal': math3d.vector(*bnormal),
                   'power': None,
                   'break_type': None
                   }
                global_data.emgr.scene_add_break_objs.emit([break_item_info], False)
            return

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
                return True
        return False