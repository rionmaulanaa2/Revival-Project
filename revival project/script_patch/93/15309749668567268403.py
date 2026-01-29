# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLobbyCockpit.py
from __future__ import absolute_import
COCKPIT_RES = 'model_new/cockpit/cockpit_01.gim'
from . import ScenePart
import world
import math3d
import math

class PartLobbyCockpit(ScenePart.ScenePart):
    INIT_EVENT = {'movie_sp_lobby_mecha_cam': 'on_sp_cam'
       }

    def __init__(self, scene, name):
        super(PartLobbyCockpit, self).__init__(scene, name, False)
        self.post_update_id = 0
        self.load_cockpit()

    def load_cockpit(self):
        self.model = world.model(COCKPIT_RES, None)
        return

    def on_enter(self):
        pass

    def load_cockpit_character(self):
        role_id = global_data.player.get_role()
        from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR
        item_data = global_data.player.get_item_by_no(role_id)
        fashion_data = item_data.get_fashion()
        dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
        head_id = fashion_data.get(FASHION_POS_HEADWEAR)
        from logic.gutils import dress_utils
        t_model = dress_utils.create_lobby_driver_model(role_id, dressed_clothing_id)
        self.model.bind('renwu', t_model)
        t_model.visible = True
        t_model.play_animation('inside_idle_8001', -1, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_LOOP)

    def on_update(self, dt):
        pass

    def do_update(self):
        camera = self.scene().active_camera
        cam_trans = camera.world_transformation
        self.model.world_position = cam_trans.translation
        target_trans = cam_trans.translation - self.model.get_socket_matrix('camera', world.SPACE_TYPE_WORLD).translation
        self.model.world_position = self.model.world_position + target_trans

    def on_exit(self):
        self.model.destroy()
        self.model = None
        global_data.game_mgr.get_post_logic_timer().unregister(self.post_update_id)
        super(PartLobbyCockpit, self).on_exit()
        return

    def on_sp_cam(self, parameter):
        self.load_cockpit_character()
        self.post_update_id = global_data.game_mgr.get_post_logic_timer().register(func=self.do_update, interval=1)
        self.scene().add_object(self.model)
        self.model.visible = True
        camera = self.scene().active_camera
        camera.z_range = (0.1, 20000)
        rotation = parameter.get('rotation', None)
        if rotation:
            rot = [ math.radians(i) for i in rotation ]
            camera.world_rotation_matrix = math3d.rotation_to_matrix(math3d.euler_to_rotation(math3d.vector(*rot)))
        fov = parameter.get('fov', None)
        if fov:
            camera.fov = fov
        cam_trans = camera.world_transformation
        self.model.world_transformation = cam_trans
        target_trans = cam_trans.translation - self.model.get_socket_matrix('camera', world.SPACE_TYPE_WORLD).translation
        self.model.world_position = self.model.world_position + target_trans
        return