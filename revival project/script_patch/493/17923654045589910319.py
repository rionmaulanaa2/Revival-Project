# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHumanIKController.py
from __future__ import absolute_import
from __future__ import print_function
from ..UnitCom import UnitCom
import weakref
import world
from logic.gcommon.const import NEOX_UNIT_SCALE
import data.weapon_action_config as weapon_action_config
import logic.gcommon.common_const.collision_const as collision_const
import collision
LEFT_FOOT_IK_ID = 'Lfoot'
RIGHT_FOOT_IK_ID = 'Rfoot'
FOOT_IK_GROUP = collision_const.GROUP_CLIMB_CHECK | collision_const.GROUP_SKATE_INCLUDE
FOOT_IK_MASK = 65535

class ComHumanIKController(UnitCom):
    BIND_EVENT = {'E_HUMAN_MODEL_LOADED': 'on_model_loaded',
       'E_GUN_MODEL_LOADED': 'set_gun_vector',
       'S_GUN_IK_ENABLE': 'set_hand_ik_enable',
       'S_FOOT_IK_ENABLE': 'set_foot_ik_enable',
       'E_CHARACTER_ATTR': '_change_character_attr',
       'E_UPDATE_FOOT_IK_PARAM': 'update_foot_ik_param'
       }

    def __init__(self):
        super(ComHumanIKController, self).__init__()
        self._model = None
        self.inited = False
        self.foot_ik_enable = False
        self.hand_ik_enable = False
        self.left_foot_ik = None
        self.right_foot_ik = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComHumanIKController, self).init_from_dict(unit_obj, bdict)

    def on_model_loaded(self, *arg):
        self.init_humam_ik()

    def init_humam_ik(self):
        model = self.ev_g_model()
        if not model:
            return
        model.set_custom_ik_solver(world.handik(), 1)
        model.set_handik_enable(self.hand_ik_enable)

    def update_foot_ik_param(self, ray_raise_height, ray_length, suspend_height, speculative_height, sink_speed):
        return
        model = self.ev_g_model()
        if not model:
            return
        else:
            if not getattr(model, 'get_ik_mgr', None):
                return
            if not global_data.feature_mgr.is_support_new_foot_ik():
                return
            ik_mgr = model.get_ik_mgr()
            if self.left_foot_ik:
                self.left_foot_ik.remove_foot_chain('biped l calf')
            else:
                self.left_foot_ik = ik_mgr.create_foot_ik(LEFT_FOOT_IK_ID, 'biped l thigh', 0)
                self.left_foot_ik.set_raycast_property(FOOT_IK_MASK, FOOT_IK_GROUP, collision.INCLUDE_FILTER)
            if self.right_foot_ik:
                self.right_foot_ik.remove_foot_chain('biped r calf')
            else:
                self.right_foot_ik = ik_mgr.create_foot_ik(RIGHT_FOOT_IK_ID, 'biped r thigh', 0)
                self.right_foot_ik.set_raycast_property(FOOT_IK_MASK, FOOT_IK_GROUP, collision.INCLUDE_FILTER)
            self.left_foot_ik.add_foot_chain('biped l calf', suspend_height, speculative_height)
            self.left_foot_ik.set_raycast_line(ray_raise_height, ray_length)
            self.left_foot_ik.sink_speed = sink_speed
            self.right_foot_ik.add_foot_chain('biped r calf', suspend_height, speculative_height)
            self.right_foot_ik.set_raycast_line(ray_raise_height, ray_length)
            self.right_foot_ik.sink_speed = sink_speed
            return

    def _change_character_attr(self, name, *arg):
        if name == 'animator_info':
            print(('test--ComHumanIKController--animator_info--hand_ik_enable =', self.hand_ik_enable, '--foot_ik_enable = ', self.foot_ik_enable, '--left_foot_ik =', self.left_foot_ik, '--self.unit_obj =', self.unit_obj))

    def set_hand_ik_enable(self, enable):
        self.hand_ik_enable = enable
        human_model = self.ev_g_model()
        if human_model:
            gun_model = self.sd.ref_hand_weapon_model
            enable = enable and bool(gun_model)
            if enable:
                self.set_gun_vector(gun_model, enable)
            human_model.set_handik_enable(enable)

    def set_foot_ik_enable(self, enable):
        self.foot_ik_enable = enable
        model = self.ev_g_model()
        if not model:
            return
        else:
            if self.left_foot_ik and self.right_foot_ik:
                ik_mgr = model.get_ik_mgr()
                ik_mgr.enabled = enable
                self.left_foot_ik.enabled = enable
                self.right_foot_ik.enabled = enable
            else:
                ik_inst = world.footik() if enable else None
                model.set_custom_ik_solver(ik_inst, 0)
                if ik_inst:
                    ik_inst.set_collision_group(FOOT_IK_GROUP)
                    ik_inst.set_collision_mask(FOOT_IK_MASK)
            return

    def set_gun_vector(self, model, hand_ik_enable, *args):
        import math3d
        import world
        human_model = self.ev_g_model()
        if human_model:
            if model:
                if hand_ik_enable:
                    hand_socket = 'hand'
                    weapon_type = self.ev_g_weapon_type()
                    ik_role_sockets = weapon_action_config.weapon_type_2_action.get(weapon_type, {}).get('ik_role_sockets', None)
                    role_id = self.ev_g_role_id()
                    hand_socket = ik_role_sockets.get(role_id, hand_socket)
                    socket_matrix = model.get_socket_matrix(hand_socket, world.SPACE_TYPE_LOCAL)
                    if not socket_matrix:
                        human_model.set_handik_gun_vector(math3d.vector(0, 0, 0))
                        return
                    rotation = socket_matrix.rotation
                    rotation.inverse()
                    translation = socket_matrix.translation * rotation
                    human_model.set_handik_gun_vector(translation)
            else:
                human_model.set_handik_gun_vector(math3d.vector(0, 0, 0))
        return