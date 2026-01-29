# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/advertising/TemplateLottery3.py
from __future__ import absolute_import
from logic.comsys.activity.SimpleAdvance import SimpleAdvance

class TemplateLottery3(SimpleAdvance):
    PANEL_CONFIG_NAME = ''
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn'
       }
    NEED_GAUSSIAN_BLUR = False
    LOTTERY_ID = None
    SS_SKIN_ID = None
    S_SKIN_IDS = None
    NA_DESC_ID = None
    DESC_ID = None
    NA_TITLE_ID = None
    TITLE_ID = None
    TIME_DESC = None

    def set_content(self):
        from logic.gutils import item_utils
        skin_list = [
         self.SS_SKIN_ID] + self.S_SKIN_IDS
        for idx, skin_id in enumerate(skin_list):
            if idx == 0:
                node = self.panel.lab_name
            else:
                node = getattr(self.panel, 'lab_name_%s' % idx)
            if not node:
                continue
            name_text = item_utils.get_lobby_item_name(skin_id)
            node.SetString(name_text)
            node.ResizeAndPosition()

        desc_text = self.NA_DESC_ID if G_IS_NA_PROJECT else self.DESC_ID
        self.panel.lab_des.SetString(desc_text)
        title_text = self.NA_TITLE_ID if G_IS_NA_PROJECT else self.TITLE_ID
        self.panel.lab_title.SetString(title_text)
        if self.TIME_DESC and self.panel.lab_time:
            self.panel.lab_time.SetString(self.TIME_DESC)

    def on_click_btn(self, *args):
        from logic.gutils import jump_to_ui_utils
        jump_to_ui_utils.jump_to_lottery(self.LOTTERY_ID, self.SS_SKIN_ID)