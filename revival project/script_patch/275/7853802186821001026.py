# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapMagicMonsterWidget.py
from __future__ import absolute_import
from logic.comsys.map.map_widget.MapScaleInterface import CommonMapMark

class MapMagicMonsterWidget(CommonMapMark):

    def __init__(self, parent_nd, mark_no, is_deep, state, parent=None, require_follow_model=False):
        super(MapMagicMonsterWidget, self).__init__(parent_nd, mark_no, is_deep, state, parent, require_follow_model)
        self._is_bind_event = False
        self.process_event(True)
        self.region_id = None
        self.set_node_visible(False)
        return

    def destroy(self):
        self.process_event(False)
        super(MapMagicMonsterWidget, self).destroy()

    def on_set_v3d_pos(self, v3d_pos):
        super(MapMagicMonsterWidget, self).on_set_v3d_pos(v3d_pos)
        if global_data.magic_sur_battle_mgr:
            region_id = global_data.magic_sur_battle_mgr.get_region_by_pos(v3d_pos)
            if region_id is None:
                log_error('there is a magic monster point can not find its belonging magic circle', v3d_pos)
            else:
                self.region_id = region_id
                self.on_notify_inside_magic_region_id()
        return

    def process_event(self, is_bind):
        if self._is_bind_event == is_bind:
            return
        emgr = global_data.emgr
        econf = {'notify_inside_magic_region_id': self.on_notify_inside_magic_region_id
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self._is_bind_event = is_bind

    def on_notify_inside_magic_region_id(self, *args):
        if not global_data.magic_sur_battle_mgr:
            return
        else:
            region_id = global_data.magic_sur_battle_mgr.get_player_region()
            if region_id is not None and region_id == self.region_id:
                self.set_node_visible(True)
            else:
                self.set_node_visible(False)
            return