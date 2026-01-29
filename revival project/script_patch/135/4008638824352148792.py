# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/GulagPoisonCircleManager.py
from __future__ import absolute_import
import six
import world
import math3d
import game3d
from math import pi
from common.cfg import confmgr
from .PoisonCircleManager import PoisonCircleManager, CIRCLE_HIDE_DISTANCE, CIRCLE_SCALE, CIRCLE_MAX_VISIBLE_DISTANCE, _HASH_player_pos, _HASH_poison_radius, _HASH_poison_scale, _HASH_visible_distance
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon import time_utility
from common.utilities import vector_radian
from logic.gcommon.common_const.battle_const import REVIVE_NONE, REVIVE_WAIT, ST_IDLE, ST_IN_QUEUE, ST_IN_GAME
from logic.gcommon.common_const.poison_circle_const import POISON_CIRCLE_STATE_REDUCE

class GulagPoisonCircleManager(PoisonCircleManager):

    def __init__(self):
        super(GulagPoisonCircleManager, self).__init__()
        self.main_circle_need_update = False
        self.revive_circle_need_update = set()
        self.revive_game_circle_info = {}
        self.revive_game_id = REVIVE_NONE

    def get_cnt_circle_info(self):
        if not global_data.cam_lplayer:
            return {}
        player_status = global_data.cam_lplayer.ev_g_gulag_status()
        if player_status == ST_IDLE:
            return super(GulagPoisonCircleManager, self).get_cnt_circle_info()
        if player_status == ST_IN_QUEUE:
            return {}
        revive_game_id = global_data.cam_lplayer.ev_g_gulag_game_id()
        if revive_game_id not in self.revive_game_circle_info:
            return {}
        keys = [
         'level', 'harm_center', 'harm_radius', 'safe_center', 'safe_radius', 'start_time', 'last_time',
         'state', 'original_radius', 'original_center', 'reduce_type']
        ret = {}
        for k in keys:
            if k not in self.revive_game_circle_info[revive_game_id]:
                return {}
            ret[k] = self.revive_game_circle_info[revive_game_id][k]

        ret['is_inside'] = self.is_inside()

    def register_event(self, bind=True):
        super(GulagPoisonCircleManager, self).register_event(bind)
        func = global_data.emgr.bind_events if bind else global_data.emgr.unbind_events
        func({'refresh_gulag_poison_circle': self.start_gulag_circle_callback,
           'reduce_gulag_poison_circle': self.update_gulag_circle_callback,
           'cam_lplayer_gulag_state_changed': self.on_cam_lplayer_gulag_state_changed,
           'net_login_reconnect_event': self.on_login_reconnect,
           'net_reconnect_event': self.on_login_reconnect
           })

    def on_login_reconnect(self, *args):
        if self._circle_timer:
            global_data.game_mgr.unregister_logic_timer(self._circle_timer)
            self._circle_timer = None
        return

    def on_cam_lplayer_gulag_state_changed(self, game_id, **kwargs):
        self.revive_game_id = game_id
        player_pos = self.get_player_pos()
        self.refresh_circle(player_pos)
        for game_id, cinfo in six.iteritems(self.revive_game_circle_info):
            self.refresh_gulag_circle(player_pos, game_id)

        self.check_circle_timer_valid()

    def on_revive_game_settle(self, notify_detail):
        parachute_timestamp = notify_detail.get('parachute_timestamp', None)
        if not parachute_timestamp:
            return
        else:
            return

    def is_in_poison(self):
        if not global_data.cam_lplayer or not global_data.cam_lplayer.is_valid():
            return True
        else:
            player_status = global_data.cam_lplayer.ev_g_gulag_status()
            if player_status == ST_IDLE:
                return super(GulagPoisonCircleManager, self).is_in_poison()
            if player_status == ST_IN_QUEUE:
                return True
            pos = global_data.cam_lplayer.ev_g_position()
            if pos is None:
                return
            revive_game_id = global_data.cam_lplayer.ev_g_gulag_game_id()
            if revive_game_id not in self.revive_game_circle_info:
                return True
            circle_pos = self.revive_game_circle_info[revive_game_id].get('cur_circle_pos', None)
            circle_r = self.revive_game_circle_info[revive_game_id].get('cur_circle_r', None)
            if circle_pos is None or circle_r is None:
                return True
            return (pos.x - circle_pos.x) ** 2 + (pos.z - circle_pos.z) ** 2 < circle_r ** 2
            return

    def start_gulag_circle_callback(self, game_id, circle_info):
        if not circle_info:
            return
        else:
            if game_id in self.revive_game_circle_info:
                _circle_info = self.revive_game_circle_info[game_id]
            else:
                self.revive_game_circle_info[game_id] = _circle_info = {}
                _circle_info['model'] = world.model(confmgr.get('script_gim_ref')['screen_effect_poison'], self._scene)
                _circle_info['model'].all_materials.set_var(_HASH_visible_distance, 'visible_distance', CIRCLE_MAX_VISIBLE_DISTANCE)
                _circle_info['model'].all_materials.set_var(_HASH_poison_scale, 'poison_scale', CIRCLE_SCALE)
            _circle_info['state'] = circle_info['state']
            _circle_info['start_time'] = circle_info['refresh_time']
            _circle_info['last_time'] = circle_info['last_time']
            _circle_info['level'] = circle_info['level']
            _circle_info['reduce_type'] = circle_info['reduce_type']
            _circle_info['poison_to_player_vector'] = None
            _circle_info['poison_close_radius'] = _circle_info['model'].bounding_box.x / pi
            _circle_info['original_pos'] = _circle_info['cur_circle_pos'] = math3d.vector(circle_info['poison_point'][0], -40.0 * NEOX_UNIT_SCALE, circle_info['poison_point'][1])
            _circle_info['original_r'] = _circle_info['cur_circle_r'] = circle_info['poison_point'][2]
            _circle_info['target_pos'] = math3d.vector(circle_info['safe_point'][0], -40.0 * NEOX_UNIT_SCALE, circle_info['safe_point'][1])
            _circle_info['target_r'] = circle_info['safe_point'][2]
            self.refresh_gulag_circle(self.get_player_pos(), game_id)
            self._poison_damage_view.start_check()
            if circle_info['state'] == POISON_CIRCLE_STATE_REDUCE:
                self.start_circle_timer(True, game_id)
            return

    def update_gulag_circle_callback(self, game_id, circle_info):
        if game_id not in self.revive_game_circle_info:
            self.start_gulag_circle_callback(game_id, circle_info)
        else:
            self.revive_game_circle_info[game_id]['state'] = circle_info['state']
            self.revive_game_circle_info[game_id]['reduce_type'] = circle_info['reduce_type']
            self.revive_game_circle_info[game_id]['start_time'] = circle_info['refresh_time']
            self.revive_game_circle_info[game_id]['last_time'] = circle_info['last_time']
        self.revive_game_circle_info[game_id]['cur_time'] = time_utility.time() - circle_info['refresh_time']
        self.start_circle_timer(True, game_id)

    def update_circle(self, start_time, last_time):
        if not self._circle:
            return
        self._start_time = start_time
        self._cur_time = time_utility.time() - self._start_time
        self._last_time = last_time
        self.start_circle_timer()

    def start_circle_timer(self, start=True, game_id=REVIVE_NONE):
        if game_id == REVIVE_NONE:
            self.main_circle_need_update = start
        elif start:
            self.revive_circle_need_update.add(game_id)
        elif game_id in self.revive_circle_need_update:
            self.revive_circle_need_update.remove(game_id)
        self.check_circle_timer_valid()

    def check_circle_timer_valid(self):
        if self.revive_game_id == REVIVE_NONE:
            need_timer = self.main_circle_need_update
        else:
            need_timer = bool(self.revive_circle_need_update)
        if need_timer and not self._circle_timer:
            self._circle_timer = global_data.game_mgr.register_logic_timer(self._circle_timer_callback, interval=1, times=-1)
        elif not need_timer and self._circle_timer:
            global_data.game_mgr.unregister_logic_timer(self._circle_timer)
            self._circle_timer = None
        return

    def _circle_timer_callback(self):
        if self.revive_game_id == REVIVE_NONE:
            super(GulagPoisonCircleManager, self)._circle_timer_callback()
        else:
            player_pos = self.get_player_pos()
            for game_id, cinfo in six.iteritems(self.revive_game_circle_info):
                if cinfo['state'] < POISON_CIRCLE_STATE_REDUCE:
                    self.refresh_gulag_circle(player_pos, game_id)
                    continue
                cinfo['cur_time'] = time_utility.time() - cinfo['start_time']
                if cinfo['cur_time'] >= cinfo['last_time']:
                    self.start_circle_timer(False, game_id)
                    cinfo['cur_time'] = cinfo['last_time']
                rate = cinfo['cur_time'] / cinfo['last_time'] if cinfo['last_time'] > 0 else 1
                rate = min(1.0, max(0.0, rate))
                cinfo['cur_circle_pos'] = cinfo['original_pos'] + (cinfo['target_pos'] - cinfo['original_pos']) * rate
                cinfo['cur_circle_r'] = cinfo['original_r'] + (cinfo['target_r'] - cinfo['original_r']) * rate
                self.refresh_gulag_circle(player_pos, game_id)
                if game_id == self.revive_game_id and self._scene.valid:
                    self._scene.set_poison_info(cinfo['cur_circle_pos'].x, cinfo['cur_circle_pos'].y, cinfo['cur_circle_pos'].z, cinfo['cur_circle_r'])

    def start_circle(self, start_pos, start_r, target_pos, target_r):
        if not self._circle:
            screen_posion_model_path = confmgr.get('script_gim_ref')['screen_effect_poison']
            self._circle = world.model(screen_posion_model_path, self._scene)
            self._circle.all_materials.set_var(_HASH_visible_distance, 'visible_distance', CIRCLE_MAX_VISIBLE_DISTANCE)
            self._circle.all_materials.set_var(_HASH_poison_scale, 'poison_scale', CIRCLE_SCALE)
            self._poison_close_radius = self._circle.bounding_box.x / 3.1415926
            self._cur_circle_pos = start_pos + math3d.vector(0, -40 * NEOX_UNIT_SCALE, 0)
            self._cur_circle_r = start_r
            self._poison_damage_view.start_check()
        self._original_pos = start_pos + math3d.vector(0, -40 * NEOX_UNIT_SCALE, 0)
        self._original_r = start_r
        self._target_pos = target_pos + math3d.vector(0, -40 * NEOX_UNIT_SCALE, 0)
        self._target_r = target_r
        player_pos = self.get_player_pos()
        self.refresh_circle(player_pos)

    def refresh_circle(self, player_pos):
        if not self._circle or not self._circle.valid:
            return
        if self.revive_game_id == REVIVE_NONE:
            super(GulagPoisonCircleManager, self).refresh_circle(player_pos)
        else:
            self._circle.visible = False

    def refresh_gulag_circle(self, player_pos, game_id):
        if game_id not in self.revive_game_circle_info:
            return
        else:
            circle_info = self.revive_game_circle_info[game_id]
            circle_model = circle_info.get('model')
            if not circle_model or not circle_model.valid:
                return
            circle_vect = player_pos - circle_info['cur_circle_pos']
            circle_vect.y = 0.0
            if self.revive_game_id == REVIVE_NONE or self.revive_game_id != REVIVE_WAIT and self.revive_game_id != game_id or circle_info['state'] < POISON_CIRCLE_STATE_REDUCE or abs(circle_vect.length - circle_info['cur_circle_r']) > CIRCLE_HIDE_DISTANCE:
                circle_model.visible = False
                circle_info['poison_to_player_vector'] = None
                return
            circle_model.visible = True
            if not circle_info['poison_to_player_vector'] or circle_info['cur_circle_r'] > circle_info['poison_close_radius']:
                circle_radian = vector_radian(circle_vect) + pi
                circle_model.rotation_matrix = math3d.matrix.make_rotation_y(circle_radian)
                if not circle_vect.is_zero:
                    circle_vect.normalize()
                else:
                    circle_vect = math3d.vector(0, 0, 1)
                circle_info['poison_to_player_vector'] = circle_vect
            else:
                circle_vect = circle_info['poison_to_player_vector']
            circle_pos = circle_info['cur_circle_pos'] + circle_vect * circle_info['cur_circle_r']
            circle_model.position = circle_pos
            circle_model.all_materials.set_var(_HASH_player_pos, 'player_pos', (player_pos.x, player_pos.y, player_pos.z))
            circle_model.all_materials.set_var(_HASH_poison_radius, 'poison_radius', circle_info['cur_circle_r'])
            if circle_info['cur_circle_r'] < 100 * NEOX_UNIT_SCALE:
                scale = circle_info['cur_circle_r'] * CIRCLE_SCALE / (100 * NEOX_UNIT_SCALE)
                circle_model.all_materials.set_var(_HASH_poison_scale, 'poison_scale', scale)
            return

    def destroy(self):
        super(GulagPoisonCircleManager, self).destroy()
        self.register_event(False)
        for circle_info in six.itervalues(self.revive_game_circle_info):
            circle_model = circle_info.get('model')
            if circle_model and circle_model.valid:
                circle_model.destroy()

        self.revive_game_circle_info = None
        if self._circle_timer:
            global_data.game_mgr.unregister_logic_timer(self._circle_timer)
            self._circle_timer = None
        return