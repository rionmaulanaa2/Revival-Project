# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBelonging.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager
import logic.gcommon.common_const.sync_const as sync_const
from logic.gcommon.time_utility import time as server_time
from common.cfg import confmgr

class ComBelonging(UnitCom):
    BIND_EVENT = {'G_IS_CONTROLER': '_is_controler',
       'E_GAIN_CONTROL': '_gain_control',
       'E_YIELD_CONTROL': '_yield_control',
       'G_CONTROLER': '_get_controler',
       'G_LEFT_TIME': '_get_left_time',
       'E_END_SHOW_CONTROL_DRONE': '_on_end_control_drone'
       }

    def __init__(self):
        super(ComBelonging, self).__init__()
        self._controller_id = None
        self._create_timestamp = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComBelonging, self).init_from_dict(unit_obj, bdict)
        self.cache_bdict = bdict
        self.npc_id = bdict.get('npc_id', 6006)
        self._controller_id = bdict.get('controller_id', None)
        self._create_timestamp = bdict.get('create_timestamp', 0)
        return

    def on_init_complete(self):
        if self._controller_id:
            drone_model = self.ev_g_model()
            if not drone_model:
                self.regist_event('E_MODEL_LOADED', self._drone_model_loaded)
                return
            entity = EntityManager.getentity(self._controller_id)
            if entity and entity.logic:
                control_model = entity.logic.ev_g_model()
                if not control_model:
                    entity.logic.regist_event('E_MODEL_LOADED', self._control_model_loaded)
                    return
            self.send_event('E_GAIN_CONTROL', self._controller_id)

    def _drone_model_loaded(self, model):
        self.unregist_event('E_MODEL_LOADED', self._drone_model_loaded)
        entity = EntityManager.getentity(self._controller_id)
        if entity and entity.logic:
            ctrl_model = entity.logic.ev_g_model()
            if not ctrl_model:
                entity.logic.regist_event('E_MODEL_LOADED', self._control_model_loaded)
                return
            self.send_event('E_GAIN_CONTROL', self._controller_id)
        else:
            log_error('drone exist and controller not exist!!!!!!!')

    def _control_model_loaded(self, model):
        self.unregist_event('E_MODEL_LOADED', self._control_model_loaded)
        self.send_event('E_GAIN_CONTROL', self._controller_id)

    def _loss_control(self, *args):
        self._yield_control(self._controller_id, False)

    def _is_controler(self, controller_id):
        return self._controller_id == controller_id

    def _get_controler(self):
        return self._controller_id

    def _gain_control(self, controller_id):
        import math3d
        from mobile.common.EntityManager import EntityManager
        from ...time_utility import time
        self._controller_id = controller_id
        is_first = time() - self._create_timestamp <= 5
        model = self.unit_obj.ev_g_model()
        ctrler = EntityManager.getentity(self._controller_id)
        if ctrler and ctrler.logic:
            ctrler.logic.regist_event('E_AGONY', self._loss_control)
            ctrler.logic.regist_event('E_DEFEATED', self._loss_control)
            ctrler.logic.regist_event('E_DEATH', self._loss_control)
            ctrler.logic.send_event('E_CTRL_LOOK_CONSOLE')
        if controller_id == global_data.player.id:
            self._real_control()
            if is_first:
                from logic.comsys.common_ui.ScreenLockerUI import ScreenLockerUI
                drone_ui = global_data.ui_mgr.get_ui('DroneUI')
                if drone_ui:
                    drone_ui.add_hide_count()
                ScreenLockerUI(None, is_auto_unlocker=True, auto_unlocker_time=5)
            ctrler.logic.send_event('E_SET_CONTROL_TARGET', self.unit_obj.get_owner())
            ctrler.logic.send_event('E_TO_DRONE_CAMERA')
        else:
            if global_data.cam_lplayer and global_data.cam_lplayer.id == controller_id:
                ui = global_data.ui_mgr.get_ui('FrontSightUI')
                ui.hide()
            ctrler.logic.send_event('E_SET_CONTROL_TARGET', self.unit_obj.get_owner())
            ctrler.logic.send_event('E_TO_DRONE_CAMERA')
            self.unit_obj.del_com('ComMoveSyncSender2')
            com = self.unit_obj.get_com('ComMoveSyncReceiver2')
            if not com:
                com = self.unit_obj.add_com('ComMoveSyncReceiver2', 'client')
                com.init_from_dict(self.unit_obj, {})
                itpler_lst = []
                itpler_lst.append(sync_const.SYNC_ITPLER_NAME_EULER)
                com.set_enable_sync_itpler(itpler_lst)
            self.send_event('E_BELONG_CHANGE_LOSE_CONTROL')
        if ctrler and ctrler.logic:
            message = 'E_BEGIN_CONTROL' if is_first else 'E_SECOND_CONTROL'
            ctrler.logic.send_event(message, self.unit_obj.id, 'ActionDriveDrone')
        return

    def _get_left_time(self):
        stime = self.cache_bdict.get('suicide_timestamp', None)
        if stime:
            diff_time = stime - server_time()
            return [
             diff_time, 120]
        else:
            return [
             120, 120]

    def _get_human_drone_distance(self):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        controler = EntityManager.getentity(self._controller_id)
        ctrl_model = controler.logic.ev_g_model()
        if ctrl_model:
            ctrl_pos = ctrl_model.position
            drone_pos = self.unit_obj.ev_g_position()
            return (ctrl_pos - drone_pos).length / NEOX_UNIT_SCALE
        return 0

    def _real_control(self):
        ctrler = EntityManager.getentity(self._controller_id)
        if ctrler and ctrler.logic:
            global_data.emgr.scene_set_control_drone_event.emit(self.unit_obj)
            global_data.emgr.scene_sound_visible.emit(False)
            ui = global_data.ui_mgr.show_ui('DroneUI', 'logic.comsys.control_ui')
            max_dis = confmgr.get('drone_data', str(self.npc_id), 'suicide_distance')
            ui.set_drone_npc(self.unit_obj, max_dis)
            left_time, all_time = self._get_left_time()
            dis = self._get_human_drone_distance()
            global_data.emgr.scene_update_life_time.emit(left_time, all_time)
            global_data.emgr.scene_update_drone_distance.emit(dis)
            sender_com = self.unit_obj.get_com('ComMoveSyncSender2')
            if not sender_com:
                sender_com = self.unit_obj.add_com('ComMoveSyncSender2', 'client')
                sender_com.init_from_dict(self.unit_obj, {})
                sender_com.set_ask_enable(False)
                trigger_lst = []
                trigger_lst.append(sync_const.SYNC_TRIGGER_NAME_EULER)
                sender_com.set_enable_sync_trigger(trigger_lst)
            self.unit_obj.del_com('ComMoveSyncReceiver2')
            self.send_event('E_BELONG_CHANGE_GAIN_CONTROL')

    def _on_end_control_drone(self):
        global_data.ui_mgr.close_ui('ScreenLockerUI')
        drone_ui = global_data.ui_mgr.get_ui('DroneUI')
        if drone_ui:
            drone_ui.add_show_count()
        ctrler = EntityManager.getentity(self._controller_id)
        if ctrler and ctrler.logic:
            com_driver = ctrler.logic.get_com('ComHumanDriver')
            com_appearance = ctrler.logic.get_com('ComHumanAppearance')
            if com_driver:
                com_driver._enable_bind_event(True, elist=['E_MOVE', 'E_CTRL_JUMP'])
            if com_appearance:
                com_appearance._enable_bind_event(True, elist=['E_CTRL_SQUAT', 'E_CTRL_GROUND', 'E_MOVE', 'E_CTRL_JUMP', 'E_SET_MOVE_STATE', 'E_CHANGE_MOVE_STATE'])
            global_data.emgr.show_scene_interaction_ui_event.emit('drone')

    def _yield_control(self, controller_id, sync_flag=True):
        import math3d
        if self._controller_id != controller_id:
            return
        else:
            if global_data.cam_lplayer and global_data.cam_lplayer.id == controller_id:
                ui = global_data.ui_mgr.get_ui('FrontSightUI')
                ui.show()
            if sync_flag:
                self.send_event('E_CALL_SYNC_METHOD', 'yield_control', (self._controller_id,), True)
            if global_data.player and self._controller_id == global_data.player.id:
                global_data.emgr.scene_set_control_drone_event.emit(global_data.player.logic)
                if global_data.player.logic:
                    global_data.player.logic.send_event('E_ASSIST_GET_OFF')
                global_data.emgr.scene_close_drone_ui.emit()
                global_data.emgr.scene_sound_visible.emit(True)
                left_time, _ = self._get_left_time()
                if self.ev_g_hp() <= 0:
                    global_data.emgr.battle_show_message_event.emit(get_text_local_content(19054))
                if left_time <= 0:
                    global_data.emgr.battle_show_message_event.emit(get_text_local_content(19053))
            self._controller_id = None
            from mobile.common.EntityManager import EntityManager
            ctrler = EntityManager.getentity(controller_id)
            if ctrler and ctrler.logic:
                model = ctrler.logic.get_com('ComHumanAppearance').model
                pos = model.position if model else math3d.vector(0, 0, 0)
                ctrler.logic.send_event('E_SET_CONTROL_TARGET', None, {'reset_pos': pos})
                ctrler.logic.send_event('E_TO_THIRD_PERSON_CAMERA')
                ctrler.logic.unregist_event('E_AGONY', self._loss_control)
                ctrler.logic.unregist_event('E_DEFEATED', self._loss_control)
                ctrler.logic.unregist_event('E_DEATH', self._loss_control)
                ctrler.logic.send_event('E_ASSIST_GET_OFF')
                ctrler.logic.send_event('E_CANCEL_LOOK_CONSOLE')
            return

    def destroy(self):
        super(ComBelonging, self).destroy()