# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaShieldCollision.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.common_const.collision_const import GROUP_SHIELD, GROUP_GRENADE
from common.cfg import confmgr
from common.framework import Functor
from common.utils.timer import LOGIC
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from logic.gutils.effect_utils import check_need_ignore_effect_behind_camera
import weakref
import collision
import math3d
import world
import time

class ComMechaShieldCollision(UnitCom):
    BIND_EVENT = {'E_HUMAN_MODEL_LOADED': 'on_human_model_load',
       'E_HIT_SHIELD_SFX': 'on_hit_shield_sfx',
       'E_SET_SHIELD': 'on_shield_change',
       'E_ON_LEAVE_MECHA': 'on_leave_mecha',
       'G_MECHA_SHIELD_ID': '_get_mecha_shield_id',
       'E_DISABLE_SHOOT_COL': 'remove_shield_col',
       'E_RESET_SHOOT_COL': 'add_shield_col',
       'E_REBIND_SHOOT_COL': 'rebind_col',
       'E_GM_RESCALE_TARGET': 'gm_rescale_mecha_model',
       'E_DEATH': 'die',
       'E_SWITCH_MODEL': 'on_switch_model',
       'E_BEGIN_REFRESH_WHOLE_MODEL': 'remove_shield_col',
       'E_CHANGE_MECHA_COLLISION': 'on_change_collision'
       }
    SHIELD_SFX_MAP = {1: 'effect/fx/weapon/other/dun_shoujismall.sfx',
       2: 'effect/fx/weapon/other/dun_shoujimiddle.sfx',
       3: 'effect/fx/weapon/other/dun_shouji.sfx'
       }
    SHIELD_SFX_MAX_COUNT = {1: 2,
       2: 2,
       3: 2
       }
    SHIELD_BREAK_EFFECT = 'effect/fx/weapon/other/dun_shoujiposui_distortion.sfx'
    BREAK_EFFECT_RADIUS = 3.75 * NEOX_UNIT_SCALE

    def __init__(self):
        super(ComMechaShieldCollision, self).__init__()
        self.shield_col = None
        self.sd.ref_mecha_shield_col_id = None
        self.is_active = False
        self.shield_radius = 100
        self.tm_mgr = global_data.game_mgr.get_logic_timer()
        self.shield_max_list = {1: [],2: [],3: []}
        self.is_add_shield_col = False
        self.break_effect_id = None
        self.last_show_break_effect_time = 0
        self._last_show_shield_time = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaShieldCollision, self).init_from_dict(unit_obj, bdict)
        mecha_conf = self.ev_g_mecha_config('PhysicConfig')
        pve_fix = global_data.game_mode.is_pve()
        self.shield_radius = pve_fix or mecha_conf['shield_radius'] if 1 else mecha_conf['pve_shield_radius']
        self.pos_offset = None
        self.is_reycling = bdict.get('pre_standby', False)
        self.sd.ref_mecha_shield_col_id = None
        self._mecha_id = bdict.get('mecha_id', '8001')
        self.handle_sunshine()
        return

    def handle_sunshine(self):
        if not global_data.use_sunshine:
            return
        p = global_data.sunshine_mecha_col_dict
        if not p:
            return
        m_id = p.get('mecha_id', 0)
        if str(m_id) == str(self._mecha_id):
            shiled_radius = p.get('shield_radius', 0)
            if shiled_radius:
                self.shield_radius = shiled_radius

    def on_human_model_load(self, model, *args):
        if self.is_reycling:
            return
        self.create_collision()

    def create_collision(self):
        self.shield_col = collision.col_object(collision.SPHERE, math3d.vector(self.shield_radius, 0, 0), 0, 0, 0)
        self.shield_col.car_undrivable = True
        self.shield_col.mask = GROUP_GRENADE
        self.shield_col.group = GROUP_SHIELD
        self.add_shield_col()
        self.sd.ref_mecha_shield_col_id = self.shield_col.cid

    def _get_mecha_shield_id(self):
        if self.shield_col:
            return self.shield_col.cid

    def on_hit_shield_sfx(self, begin=None, end=None, itype=None):
        now = global_data.game_time
        if now - self._last_show_shield_time <= 0.1:
            return
        else:
            if self.ev_g_shield() <= 0:
                return
            self._last_show_shield_time = now
            if itype is None:
                itype = 1001
            sfx_level = confmgr.get('firearm_config', str(itype), 'iScreenLevel', default=1)
            shield_sfx = self.SHIELD_SFX_MAP.get(sfx_level)
            sfx_reuse = None
            sfx_list = self.shield_max_list[sfx_level]
            if len(sfx_list) >= self.SHIELD_SFX_MAX_COUNT[sfx_level]:
                sfx_reuse = sfx_list[0]
            if type(begin) in [list, tuple]:
                begin = math3d.vector(*begin)
            if type(end) in [list, tuple]:
                end = math3d.vector(*end)
            if check_need_ignore_effect_behind_camera(itype, end):
                return
            if begin is None and self.shield_col is not None:
                begin = self.shield_col.position
                hit_dir = end - begin
                if hit_dir.is_zero:
                    return
                hit_dir.normalize()
                hit_pos = begin + hit_dir * self.shield_radius
                hit_normal = hit_dir
                if sfx_reuse:
                    sfx_reuse.restart()
                    sfx_reuse.world_position = hit_pos
                    global_data.sfx_mgr.set_rotation_by_normal(sfx_reuse, hit_normal)
                else:

                    def create_cb(sfx):
                        if self.is_valid():
                            global_data.sfx_mgr.set_rotation_by_normal(sfx, hit_normal)
                            sfx.scale = math3d.vector(1.5, 1.5, 1.5)
                            self.add_sfx(sfx, sfx_level)
                        else:
                            global_data.sfx_mgr.remove_sfx(sfx)

                    def remove_cb(sfx):
                        if self.is_valid():
                            self.del_sfx(sfx, sfx_level)

                    global_data.sfx_mgr.create_sfx_in_scene(shield_sfx, hit_pos, on_create_func=create_cb, on_remove_func=remove_cb, int_check_type=CREATE_SRC_SIMPLE)
                return
            scn = global_data.game_mgr.scene
            if scn and self.shield_col:
                result = scn.scene_col.hit_by_ray(begin, end + (end - begin) * self.shield_radius, 0, GROUP_GRENADE, GROUP_SHIELD, collision.EQUAL_FILTER, True)
                if result[0]:
                    hit_pos = None
                    hit_normal = None
                    for cobj_info in result[1]:
                        if cobj_info[4].cid == self.shield_col.cid:
                            hit_pos = cobj_info[0]
                            hit_normal = cobj_info[1]
                            break

                    if not hit_pos or not hit_normal or hit_normal.is_zero:
                        return
                    if sfx_reuse:
                        sfx_reuse.restart()
                        sfx_reuse.world_position = hit_pos
                        global_data.sfx_mgr.set_rotation_by_normal(sfx_reuse, hit_normal)
                    else:

                        def create_cb(sfx):
                            if self.is_valid():
                                global_data.sfx_mgr.set_rotation_by_normal(sfx, hit_normal)
                                sfx.scale = math3d.vector(1.5, 1.5, 1.5)
                                self.add_sfx(sfx, sfx_level)
                            else:
                                global_data.sfx_mgr.remove_sfx(sfx)

                        def remove_cb(sfx):
                            if self.is_valid():
                                self.del_sfx(sfx, sfx_level)

                        global_data.sfx_mgr.create_sfx_in_scene(shield_sfx, hit_pos, on_create_func=create_cb, on_remove_func=remove_cb, int_check_type=CREATE_SRC_SIMPLE)
            return

    def add_sfx(self, sfx, level):
        sfx_list = self.shield_max_list[level]
        sfx_list.append(sfx)

    def del_sfx(self, sfx, level):
        sfx_list = self.shield_max_list[level]
        if sfx in sfx_list:
            sfx_list.remove(sfx)

    def on_shield_change(self, shield, add_from_dmg=False):
        if shield <= 0:
            self.show_break_effect()
            self.remove_shield_col()
        else:
            self.add_shield_col()

    def reset_break_effect(self):
        if self.break_effect_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.break_effect_id)
            self.break_effect_id = None
        return

    def show_break_effect(self):
        now = global_data.game_time
        if now - self.last_show_break_effect_time <= 5:
            return
        model = self.ev_g_model()
        if not model:
            return
        self.last_show_break_effect_time = now
        self.reset_break_effect()
        scale = self.shield_radius / self.BREAK_EFFECT_RADIUS
        mat = model.get_bone_matrix(animation_const.BONE_BIPED_NAME, world.SPACE_TYPE_WORLD)
        if mat:
            epos = mat.translation

            def create_cb(sfx):
                sfx.scale = math3d.vector(scale, scale, scale)

            self.break_effect_id = global_data.sfx_mgr.create_sfx_in_scene(self.SHIELD_BREAK_EFFECT, epos, on_create_func=create_cb, on_remove_func=self.del_break_effect_cb, int_check_type=CREATE_SRC_SIMPLE)

    def del_break_effect_cb(self, *args):
        self.break_effect_id = None
        return

    def die(self):
        self.remove_shield_col()
        self.shield_col = None
        self.sd.ref_mecha_shield_col_id = None
        return

    def remove_shield_col(self, model=None):
        if model is None:
            model = self.ev_g_model()
        if not model:
            return
        else:
            if self.shield_col and self.is_add_shield_col:
                global_data.emgr.scene_remove_mecha_shield_event.emit(self.shield_col.cid)
                self.is_add_shield_col = False
                model.unbind_col_obj(self.shield_col)
            return

    def add_shield_col(self, model=None):
        if model is None:
            model = self.ev_g_model()
        if not model:
            return
        else:
            if self.shield_col and not self.is_add_shield_col:
                global_data.emgr.scene_add_mecha_shield_event.emit(self.shield_col.cid, self.unit_obj)
                model.bind_col_obj(self.shield_col, animation_const.BONE_BIPED_NAME)
                if self.pos_offset:
                    self.shield_col.bone_matrix = math3d.matrix.make_translation(self.pos_offset.x, self.pos_offset.y, self.pos_offset.z)
                self.is_add_shield_col = True
            return

    def on_leave_mecha(self):
        if self.unit_obj.get_owner().is_share():
            return
        self.remove_shield_col()

    def destroy(self):
        self.reset_break_effect()
        self.remove_shield_col()
        self.shield_col = None
        self.sd.ref_mecha_shield_col_id = None
        self.tm_mgr = None
        super(ComMechaShieldCollision, self).destroy()
        return

    def rebind_col(self, bone_name):
        if not self.shield_col or not self.shield_col.valid:
            return
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        model.unbind_col_obj(self.shield_col)
        model.bind_col_obj(self.shield_col, bone_name)

    def gm_rescale_mecha_model(self, scl_xyz):
        f_scl_xyz = float(scl_xyz)
        model = self.ev_g_model()
        if not model:
            return
        self.remove_shield_col()
        self.shield_radius = self.shield_radius * f_scl_xyz
        self.create_collision()

    def on_switch_model(self, model):
        old_model = self.ev_g_mecha_original_model() if self.sd.ref_using_second_model else self.ev_g_mecha_second_model()
        self.remove_shield_col(old_model)
        self.add_shield_col(model)

    def on_change_collision(self, shield_col_info=None, shoot_col_info=None):
        mecha_conf = self.ev_g_mecha_config('PhysicConfig')
        pve_fix = global_data.game_mode.is_pve()
        self.shield_radius = pve_fix or mecha_conf['shield_radius'] if 1 else mecha_conf['pve_shield_radius']
        self.pos_offset = None
        if shield_col_info:
            self.shield_radius, self.pos_offset = shield_col_info
        self.remove_shield_col()
        self.create_collision()
        return