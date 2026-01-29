# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/JudgeCameraController.py
from __future__ import absolute_import
import six
from six.moves import range
import game
import world
import math3d
from logic.vscene.parts.keyboard.CameraDirectionKeyboardHelper import CameraDirectionKeyboardHelper
from common.framework import Singleton
import math
from logic.gcommon.common_const.collision_const import GROUP_DEFAULT_VISIBLE, GROUP_STATIC_SHOOTUNIT
from logic.gcommon.common_const import spectate_const as sp_const
import time
MAX_CAMERA_HEIGHT = 4000

class CameraCollisionObject(object):

    def __init__(self, bdict):
        import world
        import collision
        scn_col = world.get_active_scene().scene_col if world.get_active_scene() else None
        if scn_col:
            self.radius = bdict.get('range', 0)
            self._col_obj = collision.col_object(collision.SPHERE, math3d.vector(self.radius, 0, 0), 0, 0, 1)
            self._col_obj.mask = GROUP_STATIC_SHOOTUNIT
            self._col_obj.group = GROUP_DEFAULT_VISIBLE
            self._pos = math3d.vector(*bdict['position'])
            self._col_obj.position = self._pos
            self._col_obj.set_damping(0.4, 0.4)
            self._col_obj.disable_gravity(True)
            self._col_obj.enable_ccd = True
            scn_col.add_object(self._col_obj)
        else:
            log_error('CameraCollisionObject create col failed!!!!')
        return

    def move_collision(self, speed):
        self._col_obj.set_linear_velocity(speed)

    def stop_move(self):
        self._col_obj.mass = 0

    def start_move(self):
        self._col_obj.mass = 1.0

    def _get_col_character(self):
        return self._col_obj

    def set_col_off(self):
        if not self._col_obj:
            return
        self._hide = True
        self._col_obj.group = 0
        self._col_obj.mask = 0

    def set_col_on(self):
        if not self._col_obj:
            return
        self._hide = False
        self._col_obj.group = GROUP_DEFAULT_VISIBLE
        self._col_obj.mask = GROUP_STATIC_SHOOTUNIT

    def destroy(self):
        scn_col = world.get_active_scene().scene_col if world.get_active_scene() else None
        if scn_col:
            if self._col_obj:
                scn_col.remove_object(self._col_obj)
            self._col_obj = None
        return

    def get_pos(self):
        if self._col_obj:
            return self._col_obj.position
        else:
            return None
            return None

    def set_pos(self, pos):
        if self._col_obj:
            self._col_obj.position = pos


class PositionChecker(object):

    def __init__(self):
        self.update_from_config_data()

    def destroy(self):
        pass

    def check_is_in_boundary(self, pos):
        if not (self._min_x <= pos.x <= self._max_x and self._min_z <= pos.z <= self._max_z):
            return False
        else:
            return True

    def update_from_config_data(self):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        self._default_ll_pos = [-350 * NEOX_UNIT_SCALE, -600 * NEOX_UNIT_SCALE]
        self._default_ru_pos = [480 * NEOX_UNIT_SCALE, 390 * NEOX_UNIT_SCALE]
        battle = global_data.battle
        move_range = battle.get_move_range()
        if move_range:
            if len(move_range) == 2:
                self._min_x = min(move_range[0][0], move_range[1][0])
                self._max_x = max(move_range[0][0], move_range[1][0])
                self._min_z = min(move_range[0][1], move_range[1][1])
                self._max_z = max(move_range[0][1], move_range[1][1])
            else:
                self._min_x = 100000
                self._min_z = 100000
                self._max_x = -100000
                self._max_z = -100000
                self._polygon_check_pos = move_range
                for idx in range(len(self._polygon_check_pos)):
                    check_pos = self._polygon_check_pos[idx]
                    if check_pos[0] > self._max_x:
                        self._max_x = check_pos[0]
                    if check_pos[0] < self._min_x:
                        self._min_x = check_pos[0]
                    if check_pos[1] > self._max_z:
                        self._max_z = check_pos[1]
                    if check_pos[1] < self._min_z:
                        self._min_z = check_pos[1]

        else:
            from common.cfg import confmgr
            map_id = battle.map_id
            conf = confmgr.get('map_config', str(map_id), default={})
            l_pos = conf.get('walkLowerLeftPos', self._default_ll_pos)
            r_pos = conf.get('walkUpRightPos', self._default_ru_pos)
            self._min_x = l_pos[0]
            self._max_x = r_pos[0]
            self._min_z = l_pos[1]
            self._max_z = r_pos[1]


class JudgeCameraController(Singleton):
    ALIAS_NAME = 'judge_camera_mgr'

    def init(self):
        self._camera_direction_helper = CameraDirectionKeyboardHelper()
        self._is_enable = False
        self.update_timer_id = None
        self._cameraCollisionObject = None
        self._scope_old_value = None
        self._last_sync_pos = None
        self._last_valid_pos = None
        self._camera_mat_when_enabled = None
        self.need_reset_to_start_pos = False
        self._is_waiting_for_cam_entity = False
        self._last_disable_time = 0
        self._move_direction_generator = None
        global_data.camera_freefly_speed = 2
        from data import hot_key_def
        self.quick_trk_key_list = {hot_key_def.JUDGE_CAMERA_FORWARD: game.VK_W,hot_key_def.JUDGE_CAMERA_BACKWARD: game.VK_S,
           hot_key_def.JUDGE_CAMERA_LEFT: game.VK_A,
           hot_key_def.JUDGE_CAMERA_RIGHT: game.VK_D,
           hot_key_def.JUDGE_CAMERA_UP: game.VK_NUM4,
           hot_key_def.JUDGE_CAMERA_DOWN: game.VK_NUM1
           }
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        global_data.emgr.net_reconnect_event += self.on_login_reconnect
        self._pos_checker = PositionChecker()
        return

    def on_finalize(self):
        self._move_direction_generator = None
        self.disable(is_destroy=True)
        self.stop_timer()
        self._camera_direction_helper.destroy()
        self._camera_direction_helper = None
        if self._cameraCollisionObject:
            self._cameraCollisionObject.destroy()
            self._cameraCollisionObject = None
        if self._pos_checker:
            self._pos_checker.destroy()
            self._pos_checker = None
        return

    def stop_timer(self):
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = None
        return

    def check_can_enable(self):
        if not global_data.player:
            return False
        if global_data.player.is_in_judge_ob():
            cur_time = time.time()
            if cur_time - self._last_disable_time < 5:
                global_data.game_mgr.show_tip(get_text_by_id(19603))
                return False
        return True

    def enable(self):
        self.init_keyboard_ctrl()
        self._camera_direction_helper.reset()
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 1)
        touch_mgr = global_data.touch_mgr_agent
        touch_mgr.register_wheel_event(self.__class__.__name__, self.on_mouse_scroll)
        camera_pos = global_data.game_mgr.scene.active_camera.world_position
        self._camera_mat_when_enabled = global_data.game_mgr.scene.active_camera.world_transformation
        from data.camera_state_const import JUDGE_MODE
        global_data.emgr.switch_camera_state_event.emit(JUDGE_MODE)
        self._is_enable = True
        self._is_waiting_for_cam_entity = False
        self._last_sync_pos = camera_pos
        self._last_valid_pos = camera_pos
        global_data.emgr.set_observe_target_id_event.emit(None, True)
        global_data.emgr.switch_cam_state_enable_event.emit(False)
        global_data.emgr.camera_switch_collision_check_event.emit(False)
        global_data.emgr.camera_added_trk_enable.emit(False)
        if not self._cameraCollisionObject:
            camera_pos_tuple = [
             camera_pos.x, camera_pos.y, camera_pos.z]
            self._cameraCollisionObject = CameraCollisionObject({'range': 10,'position': camera_pos_tuple})
        global_data.emgr.enable_target_pos_update_flag_event.emit(True)
        global_data.emgr.enable_special_target_pos_logic_for_judge.emit(True)
        global_data.emgr.set_target_pos_for_special_logic.emit(camera_pos)
        if self._cameraCollisionObject:
            self._cameraCollisionObject.set_pos(camera_pos)
            self._cameraCollisionObject.set_col_on()
        from logic.gutils.pc_ui_utils import MOBILE_2_PC_UI_DICT, PC_2_MOBILE_UI_DICT
        white_ls = [
         'SmallMapUI', 'BigMapUI', 'ScopePlayerUI', 'JudgeObserveUINew', 'NoticeUI', 'BattleReconnectUI', 'NormalConfirmUI2', 'JudgeObSettleUI', 'EndTransitionUI', 'SurviveInfoUI', 'SurviveInfoUIPC',
         'TopLevelConfirmUI2', 'SecondConfirmDlg2', 'ExitConfirmDlg', 'BusyReconnectBg', 'MainSettingUI', 'PickUI', 'GVGTopScoreJudgeUI', 'GVGScoreDetailsUI', 'FFABeginCountDown', 'FFAFinishCountDown',
         'ObserveUI', 'BattleSceneOnlyUI']
        for ui_name in white_ls:
            if ui_name in MOBILE_2_PC_UI_DICT:
                white_ls.append(MOBILE_2_PC_UI_DICT[ui_name])

        global_data.ui_mgr.add_ui_show_whitelist(white_ls, self.__class__.__name__)
        from common.framework import Functor
        if global_data.pc_ctrl_mgr:
            for hotkey_func_name, mapped_key in six.iteritems(self.quick_trk_key_list):
                global_data.pc_ctrl_mgr.process_custom_key_binding(hotkey_func_name, Functor(self.on_quick_key, mapped_key=mapped_key), True)

        _scope_old_value = global_data.emgr.switch_judge_scope_show_event.emit(True)
        if type(_scope_old_value) in [list, tuple] and len(_scope_old_value) >= 1:
            self._scope_old_value = _scope_old_value[0]
        else:
            self._scope_old_value = _scope_old_value
        if global_data.game_mgr.scene:
            global_data.game_mgr.scene.set_view_range(1, 10000)
        if global_data.player:
            global_data.player.req_ob_operate_god_camera(sp_const.GLOBAL_SPECTATE_OB_GOD_CAMERA_OPER_ENTER, {'pos': [camera_pos.x, camera_pos.y, camera_pos.z]})
        return

    def disable(self, is_destroy=False):
        if not self._is_enable:
            return
        else:
            if global_data.player:
                global_data.player.req_ob_operate_god_camera(sp_const.GLOBAL_SPECTATE_OB_GOD_CAMERA_OPER_LEAVE, {})
            if not is_destroy:
                if not self.check_can_recover_to_cam_player():
                    self._is_waiting_for_cam_entity = True
                    return
            self._is_waiting_for_cam_entity = False
            self.recover_keyboard_ctrl()
            self._camera_direction_helper.reset()
            if self._cameraCollisionObject:
                self._cameraCollisionObject.move_collision(math3d.vector(0, 0, 0))
            self.stop_timer()
            self._last_sync_pos = None
            touch_mgr = global_data.touch_mgr_agent
            touch_mgr.unregister_wheel_event(self.__class__.__name__)
            if global_data.player and global_data.player.logic:
                tid = global_data.player.logic.ev_g_spectate_target_id()
                if tid:
                    global_data.emgr.set_observe_target_id_event.emit(tid)
                else:
                    global_data.emgr.set_observe_target_id_event.emit(None, True, global_data.player.logic)
                global_data.emgr.switch_cam_state_enable_event.emit(True)
                global_data.emgr.recover_observe_camera_event.emit()
                global_data.emgr.camera_switch_collision_check_event.emit(True)
                global_data.emgr.camera_added_trk_enable.emit(True)
            if global_data.cam_lplayer:
                cam_lpos = global_data.cam_lplayer.ev_g_position()
                if cam_lpos:
                    global_data.emgr.set_target_pos_for_special_logic.emit(cam_lpos)
            global_data.emgr.enable_special_target_pos_logic_for_judge.emit(False)
            self._is_enable = False
            self._last_disable_time = time.time()
            if self._cameraCollisionObject:
                self._cameraCollisionObject.set_col_off()
            global_data.ui_mgr.remove_ui_show_whitelist(self.__class__.__name__)
            if global_data.pc_ctrl_mgr:
                for hotkey_func_name, mapped_key in six.iteritems(self.quick_trk_key_list):
                    global_data.pc_ctrl_mgr.process_custom_key_binding(hotkey_func_name, None, False)

            if self._scope_old_value is not None:
                global_data.emgr.switch_judge_scope_show_event.emit(self._scope_old_value)
                self._scope_old_value = None
            return

    def check_can_recover_to_cam_player(self):
        if global_data.player and global_data.player.logic:
            tid = global_data.player.logic.ev_g_spectate_target_id()
            if not tid:
                return True
            from mobile.common.EntityManager import EntityManager
            ent = EntityManager.getentity(tid)
            if ent and ent.logic:
                return True
        return False

    def remove_ui_block(self):
        global_data.ui_mgr.remove_ui_show_whitelist(self.__class__.__name__)

    def is_enable(self):
        return self._is_enable

    def init_keyboard_ctrl(self):
        pass

    def recover_keyboard_ctrl(self):
        pass

    def on_quick_key(self, msg, keycode, mapped_key):
        if msg == game.MSG_KEY_DOWN:
            self.on_quick_key_down(msg, mapped_key)
        else:
            self.on_quick_key_up(msg, mapped_key)

    def on_quick_key_down(self, msg, keycode):
        self._camera_direction_helper.move_key_func(msg, keycode)

    def on_quick_key_up(self, msg, keycode):
        self._camera_direction_helper.move_key_func(msg, keycode)

    def on_update(self):
        if self._is_waiting_for_cam_entity:
            if self.check_can_recover_to_cam_player():
                self.disable()
        if not self._is_enable:
            return
        if self.need_reset_to_start_pos:
            self.need_reset_to_start_pos = False
            pos = self._camera_mat_when_enabled.translation
            if self._cameraCollisionObject:
                self._cameraCollisionObject.set_pos(pos)
            yaw = self._camera_mat_when_enabled.yaw
            pitch = self._camera_mat_when_enabled.pitch
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(yaw, pitch, False, 0)
        if not self._move_direction_generator:
            move_dir = self._camera_direction_helper.get_move_direction()
        else:
            move_dir = self._move_direction_generator.get_move_direction()
            if move_dir:
                speed = self._move_direction_generator.get_move_speed()
                global_data.camera_freefly_speed = speed
            else:
                move_dir = self._camera_direction_helper.get_move_direction()
        if move_dir and move_dir.length > 0.001:
            move_dir.normalize()
            if global_data.camera_freefly_speed:
                speed = global_data.camera_freefly_speed
            else:
                speed = 1.0
            speed_vec = move_dir * global_data.game_mgr.scene.active_camera.world_rotation_matrix * speed * 100
            if self._cameraCollisionObject:
                self._cameraCollisionObject.move_collision(speed_vec)
                col_pos = self._cameraCollisionObject.get_pos()
                if col_pos:
                    new_col_pos = self.check_pos(col_pos)
                    self._cameraCollisionObject.set_pos(new_col_pos)
                    global_data.emgr.set_target_pos_for_special_logic.emit(new_col_pos)
                    self.check_sync_aoi_pos(new_col_pos)
        elif self._cameraCollisionObject:
            self._cameraCollisionObject.move_collision(math3d.vector(0, 0, 0))
            col_pos = self._cameraCollisionObject.get_pos()
            if col_pos:
                new_col_pos = self.check_pos(col_pos)
                self._cameraCollisionObject.set_pos(new_col_pos)
                global_data.emgr.set_target_pos_for_special_logic.emit(new_col_pos)
                self.check_sync_aoi_pos(new_col_pos)

    def check_pos(self, col_pos):
        if col_pos.y > MAX_CAMERA_HEIGHT:
            col_pos.y = MAX_CAMERA_HEIGHT
        if not self.check_is_in_boundary(col_pos):
            return self._last_valid_pos
        self._last_valid_pos = col_pos
        return col_pos

    def check_is_in_boundary(self, pos):
        return self._pos_checker.check_is_in_boundary(pos)

    def check_sync_aoi_pos(self, new_pos):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        if self._last_sync_pos and (new_pos - self._last_sync_pos).length < 100 * NEOX_UNIT_SCALE:
            return
        self._last_sync_pos = new_pos
        if global_data.player:
            global_data.player.req_ob_operate_god_camera(sp_const.GLOBAL_SPECTATE_OB_GOD_CAMERA_OPER_MOVE, {'pos': [new_pos.x, new_pos.y, new_pos.z]})

    def on_mouse_scroll(self, msg, delta, key_state):
        cur_speed = global_data.camera_freefly_speed
        if cur_speed is None:
            global_data.camera_freefly_speed = 2
        global_data.camera_freefly_speed += delta / 100.0
        global_data.camera_freefly_speed = min(max(1, global_data.camera_freefly_speed), 20.0)
        return

    def on_login_reconnect(self):
        if self._is_enable:
            self.update_timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 1)

    def set_move_direction_generator(self, move_direction_generator):
        self._move_direction_generator = move_direction_generator

    def reset_camera_to_original_pos(self):
        if self._camera_mat_when_enabled:
            self.need_reset_to_start_pos = True