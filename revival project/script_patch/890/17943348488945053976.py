# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/LobbySceneOnlyUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_00, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from common.uisys.uielment.CCSprite import CCSprite
import cc
from logic.comsys.share.ShareManager import ShareManager
from logic.comsys.lobby.LobbyInteractionUI import LobbyInteractionUI
import math
from logic.gutils.share_utils import get_pc_share_save_path
from logic.gutils.rocker_widget_utils import RockerWidget
import data.camera_state_const as camera_state_const
from logic.client.const import game_mode_const
from common.cfg import confmgr
from common.utils.cocos_utils import ccp
DELAY_HIDE_LIST = [
 'LobbyUI', 'MainChat']

class CameraModifyWidget(object):

    def __init__(self, panel):
        self.panel = panel
        self.process_event(True)
        self.focus_offset = None
        self.pos_offset = None
        self.fov_offset = None
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CONCERT):
            self.fov_offsets = confmgr.get('game_mode/concert/play_data', str('shot_fov_offsets'), default=[0, 30, 20, 10, 0, -10, -20, -30])
        else:
            self.fov_offsets = [
             0, 30, 20, 10, 0, -10, -20, -30]
        self.fov_offset_idx = 0
        self.hoffset = None
        self.height_offsets = [0, 5, 10, 15, 0]
        self.height_idx = 0
        self._rocker_direction = cc.Vec2(0, 0)
        self._rocker_move_percent = 0.0
        self.touch_begin_pos = cc.Vec2(0, 0)
        self.init_rocker()
        self.bind_btn_event()
        self.init_menu()
        self.update_fov_button_show()
        self.update_height_button_show()
        self._ent_vis_mgr = None
        return

    def set_enable_ent_vis(self):
        from logic.gutils.ent_visibility_utils import EntSimpleVisibilityMgr
        self._ent_vis_mgr = EntSimpleVisibilityMgr()
        self._ent_vis_mgr.set_concern_types(['Puppet'])
        self._ent_vis_mgr.set_is_enable_control(True)

    def init_menu(self):
        self._hide_others = False
        self._show_teammates = False

        def update_ent_show():
            if not self._ent_vis_mgr:
                return
            teamate_list = []
            if global_data.player and global_data.player.logic:
                lplayer = global_data.player.logic
                teamate_list = lplayer.ev_g_groupmate()
                if lplayer.id in teamate_list:
                    teamate_list.remove(lplayer.id)
            if self._hide_others:
                if not self._show_teammates:
                    self._ent_vis_mgr.hide_all_ent()
                else:
                    self._ent_vis_mgr.hide_all_ent(except_list=teamate_list)
                    self._ent_vis_mgr.set_independent_ent_list_vis(teamate_list, True)
            else:
                self._ent_vis_mgr.show_all_ent()

        def hide_others(enable):
            self._hide_others = enable
            update_ent_show()

        def show_teammates(enable):
            self._show_teammates = enable
            update_ent_show()

        def dof(enable):
            pass

        big_menu_names = [
         83239]
        big_menu_conf = [
         [
          (
           83236, False, hide_others)]]
        self.menu_select = {}
        big_menu_count = len(big_menu_conf)
        self.panel.list_setting_item.SetInitCount(big_menu_count)
        for i in range(big_menu_count):
            menu_list_item = self.panel.list_setting_item.GetItem(i)
            menu_list_item.lab_title.SetString(big_menu_names[i])
            menu_choose_confs = big_menu_conf[i]
            menu_list_item.list_choose.SetInitCount(len(menu_choose_confs))
            for j in range(len(menu_choose_confs)):
                menu_item = menu_list_item.list_choose.GetItem(j)
                menu_conf = menu_choose_confs[j]
                menu_item.text.SetString(menu_conf[0])
                self.menu_select.setdefault(i, {})
                self.menu_select[i][j] = menu_conf[1]
                callback = menu_conf[2]
                menu_item.choose.setVisible(menu_conf[1])

                @menu_item.btn.callback()
                def OnClick(btn, touch, out_idx=i, inner_idx=j, callback=callback, menu_item=menu_item):
                    cur_val = self.menu_select[out_idx][inner_idx]
                    new_val = not cur_val
                    self.menu_select[out_idx][inner_idx] = new_val
                    menu_item.choose.setVisible(new_val)
                    callback(new_val)

    def destroy(self):
        self.panel.list_setting_item.SetInitCount(0)
        if self._ent_vis_mgr:
            self._ent_vis_mgr.show_all_ent()
            self._ent_vis_mgr.destroy()
            self._ent_vis_mgr = None
        self.process_event(False)
        if self._rocker_widget:
            self._rocker_widget.destroy()
            self._rocker_widget = None
        self.panel = None
        return

    def process_event(self, is_bind):
        pass

    def update_fov_button_show(self):
        self.panel.btn_scale.lab_scale.SetString(str(self.fov_offsets[self.fov_offset_idx]))

    def update_height_button_show(self):
        self.panel.lab_scale_height.SetString(str(self.height_offsets[self.height_idx]))

    def bind_btn_event(self):

        @self.panel.btn_scale.callback()
        def OnClick(btn, touch):
            self.fov_offset_idx += 1
            self.fov_offset_idx %= len(self.fov_offsets)
            self.fov_offset = self.fov_offsets[self.fov_offset_idx]
            self.update_fov_button_show()
            self.update_camera_show()

        @self.panel.btn_scale_height.callback()
        def OnClick(btn, touch):
            self.height_idx += 1
            self.height_idx %= len(self.height_offsets)
            self.hoffset = self.height_offsets[self.height_idx]
            self.update_height_button_show()
            if self.pos_offset:
                self.pos_offset[1] = self.hoffset
            else:
                self.pos_offset = [
                 0, 0, 0]
                self.pos_offset[1] = self.hoffset
            self.update_camera_show()

        @self.panel.btn_reset.callback()
        def OnClick(btn, touch):
            self.reset_camera_show()

        @self.panel.btn_setting.callback()
        def OnClick(btn, touch):
            self.panel.nd_menu.setVisible(True)

        @self.panel.nd_menu.btn_close.callback()
        def OnClick(btn, touch):
            self.panel.nd_menu.setVisible(False)

    def refresh_menu_show(self):
        pass

    def reset_camera_show(self):
        self.focus_offset = None
        self.pos_offset = None
        self.fov_offset = None
        self.hoffset = None
        self.fov_offset_idx = 0
        self.height_idx = 0
        self.update_fov_button_show()
        self.update_height_button_show()
        self.update_camera_show()
        return

    def init_rocker(self):
        self._rocker_widget = RockerWidget(self.panel.walk_bar, self.panel.walk_bar, self.panel.run_button)
        self._rocker_center_wpos = self.panel.walk_bar.ConvertToWorldSpacePercentage(50, 50)
        self._rocker_widget.enable_drag = True
        self._rocker_widget.set_begin_callback(self.on_rocker_begin)
        self._rocker_widget.set_drag_callback(self.on_rocker_drag)
        self._rocker_widget.set_end_callback(self.on_rocker_end)
        self.btn_dragged = False
        self.btn_dragged_dir = None
        return

    def on_rocker_begin(self, btn, touch):
        self.touch_begin_pos = touch.getLocation()
        self._rocker_widget.enable_rocker_tick(self.rocker_tick)
        return True

    def on_rocker_drag(self, btn, touch):
        if not self._rocker_widget.is_rocker_enable:
            return
        pt = touch.getLocation()
        delta_vec = ccp(pt.x - self.touch_begin_pos.x, pt.y - self.touch_begin_pos.y)
        if delta_vec.x != 0 and delta_vec.y != 0:
            angle = math.degrees(math.atan2(delta_vec.x, delta_vec.y))
            self.panel.dec_bar_running.setVisible(True)
            self.panel.dec_bar_running.setRotation(angle)
        self.btn_dragged = True
        self._rocker_move_percent = delta_vec.length() / float(self._rocker_widget.get_spawn_radius())
        if delta_vec.length() > 0:
            delta_vec.normalize()
        self._rocker_direction.x = delta_vec.x
        self._rocker_direction.y = delta_vec.y

    def on_rocker_end(self, btn, touch):
        self.btn_dragged = False
        self.panel.dec_bar_running.setVisible(False)
        self._rocker_direction = ccp(0, 0)
        self._rocker_move_percent = 0
        self._rocker_widget.enable_rocker_tick(None)
        return

    def on_add_camera_offset(self, x, y, z):
        pass

    def update_camera_show(self):
        pass

    def rocker_tick(self, dt):
        self.on_add_camera_offset(self._rocker_direction.x, 0, self._rocker_direction.y)


class LobbyCameraModifyWidget(CameraModifyWidget):

    def __init__(self, panel):
        super(LobbyCameraModifyWidget, self).__init__(panel)
        self.panel.nd_setting.setVisible(False)
        self.update_data()

    def destroy(self):
        self.panel.btn_reset.OnClick(None)
        super(LobbyCameraModifyWidget, self).destroy()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        event_info = {}
        if not event_info:
            return
        if is_bind:
            emgr.bind_events(event_info)
        else:
            emgr.unbind_events(event_info)

    def on_camera_state_changed(self, new_type, old_type, *args):

        def inner_update():
            self.update_data()

        self.panel.SetTimeOut(0.3, inner_update)

    def set_lobby_custom_camera(self, focus_point, distance, fov):
        global_data.emgr.modify_lobby_camera_display_parameter.emit(focus_point, distance, fov)

    def on_add_camera_offset(self, x, y, z):
        if self.pos_offset:
            self.pos_offset = [
             x + self.pos_offset[0], y + self.pos_offset[1], z + self.pos_offset[2]]
        else:
            self.pos_offset = [
             x, y or 0, z]
        ranges = [(-30, 30), (-25, 50), (-50, 10)]
        for i, val in enumerate(self.pos_offset):
            bound = ranges[i]
            self.pos_offset[i] = min(max(bound[0], self.pos_offset[i]), bound[1])

        self.update_camera_show()

    def update_data(self):
        from common.cfg import confmgr
        if global_data.player:
            role_id = global_data.player.get_role()
        else:
            role_id = '11'
        camera_config = confmgr.get('mecha_display', 'LobbyCameraConfig', 'Content')['1']
        focus_vector = camera_config['focus'].get(str(role_id), camera_config['focus'].get('other', [5, 22]))
        camera_distance = camera_config['distance'].get(str(role_id), camera_config['distance'].get('other', 19))
        init_camera_info = confmgr.get('mecha_display', 'LobbyTransform', 'Content', 'init_camera')
        self._focus_vector = list(focus_vector)
        self._camera_distance = camera_distance
        if global_data.game_mgr.scene and global_data.game_mgr.scene.active_camera:
            self._vfov = global_data.game_mgr.scene.active_camera.fov
        else:
            self._vfov = camera_config['fov']

    def update_camera_show(self):
        new_focus_point = self._focus_vector
        new_distance = self._camera_distance
        if self.pos_offset:
            new_distance = self._camera_distance - self.pos_offset[2]
            new_focus_point = [self._focus_vector[0] + self.pos_offset[0], self._focus_vector[1] + self.pos_offset[1]]
        new_vfov = self._vfov
        if self.fov_offset:
            new_vfov = self._vfov + self.fov_offset
        self.set_lobby_custom_camera(new_focus_point, new_distance, new_vfov)


class LobbySceneOnlyUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/screen_shot'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_00
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_screen.OnClick': 'on_click_screen_btn',
       'temp_btn_back.btn_back.OnClick': 'on_click_close_btn',
       'btn_gride.OnClick': 'on_click_gride_btn',
       'temp_btn_share.btn_common.OnClick': 'on_click_share_btn'
       }
    HOT_KEY_FUNC_MAP = {'switch_interaction.CANCEL': 'keyboard_use_spray_ui_cancel',
       'switch_interaction.DOWN_UP': 'keyboard_use_spray_ui'
       }

    def on_init_panel(self):
        self.regist_main_ui()
        self.save_pic_path = None
        self.panel.temp_btn_share.setVisible(False)
        self._screen_capture_helper = ScreenFrameHelper()
        screen_sprite = CCSprite.Create()
        self.panel.nd_screenshot.AddChild('sp_scr', screen_sprite)
        self.panel.nd_screenshot.sp_scr.SetPosition('50%', '50%')
        self.panel.nd_lens.setVisible(True)
        import cc
        self.panel.nd_screenshot.sp_scr.setAnchorPoint(cc.Vec2(0.5, 0.5))
        self._sprite = None
        self.hide_main_ui(exceptions=['LobbyRockerUI', 'LobbyUI', 'MainChat', 'MoveRockerUI', 'ObserveUI'])
        global_data.emgr.on_switch_scene_capture_event.emit(True)
        self.add_hide_count(self.__class__.__name__)
        self.panel.SetTimeOut(0.3, lambda : self.start_play())
        self.init_interaction_btn()
        self._camera_modify_widget = None
        self._is_in_saving = False
        self.switch_gride_show(True)
        self.init_camera_modify_widget()
        return

    def init_camera_modify_widget(self):
        self._camera_modify_widget = LobbyCameraModifyWidget(self.panel)

    def start_play(self):
        self.panel.PlayAnimation('in')
        self.add_show_count(self.__class__.__name__)
        global_data.ui_mgr.hide_all_ui_by_key(self.__class__.__name__, DELAY_HIDE_LIST)

    def on_finalize_panel(self):
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
            self._screen_capture_helper = None
        if self._camera_modify_widget:
            self._camera_modify_widget.destroy()
            self._camera_modify_widget = None
        self._inter_invoke_btn_widget.destory()
        self._inter_invoke_btn_widget = None
        self._sprite = None
        global_data.ui_mgr.revert_hide_all_ui_by_key_action(self.__class__.__name__, DELAY_HIDE_LIST)
        global_data.emgr.on_switch_scene_capture_event.emit(False)
        self.show_main_ui()
        return

    def on_click_close_btn(self, *args):
        self.close()
        part = global_data.game_mgr.scene.get_com('PartMirror')
        if part:
            part.stop_area_timer = True

    def on_click_screen_btn(self, btn, touch):
        from logic.gutils.share_utils import huawei_permission_confirm
        permission = 'android.permission.WRITE_EXTERNAL_STORAGE'
        huawei_permission_confirm(permission, 635572, self._real_click_screen_btn)

    def _real_click_screen_btn(self):
        import game3d
        if self.panel and self.panel.isValid():
            self.save_pic_path = None
            self.panel.temp_btn_share.setVisible(False)

            def custom_cb(rt):
                if not rt:
                    return
                import device_compatibility
                self.panel.nd_screenshot.sp_scr.setSpriteFrame(rt.getSprite().getSpriteFrame())
                if not device_compatibility.IS_DX:
                    self.panel.nd_screenshot.sp_scr.setScaleY(-1)
                self.panel.PlayAnimation('screen_shot')
                t = self.panel.GetAnimationMaxRunTime('screen_shot')
                self.panel.SetTimeOut(t, lambda : self.panel.nd_screenshot.setVisible(False) if self.panel else None, tag=210120)
                game3d.delay_exec(100, lambda : self.save_to_gallery(rt))
                if game3d.get_platform() != game3d.PLATFORM_WIN32:
                    from logic.comsys.share.ShareScreenCaptureUI import ShareScreenCaptureUI
                    ShareScreenCaptureUI().on_file_ready()

            if self._screen_capture_helper:
                self._screen_capture_helper.take_screen_shot([], self.panel, custom_cb=custom_cb, head_nd_name='nd_player_info_1', need_share_ui=False, white_lab=True)
        return

    def save_to_gallery(self, save_rt):
        if self._is_in_saving:
            return
        self._is_in_saving = True
        import game3d

        def save_helper(cb):

            def wrapper(rt, filename):
                if not (rt and rt.isValid()):
                    return
                cb(rt, filename)

            return lambda rt, filename: global_data.game_mgr.post_exec(lambda : wrapper(rt, filename))

        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            file_whole_path = get_pc_share_save_path()

            def save_callback(rt, file_name):
                self._is_in_saving = False
                global_data.game_mgr.show_tip(get_text_by_id(920706, {'path': file_whole_path}))
                if global_data.channel.get_app_channel() == 'steam':
                    image_size = rt.getSprite().getContentSize()
                    json_dict = {'methodId': 'AddScreenshotToLibrary',
                       'filePath': file_whole_path,
                       'imageWidth': int(image_size.width),
                       'imageHeight': int(image_size.height)
                       }
                    global_data.channel.extend_func_by_dict(json_dict)
                self.save_pic_end(file_whole_path)

            if save_rt:
                if file_whole_path.endswith('.png'):
                    save_img_type = cc.IMAGE_FORMAT_PNG
                elif file_whole_path.endswith('.jpg'):
                    save_img_type = cc.IMAGE_FORMAT_JPG
                else:
                    log_error('unsupport image type when _save_rt_to_file')
                    save_img_type = cc.IMAGE_FORMAT_UNKOWN
                    return
                save_rt.saveToFile(file_whole_path, save_img_type, False, save_helper(save_callback))
            return

        def on_save_to_document(rt, filename):
            if not (rt and rt.isValid()):
                return
            import game3d
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                global_data.game_mgr.show_tip(get_text_by_id(2183))
                self._is_in_saving = False
                return
            self._is_in_saving = False
            if not global_data.is_android_pc:
                global_data.game_mgr.post_exec(self._save_to_gallery)

        if save_rt:
            save_rt.saveToFile(ShareManager().SHARE_SAVE_PATH, cc.IMAGE_FORMAT_PNG, True, save_helper(on_save_to_document))

    def _save_to_gallery(self):

        def _cb():
            if global_data.share_mgr:
                self.save_pic_end(global_data.share_mgr.SHARE_SAVE_PATH)

        ShareManager().save_to_gallery(callback=_cb)

    def save_pic_end(self, path):
        self.save_pic_path = path
        if not (self.panel and self.panel.isValid()):
            return
        if global_data.player:
            self.panel.temp_btn_share.setVisible(not global_data.player.is_in_battle() and global_data.is_share_show)

    def on_click_share_btn(self, *args, **kargs):
        if not self.save_pic_path:
            return
        if not global_data.player:
            return
        visitor = global_data.player.get_all_puppet_info() or {}
        if not len(visitor):
            global_data.game_mgr.show_tip(get_text_by_id(611624))
            return

        def _cb():
            import os
            if not os.path.exists(self.save_pic_path):
                return
            global_data.player.try_share_image(self.save_pic_path)

        from logic.comsys.lottery.LotterySmallSecondConfirmWidget import LotterySmallSecondConfirmWidget
        LotterySmallSecondConfirmWidget(title_text_id=611617, content_text_id=get_text_by_id(611603), confirm_callback=_cb)

    def init_interaction_btn(self):
        from logic.comsys.map.InteractionInvokeBtnWidget import InteractionInvokeBtnWidget
        from logic.comsys.lobby.LobbyInteractionUI import LobbyInteractionUI
        self._inter_invoke_btn_widget = InteractionInvokeBtnWidget(self.panel.btn_interaction, self.panel, LobbyInteractionUI, self.__class__.__name__)
        self.panel.btn_interaction.BindMethod('OnBegin', self._inter_invoke_btn_widget.on_touch_inter_begin)
        self.panel.btn_interaction.BindMethod('OnDrag', self._inter_invoke_btn_widget.on_touch_inter_drag)
        self.panel.btn_interaction.BindMethod('OnEnd', self._inter_invoke_btn_widget.on_touch_inter_end)
        self.panel.btn_interaction.BindMethod('OnCancel', self._inter_invoke_btn_widget.on_touch_inter_cancel)

    def keyboard_use_spray_ui(self, msg, keycode):
        return self._inter_invoke_btn_widget.on_switch_interactio_key_down_up(msg, keycode)

    def keyboard_use_spray_ui_cancel(self):
        return self._inter_invoke_btn_widget.on_switch_interactio_key_cancel()

    def on_click_gride_btn(self, btn, touch):
        self.switch_gride_show(not self._is_gride_show)

    def switch_gride_show(self, show):
        self._is_gride_show = show
        if show:
            self.panel.btn_gride.SetSelect(True)
            self.panel.StopAnimation('disappear_gride')
            self.panel.PlayAnimation('show_gride')
        else:
            self.panel.btn_gride.SetSelect(False)
            self.panel.StopAnimation('show_gride')
            self.panel.PlayAnimation('disappear_gride')