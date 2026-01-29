# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComHumanTransparentModel.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
from common.utils import pc_platform_utils
import game3d
import render
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from common.cfg import confmgr
import world

class ComHumanTransparentModel(UnitCom):
    BIND_EVENT = {'E_SET_MODEL_OPACITY': 'enter_opacity_mode',
       'E_LEAVE_MODEL_OPACITY': 'leave_opacity_mode',
       'G_IS_MODEL_OPACITY': 'get_is_model_opacity',
       'G_MODEL_OPACITY': 'get_model_opacity',
       'E_DISABLE_TRANSPARENT': 'disable_transparent',
       'E_FORCE_ENTER_MODEL_OPACITY': 'force_enter_opacity_mode',
       'E_FORCE_LEAVE_MODEL_OPACITY': 'force_leave_opacity_mode'
       }

    def __init__(self):
        super(ComHumanTransparentModel, self).__init__()
        self.need_update = False
        self._is_in_opacity = False
        self._opacity = 255
        self._is_enable = True

    def enter_opacity_mode(self, opacity):
        model = self.ev_g_model()
        if model and model.valid:
            if global_data.is_multi_pass_support:
                pc_platform_utils.disable_multi_pass_outline(model)
            if not self.ev_g_is_avatar():
                model.set_rendergroup_and_priority(0, 0)
                model.enable_dynamic_culling(False)
            self._set_socket_model(True, opacity)
        model = self.ev_g_model()
        self._set_model_opacity(model, opacity, False)
        if not self._is_in_opacity:
            self._is_in_opacity = True
            if game3d.get_platform() == game3d.PLATFORM_IOS and global_data.cam_lctarget and self.unit_obj == global_data.cam_lctarget:
                global_data.emgr.camera_lctarget_open_prez.emit(self._is_in_opacity)
        self._opacity = opacity

    def leave_opacity_mode(self):
        if self._is_in_opacity:
            model = self.ev_g_model()
            self._set_model_opaque(model)
            self._is_in_opacity = False
            if game3d.get_platform() == game3d.PLATFORM_IOS and global_data.cam_lctarget and self.unit_obj == global_data.cam_lctarget:
                global_data.emgr.camera_lctarget_open_prez.emit(self._is_in_opacity)
            if model and model.valid:
                if global_data.is_multi_pass_support:
                    pc_platform_utils.set_multi_pass_outline(model)
                if not self.ev_g_is_avatar():
                    model.set_rendergroup_and_priority(28, 0)
                    model.enable_dynamic_culling(True)
                self._set_socket_model(False)
        self._opacity = 255

    def disable_transparent(self, is_disable):
        if is_disable:
            model = self.ev_g_model()
            self._set_model_opaque(model)
            self._set_socket_model(False)
        self._is_enable = not is_disable

    def _set_model_opacity(self, model, opacity, single_model=False):
        if not self._is_enable:
            return
        if model and model.valid:
            if global_data.is_multi_pass_support:
                model.enable_prez_transparent(True, opacity / 255)
            elif global_data.feature_mgr.is_support_ext_tech_fix():
                from logic.gutils.tech_pass_utils import set_prez_transparent
                set_prez_transparent(model, True, int(opacity))

    def _set_model_opaque(self, model):
        if not self._is_enable:
            return
        if model:
            if global_data.is_multi_pass_support:
                model.all_materials.alpha = 255
                model.enable_prez_transparent(False, 255)
            elif global_data.feature_mgr.is_support_ext_tech_fix():
                from logic.gutils.tech_pass_utils import set_prez_transparent
                set_prez_transparent(model, False, 255)

    def _set_socket_model(self, is_opacity, opacity=None):
        socket_name_dict = {}
        gun_socket = self.ev_g_gun_bind_point()
        if gun_socket:
            socket_name_dict['weapon'] = gun_socket
        fashion_dict = self.ev_g_fashion()
        dressed_clothing_id = fashion_dict.get(FASHION_POS_SUIT)
        config_socket_name_list = confmgr.get('role_info', 'RoleSkin', 'Content', str(dressed_clothing_id), 'sockets_in_socket_obj')
        if config_socket_name_list:
            socket_name_dict['body'] = config_socket_name_list
        if self.sd.ref_role_skin_sub_model:
            for sub_model in self.sd.ref_role_skin_sub_model:
                if sub_model and sub_model.valid:
                    self._set_signle_socket_model(sub_model, is_opacity, opacity)

        model = self.ev_g_model()
        for socket_type, socket_name_list in six.iteritems(socket_name_dict):
            for socket_name in socket_name_list:
                if socket_name and model.has_socket(socket_name):
                    model_list = model.get_socket_objects(socket_name)
                    if model_list and len(model_list) > 0:
                        socket_model = model_list[0]
                        if socket_type == 'weapon':
                            self._set_weapon_model(socket_model, is_opacity, opacity)
                            if socket_model.has_socket('danjia'):
                                obj_list = socket_model.get_socket_objects('danjia')
                                if obj_list:
                                    self._set_weapon_model(obj_list[0], is_opacity, opacity)
                        elif type(socket_model) == world.model:
                            self._set_signle_socket_model(socket_model, is_opacity, opacity)

    def _set_signle_socket_model(self, socket_model, is_opacity, opacity=None):
        if is_opacity:
            pc_platform_utils.disable_multi_pass_outline(socket_model)
            self._set_model_opacity(socket_model, opacity, True)
        else:
            pc_platform_utils.set_multi_pass_outline(socket_model)
            self._set_model_opaque(socket_model)

    def _set_weapon_model(self, socket_model, is_opactiy, opacity=None):
        if is_opactiy:
            self._set_model_opacity(socket_model, opacity, True)
        else:
            self._set_model_opaque(socket_model)

    def get_is_model_opacity(self):
        return self._is_in_opacity

    def get_model_opacity(self):
        return self._opacity

    def force_enter_opacity_mode(self, model, opacity):
        if model and model.valid:
            self._set_model_opacity(model, opacity)

    def force_leave_opacity_mode(self, model):
        if model and model.valid:
            self._set_model_opaque(model)

    def destroy(self):
        self.leave_opacity_mode()
        super(ComHumanTransparentModel, self).destroy()