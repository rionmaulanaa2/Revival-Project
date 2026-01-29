# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/custom_ui_utils.py
from __future__ import absolute_import
import six_ex
from six.moves import range
import six

def get_cut_name(name, max_len):
    cut_name_list = []
    utf8_cnt = 0
    cut_off = False
    for ch in name:
        if u'\u4e00' <= ch <= u'\u9fff':
            utf8_cnt += 2
        else:
            utf8_cnt += 1
        if utf8_cnt < max_len:
            cut_name_list.append(ch)
        else:
            cut_off = True

    if not cut_off:
        return name
    cut_name_list.append('\xe2\x80\xa6')
    return ''.join(cut_name_list)


def get_group_names():
    from common.cfg import confmgr
    group_names = set()
    conf = confmgr.get('c_panel_node_custom_conf')
    for node_id, node_conf in six.iteritems(conf):
        cGroup = node_conf.get('cGroup', '')
        if cGroup:
            group_names.add(cGroup)

    return group_names


def get_custom_node_conf(node_id):
    from common.cfg import confmgr
    node_conf = confmgr.get('c_panel_node_custom_conf', str(node_id), default={})
    return node_conf


def get_group_all_node_ids(target_group_name):
    from common.cfg import confmgr
    node_ids = []
    nodes_conf = confmgr.get('c_panel_node_custom_conf')
    for node_id, node_conf in six.iteritems(nodes_conf):
        group_name = node_conf.get('cGroup')
        if group_name == target_group_name:
            node_ids.append(node_id)

    node_ids = sorted(node_ids, key=lambda k: nodes_conf[k].get('iGroupRank', 0), reverse=True)
    return node_ids


def check_custom_node_group_setting():
    from logic.gcommon.common_const import ui_operation_const
    all_group_names = get_group_names()
    all_setting_no_conf = {}
    for setting_no in range(ui_operation_const.CUSTOM_SETTING_NO_COUNT):
        s_no_group_conf = global_data.player.get_setting(ui_operation_const.CUSTOM_NODE_GROUPS, default={}).get(str(setting_no), None)
        if s_no_group_conf is None:
            conf = _generate_custom_node_group_setting(setting_no, all_group_names)
            all_setting_no_conf.setdefault(str(setting_no), {})
            all_setting_no_conf[str(setting_no)] = conf
        else:
            target_group_names = []
            for gp_name in all_group_names:
                gr_conf = s_no_group_conf.get(gp_name, {})
                if not gr_conf:
                    target_group_names.append(gp_name)

            if target_group_names:
                conf = _generate_custom_node_group_setting(setting_no, target_group_names)
                s_no_group_conf.update(conf)
            all_setting_no_conf[str(setting_no)] = s_no_group_conf

    if all_setting_no_conf:
        global_data.player.write_setting(ui_operation_const.CUSTOM_NODE_GROUPS, all_setting_no_conf, upload=True)
    return


def _generate_custom_node_group_setting(setting_no, group_name_list):
    from logic.gcommon.common_const import ui_operation_const
    from common.cfg import confmgr
    group_conf = {}
    nodes_conf = confmgr.get('c_panel_node_custom_conf')
    panel_nodes_conf = confmgr.get('c_panel_custom_key_conf')
    node_id_to_ui_name_dict = {}
    for ui_name, setting_key_val_conf in six.iteritems(panel_nodes_conf):
        if type(setting_key_val_conf) in (str, six.text_type):
            continue
        for set_key, set_val_conf in six.iteritems(setting_key_val_conf):
            for adjust_node_name, node_conf in six.iteritems(set_val_conf):
                arrConfigList = node_conf.get('arrConfigList', [])
                for node_id in arrConfigList:
                    node_id_to_ui_name_dict[str(node_id)] = ui_name

    cust_conf = global_data.player.get_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=setting_no)
    for node_id, node_conf in six.iteritems(nodes_conf):
        group_name = node_conf.get('cGroup')
        group_rank = node_conf.get('iGroupRank', 0)
        is_top_no = group_rank == ui_operation_const.CUSTOM_NODE_TOP_GROUP_RANK
        if group_name and group_name in group_name_list:
            group_conf.setdefault(group_name, [])
            if not is_top_no:
                ui_name = node_id_to_ui_name_dict.get(str(node_id))
                node_cust_conf = cust_conf.get(ui_name, {})
                if node_cust_conf:
                    if len(six_ex.keys(node_cust_conf)) == 1 and six_ex.keys(node_cust_conf)[0] != '':
                        log_error('node with setting key is not work with group name!')
                        continue
                    node_setting_conf = node_cust_conf.get('', {}).get('', {})
                    if not six_ex.values(node_setting_conf) and ui_name:
                        group_conf[group_name].append(node_id)
                else:
                    group_conf[group_name].append(node_id)
            else:
                group_conf[group_name].append(node_id)

    return group_conf