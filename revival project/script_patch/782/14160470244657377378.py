# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/BigMapTouchLayerWidget.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import cc
from common.utils.ui_utils import get_scale
from logic.gcommon.common_const.battle_const import MARK_NORMAL, MAP_POS_NO_Y
from common.utils.cocos_utils import ccp

class BigMapTouchLayerWidget(object):

    def __init__(self, panel):
        super(BigMapTouchLayerWidget, self).__init__()
        self.map_panel = panel
        self._cur_touch_IDs = []
        self.touch_poses = {}
        self._touch_center = None
        self._cur_multi_touch = False
        self._touch_start_dist = 0
        self._touch_start_scale = self.map_panel.max_map_scale
        self.init_scroll_touch_event()
        self.init_mouse_event()
        return

    def destroy(self):
        self.map_panel = None
        return

    def __getattr__(self, name):
        print('[warning]touch layer name', name, 'may be map_panel attribute')
        return self.map_panel.__getattr__(name)

    def on_layer_double_clicked(self, layer, touch_pt1, touch_pt2):
        if len(self._cur_touch_IDs) >= 1:
            return
        touch_pt1.subtract(touch_pt2)
        if touch_pt1.getLength() > get_scale('20w'):
            return
        if self.map_panel.min_map_scale + 0.1 > self.map_panel.cur_map_scale:
            wpos = touch_pt2
            lpos = self.map_panel.map_nd.convertToNodeSpace(wpos)
            sz = self.map_panel.map_nd.getContentSize()
            x_percent = lpos.x / sz.width
            y_percent = lpos.y / sz.height
            self.map_panel.set_map_scale_with_anchor(self.map_panel.max_map_scale, x_percent, y_percent)
        else:
            self.map_panel.set_map_scale(self.map_panel.min_map_scale)
            self.map_panel.sv_map.ResetContentOffset()

    def on_layer_single_clicked(self, layer, touch_wpos):
        from logic.gutils import map_utils
        if not map_utils.check_can_draw_mark_or_route():
            return
        map_pos = self.map_panel.map_nd.convertToNodeSpace(touch_wpos)
        if map_pos and global_data.player and global_data.player.logic:
            part_map = global_data.game_mgr.scene.get_com('PartMap')
            v3d_scn_pos = part_map.get_map_pos_in_world(map_pos)
            v3d_scn_pos.y = MAP_POS_NO_Y
            global_data.player.logic.send_event('E_TRY_DRAW_MAP_MARK', MARK_NORMAL, v3d_scn_pos)
            map_utils.send_mark_group_msg(MARK_NORMAL)
            global_data.sound_mgr.play_ui_sound('ui_confirm_location')

    def init_mouse_event(self):
        listener = cc.EventListenerMouse.create()
        listener.setOnMouseScrollCallback(self.on_mouse_scroll)
        cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(listener, self.map_panel.panel.touch_layer.get())

    def on_mouse_scroll(self, event):
        dist = event.getScrollY() + event.getScrollX()
        if dist >= 0:
            magn = dist / 240.0 + 1
        else:
            magn = min(-60.0 / dist, 1)
        new_scale = self.map_panel.calc_map_scale(magn)
        self.map_panel.cur_map_scale = new_scale
        wpos = event.getLocation()
        lpos = self.map_panel.map_nd.getParent().convertToNodeSpace(wpos)
        sz = self.map_panel.panel.sv_map.GetInnerContentSize()
        zoom_anchor_x = lpos.x / sz.width
        zoom_anchor_y = lpos.y / sz.height
        self.map_panel.set_map_scale_with_anchor(new_scale, zoom_anchor_x, zoom_anchor_y)

    def on_layer_touch_ended(self, layer, touch):
        tid = touch.getId()
        if tid in self._cur_touch_IDs:
            self._cur_touch_IDs.remove(tid)
            del self.touch_poses[tid]
        if len(self._cur_touch_IDs) <= 1:
            if not self.panel.sv_map.isTouchEnabled():
                if self.cur_map_draw_mode is None:
                    self.panel.sv_map.setTouchEnabled(True)
                    layer.setSwallowTouch(False)
            self._touch_start_dist = 0
            self._touch_center = None
        return

    def on_layer_touch_begin(self, layer, touch):
        if len(self._cur_touch_IDs) >= 2:
            self._cur_multi_touch = True
            return False
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._cur_touch_IDs:
            self.touch_poses[tid] = touch_wpos
            self._cur_touch_IDs.append(tid)
        if len(self._cur_touch_IDs) >= 2:
            self.map_panel.panel.sv_map.setTouchEnabled(False)
            layer.SetSwallowTouch(True)
            pts = six_ex.values(self.touch_poses)
            self._touch_center = ccp((pts[0].x + pts[1].x) / 2.0, (pts[0].y + pts[1].y) / 2.0)
            self._touch_start_dist = ccp(pts[0].x - pts[1].x, pts[0].y - pts[1].y).getLength()
            self._touch_start_scale = self.map_panel.cur_map_scale
        else:
            layer.SetSwallowTouch(False)
        return True

    def on_layer_touch_drag(self, layer, touch):
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._cur_touch_IDs:
            return
        if len(self._cur_touch_IDs) >= 2:
            self.touch_poses[tid] = touch_wpos
            pts = six_ex.values(self.touch_poses)
            tmp_vec = cc.Vec2(pts[0])
            tmp_vec.subtract(pts[1])
            cur_dist = tmp_vec.getLength()
            start_dist = max(self._touch_start_dist, 1.0)
            magn = cur_dist / start_dist
            new_scale = magn * self._touch_start_scale
            new_scale = max(min(new_scale, self.map_panel.max_map_scale), self.map_panel.min_map_scale)
            sz = self.map_panel.panel.sv_map.GetInnerContentSize()
            lpos = self.map_panel.map_nd.getParent().convertToNodeSpace(self._touch_center)
            zoom_anchor_x = lpos.x / sz.width
            zoom_anchor_y = lpos.y / sz.height
            self.map_panel.set_map_scale_with_anchor(new_scale, zoom_anchor_x, zoom_anchor_y)

    def on_layer_touch_end(self, layer, touch):
        tid = touch.getId()
        if tid in self._cur_touch_IDs:
            self._cur_touch_IDs.remove(tid)
            del self.touch_poses[tid]
        if len(self._cur_touch_IDs) <= 1:
            self.map_panel.panel.sv_map.setTouchEnabled(True)
            self._touch_start_dist = 0
            self._touch_center = None
        if len(self._cur_touch_IDs) == 0:
            if not self._cur_multi_touch:
                start_location = touch.getStartLocation()
                cnt_location = touch.getLocation()
                start_location.subtract(cnt_location)
                if start_location.getLength() < get_scale('20w'):
                    self.on_layer_single_clicked(layer, cnt_location)
            self._cur_multi_touch = False
        return

    def init_scroll_touch_event(self):
        touch_layer = self.map_panel.touch_layer
        touch_layer.EnableDoubleClick(False)
        touch_layer.set_sound_enable(False)
        touch_layer.BindMethod('OnSingleClick', self.on_layer_single_clicked)
        touch_layer.BindMethod('OnBegin', self.on_layer_touch_begin)
        touch_layer.BindMethod('OnDrag', self.on_layer_touch_drag)
        touch_layer.BindMethod('OnEnd', self.on_layer_touch_end)