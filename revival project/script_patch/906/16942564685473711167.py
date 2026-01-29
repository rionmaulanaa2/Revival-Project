# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/battlemembers/impSceneSwitcher.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gutils.EntityPool import EntityPool
from logic.gutils.sunshine_utils import refresh_mecha_cam_view
import world
EVN_PARAM = {'01': ('pve_01', 'pve_01_b', 'pve_01_c'),
   '02': ('pve_02', 'pve_02_b', 'pve_02_c'),
   '03': ('pve_03_a', 'pve_03_b', 'pve_03_c')
   }
REPLACE_GIMS = {'01': (
        (),
        (('model_new/scene/pve/pve_01/mesh/pve_ty/sky_pve_01_b.gim', 'model_new/scene/pve/pve_01/mesh/pve_ty/sky_pve_01_d.gim'), ),
        (('model_new/scene/pve/pve_01/mesh/pve_ty/sky_pve_01_b.gim', 'model_new/scene/pve/pve_01/mesh/pve_ty/sky_pve_01_e.gim'), )),
   '02': (
        (),
        (('model_new/scene/pve/pve_02/mesh/pve_02_ty/sky_pve02.gim', 'model_new/scene/pve/pve_02/mesh/pve_02_ty/sky_pve02_hard.gim'), ),
        (('model_new/scene/pve/pve_02/mesh/pve_02_ty/sky_pve02.gim', 'model_new/scene/pve/pve_02/mesh/pve_02_ty/sky_pve02_hell.gim'), )),
   '03': (
        (),
        (('model_new/scene/pve/pve_03/mesh/sky_pve_04.gim', 'model_new/scene/pve/pve_03/mesh/sky_pve_03_hard.gim'), ),
        (('model_new/scene/pve/pve_03/mesh/sky_pve_04.gim', 'model_new/scene/pve/pve_03/mesh/sky_pve_03_hell.gim'), ))
   }

class impSceneSwitcher(object):
    EVN_DEFAULT = 'pve_01'

    def _init_sceneswitcher_from_dict(self, bdict):
        self.env_key = None
        return

    def _init_sceneswitcher_completed(self, bdict):
        global_data.emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted

    def _tick_sceneswitcher(self, delta):
        pass

    def _destroy_sceneswitcher(self, clear_cache):
        global_data.emgr.scene_camera_player_setted_event -= self.on_cam_lplayer_setted

    def switch_scene(self, scene_info):
        if global_data.mecha and global_data.mecha.logic:
            global_data.mecha.logic.send_event('E_CLEAR_BEHAVIOR')
        if global_data.player:
            self.remove_entity_imp(global_data.player.id)
        self.destroy_all_entities()
        EntityPool.clear()
        scene_data = self.gen_scene_data(scene_info)
        self.load_scene(scene_data)
        self.clear_all_tips()
        global_data.emgr.battle_switch_scene_event.emit()

    def gen_scene_data(self, scene_info):
        map_id = scene_info.get('map_id')
        scene_name = scene_info.get('scene_name')
        scene_path = scene_info.get('scene_path')
        bdict = self._save_init_bdict
        scene_data = {}
        view_position = bdict.get('view_position', None)
        if view_position:
            scene_data['view_position'] = view_position
        view_range = bdict.get('view_range', None)
        if view_range:
            scene_data['view_range'] = view_range
        brief_group_data = bdict.get('brief_group_data', None)
        self._brief_group_data = brief_group_data
        scene_data['group_data'] = brief_group_data
        scene_data['is_battle'] = True
        is_spectate = bdict.get('is_spectate', False)
        scene_data['is_spectate'] = is_spectate
        scene_data['scene_name'] = scene_name
        self._scene_name = scene_name
        scene_data['scene_path'] = scene_path
        self._scene_path = scene_path
        str_lst = scene_name.split('_')
        if len(str_lst) > 2:
            self.env_key = str_lst[1]
            env_param = EVN_PARAM.get(self.env_key, (self.EVN_DEFAULT, self.EVN_DEFAULT, self.EVN_DEFAULT))[self.get_cur_pve_difficulty() - 1]
        else:
            env_param = self.EVN_DEFAULT
        scene_data['fog_config'] = scene_data['light_config'] = env_param
        scene_data['hdr_config'] = self.EVN_DEFAULT
        scene_data['async_load'] = False if 'pve' in scene_name else True
        self.map_id = map_id
        self.battle_tid = bdict.get('battle_type')
        global_data.game_mode.set_enviroment(bdict.get('environment', None))
        global_data.game_mode.set_map(self.map_id, self.battle_tid)
        return scene_data

    def on_cam_lplayer_setted(self, *args):
        if global_data.cam_lplayer:
            refresh_mecha_cam_view()

    def replace_scene_model(self):
        if not self.env_key:
            return
        world.reset_res_object_filemap()
        for gim_info in REPLACE_GIMS.get(self.env_key, ((), (), ()))[self.get_cur_pve_difficulty() - 1]:
            if not gim_info:
                continue
            old_gim, new_gim = gim_info
            world.set_res_object_filemap(old_gim.replace('/', '\\'), new_gim.replace('/', '\\'))

    def get_env_key(self):
        return self.env_key