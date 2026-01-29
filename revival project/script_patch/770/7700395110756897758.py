# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/UIRTManager.py
from __future__ import absolute_import
from common.framework import Singleton
import cc
import game3d
import render
from logic.manager_agents.manager_decorators import sync_exec
from common.cfg import confmgr

class UIRTManager(Singleton):
    ALIAS_NAME = 'ui_rt_mgr'

    def init(self):
        self.ui_rts = {}

    def on_finalize(self):
        self._clear_all_ui_rt()

    def create_ui_rt(self, ui_rt_key, info_data=None):
        ui_rt_key = str(ui_rt_key)
        if ui_rt_key in self.ui_rts:
            return self.ui_rts[ui_rt_key]
        if not info_data:
            return
        resource_path = info_data.get('UI_path')
        if not resource_path:
            return
        panel = global_data.uisystem.load_template_create(resource_path)
        panel.retain()
        size = panel.getContentSize()
        old_design_size = global_data.ui_mgr.design_screen_size
        scale = min(old_design_size.width / size.width, old_design_size.height / size.height)
        if global_data.is_low_mem_mode:
            scale = scale * 0.5
        render_texture_size = (size.width * scale, size.height * scale)
        panel.setAnchorPoint(cc.Vec2(0, 0))
        if game3d.get_render_device() not in (game3d.DEVICE_GLES, game3d.DEVICE_GL):
            panel.setScale(scale)
            panel.SetPosition(0, 0)
        else:
            panel.setScaleX(scale)
            panel.setScaleY(-scale)
            panel.SetPosition(0, size.height * scale)
        tex = render.texture.create_empty(int(render_texture_size[0]), int(render_texture_size[1]), render.PIXEL_FMT_A8R8G8B8, True)
        rt = cc.RenderTexture.createWithITexture(tex)
        rt.retain()
        self.ui_rts[ui_rt_key] = (
         rt, tex, panel)
        return (
         rt, tex, panel)

    @sync_exec
    def _draw_ui_to_rt(self, rt, panel):
        if not panel or not panel.isValid():
            return
        rt.beginWithClear(0, 0, 0, 0, 0, 0)
        if hasattr(rt, 'addCommandsForNode'):
            rt.addCommandsForNode(panel.get())
        else:
            panel.visit()
        rt.end()

    def _clear_ui_rt(self, ui_rt_key):
        ui_rt_key = str(ui_rt_key)
        if ui_rt_key not in self.ui_rts:
            return
        rt, tex, panel = self.ui_rts[ui_rt_key]
        if panel:
            panel.Destroy()
            panel.release()
        rt.release()
        del tex
        del self.ui_rts[ui_rt_key]

    def _clear_all_ui_rt(self):
        for ui_rt_key in self.ui_rts.keys():
            self._clear_ui_rt(ui_rt_key)

    def update_ui_rt(self, ui_rt_key):
        ui_rt_key = str(ui_rt_key)
        if ui_rt_key not in self.ui_rts:
            return
        rt, tex, panel = self.ui_rts[ui_rt_key]
        self._draw_ui_to_rt(rt, panel)