# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impCredit.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Bool, Dict, Str
from logic.comsys.common_ui.NormalConfirmUI import LobbyConfirmUI2
from logic.gutils.scene_utils import is_in_lobby

class impCredit(object):

    def _init_credit_from_dict(self, bdict):
        self._credit_point = bdict.get('credit_point', 100)
        self._credit_level = bdict.get('credit_level', 5)
        self._credit_reward_sts = bdict.get('credit_reward_sts', [])
        self._point_limit = bdict.get('point_limit', 0)

    def credit_report(self, report_uid, report_info):
        self.call_server_method('credit_report', (report_uid, report_info))

    @rpc_method(CLIENT_STUB, (Bool('ret'), Dict('info')))
    def on_credit_report(self, ret, info):
        if ret:
            ui = global_data.ui_mgr.show_ui('CreditReportResultSuccess', 'logic.comsys.role')
        else:
            ui = global_data.ui_mgr.show_ui('CreditReportResultFail', 'logic.comsys.role')
        ui.show_info(info)

    @rpc_method(CLIENT_STUB, (Dict('info'),))
    def refresh_credit_info(self, info):
        credit_point = info.get('credit_point', None)
        if credit_point:
            self._credit_point = credit_point
        credit_level = info.get('credit_level', None)
        if credit_level:
            if self._credit_level != credit_level:
                if self._credit_level > credit_level:
                    ui = global_data.ui_mgr.show_ui('CreditDownUI', 'logic.comsys.role')
                    ui.show_level(credit_level)
                self._credit_level = credit_level
                lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
                if lobby_ui:
                    lobby_ui.update_role_head_rp()
        credit_reward_sts = info.get('credit_reward_sts', None)
        if credit_reward_sts:
            self._credit_reward_sts = credit_reward_sts
        point_limit = info.get('point_limit', None)
        if point_limit:
            self._point_limit = point_limit
        return

    def request_credit_reward(self, level):
        self.call_server_method('request_credit_reward', (int(level),))

    @rpc_method(CLIENT_STUB, (Int('level'), Bool('opt')))
    def on_request_credit_reward(self, level, opt):
        if opt:
            self._credit_reward_sts.append(level)
            global_data.emgr.on_receive_credit_reward.emit(level)

    @rpc_method(CLIENT_STUB, (Str('game_id'), Int('reward_id'), Dict('param')))
    def credit_compensation_reward(self, game_id, reward_id, param):
        ui = global_data.ui_mgr.show_ui('CreditCompensateUI', 'logic.comsys.role')
        ui.init_data(game_id, reward_id, param)

    @rpc_method(CLIENT_STUB, (Int('afk_ban'),))
    def credit_afk_ban(self, afk_ban):
        if afk_ban > 0:
            LobbyConfirmUI2(content=get_text_by_id(900030).format(time=afk_ban))
        else:
            LobbyConfirmUI2(content=get_text_by_id(900029))

    def request_credit_compensation_reward(self, game_id):
        self.call_server_method('request_credit_compensation_reward', (game_id,))

    @rpc_method(CLIENT_STUB)
    def credit_afk_tips(self):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def confirm_callback():
            from logic.gutils.jump_to_ui_utils import jump_to_mode_choose
            from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN
            jump_to_mode_choose(PLAY_TYPE_CHICKEN, select_mode=False)

        SecondConfirmDlg2().confirm(content=get_text_by_id(900013), confirm_callback=confirm_callback, confirm_text=80284)

    def get_credit_point(self):
        return self._credit_point

    def get_credit_level(self):
        return self._credit_level

    def get_credit_day_point(self):
        return self._point_limit

    def get_credit_reward_sts(self):
        return self._credit_reward_sts