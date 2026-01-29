# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapImgWidget.py
from __future__ import absolute_import
from logic.comsys.map.map_widget import MapScaleInterface
import cc

class MapImgWidget(MapScaleInterface.MapScaleInterface):

    def __init__(self, panel, map_nd, res_img_list, scale_list, img_scale_list, img_rect=None, cut_edge_list=None):
        super(MapImgWidget, self).__init__(map_nd, panel)
        self.res_img_list = res_img_list
        self.scale_list = scale_list
        self.scale_level = len(scale_list)
        self.img_scale_list = img_scale_list
        self.cut_edge_list = cut_edge_list
        self.build_in_scale = None
        self.res_img_rect = img_rect
        self._last_idx = None
        self.init_widget()
        return

    def init_widget(self):
        self.parent_nd.map_img.setVisible(True)
        self.parent_nd.map_img_2.setVisible(False)
        if self.res_img_rect:
            center_pos_u, center_pos_v, pixel_width, pixel_height = self.res_img_rect
            width, height = self.parent_nd.GetContentSize()
            self.parent_nd.map_img.SetPosition(width * center_pos_u, height * center_pos_v)
            self.parent_nd.map_img_2.SetPosition(width * center_pos_u, height * center_pos_v)
            self.map_content_size = (pixel_width, pixel_height)
        else:
            self.map_content_size = self.parent_nd.GetContentSize()
            if self.cut_edge_list:
                edges = self.cut_edge_list
                offset = (-(edges[0] - edges[1]) / 2.0, -(edges[2] - edges[3]) / 2.0)
                pos_ls = ('50%%%d' % offset[0], '50%%%d' % offset[1])
                self.parent_nd.map_img.SetPosition(*pos_ls)
                self.parent_nd.map_img_2.SetPosition(*pos_ls)
                width_cut = edges[0] + edges[1]
                height_cut = edges[2] + edges[3]
                width_scale = self.map_content_size[0] / (self.map_content_size[0] - width_cut)
                height_scale = self.map_content_size[1] / (self.map_content_size[1] - height_cut)
                self.build_in_scale = [width_scale, height_scale]
            else:
                self.parent_nd.map_img.SetPosition('50%', '50%')
                self.parent_nd.map_img_2.SetPosition('50%', '50%')
        self.set_img_res(0)

    def set_img_res(self, img_idx):
        if self.map_panel:
            global_data.emgr.on_map_res_detail_changed_event.emit(self.map_panel.__class__.__name__, img_idx)
        if img_idx == self._last_idx:
            return
        else:
            map_img = self.parent_nd.map_img
            map_img2 = self.parent_nd.map_img_2
            map_img.SetDisplayFrameByPath(None, self.res_img_list[img_idx], lambda _map_img=map_img, _map_img2=map_img2, _img_idx=img_idx: self._on_set_img_res(_map_img, _map_img2, _img_idx))
            return

    def _on_set_img_res(self, map_img, map_img2, img_idx):
        if not (self.parent_nd and self.parent_nd.isValid()):
            return
        else:
            sz_scale = self.map_content_size[0] / map_img.GetContentSize()[0] * self.img_scale_list[0]
            if not self.build_in_scale:
                map_img.setScale(sz_scale)
            else:
                map_img.setScaleX(sz_scale * self.build_in_scale[0])
                map_img.setScaleY(sz_scale * self.build_in_scale[1])
            if self._last_idx and self._last_idx != img_idx:
                map_img.setOpacity(0)
                map_img2.setOpacity(255)
                self.parent_nd.StopAnimation('change')
                map_img2.setVisible(True)
                map_img2.SetDisplayFrameByPath(None, self.res_img_list[self._last_idx])
                _scale = self.parent_nd.GetContentSize()[0] / map_img2.GetContentSize()[0] * self.img_scale_list[1]
                if not self.build_in_scale:
                    map_img2.setScale(_scale)
                else:
                    map_img2.setScaleX(_scale * self.build_in_scale[0])
                    map_img2.setScaleY(_scale * self.build_in_scale[1])
                map_img2.setVisible(True)
                self.parent_nd.PlayAnimation('change')
            self._last_idx = img_idx
            return

    def on_map_scale(self, map_scale):
        img_idx = 0
        while img_idx < self.scale_level and self.scale_list[img_idx] < map_scale:
            img_idx += 1

        self.set_img_res(img_idx)

    def destroy(self):
        super(MapImgWidget, self).destroy()