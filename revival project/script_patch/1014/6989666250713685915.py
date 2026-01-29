# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impRealName.py
from __future__ import absolute_import
import base64
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Bool, Str
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.realname.RealNameRegisterMgr import RealNameRegisterMgr
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from logic.gcommon import const
from logic.gcommon import time_utility as tutil

class impRealName(object):

    def _init_realname_from_dict(self, bdict):
        self._age_range = bdict.get('age_range', const.AGE_RANGE_UNKONWN)
        self._check_realname = bdict.get('check_realname', False)
        self._verify_status = bdict.get('verify_status', const.REALNAME_VERIFY_UNKNOWN)
        self._today_birthday = bdict.get('today_birthday', False)

    @rpc_method(CLIENT_STUB, (Int('tid'),))
    def notify_realname(self, tid):
        self.show_realname_notification(tid)

    def show_realname_notification(self, text_id):
        RealNameRegisterMgr().show_realname_notification(text_id, confirm_callback=self.show_realname_dialog)

    def show_realname_dialog(self):
        RealNameRegisterMgr().show_realname_dialog(self._realname_result, ui_confirm_cb=self.regist_realname)

    def _realname_result(self, success):
        if success:
            global_data.emgr.realname_state_change.emit()
            NormalConfirmUI2(on_confirm=self.change_to_login).set_content_string(81985)

    def show_birthday_tip(self):
        if not self._check_realname:
            return
        if self._today_birthday:
            NormalConfirmUI2().set_content_string(82113)

    @rpc_method(CLIENT_STUB, (Bool('relogin'), Int('age_range')))
    def realname_state_change_action(self, relogin, age_range):
        if relogin:
            NormalConfirmUI2(on_confirm=self.change_to_login).set_content_string(81985)
            return
        self._age_range = age_range

    def regist_realname(self, realname, id_num, region_id):
        try:
            id_num_base64 = base64.encodestring(str(id_num))
        except:
            global_data.emgr.regist_realname_result.emit(False, get_text_by_id(81986))
        else:
            self.call_server_method('regist_realname', (realname, id_num_base64, region_id))

    @rpc_method(CLIENT_STUB, (Bool('ret'), Str('msg')))
    def regist_realname_ret(self, ret, msg):
        global_data.emgr.regist_realname_result.emit(ret, msg)

    @rpc_method(CLIENT_STUB, (Int('msg_tid'),))
    def regist_realname_failed(self, msg_tid):
        global_data.emgr.regist_realname_result.emit(False, get_text_by_id(msg_tid))

    def is_realname(self):
        return global_data.channel.get_realname_state()

    def is_realname_verify_fail(self):
        return self._verify_status == const.REALNAME_VERIFY_FAIL