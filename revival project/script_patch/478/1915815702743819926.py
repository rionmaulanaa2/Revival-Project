# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impAntiAddiction.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict, Int
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2, SecondConfirmDlg2
from logic.comsys.guide_ui.GuideSetting import GuideSetting
from logic.gcommon.common_utils.local_text import get_text_by_id

class impAntiAddiction(object):

    def _init_antiaddiction_from_dict(self, bdict):
        self.anti_addiction_msg = bdict.get('anti_addiction_msg', '')

    def _destroy_antiaddiction(self):
        pass

    def show_antiaddiction_msg(self):
        if G_IS_NA_USER:
            return
        if not self.anti_addiction_msg:
            return

        def confirm_cb():
            self._clear_antiaddiction_msg()
            if not global_data.player:
                return
            if global_data.player.is_realname_verify_fail():
                from logic.comsys.chat import chat_link

                def touch_callback(dict_str, ele, touch, touch_event):
                    chat_link.link_touch_callback(dict_str)

                msg = get_text_by_id(82101)
                msg = chat_link.linkstr_to_richtext(msg)
                ui = NormalConfirmUI2()
                ui.set_content_string(msg)
                ui.panel.temp_second_confirm.lab_content.SetCallback(touch_callback)
            else:
                global_data.player.show_birthday_tip()

        NormalConfirmUI2(on_confirm=confirm_cb).set_content_string(self.anti_addiction_msg)

    def _clear_antiaddiction_msg(self):
        self.anti_addiction_msg = ''

    @rpc_method(CLIENT_STUB, (Int('text_id'),))
    def show_curfew_countdown(self, text_id):
        NormalConfirmUI2().set_content_string(text_id)