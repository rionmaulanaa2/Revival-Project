# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/feedback/echoes.py
from __future__ import absolute_import
from __future__ import print_function
import game3d
import social
import six
PATCH = 1
LOBBY = 2
LOGIN = 3
BATTLE = 4
DEFAULT_FEEDBACK_URL = 'https://share.easebar.com/ace/2018/quick-feedback/en/'
LANG_TO_URL = {'cn': 'https://share.easebar.com/ace/2018/quick-feedback/',
   'en': 'https://share.easebar.com/ace/2018/quick-feedback/en/',
   'tw': 'https://share.easebar.com/ace/2018/quick-feedback/zhtw/',
   'id': 'https://share.easebar.com/ace/2018/quick-feedback/id/',
   'jp': 'https://share.easebar.com/ace/2018/quick-feedback/jp/',
   'th': 'https://share.easebar.com/ace/2018/quick-feedback/th/'
   }
player_info = {}
server_info = {'server_list_url': '','server_name': '','server_host': ''}

def set_server_info(key, value):
    server_info[key] = value


def show_feedback_view(stage):
    if stage != PATCH:
        from common.platform.dctool import interface
        if interface.is_mainland_package():
            global_data.ui_mgr.show_ui('GameFeedbackUI', 'logic.comsys.setting_ui')
            return
    if game3d.get_app_name() == 'com.netease.g93natw':
        show_tw_customer_service_view(stage)
        return
    else:
        if stage > PATCH:
            from logic.gcommon.common_utils.local_text import get_cur_lang_name
            lang_name = get_cur_lang_name()
        else:
            try:
                from patch import patch_dctool
                dc_tool_inst = patch_dctool.get_dctool_instane()
                lang_name = 'cn' if dc_tool_inst.is_mainland_package() else 'en'
            except Exception as e:
                lang_name = 'cn'
                print('show feedback view except:', str(e))

        web_url = '{0}?query={1}'.format(LANG_TO_URL.get(lang_name, DEFAULT_FEEDBACK_URL), stage)
        if game3d.get_platform() not in (game3d.PLATFORM_ANDROID, game3d.PLATFORM_IOS):
            game3d.open_url(web_url)
            print(server_info, 'will be feedback on ios/android platform')
            return
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            channel = social.get_channel()
            os_ver = channel.get_prop_str('SDC_LOG_OS_VER')
            if os_ver.startswith('8'):
                game3d.open_url(web_url)
                return
        login_status = '1' if stage > PATCH else '0'
        client_info = {}
        player_uid = ('patching', )
        player_name = ('patching', )
        battle_id = 0
        player_pos = None
        custom_webview_float = None
        if stage > PATCH:
            from common.platform.device_info import DeviceInfo
            client_info = DeviceInfo.get_instance().get_device_info()
            device_model = DeviceInfo.get_instance().get_device_model()
            idx = device_model.find('#')
            if idx != -1:
                device_model = device_model[0:idx]
                if device_model in ('iPhone10_3', 'iPhone10_6'):
                    custom_webview_float = '6'
                    print('Detect ipx device, and set WEBVIEW_CLBTN_FLOAT value to 6')
            if global_data.player:
                player_uid = global_data.player.uid
                player_name = global_data.player.get_name()
                battle = global_data.player.get_battle()
                if battle:
                    battle_id = battle.get_battle_tid()
                    if global_data.player.logic:
                        player_pos = global_data.player.logic.ev_g_position() or global_data.player.logic.ev_g_model_position()
                        if player_pos:
                            player_pos = [
                             int(player_pos.x), int(player_pos.y), int(player_pos.z)]
            else:
                player_uid = 'login'
                player_name = 'login'
                last_login_info = read_last_login_info('login', 'login')
                if last_login_info:
                    player_uid, player_name = last_login_info
        else:
            last_login_info = read_last_login_info('patching', 'patching')
            if last_login_info:
                player_uid, player_name = last_login_info
        if stage > PATCH:
            from common.platform.dctool import interface
            game_id = interface.get_game_id()
        else:
            try:
                from patch import patch_dctool
                game_id = patch_dctool.get_dctool_instane().get_game_id()
            except Exception as e:
                game_id = 'g93'
                print('show feedback view except:', str(e))

        custom_log = {'project': game_id}
        if player_pos:
            custom_log['battle_id'] = str(battle_id)
            custom_log['player_pos'] = str(player_pos)
        para_dict = {'ECHOES_URL': web_url,'ECHOES_TID': '3684901',
           'UDID': client_info.get('udid', ''),
           'ECHOES_USR_STATUS': login_status,
           'SDC_LOG_OS_VER': client_info.get('os_ver', 'android'),
           'SDC_LOG_APP_VER': client_info.get('app_ver', '1.0.0'),
           'ECHOES_APPVER': client_info.get('app_ver', '1.0.0'),
           'ECHOES_SERVERLIST': str(server_info['server_list_url']),
           'USERINFO_HOSTNAME': str(server_info['server_name']),
           'USERINFO_HOSTID': str(server_info['server_host']),
           'ECHOES_USR_AVATARID': '',
           'USERINFO_UID': str(player_uid),
           'USERINFO_NAME': str(player_name),
           'ECHOES_CUSTOM_LOG': str(custom_log),
           'WEBVIEW_FULLFIT': '1',
           'WEBVIEW_CLBTN': '0'
           }
        if custom_webview_float:
            para_dict['WEBVIEW_CLBTN_FLOAT'] = custom_webview_float
        channel = social.get_channel()
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            channel.set_prop_int('WEBVIEW_MODE', 0)
        else:
            channel.set_prop_int('WEBVIEW_MODE', 1)
        for cur_key, cur_value in six.iteritems(para_dict):
            channel.set_prop_str(cur_key, cur_value)

        channel.open_echoes()
        channel.set_prop_int('WEBVIEW_MODE', 1)
        return


def close_feedback_view():
    if game3d.get_platform() in (game3d.PLATFORM_ANDROID, game3d.PLATFORM_IOS):
        channel = social.get_channel()
        channel.close_web_view()
        return


def show_tw_customer_service_view(stage, dict_args=None):
    if stage <= PATCH or not (global_data and global_data.player or dict_args):
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            web_url = 'https://support.longeplay.com.tw/service_quick?param_game_id=G93PC'
        else:
            web_url = 'https://game.longeplay.com.tw/service_quick?param_game_id=G93&site=long_e'
    else:
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            web_url = 'https://support.longeplay.com.tw/service_quick?'
            game_id = 'G93PC'
            key = 'x3565qszd8'
        else:
            web_url = 'https://game.longeplay.com.tw/service_quick?'
            game_id = 'G93'
            key = 'pgggma3687'
        from common.platform.device_info import DeviceInfo
        from common.utils import network_utils
        import hashlib
        import six.moves.urllib.request
        import six.moves.urllib.parse
        import six.moves.urllib.error
        client_info = DeviceInfo.get_instance().get_device_info()
        account_id = global_data.channel.get_sdk_uid()
        if not account_id:
            print('can get ac_id in tw_customer_service call.')
            return
        player_level = None
        if global_data and global_data.player:
            player_uid = global_data.player.uid
            player_name = global_data.player.get_name()
            player_level = global_data.player.get_lv()
        else:
            player_uid = dict_args.get('uid')
            player_name = dict_args.get('char_name')
        is_using_wifi = 0
        if network_utils.g93_get_network_type() == network_utils.TYPE_WIFI:
            is_using_wifi = 1
        url_params_dict = {'game_id': game_id,'partner_uid': str(account_id),
           'in_game_id': str(player_uid),
           'server_name': server_info.get('server_host', 0),
           'character_name': player_name,
           'usr_device': client_info.get('os_name', 'unknow'),
           'os_ver': client_info.get('os_ver', 'unknow'),
           'app_ver': client_info.get('app_ver', '1.0.0'),
           'network': str(is_using_wifi),
           'key': key
           }
        if player_level is not None:
            url_params_dict['level'] = str(player_level)
        url_params_str = six.moves.urllib.parse.urlencode(url_params_dict)
        m = hashlib.md5()
        m.update(six.ensure_binary(url_params_str))
        url_params_dict['key'] = m.hexdigest()
        url_params_str = six.moves.urllib.parse.urlencode(url_params_dict)
        web_url = web_url + url_params_str
    game3d.open_url(web_url)
    return


def read_last_login_info(default_player_uid='patching', default_player_name='patching'):
    try:
        import os
        path = os.path.join(game3d.get_doc_dir(), 'll_inf')
        with open(path, 'r') as f:
            line = f.readline()
            line = line.decode('utf-8')
            player_uid, player_name = line.split('#')
            return (
             str(player_uid), str(player_name))
    except Exception as e:
        print('echoes failed to read_last_login_info except,', str(e))

    return (default_player_uid, default_player_name)


def write_last_login_info(player_uid, player_name):
    print('echoes write_last_login_info begin ', player_uid, player_name)
    try:
        import os
        path = os.path.join(game3d.get_doc_dir(), 'll_inf')
        with open(path, 'w') as f:
            line = str(player_uid) + '#' + str(player_name)
            line = six.ensure_str(line)
            f.write(line)
    except Exception as e:
        print('echoes failed to write_last_login_info except,', str(e))

    print('echoes write_last_login_info done.')