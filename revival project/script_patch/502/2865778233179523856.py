# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartCloud.py
from __future__ import absolute_import
from . import ScenePart
from common.cfg import confmgr
from logic.gcommon.common_const.scene_const import FOG_SKY_HEIGHT, FOG_GROUND_HEIGHT
import math
import copy
import common.utils.timer as timer
import world
import math3d
NORMAL_CLOUD_VISIBLE_HEIGHT_START = 2500.0
NORMAL_CLOUD_VISIBLE_HEIGHT_END = 2000.0
NEAR_CLOUD_VISIBLE_HEIGHT_START = 3500.0
NEAR_CLOUD_VISIBLE_HEIGHT_END = 2700.0
HEIGHT_ALLOWANCE = 10.0

class PartCloud(ScenePart.ScenePart):
    ENTER_EVENT = {'scene_tigger_auto_fog': 'trigger_active'
       }

    def __init__(self, scene, name):
        super(PartCloud, self).__init__(scene, name)
        self._timer = None
        self._last_height = -999999
        self._last_factor = -1.0
        self._auto_active = True
        return

    def trigger_active(self, active):
        self._auto_active = active
        self._last_factor = -1.0
        self.on_update()

    def on_enter(self):
        import game3d
        _T = lambda x: (
         x, game3d.calc_string_hash(x))
        STR_UV_SCALE, HASH_UV_SCALE = _T('u_uv_scale')
        STR_UV_SCALE2, HASH_UV_SCALE2 = _T('u_uv_scale2')
        STR_UV_MOVE, HASH_UV_MOVE = _T('u_uv_move')
        STR_UV_MOVE2, HASH_UV_MOVE2 = _T('u_uv_move2')
        STR_DISSOLVE, HASH_DISSOLVE = _T('u_dissolve')
        STR_FADE_INFO, HASH_FADE_INFO = _T('u_fade_info')
        STR_SCALE_INFO, HASH_SCALE_INFO = _T('u_scale_info')
        STR_VERTICAL_OFFSET, HASH_VERTICAL_OFFSET = _T('u_vertical_offset')
        cloud_model = confmgr.get('script_gim_ref')['sky_cloud']
        self._cloud_large = world.model(cloud_model, None)
        self._cloud_large2 = world.model(cloud_model, None)
        self._cloud_small = world.model(cloud_model, None)
        self._cloud_small2 = world.model(cloud_model, None)
        cam = self.scene().active_camera
        m = self._cloud_large
        m.visible = False
        m.inherit_flag = world.INHERIT_TRANSLATION
        m.position = math3d.vector(0, -500, 0)
        m.all_materials.set_var(HASH_UV_SCALE, STR_UV_SCALE, 0.5)
        m.all_materials.set_var(HASH_UV_SCALE2, STR_UV_SCALE2, 0.1)
        m.all_materials.set_var(HASH_UV_MOVE, STR_UV_MOVE, 0.01)
        m.all_materials.set_var(HASH_UV_MOVE2, STR_UV_MOVE2, 0.02)
        m.all_materials.set_var(HASH_DISSOLVE, STR_DISSOLVE, 0.65)
        m.all_materials.set_var(HASH_FADE_INFO, STR_FADE_INFO, (NORMAL_CLOUD_VISIBLE_HEIGHT_START, NORMAL_CLOUD_VISIBLE_HEIGHT_END + HEIGHT_ALLOWANCE, 5000.0, 15000.0))
        m.all_materials.set_var(HASH_SCALE_INFO, STR_SCALE_INFO, (NORMAL_CLOUD_VISIBLE_HEIGHT_START, NEAR_CLOUD_VISIBLE_HEIGHT_START, 10.0, 15.0))
        m.all_materials.set_var(HASH_VERTICAL_OFFSET, STR_VERTICAL_OFFSET, 0.0)
        m.set_parent(cam)
        m = self._cloud_large2
        m.visible = False
        m.inherit_flag = world.INHERIT_TRANSLATION
        m.position = math3d.vector(0, -500, 0)
        m.all_materials.set_var(HASH_UV_SCALE, STR_UV_SCALE, 0.3)
        m.all_materials.set_var(HASH_UV_SCALE2, STR_UV_SCALE2, 0.1)
        m.all_materials.set_var(HASH_UV_MOVE, STR_UV_MOVE, 0.03)
        m.all_materials.set_var(HASH_UV_MOVE2, STR_UV_MOVE2, 0.01)
        m.all_materials.set_var(HASH_DISSOLVE, STR_DISSOLVE, 0.65)
        m.all_materials.set_var(HASH_FADE_INFO, STR_FADE_INFO, (NORMAL_CLOUD_VISIBLE_HEIGHT_START, NORMAL_CLOUD_VISIBLE_HEIGHT_END + HEIGHT_ALLOWANCE, 5000.0, 15000.0))
        m.all_materials.set_var(HASH_SCALE_INFO, STR_SCALE_INFO, (NORMAL_CLOUD_VISIBLE_HEIGHT_START, NEAR_CLOUD_VISIBLE_HEIGHT_START, 10.0, 15.0))
        m.all_materials.set_var(HASH_VERTICAL_OFFSET, STR_VERTICAL_OFFSET, 250.0)
        m.set_parent(cam)
        m = self._cloud_small
        m.visible = False
        m.inherit_flag = world.INHERIT_TRANSLATION
        m.position = math3d.vector(0, -500, 0)
        m.all_materials.set_var(HASH_UV_SCALE, STR_UV_SCALE, 0.5)
        m.all_materials.set_var(HASH_UV_SCALE2, STR_UV_SCALE2, 0.2)
        m.all_materials.set_var(HASH_UV_MOVE, STR_UV_MOVE, 0.04)
        m.all_materials.set_var(HASH_UV_MOVE2, STR_UV_MOVE2, 0.08)
        m.all_materials.set_var(HASH_DISSOLVE, STR_DISSOLVE, 0.6)
        m.all_materials.set_var(HASH_FADE_INFO, STR_FADE_INFO, (NEAR_CLOUD_VISIBLE_HEIGHT_START, NEAR_CLOUD_VISIBLE_HEIGHT_END + HEIGHT_ALLOWANCE, 5000.0, 15000.0))
        m.all_materials.set_var(HASH_SCALE_INFO, STR_SCALE_INFO, (NEAR_CLOUD_VISIBLE_HEIGHT_START, NEAR_CLOUD_VISIBLE_HEIGHT_END, 4.0, 4.0))
        m.all_materials.set_var(HASH_VERTICAL_OFFSET, STR_VERTICAL_OFFSET, 0.0)
        m.set_parent(cam)
        m = self._cloud_small2
        m.visible = False
        m.inherit_flag = world.INHERIT_TRANSLATION
        m.position = math3d.vector(0, -500, 0)
        m.all_materials.set_var(HASH_UV_SCALE, STR_UV_SCALE, 0.1)
        m.all_materials.set_var(HASH_UV_SCALE2, STR_UV_SCALE2, 0.3)
        m.all_materials.set_var(HASH_UV_MOVE, STR_UV_MOVE, 0.05)
        m.all_materials.set_var(HASH_UV_MOVE2, STR_UV_MOVE2, 0.1)
        m.all_materials.set_var(HASH_DISSOLVE, STR_DISSOLVE, 0.6)
        m.all_materials.set_var(HASH_FADE_INFO, STR_FADE_INFO, (NEAR_CLOUD_VISIBLE_HEIGHT_START, NEAR_CLOUD_VISIBLE_HEIGHT_END + HEIGHT_ALLOWANCE, 5000.0, 15000.0))
        m.all_materials.set_var(HASH_SCALE_INFO, STR_SCALE_INFO, (NEAR_CLOUD_VISIBLE_HEIGHT_START, NEAR_CLOUD_VISIBLE_HEIGHT_END, 4.0, 4.0))
        m.all_materials.set_var(HASH_VERTICAL_OFFSET, STR_VERTICAL_OFFSET, 250.0)
        m.set_parent(cam)
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.on_update, interval=0.1, mode=timer.CLOCK, strict=False)
        return

    def on_update(self):
        if not self._auto_active:
            return
        scn = self.scene()
        cam = scn.active_camera
        height = cam.world_position.y
        if math.isnan(height):
            return
        show_normal_cloud = height > NORMAL_CLOUD_VISIBLE_HEIGHT_END
        if self._cloud_large.visible != show_normal_cloud:
            self._cloud_large.visible = show_normal_cloud
        if self._cloud_large2.visible != show_normal_cloud:
            self._cloud_large2.visible = show_normal_cloud
        show_near_cloud = height > NEAR_CLOUD_VISIBLE_HEIGHT_END
        if self._cloud_small.visible != show_near_cloud:
            self._cloud_small.visible = show_near_cloud
        if self._cloud_small2.visible != show_near_cloud:
            self._cloud_small2.visible = show_near_cloud

    def on_exit(self):
        if self._timer is not None:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = None
        return