# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/EndStatisticsShareUI.py
from __future__ import absolute_import
import six
import math
import functools
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils.end_statics_utils import init_end_person_statistics_new, init_end_teammate_statistics_new
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gcommon import time_utility
from common.const import uiconst

class EndStatisticsShareUI(BasePanel):
    PANEL_CONFIG_NAME = 'role/role_battle_record_brv'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_exit.btn_major.OnClick': '_on_click_btn_exit',
       'btn_details.OnClick': '_on_click_btn_show_details',
       'nd_stat_details.btn_close.OnClick': '_on_click_btn_close_details',
       'btn_report.OnClick': '_on_click_btn_report'
       }
    SHARE_TIPS_INFO = (
     'btn_share', 3154, ('50%', '100%5'))

    def on_init_panel(self, settle_dict, teammate_num, groupmate_info, achievement, total_fighter_num, player_info, game_info=None):
        self.hide_main_ui(exceptions=['KothEndFullScreenBg'])
        self._teammate_num = teammate_num
        self._total_fighter_num = total_fighter_num
        self._game_info = game_info
        self._game_end_ts = game_info.get('game_end_ts', None)
        self_id = player_info.get('eid', None)
        self.self_id = self_id
        self_settle_dict = settle_dict.get(self_id, {})
        self._self_settle_dict = self_settle_dict
        game_type = game_info.get('game_type')
        if game_type:
            max_team_size = confmgr.get('battle_config', str(game_type), default={}).get('cTeamNum', None)
            if max_team_size:
                self._self_settle_dict['max_team_size'] = max_team_size
        self._groupmate_info = groupmate_info
        self._init_teammate(groupmate_info, settle_dict, achievement)
        self._init_statistics(teammate_num, achievement, total_fighter_num, player_info)
        self._play_animation()
        self.init_share_btn()
        self.panel.nd_stat_details.setVisible(False)
        self.panel.btn_exit.btn_major.SetText(get_text_by_id(80373))
        if not groupmate_info:
            self.panel.btn_report.setVisible(False)
        elif self._game_end_ts:
            report_max_interval = confmgr.get('credit_conf', 'CreditCommon', 'Content', 'settle_credit_interval', 'common_param', default=0)
            to_hide_report_time = self._game_end_ts + report_max_interval - time_utility.get_server_time()
            if to_hide_report_time > 0:

                def hide_report():
                    self.panel.btn_report.setVisible(False)

                self.panel.DelayCall(to_hide_report_time, hide_report)
            else:
                self.panel.btn_report.setVisible(False)
        return

    def _init_teammate(self, groupmate_info, team_settle_info, achievement):
        init_end_teammate_statistics_new(self.panel, groupmate_info, team_settle_info, achievement)

    def _init_statistics(self, teammate_num, achievement, total_fighter_num, player_info):
        init_end_person_statistics_new(self.panel, teammate_num, self._self_settle_dict, achievement, total_fighter_num, player_info)

    def _play_animation(self):
        self.panel.PlayAnimation('appear')

    def _on_click_btn_exit(self, *args):
        global_data.emgr.on_close_end_share_ui.emit()
        self.close()

    def _on_click_btn_share(self, btn, touch):
        from logic.comsys.share.EndStaticsShareCreator import EndStaticsShareCreator
        if not self._share_content:
            share_creator = EndStaticsShareCreator()
            share_creator.create(None)
            self._share_content = share_creator
        self._share_content.init_end_person_nd(self._teammate_num, self._total_fighter_num, self._self_settle_dict)
        self._share_content.update_mecha_sprite_bg()
        from logic.comsys.share.ShareUI import ShareUI
        ShareUI(parent=self.panel).set_share_content_raw(self._share_content.get_render_texture(), share_content=self._share_content)
        return

    def init_share_btn(self):
        self._share_content = None

        @self.panel.btn_share.btn_major.callback()
        def OnClick(btn, touch):
            self._on_click_btn_share(btn, touch)

        return

    def _on_click_btn_show_details(self, *args):
        self.panel.nd_stat_details.setVisible(True)

    def _on_click_btn_close_details(self, *args):
        self.panel.nd_stat_details.setVisible(False)

    def _on_click_btn_report(self, *args):
        user_info_list = []
        if self._groupmate_info:
            for uid, single_groupmate_info in six.iteritems(self._groupmate_info):
                char_name = single_groupmate_info.get('char_name', '')
                user_info_list.append({'uid': int(uid),'name': char_name})

        if not user_info_list:
            return
        from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_BATTLE_HISTORY, REPORT_CLASS_BATTLE
        ui = global_data.ui_mgr.show_ui('UserReportUI', 'logic.comsys.report')
        ui.report_users(user_info_list)
        ui.set_report_class(REPORT_CLASS_BATTLE)
        ui.set_extra_report_info('', '', REPORT_FROM_TYPE_BATTLE_HISTORY)
        ui.set_additional_report_info(self._game_info)
        if self._game_end_ts:
            report_max_interval = confmgr.get('credit_conf', 'CreditCommon', 'Content', 'settle_credit_interval', 'common_param', default=0)
            ui.set_report_ddl(self._game_end_ts + report_max_interval)

    def on_finalize_panel--- This code section failed: ---

 134       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  '_share_content'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    49  'to 49'

 135      12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  '_share_content'
          18  POP_JUMP_IF_FALSE    37  'to 37'

 136      21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             1  '_share_content'
          27  LOAD_ATTR             2  'destroy'
          30  CALL_FUNCTION_0       0 
          33  POP_TOP          
          34  JUMP_FORWARD          0  'to 37'
        37_0  COME_FROM                '34'

 137      37  LOAD_CONST            0  ''
          40  LOAD_FAST             0  'self'
          43  STORE_ATTR            1  '_share_content'
          46  JUMP_FORWARD          0  'to 49'
        49_0  COME_FROM                '46'

 138      49  LOAD_FAST             0  'self'
          52  LOAD_ATTR             4  'show_main_ui'
          55  CALL_FUNCTION_0       0 
          58  POP_TOP          

 139      59  LOAD_GLOBAL           5  'global_data'
          62  LOAD_ATTR             6  'ui_mgr'
          65  LOAD_ATTR             7  'close_ui'
          68  LOAD_CONST            2  'KothEndFullScreenBg'
          71  CALL_FUNCTION_1       1 
          74  POP_TOP          
          75  LOAD_CONST            0  ''
          78  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6