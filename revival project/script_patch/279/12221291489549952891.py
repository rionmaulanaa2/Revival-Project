# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBindReminder.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Str, Dict, Bool, List

class impBindReminder(object):

    def _init_bindreminder_from_dict(self, bdict):
        self._has_reminded_bind = bdict.get('has_reminded_bind', False)
        self._reach_battle_cond = False

    def need_remind_bind(self):
        return global_data.channel.is_guest() and not self._has_reminded_bind

    @rpc_method(CLIENT_STUB, (Bool('is_battle'),))
    def reach_bind_remind_cond(self, is_battle):
        if not is_battle:
            self.check_remind_bind()
        else:
            self._reach_battle_cond = True

    @rpc_method(CLIENT_STUB, ())
    def clear_bind_remind_per_day(self):
        self._has_reminded_bind = False

    def check_remind_bind(self, is_battle=False):
        if not self.need_remind_bind():
            return
        if is_battle and not self._reach_battle_cond:
            return
        self._reach_battle_cond = False
        self._has_reminded_bind = True

        def show_guest_binding():
            global_data.channel.guest_bind()

        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlgForBind
        SecondConfirmDlgForBind().confirm(content=get_text_by_id(3111), cancel_text=3109, confirm_text=3110, confirm_callback=show_guest_binding)
        self.call_server_method('remind_bind')