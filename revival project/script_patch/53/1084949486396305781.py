# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/realname/RealNameRegisterMgr.py
from __future__ import absolute_import
from common.framework import Singleton
from logic.comsys.realname.RealNameRegisterUI import RealNameRegisterUI
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2, NormalConfirmUI2

class RealNameRegisterMgr(Singleton):
    ALIAS_NAME = 'realname_mgr'

    def init(self):
        self._realname_notification = RealNameNotification()
        self._realname_dialog = RealNameDialog()

    def on_finalize(self):
        self._realname_dialog.destroy()
        self._realname_notification.destroy()
        self._realname_dialog = None
        self._realname_notification = None
        return

    def show_realname_notification(self, content, confirm_callback):
        self._realname_notification.show(content, confirm_callback)

    def show_realname_dialog(self, *args, **kwargs):
        self._realname_dialog.show(*args, **kwargs)

    def support_realname_dialog(self):
        channel = global_data.channel
        if not channel:
            return False
        channel_name = channel.get_name()
        if channel_name and channel_name == 'netease':
            return True
        if channel_name and channel_name in ('oppo', ):
            return False
        return channel.is_support_realname_dialog()


class RealNameNotification(object):

    def __init__(self):
        self._channel = global_data.channel
        self._channel_name = self._channel.get_name()
        self._confirm_callback = None
        return

    def destroy(self):
        self._confirm_callback = None
        self._channel_name = None
        return

    def show(self, content, confirm_callback):
        self._confirm_callback = confirm_callback
        if self._channel_name and self._channel_name == 'netease':
            self._netease_realname_notifier(content)
        else:
            self._channel_sdk_realname_notifier(content)

    def _netease_realname_notifier(self, content):
        player = global_data.player
        if not player:
            return
        if player.is_realname() or not player._check_realname:
            return
        NormalConfirmUI2(content=content, on_confirm=self._confirm_callback)

    def _channel_sdk_realname_notifier(self, content):
        player = global_data.player
        if not player:
            return
        if player.is_realname():
            return
        if self._channel and self._channel.is_support_realname_dialog():
            SecondConfirmDlg2().confirm(content=content, confirm_callback=self._confirm_callback)


DIALOG_KEY_NETEASE = 'netease'
DIALOG_KEY_OPPO = 'oppo'
DIALOG_KEY_SDK = 'sdk'
DIALOG_KEY_NOT_SUPPORT = 'not_support'

class RealNameDialog(object):

    def __init__(self):
        self._channel = global_data.channel
        self._channel_name = self._channel and self._channel.get_name()
        self._ui_confirm_callback = None
        self._realname_dialog_callback = None
        self._REALNAME_DIALOG_HANDLER = {DIALOG_KEY_NETEASE: self._open_netease_realname_dialog,
           DIALOG_KEY_OPPO: self._open_oppo_realname_dialog,
           DIALOG_KEY_SDK: self._open_sdk_realname_dialog,
           DIALOG_KEY_NOT_SUPPORT: self._show_realname_guide_notification
           }
        return

    def destroy(self):
        self._realname_dialog_callback = None
        self._ui_confirm_callback = None
        return

    def show(self, ret_callback, ui_confirm_cb=None):
        handler = self._get_realname_dialog_handler()
        self._realname_dialog_callback = ret_callback
        self._ui_confirm_callback = ui_confirm_cb
        handler()

    def _get_realname_dialog_handler(self):
        if self._channel_name:
            if self._channel_name in self._REALNAME_DIALOG_HANDLER:
                return self._REALNAME_DIALOG_HANDLER[self._channel_name]
            if self._channel.is_support_realname_dialog():
                return self._REALNAME_DIALOG_HANDLER[DIALOG_KEY_SDK]
        return self._REALNAME_DIALOG_HANDLER[DIALOG_KEY_NOT_SUPPORT]

    def _open_netease_realname_dialog(self):
        confirm_cb = self._ui_confirm_callback or global_data.player.regist_realname
        RealNameRegisterUI(confirm_cb=confirm_cb, close_cb=self._netease_realname_callback)

    def _open_oppo_realname_dialog(self):
        if not self._channel:
            return False
        extend_callback_dict = self._channel.extend_callback_dict
        method_name = 'doGetVerifiedInfo'
        extend_data_dict = {'methodId': method_name
           }
        extend_callback_dict[method_name] = self._oppo_realname_callback
        self._channel.extend_func_by_dict(extend_data_dict)

    def _open_sdk_realname_dialog(self):
        self._channel.show_realname_dialog(self._sdk_realname_callback)

    def _show_realname_guide_notification(self):

        def callback():
            self._realname_dialog_callback(success=False)

        NormalConfirmUI2(content=82055, on_confirm=callback)

    def _netease_realname_callback(self, verify_result):
        success = verify_result['success']
        if self._realname_dialog_callback:
            self._realname_dialog_callback(success=success)

    def _oppo_realname_callback(self, verify_result):
        callback_str = verify_result.get('callback')
        if callback_str == 'onSuccess':
            try:
                self._realname_dialog_callback(success=True)
            except Exception as e:
                log_error('oppo_realname_callback -  parse age failed %s', str(e))

        elif callback_str == 'onFailure':
            resultMsg = verify_result.get('resultMsg')
            self._realname_dialog_callback(success=False)
        else:
            log_error('oppo_realname_callback - unknown callback %s' % callback_str)
            self._realname_dialog_callback(success=False)

    def _sdk_realname_callback(self, realname_result):
        result = realname_result.get('result')
        XIAOMI_CHANNEL_NAME = 'xiaomi_app'
        if result is None and self._channel_name == XIAOMI_CHANNEL_NAME:
            self._realname_dialog_callback(success=True)
            return
        else:
            if result is not None:
                self._realname_dialog_callback(success=bool(result))
                return
            self._realname_dialog_callback(success=True)
            return