# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/JudgeOptionUINewWidget.py
from __future__ import absolute_import
from logic.gutils import judge_utils
from logic.client.const.game_mode_const import GAME_MODE_SURVIVALS

class JudgeOptionUINewWidget(object):

    def on_init_panel(self, parent_panel):
        self.panel = parent_panel
        self._init_view()
        self._init_ui_events()
        self.process_event(True)

    def _init_view(self):
        self.panel.nd_select.setVisible(False)
        self._refresh_view()

    def on_finalize_panel(self):
        self.process_event(False)
        self.panel = None
        return

    def _init_ui_events(self):

        @self.panel.btn_setting.unique_callback()
        def OnClick(btn, touch):
            self._on_click_setting_btn()

        @self.panel.btn_tick_1.unique_callback()
        def OnClick(btn, touch):
            self._on_click_model_show()

        @self.panel.btn_tick_2.unique_callback()
        def OnClick(btn, touch):
            self._on_click_scope_show()

        @self.panel.btn_tick_3.unique_callback()
        def OnClick(btn, touch):
            self._on_click_show_other_locate()

        if global_data.game_mode.get_mode_type() in GAME_MODE_SURVIVALS:
            self.panel.btn_tick_3.SetSelect(True)
        else:
            self.panel.btn_tick_3.SetEnable(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'net_reconnect_event': self._on_net_reconnect,
           'switch_judge_scope_show_event': self._on_switch_scope_show
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _refresh_view(self):
        self.panel.btn_tick_1.SetSelect(judge_utils.is_perspective_enabled())
        ui_inst = global_data.ui_mgr.get_ui('ScopePlayerUI')
        if ui_inst and ui_inst.isPanelVisible():
            show_opponent_hud = True
        else:
            show_opponent_hud = False
        self.panel.btn_tick_2.SetSelect(show_opponent_hud)

    def _on_click_setting_btn(self, *args):
        self.panel.nd_select.setVisible(not self.panel.nd_select.isVisible())

    def _on_click_model_show(self, *args):
        dst_select = not self.panel.btn_tick_1.GetSelect()
        if judge_utils.set_perspective_enabled(dst_select):
            self.panel.btn_tick_1.SetSelect(dst_select)

    def _on_click_scope_show(self, *args):
        self.panel.btn_tick_2.SetSelect(not self.panel.btn_tick_2.GetSelect())
        ui_inst = global_data.ui_mgr.get_ui('ScopePlayerUI')
        if not ui_inst:
            ui_inst = global_data.ui_mgr.show_ui('ScopePlayerUI', 'logic.comsys.observe_ui')
        if self.panel.btn_tick_2.GetSelect():
            ui_inst.show()
        else:
            ui_inst.hide()

    def _on_click_show_other_locate(self, *args):
        self.panel.btn_tick_3.SetSelect(not self.panel.btn_tick_3.GetSelect())
        if global_data.game_mode.get_mode_type() not in GAME_MODE_SURVIVALS:
            return
        small_map_ui = global_data.ui_mgr.get_ui('SmallMapUI')
        big_map_ui = global_data.ui_mgr.get_ui('BigMapUI')
        show_others = self.panel.btn_tick_3.GetSelect()
        if small_map_ui:
            player_info_widget = small_map_ui.get_player_info_widget()
            player_info_widget and player_info_widget.set_locate_widgets_visible_for_judge(show_others)
        if big_map_ui:
            player_info_widget = big_map_ui.get_player_info_widget()
            player_info_widget and player_info_widget.set_locate_widgets_visible_for_judge(show_others)

    def _on_switch_scope_show(self, is_show):
        cur_value = self.panel.btn_tick_2.GetSelect()
        if cur_value == is_show:
            return cur_value
        else:
            self._on_click_scope_show()
            return cur_value

    def _on_net_reconnect(self):
        ui_inst = global_data.ui_mgr.get_ui('ScopePlayerUI')
        show_before = ui_inst and ui_inst.isPanelVisible()
        global_data.ui_mgr.close_ui('ScopePlayerUI')
        if show_before:
            ui_inst = global_data.ui_mgr.show_ui('ScopePlayerUI', 'logic.comsys.observe_ui')
            ui_inst.show()
        self._refresh_view()

    def get_hide_other_locate_widget(self):
        return not self.panel.btn_tick_3.GetSelect()