# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVELeftButtonWidget.py
from __future__ import absolute_import
from logic.gutils.client_utils import safe_call, post_ui_method, safe_widget
from logic.comsys.lobby.LobbyVoiceWidget import LobbyVoiceWidget
from logic.gcommon.common_const.friend_const import SOCIAL_ID_TYPE_LINEGAME
from logic.comsys.lobby.EntryWidget.LotterySummerPeakLiveEntryWidget import check_show_entry
from logic.comsys.message import MainFriend, AddFriend
from logic.gutils.lobby_click_interval_utils import check_click_interval
from common.platform.dctool import interface
from logic.gcommon.common_utils.local_text import get_cur_text_lang
from logic.gcommon.common_const.lang_data import LANG_ZHTW, LANG_CN, LANG_EN, LANG_JA, LANG_KO
from logic.comsys.login.LoginSetting import LoginSetting
from common.cfg import confmgr
import game3d
from logic.gcommon.common_const.liveshow_const import SUMMER_FINAL_LIVE_RED_POINT
SURVEY_TYPE = 0
SUGGEST_TYPE = 1

class PVELeftButtonWidget(object):

    def __init__(self, parent, panel):
        self.parent = parent
        self.panel = panel
        self.init_params()
        self.init_panel()
        self.init_event()
        self.init_ui_event()

    def destroy(self):
        global_data.emgr.on_add_red_packet_msg -= self.show_red_packet_vx
        global_data.emgr.on_finish_survey -= self.update_btn_survey
        if self.voice_widget:
            self.voice_widget.destroy()
            self.voice_widget = None
        self.survey_info = None
        return

    def init_params(self):
        self.survey_info = global_data.player.get_survey_info() if global_data.player else None
        return

    def init_panel(self):
        self.init_voice_widget()
        self.init_red_packet()
        self.init_linegame_node()
        self.update_btn_survey()
        self.update_rank_btn_red_point()

    def init_event(self):
        global_data.emgr.on_add_red_packet_msg += self.show_red_packet_vx
        global_data.emgr.on_finish_survey += self.update_btn_survey

    @safe_widget
    def init_voice_widget(self):
        self.voice_widget = LobbyVoiceWidget(self.parent, self.panel)

    def init_red_packet(self):
        self._red_packet_timer = None
        position = None
        if G_IS_NA_USER:
            position = 466
        else:
            position = 400
        if not self.check_show_btn_survey():
            position -= 80
        self.panel.btn_red_packet.SetPosition(position, 120)
        self.panel.btn_red_packet.setVisible(False)
        return

    def update_rank_btn_red_point(self):
        visible = False
        IS_CLICK_LOCAL_KEY = 'pve_btn_rank_red_point'
        ic_click = global_data.achi_mgr.get_cur_user_archive_data(IS_CLICK_LOCAL_KEY, False)
        if not ic_click:
            visible = True
        self.panel.btn_rank.red_point.setVisible(visible)

    @safe_call
    def init_linegame_node(self, *args):
        if not global_data.player:
            self.panel.btn_line.setVisible(False)
            return
        visible = False
        bind_line_tips = global_data.achi_mgr.get_cur_user_archive_data('bind_line_tips', default=False)
        has_rewarded = global_data.player.is_receive_social_reward(SOCIAL_ID_TYPE_LINEGAME)
        if global_data.feature_mgr.is_linegame_ready() and not global_data.channel.is_bind_linegame() and not bind_line_tips and not has_rewarded:
            visible = True
            self.panel.btn_line.red_point.setVisible(True)
        self.panel.btn_line.setVisible(visible)

    def init_ui_event(self):
        self.panel.btn_friends.BindMethod('OnClick', self.on_main_friend_ui)
        self.panel.btn_mail.BindMethod('OnClick', self.on_click_mail_btn)
        self.panel.btn_rank.BindMethod('OnClick', self.on_main_rank_ui)
        self.panel.temp_live.btn_live.BindMethod('OnClick', self.on_click_live_btn)
        self.panel.btn_line.BindMethod('OnClick', self.on_line_ui)
        self.panel.btn_red_packet.BindMethod('OnClick', self.on_click_btn_red_packet)
        self.panel.btn_survey.BindMethod('OnClick', self.on_click_survey)

    def on_main_friend_ui(self, *args):
        global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')

    def on_click_mail_btn(self, btn, touch):
        global_data.ui_mgr.show_ui('MainEmail', 'logic.comsys.message')

    @check_click_interval()
    def on_main_rank_ui(self, *args):
        IS_CLICK_LOCAL_KEY = 'pve_btn_rank_red_point'
        global_data.achi_mgr.set_cur_user_archive_data(IS_CLICK_LOCAL_KEY, True)
        self.update_rank_btn_red_point()
        global_data.ui_mgr.show_ui('MainRank', 'logic.comsys.rank')

    def on_click_live_btn(self, btn, touch):
        ui = global_data.ui_mgr.get_ui('LiveMainUI')
        if not ui:
            ui = global_data.ui_mgr.show_ui('LiveMainUI', 'logic.comsys.live')
        ui.show()
        if check_show_entry():
            global_data.achi_mgr.set_cur_user_archive_data(SUMMER_FINAL_LIVE_RED_POINT + str(global_data.player.uid), True)
            self.panel.temp_live.red_point.setVisible(False)

    def on_line_ui(self, *args):
        if G_IS_NA_USER:
            global_data.achi_mgr.set_cur_user_archive_data('bind_line_tips', True)
            self.init_linegame_node()
            MainFriend.MainFriend(None, init_tab_index=MainFriend.FRIEND_TAB_ADDFRIEND, init_sub_tab_index=AddFriend.RECOMMEND_TAB_PLATFORM)
        elif global_data.player:
            data = {'methodId': 'ntOpenGMPage','refer': '/sprite/index'
               }
            global_data.channel.extend_func_by_dict(data)
        return

    def on_click_btn_red_packet(self, btn, touch):
        ui = global_data.ui_mgr.get_ui('MainChat')
        if ui:
            ui.show_main_chat_ui()
        self.hide_red_packet_vx()

    def show_red_packet_vx(self, red_packet_info):
        self.panel.PlayAnimation('hongbaorukou_loop')
        self.panel.btn_red_packet.setVisible(True)
        if self._red_packet_timer:
            global_data.game_mgr.unregister_logic_timer(self._red_packet_timer)
        global_data.game_mgr.register_logic_timer(self.hide_red_packet_vx, interval=6, times=1, mode=2)

    def hide_red_packet_vx(self):
        if not self.panel or not self.panel.isValid():
            return
        self.panel.StopAnimation('hongbaorukou_loop')
        self.panel.btn_red_packet.setVisible(False)

    def check_show_btn_survey(self):
        state = self.check_survey_type()
        if state == SURVEY_TYPE:
            if interface.is_tw_package():
                return False
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                return False
            if not self.survey_info or 'cSurveyID' not in self.survey_info:
                return False
            survey_id = str(self.survey_info.get('cSurveyID', 0))
            survey_data = confmgr.get('survey_info', survey_id, default={})
            if survey_data.get('is_show_on_lobby', 0) == 1:
                return False
            return True
        if state == SUGGEST_TYPE:
            return interface.is_mainland_package()

    def update_btn_survey(self):
        is_show_btn = self.check_show_btn_survey()
        self.panel.btn_survey.setVisible(is_show_btn)
        if is_show_btn:
            state = self.check_survey_type()
            if state == SURVEY_TYPE:
                self.panel.lab_btn.setString(get_text_by_id(860297))
            elif state == SUGGEST_TYPE:
                self.panel.lab_btn.setString(get_text_by_id(860311))

    def on_click_survey(self, *args):
        state = self.check_survey_type()
        if state == SURVEY_TYPE:
            self.on_click_survey_type()
        elif state == SUGGEST_TYPE:
            self.on_click_opinion_type()

    def check_survey_type(self):
        period_id = global_data.player and global_data.player.get_pve_suggest_is_open()
        if period_id:
            return SUGGEST_TYPE
        else:
            return SURVEY_TYPE

    def on_click_survey_type(self):
        import datetime
        if not self.check_show_btn_survey():
            return
        if not self.survey_info or 'cSurveyID' not in self.survey_info:
            return
        survey_id = str(self.survey_info['cSurveyID'])
        url = self._get_survey_url(self.survey_info)
        if not url:
            return
        survey_data = confmgr.get('survey_info', survey_id, default={})
        if survey_data.get('is_show_on_lobby', 0) == 1:
            return False
        aid = global_data.channel.get_prop_str('USERINFO_AID')
        aid = aid if aid else '0'
        aid_str = '?uid=%s' % str(aid)
        rold_id_str = '&role_id=%s' % str(global_data.player.uid)
        server_info = LoginSetting().last_logined_server or {}
        user_server = server_info.get('svr_name', '0')
        server_str = '&server=%s' % user_server
        url = url + aid_str + rold_id_str + server_str

        def callback(status, param):
            if status.endswith('close'):
                return
            if not global_data.player:
                return
            global_data.player.do_commit_survey_finish(survey_id)
            if not self.panel:
                return

        global_data.channel.open_survey(url, callback)
        import time
        survey_btn_data = global_data.achi_mgr.get_cur_user_archive_data('survey_btn', default={})
        survey_btn_data[survey_id] = int(time.time())
        global_data.achi_mgr.set_cur_user_archive_data('survey_btn', survey_btn_data)

    def _get_survey_url(self, survey_info):
        survey_id = str(survey_info.get('cSurveyID', 0))
        country_ip = survey_info.get('country', None)
        survey_data = confmgr.get('survey_info', survey_id)
        if not survey_data:
            return
        else:
            url = None
            if country_ip and country_ip in survey_data:
                url = survey_data[country_ip]
            else:
                cur_text_lang = get_cur_text_lang()
                lang_dict = {LANG_CN: 'cCN',LANG_EN: 'cEN',LANG_ZHTW: 'cZHTW',LANG_JA: 'cJP',LANG_KO: 'cKO'}
                url = survey_data[lang_dict.get(cur_text_lang, 'cEN')]
            return url

    def on_click_opinion_type(self):
        global_data.ui_mgr.show_ui('PVESuggestUI', 'logic.comsys.battle.pve.PVEMainUIWidgetUI')