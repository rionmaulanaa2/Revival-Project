# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/BackgroundManager.py
from __future__ import absolute_import
import six
import render
import cc
import time
from common.utils.timer import CLOCK
from common.framework import Singleton
from common.utils import ui_utils
from logic.manager_agents.manager_decorators import sync_exec

class SceneBackground(Singleton):
    ALIAS_NAME = 'scene_background'

    def init(self):
        self._panel_dict = {}
        self._tex = None
        self._rt = None
        self._cur_panel = None
        self._finish_time = -1
        self._render_timer = None
        self._retain_render_timer = None
        return

    def init_rt(self):
        if self._rt:
            return
        screen_size = global_data.ui_mgr.design_screen_size
        self._tex = render.texture.create_empty(int(screen_size.width), int(screen_size.height), render.PIXEL_FMT_A8R8G8B8, True)
        self._rt = cc.RenderTexture.createWithITexture(self._tex)
        self._rt.retain()

    def leave_lobby(self):
        self.destroy_all_background()
        self.destroy_rt()

    def destroy_rt(self):
        if self._rt:
            self._rt.release()
        self._rt = None
        self._tex = None
        return

    def destroy_all_background(self):
        for panel in six.itervalues(self._panel_dict):
            panel.destroy()

        self._panel_dict = {}
        self._set_active_panel(None)
        return

    def destroy_background(self, cls_name):
        if cls_name in self._panel_dict:
            panel = self._panel_dict.pop(cls_name)
            panel.destroy()
            if self._cur_panel == cls_name:
                self._set_active_panel(None)
        return

    def create_ui(self, cls_name, path='logic.comsys.scene_background'):
        if cls_name in self._panel_dict:
            return
        self._panel_dict[cls_name] = global_data.ui_mgr.show_ui(cls_name, path)

    def get_ui(self, cls_name):
        return self._panel_dict.get(cls_name, None)

    def set_active_background(self, cls_name, path='logic.comsys.scene_background'):
        self.init_rt()
        self.create_ui(cls_name, path)
        self._set_active_panel(cls_name)
        self._draw_ui_to_rt()

    def get_texture(self):
        return self._tex

    def start_render(self, t):
        if t == -1:
            self._finish_time = -1
        else:
            self._finish_time = max(time.time() + t, self._finish_time)
        if self._render_timer:
            global_data.game_mgr.unregister_logic_timer(self._render_timer)
            self._render_timer = None
        self._render_timer = global_data.game_mgr.register_logic_timer(self.tick, 0.0333, mode=CLOCK)
        return

    def stop_render(self):
        self._finish_time = 0
        if self._render_timer:
            global_data.game_mgr.unregister_logic_timer(self._render_timer)
            self._render_timer = None
        return

    def tick(self):
        if self._finish_time != -1 and time.time() > self._finish_time:
            self.stop_render()
        self._draw_ui_to_rt()

    @sync_exec
    def _draw_ui_to_rt(self):
        panel = self._panel_dict.get(self._cur_panel)
        if not panel or not panel.isValid():
            return
        rt = self._rt
        rt.begin()
        if hasattr(rt, 'addCommandsForNode'):
            rt.addCommandsForNode(panel.get())
        else:
            panel.visit()
        rt.end()

    def _set_active_panel(self, cls_name):
        self._cur_panel = cls_name
        if cls_name and not self._retain_render_timer:
            cb = lambda *args: self._draw_ui_to_rt()
            self._retain_render_timer = global_data.game_mgr.register_logic_timer(cb, 60, mode=CLOCK)
        elif not cls_name and self._retain_render_timer:
            global_data.game_mgr.unregister_logic_timer(self._retain_render_timer)
            self._retain_render_timer = None
        return

    def get_cur_panel(self):
        return self._cur_panel