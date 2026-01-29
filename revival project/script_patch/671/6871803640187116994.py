# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Rank/RankListUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from logic.comsys.battle.Rank.GroupsRankWidget import GroupsRankWidget
from logic.comsys.battle.Rank.TeammatesRankWidget import TeammatesRankWidget
from common.const import uiconst

class RankListUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_point/fight_point_mode_continue'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_details.OnClick': 'on_show_lstview',
       'temp_panel_point.temp_panel.btn_close.OnClick': 'on_hide_lstview'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.hide_main_ui()
        self.init_rank_bar()

    def on_finalize_panel(self):
        self.panel.nd_continue.StopTimerAction()
        self.show_main_ui()
        ui_obj = global_data.ui_mgr.get_ui('BriefRankUI')
        if ui_obj:
            ui_obj.show()

    def init_parameters(self):
        self.tab_widgets = {}
        self.cur_index = 0
        self.tab_list = [
         {'index': 0,'text': 19407,'widget_func': self.init_groups_template,'widget': 'battle_point/i_panel_details_all'
            },
         {'index': 1,'text': 19408,'widget_func': self.init_teammates_template,'widget': 'battle_point/i_panel_details_team'
            }]

    def init_event(self):
        pass

    def init_rank_bar(self):

        def init_rank_btn(node, data):
            node.btn_tab.SetText(get_text_by_id(data.get('text', '')))

        def rank_btn_click_cb(ui_item, data):
            index = data.get('index', 0)
            self.cur_index = index
            if index in self.tab_widgets:
                for ind in self.tab_widgets:
                    widget = self.tab_widgets[ind]
                    if index == ind:
                        widget.show()
                    else:
                        widget.hide()

            else:
                widget = data.get('widget')
                widget_func = data.get('widget_func')
                if widget and widget_func:
                    _nd = global_data.uisystem.load_template_create(widget, self.panel.temp_panel_point.template_list)
                    _nd.SetPosition('50%', '50%')
                    widget_wrapper = widget_func(_nd)
                    self.tab_widgets[index] = widget_wrapper
                    for ind in self.tab_widgets:
                        cur_widget = self.tab_widgets[ind]
                        if index != ind:
                            cur_widget.hide()

            self.request_data()

        self._rank_bar_wrapper = WindowTopSingleSelectListHelper()
        self._rank_bar_wrapper.set_up_list(self.panel.temp_panel_point.title.list_tab, self.tab_list, init_rank_btn, rank_btn_click_cb)
        self._rank_bar_wrapper.set_node_click(self.panel.temp_panel_point.title.list_tab.GetItem(0))

    def init_groups_template(self, nd):
        return GroupsRankWidget(nd, self.panel)

    def init_teammates_template(self, nd):
        return TeammatesRankWidget(nd, self.panel)

    def on_show_lstview(self, *args, **kargs):
        self.panel.PlayAnimation('show')
        widget = self.tab_widgets.get(self.cur_index)
        widget and widget.refresh_listview()

    def on_hide_lstview(self, *args, **kargs):
        self.panel.PlayAnimation('disappear')

    def set_group_data(self, index, data):
        widget = self.tab_widgets.get(index)
        widget and widget.set_group_data(data)

    def request_data(self):
        widget = self.tab_widgets.get(self.cur_index)
        widget and widget.request_data()

    def on_delay_close(self, revive_time):
        self.pass_time = 0
        self.request_data()

        def refresh_time(pass_time):
            if int(pass_time) - self.pass_time >= 2:
                self.request_data()
                self.pass_time = int(pass_time)
            self.panel.lab_time.SetString(str(int(revive_time - pass_time)))

        def refresh_time_finsh():
            self.panel.lab_time.SetString(str(0))
            self.close()

        self.panel.nd_continue.StopTimerAction()
        self.panel.nd_continue.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh)