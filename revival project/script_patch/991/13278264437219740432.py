# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_concert_arena/ComConcertArenaAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.client.ComBaseModelAppearance import ComBaseModelAppearance
from logic.gcommon.const import NEOX_UNIT_SCALE
import math3d
import collision
import render
import game3d
import world
from common.cfg import confmgr

class ComConcertArenaAppearance(ComBaseModelAppearance):
    TRI_RADIUS = 5
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_CHECK_ENTER_CONSOLOE_ZONE': '_check_enter_zone'
       })

    def __init__(self):
        super(ComConcertArenaAppearance, self).__init__()
        self._trigger_radius = self.TRI_RADIUS * NEOX_UNIT_SCALE
        self.lplayer = None
        self.ui_nd = None
        self.space_node = None
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_player_setted_event': self.on_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        super(ComConcertArenaAppearance, self).destroy()
        self.process_event(False)

    def init_from_dict(self, unit_obj, bdict):
        super(ComConcertArenaAppearance, self).init_from_dict(unit_obj, bdict)
        self._building_no = bdict.get('building_no', None)
        self.on_player_setted(global_data.cam_lplayer)
        return

    def on_player_setted(self, lplayer):
        if lplayer is None:
            return
        else:
            self.lplayer = lplayer
            return

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rot = bdict.get('rot', [0, 0, 0, 1])
        model_path = confmgr.get('c_building_res', str(self._building_no), 'ResPath', default='')
        return (
         model_path, None, (pos, rot, bdict))

    def on_load_model_complete(self, model, userdata):
        pos, rot = userdata[0], userdata[1]
        pos = math3d.vector(pos[0], pos[1], pos[2])
        model.world_position = pos
        from logic.gcommon.common_utils.building_utils import get_bounding_box_slope_rot_mat
        rot_mat = get_bounding_box_slope_rot_mat(model, 1.0)
        model.rotation_matrix = rot_mat
        model.active_collision = True
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner())
        self.ui_nd = global_data.uisystem.load_template_create('battle_arena/i_arena_ui_sign')
        from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
        space_node = CCUISpaceNode.Create()
        space_node.setLocalZOrder(0)
        space_node.AddChild('', self.ui_nd)

        def vis_callback(last_need_draw, cur_need_draw):
            if self.ui_nd and self.ui_nd.isValid():
                self.ui_nd.setVisible(bool(cur_need_draw))
            else:
                self.ui_nd.setVisible(False)

        space_node.set_visible_callback(vis_callback)
        self.ui_nd.setPosition(0, 0)
        xuetiao_pos = model.get_socket_matrix('fx_head', world.SPACE_TYPE_WORLD)
        space_node.set_assigned_world_pos(xuetiao_pos.translation)
        self.space_node = space_node

    def on_model_destroy(self):
        global_data.emgr.scene_del_console.emit(self.unit_obj.id)
        if self.space_node:
            self.space_node.Destroy()
        self.space_node = None
        self.ui_nd = None
        return

    def _check_enter_zone(self, pos):
        if self.model:
            model_pos = self.model.world_position
            lpos = pos - model_pos
            length = lpos.length
            if length <= self._trigger_radius:
                return (True, length)
        return (False, None)