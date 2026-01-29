# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_rocket_gravity_switch/ComRocketGravitySwitchAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.client.ComBaseModelAppearance import ComBaseModelAppearance
import math3d
import collision
import render
import game3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr

class ComRocketGravitySwitchAppearance(ComBaseModelAppearance):
    TRI_RADIUS = 5
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_CHECK_ENTER_CONSOLOE_ZONE': '_check_enter_zone'
       })

    def __init__(self):
        super(ComRocketGravitySwitchAppearance, self).__init__()
        self._trigger_radius = self.TRI_RADIUS * NEOX_UNIT_SCALE
        self.lplayer = None
        self.effect_id = None
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
        super(ComRocketGravitySwitchAppearance, self).destroy()
        self.process_event(False)

    def init_from_dict(self, unit_obj, bdict):
        super(ComRocketGravitySwitchAppearance, self).init_from_dict(unit_obj, bdict)
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, lplayer):
        if lplayer is None:
            return
        else:
            self.lplayer = lplayer
            return

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rot = bdict.get('rot', [0, 0, 0, 1])
        model_path = 'model_new/scene/box/box_01.gim'
        return (
         model_path, None, (pos, rot, bdict))

    def on_load_model_complete(self, model, userdata):
        pos, rot = userdata[0], userdata[1]
        pos = math3d.vector(pos[0], pos[1], pos[2])
        model.world_position = pos
        from logic.gcommon.common_utils.building_utils import get_bounding_box_slope_rot_mat
        rot_mat = get_bounding_box_slope_rot_mat(model, 1.0)
        model.rotation_matrix = rot_mat
        model.visible = False
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner())
        pos.y += 20
        self.effect_id = global_data.sfx_mgr.create_sfx_in_scene('effect/fx/scenes/common/fashecang/fx_huojian_fashe_09.sfx', pos)

    def on_model_destroy(self):
        global_data.emgr.scene_del_console.emit(self.unit_obj.id)
        self.effect_id and global_data.sfx_mgr.remove_sfx_by_id(self.effect_id)
        self.effect_id = None
        return

    def _check_enter_zone(self, pos):
        if self.model:
            model_pos = self.model.world_position
            lpos = pos - model_pos
            length = lpos.length
            if length <= self._trigger_radius:
                return (True, length)
        return (False, None)