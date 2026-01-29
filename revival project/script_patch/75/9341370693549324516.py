# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Assault/AssaultRoomCloseTipsUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
import cc
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.utils.timer import CLOCK
from logic.gcommon import time_utility as tutil

class AssaultRoomCloseTipsUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_assault/battle_assault_tips_end_countdown'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'show_assault_room_close_tips': 'show_assault_room_close_tips',
       'hide_assault_room_close_tips': 'hide_assault_room_close_tips'
       }

    def on_init_panel(self, *args, **kwargs):
        self._tick_timer = None
        self.panel.lab_text_2.setVisible(False)
        return

    def destroy_timer(self):
        if self._tick_timer:
            global_data.game_mgr.unregister_logic_timer(self._tick_timer)
        self._tick_timer = None
        return

    def show_assault_room_close_tips(self, end_timestamp, reason):
        self.destroy_timer()

        def tick(end_timestamp=end_timestamp):
            server_time = tutil.time()
            if server_time >= end_timestamp:
                return
            last_time = end_timestamp - server_time
            self.panel.lab_text.SetString(get_text_by_id(18340).format(num=int(last_time)))

        self._tick_timer = global_data.game_mgr.register_logic_timer(tick, interval=1.0, times=-1, mode=CLOCK)
        self.panel.lab_text_2.setVisible(True)
        self.panel.lab_text_2.SetString(reason)
        self.panel.lab_text.SetString(get_text_by_id(18340).format(num=int(end_timestamp - tutil.time())))

    def hide_assault_room_close_tips(self):
        self.destroy_timer()
        self.panel.lab_text_2.setVisible(False)

    def on_finalize_panel(self):
        self.destroy_timer()