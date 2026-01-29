# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/tech_pass_utils.py
from __future__ import absolute_import
from six.moves import range
import render
import world
import game3d

def _T(strname):
    return (
     game3d.calc_string_hash(strname), strname)


HASH_IS_MECHA, STR_IS_MECHA = _T('u_is_mecha')
HASH_OUTLINE_WIDTH, STR_OUTLINE_WIDTH = _T('outline_width')
RAGDOLL_HIDE_SUBMESH_SUFFIX = '_ragdoll_hide'

def set_xray_param(model, hash_name, name, value):
    if global_data.is_multi_pass_support:
        model.all_materials.set_var(hash_name, name, value)
    else:
        model.set_ext_technique_var(render.EXT_TECH_XRAY, hash_name, name, value)


def set_outline_param(model, hash_name, name, value):
    model.all_materials.set_var(hash_name, name, value)


CHARACTER_OUTLINE = 0.0012
MECHA_OUTLINE = 0.0012

def set_multi_pass_wrapper(model, shader_name, is_lobby_display=False):
    is_mecha = 1.0 if 'mecha' in shader_name else 0.0
    outline_width = MECHA_OUTLINE if is_mecha else CHARACTER_OUTLINE
    if global_data.is_multi_pass_support or 'outline' in shader_name:
        sub_count = model.get_submesh_count()
        for index in range(sub_count):
            sub_material = model.get_sub_material(index)
            sub_material_name = sub_material.get_technique_name()
            if sub_material.transparent_mode <= 1 and 'mecha' in sub_material_name:
                sub_material.set_technique(1, shader_name)
                sub_material.set_var(HASH_IS_MECHA, STR_IS_MECHA, is_mecha)

    elif 'xray' in shader_name:
        model.show_ext_technique(render.EXT_TECH_XRAY, True)
    else:
        sub_count = model.get_submesh_count()
        for index in range(sub_count):
            sub_material = model.get_sub_material(index)
            if sub_material.transparent_mode <= 1:
                sub_material.set_technique(1, shader_name)

        model.show_ext_technique(render.EXT_TECH_XRAY, False)
        model.show_ext_technique(render.EXT_TECH_OUTLINE, False)


def set_prez_transparent(model, is_show, opacity):
    if is_show:
        sub_count = model.get_submesh_count()
        for index in range(sub_count):
            sub_material = model.get_sub_material(index)
            technique_name = sub_material.get_technique_name()
            if 'alpha' not in technique_name:
                sub_material.alpha = opacity / 255.0
                sub_material.transparent_mode = render.TRANSPARENT_MODE_ALPHA_R_Z

        model.show_ext_technique(render.EXT_TECH_PRE_ALPHA_Z, True)
    else:
        sub_count = model.get_submesh_count()
        for index in range(sub_count):
            sub_material = model.get_sub_material(index)
            technique_name = sub_material.get_technique_name()
            if 'alpha' not in technique_name:
                sub_material.alpha = 1.0
                sub_material.transparent_mode = render.TRANSPARENT_MODE_OPAQUE

        model.show_ext_technique(render.EXT_TECH_PRE_ALPHA_Z, False)


def hide_ragdoll_submesh(model):
    if not model:
        return
    sub_count = model.get_submesh_count()
    for index in range(sub_count):
        mesh_name = model.get_submesh_name(index)
        if mesh_name.endswith(RAGDOLL_HIDE_SUBMESH_SUFFIX):
            model.set_submesh_visible(index, False)