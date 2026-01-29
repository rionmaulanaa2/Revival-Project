# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/MoveRockerTouchUI.py
from __future__ import absolute_import
import math3d
import world
from common.uisys.basepanel import BasePanel
from common.utils.cocos_utils import ccp
from data.camera_state_const import AIM_MODE
from logic.client.const.camera_const import POSTURE_GROUND
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon.cdata import status_config as st_const
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.common_const.animation_const import MOVE_STATE_WALK, MOVE_STATE_RUN
UP_VECTOR = ccp(0, 1)
from common.const.uiconst import BG_ZORDER
TAN45 = 1.0
TAN30 = 0.577
from common.const import uiconst

class MoveRockerTouchUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/rocker_touch'
    DLG_ZORDER = BG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def set_touch_layer_swallow_touch(self, flag):
        if self.panel.rocker_touch:
            self.panel.rocker_touch.SetSwallowTouch(flag)

    def register_touch_layer(self, clone_nd, nd_conf, begin_func, drag_func, end_func, cancel_func):
        name = nd_conf.get('name', '')
        bSwallow = nd_conf.get('bSwallow', False)
        from common.uisys.uielment.CCLayer import CCLayer
        left_bottom_pos = clone_nd.ConvertToWorldSpacePercentage(0, 0)
        right_top_pos = clone_nd.ConvertToWorldSpacePercentage(100, 100)
        nd = CCLayer.Create()
        nd.SetContentSize(right_top_pos.x - left_bottom_pos.x, right_top_pos.y - left_bottom_pos.y)
        nd.setPosition(left_bottom_pos)
        nd.setAnchorPoint(ccp(0, 0))
        nd.HandleTouchMove(True, bSwallow, False)
        nd.set_sound_enable(False)
        self.panel.AddChild(name, nd)

        @nd.callback()
        def OnBegin(layer, touch):
            if begin_func:
                return begin_func(layer, touch)
            else:
                return False

        @nd.callback()
        def OnDrag(layer, touch):
            if drag_func:
                drag_func(layer, touch, layer.GetMovedDistance())

        @nd.callback()
        def OnEnd(layer, touch):
            if end_func:
                end_func(layer, touch)

        @nd.callback()
        def OnCancel(layer, touch):
            if cancel_func:
                cancel_func(layer, touch)

    def set_touch_nd_visible(self, nd_name, visible):
        nd = getattr(self.panel, nd_name)
        if nd:
            nd.setVisible(visible)

    def get_touch_nd(self, nd_name):
        nd = getattr(self.panel, nd_name)
        return nd