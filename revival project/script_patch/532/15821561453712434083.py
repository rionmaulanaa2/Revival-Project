# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/skin_tag_utils.py
from __future__ import absolute_import
import math
import time
import copy
from logic.client.const import mall_const
import logic.gcommon.const as gconst
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc, get_lobby_item_pic_by_item_no, get_lobby_item_model_display_info, get_lobby_item_type, get_lobby_item_model_scale, get_lobby_item_use_parms
from logic.gcommon.item import lobby_item_type
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils import task_utils
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const
from logic.client.const import lobby_model_display_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.vscene.parts.gamemode.GMDecorator import halt_by_create_login
from logic.gcommon.item import item_const
from logic.gcommon.time_utility import get_server_time
import math
import time
import copy
from logic.client.const import mall_const
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc, get_lobby_item_pic_by_item_no, get_lobby_item_model_display_info, get_lobby_item_type, get_lobby_item_model_scale, get_lobby_item_use_parms
from logic.gcommon.item import lobby_item_type
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils import task_utils
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const
from logic.client.const import lobby_model_display_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.vscene.parts.gamemode.GMDecorator import halt_by_create_login
from logic.gcommon.item import item_const
from logic.gcommon.time_utility import get_server_time

def granbelm_tag_init_func(node, item_no, tag):
    item_type = get_lobby_item_type(item_no)
    if item_type in (lobby_item_type.L_ITEM_TYPE_ROLE, lobby_item_type.L_ITEM_TYPE_ROLE_SKIN):
        node.moon_mech.setVisible(False)
        node.moon_role.setVisible(True)
    elif item_type in (lobby_item_type.L_ITEM_TYPE_MECHA, lobby_item_type.L_ITEM_TYPE_MECHA_SKIN):
        node.moon_mech.setVisible(True)
        node.moon_role.setVisible(False)
    else:
        node.moon_mech.setVisible(True)
        node.moon_role.setVisible(False)


def season_tag_init_func(node, item_no, tag, season):
    node.lab_season.SetString('S' + str(season))


def get_limit_tag_path(item_no, big, img_path_dict):
    img_path_key = 'role'
    item_type = get_lobby_item_type(item_no)
    if item_type in (lobby_item_type.L_ITEM_TYPE_MECHA, lobby_item_type.L_ITEM_TYPE_MECHA_SKIN) and 'mecha' in img_path_dict:
        img_path_key = 'mecha'
    if big and img_path_key + '_big' in img_path_dict:
        img_path_key = img_path_key + '_big'
    return img_path_dict[img_path_key]