# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/CameraSettingUI.py
from __future__ import absolute_import
from common.const.uiconst import TOP_ZORDER
from common.uisys.basepanel import BasePanel
from logic.client.const.camera_const import FREE_MODEL, FIRST_PERSON_MODEL, THIRD_PERSON_MODEL, AIM_MODE, PREVIEW_MODEL
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const import uiconst

class CameraSettingUI(BasePanel):
    PANEL_CONFIG_NAME = 'setting/camera_setting'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    CAMERA_IDX = 0
    OTHER_MODEL_IDX = 7

    def on_init_panel(self):
        self.init_event()

    def on_finalize_panel(self):
        self.player = None
        return

    def init_parameters(self):
        self.player = None
        import world
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        if player:
            self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)
        return

    def on_player_setted(self, player):
        self.player = player

    def init_event(self):
        self.init_parameters()
        self.init_camera_settings()
        self.init_camera_slider()

        @self.panel.ck_revert_y_slide.callback()
        def OnChecked(btn, check, index):
            import world
            scene = world.get_active_scene()
            com_camera = scene.get_com('PartCamera')
            com_camera.camera_y_slide_dir = -1 if check else 1

    def init_camera_settings(self):

        def _cc_to_free_camera():
            self.switch_to_camera_state(FREE_MODEL)

        def _cc_to_first_camera():
            self.switch_to_camera_state(FIRST_PERSON_MODEL)

        def _cc_to_third_camera():
            self.switch_to_camera_state(THIRD_PERSON_MODEL)

        def _cc_to_preview_camera():
            self.switch_to_camera_state(PREVIEW_MODEL)

        def _cc_to_aim_camera1():
            self.switch_to_aim_state(1)

        def _cc_to_aim_camera2():
            self.switch_to_aim_state(2)

        def _cc_to_aim_camera4():
            self.switch_to_aim_state(4)

        def _cc_to_other():
            self.show_warning()

        confs = [
         {'title': get_text_by_id(2103),'check_group': [(get_text_by_id(2104), _cc_to_free_camera),
                          (
                           get_text_by_id(2105), _cc_to_first_camera),
                          (
                           get_text_by_id(2106), _cc_to_third_camera),
                          (
                           get_text_by_id(2107), _cc_to_preview_camera),
                          (
                           get_text_by_id(2108), _cc_to_aim_camera1),
                          (
                           get_text_by_id(2109), _cc_to_aim_camera2),
                          (
                           get_text_by_id(2110), _cc_to_aim_camera4),
                          (
                           get_text_by_id(2111), _cc_to_other)],
            'group_check_func': self.camera_group_check_func
            }]
        self.camera_state_list = [
         FREE_MODEL, FIRST_PERSON_MODEL, THIRD_PERSON_MODEL, PREVIEW_MODEL]
        self.aim_magn_list = [1, 2, 4]
        self.panel.sv_setting.SetInitCount(len(confs))
        for idx, check_group_item in enumerate(self.panel.sv_setting.GetAllItem()):
            conf = confs[idx]
            check_group_item.lab_title.setString(conf.get('title'))
            ck_group_conf = conf.get('check_group')
            check_group_item.cb_normal.SetInitCount(len(ck_group_conf))

            @check_group_item.cb_normal.unique_callback()
            def SetGroupChecked(group_ui_item, button, ck, check_index):
                self.on_group_btn_check(button, ck)

            for ck_idx, ck_btn in enumerate(check_group_item.cb_normal.GetAllItem()):
                ck_conf = ck_group_conf[ck_idx]
                ck_desc, ck_func = ck_conf
                ck_btn.lab_name.setString(ck_desc)

                @ck_btn.btn_selected.unique_callback()
                def OnClick(btn, touch, check_group_item=check_group_item, ck_func=ck_func, ck_idx=ck_idx):
                    ck_func()

        import world
        scene = world.get_active_scene()
        com_camera = scene.get_com('PartCamera')
        self.on_camera_switch_to_state(com_camera.get_cur_camera_state_type())

    def on_camera_switch_to_state(self, state, *args):
        self.camera_group_check_func(state)

    def camera_group_check_func(self, state):
        if state in self.camera_state_list:
            idx = self.camera_state_list.index(state)
            ck_group_ui = self.panel.sv_setting.GetItem(CameraSettingUI.CAMERA_IDX)
            ck_group_ui.cb_normal.SetCheck(idx, True)
        elif state == AIM_MODE:
            self.aim_group_check_func()
        else:
            ck_group_ui = self.panel.sv_setting.GetItem(CameraSettingUI.CAMERA_IDX)
            ck_group_ui.cb_normal.SetCheck(CameraSettingUI.OTHER_MODEL_IDX, True)

    def aim_group_check_func(self):
        import world
        scene = world.get_active_scene()
        com_camera = scene.get_com('PartCamera')
        magn = com_camera.cam_state.magnification
        ck_group_ui = self.panel.sv_setting.GetItem(CameraSettingUI.CAMERA_IDX)
        idx = self.aim_magn_list.index(int(magn)) + len(self.camera_state_list)
        ck_group_ui.cb_normal.SetCheck(idx, True)

    def on_group_btn_check(self, btn, check):
        btn.img_selected.setVisible(check)

    def switch_to_camera_state(self, cam_state):
        import world
        scene = world.get_active_scene()
        com_camera = scene.get_com('PartCamera')
        com_camera.switch_cam_state(cam_state)

    def switch_to_aim_state(self, magn):
        import world
        scene = world.get_active_scene()
        com_camera = scene.get_com('PartCamera')
        com_camera.switch_cam_state(AIM_MODE, magnification=magn, trans_time=0.2)

    def init_camera_slider(self):
        import world
        scene = world.get_active_scene()
        com_camera = scene.get_com('PartCamera')
        self.init_percent = 50

        def OnFovPercentageChanged(slider):
            val = int(slider.getPercent()) - self.init_percent
            com_camera.set_fov(self.init_fov + val)

        def OnDistPercentageChanged(slider):
            import math3d
            val = int(slider.getPercent()) - self.dist_old_percent
            self.dist_old_percent = slider.getPercent()
            cam_pos = com_camera.get_pos()
            yaw = com_camera.get_yaw()
            offset = math3d.vector(0, 0, -1 * val) * math3d.matrix.make_rotation_y(yaw)
            new_pos = math3d.vector(cam_pos + offset)
            com_camera.set_pos(new_pos)

        def OnHeightPercentageChanged(slider):
            import math3d
            val = int(slider.getPercent()) - self.height_old_percent
            self.height_old_percent = slider.getPercent()
            val = val * 15
            cam_pos = com_camera.get_pos()
            new_pos = math3d.vector(cam_pos.x, cam_pos.y + val, cam_pos.z)
            com_camera.set_pos(new_pos)

        camera_slider_conf = [
         (
          self.panel.slider_dist, get_text_by_id(2112), lambda : self.init_dist_slider(), OnDistPercentageChanged),
         (
          self.panel.slider_fov, get_text_by_id(2113), lambda : self.init_fov_slider(), OnFovPercentageChanged),
         (
          self.panel.slider_high, get_text_by_id(2114), lambda : self.init_height_slider(), OnHeightPercentageChanged)]
        for conf in camera_slider_conf:
            slider, desc, init_func, slider_func = conf
            slider.tf_name.setString(desc)
            slider.tf_value.setVisible(False)
            init_func()

            @slider.slider.unique_callback()
            def OnPercentageChanged(ctrl, sl, slider_func=slider_func):
                slider_func(sl)

    def init_dist_slider(self):
        init_percent = self.init_percent
        self.panel.slider_dist.slider.setPercent(init_percent)
        self.dist_old_percent = init_percent

    def init_height_slider(self):
        init_percent = self.init_percent
        self.panel.slider_high.slider.setPercent(init_percent)
        self.height_old_percent = init_percent

    def init_fov_slider(self):
        import world
        init_percent = self.init_percent
        scene = world.get_active_scene()
        com_camera = scene.get_com('PartCamera')
        self.init_fov = com_camera.cam.fov
        self.panel.slider_fov.slider.setPercent(init_percent)

    def show_warning(self):
        global_data.emgr.battle_show_message_event.emit(get_text_by_id(2115))