# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComKillerCamera.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.client.const.camera_const import FOCUS_MODE
import world
import math3d
import time
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const.mecha_const import MECHA_MODE_BLOOD_SOCKET_POS_OFFSET
from logic.gcommon.common_utils.parachute_utils import STAGE_NONE
from common.cfg import confmgr

class ComKillerCamera(UnitCom):
    BIND_EVENT = {'E_SET_KILLER_ID_NAME': 'on_got_kill',
       'E_RECOVER_KILLER_CAM': 'on_recover_killer_cam',
       'E_ON_LEAVE_MECHA': ('_on_leave_mecha', 99),
       'E_PLAY_VICTORY_CAMERA': '_on_focus_oneself_camera',
       'E_EXIT_FOCUS_CAMERA': 'exit_focus_camera'
       }

    def __init__(self):
        super(ComKillerCamera, self).__init__()
        self._focus_timer_id = None
        self._killer_id = None
        self._killer_name = ''
        self._focus_track = None
        self._is_leave_mecha = False
        self.cache_args = None
        self._delay_timer = None
        self._is_in_oneself_focus = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComKillerCamera, self).init_from_dict(unit_obj, bdict)
        self.process_event(True)

    def process_event(self, is_bind=True):
        emgr = global_data.emgr
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_camera_switch_to_state(self, new_cam_type, old_cam_type, is_finish_switch):
        return
        if self._focus_timer_id:
            if is_finish_switch and self._killer_id:
                self.unregist_focus_camera_timer()
                self.got_kill_camera(self._killer_id)

    def got_kill_camera(self, killer_id):
        self.send_event('E_TRY_SWITCH_TO_CAMERA_STATE', FOCUS_MODE, focus_id=killer_id)
        self._focus_timer_id = None
        return

    def is_game_over(self):
        bat = global_data.battle
        if bat:
            return bat.is_settle
        return True

    @execute_by_mode(True, (game_mode_const.GAME_MODE_PURE_MECHA, game_mode_const.GAME_MODE_HUNTING))
    def _on_leave_mecha(self, *args, **kargs):
        if self.ev_g_is_pure_mecha() and self.cache_args:
            self.on_got_kill(*self.cache_args)
        self._is_leave_mecha = True

    @execute_by_mode(True, game_mode_const.KillerCamera)
    def on_got_kill(self, killer_id, killer_name):
        if self.is_game_over():
            return
        else:
            if self.ev_g_is_pure_mecha() and not self._is_leave_mecha:
                self.cache_args = (
                 killer_id, killer_name)
                return
            if killer_id is None or self.unit_obj and self.unit_obj.id == killer_id:
                return
            if global_data.gvg_battle_data and global_data.gvg_battle_data.somebody_is_over(self.unit_obj.id):
                return
            self._killer_id = killer_id
            self._killer_name = killer_name
            killer = EntityManager.getentity(killer_id)
            if not (killer and killer.logic):
                return
            if global_data.game_mode.get_mode_type() == game_mode_const.GAME_MODE_KING:

                def got_kill_camera():
                    self.got_kill_camera(killer_id)

                from common.utils.timer import CLOCK
                tmr = global_data.game_mgr.get_logic_timer()
                self._focus_timer_id = tmr.register(func=got_kill_camera, times=1, mode=CLOCK, interval=2)
            else:
                self.on_focus_killer(killer_id)
            return

    def unregist_focus_camera_timer(self):
        if self._focus_timer_id is not None:
            global_data.game_mgr.get_logic_timer().unregister(self._focus_timer_id)
            self._focus_timer_id = None
        return

    def destroy(self):
        self.process_event(False)
        self.unregist_focus_camera_timer()
        self.destroy_track()
        super(ComKillerCamera, self).destroy()
        self.exit_focus_camera()

    @execute_by_mode(True, game_mode_const.KillerCamera)
    def on_focus_killer(self, focus_id):
        if not self._focus_track:
            self._focus_track = FocusTrack()
        self._focus_track.set_focus_id(focus_id)
        self._focus_track.on_enter()

    @execute_by_mode(True, game_mode_const.KillerCamera)
    def on_target_revive(self):
        if self._focus_track:
            self._focus_track.on_exit()

    @execute_by_mode(True, game_mode_const.KillerCamera)
    def on_recover_killer_cam(self):
        self.destroy_track()

    def destroy_track(self):
        if self._focus_track:
            self._focus_track.destroy()
            self._focus_track = None
        self._is_leave_mecha = False
        self.cache_args = None
        return

    def _on_focus_oneself_camera(self):
        if self.ev_g_is_cam_target() and global_data.cam_lctarget:
            if self.sd.ref_in_aim:
                self.send_event('E_QUIT_AIM')
            elif self.ev_g_in_right_aim():
                self.send_event('E_QUIT_RIGHT_AIM')
            self._is_in_oneself_focus = True
            global_data.cam_lplayer.send_event('E_FREE_CAMERA_STATE', False)
            global_data.game_mgr.set_global_speed_rate(0.3)
            global_data.emgr.camera_switch_collision_check_event.emit(False)
            global_data.cam_lctarget.send_event('E_SET_CAMERA_FOLLOW_SPEED', False, 1)
            yaw = global_data.cam_lctarget.ev_g_yaw()
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(yaw if yaw is not None else None, 0, True, 0.3)
            _camera_state = global_data.cam_data.camera_state_type
            global_data.emgr.switch_cam_state_enable_event.emit(False)
            global_data.emgr.enable_camera_yaw.emit(False)
            from common.utils import timer
            self._delay_timer = global_data.game_mgr.get_post_logic_timer().register(func=lambda : self._focus_cam_trk_func(_camera_state), interval=0.3 * global_data.game_mgr.get_global_speed_rate(), times=1, mode=timer.CLOCK)
            if global_data.game_mode and not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CONCERT):
                global_data.sound_mgr.post_event_2d('Play_time_stretching', None)
        return

    def _focus_cam_trk_func(self, camera_state):
        from logic.client.const.camera_const import MECHA_MODE
        self._delay_timer = None
        from logic.gcommon.common_const import mecha_const
        if self.ev_g_is_cam_target():
            if self.ev_g_in_mecha():
                from logic.gutils.CameraHelper import get_camera_state_def_mat
                from logic.client.const.camera_const import POSTURE_STAND
                mecha_camera_state = camera_state
                start_mat_org = get_camera_state_def_mat(mecha_camera_state, POSTURE_STAND, None)
                firefox_mat_org = get_camera_state_def_mat(MECHA_MODE, POSTURE_STAND, None)
                diff = start_mat_org.translation - firefox_mat_org.translation
                mat = math3d.matrix()
                mat.translation = math3d.vector(diff.x * -0.5, diff.y * -0.5, diff.z * -1)
                if global_data.cam_lctarget.ev_g_pattern() == mecha_const.MECHA_TYPE_VEHICLE:
                    mat.translation = math3d.vector(20, 20, -30)
                elif self.ev_g_in_mecha('MechaTrans'):
                    mat.translation = math3d.vector(0, 20, -30)
                add_trk_data = {'trk_start_time': 0.1,'end_mat': mat,'duration': 1,'is_to_target': False}
                custom_data = {'end_add_trk': add_trk_data}

                def callback():
                    pass

                global_data.cam_lctarget.send_event('E_PLAY_CAMERA_TRK', 'MECHA_SETTLE_CAMERA', callback, custom_data)
            else:
                global_data.cam_lctarget.send_event('E_PLAY_CAMERA_TRK', 'HUMAN_SETTLE_CAMERA')
        return

    def exit_focus_camera(self):
        if self._is_in_oneself_focus:
            self._is_in_oneself_focus = False
            if self._delay_timer:
                global_data.game_mgr.get_post_logic_timer().unregister(self._delay_timer)
                self._delay_timer = None
            global_data.emgr.camera_switch_collision_check_event.emit(True)
            global_data.emgr.switch_cam_state_enable_event.emit(True)
            global_data.emgr.enable_camera_yaw.emit(True)
            if global_data.game_mgr.get_global_speed_rate() < 1.0:
                global_data.game_mgr.set_global_speed_rate(1.0)
            if self.ev_g_in_mecha():
                global_data.cam_lctarget and global_data.cam_lctarget.send_event('E_CANCEL_CAMERA_TRK', 'MECHA_SETTLE_CAMERA')
            else:
                global_data.cam_lctarget and global_data.cam_lctarget.send_event('E_CANCEL_CAMERA_TRK', 'HUMAN_SETTLE_CAMERA')
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(None, None)
            from logic.gutils.CameraHelper import get_state_def_camera_for_exit_focus
            if self.unit_obj:
                ctarget = self.unit_obj.ev_g_control_target()
                if ctarget and ctarget.logic:
                    camera_state = get_state_def_camera_for_exit_focus(ctarget.logic)
                    self.send_event('E_TRY_SWITCH_TO_CAMERA_STATE', camera_state)
            if self.ev_g_in_mecha() and global_data.cam_lctarget:
                global_data.cam_lctarget.send_event('E_EXIT_FOCUS_CAMERA')
        return


class FocusTrack(object):

    def __init__(self, **kwargs):
        self._timer_id = None
        self._last_time = 8
        self.init_parameter()
        self.slerp_action_list = []
        self.slerp_target_time = 0
        self._has_exited = False
        self._focus_id = None
        self._stoped_driver_entity_ids = []
        self._stoped_control_entity_ids = []
        return

    def set_focus_id(self, focus_id):
        self._focus_id = focus_id

    def set_parameter(self, para_dict):
        if 'global_speed_rate' in para_dict:
            self._global_speed_rate = para_dict['global_speed_rate']
        if 'focus_angle' in para_dict:
            self._angle = para_dict['focus_angle']
        if 'need_catch_screen' in para_dict:
            self._need_catch_screen = para_dict['need_catch_screen']

    def init_parameter(self):
        self._target_dist = [20, 80]
        self._target_y_offset = [-16, -40]
        self._angle = -0.3
        self._action_type = 'CubicBezier'
        self._action_parameter = [0.16, -0.01, 0.23, 0.89]
        self._rot_time = 0.6
        self._translate_time = 1.0
        self._global_speed_rate = 0
        self._need_catch_screen = True

    def on_enter(self, **kwargs):
        self.set_focus_slerp_target()

    def get_target_yaw_pitch(self):
        pos = self.get_target_pos()
        rotate_center = self.get_rotate_center()
        center_pos = rotate_center
        if pos and center_pos:
            diff_vec = pos - center_pos
            return (
             diff_vec.yaw, diff_vec.pitch)
        else:
            return (None, None)
            return None

    def get_rotate_center(self):
        PartCamera = global_data.game_mgr.scene.get_com('PartCamera')
        if not PartCamera:
            return None
        else:
            rotate_center = PartCamera.get_rotate_center()
            return rotate_center

    def get_target_pos(self):
        if self._focus_id:
            from mobile.common.IdManager import IdManager
            ent = EntityManager.getentity(IdManager.str2id(self._focus_id))
            if ent and ent.logic:
                con_target = ent.logic.ev_g_control_target()
                if con_target and con_target.logic:
                    model = con_target.logic.ev_g_model()
                    if model:
                        mecha_mode = con_target.logic.ev_g_mecha_mode()
                        mecha_id = con_target.logic.ev_g_mecha_id()
                        pos_offset = MECHA_MODE_BLOOD_SOCKET_POS_OFFSET.get(mecha_id, {}).get(mecha_mode, 0)
                        socket_name = 's_xuetiao' if con_target.__class__.__name__ == 'Puppet' else 'xuetiao'
                        matrix = model.get_socket_matrix(socket_name, world.SPACE_TYPE_WORLD)
                        if matrix:
                            pos = matrix.translation
                            pos.y += pos_offset * model.scale.y
                        else:
                            pos = model.world_position
                            pos.y += model.bounding_radius_w * 2
                    else:
                        pos = con_target.logic.ev_g_position()
                else:
                    pos = ent.logic.ev_g_position()
                return pos
        return None

    def get_target_in_mecha(self):
        if self._focus_id:
            from mobile.common.IdManager import IdManager
            ent = EntityManager.getentity(IdManager.str2id(self._focus_id))
            if ent and ent.logic:
                return ent.logic.ev_g_in_mecha()
        return False

    def set_target_focus_status(self, enable):
        if not self._focus_id:
            return
        else:
            from mobile.common.IdManager import IdManager
            ent = EntityManager.getentity(IdManager.str2id(self._focus_id))
            if not (ent and ent.logic):
                return
            ent.logic.send_event('E_FORCE_HIGH_MODEL', enable)
            if enable:
                ent.logic.send_event('E_FORCE_LOBBY_OUTLINE', True)
            else:
                ent.logic.send_event('E_FORCE_LOBBY_OUTLINE', False)
            con_target = ent.logic.ev_g_control_target()
            if con_target and con_target.logic:
                con_target.logic.send_event('E_FORCE_HIGH_MODEL', enable)
                if enable:
                    con_target.logic.send_event('E_FORCE_SHADER_LOD_LEVEL', 0)
                else:
                    con_target.logic.send_event('E_FORCE_SHADER_LOD_LEVEL', None)
            return

    def set_all_puppet_stop_status(self):
        from logic.gutils import scene_utils
        if scene_utils.need_game_mode_outline():
            scene_utils.set_outline_process_enable(False, scene_utils.GAME_MODE_OUTLINE_MASK)
        all_puppet = EntityManager.get_entities_by_type('Puppet')
        for k, v in six.iteritems(all_puppet):
            if not v.logic:
                continue
            v.logic.send_event('E_SET_SYNC_RECEIVER_ENABLE', False)
            if v.logic.id not in self._stoped_driver_entity_ids:
                self.add_stoped_driver(v.logic)
            con_target = v.logic.ev_g_control_target()
            if con_target and con_target.logic:
                con_target.logic.send_event('E_SET_SYNC_RECEIVER_ENABLE', False)
                self._stoped_control_entity_ids.append(con_target.logic.id)

    def resume_stoped_entities(self):
        from logic.gutils import scene_utils
        if scene_utils.need_game_mode_outline():
            scene_utils.set_outline_process_enable(True, scene_utils.GAME_MODE_OUTLINE_MASK)
        for e_id in self._stoped_control_entity_ids:
            ent = EntityManager.getentity(e_id)
            if ent and ent.logic:
                ent.logic.send_event('E_SET_SYNC_RECEIVER_ENABLE', True)

        self._stoped_control_entity_ids = []
        for e_id in self._stoped_driver_entity_ids:
            ent = EntityManager.getentity(e_id)
            if ent and ent.logic:
                ent.logic.send_event('E_SET_SYNC_RECEIVER_ENABLE', True)
            self.removed_stoped_driver(e_id)

        self._stoped_driver_entity_ids = []

    def add_stoped_driver(self, ldriver):
        if ldriver:
            ldriver.regist_event('E_ON_CONTROL_TARGET_CHANGE', self.on_changed_control_target)
            self._stoped_driver_entity_ids.append(ldriver.id)

    def removed_stoped_driver(self, ldriver_id):
        ent = EntityManager.getentity(ldriver_id)
        if ent and ent.logic:
            ent.logic.unregist_event('E_ON_CONTROL_TARGET_CHANGE', self.on_changed_control_target)

    def on_changed_control_target(self, target_id, pos, *args):
        if self._has_exited:
            return
        con_target = EntityManager.getentity(target_id)
        if con_target and con_target.logic:
            con_target.logic.send_event('E_SET_SYNC_RECEIVER_ENABLE', False)
            self._stoped_control_entity_ids.append(con_target.logic.id)

    def set_focus_slerp_target(self):
        if not global_data.cam_lplayer:
            return
        else:
            role_id = global_data.cam_lplayer.ev_g_role_id()
            player_pos = global_data.cam_lplayer.ev_g_position()
            if not role_id or not player_pos:
                return
            if not self._focus_id:
                return
            enemy_pos = self.get_target_pos()
            if not enemy_pos:
                return
            rotate_center = self.get_rotate_center()
            if not rotate_center:
                return
            self._has_exited = False
            global_data.emgr.set_in_killer_focus_camera_event.emit(True)
            self.set_target_focus_status(True)
            if self._global_speed_rate <= 0:
                self.set_all_puppet_stop_status()
            if self._need_catch_screen:
                global_data.ui_mgr.set_all_ui_visible(False)
                global_data.touch_mgr_agent.disable_touch_event()
            global_data.emgr.enable_camera_yaw.emit(False)
            global_data.game_mgr.scene.do_set_viewer_position(enemy_pos)
            center_pos = rotate_center
            view_dir = (center_pos - enemy_pos) * math3d.vector(1, 0, 1)
            from common.utils.timer import LOGIC
            tmr = global_data.game_mgr.get_logic_timer()
            self._start_time = time.time()
            self._timer_id = tmr.register(func=self.on_focus_update, times=(self._last_time + 30) * 120, mode=LOGIC)
            if view_dir and not view_dir.is_zero:
                view_dir.normalize()
            else:
                self.slerp_target_time = 1
                if self._need_catch_screen:
                    self.slerp_action_list.append((self.slerp_target_time + 1, 'CATCH_SCREEN'))
                self.slerp_action_list.append((self.slerp_target_time + self._last_time, 'EXIT'))
                return
            offset = self._target_dist[0]
            y_offset = self._target_y_offset[0]
            if self.get_target_in_mecha():
                offset = self._target_dist[1]
                y_offset = self._target_y_offset[1]
            stop_pos = enemy_pos + view_dir * offset
            stop_pos.y += y_offset
            cam = world.get_active_scene().active_camera
            scn = global_data.game_mgr.scene
            from logic.gcommon.common_const.collision_const import GROUP_CAMERA_INCLUDE
            if scn:
                hit, point, normal, fraction, color, obj = scn.scene_col.hit_by_ray(enemy_pos, stop_pos, 0, GROUP_CAMERA_INCLUDE, -1, 0)
                if hit:
                    stop_pos = point
            yaw, pitch = self.get_target_yaw_pitch()
            if yaw is not None and pitch is not None:
                rot_mat = math3d.matrix.make_rotation_x(self._angle) * math3d.matrix.make_rotation_y(yaw)
            else:
                rot_mat = cam.world_rotation_matrix
            from logic.gutils.CameraHelper import get_camera_transform_matrix, get_camera_state_def_mat, rotate_by_center
            from logic.client.const.camera_const import POSTURE_STAND, THIRD_PERSON_MODEL
            end_mat = get_camera_state_def_mat(THIRD_PERSON_MODEL, POSTURE_STAND, role_id, rot_mat)
            end_mat.translation += player_pos
            rot_time = self._rot_time
            translate_time = self._translate_time
            slerp_list = []
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(yaw, pitch, True, rot_time)
            self.slerp_target_time = rot_time
            slerp_list.append((rot_time + 0.1, 'STOP_ANIM'))
            self._pre_enemy_pos = (
             enemy_pos, get_camera_transform_matrix(stop_pos, end_mat.rotation))
            self.slerp_action_list = slerp_list
            if self._need_catch_screen:
                self.slerp_action_list.append((translate_time + rot_time + 0.1, 'CATCH_SCREEN'))
            self.slerp_action_list.append((translate_time + rot_time + self._last_time, 'EXIT'))
            return

    def on_focus_update(self):
        pass_time = time.time() - self._start_time
        if pass_time > self.slerp_target_time and len(self.slerp_action_list) > 0:
            duration, top_mat = self.slerp_action_list.pop(0)
            piece_dur = max(duration - pass_time, 0.1)
            self.slerp_target_time = duration
            if not isinstance(top_mat, str):
                global_data.emgr.camera_set_slerp_target_event.emit(top_mat.translation, top_mat.rotation, cost_time=piece_dur)
                global_data.emgr.camera_set_slerp_target_speed_action_event.emit('CubicBezier', [0.16, -0.01, 0.23, 0.89])
            elif top_mat == 'STOP_ANIM':
                global_data.game_mgr.set_global_speed_rate(0.8)
                global_data.emgr.camera_switch_collision_check_event.emit(False)
                enemy_pos = self.get_target_pos()
                if enemy_pos:
                    old_enemy_pos, trans = self._pre_enemy_pos
                    offset = enemy_pos - old_enemy_pos
                    trans.translation += offset
                    self.slerp_action_list.insert(0, (self._translate_time + self._rot_time, trans))
                else:
                    log_error('on_focus_update: can not get enemy_pos', enemy_pos, self._focus_id)
                    if global_data.is_inner_server:
                        from mobile.common.IdManager import IdManager
                        ent = EntityManager.getentity(IdManager.str2id(self._focus_id))
                        msg = 'on_focus_update: can not get enemy_pos : %s, %s, %s' % (str(enemy_pos), str(self._focus_id), str(ent))
                        global_data.uisystem.post_wizard_trace_inner_server(msg)
                    old_enemy_pos, trans = self._pre_enemy_pos
                    self.slerp_action_list.insert(0, (self._translate_time + self._rot_time, trans))
            elif top_mat == 'CATCH_SCREEN':
                global_data.ui_mgr.show_ui('SceneSnapShotUI', 'logic.comsys.common_ui')
                ui_inst = global_data.ui_mgr.get_ui('SceneSnapShotUI')
                if ui_inst:
                    ui_inst.show()
                global_data.ui_mgr.get_ui('SceneSnapShotUI').take_scene_snapshot()
            elif top_mat == 'EXIT':
                global_data.ui_mgr.set_all_ui_visible(True)
                global_data.touch_mgr_agent.enable_touch_event()
        if pass_time > self.slerp_target_time and len(self.slerp_action_list) <= 0:
            self.on_exit_focus()

    def on_exit_focus(self):
        if not self._has_exited:
            self._has_exited = True
            global_data.game_mgr.set_global_speed_rate(1)
            self.set_target_focus_status(False)
            if self._global_speed_rate <= 0:
                self.resume_stoped_entities()
            global_data.emgr.screen_locker_event.emit(False, 3.5)
            global_data.emgr.enable_camera_yaw.emit(True)
            global_data.emgr.camera_switch_collision_check_event.emit(True)
            global_data.ui_mgr.set_all_ui_visible(True)
            global_data.touch_mgr_agent.enable_touch_event()
            self.unreigster_timer()
            global_data.emgr.set_in_killer_focus_camera_event.emit(False)

    def on_exit(self):
        self.on_exit_focus()
        self._focus_id = None
        ui_inst = global_data.ui_mgr.get_ui('SceneSnapShotUI')
        if ui_inst:
            ui_inst.hide()
        self.unreigster_timer()
        return

    def destroy(self):
        self.on_exit()

    def unreigster_timer(self):
        if self._timer_id is not None:
            global_data.game_mgr.get_logic_timer().unregister(self._timer_id)
            self._timer_id = None
        return