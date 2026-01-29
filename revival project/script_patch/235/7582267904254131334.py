# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/career/CareerBadgeWallInfoUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils import career_utils

class BadgeWallBadgeData(object):

    def __init__(self, sub_branch, lv, max_cur_prog):
        self.sub_branch = sub_branch
        self.lv = lv
        self.max_cur_prog = max_cur_prog

    def __str__(self):
        return '<BadgeWallBadgeData: %s, lv: %s, max_cur_prog: %s>' % (self.sub_branch, self.lv, self.max_cur_prog)

    __repr__ = __str__


class CareerBadgeWallInfoUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'life/display_wall/display_wall_other'
    TEMPLATE_NODE_NAME = 'temp_bg'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    SLOT_CNT = 8
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        super(CareerBadgeWallInfoUI, self).on_init_panel()
        from logic.comsys.career.CareerBadgeTipsWidget import CareerBadgeTipsWidget
        self._badge_tips_wgt = CareerBadgeTipsWidget(self.panel.temp_medal_tips)
        self._badge_tips_wgt.on_init_panel()
        self._init_view()
        self.hide_main_ui()

    def on_finalize_panel(self):
        self.show_main_ui()
        self._badge_tips_wgt.on_finalize_panel()
        self._badge_tips_wgt = None
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)
        super(CareerBadgeWallInfoUI, self).on_finalize_panel()
        return

    def do_hide_panel(self):
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)
        super(CareerBadgeWallInfoUI, self).do_hide_panel()

    def do_show_panel(self):
        super(CareerBadgeWallInfoUI, self).do_show_panel()
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)

    def _init_view(self):
        self.panel.list_medal.SetInitCount(self.SLOT_CNT)
        self.panel.temp_medal_tips.setVisible(False)

    def refresh(self, badge_data_dict):
        is_empty = not bool(badge_data_dict)
        if is_empty:
            self.panel.lab_empty.setVisible(True)
        else:
            self.panel.lab_empty.setVisible(False)
        cnt = self.panel.list_medal.GetItemCount()
        for i in range(cnt):
            item = self.panel.list_medal.GetItem(i)
            empty = i not in badge_data_dict
            if empty:
                item.setVisible(False)
            else:
                data = badge_data_dict[i]
                sub_branch = data.sub_branch
                lv = data.lv
                max_cur_prog = data.max_cur_prog
                item.setVisible(True)
                badge_item = item.temp_icon
                career_utils.refresh_badge_item(badge_item, sub_branch, lv, check_got=False)
                item.lab_name.SetString(career_utils.get_badge_name_text(sub_branch))
                item.lab_times.SetString(career_utils.get_badge_b_max_cur_prog_desc_text(sub_branch, max_cur_prog))

                @item.callback()
                def OnClick(btn, touch, data=data):
                    wpos = touch.getLocation()
                    self._badge_tips_wgt.show_badge_tips(wpos, data)