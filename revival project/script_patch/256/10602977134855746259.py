# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/NeoXSceneUI.py
from __future__ import absolute_import
from __future__ import print_function
import world
import math3d
import cocosui
from common.utils.cocos_utils import getDesignScreenSize
CAMERA_SCALE = 10

class NeoXSceneUI(object):
    scene = None
    logic_timer_id = None
    ORTHO_VIEW_DEPTH = 300.0

    @classmethod
    def attach_scene(cls, scene=None, use_active_scene_light=False):
        if scene:
            cls.scene = scene
        if not cls.scene:
            ui_scene = world.scene()
            cls.scene = ui_scene
            ui_camera = ui_scene.create_camera(True)
            ui_camera.set_placement(math3d.vector(0, 0, -cls.ORTHO_VIEW_DEPTH / 2), math3d.vector(0, 0, 1), math3d.vector(0, 1, 0))
            winSize = getDesignScreenSize()
            ui_camera.set_ortho(winSize.width / CAMERA_SCALE, winSize.height / CAMERA_SCALE, 0, cls.ORTHO_VIEW_DEPTH)
            cls.set_up_light(use_active_scene_light)
            tm = global_data.game_mgr.get_logic_timer()
            cls.logic_timer_id = tm.register(func=cls.logic_func)
        ret = cocosui.render_step.attach_render_step(cls.scene)
        if ret == -1:
            print('attach_scene error')
            return

    @classmethod
    def set_up_light(cls, use_active_scene_light):
        if not use_active_scene_light:
            return
        else:
            active_scene = world.get_active_scene()
            if not getattr(active_scene, 'get_light_group', None):
                return
            all_lights = active_scene.get_light_group()
            for one_src_light in all_lights:
                one_dest_light = cls.scene.create_light(one_src_light.type)
                one_dest_light.direction = one_src_light.direction
                one_dest_light.ambient = one_src_light.ambient
                one_dest_light.diffuse = one_src_light.diffuse
                one_dest_light.specular = 4291611852L
                center, radius = one_src_light.get_shadow_caster_info()
                one_dest_light.set_shadow_caster_info(center, radius)
                one_dest_light.shadow_quality = one_src_light.shadow_quality
                one_dest_light.shadow_bias = one_src_light.shadow_bias
                one_dest_light.intensity = one_src_light.intensity
                one_dest_light.enable_lit = one_src_light.enable_lit

            return

    @classmethod
    def logic_func(cls, *args):
        cls.scene.update()

    @classmethod
    def detach_scene(cls):
        cocosui.render_step.detach_all_render_steps()

    @classmethod
    def remove_neox_node(cls, node):
        node.remove_from_parent()

    @classmethod
    def add_neox_node(cls, node):
        if cls.scene:
            cls.scene.add_object(node)

    @classmethod
    def destroy(cls):
        cls.detach_scene()
        cls.scene = None
        tm = global_data.game_mgr.get_logic_timer()
        if cls.logic_timer_id:
            tm.unregister(cls.logic_timer_id)
        cls.logic_timer_id = None
        return