# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/spray/SprayUIPC.py
from __future__ import absolute_import
import six
from logic.gcommon.common_utils.local_text import get_text_by_id
from .SprayUI import SprayBaseUI
from common.utils.cocos_utils import ccp
import cc
import math

class SprayUIPC(SprayBaseUI):
    PANEL_CONFIG_NAME = 'battle/fight_action_spray_panel_pc'
    HOT_KEY_FUNC_MAP = {'close_wheel_panel': 'mouse_close_wheel_panel'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'switch_interaction': {'node': 'nd_hint.nd_hint_1.temp_pc'},'close_wheel_panel': {'node': 'nd_hint.nd_hint_2.temp_pc'}}

    def on_init_panel(self, *args, **kwargs):
        self._mouse_listener = None
        self._last_delta_vec = None
        super(SprayUIPC, self).on_init_panel(*args, **kwargs)
        self.panel.btn_close.setVisible(False)
        return

    def _register_mouse_event(self):
        if self._mouse_listener:
            return
        self._mouse_listener = cc.EventListenerMouse.create()
        self._mouse_listener.setOnMouseMoveCallback(self._on_mouse_move)
        cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(self._mouse_listener, self.panel.get())

    def _on_mouse_move(self, event):
        self.panel.nd_select.setRotation(math.degrees(self.sel_angle))
        self.update_tips()

    def _unregister_mouse_event(self):
        if self._mouse_listener:
            cc.Director.getInstance().getEventDispatcher().removeEventListener(self._mouse_listener)
            self._mouse_listener = None
        return

    def on_finalize_panel(self):
        super(SprayUIPC, self).on_finalize_panel()
        self._unregister_mouse_event()

    def show(self):
        super(SprayUIPC, self).show()
        self.panel.btn_close.setVisible(False)
        is_empty = self.is_action_dict_empty()
        self.panel.nd_empty.setVisible(is_empty)
        self.panel.lab_item.setVisible(not is_empty)
        self.panel.nd_hint.setVisible(not is_empty)
        self._register_mouse_event()

    def hide(self):
        super(SprayUIPC, self).hide()
        self._unregister_mouse_event()

    def mouse_close_wheel_panel(self, *args):
        self.close()

    def init_tips(self):
        tip_1 = self.panel.nd_hint.nd_hint_1.temp_pc.pc_tip_list.GetItem(0)
        tip_2 = self.panel.nd_hint.nd_hint_2.temp_pc.pc_tip_list.GetItem(0)
        if tip_1:
            tip_1.lab_hint1.SetString(get_text_by_id(920823))
        if tip_2:
            tip_2.lab_hint1.SetString(get_text_by_id(920824))
            tip_2.lab_pc.setVisible(True)
            tip_2.lab_pc.nd_auto_fit.setVisible(False)
            tip_2.lab_pc.SetString('')

    def update_tips(self):
        tip_1 = self.panel.nd_hint.nd_hint_1.temp_pc.pc_tip_list.GetItem(0)
        tip_2 = self.panel.nd_hint.nd_hint_2.temp_pc.pc_tip_list.GetItem(0)
        if self.select_idx not in self.action_dict:
            if not tip_1:
                return
            tip_1.lab_hint2.SetString(get_text_by_id(80595))
            self.panel.nd_hint.nd_hint_1.setVisible(True)
            self.panel.nd_hint.nd_hint_2.setVisible(False)
        else:
            if not tip_1 or not tip_2:
                return
            tip_1.lab_hint2.SetString(get_text_by_id(80338))
            self.panel.nd_hint.nd_hint_1.setVisible(True)
            self.panel.nd_hint.nd_hint_2.setVisible(True)
            tip_2.lab_pc.setVisible(True)
            tip_2.lab_pc.nd_auto_fit.setVisible(False)
            tip_2.lab_pc.SetString('')

    def on_hot_key_closed_state(self):
        self.panel.nd_action_spray_close.setVisible(True)

    def is_action_dict_empty(self):
        if len(self.action_dict) <= 0:
            return True
        for k, v in six.iteritems(self.action_dict):
            if v != 0:
                return False

        return True