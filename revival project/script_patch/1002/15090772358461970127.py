# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/mail_const.py
from __future__ import absolute_import
import six_ex
_reload_all = True
GMAIL_DB_ID = 'global'
MAIL_DATA = 'mails'
MAIL_DATA_KEYS = set()
__MAIL_KEY = lambda key: MAIL_DATA_KEYS.add(key) or key
GMAIL_ID = __MAIL_KEY('gid')
MAIL_ID = __MAIL_KEY('mid')
MAIL_KIND = __MAIL_KEY('kind')
MAIL_TAG = __MAIL_KEY('tag')
MAIL_TITLE = __MAIL_KEY('title')
MAIL_CONTENT = __MAIL_KEY('content')
MAIL_ATTACHMENT = __MAIL_KEY('attachment')
MAIL_GATTFLAG = __MAIL_KEY('gattflag')
MAIL_SENDER = __MAIL_KEY('sender')
MAIL_SENDTIME = __MAIL_KEY('sendtime')
MAIL_EXPIRETIME = __MAIL_KEY('expiretime')
MAIL_STATE = __MAIL_KEY('state')
MAIL_MIN_LEVEL = __MAIL_KEY('minlvl')
MAIL_OS = __MAIL_KEY('os')
MAIL_PACKAGE = __MAIL_KEY('package')
MAIL_APP_CHANNEL = __MAIL_KEY('appchannel')
MAIL_RECEIVE_LV = __MAIL_KEY('reclv')
MAIL_RECEIVE_LVER = __MAIL_KEY('lver')
MAIL_RECEIVE_EVER = __MAIL_KEY('ever')
MAIL_DAN = __MAIL_KEY('dan')
MAIL_CHECK_CHECKER = __MAIL_KEY('checker')
MAIL_EXTRA = __MAIL_KEY('extra')
MAIL_TAG_SYS = 0
MAIL_TAG_CREDIT = 1
MAIL_TAG_FRIEND = 2
MAIL_STATE_UNREAD = 0
MAIL_STATE_READ = 1
MAIL_STATE_REWARD_GET = 2
MAIL_ATTACHMENT_TYPE = 'type'
MAIL_ATTACHMENT_CNT = 'cnt'
MAIL_ATTACHMENT_EXPIRE = 'expire'
MAIL_MAX_CNT = 2000
MAIL_PLAYER_MAX_CNT = 200
MAIL_GLOBAL_MAX_CNT = 1000
MAIL_MAX_TIMELEN = 7776000
MAIL_ALL_DEL_MIN_CNT = 10
MAIL_ALL_DEL_MAX_CNT = MAIL_MAX_CNT
MAIL_BROADCAST_TIME = 300
MAIL_KIND_NORMAL = 0
MAIL_KIND_AVATAR_SUMMER_COMPETITION = 1
MAIL_KIND_GLOBAL_ALL_ADS = 100

def check_mail_data(mail_info):
    from logic.gcommon import time_utility as tutil
    from data import lobby_item_data
    for mail_key in six_ex.keys(mail_info):
        if mail_key not in MAIL_DATA_KEYS:
            return False

    if GMAIL_ID not in mail_info:
        if MAIL_TITLE not in mail_info or MAIL_CONTENT not in mail_info:
            return False
    if MAIL_EXPIRETIME in mail_info:
        if mail_info[MAIL_EXPIRETIME] < tutil.get_time():
            return False
    if MAIL_OS in mail_info:
        if type(mail_info[MAIL_OS]) not in [list, tuple]:
            return False
        mail_info[MAIL_OS] = [ os_name.upper() for os_name in mail_info[MAIL_OS] ]
    if MAIL_PACKAGE in mail_info:
        if type(mail_info[MAIL_PACKAGE]) not in [list, tuple]:
            return False
        mail_info[MAIL_PACKAGE] = [ package_type.upper() for package_type in mail_info[MAIL_PACKAGE] ]
    if MAIL_APP_CHANNEL in mail_info:
        if type(mail_info[MAIL_APP_CHANNEL]) not in [list, tuple]:
            return False
        mail_info[MAIL_APP_CHANNEL] = [ app_channel.upper() for app_channel in mail_info[MAIL_APP_CHANNEL] ]
    if MAIL_ATTACHMENT in mail_info:
        if type(mail_info[MAIL_ATTACHMENT]) not in [list, tuple]:
            return False
        for item in mail_info[MAIL_ATTACHMENT]:
            for item_key in six_ex.keys(item):
                if item_key not in [MAIL_ATTACHMENT_TYPE, MAIL_ATTACHMENT_CNT, MAIL_ATTACHMENT_EXPIRE]:
                    return False

            if item.get(MAIL_ATTACHMENT_TYPE) not in lobby_item_data.data:
                return False

    return True


def check_mail_app_channel(mail_info, app_channel):
    if MAIL_APP_CHANNEL not in mail_info:
        return True
    mail_app_channel = mail_info[MAIL_APP_CHANNEL]
    app_channel = app_channel.upper()
    if app_channel in mail_app_channel:
        return True
    is_netease_channel = app_channel.startswith('NETEASE')
    if 'NETEASE_CHANNEL' in mail_app_channel and is_netease_channel:
        return True
    if 'NON_NETEASE_CHANNEL' in mail_app_channel and not is_netease_channel:
        return True
    return False