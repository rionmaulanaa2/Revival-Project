# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/GoldFeedback.py
from __future__ import absolute_import
from common.const.property_const import *
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI
from common.const.uiconst import SECOND_CONFIRM_LAYER

class GoldFeedback(NormalConfirmUI):

    def on_init_panel(self, *args, **kargs):
        uid = kargs.get('uid', None)
        text = 3206
        if uid:
            data = global_data.message_data.get_player_simple_inf(uid) or {}
            text = get_text_by_id(3205, {'name': data.get(C_NAME, '')})
        super(GoldFeedback, self).on_init_panel(text)
        return