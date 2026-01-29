# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartHouseSys.py
from __future__ import absolute_import
import render
import game3d
from . import ScenePart
from common.cfg import confmgr
from logic.gcommon.const import LOBBY_TV_TOUCH_MAX_DISTANCE
from logic.gutils.tv_panel_utils import get_tv_texture_path
DEFAULT_PHOTO_PATH = 'gui/ui_res_2/poster/poster_01.png'
_HASH_Tex0 = game3d.calc_string_hash('Tex0')
REFLECT_MODEL = ['dating_11_z_131', 'new_jiemian_10_125']
SUB_MATERIAL_NAME = 'dt_prop_xianshiqi_020'

class PartHouseSys(ScenePart.ScenePart):
    INIT_EVENT = {'housesys_touch_model': 'on_model_touch',
       'housesys_wall_picture_change': 'on_picture_change',
       'loading_end_event': 'on_loading_end',
       'display_quality_change': 'on_display_quality_change',
       'player_leave_visit_scene_event': 'on_leave_scene',
       'player_enter_visit_scene_event': 'on_enter_scene'
       }

    def __init__(self, scene, name):
        super(PartHouseSys, self).__init__(scene, name)
        self._tv_model = None
        self._model_func_map = {}
        return

    def on_display_quality_change(self, quality):
        if global_data.is_ue_model:
            mirror_reflect = quality > 1
            if self._tv_model:
                self._tv_model.mirror_reflect = mirror_reflect
            for model_name in REFLECT_MODEL:
                model = self.scene().get_model(model_name)
                if model:
                    model.mirror_reflect = mirror_reflect

    def on_enter_scene(self, *args):
        self.on_picture_change()

    def on_leave_scene(self, *args):
        self.on_picture_change()

    def on_enter(self):
        if global_data.game_mgr.gds:
            mirror_reflect = global_data.game_mgr.gds.get_actual_quality() > 1 if 1 else False
            if global_data.is_ue_model:
                for model_name in REFLECT_MODEL:
                    model = self.scene().get_model(model_name)
                    if model:
                        model.all_materials.enable_write_alpha = True
                        model.mirror_reflect = mirror_reflect

            model = self.scene().get_model('dt_prop_xianshiqi_02')
            if not model:
                return
            self._tv_model = model
            model.pickable = True
            model.all_materials.enable_write_alpha = True
            tex_path = G_IS_NA_PROJECT or get_tv_texture_path()
            wall_texture = render.texture(tex_path, False, False, render.TEXTURE_TYPE_UNKNOWN, game3d.ASYNC_NONE)
            material = self._tv_model.get_sub_material(SUB_MATERIAL_NAME)
            material.set_texture(_HASH_Tex0, 'Tex0', wall_texture)
            self._model_func_map[model] = self.touch_furniture_mainland
        else:
            self._model_func_map[model] = self.touch_furniture
            self.on_picture_change()
        global_data.ui_mgr.show_ui('ModelArrowUI', 'logic.comsys.housesys')
        if global_data.is_ue_model:
            model.mirror_reflect = mirror_reflect

    def on_loading_end(self):
        pass

    def on_model_touch(self, model):
        function = self._model_func_map.get(model)
        if not function:
            return
        scene = global_data.game_mgr.scene
        if scene and scene.valid:
            cam = scene.active_camera
            mpos = model.center_w
            mpos.y -= model.bounding_box_w.y
            if cam and (cam.world_position - mpos).length > LOBBY_TV_TOUCH_MAX_DISTANCE:
                return
        if not global_data.player or global_data.player.is_visit_others():
            return
        function()

    def touch_furniture(self):
        global_data.ui_mgr.close_ui('LobbySceneOnlyUI')
        global_data.ui_mgr.show_ui('MainHouseUI', 'logic.comsys.housesys')
        global_data.sound_mgr.play_sound_2d('Play_ui_click', ('ui_click', 'ui_1_open'))

    def touch_furniture_mainland(self):
        key = global_data.channel.is_steam_channel() or 'mainland' if 1 else 'steam'
        jump_conf = confmgr.get('tv_conf', 'LobbyTV', 'Content', key, 'jump_params', default={})
        func_name = jump_conf.get('func')
        args = jump_conf.get('args', [])
        if func_name:
            from logic.gutils import jump_to_ui_utils
            func = getattr(jump_to_ui_utils, func_name)
            func and func(*args)
        from logic.gcommon.const import LOBBY_TV_TEXTURE_KEY
        tex_path = get_tv_texture_path()
        global_data.achi_mgr.get_general_archive_data().set_field(LOBBY_TV_TEXTURE_KEY, tex_path)
        global_data.emgr.refresh_tv_new.emit()

    def on_picture_change(self, item_no=-1):
        if not G_IS_NA_PROJECT:
            return
        if not global_data.player:
            return
        if item_no == -1:
            if global_data.player.is_in_visit_mode():
                cur_wall_picture = global_data.player.get_visit_wall_picture()
            else:
                cur_wall_picture = global_data.player.get_wall_picture()
        else:
            cur_wall_picture = item_no
        if self._tv_model:
            house_photo_data = confmgr.get('house_photo', str(cur_wall_picture))
            if house_photo_data:
                res_path = house_photo_data['cRes']
            else:
                res_path = DEFAULT_PHOTO_PATH
            wall_texture = render.texture(res_path, False, False, render.TEXTURE_TYPE_UNKNOWN, game3d.ASYNC_NONE)
            material = self._tv_model.get_sub_material(SUB_MATERIAL_NAME)
            material.set_texture(_HASH_Tex0, 'Tex0', wall_texture)

    def on_exit(self):
        global_data.ui_mgr.close_ui('ModelArrowUI')