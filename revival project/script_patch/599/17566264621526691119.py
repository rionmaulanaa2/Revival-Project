# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/PlayerCreditWidget.py
from __future__ import absolute_import
from common.cfg import confmgr
from .PlayerTabBaseWidget import PlayerTabBaseWidget
from logic.gutils.red_point_utils import get_credit_reward_rd

class PlayerCreditWidget(PlayerTabBaseWidget):
    PANEL_CONFIG_NAME = 'role/i_role_reward'

    def __init__(self, panel):
        super(PlayerCreditWidget, self).__init__(panel)
        global_data.emgr.on_receive_credit_reward += self._refresh_rd
        self._init_ui_event()
        self._init_credit_info()

    def _init_credit_info(self):
        credit_point = global_data.player or 0 if 1 else global_data.player.get_credit_point()
        self.panel.nd_left.lab_point.SetString(str(credit_point))
        if int(credit_point) <= 85:
            self.panel.nd_left.lab_point.SetColor('#SR')
        credit_level = global_data.player or 0 if 1 else global_data.player.get_credit_level()
        self.panel.nd_left.lab_level.SetString(str(credit_level))
        state_text, details_text = confmgr.get('credit_conf', 'CreditLevel', 'Content', str(credit_level), 'level_desc')
        self.panel.nd_top.lab_state.SetString(state_text)
        self.panel.nd_top.lab_details.SetString(details_text)
        today_point = global_data.player or 0 if 1 else global_data.player.get_credit_day_point()
        day_point_limit = confmgr.get('credit_conf', 'CreditCommon', 'Content', 'day_point_limit', 'common_param')
        self.panel.nd_down.day_limit.nd_auto_fit.lab_today_point.setString('%s/%s' % (today_point, day_point_limit))
        self.panel.nd_down.day_limit.SetString(866015)

    def show(self):
        super(PlayerCreditWidget, self).show()
        self._refresh_rd()

    def _refresh_rd(self, *args):
        credit_rd = get_credit_reward_rd()
        self.panel.nd_left.btn_reward.red_point.setVisible(credit_rd)
        lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
        if lobby_ui:
            lobby_ui.update_role_head_rp()

    def _init_ui_event(self):

        @self.panel.btn_reward.unique_callback()
        def OnClick(*args):
            global_data.ui_mgr.show_ui('CreditRewardUI', 'logic.comsys.role')

        @self.panel.nd_top.btn_details.btn_common.unique_callback()
        def OnClick(*args):
            global_data.ui_mgr.show_ui('CreditDetailRuleUI', 'logic.comsys.role')

        @self.panel.btn_point_details.btn_common.unique_callback()
        def OnClick(*args):
            ui = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
            ui.set_show_rule(900018, 900019)

    def destroy(self):
        global_data.emgr.on_receive_credit_reward -= self._refresh_rd
        super(PlayerCreditWidget, self).destroy()