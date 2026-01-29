# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBreakable.py
from __future__ import absolute_import
from ..UnitCom import UnitCom

class ComBreakable(UnitCom):
    BIND_EVENT = {'E_EXPLODE': 'explode'
       }

    def __init__(self):
        super(ComBreakable, self).__init__()
        self._model_name = None
        return

    def init_from_dict(self, unit, bdict):
        super(ComBreakable, self).init_from_dict(unit, bdict)
        index = bdict.get('id', None)
        if index is not None:
            from common.cfg import confmgr
            break_info = confmgr.get('break_info', 'data')
            if index < len(break_info):
                self._model_name = break_info[index]['name']
        return

    def explode(self):
        import world
        from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_EXCLUDE
        if self._model_name:
            model = self.scene.get_model(self._model_name)
            if model:
                model.flag |= world.ENABLE_PHYSICS
                model.physics_enable = True
                model.set_mask_and_group(GROUP_CHARACTER_EXCLUDE, GROUP_CHARACTER_EXCLUDE)
                model.explode(model.world_position, 400, 500)