# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_art_check/ComArtCheckSocketLogic.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from common.animate import animator
from logic.gcommon.common_const.character_anim_const import HAIR_DIR_TYPE, HAIR_SINGLE_TYPE
from logic.gcommon.common_const import lobby_ani_const
from common.algorithm import resloader
import game3d
import world
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.cdata import status_config
from common.cfg import confmgr
from logic.gcommon.item.item_const import FASHION_POS_SUIT
XML_PATH = 'animator_conf/hair.xml'
SINGLE_TYPE_IDLE = 1
SINGLE_TYPE_RUN = 2
SINGLE_TYPE_DYING = 3

class ComArtCheckSocketLogic(UnitCom):
    BIND_EVENT = {'E_INIT_HAIR_MODEL': 'on_init_hair_model',
       'E_INIT_BODY_SOCKET_ANIMATOR': 'on_init_body_socket_animator',
       'E_DESTROY_HAIR_ANIMATOR': 'destroy_hair_animator',
       'E_DESTROY_BODY_SOCKET_ANIMATOR': 'destroy_body_socket_animator',
       'E_SET_ANIMATOR_FLOAT_STATE': 'set_ani_float_state',
       'E_SET_ANIMATOR_INT_STATE': 'set_ani_int_state'
       }

    def __init__(self):
        super(ComArtCheckSocketLogic, self).__init__(False)
        self.hair_animator = None
        self.body_socket_animators = []
        self.body_socket_animators_count = 0
        self.cur_animators_loaded_count = 0
        self.sd.ref_hair_model = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComArtCheckSocketLogic, self).init_from_dict(unit_obj, bdict)

    def on_init_hair_model(self):
        model = self.ev_g_model()
        if not model:
            return
        hair_model = model.get_socket_obj('gj_hair', 0)
        if hair_model:
            hair_model.visible = model.visible
            hair_model.cast_shadow = True
            hair_model.receive_shadow = True
            self.load_hair_animator(hair_model)
            self.sd.ref_hair_model = hair_model

    def load_hair_animator(self, model):
        self.destroy_hair_animator()
        self.hair_animator = animator.Animator(model, XML_PATH, self.unit_obj)
        self.hair_animator.Load(True, self.on_load_animator_complete)

    def on_load_animator_complete(self, *args):
        self.init_animators_state()

    def init_animators_state(self):
        self.reset_animator_state()

    def reset_animator_state(self):
        if self.hair_animator:
            self.hair_animator.SetInt(HAIR_DIR_TYPE, 1)
            self.hair_animator.SetInt(HAIR_SINGLE_TYPE, SINGLE_TYPE_IDLE)
        for animator_obj in self.body_socket_animators:
            animator_obj.SetInt(HAIR_DIR_TYPE, 1)
            animator_obj.SetInt(HAIR_SINGLE_TYPE, SINGLE_TYPE_IDLE)

    def load_body_socket_animator(self, model):
        animator_obj = animator.Animator(model, XML_PATH, self.unit_obj)
        self.body_socket_animators.append(animator_obj)
        animator_obj.Load(True, self.on_load_body_socket_animator_complete)

    def on_load_body_socket_animator_complete(self, *args):
        self.cur_animators_loaded_count += 1
        if self.cur_animators_loaded_count == self.body_socket_animators_count:
            self.init_animators_state()

    def on_init_body_socket_animator(self):
        model = self.ev_g_model()
        if not model:
            return
        dressed_clothing_id = self.ev_g_dress_id()
        animator_sockets = confmgr.get('role_info', 'RoleSkin', 'Content', str(dressed_clothing_id), 'animator_sockets')
        self.body_socket_animators_count = 0
        self.cur_animators_loaded_count = 0
        if animator_sockets:
            socket_model_list = []
            for socket_name in animator_sockets:
                socket_model = model.get_socket_obj(socket_name, 0)
                if socket_model:
                    socket_model.visible = model.visible
                    socket_model.cast_shadow = True
                    socket_model.receive_shadow = True
                    socket_model_list.append(socket_model)

            self.body_socket_animators_count = len(socket_model_list)
            for socket_model in socket_model_list:
                self.load_body_socket_animator(socket_model)

    def destroy_hair_animator(self):
        if self.hair_animator:
            self.hair_animator.destroy()
            self.hair_animator = None
        return

    def destroy_body_socket_animator(self):
        for animator_obj in self.body_socket_animators:
            animator_obj.destroy()

        self.body_socket_animators = []

    def destroy(self):
        self.sd.ref_hair_model = None
        self.destroy_hair_animator()
        self.destroy_body_socket_animator()
        return

    def set_ani_float_state(self, name, value):
        if not self.hair_animator and not self.body_socket_animators:
            return
        name = 'dir_y' if name == 'dir_z' else name
        value = float('%.2f' % value)
        if self.hair_animator:
            self.hair_animator.SetFloat(name, value)
        for animator_obj in self.body_socket_animators:
            animator_obj.SetFloat(name, value)

    def set_ani_int_state(self, name, value):
        if not self.hair_animator and not self.body_socket_animators:
            return
        else:
            if name == 'state_idx':
                hair_dir_type_value = None
                hair_single_type_value = SINGLE_TYPE_IDLE
                if value == lobby_ani_const.STATE_MOVE:
                    hair_dir_type_value = 7
                else:
                    hair_dir_type_value = 1
                    hair_single_type_value = SINGLE_TYPE_IDLE
                if self.hair_animator:
                    self.hair_animator.SetInt(HAIR_DIR_TYPE, hair_dir_type_value)
                    self.hair_animator.SetInt(HAIR_SINGLE_TYPE, hair_single_type_value)
                for animator_obj in self.body_socket_animators:
                    animator_obj.SetInt(HAIR_DIR_TYPE, hair_dir_type_value)
                    animator_obj.SetInt(HAIR_SINGLE_TYPE, hair_single_type_value)

            return