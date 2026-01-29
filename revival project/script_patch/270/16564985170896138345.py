# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mechatran_appearance/ComMechaTransEffect.py
from __future__ import absolute_import
import weakref
from ...UnitCom import UnitCom
from logic.gcommon.common_const import vehicle_const, mecha_const, scene_const, collision_const
import world
import common.utils.timer as timer
import logic.gcommon.common_utils.bcast_utils as bcast
import math3d
import time

class ComMechaTransEffect(UnitCom):
    EFFECT_MAP = {vehicle_const.MOVE_FORWARD_ACC: [
                                      'fx_penqi_1', 'fx_penqi_2', 'fx_penqi_3', 'fx_penqi_4', 'fx_penqi_zhong'],
       vehicle_const.MOVE_CHONGCI: [
                                  'fx_penqi_1', 'fx_penqi_2', 'fx_penqi_3', 'fx_penqi_4', 'fx_penqi_chongci'],
       vehicle_const.MOVE_STOP: [],vehicle_const.MOVE_JIJIA: []}
    SPECIAL_EFFECT_MAP = {'xingshi': {scene_const.MTL_WATER: ('level_point', 0),scene_const.MTL_DEEP_WATER: ('level_point', 0),'default': ('fx_xingshi', 0)},'shuimian_stop': {scene_const.MTL_WATER: ('level_point', 1),scene_const.MTL_DEEP_WATER: ('level_point', 1),'default': None},'jijia': {}}
    SPECIAL_STATUS_EFFECT_MAP = {vehicle_const.MOVE_FORWARD_ACC: 'xingshi',
       vehicle_const.MOVE_CHONGCI: 'xingshi',
       vehicle_const.MOVE_STOP: 'shuimian_stop',
       vehicle_const.MOVE_JIJIA: 'jijia'
       }
    CHONGCI_EFFECT = 'effect/fx/robot/autobot/autobot_yanwu.sfx'
    AVATAR_CHONGCI_EFFECT = 'effect/fx/robot/autobot/autobot_pinmujiasu.sfx'
    DROP_WATER_EFFECT = 'effect/fx/robot/autobot/chushui.sfx'
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_PLAY_EFFECT_BY_STATUS': 'play_effect_by_status',
       'E_PATTERN_HANDLE': 'update_pattern',
       'E_HEALTH_HP_CHANGE': 'on_health_change',
       'E_HEALTH_INIT': 'on_health_change',
       'E_CHONGCI': 'on_chongci',
       'E_CHONGCI_SYNC': 'on_chongci',
       'E_PLAY_CHONGCI_EFFECT': 'play_chongci_effect',
       'E_CONTROL_MECHA_TWO': 'on_control',
       'E_LAST_MATERIAL_CHANGE': 'handle_special_effect',
       'E_DEATH': 'on_die',
       'E_PLAY_DROP_WATER': 'play_drop_water_effect'
       }

    def __init__(self):
        super(ComMechaTransEffect, self).__init__()
        self._model_ref = None
        self._cur_status = None
        self.is_chongci = False
        self.chongci_effect_id = None
        self._cur_special_effect = None
        self._last_collision_water_sfx_time = 0
        self._pattern = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaTransEffect, self).init_from_dict(unit_obj, bdict)

    def on_model_loaded(self, model):
        self._model_ref = weakref.ref(model)
        self.on_health_change()

    def update_pattern(self, pattern, bdict=None, force_update=False):
        self._pattern = pattern
        if pattern == mecha_const.MECHA_TYPE_NORMAL:
            self.play_effect_by_status(vehicle_const.MOVE_JIJIA)

    def on_health_change(self, *args):
        if not self._model_ref:
            model = None if 1 else self._model_ref()
            return model or None
        else:
            percent = self.ev_g_health_percent() * 100
            if percent < 30:
                model.set_socket_bound_obj_active('fx_buff', 0, True)
            else:
                model.set_socket_bound_obj_active('fx_buff', 0, False)
            return

    def on_die(self, *args):
        model = self._model_ref() if self._model_ref else None
        if model and model.valid:
            sfx_path = 'effect/fx/scenes/common/break/fengxiang_02.sfx'
            global_data.sfx_mgr.create_sfx_in_scene(sfx_path, model.position)
        return

    def play_effect_by_status(self, status, is_sync=True):
        mecha_pattern = self._pattern
        if mecha_pattern == mecha_const.MECHA_PATTERN_NORMAL:
            status = vehicle_const.MOVE_JIJIA
        if status == vehicle_const.MOVE_FORWARD_ACC:
            if self.is_chongci:
                status = vehicle_const.MOVE_CHONGCI
            else:
                status = vehicle_const.MOVE_FORWARD_ACC
        if status == self._cur_status:
            return
        else:
            self.send_event('E_CHONGCI_SOUND', status == vehicle_const.MOVE_CHONGCI)
            if not self._model_ref:
                model = None if 1 else self._model_ref()
                global_data.model = model
                return model or None
            cur_status = self._cur_status or vehicle_const.MOVE_STOP if 1 else self._cur_status
            old_effect_list = self.EFFECT_MAP[cur_status]
            new_effect_list = self.EFFECT_MAP[status]
            for ename in old_effect_list:
                if ename not in new_effect_list:
                    effect = model.get_socket_obj(ename, 0)
                    if effect:
                        effect.shutdown(True)

            for ename in new_effect_list:
                effect = model.get_socket_obj(ename, 0)
                if effect:
                    effect.restart()
                else:
                    global_data.game_mgr.register_logic_timer(self.reset_sfx, interval=0.5, times=1, mode=timer.CLOCK)
                    break

            special_key = self.SPECIAL_STATUS_EFFECT_MAP.get(status, None)
            if special_key:
                last_material_index = self.ev_g_last_material()
                self.handle_special_effect(status, last_material_index)
            self._cur_status = status
            if global_data.player and self.sd.ref_driver_id == global_data.player.id:
                self.play_avatar_effect()
            if is_sync:
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_PLAY_EFFECT_BY_STATUS, (status,)], False)
            return

    def handle_special_effect(self, status=None, last_material_index=None):
        mecha_pattern = self._pattern
        if mecha_pattern == mecha_const.MECHA_PATTERN_NORMAL:
            status = vehicle_const.MOVE_JIJIA
        model = self._model_ref() if self._model_ref else None
        if not model or not model.valid:
            return
        else:
            if status == None:
                status = self._cur_status if 1 else status
                if not status:
                    return
                last_material_index = last_material_index if last_material_index in (scene_const.MTL_WATER, scene_const.MTL_DEEP_WATER) else 'default'
                old_last_material = self.ev_g_last_material()
                water_mtl_list = [scene_const.MTL_DEEP_WATER, scene_const.MTL_WATER]
                if last_material_index in water_mtl_list and old_last_material not in water_mtl_list and mecha_pattern == mecha_const.MECHA_PATTERN_VEHICLE:
                    vehicle = self.ev_g_vehicle()
                    vert_speed = 0
                    point = None
                    if vehicle:
                        vert_speed = vehicle.speed.y
                        point = vehicle.get_wheel_contact_point(0)
                    self.play_drop_water_effect(point, vert_speed)
            if self._cur_special_effect:
                if status == self._cur_special_effect[0] and last_material_index == self._cur_special_effect[1]:
                    return
                socket_name, index = self._cur_special_effect[2]
                model.set_socket_bound_obj_active(socket_name, index, False)
                self._cur_special_effect = None
            special_key = self.SPECIAL_STATUS_EFFECT_MAP[status]
            if last_material_index in self.SPECIAL_EFFECT_MAP[special_key]:
                special_effect = self.SPECIAL_EFFECT_MAP[special_key][last_material_index]
                if special_effect:
                    model.set_socket_bound_obj_active(special_effect[0], special_effect[1], True)
                    self._cur_special_effect = [status, last_material_index, special_effect]
            return

    def reset_sfx(self):
        model = self._model_ref() if self._model_ref else None
        if not model or not model.valid:
            return
        else:
            cur_status = self._cur_status if self._cur_status else vehicle_const.MOVE_STOP
            cur_effect_list = self.EFFECT_MAP[cur_status]
            for ename in cur_effect_list:
                effect = model.get_socket_obj(ename, 0)
                if effect:
                    effect.restart()
                else:
                    global_data.game_mgr.register_logic_timer(self.reset_sfx, interval=0.1, times=1, mode=timer.CLOCK)
                    break

            return

    def play_drop_water_effect(self, point, vert_speed):
        now = time.time()
        if vert_speed < collision_const.COLLISION_VERT_SPEED_LIMIT and point:
            if now - self._last_collision_water_sfx_time > collision_const.COLLISION_WATER_SFX_INTERVAL:
                self._last_collision_water_sfx_time = now

                def create_cb(sfx):
                    sfx.scale = math3d.vector(5, 5, 5)
                    global_data.sfx_mgr.set_rotation_by_normal(sfx, math3d.vector(0, 1, 0))

                global_data.sfx_mgr.create_sfx_in_scene(ComMechaTransEffect.DROP_WATER_EFFECT, point, on_create_func=create_cb)

    def play_avatar_effect(self):
        import math3d
        if self._cur_status == vehicle_const.MOVE_CHONGCI and self.is_chongci:
            global_data.emgr.show_screen_effect.emit('MechaChongCiEffect', {'position': math3d.vector(0, 0, 100)})
        else:
            global_data.emgr.destroy_screen_effect.emit('MechaChongCiEffect')

    def on_control(self, is_control, *args):
        if not is_control:
            global_data.emgr.destroy_screen_effect.emit('MechaChongCiEffect')

    def on_chongci(self, is_chongci):
        if is_chongci != self.is_chongci:
            self.is_chongci = is_chongci
            if self._cur_status != vehicle_const.MOVE_STOP and self._cur_status != vehicle_const.MOVE_JIJIA:
                self.play_effect_by_status(vehicle_const.MOVE_FORWARD_ACC, is_sync=False)
            if self.is_chongci:
                self.play_chongci_effect()
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CHONGCI_SYNC, (is_chongci,)], False)

    def play_chongci_effect(self):
        model = self._model_ref() if self._model_ref else None
        if model:
            socket_matrix = model.get_socket_matrix('fx_penqi_zhong', world.SPACE_TYPE_WORLD)
            if socket_matrix:
                pos = socket_matrix.translation
                rot_mat = socket_matrix.rotation

                def create_cb(sfx):
                    global_data.sfx_mgr.set_rotation(sfx, rot_mat)

                self.chongci_effect_id = global_data.sfx_mgr.create_sfx_in_scene(self.CHONGCI_EFFECT, pos, on_create_func=create_cb)
        return

    def destroy(self):
        if self.chongci_effect_id is not None:
            global_data.sfx_mgr.remove_sfx_by_id(self.chongci_effect_id)
        self._model_ref = None
        self.is_chongci = False
        self._cur_status = None
        self._cur_special_effect = None
        super(ComMechaTransEffect, self).destroy()
        return