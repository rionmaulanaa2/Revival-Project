# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/SnatchEgg/SnatchEggEndStatisticsUI.py
from __future__ import absolute_import
import six_ex
from logic.comsys.battle.Settle.EndSceneUIBase import EndSceneUIBase
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import statistics_const as stat_const
from logic.gutils.role_head_utils import init_role_head, get_role_default_photo, get_mecha_photo
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL
from logic.gcommon.common_const.battle_const import PLAY_TYPE_DEATH
from logic.gutils.new_template_utils import ModeSatSurveyButtonWidget
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.gutils.settle_scene_utils import *
from logic.comsys.battle.Settle.GenericSettleWidgets import SettleInputWidget, SettleNameWidget, SettleInteractionWidget
from logic.gutils.item_utils import get_lobby_item_type
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_EMOTICON, L_ITEM_TYPE_GESTURE
from logic.gcommon.common_const.scene_const import SCENE_NORMAL_SETTLE, SCENE_NIGHT_SETTLE
from logic.gcommon.common_utils import battle_utils
from common.cfg import confmgr
from logic.gcommon.cdata.round_competition import check_is_in_competition_battle
from logic.comsys.battle.Death.DeathEndStatisticsUI import DeathStatisticsUI
from common.const import uiconst
hide_ui_list = [
 'SnatchEggTopScoreUI', 'FFABeginCountDown', 'FFAFinishCountDown', 'DeathWeaponChooseBtn', 'GoldenEggThrowUI', 'SnatchEggGuideUI', 'ParachuteInfoUI', 'EggMarkUI', 'MainSettingUI', 'SnatchEggPromoteUI']

class SnatchEggEndStatisticsUI(DeathStatisticsUI):

    def on_init_panel(self, group_num, settle_dict, reward, teammate_num, teaminfo, enemy_info, achievenment):
        super(SnatchEggEndStatisticsUI, self).on_init_panel(group_num, settle_dict, reward, teammate_num, teaminfo, enemy_info, achievenment)
        global_data.ui_mgr.add_blocking_ui_list(hide_ui_list, 'egg_settle')

    def on_finalize_panel(self):
        super(SnatchEggEndStatisticsUI, self).on_finalize_panel()
        global_data.ui_mgr.remove_blocking_ui_list(hide_ui_list, 'egg_settle')

    def on_click_btn_switch(self, *args):
        pass

    def on_report_user(self, btn, *args):
        if self.interaction_widget.selecting_emote:
            return
        flag = not btn.GetSelect()
        btn.SetSelect(flag)
        if flag and self.is_show_detail:
            self.on_click_btn_switch()
        if flag:
            anim_name = 'show_report' if 1 else 'disappear_report'
            return self.panel.nd_2.temp_data2 or None
        list_scores = [ nd.list_team for nd in self.panel.nd_2.temp_data2.list_item.GetAllItem() ]
        for list_score in list_scores:
            for item in list_score.GetAllItem():
                item.PlayAnimation(anim_name)
                if item != self._avatar_item:
                    is_ob_settle = self._is_ob_settle()
                    item.btn_add_friend.setVisible(not flag and not is_ob_settle)
                    item.btn_like.setVisible(not flag and not is_ob_settle)
                    item.btn_report.setVisible(flag and not is_ob_settle)

        if not self.showing_settle_data and flag:
            self.on_click_btn_hide()

    def init_settle_score_ui(self):
        self.group_dict = global_data.battle.get_group_loading_dict()
        idx = 0
        self.group_idx_dict = {}
        group_list = global_data.battle.get_show_group_list()
        for gid in group_list:
            self.group_idx_dict[gid] = idx
            idx += 1

        self.panel.temp_data.setVisible(False)
        self.panel.nd_switch.setVisible(False)
        temp_data2 = global_data.uisystem.load_template_create('battle_golden_egg/i_battle_golden_egg_end_data', parent=self.panel.nd_2, name='temp_data2')
        temp_data2.list_item.SetInitCount(len(self.group_dict))
        for gid in group_list:
            g_idx = self.group_idx_dict[gid]
            g_item = temp_data2.list_item.GetItem(g_idx)
            g_item.list_team.SetInitCount(len(six_ex.keys(self.group_dict[gid])))
            for idx, soul_id in enumerate(sorted(six_ex.keys(self.group_dict[gid]))):
                ui_item = g_item.list_team.GetItem(idx)
                self.init_player_ui_item(ui_item, soul_id)

    def _get_self_head_photo(self):
        if self._is_ob_settle():
            eid = self._get_self_eid()
            if eid:
                return self.teammate_info.get(eid, {}).get('head_photo', 0)
            else:
                return 0

        else:
            return global_data.player.get_head_photo()

    def init_player_ui_item(self, item, soul_id):
        ginfo = []
        str_soul_id = str(soul_id)
        if soul_id in self.teammate_info:
            dic = self.teammate_info.get(soul_id, {})
            ginfo.append(dic.get('uid', ''))
            ginfo.append(dic.get('char_name', ''))
            ginfo.append(dic.get('statistics', {}).get('kill', 0))
            ginfo.append(dic.get('statistics', {}).get('kill_mecha', 0))
            ginfo.append(0)
            ginfo.append(dic.get('head_photo', 0))
            ginfo.append(dic.get('head_frame', 0))
            ginfo.append(soul_id)
        elif str_soul_id in self._enemy_info:
            dic = self._enemy_info.get(str_soul_id, {})
            ginfo.append(dic.get('uid', ''))
            ginfo.append(dic.get('char_name', ''))
            ginfo.append(dic.get('statistics', {}).get('kill', 0))
            ginfo.append(dic.get('statistics', {}).get('kill_mecha', 0))
            ginfo.append(0)
            ginfo.append(dic.get('head_photo', 0))
            ginfo.append(dic.get('head_frame', 0))
            ginfo.append(soul_id)
        elif soul_id == self._get_self_eid():
            ginfo.append(self._get_self_uid())
            ginfo.append(self._get_self_name())
            if not self._is_ob_settle():
                settle_dict = self._settle_dict
                self_statis = settle_dict.get('statistics', {})
                ginfo.append(self_statis.get('kill', 0))
                ginfo.append(self_statis.get('kill_mecha', 0))
            else:
                dic = self.teammate_info
                ginfo.append(dic.get('statistics', {}).get('kill', 0))
                ginfo.append(dic.get('statistics', {}).get('kill_mecha', 0))
            ginfo.append(0)
            ginfo.append(self._get_self_head_photo())
            ginfo.append(self._get_self_head_frame())
            ginfo.append(soul_id)
        else:
            log_error('can not find info for id %s' % str(soul_id))
            return
        item.lab_name.SetString(ginfo[1])
        item.lab_kill.SetString(str(ginfo[2]))
        item.lab_mech.SetString(str(ginfo[3]))
        score = self._settle_dict.get('extra_detail', {}).get('soul_egg_cnt_dict', {}).get(str_soul_id, 0)
        item.lab_score.SetString(str(score))
        init_role_head(item.temp_role, ginfo[6], ginfo[5])
        battle = global_data.battle
        settle_likenum_dict = battle.settle_likenum_dict
        if ginfo[7] in settle_likenum_dict:
            item.lab_num.SetString(str(settle_likenum_dict[ginfo[7]]))
            item.lab_num.setVisible(True)
        else:
            item.lab_num.setVisible(False)
        item.btn_report.setVisible(False)
        if ginfo[0] == self._get_self_uid():
            self._avatar_item = item
            self._eid_to_like_lab[ginfo[7]] = item.lab_num_big
            item.btn_add_friend.SetEnable(False)
            item.btn_add_friend.setVisible(False)
            item.btn_like.SetEnable(False)
            item.btn_like.setVisible(False)
            item.btn_report.SetEnable(False)
            item.btn_report.setVisible(False)
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
            self._eid_to_like_lab[ginfo[7]] = item.lab_num
            if global_data.message_data.is_friend(ginfo[0]):
                item.btn_add_friend.setVisible(False)
            else:

                @item.btn_add_friend.callback()
                def OnClick(btn, touch, uid=ginfo[0]):
                    global_data.player.req_add_friend(uid)
                    btn.SetSelect(True)
                    btn.SetEnable(False)

            @item.btn_report.callback()
            def OnClick(btn, touch, uid=ginfo[0], name=ginfo[1], eid=ginfo[7]):
                from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_BATTLE_END, REPORT_CLASS_BATTLE
                if check_is_in_competition_battle():
                    ui = global_data.ui_mgr.show_ui('RoundCompetitionReportUI', 'logic.comsys.report')
                    ui.report_battle_users([{'eid': eid,'name': name}], False, False)
                    ui.set_report_class(REPORT_CLASS_BATTLE)
                    ui.set_extra_report_info('', '', REPORT_FROM_TYPE_BATTLE_END)
                    ui.set_settle_info(self._settle_dict)
                else:
                    ui = global_data.ui_mgr.show_ui('UserReportUI', 'logic.comsys.report')
                    ui.report_battle_users([{'eid': eid,'name': name}], True, True)
                    ui.set_report_class(REPORT_CLASS_BATTLE)
                    ui.set_extra_report_info('', '', REPORT_FROM_TYPE_BATTLE_END)
                    ui.set_settle_info(self._settle_dict)
                btn.SetSelect(True)
                btn.SetEnable(False)

                def cancel_report():
                    btn.SetSelect(False)
                    btn.SetEnable(True)

                ui.set_close_callback(cancel_report)

            @item.btn_like.callback()
            def OnClick(btn, touch, eid=ginfo[7]):
                if not btn.GetSelect():
                    if btn.lab_num.isVisible():
                        btn.lab_num_big.SetString(btn.lab_num.GetString())
                        btn.lab_num.setVisible(False)
                    self._eid_to_like_lab[eid] = btn.lab_num_big
                    global_data.player.like_player_after_settle(eid)
                    btn.SetEnable(False)
                    btn.SetSelect(True)
                    btn.img_like_star.setVisible(True)

        if self._is_ob_settle():
            item.btn_add_friend.setVisible(False)
            item.btn_like.setVisible(False)
            item.btn_report.setVisible(False)

    def _get_self_group_id(self):
        if self._is_ob_settle():
            return self._settle_dict.get('ob_data', {}).get('watching_group_id', None)
        else:
            self_group_id = global_data.player.logic.ev_g_group_id(exclude_observe=True)
            return self_group_id
            return None

    def get_score(self):
        settle_dict = self._settle_dict
        self_group_id = self._get_self_group_id()
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