# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_charger/ComChargerAppearance.py
from __future__ import absolute_import
import six
import six_ex
from logic.gcommon.component.client.ComBaseModelAppearance import ComBaseModelAppearance
from mobile.common.EntityManager import EntityManager
import world
import math3d
from logic.gcommon.common_const import mecha_const
from data.c_guide_data import get_charge_rate
from logic.gutils.client_unit_tag_utils import preregistered_tags
from logic.gcommon.common_const.buff_const import BUFF_ID_MECHA_RECOVERY_BY_CHARGE
from logic.gcommon.common_const import buff_const as bconst

class ComChargerAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_UPDATE_CHARGER': '_update_charger',
       'E_LBS_CHARGER_CHECK': '_lbs_charger_check'
       })

    def __init__(self):
        super(ComChargerAppearance, self).__init__()
        self._mecha_buff_idx = 1
        self.charger_conf = None
        self._charging_target_infos = {}
        self._charging_target_infos_sfx = {}
        self._charging_screen_sfx = {}
        self._binding_target_set = set()
        self._charging_line_start_pos = None
        self._battery_sfx_ids = {}
        self._battery_progress_sfx_id = None
        self._battery_sfx_dict = {}
        self._switch_sfx_dict = {}
        self._switch_sfx_ids = []
        self._switch_sfx_show_key = None
        self._switch_timer_id = None
        self._progress_sfx = None
        self._is_local_charging = None
        return

    def init_from_dict(self, unit_obj, bdict):
        self._charger_id = bdict.get('npc_id', None)
        self._energy = bdict.get('energy', 0)
        is_charging, charger_state = bdict.get('state', (False, None))
        self._is_charging = is_charging
        self._charger_state = charger_state
        self._get_charger_conf()
        self._energy_cap = self.charger_conf['capacity']
        self._energy_colors = self.charger_conf['battery_colors']
        self._entity_ids = bdict.get('entity_ids', tuple())
        self._charge_rate = self.charger_conf.get('charge_rate', 2)
        self._cur_user_count = 0
        self._cur_energy_color = None
        self._cur_show_battle_sfx_idx = None
        super(ComChargerAppearance, self).init_from_dict(unit_obj, bdict)
        return

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rot = bdict.get('rot', [0, 0, 0, 1])
        model_path = self.charger_conf['model_path']
        return (
         model_path, None, (pos, rot, bdict))

    def _get_charger_conf(self):
        from common.cfg import confmgr
        if self.charger_conf:
            return self.charger_conf
        self.charger_conf = confmgr.get('charger_data', str(self._charger_id))
        return self.charger_conf

    def on_load_model_complete(self, model, userdata):
        import math3d
        import collision
        import render
        import game3d
        pos, rot = userdata[0], userdata[1]
        pos = math3d.vector(pos[0], pos[1], pos[2])
        mat = math3d.rotation_to_matrix(math3d.rotation(rot[0], rot[1], rot[2], rot[3]))
        model.world_position = pos
        model.rotation_matrix = mat
        model.active_collision = True
        self._charging_line_start_pos = model.get_socket_matrix('fx_lianjie', world.SPACE_TYPE_WORLD).translation
        self.select_battery_sfx(self._charger_state)
        global_data.game_mgr.post_exec(self.create_energy_sfx)
        global_data.game_mgr.post_exec(self.refresh)

    def refresh(self):
        self._update_charger((self._is_charging, self._charger_state), self._energy, self._entity_ids)
        self.select_battery_sfx(self._charger_state)

    def _lbs_charger_check(self):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        pos = self.ev_g_position()
        lplayer = global_data.player.logic
        avt_pos = lplayer.ev_g_position()
        if not (pos and avt_pos):
            return
        is_charging = False
        rate = 1
        if (pos - avt_pos).length < self.charger_conf['charge_range'] * NEOX_UNIT_SCALE:
            is_charging = True
            rate = get_charge_rate()
            lplayer.send_event('E_GUIDE_CHARGER')
            if not self._is_local_charging:
                self._is_local_charging = True
                from logic.comsys.guide_ui.GuideUI import GuideUI
                ui = GuideUI()
                ui.play_nd_animation('nd_step_13', 'show_13_charging')
        elif self._is_local_charging:
            self._is_local_charging = False
            from logic.comsys.guide_ui.GuideUI import GuideUI
            ui = GuideUI()
            ui.play_nd_animation_destroy('nd_step_13', 'show_13_charging')
        max_state = len(self.charger_conf['state_table']) - 1
        state = (is_charging, max_state)
        lplayer.send_event('S_MECHA_RECALL_CD_TYPE', mecha_const.RECALL_CD_TYPE_GETMECHA)
        self._update_charger(state, self.charger_conf['capacity'], [global_data.player.id])
        lplayer.send_event('S_CALL_MECHA_SPEED_RATE', rate)
        ui = global_data.ui_mgr.get_ui('MechaUI')
        if ui:
            progress = ui.panel.temp_mech_call.progress_mech_call.getPercentage()
            ui = global_data.ui_mgr.get_ui('MechaChargeUI')
            if ui:
                ui.sync_mecha_percent(progress)

    def _update_charger(self, state, energy, entity_ids):
        self._entity_ids = entity_ids
        self._energy = energy
        is_charging, energy_state = state
        self._is_charging = is_charging
        if energy_state != self._charger_state:
            self._charger_state = energy_state
            self.select_battery_sfx(self._charger_state)
        self.update_energy_show()
        self.update_charging_ids(entity_ids)
        if len(self._entity_ids) != self._cur_user_count:
            global_data.emgr.charger_user_count_changed.emit(self)
            self._cur_user_count = len(self._entity_ids)

    def update_charging_ids(self, entity_ids):
        if self._is_charging:
            valid_ids = []
            valid_control_ids = []
            for ent_id in entity_ids:
                ent = EntityManager.getentity(ent_id)
                if ent and ent.logic and self.check_entity_can_charging(ent.logic):
                    valid_ids.append(ent_id)
                    if not ent.logic.ev_g_in_mecha('Mecha'):
                        valid_control_ids.append(ent_id)
                    else:
                        valid_control_ids.append(ent.logic.ev_g_control_target().id)

            for ent_idx, ent_id in enumerate(valid_ids):
                if valid_control_ids[ent_idx] not in self._charging_target_infos:
                    ent = EntityManager.getentity(ent_id)
                    self.show_charging_sfx(ent.logic)

            cur_targets = six_ex.keys(self._charging_target_infos)
            for eid in cur_targets:
                if eid not in valid_control_ids:
                    self.destroy_charging_sfx(eid)

        else:
            cur_targets = six_ex.keys(self._charging_target_infos)
            for eid in cur_targets:
                self.destroy_charging_sfx(eid)

    def show_charging_sfx(self, lentity):
        if not lentity:
            return
        else:
            if not lentity.ev_g_in_mecha('Mecha'):
                lentity.send_event('E_ON_MECHA_CHARGING', True, None)
                ltarget = lentity
                sfx_key = 'human'
            else:
                target = lentity.ev_g_control_target()
                if target and target.logic:
                    ltarget = target.logic
                    if not ltarget.ev_g_has_buff_by_id(BUFF_ID_MECHA_RECOVERY_BY_CHARGE):
                        from logic.gcommon import time_utility
                        data = {'add_time': time_utility.get_server_time() - 1}
                        ltarget.send_event('E_BUFF_ADD_DATA', bconst.BUFF_GLOBAL_KEY, BUFF_ID_MECHA_RECOVERY_BY_CHARGE, self._mecha_buff_idx, data)
                else:
                    ltarget = lentity
                sfx_key = 'mecha'
            model = ltarget.ev_g_model()
            if not model:
                return
            charging_sfx = self.charger_conf['charging_sfx']
            if type(charging_sfx) == dict:
                charging_sfx = charging_sfx.get(sfx_key, '')
            if not charging_sfx:
                return
            if not self._charging_line_start_pos:
                return
            ltarget_id = ltarget.id

            def create_cb(sfx):
                model = ltarget.ev_g_model()
                if not model:
                    log_error("Charging sfx can't attached!")
                    return
                if model and model.valid:
                    if ltarget.MASK & preregistered_tags.HUMAN_TAG_VALUE:
                        socket_name = 'gliding'
                    elif ltarget.MASK & preregistered_tags.MECHA_TAG_VALUE:
                        socket_name = 'part_point0'
                    else:
                        socket_name = 'part_point1'
                    sfx.endpos_attach(model, socket_name, True)
                self._charging_target_infos_sfx[ltarget_id] = sfx

            _sfx_id = global_data.sfx_mgr.create_sfx_in_scene(charging_sfx, self._charging_line_start_pos, on_create_func=create_cb)
            self._charging_target_infos[ltarget_id] = _sfx_id
            if not lentity.ev_g_in_mecha('Mecha'):
                self.setup_control_target_event(lentity, is_bind=True)
            self.record_target_charing_state(ltarget, True)
            if not lentity.ev_g_is_cam_target():
                return
            screen_sfx = self.charger_conf['charging_screen_effect']
            if type(screen_sfx) == dict:
                screen_sfx = screen_sfx.get(sfx_key, '')
            if not screen_sfx:
                return
            import math3d
            size = global_data.really_sfx_window_size
            scale = math3d.vector(size[0] / 1280.0, size[1] / 720.0, 1.0)

            def create_screen_cb(sfx):
                sfx.scale = scale
                sfx.loop = True

            def remove_sfx_cb(sfx):
                sfx.loop = False

            _screen_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(screen_sfx, on_create_func=create_screen_cb, on_remove_func=remove_sfx_cb)
            self._charging_screen_sfx[ltarget_id] = _screen_sfx_id
            return

    def destroy_charging_sfx(self, target_id):
        if target_id in self._charging_target_infos_sfx:
            del self._charging_target_infos_sfx[target_id]
        if target_id in self._charging_target_infos:
            global_data.sfx_mgr.remove_sfx_by_id(self._charging_target_infos[target_id])
            del self._charging_target_infos[target_id]
        if target_id in self._charging_screen_sfx:
            global_data.sfx_mgr.remove_sfx_by_id(self._charging_screen_sfx[target_id])
            del self._charging_screen_sfx[target_id]
        ent = EntityManager.getentity(target_id)
        if ent and ent.logic:
            if ent.logic.MASK & preregistered_tags.HUMAN_TAG_VALUE == 0:
                ent.logic.send_event('E_BUFF_DEL_DATA', bconst.BUFF_GLOBAL_KEY, BUFF_ID_MECHA_RECOVERY_BY_CHARGE, self._mecha_buff_idx)
            if ent.logic.MASK & preregistered_tags.HUMAN_TAG_VALUE:
                ent.logic.send_event('E_ON_MECHA_CHARGING', False, None)
            self.setup_control_target_event(ent.logic, is_bind=False)
            self.record_target_charing_state(ent.logic, False)
        return

    def on_model_destroy(self):
        cur_targets = six_ex.keys(self._charging_target_infos)
        for eid in cur_targets:
            self.destroy_charging_sfx(eid)

        self._charging_target_infos = {}
        self._charging_target_infos_sfx = {}
        if self._binding_target_set:
            for eid in list(self._binding_target_set):
                ent = EntityManager.getentity(eid)
                if ent and ent.logic:
                    self.setup_control_target_event(ent.logic, False)

            self._binding_target_set = set()
        self.destroy_energy_sfx()
        self.destroy_switch_sfx()

    def update_energy_show(self):
        if self._energy is not None and self._progress_sfx:
            percent = self.get_energy_percent()
            self._progress_sfx.scale = math3d.vector(1, percent, 1)
        return

    def check_energy_color(self):
        if self._charger_state and self._charger_state < len(self._energy_colors):
            new_energy_color = self._energy_colors[self._charger_state]
            if self._cur_energy_color != new_energy_color:
                if self._progress_sfx:
                    self._progress_sfx.clear_frame()
                    for color_frame in new_energy_color:
                        percent, a, r, g, b = color_frame
                        color = a << 24 | r << 16 | g << 8 | b
                        self._progress_sfx.add_frame(percent, color)
                        self._cur_energy_color = new_energy_color

    def get_energy_percent(self):
        if self._energy is not None:
            return float(self._energy) / self._energy_cap
        else:
            return 0
            return

    def create_energy_sfx(self):
        battery_progress_sfx = self.charger_conf['battery_progress_sfx']

        def create_battery_progress_sfx_ids_cb(sfx):
            if self and self.is_valid():
                self._progress_sfx = sfx
                self.update_energy_show()
                self.check_energy_color()
            else:
                global_data.sfx_mgr.remove_sfx(sfx)

        self._battery_progress_sfx_id = global_data.sfx_mgr.create_sfx_on_model(battery_progress_sfx, self.model, 'fx_time', world.BIND_TYPE_TRANSLATE, on_create_func=create_battery_progress_sfx_ids_cb)

    def create_battery_sfx(self, state):
        if state in self._battery_sfx_dict and self._battery_sfx_dict[state]:
            return
        if state in self._battery_sfx_ids and self._battery_sfx_ids[state]:
            return
        battery_sfxes = self.charger_conf['battery_sfxes']
        for sfx_idx, battery_sfx in enumerate(battery_sfxes):
            if sfx_idx == state:
                same_sfx_idx_set = [ other_idx for other_idx, other_sfx_path in enumerate(battery_sfxes) if other_sfx_path == battery_sfx ]

                def create_battery_sfx_cb(sfx):
                    for idx in same_sfx_idx_set:
                        self._battery_sfx_dict[idx] = sfx

                    sfx.visible = False
                    if self._cur_show_battle_sfx_idx == state:
                        self._check_switch_sfx(state, self._switch_sfx_show_key)

                tid = global_data.sfx_mgr.create_sfx_on_model(battery_sfx, self.model, 'fx_root', world.BIND_TYPE_TRANSLATE, on_create_func=create_battery_sfx_cb)
                self._battery_sfx_ids[state] = tid

    def select_battery_sfx(self, state):
        if state not in self._battery_sfx_dict:
            if self._cur_show_battle_sfx_idx is not None:
                self._switch_sfx_show_key = str(self._cur_show_battle_sfx_idx) + '_' + str(state)
            self._cur_show_battle_sfx_idx = state
            self.create_battery_sfx(state)
            return
        else:
            if self._cur_show_battle_sfx_idx == state:
                return
            if self._battery_sfx_dict.get(self._cur_show_battle_sfx_idx) != self._battery_sfx_dict.get(state):
                if self._cur_show_battle_sfx_idx in self._battery_sfx_dict:
                    sfx = self._battery_sfx_dict[self._cur_show_battle_sfx_idx]
                    sfx.visible = False
                if self._cur_show_battle_sfx_idx is not None:
                    self._switch_sfx_show_key = str(self._cur_show_battle_sfx_idx) + '_' + str(state)
                if state in self._battery_sfx_dict:
                    self._check_switch_sfx(state, self._switch_sfx_show_key)
            self._cur_show_battle_sfx_idx = state
            return

    def show_battle_sfx(self, state):
        for _sfx in six_ex.values(self._battery_sfx_dict):
            _sfx.visible = False

        if state in self._battery_sfx_dict:
            _sfx2 = self._battery_sfx_dict[state]
            _sfx2.visible = True
            switch_start_time = self.charger_conf['switch_start_time'].get(self._switch_sfx_show_key, 0)
            if switch_start_time:
                _sfx2.set_curtime_directly(switch_start_time)
            else:
                _sfx2.restart()

    def _check_switch_sfx(self, state, show_key):
        if show_key == self._switch_sfx_show_key and self._switch_sfx_ids:
            return None
        else:
            if self._switch_sfx_ids:
                self.destroy_switch_sfx()
            has_switch_sfx = False
            if show_key:
                show_time, show_sfx_path = self.charger_conf['switch_sfxes'].get(show_key, (None,
                                                                                            None))
                if show_sfx_path:
                    has_switch_sfx = True

                    def callback(switch_sfx):
                        for _sfx in six_ex.values(self._battery_sfx_dict):
                            _sfx.visible = False

                        self._switch_sfx_dict[show_key] = switch_sfx
                        if self.model and self.model.valid:
                            switch_sfx.remove_from_parent()
                            self.model.bind('fx_root', switch_sfx, world.BIND_TYPE_TRANSLATE)
                            switch_sfx.position = math3d.vector(0, 0, 0)
                        if self._switch_sfx_show_key == show_key:
                            switch_sfx.visible = True
                            switch_sfx.restart()
                        if self._progress_sfx:
                            colors = self.charger_conf['switch_color_effect'].get(show_key, [])
                            if colors:
                                self.set_sfx_color(self._progress_sfx, colors)
                        else:
                            switch_sfx.visible = False
                        self.destroy_switch_timer()
                        from common.utils.timer import CLOCK
                        self._switch_timer_id = global_data.game_mgr.get_logic_timer().register(interval=show_time, times=1, mode=CLOCK, func=self.on_switch_end)

                    self.create_switch_sfx(show_sfx_path, callback)
            if not has_switch_sfx:
                self.show_battle_sfx(state)
                colors = self.charger_conf['switch_color_effect'].get(show_key, [])
                if colors:
                    if self._progress_sfx:
                        self.set_sfx_color(self._progress_sfx, colors)
                        self._cur_energy_color = self._energy_colors[self._charger_state]
                else:
                    self.check_energy_color()
            return None

    def on_switch_end(self):

        def delay_destroy():
            self.destroy_switch_timer()
            self.destroy_switch_sfx()

        global_data.game_mgr.post_exec(delay_destroy)
        self.show_battle_sfx(self._cur_show_battle_sfx_idx)
        self.check_energy_color()
        self._switch_sfx_show_key = None
        return

    def destroy_switch_timer(self):
        if self._switch_timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self._switch_timer_id)
            self._switch_timer_id = None
        return

    def destroy_switch_sfx(self):
        if self._switch_sfx_ids:
            for sfx_id in self._switch_sfx_ids:
                global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

            self._switch_sfx_ids = []
        if self._switch_sfx_dict:
            self._switch_sfx_dict = {}

    def create_switch_sfx(self, show_sfx_path, callback):
        if show_sfx_path:
            tid = global_data.sfx_mgr.create_sfx_in_scene(show_sfx_path, on_create_func=callback)
            self._switch_sfx_ids.append(tid)

    def destroy_energy_sfx(self):
        if self._battery_sfx_ids:
            for sfx_id in six.itervalues(self._battery_sfx_ids):
                global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._battery_sfx_ids = {}
        self._battery_sfx_dict = {}
        if self._battery_progress_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._battery_progress_sfx_id)
        self._battery_progress_sfx_id = None
        self._progress_sfx = None
        return

    def check_entity_can_charging(self, lentity):
        if not lentity:
            return False
        if lentity.ev_g_death() or lentity.ev_g_agony():
            return False
        if not lentity.ev_g_in_mecha('Mecha'):
            cd_type, total_cd, left_time = lentity.ev_g_get_change_state()
            if cd_type not in [mecha_const.RECALL_CD_TYPE_GETMECHA, mecha_const.RECALL_CD_TYPE_DIE]:
                return False
            else:
                if left_time > 0:
                    return True
                return False

        else:
            target = lentity.ev_g_control_target()
            if target and target.logic:
                if target.logic.ev_g_health_percent() >= 1:
                    return False
                else:
                    return True

            else:
                return False

    def set_sfx_color(self, sfx, colors):
        if colors:
            sfx.clear_frame()
            for color_frame in colors:
                percent, a, r, g, b = color_frame
                color = a << 24 | r << 16 | g << 8 | b
                sfx.add_frame(percent, color)

            sfx.restart()

    def setup_control_target_event(self, input_target, is_bind):
        if input_target and input_target.is_valid():
            target = self.get_correct_driver_target(input_target)
            if target:
                if is_bind:
                    if target.id not in self._binding_target_set:
                        ope_func = target.regist_event
                        ope_func('E_ON_CONTROL_TARGET_CHANGE', self.on_switch_control_target, 10)
                        self._binding_target_set.add(target.id)
                elif target.id in self._binding_target_set:
                    ope_func = target.unregist_event
                    ope_func('E_ON_CONTROL_TARGET_CHANGE', self.on_switch_control_target)
                    self._binding_target_set.remove(target.id)

    def get_correct_driver_target(self, ltarget):
        if ltarget.MASK & preregistered_tags.HUMAN_TAG_VALUE == 0:
            driver_id = ltarget.sd.ref_driver_id
            driver = EntityManager.getentity(driver_id)
            if driver and driver.logic:
                return driver.logic
        else:
            return ltarget

    def on_switch_control_target(self, control_target_id, pos, *args):
        target = EntityManager.getentity(control_target_id)
        if target and target.logic and target.logic.is_valid():
            if target.logic.MASK & preregistered_tags.HUMAN_TAG_VALUE == 0:
                driver_id = target.logic.sd.ref_driver_id
                driver = EntityManager.getentity(driver_id)
                driver_model = None
                if driver and driver.logic:
                    driver_model = driver.logic.ev_g_model()
            else:
                driver_id = target.id
                driver_model = target.logic.ev_g_model()
            if driver_model and driver_model.valid and driver_id in self._charging_target_infos_sfx:
                sfx = self._charging_target_infos_sfx[driver_id]
                if sfx and sfx.valid:
                    sfx.endpos_attach(driver_model, 'gliding', True)
        return

    def record_target_charing_state(self, ltarget, is_charging):
        if ltarget and ltarget.is_valid():
            if ltarget.__class__.__name__ == 'LPuppet':
                ltarget.send_event('E_SET_CHARGING_STATE', is_charging)