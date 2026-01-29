# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_pet/ComLodPet.py
import world
import math3d
from six.moves import range
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.component.client.com_base_appearance.ComLodBase import ComLodBase, MAX_LOD_LEVEL
from common.cfg import confmgr
import game3d
from common.utils import pc_platform_utils
import device_compatibility
from logic.client.const import game_mode_const
from logic.gcommon.common_const import battle_const
from mobile.common.EntityManager import EntityManager
EMPTY_SUBMESH_NAME = 'empty'
INHERIT_MACROS = [
 'CHANGECOLOR_ENABLE']
MACRO_VALUE_NOT_UNIQUE_MECHA_IDS = {
 8025}

class ComLodPet(ComLodBase):
    BIND_EVENT = {'E_PET_MODEL_LOADED': 'on_pet_model_load',
       'E_UPDATE_LOD': 'update_lod',
       'E_FORCE_LOD': 'force_lod',
       'G_LOD_LEVEL': 'get_lod_level',
       'G_LOD_LEVEL_NAME': 'get_lod_level_name',
       'E_REFRESH_MODEL': 'load_lod_model',
       'E_BEGIN_REFRESH_WHOLE_MODEL': 'reset_is_loaded_first_time',
       'E_SWITCH_MODEL': 'on_switch_model'
       }
    LOD_UPDATE_INTERVAL = 0.5
    LOD_LV_MAP = {'l': 0,
       'l1': 1,
       'l2': 2,
       'l3': 3
       }

    def __init__(self):
        super(ComLodPet, self).__init__()
        self._cur_res_path = None
        self._last_res_path = None
        self._is_loaded_first_time = True
        self._load_mesh_task = None
        self._force_lod = None
        self.macro_value_map = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComLodPet, self).init_from_dict(unit_obj, bdict)
        self.init_events()
        self.skin_id = bdict.get('pet_id', None)
        self.in_lobby = bdict.get('in_lobby', False)
        self._owner_logic = bdict.get('owner_logic', None)
        self._owner_id = bdict.get('owner_id', None)
        self._owner_is_avatar = None
        self.need_update = True
        return

    def owner_logic(self):
        if not self._owner_logic and self._owner_id:
            owner = EntityManager.getentity(self._owner_id)
            if owner:
                self._owner_logic = owner.logic
        return self._owner_logic

    def owner_is_avatar(self):
        if self._owner_is_avatar is not None:
            return self._owner_is_avatar
        else:
            owner_logic = self.owner_logic()
            if owner_logic:
                self._owner_is_avatar = owner_logic.sd.ref_is_avatar
            return bool(self._owner_is_avatar)

    def onwer_is_cam_campmate(self):
        if not global_data.cam_lctarget:
            return False
        owner_logic = self.owner_logic()
        if not owner_logic:
            return False
        camp_id = owner_logic.ev_g_camp_id()
        return global_data.cam_lctarget.ev_g_is_campmate(camp_id)

    def destroy(self):
        super(ComLodPet, self).destroy()

    def int_data(self):
        from common.cfg import confmgr
        conf_name = 'LodConst'
        if pc_platform_utils.is_pc_hight_quality_simple():
            conf_name = 'LodConstPC'
        self._lod_config = confmgr.get('mecha_conf', conf_name, 'Content')

    def init_lod(self):
        model = self.ev_g_model()
        if not model:
            return
        if self.in_lobby or self.owner_is_avatar():
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

    def on_pet_model_load(self, model, user_data, *arg):
        self.init_lod()

    def force_lod(self, lod_level):
        self._force_lod = lod_level
        self.load_lod_model()

    def get_lod_level_name(self):
        lod_name = 'l'
        lod_level = self._start_lod_level + self._cur_lod_level
        if self._force_lod is not None:
            lod_name = self._force_lod
        else:
            if lod_level > 0:
                lod_name += str(lod_level)
            if lod_level >= 3 and global_data.cam_lctarget and global_data.cam_lctarget.sd.ref_in_aim:
                lod_name = 'l2'
            if lod_level > 3 or lod_name == 'l4':
                lod_name = 'l3'
        lod_name = pc_platform_utils.get_effect_lod_level(lod_name)
        return lod_name

    def get_lod_level(self):
        return self.LOD_LV_MAP[self.get_lod_level_name()]

    def get_model_path(self, skin_id):
        path = confmgr.get('c_pet_info', str(skin_id), 'model_path')
        if global_data.force_pet_data and global_data.force_pet_data.get('use_editor_res', True):
            path = global_data.force_pet_data.get('model_path', path)
        return path

    def load_lod_model(self, force_lod_level=None, force_skin_id=None):
        lod_name = self.get_lod_level_name()
        lod_name = global_data.gsetting.mapping_mecha_lod_name(lod_name)
        skin_id = force_skin_id or self.skin_id
        if force_lod_level:
            lod_name = force_lod_level
        res_path = self.get_model_path(skin_id)
        index = res_path.find('empty.gim')
        if index != -1:
            res_path = res_path[0:index] + lod_name + '.gim'
            self.ev_g_load_model(res_path, self.on_add_fullbody_model, res_path, sync_priority=game3d.ASYNC_HIGH)
        elif self._is_loaded_first_time:
            self._is_loaded_first_time = False
            self.send_event('E_MECHA_LOD_LOADED_FIRST')

    def update_cur_lod(self):
        super(ComLodPet, self).update_cur_lod()
        self.send_event('E_PET_LOD_CHANGED')

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
            if model.get_submesh_name(i) != 'hit':
                model.set_submesh_hitmask(i, world.HIT_SKIP)

        if self.unit_obj.__class__.__name__ != 'LMechaTrans':
            if self.sd.ref_mecha_id in MACRO_VALUE_NOT_UNIQUE_MECHA_IDS:
                for macro, macro_value_list in self.macro_value_map.iteritems():
                    for i in range(2, submesh_cnt):
                        model.get_sub_material(i).set_macro(macro, macro_value_list[i - 2])

                model.all_materials.rebuild_tech()
        if self._is_loaded_first_time:
            self._is_loaded_first_time = False
            self.send_event('E_MECHA_LOD_LOADED_FIRST')
        owner_model = model
        self.send_event('E_MECHA_LOD_LOADED', owner_model, self._cur_res_path)
        if global_data.debug_perf_switch_global:
            avatar_visible = global_data.get_debug_perf_val('enable_avatar_model', True)
            model.visible = avatar_visible
        self._load_mesh_task = None
        return

    def reset_is_loaded_first_time(self):
        self._last_res_path = None
        self._cur_res_path = None
        self._is_loaded_first_time = True
        return

    def on_switch_model(self, model):
        old_model = self.ev_g_mecha_original_model() if self.sd.ref_using_second_model else self.ev_g_mecha_second_model()
        self.on_before_add_new_mesh(old_model)
        if self._cur_res_path:
            old_model.remove_mesh(self._cur_res_path)
            self._cur_res_path = None
        else:
            self._is_loaded_first_time = True
        self.load_lod_model()
        return

    def on_display_quality_change(self, quality):
        if self.in_lobby:
            return
        super(ComLodPet, self).on_display_quality_change(quality)

    def calc_lod_dist(self):
        import game3d
        if global_data.game_mgr.gds:
            quality = global_data.game_mgr.gds.get_actual_quality()
        else:
            quality = 0
        perf_flag = device_compatibility.get_device_perf_flag()
        if self.in_lobby or self.owner_is_avatar():
            camp_flag = 0
        elif self.onwer_is_cam_campmate():
            camp_flag = 1
        else:
            camp_flag = 2
        game_mode = global_data.game_mode.get_mode_type() if global_data.game_mode else None
        game_mode_idx = game_mode_const.get_game_mode_index(game_mode)
        if pc_platform_utils.is_pc_hight_quality_simple():
            index = ','.join([str(battle_const.PLAY_TYPE_CHICKEN), str(perf_flag), str(4), str(camp_flag)])
        else:
            index = ','.join([str(game_mode_idx), str(perf_flag), str(quality), str(camp_flag)])
        default_config = {'lod_0': -1,'lod_1': 20,'lod_2': 40,'lod_3': 60}
        quality_lod_config = self._lod_config.get(index, None)
        if quality_lod_config is None:
            subs_index = ','.join([str(battle_const.PLAY_TYPE_DEATH), str(perf_flag), str(quality), str(camp_flag)])
            quality_lod_config = self._lod_config.get(subs_index, default_config)
        for level in range(MAX_LOD_LEVEL):
            key = 'lod_' + str(level)
            dist = quality_lod_config[key]
            if dist >= 0:
                start_lod_level = level
                break

        lod_dist_list = []
        for level in range(start_lod_level, MAX_LOD_LEVEL):
            key = 'lod_' + str(level)
            dist = quality_lod_config[key] * NEOX_UNIT_SCALE
            lod_dist_list.append(dist)

        supply_len = 3 - len(lod_dist_list)
        supply_len = max(supply_len, 0)
        for _ in range(supply_len):
            lod_dist_list.append(-1)

        lod_dist_list = tuple(lod_dist_list)
        return (
         start_lod_level, lod_dist_list)