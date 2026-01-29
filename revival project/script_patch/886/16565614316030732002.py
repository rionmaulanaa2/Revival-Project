# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyMoreListPanelWidget.py
from __future__ import absolute_import
from __future__ import print_function
import cc
import collision
from logic.comsys.login.LoginSetting import LoginSetting
from common.platform.dctool import interface
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_cur_text_lang
from logic.gcommon.common_const.lang_data import LANG_ZHTW, LANG_CN, LANG_EN, LANG_JA, LANG_KO
import game3d
from logic.gutils import dress_utils
from logic.gutils import lobby_model_display_utils
from logic.gutils.lobby_click_interval_utils import check_click_interval

class LobbyMoreListPanelWidget(object):

    def init(self):
        self.survey_info = global_data.player.get_survey_info()
        self.init_survey()
        self.init_list_more()
        self.hide_widget()

    def __init__(self, parent_ui, panel):
        self.panel = panel.list_more_panel
        self.parent_ui = parent_ui
        self.init()

    def destroy(self):
        self.panel = None
        self.parent_ui = None
        return

    def init_survey(self, *args):
        self.survey_info = global_data.player.get_survey_info()
        if not self._get_survey_url(self.survey_info):
            self.survey_info = {}

    def is_need_show_btn_questionair(self):
        if interface.is_tw_package():
            return False
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            return False
        if not self.survey_info or 'cSurveyID' not in self.survey_info:
            return
        survey_id = str(self.survey_info.get('cSurveyID', 0))
        survey_data = confmgr.get('survey_info', survey_id, default={})
        if survey_data.get('is_show_on_lobby', 0) == 0:
            return
        return True

    def need_btn_questionair_red_point(self):
        if global_data.player.get_lv() < 4:
            return False
        if self.survey_info and 'cSurveyID' in self.survey_info:
            survey_id = str(self.survey_info['cSurveyID'])
            survey_data = confmgr.get('survey_info', survey_id, default={})
            if survey_data.get('is_show_on_lobby', 0) == 0:
                return False
            survey_btn_data = global_data.achi_mgr.get_cur_user_archive_data('survey_btn', default={})
            if not survey_btn_data.get(survey_id, 0):
                return True
        return False

    def on_survey(self, *args):
        import datetime
        btn_questionair = self.get_small_btn_by_tag('btn_questionair')
        if not btn_questionair:
            return
        btn_questionair.red_point.setVisible(False)
        if not self.survey_info or 'cSurveyID' not in self.survey_info:
            return
        survey_id = str(self.survey_info['cSurveyID'])
        survey_data = confmgr.get('survey_info', survey_id, default={})
        if survey_data.get('is_show_on_lobby', 0) == 0:
            return
        url = self._get_survey_url(self.survey_info)
        if not url:
            return
        aid = global_data.channel.get_prop_str('USERINFO_AID')
        aid = aid if aid else '0'
        aid_str = '?uid=%s' % str(aid)
        rold_id_str = '&role_id=%s' % str(global_data.player.uid)
        server_info = LoginSetting().last_logined_server or {}
        userServer = server_info.get('svr_name', '0')
        server_str = '&server=%s' % userServer
        url = url + aid_str + rold_id_str + server_str

        def callback(status, param):
            if status.endswith('close'):
                return
            if not global_data.player:
                return
            global_data.player.do_commit_survey_finish(survey_id)
            if not self.panel:
                return
            btn_questionair = self.get_small_btn_by_tag('btn_questionair')
            if not btn_questionair:
                return
            btn_questionair.red_point.setVisible(False)

        global_data.channel.open_survey(url, callback)
        import time
        survey_btn_data = global_data.achi_mgr.get_cur_user_archive_data('survey_btn', default={})
        survey_btn_data[survey_id] = int(time.time())
        global_data.achi_mgr.set_cur_user_archive_data('survey_btn', survey_btn_data)
        self.update_list_more_red_point()

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

    def on_view_mode_change(self, btn, touch):
        lobby_player = global_data.lobby_player
        if not lobby_player:
            return
        is_free = lobby_player.ev_g_is_free_camera()
        is_celebrate = lobby_player.ev_g_is_celebrate()
        if is_free and not is_celebrate:
            global_data.emgr.enable_lobby_player_free_cam.emit(False)
            btn.SetSelect(False)
            global_data.ui_mgr.close_ui('LobbySceneOnlyUI')
        else:
            global_data.emgr.enable_lobby_player_free_cam.emit(True)
            btn.SetSelect(True)
            from logic.comsys.share.LobbySceneOnlyUI import LobbySceneOnlyUI
            LobbySceneOnlyUI()

    def init_view_mode_selection(self, *args):
        btn = self.get_small_btn_by_tag('btn_view')
        if not btn:
            return
        lobby_player = global_data.lobby_player
        if not lobby_player:
            return
        btn.btn_lobby_more.SetSelect(False)

    def on_click_naver_cafe_btn(self, btn, touch):
        from logic.comsys.share.NaverCafeManager import NaverCafeManager
        NaverCafeManager().open_community_homepage()

    def on_click_ar(self, btn, touch):
        try:
            import ar
        except:
            ui = global_data.ui_mgr.show_ui('UpdateGameConfirmUI', 'logic.comsys.lobby')
            return

        try:
            import ar
            if not ar.is_support_ar():
                global_data.game_mgr.show_tip(get_text_by_id(609393))
                return
        except:
            pass

        if global_data.player and global_data.player.get_self_ready() or global_data.player.is_matching or global_data.player.get_battle():
            global_data.game_mgr.show_tip(get_text_by_id(12097))
            return
        cur_use_mecha_id = global_data.emgr.lobby_cur_mecha_id.emit()[0]
        from logic.comsys.ar.MechaARMainUI1 import IGNORE_MECHA_IDS
        if cur_use_mecha_id in IGNORE_MECHA_IDS:
            global_data.game_mgr.show_tip(get_text_by_id(80715))
            return
        cur_use_mecha_clothing_id = global_data.emgr.lobby_cur_mecha_clothing_id.emit()[0]
        cur_use_mecha_shiny_weapon_id = global_data.emgr.lobby_cur_mecha_shiny_weapon_id.emit()[0]
        global_data.ui_mgr.show_ui('MechaARMainUI1', 'logic.comsys.ar')
        ui = global_data.ui_mgr.get_ui('MechaARMainUI1')
        if ui:
            item_no = dress_utils.get_mecha_skin_item_no(cur_use_mecha_id, cur_use_mecha_clothing_id)
            res_path = dress_utils.get_mecha_model_path(cur_use_mecha_id, cur_use_mecha_clothing_id)
            mesh_path = dress_utils.get_mecha_model_h_path(cur_use_mecha_id, cur_use_mecha_clothing_id)
            display_model_info = {'model_path': res_path,'sub_mesh_path_list': [mesh_path]}
            print(('test--on_click_ar--step3--mecha_id =', cur_use_mecha_id, '--mecha_clothing_id =', cur_use_mecha_clothing_id, '--shiny_weapon_id =', cur_use_mecha_shiny_weapon_id))
            ui.init_model_data(display_model_info, cur_use_mecha_id, cur_use_mecha_clothing_id, cur_use_mecha_shiny_weapon_id)

    def init_list_more(self):
        from logic.gutils.third_party_sdk_utils import check_need_show_naver_cafe
        small_btn_list = ['btn_questionair', 'btn_view', 'btn_naver_cafe', 'btn_ar']
        self.small_btn_settings = {'btn_questionair': {'img': ['gui/ui_res_2/main/icon_btn_questionnaire.png',
                                     'gui/ui_res_2/main/icon_btn_questionnaire.png'],
                               'func': self.on_survey,
                               'check_func': self.is_need_show_btn_questionair,
                               'red_point_func': self.need_btn_questionair_red_point
                               },
           'btn_view': {'img': ['gui/ui_res_2/main/btn_view_0.png',
                              'gui/ui_res_2/main/btn_view_2.png'],
                        'func': self.on_view_mode_change,
                        'init_func': self.init_view_mode_selection
                        },
           'btn_naver_cafe': {'img': ['gui/ui_res_2/main/icon_btn_naver.png',
                                    'gui/ui_res_2/main/icon_btn_naver.png'],
                              'func': self.on_click_naver_cafe_btn,
                              'check_func': check_need_show_naver_cafe
                              },
           'btn_ar': {'img': ['gui/ui_res_2/main/icon_btn_ar.png',
                            'gui/ui_res_2/main/icon_btn_ar.png'],
                      'func': self.on_click_ar,
                      'check_func': self.need_show_ar
                      }
           }
        self.small_final_list = self._get_show_button_list(small_btn_list, self.small_btn_settings)
        self._init_small_show_button(self.small_final_list, self.small_btn_settings)
        self.update_list_more_red_point()
        self.panel.bg_list_more.SetContentSize(*self.panel.list_more.GetContentSize())

    def need_show_ar(self):
        return False

    def update_list_more_red_point(self):
        has_red_point = False
        for btn_name in self.small_final_list:
            btn_setting = self.small_btn_settings.get(btn_name)
            red_point_func = btn_setting.get('red_point_func', None)
            if red_point_func:
                has_red_point = has_red_point or red_point_func()
            if has_red_point:
                break

        self.parent_ui.panel.btn_more.red_point.setVisible(has_red_point)
        return

    def _get_show_button_list(self, btn_show_list, btn_show_settings):
        final_show_list = []
        for btn in btn_show_list:
            btn_show_setting = btn_show_settings.get(btn)
            if btn_show_setting:
                check_func = btn_show_setting.get('check_func')
                if check_func and not check_func():
                    continue
                final_show_list.append(btn)

        return final_show_list

    def _init_small_show_button(self, show_list, btn_settings):
        self.panel.list_more.SetInitCount(len(show_list))
        all_item = self.panel.list_more.GetAllItem()
        for idx, ui_item in enumerate(all_item):
            btn_name = show_list[idx]
            ui_item.btn_name = btn_name
            btn_set = btn_settings.get(btn_name)
            if not btn_set:
                ui_item.setVisible(False)
            else:
                ui_item.red_point.setVisible(False)
                img_list = btn_set.get('img', [])
                func = btn_set.get('func')
                init_func = btn_set.get('init_func')
                red_point_func = btn_set.get('red_point_func', None)
                has_red_point = False
                if red_point_func:
                    has_red_point = red_point_func()
                ui_item.red_point.setVisible(has_red_point)
                ui_item.btn_lobby_more.SetFrames('', img_list, False, None)
                if init_func:
                    init_func(ui_item)

                @check_click_interval()
                def OnClick(btn, touch, ui_item=ui_item, func=func):
                    func(btn, touch)

                ui_item.btn_lobby_more.BindMethod('OnClick', OnClick)

        return

    def get_small_btn_by_tag(self, btn_name):
        all_item = self.panel.list_more.GetAllItem()
        for idx, ui_item in enumerate(all_item):
            if ui_item and hasattr(ui_item, 'btn_name') and ui_item.btn_name == btn_name:
                return ui_item

        return None

    def show_widget(self):
        self.panel.setVisible(True)
        global_data.ui_mgr.hide_all_ui_by_key('LobbyMoreListPanelWidget', ['MainChat'])

    def hide_widget(self):
        self.panel.setVisible(False)
        global_data.ui_mgr.revert_hide_all_ui_by_key_action('LobbyMoreListPanelWidget', ['MainChat'])