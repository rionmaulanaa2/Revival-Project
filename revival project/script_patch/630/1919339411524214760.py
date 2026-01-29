# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComExecute.py
from __future__ import absolute_import
import world
import math3d
import C_file
import collision
from logic.gcommon.component.UnitCom import UnitCom
import logic.gcommon.common_const.robot_animation_const as robot_animation_const
from logic.gcommon.cdata import mecha_status_config
from mobile.common.EntityManager import EntityManager
from logic.gutils import mecha_utils
DASH_ACC = 0
DASH_MOVE = 1
DASH_BRAKE = 2
DASH_STOP = 3
DETECT_LEN = 1000

class ComExecute(UnitCom):
    BIND_EVENT = {'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_EXECUTE': 'begin_execute',
       'G_EXECUTE': 'be_executed',
       'E_LEAVE_STATE': 'leave_states',
       'E_ON_JOIN_MECHA': 'on_join_mecha'
       }

    def __init__(self):
        super(ComExecute, self).__init__()
        self._is_target = False
        self._be_executed = False
        self._trigger_obj = None
        self._driver_id = None
        self._trigger_model = None
        self._ori_pos = None
        self._ori_rot = None
        self.model = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComExecute, self).init_from_dict(unit_obj, bdict)

    def on_init_complete(self):
        pass

    def on_load_animator_complete(self, *args):
        animator = self.ev_g_animator()
        if not animator:
            return
        model = self.ev_g_model()
        if model and model.valid:
            self.model = model
        self.send_event('E_REGISTER_ANIM_STATE_EXIT', robot_animation_const.END_EXECUTE, self.end_execute)
        self.send_event('E_REGISTER_ANIM_DEACTIVE', robot_animation_const.END_EXECUTE, self.end_execute)

    def destroy(self):
        self.end_execute()
        self.need_update = False
        self.model = None
        self.character = None
        self._trigger_obj = None
        self._trigger_model = None
        super(ComExecute, self).destroy()
        return

    def leave_states(self, leave_state, new_state=None):
        if not self.ev_g_is_avatar():
            return

    def stop_gravity(self, trigger, target):
        trigger.send_event('E_SET_SYNC_ACTION_RECEVIVER_ENABLE', False)
        target.send_event('E_SET_SYNC_RECEIVER_ENABLE', False)

    def resume_gravity(self, trigger, target):
        trigger.send_event('E_SET_SYNC_ACTION_RECEVIVER_ENABLE', True)
        target.send_event('E_SET_SYNC_RECEIVER_ENABLE', True)

    def begin_execute(self, trigger_id):
        if self.sd.ref_mecha_id != 8001:
            return
        if global_data.mecha:
            if global_data.mecha.id in (trigger_id,):
                global_data.ui_mgr.show_ui('MechaExecute', 'logic.comsys.mecha_ui')
                if self.model and self.model.valid:
                    global_data.emgr.camera_bind_to_model_socket_event.emit(self.model, 'execute')
                    global_data.emgr.camera_set_hfov_event.emit(45, True)

                    def end_callback():
                        global_data.emgr.camera_bind_to_scene_event.emit()
                        global_data.emgr.camera_set_hfov_event.emit(None, False)
                        global_data.emgr.slerp_into_setupped_camera_event.emit(0.03, False, 0.03)
                        return

                    global_data.emgr.camera_play_plot_trk_event.emit('MECHA_EXECUTE', end_callback)
        self._be_executed = True
        self._is_target = True
        trigger, target = EntityManager.getentity(trigger_id), self.unit_obj
        if trigger and trigger.logic and target:
            self.execute_anim(trigger.logic, target)
            self.stop_gravity(trigger.logic, target)
            self._trigger_obj = trigger.logic
        self.need_update = True

    def execute_anim(self, trigger, target):
        if not self.swtich_anim_source(trigger, True) or not self.swtich_anim_source(target, False):
            return
        trigger.ev_g_status_try_trans(mecha_status_config.MC_EXECUTE)
        self.ev_g_status_try_trans(mecha_status_config.MC_EXECUTE)
        self.rotate_model_to_target(trigger, target)
        trigger.send_event('E_RESUME_HIT_ANIM')
        trigger.send_event('E_HAND_ACTION', robot_animation_const.HAND_STATE_NONE)
        trigger.send_event('E_SWITCH_STATUS', robot_animation_const.STATE_EXECUTE)
        self.send_event('E_HAND_ACTION', robot_animation_const.HAND_STATE_NONE)
        self.send_event('E_SWITCH_STATUS', robot_animation_const.STATE_EXECUTE)
        self.unit_obj.del_com('ComMechaStaticCollision')

    def rotate_model_to_target(self, trigger, target):
        trigger_model, target_model = trigger.ev_g_model(), target.ev_g_model()
        trigger_pos, target_pos = trigger_model.position, target_model.position
        turn_dir = target_pos - trigger_pos
        turn_dir.y = 0
        if turn_dir.is_zero:
            return
        turn_dir.normalize()
        trigger_model.rotation_matrix = math3d.matrix.make_orient(turn_dir, math3d.vector(0, 1, 0))
        target_model.rotation_matrix = math3d.matrix.make_orient(-turn_dir, math3d.vector(0, 1, 0))
        self._ori_pos = trigger_model.position
        self._ori_rot = trigger_model.rotation_matrix
        trigger_model.remove_from_parent()
        trigger_model.position = math3d.vector(0, 0, 0)
        trigger_model.rotation_matrix = math3d.matrix()
        target_model.bind('execute', trigger_model, world.BIND_TYPE_ALL)
        self._trigger_model = trigger_model

    def swtich_anim_source(self, mecha, is_trigger):
        animator = mecha.ev_g_animator()
        if not animator:
            return False
        animation_node = animator.find('execute')
        if not animation_node:
            return False
        clip_name = 'executed' if is_trigger else 'be_executed'
        animator.replace_clip_name('execute', clip_namem)
        return True

    def end_execute(self, *args):
        if self._is_target and not self._be_executed:
            return
        else:
            self.ev_g_cancel_state(mecha_status_config.MC_EXECUTE)
            self.need_update = False
            self._be_executed = False
            if self._is_target:
                if self._driver_id:
                    entity = EntityManager.getentity(self._driver_id)
                    if entity and entity.logic:
                        entity.logic.send_event('E_ON_LEAVE_MECHA')
                if self._trigger_model and self._trigger_model.valid:
                    position = self._trigger_model.world_position
                    self._trigger_model.remove_from_parent()
                    self.scene.add_object(self._trigger_model)
                    self._trigger_model.position = position
                    self._trigger_model.rotation_matrix = self._ori_rot
                    self._trigger_model = None
                if self._trigger_obj:
                    self.resume_gravity(self._trigger_obj, self.unit_obj)
                    pos = self._trigger_obj.ev_g_position()
                    if pos:
                        self._trigger_obj.send_event('E_POSITION', pos)
                global_data.game_mgr.delay_exec(0.5, lambda : mecha_utils.create_call_up_sfx(self, self.model, self.ev_g_select_sfx()))
            if not self._is_target and global_data.mecha and global_data.mecha.id == self.unit_obj.id:
                self.send_event('E_ROTATE_MODEL_TO_CAMERA_DIR')
            if not self._is_target:
                self.send_event('E_CTRL_STAND')
                animator = self.ev_g_animator()
                if not animator:
                    return
                node = animator.find('execute')
                if node:
                    blend_state = node.GetBlendState()
                    blend_state.SetSmoothWeightSpeed(0)
                    blend_state.currentWeight = 0
            ui = global_data.ui_mgr.get_ui('MechaExecute')
            if ui and not ui.disappearing:
                ui.disappear()
            return

    def be_executed(self):
        return self._be_executed

    def on_join_mecha(self):
        self._driver_id = self.sd.ref_driver_id

    def tick(self, delta):
        if self._trigger_model and self._trigger_model.valid:
            self._trigger_model.position = math3d.vector(0, 0, 0)
            self._trigger_model.rotation_matrix = math3d.matrix()