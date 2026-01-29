# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyFlexibleWidgetList.py
from __future__ import absolute_import
import six_ex
from common.cfg import confmgr

class LobbyFlexibleWidgetList(object):

    def __init__(self, parent_ui, panel):
        super(LobbyFlexibleWidgetList, self).__init__()
        self.parent = parent_ui
        self._timer_dict = {}
        self._show_set = set()
        self.process_event(True)
        self.on_init_panel(panel)

    def on_init_panel(self, panel):
        self.panel = panel
        self.init_data()
        self.init_widget_list()

    def destroy(self):
        self._show_set = set()
        self.process_event(False)
        for widget in self.widget_list:
            widget.destroy()

        self.unregister_widget_showhide_timer()
        self.widget_list = []
        self.btn_list = None
        return

    def init_data(self):
        self.btn_list = self.panel.list_temp
        self.widget_list = []
        cfg = confmgr.get('activity_lobby_widget_config', default={})
        self.sorted_widget_ids = cfg.get('sorted_id', [])
        self.widget_cfgs = cfg.get('widget_cfgs', {})

    def init_widget_list(self):
        self.btn_list.DeleteAllSubItem()
        for widget_id in self.sorted_widget_ids:
            widget_cfg = self.widget_cfgs.get(str(widget_id), {})
            if not widget_cfg:
                log_error(widget_id, 'Widget Config not found')
                continue
            widget_temp = widget_cfg.get('cWidgetTemp')
            widget_name = widget_cfg.get('cWidgetClass', '')
            widget_type = widget_cfg.get('cWidgetType', '')
            widget_cls = self.get_entry_widget_class(widget_name)
            if widget_temp is None:
                log_error(widget_id, 'Widget Template Not Set!!!')
                continue
            if not widget_cls:
                log_error(widget_id, widget_name, 'not found')
                continue
            is_shown = widget_cls.check_shown(widget_type)
            if not is_shown:
                continue
            temp_conf = global_data.uisystem.load_template(widget_temp)
            item = self.btn_list.AddItem(temp_conf)
            widget = widget_cls(self, item, widget_id, widget_type)
            self.widget_list.append(widget)

        self.check_register_widget_show_hide_timer()
        return

    def get_entry_widget_class(self, widget_name):
        from logic.comsys.lobby import EntryWidget
        module = getattr(EntryWidget, widget_name, None)
        if not module:
            try:
                mod_path = EntryWidget.__name__ + '.' + widget_name
                module = __import__(mod_path, fromlist=[widget_name], level=0)
            except ImportError:
                return

        return getattr(module, widget_name, None)

    def refresh_widget_list(self):
        for widget in self.widget_list:
            widget.destroy()

        self.widget_list = []
        self.init_widget_list()

    def refresh_widgets_red_point(self):
        for widget in self.widget_list:
            widget.refresh_red_point()

    def get_showhide_dict(self):
        unshow_dict = {}
        show_dict = {}
        for widget_id in self.sorted_widget_ids:
            widget_cfg = self.widget_cfgs.get(str(widget_id), {})
            widget_name = widget_cfg.get('cWidgetClass', '')
            widget_type = widget_cfg.get('cWidgetType', '')
            widget_cls = self.get_entry_widget_class(widget_name)
            cBeginTime = widget_cfg.get('cBeginTime')
            cEndTime = widget_cfg.get('cEndTime')
            if cBeginTime or cEndTime:
                is_shown = widget_cls.check_shown(widget_type)
                from logic.gcommon import time_utility
                cur_time = time_utility.get_server_time()
                if not is_shown:
                    if cBeginTime:
                        time_gap = cBeginTime - cur_time
                        if time_gap > 0:
                            unshow_dict[widget_id] = time_gap
                elif cEndTime:
                    time_gap = cEndTime - cur_time
                    if time_gap > 0:
                        show_dict[widget_id] = time_gap

        return (
         unshow_dict, show_dict)

    def check_register_widget_show_hide_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_widget_showhide_timer()
        if not global_data.player:
            return
        unshow_dict, show_dict = self.get_showhide_dict()
        self._show_set = set(six_ex.keys(unshow_dict))
        if show_dict:
            min_key = min(show_dict, key=show_dict.get)
            widget_id = min_key
            timer_id = global_data.game_mgr.register_logic_timer(self.check_diff_showhide, interval=10, times=-1, mode=CLOCK)
            self._timer_dict[widget_id] = timer_id
        if unshow_dict:
            min_key = min(unshow_dict, key=unshow_dict.get)
            widget_id = min_key
            timer_id = global_data.game_mgr.register_logic_timer(self.check_diff_showhide, interval=10, times=-1, mode=CLOCK)
            self._timer_dict[widget_id] = timer_id

    def unregister_widget_showhide_timer(self):
        if self._timer_dict:
            for widget_id, timer_id in six_ex.items(self._timer_dict):
                global_data.game_mgr.unregister_logic_timer(timer_id)

            self._timer_dict = {}

    def check_diff_showhide(self):
        if not global_data.player:
            return
        new_unshow_dict, new_show_dict = self.get_showhide_dict()
        if set(six_ex.keys(new_unshow_dict)) != self._show_set:
            self.refresh_widget_list()
            self.parent.refresh_vertical_icon()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'net_login_reconnect_event': self.on_net_reconnect,
           'net_reconnect_event': self.on_net_reconnect
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_net_reconnect(self, *args):
        self.check_register_widget_show_hide_timer()