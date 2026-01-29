# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/skate_appearance_utils.py
from __future__ import absolute_import
from mobile.common.mobilecommon import singleton
from common.utils.timer import CLOCK
from common.framework import Functor
import world
import os

@singleton
class AllSkateEntityIDRecorder(object):

    def __init__(self):
        self.entity_id_set = set()

    def record(self, entity_id):
        if entity_id is None:
            return False
        else:
            if entity_id in self.entity_id_set:
                return False
            self.entity_id_set.add(entity_id)
            return True

    def reset(self):
        self.entity_id_set.clear()


_all_skate_entity_id_recorder = AllSkateEntityIDRecorder()
COMMON_SKATE_SOCKET_LIST = [
 'effect_01', 'effect_02']
SKATE_MOVE_EFFECT_PATH_MAP = {'6008_skin_sm01': {'fx_airflow': ['effect/fx/vehicle/jindouyun/jindouyun_airflow.sfx']},'6008_skin_sm01a': {'fx_airflow': ['effect/fx/vehicle/jindouyun/jindouyun_airflow.sfx']},'6008_skin_sm01b': {'fx_airflow': ['effect/fx/vehicle/jindouyun/jindouyun_airflow.sfx']},'6008_skin_sm01c': {'fx_airflow': ['effect/fx/vehicle/jindouyun/jindouyun_airflow.sfx']}}
SKATE_SHOW_EFFECT_PATH_MAP = {'6008_skin_sm01': {'fx_airflow': ['effect/fx/vehicle/jindouyun/hb_jindouyun_start.sfx']},'6008_skin_sm01a': {'fx_airflow': ['effect/fx/vehicle/jindouyun/hb_jindouyun_01a_start.sfx']},'6008_skin_sm01b': {'fx_airflow': ['effect/fx/vehicle/jindouyun/hb_jindouyun_01b_start.sfx']},'6008_skin_sm01c': {'fx_airflow': ['effect/fx/vehicle/jindouyun/hb_jindouyun_01c_start.sfx']}}
SKATE_BROKEN_EFFECT_PATH_MAP = {'6008_skin_sm01': {'fx_airflow': ['effect/fx/vehicle/jindouyun/hb_jindouyun_end.sfx']},'6008_skin_sm01a': {'fx_airflow': ['effect/fx/vehicle/jindouyun/hb_jindouyun_01a_end.sfx']},'6008_skin_sm01b': {'fx_airflow': ['effect/fx/vehicle/jindouyun/hb_jindouyun_01b_end.sfx']},'6008_skin_sm01c': {'fx_airflow': ['effect/fx/vehicle/jindouyun/hb_jindouyun_01c_end.sfx']}}
SKATE_MESH_RENDER_PRIORITY_MAP = {'6008_skin_sm01': {'jindouyun': {'tail01': -3,
                                    'tail02': -2,
                                    'jdy02': -1
                                    }
                      },
   '6008_skin_sm01a': {'jindouyun': {'tail01': -3,
                                     'tail02': -2,
                                     'jdy02': -1
                                     }
                       },
   '6008_skin_sm01b': {'jindouyun': {'tail01': -3,
                                     'tail02': -2,
                                     'jdy02': -1
                                     }
                       },
   '6008_skin_sm01c': {'jindouyun': {'tail01': -3,
                                     'tail02': -2,
                                     'jdy02': -1
                                     }
                       }
   }
MOVE_EFFECT_DISAPPEAR_INTERVAL = 0.3

class SkateAppearanceAgent(object):

    def __init__(self, parent=None):
        self.parent = parent
        self.model = None
        self.entity_id = None
        self.set_render_priority_timer = None
        self.showing_move_effect = False
        self.move_sfx_id_list = []
        self.pos_changed_event_registered = False
        self.cur_move_effect_map = {}
        self.delay_remove_move_effect_timer = None
        return

    def _register_pos_changed_event(self, flag):
        if self.pos_changed_event_registered ^ flag:
            self.pos_changed_event_registered = flag
            if G_POS_CHANGE_MGR:
                self.parent.regist_pos_change(self.update_pos, 0.1)
            else:
                self.parent.regist_event('E_POSITION', self.update_pos)

    def _unregister_set_render_priority_timer(self):
        if self.set_render_priority_timer:
            global_data.game_mgr.unregister_logic_timer(self.set_render_priority_timer)
            self.set_render_priority_timer = None
        return

    def destroy(self):
        self._unregister_set_render_priority_timer()
        self._register_pos_changed_event(False)
        self.parent = None
        self.model = None
        self.entity_id = None
        return

    @staticmethod
    def get_model_skin_name(file_name):
        return os.path.basename(os.path.dirname(file_name.replace('\\', '/')))

    def try_set_render_priority(self):
        if self.model and self.model.valid:
            skin_name = self.get_model_skin_name(self.model.filename)
            if skin_name in SKATE_MESH_RENDER_PRIORITY_MAP:
                for socket, render_priority_map in SKATE_MESH_RENDER_PRIORITY_MAP[skin_name].items():
                    socket_obj = self.model.get_socket_obj(socket, 0)
                    if socket_obj:
                        for sub_mesh_name, render_priority in render_priority_map.items():
                            socket_obj.set_submesh_rendergroup_and_priority(sub_mesh_name, world.RENDER_GROUP_TRANSPARENT, render_priority)

                    else:
                        self.set_render_priority_timer = global_data.game_mgr.register_logic_timer(self.try_set_render_priority, interval=1, times=1)
                        return

        self.set_render_priority_timer = None
        return

    def on_skate_model_loaded(self, model, need_handle_common_socket=True):
        self.model = model
        if need_handle_common_socket:
            self.set_common_socket_vis(False)
        self.try_set_render_priority()

    def show_skate_move_effect(self, flag):
        if self.showing_move_effect ^ flag:
            if flag:
                for socket, effect_path_list in self.cur_move_effect_map.items():
                    for effect_path in effect_path_list:
                        self.move_sfx_id_list.append(global_data.sfx_mgr.create_sfx_on_model(effect_path, self.model, socket))

            else:
                for sfx_id in self.move_sfx_id_list:
                    global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

                del self.move_sfx_id_list[:]
                self.delay_remove_move_effect_timer = None
            self.showing_move_effect = flag
        return

    def update_pos(self, *args):
        if self.delay_remove_move_effect_timer is None:
            self.delay_remove_move_effect_timer = global_data.game_mgr.register_logic_timer(lambda : self.show_skate_move_effect(False), interval=MOVE_EFFECT_DISAPPEAR_INTERVAL, times=1, mode=CLOCK)
        else:
            global_data.game_mgr.get_logic_timer().restart(self.delay_remove_move_effect_timer)
        self.show_skate_move_effect(True)
        return

    def on_board_skate(self, model=None):
        if model:
            self.model = model
            self.on_skate_model_loaded(model, need_handle_common_socket=False)
        self.set_common_socket_vis(True)
        skin_name = self.get_model_skin_name(self.model.filename)
        if _all_skate_entity_id_recorder.record(self.entity_id):
            if skin_name in SKATE_SHOW_EFFECT_PATH_MAP:
                for socket, effect_path_list in SKATE_SHOW_EFFECT_PATH_MAP[skin_name].items():
                    for effect_path in effect_path_list:
                        global_data.sfx_mgr.create_sfx_on_model(effect_path, self.model, socket)

        if self.parent:
            if skin_name in SKATE_MOVE_EFFECT_PATH_MAP:
                self.cur_move_effect_map = SKATE_MOVE_EFFECT_PATH_MAP[skin_name]
                self._register_pos_changed_event(True)

    def on_leave_skate(self):
        self.set_common_socket_vis(False)
        self.model = None
        if self.parent:
            self._register_pos_changed_event(False)
        self._unregister_set_render_priority_timer()
        return

    def set_common_socket_vis(self, vis):
        if not self.model or not self.model.valid:
            return
        for i in range(1, 10):
            socket = 'effect_%02d' % i
            if not self.model.has_socket(socket):
                break
            self.model.set_socket_bound_obj_active(socket, 0, vis)

    @staticmethod
    def on_destroyed_sfx_create_callback(sfx, rotation_matrix):
        if sfx:
            sfx.rotation_matrix = rotation_matrix

    def on_skate_destroyed(self):
        if self.model and self.model.valid:
            skin_name = self.get_model_skin_name(self.model.filename)
            if skin_name in SKATE_BROKEN_EFFECT_PATH_MAP:
                for socket, effect_path_list in SKATE_BROKEN_EFFECT_PATH_MAP[skin_name].items():
                    socket_mat = self.model.get_socket_matrix(socket, world.SPACE_TYPE_WORLD)
                    if not socket_mat:
                        continue
                    socket_pos = socket_mat.translation
                    socket_rot_mat = socket_mat.rotation
                    for effect_path in effect_path_list:
                        global_data.sfx_mgr.create_sfx_in_scene(effect_path, socket_pos, duration=1.5, on_create_func=Functor(self.on_destroyed_sfx_create_callback, rotation_matrix=socket_rot_mat))

            else:
                global_data.sfx_mgr.create_sfx_in_scene('effect/fx/niudan/daojubeicuihui.sfx', self.model.world_position, duration=1.5)
        if self.parent:
            self._register_pos_changed_event(False)
        self._unregister_set_render_priority_timer()

    def set_cur_skate_entity_id(self, entity_id):
        self.entity_id = entity_id


record_skate_entity_id = _all_skate_entity_id_recorder.record
reset_skate_entity_id_recorder = _all_skate_entity_id_recorder.reset