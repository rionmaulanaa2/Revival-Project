# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/draw_utils.py
from __future__ import absolute_import
from six.moves import range
from common.utils.cocos_utils import ccp, CCRectZero, CCRect
from common.uisys.uielment.CCScale9Sprite import CCScale9Sprite
import cc

class Scale9Line(object):

    def __init__(self, parent_nd, line_width=4):
        self.line_width = line_width
        self.parent_nd = parent_nd
        self.child_list = []
        self._free_nd = []
        self.is_drawed = False
        self._pos_list = None
        return

    def set_brush(self, pic_path='gui/ui_res_2/battle/map/plane_line.png', capInsets=CCRectZero):
        self._pic_path = pic_path
        self._capinset = capInsets

    def get_line_segment(self):
        if len(self._free_nd) > 0:
            return self._free_nd.pop()
        nd = CCScale9Sprite.Create('', self._pic_path, self._capinset)
        self.parent_nd.AddChild('', nd, Z=0)
        nd.setAnchorPoint(cc.Vec2(0, 0.5))
        self.child_list.append(nd)
        return nd

    def release_cur_line(self, is_destroy=False):
        for nd in self.child_list:
            nd.Destroy()

        self.child_list = []

    def draw_line_data(self, pos_list):
        self._pos_list = pos_list
        if len(self._pos_list) <= 1:
            return
        self._real_draw()

    def _real_draw(self):
        if not self._pos_list:
            return
        if self.is_drawed:
            self.release_cur_line()
        self.is_drawed = True
        for i in range(0, len(self._pos_list) - 1):
            nd_seg = self.get_line_segment()
            pos = self._pos_list[i]
            next_pos = self._pos_list[i + 1]
            vec_pos = cc.Vec2(pos[0], pos[1])
            next_vec_pos = cc.Vec2(next_pos[0], next_pos[1])
            nd_seg.setPosition(cc.Vec2(pos[0], pos[1]))
            next_vec_pos.subtract(vec_pos)
            nd_seg.SetContentSize(next_vec_pos.length(), self.line_width)
            cur_angle = next_vec_pos.getAngle() * 180 / 3.1415
            nd_seg.setRotation(-1 * cur_angle)

    def destroy(self):
        self.parent_nd = None
        self.release_cur_line(is_destroy=True)
        self.child_list = []
        self.release_free_nd()
        return

    def release_free_nd(self):
        for nd in self._free_nd:
            nd.Destroy()

        self._free_nd = []