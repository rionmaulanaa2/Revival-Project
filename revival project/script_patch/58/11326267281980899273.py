# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartTouch.py
from __future__ import absolute_import
from . import ScenePart

class PartTouch(ScenePart.ScenePart):
    ENTER_EVENT = {'screen_locker_event': 'on_screen_locker'
       }

    def __init__(self, scene, name):
        super(PartTouch, self).__init__(scene, name)

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('ScreenLockerUI')

    def on_enter(self):
        pass

    def on_exit(self):
        self.destroy_ui()

    def on_screen_locker(self, is_locker, max_locker_time):
        if is_locker:
            ui = global_data.ui_mgr.get_ui('ScreenLockerUI')
            if ui:
                ui.reset_lock_time(max_locker_time)
                return
            from logic.comsys.common_ui.ScreenLockerUI import ScreenLockerUI
            ScreenLockerUI(None, is_auto_unlocker=True, auto_unlocker_time=max_locker_time)
        else:
            global_data.ui_mgr.close_ui('ScreenLockerUI')
        return