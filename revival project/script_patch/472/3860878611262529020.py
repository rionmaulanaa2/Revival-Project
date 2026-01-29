# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_art_check/ComArtCheckModel.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.common_const import lobby_ani_const
from logic.gcommon.component.UnitCom import UnitCom
from common.algorithm import resloader
from logic.gutils import dress_utils
from common.animate import animator
import game3d
import world
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE
from common.cfg import confmgr
import math3d
from logic.vscene.parts.PartArtCheckModelDisplay import enable_outline, disable_outline, check_add_mesh_valid
import copy
BODY_LOD = {'l': 'l.gim',
   'l1': 'l1.gim',
   'l2': 'l2.gim',
   'l3': 'l3.gim'
   }
HEAD_LOD = {'l': 'parts/l_head.gim',
   'l1': 'parts/l1_head.gim',
   'l2': 'parts/l2_head.gim',
   'l3': 'parts/l3_head.gim'
   }

class ComArtCheckModel(UnitCom):
    BIND_EVENT = {'E_POSITION': 'on_pos_changed',
       'G_MODEL': 'get_model',
       'G_ANIMATOR': 'get_animator',
       'G_ROLE_ID': 'get_role_id',
       'G_DRESS_ID': 'get_dress_id',
       'E_SET_ROTATION_MATRIX': 'on_set_rotation_matrix',
       'E_SET_ANIMATOR_INT_STATE': 'set_ani_int_state',
       'E_SET_ANIMATOR_FLOAT_STATE': 'set_ani_float_state',
       'E_CHANGE_MODEL': 'on_change_model',
       'E_ENABLE_OUTLINE': 'on_enable_outline',
       'E_DISABLE_OUTLINE': 'on_disable_outline'
       }

    def __init__(self):
        super(ComArtCheckModel, self).__init__(True)
        self.model = None
        self.model_id = None
        self.animator = None
        self.role_id = 11
        self.res_path = 'character/11/2000/empty.gim'
        self.mesh_path_list = ['character/11/2000/l.gim', 'character/11/2000/parts/l_head.gim']
        self.pendant_list = []
        self.sfx_list = []
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComArtCheckModel, self).init_from_dict(unit_obj, bdict)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self.on_pos_changed)

    def tick(self, delta):
        if not self.model_id:
            self.load_model()
            self.need_update = False

    def on_change_model(self, model_data):
        if not model_data:
            return
        else:
            if self.model:
                self.model.destroy()
                self.model = None
            if self.animator:
                self.animator.destroy()
                self.animator = None
            self.pendant_list = []
            self.sfx_list = []
            model_path = model_data.get('m_path', None)
            pendant_list = model_data.get('pendant', [])
            sfx_list = model_data.get('sfx', [])
            lod = model_data.get('lod', [])
            self.res_path = model_path
            self.mesh_path_list = [copy.copy(model_path).replace('empty.gim', BODY_LOD.get(lod, 'l.gim')),
             copy.copy(model_path).replace('empty.gim', HEAD_LOD.get(lod, 'parts/l_head.gim'))]
            for pendant_data in pendant_list:
                if not pendant_data:
                    continue
                socket_name = pendant_data.get('socket_name')
                pendant_path = pendant_data.get('pendant_path')
                if 'h_' in pendant_path:
                    print(pendant_path, model_data)
                    pendant_path.replace('h_', lod)
                elif 'h.gim' in pendant_path:
                    pendant_path.replace('h.gim', BODY_LOD.get(lod))
                if not socket_name:
                    pendant = world.model(pendant_path, None)
                    empty_model = world.model(self.res_path, None)
                    if not pendant_path:
                        global_data.game_mgr.show_tip('\xe6\x8c\x82\xe4\xbb\xb6{}\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8'.format(pendant_path))
                        continue
                    elif not check_add_mesh_valid(pendant, empty_model):
                        global_data.game_mgr.show_tip('\xe6\x8c\x82\xe4\xbb\xb6{}\xe4\xb8\x8e\xe6\xa8\xa1\xe5\x9e\x8b\xe9\xaa\xa8\xe9\xaa\xbc\xe4\xb8\x8d\xe5\x8c\xb9\xe9\x85\x8d'.format(pendant_path))
                        continue
                    self.mesh_path_list.append(pendant_path)
                else:
                    self.pendant_list.append((socket_name, pendant_path))

            for sfx_data in sfx_list:
                socket_name = sfx_data.get('socket_name')
                second_socket_name = sfx_data.get('second_socket_name')
                sfx_path = sfx_data.get('sfx_path')
                self.sfx_list.append((socket_name, second_socket_name, sfx_path))

            self.load_model()
            return

    def load_model(self):
        self.role_id = 11
        self.dress_id = 201001100
        self.model_id = global_data.model_mgr.create_model_in_scene(self.res_path, pos=math3d.vector(0, 300, 0), mesh_path_list=self.mesh_path_list, on_create_func=self.on_load_model_complete, create_scene=global_data.artcheck_scene)

    def on_load_model_complete(self, model, *args):
        global_data.model = model
        model.set_submesh_visible('empty', False)
        self.model = model
        self.animator = animator.Animator(self.model, lobby_ani_const.XML_PATH, self.unit_obj)
        self.animator.Load(False, self.on_load_animator_complete)
        self.send_event('E_INIT_HAIR_MODEL')
        self.send_event('E_INIT_BODY_SOCKET_ANIMATOR')
        self.send_event('E_INIT_SPRING_ANI')
        if self.model:
            self.model.cast_shadow = True
            self.model.receive_shadow = True
        global_data.emgr.update_role_id.emit(self.role_id)
        global_data.emgr.trigger_lobby_player_move.emit(math3d.vector(1, 0, 0))
        global_data.emgr.trigger_lobby_player_move_stop.emit()
        self.update_pendant()
        self.update_sfx()

    def update_pendant(self):
        if not self.model or not self.model.valid:
            return
        else:
            for socket, pendant_path in self.pendant_list:
                model = world.model(pendant_path, None)
                if self.model.has_socket(socket):
                    self.model.bind(socket, model)
                else:
                    global_data.game_mgr.show_tip('\xe6\x8c\x82\xe4\xbb\xb6{}\xe6\x8c\x82\xe6\x8e\xa5\xe4\xb8\x8d\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe7\xbc\xba\xe5\xb0\x91\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9{}'.format(pendant_path, socket))

            return

    def update_sfx(self):
        if not self.model or not self.model.valid:
            return
        else:
            for socket_name, second_socket_name, sfx_path in self.sfx_list:
                if not self.model.has_socket(socket_name):
                    global_data.game_mgr.show_tip('\xe7\x89\xb9\xe6\x95\x88{}\xe6\x8c\x82\xe6\x8e\xa5\xe4\xb8\x8d\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe4\xbd\x8e\xe6\xa8\xa1\xe7\xbc\xba\xe5\xb0\x91\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9{}'.format(sfx_path, socket_name))
                    continue
                if second_socket_name:
                    if socket_name == 'head':
                        if not self.model.has_socket(second_socket_name):
                            global_data.game_mgr.show_tip('\xe7\x89\xb9\xe6\x95\x88{}\xe6\x8c\x82\xe6\x8e\xa5\xe4\xb8\x8d\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe4\xbd\x8e\xe6\xa8\xa1head\xe7\xbc\xba\xe5\xb0\x91\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9{}'.format(sfx_path, second_socket_name))
                        else:
                            sfx = world.sfx(sfx_path, scene=None)
                            self.model.bind(second_socket_name, sfx, world.BIND_TYPE_ALL)
                    else:
                        socket_objs = self.model.get_socket_objects(socket_name)
                        for obj in socket_objs:
                            if str(obj.filename).endswith('.gim'):
                                if not obj.has_socket(second_socket_name):
                                    global_data.game_mgr.show_tip('\xe7\x89\xb9\xe6\x95\x88{}\xe6\x8c\x82\xe6\x8e\xa5\xe4\xb8\x8d\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe4\xbd\x8e\xe6\xa8\xa1\xe6\x8c\x82\xe4\xbb\xb6\xe7\xbc\xba\xe5\xb0\x91\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9{}'.format(sfx_path, socket_name))
                                else:
                                    sfx = world.sfx(sfx_path, scene=None)
                                    obj.bind(second_socket_name, sfx, world.BIND_TYPE_ALL)

                else:
                    sfx = world.sfx(sfx_path, scene=None)
                    self.model.bind(socket_name, sfx, world.BIND_TYPE_ALL)

            return

    def on_load_animator_complete(self, *args):
        self.send_event('E_ANIMATOR_LOADED')

    def get_model(self):
        return self.model

    def get_animator(self):
        return self.animator

    def get_role_id(self):
        return self.role_id

    def get_dress_id(self):
        return self.dress_id

    def on_pos_changed(self, pos):
        if self.model:
            self.model.world_position = pos

    def on_set_rotation_matrix(self, matrix):
        if self.model:
            self.model.world_rotation_matrix = matrix

    def set_ani_int_state(self, name, value):
        if self.animator:
            self.animator.SetInt(name, value)

    def set_ani_float_state(self, name, value):
        if self.animator:
            value = float('%.2f' % value)
            self.animator.SetFloat(name, value)
            if self.sd.ref_animator_mirror:
                self.sd.ref_animator_mirror.SetFloat(name, value)

    def on_enable_outline(self):
        if not self.model:
            return
        enable_outline(self.model)
        socket_objs = self.model.get_all_objects_on_sockets()
        for obj in socket_objs:
            if '.gim' in obj.filename:
                enable_outline(obj)

    def on_disable_outline(self):
        if not self.model:
            return
        disable_outline(self.model)
        socket_objs = self.model.get_all_objects_on_sockets()
        for obj in socket_objs:
            if '.gim' in obj.filename:
                enable_outline(obj)

    def destroy(self):
        super(ComArtCheckModel, self).destroy()
        if self.model and self.model.valid:
            self.model.destroy()
            self.model = None
        return