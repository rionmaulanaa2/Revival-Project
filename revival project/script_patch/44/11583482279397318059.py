# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryBannerS4SP.py
from __future__ import absolute_import
from logic.gutils import item_utils
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.gutils.item_utils import get_lobby_item_name, jump_to_ui
from logic.gutils import jump_to_ui_utils
from common.cfg import confmgr
from logic.comsys.activity.SimpleAdvance import SimpleAdvance

class LotteryBannerS4SP(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/family_portraits/i_ai_family_ad'
    APPEAR_ANIM = 'show'
    LOOP_ANIM = ''
    LASTING_TIME = 1.333
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn'
       }
    NEED_GAUSSIAN_BLUR = True

    def on_init_panel(self, *args):
        self.ai_skins = [
         201011152, 201011100, 201011151, 201011153]
        super(LotteryBannerS4SP, self).on_init_panel(*args)
        self.panel.PlayAnimation('loop')

    def get_close_node(self):
        return (
         self.panel.btn_close,)

    def set_content(self):
        from logic.gutils.item_utils import get_lobby_item_name
        for idx, skin_id in enumerate(self.ai_skins):
            nd = getattr(self.panel, 'temp_ad_%d' % (idx + 1))
            nd.btn_search.BindMethod('OnClick', lambda btn, touch, skin_id=skin_id: self.on_click_research(skin_id))

    def on_click_research(self, skin_id):
        from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
        jump_to_display_detail_by_item_no(skin_id, extra_parameter={'role_info_ui': True})

    def on_click_btn(self, *args):
        jump_to_ui_utils.jump_to_lottery('28')