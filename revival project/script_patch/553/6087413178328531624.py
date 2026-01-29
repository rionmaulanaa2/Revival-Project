# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaControlBtn/MechaWeaponMovable.py
from __future__ import absolute_import

class MechaWeaponMovable(object):

    def __init__(self, parent, nd_aprent, kargs):
        self.parent = parent
        self.nd_parent = nd_aprent
        if not global_data.move_rocker_simple:
            from logic.comsys.control_ui.MoveRockerUI import MoveRockerSimpleFunction
            MoveRockerSimpleFunction()
        self.simple_move_rocker = global_data.move_rocker_simple
        self.init_move_rocker()

    def destroy(self):
        self.parent.setOnBeginCallback(None)
        self.parent.setOnDragCallback(None)
        self.parent.setOnEndCallback(None)
        self.parent = None
        self.nd_parent = None
        self.simple_move_rocker = None
        return

    def bind_events(self, mecha):
        if self.simple_move_rocker:
            self.simple_move_rocker.on_player_setted(mecha)

    def unbind_events(self, mecha):
        pass

    def init_move_rocker(self):
        if not global_data.is_pc_mode:
            if self.simple_move_rocker:
                self.simple_move_rocker.update_rocker_size(self.parent.rocker.get_spawn_radius())

            def begin_cb(btn, touch):
                if self.simple_move_rocker:
                    self.simple_move_rocker.on_rocker_touch_begin(btn, touch)

            def move_cb(btn, touch):
                if self.simple_move_rocker:
                    self.simple_move_rocker.on_rocker_touch_drag(btn, touch, btn.GetMovedDistance())

            def end_cb(btn, touch):
                if self.simple_move_rocker:
                    self.simple_move_rocker.on_rocker_touch_end(btn, touch)

            if global_data.disable_action3_move_func:
                return
            self.parent.setOnBeginCallback(begin_cb)
            self.parent.setOnDragCallback(move_cb)
            self.parent.setOnEndCallback(end_cb)

    def refresh_rocker(self):
        if self.simple_move_rocker:
            self.simple_move_rocker.update_rocker_size(self.parent.rocker.get_spawn_radius())