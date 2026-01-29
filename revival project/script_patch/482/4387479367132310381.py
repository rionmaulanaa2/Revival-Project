# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/live/cclive_agent.py
from __future__ import absolute_import
from .live_agent_interface import LiveAgentInterface
import json
from logic.gcommon.common_const import liveshow_const

class CCLiveAgent(LiveAgentInterface):

    def __init__(self):
        super(CCLiveAgent, self).__init__()
        import cclive
        self._player = cclive.player()
        self._timer_id = None
        self._has_regist = False
        self._set_up_callback()
        return

    def init(self, live_data):
        super(CCLiveAgent, self).init(live_data)

    def destroy(self):
        super(CCLiveAgent, self).destroy()
        self.unregist_msg()
        self._clear_callback()

    def play_live(self, url):
        self._player.play_live(url)

    def login(self, usr_name, password):
        if global_data.channel.is_free_login:
            return
        self._player.login(liveshow_const.CC_GAME_SRC, usr_name, password)
        self._player.set_user_info(global_data.player.uid, global_data.channel.get_udid())
        import game3d
        platform = game3d.get_platform()
        if platform == game3d.PLATFORM_ANDROID:
            client_type = liveshow_const.CC_ANDROID_CLIENT_TYPE
        elif platform == game3d.PLATFORM_IOS:
            client_type = liveshow_const.CC_IOS_CLIENT_TYPE
        else:
            client_type = liveshow_const.CC_WINDOWS_CLIENT_TYPE
        from logic.comsys.feedback import echoes
        extra_info = {'udid': global_data.channel.get_udid(),'game_server': str(echoes.server_info['server_name']),'game_uid': global_data.player.uid,
           'client_type': client_type,
           'platform': liveshow_const.CC_GAME_PLATFORM
           }
        data = json.dumps(extra_info)
        self._player.set_extra_info(data)

    def set_vbr(self, vbr_str):
        self._player.set_vbr(vbr_str)

    def pause(self):
        self._player.pause()

    def resume(self):
        self._player.resume()

    def clear_live_room_msg(self):
        if self.has_regist_msg():
            self.unregist_msg()

    def stop(self):
        self._player.stop()

    def set_volume(self, vol):
        self._player.set_voume(vol)

    def fetch_data_provider(self):
        return self._player.fetch_data_provider()

    def _set_up_callback(self):
        self._player.get_vbr_list_callback = self._get_vbr_list_callback
        self._player.error_callback = self._error_callback
        self._player.video_ready_callback = self._video_ready_callback
        self._player.video_complete_callback = self._video_complete_callback
        self._player.report_stat_callback = self._report_stat_callback
        self._player.seek_complete_callback = self._seek_complete_callback

    def _clear_callback(self):
        if self._player:
            self._player.get_vbr_list_callback = None
            self._player.error_callback = None
            self._player.video_ready_callback = None
            self._player.video_complete_callback = None
            self._player.report_stat_callback = None
            self._player.seek_complete_callback = None
        return

    def _video_ready_callback(self, player):
        global_data.emgr.live_ready_event.emit()

    def _video_complete_callback(self, player):
        global_data.emgr.live_complete_event.emit()

    def _report_stat_callback(self, player, url):
        global_data.emgr.live_report_stat_event.emit()

    def _seek_complete_callback(self, player):
        global_data.emgr.live_seek_complete_event.emit()

    def _error_callback(self, player):
        global_data.emgr.live_error_event.emit()

    def _get_vbr_list_callback(self, player, cur_vbr, available_vbr_list):
        global_data.emgr.live_get_vbr_list_event.emit(cur_vbr, available_vbr_list)

    def config_http(self):
        server_base_str = self.get_base_server_str()
        region_str = self.get_region()
        from logic.gcommon.common_const.liveshow_const import CC_GAME_ID
        game_id_str = str(CC_GAME_ID)
        config_http = {'cmd': 'config-http','address': server_base_str,'region': region_str,'game_name': game_id_str}
        self._send_control_msg(config_http)

    def regist_msg(self):
        self._has_regist = True
        self.config_http()
        from logic.gcommon.common_const.liveshow_const import CC_GAME_ID
        region_str = self.get_region()
        server_base_str = self.get_base_server_str()
        game_id_str = str(CC_GAME_ID)
        uid = global_data.player.uid
        context = 0
        regist_cmd = {'cmd': 'regist',
           'servicecgi': '%s?game_name=%s&region=%s' % (server_base_str, game_id_str, region_str),
           'info': {'uid': uid,
                    'game_name': game_id_str,
                    'region': region_str
                    }
           }
        self._send_control_msg(regist_cmd)
        self.regist_msg_tick()

    def unregist_msg(self):
        if self.has_regist_msg():
            self.unsub_msg()
            self.unregist_msg_tick()
        self._has_regist = False

    def sub_msg(self):
        if not self.has_regist_msg():
            self.regist_msg()
        groups = self._get_sub_groups()
        sub_cmd = {'cmd': 'sub',
           'groups': groups
           }
        self._send_control_msg(sub_cmd)

    def unsub_msg(self):
        groups = self._get_sub_groups()
        sub_cmd = {'cmd': 'unsub',
           'groups': groups
           }
        self._send_control_msg(sub_cmd)

    def regist_msg_tick(self):
        self.unregist_msg_tick()
        import common.utils.timer as timer
        self._timer_id = global_data.game_mgr.register_logic_timer(self.msg_fetch_tick, 0.5, mode=timer.CLOCK)

    def unregist_msg_tick(self):
        if self._timer_id:
            global_data.game_mgr.unregister_logic_timer(self._timer_id)
            self._timer_id = None
        return

    def msg_fetch_tick(self):
        import cclive
        msg_list = cclive.fetch_msg()
        if msg_list:
            for msg in msg_list:
                self.dispatch_cc_msg(msg)

    def dispatch_cc_msg(self, msg):
        msg = json.loads(msg)
        cmd = msg['cmd']
        if cmd == 'pub':
            data = msg['data']
            channel_id = int(data['group'].split('_')[1])
            global_data.emgr.live_danmu_msg_event.emit(channel_id, data)

    def get_region(self):
        return 'China'

    def get_base_server_str(self):
        import game3d
        if game3d.get_platform() == game3d.PLATFORM_IOS or game3d.get_platform() == game3d.PLATFORM_ANDROID:
            if global_data.is_inner_server:
                return 'https://api.dev.cc.163.com/v1/distroommsg/serviceip'
            else:
                return 'https://api.cc.163.com/v1/distroommsg/serviceip'

        else:
            if global_data.is_inner_server:
                return 'http://api.dev.cc.163.com/v1/distroommsg/serviceip'
            return 'http://api.cc.163.com/v1/distroommsg/serviceip'

    def has_regist_msg(self):
        return self._has_regist

    def _get_sub_groups(self):
        channel_id = self._live_data['channel_id']
        groups = ['roomchat_%s', 'gamechat_%s']
        gen_groups = [ g % str(channel_id) for g in groups ]
        return gen_groups

    def _send_control_msg(self, dict):
        import cclive
        data = json.dumps(dict)
        cclive.control_msg(data, 0)

    def send_live_dammu(self, msg):
        channel_id = self._live_data.get('channel_id')
        kind = liveshow_const.CC_LIVE
        if global_data.player:
            global_data.player.send_live_dammu(msg, channel_id, kind)