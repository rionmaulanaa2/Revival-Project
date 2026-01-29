# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ReturnPlayerAdvance.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from logic.gutils import jump_to_ui_utils
from logic.gcommon.common_const import activity_const
from logic.gcommon.time_utility import get_server_time
from logic.gutils import template_utils
from logic.gcommon.common_utils.local_text import get_text_by_id

class ReturnPlayerAdvance(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/activity_202206/comeback_sys/open_comeback'
    APPEAR_ANIM = ''

    def set_content(self):

        @self.panel.btn_click.unique_callback()
        def OnClick(*args):
            jump_to_ui_utils.jump_to_activity(activity_const.ACTIVITY_RETURN_GIFT)

        if not global_data.player:
            return
        now_time = get_server_time()
        close_time = global_data.player.activity_closetime_data.get(activity_const.ACTIVITY_RETURN_GIFT, now_time)
        left_time_delta = close_time - now_time
        is_ending, left_text, left_time, left_unit = template_utils.get_left_info(left_time_delta)
        if not is_ending:
            day_txt = get_text_by_id(left_text) + str(left_time) + get_text_by_id(left_unit)
        else:
            day_txt = get_text_by_id(left_text)
        self.panel.lab_time.SetString(day_txt)

    def get_close_node(self):
        return (
         self.panel.btn_close,)