# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/effect_utils.py
from __future__ import absolute_import
import six
from six.moves import range
from common.framework import Functor
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
import game3d
import render
import world
_HASH_u_fade_time = game3d.calc_string_hash('u_fade_time')
_HASH_u_decal_grid_size = game3d.calc_string_hash('u_decal_grid_size')
_HASH_u_use_local_uv = game3d.calc_string_hash('u_use_local_uv')
_HASH_DecalTexDiffuse = game3d.calc_string_hash('Tex2')

def get_decal_tot_count(world_pos, sfx_dict, radius_min, check_radius):
    intra_cnt = 0
    extra_cnt = 0
    for sfx_world_pos in six.itervalues(sfx_dict):
        dist = (sfx_world_pos - world_pos).length
        if dist < radius_min:
            intra_cnt += 1
        if dist < check_radius:
            extra_cnt += 1

    return (
     intra_cnt, extra_cnt)


def set_decal_fadeout(sfx, sub_idx, ttl):
    if not sfx.valid:
        return
    sfx.set_sub_decal_ttl(sub_idx, ttl)


def init_decal_attr(sfx, sfx_id, sub_idx, ex_data, decal_tex_size, decal_fadeout_time, use_local_uv=False, intra_tex_path=None, decal_life_time=0, sfx_decal_ttl_timers=None):
    if not (sfx and sfx.valid):
        return
    else:
        material = sfx.get_sub_decal_material(sub_idx)
        if not material:
            return
        material.set_var(_HASH_u_fade_time, 'u_fade_time', decal_fadeout_time)
        sfx.set_sub_decal_ttl(sub_idx, 604800.0)
        if decal_life_time > 0:
            fade_start_time = max(0.0, decal_life_time - decal_fadeout_time * 1000.0)
            ttl = (render.get_frametime() + decal_life_time) / 1000.0
            fadeout_functor = Functor(set_decal_fadeout, sfx, sub_idx, ttl)
            timer_id = game3d.delay_exec(fade_start_time, fadeout_functor)
            if sfx_decal_ttl_timers is not None:
                sfx_decal_ttl_timers.setdefault(sfx_id, {})
                if sub_idx in sfx_decal_ttl_timers:
                    old_timer_id_group = sfx_decal_ttl_timers[sub_idx]
                    if old_timer_id_group:
                        for old_timer_id in old_timer_id_group:
                            if old_timer_id:
                                game3d.cancel_delay_exec(old_timer_id)

                sfx_decal_ttl_timers[sfx_id][sub_idx] = timer_id
        if decal_tex_size[0] <= 0:
            return
        material.set_var(_HASH_u_decal_grid_size, 'u_decal_grid_size', (float(decal_tex_size[0] * NEOX_UNIT_SCALE), float(decal_tex_size[1] * NEOX_UNIT_SCALE)))
        if use_local_uv:
            material.set_var(_HASH_u_use_local_uv, 'u_use_local_uv', 1.0)
        else:
            material.set_var(_HASH_u_use_local_uv, 'u_use_local_uv', -1.0)
        if intra_tex_path:
            material.set_texture(_HASH_DecalTexDiffuse, 'Tex2', intra_tex_path)
        return


HUE_SHIFT_SUPPED_SFX_TYPES = {
 world.FX_TYPE_SPRITE,
 world.FX_TYPE_POLYTUBE,
 world.FX_TYPE_POLYTUBEEX,
 world.FX_TYPE_LEADING,
 world.FX_TYPE_LEADINGEX,
 world.FX_TYPE_PARTICLEPOLY,
 world.FX_TYPE_PARTILCEPOLYTUBE,
 world.FX_TYPE_PARTICLEMODEL,
 world.FX_TYPE_MODEL,
 world.FX_TYPE_PARTILCERES}
ENEMY_HUE = 0.0
DISABLE_HUE = 1.0
_HASH_u_hue_shift_STR = 'u_hue_shift'
_HASH_u_hue_shift = game3d.calc_string_hash(_HASH_u_hue_shift_STR)

def handle_sfx_differentiation_process(sfx, ex_data):
    hue_value = ENEMY_HUE if ex_data.get('need_diff_process') else DISABLE_HUE
    if global_data.feature_mgr.is_support_sfx_set_var_float():
        cnt = sfx.get_subfx_count()
        for i in range(cnt):
            fx_type = sfx.get_sub_type(i)
            if fx_type not in HUE_SHIFT_SUPPED_SFX_TYPES:
                continue
            sfx.sub_set_var(i, _HASH_u_hue_shift, _HASH_u_hue_shift_STR, hue_value)


NEED_IGNORE_EFFECT_BEHIND_CAMERA_MAP = {}

def check_need_ignore_effect_behind_camera(weapon_id, pos):
    if not global_data.enable_ignore_effect_behind_camera:
        return False
    if weapon_id not in NEED_IGNORE_EFFECT_BEHIND_CAMERA_MAP:
        NEED_IGNORE_EFFECT_BEHIND_CAMERA_MAP[weapon_id] = bool(confmgr.get('firearm_res_config', str(weapon_id), 'iIgnoreHitSfxBehindCamera'))
    if not NEED_IGNORE_EFFECT_BEHIND_CAMERA_MAP[weapon_id]:
        return False
    cam = world.get_active_scene().active_camera
    cam_forward = cam.rotation_matrix.forward
    hit_sfx_dir = pos - cam.position
    if hit_sfx_dir.is_zero:
        return False
    hit_sfx_dir.normalize()
    return cam_forward.dot(hit_sfx_dir) <= 0