# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapMechaSkillInfoWidget.py
from __future__ import absolute_import
from logic.gcommon.common_const.collision_const import GROUP_STATIC_SHOOTUNIT, WATER_GROUP, GROUP_CHARACTER_INCLUDE
import collision
import math3d
from six.moves import range
from logic.comsys.map.map_widget import MapScaleInterface
from mobile.common.EntityManager import EntityManager
from common.utils.cocos_utils import ccp
from common.utils.timer import CLOCK
import math

class MapMark(MapScaleInterface.MapScaleInterface):
    NODE_MARGIN = 12

    def __init__(self, parent_nd, ctrl_widget):
        super(MapMark, self).__init__(parent_nd)
        self._nd = global_data.uisystem.load_template_create('map/ccb_enemy_locate')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self._nd.setScale(1.0 / ctrl_widget.cur_map_scale)
        self.sp_dir = ccp(0, 1)

    def on_update(self, pos, is_hit):
        enemy_pos_3 = self.trans_world_position(pos)
        enemy_pos_2 = ccp(enemy_pos_3.x, enemy_pos_3.y)
        self.set_position(enemy_pos_2)
        if not is_hit:
            self._nd.icon_enemy.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/mech_attack/mech_8033/map/icon_mech_8033_enemy2.png')
        else:
            self._nd.icon_enemy.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/mech_attack/mech_8033/map/icon_mech_8033_enemy.png')


class MapMechaSkillInfoWidget:

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.enemy_widgets = []
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)
        self.clear_all_enemy()

    def clear_all_enemy(self):
        for widget in self.enemy_widgets:
            widget.destroy()

        self.enemy_widgets = []

    def get_scan_infos(self):
        scn = global_data.game_mgr.scene
        if scn:
            part_map = scn.get_com('PartMap')
            if part_map:
                return part_map.get_mecha_8033_scan_enemy()
        return []

    def update_nd_position(self):
        pos_infos = self.get_scan_infos()
        self.clear_all_enemy()
        if not pos_infos:
            return
        for pos, is_hit in pos_infos:
            widget = MapMark(self.parent_nd, self.map_panel)
            widget.on_update(pos, is_hit)
            self.enemy_widgets.append(widget)