# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect4108.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from .ComGenericMechaEffect import ComGenericMechaEffect
import data.vehicle_seat_data as vehicle_seat_data
from common.cfg import confmgr
import time
import math3d
from logic.gcommon.common_const import scene_const, collision_const
import logic.gcommon.cdata.mecha_status_config as mecha_status_config
FIRE_CD_TIME = 0.1
SHOOT_ACTION_LST = ['shoot1', 'shoot2']
DASH_STATE_ID = 'dash'
DASH_EFFECT_ID = '2'

class ComMechaEffect4108(ComGenericMechaEffect):
    SPECIAL_EFFECT_MAP = {'xingshi': {scene_const.MTL_WATER: ('level_point', 0),scene_const.MTL_DEEP_WATER: ('level_point', 0),'default': ('fx_xingshi', 0)},'shuimian_stop': {scene_const.MTL_WATER: ('level_point', 1),scene_const.MTL_DEEP_WATER: ('level_point', 1),'default': None}}
    SPECIAL_STATUS_EFFECT_MAP = {mecha_status_config.MC_RUN: 'xingshi',
       mecha_status_config.MC_MOVE: 'xingshi',
       mecha_status_config.MC_DASH: 'xingshi',
       mecha_status_config.MC_STAND: 'shuimian_stop'
       }
    DROP_WATER_EFFECT = 'effect/fx/robot/autobot/chushui.sfx'
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MODEL_LOADED': 'on_model_loaded',
       'E_PLAY_SEAT_FIRE_SFX': 'play_seat_fire_sfx',
       'E_PLAY_DROP_WATER': 'play_drop_water_effect',
       'E_PLAY_EFFECT_BY_STATUS': 'play_effect_by_status',
       'E_LAST_MATERIAL_CHANGE': 'handle_special_effect',
       'E_ENTER_STATE': 'enter_states',
       'E_TRIGGER_DASH_EFFECT': 'on_trigger_dash_effect'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect4108, self).init_from_dict(unit_obj, bdict)
        self._last_collision_water_sfx_time = 0
        self._cur_status = None
        self._cur_special_effect = None
        return

    def on_init_complete(self):
        mecha_id = self.sd.ref_mecha_id
        self.all_seat_info = vehicle_seat_data.data.get(mecha_id, {})

    def destroy(self):
        super(ComMechaEffect4108, self).destroy()
        self._last_collision_water_sfx_time = 0
        self._cur_status = None
        self._cur_special_effect = None
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect4108, self).on_model_loaded(model)
        self._seat_fire_sfx_time = {}
        self._init_shoot_action_sfx()

    def enter_states(self, new_state):
        self.play_effect_by_status(new_state)

    def _init_shoot_action_sfx(self):
        model = self.ev_g_model()
        if not model:
            return
        else:
            mecha_id = self.sd.ref_mecha_id
            all_seat_info = vehicle_seat_data.data.get(mecha_id, None)
            if not all_seat_info:
                return
            guns_info = {}
            for seat_name, one_seat_info in six_ex.items(all_seat_info):
                if not one_seat_info:
                    continue
                seat_index = self.ev_g_seat_index_by_seat_name(seat_name)
                if seat_index < 0:
                    continue
                guns = one_seat_info.get('guns', [])
                if not guns:
                    continue
                guns_info[seat_index] = guns[0]

            if not guns_info:
                return
            for seat_index, weapon_id in six_ex.items(guns_info):
                conf = confmgr.get('firearm_res_config', str(weapon_id), default={})
                if not conf:
                    return
                fire_sockets = conf.get('cBindPointEmission', [])
                fire_socket = ''
                if fire_sockets:
                    fire_socket = fire_sockets[0]
                fire_sfx_path = conf.get('cSfx', '')
                bullet_socket = conf.get('cBindPointBullet', '')
                bullet_sfx_path = conf.get('cSfxBullet', '')
                anim_name = SHOOT_ACTION_LST[seat_index]
                model.register_anim_key_event(anim_name, 'start', self.sfx_callback, (seat_index, fire_socket, fire_sfx_path, bullet_socket, bullet_sfx_path))

            return

    def play_seat_fire_sfx(self, seat_name):
        seat_index = self.ev_g_seat_index_by_seat_name(seat_name)
        if seat_index < 0:
            print(('test--play_seat_fire_sfx--step1--seat_name =', seat_name, '--seat_index =', seat_index, '--unit_obj =', self.unit_obj))
            import traceback
            traceback.print_stack()
            return
        if not self.all_seat_info:
            print(('test--play_seat_fire_sfx--step2--seat_name =', seat_name, '--mecha_id =', self.sd.ref_mecha_id, '--all_seat_info =', self.all_seat_info, '--unit_obj =', self.unit_obj))
            import traceback
            traceback.print_stack()
            return
        guns = self.all_seat_info.get(seat_name, {}).get('guns', [])
        if not guns:
            return
        weapon_id = guns[0]
        conf = confmgr.get('firearm_res_config', str(weapon_id), default={})
        if not conf:
            return
        fire_sockets = conf.get('cBindPointEmission', [])
        fire_socket = ''
        if fire_sockets:
            fire_socket = fire_sockets[0]
        fire_sfx_path = conf.get('cSfx', '')
        bullet_socket = conf.get('cBindPointBullet', '')
        bullet_sfx_path = conf.get('cSfxBullet', '')
        fire_sfx_time = self._seat_fire_sfx_time.get(seat_index, 0)
        if time.time() - fire_sfx_time < FIRE_CD_TIME:
            return
        model = self.ev_g_model()
        if not model:
            return
        self._seat_fire_sfx_time[seat_index] = time.time()
        if fire_socket and fire_sfx_path:
            global_data.sfx_mgr.create_sfx_on_model(fire_sfx_path, model, fire_socket)
        if bullet_socket and bullet_sfx_path:
            global_data.sfx_mgr.create_sfx_on_model(bullet_sfx_path, model, bullet_socket)

    def sfx_callback(self, model, anim_name, key, data=None):
        seat_index, fire_socket, fire_sfx_path, bullet_socket, bullet_sfx_path = data
        fire_sfx_time = self._seat_fire_sfx_time.get(seat_index, 0)
        if time.time() - fire_sfx_time < FIRE_CD_TIME:
            return
        self._seat_fire_sfx_time[seat_index] = time.time()
        if fire_socket and fire_sfx_path:
            global_data.sfx_mgr.create_sfx_on_model(fire_sfx_path, model, fire_socket)
        if bullet_socket and bullet_sfx_path:
            global_data.sfx_mgr.create_sfx_on_model(bullet_sfx_path, model, bullet_socket)

    def play_drop_water_effect(self, position, vert_speed):
        now = time.time()
        if vert_speed < collision_const.COLLISION_VERT_SPEED_LIMIT and position:
            if now - self._last_collision_water_sfx_time > collision_const.COLLISION_WATER_SFX_INTERVAL:
                self._last_collision_water_sfx_time = now

                def create_cb(sfx):
                    scale = 5
                    sfx.scale = math3d.vector(scale, scale, scale)
                    global_data.sfx_mgr.set_rotation_by_normal(sfx, math3d.vector(0, 1, 0))

                global_data.sfx_mgr.create_sfx_in_scene(self.DROP_WATER_EFFECT, position, on_create_func=create_cb)

    def play_effect_by_status(self, status, is_sync=True):
        if status == self._cur_status:
            if global_data.debug_water_motorcycle:
                print(('test--play_effect_by_status--step1--status =', self.ev_g_get_state_desc(status), '--unit_obj =', self.unit_obj))
            return
        else:
            model = self.ev_g_model()
            if not model:
                if global_data.debug_water_motorcycle:
                    print(('test--play_effect_by_status--step2--model =', model, '--unit_obj =', self.unit_obj))
                return
            special_key = self.SPECIAL_STATUS_EFFECT_MAP.get(status, None)
            if special_key:
                last_material_index = self.ev_g_last_material()
                if global_data.debug_water_motorcycle:
                    print(('test--play_effect_by_status--step3--status =', self.ev_g_get_state_desc(status), '--special_key =', special_key, '--last_material_index =', last_material_index, '--unit_obj =', self.unit_obj))
                self.handle_special_effect(status, last_material_index)
            self._cur_status = status
            return

    def handle_special_effect(self, status=None, last_material_index=None):
        model = self.ev_g_model()
        if not model:
            if global_data.debug_water_motorcycle:
                print(('test--handle_special_effect--step1--model =', model, '--unit_obj =', self.unit_obj))
            return
        else:
            if status == None:
                status = self._cur_status if 1 else status
                if not status:
                    for one_status in six_ex.keys(self.SPECIAL_STATUS_EFFECT_MAP):
                        if self.ev_g_get_state(one_status):
                            status = one_status
                            break

                if status or global_data.debug_water_motorcycle:
                    print(('test--handle_special_effect--step2--status =', self.ev_g_get_state_desc(status), '--unit_obj =', self.unit_obj))
                return
            last_material_index = last_material_index if last_material_index in (scene_const.MTL_WATER, scene_const.MTL_DEEP_WATER) else 'default'
            old_last_material = self.ev_g_last_material()
            water_mtl_list = [scene_const.MTL_DEEP_WATER, scene_const.MTL_WATER]
            if self._cur_special_effect:
                if status == self._cur_special_effect[0] and last_material_index == self._cur_special_effect[1]:
                    if global_data.debug_water_motorcycle:
                        print(('test--handle_special_effect--step3--_cur_special_effect =', self._cur_special_effect, '--unit_obj =', self.unit_obj))
                    return
                socket_name, index = self._cur_special_effect[2]
                model.set_socket_bound_obj_active(socket_name, index, False)
                self._cur_special_effect = None
            special_key = self.SPECIAL_STATUS_EFFECT_MAP.get(status, None)
            if global_data.debug_water_motorcycle:
                print(('test--handle_special_effect--step4--status =', self.ev_g_get_state_desc(status), '--last_material_index =', last_material_index, '--self.SPECIAL_EFFECT_MAP.keys =', list(six_ex.keys(self.SPECIAL_EFFECT_MAP)), '--unit_obj =', self.unit_obj))
            if special_key and last_material_index in self.SPECIAL_EFFECT_MAP[special_key]:
                special_effect = self.SPECIAL_EFFECT_MAP[special_key][last_material_index]
                if global_data.debug_water_motorcycle:
                    print(('test--handle_special_effect--step5--special_key =', special_key, '--special_effect =', special_effect))
                if special_effect:
                    socket_name = special_effect[0]
                    index = special_effect[1]
                    model.set_socket_bound_obj_active(socket_name, index, True)
                    sfx_obj = model.get_socket_obj(socket_name, index)
                    if sfx_obj:
                        sfx_obj.restart()
                    self._cur_special_effect = [
                     status, last_material_index, special_effect]
            return

    def on_trigger_dash_effect(self, flag):
        effect_id = DASH_EFFECT_ID if flag else ''
        self.on_trigger_state_effect(DASH_STATE_ID, effect_id, force=True, need_sync=True)