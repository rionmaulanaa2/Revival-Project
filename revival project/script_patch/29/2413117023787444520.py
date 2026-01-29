# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Assault/AssaultEndStatisticsShareUI.py
from __future__ import absolute_import
import six
import math
from logic.comsys.battle.Death.DeathEndStatisticsShareUI import DeathStatisticsShareUI
from logic.gutils.role_head_utils import init_role_head
from logic.gutils.end_statics_utils import on_click_player_head
from common.cfg import confmgr
from logic.gcommon import time_utility
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT, TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL, BATTLE_SETTLE_REASON_SURRENDER

class AssaultEndStatisticsShareUI(DeathStatisticsShareUI):
    PANEL_CONFIG_NAME = 'role/role_battle_record_assault'

    def on_init_panel(self, _settle_dict, my_group_list, other_group_list, my_uid, game_info=None):
        self.group_info = _settle_dict.get('group_info', {})
        self_group_id = _settle_dict.get('my_group_id')
        self.self_group_soul = self.group_info.get(str(self_group_id), {})
        self.other_group_soul = {}
        for group_id, group_soul in six.iteritems(self.group_info):
            if str(group_id) != str(self_group_id):
                self.other_group_soul = group_soul

        join_score_dict = _settle_dict.get('join_score_dict', {})
        list_1 = list(join_score_dict.keys())
        list_2 = list(self.self_group_soul.values()) + list(self.other_group_soul.values())
        self.my_soul_id = [ x for x in list_1 if x not in list_2 ]
        if not self.my_soul_id:
            self.my_soul_id = self.self_group_soul.get(str(my_uid), 1)
        else:
            self.my_soul_id = self.my_soul_id[0]
        self.join_score_dict = join_score_dict.get(self.my_soul_id, {})
        self.join_soul_dmg_dict = _settle_dict.get('join_soul_dmg_dict', {}).get(self.my_soul_id, {})
        self.join_soul_score_dict = _settle_dict.get('join_soul_score_dict', {}).get(self.my_soul_id, {})
        self.join_soul_assist_dict = _settle_dict.get('join_soul_assist_dict', {}).get(self.my_soul_id, {})
        super(AssaultEndStatisticsShareUI, self).on_init_panel(_settle_dict, my_group_list, other_group_list, my_uid, game_info)

    def init_game_result(self):
        settle_dict = self._settle_dict
        self_group_id = settle_dict.get('my_group_id')
        group_dict = settle_dict.get('group_points_dict')
        self_score = group_dict.get(str(self_group_id), 0) - self.join_score_dict.get(str(self_group_id), 0)
        other_score = 0
        for g_id in six.iterkeys(group_dict):
            if g_id != str(self_group_id):
                other_score = group_dict[g_id] - self.join_score_dict.get(str(g_id), 0)

        self.panel.nd_score.lab_score_blue.SetString(str(self_score))
        self.panel.nd_score.lab_score_red.SetString(str(other_score))
        reason = settle_dict.get('settle_reason', BATTLE_SETTLE_REASON_NORMAL)
        last_point_got_interval = settle_dict.get('last_point_got_interval', TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL)
        if reason == BATTLE_SETTLE_REASON_SURRENDER:
            if settle_dict.get('is_surrender', False):
                self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_fail.png')
            else:
                self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_win.png')
        elif self_score > other_score or reason == BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT:
            if self_score - other_score == 1 and last_point_got_interval < TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL:
                self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_konckout.png')
            else:
                self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_win.png')
        elif self_score == other_score:
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_deuce.png')
        else:
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_fail.png')

    def init_settle_score_ui(self):
        from logic.gutils.item_utils import get_mecha_name_by_id
        from logic.gutils.role_utils import get_role_name_id
        our_item_list = self.panel.temp_data.nd_blue.list_score.GetAllItem()
        other_item_list = self.panel.temp_data.nd_red.list_score.GetAllItem()
        our_group = self.all_infos[0][1]
        other_group = self.all_infos[1][1]
        item_list_infos = [
         (
          our_group, our_item_list, self.self_group_soul), (other_group, other_item_list, self.other_group_soul)]
        for groups, items, group_soul in item_list_infos:
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
                item.lab_kill.SetString(str(ginfo[2] + ginfo[3] - self.join_soul_score_dict.get(group_soul.get(str(ginfo[0]), 0), 0)))
                item.lab_mech.SetString(str(ginfo[11] + ginfo[12] - self.join_soul_assist_dict.get(group_soul.get(str(ginfo[0]), 0), 0)))
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

    def init_group_share_ui(self):
        our_group = self.all_infos[0][1]
        other_group = self.all_infos[1][1]
        our_nd_list = self.panel.temp_details.nd_blue.list_score
        other_nd_list = self.panel.temp_details.nd_red.list_score
        item_list_infos = [(our_group, our_nd_list, self.self_group_soul), (other_group, other_nd_list, self.other_group_soul)]
        for groups, nd_list, group_soul in item_list_infos:
            nd_list.SetInitCount(len(groups))
            for idx, ginfo in enumerate(groups):
                item = nd_list.GetItem(idx)
                item.lab_name.SetString(ginfo[1])
                init_role_head(item.temp_role, ginfo[6], ginfo[5])
                if ginfo[0] == str(self.my_uid):
                    item.img_self.setVisible(True)
                    item.lab_name.SetColor('#DB')
                detail_info = ginfo[10]
                if not detail_info:
                    detail_info = (
                     (0, 0), (0, 0), (0, 0))
                item.list_data.GetItem(0).lab_data.SetString(str(int(detail_info[0][0]) - int(self.join_soul_score_dict.get(group_soul.get(str(ginfo[0]), 0), 0))))
                item.list_data.GetItem(1).lab_data.SetString(str(int(detail_info[1][0]) - int(self.join_soul_dmg_dict.get(group_soul.get(str(ginfo[0])), 0))))
                item.list_data.GetItem(2).lab_data.SetString(str(int(detail_info[2][0])))
                for i in range(3):
                    data_item = item.list_data.GetItem(i)
                    if ginfo[0] == str(self.my_uid):
                        data_item.lab_data.SetColor('#DB')
                        data_item.lab_persent.SetColor('#DB')