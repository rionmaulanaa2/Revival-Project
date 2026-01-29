# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/login/MainLoginUI.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from common.uisys.basepanel import BasePanel
from .LoginHelper import LoginHelper
from .LoginSetting import LoginSetting
from logic.gcommon.common_const.login_const import SVR_STATE_RES_MAP
from logic.comsys.feedback import echoes
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.platform.dctool import interface
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2, SecondConfirmDlg2
from common.framework import Functor
from common.platform import channel
from common.utils import package_type
from common.cfg import confmgr
import six.moves.builtins
from patch import revert
import game3d
import time
import six
SELECT_TYPE_USER_SELECT = 1
SELECT_TYPE_USER_ACCOUNT = 2
SELECT_TYPE_REGION_SELECT = 3
SELECT_TYPE_REGION_DELAY = 4
SELECT_TYPE_AUTO_RECOMANDED = 5
SELECT_TYPE_AUTO_SELECT = 6
SELECT_TYPE_UNSELECT = 7
from common.const import uiconst

class MainLoginUI(BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'login/login'
    UI_ACTION_EVENT = {'btn_login.OnClick': 'on_click_login_btn',
       'pnl_center.OnClick': 'on_click_login_bg',
       'btn_change.OnClick': 'show_game_server_list',
       'btn_right_age.OnClick': 'show_right_age_info',
       'nd_domestic.OnClick': 'show_publication_website'
       }

    def on_init_panel(self, *args, **kargs):
        self.connect_state = LoginHelper.CONNECT_SERVER_STATE_INIT
        self._count = 0
        self._select_host_num = 0
        self._select_type = SELECT_TYPE_UNSELECT
        self.init_last_logined_server()
        self.init_event()
        self.panel.img_state.SetDisplayFrameByPath('', SVR_STATE_RES_MAP[2])
        self._need_force_up_package()
        self.init_game_version()
        self.refresh_timer = 0
        self.init_gov_slogan()
        self.panel.btn_login.set_click_sound_name('login')
        self.panel.PlayAnimation('light')
        self.panel.PlayAnimation('new 1')
        self.show_tw_agreement()
        self.reverting = False
        self.btn_login_display_frames = six_ex.values(self.panel.btn_login._cur_paths)
        self.svr_ui_auto_opened = False
        show_btn_right_age = not (G_IS_NA_PROJECT or global_data.channel.is_steam_channel())
        self.panel.btn_right_age.setVisible(show_btn_right_age)
        try:
            self.panel.img_nv.setVisible(global_data.channel.get_app_channel() != 'douyin')
        except:
            log_error('failed to get app channel')

        if self._is_invalid_version():
            NormalConfirmUI2(content=get_text_by_id(635562))

    def set_reverting(self):
        self.reverting = True

    def hide_btn_text(self, flag):
        if flag:
            path_list = self.btn_login_display_frames
            if not path_list:
                path_list = [
                 None, None, None]
            self.panel.btn_login.SetFrames('', path_list, False, None)
            self.ScaleSelfNode()
            self.ResizeAndPosition()
        else:
            self.panel.btn_login.SetFrames('', [None, None, None], False, None)
        return

    def init_gov_slogan(self):
        self.panel.nd_domestic.setVisible(interface.is_mainland_package())
        channel_name = global_data.channel.get_name()
        if channel_name == 'huawei':
            text_id = 81994
        else:
            text_id = 82102
        self.panel.gov_label_2.SetString(text_id)

    def init_event(self):
        global_data.emgr.registed_account_updated_event += self.on_server_list_refresh
        global_data.emgr.on_server_list_refresh_event += self.on_server_list_refresh
        global_data.emgr.on_delay_refreshed_event += self.on_server_list_refresh
        global_data.emgr.on_tw_agreement_change_event += self.on_protocol_changed
        global_data.emgr.hide_main_login_btn_event += self.hide_btn_text
        global_data.emgr.check_first_choosing_svr_event += self.check_first_choosing_svr
        global_data.emgr.on_login_sdk_success_event += self.on_show_tw_agreement
        global_data.emgr.hide_main_login_btn_event += self.on_show_tw_agreement

    def check_first_choosing_svr(self):
        if self.svr_ui_auto_opened:
            print('check_first_choosing_svr exit because svr ui auto opened')
            return
        else:
            if self._select_type < SELECT_TYPE_REGION_DELAY:
                print('check_first_choosing_svr exit because less than SELECT_TYPE_REGION_DELAY', self._select_type, SELECT_TYPE_REGION_DELAY)
                return
            login_helper = LoginHelper()
            if login_helper.server_list_state != LoginHelper.SERVER_LIST_STATE_INITTED:
                print('check_first_choosing_svr exit because login_helper.server_list_state', login_helper.server_list_state, LoginHelper.SERVER_LIST_STATE_INITTED)
                return
            if self._select_host_num not in login_helper.host_num_server_dict:
                print('check_first_choosing_svr exit because self._select_host_num', self._select_host_num)
                return
            language_code = global_data.ui_mgr.read_lang_conf_from_setting(False)
            if language_code is None:
                print('check_first_choosing_svr exit because not language code', language_code)
                return
            self.svr_ui_auto_opened = True
            from logic.comsys.login.SvrSelectUI import SvrSelectUI
            print('open svr selectio')
            SvrSelectUI()
            return

    def _need_force_up_package(self):
        channel_name = global_data.channel.get_name()
        if not channel_name:
            return False
        if global_data.feature_mgr.is_need_force_up_package(channel_name):
            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
            text_id = 635562 if channel_name == 'fanyou' else 609600
            confirm_text_id = 860395 if channel_name == 'fanyou' else 80305

            def callback(*args):
                from logic.gutils.version_utils import open_package_update_web
                open_package_update_web(channel_name)

            NormalConfirmUI2().init_widget(content=get_text_by_id(text_id), confirm_text=confirm_text_id, on_confirm=callback)
            return True
        return False

    def _is_invalid_version(self):
        import version
        engine_ver = version.get_engine_version()
        if engine_ver in ('1.0.18110', '1.0.18112'):
            return True
        return six.PY2

    def init_game_version(self):
        import version
        content = version.get_cur_version_str()
        try:
            if G_IS_NA_USER:
                content += '(na)'
        except:
            pass

        self.panel.label_version.SetString(get_text_by_id(90006).format(content))
        if global_data.is_32bit:
            content += '(32bit)'
        else:
            content += '(64bit)'
        if global_data.is_low_mem_mode:
            content += '(low_mem)'
        if game3d.get_render_device() == game3d.DEVICE_METAL:
            content += '(metal)'
        is_release = version.get_tag() == 'release'
        if not is_release:
            content += '(branch:%s)' % version.get_tag()
        if six.PY3:
            content += '(p3)'
        else:
            content += '(p2)'
        if package_type.is_inner_package() or not is_release:
            from common.utils.time_utils import get_timezone
            content += get_timezone()
        self.panel.label_version.SetString(get_text_by_id(90006).format(content))

    def on_click_login_btn--- This code section failed: ---

 226       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_3       3 
          12  POP_JUMP_IF_FALSE    66  'to 66'

 227      15  LOAD_GLOBAL           2  'time'
          18  LOAD_ATTR             2  'time'
          21  CALL_FUNCTION_0       0 
          24  STORE_FAST            2  'cur_time'

 228      27  LOAD_FAST             2  'cur_time'
          30  LOAD_FAST             0  'self'
          33  LOAD_ATTR             3  'login_click_time'
          36  BINARY_SUBTRACT  
          37  LOAD_CONST            2  2.5
          40  COMPARE_OP            0  '<'
          43  POP_JUMP_IF_FALSE    50  'to 50'

 229      46  LOAD_CONST            0  ''
          49  RETURN_END_IF    
        50_0  COME_FROM                '43'

 231      50  LOAD_GLOBAL           4  'setattr'
          53  LOAD_GLOBAL           1  'None'
          56  LOAD_FAST             2  'cur_time'
          59  CALL_FUNCTION_3       3 
          62  POP_TOP          
          63  JUMP_FORWARD         19  'to 85'

 233      66  LOAD_GLOBAL           4  'setattr'
          69  LOAD_GLOBAL           1  'None'
          72  LOAD_GLOBAL           2  'time'
          75  LOAD_ATTR             2  'time'
          78  CALL_FUNCTION_0       0 
          81  CALL_FUNCTION_3       3 
          84  POP_TOP          
        85_0  COME_FROM                '63'

 235      85  LOAD_GLOBAL           5  'global_data'
          88  LOAD_ATTR             6  'channel'
          91  LOAD_ATTR             7  'is_guest_blocked'
          94  CALL_FUNCTION_0       0 
          97  POP_JUMP_IF_FALSE   132  'to 132'
         100  LOAD_GLOBAL           5  'global_data'
         103  LOAD_ATTR             6  'channel'
         106  LOAD_ATTR             8  'is_guest'
         109  CALL_FUNCTION_0       0 
       112_0  COME_FROM                '97'
         112  POP_JUMP_IF_FALSE   132  'to 132'

 236     115  LOAD_GLOBAL           5  'global_data'
         118  LOAD_ATTR             6  'channel'
         121  LOAD_ATTR             9  'logout'
         124  CALL_FUNCTION_0       0 
         127  POP_TOP          

 237     128  LOAD_CONST            0  ''
         131  RETURN_END_IF    
       132_0  COME_FROM                '112'

 239     132  LOAD_GLOBAL          10  'game3d'
         135  LOAD_ATTR            11  'delay_exec'
         138  LOAD_CONST            3  100
         141  LOAD_FAST             0  'self'
         144  LOAD_ATTR            12  'on_click_login_btn_delay'
         147  CALL_FUNCTION_2       2 
         150  POP_TOP          
         151  LOAD_CONST            0  ''
         154  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9

    def on_click_login_btn_delay(self):
        if global_data.game_mgr.check_need_reload_pipeline():
            return
        if revert.REVERTING:
            global_data.game_mgr.show_tip(get_text_local_content(90037))
            return
        if not self._select_host_num:
            global_data.game_mgr.show_tip(get_text_local_content(124))
            return
        if self._need_force_up_package():
            return
        channel_inst = channel.Channel()
        if not channel_inst.is_valid or channel_inst.is_sdk_login:
            self.platform_check_connect_to_server(self._select_host_num)
        else:
            global_data.emgr.request_sdk_login.emit()

    def do_connect_to_game_server(self, host_num):
        self.connect_state = LoginHelper.CONNECT_SERVER_STATE_INIT
        connect_res = LoginHelper().connect_to_game_server(host_num)
        if connect_res == LoginHelper.CONNECT_SERVER_STATE_CONNECTING:
            self.connect_state = LoginHelper.CONNECT_SERVER_STATE_CONNECTING
            LoginSetting().last_logined_server = LoginHelper().host_num_server_dict[host_num]
            global_data.emgr.on_request_login_event.emit()
        elif connect_res == LoginHelper.CONNECT_SERVER_STAET_WAITING_DATA and self._select_type == SELECT_TYPE_USER_SELECT and LoginHelper().account_state == LoginHelper.SERVER_LIST_STATE_CONNECTING:
            from logic.comsys.login.LoginAnimationUI import LoginAnimationUI
            LoginAnimationUI()
            self.connect_state = LoginHelper.CONNECT_SERVER_STAET_WAITING_DATA

    def platform_check_connect_to_server(self, host_num):
        if not global_data.is_pc_mode:
            if host_num not in LoginHelper().host_num_server_dict:
                NormalConfirmUI2(content=get_text_local_content(175))
                return
            self.try_to_connect_to_server(host_num)
        else:
            self.try_to_connect_to_server(host_num)

    def not_show_pc_server_tips(self, not_show):
        if not_show:
            global_data.achi_mgr.save_general_archive_data_value('pc_server_tips', '0')

    def try_to_connect_to_server(self, host_num):
        if self._need_show_agreement():
            if not self.is_tw_confirmed():
                self.show_protocol_confirm_ui()
                return
        emulator_limit = six.moves.builtins.__dict__.get('RUNNING_EMULATOR', False)
        if emulator_limit:
            global_data.game_mgr.show_tip(get_text_local_content(171))
            return
        device_limit = six.moves.builtins.__dict__.get('DEVICE_LIMIT', False)
        if device_limit:
            NormalConfirmUI2().init_widget(content=get_text_by_id(170))
            return
        device_warning = six.moves.builtins.__dict__.get('DEVICE_WARNING', False)
        if device_warning:
            NormalConfirmUI2(on_confirm=Functor(self.do_connect_to_game_server, host_num), content=get_text_by_id(172))
            global_data.sound_mgr.set_device_warning()
        else:
            self.do_connect_to_game_server(host_num)

    def show_server_open_time(self):
        import logic.gcommon.time_utility as tutil
        if self._select_host_num not in LoginHelper().host_num_server_dict:
            return
        server_info = LoginHelper().host_num_server_dict[self._select_host_num]
        svr_open_time = server_info['svr_open_time']
        open_date_time = tutil.time_str_to_datetime(svr_open_time, '%Y%m%d%H%M%S')
        now_utc8_time = tutil.get_utc8_datetime()

        def reset():
            from logic.gutils.ConnectHelper import ConnectHelper
            ConnectHelper().fall_back_to_server_select()

        if now_utc8_time < open_date_time:
            time_str = tutil.datetime_to_time_str(open_date_time, '%Y/%m/%d %H:%M')
            text_id = 174 if G_IS_NA_USER else 244
            tips = get_text_by_id(text_id).format(time_str)
            NormalConfirmUI2(on_confirm=reset, content=tips)
            return

    def on_click_login_bg(self, *args):
        self._count += 1

    def show_game_server_list(self, *args):
        login_helper = LoginHelper()
        if login_helper.server_list_state == LoginHelper.SERVER_LIST_STATE_INITTED:
            self.do_show_server_list_ui()
        else:
            login_helper.get_server_list(self.do_show_server_list_ui)

    def do_show_server_list_ui(self, *args):
        import world
        if LoginHelper().server_list_state == LoginHelper.SERVER_LIST_STATE_INITTED:
            scene = world.get_active_scene()
            login_com = scene.get_com('PartLogin')
            if login_com is None:
                login_com = scene.get_com('PartLogin3D')
            login_com.show_svr_list()
        return

    def show_right_age_info(self, *args):
        if G_IS_NA_PROJECT or global_data.channel.is_steam_channel():
            return
        text = 82295 if 'netease' in global_data.channel.get_name() else 82296
        ui = global_data.ui_mgr.show_ui('AnnouncementUI', 'logic.comsys.announcement')
        if ui:
            ui.show_content(82294, get_text_by_id(text))

    def init_last_logined_server(self):
        last_login_data = LoginSetting().last_logined_server
        helper = LoginHelper()
        name = None
        if last_login_data:
            self._select_host_num = last_login_data['svr_num']
            name = helper.get_svr_text_from_ext_info(last_login_data, 'svr_id') or last_login_data['svr_name']
            self._select_type = SELECT_TYPE_USER_SELECT
        self.update_last_logined_server(name)
        return

    def set_select_host_num(self, num):
        helper = LoginHelper()
        self._select_host_num = num
        LoginSetting().last_logined_server = helper.host_num_server_dict[num]
        self._select_type = SELECT_TYPE_USER_SELECT
        self.update_last_logined_server()

    def update_auto_select_server_info(self):
        helper = LoginHelper()
        if not self._select_host_num or self._select_host_num not in helper.host_num_server_dict:
            self._select_type = SELECT_TYPE_UNSELECT
        if self._select_type > SELECT_TYPE_USER_ACCOUNT:
            account_data = helper.account_data[0]
            if account_data:
                last_login_server = -1
                last_login_time = 0
                roles = account_data.get('roles', [])
                for role_info in roles:
                    login_time = role_info.get('login_time', 0)
                    login_host = role_info.get('login_host', -1)
                    if login_time >= last_login_time and login_host in helper.host_num_server_dict:
                        last_login_time = login_time
                        last_login_server = login_host

                if last_login_server != -1:
                    self._select_host_num = last_login_server
                    self._select_type = SELECT_TYPE_USER_ACCOUNT
        if channel.Channel().is_steam_channel():
            if self._select_type <= SELECT_TYPE_USER_ACCOUNT:
                return
            else:
                self._select_host_num = 0
                self._select_type = SELECT_TYPE_UNSELECT
                return

        if not interface.is_mainland_package():
            if self._select_type > SELECT_TYPE_REGION_SELECT:
                region_server_config = confmgr.get('region_server', default={})
                if region_server_config:
                    region_server_config = region_server_config.get_conf()
                    country_str = game3d.get_country_code().lower()
                    if country_str in region_server_config:
                        server_type = region_server_config[country_str]
                        server_data = helper.get_first_server_by_server_type(server_type)
                        if server_data:
                            self._select_host_num = server_data['svr_num']
                            self._select_type = SELECT_TYPE_REGION_SELECT
            if self._select_type > SELECT_TYPE_REGION_DELAY and helper.check_delay_ip_finished:
                fast_server_type = helper.get_fast_cluster()
                server_data = helper.get_first_server_by_server_type(fast_server_type)
                if server_data:
                    self._select_host_num = server_data['svr_num']
                    self._select_type = SELECT_TYPE_REGION_DELAY
        if self._select_type > SELECT_TYPE_AUTO_RECOMANDED and helper.recommend_server_list:
            self._select_host_num = helper.recommend_server_list[0]['svr_num']
            self._select_type = SELECT_TYPE_AUTO_RECOMANDED
        if self._select_type > SELECT_TYPE_AUTO_SELECT and helper.server_list:
            self._select_host_num = helper.server_list[0]['svr_num']
            self._select_type = SELECT_TYPE_AUTO_SELECT
        if self._select_type >= SELECT_TYPE_REGION_DELAY:
            ui = global_data.ui_mgr.get_ui('AnnouncementUI')
            if not ui:
                self.check_first_choosing_svr()

    def on_server_list_refresh(self, *args):
        self.update_auto_select_server_info()
        global_data.game_mgr.unregister_logic_timer(self.refresh_timer)
        self.refresh_timer = global_data.game_mgr.register_logic_timer(self.update_last_logined_server, 1, times=1)

    def update_last_logined_server(self, server_name=None):
        helper = LoginHelper()
        if server_name is None and (self._select_host_num == 0 or self._select_host_num not in helper.host_num_server_dict):
            self.display_selected_server(-1, 0)
        else:
            if server_name:
                server_state = LoginSetting().last_logined_server['svr_state']
            else:
                selected_svr = helper.host_num_server_dict[self._select_host_num]
                server_state = selected_svr['svr_state']
                server_name = helper.get_svr_text_from_ext_info(selected_svr, 'svr_id') or selected_svr['svr_name']
            self.display_selected_server(server_state, server_name)
            if self._select_host_num in helper.host_num_server_dict:
                svr_num = helper.host_num_server_dict[self._select_host_num]['svr_num']
                echoes.set_server_info('server_host', svr_num)
                echoes.set_server_info('server_name', server_name)
        if self.connect_state == LoginHelper.CONNECT_SERVER_STAET_WAITING_DATA and helper.account_state == helper.SERVER_LIST_STATE_INITTED:
            global_data.ui_mgr.close_ui('LoginAnimationUI')
            self.do_connect_to_game_server(self._select_host_num)
        return

    def display_selected_server(self, server_state=-1, server_name=None):
        self.display_selectd_server_state(server_state)
        self.display_selected_server_name(server_name)

    def display_selectd_server_state(self, server_state):
        if not self.panel:
            return
        img_state = self.panel.img_state
        if server_state < 0:
            img_state.setVisible(False)
        else:
            img_state.setVisible(True)
            img_state.SetDisplayFrameByPath('', SVR_STATE_RES_MAP.get(server_state, SVR_STATE_RES_MAP[0]))

    def display_selected_server_name(self, server_name):
        if not self.panel:
            return
        lab_server = self.panel.lab_server
        if server_name or channel.Channel().is_steam_channel():
            server_id = 609610 if 1 else 132
            lab_server.SetString(get_text_local_content(server_id))
            return
        lab_server.SetString(server_name)

    def on_show_tw_agreement(self, flag):
        if self._need_show_agreement():
            self.panel.nd_agreement.setVisible(flag)

    def _need_show_agreement(self):
        need_show_channel = ('fanyou', )
        if interface.is_tw_package() or global_data.channel.get_name() in need_show_channel:
            return True
        else:
            return False

    def show_tw_agreement(self):
        if self._need_show_agreement():
            self.panel.nd_agreement.setVisible(True)
            self.init_protocol_btn()
        else:
            self.panel.nd_agreement.setVisible(False)
            return

    def init_protocol_btn(self):
        if not interface.is_tw_package():
            self.panel.btn_read_agreement.read_txt.SetString(83399)
            self.panel.nd_agreement.agreement_txt.SetString(83398)
        self.panel.btn_agreement.EnableCustomState(True)
        self.panel.btn_agreement.BindMethod('OnClick', self.on_click_agree_btn)
        self.panel.btn_read_agreement.BindMethod('OnClick', self.on_click_read_agreement)
        self.on_protocol_changed()

    def on_click_read_agreement(self, *args):
        channel.Channel().show_compact_view()

    def is_tw_confirmed(self):
        return channel.Channel().get_protocol_state() == 1

    def show_protocol_confirm_ui(self):
        from .ProtocolConfirmUI import ProtocolConfirmUI
        ProtocolConfirmUI()

    def on_click_agree_btn(self, btn, *args):
        self.show_protocol_confirm_ui()

    def on_protocol_changed(self):
        self.panel.btn_agreement.SetSelect(channel.Channel().get_protocol_state() == 1)

    def show_publication_website(self, *args):
        from common.utils.web_browser import WebBrowser
        channels = {
         '4399com'}
        if global_data.channel.get_name() in channels:
            WebBrowser.get_instance().open_out_web('https://www.miit.gov.cn/')