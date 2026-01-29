# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotterySSBanner3.py
from __future__ import absolute_import
from logic.gutils import item_utils
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.gutils.item_utils import get_lobby_item_name, jump_to_ui
from logic.gutils import jump_to_ui_utils
from common.cfg import confmgr
from logic.comsys.activity.SimpleAdvance import SimpleAdvance

class LotterySSBanner3(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/lottery_ss_banner_6'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn'
       }
    NEED_GAUSSIAN_BLUR = False

    def on_init_panel(self, *args):
        self.ss_skin = 201800451
        self.s_skin = [201800342, 201001352, 208200222]
        super(LotterySSBanner3, self).on_init_panel(*args)

    def set_content(self):
        skin_list = [
         self.ss_skin] + self.s_skin
        for idx, skin_id in enumerate(skin_list):
            if idx == 0:
                node = self.panel.lab_ss_name
            else:
                node = getattr(self.panel, 'lab_s_name_%s' % idx)
            name_text = item_utils.get_lobby_item_name(skin_id)
            node.SetString(name_text)
            node.ResizeAndPosition()

        desc_text = 610324
        self.panel.lab_des.SetString(desc_text)
        appear_time = self.panel.GetAnimationMaxRunTime('appear')
        self.panel.DelayCall(appear_time, lambda *args: self.panel.PlayAnimation('loop') and 0)

    def on_click_btn(self, *args):
        jump_to_ui_utils.jump_to_lottery('35', self.ss_skin)