# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComLodMecha.py
from __future__ import absolute_import
from __future__ import print_function
import exception_hook
import six
from six.moves import range
import world
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.component.client.com_base_appearance.ComLodBase import ComLodBase
from common.cfg import confmgr
import logic.gcommon.item.item_const as item_const
import game3d
from logic.gcommon import const
from common.utils import pc_platform_utils
EMPTY_SUBMESH_NAME = 'empty'
INHERIT_MACROS = [
 'CHANGECOLOR_ENABLE']
MACRO_VALUE_NOT_UNIQUE_MECHA_IDS = {
 8025}

class ComLodMecha(ComLodBase):
    BIND_EVENT = {'E_HUMAN_MODEL_LOADED': 'on_humman_model_load',
       'E_UPDATE_LOD': 'update_lod',
       'E_FORCE_HIGH_MODEL': 'force_hight_model',
       'G_LOD_LEVEL': 'get_lod_level',
       'E_REFRESH_MODEL': 'load_lod_model',
       'E_BEGIN_REFRESH_WHOLE_MODEL': 'rest_is_loaded_first_time',
       'E_SWITCH_MODEL': 'on_switch_model',
       'E_FORCE_LOBBY_OUTLINE': 'force_lobby_outline',
       'G_FORCE_LOBBY_OUTLINE': 'get_force_lobby_outline',
       'E_FORCE_SHADER_LOD_LEVEL': 'force_shader_lod_level',
       'G_FORCE_SHADER_LOD_LEVEL': 'get_shader_force_lod_level'
       }
    LOD_UPDATE_INTERVAL = 0.5
    LOD_LV_MAP = {'h': 0,
       'l': 0,
       'l1': 1,
       'l2': 2,
       'l3': 3
       }

    def __init__(self):
        super(ComLodMecha, self).__init__()
        self._cur_res_path = None
        self._last_res_path = None
        self._is_loaded_firt_time = True
        self._load_mesh_task = None
        self._is_force_high_model = False
        self._is_lobby_outline = False
        self._force_shader_lod_level = None
        self.macro_value_map = {}
        self.get_model_path_func = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComLodMecha, self).init_from_dict(unit_obj, bdict)
        self.init_events()
        self._refresh_get_model_path_func()
        self.need_update = True

    def _refresh_get_model_path_func(self):
        if global_data.force_mecha_empty_model_path:
            self.get_model_path_func = self.get_model_path_in_editor
        else:
            self.get_model_path_func = self.get_model_path

    def destroy(self):
        super(ComLodMecha, self).destroy()
        self.get_model_path_func = None
        return

    def int_data(self):
        from common.cfg import confmgr
        conf_name = 'LodConst'
        if pc_platform_utils.is_pc_hight_quality_simple():
            conf_name = 'LodConstPC'
        self._lod_config = confmgr.get('mecha_conf', conf_name, 'Content')

    def init_lod(self):
        model = self.ev_g_model()
        if not model:
            print(('[Error] test--init_lod--step1--model =', model, '--ev_g_is_avatar =', self.ev_g_is_avatar(), '--unit_obj =', self.unit_obj))
            return
        if self.ev_g_is_avatar():
            self.load_lod_model()
            return
        model.lod_callback = self.update_lod
        model.visible = False
        quality = global_data.game_mgr.gds.get_actual_quality()
        self.on_display_quality_change(quality)

    def init_events(self):
        econf = {'display_quality_change': self.on_display_quality_change
           }
        global_data.emgr.bind_events(econf)

    def on_humman_model_load(self, model, user_data, *arg):
        self.init_lod()
        if self._is_lobby_outline:
            self.force_lobby_outline(self._is_lobby_outline, is_force=True)
        if self._force_shader_lod_level:
            self.force_shader_lod_level(self._force_lod_level, is_force=True)

    def force_hight_model(self, is_force):
        self._is_force_high_model = is_force
        self.load_lod_model()

    def get_lod_level_name(self):
        lod_name = 'l'
        lod_level = self._start_lod_level + self._cur_lod_level
        if self.ev_g_is_avatar():
            start_lod_level, lod_dist_list = self.calc_lod_dist()
            lod_level = start_lod_level
        if lod_level > 0:
            lod_name += str(lod_level)
        if lod_level >= 3 and global_data.cam_lctarget and global_data.cam_lctarget.sd.ref_in_aim:
            lod_name = 'l2'
        if lod_level > 3 or lod_name == 'l4':
            lod_name = 'l3'
        if self._is_force_high_model:
            lod_name = 'l'
        lod_name = pc_platform_utils.get_effect_lod_level(lod_name)
        return lod_name

    def get_lod_level(self):
        return self.LOD_LV_MAP[self.get_lod_level_name()]

    def get_model_path(self, mecha_id, mecha_fashion_id, shiny_weapon_id):
        from logic.gutils.dress_utils import get_mecha_model_path
        path = get_mecha_model_path(mecha_id, mecha_fashion_id, shiny_weapon_id=shiny_weapon_id)
        if self.sd.ref_second_model_dir and self.sd.ref_using_second_model:
            index = path.rfind('/')
            path = path[:index] + '/' + self.sd.ref_second_model_dir + path[index:]
        return path

    def get_model_path_in_editor(self, mecha_id, mecha_fashion_id, shiny_weapon_id):
        if global_data.force_mecha_empty_model_path and self.ev_g_is_avatar():
            return global_data.force_mecha_empty_model_path
        else:
            from logic.gutils.dress_utils import get_mecha_model_path
            return get_mecha_model_path(mecha_id, mecha_fashion_id)

    def load_lod_model(self, force_lod_level=None, force_skin_id=None):
        lod_name = self.get_lod_level_name()
        lod_name = global_data.gsetting.mapping_mecha_lod_name(lod_name)
        mecha_id = self.sd.ref_mecha_id
        mecha_fashion_id, shiny_weapon_id = self.ev_g_mecha_skin_and_shiny_weapon_id()
        if force_lod_level:
            lod_name = force_lod_level
        if force_skin_id:
            mecha_fashion_id = force_skin_id
        if global_data.force_battle_mecha_lod_level:
            lod_name = global_data.force_battle_mecha_lod_level
        if not self._is_loaded_firt_time:
            self.send_event('E_MECHA_LOD_LEVEL_CHANGED', self.LOD_LV_MAP[lod_name])
        res_path = self.get_model_path_func(mecha_id, mecha_fashion_id, shiny_weapon_id)
        index = res_path.find('empty.gim')
        if index != -1:
            res_path = res_path[0:index] + lod_name + '.gim'
            self.ev_g_load_model(res_path, self.on_add_fullbody_model, res_path, sync_priority=game3d.ASYNC_HIGH)
        elif self._is_loaded_firt_time:
            self._is_loaded_firt_time = False
            self.send_event('E_MECHA_LOD_LOADED_FIRST')

    def on_add_fullbody_model(self, load_model, res_path, *args):
        model = self.ev_g_model()
        if not model:
            return
        if global_data.feature_mgr.is_support_model_decal():
            if self.unit_obj.__class__.__name__ != 'LMechaTrans':
                if self.sd.ref_mecha_id in MACRO_VALUE_NOT_UNIQUE_MECHA_IDS:
                    self.macro_value_map.clear()
                    for macro in INHERIT_MACROS:
                        if macro not in self.macro_value_map:
                            self.macro_value_map[macro] = []
                        for index in range(load_model.get_submesh_count()):
                            if load_model.get_sub_material(index).get_macro(macro):
                                value = 'TRUE' if 1 else 'FALSE'
                                self.macro_value_map[macro].append(value)

                else:
                    for macro in INHERIT_MACROS:
                        if load_model.all_materials.get_macro(macro) == 'TRUE':
                            model.all_materials.set_macro(macro, 'TRUE')
                        else:
                            model.all_materials.set_macro(macro, 'FALSE')

        if self._cur_res_path and not self._load_mesh_task:
            self._last_res_path = self._cur_res_path
        self._cur_res_path = res_path
        self._load_mesh_task = global_data.model_mgr.create_mesh_async(self._load_mesh_task, res_path, model, self.on_load_mesh_completed, self.on_before_add_new_mesh, game3d.ASYNC_ULTIMATE_HIGH)

    def on_before_add_new_mesh(self, model):
        if self._last_res_path:
            model.remove_mesh(self._last_res_path)
            self._last_res_path = None
        return

    def on_load_mesh_completed(self, model):
        model.set_submesh_visible(EMPTY_SUBMESH_NAME, False)
        submesh_cnt = model.get_submesh_count()
        for i in range(submesh_cnt):
            try:
                if model.get_submesh_name(i) != 'hit':
                    model.set_submesh_hitmask(i, world.HIT_SKIP)
            except UnicodeDecodeError as e:
                model.set_submesh_hitmask(i, world.HIT_SKIP)
                exception_hook.traceback_uploader()

        if self.unit_obj.__class__.__name__ != 'LMechaTrans':
            if self.sd.ref_mecha_id in MACRO_VALUE_NOT_UNIQUE_MECHA_IDS:
                for macro, macro_value_list in six.iteritems(self.macro_value_map):
                    for i in range(2, submesh_cnt):
                        if i - 2 < len(macro_value_list):
                            model.get_sub_material(i).set_macro(macro, macro_value_list[i - 2])

                model.all_materials.rebuild_tech()
        if self._is_loaded_firt_time:
            self._is_loaded_firt_time = False
            self.send_event('E_MECHA_LOD_LOADED_FIRST')
        owner_model = model
        self.send_event('E_MECHA_LOD_LOADED', owner_model, self._cur_res_path)
        self.sd.ref_socket_res_agent and self.sd.ref_socket_res_agent.on_lod_changed()
        if global_data.debug_perf_switch_global:
            avatar_visible = global_data.get_debug_perf_val('enable_avatar_model', True)
            model.visible = avatar_visible
        self._load_mesh_task = None
        return

    def rest_is_loaded_first_time(self):
        self._last_res_path = None
        self._cur_res_path = None
        self._is_loaded_firt_time = True
        self._refresh_get_model_path_func()
        return

    def on_switch_model(self, model):
        old_model = self.ev_g_mecha_original_model() if self.sd.ref_using_second_model else self.ev_g_mecha_second_model()
        self.on_before_add_new_mesh(old_model)
        if self._cur_res_path:
            old_model.remove_mesh(self._cur_res_path)
            self._cur_res_path = None
        else:
            self._is_loaded_firt_time = True
        self.load_lod_model()
        return

    def force_lobby_outline(self, is_lobby_outline, is_force=False):
        if self._is_lobby_outline == is_lobby_outline and not is_force:
            return
        self._is_lobby_outline = is_lobby_outline
        from common.utils import pc_platform_utils
        model = self.ev_g_model()
        if not model:
            return
        if is_lobby_outline:
            pc_platform_utils.set_multi_pass_outline(model)
        else:
            pc_platform_utils.disable_multi_pass_outline(model)

    def get_force_lobby_outline(self):
        return self._is_lobby_outline

    def force_shader_lod_level(self, level, is_force=False):
        if self._force_shader_lod_level == level and not is_force:
            return
        else:
            self._force_shader_lod_level = level
            model = self.ev_g_model()
            if not model:
                return
            if level is not None:
                model.all_materials.set_macro('LOD_LEVEL', str(level))
            else:
                from logic.vscene.global_display_setting import GlobalDisplaySeting
                quality = GlobalDisplaySeting().get_actual_quality()
                from logic.gutils.shader_warmup import DEFAULT_LOD_MAPPING
                lod_level = DEFAULT_LOD_MAPPING.get(quality, 2)
                model.all_materials.set_macro('LOD_LEVEL', str(lod_level))
            return

    def get_shader_force_lod_level(self):
        return self._force_shader_lod_level