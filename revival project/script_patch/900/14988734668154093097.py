# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSelectionHuman.py
from __future__ import absolute_import
from .ComSelectionBase import ComSelectionBase
import math3d

class ComSelectionHuman(ComSelectionBase):
    BIND_EVENT = ComSelectionBase.BIND_EVENT.copy()
    BIND_EVENT.update({})

    def __init__(self):
        super(ComSelectionHuman, self).__init__()

    def _on_being_selected(self, id_selector, control_info):
        super(ComSelectionHuman, self)._on_being_selected(id_selector, control_info)
        model = self.ev_g_model()
        if not model:
            return
        else:
            self.do_model_binding(self.unit_obj.id, None, None)
            return

    def _on_losing_selected(self, control_info):
        c = self.unit_obj.get_com('ComHumanDriver')
        if c:
            c.need_update = False

    def do_model_binding(self, id_selector, mdl_controller, mdl_target):
        c = self.unit_obj.get_com('ComHumanDriver')
        if c and self.unit_obj.__class__.__name__ != 'LAvatar':
            c.need_update = False
            c.need_update = True
        model = self.ev_g_model()
        if not self.ev_g_is_pure_mecha():
            model.visible = True
        control_info = self.mp_holder.get(self.unit_obj.id, None)
        if not control_info:
            return
        else:
            v3d_pos = self.ev_g_position()
            if G_POS_CHANGE_MGR:
                self.notify_pos_change(v3d_pos, True)
            else:
                self.send_event('E_POSITION', v3d_pos)
            self.send_event('E_ENABLE_WATER_UPDATE', True)
            self.send_event('E_REFRESH_CUR_WATER_STATUS')
            if self.sd.ref_is_robot:
                self.send_event('E_RESUME_HUMAN_COLLISION')
                self.send_event('E_ON_SLECTION_HUMAN_BINDING')
            return