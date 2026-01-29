# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/career/CareerBadgeTipsWidget.py
from __future__ import absolute_import
from logic.gutils import career_utils

class CareerBadgeTipsWidget(object):

    def __init__(self, root_node):
        self.panel = root_node

    def on_init_panel(self):
        self.panel.setVisible(False)

        @self.panel.nd_medal_tips_close.callback()
        def OnClick(btn, touch):
            self.panel.setVisible(False)

    def on_finalize_panel(self):
        self.panel.setVisible(False)
        self.panel = None
        return

    def setVisible(self, vis):
        self.panel.setVisible(vis)

    def isVisible(self):
        return self.panel.isVisible()

    def show_badge_tips(self, wpos, badge_data):
        tips_node = self.panel
        tips_node.setVisible(True)
        tips_node.lab_name.SetString(career_utils.get_badge_name_text(badge_data.sub_branch))
        tips_node.lab_text.SetString(career_utils.get_badge_b_desc_txt(badge_data.sub_branch, badge_data.max_cur_prog))
        tips_node.img_medal.SetDisplayFrameByPath('', career_utils.get_badge_ribbon_icon_path(badge_data.sub_branch, badge_data.lv))
        tips_frame_node = tips_node.nd_medal_tips
        pos = tips_frame_node.GetParent().convertToNodeSpace(wpos)
        cur_screen_size = global_data.ui_mgr.design_screen_size
        center_x, center_y = cur_screen_size.width / 2, cur_screen_size.height / 2
        if wpos.x < center_x:
            anchor_x = 0.0
        else:
            anchor_x = 1.0
        if wpos.y < center_y:
            anchor_y = 0.0
        else:
            anchor_y = 1.0
        import cc
        tips_frame_node.setAnchorPoint(cc.Vec2(anchor_x, anchor_y))
        tips_frame_node.setPosition(pos.x, pos.y)