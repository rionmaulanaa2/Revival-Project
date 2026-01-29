# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/log/UILifetimeLogMgr.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from common.framework import Singleton
from common.cfg import confmgr
from logic.gcommon.time_utility import get_server_time

class UILifetimeLogMgr(Singleton):
    ALIAS_NAME = 'ui_lifetime_log_mgr'
    from common.cfg import confmgr

    def init(self):
        self._timer = None
        self._ui_start_time_dict = {}
        self._page_start_time_dict = {}
        self._page_belong_ui_dict = {}
        self._log_dict = {}
        self._is_binded = False
        return

    def on_finalize(self):
        self.stop_listener()

    def process_event(self, is_bind=True):
        if is_bind == self._is_binded:
            return
        emgr = global_data.emgr
        econf = {'ui_open_event': self.on_ui_open,
           'ui_close_event': self.on_ui_close,
           'net_login_reconnect_event': self.on_login_reconnect
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self._is_binded = is_bind

    def on_ui_open(self, ui_name):
        name_conf = confmgr.get('ui_lifetime_log_conf', 'UIList', 'Content')
        if ui_name in name_conf:
            self.start_record_ui_page_life_time(ui_name, '')

    def on_ui_close(self, ui_name):
        name_conf = confmgr.get('ui_lifetime_log_conf', 'UIList', 'Content')
        if ui_name in name_conf:
            self.finish_record_ui_page_life_time(ui_name, '')

    def start_record_ui_page_life_time(self, ui_name, page_name=None):
        print('start_record_ui_page_life_time', ui_name, page_name)
        if not page_name:
            if ui_name not in self._ui_start_time_dict:
                self._ui_start_time_dict[ui_name] = get_server_time()
        else:
            self._page_belong_ui_dict[page_name] = ui_name
            if ui_name not in self._ui_start_time_dict:
                self._ui_start_time_dict[ui_name] = get_server_time()
            self._page_start_time_dict[page_name] = get_server_time()

    def finish_record_ui_page_life_time(self, ui_name, page_name=None):
        if not page_name:
            if ui_name in self._ui_start_time_dict:
                self._log_dict.setdefault(ui_name, {})
                cur_log = self._log_dict.get(ui_name, {})
                if 'stay_time' in cur_log:
                    cur_log['stay_time'] += get_server_time() - self._ui_start_time_dict[ui_name]
                else:
                    cur_log['stay_time'] = get_server_time() - self._ui_start_time_dict[ui_name]
                for page in list(six.iterkeys(self._page_start_time_dict)):
                    page_ui_name = self._page_belong_ui_dict.get(page)
                    if page_ui_name == ui_name:
                        self._record_page_time(ui_name, page_name)
                        if page_name in self._page_start_time_dict:
                            del self._page_start_time_dict[page_name]

                del self._ui_start_time_dict[ui_name]
        else:
            self._record_page_time(ui_name, page_name)
            del self._page_start_time_dict[page_name]

    def _record_page_time(self, ui_name, page_name):
        if ui_name in self._ui_start_time_dict and page_name in self._page_start_time_dict:
            self._log_dict.setdefault(ui_name, {})
            page_stay_time_dict = self._log_dict.get(ui_name, {})
            page_stay_time_dict.setdefault(page_name, 0)
            page_stay_time_dict[page_name] += get_server_time() - self._page_start_time_dict[page_name]

    def finish_all_record(self):
        for page_name in list(six_ex.keys(self._page_start_time_dict)):
            ui_name = self._page_belong_ui_dict.get(page_name, '')
            self.finish_record_ui_page_life_time(ui_name, page_name)

        for ui_name in list(six_ex.keys(self._ui_start_time_dict)):
            self.finish_record_ui_page_life_time(ui_name, '')

    def stop_listener(self):
        self.process_event(False)
        self.unregister_timer()

    def start_listener(self):
        self.process_event(True)
        self.register_timer()

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.send_record_log_to_server, interval=60, mode=CLOCK)

    def unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = None
        return

    def send_record_log_to_server(self):
        if self._log_dict:
            if global_data.player:
                global_data.player.call_server_method('record_view_page_info', (self._log_dict,))
                self._log_dict = {}

    def convertTimeToIntDict(self, logdict):
        int_logdict = {}
        for ui_name, ui_info in six.iteritems(logdict):
            int_logdict[ui_name] = {}
            for k, t in six.iteritems(ui_info):
                int_logdict[ui_name][k] = int(t)

        return int_logdict

    def on_login_reconnect(self, *args):
        if self._timer:
            self._timer = None
            self.register_timer()
        return