# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/debug/CameraTestUI.py
from __future__ import absolute_import
import six_ex
from six.moves import zip
from six.moves import range
from six.moves import map
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER
from common.framework import Functor
import data.camera_state_const as camera_state_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.const import uiconst
import game
import math3d

class CameraTestUI(BasePanel):
    PANEL_CONFIG_NAME = 'test/test_camera'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    box_num = 7
    UI_ACTION_EVENT = {'btn_change.OnClick': 'on_click_reverse_btn'
       }
    key_map = {game.VK_W: math3d.vector(0, 0, 1),
       game.VK_S: math3d.vector(0, 0, -1),
       game.VK_A: math3d.vector(-1, 0, 0),
       game.VK_D: math3d.vector(1, 0, 0),
       game.VK_LSHIFT: math3d.vector(0, -1, 0),
       game.VK_SPACE: math3d.vector(0, 1, 0)
       }
    quick_trk_key_list = [
     game.VK_CTRL]
    quick_trk_key_list.extend([ getattr(game, 'VK_%d' % i) for i in range(1, 10) ])
    quick_trk_key_list.extend(six_ex.keys(key_map))

    def on_init_panel(self, *args, **kwargs):
        self.hide_main_ui()
        self._default_pos = [0, 0, 0]
        self._focus_pos = [0, 0, 0]
        self._hfov = 0
        self._max_hfov = 160
        self._min_hfov = 0
        self._self_define_parameters = ()
        self._last_camera_parameters = ()
        self._input_box_list = []
        self.init_input_box()
        self.update_data()
        self.update_show()
        self.init_event()
        self.init_slider()
        self.init_keyboard_ctrl()
        self.init_camera_settings()
        self.init_external_exe()

    def init_event(self):
        global_data.emgr.camera_switch_to_state_event += self.on_camera_state_changed
        global_data.emgr.camera_switch_to_state_event += self.set_camera_state
        partcam = self.get_partcam()
        if partcam:
            self.set_camera_state(partcam.get_cur_camera_state_type())

    def on_finalize_panel(self):
        self.show_main_ui()
        self.recover_keyboard_ctrl()

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

    def update(self):
        self.set_custom_camera(self._focus_pos, self._default_pos, self._hfov)

    def mod_default_pos(self, index, val):
        self._default_pos[index] = val
        self.update()

    def mod_focus_pos(self, index, val):
        self._focus_pos[index] = val
        self.update()

    def mod_fov(self, val):
        self.mod_fov_helper(val)
        self.update_slider()

    def mod_fov_helper(self, val):
        self._hfov = val
        self.update()

    def init_input_box(self):
        input_box_name_list = [ 'nd_stat%d' % (i + 1) for i in range(self.box_num) ]
        func_list = [
         Functor(self.mod_default_pos, 0),
         Functor(self.mod_default_pos, 1),
         Functor(self.mod_default_pos, 2),
         self.mod_fov,
         Functor(self.mod_focus_pos, 0),
         Functor(self.mod_focus_pos, 1),
         Functor(self.mod_focus_pos, 2)]
        index = 0
        for nd_name, func in zip(input_box_name_list, func_list):
            input_box_nd = getattr(self.panel, nd_name)
            import logic.comsys.common_ui.InputBox as InputBox

            def wrapper_func(index=index, func=func):
                box = self._input_box_list[index]
                text = box.get_text()
                try:
                    val = float(text)
                except:
                    val = 0

                func(val)

            box = InputBox.InputBox(input_box_nd.input_box, placeholder='0', send_callback=wrapper_func)
            self._input_box_list.append(box)
            index += 1

    def on_camera_state_changed(self, new_type, old_type, *args):

        def inner_update():
            self.update_data()
            self.update_show()

        self.panel.SetTimeOut(0.3, inner_update)

    def update_data(self):
        part_cam = self.get_partcam()
        camera_manager = part_cam.cam_manager
        if not camera_manager:
            return
        default_pos = camera_manager.default_pos
        focus_pos = camera_manager.focus_point
        self._default_pos = [default_pos.x, default_pos.y, default_pos.z]
        self._focus_pos = [focus_pos.x, focus_pos.y, focus_pos.z]
        self._hfov = camera_manager.get_default_hfov()

    def update_show(self):

        def get_default_pos_data(index):
            return self._default_pos[index]

        def get_focus_pos_data(index):
            return self._focus_pos[index]

        def get_fov_data():
            return self._hfov

        update_func_list = [
         Functor(get_default_pos_data, 0),
         Functor(get_default_pos_data, 1),
         Functor(get_default_pos_data, 2),
         get_fov_data,
         Functor(get_focus_pos_data, 0),
         Functor(get_focus_pos_data, 1),
         Functor(get_focus_pos_data, 2)]
        for box, func in zip(self._input_box_list, update_func_list):
            box.set_text('%.1f' % func())

    def get_partcam(self):
        part_cam = global_data.game_mgr.scene.get_com('PartCameraSimple')
        if not part_cam:
            part_cam = global_data.game_mgr.scene.get_com('PartCamera')
        return part_cam

    def update_slider(self):
        cur_percent = self._hfov / (self._max_hfov - self._min_hfov)
        self.panel.prog_slider.setPercent(cur_percent * 100.0)

    def init_slider(self):

        @self.panel.prog_slider.callback()
        def OnPercentageChanged(*args):
            percent = self.panel.prog_slider.getPercent()
            new_hfov = (self._max_hfov - self._min_hfov) * percent / 100.0 + self._min_hfov
            self.mod_fov_helper(new_hfov)
            self.update_data()
            self.update_show()

    def set_camera_state(self, state, *args):
        self.camera_state = state
        if self.camera_state != camera_state_const.DEBUG_MODE:
            self.panel.btn_change.SetText('\xe9\xbb\x98\xe8\xae\xa4\xe8\xa7\x86\xe8\xa7\x92')
        else:
            self.panel.btn_change.SetText('\xe8\x87\xaa\xe5\xae\x9a\xe8\xa7\x86\xe8\xa7\x92')
            global_data.emgr.switch_cam_state_enable_event.emit(False)

    def on_click_reverse_btn(self, btn, touch):
        if self.camera_state == camera_state_const.DEBUG_MODE:
            import copy
            self._self_define_parameters = copy.deepcopy([self.camera_state, self._default_pos, self._focus_pos, self._hfov])
            old_camera_state, real_old_camera_state = self._last_camera_parameters
            global_data.emgr.switch_cam_state_enable_event.emit(True)
            self.switch_to_camera_state(real_old_camera_state)
            self.switch_to_camera_state(old_camera_state)
        elif self._self_define_parameters:
            camera_state, self._default_pos, self._focus_point, self._hfov = self._self_define_parameters
            self.update()
            self.update_show()
        else:
            global_data.game_mgr.show_tip('\xe6\x89\xbe\xe4\xb8\x8d\xe5\x88\xb0\xe5\x8e\x86\xe5\x8f\xb2\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x81')

    def on_key_down(self, msg, changed_key):
        STEP = 0.2 * NEOX_UNIT_SCALE
        if changed_key in self.key_map:
            change_dir = self.key_map[changed_key]
            if changed_key not in [game.VK_LSHIFT, game.VK_SPACE]:
                self._default_pos = self.add_tuple(self._default_pos, (change_dir.x, change_dir.y, change_dir.z))
            else:
                self._focus_pos = self.add_tuple(self._focus_pos, (change_dir.x, change_dir.y, change_dir.z))
            self.update_show()
            self.update()

    def add_tuple(self, t1, t2):
        return list(map(lambda x, y: x + y, t1, t2))

    def init_keyboard_ctrl(self):
        partctrl = global_data.game_mgr.scene.get_com('PartCtrl')
        if not partctrl:
            return
        partctrl.unregister_keys()
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.enable_keyboard_control(False)
        game.add_key_handler(game.MSG_KEY_DOWN, self.quick_trk_key_list, self.on_quick_key_down)
        game.add_key_handler(game.MSG_KEY_UP, self.quick_trk_key_list, self.on_quick_key_up)

    def recover_keyboard_ctrl(self):
        partctrl = global_data.game_mgr.scene.get_com('PartCtrl')
        if not partctrl:
            return
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.enable_keyboard_control(True)
        game.remove_key_handler(game.MSG_KEY_DOWN, self.quick_trk_key_list, self.on_quick_key_down)
        game.remove_key_handler(game.MSG_KEY_UP, self.quick_trk_key_list, self.on_quick_key_up)
        partctrl.register_keys()

    def switch_to_aim_state(self, magn):
        com_camera = self.get_partcam().cam_manager
        com_camera.switch_cam_state(camera_state_const.AIM_MODE, magnification=magn, trans_time=0.2)

    def switch_to_camera_state(self, cam_state):
        com_camera = self.get_partcam().cam_manager
        com_camera.switch_cam_state(cam_state)

    def init_camera_settings(self):
        from common.framework import Functor
        csc = camera_state_const
        camera_list = {csc.FREE_MODEL: '\xe8\x87\xaa\xe7\x94\xb1\xe8\xa7\x86\xe8\xa7\x92',
           csc.FIRST_PERSON_MODEL: '\xe7\xac\xac\xe4\xb8\x80\xe4\xba\xba\xe7\xa7\xb0',
           csc.THIRD_PERSON_MODEL: '\xe7\xac\xac\xe4\xb8\x89\xe4\xba\xba\xe7\xa7\xb0',
           csc.DEAD_MODEL: '\xe6\xad\xbb\xe4\xba\xa1\xe9\x95\x9c\xe5\xa4\xb4',
           csc.PREVIEW_MODEL: '\xe9\xa2\x84\xe8\xa7\x88\xe6\xa8\xa1\xe5\xbc\x8f',
           csc.PLANE_MODE: '\xe9\xa3\x9e\xe6\x9c\xba\xe9\x95\x9c\xe5\xa4\xb4',
           csc.FREE_DROP_MODE: '\xe8\xb7\xb3\xe4\xbc\x9e\xe9\x95\x9c\xe5\xa4\xb4',
           csc.PARACHUTE_MODE: '\xe5\xbc\x80\xe4\xbc\x9e\xe9\x95\x9c\xe5\xa4\xb4',
           csc.VEHICLE_MODE: '\xe5\xbc\x80\xe8\xbd\xa6\xe9\x95\x9c\xe5\xa4\xb4',
           csc.FOCUS_MODE: '\xe8\x81\x9a\xe7\x84\xa6\xe9\x95\x9c\xe5\xa4\xb4',
           csc.DRONE_MODE: '\xe6\x97\xa0\xe4\xba\xba\xe6\x9c\xba\xe9\x95\x9c\xe5\xa4\xb4',
           csc.AIRSHIP_MODE: '\xe9\xa3\x9e\xe8\x89\x87\xe9\x95\x9c\xe5\xa4\xb4',
           csc.HIDING_MODE: '\xe8\x97\x8f\xe5\x8c\xbf\xe7\x8a\xb6\xe6\x80\x81\xe9\x95\x9c\xe5\xa4\xb4',
           csc.THIRD_PERSON_SPEED_UP_MODE: '\xe7\xac\xac\xe4\xb8\x89\xe4\xba\xba\xe7\xa7\xb0\xe8\xb7\x91\xe9\x9e\x8b',
           csc.PASSENGER_VEHICLE_MODE: '\xe4\xb9\x98\xe5\xae\xa2\xe9\x95\x9c\xe5\xa4\xb4',
           csc.OBSERVE_FREE_MODE: '\xe8\x87\xaa\xe7\x94\xb1\xe8\xa7\x82\xe6\x88\x98\xe9\x95\x9c\xe5\xa4\xb4',
           csc.RIGHT_AIM_MODE: '\xe5\x8f\xb3\xe7\x9e\x84\xe9\x95\x9c\xe5\xa4\xb4',
           csc.MECHA_MODE: '\xe6\x9c\xba\xe7\x94\xb2',
           csc.MELEE_MECHA_MODE: '\xe8\xbf\x91\xe6\x88\x98\xe6\x9c\xba\xe7\x94\xb2',
           csc.MECHA_MODE_TWO: '\xe4\xba\x8c\xe7\xba\xa7\xe6\x9c\xba\xe7\x94\xb2',
           csc.MECHA_MODE_JOANNA: '\xe4\xb9\x94\xe5\xae\x89\xe5\xa8\x9c\xe6\x9c\xba\xe7\x94\xb2',
           csc.DEBUG_MODE: '\xe7\xbe\x8e\xe6\x9c\xaf\xe8\xb0\x83\xe8\xaf\x95\xe9\x95\x9c\xe5\xa4\xb4'
           }
        show_camera_list = []
        camera_state_key = sorted(six_ex.keys(camera_list))
        for cam_state in camera_state_key:
            name = camera_list[cam_state]
            show_camera_list.append((name, Functor(self.switch_to_camera_state, cam_state)))

        show_camera_list.append(('\xe7\xba\xa2\xe7\x82\xb9', Functor(self.switch_to_aim_state, 1)))
        show_camera_list.append(('\xe4\xba\x8c\xe5\x80\x8d\xe9\x95\x9c', Functor(self.switch_to_aim_state, 2)))
        show_camera_list.append(('\xe5\x9b\x9b\xe5\x80\x8d\xe9\x95\x9c', Functor(self.switch_to_aim_state, 4)))
        self.panel.list_camera.SetInitCount(len(show_camera_list))
        for idx, item in enumerate(self.panel.list_camera.GetAllItem()):
            name, func = show_camera_list[idx]
            item.btn_tab.SetText(name)

            @item.btn_tab.unique_callback()
            def OnClick(btn, touch, func=func):
                global_data.emgr.switch_cam_state_enable_event.emit(True)
                func()

        self.panel.list_camera.setVisible(True)

    def init_external_exe(self):
        pass

    from logic.gutils.pc_utils import skip_when_debug_key_disabled

    @skip_when_debug_key_disabled
    def on_quick_key_down(self, msg, keycode):
        if msg == game.MSG_KEY_DOWN:
            global_data.keys[keycode] = True
        if keycode in self.key_map:
            self.on_key_down(msg, keycode)
        self.on_try_play_trk(msg, keycode)

    from logic.gutils.pc_utils import skip_when_debug_key_disabled

    @skip_when_debug_key_disabled
    def on_quick_key_up(self, msg, keycode):
        if msg == game.MSG_KEY_UP:
            global_data.keys[keycode] = False

    def on_try_play_trk(self, msg, keycode):
        if keycode == game.VK_CTRL:
            return
        else:
            if global_data.keys.get(game.VK_CTRL, None):
                ctrl_str = str(game.VK_CTRL) + '+'
            else:
                ctrl_str = ''
            current_key_str = ctrl_str + str(keycode)
            from common.cfg import confmgr
            confmgr.exit()
            trk_name = confmgr.get('debug_cam_trk_conf', current_key_str)
            if trk_name:
                global_data.emgr.play_preset_trk_animation_simple_event.emit(trk_name, 1, 1, False)
            return