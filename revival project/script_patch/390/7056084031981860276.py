# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/profile_logger/ProfileUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER
from common.const import uiconst

class ProfileUI(BasePanel):
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'test/profile_view'
    UI_ACTION_EVENT = {'btn_dump.OnClick': 'on_click_dump',
       'btn_hide.OnClick': 'on_click_hide',
       'btn_tottime.OnClick': 'on_click_tot',
       'btn_cumtime.OnClick': 'on_click_cum'
       }

    def on_init_panel(self, *args, **kwargs):
        self._stats_info = [
         '', '']
        self._current_info = 0

    def on_click_dump(self, *args):
        import logic.manager
        logic.manager.Manager().dump_one_frame(self.set_prof_text)

    def on_click_hide(self, *args):
        self.nd_dumpinfo.setVisible(False)

    def on_click_tot(self, *args):
        self._current_info = 0
        self.__update_prof_text()

    def on_click_cum(self, *args):
        self._current_info = 1
        self.__update_prof_text()

    def set_model_count(self, count):
        self.lb_count.setString('models:{}'.format(count))

    def set_prof_text(self, texts):
        self._stats_info = texts
        self.__update_prof_text()

    def __update_prof_text(self):
        self.lb_stats.setString(self._stats_info[self._current_info])
        self.nd_dumpinfo.setVisible(True)