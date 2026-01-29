# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/gvg/GVGStatisticsShareUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.gutils.role_head_utils import init_role_head
from common.cfg import confmgr
from logic.gcommon import time_utility
from logic.gutils.observe_utils import format_popular_num
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT
from common.const import uiconst
from logic.gutils.end_statics_utils import on_click_player_head
from logic.gcommon.common_const import battle_const

class GVGStatisticsShareUI(BasePanel):
    PANEL_CONFIG_NAME = 'role/role_battle_record_gvg'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_switch.OnClick': '_on_btn_switch_clicked',
       'btn_exit.btn.OnClick': '_on_exit_btn_clicked',
       'btn_share_2.btn.OnClick': 'on_share_btn_clicked'
       }
    SHARE_TIPS_INFO = (
     'btn_share_2', 3154, ('50%', '100%-5'))

    def on_init_panel(self, settle_detail, group_points_dict, settle_reason, game_result_info, my_group_id, my_uid, game_info=None):
        self._settle_detail = settle_detail if settle_detail is not None else {}
        self._group_points_dict = group_points_dict if group_points_dict is not None else {}
        self._settle_reason = settle_reason if settle_reason is not None else BATTLE_SETTLE_REASON_NORMAL
        self._game_result_info = game_result_info if game_result_info is not None else {}
        self._my_group_id = str(my_group_id) if my_group_id is not None else 1
        self._my_uid = my_uid if my_uid is not None else global_data.player.uid
        self._game_info = game_info
        self._game_end_ts = game_info.get('game_end_ts', None)
        self.hide_main_ui(exceptions=['DeathEndTransitionUI'])
        self.panel.PlayAnimation('appear_details')
        self.panel.FastForwardToAnimationTime('appear_details', self.panel.GetAnimationMaxRunTime('appear_details'))
        self.panel.btn_comment.setVisible(False)
        self._screen_capture_helper = ScreenFrameHelper()
        game_type = int(self._game_info.get('game_type', '4'))
        from logic.gcommon.common_utils import battle_utils
        self._play_type = battle_utils.get_play_type_by_battle_id(game_type)
        self._init_stat_view()
        self._showing_details = False
        self._refresh_stat_view()
        return

    def _refresh_stat_view(self):
        if self._showing_details:
            self.panel.btn_switch.lab_switch.SetString(get_text_by_id(80420))
            self.panel.temp_details.setVisible(True)
            self.panel.temp_data.setVisible(False)
        else:
            self.panel.btn_switch.lab_switch.SetString(get_text_by_id(81107))
            self.panel.temp_details.setVisible(False)
            self.panel.temp_data.setVisible(True)

    def on_finalize_panel(self):
        self.show_main_ui()
        global_data.ui_mgr.close_ui('DeathEndTransitionUI')
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
        self._screen_capture_helper = None
        super(GVGStatisticsShareUI, self).on_finalize_panel()
        return

    def _init_stat_view(self):
        if self._play_type in [battle_const.PLAY_TYPE_DUEL]:
            self.panel.temp_data = global_data.uisystem.re_create_item(self.panel.temp_data, root=self.panel, tmp_path='battle_duel/i_end_dule_data_base')
        enemy_group_id = None
        for _group_id in self._group_points_dict:
            if _group_id != self._my_group_id:
                enemy_group_id = _group_id
                break

        my_group_points, enemy_group_points = self._group_points_dict.get(self._my_group_id, 0), self._group_points_dict.get(enemy_group_id, 0)
        self.panel.lab_score_blue.SetString(str(my_group_points))
        self.panel.lab_score_red.SetString(str(enemy_group_points))
        if self._game_result_info.get('is_escape', False):
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_fail.png')
        elif self._game_result_info.get('is_draw', False):
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_deuce.png')
        elif self._game_result_info.get('game_rank', 100) == 1:
            if self._game_result_info.get('is_lore', False):
                self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_konckout.png')
            else:
                self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_win.png')
        else:
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_fail.png')
        self._init_group_settle_data(self._settle_detail.get(self._my_group_id, {}), self.panel.temp_data.nd_blue.list_score, self.panel.temp_details.nd_blue.list_score)
        self._init_group_settle_data(self._settle_detail.get(enemy_group_id, {}), self.panel.temp_data.nd_red.list_score, self.panel.temp_details.nd_red.list_score)
        return

    def _init_group_settle_data(self, group_data, nd_abstract_list, nd_detail_list):
        nd_abstract_list.SetInitCount(len(group_data))
        nd_detail_list.SetInitCount(len(group_data))
        for i, (eid, data) in enumerate(six.iteritems(group_data)):
            uid, name, head_frame, head_photo, kill_mecha, assist_mecha, score, mecha_data, mecha_dead_count = data
            is_self = uid == self._my_uid
            abstract_item = nd_abstract_list.GetItem(i)
            abstract_item.img_self and abstract_item.img_self.setVisible(is_self)
            init_role_head(abstract_item.temp_role, head_frame, head_photo)
            abstract_item.lab_name.SetString(name)
            abstract_item.lab_mech.SetString(str(kill_mecha))
            if self._play_type == battle_const.PLAY_TYPE_DUEL:
                pass
            else:
                abstract_item.lab_asistance.SetString(str(assist_mecha))
            if not isinstance(score, float):
                try:
                    score = float(score)
                except Exception as e:
                    score = 0.0

            abstract_item.lab_score.SetString('%.1f' % score)
            abstract_item.btn_like.setVisible(False)

            @abstract_item.temp_role.unique_callback()
            def OnClick(btn, touch, player_uid=uid):
                on_click_player_head(touch, player_uid)

            if not is_self:

                @abstract_item.btn_add_friend.unique_callback()
                def OnClick(btn, touch, _uid=uid):
                    global_data.player.req_add_friend(_uid)
                    btn.setVisible(False)

                if self._game_end_ts:
                    report_max_interval = confmgr.get('credit_conf', 'CreditCommon', 'Content', 'settle_credit_interval', 'common_param', default=0)
                    to_hide_report_time = self._game_end_ts + report_max_interval - time_utility.get_server_time()
                    if to_hide_report_time > 0:

                        def hide_report(btn=abstract_item.btn_report):
                            btn.setVisible(False)

                        abstract_item.DelayCall(to_hide_report_time, hide_report)
                        abstract_item.btn_report.setVisible(True)
                        abstract_item.btn_report.SetEnable(True)

                        @abstract_item.btn_report.unique_callback()
                        def OnClick(btn, touch, _uid=uid, _name=name):
                            from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_BATTLE_HISTORY, REPORT_CLASS_BATTLE
                            ui = global_data.ui_mgr.show_ui('UserReportUI', 'logic.comsys.report')
                            ui.report_users([{'uid': _uid,'name': _name}])
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

                    else:
                        abstract_item.btn_report.SetEnable(False)
                        abstract_item.btn_report.setVisible(False)
            else:
                abstract_item.btn_add_friend.SetEnable(False)
                abstract_item.btn_add_friend.setVisible(False)
                abstract_item.btn_report.SetEnable(False)
                abstract_item.btn_report.setVisible(False)
            detail_item = nd_detail_list.GetItem(i)
            detail_item.img_self and detail_item.img_self.setVisible(is_self)
            for j, (mecha_id, damage, kill_num) in enumerate(mecha_data):
                nd_mecha_data = detail_item.list_mech.GetItem(j)
                nd_mecha_data.temp_mech_head.img_mech_head.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/role/mech_%s.png' % str(mecha_id))
                nd_mecha_data.temp_mech_head.img_destoryed.setVisible(j < mecha_dead_count)
                nd_mecha_data.lab_harm.SetString(format_popular_num(damage))
                nd_mecha_data.lab_destory_num.SetString(str(kill_num))

            game_type = int(self._game_info.get('game_type', '4'))
            from logic.gcommon.common_utils import battle_utils
            play_type = battle_utils.get_play_type_by_battle_id(game_type)
            if play_type == battle_const.PLAY_TYPE_DUEL:
                soul_round_record_dict = self._game_info.get('extra_detail', {}).get('soul_round_record', {})
                for i, (eid, data) in enumerate(six.iteritems(group_data)):
                    uid, name, head_frame, head_photo, kill_mecha, assist_mecha, score, mecha_data, mecha_dead_count = data
                    is_self = uid == self._my_uid
                    record_list = soul_round_record_dict.get(str(eid), [-1, -1, -1])
                    from logic.entities.DuelBattle import ROUND_LOSE
                    for j, (mecha_id, damage, kill_num) in enumerate(mecha_data):
                        nd_mecha_data = detail_item.list_mech.GetItem(j)
                        if j < len(record_list):
                            nd_mecha_data.temp_mech_head.img_destoryed.setVisible(record_list[j] == ROUND_LOSE)
                        else:
                            nd_mecha_data.temp_mech_head.img_destoryed.setVisible(False)

    def _on_btn_switch_clicked(self, *argv):
        self._showing_details = not self._showing_details
        self._refresh_stat_view()

    def _on_exit_btn_clicked(self, *argv):
        self.close()

    def on_share_btn_clicked(self, *argv):
        if self._screen_capture_helper:
            ui_names = [
             self.__class__.__name__, 'DeathEndTransitionUI']

            def cb(*args):
                self.panel.nd_bottom.setVisible(True)

            self.panel.nd_bottom.setVisible(False)
            self._screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=cb)