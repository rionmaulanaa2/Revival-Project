# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_effect/ComHumanEffectCommon.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
import math3d
import collision
import world
import logic.gcommon.common_utils.bcast_utils as bcast
import logic.gcommon.item.item_const as item_const
from common.cfg import confmgr
from logic.gutils.sfx_utils import get_dead_sfx_scale_by_length_spr
import logic.gcommon.common_const.animation_const as animation_const
from common.platform.dctool import interface
from logic.gcommon.common_utils import battle_utils
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
ON_GROUND_SFX = {'small': 'effect/fx/mecha/8008/8008_luodi_s.sfx',
   'middle': 'effect/fx/mecha/8008/8008_luodi_m.sfx',
   'large': 'effect/fx/mecha/8008/8008_luodi.sfx'
   }

class ComHumanEffectCommon(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_CREATE_SCENE_EFFECT': 'on_create_scene_effect',
       'E_CREATE_MODEL_EFFECT': 'on_create_model_effects',
       'E_CREATE_GUN_MODEL_EFFECT': 'on_create_gun_model_effects',
       'E_REMOVE_MODEL_EFFECT': 'on_remove_model_effects',
       'E_SHOW_ONGROUND_SFX': 'on_show_onground_sfx',
       'E_SHOW_DIE_SFX': 'on_show_die_sfx',
       'E_SHOW_DIE_SFX_BY_PATH': 'on_show_die_sfx_by_path',
       'E_CREATE_RES_EFFECT': 'on_create_res_effects',
       'E_REMOVE_RES_EFFECT': 'on_remove_res_effects',
       'E_CACHE_MODEL_ANI_LIST': 'on_cache_model_ani_list'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComHumanEffectCommon, self).init_from_dict(unit_obj, bdict)
        self._last_cast_time = 0
        self._onground_sfx_info = None
        self._register_pos_event = None
        self._model_sfx_ids = {}
        self._socket_model_ids = {}
        return

    def destroy(self):
        super(ComHumanEffectCommon, self).destroy()
        self.clear_model_sfxs()
        self.clear_socket_models()

    def _on_pos_changed(self, pos):
        model = self.ev_g_model()
        if not model or not self._onground_sfx_info:
            self.unregist_event('E_POSITION', self._on_pos_changed)
            self._register_pos_event = None
            return
        else:
            try:
                dest_pos, sfx_type = self._onground_sfx_info
                diff_y = abs(pos.y - dest_pos.y)
                if diff_y <= 2:
                    global_data.sfx_mgr.create_sfx_in_scene(ON_GROUND_SFX[sfx_type], dest_pos, duration=1.2, int_check_type=CREATE_SRC_SIMPLE)
                    self.unregist_event('E_POSITION', self._on_pos_changed)
                    self._register_pos_event = None
                    self._onground_sfx_info = None
            except:
                pass

            return

    def on_show_onground_sfx(self, sfx_type='middle', pos=None):
        if pos:
            model_pos = self.ev_g_position()
            if not model_pos:
                return
            pos = math3d.vector(*pos)
            diff_y = abs(pos.y - model_pos.y)
            if diff_y <= 2:
                global_data.sfx_mgr.create_sfx_in_scene(ON_GROUND_SFX[sfx_type], pos, duration=1.2, int_check_type=CREATE_SRC_SIMPLE)
            else:
                self._onground_sfx_info = (
                 pos, sfx_type)
                if self._register_pos_event:
                    self.unregist_event('E_POSITION', self._register_pos_event)
                self.regist_event('E_POSITION', self._on_pos_changed)
                self._register_pos_event = self._on_pos_changed
        else:
            pos = self.ev_g_position()
            if not pos:
                return
        up = math3d.vector(0, 1, 0)
        start_pos = pos + up
        end_pos = pos - up * 2000
        from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE
        result = self.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER)
        if result and result[0]:
            global_data.sfx_mgr.create_sfx_in_scene(ON_GROUND_SFX[sfx_type], result[1], duration=1.2, int_check_type=CREATE_SRC_SIMPLE)
            self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_ONGROUND_SFX, (sfx_type, (result[1].x, result[1].y, result[1].z))], True)

    def on_create_model_effects(self, info, is_sync=False, all_sfx_ids=None):
        model = self.ev_g_model()
        if not model:
            return
        else:
            for sfx_path, sockets in six.iteritems(info):
                for socket_name in sockets:
                    sfx_id_key = sfx_path + socket_name
                    if sfx_id_key in self._model_sfx_ids:
                        global_data.sfx_mgr.remove_sfx_by_id(self._model_sfx_ids[sfx_id_key])
                    one_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket_name)
                    self._model_sfx_ids[sfx_id_key] = one_sfx_id
                    if all_sfx_ids is not None:
                        all_sfx_ids.append(one_sfx_id)

            if is_sync:
                self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CREATE_MODEL_EFFECT, (info,)], True)
            return

    def on_cache_model_ani_list(self, ani_list, is_cache, is_sync=False):
        model = self.ev_g_model()
        if not model:
            return
        for clip_name in ani_list:
            if is_cache:
                act = world.CACHE_ANIM_ALWAYS if 1 else world.CACHE_ANIM_NONE
                model.cache_animation(clip_name, act)

        if is_sync:
            self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CACHE_MODEL_ANI_LIST, (ani_list, is_cache)], True)

    def on_create_res_effects(self, info, model=None, is_sync=False, all_sfx_ids=None, all_model_ids=None, load_model_cb=None, model_cache_map=None):
        if not model:
            model = self.ev_g_model()
            if not model:
                return
        for res_path, bind_infos in six.iteritems(info):
            for bind_info in bind_infos:
                if type(bind_info) in (tuple, list):
                    sub_res_bind_info, socket_name = bind_info

                    def sub_callback(socket_model, s_model_path, s_model_socket_name, s_model_id):
                        if socket_model and socket_model.valid:
                            self._bind_res_to_socket(res_path, socket_model, socket_name, all_sfx_ids, all_model_ids, load_model_cb)

                    self.on_create_res_effects(sub_res_bind_info, model, False, all_sfx_ids, all_model_ids, sub_callback, model_cache_map)
                else:
                    self._bind_res_to_socket(res_path, model, bind_info, all_sfx_ids, all_model_ids, load_model_cb)

        if is_sync:
            self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CREATE_RES_EFFECT, (info,)], True)

    def _bind_res_to_socket(self, res_path, model, socket_name, all_sfx_ids=None, all_model_ids=None, model_load_cb=None, model_cache_map=None):
        from common.framework import Functor
        if res_path.endswith('sfx'):
            sfx_path = res_path
            sfx_id_key = sfx_path + socket_name
            if sfx_id_key in self._model_sfx_ids:
                global_data.sfx_mgr.remove_sfx_by_id(self._model_sfx_ids[sfx_id_key])
            one_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket_name)
            self._model_sfx_ids[sfx_id_key] = one_sfx_id
            if all_sfx_ids is not None:
                all_sfx_ids.append(one_sfx_id)
        else:
            model_path = res_path
            model_id_key = model_path + socket_name

            def on_load_socket_model_complete(socket, socket_model):
                if model and model.valid:
                    model.bind(socket, socket_model)
                if model_cache_map and model_id_key not in model_cache_map:
                    model_cache_map[model_id_key] = socket_model
                if model_load_cb:
                    model_load_cb(socket_model, model_path, socket_name, model_id)

            if model_cache_map:
                cached_s_model = model_cache_map.get(model_id_key)
                if cached_s_model:
                    on_load_socket_model_complete(socket_name, cached_s_model)
                    return
            if model_id_key in self._socket_model_ids:
                global_data.model_mgr.remove_model_by_id(self._socket_model_ids[model_id_key])
            model_id = global_data.model_mgr.create_model(res_path, [], on_create_func=Functor(on_load_socket_model_complete, socket_name))
            self._socket_model_ids[model_id_key] = model_id
            if all_model_ids is not None:
                all_model_ids.append(model_id)
        return

    def on_create_gun_model_effects(self, weapon_pos, info, sync=False):
        model = None
        if weapon_pos == animation_const.WEAPON_POS_LEFT:
            model = self.sd.ref_left_hand_weapon_model
        else:
            model = self.sd.ref_hand_weapon_model
        if not model:
            return
        else:
            for sfx_path, sockets in six.iteritems(info):
                for socket_name in sockets:
                    sfx_id_key = sfx_path + socket_name
                    one_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket_name)

            if sync:
                self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CREATE_GUN_MODEL_EFFECT, (weapon_pos, info)], True)
            return

    def on_remove_model_effects(self, info):
        for sfx_path, sockets in six.iteritems(info):
            for socket_name in sockets:
                sfx_id_key = sfx_path + socket_name
                if sfx_id_key in self._model_sfx_ids:
                    global_data.sfx_mgr.remove_sfx_by_id(self._model_sfx_ids[sfx_id_key])
                    del self._model_sfx_ids[sfx_id_key]

    def on_remove_res_effects(self, info):
        for res_path, bind_infos in six.iteritems(info):
            for bind_info in bind_infos:
                if type(bind_info) in [tuple, list]:
                    sub_res_bind_info, socket_name = bind_info
                    self._remove_res_effect_helper(res_path, socket_name)
                    self.on_remove_res_effects(sub_res_bind_info)
                else:
                    self._remove_res_effect_helper(res_path, bind_info)

    def _remove_res_effect_helper(self, res_path, bind_info):
        socket_name = bind_info
        sfx_path = res_path
        if res_path.endswith('sfx'):
            sfx_id_key = sfx_path + socket_name
            if sfx_id_key in self._model_sfx_ids:
                global_data.sfx_mgr.remove_sfx_by_id(self._model_sfx_ids[sfx_id_key])
                del self._model_sfx_ids[sfx_id_key]
        else:
            model_path = res_path
            model_id_key = model_path + socket_name
            if model_id_key in self._socket_model_ids:
                global_data.model_mgr.remove_model_by_id(self._socket_model_ids[model_id_key])
                del self._socket_model_ids[model_id_key]

    def clear_model_sfxs(self):
        for sfx_id in six.itervalues(self._model_sfx_ids):
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._model_sfx_ids = {}

    def clear_socket_models(self):
        for model_id in self._socket_model_ids:
            global_data.model_mgr.remove_model_by_id(model_id)

        self._socket_model_ids = {}

    def on_create_scene_effect(self, sfx, pos, duration):
        global_data.sfx_mgr.create_sfx_in_scene(sfx, math3d.vector(*pos), duration=duration)
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CREATE_SCENE_EFFECT, (sfx, pos, duration)], True)

    def create_die_sfx_callback(self, sfx):
        import game3d
        import math3d
        game3d.delay_exec(sfx.life_span * 1000, lambda del_sfx=sfx: global_data.sfx_mgr.shutdown_sfx(del_sfx))
        model = self.ev_g_model()
        if not model:
            return
        pos = model.world_position
        cam = world.get_active_scene().active_camera
        dist = cam.position - pos
        scale = get_dead_sfx_scale_by_length_spr(dist.length)
        sfx.world_scale = math3d.vector(scale, scale, scale)
        up = cam.world_rotation_matrix.up
        if up.is_zero:
            up = math3d.vector(0, 1, 0)
        if dist.is_zero:
            forward = math3d.vector(0, 0, -1)
        else:
            forward = -dist
        sfx.world_rotation_matrix = math3d.matrix.make_orient(forward, up)

    def on_show_die_sfx(self, killer_id, kill_effect_id):
        signal = self.ev_g_signal()
        if battle_utils.is_battle_signal_open() and (signal is None or signal <= 0) and killer_id is None:
            return
        else:
            position = math3d.vector(0, 0, 0)
            model = self.ev_g_model()
            if model:
                position = model.world_position
            res_path = None
            if kill_effect_id and kill_effect_id != item_const.DEFAULT_KILL_EFFECT_ITEM_ID:
                kill_effect_cnf = confmgr.get('items_book_conf', 'KillSfxConfig', 'Content', str(kill_effect_id))
                if kill_effect_cnf:
                    res_path = kill_effect_cnf.get('sfx_path')
            if res_path:
                offset_y = 35
                position = math3d.vector(position.x, position.y + offset_y, position.z)
                global_data.sfx_mgr.create_sfx_in_scene(res_path, position, on_create_func=self.create_die_sfx_callback)
            else:
                res_path = 'effect/fx/weapon/other/siwangyanwu_tongyong.sfx'
                if killer_id and (killer_id == global_data.player.id or global_data.player.logic.ev_g_is_in_spectate() and killer_id == global_data.player.logic.ev_g_spectate_target_id()):
                    res_path = 'effect/fx/weapon/other/siwangyanwu.sfx'
                global_data.sfx_mgr.create_sfx_in_scene(res_path, position)
            return

    def on_show_die_sfx_by_path(self, res_path, position=None):
        if position is None:
            position = math3d.vector(0, 0, 0)
            model = self.ev_g_model()
            if model:
                position = model.world_position
        position.y += 35
        global_data.sfx_mgr.create_sfx_in_scene(res_path, position, on_create_func=self.create_die_sfx_callback)
        return