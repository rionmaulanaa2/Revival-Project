# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartJieMianCommon.py
from __future__ import absolute_import
from . import ScenePart
import math
import math3d
import world
from common.cfg import confmgr
from logic.gutils import lobby_model_display_utils
DefaultModels = [
 'shangcheng_beijing_template_01', 'shangcheng_jingzi_01', 'shangcheng_beijing_template_03', 'shangcheng_beijing_template_02', 'box_shangcheng_01']
DefaultSfxs = ['sfx_template_01']

def str_to_list(info_str):
    return [ float(x) for x in info_str.split(',') ]


class PartJieMianCommon(ScenePart.ScenePart):
    ENTER_EVENT = {'update_jiemian_scene_content': 'on_update_update_scene_content'
       }

    def __init__(self, scene, name):
        super(PartJieMianCommon, self).__init__(scene, name)
        self._scene_content_type = None
        self._new_scene_objs = []
        return

    def on_enter(self):
        for model_name in DefaultModels:
            d_model = self.scene().get_model(model_name)
            if d_model and d_model.valid:
                d_model.visible = False

        for sfx_name in DefaultSfxs:
            d_sfx = self.scene().get_sfx(sfx_name)
            if d_sfx:
                d_sfx.visible = False

    def on_update_update_scene_content(self, scene_type, scene_content_type):
        if self.scene().scene_type == scene_type and scene_content_type and self._scene_content_type != scene_content_type:
            self._scene_content_type = scene_content_type
            for obj in self._new_scene_objs:
                obj.destroy()

            self._new_scene_objs = []
            global_data.emgr.change_model_display_scene_item.emit(None)
            content_cnf = confmgr.get('scene_content_config', str(scene_content_type))
            model_list = content_cnf.get('models')
            for info in model_list:
                model = world.model(info.get('path'), None)
                name = info.get('Name')
                model.name = name
                self.scene().add_object(model)
                model.world_position = math3d.vector(*str_to_list(info.get('Position')))
                scale = info.get('Scale')
                if scale:
                    model.world_scale = math3d.vector(*str_to_list(scale))
                rotation = info.get('Rotation')
                if rotation:
                    rotation_matrix = math3d.matrix()
                    rotation_matrix.set_all(*str_to_list(rotation))
                    model.world_rotation_matrix = rotation_matrix
                if name.startswith('use_mirror'):
                    model.enable_instancing(False)
                    model.all_materials.enable_write_alpha = True
                    model.mirror_reflect = True
                self._new_scene_objs.append(model)

            sfx_list = content_cnf.get('sfx')
            for info in sfx_list:
                sfx = world.sfx(info.get('path'), scene=self.scene())
                sfx.world_position = math3d.vector(*str_to_list(info.get('Position')))
                scale = info.get('Scale')
                if scale:
                    sfx.world_scale = math3d.vector(*str_to_list(scale))
                rotation = info.get('Rotation')
                if rotation:
                    rotation_matrix = math3d.matrix()
                    rotation_matrix.set_all(*str_to_list(rotation))
                    sfx.world_rotation_matrix = rotation_matrix
                self._new_scene_objs.append(sfx)

            light_list = content_cnf.get('lights')
            for info in light_list:
                if info.get('Name') == 'dir_light':
                    light = self.scene().get_light('dir_light')
                    if light:
                        light.world_position = math3d.vector(*str_to_list(info.get('Position')))
                        light.direction = math3d.vector(*str_to_list(info.get('Direction')))
                    break

            support_reflect = lobby_model_display_utils.is_scene_surpport_reflect(scene_content_type)
            self.scene().get_model('shangcheng_jingzi_01').visible = support_reflect and not global_data.is_32bit
        return

    def on_pause(self, flag):
        if flag:
            pass