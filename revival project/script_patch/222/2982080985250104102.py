# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/device_info.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import game3d
import profiling
from common.framework import Singleton
import version
from common.utils import network_utils
from common.platform.dctool import interface
from logic.gcommon.common_utils.local_text import get_cur_text_lang
import time
import common.utils.timer as timer
from common.platform.third_part_app_utils import gen_tpa_data_for_launch_report

class DeviceInfo(Singleton):
    ALIAS_NAME = 'deviceinfo'

    def init(self):
        self.device_info = {}
        self._is_full_screen = None
        self._screen_margins = None
        self._is_emulator = None
        self._pids = []
        self._all_proc_name = []
        self._count = 0
        self._index = 0
        self._timer = None
        self._upload_timer = None
        self._score = None
        return

    def start_upload_proc_info_pc(self):
        if game3d.get_platform() != game3d.PLATFORM_WIN32:
            return
        try:
            import _psutil_windows
        except:
            return

        if self._upload_timer:
            return
        self.upload_process_info()

        def tick_callback():
            self.upload_process_info()

        self._upload_timer = global_data.game_mgr.register_logic_timer(tick_callback, 1200, mode=timer.CLOCK)

    def get_device_model(self):
        return self.device_info.get('device_model', 'unknown')

    def get_mac_addr(self):
        return self.device_info.get('mac_addr', 'unknown')

    def get_udid(self):
        return self.device_info.get('udid', 'unknown')

    def get_isp(self):
        return self.device_info['isp']

    def get_ip(self):
        return game3d.get_ip_infos()[0]

    def get_network(self):
        return network_utils.get_network_desc()

    def get_os_name(self):
        return self.device_info.get('os_name', 'unknown')

    def get_os_ver(self):
        return self.device_info.get('os_ver', 'unknown')

    def get_device_width(self):
        return self.device_info.get('device_width', '0')

    def get_device_height(self):
        return self.device_info.get('device_height', '0')

    def is_open_3d_touch(self):
        if hasattr(game3d, 'get_3dtouch_status'):
            return game3d.get_3dtouch_status()
        else:
            return False

    def get_install_dir(self):
        return self.device_info.get('root_dir', 'unknown')

    def get_sdk_version(self):
        return self.device_info.get('sdk_ver', '1.0')

    def get_device_info(self):
        return self.device_info

    def is_huawei_device(self):
        return False
        if G_IS_NA_USER:
            return False
        return 'huawei' in self.device_info.get('device_manufacturer', 'unknown').lower()

    def get_device_manufacturer(self):
        return self.device_info.get('device_manufacturer', 'unknown')

    def init_device_info(self):
        import profiling
        device_info = {}
        device_info_s = game3d.netease_universal_log_info()
        device_infos = device_info_s.split(',')
        for info in device_infos:
            key_value = info.split('=')
            if len(key_value) != 2:
                continue
            device_info[key_value[0]] = key_value[1]

        device_info['ip'] = self.get_ip()
        device_info['network_type'] = self.get_network()
        device_info['root_mark'] = game3d.is_outlaw_device()
        device_model = [
         device_info.get('device_manufacturer', 'unknown'),
         profiling.get_device_model().replace(',', '_'),
         str(profiling.get_cpu_name(0)),
         str(profiling.get_cpu_count()),
         str(profiling.get_cpu_mhz(0)),
         str(profiling.get_video_card_name())]
        device_info['device_model'] = '#'.join(device_model)
        device_info['game_version'] = version.get_cur_version_str()
        device_info['game_tag'] = version.get_tag()
        from common.platform.channel import Channel
        channel = Channel()
        device_info['os_ver'] = channel.get_os_ver()
        device_info['sdk_ver'] = channel.get_sdk_version()
        device_info['app_channel'] = channel.get_app_channel()
        device_info['app_ver'] = version.get_cur_version_str()
        device_info['network'] = self.get_network()
        device_info['is_free_login'] = channel.is_free_login
        device_info['idfa'] = self.get_idfa()
        device_info['udid'] = channel.get_udid()
        device_info['package_type'] = interface.get_package_type()
        device_info['time_zone'] = self._get_timezone_offset()
        device_info['is_emulator'] = self.is_emulator()
        device_info['aarch_bit'] = self.get_bit_name()
        tpa_data_dict = gen_tpa_data_for_launch_report()
        if tpa_data_dict:
            device_info['third_party_app_data'] = tpa_data_dict
            global_data.tpa_launch_data = tpa_data_dict
        from ext_package.ext_decorator import has_kongdao_ext, has_skin_ext, has_video_ext, has_audio_ext, has_pve_ext
        device_info['kongdao_ext'] = has_kongdao_ext()
        device_info['skin_ext'] = has_skin_ext()
        device_info['video_ext'] = has_video_ext()
        device_info['audio_ext'] = has_audio_ext()
        device_info['pve_ext'] = has_pve_ext(1)
        self.device_info = device_info
        return device_info

    def update_ext_info(self):
        from ext_package.ext_decorator import has_kongdao_ext, has_skin_ext, has_video_ext, has_audio_ext, has_pve_ext
        self.device_info['kongdao_ext'] = has_kongdao_ext()
        self.device_info['skin_ext'] = has_skin_ext()
        self.device_info['video_ext'] = has_video_ext()
        self.device_info['audio_ext'] = has_audio_ext()
        self.device_info['pve_ext'] = has_pve_ext(1)

    def get_bit_name(self):
        try:
            import sys
            if sys.maxsize > 4294967296:
                return '64bit'
            return '32bit'
        except:
            return 'except'

    def drop_tpa_launch_data(self):
        if 'third_party_app_data' in self.device_info:
            del self.device_info['third_party_app_data']

    def on_lang_changed(self):
        self.device_info['lang'] = get_cur_text_lang()

    def _get_timezone_offset(self):
        now = time.localtime()
        if time.daylight and now.tm_isdst:
            offset = time.altzone
        else:
            offset = time.timezone
        return offset / -3600

    def get_idfa(self):
        try:
            if hasattr(game3d, 'get_idfa'):
                idfa = game3d.get_idfa()
            else:
                idfa = ''
            return idfa
        except:
            return ''

    def is_can_full_screen(self):
        if self._is_full_screen is None:
            screen_margins = self.get_screen_adapt_margins()
            self._is_full_screen = False if screen_margins else True
        return self._is_full_screen

    def get_screen_adapt_margins(self):
        if self._screen_margins is None:
            device_model_name = self.get_device_model_name()
            from common.cfg import confmgr
            screen_conf = confmgr.get('c_screen_adapt')
            fit_rule = self.check_device_name_prefix_fit(device_model_name, six_ex.keys(screen_conf))
            if fit_rule:
                self._screen_margins = screen_conf[fit_rule]
            else:
                res = game3d.is_notch_screen()
                print('is_notch_screen', res)
                if not isinstance(res, bool):
                    is_notch, left, right, top, down = res
                else:
                    is_notch = res
                is_notch = is_notch or bool(global_data.force_notch_screen)
                if is_notch:
                    if game3d.get_platform() == game3d.PLATFORM_ANDROID:
                        self._screen_margins = screen_conf['android_default']
                    else:
                        self._screen_margins = screen_conf['iphone_default']
                else:
                    self._screen_margins = {}
        return self._screen_margins

    def refresh_screen_margin_info(self):
        self._screen_margins = None
        self._is_full_screen = None
        self.is_can_full_screen()
        return

    def get_device_model_name(self):
        device_model_name = profiling.get_device_model()
        if device_model_name:
            device_model_name = device_model_name.lower()
        return device_model_name

    def get_process_info(self):
        import os
        import re
        import game3d
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            return ''
        info = []
        try:
            output = os.popen('ps')
            out_text = output.read()
            output.close()
        except:
            out_text = ''

        relink = 'com.*?\n'
        item_text = re.findall(relink, out_text)
        for text in item_text:
            text = text.replace('\n', ';')
            info.append(text)

        return ''.join(info)

    def get_process_info_pc_async(self, callback=None):
        try:
            import _psutil_windows
        except:
            return

        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        self._pids = _psutil_windows.pids()
        if not self._pids:
            return
        else:
            self._count = len(self._pids)
            self._index = 0
            self._all_proc_name = []

            def process_name_callback():
                try:
                    name = _psutil_windows.proc_name(self._pids[self._index])
                    self._all_proc_name.append(name)
                except:
                    if callback:
                        callback(self._all_proc_name)
                    global_data.game_mgr.unregister_logic_timer(self._timer)
                    self._timer = None
                    return

                self._index += 1
                if self._index >= self._count:
                    global_data.game_mgr.unregister_logic_timer(self._timer)
                    self._timer = None
                    if callback:
                        callback(self._all_proc_name)
                return

            self._timer = global_data.game_mgr.register_logic_timer(process_name_callback, 1, mode=timer.LOGIC)
            return

    def upload_process_info(self):

        def callback--- This code section failed: ---

 334       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  STORE_FAST            1  'player'

 335       9  LOAD_FAST             1  'player'
          12  POP_JUMP_IF_FALSE    44  'to 44'

 336      15  LOAD_FAST             1  'player'
          18  LOAD_ATTR             2  'call_server_method'
          21  LOAD_CONST            1  'client_sa_log'
          24  LOAD_CONST            2  'ClientInfo'
          27  BUILD_MAP_1           1 
          30  BUILD_MAP_3           3 
          33  STORE_MAP        
          34  BUILD_TUPLE_2         2 
          37  CALL_FUNCTION_2       2 
          40  POP_TOP          
          41  JUMP_FORWARD          0  'to 44'
        44_0  COME_FROM                '41'

Parse error at or near `STORE_MAP' instruction at offset 33

        self.get_process_info_pc_async(callback)

    def check_device_name_prefix_fit(self, device_name, rule_set):
        import re
        for rule in rule_set:
            if re.match(rule.lower(), device_name):
                return rule

        return

    def is_ios_ver_13_1(self):
        if game3d.get_platform() == game3d.PLATFORM_IOS and global_data.channel and global_data.channel.get_os_ver() == '13.10':
            return True
        return False

    def is_emulator(self):
        if self._is_emulator is None:

            def _is_emulator():
                if global_data.is_android_pc:
                    return True
                if game3d.get_platform() != game3d.PLATFORM_ANDROID:
                    return False
                try:
                    if global_data.channel.check_emulator_local():
                        return True
                    if global_data.channel.check_emulator_remote():
                        return True
                    if global_data.feature_mgr.is_support_yidun_simulator_detect():
                        ret, name = global_data.channel.yidun_request(1, '')
                        if ret and name and not name.endswith('None'):
                            return True
                except:
                    return False

                return False

            self._is_emulator = _is_emulator()
        return self._is_emulator

    def set_emulator(self, flag):
        self._is_emulator = flag
        if self.device_info:
            self.device_info['is_emulator'] = flag

    def set_device_score(self, val):
        self._score = val

    def get_device_score(self):
        return self._score