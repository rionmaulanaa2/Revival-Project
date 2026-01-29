# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComCtrlTVMissileLogic.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from logic.gcommon.cdata.status_config import ST_CONTROLLING_SPECIAL_WEAPON
from mobile.common.mobilecommon import singleton
import math3d
CONTROL_SELF = 0
CONTROL_TV_MISSILE_LAUNCHER = 1
CONTROL_TV_MISSILE = 2
FULL_CONTROL_TARGET_MASK = CONTROL_TV_MISSILE_LAUNCHER | CONTROL_TV_MISSILE
INVERSE_CONTROL_TV_MISSILE_LAUNCHER = ~CONTROL_TV_MISSILE_LAUNCHER
INVERSE_CONTROL_TV_MISSILE = ~CONTROL_TV_MISSILE
CONTROL_TARGET_INDEX = 0
SWITCH_CAMERA_STATE_FUNC_INDEX = 1

@singleton
class TVMissileLogicUIAgent(object):

    def __init__(self):
        self.cur_cam_lplayer = None
        self.component_to_mask_map = {}
        self.missile_launcher_unit = None
        self.missile_unit = None
        self.event_registered = False
        return

    def try_register_event(self):
        if self.event_registered:
            return
        global_data.emgr.scene_camera_player_setted_event += self.on_cam_lplayer_changed
        self.event_registered = True

    def on_cam_lplayer_changed(self):
        cam_lplayer = global_data.cam_lplayer
        if self.cur_cam_lplayer is cam_lplayer:
            return
        else:
            if self.cur_cam_lplayer and self.cur_cam_lplayer.is_valid():
                mask = self.component_to_mask_map.get(self.cur_cam_lplayer.get_com('ComCtrlTVMissileLogic'), None)
                if mask:
                    if mask & CONTROL_TV_MISSILE_LAUNCHER:
                        self._do_hide_tv_missile_launcher_ui()
                    if mask & CONTROL_TV_MISSILE:
                        self._do_hide_tv_missile_ui()
            if cam_lplayer and cam_lplayer.is_valid():
                component = cam_lplayer.get_com('ComCtrlTVMissileLogic')
                mask = self.component_to_mask_map.get(component, None)
                if mask:
                    if mask & CONTROL_TV_MISSILE_LAUNCHER:
                        self._do_show_tv_missile_launcher_ui(component)
                    if mask & CONTROL_TV_MISSILE:
                        self._do_show_tv_missile_ui(component)
                self.cur_cam_lplayer = cam_lplayer
            else:
                self.cur_cam_lplayer = None
            return

    def register_component(self, component):
        self.try_register_event()
        self.component_to_mask_map[component] = CONTROL_SELF
        if component.ev_g_is_avatar():
            self.cur_cam_lplayer = component.unit_obj

    def unregister_component(self, component):
        if component in self.component_to_mask_map:
            self.component_to_mask_map.pop(component)

    def _do_show_tv_missile_launcher_ui(self, component):
        if component.ev_g_is_avatar():
            ui = global_data.ui_mgr.get_ui('MechaControlMain')
            if ui:
                ui.enter_screen()
            else:
                ui = global_data.ui_mgr.show_ui('MechaControlMain', 'logic.comsys.mecha_ui')
            ui.on_player_setted(global_data.player.logic)
            ui.on_mecha_setted(component.controlling_launcher_unit)
            ui = global_data.ui_mgr.show_ui('TVMissileLauncherUI', 'logic.comsys.mecha_ui')
            ui.set_player(global_data.player.logic)
            ui.set_mecha(component.controlling_launcher_unit)
        global_data.ui_mgr.show_ui('TVMissileLauncherAimUI', 'logic.comsys.mecha_ui')

    def _do_hide_tv_missile_launcher_ui(self):
        if self.cur_cam_lplayer.ev_g_is_avatar():
            ui = global_data.ui_mgr.get_ui('MechaControlMain')
            ui and ui.leave_screen()
            global_data.ui_mgr.close_ui('TVMissileLauncherUI')
        global_data.ui_mgr.close_ui('TVMissileLauncherAimUI')

    def _do_show_tv_missile_ui(self, component):
        ui = global_data.ui_mgr.get_ui('TVMissileLauncherUI')
        if ui:
            ui.panel.nd_info.setVisible(False)
        ui = global_data.ui_mgr.show_ui('TVMissileAimUI', 'logic.comsys.mecha_ui')
        ui.set_missile_unit(component.fired_missile_entity.logic if component.ev_g_is_avatar() else None)
        return

    def _do_hide_tv_missile_ui(self):
        ui = global_data.ui_mgr.get_ui('TVMissileLauncherUI')
        if ui:
            ui.panel.nd_info.setVisible(True)
        global_data.ui_mgr.close_ui('TVMissileAimUI')

    def show_tv_missile_launcher_ui(self, component):
        if self.component_to_mask_map[component] & CONTROL_TV_MISSILE_LAUNCHER:
            return
        self.component_to_mask_map[component] |= CONTROL_TV_MISSILE_LAUNCHER
        if component.unit_obj is self.cur_cam_lplayer:
            self._do_show_tv_missile_launcher_ui(component)

    def hide_tv_missile_launcher_ui(self, component):
        if self.component_to_mask_map[component] & CONTROL_TV_MISSILE_LAUNCHER:
            self.component_to_mask_map[component] &= INVERSE_CONTROL_TV_MISSILE_LAUNCHER
            if component.unit_obj is self.cur_cam_lplayer:
                self._do_hide_tv_missile_launcher_ui()

    def show_tv_missile_ui(self, component):
        if self.component_to_mask_map[component] & CONTROL_TV_MISSILE:
            return
        self.show_tv_missile_launcher_ui(component)
        self.component_to_mask_map[component] |= CONTROL_TV_MISSILE
        if component.unit_obj is self.cur_cam_lplayer:
            self._do_show_tv_missile_ui(component)

    def hide_tv_missile_ui(self, component):
        if self.component_to_mask_map[component] & CONTROL_TV_MISSILE:
            self.component_to_mask_map[component] &= INVERSE_CONTROL_TV_MISSILE
            if component.unit_obj is self.cur_cam_lplayer:
                self._do_hide_tv_missile_ui()

    def hide_tv_missile_ui_fuel_info(self, component):
        if component.unit_obj is self.cur_cam_lplayer:
            ui = global_data.ui_mgr.get_ui('TVMissileAimUI')
            ui and ui.hide_fuel_info()


tv_missile_logic_agent = TVMissileLogicUIAgent()

class ComCtrlTVMissileLogic(UnitCom):
    BIND_EVENT = {'E_ENABLE_BEHAVIOR': ('on_enable_behavior', 99),
       'E_ANIMATOR_LOADED': ('on_load_animator_complete', 99),
       'E_START_CONTROL_TV_MISSILE_LAUNCHER': 'start_control_launcher',
       'E_STOP_CONTROL_TV_MISSILE_LAUNCHER': 'stop_control_launcher',
       'E_TV_MISSILE_FIRED': 'on_missile_fired',
       'E_START_CONTROL_TV_MISSILE': 'start_control_missile',
       'E_STOP_CONTROL_TV_MISSILE': 'stop_control_missile',
       'G_TRY_EXPLODE_TV_MISSILE_IN_ADVANCE': 'try_explode_tv_missile_in_advance',
       'E_TV_MISSILE_EXPLODED': 'on_tv_missile_exploded',
       'G_CONTROLLING_TV_MISSILE_LAUNCHER': 'is_controlling_tv_missile_launcher'
       }

    def __init__(self):
        super(ComCtrlTVMissileLogic, self).__init__()
        self._controlling_launcher_id = None
        self._controlling_launcher_unit = None
        return

    @property
    def controlling_launcher_id(self):
        return self._controlling_launcher_id

    @controlling_launcher_id.setter
    def controlling_launcher_id(self, eid):
        self._controlling_launcher_id = eid
        if eid:
            entity = global_data.battle.get_entity(eid)
            if entity and entity.logic and entity.logic.is_valid():
                self._controlling_launcher_unit = entity.logic
        else:
            self._controlling_launcher_unit = None
        return

    @property
    def controlling_launcher_unit(self):
        if self._controlling_launcher_unit and self._controlling_launcher_unit.is_valid():
            return self._controlling_launcher_unit
        else:
            if self._controlling_launcher_id:
                entity = global_data.battle.get_entity(self._controlling_launcher_id)
                if entity and entity.logic and entity.logic.is_valid():
                    self._controlling_launcher_unit = entity.logic
                    return self._controlling_launcher_unit
            self._controlling_launcher_unit = None
            return

    def _is_camera_player(self):
        return global_data.cam_lplayer and global_data.cam_lplayer.id == self.unit_obj.id

    def _do_control_tv_missile_launcher_appearance(self, check_execute_ret=None):
        if check_execute_ret is None:
            human_model = self.ev_g_model()
            if not human_model:
                return (False, ())
            if self.controlling_launcher_unit:
                launcher_model = self.controlling_launcher_unit.ev_g_model()
                if launcher_model:
                    return (True, (human_model, launcher_model))
            return (
             False, ())
        else:
            human_model, launcher_model = check_execute_ret
            human_model.remove_from_parent()
            launcher_model.bind('renwu', human_model)
            human_model.position = math3d.vector(0, 0, 0)
            if self.ev_g_is_avatar() or self.sd.ref_is_agent:
                self.send_event('E_SET_EMPTY_HAND', False)
            self.sd.ref_logic_trans.yaw_target = 0
            self.sd.ref_common_motor.set_yaw_time(0)
            self.send_event('E_SET_ACTION_VISIBLE', 'MoveRocker', False)
            self.controlling_launcher_unit.send_event('E_DO_CONTROLLED_APPEARANCE', self.unit_obj.id)
            tv_missile_logic_agent.show_tv_missile_launcher_ui(self)
            self.sd.ref_controlling_tv_missile_launcher = True
            return

    def _undo_control_tv_missile_launcher_appearance(self, check_execute_ret=None):
        if check_execute_ret is None:
            human_model = self.ev_g_model()
            if human_model:
                return (True, human_model)
            return (False, None)
        else:
            human_model = check_execute_ret
            human_model.remove_from_parent()
            self.scene.add_object(human_model)
            if self.ev_g_is_avatar() or self.sd.ref_is_agent:
                if self.cur_control_target_mask & CONTROL_TV_MISSILE:
                    self.sd.ref_logic_trans.yaw_target = self.recorded_yaw
                else:
                    self.sd.ref_logic_trans.yaw_target = self.scene.active_camera.rotation_matrix.yaw
                self.sd.ref_common_motor.set_yaw_time(0)
                self.send_event('E_SWITCH_LAST_GUN', switch_status=False)
                self.send_event('E_FOOT_POSITION', self.get_off_position)
            else:
                if self.controlling_launcher_unit:
                    self.sd.ref_logic_trans.yaw_target = self.controlling_launcher_unit.sd.ref_logic_trans.yaw_target
                else:
                    self.sd.ref_logic_trans.yaw_target = human_model.world_rotation_matrix.yaw
                self.sd.ref_common_motor.set_yaw_time(0)
            self.send_event('E_SET_ACTION_VISIBLE', 'MoveRocker', True)
            if self.controlling_launcher_unit:
                self.controlling_launcher_unit.send_event('E_UNDO_CONTROLLED_APPEARANCE')
            tv_missile_logic_agent.hide_tv_missile_launcher_ui(self)
            self.sd.ref_controlling_tv_missile_launcher = False
            return

    def _do_control_tv_missile_appearance(self, check_execute_ret=None):
        if check_execute_ret is None:
            if self.ev_g_model():
                return (True, ())
            return (False, ())
        else:
            if self.ev_g_is_avatar():
                matrix = self.scene.active_camera.rotation_matrix
                self.recorded_yaw, self.recorded_pitch = matrix.yaw, matrix.pitch
                tv_missile_logic_agent.show_tv_missile_ui(self)
                global_data.emgr.scene_sound_visible.emit(False)
            return

    def _undo_control_tv_missile_appearance(self, check_execute_ret=None):
        if check_execute_ret is None:
            if self.ev_g_model():
                return (True, ())
            return (False, ())
        else:
            if self.ev_g_is_avatar():
                global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(self.recorded_yaw, self.recorded_pitch, False)
                tv_missile_logic_agent.hide_tv_missile_ui(self)
                global_data.emgr.scene_sound_visible.emit(True)
            return

    def init_from_dict(self, unit_obj, bdict):
        super(ComCtrlTVMissileLogic, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_controlling_tv_missile_launcher = False
        self.controlling_launcher_id = bdict.get('tvml_eid', None)
        self.fired_missile_entity = None
        self.get_off_position = None
        self.data_notified = True
        self.launcher_appearance_done = False
        self.cur_control_target = None
        self.cur_control_target_mask = CONTROL_SELF
        self.expected_control_target_mask = CONTROL_SELF
        self.recorded_yaw = 0
        self.recorded_pitch = 0
        self.execute_mask_func_map = {CONTROL_TV_MISSILE_LAUNCHER: {0: self._undo_control_tv_missile_launcher_appearance,
                                         CONTROL_TV_MISSILE_LAUNCHER: self._do_control_tv_missile_launcher_appearance
                                         },
           CONTROL_TV_MISSILE: {0: self._undo_control_tv_missile_appearance,
                                CONTROL_TV_MISSILE: self._do_control_tv_missile_appearance
                                }
           }
        self.mask_appearance_map = {CONTROL_SELF: (
                        None, lambda : self._is_camera_player() and global_data.cam_lplayer.send_event('E_TO_THIRD_PERSON_CAMERA')),
           CONTROL_TV_MISSILE_LAUNCHER: [
                                       None, lambda : self._is_camera_player() and global_data.cam_lplayer.send_event('E_TRY_SWITCH_CAM_STATE', 'E_MECHA_CAMERA', '112')],
           CONTROL_TV_MISSILE: [
                              None, lambda : self._is_camera_player() and global_data.cam_lplayer.send_event('E_TRY_SWITCH_CAM_STATE', 'E_MECHA_CAMERA', '197')]
           }
        self.mask_appearance_map[FULL_CONTROL_TARGET_MASK] = self.mask_appearance_map[CONTROL_TV_MISSILE]
        self.fire_time = 0
        return

    def on_post_init_complete(self, bdict):
        if self.controlling_launcher_id:
            self.sd.ref_force_zero_body_pitch = True
        tv_missile_logic_agent.register_component(self)

    def destroy(self):
        if self.ev_g_is_avatar():
            global_data.emgr.set_pickable_manager_get_pos_type.emit(False)
        self.controlling_launcher_id = None
        self.execute_mask_func_map.clear()
        self.mask_appearance_map.clear()
        tv_missile_logic_agent.unregister_component(self)
        super(ComCtrlTVMissileLogic, self).destroy()
        return

    def _activate_state(self, flag):
        if self.ev_g_is_avatar() or self.sd.ref_is_agent:
            event_name = 'E_ACTIVE_STATE' if flag else 'E_DISABLE_STATE'
            self.send_event(event_name, ST_CONTROLLING_SPECIAL_WEAPON)

    def on_enable_behavior(self, *args):
        if self.controlling_launcher_id:
            self._activate_state(True)

    def _update_expected_control_target_mask(self, single_target_mask, target_entity):
        if target_entity is None:
            self.expected_control_target_mask = self.cur_control_target_mask & ~single_target_mask
        else:
            self.expected_control_target_mask = self.cur_control_target_mask | single_target_mask
        self.mask_appearance_map[single_target_mask][CONTROL_TARGET_INDEX] = target_entity
        return

    def _refresh_control_target_appearance(self):
        diff_mask = self.expected_control_target_mask ^ self.cur_control_target_mask
        if diff_mask:
            new_mask = 0
            for single_mask, execute_func_map in six.iteritems(self.execute_mask_func_map):
                if diff_mask & single_mask:
                    func = execute_func_map[self.expected_control_target_mask & single_mask]
                    can_execute, check_execute_ret = func()
                    if can_execute:
                        func(check_execute_ret)
                        new_mask |= self.expected_control_target_mask & single_mask
                    else:
                        new_mask |= self.cur_control_target_mask & single_mask
                else:
                    new_mask |= self.cur_control_target_mask & single_mask

            self.cur_control_target_mask = new_mask
            if new_mask == self.expected_control_target_mask:
                new_control_target, switch_camera_state_func = self.mask_appearance_map[self.cur_control_target_mask]
                if self.cur_control_target != new_control_target:
                    if self.cur_control_target_mask == CONTROL_SELF:
                        ctrl_conf = {'reset_pos': self.get_off_position}
                    else:
                        ctrl_conf = None
                    self.send_event('E_SET_CONTROL_TARGET', new_control_target, ctrl_conf)
                    switch_camera_state_func()
                    self.cur_control_target = new_control_target
                if self.ev_g_is_avatar():
                    if self.cur_control_target_mask == CONTROL_SELF:
                        self.send_event('E_CAM_PITCH', self.scene.active_camera.rotation_matrix.pitch)
                        self.send_event('E_ACTION_SYNC_HEAD_PITCH')
                    global_data.emgr.set_pickable_manager_get_pos_type.emit(self.cur_control_target_mask != CONTROL_SELF)
        return

    def on_load_animator_complete(self, *args):
        self._refresh_control_target_appearance()

    def start_control_launcher(self, eid):
        launcher_entity = global_data.battle.get_entity(eid)
        if not launcher_entity:
            return
        else:
            self._activate_state(True)
            self.sd.ref_force_zero_body_pitch = True
            self.controlling_launcher_id = eid
            self.get_off_position = None
            self._update_expected_control_target_mask(CONTROL_TV_MISSILE_LAUNCHER, launcher_entity)
            self._refresh_control_target_appearance()
            return

    def stop_control_launcher(self, get_off_position):
        self._activate_state(False)
        self.sd.ref_force_zero_body_pitch = False
        self.get_off_position = math3d.vector(*get_off_position)
        self._update_expected_control_target_mask(CONTROL_TV_MISSILE_LAUNCHER, None)
        self._refresh_control_target_appearance()
        if self.fired_missile_entity and self.fired_missile_entity.logic and self.fired_missile_entity.logic.is_valid():
            self.fired_missile_entity.logic.send_event('E_EXPLODE_IN_ADVANCE', with_delay_appearance=False)
        return

    def on_missile_fired(self, missile_entity):
        self.fired_missile_entity = missile_entity

    def start_control_missile(self, missile_entity):
        self._update_expected_control_target_mask(CONTROL_TV_MISSILE, missile_entity)
        self._refresh_control_target_appearance()

    def stop_control_missile(self):
        self._update_expected_control_target_mask(CONTROL_TV_MISSILE, None)
        self._refresh_control_target_appearance()
        self.fired_missile_entity = None
        return

    def try_explode_tv_missile_in_advance(self):
        if self.fired_missile_entity and self.fired_missile_entity.logic and self.fired_missile_entity.logic.is_valid():
            self.fired_missile_entity.logic.send_event('E_EXPLODE_IN_ADVANCE')
            return True
        else:
            return False

    def on_tv_missile_exploded(self):
        tv_missile_logic_agent.hide_tv_missile_ui_fuel_info(self)
        if self.cur_control_target_mask == CONTROL_TV_MISSILE_LAUNCHER:
            if self.controlling_launcher_unit:
                self.controlling_launcher_unit.send_event('E_TRY_LAUNCHER_RELOAD')

    def is_controlling_tv_missile_launcher(self):
        return self.cur_control_target_mask & CONTROL_TV_MISSILE_LAUNCHER