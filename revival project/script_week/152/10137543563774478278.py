# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/ItemsBookItemLstWidget.py
from __future__ import absolute_import
from logic.gutils import items_book_utils

class ItemsBookItemLstWidget(object):

    def __init__(self, parent):
        self.parent = parent
        self.panel = parent.panel
        self.cur_page_node_name = None
        self.interaction_state = None
        self._cache_temp_path_list = []
        self.init_parameters()
        self.init_event()
        return

    def init_goods_for_tab(self):
        pass

    def init_event(self):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.on_player_item_update,
           'refresh_item_red_point': self.on_player_item_update,
           'on_change_interaction_data': self.on_change_interaction_data,
           'del_item_red_point': self.on_red_point_update,
           'del_item_red_point_list': self.on_red_point_list_update
           }
        emgr.bind_events(econf)

    def check_page_widget_valid(self, func_name):
        return self._cur_view_page_widget and self._cur_view_page_widget.panel and self._cur_view_page_widget.panel.isVisible() and hasattr(self._cur_view_page_widget, func_name)

    def on_red_point_update(self, item_no):
        if self.check_page_widget_valid('on_red_point_update'):
            self._cur_view_page_widget.on_red_point_update(item_no)

    def on_red_point_list_update(self, item_no_list):
        if self.check_page_widget_valid('on_red_point_update'):
            for item_no in item_no_list:
                self._cur_view_page_widget.on_red_point_update(item_no)

    def on_player_item_update(self):
        if self.check_page_widget_valid('refresh_widget'):
            self._cur_view_page_widget.refresh_widget()

    def on_change_interaction_data(self, role_id):
        if self.check_page_widget_valid('on_change_interaction_data'):
            self._cur_view_page_widget.on_change_interaction_data(role_id)

    def init_data(self):
        pass

    def add_clear_templates(self, _cache_temp_path):
        if _cache_temp_path not in self._cache_temp_path_list:
            self._cache_temp_path_list.append(_cache_temp_path)

    def destroy(self):
        self._cur_view_page_widget and self._cur_view_page_widget.destroy()
        self._cur_view_page_widget = None
        if self._cache_temp_path_list:

            def clear_template(_cache_temp_path_list):
                if not global_data.ui_mgr.get_ui('ItemsBookMainUI'):
                    if global_data.item_cache_without_check:
                        for _cache_temp_path in _cache_temp_path_list:
                            global_data.item_cache_without_check.clear_cache_by_json(_cache_temp_path, None)

                return

            global_data.game_mgr.next_exec(clear_template, list(self._cache_temp_path_list))
            self._cache_temp_path_list = []
        return

    def init_parameters(self):
        self._cur_page_index = None
        self._cur_view_page_widget = None
        return

    def get_cur_page_index(self):
        return self._cur_page_index

    def reset_items_list(self):
        self.refresh_items_list(self._cur_page_index)

    def init_items_list(self, page_index):
        self.refresh_items_list(page_index)

    def refresh_items_list(self, page_index):
        if page_index is None:
            return
        else:
            node_name, template_name, cls = items_book_utils.get_items_book_list_widget_info(page_index)
            dlg = getattr(self.panel.temp_content, node_name)
            if not dlg:
                dlg = global_data.uisystem.load_template_create(template_name, parent=self.panel.temp_content, name=node_name)
            if self._cur_page_index != page_index:
                if self._cur_view_page_widget:
                    self._cur_view_page_widget.panel.setVisible(False)
                    self._cur_view_page_widget.destroy()
                    self._cur_view_page_widget = None
                self._cur_view_page_widget = cls(self, dlg)
                self._cur_view_page_widget.panel.setVisible(True)
                self.cur_page_node_name = node_name
                self._cur_page_index = page_index

                def play_anim():
                    if dlg and dlg.isValid() and dlg.HasAnimation('in'):
                        dlg.PlayAnimation('in')

                import game3d
                game3d.delay_exec(1, play_anim)
            return

    def jump_to_item_no(self, item_no):
        if self.check_page_widget_valid('jump_to_item_no'):
            self._cur_view_page_widget.jump_to_item_no(item_no)

    def do_show_panel(self):
        if self._cur_view_page_widget:
            if self._cur_view_page_widget.panel:
                self._cur_view_page_widget.panel.setVisible(True)
        if self.check_page_widget_valid('refresh_widget'):
            self._cur_view_page_widget.refresh_widget()

    def do_hide_panel(self):
        if self._cur_view_page_widget:
            if self._cur_view_page_widget.panel:
                self._cur_view_page_widget.panel.setVisible(False)
            if hasattr(self._cur_view_page_widget, 'do_hide_panel'):
                self._cur_view_page_widget.do_hide_panel()

    def check_can_mouse_scroll(self, *args, **kw):
        if not self._cur_view_page_widget:
            return False
        else:
            func = getattr(self._cur_view_page_widget, 'check_can_mouse_scroll', None)
            if not callable(func):
                return False
            return func(*args, **kw)

    def on_hot_key_mouse_scroll(self, *args, **kw):
        if not self._cur_view_page_widget:
            return
        else:
            func = getattr(self._cur_view_page_widget, 'on_hot_key_mouse_scroll', None)
            if not callable(func):
                return
            func(*args, **kw)
            return