# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/HintLineUI.py
from __future__ import absolute_import
import six
import time
from cocosui import cc, ccui, ccs
from common.platform import channel_const
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_const import friend_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

def query_friend_apply_from_line(callback):
    if not global_data.channel.is_bind_linegame():
        callback()
        return
    if not global_data.message_data:
        return
    apply_friends = global_data.message_data.get_apply_friends()
    for uid, data in six.iteritems(apply_friends):
        social_ids = data.get('social_ids', {}).get(friend_const.SOCIAL_ID_TYPE_LINEGAME, [])
        if social_ids:
            check_hint_line(callback)
            return

    callback()


def check_hint_line(callback):
    if not global_data.channel.is_bind_linegame():
        callback()
        return
    channel_line_warning = global_data.achi_mgr.get_cur_user_archive_data('channel_line_warning', default=False)
    if not channel_line_warning:
        ui = global_data.ui_mgr.show_ui('HintLineUI', 'logic.comsys.message')
        ui.set_end_callback(callback)
    else:
        callback()


class HintLineUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'friend/hint_line'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_done.btn_common.OnClick': 'on_accept_all'
       }

    def on_init_panel(self, *args, **kargs):
        super(HintLineUI, self).on_init_panel()
        self._end_callback = None
        return

    def on_accept_all(self, *args):
        self.close()

    def on_login_reconnect(self, *args):
        self.close()

    def on_finalize_panel(self):
        if self._end_callback:
            self._end_callback()
        self._end_callback = None
        global_data.achi_mgr.set_cur_user_archive_data('channel_line_warning', True)
        return

    def set_end_callback(self, callback):
        self._end_callback = callback