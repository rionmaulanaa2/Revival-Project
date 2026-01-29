# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SSLevelSkinFullScreen2.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from logic.gutils.item_utils import get_lobby_item_belong_name, get_lobby_item_name, jump_to_ui
from logic.gutils import jump_to_ui_utils

class SSLevelSkinFullScreen2(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_202004/open_vk'
    SKIN_ID = 201801441
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5
    UI_ACTION_EVENT = {'btn_review.OnClick': 'on_click_btn'
       }

    def set_content(self):
        from logic.gcommon.common_utils.local_text import get_text_by_id
        name = get_lobby_item_belong_name(self.SKIN_ID) + '\xc2\xb7' + get_lobby_item_name(self.SKIN_ID)
        self.panel.img_name.SetString(name)
        self.panel.btn_review.SetText(80706)

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)

    def on_click_btn(self, *args):
        jump_to_ui_utils.jump_to_display_detail_by_item_no(self.SKIN_ID)