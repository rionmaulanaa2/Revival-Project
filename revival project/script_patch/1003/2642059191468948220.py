# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/NewbieStageEndUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_VKB_NO_EFFECT, NORMAL_LAYER_ZORDER

class NewbieStageEndUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_tdm'
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UI_ACTION_EVENT = {'nd_touch_layer.OnClick': 'on_click_next'
       }

    def on_init_panel(self, finish_cb=None):
        self.hide_main_ui()
        self.finish_cb = finish_cb
        global_data.sound_mgr.play_music('firstplace')
        self.begin_show()

    def on_finalize_panel(self):
        self.panel.stopAllActions()
        self.show_main_ui()
        if self.show_next_timer:
            global_data.game_mgr.unregister_logic_timer(self.show_next_timer)
            self.show_next_timer = None
        return

    def begin_show(self):
        global_data.sound_mgr.play_ui_sound('bt_victory')
        self.panel.PlayAnimation('win')
        self.show_next_timer = global_data.game_mgr.register_logic_timer(self.show_next, interval=28, times=1, args=('guide_new', ))

    def show_next(self, anim_name):
        self.show_next_timer = None
        if self and self.is_valid():
            self.panel.PlayAnimation(anim_name)
        return

    def on_click_next(self, *args):
        if self.finish_cb and callable(self.finish_cb):
            self.finish_cb()
        self.close()