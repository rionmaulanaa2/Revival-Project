# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/MoveRockerUI.py
from __future__ import absolute_import
import math3d
import world
from common.uisys.basepanel import BasePanel
from common.utils.cocos_utils import ccp
from data.camera_state_const import AIM_MODE
from logic.client.const.camera_const import POSTURE_GROUND
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon.cdata import status_config as st_const
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.common_const.animation_const import MOVE_STATE_WALK, MOVE_STATE_RUN
from logic.units.LAvatar import LAvatar
from logic.vscene.parts.ctrl.ShortcutFunctionalityMutex import claim_shortcut_functionality, unclaim_shortcut_functionality, movement_shortcut_names, drive_movement_shortcut_names
from logic.gutils.move_utils import can_move
UP_VECTOR = ccp(0, 1)
from common.const.uiconst import ROCKER_LAYER_ZORDER
from common.utils.ui_utils import get_scale
import logic.gcommon.common_const.animation_const as animation_const
import logic.gcommon.common_const.robot_animation_const as robot_animation_const
import time
import cc
import math3d
import math
from logic.gcommon.common_utils import parachute_utils
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
from logic.client.const.rocker_const import KEEP_RUNNING_ANGLE, RUNNING_ANGLE
from logic.gutils.client_unit_tag_utils import preregistered_tags
import math
TAN45 = 1.0
TAN30 = 0.577
MECH_WALK_BAR_PIC = [
 'gui/ui_res_2/battle/mech_main/mech_bar_rocker_nml.png',
 'gui/ui_res_2/battle/mech_main/mech_bar_rocker_sel.png',
 'gui/ui_res_2/battle/mech_main/mech_bar_rocker_nml.png']
MECH_RUN_BUTTON_PIC = ['gui/ui_res_2/battle/mech_main/mech_btn_rocker_nml.png',
 'gui/ui_res_2/battle/mech_main/mech_btn_rocker_sel.png',
 'gui/ui_res_2/battle/mech_main/mech_btn_rocker_nml.png']
WALK_BAR_PIC = [
 'gui/ui_res_2/battle/button/bar_rocker_nml.png',
 'gui/ui_res_2/battle/button/bar_rocker_nml.png',
 'gui/ui_res_2/battle/button/bar_rocker_nml.png']
RUN_BUTTON_PIC = ['gui/ui_res_2/battle/button/btn_rocker_nml.png',
 'gui/ui_res_2/battle/button/btn_rocker_choose.png',
 'gui/ui_res_2/battle/button/btn_rocker_nml.png']
KIZUNA_RUN_BUTTON_PIC = [
 'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/button/btn_rocker.png',
 'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/button/btn_rocker_click.png',
 'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/button/btn_rocker.png']
KEEP_RUNNING = [
 'gui/ui_res_2/battle/icon/human_keep_running.png', 'gui/ui_res_2/battle/icon/keep_running.png']
KEEP_RUNNING_SEL = ['gui/ui_res_2/battle/icon/human_keep_running_sel.png', 'gui/ui_res_2/battle/icon/keep_running_sel.png']
BAR_CION_NML = ['gui/ui_res_2/battle/icon/human_bar_cion_nml.png', 'gui/ui_res_2/battle/icon/bar_cion_nml.png']
BAR_CION_SEL = ['gui/ui_res_2/battle/icon/human_bar_cion_sel.png', 'gui/ui_res_2/battle/icon/bar_cion_sel.png']
LAB_RUNNING = ['gui/ui_res_2/battle/panel/pnl_lab_running.png', 'gui/ui_res_2/battle/panel/panel_lab_1.png']
ROCKER_MOVING = ['gui/ui_res_2/battle/icon/human_dec_rocker_moving.png', 'gui/ui_res_2/battle/icon/dec_rocker_moving.png']
from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
MECHA_MODE = 1
HUMAN_MODE = 2
from common.const import uiconst

class MoveRockerUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/rocker'
    DLG_ZORDER = ROCKER_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    LOCK_OFFSET = get_scale('35w')
    MOVE_OFFSET = get_scale('10w')
    TAG = 180423
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'set_move_rocker_opacity_event': 'set_move_rocker_opacity',
       'set_move_rocker_opacity_and_swallow_touch': 'set_move_rocker_opacity_and_swallow_touch',
       'enable_dynamic_switch_swallow_touch': 'enable_dynamic_switch_swallow_touch',
       'check_drive_control_continue_event': 'check_drive_control_continue'
       }

    def on_init_panel(self, *args, **kwargs):
        self._rocker_move_disable = False
        self.panel.setLocalZOrder(uoc.MOVE_LOCAL_ZORDER)
        self._non_mecha_run_button_pics = RUN_BUTTON_PIC
        self.touch_mock = TouchMock()
        self.touch_mock.setTouchId(10)
        self.touch_mock.setNeedAddStartPos(True)
        self.touch_mock_trigger = None
        self.init_rocker()
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {uoc.FIREROCKER_OPE_KEY: 'cur_rocker_ope_sel'})
        self.init_parameters()
        self.init_other_event()
        if global_data.player and global_data.player.logic:
            ctrl_target = global_data.player.logic.ev_g_control_target()
            if ctrl_target and ctrl_target.logic:
                self.on_player_setted(ctrl_target.logic)
        return

    def on_custom_template_create(self, *arg, **kwargs):
        super(MoveRockerUI, self).on_custom_template_create()
        if kwargs.get('need_kizuna'):
            self.PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/ai_dacall/ai_move'
        else:
            self.PANEL_CONFIG_NAME = 'battle/rocker'

    def init_parameters(self):
        self._ui_state = HUMAN_MODE
        self.is_highlight = False
        self._cur_touch_id = None
        self._last_finger_down_time = 0
        self.is_run_lock = False
        self.last_move_dir = None
        self.cur_rocker_dir = None
        self.cur_camera_state = None
        self.cur_rocker_ope_sel = None
        self.is_rocker_enable = False
        self.init_keep_running_area_pos = self.panel.nd_keep_running_area.getPosition()
        self.on_rocker_ope_sel_change_event(global_data.player.firerocker_ope_setting)
        self.is_can_run_lock = False
        self.run_lock_forbidden = False
        self.is_in_run_angle = False
        self.is_in_run_dir = False
        self.is_ui_can_run_lock = False
        self.last_move_state = animation_const.MOVE_STATE_STAND
        self.check_run_timer = None
        self.dynamic_switch_swallow_touch = False
        self.need_swallow_touch = True
        self.visible = True
        self.vehicle_pattern = False
        self.forward_factor = 0
        self.turn_offset_angle = 0
        self.turn_factor = 0
        self.max_turn_offset = 0
        self._is_in_touch_bottom = False
        self.last_vec = None
        self.is_rocking = False
        self.touch_begin_pos = None
        self.finger_move_list = []
        self.finger_up_list = []
        self.player = None
        self.finger_down = False
        scn = world.get_active_scene()
        player = scn.get_player()
        self.panel.setVisible(False)
        if player:
            self.on_player_setted(player)
        global_data.emgr.scene_player_setted_event += self.on_player_setted
        self.on_ctrl_target_changed()
        return

    def _on_reconnected(self, *args):
        if self.player:
            self.player.send_event('E_MOVE_STOP')
        self.last_move_state = animation_const.MOVE_STATE_STAND
        self.last_move_dir = None
        return

    def on_finalize_panel(self):
        self.touch_mock = None
        if self.get_is_run_lock():
            if global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_TRY_CANCEL_RUN_LOCK')
        self.destroy_touch_proxy()
        global_data.emgr.net_reconnect_before_destroy_event -= self._on_reconnected
        self.on_player_setted(None)
        if self.custom_ui_com:
            self.custom_ui_com.destroy()
            self.custom_ui_com = None
        self.clear_check_run_timer()
        return

    def clear_check_run_timer(self):
        if self.check_run_timer:
            self.panel.stopAction(self.check_run_timer)
        self.check_run_timer = None
        return

    def _get_controller_info(self):
        if self.player.MASK & preregistered_tags.MECHA_VEHICLE_TAG_VALUE:
            run_state = mecha_status_config.MC_RUN
            move_state = mecha_status_config.MC_MOVE
        else:
            run_state = st_const.ST_RUN
            move_state = st_const.ST_MOVE
        return (run_state, move_state)

    def check_run_lock(self):
        if not self.player:
            return
        run_state, move_state = self._get_controller_info()
        if self.is_run_lock and self.last_move_dir:
            is_can_run = self.player.ev_g_status_try_trans(run_state)
            if is_can_run:
                self.last_move_state = MOVE_STATE_RUN
            else:
                is_can_walk = self.player.ev_g_status_try_trans(move_state)
                if is_can_walk:
                    self.last_move_state = MOVE_STATE_WALK

    def check_move(self):
        if not self.player:
            return
        if not self.is_rocker_enable:
            return
        run_state, move_state = self._get_controller_info()
        if self.last_move_dir:
            if self.is_run_lock:
                is_can_run = self.player.ev_g_status_try_trans(run_state)
                if is_can_run:
                    self.last_move_state = MOVE_STATE_RUN
                    return
            is_can_walk = self.player.ev_g_status_try_trans(move_state)
            if is_can_walk:
                self.last_move_state = MOVE_STATE_WALK

    def on_player_setted(self, player, stop_rocker=True):
        self.unbind_ui_event(self.player)
        if stop_rocker:
            self.stop_rocker(False)
        self.player = player
        self._check_show_count_dict()
        if player:
            self.bind_ui_event(player)
            self.check_continue_run()
            import world
            scn = world.get_active_scene()
            if scn:
                part_cam = scn.get_com('PartCamera')
                if part_cam:
                    self.on_camera_switch_to_state(part_cam.get_cur_camera_state_type())
        class_name = player.__class__.__name__
        self.vehicle_pattern = False
        player and player.send_event('E_SET_ROCKER_RADIUS', self.spawn_radius / 0.9)
        if class_name == 'LMecha':
            self.on_part_disabled(player.sd.ref_is_paralyze)
            return
        if player and player.MASK & preregistered_tags.VEHICLE_TAG_VALUE:
            from logic.gcommon.common_const import mecha_const as mconst
            self.vehicle_pattern = player.ev_g_pattern() == mconst.MECHA_PATTERN_VEHICLE
            if self.vehicle_pattern:
                from common.cfg import confmgr
                vehicle_type = player.ev_g_vehicle_type()
                config = confmgr.get('vehicle_data2', str(vehicle_type))
                self.forward_factor = math.tan(math.radians(90 - config.get('forward_max_angle', 75)))
                self.turn_offset_angle = math.radians(config.get('turn_min_angle', 15))
                self.turn_factor = config.get('turn_offset_factor', 1)
                self.max_turn_offset = config.get('max_steer', 0.2)
                if global_data.player.get_setting_2(uoc.DRIVE_OPE_KEY) != uoc.DRIVE_OPE_ROCKER:
                    self.stop_rocker()
                elif self.finger_move_list:
                    touch_info = self.finger_move_list[0]
                    self.finger_move(touch_info)
            elif self.finger_move_list:
                touch_info = self.finger_move_list[0]
                self.finger_move(touch_info)
        self.on_part_disabled(False)
        self.run_lock_forbidden = False

    def check_continue_run(self):
        if not self.player:
            return
        if not self.is_run_lock:
            return
        last_move_dir = self.last_move_dir = math3d.vector(0, 0, 1)

        def check(pass_time):
            if not self.player:
                return
            if not self.is_run_lock:
                return
            if self.player.__class__.__name__ == 'LMechaTrans' and self.vehicle_pattern:
                if self.is_run_lock:
                    self.player.send_event('E_MOVE_FORWARD')
                self.clear_check_run_timer()
                return
            if self.player.MASK & preregistered_tags.MECHA_VEHICLE_TAG_VALUE:
                is_can_run = self.player.ev_g_status_check_pass(mecha_status_config.MC_RUN)
                is_can_walk = self.player.ev_g_status_check_pass(mecha_status_config.MC_MOVE)
                if is_can_run:
                    self.player.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_RUN)
                elif is_can_walk:
                    self.player.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_WALK)
            else:
                is_can_run = self.player.ev_g_status_check_pass(st_const.ST_RUN)
                is_can_walk = self.player.ev_g_status_check_pass(st_const.ST_MOVE)
            if is_can_run or is_can_walk:
                self.player.send_event('E_MOVE', last_move_dir)
                self.player.send_event('E_MOVE_ROCK', last_move_dir, True)
                self.clear_check_run_timer()

        self.clear_check_run_timer()
        self.check_run_timer = self.panel.TimerAction(check, 10, interval=0.1)

    def init_rocker(self):
        self.init_rocker_mapping()
        self.rocker_base_layer.SetNoEventAfterMove(False)
        self.update_spawn_radius()
        self.rocker_base_layer.set_sound_enable(False)
        self._layer_moved_dist = 0
        self.init_touch_proxy()
        if self._touch_proxy:
            self._touch_proxy.register_touch_layer(self.panel.layer_bottom, {'name': 'layer_bottom','bSwallow': False
               }, self.on_touch_bottom_begin, None, self.on_touch_bottom_end, self.on_touch_bottom_end)
            self._touch_proxy.register_touch_layer(self.panel.rocker_touch, {'name': 'rocker_touch','bSwallow': True
               }, self.on_rocker_touch_begin, self.on_rocker_touch_drag, self.on_rocker_touch_end, self.on_rocker_touch_cancel)

        @self.rocker_base_layer.callback()
        def OnBegin(layer, touch):
            return self.on_rocker_touch_begin(layer, touch)

        @self.rocker_base_layer.callback()
        def OnDrag(layer, touch):
            self.on_rocker_touch_drag(layer, touch, layer.GetMovedDistance())

        @self.rocker_base_layer.callback()
        def OnCancel(layer, touch):
            self.on_rocker_touch_cancel(layer, touch)

        @self.rocker_base_layer.callback()
        def OnEnd(layer, touch):
            self.on_rocker_touch_end(layer, touch)

        global_data.emgr.rocker_run_span_scale_event += self.on_rocker_run_scale_changed_event
        global_data.emgr.rocker_walk_span_scale_event += self.on_rocker_walk_scale_changed_event
        global_data.emgr.on_player_disable_rocker_move += self.on_disable_rocker_move
        self.span_center_pos = self.rocker_span_node.ConvertToWorldSpacePercentage(50, 50)
        self.local_center_pos = self.rocker_center_node.getPosition()
        keep_run_top_center_pos = self.panel.nd_keep_running_area.ConvertToWorldSpacePercentage(50, 100)
        self.keep_running_radius = keep_run_top_center_pos.y - self.span_center_pos.y

        @self.rocker_center_node.callback()
        def OnClick(btn, touch):
            self._try_cancel_run_lock()

        self.rocker_center_node.set_sound_enable(False)
        return

    @claim_shortcut_functionality(movement_shortcut_names + drive_movement_shortcut_names, 'MoveRockerUI')
    def on_rocker_touch_begin(self, nd, touch, is_mock=False):
        if self.dynamic_switch_swallow_touch:
            global_data.game_mgr.next_exec(lambda : self.finger_down and self.set_move_rocker_swallow_touch(self.need_swallow_touch))
        cur_touch_id = touch.getId()
        if self._cur_touch_id is None:
            self._cur_touch_id = cur_touch_id
            nd.SetPassedTouchId(cur_touch_id)
            world_pt = touch.getLocation()
            if global_data.moveKeyboardMgr:
                global_data.moveKeyboardMgr.stop_move_lock()
            self.rocker_start(world_pt)
            if not is_mock:
                global_data.emgr.on_touch_move_rocker_event.emit(touch)
            return True
        else:
            return True
            return

    def on_rocker_touch_drag(self, nd, touch, moved_dist):
        self._layer_moved_dist = moved_dist
        if moved_dist < self.MOVE_OFFSET:
            return
        touch_info = self.get_touch_info(touch)
        self.finger_move_list = [touch_info]
        self.finger_move(touch_info)

    @unclaim_shortcut_functionality(movement_shortcut_names + drive_movement_shortcut_names, 'MoveRockerUI')
    def on_rocker_touch_end(self, nd, touch):
        if not nd:
            return
        else:
            if self.dynamic_switch_swallow_touch:
                self.set_move_rocker_swallow_touch(False)
            self._layer_moved_dist = 0
            self._cur_touch_id = None
            nd.SetPassedTouchId(None)
            touch_info = self.get_touch_info(touch)
            self.finger_up(touch_info)
            return

    def on_rocker_touch_cancel(self, nd, touch):
        if self.dynamic_switch_swallow_touch:
            self.set_move_rocker_swallow_touch(False)
        self.on_rocker_touch_end(nd, touch)

    def on_disable_rocker_move(self, enable):
        self._rocker_move_disable = enable

    def get_touch_info(self, touch):
        touch_info = {'pos': touch.getLocation(),
           'id': touch.getId()
           }
        return touch_info

    def init_rocker_mapping(self):
        self.rocker_base_layer = self.panel.empty_button
        self.rocker_span_node = self.panel.run_bar
        self.rocker_dir_node = self.panel.direction
        self.rocker_center_node = self.panel.run_button

    def finger_move(self, move_info):
        from common.utils.cocos_utils import ccp
        if not self.is_rocker_enable:
            return
        else:
            pt = move_info.get('pos')
            self.calc_rocker_pos_in_span(pt)
            delta_vec = ccp(pt.x - self.touch_begin_pos.x, pt.y - self.touch_begin_pos.y)
            if delta_vec.length() > 0:
                self.player and self.player.send_event('E_SET_ROCKER_MOVE_DIST', delta_vec.length())
                delta_vec.normalize()
                if self.last_vec != delta_vec:
                    self.last_vec = delta_vec
                    angle = math.degrees(math.atan2(delta_vec.x, delta_vec.y))
                    self.rocker_dir_node.setVisible(True)
                    self.rocker_dir_node.setRotation(angle)
                    self.panel.dec_bar_running.setVisible(True)
                    self.panel.dec_bar_running.setRotation(angle)
                move_dir = self.screen_dir_to_move_dir(delta_vec)
                if self.player:
                    if not can_move():
                        self.start_delay_check()
                        return
                    key = '%s_finger_move' % self.player.__class__.__name__
                    func = getattr(self, key, None)
                    if func:
                        func(move_dir, pt)
            return

    def screen_dir_to_move_dir(self, screen_dir):
        v = math3d.vector(screen_dir.x, 0, screen_dir.y)
        return v

    def wark_area_is_point_in(self, touch_wpos):
        center_pos = self.panel.nd_wark_area.ConvertToWorldSpacePercentage(50, 50)
        w, h = self.panel.nd_wark_area.GetContentSize()
        tmp_vec = cc.Vec2(touch_wpos)
        tmp_vec.subtract(center_pos)
        finger_radius = tmp_vec.getLength()
        return finger_radius < w * 0.5

    def LAvatar_finger_move(self, move_dir, touch_wpos):
        run = not self.wark_area_is_point_in(touch_wpos)
        is_can_run = self.player.ev_g_status_check_pass(st_const.ST_RUN)
        is_can_walk = self.player.ev_g_status_check_pass(st_const.ST_MOVE)
        if run and self.is_in_run_angle:
            if is_can_run:
                self.last_move_state = MOVE_STATE_RUN
            elif is_can_walk:
                self.last_move_state = MOVE_STATE_WALK
            self.rocker_dir_node.setVisible(not self.is_can_run_lock)
            self.panel.dec_bar_running.setVisible(not self.is_can_run_lock)
            self.switch_dir_state(not self.is_can_run_lock)
        else:
            if is_can_walk:
                self.last_move_state = MOVE_STATE_WALK
            self.switch_dir_state(is_run=False)
        if is_can_run or is_can_walk:
            self.player.send_event('E_MOVE', move_dir)
        else:
            self.start_delay_check()
        self.player.send_event('E_MOVE_ROCK_STATE', run)
        self.player.send_event('E_MOVE_ROCK', move_dir, run and self.is_in_run_angle)
        self.last_move_dir = move_dir
        self.cur_rocker_dir = move_dir

    def LMechaTrans_chongci(self, flag):
        if flag:
            if not self.panel.isVisible():
                return
            if self.is_rocker_enable or self.is_run_lock:
                return
            center_pos = self.panel.nd_wark_area.ConvertToWorldSpacePercentage(50, 50)
            pt = cc.Vec2(center_pos.x, center_pos.y + 1000)
            self.rocker_start(center_pos)
            self.finger_move({'pos': pt})
            self.finger_up(None)
        return

    def set_run_lock_with_flag(self, lock_flag):
        if not lock_flag and global_data.player.get_setting_2(uoc.DRIVE_OPE_KEY) == uoc.DRIVE_OPE_ROCKER:
            if self.finger_move_list:
                touch_info = self.finger_move_list[0]
                self.finger_move(touch_info)
            return
        else:
            self.stop_rocker(True)
            if not lock_flag:
                return
            center_pos = self.panel.nd_wark_area.ConvertToWorldSpacePercentage(50, 50)
            offset = 1000
            pos_d = {'pos': cc.Vec2(center_pos.x, center_pos.y + offset)}
            self.rocker_start(center_pos)
            self.finger_move(pos_d)
            self.finger_up(None)
            return

    def LMotorcycle_finger_move(self, move_dir, touch_wpos):
        self.LMecha_finger_move(move_dir, touch_wpos)

    def LMechaTrans_finger_move(self, move_dir, touch_wpos):
        if not self.vehicle_pattern:
            self.LMecha_finger_move(move_dir, touch_wpos)
            return
        center_pos = self.panel.nd_wark_area.ConvertToWorldSpacePercentage(50, 50)
        w, h = self.panel.nd_wark_area.GetContentSize()
        tmp_vec = cc.Vec2(touch_wpos)
        tmp_vec.subtract(center_pos)
        x, y, radius = abs(tmp_vec.x), abs(tmp_vec.y), tmp_vec.getLength()
        vehicle_event = self.player.send_event
        if x * self.forward_factor < y:
            if tmp_vec.y > 0:
                vehicle_event('E_MOVE_FORWARD') if 1 else vehicle_event('E_MOVE_BACK')
                ratio = 3.5 * (radius / w) - 1.45
                ratio = max(min(ratio, 1.0), 0.3)
                vehicle_event('E_SET_MAX_OMEGA', ratio)
            else:
                vehicle_event('E_MOVE_NO_FORCE')
            angle = max(math.atan(x / max(y, 1.0)) - self.turn_offset_angle, 0)
            offset = min(angle * self.turn_factor, self.max_turn_offset)
            if tmp_vec.x < 0:
                offset *= -1
            vehicle_event('E_SET_TARGET_YAW_OFFSET', offset)
            self._is_in_touch_bottom or vehicle_event('E_ENABLE_VEHICLE_CAMERA_FOLLOW', True)

    def on_touch_bottom_begin(self, *args):
        self.enable_camera_follow(False)
        self._is_in_touch_bottom = True
        return True

    def on_touch_bottom_end(self, *args):
        self._is_in_touch_bottom = False

    def enable_camera_follow(self, enable):
        if self.vehicle_pattern:
            self.player.send_event('E_ENABLE_VEHICLE_CAMERA_FOLLOW', enable)

    def LMecha_finger_move(self, move_dir, touch_wpos):
        run = not self.wark_area_is_point_in(touch_wpos)
        is_can_run = self.player.ev_g_status_check_pass(mecha_status_config.MC_RUN)
        is_can_walk = self.player.ev_g_status_check_pass(mecha_status_config.MC_MOVE)
        in_run_state = run and (self.is_in_run_angle or self.player.sd.ref_support_all_direction_run)
        if in_run_state:
            if is_can_run:
                self.player.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_RUN)
                self.last_move_state = robot_animation_const.MOVE_STATE_RUN
            elif is_can_walk:
                self.player.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_WALK)
                self.last_move_state = robot_animation_const.MOVE_STATE_WALK
            self.rocker_dir_node.setVisible(not self.is_can_run_lock)
            self.panel.dec_bar_running.setVisible(not self.is_can_run_lock)
            self.switch_dir_state(not self.is_can_run_lock)
        else:
            if is_can_walk:
                self.player.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_WALK)
                self.last_move_state = robot_animation_const.MOVE_STATE_WALK
            self.switch_dir_state(is_run=False)
        if not is_can_run and not is_can_walk:
            self.start_delay_check()
        self.player.send_event('E_MOVE_ROCK', move_dir, in_run_state)
        if self.player.__class__.__name__ == 'LMotorcycle' and global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_driver():
            global_data.player.logic.send_event('E_MOVE_ROCK', move_dir, in_run_state)
        self.last_move_dir = move_dir
        self.cur_rocker_dir = move_dir

    def show_keep_running_icon(self):
        self.panel.nd_keep_running_area.setVisible(True)
        if self.cur_rocker_ope_sel == uoc.ALL_FIX_ROCKER:
            return
        max_y = global_data.ui_mgr.design_screen_size.height
        cur_pos = cc.Vec2(self.touch_begin_pos)
        cur_pos.y = cur_pos.y + self.keep_running_radius
        top = self.panel.nd_keep_running_area.ConvertToWorldSpacePercentage(50, 100)
        down = self.panel.nd_keep_running_area.ConvertToWorldSpacePercentage(50, 0)
        anchor_height = top.y - down.y
        cur_pos.y = min(max_y - anchor_height, cur_pos.y - anchor_height)
        lpos = self.panel.nd_keep_running_area.getParent().convertToNodeSpace(cur_pos)
        self.panel.nd_keep_running_area.setPosition(lpos)

    def calc_rocker_pos_in_span(self, finger_wpos):
        translate = ccp(finger_wpos.x - self.touch_begin_pos.x, finger_wpos.y - self.touch_begin_pos.y)
        trans_len = translate.getLength()
        self.is_can_run_lock = False
        self.is_in_run_angle = False
        if translate.y > 1 and not self.run_lock_forbidden:
            self.show_keep_running_icon()
        else:
            self.panel.nd_keep_running_area.setVisible(False)
        if self.cur_rocker_ope_sel != uoc.ALL_FIX_ROCKER:
            span_pos = self.touch_begin_pos
        else:
            span_pos = self.rocker_span_node.ConvertToWorldSpacePercentage(50, 50)
        tmp_vec = cc.Vec2(finger_wpos)
        tmp_vec.subtract(span_pos)
        finger_radius = tmp_vec.getLength()
        unit_trans = cc.Vec2(translate)
        angle = 0
        if unit_trans.getLength() > 0:
            unit_trans.normalize()
            angle = math.acos(min(max(unit_trans.dot(UP_VECTOR), -1), 1))
        if angle <= RUNNING_ANGLE / 2.0:
            self.is_in_run_angle = True
            if not self.run_lock_forbidden and finger_radius >= self.keep_running_radius and angle <= KEEP_RUNNING_ANGLE / 2.0:
                self.is_can_run_lock = True
                translate = ccp(unit_trans.x * (self.keep_running_radius - self.LOCK_OFFSET), unit_trans.y * (self.keep_running_radius - self.LOCK_OFFSET))
        if not self.is_can_run_lock and trans_len >= self.spawn_radius:
            translate = ccp(unit_trans.x * self.spawn_radius, unit_trans.y * self.spawn_radius)
        if self.is_can_run_lock:
            self.set_run_rocker_lock(True)
        else:
            self.set_run_rocker_lock(False)
        span_pos = self.rocker_span_node.ConvertToWorldSpacePercentage(50, 50)
        wpos = ccp(span_pos.x + translate.x, span_pos.y + translate.y)
        lpos = self.rocker_center_node.getParent().convertToNodeSpace(wpos)
        self.rocker_center_node.setPosition(lpos)

    def set_run_rocker_lock(self, lock):
        if lock == self.is_ui_can_run_lock:
            return
        self.is_ui_can_run_lock = lock
        if lock and self.player:
            self.player.send_event('E_MOVE_ROCK_STATE', True)
            self.player.send_event('E_CHANGE_SPEED')
        self.highlight_run_rocker_show(lock)
        if not lock:
            self.set_run_locker(False)

    def get_is_run_lock(self):
        return self.is_run_lock

    def highlight_run_rocker_show(self, is_highlight):
        index = 1 if self.is_mecha() else 0
        if is_highlight:
            self.rocker_center_node.SetSelect(True)
            self.panel.img_keep_running.SetDisplayFrameByPath('', KEEP_RUNNING_SEL[index])
            self.panel.icon_lock_bar.SetDisplayFrameByPath('', BAR_CION_SEL[index])
            self.panel.icon_lock.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/icon/icon_lock_sel.png')
        else:
            self.panel.img_keep_running.SetDisplayFrameByPath('', KEEP_RUNNING[index])
            self.panel.icon_lock_bar.SetDisplayFrameByPath('', BAR_CION_NML[index])
            self.panel.icon_lock.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/icon/icon_lock_nml.png')
            if not self.is_rocker_enable:
                self.rocker_center_node.SetSelect(False)

    def finger_up(self, up_info):
        self.panel.walk_bar.SetSelect(False)
        self.panel.rocker_light.setVisible(False)
        if self.is_run_lock:
            if self._layer_moved_dist < self.MOVE_OFFSET:
                return
        self.rocker_dir_node.setVisible(False)
        self.panel.dec_bar_running.setVisible(False)
        if self._ui_state == HUMAN_MODE:
            pic = ''
        else:
            pic = 'gui/ui_res_2/battle/mech_main/mech_icon_rocker_nml.png'
        self.panel.walk_dec1.setVisible(False)
        self.panel.walk_dec2.setVisible(False)
        self.panel.icon_rocker.SetDisplayFrameByPath('', pic)
        self.finger_down = False
        self.panel.StopAnimation('run')
        if self.is_can_run_lock:
            self.rocker_center_node.SetSelect(True)
        else:
            self.rocker_center_node.SetSelect(False)
        if self.is_rocker_enable:
            self.is_rocker_enable = False
            self._cur_touch_id = None
            func_name = '%s_finger_up' % self.player.__class__.__name__
            func = getattr(self, func_name, None)
            is_run_locker_success = False
            if func:
                is_run_locker_success = func()
            self.is_can_run_lock = False
            if is_run_locker_success:
                if self.is_run_lock:
                    self.panel.run_button.SetPosition('50%', '50%54')
                return
            self.panel.nd_keep_running_area.setVisible(False)
            self.rocker_center_node.setPosition(self.local_center_pos)
            self.stop_rocker()
        return

    def LAvatar_finger_up(self):
        if self.is_can_run_lock and self.player:
            self.set_run_locker(True)
            is_can_run = self.player.ev_g_status_check_pass(st_const.ST_RUN)
            is_can_move = self.player.ev_g_status_check_pass(st_const.ST_MOVE)
            return True
        return False

    def LDrone_finger_up(self):
        if self.is_can_run_lock and self.player:
            self.set_run_locker(False)
            return True
        return False

    def LMecha_finger_up(self):
        if self.is_can_run_lock and self.player:
            self.set_run_locker(True)
            is_can_run = self.player.ev_g_status_check_pass(mecha_status_config.MC_RUN)
            is_can_move = self.player.ev_g_status_check_pass(mecha_status_config.MC_MOVE)
            if is_can_run:
                self.player.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_RUN)
            elif is_can_move:
                self.player.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_WALK)
            return True
        return False

    def LMotorcycle_finger_up(self):
        return self.LMecha_finger_up()

    def LMechaTrans_finger_up(self):
        if not self.vehicle_pattern:
            return self.LMecha_finger_up()
        if self.is_can_run_lock and self.player:
            self.set_run_locker(True)
            return True
        vehicle_event = self.player.send_event
        vehicle_event('E_MOVE_NO_FORCE')
        vehicle_event('E_SET_TARGET_YAW_OFFSET', 0)
        vehicle_event('E_SET_MAX_OMEGA', 1.0)
        return False

    def stop_rocker(self, need_send=True):
        self.rocker_center_node.setPosition(self.local_center_pos)
        self.rocker_dir_node.setVisible(False)
        self.panel.dec_bar_running.setVisible(False)
        self.clear_finger_move()
        self.last_vec = None
        self.cur_rocker_dir = None
        self.is_rocker_enable = False
        self._cur_touch_id = None
        self.rocker_span_node.setVisible(False)
        self.last_move_state = animation_const.MOVE_STATE_STAND
        self.last_move_dir = None
        if need_send and self.player:
            self.check_send_move_stop()
        if self.is_can_run_lock:
            self.is_can_run_lock = False
        self.highlight_run_rocker_show(False)
        if self.is_run_lock:
            self.panel.nd_locking_running.setVisible(False)
            self.panel.nd_keep_running_area.setVisible(False)
        self.set_run_locker(False)
        return

    def check_send_move_stop(self):
        if not self.player:
            return
        self.player.send_event('E_ROCK_STOP')
        if self.player.__class__.__name__ == 'LMotorcycle':
            if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_driver():
                global_data.player.logic.send_event('E_ROCK_STOP')

    def rocker_start(self, pos):
        if not self.is_run_lock:
            self._last_finger_down_time = time.time()
            span_center = self.rocker_span_node.ConvertToWorldSpacePercentage(50, 50)
            npos = self.rocker_center_node.getParent().convertToNodeSpace(span_center)
            self.rocker_center_node.setPosition(npos)
        self.touch_begin_pos = pos
        self.is_rocker_enable = True
        if self.rocker_dir_node:
            self.rocker_dir_node.setVisible(False)
        self.panel.dec_bar_running.setVisible(False)
        self.rocker_center_node.setVisible(True)
        self.clear_finger_move()
        self.panel.walk_bar.SetSelect(True)
        self.panel.rocker_light.setVisible(True and self.is_mecha())
        if self._ui_state == HUMAN_MODE:
            pic = ''
        else:
            pic = 'gui/ui_res_2/battle/mech_main/mech_icon_rocker_sel.png'
            self.panel.walk_dec1.setVisible(True)
            self.panel.walk_dec2.setVisible(True)
        self.panel.icon_rocker.SetDisplayFrameByPath('', pic)
        self.finger_down = True
        self.rocker_center_node.SetSelect(True)

    def init_other_event(self):
        emgr = global_data.emgr
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state,
           'firerocker_ope_change_event': self.on_rocker_ope_sel_change_event,
           'scene_set_control_drone_event': self.on_player_setted,
           'avatar_reset_state_event': self.on_player_reset_state,
           'switch_control_target_event': self.on_ctrl_target_changed,
           'on_observer_try_use_drug': self.on_ctrl_use_drug,
           'set_run_lock_event': self.set_run_lock_with_flag
           }
        emgr.bind_events(econf)
        global_data.emgr.net_reconnect_before_destroy_event += self._on_reconnected

    def on_posture_stand(self, **kwargs):
        return
        is_break_run = True
        if kwargs:
            is_break_run = kwargs.get('is_break_run', True)
        if is_break_run:
            self._try_cancel_run_lock()

    def on_posture_squat(self, **kwargs):
        return
        is_break_run = True
        if kwargs:
            is_break_run = kwargs.get('is_break_run', True)
        if is_break_run:
            self._try_cancel_run_lock()

    def on_camera_switch_to_state(self, state, *args):
        if state == AIM_MODE:
            is_in_mecha = not isinstance(self.player, LAvatar)
            if is_in_mecha:
                self._try_cancel_run_lock()
        self.cur_camera_state = state

    def set_run_locker(self, is_lock):
        self.is_run_lock = is_lock
        if is_lock:
            self.panel.nd_keep_running_area.setVisible(False)
            self.panel.nd_locking_running.setVisible(True)
        else:
            self.panel.nd_locking_running.setVisible(False)
            if self.is_can_run_lock and self.is_rocker_enable:
                self.panel.nd_keep_running_area.setVisible(True)
            else:
                self.panel.nd_keep_running_area.setVisible(False)

    def switch_dir_state(self, is_run):
        if self.is_in_run_dir == is_run:
            return
        self.is_in_run_dir = is_run
        if is_run:
            self.rocker_dir_node.img_dir.setVisible(False)
            self.rocker_dir_node.img_dir1.setVisible(True)
            self.panel.PlayAnimation('run')
        else:
            self.rocker_dir_node.img_dir.setVisible(True)
            self.rocker_dir_node.img_dir1.setVisible(False)
            self.rocker_dir_node.img_dir2.setVisible(False)
            self.rocker_dir_node.img_dir3.setVisible(False)
            self.panel.StopAnimation('run')

    def check_move_direction(self, delta_vec):
        tan_value = TAN45
        if not self.player:
            return
        if self.player.share_data.ref_parachute_stage == parachute_utils.STAGE_PARACHUTE_DROP and delta_vec.y > 0:
            tan_value = TAN30
        abs_y = abs(delta_vec.y)
        abs_x = abs(delta_vec.x)
        if abs_y == 0 or abs_x / abs_y > tan_value:
            if delta_vec.x < 0:
                self.panel.left_dir.setVisible(True)
            elif delta_vec.x > 0:
                self.panel.right_dir.setVisible(True)
        elif delta_vec.y < 0:
            self.panel.down_dir.setVisible(True)
        elif delta_vec.y > 0:
            self.panel.up_dir.setVisible(True)

    def get_rocker_setting(self):
        self.run_scale = self.player.get_owner().read_local_setting(uoc.MR_RUN_KEY, uoc.MR_DEF_RUN_SPAN_SCALE)
        self.walk_scale = self.player.get_owner().read_local_setting(uoc.MR_WALK_KEY, uoc.MR_DEF_WALK_SPAN_SCALE)

    def on_rocker_run_scale_changed_event(self, scale):
        self.run_scale = scale
        self.rocker_span_node.setScale(scale)
        self.update_spawn_radius()

    def on_rocker_walk_scale_changed_event(self, scale):
        self.walk_scale = scale
        self.panel.walk_bar.setScale(scale)
        self.update_spawn_radius()

    def bind_ui_event(self, target):
        if target:
            target.regist_event('E_CTRL_JUMP', self.on_ctrl_target_jump)
            target.regist_event('E_CTRL_STAND', self.on_posture_stand)
            target.regist_event('E_CTRL_SQUAT', self.on_posture_squat)
            target.regist_event('E_TRY_FIRE', self.on_try_to_fire)
            target.regist_event('E_TRY_STOP_SKATE', self.on_try_stop_skate)
            target.regist_event('E_MOVE_STOP', self._on_move_stop)
            target.regist_event('E_MECHA_PARALYZE', self.on_part_disabled)
            target.regist_event('E_SET_ACTION_VISIBLE', self.on_action_ui_show)
            self.on_action_ui_show('MoveRocker', True)
            self.reset_move_rocker_opacity_and_swallow_touch()
            self.set_move_rocker_opacity_and_swallow_touch(255, True)
            target.regist_event('E_SUCCESS_BOARD', self.on_success_board)
            target.regist_event('E_CHONGCI', self.LMechaTrans_chongci)
            target.regist_event('E_ACTION_CANCEL_RESCUE', self.cancel_rescue)
            target.regist_event('E_TRY_CANCEL_RUN_LOCK', self._try_cancel_run_lock)
            target.regist_event('E_FORBID_RUN_LOCK', self.forbid_run_lock)
            target.regist_event('E_ON_FROZEN', self._on_frozen)
            self.dynamic_switch_swallow_touch = bool(target.share_data.ref_dynamic_switch_move_rocker_swallow_touch)
            if self.dynamic_switch_swallow_touch:
                self.set_move_rocker_swallow_touch(False)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            target.unregist_event('E_CTRL_JUMP', self.on_ctrl_target_jump)
            target.unregist_event('E_CTRL_STAND', self.on_posture_stand)
            target.unregist_event('E_CTRL_SQUAT', self.on_posture_squat)
            target.unregist_event('E_TRY_FIRE', self.on_try_to_fire)
            target.unregist_event('E_TRY_STOP_SKATE', self.on_try_stop_skate)
            target.unregist_event('E_MOVE_STOP', self._on_move_stop)
            target.unregist_event('E_MECHA_PARALYZE', self.on_part_disabled)
            target.unregist_event('E_SET_ACTION_VISIBLE', self.on_action_ui_show)
            target.unregist_event('E_SUCCESS_BOARD', self.on_success_board)
            target.unregist_event('E_CHONGCI', self.LMechaTrans_chongci)
            target.unregist_event('E_ACTION_CANCEL_RESCUE', self.cancel_rescue)
            target.unregist_event('E_TRY_CANCEL_RUN_LOCK', self._try_cancel_run_lock)
            target.unregist_event('E_FORBID_RUN_LOCK', self.forbid_run_lock)
            target.unregist_event('E_ON_FROZEN', self._on_frozen)

    def cancel_rescue(self, *args, **kargs):
        self.check_continue_run()

    def _on_frozen(self, frozen, *args):
        if not frozen:
            self.check_continue_run()

    def on_success_board(self, *args, **kargs):
        self.check_continue_run()

    def _on_move_stop(self, *args):
        if self.player:
            self.start_delay_check()

    def start_delay_check(self):
        if self.is_rocker_enable and self.finger_move_list:

            def check():
                if self.finger_move_list and self.is_rocker_enable:
                    self.finger_move(self.finger_move_list[0])

            self.panel.SetTimeOut(0.1, lambda : check(), tag=self.TAG)

    def forbid_run_lock(self, flag):
        self.run_lock_forbidden = flag

    def _try_cancel_run_lock(self):
        if self.is_run_lock:
            if not self.is_rocker_enable:
                self.rocker_center_node.setPosition(self.local_center_pos)
                self.check_send_move_stop()
            self.highlight_run_rocker_show(False)
            self.set_run_locker(False)

    def on_ctrl_target_jump(self, *args):
        pass

    def on_try_to_fire(self, *args):
        return
        if self.player.ev_g_is_in_mecha():
            self._try_cancel_run_lock()

    def on_ctrl_use_drug(self, *args):
        pass

    def on_try_stop_skate(self, *args):
        self._try_cancel_run_lock()

    def update_spawn_radius--- This code section failed: ---

1083       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'rocker_span_node'
           6  LOAD_ATTR             1  'getScale'
           9  CALL_FUNCTION_0       0 
          12  STORE_FAST            1  'span_scale'

1084      15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'rocker_center_node'
          21  LOAD_ATTR             1  'getScale'
          24  CALL_FUNCTION_0       0 
          27  STORE_FAST            2  'rocker_scale'

1085      30  LOAD_FAST             0  'self'
          33  LOAD_ATTR             0  'rocker_span_node'
          36  LOAD_ATTR             3  'ConvertToWorldSpacePercentage'
          39  LOAD_CONST            1  100
          42  LOAD_CONST            2  50
          45  CALL_FUNCTION_2       2 
          48  LOAD_ATTR             4  'x'
          51  STORE_FAST            3  'max_width'

1086      54  LOAD_FAST             0  'self'
          57  LOAD_ATTR             0  'rocker_span_node'
          60  LOAD_ATTR             3  'ConvertToWorldSpacePercentage'
          63  LOAD_CONST            2  50
          66  LOAD_CONST            2  50
          69  CALL_FUNCTION_2       2 
          72  LOAD_ATTR             4  'x'
          75  STORE_FAST            4  'mid_width'

1087      78  LOAD_CONST            3  0.9
          81  LOAD_FAST             3  'max_width'
          84  LOAD_FAST             4  'mid_width'
          87  BINARY_SUBTRACT  
          88  BINARY_MULTIPLY  
          89  STORE_FAST            5  'local_radius'

1088      92  LOAD_GLOBAL           5  'getattr'
          95  LOAD_GLOBAL           4  'x'
          98  LOAD_CONST            0  ''
         101  CALL_FUNCTION_3       3 
         104  STORE_FAST            6  'player'

1089     107  LOAD_FAST             6  'player'
         110  JUMP_IF_FALSE_OR_POP   132  'to 132'
         113  LOAD_FAST             6  'player'
         116  LOAD_ATTR             7  'send_event'
         119  LOAD_CONST            5  'E_SET_ROCKER_RADIUS'
         122  LOAD_FAST             3  'max_width'
         125  LOAD_FAST             4  'mid_width'
         128  BINARY_SUBTRACT  
         129  CALL_FUNCTION_2       2 
       132_0  COME_FROM                '110'
         132  POP_TOP          

1090     133  LOAD_FAST             5  'local_radius'
         136  LOAD_FAST             0  'self'
         139  STORE_ATTR            8  'spawn_radius'

1093     142  LOAD_FAST             0  'self'
         145  LOAD_ATTR             9  'panel'
         148  LOAD_ATTR            10  'run_bar'
         151  LOAD_ATTR             3  'ConvertToWorldSpacePercentage'
         154  LOAD_CONST            1  100
         157  LOAD_CONST            2  50
         160  CALL_FUNCTION_2       2 
         163  LOAD_ATTR            11  'y'
         166  STORE_FAST            3  'max_width'

1094     169  LOAD_FAST             0  'self'
         172  LOAD_ATTR             9  'panel'
         175  LOAD_ATTR            10  'run_bar'
         178  LOAD_ATTR             3  'ConvertToWorldSpacePercentage'
         181  LOAD_CONST            2  50
         184  LOAD_CONST            2  50
         187  CALL_FUNCTION_2       2 
         190  LOAD_ATTR            11  'y'
         193  STORE_FAST            4  'mid_width'

1095     196  LOAD_FAST             3  'max_width'
         199  LOAD_FAST             4  'mid_width'
         202  BINARY_SUBTRACT  
         203  LOAD_FAST             0  'self'
         206  STORE_ATTR           12  'run_bar_radius'
         209  LOAD_CONST            0  ''
         212  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 101

    def on_rocker_ope_sel_change_event(self, new_ope_sel):
        if self.cur_rocker_ope_sel != new_ope_sel:
            self.cur_rocker_ope_sel = new_ope_sel
            if self.cur_rocker_ope_sel in [uoc.FIXED_FIREROCKER, uoc.MOVABLE_FIREROCKER]:
                self.panel.empty_button.setContentSize(self.panel.nd_large.getContentSize())
                self.panel.empty_button.setPosition(self.panel.nd_large.getPosition())
                self.panel.empty_button.SetEnableTouch(False)
                if self._touch_proxy:
                    self._touch_proxy.set_touch_nd_visible('rocker_touch', True)
            else:
                self.panel.empty_button.setContentSize(self.panel.nd_small.getContentSize())
                self.panel.empty_button.setPosition(self.panel.nd_small.getPosition())
                self.panel.empty_button.SetEnableTouch(True)
                if self._touch_proxy:
                    self._touch_proxy.set_touch_nd_visible('rocker_touch', False)
            if self.cur_rocker_ope_sel == uoc.ALL_FIX_ROCKER:
                self.panel.nd_keep_running_area.setPosition(self.init_keep_running_area_pos)
        if self.custom_ui_com:
            self.custom_ui_com.refresh_all_custom_ui_conf()

    def get_move_dir(self):
        return self.cur_rocker_dir

    def on_change_ui_custom_data(self):
        span_center_pos = self.rocker_span_node.ConvertToWorldSpacePercentage(50, 50)
        keep_run_top_center_pos = self.panel.nd_keep_running_area.ConvertToWorldSpacePercentage(50, 100)
        self.keep_running_radius = keep_run_top_center_pos.y - span_center_pos.y
        self.touch_mock.setTouchStartPos(self.panel.run_button.ConvertToWorldSpacePercentage(50, 50))

    def change_ui_data(self):
        nd = getattr(self.panel, 'nd_custom')
        scale = nd.getScale()
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        return (
         w_pos, scale, 'nd_step_2')

    def on_player_reset_state(self):
        if global_data.mecha:
            return
        self.stop_rocker(False)

    def clear_finger_move(self):
        self.finger_move_list = []

    def on_part_disabled(self, enable):
        self.panel.img_broken.setVisible(enable)

    def show(self):
        super(MoveRockerUI, self).show()
        self.visible = True

    def hide(self):
        super(MoveRockerUI, self).hide()
        self.visible = False

    def on_action_ui_show(self, action, visible, force=False):
        if action == 'MoveRocker' and self.visible ^ visible:
            if visible:
                self.show()
            else:
                self.hide()

    def switch_to_mecha(self):
        self._ui_state = MECHA_MODE
        self.panel.walk_bar.SetFrames('', MECH_WALK_BAR_PIC, False, None)
        self.panel.run_button.SetFrames('', MECH_RUN_BUTTON_PIC, False, None)
        self.check_normal_pic()
        self.panel.PlayAnimation('show')
        UIDistorterHelper().apply_ui_distort(self.__class__.__name__)
        return

    def switch_to_non_mecha(self):
        self._ui_state = HUMAN_MODE
        self.panel.walk_bar.SetFrames('', WALK_BAR_PIC, False, None)
        self.panel.run_button.SetFrames('', self._non_mecha_run_button_pics, False, None)
        self.check_normal_pic()
        UIDistorterHelper().cancel_ui_distort(self.__class__.__name__)
        return

    def is_mecha(self):
        return self._ui_state == MECHA_MODE

    def on_ctrl_target_changed(self, *args):
        if not global_data.cam_lplayer:
            return
        is_pure_mecha = global_data.cam_lplayer.ev_g_is_pure_mecha()
        is_mecha = global_data.cam_lplayer.ev_g_in_mecha('Mecha')
        if is_mecha:
            self.switch_to_mecha()
        else:
            self.switch_to_non_mecha()
        self.replace_pic()
        if is_pure_mecha:
            if is_mecha:
                self.add_show_count('PURE_MECHA')
            else:
                self.add_hide_count('PURE_MECHA')

    def check_normal_pic(self):
        if self._ui_state == HUMAN_MODE:
            pic = ''
        else:
            pic = 'gui/ui_res_2/battle/mech_main/mech_icon_rocker_nml.png'
        self.panel.icon_rocker.SetDisplayFrameByPath('', pic)

    def replace_pic(self):
        index = 1 if self.is_mecha() else 0
        keep_running = KEEP_RUNNING_SEL if self.is_highlight else KEEP_RUNNING
        lock_bar = BAR_CION_SEL if self.is_highlight else BAR_CION_NML
        self.panel.img_keep_running.SetDisplayFrameByPath('', keep_running[index])
        self.panel.icon_lock_bar.SetDisplayFrameByPath('', lock_bar[index])
        self.panel.bar_running.SetDisplayFrameByPath('', LAB_RUNNING[index])
        self.panel.dec_bar_running.SetDisplayFrameByPath('', ROCKER_MOVING[index])
        self.panel.icon_rocker.setVisible(bool(index))

    def reset_vehicle_params(self, fa, toa, tof):
        self.forward_factor = math.tan(math.radians(90 - fa))
        self.turn_offset_angle = math.radians(toa)
        self.turn_factor = tof

    def init_touch_proxy(self):
        from logic.comsys.control_ui.MoveRockerTouchUI import MoveRockerTouchUI
        self._touch_proxy = MoveRockerTouchUI()

    def destroy_touch_proxy(self):
        global_data.ui_mgr.close_ui('MoveRockerTouchUI')
        self._touch_proxy = None
        return

    def do_hide_panel(self):
        super(MoveRockerUI, self).do_hide_panel()
        if self._touch_proxy:
            self._touch_proxy.add_hide_count(self.__class__.__name__)

    def do_show_panel(self):
        super(MoveRockerUI, self).do_show_panel()
        if self._touch_proxy:
            self._touch_proxy.add_show_count(self.__class__.__name__)

    def set_move_rocker_opacity(self, opacity):
        self.panel.SetEnableCascadeOpacityRecursion(True)
        self.panel.setOpacity(opacity)

    def set_move_rocker_swallow_touch(self, swallow_touch):
        if self._touch_proxy:
            self._touch_proxy.set_touch_layer_swallow_touch(swallow_touch)
        self.rocker_base_layer.SetSwallowTouch(swallow_touch)

    def reset_move_rocker_opacity_and_swallow_touch(self):
        self.set_move_rocker_opacity(255)
        self.set_move_rocker_swallow_touch(True)
        self.need_swallow_touch = True

    def set_move_rocker_opacity_and_swallow_touch(self, opacity, swallow_touch):
        self.set_move_rocker_opacity(opacity)
        if self.dynamic_switch_swallow_touch:
            self.finger_down and self.set_move_rocker_swallow_touch(swallow_touch)
        else:
            self.set_move_rocker_swallow_touch(swallow_touch)
        self.need_swallow_touch = swallow_touch

    def enable_dynamic_switch_swallow_touch(self, flag):
        self.dynamic_switch_swallow_touch = flag
        if flag and not self.finger_down:
            self.set_move_rocker_swallow_touch(False)

    def set_enable_custome_com(self, val):
        if self.custom_ui_com:
            self.custom_ui_com.set_enable(val)

    def set_human_run_button_pics(self, pics):
        self._non_mecha_run_button_pics = pics
        if self._ui_state == HUMAN_MODE:
            self.switch_to_non_mecha()

    def check_drive_control_continue(self):
        if self.vehicle_pattern:
            if global_data.player.get_setting_2(uoc.DRIVE_OPE_KEY) == uoc.DRIVE_OPE_ROCKER:
                if self.finger_move_list:
                    touch_info = self.finger_move_list[0]
                    self.finger_move(touch_info)

    def on_received_begin_command(self, move_vec):
        self.touch_mock.setTouchPos(None)
        if self.cur_rocker_ope_sel in [uoc.FIXED_FIREROCKER, uoc.MOVABLE_FIREROCKER]:
            if self._touch_proxy:
                self.touch_mock_trigger = self._touch_proxy.get_touch_nd('rocker_touch')
            else:
                self.touch_mock_trigger = None
        else:
            self.touch_mock_trigger = self.panel.empty_button
        if self.touch_mock_trigger:
            return self.on_rocker_touch_begin(self.touch_mock_trigger, self.touch_mock, is_mock=True)
        else:
            return

    def on_received_move_command(self, move_vec):
        self.touch_mock.setTouchPos(move_vec)
        if self.touch_mock_trigger:
            move_dist = 1000
            self.on_rocker_touch_drag(self.touch_mock_trigger, self.touch_mock, move_dist)

    def on_received_end_command(self):
        if self.touch_mock_trigger:
            self.on_rocker_touch_end(self.touch_mock_trigger, self.touch_mock)


from common.framework import Singleton

class MoveRockerSimpleFunction(Singleton):
    ALIAS_NAME = 'move_rocker_simple'
    MOVE_OFFSET = get_scale('10w')
    TAG = 220718

    def init(self):
        self.is_rocker_enable = False
        self.touch_begin_pos = None
        self.finger_down = False
        self.finger_move_list = []
        self._cur_touch_id = None
        self.last_move_dir = None
        self.cur_rocker_dir = None
        self.last_vec = None
        self.spawn_radius = 200
        self.last_move_state = animation_const.MOVE_STATE_STAND
        self.vehicle_pattern = False
        self.forward_factor = 0
        self.turn_offset_angle = 0
        self.turn_factor = 0
        self.max_turn_offset = 0
        self.player = None
        self.delay_tid = None
        if global_data.player and global_data.player.logic:
            ctrl_target = global_data.player.logic.ev_g_control_target()
            if ctrl_target and ctrl_target.logic:
                self.on_player_setted(ctrl_target.logic)
        return

    def init_player_bind(self):
        if global_data.player and global_data.player.logic:
            ctrl_target = global_data.player.logic.ev_g_control_target()
            if ctrl_target and ctrl_target.logic:
                self.on_player_setted(ctrl_target.logic)

    def on_finalize(self):
        self.clear()

    def clear(self):
        self.on_player_setted(None)
        self.clear_delay_timer()
        self.is_rocker_enable = False
        self.touch_begin_pos = None
        self.finger_down = False
        self.finger_move_list = []
        self._cur_touch_id = None
        self.last_move_dir = None
        self.cur_rocker_dir = None
        return

    def update_rocker_size(self, spawn_radius):
        self.spawn_radius = spawn_radius

    def on_player_setted(self, player, stop_rocker=True):
        if stop_rocker:
            self.stop_rocker(False)
        self.player = player
        self.vehicle_pattern = False
        player and player.send_event('E_SET_ROCKER_RADIUS', self.spawn_radius / 0.9)
        if player and player.MASK & preregistered_tags.VEHICLE_TAG_VALUE:
            from logic.gcommon.common_const import mecha_const as mconst
            self.vehicle_pattern = player.ev_g_pattern() == mconst.MECHA_PATTERN_VEHICLE
            if self.vehicle_pattern:
                from common.cfg import confmgr
                vehicle_type = player.ev_g_vehicle_type()
                config = confmgr.get('vehicle_data2', str(vehicle_type))
                self.forward_factor = math.tan(math.radians(90 - config.get('forward_max_angle', 75)))
                self.turn_offset_angle = math.radians(config.get('turn_min_angle', 15))
                self.turn_factor = config.get('turn_offset_factor', 1)
                self.max_turn_offset = config.get('max_steer', 0.2)
                if global_data.player.get_setting_2(uoc.DRIVE_OPE_KEY) != uoc.DRIVE_OPE_ROCKER:
                    self.stop_rocker()
                elif self.finger_move_list:
                    touch_info = self.finger_move_list[0]
                    self.finger_move(touch_info)
            elif self.finger_move_list:
                touch_info = self.finger_move_list[0]
                self.finger_move(touch_info)

    def clear_finger_move(self):
        self.finger_move_list = []

    def get_touch_info(self, touch):
        touch_info = {'pos': touch.getLocation(),
           'id': touch.getId()
           }
        return touch_info

    def rocker_start(self, pos):
        self.touch_begin_pos = pos
        self.is_rocker_enable = True
        self.clear_finger_move()
        self.finger_down = True
        if self.player:
            self.player.send_event('E_TRY_CANCEL_RUN_LOCK')

    @claim_shortcut_functionality(movement_shortcut_names + drive_movement_shortcut_names, 'MoveRockerFunction')
    def on_rocker_touch_begin(self, nd, touch):
        cur_touch_id = touch.getId() if touch else None
        if cur_touch_id is not None and self._cur_touch_id is None:
            self._cur_touch_id = cur_touch_id
            nd.SetPassedTouchId(cur_touch_id)
            world_pt = touch.getLocation()
            if global_data.moveKeyboardMgr:
                global_data.moveKeyboardMgr.stop_move_lock()
            self.rocker_start(world_pt)
            return True
        else:
            return True
            return

    def screen_dir_to_move_dir(self, screen_dir):
        v = math3d.vector(screen_dir.x, 0, screen_dir.y)
        return v

    def finger_move(self, move_info):
        from common.utils.cocos_utils import ccp
        if not self.is_rocker_enable:
            return
        else:
            pt = move_info.get('pos')
            delta_vec = ccp(pt.x - self.touch_begin_pos.x, pt.y - self.touch_begin_pos.y)
            if delta_vec.length() > 0:
                self.player and self.player.send_event('E_SET_ROCKER_MOVE_DIST', delta_vec.length())
                delta_vec.normalize()
                if self.last_vec != delta_vec:
                    self.last_vec = delta_vec
                    angle = math.degrees(math.atan2(delta_vec.x, delta_vec.y))
                move_dir = self.screen_dir_to_move_dir(delta_vec)
                if self.player:
                    if not can_move():
                        self.start_delay_check()
                        return
                    key = '%s_finger_move' % self.player.__class__.__name__
                    func = getattr(self, key, None)
                    if func:
                        func(move_dir, pt)
            return

    def on_rocker_touch_drag(self, nd, touch, moved_dist):
        if moved_dist < self.MOVE_OFFSET:
            return
        touch_info = self.get_touch_info(touch)
        self.finger_move_list = [touch_info]
        self.finger_move(touch_info)

    @unclaim_shortcut_functionality(movement_shortcut_names + drive_movement_shortcut_names, 'MoveRockerFunction')
    def on_rocker_touch_end(self, nd, touch):
        self._cur_touch_id = None
        if nd:
            nd.SetPassedTouchId(None)
        if not touch:
            return
        else:
            touch_info = self.get_touch_info(touch)
            self.finger_up(touch_info)
            return

    def finger_up(self, up_info):
        self.finger_down = False
        if self.is_rocker_enable:
            self.is_rocker_enable = False
            self._cur_touch_id = None
            func_name = '%s_finger_up' % self.player.__class__.__name__
            func = getattr(self, func_name, None)
            is_run_locker_success = False
            if func:
                is_run_locker_success = func()
            self.stop_rocker()
        return

    def start_delay_check(self):
        from common.utils.timer import CLOCK
        if self.is_rocker_enable and self.finger_move_list:

            def check():
                if self.finger_move_list and self.is_rocker_enable:
                    self.finger_move(self.finger_move_list[0])

            def check_wrap():
                self.delay_tid = None
                check()
                return

            self.clear_delay_timer()
            self.delay_tid = global_data.game_mgr.register_logic_timer(check_wrap, interval=0.1, times=1, mode=CLOCK)

    def clear_delay_timer(self):
        if self.delay_tid:
            global_data.game_mgr.unregister_logic_timer(self.delay_tid)
            self.delay_tid = None
        return

    def stop_rocker(self, need_send=True):
        self.clear_finger_move()
        self.last_vec = None
        self.cur_rocker_dir = None
        self.is_rocker_enable = False
        self._cur_touch_id = None
        self.last_move_state = animation_const.MOVE_STATE_STAND
        self.last_move_dir = None
        if need_send and self.player:
            self.check_send_move_stop()
        return

    def check_send_move_stop(self):
        if not self.player:
            return
        self.player.send_event('E_ROCK_STOP')
        if self.player.__class__.__name__ == 'LMotorcycle':
            if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_driver():
                global_data.player.logic.send_event('E_ROCK_STOP')

    def LMecha_finger_up(self):
        return False

    def LMechaTrans_finger_up(self):
        if not self.vehicle_pattern:
            return self.LMecha_finger_up()
        vehicle_event = self.player.send_event
        vehicle_event('E_MOVE_NO_FORCE')
        vehicle_event('E_SET_TARGET_YAW_OFFSET', 0)
        vehicle_event('E_SET_MAX_OMEGA', 1.0)
        return False

    def LMotorcycle_finger_move(self, move_dir, touch_wpos):
        self.LMecha_finger_move(move_dir, touch_wpos)

    def LMechaTrans_finger_move(self, move_dir, touch_wpos):
        if not self.vehicle_pattern:
            self.LMecha_finger_move(move_dir, touch_wpos)
            return

    def LMecha_finger_move(self, move_dir, touch_wpos):
        run = False
        is_can_run = self.player.ev_g_status_check_pass(mecha_status_config.MC_RUN)
        is_can_walk = self.player.ev_g_status_check_pass(mecha_status_config.MC_MOVE)
        in_run_state = False
        if in_run_state:
            if is_can_run:
                self.player.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_RUN)
                self.last_move_state = robot_animation_const.MOVE_STATE_RUN
            elif is_can_walk:
                self.player.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_WALK)
                self.last_move_state = robot_animation_const.MOVE_STATE_WALK
        elif is_can_walk:
            self.player.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_WALK)
            self.last_move_state = robot_animation_const.MOVE_STATE_WALK
        if not is_can_run and not is_can_walk:
            self.start_delay_check()
        self.player.send_event('E_MOVE_ROCK', move_dir, in_run_state)
        if self.player.__class__.__name__ == 'LMotorcycle' and global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_driver():
            global_data.player.logic.send_event('E_MOVE_ROCK', move_dir, in_run_state)
        self.last_move_dir = move_dir
        self.cur_rocker_dir = move_dir