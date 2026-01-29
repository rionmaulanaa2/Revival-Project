# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8036.py
from __future__ import absolute_import
import six
from .ComGenericMechaEffect import ComGenericMechaEffect
import logic.gcommon.common_utils.bcast_utils as bcast
import weakref
import world
import math3d
import render
from common.cfg import confmgr
from logic.gutils.mecha_utils import get_fire_end_posiiton
import world
import collision
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, GROUP_SHOOTUNIT
from logic.manager_agents.manager_decorators import sync_exec
from logic.gutils.client_unit_tag_utils import preregistered_tags
from logic.gcommon.const import PART_WEAPON_POS_MAIN4
from logic.gutils.screen_effect_utils import _create_screen_effect_callback
ENERGY_FINISH_SCREEN_SFX = '100'
ENERGY_FINISH_LOOP_SFX = '107'
HOOK_SFX = '101'
HOOK_TARGET_SFX = '102'
HOOK_TARGET_MECHA_SFX = '103'
HOOK_TARGET_END = '104'
HOOK_TARGET_END_MECHA = '106'
CLAW_DRAG_SFX = '108'
GHOST_SHADER_EFFECT = '105'
HOOK_MODEL_LENGTH = 1330.0
TRACK_WEAPON_POS = PART_WEAPON_POS_MAIN4

class ComMechaEffect8036(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHOW_CLAW_TARGET_EFFECT': 'on_show_hook_effect',
       'E_CANCEL_CLAW_TARGET_EFFECT': 'on_hide_hook_effect',
       'E_MECHA_LOD_LOADED_FIRST': 'on_create_all_use_hold_effect',
       'E_UPDATE_HOOK_STATE': 'on_update_hook_sfx_state',
       'E_SYNC_HOOK_POS': 'on_update_hook_sfx_pos_and_rotate',
       'E_SHOW_HOOK_TRACK_SFX': 'on_show_hook_track_sfx',
       'E_HIDE_HOOK_TRACK_SFX': 'on_hide_hook_track_sfx',
       'E_UPDATE_SFX_STATE': 'on_update_sfx_state',
       'E_SHOW_GHOST_EFFECT': 'on_show_ghost_effect',
       'E_HIDE_GHOST_EFFECT': 'on_hide_ghost_effect',
       'E_SHOW_FINISH_ENERGY_EFFECT': 'on_show_finish_energy_effect',
       'E_HIDE_FINISH_ENERGY_EFFECT': 'on_hide_finish_energy_effect',
       'E_SHOW_HOOK_END_EFFECT': 'on_show_hook_end_effect',
       'E_HIDE_HOOK_END_EFFECT': 'on_hide_hook_end_effect',
       'E_TRIGGER_THROWABLE_MAX_DIST_CHANGE': 'on_throwable_max_dist_change',
       'E_TRIGGER_THROWABLE_MAX_DIST_SCALE_CHANGE': 'on_throwable_max_dist_scale_change',
       'E_SHOW_CLAW_DRAG_SCRREN_EFFECT': 'on_show_claw_drag_screen_effect',
       'E_HIDE_CLAW_DRAG_SCRREN_EFFECT': 'on_hide_claw_drag_screen_effect'
       })
    STATE_NONE = 0
    STATE_HOOK_RELEASE = 1
    STATE_HOOK_DRAG = 2
    STATE_HOOK_RECOVERY = 3
    STATE_CLAW_MECHA = 1
    STATE_CLAW_SCENE_AND_NONE = 2

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8036, self).init_from_dict(unit_obj, bdict)
        self.model_ref = None
        self.init_hook_parameters()
        self.init_hook_target_parameters()
        self.init_hook_track_parameters()
        self.init_ghost_paramters()
        self.init_hook_end_parameters()
        return

    def init_hook_parameters(self):
        self._hook_sfx = None
        self.show_hook_sfx = False
        self.hook_state = self.STATE_NONE
        return

    def init_hook_end_parameters(self):
        self._cur_hook_end_sfx = None
        self.cur_hook_end_state = self.STATE_CLAW_MECHA
        self.hook_end_sfxs = {}
        return

    def init_hook_target_parameters(self):
        self._weapon_col_target = None
        self._cur_target_type = HOOK_TARGET_SFX
        self._cur_hook_target_sfx = None
        self.hook_target_sfxs = {}
        self.hook_target_sfxs_state = {}
        self.hook_target_pos = (0, 0, 0)
        return

    def init_hook_track_parameters(self):
        self._claw_grenade_max_dis = -1
        self._cur_track_weapon_pos = None
        self._detect_col = None
        self.fire_socket = None
        self.show_hook_track = False
        self.ignore_col_ids = []
        self.max_dist_change_rate = {}
        self.max_dist_scale_change_rate = {}
        return

    def init_ghost_paramters(self):
        self._ghost_model = None
        self._ghost_load_task = None
        self._ghost_sfx = None
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8036, self).on_model_loaded(model)
        self.model_ref = weakref.ref(model)

    def on_update_hook_sfx_state(self, state, dict_info=None, need_sync=False):
        self.hook_state = state
        self._weapon_col_target = dict_info.get('target', None)
        self.hook_target_pos = dict_info.get('hook_target_pos', (0, 0, 0))
        if need_sync:
            self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_UPDATE_HOOK_STATE, (state, dict_info)], True, False, True)
        return

    def on_update_hook_sfx_pos_and_rotate(self, pos):
        if not self.hook_sfx:
            return
        start_position = self.hook_sfx.world_position
        end_position = pos if type(pos) == math3d.vector else math3d.vector(*pos)
        dist_vec = end_position - start_position
        distance = dist_vec.length
        old_scale = self.hook_sfx.scale
        self.hook_sfx.scale = math3d.vector(old_scale.x, old_scale.y, distance / 1330.0)
        dist_vec.normalize()
        self.hook_sfx.world_rotation_matrix = math3d.matrix.make_rotation_x(dist_vec.pitch) * math3d.matrix.make_rotation_y(dist_vec.yaw)
        if self.hook_state == self.STATE_HOOK_RELEASE:
            self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SYNC_HOOK_POS, ((end_position.x, end_position.y, end_position.z),)], True, False, True)

    @property
    def hook_sfx(self):
        if not self._hook_sfx or not self._hook_sfx.valid:
            return None
        else:
            return self._hook_sfx

    @property
    def ghost_model(self):
        if not self._ghost_model or not self._ghost_model.valid:
            return None
        else:
            return self._ghost_model

    @property
    def ghost_sfx(self):
        if not self._ghost_sfx or not self._ghost_sfx.valid:
            return None
        else:
            return self._ghost_sfx

    def on_show_hook_track_sfx(self, weapon_pos):
        self.show_weapon_track(weapon_pos)

    def on_hide_hook_track_sfx(self):
        self.stop_weapon_track()

    def on_update_sfx_state(self, state):
        self.need_update = state

    def show_hook_target_sfx(self, sfx_type, sfx_target_pos):
        if not self.hook_target_sfxs or sfx_type not in self.hook_target_sfxs:
            self.hook_target_sfxs_state[self._cur_target_type] = False
            if self._cur_target_type in self.hook_target_sfxs:
                self.hook_target_sfxs[self._cur_target_type].visible = False
            self._cur_target_type = sfx_type
            self.hook_target_sfxs_state[sfx_type] = True
            return
        if self._cur_target_type in self.hook_target_sfxs:
            self.hook_target_sfxs[self._cur_target_type].visible = False
        self.hook_target_sfxs_state[self._cur_target_type] = False
        self._cur_target_type = sfx_type
        self._cur_hook_target_sfx = self.hook_target_sfxs[self._cur_target_type]
        self.hook_target_sfxs[self._cur_target_type].visible = True

    def hide_hook_target_sfx(self):
        if not self.hook_target_sfxs or self._cur_target_type not in self.hook_target_sfxs:
            self.hook_target_sfxs_state[self._cur_target_type] = False
            return
        self.hook_target_sfxs[self._cur_target_type].visible = False
        self.hook_target_sfxs_state[self._cur_target_type] = False

    def create_hook_effect(self):

        def create_cb(sfx):
            self._hook_sfx = sfx
            self._hook_sfx.remove_from_parent()
            if self.model_ref is None:
                return
            else:
                mecha_model = self.model_ref()
                if not mecha_model or not mecha_model.valid:
                    return
                mecha_model.bind_bone('bone_wp_l_root', self._hook_sfx, math3d.matrix(), world.BIND_TYPE_TRANSLATE)
                self._hook_sfx.inherit_flag &= ~world.INHERIT_VISIBLE
                self._hook_sfx.visible = self.show_hook_sfx
                return

        self.on_trigger_hold_effect(HOOK_SFX, create_cb=create_cb)

    def create_hook_end_sfx(self):

        def create_cb(sfx, sfx_type):
            sfx.visible = False
            self.hook_end_sfxs[sfx_type] = sfx

        self.on_trigger_hold_effect(HOOK_TARGET_END, create_cb=lambda sfx, sfx_type=self.STATE_CLAW_SCENE_AND_NONE: create_cb(sfx, sfx_type))
        self.on_trigger_hold_effect(HOOK_TARGET_END_MECHA, create_cb=lambda sfx, sfx_type=self.STATE_CLAW_MECHA: create_cb(sfx, sfx_type))

    def create_hook_target_effect(self):

        def create_cb(sfx, sfx_type):
            self.hook_target_sfxs[sfx_type] = sfx
            sfx.visible = self.hook_target_sfxs_state.get(sfx_type, False)

        self.on_trigger_hold_effect(HOOK_TARGET_SFX, create_cb=lambda sfx, sfx_type=HOOK_TARGET_SFX: create_cb(sfx, sfx_type))
        self.on_trigger_hold_effect(HOOK_TARGET_MECHA_SFX, create_cb=lambda sfx, sfx_type=HOOK_TARGET_MECHA_SFX: create_cb(sfx, sfx_type))

    def create_hook_track_effect(self):
        self._gravity_track = world.gravity_track(35)
        self._gravity_track.set_width(2)
        self._gravity_track.set_track_gravity(0.0)
        self.triangle_strip = self._gravity_track.get_primitives()
        if not self.triangle_strip:
            return
        tech = render.technique(render.TECH_TYPE_EFFECT, 'shader/throw_line.fx', 'TShader')
        self.triangle_strip.set_technique(tech)
        tex = render.texture('shader/texture/zhishixian_01_bu.tga')
        self.triangle_strip.set_texture(0, tex)
        self._set_strip_top_most()
        self.set_track_visibility(False)

    def create_ghost_effect(self):
        if not self.model_ref():
            return
        else:
            model = self.model_ref()
            file_path = model.filename

            def create_cb(model, *args):
                if not self.ghost_model:
                    return
                else:
                    self.ghost_model.add_mesh(model)
                    effect_info = self._dynamic_effect_conf.get(GHOST_SHADER_EFFECT, {}).get('hold', {})
                    if not effect_info:
                        return
                    effect_path = effect_info[0]['final_correspond_path']
                    socket_list = effect_info[0].get('socket_list', ['fx_root'])
                    self._ghost_sfx = world.sfx(effect_path, scene=None)
                    self.ghost_model.bind(socket_list[0], self._ghost_sfx)
                    self.ghost_model.visible = False
                    return

            self._ghost_model = world.model(file_path, global_data.game_mgr.scene)
            self._ghost_load_task = world.create_res_object_async(file_path.replace('empty', 'l3'), create_cb, None)
            return

    def on_create_all_use_hold_effect(self):
        self.create_hook_effect()
        self.create_hook_target_effect()
        self.create_hook_track_effect()
        self.create_ghost_effect()
        self.create_hook_end_sfx()

    def on_show_hook_effect(self):
        if not self.hook_sfx:
            self.show_hook_sfx = True
            return
        self.need_update = True
        self.hook_sfx.visible = True
        old_scale = self.hook_sfx.scale
        self.hook_sfx.restart()
        self.hook_sfx.scale = math3d.vector(old_scale.x, old_scale.y, 0.0)
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_CLAW_TARGET_EFFECT, ()], True, False, True)

    def on_hide_hook_effect(self):
        if not self.hook_sfx or not self.hook_sfx.valid:
            self.show_hook_sfx = False
            return
        self.need_update = False
        self.hook_sfx.visible = False
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CANCEL_CLAW_TARGET_EFFECT, ()], True, False, True)

    def on_release_to_target(self, dt):
        if not self.hook_sfx:
            return
        if not self._weapon_col_target or not self._weapon_col_target.valid:
            return
        self.on_update_hook_sfx_pos_and_rotate(self._weapon_col_target.position)

    def on_drag_to_target(self, dt):
        if not self.hook_sfx:
            return
        self.on_update_hook_sfx_pos_and_rotate(self.hook_target_pos)
        self.on_update_hook_end_sfx_pos_and_rotate(self.hook_target_pos)

    def on_show_ghost_effect(self, pos, yaw, anim_name, start_time):
        if not self.ghost_model:
            return
        if self._ghost_sfx:
            self._ghost_sfx.restart()
        self.ghost_model.visible = True
        self.ghost_model.world_position = pos
        self.ghost_model.rotation_matrix = math3d.matrix.make_rotation_y(yaw)
        self.ghost_model.play_animation(anim_name, 0.0, world.TRANSIT_TYPE_NONE, start_time, False, 0.0)
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_GHOST_SFX, (pos, yaw, anim_name, start_time)], True, False, True)

    def on_hide_ghost_effect(self):
        if not self.ghost_model:
            return
        self.ghost_model.visible = False
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_HIDE_GHOST_SFX, ()], True, False, True)

    def on_show_finish_energy_effect(self):
        self.on_trigger_disposable_effect(ENERGY_FINISH_SCREEN_SFX, [0, 0, 0], duration=0.0, need_sync=False, on_create_func=lambda sfx, effect_path='ENERGY_FINISH_SCREEN_SFX': _create_screen_effect_callback(sfx, effect_path, None))
        self.on_trigger_state_effect('energy_finish', ENERGY_FINISH_LOOP_SFX, force=True, need_sync=True)

    def on_hide_finish_energy_effect(self):
        self.on_trigger_state_effect('energy_finish', '', need_sync=True)

    def on_throwable_max_dist_change(self, weapon_pos, max_dist_rate):
        if not max_dist_rate:
            self.max_dist_change_rate[weapon_pos] = 0
        else:
            self.max_dist_change_rate[weapon_pos] = max_dist_rate

    def on_throwable_max_dist_scale_change(self, weapon_pos, scale):
        if not scale:
            self.max_dist_scale_change_rate[weapon_pos] = 1.0
        else:
            self.max_dist_scale_change_rate[weapon_pos] = scale

    def on_show_claw_drag_screen_effect(self):
        self.on_trigger_state_effect('claw_drag', CLAW_DRAG_SFX, force=True, need_sync=True)

    def on_hide_claw_drag_screen_effect(self):
        self.on_trigger_state_effect('claw_drag', '', need_sync=True)

    def on_update_hook_end_sfx_pos_and_rotate(self, pos):
        pos = math3d.vector(*pos)
        if self.hook_sfx and self._cur_hook_end_sfx:
            start_position = self.hook_sfx.world_position
            end_position = pos
            dist_vec = end_position - start_position
            m_mat = self._cur_hook_end_sfx.world_rotation_matrix
            dist_vec.normalize()
            self._cur_hook_end_sfx.world_rotation_matrix = m_mat.make_rotation_x(dist_vec.pitch) * m_mat.make_rotation_y(dist_vec.yaw)
            self._cur_hook_end_sfx.world_position = pos

    def on_show_hook_end_effect(self, sfx_type, pos):
        if sfx_type not in self.hook_end_sfxs:
            return
        self._cur_hook_end_sfx = self.hook_end_sfxs[sfx_type]
        self._cur_hook_end_sfx.visible = True
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_HOOK_END_SFX, (sfx_type, pos)], True, False, True)

    def on_hide_hook_end_effect(self):
        if not self._cur_hook_end_sfx or not self._cur_hook_end_sfx.valid:
            return
        self._cur_hook_end_sfx.visible = False
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_HIDE_HOOK_END_SFX, ()], True, False, True)

    def show_weapon_track(self, weapon_pos):
        if global_data.mecha and self.unit_obj != global_data.mecha.logic:
            return
        else:
            weapon = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
            if not weapon:
                return
            if not self._cur_track_weapon_pos or self._cur_track_weapon_pos != weapon_pos:
                conf = confmgr.get('grenade_config', str(weapon.iType))
                self._claw_grenade_max_dis = conf['fMaxDistance']
                conf = confmgr.get('firearm_res_config', str(weapon.iType))
                self.fire_socket = conf.get('cBindPointEmission', None)[0]
                self._cur_track_weapon_pos = weapon_pos
            self.ignore_col_ids = self.unit_obj.ev_g_human_col_id()
            shield_id = self.unit_obj.sd.ref_mecha_shield_col_id
            if shield_id:
                self.ignore_col_ids.append(shield_id)
            relative_ids = self.unit_obj.sd.ref_mecha_relative_cols
            if relative_ids:
                self.ignore_col_ids.extend(relative_ids)
            self.show_hook_track = True
            self.set_ignore_cols()
            self.set_track_visibility(True)
            return

    def stop_weapon_track(self):
        self.show_hook_track = False
        self.set_track_visibility(False)

    def get_col(self):
        if self._detect_col is not None:
            return self._detect_col
        else:
            size = math3d.vector(0.1, 0.1, 0.1)
            self._detect_col = collision.col_object(collision.SPHERE, size, -1, -1)
            world.get_active_scene().scene_col.add_object(self._detect_col)
            return self._detect_col

    def get_contact_end(self, pos, speed):
        fpos = pos
        tpos = pos
        col = self.get_col()
        scene_col = world.get_active_scene().scene_col
        speed = math3d.vector(speed)
        t = 0.1
        for i in range(1, 10):
            tpos = fpos + speed * t
            info = scene_col.sweep_test(col, fpos, tpos, GROUP_SHOOTUNIT, -1, 0, collision.INCLUDE_FILTER)
            if info[0]:
                if info[5].cid in self.ignore_col_ids:
                    info = scene_col.sweep_test(col, info[1], tpos, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, 0, collision.INCLUDE_FILTER)
                    if not info[0] or info[5].cid in self.ignore_col_ids:
                        fpos = tpos
                        continue
                unit = global_data.emgr.scene_find_unit_event.emit(info[5].cid)[0]
                if not unit:
                    self.show_hook_target_sfx(HOOK_TARGET_SFX, info[1])
                    return (
                     info[1], info[2])
                if not self.unit_obj.ev_g_is_campmate(unit.ev_g_camp_id()):
                    if unit.MASK & preregistered_tags.MECHA_TAG_VALUE:
                        self.show_hook_target_sfx(HOOK_TARGET_MECHA_SFX, info[1])
                        return (
                         info[1], info[2])
                    if not unit.MASK & preregistered_tags.HUMAN_TAG_VALUE:
                        self.show_hook_target_sfx(HOOK_TARGET_SFX, info[1])
                        return (
                         info[1], info[2])
            fpos = tpos

        self.show_hook_target_sfx(HOOK_TARGET_SFX, tpos)
        return (
         tpos, tpos)

    @sync_exec
    def _set_strip_top_most(self):
        if self.triangle_strip and self.triangle_strip.valid:
            self.triangle_strip.top_most = True

    def set_track_visibility(self, visible):
        if self.triangle_strip:
            self.triangle_strip.visible = visible
        if self._cur_hook_target_sfx:
            self._cur_hook_target_sfx.visible = visible

    def set_ignore_cols(self):
        self.ignore_col_ids = self.unit_obj.ev_g_human_col_id()
        shield_id = self.unit_obj.sd.ref_mecha_shield_col_id
        if shield_id:
            self.ignore_col_ids.append(shield_id)
        relative_ids = self.unit_obj.sd.ref_mecha_relative_cols
        if relative_ids:
            self.ignore_col_ids.extend(relative_ids)

    def refresh_strip(self, start_pos):
        if not self.triangle_strip or not self.triangle_strip.valid:
            return
        if not start_pos:
            return
        add_rate = self.max_dist_change_rate.get(self._cur_track_weapon_pos, 0.0)
        mul_scale = self.max_dist_scale_change_rate.get(self._cur_track_weapon_pos, 1.0)
        speed = self._claw_grenade_max_dis * (1.0 + add_rate) * mul_scale
        direction = self.cal_direction(start_pos)
        vy = direction.y
        if abs(vy) < 1:
            from math import sqrt
            vz = sqrt(1 - vy * vy) * speed
        else:
            vz = 0
        vy *= speed
        end_point, normal = self.get_contact_end(start_pos, direction * speed)
        self.end_pos = end_point
        if normal:
            if self._cur_hook_target_sfx:
                self._cur_hook_target_sfx.visible = True
                self._cur_hook_target_sfx.position = end_point
        elif self._cur_hook_target_sfx:
            self._cur_hook_target_sfx.visible = False
        else:
            self.end_pos.y = -100
        offset = end_point - start_pos
        if abs(direction.x + direction.z) > 0.0001:
            time = (offset.x + offset.z) / ((direction.x + direction.z) * speed)
        else:
            time = 3.5
        self._gravity_track.set_track_info(math3d.vector(0, vy, vz), time)
        direction.y = 0
        if direction.is_zero:
            self.triangle_strip.position = start_pos
        else:
            self.triangle_strip.set_placement(start_pos, direction, math3d.vector(0, 1, 0))

    def get_fire_pos(self):
        model = self.model_ref()
        if not model or not model.valid:
            return None
        else:
            if not self.fire_socket:
                return None
            socket_matrix = model.get_socket_matrix(self.fire_socket, world.SPACE_TYPE_WORLD)
            if not socket_matrix:
                return None
            return socket_matrix.translation

    def cal_direction(self, position):
        end_pos = get_fire_end_posiiton(self.unit_obj)
        direction = end_pos - position
        if not direction.is_zero:
            direction.normalize()
        return direction

    def tick(self, delta):
        if self.show_hook_track:
            self.refresh_strip(self.get_fire_pos())
        if self.hook_state == self.STATE_HOOK_RELEASE:
            self.on_release_to_target(delta)
        elif self.hook_state == self.STATE_HOOK_DRAG:
            self.on_drag_to_target(delta)

    def destroy(self):
        super(ComMechaEffect8036, self).destroy()
        if self._ghost_load_task:
            self._ghost_load_task.cancel()
            self._ghost_load_task = None
        if self.ghost_model:
            self._ghost_model.destroy()
            self._ghost_model = None
        if self._detect_col:
            scn = world.get_active_scene()
            scn.scene_col.remove_object(self._detect_col)
            self._detect_col = None
        for _, sfxs in six.iteritems(self.hook_end_sfxs):
            if sfxs and sfxs.valid:
                sfxs.destroy()

        self.hook_end_sfxs = {}
        for _, sfx in six.iteritems(self.hook_target_sfxs):
            if sfx and sfx.valid:
                sfx.destroy()

        self.hook_target_sfxs = {}
        self.max_dist_change_rate = {}
        self.max_dist_scale_change_rate = {}
        self._cur_hook_target_sfx = None
        self._cur_hook_end_sfx = None
        self._hook_sfx = None
        return