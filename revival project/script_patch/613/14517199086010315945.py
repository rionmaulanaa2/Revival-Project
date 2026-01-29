# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impSettings.py
from __future__ import absolute_import
import six
from pickle import FALSE
from threading import local
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Bool, Dict, Str
from logic.gutils import micro_webservice_utils
import logic.gutils.delay as delay
from logic.comsys.archive import archive_key_const
from logic.gcommon.common_const.web_const import SETTINGS_REQUEST_READ, SETTINGS_REQUEST_WRITE
from logic.gcommon.item.item_const import FASHION_POS_WEAPON_SFX
import json
TIME_OUT_TIME = 2
REPEAT_TIMES = 5

class impSettings(object):

    def _init_settings_from_dict(self, bdict):
        self._get_settings_handler = None
        self._set_settings_handler = None
        self.settings_version = bdict.get('version', 0)
        self.settings_search_func_dict = {'weapon_settings': self.find_init_weapons_setting,
           'fashion_scheme_settings': self.find_fashion_scheme_setting,
           'user_setting': self.find_user_setting
           }
        self.can_write = False
        self.sync_version = 0
        return

    def get_settings_version(self):
        return self.settings_version

    def _on_login_settings_success(self):
        self.check_settings_version()

    def cancel_get_handler(self):
        if self._get_settings_handler:
            delay.cancel(self._get_settings_handler)
            self._get_settings_handler = None
        return

    def cancel_set_handler(self):
        if self._set_settings_handler:
            delay.cancel(self._set_settings_handler)
            self._set_settings_handler = None
        return

    def _repeat_settings_request(self, isread, data, cb, repeat_times):
        if isread:
            self._get_settings_handler = None
        else:
            self._set_settings_handler = None
        if repeat_times <= 0:
            if isread:
                local_settings = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {})
                if self.check_data_transfer(local_settings):
                    self.update_data(local_settings)
                self.sync_settings()
            return
        else:
            if isread:
                self._get_settings_handler = delay.call(TIME_OUT_TIME, lambda : self._repeat_settings_request(isread, data, cb, repeat_times - 1))
                micro_webservice_utils.micro_service_request('SettingsService', data, cb)
            else:
                self._set_settings_handler = delay.call(TIME_OUT_TIME, lambda : self._repeat_settings_request(isread, data, cb, repeat_times - 1))
                micro_webservice_utils.micro_service_post('SettingsService', data, cb)
            return

    def check_settings_version(self):
        local_version = 0
        local_settings = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {})
        if local_settings:
            local_version = local_settings.get('version', 0)
        if not self.in_user_setting_test and 'user_setting' in local_settings:
            game3d.post_hunter_message('microservice', 'wrong local settings')
        if local_version < self.settings_version:
            self.settings_version = local_version
            self.cancel_get_handler()
            self._repeat_settings_request(True, {'req_type': SETTINGS_REQUEST_READ,'data': json.dumps(None)}, self.get_settings_cb, REPEAT_TIMES)
        elif local_version == self.settings_version:
            self.can_write = True
            if self.check_data_transfer(local_settings):
                self.update_data(local_settings)
            self.sync_settings()
        else:
            self.can_write = True
            self.check_data_transfer(local_settings)
            self.update_data(local_settings)
            self.sync_settings()
        return

    def check_data_transfer(self, data):
        need_transfer = False
        for k, _ in six.iteritems(self.settings_search_func_dict):
            if k not in data:
                settings_data = self.settings_search_func_dict[k]()
                if settings_data:
                    need_transfer = True
                    data[k] = settings_data

        return need_transfer

    def get_settings_cb(self, res, rawdata=None):
        if not global_data.player:
            return
        if res and res.get('msg', '') == 'success':
            self.cancel_get_handler()
            self.can_write = True
            data = res.get('data', {})
            if data.get('version', 0) <= self.settings_version:
                return
            self.sync_version = self.settings_version = data.get('version', 0)
            if self.check_data_transfer(data):
                self.update_data(data)
            else:
                self.save_local_settings(data)
            self.sync_settings()
            self.call_server_method('update_settings_version', (self.settings_version,))
            global_data.emgr.on_new_user_setting.emit()
        else:
            local_settings = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {})
            if self.check_data_transfer(local_settings):
                self.update_data(local_settings)
            self.sync_settings()

    def set_settings_cb(self, res, rawdata=None):
        if not global_data.player:
            return
        if res and res.get('msg', '') == 'success':
            if self.sync_version < self.settings_version:
                self.sync_version = self.settings_version
                self.call_server_method('update_settings_version', (self.settings_version,))
        self.cancel_set_handler()

    def find_init_weapons_setting(self):
        data = {'DeathBattle': global_data.achi_mgr.get_general_archive_data_value(archive_key_const.KEY_LAST_DEATH_CHOOSE_WEAPON, {}),
           'HumanDeathBattle': global_data.achi_mgr.get_general_archive_data_value(archive_key_const.KEY_LAST_HUMAN_DEATH_CHOOSE_WEAPON, {})
           }
        data['DeathBattle'] or data.pop('DeathBattle', None)
        data['HumanDeathBattle'] or data.pop('HumanDeathBattle', None)
        return data

    def find_fashion_scheme_setting(self):
        return None

    @rpc_method(CLIENT_STUB, (Dict('fashion_scheme_setting'),))
    def response_fashion_scheme_setting(self, fashion_scheme_setting):
        local_settings = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {})
        local_settings['fashion_scheme_settings'] = fashion_scheme_setting
        self.update_data(local_settings)

    def find_user_setting(self):
        if not self.in_user_setting_test:
            return None
        else:
            self.call_server_method('request_user_setting', ())
            return None

    @rpc_method(CLIENT_STUB, (Dict('user_setting'),))
    def response_user_setting(self, user_setting):
        local_settings = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {})
        local_settings['user_setting'] = user_setting
        self.update_data(local_settings)
        global_data.emgr.on_new_user_setting.emit()

    def update_data(self, data):
        if not self.can_write:
            self.save_local_settings(data)
            return
        self.settings_version = data.get('version', 0) + 1
        data['version'] = self.settings_version
        self.save_local_settings(data)
        self.cancel_set_handler()
        self._repeat_settings_request(False, {'req_type': SETTINGS_REQUEST_WRITE,'data': json.dumps(data)}, self.set_settings_cb, REPEAT_TIMES)

    def sync_settings(self):
        self.sync_role_fashion()

    def sync_role_fashion(self):
        from logic.gutils import dress_utils
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        if not global_data.player:
            return
        else:
            item_data = global_data.player.get_item_by_no(self.role_id)
            if not item_data:
                return
            fashion_data = item_data.get_fashion()
            dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
            top_skin_id = dress_utils.get_top_skin_id_by_skin_id(dressed_clothing_id)
            local_settings = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {})
            fashion_dict, _ = dress_utils.skin_plan_to_fashion_dict(local_settings.get('fashion_scheme_settings', {}).get(str(self.role_id), {}).get(str(dressed_clothing_id), {}))
            top_skin_dict, _ = dress_utils.skin_plan_to_fashion_dict(local_settings.get('fashion_scheme_settings', {}).get(str(self.role_id), {}).get(str(top_skin_id), {}))
            is_change = False
            is_change_sec_skin = False
            for part, val in six.iteritems(fashion_data):
                if part == FASHION_POS_WEAPON_SFX:
                    continue
                if fashion_dict.get(part, None) != fashion_data.get(part, None):
                    is_change = True
                fashion_dict[part] = val

            pop_list = []
            for part, val in six.iteritems(fashion_dict):
                if part not in fashion_data:
                    pop_list.append(part)
                    is_change = True

            for part in pop_list:
                fashion_dict.pop(part)

            if dressed_clothing_id != top_skin_dict.setdefault(FASHION_POS_SUIT, top_skin_id):
                is_change = True
                is_change_sec_skin = True
                top_skin_dict[FASHION_POS_SUIT] = dressed_clothing_id
            if is_change:
                skin_plan = dress_utils.fashion_dict_to_skin_plan(fashion_dict)
                new_settings = {'version': self.settings_version,'fashion_scheme_settings.{}.{}'.format(self.role_id, dressed_clothing_id): skin_plan}
                if is_change_sec_skin:
                    top_skin_plan = dress_utils.fashion_dict_to_skin_plan(top_skin_dict)
                    new_settings.update({'fashion_scheme_settings.{}.{}'.format(self.role_id, top_skin_id): top_skin_plan})
                self.update_data(new_settings)
            return

    def save_local_settings(self, data):
        local_settings = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {})
        if type(local_settings) != dict:
            local_settings = {}
        self._parse_data(data, local_settings)
        global_data.achi_mgr.set_cur_user_archive_data('local_settings', local_settings)

    def _parse_data(self, data, local_settings):
        try:
            for k, v in six.iteritems(data):
                dict_to_change = local_settings
                key_list = k.split('.')
                last_key = key_list.pop(-1)
                for key in key_list:
                    if key not in dict_to_change:
                        dict_to_change[key] = {}
                    dict_to_change = dict_to_change.get(key, None)

                dict_to_change[last_key] = v

        except Exception as e:
            self.logger.error('parse error :%s', e)

        return

    @rpc_method(CLIENT_STUB, ())
    def reset_local_settings(self):
        global_data.achi_mgr.set_cur_user_archive_data('local_settings', {})

    def _destroy_settings(self):
        self.settings_search_func_dict = {}
        self.cancel_get_handler()
        self.cancel_set_handler()