# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComParadropPlaneAppearance.py
from __future__ import absolute_import
import math3d
from logic.gcommon.common_utils.local_text import get_text_by_id
from .ComBaseModelAppearance import ComBaseModelAppearance
from logic.gcommon.common_const.scene_const import MODEL_PLANE_PATH

class ComParadropPlaneAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_REACH_DESTINATION': '_on_reach',
       'E_PATH_DESTROY': '_on_path_destroy'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComParadropPlaneAppearance, self).init_from_dict(unit_obj, bdict)
        owner_id = bdict.get('owner_id', None)
        land_point = bdict.get('land_point', (0, 0, 0))
        if owner_id:
            if not global_data.cam_lplayer:
                return
            if owner_id == global_data.cam_lplayer.id:
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(19020))
            else:
                land_pos = math3d.vector(*land_point)
                pos = global_data.cam_lplayer.ev_g_position()
                if pos and (pos - land_pos).length <= 3000:
                    global_data.emgr.battle_show_message_event.emit(get_text_by_id(19021))
        self.sound_mgr = global_data.sound_mgr
        self._sound_id = self.sound_mgr.register_game_obj('plane')
        self.sound_mgr.set_switch('plane', 'plane_3d', self._sound_id)
        self._sound_player_id = self.sound_mgr.post_event('Play_plane', self._sound_id)
        return

    def get_model_info(self, unit_obj, bdict):
        mpath = MODEL_PLANE_PATH
        return (
         mpath, None, None)

    def on_load_model_complete(self, model, userdata):
        model.scale = math3d.vector(0.5, 0.5, 0.5)
        direction = self.ev_g_direction()
        if direction:
            r = math3d.matrix.make_orient(direction, math3d.vector(0, 1, 0))
            model.world_rotation_matrix = r

    def on_model_destroy(self):
        if self._sound_player_id:
            self.sound_mgr.stop_playing_id(self._sound_player_id)
            self._sound_player_id = None
        self.sound_mgr.unregister_game_obj(self._sound_id)
        self._sound_id = None
        return

    def _on_reach(self, pos):
        return True

    def _on_path_destroy(self):
        self.battle.destroy_entity(self.unit_obj.id)

    def _on_pos_changed(self, pos):
        super(ComParadropPlaneAppearance, self)._on_pos_changed(pos)
        if self._sound_id:
            self.sound_mgr.set_position(self._sound_id, pos)