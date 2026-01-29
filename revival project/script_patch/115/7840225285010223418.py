# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryBannerS6.py
from __future__ import absolute_import
from logic.gutils import item_utils
from logic.gutils import jump_to_ui_utils
from logic.comsys.activity.SimpleAdvance import SimpleAdvance

class LotteryBannerS6(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/lottery_s6s11_banner_01'
    APPEAR_ANIM = 'appear'
    LOOP_ANIM = 'loop'
    LASTING_TIME = 1.35
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn'
       }
    NEED_GAUSSIAN_BLUR = False

    def on_init_panel(self, *args):
        self.ss_skin = 201800751
        self.s_skin = [201800643, 201001446, 208105525, 208103220]
        super(LotteryBannerS6, self).on_init_panel(*args)

    def set_content(self):
        skin_list = [
         self.ss_skin] + self.s_skin
        for idx, skin_id in enumerate(skin_list):
            if idx == 0:
                node = self.panel.lab_name
            else:
                node = getattr(self.panel, 'lab_name_%s' % idx)
            name_text = item_utils.get_lobby_item_name(skin_id)
            node.SetString(name_text)
            node.ResizeAndPosition()

        title_text = 610609 if G_IS_NA_PROJECT else 610608
        self.panel.lab_title.SetString(title_text)

    def on_click_btn(self, *args):
        jump_to_ui_utils.jump_to_lottery('37', self.ss_skin)