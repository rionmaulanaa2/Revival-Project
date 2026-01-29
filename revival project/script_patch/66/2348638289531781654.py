# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/ui_event_utils.py
from __future__ import absolute_import
import world
from logic.gcommon.const import NEOX_UNIT_SCALE
import collision
from logic.gcommon.common_const.collision_const import GROUP_ALL_SHOOTUNIT, WATER_GROUP
import cc

def AddMouseWheelEvent(node, callback):
    if not (node.isValid() and callback):
        return

    def func_onMouseWheel(scrollValue):
        if node.isValid():
            if not node.isTouchEnabled():
                return False
            touch_mgr = global_data.touch_mgr_agent
            _curMousePos = touch_mgr.get_cursor_pos()
            if node.IsVisible() and node.IsPointIn(_curMousePos):
                return callback(node, scrollValue)

    mouseListener = cc.EventListenerMouse.create()

    def event_cb(event):
        if func_onMouseWheel(event.getScrollY() + event.getScrollX()):
            event.stopPropagation()

    mouseListener.setOnMouseScrollCallback(event_cb)
    cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(mouseListener, node.get())
    return mouseListener


def RemoveMouseWheelEvent(listener):
    cc.Director.getInstance().getEventDispatcher().removeEventListener(listener)


def AddScrollviewWheelEvent(scrollview, bHorz=False, callback=None):
    from common.utils.cocos_utils import ccp

    def cb(sv, scrollValue):
        if callback:
            callback(scrollValue)
        else:
            offset = scrollview.GetContentOffset()
            distance = scrollValue * 1.5
            if bHorz:
                scrollview.SetContentOffsetInDuration(ccp(offset.x + distance, offset.y), 0.03, True, True, over_edge=True)
            else:
                scrollview.SetContentOffsetInDuration(ccp(offset.x, offset.y - distance), 0.03, True, True, over_edge=True)
        return True

    return AddMouseWheelEvent(scrollview, cb)