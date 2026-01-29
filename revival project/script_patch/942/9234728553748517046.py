# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapMutiOccupyWidget.py
from __future__ import absolute_import
import six
import six_ex
from logic.comsys.map.map_widget import MapScaleInterface
from logic.client.const import game_mode_const
from common.utils.cocos_utils import ccp
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.comsys.battle.MutiOccupy.MutiOccupyPoint import MutiOccupyPoint
from logic.comsys.battle.MutiOccupy.MutiOccupyPoint import TICK_TIME, PROG_ADD, PROG_SCALE, PARTID_TO_TEXT
from logic.gcommon.common_const.battle_const import OCCUPY_POINT_STATE_SNATCH
import math
from common.uisys.uielment.CCNode import CCNode

class PartMutiOccupyMapMark(MapScaleInterface.MapScaleInterface, MutiOccupyPoint):

    def __init__(self, parent_nd, ctrl_widget, part_id):
        MapScaleInterface.MapScaleInterface.__init__(self, parent_nd, ctrl_widget)
        self.map_panel = ctrl_widget
        self.part_id = part_id
        self._nd = global_data.uisystem.load_template_create('battle_control/i_control_map_icon')
        self.parent_nd.AddChild('', self._nd)
        self.sp_dir = ccp(0, 1)
        self.init_parameters()

    def init_base_data(self, base_data):
        self.position = base_data.get('c_center', [0, 0, 0])
        self.init_mark_pos()

    def update_occupy_state(self, data, is_init=False):
        if not self._nd or not self._nd.frame_blue:
            return
        super(PartMutiOccupyMapMark, self).update_occupy_state(data, is_init)
        if self.state == OCCUPY_POINT_STATE_SNATCH:
            self._nd.frame_blue.setVisible(True)
        else:
            self._nd.frame_blue.setVisible(False)

    def init_mark_pos(self):
        pos_3 = self.trans_world_position_ex(self.position)
        pos_2 = ccp(pos_3.x, pos_3.y)
        self.set_position(pos_2)
        self._nd.lab_name.SetString(PARTID_TO_TEXT[self.part_id])

    def destroy(self):
        if self._nd:
            self._nd.nd_cut.StopTimerAction()
            if self.is_nd_need_remove:
                if isinstance(self._nd, CCNode):
                    self._nd.Destroy()
                else:
                    self._nd.removeFromParent()
            self._nd = None
        if self.parent_nd:
            self.parent_nd = None
        if self.map_panel:
            self.map_panel.unregister_on_scale_listener(self)
            self.map_panel = None
        return


class MapMutiOccupyInfoWidget(object):

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.part_occupy_locate = {}
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_occupy_point_state': self.update_occupy_point_state
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)
        for key in six_ex.keys(self.part_occupy_locate):
            self.part_occupy_locate[key].destroy()

        self.part_occupy_locate = {}

    def update_occupy_point_state(self):
        if not global_data.death_battle_data or global_data.battle and global_data.battle.is_settle:
            return
        else:
            occupy_data = global_data.death_battle_data.occupy_data
            is_init = False
            for part_id, occupy in six.iteritems(occupy_data):
                server_data = occupy.get_occupy_server_data()
                base_data = occupy.get_occupy_base_data()
                locate_ui = self.part_occupy_locate.get(part_id, None)
                if not locate_ui:
                    locate_ui = PartMutiOccupyMapMark(self.parent_nd, self.map_panel, part_id)
                    locate_ui.init_server_data(server_data)
                    locate_ui.init_base_data(base_data)
                    self.parent_nd.AddChild('', locate_ui._nd)
                    self.part_occupy_locate[part_id] = locate_ui
                    is_init = True
                locate_ui.update_occupy_state(server_data, is_init=is_init)

            return