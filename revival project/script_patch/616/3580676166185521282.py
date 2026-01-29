# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLogin.py
from __future__ import absolute_import
from __future__ import print_function
from . import ScenePart
from common.platform.channel import Channel
from logic.comsys.login.LoginHelper import LoginHelper
from common.crashhunter.crashhunter_utils import update_dump_user_info
from logic.comsys.login.MainLoginUI import MainLoginUI
from logic.comsys.login.LoginFunctionUI import LoginFunctionUI
from logic.comsys.login.LoginBgUI import LoginBgUI
from logic.comsys.login.RegionSelectUI import RegionSelectUI
from common.platform.dctool import interface
from logic.comsys.setting_ui.LanguageSettingUI import LanguageSettingUI
from common.platform import region_utils
from common.framework import Functor
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gcommon.common_const import lang_data
from logic.gutils.salog import SALog
import game3d

class PartLogin(ScenePart.ScenePart):
    ENTER_EVENT = {'request_sdk_login': 'login_channel',
       'on_server_list_refresh_event': 'on_server_list_refreshed',
       'account_request_create_usr': 'on_request_create_usr',
       'should_login_channel_event': 'should_login_channel'
       }

    def __init__(self, scene, name):
        super(PartLogin, self).__init__(scene, name)
        self.signal_count = 1
        self.cnt_signal = 0
        self.bg_music = None
        from logic.vscene import scene_type
        global_data.scene_type = scene_type.SCENE_TYPE_LOGIN
        self.should_hide_main_ui_btn = False
        self._is_need_login_channel = False
        if global_data.message_data:
            global_data.message_data.reset()
        return

    def reset_login_env(self):
        LoginHelper.finalize()
        update_dump_user_info()

    def on_enter(self):
        self.reset_login_env()
        self.init_login_env()
        global_data.sound_mgr.play_music('login')
        if global_data.is_pc_mode:
            from logic.vscene.parts.ctrl.PCCtrlManager import PCCtrlManager
            PCCtrlManager()
            from logic.gcommon.common_const import ui_operation_const as uoc
            archive_data = global_data.achi_mgr.get_general_archive_data()
            is_fullscreen = archive_data.get_field(uoc.PC_FULL_SCREEN_KEY, uoc.LOCAL_SETTING_CONF.get(uoc.PC_FULL_SCREEN_KEY))
            global_data.pc_ctrl_mgr.request_fullscreen(is_fullscreen, req_from_setting_ui=False)
            from logic.gutils.pc_resolution_utils import ensure_pc_windowed_resolution
            ensure_pc_windowed_resolution()
            global_data.pc_ctrl_mgr.enable_keyboard_control(True)

    def init_login_env(self):
        LoginHelper().get_server_list()
        is_show = self.show_oversea_init_setting()
        if not is_show:
            self.login_channel()
        self.on_enter_login_stage()

    def should_login_channel(self):
        if self._is_need_login_channel:
            self.login_channel()

    def on_request_create_usr(self):
        self.del_login_uis()
        global_data.ui_mgr.close_ui('LoginAnimationUI')

    def on_server_list_refreshed(self, *args):
        print('server list refreshed')
        channel_inst = Channel()
        if not channel_inst.is_valid or channel_inst.is_free_login or channel_inst.is_sdk_login:
            LoginHelper().get_account_data()

    def login_channel(self):
        channel_inst = Channel()
        if channel_inst.is_valid:
            channel_inst.regist_event(channel_inst.LOGIN_OK_EVENT, self.on_sdk_logined_cb)
            channel_inst.login()
            self.should_hide_main_ui_btn = True
        else:
            self.on_sdk_logined_cb()

    def on_sdk_logout_cb(self):
        LoginHelper().reset_account_data()
        update_dump_user_info()

    def on_sdk_logined_cb(self):
        channel_inst = Channel()
        channel_inst.regist_event(channel_inst.LOGOUT_EVENT, self.on_sdk_logout_cb)
        update_dump_user_info()
        helper = LoginHelper()
        if helper.server_list_state == helper.SERVER_LIST_STATE_INITTED and helper.account_state == helper.SERVER_LIST_STATE_UNINITED:
            helper.get_account_data()
        ui = global_data.ui_mgr.show_ui('AnnouncementUI', 'logic.comsys.announcement')
        if ui:
            ui.request_platform_announce()

    def show_login_ui(self):
        MainLoginUI()
        LoginFunctionUI()
        LoginBgUI()

    def show_init_language_setting_ui(self):
        ui = LanguageSettingUI()
        ui.hide_close_btn()

    def show_oversea_init_setting(self):
        if not interface.is_mainland_package():
            if global_data.ui_mgr.read_lang_conf_from_setting(False) is None:
                self.check_default_language()
                return True
            self.check_oversea_country()
        return False

    def check_default_language(self):
        local_language_code = global_data.ui_mgr.get_local_language_code(False)
        local_lang_data = lang_data.lang_data.get(local_language_code, {})
        lang_enable = local_lang_data.get('cLangEnable', 0) == 1

        def on_cancel(*args):
            self._is_need_login_channel = True
            self.show_init_language_setting_ui()

        def on_confirm(lang_code, *args):
            global_data.ui_mgr.change_lang(lang_code)

        if local_language_code is not None and lang_enable:
            context = get_text_by_id(80837, {'lang': lang_data.code_2_showname[local_language_code]})
            SecondConfirmDlg2().confirm('', context, cancel_text=80869, cancel_callback=on_cancel, confirm_callback=Functor(on_confirm, local_language_code), unique_callback=lambda : None)
        else:
            self.show_init_language_setting_ui()
        return

    def check_oversea_country(self):
        pass

    def show_svr_list(self):
        from logic.comsys.login.SvrSelectUI import SvrSelectUI
        SvrSelectUI()

    def on_exit(self):
        channel_inst = Channel()
        channel_inst.unregist_event(channel_inst.LOGIN_OK_EVENT, self.on_sdk_logined_cb)
        channel_inst.unregist_event(channel_inst.LOGOUT_EVENT, self.on_sdk_logout_cb)
        self.del_login_uis()
        from logic.comsys.login.LoginHelper import LoginHelper
        LoginHelper().finalize()
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.enable_keyboard_control(False)

    def del_login_uis(self):
        global_data.ui_mgr.close_ui('MainLoginUI')
        global_data.ui_mgr.close_ui('SvrSelectUI')
        global_data.ui_mgr.close_ui('LoginFunctionUI')
        global_data.ui_mgr.close_ui('AnnouncementUI')
        global_data.ui_mgr.close_ui('LoginBgUI')
        global_data.ui_mgr.close_ui('CharacterCreatorUINew')
        global_data.ui_mgr.close_ui('LoginAnimationUI')

    def on_enter_login_stage(self):
        self.show_login_ui()
        if self.should_hide_main_ui_btn:
            self.should_hide_main_ui_btn = False
            global_data.emgr.hide_main_login_btn_event.emit(False)