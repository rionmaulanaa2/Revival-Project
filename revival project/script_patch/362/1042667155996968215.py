# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/role_utils.py
from __future__ import absolute_import
import six
from common.cfg import confmgr

def has_kizuna_ai(*args):
    return True


ROLE_CHECK_SHOW_HANDLERS = {'has_kizuna_ai': has_kizuna_ai
   }

def get_role_check_show_handler(handler_name):
    return ROLE_CHECK_SHOW_HANDLERS.get(handler_name)


def check_show_role_panel(role_id):
    role_config = confmgr.get('role_info', 'RoleInfo', 'Content')
    check_show_handler_name = role_config.get(str(role_id), {}).get('check_show_handler')
    if not check_show_handler_name:
        return True
    check_show_handler_func = get_role_check_show_handler(check_show_handler_name)
    if check_show_handler_func and not check_show_handler_func():
        return False
    return True


def is_role_publish(role_id):
    return not confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'is_skip', default=0)


LOCK_TIPS_BY_ROLE_LIMIT = {111: 82243
   }

def get_crossover_role_id(role_id):
    role_profile = confmgr.get('role_info', 'RoleProfile', 'Content')
    crossover_roles = role_profile.get(str(role_id), {}).get('crossover_roles', [])
    for role_id in crossover_roles:
        if global_data.player and global_data.player.has_role(role_id):
            return role_id

    return None


def is_crossover_role(role_id):
    role_profile = confmgr.get('role_info', 'RoleProfile', 'Content')
    crossover_roles = role_profile.get(str(role_id), {}).get('crossover_roles')
    if crossover_roles is not None:
        return True
    else:
        return False


def get_crossover_info(role_id):
    role_profile = confmgr.get('role_info', 'RoleProfile', 'Content')
    crossover_info = role_profile.get(str(role_id), {}).get('crossover_info')
    return crossover_info


def check_show_role_panel(role_id):
    role_profile = confmgr.get('role_info', 'RoleProfile', 'Content')
    check_show_handler_name = role_profile.get(str(role_id), {}).get('check_show_handler')
    if not check_show_handler_name:
        return True
    check_show_handler_func = get_role_check_show_handler(check_show_handler_name)
    if check_show_handler_func and not check_show_handler_func():
        return False
    return True


def get_show_role_id_list():
    role_id_list = []
    role_config = confmgr.get('role_info', 'RoleInfo', 'Content')
    if global_data.player:
        open_role_id_list = global_data.player.get_role_open_seq()
        for k, v in six.iteritems(role_config):
            if not is_role_publish(k):
                continue
            goods_id = v.get('goods_id', None)
            if not goods_id:
                continue
            if open_role_id_list and k not in open_role_id_list:
                continue
            if not check_show_role_panel(k):
                continue
            role_id_list.append(k)

    return role_id_list


def get_role_name_id(role_id):
    role_profile = confmgr.get('role_info', 'RoleProfile', 'Content')
    text_id = role_profile.get(str(role_id), {}).get('role_name', 0)
    return text_id