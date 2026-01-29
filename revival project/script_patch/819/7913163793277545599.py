# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComExplosiveRobotAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
import world
import math3d
import weakref
import game3d
from common.cfg import confmgr
from logic.client.const import game_mode_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.soc_utils import set_model_attach_soc
from logic.gutils.weapon_skin_utils import get_explosive_robot_conf_val
RENDER_GROUP_DYOCC_OBJ = 28
EMPTY_SUBMESH_NAME = 'empty'
DEFAULT_CLOTHING_ID = -1

class ComExplosiveRobotAppearance(ComBaseModelAppearance):
    BIND_LOAD_FINISH_EVENT = ComBaseModelAppearance.BIND_LOAD_FINISH_EVENT.copy()
    BIND_LOAD_FINISH_EVENT.update({'E_ROTATION': '_on_rotation_changed',
       'G_YAW': '_get_yaw'
       })

    def __init__(self):
        super(ComExplosiveRobotAppearance, self).__init__()
        self.itype = None
        self._is_outline = False
        self._cur_lod_level = 0
        self._start_lod_level = 0
        self._to_lod_level = 0
        self.LOD_UPDATE_INTERVAL = 0.5
        self._lod_update_last_time = 0
        self._lod_dist_list = (15 * NEOX_UNIT_SCALE, 30 * NEOX_UNIT_SCALE)
        self._cur_lod_res_path = None
        self._last_lod_res_path = None
        self._load_lod_mesh_task = None
        return

    def init_from_dict(self, unit_obj, bdict):
        self.itype = bdict.get('robot_no', 105602)
        self._owner_fashion_id = bdict.get('owner_fashion_id', DEFAULT_CLOTHING_ID)
        super(ComExplosiveRobotAppearance, self).init_from_dict(unit_obj, bdict)

    def _on_rotation_changed(self, mat):
        self._model.world_rotation_matrix = mat

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rotation = bdict.get('yaw', 0)
        data = {'pos': math3d.vector(*pos),'rotation': rotation}
        model_path = self._get_empty_model_path()
        return (
         model_path, None, data)

    def _get_empty_model_path(self):
        model_path = 'character/weapons/1056_boomer_robot/1056/empty.gim'
        if self.itype:
            model_path = get_explosive_robot_conf_val(self.itype, 'model', default=model_path, skin_id=self._owner_fashion_id)
        return model_path

    def _get_yaw(self):
        return self._model.world_rotation_matrix.yaw

    def on_load_model_complete(self, model, userdata):
        import math3d
        model.position = userdata['pos']
        m = math3d.matrix.make_rotation_y(userdata['rotation'])
        model.rotation_matrix = m
        scale = 0.2
        if self.itype:
            scale = get_explosive_robot_conf_val(self.itype, 'model_scale', default=scale, skin_id=self._owner_fashion_id)
        model.scale = math3d.vector(scale, scale, scale)
        self.init_lod()
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.ExplosiveRobot_OutLine):
            if self.ev_g_is_enemy() and self._is_outline == False:
                self.send_event('E_ADD_MATERIAL_STATUS', 'ComCamp_always_outline', param={'status_type': 'OUTLINE_ONLY',
                   'outline_alpha': 0.3333
                   }, prority=0)
                self._is_outline == True

    def destroy(self):
        if self._is_outline:
            self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_always_outline')
            self._is_outline = False
        super(ComExplosiveRobotAppearance, self).destroy()

    def init_lod(self):
        model = self.ev_g_model()
        if not model:
            return
        model.lod_config = self._lod_dist_list
        model.lod_callback = self.on_update_lod
        self.load_lod_model()

    def tick(self, delta):
        now = global_data.game_time
        if now - self._lod_update_last_time > self.LOD_UPDATE_INTERVAL:
            self.update_cur_lod()
            self._lod_update_last_time = now
            self.need_update = False

    def on_update_lod(self, lod_level):
        leng = len(self._lod_dist_list)
        if lod_level >= 0 and lod_level < leng:
            if self._lod_dist_list[lod_level] < 0:
                return
        elif lod_level != leng:
            return
        self._to_lod_level = lod_level
        self.need_update = True

    def update_cur_lod(self):
        if self._cur_lod_level == self._to_lod_level:
            return
        self._cur_lod_level = self._to_lod_level
        self.load_lod_model()

    def get_model_lod_level_name(self):
        model_lod_level = self._start_lod_level + self._cur_lod_level
        model_lod_level = min(model_lod_level, 2)
        lod_name = 'h'
        if model_lod_level > 0:
            lod_name = 'l'
            lod_name += str(model_lod_level)
        return lod_name

    def load_lod_model(self):
        model = self.ev_g_model()
        if not model:
            return
        res_path = self._get_empty_model_path()
        index = res_path.find('empty.gim')
        if index != -1:
            lod_name = self.get_model_lod_level_name()
            res_path = res_path[0:index] + lod_name + '.gim'
            if self._cur_lod_res_path:
                self._last_lod_res_path = self._cur_lod_res_path
            self._cur_lod_res_path = res_path
            self._load_lod_mesh_task = global_data.model_mgr.create_mesh_async(self._load_lod_mesh_task, res_path, model, self.on_load_mesh_completed, self.on_before_add_new_mesh)

    def on_before_add_new_mesh(self, model):
        if self._last_lod_res_path:
            model.remove_mesh(self._last_lod_res_path)
            self._last_lod_res_path = None
        return

    def on_load_mesh_completed(self, model):
        model.set_submesh_visible(EMPTY_SUBMESH_NAME, False)
        model.set_rendergroup_and_priority(RENDER_GROUP_DYOCC_OBJ, 0)
        model.set_ignore_dyn_culling(True)
        set_model_attach_soc(model, False)