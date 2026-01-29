# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_art_check/ComArtCheckMechaModel.py
from __future__ import absolute_import
from common.utils.path import check_file_exist
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

class ComArtCheckMechaModel(UnitCom):
    BIND_EVENT = {'E_CALL_MECHA': 'on_call_mecha',
       'E_SWITCH_LOD': 'on_switch_lod',
       'E_POSITION': 'on_pos_changed',
       'G_MODEL': 'get_model',
       'G_ANIMATOR': 'get_animator',
       'G_MECHA_ID': 'get_mecha_id',
       'G_DRESS_ID': 'get_dress_id',
       'E_SET_ROTATION_MATRIX': 'on_set_rotation_matrix',
       'E_SET_ANIMATOR_INT_STATE': 'set_ani_int_state',
       'E_SET_ANIMATOR_FLOAT_STATE': 'set_ani_float_state',
       'G_IS_AVATAR': 'is_avatar'
       }
    MODEL_INIT_POS = (0, 300, 0)

    def __init__(self):
        super(ComArtCheckMechaModel, self).__init__()
        self.model = None
        self.model_id = None
        self.animator = None
        self.mecha_id = None
        self.skin_folder = None
        self.lod_level = 'h'
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComArtCheckMechaModel, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_is_mecha = True
        self.sd.ref_mecha_id = bdict.get('mecha_id', '8001')
        self.lod_level = bdict.get('lod', 'h')
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self.on_pos_changed)

    def on_post_init_complete(self, bdict):
        if not self.on_call_mecha(bdict.get('mecha_id', 8001), bdict.get('skin_folder', '8001')):
            global_data.emgr.on_player_rechoose_mecha_event.emit()
            global_data.game_mgr.show_tip('\xe6\x97\xa0\xe6\x95\x88\xe7\x9a\x84\xe6\x9c\xba\xe7\x94\xb2\xe7\x9a\xae\xe8\x82\xa4\xe8\xb7\xaf\xe5\xbe\x84')

    def on_call_mecha(self, mecha_id, skin_folder=None, lod=None):
        if skin_folder is None:
            skin_folder = mecha_id
        if lod is not None:
            self.lod_level = lod
        empty_path = 'model_new/mecha/{}/{}/empty.gim'.format(mecha_id, skin_folder)
        if not check_file_exist(empty_path):
            empty_path = 'model_new/mecha/{}/{}/empty.gim'.format(mecha_id, mecha_id)
            if not check_file_exist(empty_path):
                return False
        self.mesh_folder = 'model_new/mecha/{}/{}'.format(mecha_id, skin_folder)
        sub_mesh_path = '{}/{}.gim'.format(self.mesh_folder, self.lod_level)
        if not check_file_exist(sub_mesh_path):
            return False
        else:
            self.mecha_id = mecha_id
            self.skin_folder = skin_folder
            self.model_path = empty_path
            self.sub_mesh_list = [sub_mesh_path]
            self.load_model()
            return True

    def load_model(self):
        if not self.model_path or not self.sub_mesh_list:
            return
        else:
            model_pos = math3d.vector(*self.MODEL_INIT_POS)
            if self.model and self.model.valid:
                model_pos = self.model.world_position
                self.model.destroy()
                self.model = None
            self.model_id = global_data.model_mgr.create_model_in_scene(self.model_path, pos=model_pos, mesh_path_list=self.sub_mesh_list, on_create_func=self.on_load_model_complete)
            return

    def on_load_model_complete(self, model, *args):
        global_data.model = model
        self.model = model
        self.animator = animator.Animator(self.model, 'animator_conf/mecha/mecha.xml', self.unit_obj)
        self.animator.Load(False, self.on_load_animator_complete)
        self.send_event('E_MODEL_LOADED', model)
        self.send_event('E_INIT_SPRING_ANI')
        if self.model:
            self.model.cast_shadow = True
            self.model.receive_shadow = True
        global_data.emgr.update_role_id.emit(self.mecha_id, is_mecha=True)

    def on_load_animator_complete(self, *args):
        self.send_event('E_ANIMATOR_LOADED')

    def on_switch_lod(self, lod):
        if not self.model or not self.model.valid:
            return
        cur_mesh = '{}/{}.gim'.format(self.mesh_folder, self.lod_level)
        self.model.remove_mesh(cur_mesh)
        new_mesh = '{}/{}.gim'.format(self.mesh_folder, lod)
        self.model.add_mesh(new_mesh)
        self.lod_level = lod

    def get_model(self):
        return self.model

    def get_animator(self):
        return self.animator

    def get_mecha_id(self):
        return self.mecha_id

    def get_dress_id(self):
        return self.dress_id

    def on_pos_changed(self, pos):
        if self.model and self.model.valid:
            self.model.world_position = pos

    def on_set_rotation_matrix(self, matrix):
        if self.model and self.model.valid:
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

    def destroy(self):
        super(ComArtCheckMechaModel, self).destroy()
        if self.model and self.model.valid:
            self.model.destroy()
            self.model = None
        return

    def is_avatar(self):
        return True