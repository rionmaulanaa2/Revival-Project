# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/GuideHighLight.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const

class GuideHighLight(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/i_lobby_guide'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = ui_const.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'panel.nd_intercept_1.OnClick': 'on_cancel_close',
       'panel.nd_intercept_2.OnClick': 'on_cancel_close',
       'panel.nd_intercept_3.OnClick': 'on_cancel_close',
       'panel.nd_intercept_4.OnClick': 'on_cancel_close',
       'panel.nd_close.OnClick': 'on_confirm_close'
       }

    def on_init_panel(self, *args):
        self.panel.PlayAnimation('new_guide')
        self._cancel_callback = None
        self._confirm_callback = None
        return

    def on_finalize_panel(self):
        self._cancel_callback = None
        self._confirm_callback = None
        return

    def set_tips_text(self, text_id, text_anchor):
        for nd in (self.panel.img_line_left_top, self.panel.img_line_left_bottom):
            nd.setVisible(False)

        nd = self.panel.img_line_left_top
        if text_anchor == 'lb':
            nd = self.panel.img_line_left_bottom
        if nd:
            nd.setVisible(True)
            nd.lab_tips.SetString(text_id)

    def attach_to_node(self, node, text_id, text_anchor='lt', w_scale=1.0, h_scale=1.0):
        anchor = node.getAnchorPoint()
        pos = node.getParent().convertToWorldSpace(node.getPosition())
        pos = self.panel.convertToNodeSpace(pos)
        w, h = node.GetContentSize()
        x = pos.x - w * (anchor.x - 0.5)
        y = pos.y - h * (anchor.y - 0.5)
        self.set_position(x, y, w * w_scale, h * h_scale)
        self.set_tips_text(text_id, text_anchor)

    def set_position(self, x, y, width, height):
        self.panel.nd_guide.SetPosition(x, y)
        self.panel.nd_guide.SetContentSize(width, height)
        self.panel.nd_guide.ResizeAndPosition(False)
        self.panel.nd_bg.setScaleX(width / 20.0)
        self.panel.nd_bg.setScaleY(height / 10.0)
        self.panel.nd_bg.SetPosition(x, y)
        self.panel.nd_intercept_1.SetPosition(x, y + height / 2.0)
        self.panel.nd_intercept_2.SetPosition(x, y - height / 2.0)
        self.panel.nd_intercept_3.SetPosition(x + width / 2.0, y)
        self.panel.nd_intercept_4.SetPosition(x - width / 2.0, y)

    def set_confirm_callback(self, func, *args):
        self._confirm_callback = (
         func, args)

    def on_confirm_close(self, *_):
        if self._confirm_callback:
            func, args = self._confirm_callback
            func(*args)
        self.close()

    def set_cancel_callback(self, func, *args):
        self._cancel_callback = (
         func, args)

    def on_cancel_close(self, *_):
        if self._cancel_callback:
            func, args = self._cancel_callback
            func(*args)
        self.close()