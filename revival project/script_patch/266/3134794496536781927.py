# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/CommonShareCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper

class CommonShareCreator(ShareTemplateBase):
    KIND = 'COMMON_SHARE'

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None):
        super(CommonShareCreator, self).create(parent, tmpl)

    def set_img_bg(self, img_path):
        if self.base_node and self.base_node.img_bg:
            self.base_node.img_bg.SetDisplayFrameByPath('', img_path, force_sync=True)


class CommonPosterShareCreator(ShareTemplateBase):
    KIND = 'COMMON_POSTER_SHARE'

    def set_img_bg(self, img_path):
        if self.base_node and self.base_node.img_bg:
            self.base_node.img_bg.SetDisplayFrameByPath('', img_path, force_sync=True)

    def set_only_pic_content(self, vis):
        base_nd = self.base_node
        if base_nd and base_nd.img_logo:
            base_nd.img_logo.setVisible(vis)
        self.set_qr_code_vis(vis)
        self.set_head_nd_vis(vis)
        self.update_to_fit_bg_sprite()

    def update_to_fit_bg_sprite(self):
        sz = self.panel.img_bg.getContentSize()
        from common.utils.ui_utils import get_scale
        scale = get_scale('1w')
        self.panel.setScale(scale)
        self.panel.setContentSize(sz)
        self.panel.ChildResizeAndPosition()
        self.panel.img_bg.SetPosition('50%', '50%')
        self.panel.img_bg.setScale(1)

    def update_ui_bg_sprite(self):
        from logic.gutils.share_utils import get_share_size
        sz = get_share_size()
        from common.utils.ui_utils import get_scale
        scale = get_scale('1w')
        self.panel.setScale(scale)
        self.panel.setContentSize(global_data.ui_mgr.design_screen_size)
        self.panel.ChildResizeAndPosition()
        self.panel.img_bg.SetPosition('50%', '50%')
        bg_scale = global_data.ui_mgr.design_screen_size.width / self.panel.img_bg.getContentSize().width
        self.panel.img_bg.setScale(bg_scale)

    def get_ui_bg_sprite(self):
        if self.base_node and self.base_node.img_bg:
            return self.base_node.img_bg
        else:
            return None
            return None