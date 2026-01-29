# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMaterialStatus.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from ..UnitCom import UnitCom
import game3d
import time
import world
from common.utils import pc_platform_utils
from logic.gutils import tech_pass_utils
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from common.cfg import confmgr
from logic.gutils.soc_utils import set_model_attach_soc
_HASH_outline_alpha = game3d.calc_string_hash('outline_alpha')
_HASH_u_color = game3d.calc_string_hash('u_color')
RENDER_GROUP_SEE_THROUGH = 3
RENDER_GROUP_DYOCC_OBJ = 28
TEAM_OUTLINE_ENABLE_DIS = 260.0 * 260.0

class ComMaterialStatus(UnitCom):
    BIND_EVENT = {'E_ADD_MATERIAL_STATUS': 'add_status',
       'E_DEL_MATERIAL_STATUS': 'del_status',
       'E_ADD_BIND_MODEL': 'add_bind_model',
       'E_DEL_BIND_MODEL': 'del_bind_model',
       'E_MODEL_LOADED': 'on_model_loaded',
       'E_SWITCH_MODEL': 'on_switch_model',
       'E_ENABLE_XRAY_ONLY': 'on_enable_xray_only',
       'E_MECHA_LOD_LOADED_FIRST': 'on_mecha_lod_loaded_first',
       'E_HUMAN_LOD_LOADED': 'on_human_lod_loaded',
       'E_MECHA_LOD_LOADED': 'on_mecha_lod_loaded',
       'E_UPDATE_MATERIAL_STATUS_PARAM': 'update_status_param',
       'E_UPDATE_CURRENT_MATERIAL_STATUS': 'update_top_status'
       }
    OUTLINE_ONLY = 0
    XRAY_ONLY = 1
    SEE_THROUGH_OUTLINE = 2
    XRAY_AND_OUTLINE = 3

    def __init__(self):
        super(ComMaterialStatus, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComMaterialStatus, self).init_from_dict(unit_obj, bdict)
        self._model = None
        self._status_stack = []
        self._key_to_index = {}
        self._last_update_time = time.time()
        self._enable_xray_only = False
        self._xray_only_param = None
        self._bind_model_config = {}
        self._up_error_msg = False
        global_data.emgr.cam_lplayer_in_fog_changed += self.on_cam_in_fog_changed
        return

    def destroy(self):
        super(ComMaterialStatus, self).destroy()
        global_data.emgr.cam_lplayer_in_fog_changed -= self.on_cam_in_fog_changed

    def on_cam_in_fog_changed(self, *args):
        self.update_top_status()

    def tick(self, delta):
        count = len(self._status_stack)
        if count <= 0:
            return
        else:
            del_info = None
            is_top_deled = False
            now = time.time()
            for index in range(len(self._status_stack)):
                stack_info = self._status_stack[index]
                end_time = stack_info.get('end_time', 0)
                if end_time > 0 and end_time < now:
                    key = stack_info['unique_key']
                    top_stack = self.get_top_status_stack()
                    del_info = self._del_status(key)
                    is_top_deled = del_info and del_info == top_stack
                    break

            count = len(self._status_stack)
            if del_info and is_top_deled:
                self.call_func('on_disable', del_info['param'])
                if count > 0:
                    top_stack = self.get_top_status_stack()
                    self.call_func('on_enable', top_stack['param'])
                self._last_update_time = now
            else:
                top_stack = self.get_top_status_stack()
                update_interval = top_stack['param'].get('update_interval', 5.0)
                if now - self._last_update_time > update_interval:
                    self._last_update_time = now
                    self.call_func('on_update', top_stack['param'])
            return

    def refresh_updata(self):
        count = len(self._status_stack)
        if count <= 0:
            return
        top_stack = self.get_top_status_stack()
        self._last_update_time = time.time()
        self.call_func('on_update', top_stack['param'])

    def call_func(self, func_prefix, param):
        status_type = param.get('status_type', '')
        func_name = '{}_{}'.format(func_prefix, status_type.lower())
        func_callback = param.get(func_prefix, None)
        if not func_callback and hasattr(self, func_name):
            func_callback = getattr(self, func_name)
        if func_callback:
            func_callback(param)
        return

    def get_status(self, key):
        index = self._key_to_index.get(key, -1)
        if index < 0:
            return None
        else:
            return self._status_stack[index]

    def get_top_status_stack(self):
        top_stack = None
        max_prority = -999
        for i, status_info in enumerate(self._status_stack):
            if status_info['prority'] >= max_prority:
                top_stack = status_info
                max_prority = status_info['prority']

        return top_stack

    def update_status_param(self, key, param=None, partial=True):
        if param is None:
            param = {}
        stack_info = self.get_status(key)
        if stack_info is not None:
            if partial:
                if 'param' in stack_info:
                    stack_info['param'].update(param)
            else:
                stack_info['param'] = param
        return

    def update_top_status(self):
        top_stack = self.get_top_status_stack()
        if top_stack:
            self.call_func('on_update', top_stack['param'])

    def add_bind_model(self, model, param):
        if not model or not model.valid:
            return
        self._bind_model_config[model] = param
        if self._enable_xray_only:
            self.on_enable_one_bind_model_xray_only(model, param)

    def del_bind_model(self, model):
        if model in self._bind_model_config:
            del self._bind_model_config[model]

    def add_status(self, key, param=None, prority=1, update_when_exist=False):
        if param == None:
            param = {}
        end_time = 0
        start_time = time.time()
        last_time = param.get('last_time', 0)
        if last_time > 0:
            end_time = start_time + last_time
        stack_info = self.get_status(key)
        if stack_info:
            stack_info['start_time'] = start_time
            stack_info['end_time'] = end_time
            if update_when_exist:
                self.call_func('on_update', stack_info['param'])
        else:
            old_top_stack = None
            if self._status_stack:
                old_top_stack = self.get_top_status_stack()
            stack_info = {'start_time': start_time,'end_time': end_time,'unique_key': key,'param': param,'prority': prority}
            self._status_stack.append(stack_info)
            self._key_to_index[key] = len(self._status_stack) - 1
            new_top_stack = self.get_top_status_stack()
            if old_top_stack != new_top_stack:
                if old_top_stack:
                    self.call_func('on_disable', old_top_stack['param'])
                self.call_func('on_enable', param)
        self.need_update = True
        return

    def del_status(self, key):
        top_stack = self.get_top_status_stack()
        del_info = self._del_status(key)
        if del_info:
            is_top_deled = del_info == top_stack
            if is_top_deled:
                self.call_func('on_disable', del_info['param'])
                top_stack = self.get_top_status_stack()
                if top_stack:
                    self.call_func('on_enable', top_stack['param'])

    def _del_status(self, key):
        index = self._key_to_index.get(key, -1)
        if index < 0:
            return None
        else:
            del_info = self._status_stack.pop(index)
            del self._key_to_index[key]
            for k, i in six.iteritems(self._key_to_index):
                if i > index:
                    self._key_to_index[k] -= 1

            if len(self._status_stack) <= 0:
                self.need_update = False
            return del_info

    def _do_enable_top_status(self):
        top_stack = self.get_top_status_stack()
        if top_stack:
            self.call_func('on_enable', top_stack['param'])

    def _do_disable_top_status(self):
        top_stack = self.get_top_status_stack()
        if top_stack:
            self.call_func('on_disable', top_stack['param'])

    def on_model_loaded(self, model):
        if self._model and self._model.valid:
            self._do_disable_top_status()
        self._model = model
        self._do_enable_top_status()

    def on_switch_model(self, model):
        if self._model and self._model.valid:
            self._do_disable_top_status()
        self._model = model
        self._do_enable_top_status()

    def on_mecha_lod_loaded_first(self):
        if self._enable_xray_only and self._xray_only_param:
            self.do_xray_only(self._xray_only_param)

    def on_human_lod_loaded(self, owner_model):
        self._do_enable_top_status()
        self.refresh_updata()

    def on_mecha_lod_loaded(self, owner_model, *args, **kwargs):
        self._do_enable_top_status()
        self.refresh_updata()

    def active_bind_socket_objs(self, func_name, *args):
        func = getattr(self, func_name)
        if self.ev_g_is_human():
            if self.sd.ref_role_skin_sub_model:
                for socket_model in self.sd.ref_role_skin_sub_model:
                    if socket_model:
                        func(socket_model, *args)

            else:
                fashion_dict = self.ev_g_fashion()
                dressed_clothing_id = fashion_dict.get(FASHION_POS_SUIT)
                socket_name_list = confmgr.get('role_info', 'RoleSkin', 'Content', str(dressed_clothing_id), 'sockets_in_socket_obj')
                if socket_name_list:
                    for socket_name in socket_name_list:
                        socket_model = self._model.get_socket_obj(socket_name, 0)
                        if not socket_model and self._model.has_socket(socket_name):
                            model_list = self._model.get_socket_objects(socket_name)
                            if model_list:
                                socket_model = model_list[0]
                        if socket_model:
                            if type(socket_model) == world.sfx:
                                continue
                            func(socket_model, *args)

        elif self.sd.ref_is_mecha and self.sd.ref_socket_res_agent:
            for model_res in self.sd.ref_socket_res_agent.model_res_list:
                func(model_res, *args)

        elif self.sd.ref_is_pve_monster:
            if self.sd.ref_sub_model_map:
                for sub_model_list in six.itervalues(self.sd.ref_sub_model_map):
                    for socket_model in sub_model_list:
                        if socket_model:
                            func(socket_model, *args)

    def _refresh_render_priority(self, render_group=None):
        if self.sd.ref_is_mecha and self.sd.ref_socket_res_agent:
            self.sd.ref_socket_res_agent.refresh_render_priority(render_group)

    def on_enable_outline_only(self, param):
        if not self._model or not self._model.valid:
            return
        self.set_outline(self._model, param)
        self.active_bind_socket_objs('set_outline', param)
        self._refresh_render_priority(RENDER_GROUP_DYOCC_OBJ)

    def set_outline(self, model, param):
        pc_platform_utils.set_model_write_alpha(model, True, param.get('outline_alpha', 0.3333))
        model.set_rendergroup_and_priority(RENDER_GROUP_DYOCC_OBJ)

    def on_disable_outline_only(self, param):
        if not self._model or not self._model.valid:
            return
        self.cancel_outline(self._model, param)
        self.active_bind_socket_objs('cancel_outline', param)
        self._refresh_render_priority(RENDER_GROUP_DYOCC_OBJ)

    def cancel_outline(self, model, param):
        pc_platform_utils.set_model_write_alpha(model, False, 1.0)

    def on_update_outline_only(self, param):
        if not self._model or not self._model.valid:
            return
        outline_alpha = param.get('outline_alpha', 0.3333)
        if param.get('team_outline_tick', 0):
            if global_data.cam_lctarget:
                player_pos = global_data.cam_lctarget.ev_g_model_position()
                pos = self.ev_g_model_position()
                if player_pos and pos:
                    if (player_pos - pos).length_sqr > TEAM_OUTLINE_ENABLE_DIS:
                        outline_alpha = 1.0
        if global_data.cam_lplayer and outline_alpha == 0.3333 and (global_data.cam_lplayer.sd.ref_is_blinded or self.sd.ref_is_covered):
            outline_alpha = 1.0
        self.set_update_outline(self._model, outline_alpha)
        self.active_bind_socket_objs('set_update_outline', outline_alpha)

    def set_update_outline(self, model, outline_alpha):
        pc_platform_utils.set_model_alpha_only(model, outline_alpha)

    def on_enable_xray_only(self, param):
        if not self._model or not self._model.valid:
            return
        self._enable_xray_only = True
        self._xray_only_param = param
        self.do_xray_only(param)

    def do_xray_only(self, param):
        self.set_xray(self._model, param)
        self.active_bind_socket_objs('set_xray', param)
        self.on_enable_bind_model_xray_only()
        self._refresh_render_priority(world.RENDER_GROUP_XRAY)

    def set_xray(self, model, param):
        u_color = param.get('u_color', (1.0, 0.0, 0.0, 1.0))
        if not self.sd.ref_is_mecha:
            pc_platform_utils.set_socket_model_xray_technique(model, self.sd.ref_dressed_clothing_id, u_color)
        pc_platform_utils.set_multi_pass_xray(model, u_color)
        model.set_rendergroup_and_priority(world.RENDER_GROUP_XRAY)
        model.set_ignore_dyn_culling(True)
        set_model_attach_soc(model, False)

    def on_enable_bind_model_xray_only(self):
        for model, param in six_ex.items(self._bind_model_config):
            if not model or not model.valid:
                continue
            self.on_enable_one_bind_model_xray_only(model, param)

    def on_enable_one_bind_model_xray_only(self, model, param):
        u_color = param.get('u_color', (1.0, 0.0, 0.0, 1.0))
        pc_platform_utils.set_multi_pass_xray(model, u_color)
        model.set_rendergroup_and_priority(world.RENDER_GROUP_XRAY, 1)
        model.set_ignore_dyn_culling(True)
        set_model_attach_soc(model, False)

    def on_disable_xray_only(self, param):
        if not self._model or not self._model.valid:
            return
        else:
            self._enable_xray_only = False
            self._xray_only_param = None
            self.cancel_xray(self._model, param)
            self.active_bind_socket_objs('cancel_xray', param)
            self.on_disable_bind_model_xray_only()
            self._refresh_render_priority(RENDER_GROUP_DYOCC_OBJ)
            return

    def cancel_xray(self, model, param):
        if not self.sd.ref_is_mecha:
            pc_platform_utils.recover_socket_model_xray_technique(model, self.sd.ref_dressed_clothing_id)
        pc_platform_utils.disable_multi_pass_xray(model)
        model.set_rendergroup_and_priority(RENDER_GROUP_DYOCC_OBJ)
        model.enable_dynamic_culling(True)

    def on_disable_bind_model_xray_only(self):
        for model, param in six_ex.items(self._bind_model_config):
            if not model or not model.valid:
                continue
            pc_platform_utils.disable_multi_pass_xray(model)
            model.set_rendergroup_and_priority(RENDER_GROUP_DYOCC_OBJ)
            model.enable_dynamic_culling(True)

    def on_update_xray_only(self, param):
        set_xray_parm = tech_pass_utils.set_xray_param
        if self._model and self._model.valid:
            set_xray_parm(self._model, _HASH_u_color, 'u_color', param.get('u_color', (1.0,
                                                                                       0.0,
                                                                                       0.0,
                                                                                       1.0)))
        for model, param in six.iteritems(self._bind_model_config):
            if not model or not model.valid:
                continue
            set_xray_parm(model, _HASH_u_color, 'u_color', param.get('u_color', (1.0,
                                                                                 0.0,
                                                                                 0.0,
                                                                                 1.0)))

    def on_enable_see_through_outline(self, param):
        if not self._model or not self._model.valid:
            return
        flag = True
        self.scene.enable_hero_outline(flag, self.unit_obj.id)
        self.set_enable_see_through_outline(self._model, flag, param)
        self.active_bind_socket_objs('set_enable_see_through_outline', flag, param)
        self._refresh_render_priority(RENDER_GROUP_SEE_THROUGH)

    def set_enable_see_through_outline(self, model, flag, param):
        OUTLINE_ALPHA = 0.3333
        pc_platform_utils.set_model_write_alpha(model, flag, param.get('outline_alpha', OUTLINE_ALPHA))
        model.set_rendergroup_and_priority(RENDER_GROUP_SEE_THROUGH)
        model.set_ignore_dyn_culling(flag)
        set_model_attach_soc(model, not flag)

    def on_disable_see_through_outline(self, param):
        if not self._model or not self._model.valid:
            return
        flag = False
        self.scene.enable_hero_outline(flag, self.unit_obj.id)
        self.set_disable_see_through_outline(self._model, flag, param)
        self.active_bind_socket_objs('set_disable_see_through_outline', flag, param)
        self._refresh_render_priority(RENDER_GROUP_DYOCC_OBJ)

    def set_disable_see_through_outline(self, model, flag, param):
        OUTLINE_ALPHA = 2.0
        pc_platform_utils.set_model_write_alpha(model, flag, param.get('outline_alpha', OUTLINE_ALPHA))
        model.set_rendergroup_and_priority(RENDER_GROUP_DYOCC_OBJ)
        model.set_ignore_dyn_culling(flag)
        set_model_attach_soc(model, not flag)

    def on_update_see_through_outline(self, param):
        if not self._model or not self._model.valid:
            return
        self.set_update_see_through_outline(self._model)
        self.active_bind_socket_objs('set_update_see_through_outline', param)

    def set_update_see_through_outline(self, model, param):
        OUTLINE_ALPHA = 0.3333
        pc_platform_utils.set_model_alpha_only(model, param.get('outline_alpha', OUTLINE_ALPHA))

    def on_enable_xray_and_outline(self, param):
        if not self._model or not self._model.valid:
            return
        self.set_xray_and_outline(self._model, param)
        self.active_bind_socket_objs('set_xray_and_outline', param)
        self._refresh_render_priority(RENDER_GROUP_DYOCC_OBJ)
        self.scene.enable_detector_outline(True, self.unit_obj.id)

    def set_xray_and_outline(self, model, param):
        u_color = param.get('u_color', (1.0, 0.0, 0.0, 1.0))
        if not self.sd.ref_is_mecha:
            pc_platform_utils.set_socket_model_xray_technique(model, self.sd.ref_dressed_clothing_id, param.get('u_color', (1.0,
                                                                                                                            0.0,
                                                                                                                            0.0,
                                                                                                                            1.0)))
        pc_platform_utils.set_multi_pass_xray(model, u_color)
        model.set_rendergroup_and_priority(world.RENDER_GROUP_XRAY)
        model.set_ignore_dyn_culling(True)
        set_model_attach_soc(model, False)
        enable = True
        pc_platform_utils.set_model_write_alpha(model, enable, param.get('outline_alpha', 0.3333))
        model.set_rendergroup_and_priority(RENDER_GROUP_DYOCC_OBJ)

    def on_disable_xray_and_outline(self, param):
        if not self._model or not self._model.valid:
            return
        self.cancel_xray_and_outline(self._model, param)
        self.active_bind_socket_objs('cancel_xray_and_outline', param)
        self._refresh_render_priority(RENDER_GROUP_DYOCC_OBJ)
        self.scene.enable_detector_outline(False, self.unit_obj.id)

    def cancel_xray_and_outline(self, model, param):
        if not self.sd.ref_is_mecha:
            pc_platform_utils.recover_socket_model_xray_technique(model, self.sd.ref_dressed_clothing_id)
        pc_platform_utils.disable_multi_pass_xray(model)
        model.set_rendergroup_and_priority(RENDER_GROUP_DYOCC_OBJ)
        model.enable_dynamic_culling(True)
        enable = False
        model.all_materials.enable_write_alpha = enable

    def on_update_xray_and_outline(self, param):
        if not self._model or not self._model.valid:
            return
        outline_alpha = param.get('outline_alpha', 0.3333)
        if param.get('team_outline_tick', 0) and global_data.cam_lctarget:
            player_pos = global_data.cam_lctarget.ev_g_model_position()
            pos = self.ev_g_model_position()
            if player_pos and pos:
                if (player_pos - pos).length_sqr > TEAM_OUTLINE_ENABLE_DIS:
                    outline_alpha = 1.0
        self.set_update_xray_and_outline(self._model, outline_alpha)
        self.active_bind_socket_objs('set_update_xray_and_outline', outline_alpha)

    def set_update_xray_and_outline(self, model, outline_alpha):
        sub_count = model.get_submesh_count()
        for index in range(sub_count):
            sub_material = model.get_sub_material(index)
            if sub_material.transparent_mode <= 1:
                sub_material.set_var(_HASH_outline_alpha, 'outline_alpha', outline_alpha)