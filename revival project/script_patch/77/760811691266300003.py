# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/ConnectHelper.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import sys
import json
import C_file
import os
from common.framework import Singleton
from common.utils.path import get_neox_dir
from mobile.mobilelog.LogManager import LogManager
from mobile.client.NetService import NetService
from mobile.client.GateClient import GateClient
from mobile.simplerpc.DirectProxy import DirectProxy
from mobile.simplerpc.rpc_code import RPC_CODE
from logic.gcommon.common_utils.local_text import get_text_by_id
import time as org_time
from logic.gcommon.time_utility import ONE_HOUR_SECONS, ONE_WEEK_SECONDS, time
import six.moves.builtins
from logic.gutils.salog import SALog
import random
import common.http
import game3d

class ConnectHelper(Singleton):
    ALIAS_NAME = 'connect_helper'
    GATE_CLIENT_CONFIG = {'enforce_encryption': True,
       'loginkeypath': None,
       'loginkeycontent': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQD491p2WNhXY14+TsxjYID3SytOrw/l5s+IKq6Rwg7q8rMpSywlm68MvIFlcC2xPJ7aZZ09Cc9NJ142mKOaForU9IIT2u/3Vt1Bf6su1aR9yoIF7NHvHvbLdWSG379Nbu2y6+uNJZfbCbPipQPc2MRCHZLsqOcsaGl9q3kBGDVJ6w==',
       'use_keyczar': False,
       'zipped_channel': 1,
       'proto': 'msgpack',
       'con_type': 'TCP',
       'compressor_type': 'ZLIB',
       'is_support_comperssor_type': global_data.feature_mgr.is_support_oodle(),
       'oodnet_up_dict_path': os.path.join(game3d.get_doc_dir(), 'oodle_dict/gate/client_to_server.mdic'),
       'oodnet_down_dict_path': os.path.join(game3d.get_doc_dir(), 'oodle_dict/gate/server_to_client.mdic')
       }
    BATTLE_CLIENT_CONFIG = {'key_content': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQD491p2WNhXY14+TsxjYID3SytOrw/l5s+IKq6Rwg7q8rMpSywlm68MvIFlcC2xPJ7aZZ09Cc9NJ142mKOaForU9IIT2u/3Vt1Bf6su1aR9yoIF7NHvHvbLdWSG379Nbu2y6+uNJZfbCbPipQPc2MRCHZLsqOcsaGl9q3kBGDVJ6w==',
       'con_type': 'KCP',
       'kcp_judgment_limit': ONE_WEEK_SECONDS,
       'kcp_judgment_step': ONE_HOUR_SECONS,
       'kcp_interval': 20,
       'compressor_type': 'OODLE' if global_data.feature_mgr.is_support_oodle_v2() else 'ZLIB',
       'oodnet_up_dict_path': os.path.join(game3d.get_doc_dir(), 'oodle_dict', 'battle', 'client_to_server.mdic'),
       'oodnet_down_dict_path': os.path.join(game3d.get_doc_dir(), 'oodle_dict', 'battle', 'server_to_client.mdic')
       }
    LOBBY_SILENT_RECONNECT_TIMES = 2
    BATTLE_SILENT_RECONNECT_TIMES = 3
    RECONNECT_FALLBACK_TIMES = 8
    RECONNECT_CHOOSE_INTERVAL_TIME = 5
    ST_UI_WAITING = 1
    ST_UI_RECONNECT_SUCCESS = 2
    ST_UI_SELECT = 3

    def init(self):
        self.logger = LogManager.get_logger('ConnectHelper')
        self._server_host = None
        self._server_peername = None
        self._gate_service = NetService(self.GATE_CLIENT_CONFIG, sys.excepthook)
        self.set_service_default_callback()
        self._battle_service = None
        self._reconnect_uname = None
        self._reconnect_token = None
        self._reconnect_game = None
        self._login_reconnect = False
        self._reconnect_time = 0
        self._enable_lobby_reconnect_ui_show = True
        self._last_connect_start_time = 0
        self._connect_using_secs = 0
        self._reconnect_from = 'unkown'
        self._last_choose_reconnect_time = 0
        self.is_steam_lighten = False
        self.lighten_data = None
        self.lighten_log_body_login = {'project': 'g93','type': 'login','scene': 'login','region': 'cn','method': '','failed_count': 0}
        self.lighten_log_body_battle = {'project': 'g93','type': 'login','scene': 'battle','region': 'cn','method': '','failed_count': 0}
        self.connect_game_server_info = None
        return

    def tick(self):
        self._gate_service.tick()

    @staticmethod
    def DisconnectUnCheckMethod(func):

        def check_with_connect_status(*args, **kwargs):
            if ConnectHelper().get_connect_status() == NetService.ST_CONNECTED:
                func(*args, **kwargs)

        return check_with_connect_status

    def get_connect_status(self):
        return self._gate_service.get_connect_status()

    def is_disconnected(self):
        return self._gate_service.disconnected()

    def is_connected(self):
        return self._gate_service.connected()

    def is_connecting(self):
        return self._gate_service.connecting()

    def is_login_reconnect(self):
        _login_reconnect = self._login_reconnect
        self._login_reconnect = False
        return _login_reconnect

    def get_host(self):
        return self._server_host

    def connect(self, host, ip, port):
        if not self.is_disconnected():
            return False
        if ip == '127.0.0.1':
            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2 as ConfirmUI
            ConfirmUI(content=get_text_by_id(271), on_confirm=self.fall_back_to_server_select)
            return False
        self._server_host = host
        self._server_peername = (ip, port)
        self._gate_service.connect(ip, port, self.get_connect_authmsg())
        self._last_connect_start_time = org_time.time()
        self._connect_using_secs = 0
        return True

    def connect_battle(self, avatar, ip, port, token, bind_cb, kcp_valid=True):
        import logic.gcommon.common_utils.sync_key_mapping_utils
        if self._battle_service and not self._battle_service.is_close():
            self._battle_service.close()
            return
        else:
            ip, port = self.convert_ip_port_from_lighten(ip, port, 'battle')
            con_type = self._judge_connect(self.BATTLE_CLIENT_CONFIG.get('con_type', 'TCP')) if kcp_valid else 'TCP'
            conf = {'key_content': self.BATTLE_CLIENT_CONFIG.get('key_content', None),
               'con_type': con_type,
               'bind_token': token,
               'compressor_type': self.BATTLE_CLIENT_CONFIG.get('compressor_type') if global_data.enable_battle_oodle and global_data.feature_mgr.is_support_oodle_v2() else 'ZLIB',
               'is_support_oodle': global_data.feature_mgr.is_support_oodle(),
               'oodnet_up_dict_path': self.BATTLE_CLIENT_CONFIG.get('oodnet_up_dict_path', ''),
               'oodnet_down_dict_path': self.BATTLE_CLIENT_CONFIG.get('oodnet_down_dict_path', '')
               }

            def _bind_callback(code):
                if code == RPC_CODE.OK:
                    self._battle_service.add_lose_bind_cb(self.disconnect)
                    self.send_lighten_log('battle', True)
                    if con_type == 'KCP':
                        self._judge_kcp(False)
                        kcp_interval = self.BATTLE_CLIENT_CONFIG['kcp_interval']
                        self._battle_service.get_connection().set_kcp_interval(kcp_interval)
                elif code in (RPC_CODE.CONNECT_FAIL, RPC_CODE.TIMEOUT):
                    self.send_lighten_log('battle', False)
                    if con_type == 'KCP':
                        self._judge_kcp(True)
                else:
                    self.send_lighten_log('battle', False)
                bind_cb(code, con_type)

            def _handle_sync--- This code section failed: ---

 220       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'battle'
           6  POP_JUMP_IF_FALSE    50  'to 50'
           9  LOAD_FAST             1  'connection'
          12  LOAD_ATTR             2  'entity'
          15  POP_JUMP_IF_FALSE    50  'to 50'
          18  LOAD_FAST             1  'connection'
          21  LOAD_ATTR             2  'entity'
          24  LOAD_ATTR             3  'is_valid'
        27_0  COME_FROM                '15'
        27_1  COME_FROM                '6'
          27  POP_JUMP_IF_FALSE    50  'to 50'

 221      30  LOAD_GLOBAL           0  'global_data'
          33  LOAD_ATTR             1  'battle'
          36  LOAD_ATTR             4  'sync_battle_direct'
          39  LOAD_ATTR             1  'battle'
          42  BINARY_SUBSCR    
          43  CALL_FUNCTION_1       1 
          46  POP_TOP          
          47  JUMP_FORWARD          0  'to 50'
        50_0  COME_FROM                '47'

Parse error at or near `BINARY_SUBSCR' instruction at offset 42

            self._battle_service = DirectProxy(avatar, avatar.id, (ip, port), conf, _bind_callback, _handle_sync, _handle_sync)
            return

    def request_lighten_list(self, *args):
        self.is_steam_lighten = True
        self.connect_game_server_info = args
        listen_list_url = 'https://impression.update.netease.com/lighten/g93na/cn.txt'
        from common.platform.orbit_utils import OrbitHelper
        OrbitHelper().add_request(listen_list_url, 'lighten_list', self.parse_ip_port_from_lighten)

    def parse_ip_port_from_lighten(self, content):
        gate_host, gate_ip, gate_port = self.connect_game_server_info
        if not content:
            print('====request_lighten_list Failed!!!!!====')
            target_ip, target_port = self.convert_ip_port_from_lighten(gate_ip, gate_port, 'login')
            self.connect(gate_host, target_ip, target_port)
            return
        self.lighten_data = {}
        for line in content.split('\n'):
            line_data = line.split(' ')
            if len(line_data) < 4:
                continue
            origin_info, _, port_info, address_info = line_data[:4]
            address = address_info.split(',')
            origin_host, origin_port, origin_step, origin_number = origin_info.split(':')[:4]
            lighten_port, lighten_step, lighten_number = port_info.split(':')[:3]
            self.lighten_data.setdefault(origin_host, {})
            for step in range(min(int(origin_number), int(lighten_number))):
                port = int(origin_port) + step * int(origin_step)
                port_lighten = int(lighten_port) + step * int(lighten_step)
                self.lighten_data[origin_host][port] = [ [addr, port_lighten] for addr in address ]

        target_ip, target_port = self.convert_ip_port_from_lighten(gate_ip, gate_port, 'login')
        self.connect(gate_host, target_ip, target_port)

    def convert_ip_port_from_lighten(self, ip, port, scene):
        if self.is_steam_lighten:
            cur_lighten_log_body = self.lighten_log_body_login if scene == 'login' else self.lighten_log_body_battle
            cur_lighten_log_body['origin_host'] = ip
            cur_lighten_log_body['origin_port'] = port
            if self.lighten_data:
                if ip in self.lighten_data and port in self.lighten_data[ip]:
                    speed_host, speed_port = random.choice(self.lighten_data[ip][port])
                    cur_lighten_log_body['login_msg'] = 'HARBOR_SUCCESS'
                    cur_lighten_log_body['speed_host'] = speed_host
                    cur_lighten_log_body['speed_port'] = speed_port
                    return (
                     speed_host, speed_port)
                cur_lighten_log_body['login_msg'] = 'HARBOR_NOT_SPEED'
            else:
                cur_lighten_log_body['login_msg'] = 'HARBOR_NOT_SERVER'
        return (ip, port)

    def send_lighten_log(self, scene, success):
        if not self.is_steam_lighten:
            return
        if scene == 'login':
            cur_lighten_log_body = self.lighten_log_body_login if 1 else self.lighten_log_body_battle
            header = {'content-type': 'application/json'}
            cur_time = int(org_time.time())
            if 'login_timestamp' in cur_lighten_log_body:
                cur_lighten_log_body['login_interval'] = cur_time - cur_lighten_log_body['login_timestamp']
            login_status = 0
            if cur_lighten_log_body['login_msg'] == 'HARBOR_SUCCESS':
                if success:
                    login_status = 2
                else:
                    login_status = 3
            elif success:
                login_status = 0
            else:
                login_status = 1
            cur_lighten_log_body['failed_count'] = success or cur_lighten_log_body['failed_count'] + 1
            cur_lighten_log_body['login_error'] = cur_lighten_log_body['failed_count']
        cur_lighten_log_body['login_status'] = login_status
        cur_lighten_log_body['login_timestamp'] = cur_time
        cur_lighten_log_body['udid'] = global_data.channel.get_udid()
        body_str = json.dumps(cur_lighten_log_body)
        print('======send_lighten_log ==body_str:', body_str)

        def callback(ret, url, args):
            print('====send_lighten_log callback, ret:', ret)

        log_url = 'https://netlink-sigma.proxima.nie.netease.com/login'
        common.http.request(log_url, data=body_str, header=header, callback=callback)

    def _judge_connect(self, con_type):
        if con_type == 'KCP':
            archive_data = global_data.achi_mgr.get_general_archive_data()
            kcp_judgment = archive_data.get_field('kcp_judgment', 0)
            con_type = 'KCP' if time() >= kcp_judgment else 'TCP'
        return con_type

    def _judge_kcp(self, is_failure):
        archive_data = global_data.achi_mgr.get_general_archive_data()
        if is_failure:
            kcp_failure = archive_data.get_field('kcp_failure', 0)
            kcp_judgment_step = self.BATTLE_CLIENT_CONFIG['kcp_judgment_step']
            kcp_judgment_limit = self.BATTLE_CLIENT_CONFIG['kcp_judgment_limit']
            kcp_judgment = min(2 ** kcp_failure * kcp_judgment_step, kcp_judgment_limit) + int(time())
            kcp_failure += 1
        else:
            kcp_failure = 0
            kcp_judgment = 0
        archive_data.set_field('kcp_failure', kcp_failure)
        archive_data.set_field('kcp_judgment', kcp_judgment)

    def disconnect(self):
        self._gate_service.disconnect()

    def disconnect_battle(self):
        if self._battle_service:
            self._battle_service.close()
            self._battle_service = None
        return

    def get_reconnect_game(self):
        return self._reconnect_game or ''

    def set_reconnect_info(self, uname, token, game):
        self._reconnect_uname = uname
        self._reconnect_token = token
        self._reconnect_game = game

    def reset_reconnect_info(self):
        self._reconnect_uname = None
        self._reconnect_token = None
        self._reconnect_game = None
        return

    def can_token_reconnect(self):
        return self._reconnect_uname is not None and self._reconnect_token is not None

    def get_reconnect_authmsg(self):
        auth_msg = {'accountname': self._reconnect_uname,
           'token': self._reconnect_token,
           'game': self._reconnect_game,
           'client_received_seq': self._gate_service.get_received_srv_msg_seq(),
           'client_send_seq_range': self._gate_service.get_send_srv_msg_seq_range()
           }
        return auth_msg

    def get_connect_authmsg(self):
        try:
            server_conf = json.loads(C_file.get_res_file('confs/server.json', ''))
            if 'auth_msg' in server_conf:
                return server_conf['auth_msg']
            return None
        except Exception as e:
            return None

        return None

    def reconnect(self):
        self.do_auth_reconnect()

    def do_auth_reconnect(self):
        if not self.is_disconnected():
            return
        else:
            if not self._server_peername:
                self.pop_failed_confirm_fall_back_server_select()
                return
            avt_id = None if global_data.player is None else global_data.player.id
            if avt_id is None:
                self.pop_failed_confirm_fall_back_server_select()
                return
            global_data.player.reset_network_type_check()
            if global_data.player.local_battle:
                if global_data.owner_entity and global_data.owner_entity.__class__.__name__ == 'CharacterSelect':
                    global_data.ui_mgr.close_ui('SecondConfirmDlg2')
                    global_data.ui_mgr.close_ui('MainSettingUI')
                    self.do_login_reconnect()
                    return
                if not global_data.player.logic or not global_data.player.logic.get_value('G_GUIDE_CONSTRUCT'):
                    global_data.player.quit_battle()

            def on_disconnect():
                self.select_reconnect_action(self.do_auth_reconnect, self.do_login_reconnect)

            self.clean_service_callback()
            self.set_service_callback(GateClient.CB_ON_DISCONNECTED, on_disconnect)
            self.set_service_callback(GateClient.CB_ON_CONNECT_FAILED, on_disconnect)
            ip, port = self._server_peername
            self._gate_service.reconnect(ip, port, avt_id, self.get_reconnect_authmsg())
            self._last_connect_start_time = org_time.time()
            return

    def do_login_reconnect(self):
        if self.is_connecting():
            return
        else:
            if not self._server_peername:
                self.pop_failed_confirm_fall_back_server_select()
                return
            avt_id = None if global_data.player is None else global_data.player.id
            if avt_id is None:
                self.pop_failed_confirm_fall_back_server_select()
                return
            global_data.player.reset_network_type_check()
            self.clean_service_callback()
            self.set_service_callback(GateClient.CB_ON_DISCONNECTED, self.defualt_dummy_cb)
            self.set_service_callback(GateClient.CB_ON_CONNECT_FAILED, self.defualt_dummy_cb)
            self.set_service_callback(GateClient.CB_ON_CONNECT_REPLY, self.defualt_dummy_cb)
            self.disconnect()
            self.clean_service_callback()

            def on_disconnect():
                self.select_reconnect_action(self.do_login_reconnect, self.do_login_reconnect, ConnectHelper.RECONNECT_FALLBACK_TIMES)

            self.set_service_callback(GateClient.CB_ON_DISCONNECTED, on_disconnect)
            self.set_service_callback(GateClient.CB_ON_CONNECT_FAILED, on_disconnect)
            self.set_service_callback(GateClient.CB_ON_CONNECT_REPLY, self.login_reconnect_reply)
            global_data.emgr.on_request_login_event.emit()
            self._login_reconnect = True
            host = self._server_host
            ip, port = self._server_peername
            if self.connect(host, ip, port):
                pass
            return

    def login_reconnect_reply(self, reply_type):
        from mobile.common.proto_python.common_pb2 import ConnectServerReply
        print('################ login_reconnect_reply reply_type=', reply_type)
        if reply_type == ConnectServerReply.CONNECTED:
            self.on_reconnect_success('login_reconnect')
            self.clean_service_callback()
            global_data.emgr.net_login_reconnect_before_destroy_event.emit()
            global_data.game_mgr.stop_game(True)
            global_data.emgr.avatar_reconnect_destroy_event.emit()
            global_data.emgr.net_login_reconnect_event.emit()
        else:
            self.clean_service_callback()
            self.set_service_callback(GateClient.CB_ON_DISCONNECTED, self.defualt_dummy_cb)
            self.set_service_callback(GateClient.CB_ON_CONNECT_FAILED, self.defualt_dummy_cb)
            self.set_service_callback(GateClient.CB_ON_CONNECT_REPLY, self.defualt_dummy_cb)
            self.disconnect()
            self._gate_service.set_disconnect_msg(get_text_by_id(119, {'code': reply_type}))
            self.fall_back_to_server_select()

    def set_service_disconnect_msg(self, msg):
        self._gate_service.set_disconnect_msg(msg)

    def set_service_default_callback(self):
        set_default_callback = self._gate_service.set_default_callback
        set_default_callback(GateClient.CB_ON_CONNECT_FAILED, self.default_connect_failed_cb)
        set_default_callback(GateClient.CB_ON_DISCONNECTED, self.default_disconnect_cb)
        set_default_callback(GateClient.CB_ON_RELIABLE_MESSAGE_CANNOT_SENT, self.default_reliable_message_cannot_sent_cb)
        set_default_callback(GateClient.CB_ON_CONNECT_REPLY, self.default_connected_reply_cb)

    def set_service_callback(self, cb_type, callback):
        self._gate_service.set_user_callback(cb_type, callback)

    def unset_service_callback(self, cb_type, callback):
        self._gate_service.unset_user_callback(cb_type, callback)

    def clean_service_callback(self):
        self._gate_service.clean_all_user_callback()

    def clean_service_cache(self, reset_seq=True):
        self._gate_service.clean_cache(reset_seq)

    def default_connect_failed_cb(self):
        err_code = 121
        error_log = 'CONNECT_FAILED'
        global_data.emgr.on_login_failed_event.emit(err_code, error_log)
        self.send_lighten_log('login', False)

    def default_disconnect_cb(self):
        self.disconnect_battle()
        self.reconnect()
        global_data.emgr.net_disconnect_event.emit()

    def default_reliable_message_cannot_sent_cb(self, op_code):
        print('################ default_reliable_message_cannot_sent_cb op_code=', op_code)

    def default_connected_reply_cb(self, reply_type):
        from mobile.common.proto_python.common_pb2 import ConnectServerReply
        print('################ default_connected_reply_cb reply_type=', reply_type)
        if reply_type == ConnectServerReply.CONNECTED:
            global_data.game_mgr.init_ingame_env()
            salog_writer = SALog.get_instance()
            salog_writer.write(SALog.SUCCESS_CONNECT_SERVER)
            self.send_lighten_log('login', True)
            return
        if reply_type == ConnectServerReply.RECONNECT_SUCCEEDED:
            self.on_reconnect_success('reconnect')
            self.clean_service_callback()
            return
        if reply_type == ConnectServerReply.RECONNECT_FAILED:
            self.do_login_reconnect()
            return
        if reply_type == ConnectServerReply.MAX_CONNECTION:
            self._gate_service.set_disconnect_msg(get_text_by_id(2))
        else:
            self._gate_service.set_disconnect_msg(get_text_by_id(119, {'code': reply_type}))
        self.fall_back_to_server_select()

    def defualt_dummy_cb(self):
        pass

    def pop_failed_confirm_fall_back_server_select(self):
        self.clean_service_callback()
        self.set_service_callback(GateClient.CB_ON_DISCONNECTED, self.defualt_dummy_cb)
        self.set_service_callback(GateClient.CB_ON_CONNECT_FAILED, self.defualt_dummy_cb)
        msg = self._gate_service.pop_disconnect_msg()
        if msg:
            if not global_data.ui_mgr.get_all_ui_visible():
                global_data.ui_mgr.set_all_ui_visible(True)
                self.fall_back_to_server_select()
                return
            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2 as ConfirmUI
            ConfirmUI(content=msg, on_confirm=self.fall_back_to_server_select)
        else:
            self.fall_back_to_server_select()

    def fall_back_to_server_select(self):
        self._login_reconnect = False
        self._reconnect_time = 0
        global_data.ui_mgr.close_all_ui()
        self.clean_service_callback()
        global_data.game_mgr.restart()

    def select_reconnect_action(self, reconnect_handler, timeout_handler, fallback_times=None):
        self._reconnect_time += 1
        if fallback_times is not None and self._reconnect_time >= ConnectHelper.RECONNECT_FALLBACK_TIMES:
            self.pop_failed_confirm_fall_back_server_select()
            return
        else:
            is_in_lobby = self.check_is_in_lobby()

            def _reconnect_choose():
                self._last_choose_reconnect_time = time()
                timeout_handler()

            if is_in_lobby:
                if self._reconnect_time <= ConnectHelper.LOBBY_SILENT_RECONNECT_TIMES or time() - self._last_choose_reconnect_time < self.RECONNECT_CHOOSE_INTERVAL_TIME:
                    reconnect_handler()
                else:
                    self.show_battle_reconnect_ui(ConnectHelper.ST_UI_SELECT, _reconnect_choose)
            elif not is_in_lobby:
                if global_data.player and global_data.player.is_in_global_spectate():
                    self.show_battle_reconnect_ui(ConnectHelper.ST_UI_SELECT, _reconnect_choose)
                elif self._reconnect_time <= ConnectHelper.BATTLE_SILENT_RECONNECT_TIMES or time() - self._last_choose_reconnect_time < self.RECONNECT_CHOOSE_INTERVAL_TIME:
                    reconnect_handler()
                else:
                    self.show_battle_reconnect_ui(ConnectHelper.ST_UI_SELECT, _reconnect_choose)
            return

    def on_reconnect_success(self, str_from='default'):
        self._reconnect_time = 0
        self.show_success_reconnect_ui()
        self._connect_using_secs = org_time.time() - self._last_connect_start_time
        self._reconnect_from = str_from
        if global_data.player:
            global_data.player.call_server_method('reconnect_using_time', (str(str_from), self._connect_using_secs))

    def get_reconnnect_using_time_info(self):
        return (
         self._connect_using_secs, self._reconnect_from)

    def show_success_reconnect_ui(self):
        ui_inst = global_data.ui_mgr.get_ui('BattleReconnectUI')
        if ui_inst:
            ui_inst.show_info_message(get_text_by_id(120), alive_time=2)

    def show_battle_reconnect_ui(self, st, reconnect_func=None):
        ui_inst = global_data.ui_mgr.get_ui('BattleReconnectUI')
        if not ui_inst:
            from logic.comsys.reconnect_ui.BattleReconnectUI import BattleReconnectUI
            BattleReconnectUI()
            ui_inst = global_data.ui_mgr.get_ui('BattleReconnectUI')
        if st == ConnectHelper.ST_UI_SELECT:

            def sure_callback():
                if reconnect_func:
                    ui_inst.show_info_message(get_text_by_id(121), cancel_callback=lambda : self.fall_back_to_server_select())
                    reconnect_func()
                else:
                    self.fall_back_to_server_select()

            def cancel_callback():
                ui_inst.close()
                self.fall_back_to_server_select()

            ui_inst.show_select_message(sure_callback=sure_callback, cancel_callback=cancel_callback)
        elif st == ConnectHelper.ST_UI_WAITING:
            ui_inst.show_info_message(get_text_by_id(121), cancel_callback=lambda : self.fall_back_to_server_select())
        elif st == ConnectHelper.ST_UI_RECONNECT_SUCCESS:
            ui_inst.show_info_message(get_text_by_id(120), alive_time=2)

    def check_is_in_lobby(self):
        if global_data.player:
            return not global_data.player.is_in_battle()
        return True

    def get_proto_encoder(self):
        return self._gate_service._gate_client.proto_encoder