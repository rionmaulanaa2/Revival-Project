# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/KizunaConcertViewUI.py
from __future__ import absolute_import
from six.moves import map
from common.const.uiconst import BASE_LAYER_ZORDER_1, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import battle_const
from data.hot_key_def import SUMMON_CALL_MECHA, OPEN_QUICK_SUMMON_PREVIEW, SUMMON_CALL_MECHA_CONFIRM
VIEW_BLOCK_HOTKEYS = [
 SUMMON_CALL_MECHA, OPEN_QUICK_SUMMON_PREVIEW, SUMMON_CALL_MECHA_CONFIRM]

class KizunaConcertViewUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/ai_dacall/ai_best_view'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_quit.OnClick': 'on_click_btn_quit',
       'btn_last.OnClick': 'on_click_btn_last',
       'btn_next.OnClick': 'on_click_btn_next',
       'btn_resolution.OnClick': 'on_click_btn_resolution'
       }
    MOUSE_CURSOR_TRIGGER_SHOW = True
    GLOBAL_EVENT = {'change_concert_song_data_event': 'on_update_concert_song_data_ex',
       'concert_video_stuck_event': 'show_reso_tips'
       }
    VIEW_CAMERAS = [
     [
      82340, 'cam_wutai', 60, (70, 50), (0, 0, 0)],
     [
      82351, 'cam_texie', 30, (25, 35), (-14, 88, -600)]]
    TOUCH_TAG = 20211013

    def on_init_panel(self, *args, **kwargs):
        super(KizunaConcertViewUI, self).on_init_panel()
        self.hide_main_ui(exceptions=('KizunaSongbarUI', 'KizunaLotteryWidgetUI'))
        self._song_idx = -1
        self.song_offset_dict = {}
        self.cur_song_offset = [0, 0, 0]
        self.view_slider = None
        self.VIEW_CAMERAS = [
         [
          82340, 'cam_wutai', 60, (70, 40), (0, 0, 0)],
         [
          82351, 'cam_texie', 60, (70, 40), (0, 0, 0)]]
        self.panel.btn_next.setVisible(len(self.VIEW_CAMERAS) > 1)
        self._camera_index = 0
        self._hfov = self.VIEW_CAMERAS[self._camera_index][2]
        VIEW_FOV_RANGE = self.VIEW_CAMERAS[self._camera_index][3]
        if global_data.battle:
            self._song_idx = global_data.battle.song_idx
        self._max_hfov = VIEW_FOV_RANGE[1]
        self._min_hfov = VIEW_FOV_RANGE[0]
        self.init_slider_component()
        self.enable()
        self.switch_into_cam_idx(self._camera_index)
        self.panel.PlayAnimation('show')
        self._is_disappear = False
        self.panel.nd_layer.BindMethod('OnBegin', lambda b, t: self.on_begin_touch_bg())
        self.panel.nd_layer.BindMethod('OnEnd', lambda b, t: self.on_end_touch_bg())
        self.start_disappear_countdown()
        from logic.gutils.ent_visibility_utils import EntSimpleVisibilityMgr
        self._ent_vis_mgr = EntSimpleVisibilityMgr()
        self._ent_vis_mgr.set_is_enable_control(True)
        self._ent_vis_mgr.hide_all_ent()
        self.panel.nd_tips.setVisible(False)
        global_data.emgr.into_concert_view_camera_event.emit(True)
        if global_data.pc_ctrl_mgr:
            for hotkey in VIEW_BLOCK_HOTKEYS:
                global_data.pc_ctrl_mgr.block_hotkey(hotkey, 'concert_view')

        return

    def start_disappear_countdown(self):
        self.panel.SetTimeOut(3.0, lambda : self.into_disappear(), tag=self.TOUCH_TAG)

    def into_disappear(self):
        if not self._is_disappear:
            self._is_disappear = True
            self.panel.StopAnimation('appear')
            self.panel.PlayAnimation('disappear')
            self.panel.nd_layer.SetSwallowTouch(True)

    def into_appear(self):
        if self._is_disappear:
            self._is_disappear = False
            self.panel.StopAnimation('disappear')
            self.panel.PlayAnimation('appear')
            self.start_disappear_countdown()
            self.panel.nd_layer.SetSwallowTouch(False)

    def on_end_touch_bg(self):
        self.start_disappear_countdown()

    def on_begin_touch_bg(self):
        if self._is_disappear:
            self.into_appear()
        self.panel.stopActionByTag(self.TOUCH_TAG)

    def switch_into_cam_idx(self, idx, need_slerp=False):
        self._camera_index = idx
        cam_info = self.VIEW_CAMERAS[self._camera_index]
        self.cur_song_offset = self.song_offset_dict.get(self._song_idx, [0, 0, 0])
        dist = list(map(lambda x, y: x + y, cam_info[4], self.cur_song_offset))
        self.set_custom_camera_by_scene_cam(cam_info[1], cam_info[2], dist, need_slerp)
        self.panel.lab_loc.SetString(cam_info[0])
        VIEW_FOV_RANGE = self.VIEW_CAMERAS[self._camera_index][3]
        self._max_hfov = VIEW_FOV_RANGE[1]
        self._min_hfov = VIEW_FOV_RANGE[0]
        if self.view_slider:
            self.view_slider.update_change_step(max((self._max_hfov - self._min_hfov) * 0.05, 1))
        self.on_fov_scaling(cam_info[2])

    def init_data(self):
        part_cam = self.get_partcam()
        camera_manager = part_cam.cam_manager
        if not camera_manager:
            return
        self._hfov = camera_manager.get_default_hfov()

    def on_finalize_panel(self):
        super(KizunaConcertViewUI, self).on_finalize_panel()
        if global_data.pc_ctrl_mgr:
            for hotkey in VIEW_BLOCK_HOTKEYS:
                global_data.pc_ctrl_mgr.unblock_hotkey(hotkey, 'concert_view')

        if self._ent_vis_mgr:
            self._ent_vis_mgr.show_all_ent()
            self._ent_vis_mgr.destroy()
            self._ent_vis_mgr = None
        self.show_main_ui()
        global_data.emgr.into_concert_view_camera_event.emit(False)
        self.destroy_widget('view_slider')
        self.disable()
        return

    def init_slider_component(self):
        from logic.comsys.common_ui.UIScaleSliderWidget import UIScaleSliderWidget
        init_percent = (self._hfov - self._min_hfov) / (self._max_hfov - self._min_hfov) * 100.0
        slider_args = {'slider': self.panel.progress_scale,
           'init_percent': init_percent,
           'scale_callback': self.on_scale_callback,
           'change_step': max((self._max_hfov - self._min_hfov) * 0.05, 1),
           'btn_up': self.panel.btn_plus,
           'btn_down': self.panel.btn_minus
           }
        self.view_slider = UIScaleSliderWidget(**slider_args)

    def on_scale_callback(self, percent):
        new_hfov = (self._max_hfov - self._min_hfov) * percent / 100.0 + self._min_hfov
        self.mod_fov_helper(new_hfov)

    def mod_fov_helper(self, val):
        self._hfov = val
        part_cam = self.get_partcam()
        part_cam.cam_manager.set_hoz_fov(self._hfov)

    def on_fov_scaling(self, fov):
        if self.view_slider:
            percent = (fov - self._min_hfov) / float(self._max_hfov - self._min_hfov) * 100.0
            self.view_slider.force_slider_changed(percent)

    def get_partcam(self):
        part_cam = global_data.game_mgr.scene.get_com('PartCameraSimple')
        if not part_cam:
            part_cam = global_data.game_mgr.scene.get_com('PartCamera')
        return part_cam

    def set_custom_camera(self, focus_point, default_pos, fov):
        part_cam = self.get_partcam()
        if self.camera_state != camera_state_const.DEBUG_MODE:
            self._last_camera_parameters = [
             self.camera_state, part_cam.cam_manager.cam_state.get_real_camera_type()]
            global_data.emgr.switch_target_to_camera_state_event.emit(camera_state_const.DEBUG_MODE)
        import math3d
        from logic.gutils.CameraHelper import cal_horizontal_default_pos
        new_default_pos = cal_horizontal_default_pos(math3d.vector(*default_pos), math3d.vector(*focus_point))
        part_cam.cam_manager.update_camera_config(new_default_pos, math3d.vector(*focus_point))
        part_cam.cam_manager.set_hoz_fov(fov)
        global_data.emgr.slerp_into_setupped_camera_event.emit(0)

    def set_custom_camera_by_scene_cam(self, cam_name, fov, dist, need_slerp):
        from logic.gutils.CameraHelper import get_adaptive_camera_fov
        import math3d
        scene = global_data.game_mgr.scene
        part_cam = self.get_partcam()
        cam_hanger = math3d.matrix()
        if cam_name == 'cam_wutai':
            cam_hanger.translation = math3d.vector(0, 220, -800)
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(cam_hanger.rotation.yaw, -0.084 / 2.0, True, 1)
        else:
            cam_hanger.translation = math3d.vector(0, 109.96, -323.46)
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(cam_hanger.rotation.yaw, 0, True, 1)
        part_cam.cam_manager.set_hoz_fov(fov)
        vec = cam_hanger.forward * dist[2] + cam_hanger.up * dist[1] + cam_hanger.right * dist[0]
        global_data.emgr.set_target_pos_for_special_logic.emit(cam_hanger.translation + vec)
        t = need_slerp or 0 if 1 else 1
        if need_slerp:
            global_data.emgr.camera_target_follow_speed_event.emit(True, 0.3, 1)
        global_data.emgr.slerp_into_setupped_camera_event.emit(0)

    def enable(self):
        from logic.vscene.parts.camera.FreeflyNonAOICameraController import FreeflyNonAOICameraController
        cam_controller = FreeflyNonAOICameraController()
        if cam_controller.check_can_enable():
            cam_controller.enable()

    def disable(self):
        from logic.vscene.parts.camera.FreeflyNonAOICameraController import FreeflyNonAOICameraController
        cam_controller = FreeflyNonAOICameraController()
        cam_controller.disable()

    def on_click_btn_quit(self, btn, touch):
        self.close()

    def on_click_btn_last(self, btn, touch):
        self.panel.PlayAnimation('click_left')
        self.switch_into_cam_idx((self._camera_index - 1) % len(self.VIEW_CAMERAS))

    def on_click_btn_next(self, btn, touch):
        self.panel.PlayAnimation('click_right')
        self.switch_into_cam_idx((self._camera_index + 1) % len(self.VIEW_CAMERAS))

    def on_update_concert_song_data_ex(self, stage, song_idx, song_end_ts):
        self.on_update_concert_song_data(stage, song_idx, song_end_ts)

    def on_update_concert_song_data(self, stage, song_idx, song_end_ts):
        if stage == battle_const.CONCERT_SING_STAGE and song_end_ts:
            self._song_idx = song_idx
            _offset = self.song_offset_dict.get(song_idx, [0, 0, 0])
            if self.cur_song_offset != _offset:
                self.switch_into_cam_idx(self._camera_index, need_slerp=True)

    def on_click_btn_resolution(self, btn, touch):
        from logic.comsys.concert.KizunaResolutionUI import KizunaResolutionUI
        KizunaResolutionUI()

    def show_reso_tips(self):
        if self.panel.IsPlayingAnimation('show_tips'):
            return
        self.panel.nd_tips.setVisible(True)
        self.panel.PlayAnimation('show_tips')