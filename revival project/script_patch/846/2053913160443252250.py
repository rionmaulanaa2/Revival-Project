# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComExerciseTargetAppearance.py
from __future__ import absolute_import
import six
from .ComBaseModelAppearance import ComBaseModelAppearance
import math3d
import math
from logic.gcommon.const import NEOX_UNIT_SCALE
import logic.gcommon.common_utils.bcast_utils as bcast
import logic.client.path_utils as path_utils
from common.cfg import confmgr

class ComExerciseTargetAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MODIFY_MODEL_SCALE': '_modify_model_scale',
       'E_HIT_BLOOD_SFX': '_on_be_hited',
       'E_HANDLE_ADD_BUFF': '_handle_buff',
       'E_HANDLE_DEL_BUFF': '_remove_buff',
       'E_CREATE_SCENE_EFFECT': 'on_create_scene_effect',
       'E_CREATE_MODEL_EFFECT': 'on_create_model_effects',
       'E_REMOVE_MODEL_EFFECT': 'on_remove_model_effects',
       'E_FIRE_EFFECT': '_on_fire_effect',
       'G_HEADSHOOT_TAG': '_return_headshoot_type_tag'
       })
    TYPE_SOLID = 1126
    TYPE_PATROL = 1211
    target_model_path_dict = {TYPE_SOLID: confmgr.get('script_gim_ref')['exercise_target_path_01'],TYPE_PATROL: confmgr.get('script_gim_ref')['exercise_target_path_02']
       }
    trace_model_path = {TYPE_PATROL: (confmgr.get('script_gim_ref')['exercise_trace_path_01'],
                   confmgr.get('script_gim_ref')['exercise_trace_path_02'])
       }
    TRACE_HIGHT_OFFSET = math3d.vector(0, -0.25, 0)
    FIRE_EFFECT = {path_utils.EXERCISE_FIRE_EFFECT: ['part_point1']}

    def __init__(self):
        super(ComExerciseTargetAppearance, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComExerciseTargetAppearance, self).init_from_dict(unit_obj, bdict)
        self.move_path = bdict.get('move_path', [])
        if self.move_path:
            self.start_pos = self.move_path[0][0]
            self.start_vec = math3d.vector(self.start_pos[0], self.start_pos[1], self.start_pos[2])
            self.end_pos = self.move_path[1][0]
            self.end_vec = math3d.vector(self.end_pos[0], self.end_pos[1], self.end_pos[2])
        self._model_sfx_ids = {}

    def get_model_info(self, unit_obj, bdict):
        type_id = bdict.get('npc_id', self.TYPE_SOLID)
        model_path = self.target_model_path_dict.get(type_id, self.target_model_path_dict[self.TYPE_SOLID])
        merge_info = None
        pos = math3d.vector(*bdict.get('position', [-217, 812, 18030]))
        rot_y = bdict.get('rot_y', 0)
        self.scl_x = bdict.get('scl_x', 1)
        self.scl_y = bdict.get('scl_y', 1)
        self.scl_z = bdict.get('scl_z', 1)
        data = {'pos': pos,'rot_y': rot_y,'scl_x': self.scl_x,
           'scl_y': self.scl_y,'scl_z': self.scl_z,'type_id': type_id
           }
        self.data = data
        return (
         model_path, merge_info, data)

    def on_load_model_complete(self, model, user_data):
        self._create_trace_model(model)
        model.position = user_data['pos']
        model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(0, math.pi * user_data['rot_y'] / 180, 0))
        model.scale = math3d.vector(user_data['scl_x'] * 1.1, user_data['scl_y'] * 1.1, user_data['scl_z'] * 1.1)

    def _modify_model_scale(self, model):
        model.scale = math3d.vector(self.scl_x, self.scl_y, self.scl_z)

    def _create_trace_model(self, model):
        data = self.data if self.data else None
        if not data or not model:
            return
        else:
            type_id = data.get('type_id', self.TYPE_SOLID)
            if type_id != self.TYPE_PATROL:
                return
            model_mgr = global_data.model_mgr
            trace_model_paths = self.trace_model_path.get(type_id)
            model_mgr.create_model_in_scene(model_path=trace_model_paths[0], on_create_func=self.modify_trace)
            return

    def modify_trace(self, trace_model):
        trace_model.scale = math3d.vector(self.scl_x, self.scl_y, self.scl_z * 1.1)
        trace_model.position = (self.end_vec + self.start_vec) * 0.5 + self.TRACE_HIGHT_OFFSET
        trace_model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(0, math.pi * self.data['rot_y'] / 180, 0))

    def modify_trace_side_a(self, trace_side_a_model):
        trace_side_a_model.position = self.model.position + math3d.vector(self.TRACE_LENGTH / NEOX_UNIT_SCALE, 0, 0)
        trace_side_a_model.scale = math3d.vector(1, 1, 1)
        trace_side_a_model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(0, 0, 0))

    def modify_trace_side_b(self, trace_side_b_model):
        trace_side_b_model.position = self.model.position - math3d.vector(self.TRACE_LENGTH / NEOX_UNIT_SCALE, 0, 0)
        trace_side_b_model.scale = math3d.vector(1, 1, 1)
        trace_side_b_model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(0, math.pi, 0))

    def _handle_buff(self, hdl_name, data, left_time, overlying):
        handler = getattr(self, hdl_name) if hasattr(self, hdl_name) else None
        if handler:
            handler(data, left_time, overlying)
        return

    def _remove_buff(self, hdl_name, buff_key, buff_id, buff_idx):
        handler = getattr(self, hdl_name) if hasattr(self, hdl_name) else None
        if handler:
            handler(buff_key, buff_id, buff_idx)
        return

    def handle_fire_debuff(self, data, left_time, *args):
        self._fire_debuff = True
        self.send_event('E_FIRE_EFFECT', True, data.get('big_fire', False))

    def del_fire_debuff(self, buff_key, buff_id, buff_idx):
        self._fire_debuff = False
        self.send_event('E_FIRE_EFFECT', False)

    def _get_fire_debuff(self):
        return self._fire_debuff

    def on_create_model_effect(self, **info):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        for sfx_path, sockets in six.iteritems(info):
            for socket_name in sockets:
                sfx_id_key = sfx_path + socket_name
                if sfx_id_key in self._model_sfx_ids:
                    global_data.sfx_mgr.remove_sfx_by_id(self._model_sfx_ids[sfx_id_key])
                self._model_sfx_ids[sfx_id_key] = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket_name)

    def on_remove_model_effects(self, **info):
        for sfx_path, sockets in six.iteritems(info):
            for socket_name in sockets:
                sfx_id_key = sfx_path + socket_name
                if sfx_id_key in self._model_sfx_ids:
                    global_data.sfx_mgr.remove_sfx_by_id(self._model_sfx_ids[sfx_id_key])
                    del self._model_sfx_ids[sfx_id_key]

    def _on_fire_effect(self, show, big_fire=False):
        if show:
            self.on_create_model_effect(**self.FIRE_EFFECT)
        else:
            self.on_remove_model_effects(**self.FIRE_EFFECT)

    def _on_create_scene_effect(self, sfx, pos, duration):
        global_data.sfx_mgr.create_sfx_in_scene(sfx, math3d.vector(*pos), duration=duration)
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CREATE_SCENE_EFFECT, (sfx, pos, duration)], True)

    def _return_headshoot_type_tag(self):
        type_id = self.data.get('type_id', self.TYPE_PATROL)
        return type_id == self.TYPE_SOLID