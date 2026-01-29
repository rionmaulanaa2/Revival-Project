# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/patch_dctool.py
from __future__ import absolute_import
from __future__ import print_function
from dctool3 import DCTool
import version
import json
import C_file
import social
import game3d
import time
import six.moves.builtins
import profiling
import os
import six
SCN_DLD_PATCH_LIST_FAILED = 2
SCN_DLD_PATCH_FAILED = 6
SCN_DLD_PATCH_LIST_OK = 32
SCN_DLD_PATCH_OK = 36
SCN_PATCH_CHECK_FAILD = 106
SCN_PATCH_CHECK_OK = 206
HTTP_OK = '200'
HTTP_FAILED = '-1'
DCTOOL_INSTANCE = None
PATCH_UPDATE_PHASE_ENTER = 0
PATCH_UPDATE_PHASE_OK = 1
PATCH_UPDATE_PAHSE_FAILED = -1

def get_dctool_instane():
    global DCTOOL_INSTANCE
    if DCTOOL_INSTANCE is None:
        DCTOOL_INSTANCE = Dctool()
    return DCTOOL_INSTANCE


class Dctool(object):

    def __init__(self):
        super(Dctool, self).__init__()
        self.enable = False
        self.game_id = ''
        self.channel_name = 'internal'
        self.drpf_channel_name = None
        self.pc_engine_channel_name = 'inner'
        self.udid = 'pc'
        self.drpf_dict = {}
        self.device_info = {}
        self.reach_update_time = 0
        self.update_phase_extra_dict = {}
        self._is_first_patch = None
        self.init_dctool()
        return

    def get_device_info(self):
        try:
            device_info = {}
            device_info_s = game3d.netease_universal_log_info()
            device_infos = device_info_s.split(',')
            for info in device_infos:
                key_value = info.split('=')
                if len(key_value) != 2:
                    continue
                device_info[key_value[0]] = key_value[1]

            device_info['root_mark'] = game3d.is_outlaw_device()
            device_model = [
             profiling.get_device_model().replace(',', '_'),
             str(profiling.get_cpu_name(0)),
             str(profiling.get_cpu_count()),
             str(profiling.get_cpu_mhz(0)),
             str(profiling.get_video_card_name())]
            device_info['device_model'] = '#'.join(device_model)
            self.device_info = device_info
            return device_info
        except:
            print('[patch]init device info error')
            return {}

    def get_device_model(self):
        return self.device_info.get('device_model', 'unknown')

    def get_channel_name(self):
        return self.channel_name

    def get_udid(self):
        return self.udid

    def init_game_id(self):
        channel = social.get_channel()
        if channel and channel.name != 'null':
            self.channel_name = channel.name
            self.udid = channel.udid
            if channel.name in ('netease_global', 'steam'):
                channel_conf = C_file.get_res_file('confs/channel_info.json', '')
                channel_info = json.loads(channel_conf)
                platform_info = channel_info.get(str(game3d.get_platform()), channel_info['default'])
                app_name = game3d.get_app_name()
                conf_game_id = platform_info.get(app_name, platform_info['default'])
                self.game_id = conf_game_id
            else:
                self.game_id = six.moves.builtins.__dict__.get('game_id_by_magic', 'g93')
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                self.pc_engine_channel_name = self.channel_name
                if self.is_tw_package():
                    self.pc_engine_channel_name = self.pc_engine_channel_name + '_tw'
                second_channel = channel.get_prop_str('SECOND_CHANNEL')
                if second_channel:
                    self.pc_engine_channel_name = self.pc_engine_channel_name + '_' + second_channel
                try:
                    pc_engine_channel_flag = os.path.join(game3d.get_root_dir(), 'channel_flag')
                    with open(pc_engine_channel_flag, 'w') as tmp_file:
                        tmp_file.write(self.pc_engine_channel_name)
                except Exception as e:
                    print('[ERROR] write pc_engine_channel flag error:{}'.format(str(e)))

        else:
            self.game_id = six.moves.builtins.__dict__.get('game_id_by_magic', 'g93')
            return

    def need_download_by_cur_channel(self, path):
        if path.find('bin_patch') >= 0:
            rel_path = 'bin_patch/{0}/'.format(self.pc_engine_channel_name)
            is_channel_file = path.find(rel_path) >= 0
            is_common_file = len(path.split('/')) == 2
            return is_channel_file or is_common_file
        else:
            return True

    def get_ip(self):
        try:
            return game3d.get_ip_infos()[0]
        except:
            return ''

    def is_activated(self):
        doc_dir = game3d.get_doc_dir()
        activated_file_path = os.path.join(doc_dir, 'activation_log')
        return os.path.exists(activated_file_path)

    def set_activated(self):
        doc_dir = game3d.get_doc_dir()
        activated_file_path = os.path.join(doc_dir, 'activation_log')
        try:
            self.send_activation_info()
            with open(activated_file_path, 'w') as tmp_file:
                tmp_file.write('1')
        except Exception as e:
            print('[ERROR] SET ACTIVATION STATE_ERROR:', str(e))

    def send_activation_info(self):
        data_dict = {'type': 'Activation'}
        data_dict.update(self.drpf_dict)
        data_dict['active_time'] = int(time.time())
        self.drpf(json.dumps(data_dict))

    def send_aab_begin_info(self):
        data_dict = {'type': 'AabBegin'}
        data_dict.update(self.drpf_dict)
        data_dict['begin_time'] = int(time.time())
        self.drpf(json.dumps(data_dict))

    def send_aab_error_info(self, sdk_error_code):
        data_dict = {'type': 'AabError','error_code': int(sdk_error_code)}
        data_dict.update(self.drpf_dict)
        self.drpf(json.dumps(data_dict))

    def send_aab_stage_info(self, info_dict):
        data_dict = {'type': 'AabStage'}
        data_dict.update(info_dict)
        data_dict.update(self.drpf_dict)
        data_dict['begin_time'] = int(time.time())
        self.drpf(json.dumps(data_dict))

    def send_aab_finish_info(self):
        data_dict = {'type': 'AabFinish'}
        data_dict.update(self.drpf_dict)
        data_dict['finish_time'] = int(time.time())
        self.drpf(json.dumps(data_dict))

    def send_patch_heart_beat_info(self):
        data_dict = {'type': 'PatchHeartBeat'}
        cnt_beat = six.moves.builtins.__dict__.get('PATCH_BEAT', 0)
        cnt_beat += 1
        six.moves.builtins.__dict__['PATCH_BEAT'] = cnt_beat
        data_dict['beat'] = cnt_beat
        data_dict.update(self.drpf_dict)
        self.drpf(json.dumps(data_dict))

    def send_patch_process_info_info(self, info):
        try:
            data_dict = {'type': 'PatchProcessInfo'}
            data_dict.update(info)
            data_dict.update(self.drpf_dict)
            self.drpf(json.dumps(data_dict))
        except:
            pass

    def ext_drpf_info(self, type_name, info):
        try:
            data_dict = {'type': type_name}
            data_dict.update(info)
            data_dict.update(self.drpf_dict)
            self.drpf(json.dumps(data_dict))
        except:
            pass

    def set_update_phase_extra_dict(self, extra_dict):
        self.update_phase_extra_dict.update(extra_dict)

    def drpf(self, json_str):
        channel = social.get_channel()
        if not channel:
            return None
        else:
            return channel.drpf(json_str)
            return None

    def get_default_dis_channel(self):
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            if self.is_global_package():
                return 'google_play'
            if self.is_tw_package():
                return 'g93naxx2tw@google_play'
        elif game3d.get_platform() == game3d.PLATFORM_IOS:
            if self.is_global_package():
                return 'Apple_store'
            if self.is_tw_package():
                return 'g93naxx2tw@app_store'
        else:
            return self.get_channel_name()
        return self.get_channel_name()

    def get_app_channel(self):
        try:
            return self.get_default_dis_channel()
        except:
            pass

        return self.get_channel_name()

    def get_country_code(self):
        try:
            if hasattr(game3d, 'get_country_code'):
                return game3d.get_country_code().upper()
        except:
            pass

        return 'UNKNOWN'

    def get_drpf_app_channel(self):
        if not self.drpf_channel_name:

            def _drpf_channel_name():
                try:
                    if game3d.get_platform() == game3d.PLATFORM_ANDROID:
                        if self.is_global_package():
                            return 'google_play'
                        if self.is_tw_package():
                            return 'g93naxx2tw@google_play'
                    elif game3d.get_platform() == game3d.PLATFORM_IOS:
                        if self.is_tw_package():
                            return 'g93naxx2tw@app_store'
                        else:
                            return 'app_store'

                    channel = social.get_channel()
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
                    print('patch_dctool drpf app channel error:', str(e))

                return 'null'

            self.drpf_channel_name = _drpf_channel_name()
        return self.drpf_channel_name

    def get_drpf_dict(self):
        ret_dict = {}
        ret_dict['source'] = 'source'
        try:
            ret_dict['project'] = self.get_project_id()
            ret_dict['ip'] = self.get_ip()
            ret_dict['device_model'] = self.get_device_model()
            ret_dict['os_name'] = self.get_os_name()
            ret_dict['os_ver'] = self.get_os_ver()
            ret_dict['mac_addr'] = self.get_mac_addr()
            ret_dict['udid'] = self.get_udid()
            ret_dict['app_channel'] = self.get_drpf_app_channel()
            ret_dict['app_ver'] = version.get_cur_version_str()
            ret_dict['country_code'] = self.get_country_code()
            ret_dict['aarch_bit'] = self.get_bit_name()
            ret_dict['is_first_patch'] = self._is_first_patch
            return ret_dict
        except:
            return {}

    def get_bit_name(self):
        try:
            import sys
            if sys.maxsize > 4294967296:
                return '64bit'
            return '32bit'
        except:
            return 'except'

    def get_os_name(self):
        return self.device_info.get('os_name', 'unknown')

    def get_os_ver(self):
        return self.device_info.get('os_ver', 'unknown')

    def check_update(self, phase):
        try:
            from patch import network_utils
            json_paras = {}
            json_paras['network'] = network_utils.get_network_desc()
            cnt_time = int(time.time())
            if phase == PATCH_UPDATE_PHASE_ENTER:
                self.reach_update_time = cnt_time
                json_paras['reach_update_time'] = self.reach_update_time
            json_paras['update_time'] = cnt_time
            json_paras['type'] = 'Update'
            if phase in (PATCH_UPDATE_PHASE_ENTER,):
                json_paras['use_time'] = 0
            else:
                json_paras['use_time'] = cnt_time - self.reach_update_time
            json_paras['update_status'] = phase
            json_paras['bundleid'] = game3d.get_app_name()
            if self.update_phase_extra_dict:
                json_paras.update(self.update_phase_extra_dict)
                self.update_phase_extra_dict = {}
            json_paras.update(self.drpf_dict)
            self.drpf(json.dumps(json_paras))
        except:
            print('[PATCH] DRPF CHECK UPDATE ERROR')

    def check_activation(self):
        try:
            self.set_activated()
        except:
            print('[error] check activation error')

    def get_mac_addr(self):
        return self.device_info.get('mac_addr', 'unknown')

    def get_game_id(self):
        return self.game_id

    def get_detect_os(self):
        ret = 'Windows'
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            ret = 'iOS'
        elif game3d.get_platform() == game3d.PLATFORM_ANDROID:
            ret = 'Android'
        return ret

    def get_project_id(self):
        if self.game_id == 'g93':
            return 'g93'
        else:
            return 'g93na'

    def is_mainland_package(self):
        return self.game_id == 'g93'

    def is_tw_package(self):
        return six.moves.builtins.__dict__.get('channel_info', None) == 'g93natw' or game3d.get_app_name() == 'com.netease.g93natw'

    def is_global_package(self):
        return six.moves.builtins.__dict__.get('channel_info', None) == 'g93na' or self.game_id == 'g93na'

    def is_steam_channel(self):
        channel = social.get_channel()
        return channel and channel.name == 'steam'

    def init_dctool(self):
        self.init_game_id()
        try:
            setting_conf = C_file.get_res_file('confs/setting.json', '')
            setting = json.loads(setting_conf)
            self.enable = setting.get('dctool', False)
        except:
            pass

        try:
            doc_dir = game3d.get_doc_dir()
            patched_file_path = os.path.join(doc_dir, 'patched_log')
            self._is_first_patch = False if os.path.exists(patched_file_path) else True
        except Exception as e:
            print('[Except] process patched log except:', str(e))

        self.default_dict = {'user_id': '',
           'user_name': '',
           'ProductName': self.get_project_id(),
           'channel_name': self.channel_name,
           'os': self.get_detect_os()
           }
        if self.is_tw_package() or self.is_global_package():
            self.default_dict['region'] = '2'
        try:
            self.device_info = self.get_device_info()
            self.drpf_dict = self.get_drpf_dict()
        except Exception as e:
            print('[Except] get device info or drpf dict except:', str(e))

    def on_download_patch_list_failed(self, url, log):
        res_dict = {}
        res_dict['Scene'] = SCN_DLD_PATCH_LIST_FAILED
        res_dict['patchlist_url'] = url
        res_dict['http_code'] = HTTP_FAILED
        res_dict['error_log'] = log
        self.lazy_diagnose(res_dict)

    def on_download_patch_list_ok(self, url, spd, time_cost):
        res_dict = {}
        res_dict['Scene'] = SCN_DLD_PATCH_LIST_OK
        res_dict['patchlist_url'] = url
        res_dict['dl_speed'] = spd
        res_dict['time_cost'] = time_cost
        res_dict['http_code'] = HTTP_OK
        self.lazy_diagnose(res_dict)

    def on_download_patch_failed(self, url, dld_id, log, file_num, version):
        res_dict = {}
        res_dict['Scene'] = SCN_DLD_PATCH_FAILED
        res_dict['patch_url'] = url
        res_dict['download_id'] = int(float(dld_id))
        res_dict['http_code'] = HTTP_FAILED
        res_dict['error_log'] = log
        res_dict['file_num'] = file_num
        res_dict['patch_version'] = version
        self.lazy_diagnose(res_dict)

    def on_download_patch_ok(self, url, spd, time_cost, download_id, file_num, patch_version, file_size):
        res_dict = {}
        res_dict['Scene'] = SCN_DLD_PATCH_OK
        res_dict['patch_url'] = url
        res_dict['dl_speed'] = spd
        res_dict['time_cost'] = time_cost
        res_dict['download_id'] = int(float(download_id))
        res_dict['http_code'] = HTTP_OK
        res_dict['file_num'] = file_num
        res_dict['patch_version'] = patch_version
        res_dict['file_size'] = file_size
        res_dict['error_log'] = -1
        self.lazy_diagnose(res_dict)

    def on_patch_check_failed(self, url, error_log):
        res_dict = {}
        res_dict['Scene'] = SCN_PATCH_CHECK_FAILD
        res_dict['patch_check_result'] = 'false'
        res_dict['patch_url'] = url
        res_dict['http_code'] = HTTP_FAILED
        res_dict['error_log'] = error_log
        self.lazy_diagnose(res_dict)

    def on_patch_check_ok(self, url, file_size, file_num, time_cost):
        res_dict = {}
        res_dict['Scene'] = SCN_PATCH_CHECK_OK
        res_dict['patch_check_result'] = 'true'
        res_dict['download_newpatch'] = 'true' if file_size > 0 else 'false'
        res_dict['download_id'] = int(float(time.time()))
        res_dict['patch_url'] = url
        res_dict['http_code'] = HTTP_OK
        res_dict['file_num'] = file_num
        res_dict['file_size'] = file_size
        res_dict['time_cost'] = time_cost
        res_dict['error_log'] = -1
        self.lazy_diagnose(res_dict)

    def lazy_diagnose(self, json_dict):
        if self.enable:
            json_dict.update(self.default_dict)
            print('@@@@@@@@@@ data-detect', json_dict['Scene'], json_dict.get('region', None))
            print('detect dict', json.dumps(json_dict))
            DCTool.lazy_diagnose(json.dumps(json_dict))
        return