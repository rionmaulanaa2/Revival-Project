# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/SnatchEgg/GoldenEggEndStatisticsShareUI.py
from __future__ import absolute_import
import six
import six_ex
import math
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import statistics_const as stat_const
from logic.gutils.role_head_utils import init_role_head, get_role_default_photo, get_mecha_photo
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL
from common.cfg import confmgr
from logic.gcommon import time_utility
from common.const import uiconst
from logic.gutils.end_statics_utils import on_click_player_head

class GoldenEggEndStatisticsShareUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_golden_egg/golden_egg_battle_record_contention'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_exit.btn.OnClick': 'on_show_detail',
       'btn_share_2.btn.OnClick': 'on_click_share_btn_2'
       }
    SHOW_SELF_SCORE = 0
    SHOW_ALL_SCORE = 1
    SHARE_TIPS_INFO = (
     'btn_share_2', 3154, ('50%', '100%'))

    def on_init_panel(self, _settle_dict, my_group_list, other_group_dict, my_uid, game_info=None):
        self.regist_main_ui()
        self.hide_main_ui(exceptions=['DeathEndTransitionUI'])
        self.panel.nd_1.setVisible(False)
        self._cur_status = GoldenEggEndStatisticsShareUI.SHOW_SELF_SCORE
        self._settle_dict = _settle_dict
        self.my_group_list = my_group_list
        self.other_group_dict = other_group_dict
        self.my_uid = my_uid
        self._game_info = game_info
        self._game_end_ts = game_info.get('game_end_ts', None)
        self.is_show_detail = False
        self._screen_capture_helper = ScreenFrameHelper()
        self.init_settle_data_ui()
        self.init_event()
        self.check_button_status()
        return

    def on_finalize_panel(self):
        self.show_main_ui()
        global_data.ui_mgr.close_ui('DeathEndTransitionUI')
        self._settle_dict = {}
        self.all_infos = []
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
        self._screen_capture_helper = None
        super(GoldenEggEndStatisticsShareUI, self).on_finalize_panel()
        return

    def init_settle_data_ui(self):
        self.on_show_detail()
        self.init_settle_score_ui()
        self.init_game_result()

    def init_event(self):
        pass

    def check_button_status(self):
        btn_list = [
         self.panel.btn_report, self.panel.btn_comment]
        for idx, btn in enumerate(btn_list):
            if btn:
                btn.setVisible(False)

        self.panel.btn_exit.btn.SetText(get_text_by_id(80373))

    def on_show_detail(self, *args):
        if self._cur_status == GoldenEggEndStatisticsShareUI.SHOW_SELF_SCORE:
            self.panel.PlayAnimation('appear_details')
            self.panel.FastForwardToAnimationTime('appear_details', self.panel.GetAnimationMaxRunTime('appear_details'))
            self.panel.SetTimeOut(0.01, self.check_button_status)
            self._cur_status = GoldenEggEndStatisticsShareUI.SHOW_ALL_SCORE
            self.panel.StopAnimation('next')
        elif self._cur_status == GoldenEggEndStatisticsShareUI.SHOW_ALL_SCORE:
            self.close()

    def init_settle_score_ui(self):
        settle_dict = self._settle_dict
        group_dict = settle_dict.get('extra_detail', {}).get('group_info')
        my_group_id = str(settle_dict.get('my_group_id'))
        group_list = sorted(six_ex.keys(group_dict))
        if my_group_id in group_list:
            group_list.remove(my_group_id)
            group_list.insert(0, my_group_id)
        idx = 0
        group_idx_dict = {}
        for gid in group_list:
            group_idx_dict[gid] = idx
            idx += 1

        self.panel.nd_switch.setVisible(False)
        temp_data2 = self.panel.temp_data
        temp_data2.list_item.SetInitCount(len(group_dict))
        for gid in group_list:
            g_idx = group_idx_dict[gid]
            g_item = temp_data2.list_item.GetItem(g_idx)
            g_item.list_team.SetInitCount(len(group_dict[gid]))
            member_list = sorted(six_ex.keys(group_dict[gid]))
            for member_idx, soul_id in enumerate(member_list):
                ui_item = g_item.list_team.GetItem(member_idx)
                self.init_player_ui_item(ui_item, soul_id, gid, member_idx)

    def init_player_ui_item(self, item, soul_id, gid, member_idx):
        ginfo = []
        str_soul_id = str(soul_id)
        if str_soul_id in self.other_group_dict:
            ene_tuple = self.other_group_dict.get(str_soul_id, [])
            ginfo.append(ene_tuple[0])
            ginfo.append(ene_tuple[1])
            ginfo.append(ene_tuple[2])
            ginfo.append(ene_tuple[3])
            ginfo.append(ene_tuple[4])
            ginfo.append(ene_tuple[5])
            ginfo.append(ene_tuple[6])
            ginfo.append(ene_tuple[7])
        else:
            if member_idx >= len(self.my_group_list):
                log_error('no member data!!!!')
                return
            mem_tuple = self.my_group_list[member_idx]
            ginfo.append(mem_tuple[0])
            ginfo.append(mem_tuple[1])
            ginfo.append(mem_tuple[2])
            ginfo.append(mem_tuple[3])
            ginfo.append(mem_tuple[4])
            ginfo.append(mem_tuple[5])
            ginfo.append(mem_tuple[6])
            ginfo.append(mem_tuple[7])
        item.btn_like.setVisible(False)
        item.btn_report.setVisible(True)
        item.lab_name.SetString(ginfo[1])
        item.lab_kill.SetString(str(ginfo[2]))
        item.lab_mech.SetString(str(ginfo[3]))
        score = 0
        if str_soul_id in self.other_group_dict:
            score = self._settle_dict.get('extra_detail', {}).get('soul_egg_cnt_dict', {}).get(str_soul_id, 0)
        else:
            group_dict = self._settle_dict.get('extra_detail', {}).get('group_info', {})
            if gid in group_dict:
                member_dict = group_dict[gid]
                for _eid, _uid in six.iteritems(member_dict):
                    if str(_uid) == str(ginfo[0]):
                        score = self._settle_dict.get('extra_detail', {}).get('soul_egg_cnt_dict', {}).get(_eid, 0)
                        break

        item.lab_score.SetString(str(score))
        init_role_head(item.temp_role, ginfo[6], ginfo[5])

        @item.temp_role.unique_callback()
        def OnClick(btn, touch, player_uid=ginfo[0]):
            on_click_player_head(touch, player_uid)

        item.btn_like.setVisible(False)
        if ginfo[0] == str(self.my_uid):
            item.btn_add_friend.SetEnable(False)
            item.btn_report.SetEnable(False)
            item.img_self.setVisible(True)
            color = 187123
            item.lab_name.SetColor('#DB')
            item.lab_kill.SetColor(color)
            item.lab_mech.SetColor(color)
            item.lab_score.SetColor(color)
            item.lab_team.SetColor(8526)
            bar_path = 'gui/ui_res_2/battle_golden_egg/bar_golden_egg_end_blue_2.png'
            item.bar_team.SetDisplayFrameByPath('', bar_path)
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

    def init_game_result(self):
        settle_dict = self._settle_dict
        self.panel.nd_score.lab_score_blue.setVisible(False)
        self.panel.nd_score.lab_score_red.setVisible(False)
        group_dict = settle_dict.get('extra_detail', {}).get('group_round_egg_cnt_dict')
        is_draw = settle_dict.get('is_draw')
        if is_draw:
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_deuce.png')
            return
        if not group_dict:
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_fail.png')
            return
        self_score, other_score = self.get_score()
        reason = settle_dict.get('settle_reason', BATTLE_SETTLE_REASON_NORMAL)
        last_point_got_interval = settle_dict.get('last_point_got_interval', TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL)
        if self_score > other_score:
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_win.png')
        elif self_score == other_score:
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_deuce.png')
        else:
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_fail.png')

    def get_score(self):
        settle_dict = self._settle_dict
        self_group_id = settle_dict.get('my_group_id')
        group_dict = settle_dict.get('extra_detail', {}).get('group_round_egg_cnt_dict')
        self_score = group_dict.get(str(self_group_id), 0)
        other_score = None
        if self_score <= 0:
            if self_score == 0 and any([ i != 0 for i in six_ex.values(group_dict) ]):
                other_score = 1
            elif all([ i == 0 for i in six_ex.values(group_dict) ]):
                other_score = 0
        else:
            other_score = 0
        return (
         self_score, other_score)

    def on_click_share_btn(self, btn, touch):
        ui_names = [
         self.__class__.__name__, 'DeathEndTransitionUI']

        def cb(*args):
            self.panel.btn_share_1.setVisible(True)
            self.panel.nd_bottom.setVisible(True)
            self.panel.nd_btn_2.setVisible(True)

        if self._screen_capture_helper:
            self.panel.btn_share_1.setVisible(False)
            self.panel.nd_bottom.setVisible(False)
            self.panel.nd_btn_2.setVisible(False)
            self._screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=cb)

    def on_click_share_btn_2(self, btn, touch):
        ui_names = [self.__class__.__name__, 'DeathEndTransitionUI']

        def cb(*args):
            self.panel.btn_share_2.setVisible(True)
            self.panel.nd_bottom.setVisible(True)
            self.panel.nd_btn_2.setVisible(True)

        if self._screen_capture_helper:
            self.panel.btn_share_2.setVisible(False)
            self.panel.nd_bottom.setVisible(False)
            self.panel.nd_btn_2.setVisible(False)
            self._screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=cb)