# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/SceneSnapShotUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BG_ZORDER, UI_TYPE_EFFECT
import time
import game3d

class RenderFrame(object):

    def __init__(self, width, height):
        self.tex = None
        self.rt = None
        self.sprite_parent = None
        self._sprite_child = None
        self._callback = None
        self.width = width
        self.height = height
        self._render_timer_id = None
        self._last_capture_time = 0
        self._is_in_capture = False
        self._ui_exceptions = []
        self._hidden_ui_names = []
        return

    def set_render_frame_output(self, sprite_parent, sprite=None, callback=None):
        self._sprite_child = sprite
        self._callback = callback
        self.sprite_parent = sprite_parent

    def set_exception_uis(self, uis):
        self._ui_exceptions = uis

    def is_in_capture(self):
        return self._is_in_capture

    def destroy(self):
        if self._is_in_capture:
            log_error('Should not release before finish!!!!')
            return
        else:
            self.tex = None
            self.sprite_parent = None
            self._sprite_child = None
            self._callback = None
            return

    def init_render_frame(self):
        cur_time = time.time()
        if cur_time - self._last_capture_time < 3 or self._is_in_capture:
            log_error('ENTER CATCH TOO SOON')
            return
        self._last_capture_time = cur_time
        self._is_in_capture = True
        import render
        import cc
        if not self.tex:
            self.tex = render.texture.create_empty(int(self.width), int(self.height), render.PIXEL_FMT_A8R8G8B8, False)
        data = self.tex.get_data()

        def capture_func():
            import device_compatibility
            self._is_in_capture = False
            if not self._ui_exceptions:
                global_data.ui_mgr.set_all_ui_visible(True)
            else:
                global_data.ui_mgr.revert_hide_all_ui_by_key_action(self.__class__.__name__, self._hidden_ui_names)
                self._hidden_ui_names = []
            if self.tex:
                self.tex.flush_data(data)
                screen_tex = cc.Texture2D.createWithITexture(self.tex)
                if not self._sprite_child:
                    screen_sprite = cc.Sprite.create()
                    if self.sprite_parent:
                        self.sprite_parent.addChild(screen_sprite)
                else:
                    screen_sprite = self._sprite_child
                if screen_sprite and screen_sprite.isValid():
                    rect = cc.Rect(0, 0, self.width, self.height)
                    screen_sprite.setSpriteFrame(cc.SpriteFrame.createWithTexture(screen_tex, rect))
                    if self.sprite_parent:
                        screen_sprite.setPosition(cc.Vec2(0, 0))
                        screen_sprite.setAnchorPoint(cc.Vec2(0, 0))
                    screen_sprite.getTexture().setAntiAliasTexParameters()
                    from logic.comsys.effect.ui_effect import create_shader
                    if game3d.get_platform() == game3d.PLATFORM_WIN32 and not device_compatibility.IS_DX:
                        gl_swap_rgb = create_shader('positiontexture_bgra_to_rgba', 'positiontexture_bgra_to_rgba')
                    else:
                        gl_swap_rgb = create_shader('positiontexture_rgba_to_rgb', 'positiontexture_rgba_to_rgb')
                    program_swap_rgb = cc.GLProgramState.getOrCreateWithGLProgram(gl_swap_rgb)
                    screen_sprite.setGLProgramState(program_swap_rgb)
                if self._callback:
                    self._callback()

        if not self._ui_exceptions:
            global_data.ui_mgr.set_all_ui_visible(False)
        else:
            self._hidden_ui_names = global_data.ui_mgr.hide_all_ui_by_key(self.__class__.__name__, [], self._ui_exceptions)
        if not (game3d.get_platform() == game3d.PLATFORM_IOS and global_data.channel.get_os_ver() == '14.0'):
            render.save_screen_to_array(data, int(self.width), int(self.height), capture_func)


from common.const import uiconst

class SceneSnapShotUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/empty_no_scale'
    IS_FULLSCREEN = True
    DLG_ZORDER = BG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_EFFECT

    def on_init_panel(self):
        sz = self.panel.getContentSize()
        self.render_frame = RenderFrame(sz.width * self.panel.getScaleX(), sz.height * self.panel.getScaleY())
        self.render_frame.set_render_frame_output(self.panel)

    def on_finalize_panel(self):
        if self.render_frame:
            self.render_frame.destroy()
            self.render_frame = None
        return

    def take_scene_snapshot(self):
        if self.render_frame:
            self.render_frame.init_render_frame()
            self.panel.SetTimeOut(10, self.check_for_close)

    def check_for_close(self):
        if self.render_frame:
            if not self.render_frame.is_in_capture():
                self.close()
            else:
                self.panel.SetTimeOut(10, self.check_for_close)


class ScreenSnapShotUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/empty_no_scale'
    IS_FULLSCREEN = True
    DLG_ZORDER = BG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_EFFECT

    def on_init_panel(self, width, height):
        self.render_frame = RenderFrame(width, height)

    def on_finalize_panel(self):
        if self.render_frame:
            self.render_frame.destroy()
            self.render_frame = None
        return

    def take_screen_snapshot(self, sprite, callback, exception_uis):

        def finish_callback():
            import cc
            if callback and callable(callback):
                callback()
            self.close()

        if self.render_frame:
            self.render_frame.set_render_frame_output(None, sprite, finish_callback)
            self.render_frame.set_exception_uis(exception_uis)
            self.render_frame.init_render_frame()
        return

    def take_screen_snapshot_test(self):

        def finish_callback():
            import cc

        if self.render_frame:
            self.render_frame.set_render_frame_output(self.panel, None, finish_callback)
            self.render_frame.init_render_frame()
        return

    def test(self):
        from common.utils.ui_utils import get_screen_size
        sz = get_screen_size()
        from logic.comsys.common_ui.SceneSnapShotUI import ScreenSnapShotUI
        global_data.ui_mgr.close_ui('ScreenSnapShotUI')
        ui_inst = ScreenSnapShotUI(None, sz.width, sz.height)
        ui_inst.take_screen_snapshot_test()
        return