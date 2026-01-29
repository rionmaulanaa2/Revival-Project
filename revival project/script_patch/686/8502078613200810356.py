# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/pc_platform_utils.py
from __future__ import absolute_import
from six.moves import range
import game3d
import world
import render
from common.cfg import confmgr

def _T(strname):
    return (
     game3d.calc_string_hash(strname), strname)


_HASH_u_is_mecha, STR_u_is_mecha = _T('u_is_mecha')
_HASH_outline_alpha, STR_outline_alpha = _T('outline_alpha')
_HASH_u_color, STR_u_color = _T('u_color')
IS_PC_PLATFORM = game3d.get_platform() == game3d.PLATFORM_WIN32
FPS_MODE = [
 30, 60, 144, 90, 45]

def is_pc_hight_quality():
    return IS_PC_PLATFORM and global_data.is_pc_mode or global_data.is_android_pc or global_data.is_in_mumu


def is_pc_hight_quality_simple():
    return IS_PC_PLATFORM or global_data.is_android_pc or global_data.is_in_mumu


def is_pc_control():
    return IS_PC_PLATFORM and global_data.is_pc_mode or global_data.is_android_pc or global_data.is_mumu_pc_control


need_add_xray_skin_id = ('201002542', '201002543', '201002544', '201002545', '201002546',
                         '201002547', '201001950')
TO_XRAY_MAP = {'shader\\g93shader\\nuoma_tail.fx::TShader': 'shader\\g93shader\\nuoma_tail_xray.fx::TShader',
   'shader\\vbr_toon_nx2_mobile.fx::TShader': 'shader\\vbr_toon_nx2_xray.fx::TShader',
   'shader\\lut_promare_toon_nx2_mobile.fx::TShader': 'shader\\promare_xray.fx::TShader',
   'shader\\vbr_toon_mecha_nx2_mobile.fx::TShader': 'shader\\vbr_toon_mecha_nx2_xray.fx::TShader',
   'shader\\vbr_toon_mecha_nx2_mobile_simple.fx::TShader': 'shader\\vbr_toon_mecha_nx2_xray_simple.fx::TShader',
   'shader\\vbr_cyber_ydj.fx::TShader': 'shader\\vbr_cyber_ydj_xray.fx::TShader',
   'shader\\vbr_pinganjing.fx::TShader': 'shader\\vbr_pinganjing_xray.fx::TShader'
   }
XRAY_RECOVER_MAP = {'shader\\g93shader\\nuoma_tail_xray.fx::TShader': 'shader\\g93shader\\nuoma_tail.fx::TShader',
   'shader\\vbr_toon_nx2_xray.fx::TShader': 'shader\\vbr_toon_nx2_mobile.fx::TShader',
   'shader\\promare_xray.fx::TShader': 'shader\\lut_promare_toon_nx2_mobile.fx::TShader',
   'shader\\vbr_toon_mecha_nx2_xray.fx::TShader': 'shader\\vbr_toon_mecha_nx2_mobile.fx::TShader',
   'shader\\vbr_toon_mecha_nx2_xray_simple.fx::TShader': 'shader\\vbr_toon_mecha_nx2_mobile_simple.fx::TShader',
   'shader\\vbr_cyber_ydj_xray.fx::TShader': 'shader\\vbr_cyber_ydj.fx::TShader',
   'shader\\vbr_pinganjing_xray.fx::TShader': 'shader\\vbr_pinganjing.fx::TShader'
   }
TO_OUTLINE_MAP = {'shader\\vbr_toon_nx2_mobile.fx::TShader': ('shader\\vbr_toon_nx2_outline.fx::TShader', 0.0),
   'shader\\lut_promare_toon_nx2_mobile.fx::TShader': ('shader\\promare_outline.fx::TShader', 0.0),
   'shader\\vbr_toon_mecha_nx2_mobile.fx::TShader': ('shader\\vbr_toon_mecha_nx2_outline.fx::TShader', 1.0),
   'shader\\vbr_toon_mecha_nx2_mobile_simple.fx::TShader': ('shader\\vbr_toon_mecha_nx2_outline_simple.fx::TShader', 1.0)
   }
OUTLINE_RECOVER_MAP = {'shader\\vbr_toon_nx2_outline.fx::TShader': 'shader\\vbr_toon_nx2_mobile.fx::TShader',
   'shader\\promare_outline.fx::TShader': 'shader\\lut_promare_toon_nx2_mobile.fx::TShader',
   'shader\\vbr_toon_mecha_nx2_outline.fx::TShader': 'shader\\vbr_toon_mecha_nx2_mobile.fx::TShader',
   'shader\\vbr_toon_mecha_nx2_outline_simple.fx::TShader': 'shader\\vbr_toon_mecha_nx2_mobile_simple.fx::TShader'
   }

def set_multi_pass_xray(model, u_color):
    sub_count = model.get_submesh_count()
    for index in range(sub_count):
        sub_material = model.get_sub_material(index)
        sub_material_name = sub_material.get_technique_name()
        new_shader = TO_XRAY_MAP.get(sub_material_name)
        if new_shader:
            sub_material.set_technique(1, new_shader)
            sub_material.set_var(_HASH_u_color, STR_u_color, u_color)


def disable_multi_pass_xray(model):
    sub_count = model.get_submesh_count()
    for index in range(sub_count):
        sub_material = model.get_sub_material(index)
        sub_material_name = sub_material.get_technique_name()
        new_shader = XRAY_RECOVER_MAP.get(sub_material_name)
        if new_shader:
            sub_material.set_technique(1, new_shader)


def set_multi_pass_outline(model, is_lobby_display=False):
    sub_count = model.get_submesh_count()
    for index in range(sub_count):
        sub_material = model.get_sub_material(index)
        sub_material_name = sub_material.get_technique_name()
        new_shader_info = TO_OUTLINE_MAP.get(sub_material_name)
        if new_shader_info:
            if is_lobby_display and sub_material.transparent_mode <= 1 or not is_lobby_display and sub_material.alpha >= 1.0:
                sub_material.set_technique(1, new_shader_info[0])
                sub_material.set_var(_HASH_u_is_mecha, STR_u_is_mecha, new_shader_info[1])


def disable_multi_pass_outline(model):
    sub_count = model.get_submesh_count()
    for index in range(sub_count):
        sub_material = model.get_sub_material(index)
        sub_material_name = sub_material.get_technique_name()
        new_shader = OUTLINE_RECOVER_MAP.get(sub_material_name)
        if new_shader:
            sub_material.set_technique(1, new_shader)


def set_socket_model_xray_technique(model, dressed_clothing_id, u_color):
    if str(dressed_clothing_id) in need_add_xray_skin_id:
        config_socket_name_list = confmgr.get('role_info', 'RoleSkin', 'Content', str(dressed_clothing_id), 'sockets_in_socket_obj')
        if config_socket_name_list:
            for socket_name in config_socket_name_list:
                socket_model = model.get_socket_obj(socket_name, 0)
                if socket_model:
                    for index in range(socket_model.get_submesh_count()):
                        sub_material = socket_model.get_sub_material(index)
                        sub_tech_name = sub_material.get_technique_name()
                        replace_shader = TO_XRAY_MAP.get(sub_tech_name, None)
                        if replace_shader:
                            sub_material.set_technique(1, replace_shader)
                            sub_material.set_var(_HASH_u_color, STR_u_color, u_color)

    return


def recover_socket_model_xray_technique(model, dressed_clothing_id):
    if str(dressed_clothing_id) in need_add_xray_skin_id:
        config_socket_name_list = confmgr.get('role_info', 'RoleSkin', 'Content', str(dressed_clothing_id), 'sockets_in_socket_obj')
        if config_socket_name_list:
            for socket_name in config_socket_name_list:
                socket_model = model.get_socket_obj(socket_name, 0)
                if socket_model:
                    socket_model.all_materials.reset()


def get_shader_name_from_tech_name(tech_name):
    s = tech_name.index('\\') + 1
    e = tech_name.index('.')
    return tech_name[s:e]


def set_vbr_toon_technique_display(model, shader_name):
    if global_data.is_ue_model:
        map_name = ue_toon_map.get(shader_name)
        if map_name:
            shader_name = map_name
    model.all_materials.set_technique(1, 'shader/%s.nfx::TShader' % shader_name)
    model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 0)


def set_model_write_alpha(model, enable_write_alpha, alpha):
    model.all_materials.enable_write_alpha = enable_write_alpha
    sub_count = model.get_submesh_count()
    for index in range(sub_count):
        sub_material = model.get_sub_material(index)
        if sub_material.transparent_mode <= 1:
            sub_material.set_var(_HASH_outline_alpha, STR_outline_alpha, alpha)


def set_alpha_submesh_rendergroup(model):
    sub_count = model.get_submesh_count()
    for index in range(sub_count):
        sub_material = model.get_sub_material(index)
        if sub_material.transparent_mode > 1:
            model.set_submesh_rendergroup_and_priority(index, world.RENDER_GROUP_TRANSPARENT)


def set_model_alpha_only(model, alpha):
    model.all_materials.set_var(_HASH_outline_alpha, STR_outline_alpha, alpha)


vbr_toon_alpha_map = {}

def set_display_model_alpha(model, is_render_target_model):
    if not model or not model.valid:
        return
    sub_count = model.get_submesh_count()
    if not is_render_target_model:
        for index in range(sub_count):
            sub_material = model.get_sub_material(index)
            if sub_material.transparent_mode <= 1:
                sub_material.set_var(_HASH_outline_alpha, STR_outline_alpha, 1.0)
                sub_material.enable_write_alpha = (True,)
            else:
                sub_tech_name = get_shader_name_from_tech_name(sub_material.get_technique_name())
                shader_name = vbr_toon_alpha_map.get(sub_tech_name)
                if shader_name:
                    sub_material.set_technique(1, 'shader/%s.nfx::TShader' % shader_name)
                    sub_material.enable_write_alpha = (True,)

        socket_models = model.get_all_objects_on_sockets()
        for socket_model in socket_models:
            if isinstance(socket_model, world.model):
                socket_model_sub_count = socket_model.get_submesh_count()
                for index in range(socket_model_sub_count):
                    sub_material = socket_model.get_sub_material(index)
                    if sub_material.transparent_mode <= 1:
                        sub_material.set_var(_HASH_outline_alpha, STR_outline_alpha, 1.0)
                        sub_material.enable_write_alpha = (True,)
                    else:
                        sub_tech_name = get_shader_name_from_tech_name(sub_material.get_technique_name())
                        shader_name = vbr_toon_alpha_map.get(sub_tech_name)
                        if shader_name:
                            sub_material.set_technique(1, 'shader/%s.nfx::TShader' % shader_name)
                            sub_material.enable_write_alpha = (True,)

    else:
        for index in range(sub_count):
            sub_material = model.get_sub_material(index)
            if sub_material.transparent_mode <= 1:
                sub_material.set_var(_HASH_outline_alpha, STR_outline_alpha, 1.0)
            sub_material.enable_write_alpha = (
             True,)

    socket_models = model.get_all_objects_on_sockets()
    for socket_model in socket_models:
        if isinstance(socket_model, world.model):
            socket_model_sub_count = socket_model.get_submesh_count()
            for index in range(socket_model_sub_count):
                sub_material = socket_model.get_sub_material(index)
                if sub_material.transparent_mode <= 1:
                    sub_material.set_var(_HASH_outline_alpha, STR_outline_alpha, 1.0)
                sub_material.enable_write_alpha = (
                 True,)


lod_level_map = {'l': 'l',
   'l1': 'l1',
   'l2': 'l1',
   'l3': 'l2',
   'l4': 'l4'
   }
lod_level_map_enable = (
 False, False, True, True, True)

def get_effect_lod_level(old_lod_level):
    quality_level = global_data.game_mgr.gds.get_actual_quality()
    enable = lod_level_map_enable[quality_level]
    if is_pc_hight_quality() and enable:
        return lod_level_map.get(old_lod_level, old_lod_level)
    return old_lod_level


lod_dist_scale = (
 (1.0, 1.3, 1.3, 1.3),
 (1.3, 1.5, 1.5, 1.5),
 (1.5, 1.7, 1.7, 1.7),
 (1.7, 2.0, 2.0, 2.0),
 (1.7, 2.0, 2.0, 2.0))

def get_lod_dist_scale():
    if is_pc_hight_quality():
        quality_level = global_data.game_mgr.gds.get_actual_quality()
        return lod_dist_scale[quality_level]
    return (1.0, 1.0, 1.0, 1.0)


terrain_lod_dist_scale = (
 (1.0, 1.0, 2.0),
 (1.0, 1.0, 3.0),
 (1.0, 1.0, 4.0),
 (1.5, 1.0, 4.0),
 (1.5, 1.0, 4.0))

def get_terrain_lod_dist_scale():
    return 1.0


def get_terrain_lod_dist_scale_list():
    if is_pc_hight_quality():
        quality_level = global_data.game_mgr.gds.get_actual_quality()
        return terrain_lod_dist_scale[quality_level]
    return (1.0, 1.0, 1.0)


def is_redirect_scale_enable():
    if global_data.is_pc_mode and game3d.get_engine_svn_version() > 1277960 and global_data.is_ue_model:
        return True
    return False