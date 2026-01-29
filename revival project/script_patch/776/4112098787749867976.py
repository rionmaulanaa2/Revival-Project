# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Crown/CrownEndStatisticsShareUI.py
from __future__ import absolute_import
from six.moves import range
import math
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import statistics_const as stat_const
from logic.gutils.role_head_utils import init_role_head, get_role_default_photo, get_mecha_photo
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from common.cfg import confmgr
from logic.gcommon import time_utility
from common.const import uiconst
from logic.gutils.end_statics_utils import on_click_player_head
from logic.comsys.battle.Death.DeathEndStatisticsShareUI import DeathStatisticsShareUI
from logic.gutils.item_utils import get_mecha_name_by_id
from logic.gutils.role_utils import get_role_name_id

class CrownStatisticsShareUI(DeathStatisticsShareUI):

    def init_group_share_ui(self):
        our_group = self.all_infos[0][1]
        other_group = self.all_infos[1][1]
        our_nd_list = self.panel.temp_details.nd_blue.list_score
        other_nd_list = self.panel.temp_details.nd_red.list_score
        self.panel.temp_details.nd_blue.nd_title._nameless_children[0].lab_blue_title_1.SetString(get_text_by_id(83480))
        self.panel.temp_details.nd_red.nd_title._nameless_children[0].lab_red_title_1.SetString(get_text_by_id(83480))
        item_list_infos = [
         (
          our_group, our_nd_list), (other_group, other_nd_list)]
        for groups, nd_list in item_list_infos:
            nd_list.SetInitCount(len(groups))
            total_kill_num = 0
            for p_ginfo in groups:
                total_kill_num += p_ginfo[2] + p_ginfo[3]

            for idx, ginfo in enumerate(groups):
                item = nd_list.GetItem(idx)
                item.lab_name.SetString(ginfo[1])
                init_role_head(item.temp_role, ginfo[6], ginfo[5])
                if ginfo[0] == str(self.my_uid):
                    item.img_self.setVisible(True)
                    item.lab_name.SetColor('#DB')
                if ginfo[10] is None:
                    ginfo[10] = (
                     (0, 0), (0, 0), (0, 0))
                for i in range(3):
                    data_item = item.list_data.GetItem(i)
                    if i == 0:
                        kill_num = ginfo[2] + ginfo[3]
                        data_item.lab_data.SetString('%d' % kill_num)
                        percent = float(kill_num) / total_kill_num * 100 if total_kill_num > 0 else 0
                    else:
                        data_item.lab_data.SetString('%d' % ginfo[10][i][0])
                        percent = ginfo[10][i][1] * 100
                    data_item.progress.SetPercentage(percent)
                    data_item.lab_persent.SetString('%.1f%%' % percent)
                    if ginfo[0] == str(self.my_uid):
                        data_item.lab_data.SetColor('#DB')
                        data_item.lab_persent.SetColor('#DB')

        return

    def init_settle_score_ui(self):
        self.panel.temp_details.nd_blue.nd_title._nameless_children[0].lab_blue_title_1.SetString(get_text_by_id(83480))
        self.panel.temp_details.nd_red.nd_title._nameless_children[0].lab_red_title_1.SetString(get_text_by_id(83480))
        our_item_list = self.panel.temp_data.nd_blue.list_score.GetAllItem()
        other_item_list = self.panel.temp_data.nd_red.list_score.GetAllItem()
        our_group = self.all_infos[0][1]
        other_group = self.all_infos[1][1]
        item_list_infos = [(our_group, our_item_list), (other_group, other_item_list)]
        for groups, items in item_list_infos:
            for idx, item in enumerate(items):
                if idx >= len(groups):
                    item.setVisible(False)
                    continue
                ginfo = groups[idx]
                item.lab_name.SetString(ginfo[1])
                if ginfo[18]:
                    mecha_name = get_mecha_name_by_id(int(ginfo[18]))
                    item.lab_name2.SetString(mecha_name)
                elif ginfo[19]:
                    role_name = get_role_name_id(int(ginfo[19]))
                    item.lab_name2.SetString(role_name)
                item.lab_kill.SetString(str(ginfo[10][0][0]))
                item.lab_mech.SetString(str(ginfo[11] + ginfo[12]))
                item.lab_score.SetString('%.1f' % float(ginfo[9]))
                init_role_head(item.temp_role, ginfo[6], ginfo[5])
                is_mvp = ginfo[8]

                @item.temp_role.unique_callback()
                def OnClick(btn, touch, player_uid=ginfo[0]):
                    on_click_player_head(touch, player_uid)

                item.btn_like.setVisible(False)
                if ginfo[0] == str(self.my_uid):
                    item.btn_add_friend.SetEnable(False)
                    item.btn_report.SetEnable(False)
                    item.img_self.setVisible(True)
                    item.lab_name.SetColor('#DB')
                    item.lab_kill.SetColor('#DB')
                    item.lab_mech.SetColor('#DB')
                    item.lab_score.SetColor('#DB')
                else:
                    if not global_data.message_data.is_friend(ginfo[0]):

                        @item.btn_add_friend.callback()
                        def OnClick(btn, touch, uid=int(ginfo[0])):
                            global_data.player.req_add_friend(uid)
                            btn.setVisible(False)

                    else:
                        item.btn_add_friend.setVisible(False)
                    if self._game_end_ts:
                        report_max_interval = confmgr.get('credit_conf', 'CreditCommon', 'Content', 'settle_credit_interval', 'common_param', default=0)
                        to_hide_report_time = self._game_end_ts + report_max_interval - time_utility.get_server_time()
                        if to_hide_report_time > 0:

                            def hide_report(btn=item.btn_report):
                                btn.setVisible(False)

                            item.DelayCall(to_hide_report_time, hide_report)
                        else:
                            item.btn_report.setVisible(False)

                    @item.btn_report.callback()
                    def OnClick(btn, touch, uid=ginfo[0], name=ginfo[1], eid=ginfo[7]):
                        from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_BATTLE_HISTORY, REPORT_CLASS_BATTLE
                        ui = global_data.ui_mgr.show_ui('UserReportUI', 'logic.comsys.report')
                        ui.report_users([{'uid': uid,'name': name}])
                        ui.set_report_class(REPORT_CLASS_BATTLE)
                        ui.set_extra_report_info('', '', REPORT_FROM_TYPE_BATTLE_HISTORY)
                        ui.set_additional_report_info(self._game_info)
                        if self._game_end_ts:
                            report_max_interval = confmgr.get('credit_conf', 'CreditCommon', 'Content', 'settle_credit_interval', 'common_param', default=0)
                            ui.set_report_ddl(self._game_end_ts + report_max_interval)
                        btn.SetSelect(True)
                        btn.SetEnable(False)

                        def cancel_report():
                            btn.SetSelect(False)
                            btn.SetEnable(True)

                        ui.set_close_callback(cancel_report)

                if is_mvp:
                    item.lab_score.setVisible(False)
                    if groups == our_group and (self.win or self._battle_draw) or groups == other_group and not (self.win or self._battle_draw):
                        path = 'gui/ui_res_2/fight_end/img_mvp1.png'
                    else:
                        path = 'gui/ui_res_2/fight_end/img_mvp2.png'
                    item.img_mvp.SetDisplayFrameByPath('', path)
                    item.img_mvp.setVisible(True)
                    item.lab_score2.SetString('%.1f' % float(ginfo[9]))