# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/live/LiveFloatingWidget.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from common.live.live_agent_mgr import LiveAgentMgr
from logic.gcommon.common_utils.local_text import get_text_by_id
import time
import game3d
import render
from cocosui import cc
from logic.gcommon.common_utils.text_utils import check_review_words
from common.uisys.BaseUIWidget import BaseUIWidget

class LiveFloatingWidget(BaseUIWidget):

    def __init__(self, panel_cls, ui_panel, *args, **kwargs):
        super(LiveFloatingWidget, self).__init__(panel_cls, ui_panel)
        self._move_start_pos = None
        self._start_pos = None
        self.on_init_panel()
        self.register_touch_move()
        return

    def on_init_panel(self, *args, **kwargs):
        self.panel.temp_close.btn_back.BindMethod('OnClick', self.on_click_close_btn)
        self.panel.btn_catalog.BindMethod('OnClick', self.on_click_btn_catalog)
        self.panel.btn_danmu.BindMethod('OnClick', self.on_click_danmu_btn)
        self.panel.btn_scale.BindMethod('OnClick', self.on_click_btn_scale)
        from logic.vscene.part_sys.live.LivePlatformManager import LivePlatformManager
        is_support_dammu = LivePlatformManager().get_cur_platform().is_support_dammu()
        self.panel.btn_danmu.setVisible(is_support_dammu)
        self.refresh_danmu_show()

    def destroy(self):
        super(LiveFloatingWidget, self).destroy()
        self.switch_danmu_to_float(False)

    def refresh_danmu_show(self):
        if self.parent.is_danmu_enable:
            self.panel.lab_danmu.SetString(15847)
        else:
            self.panel.lab_danmu.SetString(15848)

    def on_click_close_btn(self, btn, touch):
        ui = global_data.ui_mgr.get_ui('LiveMainUI')
        if ui and not ui.panel.isVisible():
            global_data.ui_mgr.close_ui('LiveMainUI')
        global_data.ui_mgr.close_ui('LiveTVUI')

    def setup_anchor_data(self, live_type, data):
        from logic.gutils.live_utils import format_one_line_text, format_view_person
        nickname = data.get('nickname', '')
        title = data.get('title', '') or ''
        hot_score = data.get('hot_score', 0)
        formated_title = format_one_line_text(self.panel.lab_title, title, self.panel.nd_title_max_length.getContentSize().width)
        self.panel.lab_title.SetString(formated_title)
        formated_name = format_one_line_text(self.panel.lab_name, nickname, self.panel.nd_max_name_length.getContentSize().width)
        self.panel.lab_name.SetString(formated_name)
        self.panel.lab_pop.SetString(format_view_person(hot_score))
        head_img = data.get('head')
        uid = data.get('uid')
        sp_head_name = '%s_%s_head' % (str(live_type), str(uid))
        if head_img:
            from logic.vscene.part_sys.live.LiveSpriteManager import LiveSpriteManager
            LiveSpriteManager().SetSpriteByLink(self.panel.img_head, head_img, sp_head_name)

    def on_click_btn_catalog(self, btn, touch):
        ui = global_data.ui_mgr.get_ui('LiveMainUI')
        if ui:
            ui.clear_show_count_dict()
        else:
            from logic.comsys.live.LiveMainUI import LiveMainUI
            LiveMainUI()

    def on_click_danmu_btn(self, btn, touch):
        self.parent.set_danmu_enable(not self.parent.is_danmu_enable)
        if self.parent.is_danmu_enable:
            self.panel.lab_danmu.SetString(15847)
        else:
            self.panel.lab_danmu.SetString(15848)

    def on_click_btn_scale(self, btn, touch):
        if self.parent:
            self.parent.scale_to_floating_windows(False)

    def register_touch_move(self):
        nd_drag = self.panel.touch_layer

        @nd_drag.unique_callback()
        def OnBegin(layer, touch):
            self._move_start_pos = touch.getLocation()
            self._start_pos = self.parent.panel.nd_move.getParent().convertToWorldSpace(self.parent.panel.nd_move.getPosition())

        @nd_drag.unique_callback()
        def OnDrag(layer, touch):
            w_pos = touch.getLocation()
            w_pos.subtract(self._move_start_pos)
            w_pos.add(self._start_pos)
            self.parent.panel.nd_move.setPosition(self._boundary_check(w_pos))
            ui = global_data.ui_mgr.get_ui('DanmuLinesUI')
            if ui:
                wpos = self.panel.nd_show.ConvertToWorldSpace(0, 0)
                ui.update_float_pos(wpos)

        @nd_drag.unique_callback()
        def OnEnd(layer, touch):
            pass

    def _boundary_check(self, w_pos):

        def PointCheck(p_node, pt, left_xb, right_xb, bottom_yb, up_yb):
            p = p_node.convertToNodeSpace(pt)
            c_size_node = p_node.getContentSize()
            l_pos_x = max(min(c_size_node.width - right_xb, p.x), left_xb)
            l_pos_y = max(min(c_size_node.height - up_yb, p.y), bottom_yb)
            return cc.Vec2(l_pos_x, l_pos_y)

        sz = self.panel.nd_show.getContentSize()
        anchor = cc.Vec2(0.5, 0.5)
        left_boundary = sz.width * anchor.x * 0.1
        right_boundary = sz.width * (1 - anchor.x) * 0.1
        bottom_boundary = sz.height * anchor.y * 0.1
        up_boundary = sz.height * (1 - anchor.y) * 0.1
        node = self.parent.panel.nd_move.getParent()
        return PointCheck(node, w_pos, left_boundary, right_boundary, bottom_boundary, up_boundary)

    def switch_danmu_to_float(self, is_float):
        ui = global_data.ui_mgr.get_ui('DanmuLinesUI')
        if not ui:
            return
        else:
            if not is_float:
                ui.switch_to_float(False, None, None)
            else:
                wpos = self.panel.nd_show.ConvertToWorldSpace(0, 0)
                sz = self.panel.nd_show.getContentSize()
                scale = self.panel.nd_show.GetNodeToWorldScale()
                ui.switch_to_float(True, wpos, cc.Size(sz.width * scale.x, sz.height * scale.y))
            return