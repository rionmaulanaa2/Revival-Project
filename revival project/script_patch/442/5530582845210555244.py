# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/SpringBenefitsShareCreator.py
from __future__ import absolute_import
from logic.gutils.end_statics_utils import init_end_person_statistics, init_end_teammate_statics
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper

class SpringBenefitsShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_SPRING_TEN_BENEFITS'

    def get_ui_bg_sprite(self):
        return self.panel.pnl_bg.img_bg

    def update_ui_bg_sprite(self):
        from logic.gutils.share_utils import get_share_size
        sz = get_share_size()
        from common.utils.ui_utils import get_scale
        scale = get_scale('1w')
        panel = self.panel.pnl_bg
        self.panel.setScale(scale)
        self.panel.setContentSize(global_data.ui_mgr.design_screen_size)
        self.panel.ChildResizeAndPosition()
        self.panel.pnl_bg.img_bg.SetPosition('50%', '50%')
        bg_scale = global_data.ui_mgr.design_screen_size.width / self.panel.pnl_bg.img_bg.getContentSize().width
        self.panel.pnl_bg.img_bg.setScale(bg_scale)