# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryBannerChristmasBingo.py
from __future__ import absolute_import
from logic.gutils.jump_to_ui_utils import jump_to_lottery
from logic.gutils.item_utils import get_lobby_item_name
from logic.comsys.activity.SimpleAdvance import SimpleAdvance

class LotteryBannerChristmasBingo(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_202112/open_christmas'
    APPEAR_ANIM = 'appear'
    LOOP_ANIM = 'loop'
    LASTING_TIME = 0
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn'
       }
    NEED_GAUSSIAN_BLUR = False

    def on_init_panel(self, *args):
        self.s_plus_skin = 201800144
        self.s_skins = [201001541, 201001347, 201800841, 201800542]
        if G_IS_NA_PROJECT:
            self.s_skins[1] = 201001348
        super(LotteryBannerChristmasBingo, self).on_init_panel(*args)

    def set_content(self):
        self.panel.lab_name.SetString(get_lobby_item_name(self.s_plus_skin))
        self.panel.lab_name.ResizeAndPosition()
        for index, skin_id in enumerate(self.s_skins):
            nd = getattr(self.panel, 'lab_name_%d' % (index + 1))
            nd.SetString(get_lobby_item_name(skin_id))
            nd.ResizeAndPosition()

    def on_click_btn(self, *args):
        jump_to_lottery('33')