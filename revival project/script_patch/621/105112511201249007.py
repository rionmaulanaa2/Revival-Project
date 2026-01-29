# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/test/TestTouchUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_MSG_ZORDER
import cc
from common.const import uiconst

class TestTouchUI(BasePanel):
    DLG_ZORDER = TOP_MSG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'test/test_touch'

    def on_init_panel(self):
        self.init_parameters()
        self.init_mouse_event()

    def init_parameters(self):
        self.last_location = None
        return

    def init_mouse_event(self):
        listener = cc.EventListenerMouse.create()
        listener.setOnMouseDownCallback(self.on_mouse_down)
        listener.setOnMouseMoveCallback(self.on_mouse_move)
        listener.setOnMouseUpCallback(self.on_mouse_up)
        cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(listener, self.panel.touch_layer.get())

    def on_mouse_down(self, event):
        mouse_type = event.getMouseButton()
        player = global_data.cam_lplayer
        if not player:
            return
        if mouse_type == 0:
            player.send_event('E_START_AUTO_FIRE')
            if player.ev_g_is_in_mecha():
                global_data.mecha.logic.ev_g_action_down('action1')
        elif mouse_type == 1:
            if player.ev_g_in_aim():
                player.send_event('E_QUIT_AIM')
                return
            if player.ev_g_in_right_aim():
                player.send_event('E_QUIT_RIGHT_AIM')
                return
            if player.ev_g_aim_lens_type():
                player.send_event('E_TRY_AIM')
            else:
                player.send_event('E_TRY_RIGHT_AIM')
            if player.ev_g_is_in_mecha():
                global_data.mecha.logic.ev_g_action_down('action4')

    def on_mouse_move(self, event):
        wpos = event.getLocation()
        if not self.last_location:
            self.last_location = wpos
        lx, ly = self.last_location.x, self.last_location.y
        nx, ny = wpos.x, wpos.y
        dx, dy = (nx - lx) / 200.0, (ny - ly) / 200.0
        global_data.emgr.camera_on_acc_input_update.emit(dx, dy)
        self.last_location = wpos

    def on_mouse_up(self, event):
        mouse_type = event.getMouseButton()
        player = global_data.cam_lplayer
        if not player:
            return
        if mouse_type == 0:
            player.send_event('E_STOP_AUTO_FIRE')
            if player.ev_g_is_in_mecha():
                global_data.mecha.logic.send_event('E_ACTION_UP', 'action1')
        elif mouse_type == 1:
            if player.ev_g_is_in_mecha():
                global_data.mecha.logic.send_event('E_ACTION_UP', 'action4')