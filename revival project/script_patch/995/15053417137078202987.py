# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaAimSpreadMgr.py
from __future__ import absolute_import
from logic.client.const.camera_const import THIRD_PERSON_MODEL, POSTURE_STAND
import logic.gcommon.const as g_const
from common.utils.timer import RELEASE
from common.cfg import confmgr
import cc
import math
SPREAD_BY_SIZE = 1
SPREAD_BY_SCALE = 2
INTERPOLATION_DURATION = 0.1

class MechaAimSpreadMgr(object):
    AUTO_AIM_SIZE = 60.0
    AIM_SIZE = 20.0

    def __init__(self, parent, spread_type=SPREAD_BY_SCALE):
        self.spread_type = spread_type
        self.panel = parent
        self.init_parameters()
        from logic.comsys.battle.AimColorWidget import AimColorWidget
        self._aimColorWidget = AimColorWidget(self, self.panel)
        self._aimColorWidget.set_top_color_exclude_list([self.panel.nd_bullet_ob])
        self._aimColorWidget.calculate_aim_node()

    def init_parameters(self):
        self.mecha = None
        width, height = self.panel.GetContentSize()
        x_fov = confmgr.get('camera_config', THIRD_PERSON_MODEL, POSTURE_STAND, 'fov', default=80)
        d = width / 2.0 / math.tan(math.radians(x_fov / 2.0))
        cell = 30
        y_fov = math.atan(cell / 2.0 / d) * 180 / math.pi * 2.0
        self._scale_value = cell / y_fov
        self.weapon_pos = None
        self.weapons = {}
        self.weapons_delay_scale = {}
        self.cur_spread_value = None
        self.cur_spread_base = 0.0
        self.spread_timer = -1
        self.spread_recover_process_life = 0.0
        self.spread_intrp_process_life = 0.0
        self.spread_recover_speed = 0.0
        self.spread_intrp_speed = 0.0
        return

    def destroy(self):
        if self._aimColorWidget:
            self._aimColorWidget.destroy()
            self._aimColorWidget = None
        self.unbind_ui_event()
        self.get_aim_node = None
        self.panel = None
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event()
        if mecha:
            self.mecha = mecha
            self.set_weapon_pos(g_const.PART_WEAPON_POS_MAIN1)
            regist_func = mecha.regist_event
            regist_func('E_AIM_SPREAD', self._on_aim_spread)
            regist_func('E_STAND', self._on_spread, 1)
            regist_func('E_JUMP', self._on_spread, 1)
            regist_func('E_MECHA_ON_GROUND', self._on_spread, 1)
            regist_func('E_ACTION_MOVE', self._on_spread, 1)
            regist_func('E_ACTION_MOVE_STOP', self._on_spread, 1)
            regist_func('E_REFRESH_SPREAD_AIM_UI', self._on_spread, 1)
            regist_func('E_MECHA_AIM_SPREAD', self._on_mecha_aim_spread)
            regist_func('E_MECHA_SPREAD', self._on_mecha_spread)
            regist_func('E_MECHA_VEHICLE_SPREAD', self._on_spread, 1)
            self._on_spread()
            self._aimColorWidget.setup_color()

    def unbind_ui_event(self):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_AIM_SPREAD', self._on_aim_spread)
            unregist_func('E_STAND', self._on_spread)
            unregist_func('E_JUMP', self._on_spread)
            unregist_func('E_MECHA_ON_GROUND', self._on_spread)
            unregist_func('E_ACTION_MOVE', self._on_spread)
            unregist_func('E_ACTION_MOVE_STOP', self._on_spread)
            unregist_func('E_REFRESH_SPREAD_AIM_UI', self._on_spread)
            unregist_func('E_MECHA_AIM_SPREAD', self._on_mecha_aim_spread)
            unregist_func('E_MECHA_SPREAD', self._on_mecha_spread)
            unregist_func('E_MECHA_VEHICLE_SPREAD', self._on_spread)
        self.mecha = None
        self._release_spread_timer()
        self.weapons = {}
        return

    def get_aim_node(self):
        if self.panel.nd_aim and self.panel.nd_aim.isVisible():
            return self.panel.nd_spread
        if self.panel.nd_sub_aim and self.panel.nd_sub_aim.isVisible():
            return self.panel.nd_sub_spread

    def replace_get_aim_node_func(self, func):
        if func and callable(func):
            self.get_aim_node = func

    def set_weapon_pos(self, weapon_pos):
        self.weapon_pos = weapon_pos
        if weapon_pos not in self.weapons and self.mecha and self.mecha.is_valid():
            self.weapons[weapon_pos] = self.mecha.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
            scale = self.weapons[weapon_pos].get_data_by_key('fHIPDelayRecoverUIScale')
            self.weapons_delay_scale[weapon_pos] = scale if scale is not None else 1.0
        return

    def fix_spread_values(self, spread_base, spread_value):
        spread_min_reference = self.weapons[self.weapon_pos].get_data_by_key('fHIPMinReference')
        if spread_base < spread_min_reference:
            spread_base = spread_min_reference
        if spread_value < spread_min_reference:
            spread_value = spread_min_reference
        return (spread_base, spread_value)

    def _release_spread_timer(self):
        if self.spread_timer != -1:
            global_data.game_mgr.get_post_logic_timer().unregister(self.spread_timer)
            self.spread_timer = -1

    def _refresh_aim_node_appearance(self):
        aim_node = self.get_aim_node()
        if aim_node and aim_node.isVisible():
            if self.spread_type == SPREAD_BY_SIZE:
                size = self.cur_spread_value * self.AIM_SIZE
                aim_node.SetContentSize(size, size)
                aim_node.ResizeAndPosition(include_self=False)
            else:
                scale_value = self._scale_value * 2.0 / self.AUTO_AIM_SIZE
                aim_node.setScale(scale_value * self.cur_spread_value)

    def _update_spread_tick(self, dt):
        if self.spread_intrp_process_life > 0:
            if self.spread_intrp_process_life >= dt:
                self.spread_intrp_process_life -= dt
            else:
                dt = self.spread_intrp_process_life
                self.spread_intrp_process_life = 0.0
            self.cur_spread_value += self.spread_intrp_speed * dt
        if self.spread_recover_process_life > 0:
            self.spread_recover_speed = (self.cur_spread_value - self.cur_spread_base) / self.spread_recover_process_life
            if self.spread_recover_process_life >= dt:
                self.spread_recover_process_life -= dt
            else:
                dt = self.spread_recover_process_life
                self.spread_recover_process_life = 0.0
            if self.spread_recover_process_life <= INTERPOLATION_DURATION:
                if self.spread_recover_process_life + dt > INTERPOLATION_DURATION:
                    dt = INTERPOLATION_DURATION - self.spread_recover_process_life
                self.cur_spread_value -= self.spread_recover_speed * dt
        self._refresh_aim_node_appearance()
        if self.spread_intrp_process_life == 0.0 and self.spread_recover_process_life == 0.0:
            self.spread_timer = -1
            return RELEASE

    def get_aim_normal_color(self):
        return self._aimColorWidget.get_aim_normal_color()

    def _on_spread(self, *args):
        if self.mecha and self.mecha.is_valid():
            aim_node = self.get_aim_node()
            if not self.mecha or not aim_node or not aim_node.isVisible():
                return
            spread_values = self.mecha.ev_g_spread_values(weapon_pos=self.weapon_pos)
            if not spread_values:
                return
            spread_base, spread_value, recover_time = spread_values
            spread_base, spread_value = self.fix_spread_values(spread_base, spread_value)
            self.mecha.send_event('E_MECHA_SPREAD', spread_base, spread_value, recover_time)

    def _on_mecha_spread(self, spread_base, spread_value, recover_time, **kwargs):
        if self.spread_recover_process_life < INTERPOLATION_DURATION - 0.03:
            self._on_mecha_aim_spread(spread_base, spread_value, 0.0, recover_time, **kwargs)
        else:
            self.cur_spread_base = spread_base

    def _on_aim_spread(self, spread_base, spread_value, delay_time, recover_time, weapon_pos=None):
        if weapon_pos != self.weapon_pos:
            return
        if self.mecha and self.mecha.is_valid():
            delay_time *= self.weapons_delay_scale[self.weapon_pos]
            aim_node = self.get_aim_node()
            if not self.mecha or not aim_node or not aim_node.isVisible():
                return
            spread_values = self.mecha.ev_g_spread_values(weapon_pos=self.weapon_pos)
            if not spread_values:
                return
            spread_base, spread_value = self.fix_spread_values(spread_base, spread_value)
            self.mecha.send_event('E_MECHA_AIM_SPREAD', spread_base, spread_value, delay_time, recover_time)

    def _on_mecha_aim_spread(self, spread_base, spread_value, delay_time, recover_time, **kwargs):
        aim_node = self.get_aim_node()
        if not self.mecha or not aim_node or not aim_node.isVisible():
            return
        else:
            if spread_value < 0.01:
                return
            spread_increase = self.mecha.ev_g_spread_increase(self.weapons[self.weapon_pos], self.weapon_pos)
            self.cur_spread_base = spread_base
            self.spread_recover_process_life = delay_time + INTERPOLATION_DURATION
            if self.cur_spread_value is None or math.fabs(spread_value - self.cur_spread_value) < spread_increase * 2.0:
                self.cur_spread_value = spread_value
                self.spread_intrp_process_life = 0.0
                self.spread_intrp_speed = 0.0
                self._refresh_aim_node_appearance()
            else:
                self.spread_intrp_process_life = INTERPOLATION_DURATION
                self.spread_intrp_speed = (spread_value - self.cur_spread_value) / INTERPOLATION_DURATION
            if self.spread_timer == -1:
                self.spread_timer = global_data.game_mgr.get_post_logic_timer().register(func=self._update_spread_tick, interval=1, times=-1, timedelta=True)
            return


class MechaAimSpreadMgr2(MechaAimSpreadMgr):

    def _on_aim_spread(self, spread_base, spread_value, delay_time, recover_time, weapon_pos=None):
        if weapon_pos != self.weapon_pos:
            return
        if self.mecha and self.mecha.is_valid():
            delay_time *= self.weapons_delay_scale[self.weapon_pos]
            aim_node = self.get_aim_node()
            if not self.mecha or not aim_node or not aim_node.isVisible():
                return
            spread_base, spread_value = self.fix_spread_values(spread_base, spread_value)
            self.mecha.send_event('E_MECHA_AIM_SPREAD', spread_base, spread_value, delay_time, recover_time)