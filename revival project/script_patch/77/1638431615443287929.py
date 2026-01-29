# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/InteractionInvokeBtnWidget.py
from __future__ import absolute_import
import six
from logic.gutils import pc_utils
from data import hot_key_def
from logic.vscene.parts.ctrl.ShortcutFunctionalityMutex import try_claim_shortcut_functionality, try_unclaim_shortcut_functionality
import cc
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock

class InteractionInvokeBtnWidget(object):

    def __init__(self, invoke_btn, move_listener_node, interaction_ui_class, shortcut_functionality_claimer):
        from common.uisys.uielment.CCNode import CCNode
        from logic.comsys.interaction.InteractionBaseUI import InteractionBaseUI
        self._invoke_btn = invoke_btn
        self._move_listener_node = move_listener_node
        self._interaction_ui_class = interaction_ui_class
        self._shortcut_functionality_claimer = shortcut_functionality_claimer
        self.is_touching_inter = False
        self.inter_touch_begin_location = None
        self.up_vec2 = cc.Vec2(0, 1)
        self._mouse_inter_position = None
        self._mouse_listener = None
        self._mouse_position = None
        self._mouse_prev_position = None
        self._interaction_ui_class()
        return

    def destory(self):
        self._unreg_mouse_event()
        self._move_listener_node = None
        return

    def decorate_touch_inter_begin_logic(self, decorator):
        if not callable(decorator):
            return
        self._on_touch_inter_begin = decorator(self._on_touch_inter_begin)

    def on_touch_inter_begin(self, btn, touch):
        if not try_claim_shortcut_functionality((hot_key_def.SWITCH_INTERACTION,), self._shortcut_functionality_claimer):
            return False
        return self._on_touch_inter_begin(btn, touch)

    def _on_touch_inter_begin(self, btn, touch):
        self.inter_touch_begin_location = touch.getLocation()
        self.is_touching_inter = True
        inter_ui = global_data.ui_mgr.get_ui(self._interaction_ui_class.__name__)
        if inter_ui:
            inter_ui.show()
        return True

    def on_touch_inter_drag(self, btn, touch):
        if self.is_touching_inter and self.inter_touch_begin_location:
            inter_ui = global_data.ui_mgr.get_ui(self._interaction_ui_class.__name__)
            if not inter_ui:
                return
            touch_rel_pos = touch.getLocation()
            touch_rel_pos.subtract(self.inter_touch_begin_location)
            touch_angle = touch_rel_pos.getAngle(self.up_vec2)
            if touch_rel_pos.length() > 3:
                inter_ui.set_sel_angle(touch_angle)
                inter_ui.try_select_action(touch_angle)
        return True

    def on_touch_inter_end(self, btn, touch):
        if not try_unclaim_shortcut_functionality((hot_key_def.SWITCH_INTERACTION,), self._shortcut_functionality_claimer):
            return True
        return self._on_touch_inter_end(btn, touch)

    def _on_touch_inter_end(self, btn, touch):
        self.inter_touch_begin_location = None
        self.is_touching_inter = False
        inter_ui = global_data.ui_mgr.get_ui(self._interaction_ui_class.__name__)
        if inter_ui:
            inter_ui.try_action()
            inter_ui.hide()
        return True

    def on_touch_inter_cancel(self, btn, touch):
        return self.on_touch_inter_end(btn, touch)

    def on_switch_interactio_key_down_up(self, msg, keycode):
        pc_op_mode = pc_utils.is_pc_control_enable()
        import game
        if msg in [game.MSG_KEY_DOWN, game.MSG_MOUSE_DOWN]:
            _break = False
            if global_data.is_pc_mode:
                if not try_claim_shortcut_functionality((hot_key_def.SWITCH_INTERACTION,), self._shortcut_functionality_claimer + '_keyboard'):
                    _break = True
            if not _break:
                from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
                from common.utils.cocos_utils import get_cocos_center_design_pos
                pos = get_cocos_center_design_pos()
                self._mouse_inter_position = cc.Vec2(*pos)
                ok = self._on_touch_inter_begin(self._invoke_btn, TouchMock(self._mouse_inter_position))
                if not ok:
                    return
                if pc_op_mode:
                    global_data.mouse_mgr.set_cursor_move_enable(True)
                self._reg_mouse_event(skip_pc_control_enable_test=not pc_op_mode)
        else:
            _break = False
            if global_data.is_pc_mode:
                if not try_unclaim_shortcut_functionality((hot_key_def.SWITCH_INTERACTION,), self._shortcut_functionality_claimer + '_keyboard'):
                    _break = True
            if not _break:
                from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
                self._on_touch_inter_end(self._invoke_btn, TouchMock(self._mouse_inter_position))
                if pc_op_mode:
                    global_data.mouse_mgr.set_cursor_move_enable(False)
                self._unreg_mouse_event()

    def on_switch_interactio_key_cancel(self):
        if self.is_touching_inter:
            pc_op_mode = pc_utils.is_pc_control_enable()
            self.inter_touch_begin_location = None
            self.is_touching_inter = False
            inter_ui = global_data.ui_mgr.get_ui(self._interaction_ui_class.__name__)
            if not inter_ui:
                return
            inter_ui.hide()
            if pc_op_mode:
                global_data.mouse_mgr.set_cursor_move_enable(False)
            self._unreg_mouse_event()
        return

    def on_mouse_move(self, event):
        pos = event.getLocation()
        self._mouse_position = pos
        delta = None
        if self._mouse_prev_position is not None:
            delta = cc.Vec2(pos.x - self._mouse_prev_position.x, pos.y - self._mouse_prev_position.y)
        if delta is None:
            delta = cc.Vec2(0.0, 0.0)
        if self.is_touching_inter:
            self._mouse_inter_position = cc.Vec2(self._mouse_inter_position.x + delta.x, self._mouse_inter_position.y + delta.y)
            _pos = cc.Vec2(self._mouse_inter_position.x, self._mouse_inter_position.y)
            self.on_touch_inter_drag(self._invoke_btn, TouchMock(_pos))
        self._mouse_prev_position = self._mouse_position
        return

    def _reg_mouse_event(self, skip_pc_control_enable_test=False):
        if self._mouse_listener:
            return
        else:
            if not skip_pc_control_enable_test:
                if not pc_utils.is_pc_control_enable():
                    return
            self._mouse_listener = cc.EventListenerMouse.create()
            self._mouse_prev_position = None
            self._mouse_listener.setOnMouseMoveCallback(self.on_mouse_move)
            cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(self._mouse_listener, self._move_listener_node.get())
            return

    def _unreg_mouse_event(self):
        if self._mouse_listener:
            cc.Director.getInstance().getEventDispatcher().removeEventListener(self._mouse_listener)
            self._mouse_listener = None
        return