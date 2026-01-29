# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/ClientAccount.py
from __future__ import absolute_import
import math
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Str, Bool, Dict, Uuid, Float
from logic.entities.BaseClientAvatar import BaseClientAvatar
from logic.gcommon.common_utils.local_text import get_text_by_id, get_cur_text_lang
from logic.gcommon import time_utility as tutil
from logic.comsys.login.LoginSetting import LoginSetting
from common.platform.appsflyer import Appsflyer
from common.platform.appsflyer_const import AF_LOGIN, AF_LOGIN_WEEK
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from mobile.common.IdManager import IdManager

class ClientAccount(BaseClientAvatar):

    def __init__(self, entityid=None):
        super(ClientAccount, self).__init__(entityid)
        global_data.connect_helper.clean_service_cache()
        self._is_reconnect = global_data.connect_helper.is_login_reconnect()
        self.cdkey_callback = lambda success: False

    def init_from_dict(self, bdict):
        super(ClientAccount, self).init_from_dict(bdict)
        global_data.is_nglbs_test = bdict.get('nglbs_test', False)
        global_data.is_inner_server = bdict.get('inner_server_type', 0)
        global_data.enable_oodle = bdict.get('enable_oodle', False)
        import version
        import render
        global_data.enable_meadow = bdict.get('enable_grass', False) and global_data.feature_mgr.is_support_meadow()
        if bdict.get('enable_nile', False):
            if not global_data.nile_sdk:
                from common.platform.nile_sdk import NileSDK
                NileSDK()

    def on_become_player(self):
        global_data.owner_entity = self
        global_data.player = None
        log_error('AAA ClientAccout on_become_player', global_data.player)
        super(ClientAccount, self).on_become_player()
        self.account_login()
        return

    @rpc_method(CLIENT_STUB, (Int('queue_time'),))
    def queue_login(self, queue_time):
        from logic.comsys.login.LoginQueueUI import LoginQueueUI
        if queue_time <= tutil.ONE_HOUR_SECONS:
            minute = math.ceil(float(queue_time) / tutil.ONE_MINUTE_SECONDS)
            time_str = get_text_by_id(3114, {'time': get_text_by_id(165).format(str(int(minute)))})
        else:
            time_str = get_text_by_id(3114, {'time': get_text_by_id(3116)})
        LoginQueueUI(on_confirm=self.change_to_login, content=time_str)

    def account_login(self):
        import version
        username = global_data.channel.get_login_name()
        if username is None:
            self.restart_client()
            return
        else:
            game_version = version.get_cur_version_str()
            game_tag = version.get_tag()
            login_host = global_data.connect_helper.get_host()
            platform = global_data.channel.get_platform()
            is_emulator = global_data.deviceinfo.is_emulator()
            self.server.call_server_method('account_login', (username, game_version, game_tag, self._is_reconnect, platform, login_host, is_emulator))
            return

    @rpc_method(CLIENT_STUB, ())
    def channel_login(self):
        global_data.ui_mgr.close_ui('LoginQueueUI')
        username = global_data.channel.get_login_name()
        old_username = global_data.channel.get_old_login_name()
        if username is None:
            self.restart_client()
            return
        else:
            activation = LoginSetting().first_logined_server
            if not activation:
                LoginSetting().first_logined_server = True
            login_host = global_data.connect_helper.get_host()
            sauth_info = global_data.channel.get_sauth_info()
            device_info = global_data.deviceinfo.get_device_info()
            device_info['ab_test'] = G_CLIENT_ABTEST
            device_info['lang'] = get_cur_text_lang()
            self.server.call_server_method('channel_login', (username, old_username, login_host, self._is_reconnect, sauth_info, device_info, activation))
            global_data.deviceinfo.drop_tpa_launch_data()
            return

    @rpc_method(CLIENT_STUB, ())
    def channel_relogin(self):
        global_data.channel.regist_event(global_data.channel.LOGIN_OK_EVENT, lambda : self.channel_login(()))
        global_data.channel.relogin()

    @rpc_method(CLIENT_STUB, (Int('hostnum'), Str('aid'), Str('unisdk_login_json'), Int('login_host'), Int('region_id'), Int('uid_prefix'), Str('hosttag')))
    def channel_verify_success(self, hostnum, aid, unisdk_login_json, login_host, region_id, uid_prefix, hosttag):
        global_data.channel.verfiy_success(hostnum, aid, unisdk_login_json, login_host, region_id, hosttag)
        global_data.uid_prefix = uid_prefix
        Appsflyer().advert_track_event(AF_LOGIN)
        Appsflyer().advert_track_event(AF_LOGIN_WEEK)
        global_data.channel.set_fee_env(not global_data.is_inner_server)
        global_data.channel.init_channel_params(not global_data.is_inner_server)
        from logic.gutils.salog import SALog
        salog_writer = SALog.get_instance()
        salog_writer.write(SALog.SUCCESS_AUTH_TYPE)

    @rpc_method(CLIENT_STUB, ())
    def check_client_version(self):
        NormalConfirmUI2(on_confirm=self.restart_client).set_content_string(get_text_by_id(166))

    @rpc_method(CLIENT_STUB, (Int('err_code'), Dict('args')))
    def login_fail(self, err_code, args):
        from logic.gcommon.time_utility import get_date_str
        if 'id_reason' in args:
            args['id_reason'] = get_text_by_id(args['id_reason'])
        if 'timelen' in args:
            if args['timelen'] < 0:
                args['timelen'] = get_text_by_id(80953)
            else:
                args['timelen'] = get_date_str('%Y.%m.%d', args['timelen'])
        if err_code == 609611:
            from logic.comsys.announcement.AnnouncementUI import AnnouncementUI
            AnnouncementUI(cb=self.change_to_login).show_content(get_text_by_id(609612), get_text_by_id(609611))
        else:
            NormalConfirmUI2(on_confirm=self.change_to_login).set_content_string(get_text_by_id(err_code, args))
        reason = args.get('reason', None)
        global_data.emgr.on_login_failed_event.emit(err_code, 'login_fail: %s , reason:%s' % (err_code, reason))
        return

    def restart_client(self):
        global_data.game_mgr.try_restart_app()

    @rpc_method(CLIENT_STUB, ())
    def active_account(self):
        from logic.comsys.common_ui.CDKeyInputUI import CDKeyInputUI
        CDKeyInputUI(on_confirm=self.req_active_cdkey, on_close=self.try_close_cdkey)

    def req_active_cdkey(self, str_sn, callback=lambda success: False):
        self.server.call_server_method('active_account', (str_sn,))
        self.cdkey_callback = callback

    def try_close_cdkey(self):
        global_data.emgr.on_login_failed_event.emit(None, 'cdkey_close')
        global_data.connect_helper.disconnect()
        return

    @rpc_method(CLIENT_STUB, (Int('ret_code'), Str('msg')))
    def active_cdkey_ret(self, ret_code, msg):
        self.cdkey_callback(ret_code, msg)

    @rpc_method(CLIENT_STUB, (Str('reason'),))
    def require_realname(self, reason):
        NormalConfirmUI2(on_confirm=self.open_realname).set_content_string(reason)

    def open_realname(self):
        from logic.comsys.realname.RealNameRegisterMgr import RealNameRegisterMgr
        RealNameRegisterMgr().show_realname_dialog(self.realname_callback, ui_confirm_cb=self.regist_realname)

    def realname_callback(self, *args, **kwargs):
        global_data.emgr.on_login_failed_event.emit()
        self.change_to_login()

    def regist_realname(self, realname, id_num, region_id):
        self.call_server_method('regist_realname', (realname, id_num, region_id))

    @rpc_method(CLIENT_STUB, (Bool('ret'), Str('msg')))
    def regist_realname_ret(self, ret, msg):
        global_data.emgr.regist_realname_result.emit(ret, msg)

    @rpc_method(CLIENT_STUB, (Int('msg_tid'),))
    def regist_realname_failed(self, msg_tid):
        global_data.emgr.regist_realname_result.emit(False, get_text_by_id(msg_tid))

    @rpc_method(CLIENT_STUB, (Str('msg'), Bool('disconnect'), Bool('require_realname')))
    def anti_addiction_message(self, msg, disconnect, require_realname):

        def confirm_cb(disconnect=disconnect, realname=require_realname):
            from common import utilities
            from common.platform import is_ios
            if realname:
                from logic.comsys.realname.RealNameRegisterMgr import RealNameRegisterMgr
                app_chanel = global_data.channel.get_name()
                if app_chanel == 'netease':
                    if utilities.compare_version(global_data.channel.get_sdk_version(), '3.23.0') >= 0:
                        global_data.channel.show_new_realname_dialog()
                    else:
                        global_data.channel.open_manager()
                    if is_ios():
                        self.set_change_to_login_and_restart(False)
                    self.change_to_login()
                    global_data.emgr.on_login_failed_event.emit()
                else:
                    RealNameRegisterMgr().show_realname_dialog(self.realname_callback, ui_confirm_cb=self.regist_realname)
                return
            if disconnect:
                self.change_to_login()
                global_data.emgr.on_login_failed_event.emit()

        NormalConfirmUI2(on_confirm=confirm_cb).set_content_string(msg)

    def bind_guest(self, bind_info):
        self.call_server_method('bind_guest', (bind_info,))

    @rpc_method(CLIENT_STUB, (Dict('bind_ret_info'),))
    def bind_guest_ret(self, bind_ret_info):
        pass