# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/social_wrap.py
from __future__ import absolute_import
from __future__ import print_function
import six
import unisdk
import json

def get_property_ignore_self(name):
    getter = getattr(unisdk, 'get' + name)
    setter = getattr(unisdk, 'set' + name, None)

    def setter_imp(self, val):
        print('set channel callback', name, val, setter)
        return setter(val)

    return property(lambda self: getter(), setter_imp if setter else None)


def call_wrapper(name):
    func = getattr(unisdk, name)

    def notifier(*args, **kwargs):
        print('callfunc', name, args, kwargs)
        return func(*args, **kwargs)

    return notifier


class ChannelWrapper(object):
    mapping = {'logout_callback': 'OnLogoutDone',
       'login_callback': 'OnLoginDone',
       'is_daren_updated_callback': 'OnQueryIsDarenUpdated',
       'extend_callback': 'OnExtendFuncCall',
       'protocol_finish_callback': 'OnProtocolFinish',
       'platform': 'Platform',
       'web_view_callback': 'OnWebviewNativeCall',
       'code_scan_callback': 'OnCodeScannerFinish'
       }
    for _old_name, _new_name in six.iteritems(mapping):
        locals()[_old_name] = get_property_ignore_self(_new_name)

    def __init__(self):
        self.name = unisdk.getChannel() or 'null'
        self.sdk_version = unisdk.getSDKVersion(unisdk.ntGetChannelID() or 'null')
        self.distribution_channel = unisdk.getChannel()
        self.udid = unisdk.getUdid()
        print('sdk info', self.name, unisdk.ntGetChannelID(), unisdk.getChannel())
        self.init_method_wrapper()
        self.init_orbit()
        self._init_unisdk()
        self._init_deeplinks()

    def _init_deeplinks(self):
        import game
        game.on_app_browsing_web = self._on_app_browsing_web

    def _on_app_browsing_web(self, info):
        try:
            info_dict = json.loads(info)
            host = info_dict.get('host', '')
            if host != 'game.163.com':
                return
            for key, value in six.iteritems(info_dict):
                if key not in ('url', 'host'):
                    unisdk.setPropStr(str(key), str(value))

            if global_data.player:
                global_data.player.filter_and_report_new_tpa_data(info_dict)
                global_data.player.on_deeplink_rewake(info_dict)
        except:
            return

    def _init_unisdk(self):
        import game3d
        unisdk.setOnQueryFriendListInGameFinished(self._on_query_fb_friend_in_game_cb)
        unisdk.setOnQuerySkuDetailsFinished(self._new_query_product_callback)
        unisdk.setOnOrderCheckDone(self._new_order_callback)
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            hwnd = game3d.get_window_handle()
            unisdk.setPropStr('NT_GAME_WND_HANDLE', str(hwnd))
        unisdk.ntInit()

    def init_method_wrapper(self):
        mapping = {'get_prop_str': 'getPropStr',
           'set_prop_str': 'setPropStr',
           'get_prop_int': 'getPropInt',
           'set_prop_int': 'setPropInt',
           'drpf': 'DRPF',
           'is_init': 'isInit',
           'login': 'ntLogin',
           'open_manager': 'ntOpenManager',
           'extend_func': 'ntExtendFunc',
           'open_web_view': 'ntOpenWebView',
           'get_auth_type': 'getAuthTypeName',
           'show_compact_view': 'ntShowCompactView',
           'game_login_success': 'ntGameLoginSuccess',
           'is_daren_updated': 'ntIsDarenUpdated',
           'present_qrcode_scanner': 'ntPresentQRCodeScanner',
           'set_user_info': 'setUserInfo',
           'push_game_voice_data': 'ntPushGameVoice',
           'upload_user_info': 'ntUpLoadUserInfo'
           }
        for src, module_func_name in six.iteritems(mapping):
            setattr(self, src, call_wrapper(module_func_name))

    def __str__(self):
        return self.name

    def __setattr__(self, key, val):
        print('set channel new key', key, val)
        super(ChannelWrapper, self).__setattr__(key, val)

    @property
    def available_pay_channels(self):
        if unisdk.getAppChannel():
            return unisdk.getAppChannel()
        else:
            return self.name

    def query_product(self, pids):
        return unisdk.ntQuerySkuDetails('inapp', pids)

    def query_product_callback(self, *args):
        pass

    def _new_query_product_callback(self, *args):
        if args:
            try:
                info_lst = args[0]
                if info_lst:
                    dict_info = {}
                    for product_info in info_lst:
                        p_id = product_info.productId
                        p_price = product_info.price
                        p_currency = product_info.priceCurrencyCode
                        dict_info[p_id] = {'price': p_price,'currency': p_currency}

                    global_data.emgr.update_charge_info_by_sdk.emit(dict_info)
                    log_error('[ChannelWrapper] _new_query_product_callback:', dict_info)
            except:
                import exception_hook
                exception_hook.post_error('on_query_product_callback jsons loads error %s' % args)

    def order_product(self, product_id, order_id, order_count, order_desc, etc):
        aid = unisdk.getPropStr('USERINFO_AID')
        uid = unisdk.getPropStr('USERINFO_UID')
        if not aid or not uid:
            return
        order_info = unisdk.OrderInfo(str(product_id))
        order_info.aid = aid
        order_info.orderId = order_id
        order_info.count = order_count
        order_info.orderDesc = order_desc
        order_info.orderEtc = etc
        order_info.userName = str(global_data.player.uid)
        order_info.userData = str(global_data.player.uid)
        order_info.serverId = str(global_data.channel.get_host_num())
        unisdk.ntCheckOrder(order_info)

    def _new_order_callback(self, orderInfo):
        global_data.ui_mgr.close_ui('Charging')
        order_status = orderInfo.orderStatus
        if order_status != 2:
            err_reason = orderInfo.orderErrReason
            if G_IS_NA_USER:
                global_data.game_mgr.show_tip(get_text_by_id(154))
                global_data.emgr.buy_good_fail.emit()
            info = {'order_id': str(id) if id else '','order_status': str(order_status) if order_status else '',
               'order_reason': str(err_reason) if err_reason else ''
               }
            from logic.gutils.salog import SALog
            SALog.get_instance().write(SALog.ORDER_FAILED, info)
            if G_IS_NA_USER:
                if 'Null data in IAB result' in str(err_reason):
                    from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
                    NormalConfirmUI2(content=get_text_by_id(12123))

    def is_downloader_enable(self):
        return False

    def init_downloader(self):
        pass

    def init_orbit(self):
        unisdk.setOnDownloadFinish(self.onDownloadFinish)
        unisdk.setOnDownloadInited(self.onDownloadInited)
        unisdk.setOnDownloadProgress(self.onDownloadProgress)
        unisdk.download.init()
        self.orbit_callback = None
        return

    def onDownloadFinish(self, *args):
        print('onDownloadFinish', args)
        if self.orbit_callback:
            self.orbit_callback(args[0], 1, 1)

    def onDownloadInited(self, *args):
        print('onDownloadInited', args)

    def onDownloadProgress(self, *args):
        print('onDownloadProgress', args)

    def start_download(self, json, callback):
        print('start download file', json, callback)
        self.orbit_callback = callback
        unisdk.download.extendFunc(json)

    def stop_download(self, url, callback):
        pass

    def query_fb_friend_info(self, code):
        if code == 3:
            unisdk.ntQueryFriendList()
        elif code == 1:
            unisdk.ntQueryFriendListInGame()
        elif code == 0:
            unisdk.ntQueryAvailablesInvitees()
        else:
            unisdk.ntQueryMyAccount()

    def _on_query_fb_friend_in_game_cb(self, *args):
        log_error('[ChannelWrapper] on_query_fb_friend_in_game_cb:', args)


s_inst = ChannelWrapper()
OK = 0
FAILED = 1
NOLOGIN = 2
NEED_RELOGIN = 3

def get_channel():
    return s_inst