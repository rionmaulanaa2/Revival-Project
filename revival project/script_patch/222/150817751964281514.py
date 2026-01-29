# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/Sys3DMapInfoMgr.py
from __future__ import absolute_import
from six.moves import range
from logic.vscene.part_sys.ScenePartSysBase import ScenePartSysBase
import world
import math3d
import weakref
import render
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.utilities import get_utf8_length
from logic.gcommon.common_utils import parachute_utils
from common.uisys.font_utils import GetMultiLangFontFaceName
import cc
from common.uisys.uielment.CCLabel import CCLabel
from common.utils.cocos_utils import CCSizeZero

class Sys3DMapInfoMgr(ScenePartSysBase):

    def __init__(self):
        super(Sys3DMapInfoMgr, self).__init__()
        self.gui_map_model_ref = None
        self.is_add_map_names = False
        self.simui_list = []
        self.init_events()
        return

    def init_events(self):
        global_data.emgr.on_player_parachute_stage_changed += self.on_player_parachute_stage_changed
        global_data.emgr.map_3d_model_loaded_event += self.map_model_loaded
        global_data.emgr.map_model_transformation_changed_event += self.reset_map_infos
        global_data.emgr.show_map_info_event += self.show_3d_info
        global_data.emgr.map_model_transformation_changed_event += self.map_model_transformation_change

    def map_model_loaded(self, model):
        self.gui_map_model_ref = weakref.ref(model)

    def show_3d_info(self):
        self.init_map_names()

    def init_map_names(self):
        if self.is_add_map_names or self.gui_map_model_ref:
            model = self.gui_map_model_ref() if 1 else None
            render.create_font('name_txt', GetMultiLangFontFaceName('DFZongYiW7-GB'), 14, True)
            if model and model.valid:
                scount = model.get_socket_count()
                self.is_add_map_names = True
                for i in range(scount):
                    sname = model.get_socket_name(i)
                    if not sname.startswith('id_'):
                        continue
                    place_name = get_text_by_id(int(sname[3:]))
                    ui_empty = render.texture('gui/ui_res_2/simui/img_place_name.png')
                    p_simui = world.simuiobject(ui_empty)
                    if len(place_name) != get_utf8_length(place_name):
                        image_ui_len = len(place_name) * 9 if 1 else len(place_name) * 18
                        image_id = p_simui.add_image_ui(0, 0, int(image_ui_len), 30, 0, 0)
                        p_simui.set_ui_align(image_id, 0.5, 0.5)
                        p_simui.set_imageui_horpercent(image_id, 0.0, 1.0)
                        name_simui_id = p_simui.add_text_ui(place_name, 'name_txt', 0, 0)
                        color = (255, 167, 251, 252)
                        p_simui.set_ui_color(name_simui_id, color)
                        p_simui.set_ui_align(name_simui_id, 0.5, 0.5)
                        p_simui.set_ui_fill_z(name_simui_id, False)
                        p_simui.set_ui_saturate(name_simui_id, 100)
                        self.simui_list.append((p_simui, name_simui_id, image_id))
                        model.bind(i, p_simui, world.BIND_TYPE_ALL)

        return

    def map_model_transformation_change(self):
        if self.gui_map_model_ref:
            model = self.gui_map_model_ref() if 1 else None
            if model and model.valid:
                pass
            map_rt = global_data.emgr.get_3d_map_rt_event.emit()[0]
            return map_rt or None
        else:
            cam = map_rt.scn.active_camera
            cur_scale = 2.5 - (cam.world_position - model.world_position).length / 400.0
            for simui, name_simui_id, image_id in self.simui_list:
                if simui and simui.valid:
                    simui.set_ui_scale(name_simui_id, cur_scale, cur_scale)
                    simui.set_ui_scale(image_id, cur_scale, cur_scale)

            return

    def on_player_parachute_stage_changed(self, *args):
        if not global_data.player or not global_data.player.logic:
            return
        stage = global_data.player.logic.share_data.ref_parachute_stage
        if stage not in (parachute_utils.STAGE_PLANE, parachute_utils.STAGE_MECHA_READY, parachute_utils.STAGE_NONE):
            self.clear()

    def clear(self):
        self.simui_list = []

    def reset_map_infos(self):
        pass

    def destroy(self):
        self.clear()