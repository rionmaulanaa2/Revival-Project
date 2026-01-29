# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impActivity.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import List, Str, Float
from logic.gutils.client_utils import post_method

class impActivity(object):

    def _init_activity_from_dict(self, bdict):
        self.activity_list = None
        self.activity_map = {}
        self.activity_closetime_data = bdict.get('activity_closetime_data', {})
        self.last_weekend_bank_reward_get_ts = bdict.get('last_weekend_bank_reward_get_ts', 0)
        return

    def _on_activity_mention_per_day_0(self):
        global_data.emgr.on_activity_mention_per_day_0.emit()

    @rpc_method(CLIENT_STUB, (List('activity_list'),))
    def update_activity(self, activity_list):
        for activity_info in activity_list:
            self.activity_map[activity_info[0]] = self._create_activity_data(activity_info)

        self.activity_list = activity_list
        global_data.emgr.refresh_activity_list.emit()

    @rpc_method(CLIENT_STUB, (Str('activity_id'), Float('close_time')))
    def update_activity_closetime(self, activity_id, close_time):
        self.activity_closetime_data[activity_id] = close_time

    def get_opened_activities(self):
        self.call_server_method('get_opened_activities', ())

    def get_activity_list(self):
        return self.activity_list

    def get_opened_activity_data(self):
        return self.activity_map

    def has_activity(self, activity_type):
        return activity_type in self.activity_map

    def read_activity_list(self, activity_type):
        if self.activity_list is None:
            return
        else:
            if activity_type in self.activity_map and self.activity_map[activity_type]['has_red_point']:
                self.activity_map[activity_type]['has_red_point'] = False
                self.annul_red_dot(activity_type)
            self.refresh_activity_redpoint()
            return

    @post_method
    def refresh_activity_redpoint(self):
        global_data.emgr.refresh_activity_redpoint.emit()

    @rpc_method(CLIENT_STUB, (Str('activity_type'),))
    def notify_del_activity(self, activity_type):
        self.del_activity(activity_type)

    def del_activity(self, activity_type):
        if not self.activity_list:
            return
        for idx, info in enumerate(self.activity_list):
            if info[0] == activity_type:
                del self.activity_list[idx]
                del self.activity_map[activity_type]
                break

        global_data.emgr.refresh_activity_list.emit()

    def annul_red_dot(self, activity_type):
        self.call_server_method('annul_red_dot', (activity_type,))

    def save_activity_click_data(self, activity_type):
        self.activity_map.setdefault(activity_type, {'activity_type': activity_type})
        self.activity_map[activity_type]['has_red_point'] = False
        self.call_server_method('on_click_activity', (activity_type,))

    def _create_activity_data(self, l_activity_info):
        data = {'activity_type': l_activity_info[0],
           'has_red_point': l_activity_info[1]
           }
        return data

    def get_last_weekend_bank_reward_get_ts(self):
        return self.last_weekend_bank_reward_get_ts

    def set_last_weekend_bank_reward_get_ts(self, ts):
        self.last_weekend_bank_reward_get_ts = ts