# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/art_check_ui/ArtCheckHumanDisplayUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel, MAIN_UI_LIST
from common.const import uiconst
from logic.gcommon.common_const import scene_const
from common.cfg import confmgr
EXCEPT_HIDE_UI_LIST = []
HIDE_UI_LIST = set(['ArtCheckMainUI'])
ROTATE_FACTOR = 850
CAM_DISPLAY_PIC = {0: 'gui/ui_res_2/common/icon/icon_glass_small.png',
   1: 'gui/ui_res_2/common/icon/icon_glass_big.png'
   }

class ArtCheckHumanDisplayUI(BasePanel):
    PANEL_CONFIG_NAME = 'art_check/art_check_display'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_role_touch.OnDrag': 'on_rotate_drag',
       'btn_change.OnClick': 'on_refresh_model'
       }
    GLOBAL_EVENT = {'change_artcheck_display_camera_state': 'update_camera_info'
       }

    def on_init_panel(self, create_scene_callback, *args, **kargs):
        self.create_scene_callback = create_scene_callback
        self.init_panel()
        self.init_parameters()
        self.init_scene()

    def init_scene(self):
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_ART_CHECK_DISPLAY, '3', finish_callback=self.on_change_scene, scene_content_type='Zhanshi', belong_ui_name='ArtCheckHumanDisplayUI')

    def init_parameters(self):
        self.display_visible = False
        self.model_data = {}
        self.cur_cam_mode = 1
        self.display_type = -1
        self.camera_info = []

    def init_panel(self):
        self.hide_main_ui(ui_list=HIDE_UI_LIST | MAIN_UI_LIST, exceptions=EXCEPT_HIDE_UI_LIST, exception_types=())
        self.panel.btn_close.BindMethod('OnClick', self.on_click_btn_close)
        self.panel.btn_glass.BindMethod('OnClick', self.on_click_change_cam_mode)
        self.panel.temp_btn_use.btn_common.BindMethod('OnClick', self.change_display_ui_state)

    def on_refresh_model(self, *args):
        pass

    def on_click_btn_close(self, *args):
        self.close()

    def on_change_scene(self, scene_type):
        if self.create_scene_callback:
            self.create_scene_callback()
        scene = global_data.game_mgr.scene
        if scene and scene.is_hdr_enable:
            scene.set_bloom_c_env('zhanshi_human')
            scene.setup_env_light_info('zhanshi', 'on_ground')

    def on_rotate_drag(self, layer, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def update_camera_info(self, camera_info):
        self.camera_info = camera_info
        global_data.emgr.set_lobby_scene_display_type.emit(str(camera_info[self.cur_cam_mode]), True)
        global_data.game_mgr.show_tip('\xe4\xbf\xae\xe6\x94\xb9\xe9\x95\x9c\xe5\xa4\xb4\xe6\x88\x90\xe5\x8a\x9f')

    def on_click_change_cam_mode(self, *args):
        if not self.camera_info:
            data = confmgr.get('lobby_model_display_conf', 'RoleDisplayCam', 'Content', default={})
            camera_info = data['11']
            self.camera_info = [camera_info['near_cam'], camera_info['far_cam'], camera_info['near_mid_cam']]
        cur_mode = (self.cur_cam_mode + 1) % 2
        self.cur_cam_mode = cur_mode
        self.display_type = str(self.camera_info[cur_mode])
        self.panel.icon_glass.SetDisplayFrameByPath('', CAM_DISPLAY_PIC[self.cur_cam_mode])
        global_data.emgr.set_lobby_scene_display_type.emit(self.display_type, True)

    def on_finalize_panel(self):
        super(ArtCheckHumanDisplayUI, self).on_finalize_panel()
        global_data.emgr.change_model_display_scene_item.emit(None)
        global_data.emgr.leave_current_scene.emit()
        self.show_main_ui()
        return

    def change_display_ui_state(self, *args):
        self.display_visible = not self.display_visible
        self.panel.nd_display.setVisible(self.display_visible)
        self.panel.temp_btn_use.btn_common.SetText('\xe9\x9a\x90\xe8\x97\x8f\xe8\xa7\x92\xe8\x89\xb2\xe5\xb1\x95\xe7\xa4\xba\xe7\x95\x8c\xe9\x9d\xa2') if self.display_visible else self.panel.temp_btn_use.btn_common.SetText('\xe6\x98\xbe\xe7\xa4\xba\xe8\xa7\x92\xe8\x89\xb2\xe5\xb1\x95\xe7\xa4\xba\xe7\x95\x8c\xe9\x9d\xa2')

    def set_model_path(self, mpath):
        if not mpath:
            return
        self.model_data['mpath'] = mpath