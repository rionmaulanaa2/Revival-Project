# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/client/const/share_const.py
from __future__ import absolute_import
import game3d
APP_SHARE_FACEBOOK = 1
APP_SHARE_TWITTER = 2
APP_SHARE_LINE = 3
APP_SHARE_MESSENGER = 4
APP_SHARE_LINEGAME = 5
APP_SHARE_MOBILE_QQ = 6
APP_SHARE_MOBILE_QZONE = 7
APP_SHARE_WEIXIN = 8
APP_SHARE_WEIXIN_MOMENT = 9
APP_SHARE_DOUYIN = 10
APP_SHARE_KUAISHOU = 11
APP_SHARE_WEIBO = 12
APP_SHARE_YOUTUBE = 13
APP_SHARE_GODLIKE = 14
APP_SHARE_WEIXIN_MINI_PROGRAM = 15
NT_SHARE_TYPE_WEIBO = 100
NT_SHARE_TYPE_WEIBO_ATTENTION = 117
NT_SHARE_TYPE_WEIXIN_FRIEND = 101
NT_SHARE_TYPE_WEIXIN_TIMELINE = 102
NT_SHARE_TYPE_WEIXIN_MINI_PROGRAM = 301
NT_SHARE_TYPE_QQ = 105
NT_SHARE_TYPE_QZONE = 106
NT_SHARE_TYPE_FACEBOOK = 108
NT_SHARE_TYPE_FACEBOOK_MESSENGER = 115
NT_SHARE_TYPE_FACEBOOK_LIKE = 116
NT_SHARE_TYPE_WHATSAPP = 120
NT_SHARE_TYPE_TWITTER_ANDROID = 111
NT_SHARE_TYPE_TWITTER_IOS = 114
NT_SHARE_TYPE_TWITTER_2 = 202
NT_SHARE_TYPE_LINE_IOS = 111
NT_SHARE_TYPE_LINE_ANDROID = 114
NT_SHARE_TYPE_YOUTUBE = 122
NT_SHARE_TYPE_LINE_2 = 203
NT_SHARE_TYPE_DOUYIN = 302
NT_SHARE_TYPE_KUAISHOU = 303
NT_SHARE_TYPE_GODLIKE_TIMELINE = 124
NT_SHARE_TYPE_GODLIKE_FRIEND = 125
SH_METHOD_SOCIAL_CHANNEL = 1
SH_METHOD_SOCIAL_CHANNEL_SIMPLE = 2
TYPE_IMAGE = 'TYPE_IMAGE'
TYPE_LINK = 'TYPE_LINK'
TYPE_VIDEO = 'TYPE_VIDEO'
TYPE_MINI_PROGRAM = 'TYPE_MINI_PROGRAM'
TYPE_GIF = 'TYPE_GIF'
TYPE_TEXT_ONLY = 'TYPE_TEXT_ONLY'
TYPE_IMAGE_ONLY = 'TYPE_IMAGE_ONLY'
DEEP_LINK_JOIN_TEAM = 'deeplink_join_team'
DEEP_LINK_JOIN_TEAM_FROM_NAME = 'deeplink_join_team_from_name'
DEEP_LINK_ADD_FRIEND = 'deeplink_add_friend'
DEEP_LINK_RECRUIT = 'deeplink_recruit'
DEEP_LINK_GIVE_COINS = 'deeplink_give_coins'
DEEP_LINK_KIZUNA_AI_RECRUIT = 'deeplink_kizuna_ai_recruit'
DEEP_LINK_JOIN_CUSTOMROOM = 'deeplink_join_customroom'
DEEP_LINK_CUSTOMROOM_OWNER_NAME = 'deep_link_customroom_owner_name'
DEEP_LINK_CUSTOMROOM_ID = 'deeplink_customroom_id'
DEEP_LINK_CUSTOMROOM_TYPE = 'deeplink_customroom_type'
DEEP_LINK_CUSTOMROOM_NEED_PWD = 'deeplink_customroom_need_pwd'
DEEPLINK_JUMP_TO_LOTTERY = 'deeplink_jump_to_lottery'
DEEPLINK_JUMP_TO_ACTIVITY = 'deeplink_jump_to_activity'
DEEPLINK_JUMP_TO_MALL = 'deeplink_jump_to_mall'
P_DOUYIN_NAME = 'douyinshare' if game3d.get_platform() != game3d.PLATFORM_IOS else 'Douyin'

def get_toutiao_share_exclude():
    exclude = []
    try:
        from common.platform.channel_const import C_TOUTIAO_NAME
        g_channel = global_data.channel
        toutiao_no_douyin_version = '2.0.5.0'
        if g_channel and g_channel.get_name() == C_TOUTIAO_NAME:
            from common.utilities import compare_version
            is_no_douyin_version = compare_version(g_channel.get_sdk_version(), toutiao_no_douyin_version) == 0
            if is_no_douyin_version and not g_channel.ng_has_platform(P_DOUYIN_NAME):
                exclude.append(APP_SHARE_DOUYIN)
    except:
        pass

    return exclude


CHANNEL_SHARE_EXCLUDE_TABLE = {'kuaishou_new': [
                  APP_SHARE_WEIXIN, APP_SHARE_WEIXIN_MOMENT],
   'toutiao_sdk': get_toutiao_share_exclude()
   }
MAINLAND_CHANNEL_QR_CODE_MAP = {'netease': 'gui/ui_res_2/share/mainland_qrcode/netease.png',
   'bilibili_sdk': 'gui/ui_res_2/share/mainland_qrcode/bilibili_sdk.png',
   'uc_platform': 'gui/ui_res_2/share/mainland_qrcode/uc_platform.png',
   'nearme_vivo': 'gui/ui_res_2/share/mainland_qrcode/nearme_vivo.png',
   'huawei': 'gui/ui_res_2/share/mainland_qrcode/huawei.png',
   'xiaomi_app': 'gui/ui_res_2/share/mainland_qrcode/xiaomi_app.png',
   '4399com': 'gui/ui_res_2/share/mainland_qrcode/4399com.png',
   'toutiao_sdk': 'gui/ui_res_2/share/mainland_qrcode/toutiao_sdk.png',
   'nubia': 'gui/ui_res_2/share/mainland_qrcode/nubia.png',
   'iaround': 'gui/ui_res_2/share/mainland_qrcode/iaround.png',
   'juefeng': 'gui/ui_res_2/share/mainland_qrcode/juefeng.png',
   'yixin': 'gui/ui_res_2/share/mainland_qrcode/yixin.png',
   'kuchang': 'gui/ui_res_2/share/mainland_qrcode/kuchang.png',
   'guopan': 'gui/ui_res_2/share/mainland_qrcode/guopan.png',
   'netease.taptap_cps_dev': 'gui/ui_res_2/share/mainland_qrcode/netease.taptap_cps_dev.png',
   'netease.hykb_cps_dev': 'gui/ui_res_2/share/mainland_qrcode/netease.hykb_cps_dev.png',
   'myapp': 'gui/ui_res_2/share/mainland_qrcode/myapp.png'
   }

def exclude_os_ver(os_name, os_ver):
    if global_data.deviceinfo.get_os_name() == os_name:
        if global_data.deviceinfo.get_os_ver() == os_ver:
            return False
    return True


def exclude_os(os_name):
    if global_data.deviceinfo.get_os_name().lower() == os_name.lower():
        return False
    return True


def init_platform_list():
    from common.platform.dctool import interface
    from logic.client.const import share_const
    plat = game3d.get_platform()
    if plat != game3d.PLATFORM_ANDROID:
        twitter_ty = share_const.NT_SHARE_TYPE_TWITTER_IOS
        line_ty = share_const.NT_SHARE_TYPE_LINE_IOS
    else:
        twitter_ty = share_const.NT_SHARE_TYPE_TWITTER_ANDROID
        line_ty = share_const.NT_SHARE_TYPE_LINE_ANDROID
    if not interface.is_mainland_package():
        share_apps_dict = {share_const.APP_SHARE_FACEBOOK: {'pic': 'gui/ui_res_2/share/fb.png',
                                            'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL,
                                                           'platform_name': 'facebook' if plat == game3d.PLATFORM_ANDROID else 'fbapi://',
                                                           'channel': share_const.NT_SHARE_TYPE_FACEBOOK,
                                                           'args': [],'platform_enum': share_const.APP_SHARE_FACEBOOK,
                                                           'auth_type': 'fb'
                                                           },
                                            'share_types': [
                                                          share_const.TYPE_IMAGE, share_const.TYPE_LINK, share_const.TYPE_VIDEO]
                                            },
           share_const.APP_SHARE_TWITTER: {'pic': 'gui/ui_res_2/share/tw.png',
                                           'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL,
                                                          'platform_name': 'twitter' if plat == game3d.PLATFORM_ANDROID else 'twitter://',
                                                          'channel': twitter_ty,
                                                          'args': [],'platform_enum': share_const.APP_SHARE_TWITTER,
                                                          'auth_type': 'twitter'
                                                          },
                                           'type_channel': {share_const.TYPE_VIDEO: share_const.SH_METHOD_SOCIAL_CHANNEL_SIMPLE},'share_types': [
                                                         share_const.TYPE_IMAGE, share_const.TYPE_LINK, share_const.TYPE_VIDEO]
                                           },
           share_const.APP_SHARE_LINE: {'pic': 'gui/ui_res_2/share/line.png',
                                        'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL_SIMPLE,
                                                       'platform_name': 'line' if plat == game3d.PLATFORM_ANDROID else 'line://',
                                                       'channel': line_ty,
                                                       'args': [],'platform_enum': share_const.APP_SHARE_LINE,
                                                       'auth_type': 'line'
                                                       },
                                        'share_types': [
                                                      share_const.TYPE_IMAGE, share_const.TYPE_LINK, share_const.TYPE_VIDEO]
                                        },
           share_const.APP_SHARE_MESSENGER: {'pic': 'gui/ui_res_2/share/messenger.png',
                                             'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL,
                                                            'platform_name': 'messenger' if plat == game3d.PLATFORM_ANDROID else 'fb-messenger-share-api://',
                                                            'channel': share_const.NT_SHARE_TYPE_FACEBOOK_MESSENGER,
                                                            'args': [],'platform_enum': share_const.APP_SHARE_MESSENGER,
                                                            'auth_type': 'messenger'
                                                            },
                                             'share_types': [
                                                           share_const.TYPE_IMAGE, share_const.TYPE_LINK]
                                             },
           share_const.APP_SHARE_YOUTUBE: {'pic': 'gui/ui_res_2/share/youtube_icon.png',
                                           'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL_SIMPLE,
                                                          'platform_name': 'youtube',
                                                          'channel': share_const.NT_SHARE_TYPE_YOUTUBE,
                                                          'args': [],'platform_enum': share_const.APP_SHARE_YOUTUBE,
                                                          'auth_type': 'youtube'
                                                          },
                                           'share_types': [
                                                         share_const.TYPE_VIDEO],
                                           'check_func': lambda share_type: exclude_os('iOS') if share_type == share_const.TYPE_VIDEO else True
                                           }
           }
    else:
        share_apps_dict = {share_const.APP_SHARE_MOBILE_QQ: {'pic': 'gui/ui_res_2/share/4.png',
                                             'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL,
                                                            'verified_packages_key': 'qq_verified',
                                                            'platform_name': 'QQ',
                                                            'channel': share_const.NT_SHARE_TYPE_QQ,
                                                            'args': [],'platform_enum': share_const.APP_SHARE_MOBILE_QQ,
                                                            'auth_type': 'qq'
                                                            },
                                             'share_types': [
                                                           share_const.TYPE_IMAGE, share_const.TYPE_LINK, share_const.TYPE_VIDEO, share_const.TYPE_MINI_PROGRAM],
                                             'type_channel': {share_const.TYPE_VIDEO: share_const.SH_METHOD_SOCIAL_CHANNEL_SIMPLE}},
           share_const.APP_SHARE_MOBILE_QZONE: {'pic': 'gui/ui_res_2/share/5.png',
                                                'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL,
                                                               'verified_packages_key': 'qq_verified',
                                                               'platform_name': 'QQ',
                                                               'channel': share_const.NT_SHARE_TYPE_QZONE,
                                                               'args': [],'platform_enum': share_const.APP_SHARE_MOBILE_QZONE,
                                                               'auth_type': 'qzone'
                                                               },
                                                'share_types': [
                                                              share_const.TYPE_IMAGE, share_const.TYPE_LINK, share_const.TYPE_VIDEO],
                                                'type_channel': {share_const.TYPE_VIDEO: share_const.SH_METHOD_SOCIAL_CHANNEL_SIMPLE}},
           share_const.APP_SHARE_WEIXIN: {'pic': 'gui/ui_res_2/share/3.png',
                                          'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL,
                                                         'verified_packages_key': 'weixin_verified',
                                                         'platform_name': 'Weixin',
                                                         'channel': share_const.NT_SHARE_TYPE_WEIXIN_FRIEND,
                                                         'args': [],'platform_enum': share_const.APP_SHARE_WEIXIN,
                                                         'auth_type': 'weixin'
                                                         },
                                          'share_types': [
                                                        share_const.TYPE_IMAGE, share_const.TYPE_LINK, share_const.TYPE_VIDEO]
                                          },
           share_const.APP_SHARE_WEIXIN_MOMENT: {'pic': 'gui/ui_res_2/share/2.png',
                                                 'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL,
                                                                'verified_packages_key': 'weixin_verified',
                                                                'platform_name': 'Weixin',
                                                                'channel': share_const.NT_SHARE_TYPE_WEIXIN_TIMELINE,
                                                                'args': [],'platform_enum': share_const.APP_SHARE_WEIXIN_MOMENT,
                                                                'auth_type': 'weixin_moment'
                                                                },
                                                 'share_types': [
                                                               share_const.TYPE_IMAGE, share_const.TYPE_LINK, share_const.TYPE_VIDEO]
                                                 },
           share_const.APP_SHARE_WEIXIN_MINI_PROGRAM: {'pic': 'gui/ui_res_2/share/3.png',
                                                       'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL,
                                                                      'platform_name': 'Weixin',
                                                                      'verified_packages_key': 'weixin_verified',
                                                                      'channel': share_const.NT_SHARE_TYPE_WEIXIN_MINI_PROGRAM,
                                                                      'args': [],'platform_enum': share_const.APP_SHARE_WEIXIN_MINI_PROGRAM,
                                                                      'auth_type': 'weixin_mini_program'
                                                                      },
                                                       'share_types': [
                                                                     share_const.TYPE_MINI_PROGRAM]
                                                       },
           share_const.APP_SHARE_DOUYIN: {'pic': 'gui/ui_res_2/share/douyin_icon.png',
                                          'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL,
                                                         'verified_packages_key': 'douyin_verified',
                                                         'platform_name': P_DOUYIN_NAME,
                                                         'channel': share_const.NT_SHARE_TYPE_DOUYIN,
                                                         'args': [],'platform_enum': share_const.APP_SHARE_DOUYIN,
                                                         'auth_type': 'douyin'
                                                         },
                                          'share_types': [
                                                        share_const.TYPE_VIDEO]
                                          },
           share_const.APP_SHARE_KUAISHOU: {'pic': 'gui/ui_res_2/share/kuaishou_icon.png',
                                            'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL_SIMPLE,
                                                           'platform_name': 'kuaishou' if game3d.get_platform() != game3d.PLATFORM_IOS else '',
                                                           'channel': share_const.NT_SHARE_TYPE_KUAISHOU,
                                                           'args': [],'platform_enum': share_const.APP_SHARE_KUAISHOU,
                                                           'auth_type': 'kuaishou'
                                                           },
                                            'share_types': [
                                                          share_const.TYPE_VIDEO]
                                            },
           share_const.APP_SHARE_WEIBO: {'pic': 'gui/ui_res_2/share/1.png',
                                         'share_args': {'method': share_const.SH_METHOD_SOCIAL_CHANNEL,
                                                        'platform_name': 'Weibo',
                                                        'channel': share_const.NT_SHARE_TYPE_WEIBO,
                                                        'args': [],'platform_enum': share_const.APP_SHARE_WEIBO,
                                                        'auth_type': 'weibo'
                                                        },
                                         'share_types': [
                                                       share_const.TYPE_IMAGE, share_const.TYPE_LINK, share_const.TYPE_VIDEO]
                                         }
           }
    return share_apps_dict