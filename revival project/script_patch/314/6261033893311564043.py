# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHairLogic.py
from __future__ import absolute_import
import six
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
EMPTY_HAND_XML_PATH = 'animator_conf/hair_with_emptyhand.xml'
BLEND_STATE_SET = set([status_config.ST_MOVE,
 status_config.ST_SHOOT,
 status_config.ST_SWITCH,
 status_config.ST_RELOAD,
 status_config.ST_LOAD,
 status_config.ST_AIM,
 status_config.ST_PICK,
 status_config.ST_USE_ITEM,
 status_config.ST_RELOAD_LOOP,
 status_config.ST_WEAPON_ACCUMULATE,
 status_config.ST_HIT])
HAIR_BLEND_TYPE_7 = 7
HAIR_BLEND_TYPE_7_MOVE = 3
HAIR_BLEND_TYPE_SINGLE = 1
HAIR_BLEND_TYPE_7_EMPTY_HAND = 4
SINGLE_TYPE_IDLE = 1
SINGLE_TYPE_RUN = 2
SINGLE_TYPE_DYING = 3
SINGLE_TYPE_INTERACTION = 4
INTERACTION_NODE_NAME = 'src_interaction'
EXTRA_HAIR_SOCKET = {'201001370': 'hair_13_2012',
   '201001371': 'hair_13_2012',
   '201001372': 'hair_13_2012'
   }

class ComHairLogic(UnitCom):
    BIND_EVENT = {'E_INIT_HAIR_MODEL': 'on_init_hair_model',
       'E_INIT_BODY_SOCKET_ANIMATOR': 'on_init_body_socket_animator',
       'E_DESTROY_HAIR_ANIMATOR': 'destroy_hair_animator',
       'E_DESTROY_BODY_SOCKET_ANIMATOR': 'destroy_body_socket_animator',
       'E_SET_ANIMATOR_FLOAT_STATE': 'set_ani_float_state',
       'E_SET_ANIMATOR_INT_STATE': 'set_ani_int_state',
       'E_ENTER_STATE': 'enter_states',
       'E_LEAVE_STATE': 'leave_states',
       'E_CHANGE_ANIM_MOVE_DIR': 'change_anim_move_dir',
       'E_UPDATE_INTERACTION_NAME': 'update_interaction_name'
       }

    def __init__(self):
        super(ComHairLogic, self).__init__(False)
        self.hair_animator = None
        self.body_socket_animators = {}
        self.sd.ref_hair_model = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComHairLogic, self).init_from_dict(unit_obj, bdict)

    def get_cur_xml(self):
        cur_xml = XML_PATH
        if not global_data.battle:
            fashion_dict = self.ev_g_fashion_info()
            if fashion_dict:
                dressed_clothing_id = fashion_dict.get(FASHION_POS_SUIT)
                animator_with_emptyhand = confmgr.get('role_info', 'RoleSkin', 'Content', str(dressed_clothing_id), 'animator_with_emptyhand')
                if animator_with_emptyhand:
                    cur_xml = EMPTY_HAND_XML_PATH
        return cur_xml

    def on_init_hair_model(self):
        model = self.ev_g_model()
        if not model:
            return
        else:
            socket_name = 'gj_hair'
            if global_data.battle:
                fashion_data = self.ev_g_fashion()
            else:
                fashion_data = self.ev_g_fashion_info()
            if fashion_data:
                dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
                extra_socket = EXTRA_HAIR_SOCKET.get(str(dressed_clothing_id), None)
                if extra_socket:
                    socket_name = extra_socket
            hair_model = model.get_socket_obj(socket_name)
            self.destroy_hair_animator()
            if hair_model and type(hair_model) == world.model:
                hair_model.visible = model.visible
                hair_model.cast_shadow = True
                hair_model.receive_shadow = True
                self.load_hair_animator(hair_model)
                self.sd.ref_hair_model = hair_model
            return

    def load_hair_animator(self, model):
        self.hair_animator = animator.Animator(model, self.get_cur_xml(), self.unit_obj)
        self.hair_animator.Load(False, self.on_load_animator_complete)

    def on_load_animator_complete(self, *args):
        self.init_animators_state()

    def init_animators_state(self):
        if global_data.battle:
            self.check_blend_state()
            walk_direction = self.ev_g_walk_direction()
            if walk_direction:
                self.change_anim_move_dir(walk_direction.x, walk_direction.z)
        else:
            self.reset_animator_state()

    def reset_animator_state(self):
        if self.hair_animator:
            self.hair_animator.SetInt(HAIR_DIR_TYPE, HAIR_BLEND_TYPE_7)
            self.hair_animator.SetInt(HAIR_SINGLE_TYPE, SINGLE_TYPE_IDLE)
        for animator_obj in six.itervalues(self.body_socket_animators):
            animator_obj.SetInt(HAIR_DIR_TYPE, HAIR_BLEND_TYPE_7)
            animator_obj.SetInt(HAIR_SINGLE_TYPE, SINGLE_TYPE_IDLE)

    def load_body_socket_animator(self, socket_name, model):
        animator_obj = animator.Animator(model, self.get_cur_xml(), self.unit_obj)
        self.body_socket_animators[socket_name] = animator_obj
        animator_obj.Load(False, self.on_load_body_socket_animator_complete)

    def on_load_body_socket_animator_complete(self, *args):
        self.init_animators_state()

    def on_init_body_socket_animator(self, socket_name=None):
        model = self.ev_g_model()
        if not model:
            return
        if global_data.battle:
            fashion_dict = self.ev_g_fashion()
        else:
            fashion_dict = self.ev_g_fashion_info()
        if fashion_dict:
            dressed_clothing_id = fashion_dict.get(FASHION_POS_SUIT)
            animator_sockets = confmgr.get('role_info', 'RoleSkin', 'Content', str(dressed_clothing_id), 'animator_sockets')
            if animator_sockets:
                if socket_name:
                    if socket_name in animator_sockets:
                        self.destroy_single_socket_animator(socket_name)
                        socket_model = model.get_socket_objects(socket_name)[0]
                        self.load_body_socket_animator(socket_name, socket_model)
                else:
                    socket_models = {}
                    for socket_name in animator_sockets:
                        socket_model = model.get_socket_obj(socket_name, 0)
                        if socket_model:
                            socket_model.visible = model.visible
                            socket_model.cast_shadow = True
                            socket_model.receive_shadow = True
                            socket_models[socket_name] = socket_model

                    if socket_models:
                        self.destroy_body_socket_animator()
                        for socket_name, socket_model in six.iteritems(socket_models):
                            self.load_body_socket_animator(socket_name, socket_model)

    def destroy_hair_animator(self):
        if self.hair_animator:
            self.hair_animator.destroy()
            self.hair_animator = None
        return

    def destroy_single_socket_animator(self, socket_name):
        animator_obj = self.body_socket_animators.get(socket_name)
        if animator_obj:
            animator_obj.destroy()
        self.body_socket_animators[socket_name] = None
        return

    def destroy_body_socket_animator(self):
        for animator_obj in six.itervalues(self.body_socket_animators):
            animator_obj.destroy()

        self.body_socket_animators = {}

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
        for animator_obj in six.itervalues(self.body_socket_animators):
            animator_obj.SetFloat(name, value)

    def set_ani_int_state(self, name, value):
        if not self.hair_animator and not self.body_socket_animators:
            return
        else:
            if name == 'state_idx':
                hair_blend_type = None
                hair_single_type_value = SINGLE_TYPE_IDLE
                if value == lobby_ani_const.STATE_MOVE:
                    hair_blend_type = HAIR_BLEND_TYPE_7
                else:
                    hair_blend_type = HAIR_BLEND_TYPE_SINGLE
                if self.hair_animator:
                    self.hair_animator.SetInt(HAIR_DIR_TYPE, hair_blend_type)
                    self.hair_animator.SetInt(HAIR_SINGLE_TYPE, hair_single_type_value)
                for animator_obj in six.itervalues(self.body_socket_animators):
                    animator_obj.SetInt(HAIR_DIR_TYPE, hair_blend_type)
                    animator_obj.SetInt(HAIR_SINGLE_TYPE, hair_single_type_value)

            return

    def update_interaction_name(self, gesture_name):
        if self.hair_animator and self.sd.ref_hair_model.has_anim(gesture_name):
            self.hair_animator.SetInt(HAIR_DIR_TYPE, HAIR_BLEND_TYPE_SINGLE)
            self.hair_animator.SetInt(HAIR_SINGLE_TYPE, SINGLE_TYPE_INTERACTION)
            self.hair_animator.replace_clip_name(INTERACTION_NODE_NAME, gesture_name, force=True)

    def enter_states(self, new_state):
        self.check_blend_state()

    def leave_states(self, leave_state, new_state=None):
        self.check_blend_state()

    def check_blend_state(self):
        if not self.hair_animator and not self.body_socket_animators:
            return
        else:
            all_state = self.ev_g_get_all_state()
            if all_state:
                hair_dir_type_value = None
                body_dir_type_value = None
                hair_single_type_value = None
                if all_state.issubset(BLEND_STATE_SET):
                    hair_dir_type_value = HAIR_BLEND_TYPE_7
                    body_dir_type_value = HAIR_BLEND_TYPE_7
                else:
                    hair_dir_type_value = HAIR_BLEND_TYPE_SINGLE
                    body_dir_type_value = HAIR_BLEND_TYPE_SINGLE
                    if self.ev_g_get_state(status_config.ST_RUN):
                        hair_single_type_value = SINGLE_TYPE_RUN
                    elif self.ev_g_get_state(status_config.ST_DOWN):
                        hair_single_type_value = SINGLE_TYPE_DYING
                    else:
                        hair_single_type_value = SINGLE_TYPE_IDLE
                if self.hair_animator:
                    self.hair_animator.SetInt(HAIR_DIR_TYPE, hair_dir_type_value)
                    self.hair_animator.SetInt(HAIR_SINGLE_TYPE, hair_single_type_value)
                for animator_obj in six.itervalues(self.body_socket_animators):
                    animator_obj.SetInt(HAIR_DIR_TYPE, body_dir_type_value)
                    animator_obj.SetInt(HAIR_SINGLE_TYPE, hair_single_type_value)

            return

    def change_anim_move_dir(self, dir_x, dir_y, *args):
        if not self.hair_animator and not self.body_socket_animators:
            return
        if not self.ev_g_get_state(status_config.ST_MOVE):
            return
        if self.hair_animator:
            self.hair_animator.SetFloat('dir_x', dir_x)
            self.hair_animator.SetFloat('dir_y', dir_y)
        for animator_obj in six.itervalues(self.body_socket_animators):
            animator_obj.SetFloat('dir_x', dir_x)
            animator_obj.SetFloat('dir_y', dir_y)