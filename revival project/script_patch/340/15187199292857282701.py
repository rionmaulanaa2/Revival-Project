# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_scene_spray/ComSprayAppearance.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
from common.cfg import confmgr
from logic.gcommon.time_utility import time
import render
import math3d
DEFAULT_SPRAY_PATH = ''
SPRAY_SFX_PATH = 'effect/fx/common/spray/spray_1.sfx'
DEFAULT_TEXTURE_PATH = 'effect/fx/common/spray/default.png'
SPRAY_SFX_PATTERN = 'effect/fx/spray/%d.sfx'
DEFAULT_DURATION = 10

class ComSprayAppearance(UnitCom):

    def __init__(self):
        super(ComSprayAppearance, self).__init__()
        self.create_time = 0
        self.last_time = 0
        self.sfx_id = -1
        self.sfx_position = None
        self.sfx_rotation_euler = None
        self.sfx_rotation_matrix = None
        self.sfx_diffuse_path = None
        self.spray_idx = -1
        self.create_timestamp = 0
        self.last_duration = 0
        self.rel_duration = 0
        self.sfx_scale = math3d.vector(1, 1, 1)
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComSprayAppearance, self).init_from_dict(unit_obj, bdict)
        pos_list = bdict.get('position', [0, 0, 0])
        euler_list = bdict.get('euler_rotation', [0, 0, 0])
        self.sfx_position = math3d.vector(*pos_list)
        self.sfx_rotation_euler = math3d.vector(*euler_list)
        self.sfx_rotation_matrix = math3d.euler_to_matrix(self.sfx_rotation_euler)
        self.spray_idx = bdict.get('spray_id', 0)
        self.sfx_diffuse_path = DEFAULT_SPRAY_PATH
        self.create_timestamp = bdict.get('create_time', time())
        spray_items_conf = confmgr.get('spray_conf', 'SprayConfig', 'Content')
        spray_item = spray_items_conf.get(str(self.spray_idx), {})
        self.last_duration = spray_item.get('duration', DEFAULT_DURATION)
        self.rel_duration = self.last_duration - (time() - self.create_timestamp)
        self.sfx_diffuse_path = DEFAULT_TEXTURE_PATH
        if self.rel_duration > 0:
            self.load_spray()

    def get_sfx_path_by_spray_id(self, spray_idx):
        return SPRAY_SFX_PATTERN % spray_idx

    def load_spray(self):
        sfx_path = self.get_sfx_path_by_spray_id(self.spray_idx) or SPRAY_SFX_PATH
        self.sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, self.sfx_position, self.rel_duration, self.on_create_spray_complete, ex_data={'allow_overlay': True})

    def on_create_spray_complete(self, sfx, *args):
        sfx.world_rotation_matrix = self.sfx_rotation_matrix
        spray_items_conf = confmgr.get('spray_conf', 'SprayConfig', 'Content')
        scale_num = spray_items_conf.get(str(self.spray_idx), {}).get('scale', 1.0)
        sfx.scale = math3d.vector(scale_num, scale_num, scale_num)
        decal_sfx_info = global_data.sfx_mgr.get_dynamic_decal_sfx_info()
        MIN_DECAL_BIAS = 0
        cnt_max_decal_bias = MIN_DECAL_BIAS
        sprite_radius = sfx.get_sub_sprite_radius(0) * sfx.scale.x
        for k, v in six.iteritems(decal_sfx_info):
            if not k.valid:
                continue
            if not k.is_sub_decal(0):
                continue
            cmp_radius = k.get_sub_sprite_radius(0) * k.scale.x
            distance = (sfx.world_position - k.world_position).length
            if cmp_radius + sprite_radius >= distance:
                render_bias = k.render_bias
                cnt_max_decal_bias = max(cnt_max_decal_bias, render_bias)

        sfx.render_bias = min(31, cnt_max_decal_bias + 1)

    def _destroy_spray(self):
        global_data.sfx_mgr.remove_sfx_by_id(self.sfx_id)

    def destroy(self):
        self._destroy_spray()
        super(ComSprayAppearance, self).destroy()