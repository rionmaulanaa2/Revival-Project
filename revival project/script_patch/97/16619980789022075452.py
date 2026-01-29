# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/NodeDragHelper.py
from __future__ import absolute_import
import six_ex
from common.utils.cocos_utils import ccp
import cc

class NodeDragHelper(object):

    def __init__(self):
        self._double_touch_prev_len = 0.0
        self._nd_touch_IDs = []
        self._nd_touch_poses = {}
        self._sfd = None
        self._dfd = None
        return

    def set_single_finger_drag(self, cb):
        self._sfd = cb

    def set_double_finger_drag(self, cb):
        self._dfd = cb

    def on_begin(self, touch):
        if len(self._nd_touch_IDs) >= 2:
            return False
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._nd_touch_IDs:
            self._nd_touch_poses[tid] = touch_wpos
            self._nd_touch_IDs.append(tid)
        if len(self._nd_touch_IDs) >= 2:
            pts = six_ex.values(self._nd_touch_poses)
            from common.utils.cocos_utils import ccp
            self._double_touch_prev_len = ccp(pts[0].x - pts[1].x, pts[0].y - pts[1].y).getLength()
        return True

    def on_drag(self, touch):
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._nd_touch_IDs:
            return
        if len(self._nd_touch_IDs) == 1:
            cc_raw_delta = touch.getDelta()
            if callable(self._sfd):
                self._sfd(cc_raw_delta)
        elif len(self._nd_touch_IDs) >= 2:
            self._nd_touch_poses[tid] = touch_wpos
            pts = six_ex.values(self._nd_touch_poses)
            vec = cc.Vec2(pts[0])
            vec.subtract(pts[1])
            cur_dist = vec.getLength()
            delta = cur_dist - self._double_touch_prev_len
            self._double_touch_prev_len = cur_dist
            cc_raw_delta = delta
            if callable(self._dfd):
                self._dfd(cc_raw_delta)

    def on_end(self, touch):
        tid = touch.getId()
        if tid in self._nd_touch_IDs:
            self._nd_touch_IDs.remove(tid)
            del self._nd_touch_poses[tid]