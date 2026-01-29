# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impTime.py
from __future__ import absolute_import
import game3d
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Float, Int
import logic.gcommon.time_utility as t_util
import common.utils.timer as timer
from common.utils import network_utils
import time
from logic.gcommon.time_utility import TYPE_BATTLE, TYPE_GAME
ITVL_CHECK_NET_TYPE = 1
MIN_SERVER_FIX_TOLERANCE = 10
LAG_FLAG_NONE = 0
LAG_FLAG_BAD = 1
LAG_CNT_TO_RECONNECT_GAME = 3
LAG_CNT_TO_RECONNECT_BATTLE = 3

class impTime(object):

    def _init_time_from_dict(self, bdict):
        self._first_server_stmp = bdict.get('first_server_stmp', 0)
        self._battle_limit_rtt = bdict.get('battle_limit_rtt', t_util.DEFAULT_BATTLE_LIMIT_RTT)
        self._tm_sync_game = None
        self._last_game_hb_sent_time = 0
        self._lag_flag_game = LAG_FLAG_NONE
        self._tm_sync_battle = None
        self._last_battle_rtt = 0
        self._last_battle_hb_sent_time = 0
        self._lag_flag_battle = LAG_FLAG_NONE
        self._min_battle_rtt = 999
        self._use_min_rtt = False
        self._check_network_itvl_cnt = ITVL_CHECK_NET_TYPE
        self._cur_network_type = 0
        self._mp_lag_trigger_cnt = {TYPE_GAME: 0,TYPE_BATTLE: 0}
        self.on_first_game_time_fix()
        return

    @rpc_method(CLIENT_STUB, ())
    def mention_per_day_0(self):
        self._call_meta_member_func('_on_@_mention_per_day_0')

    @rpc_method(CLIENT_STUB, ())
    def mention_per_day_5(self):
        self._call_meta_member_func('_on_@_mention_per_day_5')

    @rpc_method(CLIENT_STUB, ())
    def heart_beat(self):
        self.game_heart_beat(check=False)

    def do_sync_time(self):
        self.game_heart_beat(check=False)

    def start_game_sync_time(self):
        self.stop_game_sync_time()
        self._tm_sync_game = global_data.game_mgr.register_logic_timer(lambda : self.game_heart_beat(), interval=t_util.GAME_HEART_BEAT_ITVL, times=-1, mode=timer.CLOCK)

    def stop_game_sync_time(self):
        if self._tm_sync_game:
            global_data.game_mgr.unregister_logic_timer(self._tm_sync_game)
            self._tm_sync_game = None
        self._last_game_hb_sent_time = 0
        self._lag_flag_game = LAG_FLAG_NONE
        return

    def game_heart_beat(self, check=True):
        now = time.time()
        if check and not self.local_battle and not self.new_local_battle:
            if self._last_game_hb_sent_time:
                global_data.emgr.net_delay_time_event.emit(TYPE_GAME, 0.997)
                if self._lag_flag_game != LAG_FLAG_BAD:
                    self._lag_flag_game = LAG_FLAG_BAD
                    global_data.emgr.net_lag_warn_event.emit(TYPE_GAME)
                self._mp_lag_trigger_cnt[TYPE_GAME] += 1
                if self._mp_lag_trigger_cnt[TYPE_GAME] >= LAG_CNT_TO_RECONNECT_GAME:
                    self._mp_lag_trigger_cnt[TYPE_GAME] = 0
                    self._on_lag_trigger_reconnect(TYPE_GAME)
            else:
                self._last_game_hb_sent_time = now
                self._mp_lag_trigger_cnt[TYPE_GAME] = 0
        self.call_server_method('sync_time', (now,), reliable=False)
        if not self.is_in_battle():
            self.check_network_type('game')

    @rpc_method(CLIENT_STUB, (Float('f_send'), Float('f_stamp'), Int('game_ver')))
    def on_sync_time(self, f_send, f_stamp, game_ver):
        self._last_game_hb_sent_time = 0
        self.game_ver = game_ver
        rtt = time.time() - f_send
        t = f_stamp + rtt / 2.0
        t_util.on_sync_time(TYPE_GAME, t)
        global_data.emgr.net_delay_time_event.emit(TYPE_GAME, rtt)
        if self._lag_flag_game != LAG_FLAG_NONE:
            self._lag_flag_game = LAG_FLAG_NONE
            global_data.emgr.net_lag_clear_event.emit()

    def on_first_game_time_fix(self):
        if not self._first_server_stmp:
            return
        stmp_sys = time.time()
        if abs(stmp_sys - self._first_server_stmp) > MIN_SERVER_FIX_TOLERANCE:
            t_util.on_sync_time(TYPE_GAME, self._first_server_stmp + 0.1)

    def begin_battle_sync_time(self, use_min_rtt=False):
        self._use_min_rtt = use_min_rtt
        self.stop_battle_sync_time()
        self._tm_sync_battle = global_data.game_mgr.register_logic_timer(lambda : self.battle_heart_beat(), interval=t_util.BATTLE_HEART_BEAT_ITVL, times=-1, mode=timer.CLOCK)
        t_util.trans_to_battle()
        self.battle_heart_beat()

    def battle_heart_beat(self):
        if not self.battle_id:
            return
        self.do_sync_battle_time()

    def stop_battle_sync_time(self):
        if self._tm_sync_battle:
            global_data.game_mgr.unregister_logic_timer(self._tm_sync_battle)
            self._tm_sync_battle = None
        self._last_battle_rtt = 0
        self._last_battle_hb_sent_time = 0
        self._lag_flag_battle = LAG_FLAG_NONE
        self._min_battle_rtt = 999
        return

    def do_sync_battle_time(self):
        if self._last_battle_hb_sent_time:
            global_data.emgr.net_delay_time_event.emit(TYPE_BATTLE, 0.997)
            if self._lag_flag_battle != LAG_FLAG_BAD:
                self._lag_flag_battle = LAG_FLAG_BAD
                global_data.emgr.net_lag_warn_event.emit(TYPE_BATTLE)
            self._mp_lag_trigger_cnt[TYPE_BATTLE] += 1
            if self._mp_lag_trigger_cnt[TYPE_BATTLE] >= LAG_CNT_TO_RECONNECT_BATTLE:
                self._mp_lag_trigger_cnt[TYPE_BATTLE] = 0
                self._on_lag_trigger_reconnect(TYPE_BATTLE)
        else:
            self._last_battle_hb_sent_time = time.time()
            self._mp_lag_trigger_cnt[TYPE_BATTLE] = 0
        self.call_soul_method('sync_battle_time', (time.time(), self._last_battle_rtt))
        self.check_network_type('battle')

    @rpc_method(CLIENT_STUB, (Float('f_send'), Float('f_stamp'), Int('game_ver')))
    def on_sync_battle_time(self, f_send, f_stamp, game_ver):
        if global_data.battle:
            global_data.battle.game_ver = game_ver
        self._last_battle_hb_sent_time = 0
        rtt = time.time() - f_send
        t = f_stamp + rtt / 2.0
        self._last_battle_rtt = rtt
        if t_util.battle_time_delta_ready() and rtt > self._battle_limit_rtt:
            return
        if not self._use_min_rtt:
            t_util.on_sync_time(TYPE_BATTLE, t)
        elif rtt < self._min_battle_rtt or t_util.check_battle_sync_time(t):
            self._min_battle_rtt = rtt
            t_util.on_sync_time(TYPE_BATTLE, t)
        global_data.emgr.net_delay_time_event.emit(TYPE_BATTLE, rtt)
        global_data.emgr.net_lag_clear_event.emit()
        if self._lag_flag_battle != LAG_FLAG_NONE:
            self._lag_flag_battle = LAG_FLAG_NONE
            global_data.emgr.net_lag_clear_event.emit()

    @rpc_method(CLIENT_STUB, (Int('i_id'),))
    def on_query_alive(self, i_id):
        self.call_soul_method('response_alive', (i_id,))

    def _on_lag_trigger_reconnect(self, i_type):
        if self.is_in_battle() and i_type == TYPE_GAME:
            return
        import logic.gutils.ConnectHelper as cnhp
        ins = cnhp.ConnectHelper()
        if ins.is_connected():
            ins.disconnect()

    def clear_mp_lag_trigger_cnt(self):
        self._mp_lag_trigger_cnt = {TYPE_BATTLE: 0,TYPE_GAME: 0}

    @rpc_method(CLIENT_STUB, ())
    def reconnect_battle(self):
        self._on_lag_trigger_reconnect(TYPE_BATTLE)

    def check_network_type(self, s_from=''):
        self._check_network_itvl_cnt -= 1
        if self._check_network_itvl_cnt % ITVL_CHECK_NET_TYPE > 0:
            return
        self._check_network_itvl_cnt = ITVL_CHECK_NET_TYPE
        cur_type = network_utils.g93_get_network_type()
        pre_type = self._cur_network_type
        if pre_type != cur_type:
            if cur_type in (network_utils.TYPE_WIFI, network_utils.TYPE_MOBILE) and pre_type != 0:
                import logic.gutils.ConnectHelper as cnhp
                ins = cnhp.ConnectHelper()
                ins.disconnect()
            self._cur_network_type = cur_type

    def query_cur_network_type(self):
        self._cur_network_type = network_utils.g93_get_network_type()

    def reset_network_type_check(self):
        self._check_network_itvl_cnt = ITVL_CHECK_NET_TYPE
        self._cur_network_type = 0

    def _destroy_time(self):
        self.stop_game_sync_time()
        self.stop_battle_sync_time()