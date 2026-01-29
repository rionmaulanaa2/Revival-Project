# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_appearance/ComEjection.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.cdata import status_config
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.timer import LOGIC, CLOCK
import math3d
import world
import collision
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE
from logic.gcommon.common_const.attr_const import HUMAN_ATTR_EJECT_HEIGHT_FACTOR, HUMAN_ATTR_EJECT_SPEED_FACTOR
from logic.gcommon.common_const.battle_const import DEFAULT_EJECT_SPEED, DEFAULT_EJECT_ACC, DEFAULT_EJECT_TIME, DEFAULT_EJECT_GRAVITY
from logic.gcommon.common_utils.parachute_utils import EJECT_STATE_ACC, EJECT_STATE_BREAK, EJECT_STATE_FINISH, EJECT_STATE_HIT

class ComEjection(UnitCom):
    BIND_EVENT = {'E_EJECT': 'on_eject',
       'E_SHOW_TAIL': 'on_show_tail_effect',
       'E_INSERT_TAIL': 'on_insert_tail',
       'E_LEAVE_STATE': 'on_leave_states',
       'E_CHRACTER_INITED': 'on_character_inited',
       'E_DEFEATED': 'on_death',
       'E_DEATH': 'on_death'
       }

    def __init__(self):
        super(ComEjection, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComEjection, self).init_from_dict(unit_obj, bdict)
        self.character = None
        self.cur_speed = 0
        self.acc_height = 0
        self.elapsed_time = None
        self._smoke_scale = 1.5
        self._timer_id = None
        self.init_eject_param()
        return

    def on_character_inited(self, character):
        self.character = character

    def init_eject_param(self):
        self.eject_speed = DEFAULT_EJECT_SPEED
        data = global_data.game_mode.get_cfg_data('play_data')
        if data:
            self.eject_speed = data.get('kill_mecha_out_speed', 0) * NEOX_UNIT_SCALE
        self.eject_time = DEFAULT_EJECT_TIME
        self.eject_acc = DEFAULT_EJECT_ACC
        self.eject_gravity = DEFAULT_EJECT_GRAVITY

    def on_load_animator_complete(self, *args):
        animator = self.ev_g_animator()
        if not animator:
            return

    def destroy(self):
        super(ComEjection, self).destroy()
        self.character = None
        self.stop_timer()
        return

    def on_leave_states(self, leave_state, new_state=None):
        if not global_data.player or not self.unit_obj or global_data.player.id != self.unit_obj.id:
            return
        if leave_state == status_config.ST_MECH_EJECTION:
            self.ev_g_cancel_state(status_config.ST_MECH_EJECTION, sync=True)

    def on_eject(self):

        def eject_imp(*args):
            if not self.is_valid():
                return
            else:
                self.send_event('E_DISABLE_MOVE', False)
                self.ev_g_status_try_trans(status_config.ST_MECH_EJECTION, sync=True)
                self.cur_speed = self.ev_g_addition_effect(self.eject_speed, factor_attrs=[HUMAN_ATTR_EJECT_HEIGHT_FACTOR, HUMAN_ATTR_EJECT_SPEED_FACTOR])
                self.acc_height = self.ev_g_position().y + self.cur_speed * self.eject_time
                self.elapsed_time = None
                self.need_update = True
                self.send_event('E_ACTIVE_STATE', status_config.ST_JUMP_1)
                self.send_event('E_SHOW_TAIL', True)
                return

        global_data.game_mgr.next_exec(eject_imp)

    def stop_timer(self):
        if self._timer_id:
            global_data.game_mgr.unregister_logic_timer(self._timer_id)
            self._timer_id = None
        return

    def on_show_tail_effect(self, show):
        self._smoke_scale = 1.5
        if show:

            def cb(*args):
                if not self or not self.is_valid():
                    return
                self._smoke_scale -= 0.03
                if self._smoke_scale <= 0.6:
                    self._smoke_scale = 0.6
                pos = self.ev_g_position()
                if not pos:
                    return
                self.on_insert_tail(pos.x, pos.y, pos.z, self._smoke_scale)

            self.stop_timer()
            self._timer_id = global_data.game_mgr.register_logic_timer(cb, interval=1, times=-1, mode=LOGIC)
        else:
            self.stop_timer()

    def tick(self, delta):
        character = self.character
        if not character or not character.valid or not character.isActive():
            self.need_update = False
            self.stop_timer()
            return
        else:
            if self.elapsed_time is None:
                self.elapsed_time = 0
            else:
                self.elapsed_time += max(delta, 0.01)
            pos = self.ev_g_position()
            height = pos.y if pos else None
            if self.elapsed_time < self.eject_time and pos and pos.y + delta * self.cur_speed < self.acc_height:
                state = EJECT_STATE_ACC
                self.send_event('E_VERTICAL_SPEED', self.cur_speed)
                self.send_event('E_GRAVITY', 1)
                start_pos = self.ev_g_position() + math3d.vector(0, NEOX_UNIT_SCALE, 0)
                end_pos = self.ev_g_position() + math3d.vector(0, 8 * NEOX_UNIT_SCALE, 0)
                result = self.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER)
                if result and result[0]:
                    state = EJECT_STATE_HIT
                    self.elapsed_time = self.eject_time
                    self.send_event('E_VERTICAL_SPEED', self.cur_speed)
            elif self.cur_speed > NEOX_UNIT_SCALE:
                state = EJECT_STATE_BREAK
                self.cur_speed = max(self.cur_speed - delta * self.eject_gravity, NEOX_UNIT_SCALE - 1)
                self.send_event('E_VERTICAL_SPEED', self.cur_speed)
            else:
                state = EJECT_STATE_FINISH
                self.need_update = False
                self.send_event('E_VERTICAL_SPEED', self.cur_speed)
                self.send_event('E_OPEN_PARACHUTE')
                self.send_event('E_AFTER_EJECT_PARACHUTE')
                self.send_event('E_SHOW_TAIL', False)
                self.send_event('E_RESET_GRAVITY')
                self.ev_g_cancel_state(status_config.ST_MECH_EJECTION)
            self.send_event('E_CALL_SYNC_METHOD', 'eject_state', (state, self.elapsed_time, height))
            return

    def on_death(self, *args, **kwargs):
        self.send_event('E_SHOW_TAIL', False)
        if self.character:
            self.character.verticalVelocity = 0

    def on_insert_tail(self, x, y, z, scale):

        def create_cb(sfx):
            sfx.scale = math3d.vector(scale, scale, scale)

        sfx_path = 'effect/fx/renwu/jump_tuowei.sfx'
        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, math3d.vector(x, y, z), duration=3.5, on_create_func=create_cb)