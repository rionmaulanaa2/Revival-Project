# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/PrincessMilaAdvance.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.jump_to_ui_utils import jump_to_anniversary_activity
from logic.gutils.item_utils import get_lobby_item_name
import logic.gcommon.time_utility as tutil
from common.cfg import confmgr
from logic.gcommon.common_const import activity_const
from logic.gcommon.item import item_const as iconst

class PrincessMilaAdvance(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_202007/open_princess_mila'
    APPEAR_ANIM = 'appear'
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn_go'
       }

    def on_init_panel(self, *args):
        super(PrincessMilaAdvance, self).on_init_panel(*args)

        @self.panel.btn_go.callback()
        def OnClick(*args):
            self.close()
            jump_to_anniversary_activity()

    def set_content(self):
        conf = confmgr.get('c_activity_config', activity_const.ACTIVITY_ANNIV_MILA_BOW_COLLECT_1)
        start_date = tutil.get_date_str('%Y.%m.%d', conf.get('cBeginTime', 0))
        finish_date = tutil.get_date_str('%Y.%m.%d', conf.get('cEndTime', 0))
        self.panel.img_name.SetString(get_lobby_item_name(iconst.ITEM_NO_SKIN_PRINCESS_MILA))
        self.panel.lab_time.SetString(get_text_by_id(604006, (start_date, finish_date)))

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)