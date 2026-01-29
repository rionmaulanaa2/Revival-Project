# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotterySBanner.py
from __future__ import absolute_import
from logic.gutils import item_utils
from logic.comsys.activity.SimpleAdvance import SimpleAdvance

class LotterySBanner(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/lottery_ss_banner_3'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5
    NEED_GAUSSIAN_BLUR = False
    UI_ACTION_EVENT = {'panel.btn_go.OnClick': 'on_btn_go'
       }
    SKIN_LIST = [
     201801441, 201001543, 201001644]

    def set_content(self):
        self.panel.lab_s_name_1.SetString(item_utils.get_lobby_item_name(self.SKIN_LIST[1]))
        self.panel.lab_s_name_2.SetString(item_utils.get_lobby_item_name(self.SKIN_LIST[2]))
        self.hide_close_btn()

    def hide_close_btn(self):
        pass

    def on_btn_go(self, *args):
        item_utils.jump_to_ui(self.SKIN_LIST[0])