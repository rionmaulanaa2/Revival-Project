# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/title_utils.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon.common_const import title_const
from logic.gcommon.common_utils.local_text import get_text_by_id

def get_title_lv(item_no):
    return confmgr.get('title_conf', str(item_no), 'title_lv', default=1)


def is_title(item_no):
    if item_no is None:
        return False
    else:
        return False


def get_title_name(item_no):
    return item_utils.get_lobby_item_name(item_no)


def get_title_type_name(item_no):
    t_type = get_title_type(item_no)
    name_id = confmgr.get('title_type_def', str(t_type), 'name_id', default=None)
    if name_id is None:
        return ''
    else:
        return get_text_by_id(name_id)


def get_title_type(item_no):
    return confmgr.get('title_conf', str(item_no), 't_type', default=title_const.TITLE_TYPE_UNKNOWN)


def is_title_owned(item_no):
    try:
        item_no = int(item_no)
        if global_data.player:
            return global_data.player.has_item_by_no(item_no)
        return False
    except Exception as e:
        log_error(e)
        return False


def get_cur_title():
    if global_data.player:
        return global_data.player.get_cur_title()
    else:
        return None
        return None


def get_title_duration(item_no):
    return confmgr.get('title_conf', str(item_no), 'keep_duration', default=0.01)


def get_title_cocos_width_in_cam_space(title_template_node_width):
    width_in_cam = 22.3 / 400 * title_template_node_width
    return width_in_cam