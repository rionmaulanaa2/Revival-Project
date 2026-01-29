# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBet.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Dict, List
from mobile.common.rpcdecorator import CLIENT_STUB, rpc_method

class impBet(object):

    def _init_bet_from_dict(self, bdict):
        self._my_bet_info_list = []

    def bet_battle_top_player(self, battle_id, uid, comp_id, comp_round, option):
        self.call_server_method('bet_battle_top_player', (battle_id, uid, comp_id, comp_round, option))

    @rpc_method(CLIENT_STUB, (List('bet_info_list'),))
    def bet_battle_top_player_ret(self, bet_info_list):
        global_data.ui_mgr.close_ui('LiveGuessUI')
        self._my_bet_info_list = bet_info_list
        global_data.emgr.live_my_bet_info_ret.emit(bet_info_list)

    def pull_bet_player_show_info(self, battle_id, uid):
        self.call_server_method('pull_bet_player_show_info', (battle_id, uid))

    @rpc_method(CLIENT_STUB, (Dict('show_info'),))
    def pull_bet_player_show_info_ret(self, show_info):
        global_data.ui_mgr.show_ui('LiveGuessUI', 'logic.comsys.live')
        ui_inst = global_data.ui_mgr.get_ui('LiveGuessUI')
        if ui_inst:
            ui_inst.init_play_data(show_info)

    def pull_my_bet_info(self):
        self.call_server_method('pull_my_bet_info', ())

    @rpc_method(CLIENT_STUB, (List('bet_info_list'),))
    def pull_my_bet_info_ret(self, bet_info_list):
        self._my_bet_info_list = bet_info_list
        global_data.emgr.live_my_bet_info_ret.emit(bet_info_list)

    def get_my_bet_info_list(self):
        return self._my_bet_info_list