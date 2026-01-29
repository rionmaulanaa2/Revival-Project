# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ffa/FFAStatisticsShareUI.py
from __future__ import absolute_import
import six_ex
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.gutils.role_head_utils import init_role_head, init_mecha_head
from common.cfg import confmgr
from logic.gcommon import time_utility
from common.const import uiconst
from logic.gutils.end_statics_utils import on_click_player_head

class FFAStatisticsShareUI(BasePanel):
    PANEL_CONFIG_NAME = 'role/role_battle_record_ffa'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_exit.btn.OnClick': '_on_exit_btn_clicked',
       'btn_share.btn.OnClick': 'on_share_btn_clicked'
       }
    SHARE_TIPS_INFO = (
     'btn_share', 3154, ('50%', '100%'))

    def on_init_panel(self, group_rank_data, my_uid, game_info=None):
        self._group_rank_data = group_rank_data if group_rank_data is not None else []
        self._my_uid = my_uid if my_uid is not None else global_data.player.uid
        self._game_info = game_info
        self._game_end_ts = game_info.get('game_end_ts', None)
        self.hide_main_ui(exceptions=['DeathEndTransitionUI'])
        self.panel.PlayAnimation('appear')
        self._screen_capture_helper = ScreenFrameHelper()
        self.statistics_1v1_widget = None
        self._init_statistics_view()
        return

    def on_finalize_panel(self):
        self.show_main_ui()
        global_data.ui_mgr.close_ui('DeathEndTransitionUI')
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
        self._screen_capture_helper = None
        super(FFAStatisticsShareUI, self).on_finalize_panel()
        return

    def _init_statistics_view(self):
        template_name_fmt = 'battle_ffa/i_score_details_{}v{}_end'
        num_per_group = 1
        self.statistics_1v1_widget = global_data.uisystem.load_template_create(template_name_fmt.format(num_per_group, num_per_group), parent=self.panel.temp_ffa)
        data = self._group_rank_data
        nd_list = self.statistics_1v1_widget.list_score
        nd_list.SetInitCount(len(data))
        for index, widget in enumerate(nd_list.GetAllItem()):
            rank, group_id, group_point, dict_data = data[index]
            is_my_group = False
            cnt = 1
            total_damage = 0
            for e_index, eid in enumerate(six_ex.keys(dict_data)):
                if cnt > 1:
                    break
                eid, uid, name, head_photo, head_frame, kill_num, kill_mecha_num, points, has_buff, mecha_id, human_damage, mecha_damage = dict_data[eid]
                total_damage += human_damage + mecha_damage
                item_nd = getattr(widget, 'nd_player_{}'.format(e_index + 1))
                nd_stat = getattr(item_nd, 'nd_stat%d' % (e_index + 1))
                if mecha_id:
                    init_mecha_head(item_nd.temp_head, head_frame, mecha_id)
                else:
                    init_role_head(item_nd.temp_head, head_frame, head_photo)
                item_nd.lab_name.SetString(name)
                nd_stat.lab_mech.SetString(str(kill_mecha_num))

                @item_nd.temp_head.unique_callback()
                def OnClick(btn, touch, player_uid=uid):
                    on_click_player_head(touch, player_uid)

                is_my = self._my_uid is not None and self._my_uid == uid
                if is_my:
                    is_my_group = True
                item_nd.lab_name.SetColor('#DB' if is_my else '#SW')
                nd_stat.lab_mech.SetColor('#DB' if is_my else '#SW')
                cnt = cnt + 1
                self._init_individual_interaction_btns(item_nd, uid, name)

            widget.lab_rank.SetString(str(rank))
            widget.lab_rank.SetColor('#SS' if is_my_group else '#SW')
            widget.lab_score.SetString(str(total_damage))
            widget.lab_score.SetColor('#DB' if is_my_group else '#SW')
            widget.nd_self.setVisible(is_my_group)
            widget.nd_1st.setVisible(rank == 1)
            widget.nd_cover.setVisible(bool(index % 2))
            widget.img_buff_dps.setVisible(False)

        return

    def _init_individual_interaction_btns(self, item_nd, uid, name):
        item_nd.btn_like.setVisible(False)
        _, y = item_nd.btn_add.GetPosition()
        item_nd.btn_add.SetPosition(760, y)
        is_self = self._my_uid is not None and self._my_uid == uid
        item_nd.btn_add.setVisible(not is_self and uid is not None)
        show_report = not is_self and uid is not None
        item_nd.btn_report.setVisible(show_report)
        if show_report and self._game_end_ts:
            report_max_interval = confmgr.get('credit_conf', 'CreditCommon', 'Content', 'settle_credit_interval', 'common_param', default=0)
            to_hide_report_time = self._game_end_ts + report_max_interval - time_utility.get_server_time()
            if to_hide_report_time > 0:

                def hide_report(btn=item_nd.btn_report):
                    btn.setVisible(False)

                item_nd.DelayCall(to_hide_report_time, hide_report)
            else:
                item_nd.btn_report.setVisible(False)
        if not is_self:

            @item_nd.btn_add.unique_callback()
            def OnClick(btn, *args):
                if uid is not None:
                    global_data.player.req_add_friend(uid)
                btn.SetEnable(False)
                btn.SetSelect(True)
                return

            @item_nd.btn_report.unique_callback()
            def OnClick(btn, *args):
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

        return

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