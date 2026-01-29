# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/salog.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
import game3d
import json
import time
from common.platform.channel import Channel
from common.platform import device_info
from logic.comsys.archive import archivedata, appendarchievedata
import threading
from common import http
import version
import os
import profiling
import common.utils.timer as timer
import C_file
from common.platform.dctool import interface
from common.daemon_thread import DaemonThreadPool

class SALog(object):
    instance = None
    ACTIVATION = 'Activation'
    LOGINUI = 'LoginUI'
    UPDATE = 'Update'
    UICLICK = 'UIClick'
    UICLICK_ADD_UP = 'UIClick_add_up'
    IDENTIFICATION = 'Identification'
    UNISDK_LOGIN = 'UnisdkLogin'
    UNISDK_LOGINCB = 'UnisdkLoginCB'
    UNISDK_FAIL = 'UnisdkFail'
    LOAD_LOBBY = 'LoadLobby'
    LOAD = 'Load'
    FPS_INFO = 'FPSInfo'
    MD5_CHECK = 'MD5Check'
    TUTORIAL = 'TutorialBehavior'
    PROTOCOL_ACCEPT = 'ProtocolAccept'
    QUERY_PRODUCT_LAG = 'QueryProductLag'
    BATTLE_CTRL_UI = 'BattleCtrlUI'
    COLLECT_UI = 'CollectUI'
    LANGUAGE_SELECTED = 'LoginLanguageSelected'
    SUCCESS_AUTH_TYPE = 'SuccessAuthType'
    FIRST_CLOSE_NOTICE = 'FirstCloseNotice'
    TRY_CONNECT_SERVER = 'TryConnectServer'
    SUCCESS_CONNECT_SERVER = 'SuccessConnectServer'
    INVISIBLE_ATTACKER = 'InvisibleAttacker'
    CHANNEL_LOGIN = 'ChannelLogin'
    ORDER_FAILED = 'OrderFailed'
    LINE_ALL_FRIENDS = 'Line_AllFriends'
    LINE_GAME_FRIENDS = 'Line_GameFriends'
    LINE_FOLLOW_INVITE = 'Line_follow_invite'
    CG_PLAY_START = 'CGPlayStart'
    CG_PLAY_END = 'CGPlayEnd'
    GET_SERVER_LIST = 'GetServerList'
    SERVER_LIST_OK = 'ServerListOk'
    SERVER_LIST_FAILED = 'ServerListFailed'
    APP_COMMENT_UI = 'AppCommentUI'
    HIGH_LIGHT_VIDEO_RECORD_SUC = 'HL_VideoDaySuc'
    HIGH_LIGHT_VIDEO_SHARE_SUC = 'HL_VideoDayShareSuc'
    FREE_VIDEO_RECORD_SUC = 'FREE_VideoDaySuc'
    FREE_VIDEO_SHARE_SUC = 'FREE_VideoDayShareSuc'
    ANDROID_32_BIT = 'Android_32bit_new2'
    LACK_CURRENCY = 'LackCurrency'
    update_begin_time = 0
    reach_update_time = 0
    reach_game_time = 0

    @staticmethod
    def get_instance():
        if SALog.instance is None:
            SALog.instance = SALog()
        return SALog.instance

    def __init__(self):
        self._channel = Channel.get_instance()
        self._before_load_time = 0
        self._load_log_writed = False
        self._archive_data = None
        self._is_drpf_available = False
        self.country_code = None
        self._init_archive_data()
        self._device_info = device_info.DeviceInfo.get_instance()
        self._archive_lock = threading.Lock()
        DaemonThreadPool().add_threadpool(self._init_drpf_available, None)
        self._battle_archive_data = appendarchievedata.AppendArchiveData('SABattleLog')
        self._temp_bat_archive_data = []
        self._battle_stat_archive_data = archivedata.ArchiveData('SABattleStatLog')
        self._battle_stat_data = {}
        threading.Timer(60.0, self.save_temp_battle_archive_timer).start()
        self._bat_archive_lock = threading.Lock()
        self._totol_fps = 0
        self._pfs_cnt = 0
        self._t_fps_log = global_data.game_mgr.register_logic_timer(lambda : self._log_fps_info(), interval=300, times=-1, mode=timer.CLOCK)
        self._server_list_url = ''
        self._ping = 99999
        global_data.emgr.net_delay_time_event += self._update_ping
        self.init_operation_handler()
        return

    def set_server_list_url(self, url):
        self._server_list_url = url

    def _init_archive_data(self):
        if self._archive_data is None:
            self._archive_data = archivedata.ArchiveData('data_SALog')
        return

    def _init_drpf_available(self):

        def callback--- This code section failed: ---

 126       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  '_archive_lock'
           6  SETUP_WITH           61  'to 70'
           9  POP_TOP          

 127      10  POP_TOP          
          11  POP_TOP          
          12  POP_TOP          
          13  LOAD_CONST            1  'ok'
          16  BUILD_TUPLE_2         2 
          19  COMPARE_OP            6  'in'
          22  POP_JUMP_IF_FALSE    37  'to 37'

 128      25  LOAD_GLOBAL           1  'True'
          28  LOAD_DEREF            0  'self'
          31  STORE_ATTR            2  '_is_drpf_available'
          34  JUMP_FORWARD          9  'to 46'

 130      37  LOAD_GLOBAL           3  'False'
          40  LOAD_DEREF            0  'self'
          43  STORE_ATTR            2  '_is_drpf_available'
        46_0  COME_FROM                '34'

 131      46  LOAD_DEREF            0  'self'
          49  LOAD_ATTR             4  'send_saved_log'
          52  CALL_FUNCTION_0       0 
          55  POP_TOP          

 132      56  LOAD_DEREF            0  'self'
          59  LOAD_ATTR             5  'send_saved_battle_archive'
          62  CALL_FUNCTION_0       0 
          65  POP_TOP          
          66  POP_BLOCK        
          67  LOAD_CONST            0  ''
        70_0  COME_FROM_WITH           '6'
          70  WITH_CLEANUP     
          71  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 10

        if interface.is_tw_package() or interface.is_global_package():
            url = 'https://drpf-%s.proxima.nie.easebar.com' % interface.get_project_id()
        else:
            url = 'https://drpf-%s.proxima.nie.netease.com' % interface.get_project_id()
        http.request(url, None, callback=callback)
        return

    def send_saved_log(self):
        if not self._is_drpf_available:
            return
        for key, value in self._archive_data.get_items():
            if key != 'activate':
                self._channel.DRPF(value)
                self._archive_data.del_field(key)

        self._archive_data.save()

    def get_drpf_app_channel(self):
        try:
            if game3d.get_platform() == game3d.PLATFORM_ANDROID:
                if interface.is_global_package():
                    return 'google_play'
                if interface.is_tw_package():
                    return 'g93naxx2tw@google_play'
            elif game3d.get_platform() == game3d.PLATFORM_IOS:
                if interface.is_tw_package():
                    return 'g93naxx2tw@app_store'
                else:
                    return 'app_store'

            channel = self._channel._channel
            if channel:
                channel_name = channel.name
                mapping = {'huawei': 'huawei',
                   'oppo': 'oppo',
                   'nearme_vivo': 'nearme_vivo',
                   'uc_platform': 'uc_platform',
                   'xiaomi_app': 'xiaomi_app',
                   'fanyou': 'fanyou',
                   'bilibili_sdk': 'bilibili_sdk',
                   '4399com': '4399com',
                   'nubia': 'nubia',
                   'yixin': 'yixin',
                   'iaround': 'iaround',
                   'juefeng': 'juefeng',
                   'guopan': 'guopan',
                   'kuchang': 'kuchang'
                   }
                if channel_name in mapping:
                    return mapping[channel_name]
                if channel.distribution_channel:
                    return channel.distribution_channel
                if channel_name != 'null':
                    return channel_name
        except Exception as e:
            print('salog drpf app channel error:', str(e))

        return 'null'

    def fill_base(self, json_paras):
        if not self._device_info:
            device_info.DeviceInfo().init_device_info()
            self._device_info = device_info.DeviceInfo().get_instance()
        json_paras['project'] = interface.get_project_id()
        json_paras['source'] = 'netease_p1'
        json_paras['ip'] = self._device_info.get_ip()
        json_paras['device_model'] = self._device_info.get_device_model()
        json_paras['os_name'] = self._device_info.get_os_name()
        json_paras['os_ver'] = self._device_info.get_os_ver()
        json_paras['mac_addr'] = self._device_info.get_mac_addr()
        json_paras['udid'] = self._channel.get_udid()
        json_paras['app_channel'] = self.get_drpf_app_channel()
        json_paras['app_ver'] = version.get_cur_version_str()
        json_paras['country_code'] = self.get_country_code()
        try:
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                json_paras['pid'] = str(os.getpid())
        except:
            pass

    def get_country_code(self):
        if hasattr(game3d, 'get_country_code'):
            ret = game3d.get_country_code() or ''
            return ret.upper()
        return 'UNKNOWN'

    def get_timestamp(self):
        return int(time.time())

    def set_before_load_time(self):
        self._before_load_time = self.get_timestamp()

    def save_update_ui_time(self):
        SALog.reach_update_time = self.get_timestamp()

    def activation_handler(self, json_paras, info):
        if self._archive_data.get_field('activate') is not None:
            return False
        else:
            self._archive_data.set_field('activate', 1)
            json_paras['active_time'] = self.get_timestamp()
            return True

    def loginui_handler(self, json_paras, info):
        json_paras['network'] = self._device_info.get_network()
        json_paras['reach_login_time'] = self.get_timestamp()
        SALog.reach_game_time = self.get_timestamp()
        return True

    def update_handler(self, json_paras, info):
        if not info:
            return False
        json_paras['network'] = self._device_info.get_network()
        json_paras['update_time'] = info[2]
        json_paras['type'] = 'Update'
        json_paras['reach_update_time'] = info[0]
        json_paras['use_time'] = info[2] - info[1]
        json_paras['update_status'] = info[3]
        json_paras['bundleid'] = game3d.get_app_name()
        SALog.update_begin_time = info[1]
        return True

    def unisdk_login_handler(self, json_paras, info):
        json_paras['network'] = self._device_info.get_network()
        json_paras['unisdk_login_time'] = self.get_timestamp()
        return True

    def unisdk_logincb_handler(self, json_paras, info):
        json_paras['network'] = self._device_info.get_network()
        json_paras['unisdk_logincb_time'] = self.get_timestamp()
        json_paras.update(info)
        return True

    def unisdk_fail_handler(self, json_paras, info):
        is_guest = self._channel.is_guest()
        json_paras['network'] = self._device_info.get_network()
        json_paras['unisdk_fail_time'] = self.get_timestamp()
        json_paras['unisdk_fail_code'] = info
        json_paras['account_id'] = self._channel.get_login_name(is_guest) or ''
        json_paras['old_accountid'] = self._channel.get_old_login_name() or ''
        return True

    def identification_handler(self, json_paras, info):
        is_guest = self._channel.is_guest()
        json_paras['network'] = self._device_info.get_network()
        json_paras['reach_login_time'] = self.get_timestamp()
        json_paras['account_id'] = self._channel.get_login_name(is_guest) or ''
        json_paras['old_accountid'] = self._channel.get_old_login_name() or ''
        return True

    def protocol_accept_handler(self, json_paras, info):
        is_guest = self._channel.is_guest()
        json_paras['network'] = self._device_info.get_network()
        json_paras['protocol_accept_time'] = self.get_timestamp()
        json_paras['account_id'] = self._channel.get_login_name(is_guest) or ''
        json_paras['old_accountid'] = self._channel.get_old_login_name() or ''
        return True

    def lobby_ui_click_handler(self, json_paras, info):
        is_guest = self._channel.is_guest()
        json_paras['network'] = self._device_info.get_network()
        json_paras['account_id'] = self._channel.get_login_name(is_guest) or ''
        json_paras['old_accountid'] = self._channel.get_old_login_name() or ''
        json_paras['account_id'] = self._channel.get_login_name()
        json_paras['old_accountid'] = self._channel.get_old_login_name()
        json_paras['role_id'] = info[0]
        json_paras['click_type'] = info[1]
        json_paras['click_desc'] = info[2] if len(info) > 2 else ''
        return True

    def load_lobby_handler(self, json_paras, info):
        is_guest = self._channel.is_guest()
        json_paras['load_lobby_time'] = self.get_timestamp()
        json_paras['network'] = self._device_info.get_network()
        json_paras['account_id'] = self._channel.get_login_name(is_guest) or ''
        json_paras['old_accountid'] = self._channel.get_old_login_name() or ''
        return True

    def load_handler(self, json_paras, info):
        if not self._load_log_writed:
            json_paras['network'] = self._device_info.get_network()
            json_paras['account_id'] = self._channel.get_login_name()
            json_paras['old_accountid'] = self._channel.get_old_login_name()
            json_paras['load_time_long'] = self.get_timestamp() - self._before_load_time
            json_paras['reach_game_time'] = self.get_timestamp()
            self._load_log_writed = True
        else:
            return False
        return True

    def fps_handler(self, json_paras, info):
        player = global_data.player
        if player is None:
            return False
        else:
            fps_info = {'fps': info,
               'ping': self._ping,
               'time': int(time.time())
               }
            battle = player.get_battle()
            if battle is not None:
                fps_info['game_id'] = str(battle.id)
                fps_info['game_type'] = battle.battle_tid
            player.call_server_method('client_sa_log', ('FPSInfo', fps_info))
            return False

    def md5_check_handler(self, json_paras, info):
        player = global_data.player
        if player is None:
            return False
        else:
            file_list = C_file.get_md5_faild_file_list()
            if len(file_list) == 0:
                return False
            md5_info = {'file_list': file_list
               }
            player.call_server_method('client_sa_log', ('MD5Check', md5_info))
            return False

    def query_product_lag_handler(self, json_paras, info):
        player = global_data.player
        if player is None:
            return False
        else:
            player.call_server_method('client_sa_log', ('QueryProductLag', {}))
            return False

    def battle_ctrl_ui_handler(self, json_paras, info):
        player = global_data.player
        if player is None:
            return False
        else:
            player.call_server_method('client_sa_log', ('BattleCtrlUI', {'ui': info}))
            return False

    def collect_ui_handler(self, json_paras, info):
        player = global_data.player
        if player is None:
            return False
        else:
            player.call_server_method('client_sa_log', ('CollectUI', {'ui_list': info}))
            return False

    def success_auth_type_handler(self, json_paras, info):
        json_paras['auth_name'] = self._channel.get_auth_type_name()
        json_paras['account_id'] = self._channel.get_login_name()
        json_paras['old_accountid'] = self._channel.get_old_login_name()
        json_paras['auth_time'] = self.get_timestamp()
        return True

    def tutorial_handler(self, json_paras, info):
        json_paras['network'] = self._device_info.get_network()
        json_paras['account_id'] = self._channel.get_login_name()
        json_paras['old_accountid'] = self._channel.get_old_login_name()
        json_paras['finish_guide_id'] = info
        json_paras['finish_guide_time'] = self.get_timestamp()
        return True

    def invisible_attacker_handler(self, json_paras, info):
        json_paras['self_id'] = info['self_id']
        json_paras['self_pos'] = info['self_pos']
        json_paras['attacker_id'] = info['attacker_id']
        json_paras['attacker_pos'] = info['attacker_pos']
        return True

    def login_language_selected_handler(self, json_paras, info):
        json_paras['lang_selected'] = info
        json_paras['selected_time'] = self.get_timestamp()
        return True

    def try_connect_server_handler(self, json_paras, info):
        json_paras['network'] = self._device_info.get_network()
        json_paras['account_id'] = self._channel.get_login_name()
        json_paras['old_accountid'] = self._channel.get_old_login_name()
        json_paras['group_id'] = interface.get_group_id()
        json_paras['server_name'] = interface.get_server_name()
        json_paras['server_ip'] = interface.get_server_ip()
        json_paras['server_port'] = interface.get_server_port()
        return True

    def channel_login_handler(self, json_paras, info):
        json_paras['channel_has_logined'] = self._channel.is_sdk_login
        return True

    def _order_failed_handler(self, json_paras, info):
        json_paras['role_id'] = global_data.player or '' if 1 else global_data.player.uid
        json_paras['order_id'] = info['order_id']
        json_paras['order_status'] = info['order_status']
        json_paras['order_reason'] = info['order_reason']
        return True

    def success_connect_server_handler(self, json_paras, info):
        json_paras['network'] = self._device_info.get_network()
        json_paras['account_id'] = self._channel.get_login_name()
        json_paras['old_accountid'] = self._channel.get_old_login_name()
        json_paras['group_id'] = interface.get_group_id()
        json_paras['server_name'] = interface.get_server_name()
        json_paras['server_ip'] = interface.get_server_ip()
        json_paras['server_port'] = interface.get_server_port()
        return True

    def first_close_notice_handler(self, json_paras, info):
        json_paras['close_notice_time'] = self.get_timestamp()
        return True

    def line_all_friends_handler(self, json_paras, info):
        player = global_data.player
        if player is None:
            return False
        else:
            line_info = {'cnt_line_game_frnd': info['cnt_line_game_frnd'],
               'cnt_line_frnd': info['cnt_line_frnd']
               }
            player.call_server_method('client_sa_log', (SALog.LINE_ALL_FRIENDS, line_info))
            return False

    def line_game_friends_handler(self, json_paras, info):
        player = global_data.player
        if player is None:
            return False
        else:
            line_info = {'frnd_list': info['frnd_list']
               }
            player.call_server_method('client_sa_log', (SALog.LINE_GAME_FRIENDS, line_info))
            return False

    def line_follow_invite_handler(self, json_paras, info):
        player = global_data.player
        if player is None:
            return False
        else:
            line_info = {'invite_role_id': info['invite_role_id'],
               'invite_type': info['invite_type']
               }
            player.call_server_method('client_sa_log', (SALog.LINE_FOLLOW_INVITE, line_info))
            return False

    def lack_currency_handler(self, json_paras, info):
        player = global_data.player
        if player is None:
            return False
        else:
            player.call_server_method('client_sa_log', ('lack_currency', info))
            return True

    def cg_play_start_handler(self, json_paras, info):
        json_paras['cg_start_time'] = self.get_timestamp()
        return True

    def cg_play_end_handler(self, json_paras, info):
        json_paras['cg_end_time'] = self.get_timestamp()
        return True

    def get_server_list_handler(self, json_paras, info):
        json_paras['get_server_list_time'] = self.get_timestamp()
        json_paras['server_list_url'] = self._server_list_url or ''
        return True

    def server_list_ok_handler(self, json_paras, info):
        json_paras['server_list_ok_time'] = self.get_timestamp()
        json_paras['server_list_url'] = self._server_list_url or ''
        return True

    def server_list_failed_handler(self, json_paras, info):
        json_paras['server_list_failed_time'] = self.get_timestamp()
        json_paras['server_list_url'] = self._server_list_url or ''
        return True

    def app_comment_ui_handler(self, json_paras, info):
        is_guest = self._channel.is_guest()
        json_paras['network'] = self._device_info.get_network()
        json_paras['account_id'] = self._channel.get_login_name(is_guest) or ''
        json_paras['old_accountid'] = self._channel.get_old_login_name() or ''
        json_paras['account_id'] = self._channel.get_login_name()
        json_paras['old_accountid'] = self._channel.get_old_login_name()
        json_paras['role_id'] = info[0]
        json_paras['click_type'] = info[1]
        return True

    def _video_generate_suc(self, json_paras, info):
        json_paras['role_id'] = info.get('role_id', '')
        return True

    def _video_share_suc(self, json_paras, info):
        json_paras['role_id'] = info.get('role_id', '')
        json_paras['platform'] = info.get('platform', '')
        return True

    def _android_32_bit(self, json_paras, info):
        json_paras['cpu_info'] = info.get('cpu_info', '')
        json_paras['uname_text'] = info.get('uname_text', '')
        json_paras['role_id'] = global_data.player or '' if 1 else global_data.player.uid
        return True

    def init_operation_handler(self):
        self.operation_handler = {SALog.ACTIVATION: self.activation_handler,
           SALog.FPS_INFO: self.fps_handler,
           SALog.LOGINUI: self.loginui_handler,
           SALog.UPDATE: self.update_handler,
           SALog.UNISDK_LOGIN: self.unisdk_login_handler,
           SALog.UNISDK_LOGINCB: self.unisdk_logincb_handler,
           SALog.UNISDK_FAIL: self.unisdk_fail_handler,
           SALog.IDENTIFICATION: self.identification_handler,
           SALog.LOAD_LOBBY: self.load_lobby_handler,
           SALog.LOAD: self.load_handler,
           SALog.MD5_CHECK: self.md5_check_handler,
           SALog.QUERY_PRODUCT_LAG: self.query_product_lag_handler,
           SALog.BATTLE_CTRL_UI: self.battle_ctrl_ui_handler,
           SALog.COLLECT_UI: self.collect_ui_handler,
           SALog.TUTORIAL: self.tutorial_handler,
           SALog.INVISIBLE_ATTACKER: self.invisible_attacker_handler,
           SALog.SUCCESS_AUTH_TYPE: self.success_auth_type_handler,
           SALog.LANGUAGE_SELECTED: self.login_language_selected_handler,
           SALog.TRY_CONNECT_SERVER: self.try_connect_server_handler,
           SALog.SUCCESS_CONNECT_SERVER: self.success_connect_server_handler,
           SALog.FIRST_CLOSE_NOTICE: self.first_close_notice_handler,
           SALog.PROTOCOL_ACCEPT: self.protocol_accept_handler,
           SALog.UICLICK: self.lobby_ui_click_handler,
           SALog.CHANNEL_LOGIN: self.channel_login_handler,
           SALog.ORDER_FAILED: self._order_failed_handler,
           SALog.LINE_ALL_FRIENDS: self.line_all_friends_handler,
           SALog.LINE_GAME_FRIENDS: self.line_game_friends_handler,
           SALog.LINE_FOLLOW_INVITE: self.line_follow_invite_handler,
           SALog.CG_PLAY_START: self.cg_play_start_handler,
           SALog.CG_PLAY_END: self.cg_play_end_handler,
           SALog.GET_SERVER_LIST: self.get_server_list_handler,
           SALog.SERVER_LIST_OK: self.server_list_ok_handler,
           SALog.SERVER_LIST_FAILED: self.server_list_failed_handler,
           SALog.APP_COMMENT_UI: self.app_comment_ui_handler,
           SALog.HIGH_LIGHT_VIDEO_RECORD_SUC: self._video_generate_suc,
           SALog.HIGH_LIGHT_VIDEO_SHARE_SUC: self._video_generate_suc,
           SALog.FREE_VIDEO_RECORD_SUC: self._video_share_suc,
           SALog.FREE_VIDEO_SHARE_SUC: self._video_share_suc,
           SALog.ANDROID_32_BIT: self._android_32_bit,
           SALog.LACK_CURRENCY: self.lack_currency_handler
           }

    def write(self, operation, info=None):
        json_paras = {}
        json_paras['type'] = operation
        self.fill_base(json_paras)
        handler = self.operation_handler.get(operation, None)
        if not handler:
            return
        else:
            handle_res = False
            try:
                handle_res = handler(json_paras, info)
            except Exception as e:
                handle_res = False
                print('[ERROR] SALOG handler EROOR', str(e))

            if not handle_res:
                return
            try:
                str_json = json.dumps(json_paras)
            except Exception as e:
                import exception_hook
                exception_hook.post_error('salog write bad json %s, %s' % (e.message, json_paras))
                return

            with self._archive_lock:
                if not self._is_drpf_available:
                    self._archive_data.set_field(operation + str(int(time.time())), str_json)
                    return
            self._channel.DRPF(str_json)
            return

    def write_battle_log(self, operation, info=None):
        json_paras = {}
        json_paras['type'] = operation
        self.fill_base(json_paras)
        if operation == SALog.UICLICK:
            json_paras['account_id'] = self._channel.get_login_name()
            json_paras['old_accountid'] = self._channel.get_old_login_name()
            json_paras['server'] = info[0]
            json_paras['role_id'] = info[1]
            json_paras['game_id'] = info[2]
            json_paras['game_type'] = info[3]
            json_paras['gametime'] = info[4]
            json_paras['click_type'] = info[5]
            json_paras['click_desc'] = info[6] if len(info) > 6 else ''
        elif operation == SALog.UICLICK_ADD_UP:
            json_paras['account_id'] = self._channel.get_login_name()
            json_paras['old_accountid'] = self._channel.get_old_login_name()
            json_paras['server'] = info[0]
            json_paras['role_id'] = info[1]
            json_paras['game_id'] = info[2]
            json_paras['game_type'] = info[3]
            json_paras['game_start_time'] = info[4]
            store_key_1 = info[5]
            store_key_2 = info[6]
            unique_key = info[7]
            count = info[8]
            if unique_key not in self._battle_stat_data:
                self._battle_stat_data[unique_key] = json_paras
            if not store_key_1:
                return
            if store_key_1 and store_key_2:
                self._battle_stat_data[unique_key].setdefault(store_key_1, {})
                if store_key_2 not in self._battle_stat_data[unique_key][store_key_1]:
                    self._battle_stat_data[unique_key][store_key_1].setdefault(store_key_2, 0)
                self._battle_stat_data[unique_key][store_key_1][store_key_2] += count
            elif store_key_1:
                self._battle_stat_data[unique_key].setdefault(store_key_1, 0)
                self._battle_stat_data[unique_key][store_key_1] += count
            return
        try:
            str_json = json.dumps(json_paras)
        except Exception as e:
            import exception_hook
            exception_hook.post_error('salog write battle bad json %s, %s' % (e.message, json_paras))
            return

        if '\x00' in str_json:
            err_msg = 'null byte in str_json,' + str_json
            print(err_msg)
            return
        with self._bat_archive_lock:
            self._temp_bat_archive_data.append(str_json)

    def check_update_log(self):
        pass

    def _log_fps_info(self):
        self._totol_fps = 0
        self._pfs_cnt = 0
        global_data.game_mgr.register_logic_timer(lambda : self._get_cur_fps(), interval=1, times=10, mode=timer.CLOCK)

    def _get_cur_fps(self):
        self._totol_fps += profiling.get_logic_rate()
        self._pfs_cnt += 1
        if self._pfs_cnt == 10:
            avrg_fps = int(self._totol_fps / self._pfs_cnt)
            self.write(SALog.FPS_INFO, avrg_fps)

    def _update_ping(self, rtt_type, rtt):
        self._ping = rtt * 1000

    def save_temp_battle_archive_timer(self):
        pass

    def save_tmp_battle_archive(self):
        if self._battle_archive_data and self._temp_bat_archive_data:
            with self._bat_archive_lock:
                self._battle_archive_data.append_save(self._temp_bat_archive_data)
                self._temp_bat_archive_data = []
                if self._battle_stat_data:
                    self._battle_stat_archive_data.clear()
                    for k, v in six.iteritems(self._battle_stat_data):
                        self._battle_stat_archive_data[k] = v

                    self._battle_stat_archive_data.save(False)

    def send_saved_battle_archive(self):
        if not self._is_drpf_available:
            return
        self.save_tmp_battle_archive()
        with self._bat_archive_lock:
            log_list = self._battle_archive_data.load()
            for log in log_list:
                try:
                    self._channel.DRPF(log)
                except:
                    self._battle_archive_data.clear_save_data()
                    raise ValueError('send_saved_battle_archive Wrong format', log)

            self._battle_archive_data.clear_save_data()
            self._battle_stat_archive_data.load()
            log_list = six_ex.values(self._battle_stat_archive_data.get_conf())
            for log in log_list:
                try:
                    str_json = json.dumps(log)
                except Exception as e:
                    import exception_hook
                    exception_hook.post_error('salog save battle arc bad json %s, %s' % (e.message, log))
                    continue

                if str_json:
                    try:
                        self._channel.DRPF(str_json)
                    except:
                        self._battle_stat_archive_data.clear()
                        raise ValueError('send_saved_battle_archive Wrong format', str_json)

                self._battle_stat_data = {}
                self._battle_stat_archive_data.clear()