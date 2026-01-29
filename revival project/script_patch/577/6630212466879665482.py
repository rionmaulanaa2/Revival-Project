# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impTwitterReward.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict, List, Int, Bool

class impTwitterReward(object):

    def _init_twitterreward_from_dict(self, bdict):
        self._twitter_reward = bdict.get('twitter_reward')
        self._twitter_open_date = bdict.get('twitter_open_date')

    def check_twitter_follow_available(self):
        is_in_open_time = True
        if self._twitter_open_date:
            from logic.gcommon import time_utility as tutil
            is_in_open_time = tutil.check_timestamp_in_time_range({'open_dates': [self._twitter_open_date]}, tutil.get_server_time())
        return self._twitter_reward is not None and is_in_open_time

    def get_twitter_reward(self, index):
        self.call_server_method('get_twitter_reward', (index,))

    def follow_twitter(self):
        self.call_server_method('follow_twitter')

    def local_set_twitter_follow_reward_state(self, state):
        if self._twitter_reward:
            self._twitter_reward[0] = state
            global_data.emgr.update_twitter_follow_reward_event.emit()

    def get_twitter_reward_state(self):
        if self._twitter_reward:
            return (self._twitter_reward[0], self._twitter_reward[1:])

    @rpc_method(CLIENT_STUB, (List('state'),))
    def get_twitter_reward_reply(self, state):
        self._twitter_reward = state
        global_data.emgr.update_twitter_follow_reward_event.emit()