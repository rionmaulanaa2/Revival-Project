# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/PanelRTCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase

class PanelRTCreator(ShareTemplateBase):
    KIND = 'COMMON_SHARE'

    def create(self, parent=None, tmpl=None):
        self.tmpl = tmpl
        super(PanelRTCreator, self).create(parent, tmpl)

    def get_render_texture_size_scale(self):
        size = self.panel.getContentSize()
        scale = 1.0
        if size.width <= 1 or size.height <= 1:
            return ((100, 100), 1.0)
        ratio = size.height / float(size.width)
        max_width = 1334
        max_height = 1000
        if size.width * scale > max_width:
            return ((max_width, int(max_width * ratio)), float(max_width) / size.width)
        if size.height * scale > max_height:
            return ((int(max_height / ratio), max_height), float(max_height) / size.height)
        return (
         (
          size.width * scale, size.height * scale), scale)

    def save_rt_to_file(self, save_path, cb_func):
        from logic.gutils.share_utils import ShareHelper
        sh = ShareHelper()
        rt = self.get_render_texture()
        global_data.game_mgr.delay_exec(0.003, lambda : sh._save_rt_to_file(rt, save_path, cb_func, is_rgba=True))