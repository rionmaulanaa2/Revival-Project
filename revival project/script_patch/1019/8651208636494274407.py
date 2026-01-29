# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/LobbyGuideManager.py
from __future__ import absolute_import
import six
import six_ex
from common.framework import Singleton
from logic.gutils import guide_utils

class LobbyGuideManager(Singleton):
    ALIAS_NAME = 'lobby_guide_mgr'

    def init(self):
        self._working_guide_list = []
        self._lobby_guide_conf = {}
        self._is_binded_event = False
        self._guide_ui_2_name_dict = {}
        self.activated_guide_dict = {}
        self.activating_guide_name_set = set()
        self._guide_key_dict = {}
        self.saved_guide_nd_dict = {}
        self._cur_priority = 0
        self._post_guide_timer_id = None
        self._delay_guide_timer_id_dict = {}
        return

    def on_finalize(self):
        self._working_guide_list = []
        self._lobby_guide_conf = {}
        self._guide_ui_2_name_dict = {}
        self.activated_guide_dict = {}
        self._guide_key_dict = {}
        if self._is_binded_event:
            self.process_ui_event(False)
            self._is_binded_event = False
        self.saved_guide_nd_dict = {}
        self._cur_priority = 0
        self.clear_post_guide_timer()
        for _, tid in six.iteritems(self._delay_guide_timer_id_dict):
            global_data.game_mgr.unregister_logic_timer(tid)

        self._delay_guide_timer_id_dict = {}

    def process_ui_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'ui_open_event': self.on_ui_open,
           'ui_close_event': self.on_ui_close,
           'ui_page_create_event': self.on_page_create,
           'ui_page_destroy_event': self.on_page_destroy,
           'ui_page_vis_event': self.on_page_vis,
           'resolution_changed_end': self.on_resolution_changed_end,
           'on_notify_guide_event': self.on_notify_check_guide_by_event,
           'on_notify_hide_guide_event': self.on_notify_hide_guide
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def start_show_guide(self):
        from data.c_guide_data import DataDict
        lobbyGuide = DataDict.get('LobbyGuide', {}).get('Content', {})
        self._lobby_guide_conf = lobbyGuide
        waiting_guide_list = []
        self.check_guide_priority()
        for guide_name, guide_conf in six.iteritems(lobbyGuide):
            guide_key = guide_conf.get('guide_key')
            is_guided = self.is_guide_key_guided(guide_key)
            if is_guided:
                continue
            self._guide_key_dict.setdefault(guide_key, [])
            self._guide_key_dict[guide_key].append(guide_name)
            guide_check_handler_name = guide_conf.get('guide_check_handler')
            if guide_check_handler_name:
                guide_check_handler = getattr(guide_utils, guide_check_handler_name)
                if callable(guide_check_handler):
                    if not guide_check_handler():
                        continue
                else:
                    log_error('Invalid lobby guide check handler', guide_check_handler_name)
            priority = guide_conf.get('priority', None)
            if priority:
                if not self.check_guide_can_show(priority):
                    continue
            waiting_guide_list.append(guide_name)

        self._working_guide_list = waiting_guide_list
        if not self._working_guide_list:
            self.finalize()
        else:
            self._guide_ui_2_name_dict = {}
            for guide_name in self._working_guide_list:
                guide_ui_dict = lobbyGuide.get(guide_name, {}).get('guide_handler_params', {}).get('ui_list')
                if guide_ui_dict:
                    if not self._is_binded_event:
                        self.process_ui_event(True)
                        self._is_binded_event = True
                    for ui_name in six_ex.keys(guide_ui_dict):
                        self._guide_ui_2_name_dict.setdefault(ui_name, [])
                        self._guide_ui_2_name_dict[ui_name].append(guide_name)

        return

    def check_guide_priority(self):
        for guide_name, guide_conf in six.iteritems(self._lobby_guide_conf):
            guide_key = guide_conf.get('guide_key')
            is_guided = self.is_guide_key_guided(guide_key)
            if is_guided:
                continue
            guide_check_handler_name = guide_conf.get('guide_check_handler')
            if guide_check_handler_name:
                guide_check_handler = getattr(guide_utils, guide_check_handler_name)
                if callable(guide_check_handler):
                    if not guide_check_handler():
                        continue
                else:
                    log_error('Invalid lobby guide check handler', guide_check_handler_name)
            priority = guide_conf.get('priority')
            if priority and priority > self._cur_priority:
                self._cur_priority = priority

    def check_guide_can_show(self, priority):
        return priority >= self._cur_priority

    def on_ui_open(self, ui_name):
        if ui_name in self._guide_ui_2_name_dict:
            for guide_name in self._guide_ui_2_name_dict[ui_name]:
                ui_dict = self._lobby_guide_conf.get(guide_name, {}).get('guide_handler_params', {}).get('ui_list', {}).get(ui_name)
                if 'on_close' not in ui_dict and 'page' not in ui_dict:
                    if self.check_can_activate_by_guide_name(guide_name):
                        delay_show = self.check_delay_with_show(guide_name)
                        if not delay_show:
                            self.activate_ui_guide(guide_name, ui_name, ui_dict)

    def on_ui_close(self, ui_name):
        if ui_name in self._guide_ui_2_name_dict:
            for guide_name in self._guide_ui_2_name_dict[ui_name]:
                ui_dict = self._lobby_guide_conf.get(guide_name, {}).get('guide_handler_params', {}).get('ui_list', {}).get(ui_name)
                if 'on_close' in ui_dict and 'page' not in ui_dict:
                    if self.check_can_activate_by_guide_name(guide_name):
                        self.activate_ui_guide(guide_name, ui_name, ui_dict)
                if guide_name in self.activating_guide_name_set:
                    self.hide_guide_by_name(guide_name)

    def check_delay_with_show(self, guide_name):
        from common.utils.timer import CLOCK
        ui_delay_show_t = self._lobby_guide_conf.get(guide_name, {}).get('ui_delay_show_t', None)
        if ui_delay_show_t:
            tid = self._delay_guide_timer_id_dict.get(guide_name)
            if tid:
                global_data.game_mgr.unregister_logic_timer(tid)
                self._delay_guide_timer_id_dict[guide_name] = None

            def cb():
                self._delay_guide_timer_id_dict[guide_name] = None
                self.on_notify_check_guide_with_check(guide_name)
                return

            new_tid = global_data.game_mgr.register_logic_timer(cb, interval=ui_delay_show_t, times=1, mode=CLOCK)
            self._delay_guide_timer_id_dict[guide_name] = new_tid
            return True
        else:
            return

    def on_page_create(self, page_name, ui_name):
        if ui_name in self._guide_ui_2_name_dict:
            for guide_name in self._guide_ui_2_name_dict[ui_name]:
                if guide_name in self.activating_guide_name_set:
                    continue
                ui_dict = self._lobby_guide_conf.get(guide_name, {}).get('guide_handler_params', {}).get('ui_list', {}).get(ui_name)
                if 'page' not in ui_dict:
                    continue
                if page_name == ui_dict['page']:
                    if 'on_close' not in ui_dict:
                        if self.check_can_activate_by_guide_name(guide_name):
                            delay_show = self.check_delay_with_show(guide_name)
                            if not delay_show:
                                self.activate_ui_guide(guide_name, ui_name, ui_dict)

    def on_page_destroy(self, page_name, ui_name):
        if ui_name in self._guide_ui_2_name_dict:
            for guide_name in self._guide_ui_2_name_dict[ui_name]:
                ui_dict = self._lobby_guide_conf.get(guide_name, {}).get('guide_handler_params', {}).get('ui_list', {}).get(ui_name)
                if 'page' not in ui_dict:
                    continue
                if page_name == ui_dict['page']:
                    if 'on_close' in ui_dict:
                        if self.check_can_activate_by_guide_name(guide_name):
                            self.activate_ui_guide(guide_name, ui_name, ui_dict)
                    if guide_name in self.activating_guide_name_set:
                        self.hide_guide_by_name(guide_name)

    def on_page_vis(self, vis, page_name, ui_name):
        if ui_name in self._guide_ui_2_name_dict:
            for guide_name in self._guide_ui_2_name_dict[ui_name]:
                ui_dict = self._lobby_guide_conf.get(guide_name, {}).get('guide_handler_params', {}).get('ui_list', {}).get(ui_name)
                if 'page' not in ui_dict:
                    continue
                if page_name == ui_dict['page']:
                    if not vis:
                        if guide_name in self.activating_guide_name_set:
                            self.hide_guide_by_name(guide_name)
                    else:
                        self.on_page_create(page_name, ui_name)

    def is_guide_key_guided(self, guide_key):
        return global_data.player and global_data.player.is_lobby_guide_read(guide_key)

    def check_has_guided(self, guide_name):
        guide_order = self._lobby_guide_conf.get(guide_name, {}).get('guide_order')
        guide_key = self._lobby_guide_conf.get(guide_name, {}).get('guide_key')
        is_guided = self.is_guide_key_guided(guide_key)
        if is_guided:
            return True
        if guide_name in self._working_guide_list:
            return False
        if self.activated_guide_dict.get(guide_key, 0) >= guide_order and guide_name not in self.activating_guide_name_set:
            return True
        return False

    def check_can_activate_by_guide_name(self, guide_name, is_by_event=False):
        if guide_name not in self._working_guide_list:
            return False
        guide_key = self._lobby_guide_conf.get(guide_name, {}).get('guide_key')
        is_guided = self.is_guide_key_guided(guide_key)
        if is_guided:
            return False
        pre_guide = self._lobby_guide_conf.get(guide_name, {}).get('pre_guide', '')
        if pre_guide and not self.check_has_guided(pre_guide):
            return False
        guide_order = self._lobby_guide_conf.get(guide_name, {}).get('guide_order')
        if guide_name in self.activating_guide_name_set:
            return False
        if self.activated_guide_dict.get(guide_key, 0) == guide_order:
            return False
        can_auto_show = not self._lobby_guide_conf.get(guide_name, {}).get('is_trigger_by_hand', False)
        if can_auto_show or is_by_event:
            for gn in self.activating_guide_name_set:
                if self._lobby_guide_conf.get(gn, {}).get('guide_key') == guide_key:
                    if self._lobby_guide_conf.get(gn, {}).get('guide_order') + 1 == guide_order:
                        return True

            if self.activated_guide_dict.get(guide_key, 0) == 0 and guide_order == 1:
                return True
            if self.activated_guide_dict.get(guide_key, 0) + 1 == guide_order:
                return True
        return False

    def deactivate_guide_name_by_key_and_order(self, guide_key, target_guide_order):
        guide_names = self._guide_key_dict.get(guide_key, [])
        for guide_name in guide_names:
            guide_order = self._lobby_guide_conf.get(guide_name, {}).get('guide_order')
            if guide_order < target_guide_order:
                self.deactivate_guide_by_name(guide_name)

    def activate_ui_guide(self, guide_name, ui_name, ui_guide_dict):
        temp_func_name = ui_guide_dict.get('temp_func')
        guide_key = self._lobby_guide_conf.get(guide_name, {}).get('guide_key')
        guide_order = self._lobby_guide_conf.get(guide_name, {}).get('guide_order')
        is_last_one = self._lobby_guide_conf.get(guide_name, {}).get('is_last_one')
        temp_func = getattr(guide_utils, temp_func_name)
        if callable(temp_func):
            temp_func(guide_name, guide_key, ui_name, ui_guide_dict)
        self.activating_guide_name_set.add(guide_name)
        self.deactivate_guide_name_by_key_and_order(guide_key, guide_order)
        if is_last_one:
            self.deactivate_guide_by_name(guide_name)

    def deactivate_guide_by_name(self, guide_name, need_remove=True):
        guide_ui_dict = self._lobby_guide_conf.get(guide_name, {}).get('guide_handler_params', {}).get('ui_list')
        guide_key = self._lobby_guide_conf.get(guide_name, {}).get('guide_key')
        guide_order = self._lobby_guide_conf.get(guide_name, {}).get('guide_order')
        if guide_ui_dict:
            for ui_name, ui_guide_dict in six.iteritems(guide_ui_dict):
                temp_func_name = ui_guide_dict.get('temp_func', '')
                temp_func = getattr(guide_utils, temp_func_name + '_finish')
                if callable(temp_func):
                    temp_func(guide_name, guide_key, ui_name, ui_guide_dict)

        if need_remove:
            if guide_order > self.activated_guide_dict.get(guide_key, -1):
                self.activated_guide_dict[guide_key] = guide_order
            self.remove_guide_name_from_working(guide_name)
        if guide_name in self.activating_guide_name_set:
            self.activating_guide_name_set.remove(guide_name)
        self.check_post_guide(guide_name)

    def check_post_guide(self, guide_name):
        post_guide_conf = self._lobby_guide_conf.get(guide_name, {}).get('post_guide_conf', {})
        delay = post_guide_conf.get('delay')
        post_guide_name = post_guide_conf.get('to', '')
        if not post_guide_name:
            return

        def cb():
            self._post_guide_timer_id = None
            self.on_notify_check_guide_with_check(post_guide_name)
            return

        if not delay:
            self.on_notify_check_guide_with_check(post_guide_name)
            return
        self.clear_post_guide_timer()
        from common.utils.timer import CLOCK
        self._post_guide_tid = global_data.game_mgr.register_logic_timer(cb, interval=delay, times=1, mode=CLOCK)

    def clear_post_guide_timer(self):
        if self._post_guide_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._post_guide_timer_id)
            self._post_guide_timer_id = None
        return

    def hide_guide_by_name(self, guide_name):
        self.deactivate_guide_by_name(guide_name, False)

    def remove_guide_name_from_working(self, guide_name):
        if guide_name in self._working_guide_list:
            self._working_guide_list.remove(guide_name)
            global_data.emgr.deactivate_guide_by_name_event.emit(guide_name)
        remove_ui_name_list = []
        for ui_name, guide_name_list in six.iteritems(self._guide_ui_2_name_dict):
            if guide_name in guide_name_list:
                guide_name_list.remove(guide_name)
            if not guide_name_list:
                remove_ui_name_list.append(ui_name)

        for ui_name in remove_ui_name_list:
            self._guide_ui_2_name_dict.pop(ui_name)

        if not self._guide_ui_2_name_dict:
            if self._is_binded_event:
                self.process_ui_event(False)
                self._is_binded_event = False

    def deactivate_guide_by_key(self, guide_key):
        guide_names = self._guide_key_dict.get(guide_key, [])
        for guide_name in guide_names:
            self.deactivate_guide_by_name(guide_name)

    def switch_node_guide(self, node, guide_name, is_finish):
        action_dict = self._lobby_guide_conf.get(guide_name, {}).get('guide_handler_params', {})
        func_name = action_dict.get('func')
        guide_key = self._lobby_guide_conf.get(guide_name, {}).get('guide_key')
        guide_order = self._lobby_guide_conf.get(guide_name, {}).get('guide_order')
        temp_func = getattr(guide_utils, is_finish or func_name if 1 else func_name + '_finish')
        if callable(temp_func):
            temp_func(node, guide_name, guide_key, action_dict)
        if is_finish:
            self.activated_guide_dict[guide_key] = guide_order
        else:
            self.activating_guide_name_set.add(guide_name)
        self.deactivate_guide_name_by_key_and_order(guide_key, guide_order)

    def on_resolution_changed_end(self):
        for guide_name, guide_name_dict in six.iteritems(self.saved_guide_nd_dict):
            for parent_ui_name, guide_nd in six.iteritems(guide_name_dict):
                if guide_nd and guide_nd.isValid():
                    if guide_nd.isVisible():
                        parent_ui = global_data.ui_mgr.get_ui(parent_ui_name)
                        if not parent_ui or not parent_ui.panel.isVisible:
                            return
                        ui_dict = self._lobby_guide_conf.get(guide_name, {}).get('guide_handler_params', {}).get('ui_list', {}).get(parent_ui_name)
                        func_name = ui_dict.get('temp_func')
                        guide_key = self._lobby_guide_conf.get(guide_name, {}).get('guide_key')
                        temp_func = getattr(guide_utils, func_name + '_refresh')
                        if callable(temp_func):
                            temp_func(guide_name, guide_key, parent_ui_name, ui_dict)

    def save_guide_node(self, guide_name, parent_ui_name, guide_nd):
        self.saved_guide_nd_dict.setdefault(guide_name, {})
        self.saved_guide_nd_dict[guide_name][parent_ui_name] = guide_nd

    def on_notify_check_guide_by_event(self, guide_name, is_by_event=True, is_force=False):
        if self.check_can_activate_by_guide_name(guide_name, is_by_event) or is_force:
            guide_dict = self._lobby_guide_conf.get(guide_name, {}).get('guide_handler_params', {}).get('ui_list', {})
            for ui_name, ui_dict in six.iteritems(guide_dict):
                self.activate_ui_guide(guide_name, ui_name, ui_dict)

    def on_notify_check_guide(self, guide_name):
        if self.check_can_activate_by_guide_name(guide_name):
            guide_dict = self._lobby_guide_conf.get(guide_name, {}).get('guide_handler_params', {}).get('ui_list', {})
            for ui_name, ui_dict in six.iteritems(guide_dict):
                self.activate_ui_guide(guide_name, ui_name, ui_dict)

    def on_notify_check_guide_with_check(self, guide_name):
        if not self.check_can_activate_by_guide_name(guide_name):
            return
        guide_dict = self._lobby_guide_conf.get(guide_name, {}).get('guide_handler_params', {}).get('ui_list', {})
        for ui_name, ui_dict in six.iteritems(guide_dict):
            from logic.gutils import template_utils
            ui_inst = global_data.ui_mgr.get_ui(ui_name)
            if not ui_inst:
                return
            page_name = ui_dict.get('page')
            if page_name:
                page = ui_inst.get_sub_page(page_name)
                if not page:
                    return
            self.activate_ui_guide(guide_name, ui_name, ui_dict)

    def on_notify_hide_guide(self, guide_name):
        if guide_name in self.activating_guide_name_set:
            self.hide_guide_by_name(guide_name)