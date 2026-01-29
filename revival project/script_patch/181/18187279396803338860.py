# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComObserve.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import mecha_const as mconst
from common.cfg import confmgr
from logic.client.const import game_mode_const

class ComObserve(UnitCom):
    BIND_EVENT = {'E_ON_JOIN_MECHA': '_on_join_mecha',
       'E_ON_LEAVE_MECHA': '_on_leave_mecha',
       'E_SET_RECHOOSE_MECHA': ('set_rechoose_mecha', 10),
       'E_SWITCH_TO_MECHA_STATE': '_on_switch_to_mecha_state',
       'E_ON_BEING_OBSERVE': 'on_observe',
       'G_IN_OBSERVE': '_in_observe',
       'E_SET_CHARGING_STATE': '_set_charging_state',
       'G_CHARGING_STATE': '_get_charging_state'
       }

    def __init__(self):
        super(ComObserve, self).__init__()
        self.last_mecha_id_type = None
        self._being_ob = False
        self._charging = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComObserve, self).init_from_dict(unit_obj, bdict)
        self._mecha_ui = False
        self.switch_to_state_change_ui()

    def _is_spectate_target(self):
        return self.ev_g_is_cam_target()

    def _on_switch_to_mecha_state(self, mecha_id):
        if self._is_spectate_target():
            ui = global_data.ui_mgr.get_ui('StateChangeUI')
            if ui:
                ui.on_cancel_enter_mecha()

    def switch_to_state_change_ui(self, mecha_state=False):
        if self.ev_g_get_bind_mecha() and self._is_spectate_target():
            if global_data.ex_scene_mgr_agent.check_settle_scene_active():
                return
            ui = global_data.ui_mgr.get_ui('StateChangeUI')
            if not ui:
                ui = global_data.ui_mgr.show_ui('StateChangeUI', 'logic.comsys.battle')
            if ui:
                ui.on_change_state(mecha_state)

    def _on_join_mecha(self, mecha_id, *args, **kwargs):
        if self._is_spectate_target():
            self.switch_to_state_change_ui(True)
            global_data.ui_mgr.close_ui('MechaUI')
            global_data.emgr.on_observer_join_mecha.emit()
            target = EntityManager.getentity(mecha_id)
            if target is None:
                return
            self._switch_to_mecha_ui(True, target)
        return

    def _on_leave_mecha(self):
        if self._is_spectate_target():
            global_data.emgr.on_observer_leave_mecha.emit()
            self._switch_to_mecha_ui(False)

    def _switch_to_mecha_ui(self, mecha_ui=True, mecha_target=None, close=False):
        if global_data.ex_scene_mgr_agent.check_settle_scene_active():
            return
        self.mecha_ui_list = ['MechaHpInfoUI', 'MechaCockpitUI']
        pre_load_ui_list = list(self.mecha_ui_list)
        ui_conf = confmgr.get('mecha_conf', 'UIConfig', 'Content')
        if mecha_ui:
            mecha_id_type = str(self.ev_g_get_bind_mecha_type())
            self.last_mecha_id_type = mecha_id_type
        else:
            mecha_id_type = self.last_mecha_id_type
        if mecha_id_type and mecha_id_type in ui_conf:
            ui_info = ui_conf[mecha_id_type]
            self.mecha_ui_list.extend(ui_info['observe_append_ui'])
        if mecha_ui and not self._mecha_ui:
            for ui_name in self.mecha_ui_list:
                ui = global_data.ui_mgr.get_ui(ui_name)
                if not ui:
                    ui = global_data.ui_mgr.show_ui(ui_name, 'logic.comsys.mecha_ui')
                ui.leave_screen()
                ui.enter_screen()
                if hasattr(ui, 'on_mecha_setted'):
                    ui.on_mecha_setted(mecha_target.logic)

            self._mecha_ui = True
        elif not mecha_ui:
            for ui_name in self.mecha_ui_list:
                ui = global_data.ui_mgr.get_ui(ui_name)
                if ui and hasattr(ui, 'disappear') and not close:
                    ui.disappear()
                elif ui and ui_name in pre_load_ui_list:
                    ui.leave_screen()
                else:
                    global_data.ui_mgr.close_ui(ui_name)

            self.mecha_ui_list = []
            self._mecha_ui = False

    def _in_observe(self):
        return self._being_ob

    def on_observe(self, is_on_observe):
        self._being_ob = is_on_observe
        obj_target = self.ev_g_control_target()
        if obj_target and obj_target.logic and obj_target.logic is not self.unit_obj:
            obj_target.logic.send_event('E_ON_BEING_OBSERVE', self._being_ob)
        if is_on_observe:
            _bind_mecha_id = self.ev_g_get_bind_mecha()
            if _bind_mecha_id:
                global_data.ui_mgr.close_ui('MechaUI')
                if self.ev_g_in_mecha('Mecha'):
                    self._on_switch_to_mecha_state(_bind_mecha_id)
                    self.switch_to_state_change_ui(True)
                    target = EntityManager.getentity(_bind_mecha_id)
                    if target is None:
                        return
                    self._switch_to_mecha_ui(True, target)
                    global_data.game_mgr.scene.disable_vegetation()
                    return
                self.switch_to_state_change_ui(False)
                global_data.game_mgr.scene.recover_vegetation_enable()
            else:
                if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_HUMAN_SURVIVAL):
                    global_data.ui_mgr.close_ui('MechaUI')
                else:
                    global_data.ui_mgr.close_ui('StateChangeUI')
                    self.show_mecha_progress_ui()
                global_data.game_mgr.scene.recover_vegetation_enable()
        else:
            self._switch_to_mecha_ui(False, None, True)
            self._mecha_ui = False
            global_data.ui_mgr.close_ui('StateChangeUI')
            global_data.ui_mgr.close_ui('MechaUI')
        self.set_ctrl_target_static_collision(is_on_observe)
        return

    def show_mecha_progress_ui(self):
        ui = global_data.ui_mgr.show_ui('MechaUI', 'logic.comsys.battle')
        if ui:
            ui.refresh_random_mecha_icon()

    def destroy(self):
        if self._is_spectate_target():
            self._switch_to_mecha_ui(False)

    def set_ctrl_target_static_collision(self, is_coll):
        control_target = self.ev_g_control_target()
        if control_target and control_target.logic:
            if control_target.__class__.__name__ == 'MechaTrans':
                control_target.logic.send_event('E_VEHICLE_COLLISION_SET', is_coll)

    def set_rechoose_mecha(self, is_revive):
        if self._is_spectate_target():
            if is_revive:
                if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_HUMAN_SURVIVAL):
                    global_data.ui_mgr.close_ui('MechaUI')
                else:
                    global_data.ui_mgr.close_ui('StateChangeUI')
                    self.show_mecha_progress_ui()

    def _set_charging_state(self, charging):
        self._charging = charging

    def _get_charging_state(self):
        return self._charging