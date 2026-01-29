# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrackMissileAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
from common.cfg import confmgr
import math3d

class ComTrackMissileAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ROTATION': '_on_rotation_changed',
       'G_YAW': '_get_yaw'
       })
    UP = math3d.vector(0, 1, 0)

    def __init__(self):
        super(ComTrackMissileAppearance, self).__init__()
        self.item_id = None
        self.conf = None
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_from_dict(self, unit_obj, bdict):
        super(ComTrackMissileAppearance, self).init_from_dict(unit_obj, bdict)
        self.item_id = bdict.get('robot_no', 90151031)
        self.conf = confmgr.get('explosive_robot_conf', 'RobotConfig', 'Content', str(self.item_id))
        self.gobj = global_data.sound_mgr.register_game_obj('TrackMissile')
        self.sound_id = None
        return

    def _on_rotation_changed(self, mat):
        self._model.world_rotation_matrix = mat

    def _get_yaw(self):
        return self._model.world_rotation_matrix.yaw

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        forward = math3d.vector(*bdict.get('dir', [0, 0, 0]))
        forward.normalize()
        data = {'pos': math3d.vector(*pos),'forward': forward,'scale': self.conf.get('model_scale')}
        model_path = self.conf.get('model')
        return (
         model_path, None, data)

    def on_load_model_complete(self, model, data):
        pos = data['pos']
        model.position = pos
        forward = data['forward']
        mat = math3d.matrix.make_orient(forward, self.UP)
        model.rotation_matrix = mat
        scale = data['scale']
        model.scale = math3d.vector(scale, scale, scale)
        sfx_path = self.conf.get('create_sfx', None)
        if sfx_path:
            sfx_scale = self.conf.get('create_sfx_scale', 1.0)

            def cb(sfx):
                sfx.scale = math3d.vector(sfx_scale, sfx_scale, sfx_scale)

            global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=cb)
        event = self.conf.get('create_event', None)
        if event:
            global_data.sound_mgr.play_event(event, pos)
        return

    def tick(self, dt):
        pass

    def stop_sound(self):
        if self.sound_id:
            global_data.sound_mgr.stop_playing_id(self.sound_id)
            self.sound_id = None
        if self.gobj:
            global_data.sound_mgr.unregister_game_obj(self.gobj)
            self.gobj = None
        return

    def destroy(self):
        self.process_event(False)
        self.stop_sound()
        super(ComTrackMissileAppearance, self).destroy()