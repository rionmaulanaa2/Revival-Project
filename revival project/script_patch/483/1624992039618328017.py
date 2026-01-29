# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/nile_utils.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
import logic.gcommon.common_const.activity_const as activity_const

def get_nile_activity_list(widget_type):
    from logic.gutils import activity_utils
    if not global_data.player:
        return []
    else:
        if not global_data.nile_sdk:
            return []
        if widget_type is None:
            widget_type = activity_const.WIDGET_MAIN
        ret_list = []
        activity_dict = confmgr.get('nile_activity_conf')
        activity_cids = []
        for cid, _ in six.iteritems(activity_dict):
            is_ready = global_data.nile_sdk.get_activity_status(cid)
            if cid.isdigit() and is_ready:
                activity_cids.append(cid)

        activity_cids.sort()
        ignore_activity = []
        for cId in activity_cids:
            cId = str(cId)
            if activity_utils.get_activity_widget_type(cId) != widget_type:
                ignore_activity.extend(cId)
                continue
            if True:
                iLevel = confmgr.get('c_activity_config', cId, 'iLevel', default=0)
                if global_data.player.get_lv() < iLevel:
                    ignore_activity.extend(cId)
            if cId in ignore_activity:
                continue
            ret_list.append({'activity_type': cId,'has_red_point': False})

        return ret_list


def get_nile_redpoint_count_by_type(activity_type):
    count = 0
    if global_data.nile_sdk:
        count = 1 if global_data.nile_sdk.get_activity_reddot(activity_type) else 0
    return count


def is_nile_activity(activity_type):
    conf = confmgr.get('nile_activity_conf', str(activity_type), default={})
    if conf:
        return True
    return False


def is_nile_activity_finished(activity_type):
    if global_data.nile_sdk:
        return not global_data.nile_sdk.get_activity_status(activity_type)
    else:
        return True


def nile_activity_type_to_nile_id(activity_type):
    cNileID = confmgr.get('nile_activity_conf', str(activity_type), 'cNileID', default='0')
    return cNileID


def nile_id_to_activity_type(nile_id):
    conf = confmgr.get('nile_activity_conf', default={})
    for key, data_conf in six.iteritems(conf):
        if data_conf.get('cNileID') == str(nile_id):
            return str(key)

    return None


def jump_to_nile_activity(activity_type):
    activity_type = str(activity_type)
    if not is_nile_activity(activity_type):
        global_data.game_mgr.show_tip(get_text_local_content(705061))
        return
    if not global_data.nile_sdk:
        global_data.game_mgr.show_tip(get_text_local_content(705061))
        return
    is_ready = global_data.nile_sdk.get_activity_status(activity_type)
    if not is_ready:
        global_data.game_mgr.show_tip(get_text_local_content(705061))
        return
    from logic.gutils.activity_utils import get_activity_jump_args, get_activity_widget_type, lower_activity_level_limit
    from logic.gutils.jump_to_ui_utils import ACTIVITY_MAIN_UI
    w_t = get_activity_widget_type(activity_type)
    ui_info = ACTIVITY_MAIN_UI.get(w_t, ACTIVITY_MAIN_UI['default'])
    if ui_info.get('lv_limit', False) and lower_activity_level_limit(str(activity_type)):
        unlock_lv = confmgr.get('nile_activity_conf', str(activity_type), 'iLevel', default=1)
        global_data.game_mgr.show_tip(get_text_by_id(603007).format(unlock_lv))
        return
    ui = global_data.ui_mgr.get_ui(ui_info['ui_name'])
    if ui:
        ui.clear_show_count_dict()
        ui.hide_main_ui()
    else:
        ui = global_data.ui_mgr.show_ui(ui_info['ui_name'], ui_info['ui_path'])
    ui.try_select_tab(activity_type)