# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/loading/loading.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const import uiconst
import game3d
import device_compatibility
import common.utils.timer as timer
WAIT_SCENE_S = 10

class ILoadingInterface(object):

    def update_percent(self, value):
        raise 'loading widget must implement interface [update_percent]'

    def loading_init(self):
        raise 'loading widget must implement interface [loading_init]'

    def loading_end(self):
        raise 'loading widget must implement interface [loading_end]'

    def loading_update(self, dt):
        raise 'loading widget must implement interface [loading_update]'


class UILoadingWidget(BasePanel, ILoadingInterface):
    PANEL_CONFIG_NAME = 'common/common_loading'
    DLG_ZORDER = uiconst.LOADING_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = uiconst.UI_TYPE_TRANS
    IS_FULLSCREEN = True
    ASYNC_LOAD_IMAGE = False

    def play_loading_ani(self):
        self.panel.StopAnimation('loading')
        self.panel.PlayAnimation('loading')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'camera_inited_event': self.on_camera_inited,
           'event_finish_detail': self.on_scene_finish_detail
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self, *args, **kwargs):
        from common.utils.ui_path_utils import BG_LOADING
        self.panel.img_bg and self.panel.img_bg.SetDisplayFrameByPath('', BG_LOADING, force_sync=True)
        self.camera_inited = False
        self._wait_scene_s = 0
        self._wait_scene_timer = None
        self._delay_close_timer = None
        self._scene_finish = False
        self._force_close = False
        self.process_event(True)
        self.play_loading_ani()
        global_data.emgr.loading_begin_event.emit()
        self.percent = 0
        self.update_percent(0)
        if game3d.get_platform() == game3d.PLATFORM_IOS and game3d.get_engine_svn_version() < 1001744 or not device_compatibility.is_device_gpu_qualified():
            global_data.sound_mgr.set_background(True)
        return

    def on_finalize_panel(self):
        super(UILoadingWidget, self).on_finalize_panel()
        self._release_wait_scene_timer()
        self._release_delay_close_timer()
        self.process_event(False)
        if game3d.get_platform() == game3d.PLATFORM_IOS and game3d.get_engine_svn_version() < 1001744 or not device_compatibility.is_device_gpu_qualified():
            global_data.sound_mgr.set_background(False)

    def get_limited_percent(self, value):
        return max(min(100, int(value)), 0)

    def update_percent(self, value):
        if not self.panel:
            return
        value = self.get_limited_percent(value)
        self.percent = value
        self.panel.txt_loading_persent.SetString(str(value) + '%')

    def set_txt_loading(self, text_id):
        if not self.panel:
            return
        self.panel.txt_loading.SetString(text_id)

    def loading_init(self):
        pass

    def loading_end(self):
        return self.percent == 100

    def set_preload_shader_cache_txt(self):
        if self.panel.lab_load_tips:
            self.panel.lab_load_tips.setVisible(True)

    def loading_update(self, dt):
        pass

    def on_scene_finish_detail(self, *args):
        self.finish_loading()
        self._scene_finish = True

    def _release_wait_scene_timer(self):
        self._force_close = False
        if self._wait_scene_timer:
            global_data.game_mgr.unregister_logic_timer(self._wait_scene_timer)
        self._wait_scene_timer = None
        self._wait_scene_s = 0
        return

    def _release_delay_close_timer(self):
        if self._delay_close_timer:
            global_data.game_mgr.unregister_logic_timer(self._delay_close_timer)
        self._delay_close_timer = None
        return

    def finish_loading(self):
        self._release_wait_scene_timer()
        if not (self.panel and self.panel.isValid()):
            return
        self.update_percent(100)
        self._release_delay_close_timer()
        self._delay_close_timer = global_data.game_mgr.register_logic_timer(self.check_close, interval=0.1, times=1, mode=timer.CLOCK)

    def on_camera_inited(self):
        self.camera_inited = True
        self._release_wait_scene_timer()
        if self.need_wait_scene_finish_detail():

            def _wait():
                if not (self.panel and self.panel.isValid()):
                    self._release_wait_scene_timer()
                    return
                self._wait_scene_s += 1
                if self._wait_scene_s >= WAIT_SCENE_S:
                    self._force_close = True
                    self.on_scene_finish_detail()

            self._wait_scene_timer = global_data.game_mgr.register_logic_timer(_wait, interval=1, mode=timer.CLOCK)
        else:
            self.on_scene_finish_detail()

    def close(self):
        super(UILoadingWidget, self).close()
        global_data.uisystem.RecordUsedSpritePaths()
        if global_data.ui_mgr:
            global_data.ui_mgr.remove_unused_textures()
        global_data.emgr.loading_end_event.emit()

    def need_wait_scene_finish_detail(self):
        if self._force_close:
            return False
        from logic.vscene import scene_type
        from logic.gcommon.common_utils import parachute_utils
        if global_data.scene_type != scene_type.SCENE_TYPE_BATTLE:
            return False
        if global_data.cam_lplayer and global_data.cam_lplayer.share_data.ref_parachute_stage not in (parachute_utils.STAGE_LAND, parachute_utils.STAGE_ISLAND):
            return False
        if global_data.game_mode and global_data.game_mode.is_pve():
            return False
        return not self._scene_finish

    def can_close(self):
        return self.camera_inited and not self.need_wait_scene_finish_detail()

    def check_close(self):
        if self.is_valid() and self.can_close():
            self.close()
            return True
        return False