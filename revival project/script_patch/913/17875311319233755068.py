# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impUserSetting.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
from logic.gcommon.common_const import ui_operation_const
from logic.gcommon.common_const import setting_const
from logic.comsys.archive.archive_manager import ArchiveManager
import device_compatibility
import six.moves.cPickle
import copy
from common.utils import pc_platform_utils
import six
SCALE_DEGREE = 10000.0

def deserialize_setting_2_val(value):
    if isinstance(value, six.binary_type):
        value = six.moves.cPickle.loads(value)
    elif isinstance(value, six.text_type):
        value = value.encode('utf-8')
        value = six.moves.cPickle.loads(value)
    return value


class impUserSetting(object):

    def _init_usersetting_from_dict(self, bdict):
        self.init_setting_const()
        self.in_user_setting_test = bdict.get('in_user_setting_test', False)
        if not self.in_user_setting_test:
            setting_dict = bdict.get('setting', None) if 1 else None
            self._server_setting_dict = setting_dict
            self.user_data_archive = ArchiveManager().get_archive_data('setting')
            self._user_default_setting_dict = {}
            server_setting_dict_2 = copy.deepcopy(self.in_user_setting_test or bdict.get('setting_dict_2', {}) if 1 else {})
            self._deserialize_setting_dict_2(server_setting_dict_2)
            self._server_setting_dict_2 = server_setting_dict_2
            key = ui_operation_const.USER_LOGINED_BEFORE_KEY_FORMAT % self.uid
            sync_server_settings_to_local_2 = True
            if sync_server_settings_to_local_2:
                self._sync_setting_to_local_2(server_setting_dict_2)
            self._setting_no = self.in_user_setting_test or str(bdict.get('setting_no', '0')) if 1 else '0'
            self._pve_setting_no = self.in_user_setting_test or str(bdict.get('pve_setting_no', '0')) if 1 else '0'
            self._custom_setting = self.in_user_setting_test or bdict.get('custom_setting', {}) if 1 else {}
            self._custom_setting_cache = {}
            self._custom_resolution_data = {}
            self._is_old_custom_data = {}
            default_quality, default_reso, fps = device_compatibility.get_default_quality_and_resolution()
            ui_operation_const.SETTING_CONF[ui_operation_const.QUALITY_LEVEL_KEY] = default_quality
            ui_operation_const.SETTING_CONF[ui_operation_const.PVE_QUALITY_LEVEL_KEY] = default_quality
            ui_operation_const.SETTING_CONF[ui_operation_const.QUALITY_RESOLUTION_KEY] = default_reso
            ui_operation_const.SETTING_CONF[ui_operation_const.QUALITY_HIGH_FRAME_RATE_KEY] = fps
            self._user_default_setting_dict.update(ui_operation_const.SETTING_CONF)
            if global_data.channel.get_app_channel() == 'steam':
                self._user_default_setting_dict.update(ui_operation_const.SETTING_CONF_STEAM)
            if G_IS_NA_PROJECT:
                self._user_default_setting_dict.update(ui_operation_const.SETTING_CONF_SEA)
            if global_data.is_pc_mode:
                self._user_default_setting_dict.update(ui_operation_const.PC_SETTING_CONF_DEFAULT_OVERRIDES)
            if pc_platform_utils.is_pc_hight_quality():
                self._user_default_setting_dict.update(ui_operation_const.PC_HIGHT_QUALITY_SETTING_CONF)
            self._modify_cache = {}
            self.init_camera_sst_from_conf()
            if not setting_dict or ui_operation_const.NEWBIE_PASS_HIDE_UI not in setting_dict:
                setting_dict = setting_dict or {}
            setting_dict[ui_operation_const.NEWBIE_PASS_HIDE_UI] = 0
        if setting_dict is not None:
            self.init_setting_from_dict(setting_dict)
        if self._custom_setting:
            self.init_custom_setting_from_server()
        self.bind_setting_user_event(True)
        self.cur_posture_setting = self.read_local_setting(ui_operation_const.OPE_POSTURE_KEY, ui_operation_const.OPE_POSTURE_DEF_SETTING)
        self.is_open_3d_touch = self.read_local_setting(ui_operation_const.ThreeD_TOUCH_TOGGLE_KEY, ui_operation_const.ThreeD_TOUCH_TOGGLE_DEF_VAL)
        self.trigger_percent_3d_touch = self.read_local_setting(ui_operation_const.ThreeD_TOUCH_PERCENT_KEY, ui_operation_const.ThreeD_TOUCH_PERCENT_DEF_VAL)
        self.firerocker_ope_setting = self.read_local_setting(ui_operation_const.FIREROCKER_OPE_KEY, ui_operation_const.FIREROCKER_OPE_DEF)
        gyr_state, x_reverse, y_reverse = self.get_setting(ui_operation_const.GYROSCOPE_STATE_KEY)
        self.enable_pure_mecha_sens = bdict.get('enable_pure_mecha_sens', 0)
        return

    def init_setting_const(self):
        from common.cfg import confmgr
        ui_operation_const.CUSTOM_SETTING_KEY.update(six_ex.keys(confmgr.get('c_panel_custom_conf')))
        ui_operation_const.CUSTOM_SETTING_KEY.update(['resolution', 'name'])
        ui_operation_const.CUSTOM_PVE_SETTING_KEY.update(six_ex.keys(confmgr.get('c_pve_panel_custom_conf')))
        ui_operation_const.CUSTOM_PVE_SETTING_KEY.update(['resolution', 'name'])
        ui_operation_const.CUSTOM_SETTING_OPT = {0, 1, 2}
        ui_operation_const.CUSTOM_PVE_SETTING_OPT = {100, 101, 102}
        mecha_config = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content')
        for lobby_mecha_id, info in six.iteritems(mecha_config):
            ui_operation_const.CUSTOM_SETTING_OPT.add(info.get('battle_mecha_id'))
            ui_operation_const.CUSTOM_PVE_SETTING_OPT.add(info.get('battle_mecha_id') * 100)

    def _destroy_usersetting(self):
        self.save_settings_to_file()

    def bind_setting_user_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'rocker_run_span_scale_event': self.save_rocker_run_scale_data,
           'rocker_walk_span_scale_event': self.save_rocker_walk_scale_data,
           'posture_ope_ui_change_event': self.save_posture_ope_data,
           'threed_touch_change_event': self.save_3d_touch_ope_data,
           'threed_touch_pressure_change_event': self.save_3d_touch_pressure_data,
           'firerocker_ope_change_event': self.save_firerocker_ope_data,
           'one_shot_change_appear_time_event': self.save_one_shot_appear_time,
           'one_shot_change_attack_time_event': self.save_one_shot_attack_time,
           'left_fire_ope_change_event': self.save_left_fire_ope,
           'free_sight_ope_change_event': self.save_free_sight_ope,
           'weapon_bar_ui_ope_change_event': self.save_weapon_bar_ope,
           'drive_ui_ope_change_event': self.save_drive_ui_ope,
           'drive_ui_button_ope_change_event': self.save_drive_ui_button_ope,
           'hot_key_swtich_on_event': self.on_hot_key_switch_on,
           'hot_key_swtich_off_event': self.on_hot_key_switch_off,
           'on_new_user_setting': self.on_get_new_user_setting
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_login_usersetting_success(self):
        self.apply_web_setting()

    def on_get_new_user_setting(self):
        if self.is_in_battle():
            return
        self.apply_web_setting()

    def apply_web_setting(self):
        if not self.in_user_setting_test:
            return
        else:
            user_setting = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {}).get('user_setting', {})
            setting_dict = user_setting.get('setting', None)
            self._server_setting_dict = setting_dict
            server_setting_dict_2 = copy.deepcopy(user_setting.get('setting_dict_2', {}))
            self._deserialize_setting_dict_2(server_setting_dict_2)
            self._server_setting_dict_2 = server_setting_dict_2
            self._sync_setting_to_local_2(server_setting_dict_2)
            self._setting_no = str(user_setting.get('setting_no', '0'))
            self._pve_setting_no = str(user_setting.get('pve_setting_no', '0'))
            self._custom_setting = user_setting.get('custom_setting', {})
            self.enable_pure_mecha_sens = user_setting.get('enable_pure_mecha_sens', 0)
            if not setting_dict or ui_operation_const.NEWBIE_PASS_HIDE_UI not in setting_dict:
                if not setting_dict:
                    setting_dict = {}
                setting_dict[ui_operation_const.NEWBIE_PASS_HIDE_UI] = 0
            if setting_dict is not None:
                self.init_setting_from_dict(setting_dict)
            if self._custom_setting:
                self.init_custom_setting_from_server()
            else:
                self.read_and_upload_local_custom_setting()
            self.enforce_pc_quality_setting()
            return

    def encode(self, key, val):
        if isinstance(val, bool):
            if val:
                return 1
            else:
                return 0

        if isinstance(val, float):
            return int(val * SCALE_DEGREE)
        else:
            if isinstance(val, int):
                return val
            log_error('encode', key, val)
            return None

    def decode(self, val, dtype):
        if not isinstance(val, int):
            return None
        else:
            if dtype == bool:
                return val > 0
            if dtype == int:
                return val
            if dtype == float:
                return val / SCALE_DEGREE
            return None

    def call_server_setting(self, setting):
        need_update = False
        for key in self._modify_cache:
            new_contact, old_contact = self._modify_cache[key]
            if isinstance(old_contact, (list, tuple)):
                for idx in range(len(old_contact)):
                    if new_contact[idx] != old_contact[idx]:
                        val = self.encode(key, new_contact[idx])
                        if isinstance(val, int):
                            sub_key = '%s-%d' % (key, idx)
                            setting[sub_key] = val
                            need_update = True
                            if not self.in_user_setting_test:
                                self.call_server_method('change_setting', (sub_key, val))

            else:
                val = self.encode(key, new_contact)
                if isinstance(val, int):
                    setting[key] = val
                    need_update = True
                    if not self.in_user_setting_test:
                        self.call_server_method('change_setting', (key, val))

        self._modify_cache.clear()
        return need_update

    def init_setting_from_dict(self, setting_dict):
        from logic.gcommon.common_const.setting_const import SYNC_KEYS, SETTING_KEYS, KEYS2TAG
        for sub_key, val in six.iteritems(setting_dict):
            keys = sub_key.split('-')
            key = keys[0]
            if KEYS2TAG.get(key, None) not in SYNC_KEYS:
                continue
            if key in ui_operation_const.SETTINGS_USE_NEW_2_API_FOR_OLD_CALLSITE:
                continue
            local_contact = self.get_setting(key)
            if isinstance(local_contact, (list, tuple)):
                if len(keys) < 2 or not keys[1].isdigit():
                    continue
                idx = int(keys[1])
                local_val = local_contact[idx]
                val = self.decode(val, type(local_val))
                if val is None or val == local_val:
                    continue
                local_contact[idx] = val
                self.write_setting(key, local_contact)
            else:
                val = self.decode(val, type(local_contact))
                if val is None or val == local_contact:
                    continue
                self.write_setting(key, val)

        self.save_settings_to_file()
        return

    def init_custom_setting_from_server(self):
        from logic.gcommon.common_const.setting_const import RESOLUTION
        self._custom_setting_cache = {}
        save_info = copy.deepcopy(self._custom_setting)
        for setting_no, info in six.iteritems(save_info):
            for key, value in six.iteritems(info):
                info[key] = deserialize_setting_2_val(value)

            resolution_data = info.get(RESOLUTION, None)
            if resolution_data is None:
                self._custom_resolution_data[setting_no] = {'human': global_data.ui_mgr.design_screen_size.width,'mecha': global_data.ui_mgr.design_screen_size.width,
                   'pve': global_data.ui_mgr.design_screen_size.width
                   }
                self._is_old_custom_data[setting_no] = {'human': True,
                   'mecha': True
                   }
            elif type(resolution_data) in (int, float):
                self._custom_resolution_data[setting_no] = {'human': resolution_data,'mecha': resolution_data,
                   'pve': resolution_data
                   }
                self._is_old_custom_data[setting_no] = {'human': True,
                   'mecha': True
                   }
            else:
                is_common = int(setting_no) in ui_operation_const.COMMON_SETTING_NO_LIST or int(setting_no) in ui_operation_const.PVE_COMMON_SETTING_NO_LIST
                if not is_common:
                    has_value = len(six_ex.keys(info)) > 1
                    if not has_value:
                        continue
                self._custom_resolution_data[setting_no] = resolution_data
                self._is_old_custom_data[setting_no] = {'human': True,
                   'mecha': True
                   }
                if resolution_data.get('human', None):
                    self._is_old_custom_data[setting_no]['human'] = False
                if resolution_data.get('mecha', None):
                    self._is_old_custom_data[setting_no]['mecha'] = False
            if RESOLUTION in info:
                info.pop(RESOLUTION)
            self._custom_setting_cache[setting_no] = info

        return

    def get_cur_setting_no(self):
        return int(self._setting_no)

    def set_cur_setting_no(self, no):
        if int(no) < 0 or int(no) > 2:
            return
        self._setting_no = str(no)
        if self.in_user_setting_test:
            version = self.get_settings_version()
            self.update_data({'version': version,'user_setting.setting_no': int(self._setting_no)})
        else:
            self.call_server_method('modify_setting_no', (int(self._setting_no),))

    def get_cur_pve_setting_no(self):
        return int(self._pve_setting_no)

    def set_cur_pve_setting_no(self, no):
        if int(no) < 0 or int(no) > 2:
            return
        self._pve_setting_no = str(no)
        if self.in_user_setting_test:
            version = self.get_settings_version()
            self.update_data({'version': version,'user_setting.pve_setting_no': int(self._pve_setting_no)})
        else:
            self.call_server_method('modify_setting_no', (int(self._pve_setting_no),))

    def get_default_setting(self, key):
        if key in ui_operation_const.SETTINGS_USE_NEW_2_API_FOR_OLD_CALLSITE:
            return self.get_default_setting_2(key)
        else:
            return self._user_default_setting_dict.get(key, None)

    def set_default_setting(self, key, val):
        self._user_default_setting_dict[key] = val

    def read_local_setting(self, key, default_val, vtype=str):
        return self.user_data_archive.get_field(key, default_val)

    def get_pve_setting(self, key, default=None, from_local=False, from_custom_setting_no=None):
        from logic.gutils.pve_utils import get_pve_mecha_id_list
        if from_custom_setting_no is not None:
            if str(from_custom_setting_no) in get_pve_mecha_id_list():
                from_custom_setting_no *= 100
            else:
                from_custom_setting_no += 100
        else:
            from_custom_setting_no = int(self._pve_setting_no) + 100
        return self.get_setting(key, default, from_local, from_custom_setting_no)

    def write_pve_setting(self, key, contact, upload=False, page=('human', ), to_custom_setting_no=None):
        from logic.gutils.pve_utils import get_pve_mecha_id_list
        if to_custom_setting_no is not None:
            if str(to_custom_setting_no) in get_pve_mecha_id_list():
                to_custom_setting_no *= 100
            else:
                to_custom_setting_no += 100
        else:
            to_custom_setting_no = int(self._pve_setting_no) + 100
        return self.write_setting(key, contact, upload, page, to_custom_setting_no)

    def get_setting(self, key, default=None, from_local=False, from_custom_setting_no=None):
        if key in ui_operation_const.SETTINGS_USE_NEW_2_API_FOR_OLD_CALLSITE:
            return self.get_setting_2(key)
        else:
            if key == ui_operation_const.CUSTOMER_UI_KEY and not from_local:
                setting_no = str(self._setting_no if from_custom_setting_no is None else from_custom_setting_no)
                return self._custom_setting_cache.get(setting_no, {})
            import copy
            val = self.read_local_setting(key, None)
            if val is None:
                if key not in self._user_default_setting_dict:
                    if default is None:
                        pass
                    return default
                val = self._user_default_setting_dict.get(key)
            val = copy.deepcopy(val)
            return val
            return

    def write_setting(self, key, contact, upload=False, page=('human', ), to_custom_setting_no=None):
        if key in ui_operation_const.SETTINGS_USE_NEW_2_API_FOR_OLD_CALLSITE:
            return self.write_setting_2(key, contact, sync_to_server=upload)
        else:
            if key == ui_operation_const.CUSTOMER_UI_KEY:
                setting_no = str(self._setting_no if to_custom_setting_no is None else to_custom_setting_no)
                self._custom_setting_cache[setting_no] = contact
                if setting_no not in self._custom_resolution_data:
                    self._custom_resolution_data[setting_no] = {}
                for page_name in page:
                    self._custom_resolution_data[setting_no][page_name] = global_data.ui_mgr.design_screen_size.width
                    if setting_no not in self._is_old_custom_data:
                        self._is_old_custom_data[setting_no] = {}
                    self._is_old_custom_data[setting_no][page_name] = False

            else:
                if upload:
                    if key in self._modify_cache:
                        last_contact = self._modify_cache[key][1]
                    else:
                        last_contact = self.get_setting(key)
                    self._modify_cache[key] = (
                     contact, last_contact)
                self.user_data_archive[key] = contact
            return

    def get_cur_custom_setting_resolution_data(self, page='human', setting_no=None, default=None):
        if default is None:
            default = global_data.ui_mgr.design_screen_size.width
        if page == 'pve':
            setting_no = self._pve_setting_no if setting_no is None else setting_no
            setting_no = int(setting_no) + 100
        else:
            setting_no = self._setting_no if setting_no is None else setting_no
        setting_no = str(setting_no)
        return self._custom_resolution_data.get(setting_no, {}).get(page, default)

    def copy_custom_setting_resolution_data(self, page='human', from_setting_no=None, to_setting_no=None):
        if page == 'pve':
            from_setting_no += 100
            to_setting_no += 100
        if type(from_setting_no) not in [str, six.text_type]:
            from_setting_no = str(from_setting_no)
        if type(to_setting_no) not in [str, six.text_type]:
            to_setting_no = str(to_setting_no)
        if to_setting_no not in self._custom_resolution_data:
            self._custom_resolution_data[to_setting_no] = {}
        self._custom_resolution_data[to_setting_no][page] = self._custom_resolution_data.get(from_setting_no, {}).get(page, global_data.ui_mgr.design_screen_size.width)
        if to_setting_no not in self._is_old_custom_data:
            self._is_old_custom_data[to_setting_no] = {}
        self._is_old_custom_data[to_setting_no][page] = self._is_old_custom_data.get(from_setting_no, {}).get(page, True)

    def revert_custom_setting_resolution_data(self, setting_no=None, is_clear=False):
        if type(setting_no) not in [str, six.text_type]:
            setting_no = str(setting_no)
        if is_clear:
            if setting_no in self._custom_resolution_data:
                del self._custom_resolution_data[setting_no]
            if setting_no in self._is_old_custom_data:
                del self._is_old_custom_data[setting_no]
        else:
            if setting_no not in self._custom_resolution_data:
                self._custom_resolution_data[setting_no] = {}
            for page_name in ui_operation_const.CUSTOM_PAGES:
                self._custom_resolution_data[setting_no][page_name] = global_data.ui_mgr.design_screen_size.width
                if setting_no not in self._is_old_custom_data:
                    self._is_old_custom_data[setting_no] = {}
                self._is_old_custom_data[setting_no][page_name] = False

    def is_cur_custom_setting_old_data(self, page='human', setting_no=None, default=True):
        setting_no = str(self._setting_no if setting_no is None else setting_no)
        return self._is_old_custom_data.get(setting_no, {}).get(page, default)

    def save_custom_ui_config(self, save_info, to_custom_setting_no=None):
        from logic.gcommon.common_const.setting_const import RESOLUTION
        setting_no = str(self._setting_no if to_custom_setting_no is None else to_custom_setting_no)
        upload_data = {}
        custom_setting = self._custom_setting.get(setting_no, {})
        for key, value in six.iteritems(save_info):
            if key not in custom_setting:
                upload_data[key] = value
            elif custom_setting[key] != value:
                upload_data[key] = value

        is_clear = save_info == {}
        if is_clear:
            self.revert_custom_setting_resolution_data(to_custom_setting_no, True)
        custom_setting.update(upload_data)
        if not is_clear:
            if six.PY2:
                upload_data[RESOLUTION] = six.moves.cPickle.dumps(self._custom_resolution_data[setting_no])
            else:
                upload_data[RESOLUTION] = self._custom_resolution_data[setting_no]
        if self.in_user_setting_test:
            new_custom_setting = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {}).get('user_setting', {}).get('custom_setting', {})
            if is_clear:
                new_custom_setting.pop(setting_no, 0)
            if upload_data:
                if int(setting_no) not in ui_operation_const.CUSTOM_SETTING_OPT and int(setting_no) not in ui_operation_const.CUSTOM_PVE_SETTING_OPT:
                    return
                custom_setting_dict = new_custom_setting.setdefault(str(setting_no), {})
                valid_type = (int, float, str, dict, tuple, list, set)
                for key, value in six.iteritems(upload_data):
                    if (key in ui_operation_const.CUSTOM_SETTING_KEY or key in ui_operation_const.CUSTOM_PVE_SETTING_KEY) and isinstance(value, valid_type):
                        custom_setting_dict[key] = value

                version = self.get_settings_version()
                self.update_data({'version': version,'user_setting.custom_setting.%s' % setting_no: new_custom_setting.get(str(setting_no), {})})
        else:
            self.call_server_method('modify_settings', (int(setting_no), upload_data, is_clear))
        return

    def read_and_upload_local_custom_setting(self):
        setting_info = self.get_setting(ui_operation_const.CUSTOMER_UI_KEY, from_local=True)
        upload_data = copy.deepcopy(setting_info)
        self._custom_resolution_data[self._setting_no] = {'human': global_data.ui_mgr.design_screen_size.width,
           'mecha': global_data.ui_mgr.design_screen_size.width,
           'pve': global_data.ui_mgr.design_screen_size.width
           }
        self._is_old_custom_data[self._setting_no] = {'human': True,
           'mecha': True
           }
        self.write_setting(ui_operation_const.CUSTOMER_UI_KEY, setting_info)
        if six.PY2:
            for key, value in six.iteritems(upload_data):
                upload_data[key] = six.moves.cPickle.dumps(value)

        else:
            for key, value in six.iteritems(upload_data):
                upload_data[key] = value

        self.save_custom_ui_config(upload_data)

    def save_settings_to_file(self):
        setting = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {}).get('user_setting', {}).get('setting', {})
        need_update = self.call_server_setting(setting)
        if need_update and self.in_user_setting_test:
            self.update_data({'version': self.get_settings_version(),'user_setting.setting': setting})
        self.user_data_archive.save(encrypt=True)

    def save_rocker_run_scale_data(self, val):
        self.write_setting(ui_operation_const.MR_RUN_KEY, val)

    def save_rocker_walk_scale_data(self, val):
        self.write_setting(ui_operation_const.MR_WALK_KEY, val)

    def save_posture_ope_data(self, val):
        from logic.gcommon.common_const.ui_operation_const import OPE_POSTURE_KEY
        self.write_setting(OPE_POSTURE_KEY, val)
        self.cur_posture_setting = val

    def save_3d_touch_ope_data(self, toggle_val):
        self.is_open_3d_touch = toggle_val
        self.write_setting(ui_operation_const.ThreeD_TOUCH_TOGGLE_KEY, toggle_val)

    def save_3d_touch_pressure_data(self, pressure):
        self.trigger_percent_3d_touch = pressure
        self.write_setting(ui_operation_const.ThreeD_TOUCH_PERCENT_KEY, pressure)

    def save_firerocker_ope_data(self, val):
        self.firerocker_ope_setting = val
        self.write_setting(ui_operation_const.FIREROCKER_OPE_KEY, val, True)

    def save_one_shot_appear_time(self, val):
        self.write_setting(ui_operation_const.ONE_SHOT_SHOW_KEY, val)

    def save_one_shot_attack_time(self, val):
        self.write_setting(ui_operation_const.ONE_SHOT_ATTACK_KEY, val)

    def save_left_fire_ope(self, val):
        self.write_setting(ui_operation_const.LF_OPE_KEY, val, True)

    def save_free_sight_ope(self, val):
        self.write_setting(ui_operation_const.FREE_SIGHT_KEY, val, True)

    def save_weapon_bar_ope(self, val):
        self.write_setting(ui_operation_const.WEAPON_BAR_UI_KEY, val)

    def save_drive_ui_ope(self, val):
        self.write_setting_2(ui_operation_const.DRIVE_OPE_KEY, val, True)

    def save_open_sound_visible3d(self, val):
        self.write_setting(ui_operation_const.SOUND_VISIBLE_3D_KEY, val, True)

    def save_open_injure_visible3d(self, val):
        self.write_setting(ui_operation_const.INJURE_VISIBLE_3D_KEY, val, True)

    def save_drive_ui_button_ope(self, val):
        self.write_setting_2(ui_operation_const.DRIVE_OPE_BUTTON_DIR_KEY, val, True)

    def init_camera_sst_from_conf(self, is_pc=False):
        from common.cfg import confmgr
        def_settings = {}
        if not is_pc:
            sst_conf = confmgr.get('sst_config')
        else:
            sst_conf = confmgr.get('pc_sst_config')
        for sst_model, sst_content in six.iteritems(sst_conf):
            if isinstance(sst_content, str):
                continue
            sst_model_type = sst_content.get('iSSTType')
            if sst_model_type == ui_operation_const.SST_TYPE_CENTER_TYPE:
                sst_def_setting = [
                 sst_content['fBaseMultiple'],
                 sst_content['fUpMultiple'],
                 sst_content['fDownMultiple'],
                 sst_content['fLeftMultiple'],
                 sst_content['fRightMultiple']]
            elif sst_model_type == ui_operation_const.SST_TYPE_SCREEN_TYPE:
                sst_def_setting = [
                 sst_content['fBaseMultiple'],
                 sst_content['fUpMultiple'],
                 sst_content['fDownMultiple'],
                 sst_content['fLeftScreenHorMultiple'],
                 sst_content['fRightScreenHorMultiple']]
            else:
                sst_def_setting = []
            def_settings[sst_model] = sst_def_setting

        self._user_default_setting_dict.update(def_settings)

    def switch_to_sst_config(self, is_pc):
        self.init_camera_sst_from_conf(is_pc)
        from common.cfg import confmgr
        sst_conf = confmgr.get('sst_config')
        pc_sst_conf = confmgr.get('pc_sst_config')
        keys = six_ex.keys(sst_conf)
        for idx, key in enumerate(keys):
            cur_list = self.get_setting(key)
            key_conf = sst_conf.get(key)
            pc_key_conf = pc_sst_conf.get(key)
            if pc_key_conf is None:
                continue
            if isinstance(key_conf, str):
                continue
            if len(key_conf) != len(pc_key_conf):
                log_error('PLEASE Keep SST CONF of PC and MOBILE PHONE with same type!!!')
                continue
            sst_def_setting = self.get_default_setting(key)
            if not sst_def_setting:
                continue
            new_list = list(sst_def_setting)
            new_list[ui_operation_const.SST_IDX_BASE] = cur_list[ui_operation_const.SST_IDX_BASE]
            self.write_setting(keys[idx], new_list, False)
            global_data.emgr.sst_common_changed_event.emit(key, new_list)

        return

    def on_hot_key_switch_on(self):
        self.switch_to_sst_config(True)

    def on_hot_key_switch_off(self):
        self.switch_to_sst_config(False)

    def get_default_setting_2(self, key):
        return self._user_default_setting_dict.get(key, None)

    def get_local_setting_2(self, key):
        default_val = self.get_default_setting_2(key)
        local_val = self.get_local_setting_ext_2(key, default_val)
        return local_val

    def get_local_setting_ext_2(self, key, default=None):
        key_variant = self._get_setting_key_variant(key)
        return self.user_data_archive.get_field(key_variant, default)

    def has_local_setting_2(self, key):
        key_variant = self._get_setting_key_variant(key)
        return self.user_data_archive.has_field(key_variant)

    def _write_local_setting_2(self, key, val, flush):
        key_variant = self._get_setting_key_variant(key)
        self.user_data_archive[key_variant] = val
        if flush:
            self._flush_all_local_setting_2()

    def _flush_all_local_setting_2(self):
        self.user_data_archive.save(encrypt=True)

    def _deserialize_setting_dict_2(self, setting_dict_2):
        for setting_key in setting_dict_2:
            val = setting_dict_2[setting_key]
            if isinstance(val, (six.text_type, six.binary_type)):
                try:
                    val1 = val.encode('utf-8')
                    val = six.moves.cPickle.loads(val1)
                except:
                    serialized = six.moves.cPickle.dumps(val)
                    val = six.moves.cPickle.loads(serialized)

            setting_dict_2[setting_key] = val

    def _sync_setting_to_local_2(self, setting_dict):
        if not setting_dict:
            return
        for key in setting_dict:
            val = setting_dict[key]
            val = copy.deepcopy(val)
            self._write_local_setting_2(key, val, flush=False)

        self._flush_all_local_setting_2()

    def has_server_setting_2(self, key):
        key_variant = self._get_setting_key_variant(key)
        return key_variant in self._server_setting_dict_2

    def get_server_setting_2(self, key, default=None):
        key_variant = self._get_setting_key_variant(key)
        return self._server_setting_dict_2.get(key_variant, default)

    def sync_setting_to_server_2(self, key):
        local_val = self.get_local_setting_2(key)
        self._sync_setting_to_server_core_2(key, local_val)

    def _sync_setting_to_server_core_2(self, key, val):
        key_variant = self._get_setting_key_variant(key)
        val = copy.deepcopy(val)
        self._server_setting_dict_2[key_variant] = val
        if six.PY2:
            val_str = six.moves.cPickle.dumps(val)
        else:
            val_str = val
        if not setting_const.is_setting_key_valid_2(key_variant):
            return
        if self.in_user_setting_test:
            setting_2 = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {}).get('user_setting', {}).get('setting_dict_2', {})
            version = self.get_settings_version()
            setting_2.update({key_variant: val_str})
            self.update_data({'version': version,'user_setting.setting_dict_2': setting_2})
            if type(val_str) == bool:
                val_str = 'I01\n.' if val_str else 'I00\n.'
            if key in ui_operation_const.SERVER_SETTING:
                self.call_server_method('sync_setting_2', (key_variant, val_str))
        else:
            if type(val_str) == bool:
                val_str = 'I01\n.' if val_str else 'I00\n.'
            self.call_server_method('sync_setting_2', (key_variant, val_str))

    def is_setting_out_of_sync_2(self, key):
        if not self.has_server_setting_2(key):
            return True
        server_val = self.get_server_setting_2(key)
        local_val = self.get_local_setting_2(key)
        return server_val != local_val

    def has_setting_2(self, key):
        return self.has_local_setting_2(key)

    def get_setting_2(self, key):
        return self.get_local_setting_2(key)

    def get_setting_ext_2(self, key, default=None):
        return self.get_local_setting_ext_2(key, default)

    def write_setting_2(self, key, val, sync_to_server):
        val = copy.deepcopy(val)
        self._write_local_setting_2(key, val, flush=True)
        if sync_to_server:
            self._sync_setting_to_server_core_2(key, val)
        global_data.emgr.player_user_setting_changed_event.emit(key, val)

    def _get_setting_key_variant(self, base_key):
        if not isinstance(base_key, six.string_types):
            log_error('setting base_key is not string:', base_key)
            return base_key
        from logic.gcommon.common_const import ui_operation_const
        if base_key in ui_operation_const.SETTINGS_NEED_PLATFORM_VARIANT:
            if global_data.is_pc_mode:
                from logic.gcommon.common_const.setting_const import get_pc_platform_variant
                return get_pc_platform_variant(base_key)
            else:
                return base_key

        return base_key

    def pure_mecha_sens_enabled(self):
        return self.enable_pure_mecha_sens

    def enforce_pc_quality_setting(self):
        if pc_platform_utils.is_pc_hight_quality():
            for key in ui_operation_const.PC_HIDDEN_SETTING_CONF:
                if key in ui_operation_const.PC_HIGHT_QUALITY_SETTING_CONF:
                    self._write_local_setting_2(key, ui_operation_const.PC_HIGHT_QUALITY_SETTING_CONF[key], False)
                self._flush_all_local_setting_2()