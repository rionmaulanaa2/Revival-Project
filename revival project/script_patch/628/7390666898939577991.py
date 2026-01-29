# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impConcert.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Dict, List, Str, Bool
from logic.gcommon.common_const import activity_const as acconst
from logic.gcommon import time_utility as tutil
from logic.client.const import game_mode_const
from logic.gcommon.cdata import global_lottery_config

class impConcert(object):

    def _init_concert_from_dict(self, bdict):
        self.need_offer_concert_reward = bdict.get('need_offer_concert_reward', False)
        self.has_receive_normal_reward = bdict.get('receive_normal_view_reward', False)
        self.has_receive_special_reward = bdict.get('receive_special_view_reward', False)
        self.anniversary_open_reward = bdict.get('anniversary_open_reward', [False, False])
        self.concert_view_time = bdict.get('concert_view_time', 0)
        self.has_temporarily_apply_concert_reward = False

    def received_concert_reward(self):
        self.has_temporarily_apply_concert_reward = True
        self.call_server_method('receive_concert_reward')

    @rpc_method(CLIENT_STUB, (Bool('normal'), Bool('special')))
    def received_concert_reward_succ(self, normal, special):
        self.has_receive_normal_reward = normal
        self.has_receive_special_reward = special

    def check_open_live_medal(self):

        def check_can_show():
            return self.need_offer_concert_reward and not (self.has_receive_normal_reward or self.has_temporarily_apply_concert_reward)

        if check_can_show():

            def callback():
                self.has_temporarily_apply_concert_reward = True
                from logic.comsys.activity.ActivityAIConcert.KizunaBadgeUI import KizunaBadgeUI
                KizunaBadgeUI(None)
                return

            if not global_data.player.has_advance_callback('KizunaBadgeUI'):
                global_data.player.add_advance_callback('KizunaBadgeUI', callback, hide_lobby_ui=False)

    def receive_anniversary_reward(self, idx):
        if idx >= 2:
            return
        if self.anniversary_open_reward[idx]:
            return
        self.call_server_method('receive_anniversary_reward', (idx,))

    def has_received_anniversary_reward(self, idx):
        return self.anniversary_open_reward[idx]

    def attend_global_anniversary_lottery(self):
        if not global_data.battle:
            return
        from logic.gutils.concert_utils import get_concert_region_lottery_id_list
        mode_type = global_data.game_mode.get_mode_type()
        if mode_type != game_mode_const.GAME_MODE_CONCERT:
            return
        now = tutil.time()
        lid_list = get_concert_region_lottery_id_list()
        for lid in lid_list:
            lconf = global_lottery_config.get_global_lottery_conf(lid)
            start_time = lconf['start_time']
            settle_time = lconf['settle_time']
            if start_time <= now < settle_time:
                self.attend_global_lottery(lid)
                break