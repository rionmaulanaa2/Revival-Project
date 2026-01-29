# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/debug/GtraceSettingUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER
IsProfile = False
LastTime = 0
TimerId = None
from common.const import uiconst

class GtraceSettingUI(BasePanel):
    PANEL_CONFIG_NAME = 'setting/setting_gtrace'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    MAX_PROFILE_TIME = 600
    UI_ACTION_EVENT = {'profile_start.OnClick': 'on_start',
       'profile_stop.OnClick': 'on_stop'
       }

    def on_init_panel(self):
        self.init_event()

    def on_finalize_panel(self):
        pass

    def init_event(self):
        global LastTime
        global IsProfile
        self.profile_value = LastTime if IsProfile else 60
        nd = self.panel.profile_time
        nd.tf_name.SetString('profile time period')
        nd.tf_value.SetString(str(self.profile_value))
        nd.slider.setPercent(self.profile_value * 100.0 / self.MAX_PROFILE_TIME)

        @nd.slider.unique_callback()
        def OnPercentageChanged(ctrl, slider, *args):
            val = int(slider.getPercent()) / 100.0 * self.MAX_PROFILE_TIME
            self.profile_value = val
            nd.tf_value.SetString(str(self.profile_value))

        if IsProfile:
            self.stop_timer()
            self.start_timer()
        self.update_sate()

    def update_sate(self):
        text = 'Profiling...' if IsProfile else 'Start'
        self.panel.profile_start.SetEnable(not IsProfile)
        self.panel.profile_start.SetText(text)

    def start_timer(self):
        global TimerId
        from common.utils.timer import CLOCK
        tm = global_data.game_mgr.get_logic_timer()
        TimerId = tm.register(func=self.update, interval=1.0, times=-1, mode=CLOCK)

    def stop_timer(self):
        global TimerId
        if TimerId:
            tm = global_data.game_mgr.get_logic_timer()
            tm.unregister(TimerId)
            TimerId = None
        return

    def update(self):
        global LastTime
        global IsProfile
        LastTime -= 1
        if LastTime <= 0:
            self.stop_timer()
            IsProfile = False
        if self and self.is_valid():
            nd = self.panel.profile_time
            nd.tf_value.SetString(str(LastTime))

    def on_start(self, *args):
        global LastTime
        global IsProfile
        IsProfile = True
        LastTime = self.profile_value
        self.start_timer()
        import gtrace
        gtrace.start(20, self.profile_value)
        self.update_sate()
        global_data.game_mgr.show_tip('Begin profile')

    def on_stop(self, *args):
        global IsProfile
        if not IsProfile:
            return
        IsProfile = False
        self.stop_timer()
        import gtrace
        gtrace.stop('/sdcard/prof.gt')
        self.update_sate()
        global_data.game_mgr.show_tip('Finished profile\xef\xbc\x8coutput to /sdcard/prof.gt')