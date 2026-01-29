# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/CustomUIProxy.py
from __future__ import absolute_import
from logic.gcommon.common_utils.ui_gameplay_utils import apply_player_custom_setting
from logic.gcommon.common_const.ui_operation_const import CUSTOMER_UI_KEY
from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
from logic.comsys.setting_ui import button_custom_key_func
from common.cfg import confmgr
import six_ex
import six

class CustomUIProxy(object):

    def init_custom_panel(self, ui_inst, bind_key_var_dict={}, belong_page='human', ui_custom_panel_name=None):
        self._is_enable = True
        self.ui_inst = ui_inst
        self.belong_page = belong_page
        self.custom_key_val_dict = {}
        self.cur_custom_node_conf = {}
        self.cur_custom_conf_by_node_name = {}
        self.node_default_conf_dict = {}
        self._is_bind_control_target_event = False
        self.ui_custom_panel_name = ui_custom_panel_name
        UIDistorterHelper().record_ui_parameters(self.ui_inst.__class__.__name__)
        self.custom_keys = self.get_custom_panel_keys(self.ui_inst.__class__.__name__ if self.ui_custom_panel_name is None else self.ui_custom_panel_name)
        self.bind_custom_panel_event()
        for key, var_name in six.iteritems(bind_key_var_dict):
            self.bind_custom_key_val_vars(key, var_name)

        self.check_record_node_info()
        return

    def check_record_node_info(self):
        for key in self.custom_keys:
            self.record_node_info(self.ui_inst, key, self.get_custom_val_by_key(key), ui_custom_panel_name=self.ui_custom_panel_name)

        panel = self.ui_inst
        panel_name = panel.__class__.__name__
        related_conf = confmgr.get('c_panel_node_related_conf', str(panel_name))
        if related_conf:
            for node_name, info in six.iteritems(related_conf):
                nd = getattr(panel, node_name)
                if nd:
                    if not nd.HasRecordNodeInfo():
                        nd.RecordNodeInfo()

    def record_node_info(self, panel, setting_key, set_val, ui_custom_panel_name):
        if self.ui_custom_panel_name is None:
            panel_name = self.ui_inst.__class__.__name__ if 1 else self.ui_custom_panel_name
            posture_conf = confmgr.get('c_panel_custom_key_conf', str(panel_name), str(setting_key), default={})
            real_node_confs = six_ex.values(posture_conf)
            return real_node_confs or None
        else:
            for node_id_list_conf in real_node_confs:
                node_id_list = node_id_list_conf.get('arrConfigList', [])
                for node_id in node_id_list:
                    node_conf = confmgr.get('c_panel_node_custom_conf', str(node_id))
                    nd_name = node_conf['cAdjustNode'] or node_conf['cNodeName']
                    nd = getattr(panel.panel, nd_name)
                    if nd:
                        if not nd.HasRecordNodeInfo():
                            nd.RecordNodeInfo()

            return

    def bind_custom_panel_event(self):
        global_data.emgr.ui_change_custom_arrange_event += self.refresh_all_custom_ui_conf
        panel_name = self.ui_inst.__class__.__name__ if self.ui_custom_panel_name is None else self.ui_custom_panel_name
        ui_page = self.get_panel_page(panel_name)
        if ui_page == 'mecha' or ui_page == 'pve':
            self._is_bind_control_target_event = True
            global_data.emgr.switch_control_target_event += self.on_ctrl_target_changed
        return

    def unbind_custom_panel_event(self):
        global_data.emgr.ui_change_custom_arrange_event -= self.refresh_all_custom_ui_conf
        if self._is_bind_control_target_event:
            global_data.emgr.switch_control_target_event -= self.on_ctrl_target_changed
            self._is_bind_control_target_event = False

    def on_ctrl_target_changed(self, *args):
        if not global_data.cam_lplayer:
            return
        self.refresh_all_custom_ui_conf()

    def bind_custom_key_val_vars(self, key, var_name):
        self.custom_key_val_dict[key] = var_name

    def destroy(self):
        self.ui_inst = None
        self.unbind_custom_panel_event()
        self.custom_keys = []
        self.custom_key_val_dict = {}
        self.node_default_conf_dict = {}
        self.cur_custom_node_conf = {}
        self.cur_custom_conf_by_node_name = {}
        return

    def get_custom_val_by_key(self, key):
        var_name = self.custom_key_val_dict.get(key, None)
        if var_name:
            val = getattr(self.ui_inst, var_name, '')
            return val
        else:
            return ''
            return

    def refresh_all_custom_ui_conf(self):
        if not global_data.player:
            return
        if not self._is_enable:
            return
        if not self.ui_inst:
            return
        for key in self.custom_keys:
            self.on_switch_panel_ope_setting(self.ui_inst, key, self.get_custom_val_by_key(key), ui_custom_panel_name=self.ui_custom_panel_name)

        self.on_refresh_ui_data()
        global_data.emgr.ui_refresh_all_custom_ui_conf.emit()

    def refresh_custom_ui_conf(self, set_key):
        self.on_switch_panel_ope_setting(self.ui_inst, set_key, self.get_custom_val_by_key(set_key), ui_custom_panel_name=self.ui_custom_panel_name)
        self.on_refresh_ui_data()

    def set_node_default_setting(self, node_name, conf):
        self.node_default_conf_dict[node_name] = conf

    def get_panel_setting_conf(self, panel_name, setting_key, set_val, from_setting_no=None):
        custom_ui_setting_conf = self.get_panel_custom_ui_setting_conf(from_setting_no)
        ui_setting_conf = custom_ui_setting_conf.get(panel_name, {})
        repr_key_val = str(set_val)
        if not self.check_is_valid_set_key(setting_key):
            log_error('Invalid Custom setting key', panel_name, setting_key, set_val)
        key_convert_conf = confmgr.get('c_panel_custom_key_convert', str(setting_key), default={})
        convert_func_name = key_convert_conf.get('cKeyConvertFunc', None)
        if convert_func_name:
            func = getattr(button_custom_key_func, convert_func_name)
            repr_key_val = func(set_val)
        posture_conf = ui_setting_conf.get(setting_key, {}).get(repr_key_val, {})
        return posture_conf or self.get_panel_empty_setting_conf(panel_name, setting_key, set_val)

    def get_panel_empty_setting_conf(self, panel_name, setting_key, set_val):
        empty_conf = {}
        posture_conf = confmgr.get('c_panel_custom_key_conf', str(panel_name), str(setting_key), str(set_val), default={})
        node_id_list = posture_conf.get('arrConfigList', [])
        for node_id in node_id_list:
            node_conf = confmgr.get('c_panel_node_custom_conf', str(node_id))
            nd_name = node_conf['cAdjustNode'] or node_conf['cNodeName']
            empty_conf[node_id] = {nd_name: {}}

        return empty_conf

    def on_switch_panel_ope_setting(self, panel, setting_key, set_val, ui_custom_panel_name=None):
        for nd_name, nd in six.iteritems(self.cur_custom_node_conf):
            if nd:
                self.revert_node_conf(nd, nd_name)
            else:
                nd = getattr(panel.panel, nd_name)
                if nd:
                    self.revert_node_conf(nd, nd_name)

        self.cur_custom_node_conf = {}
        self.cur_custom_conf_by_node_name = {}
        if ui_custom_panel_name is None:
            panel_name = panel.__class__.__name__ if 1 else ui_custom_panel_name
            setting_no = None
            posture_conf = self.get_panel_setting_conf(panel_name, setting_key, set_val, from_setting_no=setting_no)
            is_pve = False
            if global_data.game_mode and global_data.game_mode.is_pve():
                is_pve = True
        if is_pve:
            setting_no = global_data.player.get_cur_pve_setting_no()
        else:
            setting_no = global_data.player.get_cur_setting_no()
        if global_data.mecha and global_data.mecha.logic:
            mecha_id = global_data.mecha.share_data.ref_mecha_id
            mecha_posture_conf = self.get_mecha_priority_setting(mecha_id, panel_name, setting_key, set_val)
            if mecha_posture_conf is not None:
                posture_conf = mecha_posture_conf
                setting_no = mecha_id
        real_node_confs = six_ex.values(posture_conf)
        for real_conf in real_node_confs:
            for nd_name, nd_conf in six.iteritems(real_conf):
                nd = getattr(panel.panel, nd_name)
                self.cur_custom_conf_by_node_name[nd_name] = nd_conf
                if nd:
                    if nd_conf:
                        self.revert_node_conf(nd, nd_name)
                        apply_player_custom_setting(nd, nd_conf, customize=True, belong_page=self.belong_page, setting_no=setting_no)
                        self.cur_custom_node_conf[nd_name] = nd
                    else:
                        self.revert_node_conf(nd, nd_name)
                else:
                    self.cur_custom_node_conf[nd_name] = None

        self.set_related_nodes_attr()
        return

    def get_custom_panel_keys(self, panel_name):
        _setting_conf = confmgr.get('c_panel_custom_key_conf', str(panel_name))
        if not _setting_conf:
            log_error("Can't find custom panel setting for ui ", panel_name)
            return []
        _keys = six_ex.keys(_setting_conf)
        return _keys

    def get_panel_custom_ui_setting_conf(self, from_setting_no):
        is_pve = False
        if global_data.game_mode and global_data.game_mode.is_pve():
            is_pve = True
        if is_pve:
            custom_ui_setting_conf = global_data.player.get_pve_setting(CUSTOMER_UI_KEY, from_custom_setting_no=from_setting_no)
        else:
            custom_ui_setting_conf = global_data.player.get_setting(CUSTOMER_UI_KEY, from_custom_setting_no=from_setting_no)
        return custom_ui_setting_conf

    def get_panel_page(self, panel_name):
        is_pve = False
        if global_data.game_mode and global_data.game_mode.is_pve():
            is_pve = True
        if is_pve:
            conf = confmgr.get('c_pve_panel_custom_conf', panel_name, default={})
        else:
            conf = confmgr.get('c_panel_custom_conf', panel_name, default={})
        if not conf:
            return None
        else:
            return conf['cPage']

    def get_mecha_priority_setting(self, mecha_id, panel_name, setting_key, set_val):
        custom_ui_setting_conf = self.get_panel_custom_ui_setting_conf(mecha_id)
        if not custom_ui_setting_conf:
            return None
        else:
            ui_page = self.get_panel_page(panel_name)
            if ui_page == 'mecha' or ui_page == 'pve':
                from_setting_no = mecha_id
                mecha_posture_conf = self.get_panel_setting_conf(panel_name, setting_key, set_val, from_setting_no=from_setting_no)
                return mecha_posture_conf
            return None

    def set_related_nodes_attr(self):
        custom_ui_setting_conf = global_data.player.get_setting(CUSTOMER_UI_KEY)
        panel = self.ui_inst
        panel_name = panel.__class__.__name__
        related_conf = confmgr.get('c_panel_node_related_conf', str(panel_name))
        if related_conf:
            for node_name, info in six.iteritems(related_conf):
                for related_panel_name, related_node_name in six.iteritems(info):
                    related_keys = self.get_custom_panel_keys(related_panel_name)
                    if len(related_keys) == 0:
                        log_error('Related UI has no key??? Seriously???', panel_name, related_node_name)
                        continue
                    related_key = related_keys[0]
                    if related_key == '':
                        related_val = ''
                    else:
                        related_val = str(global_data.player.get_setting(related_key))
                        key_convert_conf = confmgr.get('c_panel_custom_key_convert', str(related_key), default={})
                        convert_func_name = key_convert_conf.get('cKeyConvertFunc', None)
                        if convert_func_name:
                            func = getattr(button_custom_key_func, convert_func_name)
                            related_key = func(related_val)
                        related_setting_conf = custom_ui_setting_conf.get(related_panel_name, None)
                        if related_setting_conf is None:
                            return
                    real_nodes_conf = six_ex.values(related_setting_conf.get(related_key, {}).get(related_val, {}))
                    is_pve = False
                    if global_data.game_mode:
                        if global_data.game_mode.is_pve():
                            is_pve = True
                    if is_pve:
                        setting_no = global_data.player.get_cur_pve_setting_no()
                    else:
                        setting_no = global_data.player.get_cur_setting_no()
                    if global_data.mecha and global_data.mecha.logic:
                        mecha_id = global_data.mecha.share_data.ref_mecha_id
                        mecha_posture_conf = self.get_mecha_priority_setting(mecha_id, related_panel_name, related_key, related_val)
                        if mecha_posture_conf is not None:
                            real_nodes_conf = six_ex.values(mecha_posture_conf)
                            setting_no = mecha_id
                    for node_conf in real_nodes_conf:
                        for nd_name, nd_conf in six.iteritems(node_conf):
                            if nd_name != related_node_name:
                                continue
                            nd = getattr(panel, node_name)
                            if nd:
                                if nd_conf:
                                    ui_page = self.get_panel_page(related_panel_name)
                                    self.revert_node_conf(nd, node_name)
                                    apply_player_custom_setting(nd, nd_conf, customize=True, belong_page=ui_page, setting_no=setting_no)
                                else:
                                    self.revert_node_conf(nd, node_name)
                                break

        return

    def revert_node_conf(self, node, node_name):
        node.RevertToOrigConf()
        real_default_conf = self.node_default_conf_dict.get(node_name, {})
        if real_default_conf:
            node.ApplyCustomSetting(real_default_conf)

    def on_refresh_ui_data(self):
        if self.ui_inst:
            func = getattr(self.ui_inst, 'on_change_ui_custom_data', None)
            if func and callable(func):
                func()
        return

    def get_panel_node_custom_data(self, panel_name, node_name, set_key):
        posture_conf = self.get_panel_setting_conf(panel_name, set_key, self.get_custom_val_by_key(set_key))
        real_node_confs = six_ex.values(posture_conf)
        for real_conf in real_node_confs:
            for nd_name, nd_conf in six.iteritems(real_conf):
                if node_name == nd_name:
                    return nd_conf

    def check_is_valid_set_key(self, set_key):
        return set_key in self.custom_keys

    def revert_all_node_conf(self):
        for nd_name, nd in six.iteritems(self.cur_custom_node_conf):
            if nd:
                self.revert_node_conf(nd, nd_name)
            else:
                nd = getattr(self.ui_inst.panel, nd_name)
                if nd:
                    self.revert_node_conf(nd, nd_name)

    def on_resolution_changed(self):
        self.revert_all_node_conf()
        UIDistorterHelper().record_ui_parameters(self.ui_inst.__class__.__name__)

    def set_enable(self, enable):
        self._is_enable = enable
        if enable:
            self.refresh_all_custom_ui_conf()
        else:
            self.revert_all_node_conf()

    def get_conf_by_node_id(self, node_id):
        node_conf = confmgr.get('c_panel_node_custom_conf', str(node_id))
        nd_name = node_conf['cAdjustNode'] or node_conf['cNodeName']
        return self.cur_custom_conf_by_node_name.get(nd_name, {})


def init_custom_com(ui_inst, bind_key_var_dict, ui_custom_panel_name=None):
    if global_data.is_pc_mode:
        ui_inst.custom_ui_com = None
        return
    else:
        conf_name = 'c_panel_custom_conf'
        if ui_custom_panel_name is None:
            ui_name = ui_inst.__class__.__name__ if 1 else ui_custom_panel_name
            ui_page = None
            if global_data.game_mode:
                if global_data.game_mode.is_pve() and global_data.player:
                    conf_name = 'c_pve_panel_custom_conf'
                    ui_page = 'pve'
            conf = confmgr.get(conf_name, ui_name, default={})
            if not conf:
                conf = confmgr.get('c_panel_custom_conf', ui_name, default={})
            cIsEnable = conf.get('cIsEnable')
            if not cIsEnable:
                ui_inst.custom_ui_com = None
                return
            ui_inst.custom_ui_com = CustomUIProxy()
            if ui_page != 'pve':
                ui_page = conf.get('cPage', 'human')
            ui_inst.custom_ui_com.init_custom_panel(ui_inst, bind_key_var_dict, ui_page, ui_custom_panel_name=ui_custom_panel_name)
            bind_key_var_dict or ui_inst.custom_ui_com.refresh_all_custom_ui_conf()
        return