# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202201/LotterySpringFestivalBanner.py
from __future__ import absolute_import
from logic.gutils import item_utils
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.gutils.item_utils import get_lobby_item_name, jump_to_ui
from logic.gutils import jump_to_ui_utils

class LotterySpringFestivalBanner(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/activity_202201/spring_open_screen_advertising/i_spring_open_screen_advertising'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn',
       'btn_close.OnClick': 'close'
       }
    NEED_GAUSSIAN_BLUR = False

    def set_content(self):
        from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_belong_name, get_skin_rare_degree_icon
        nd_skin_list = (
         ('nd_mecha_1', 201801641),
         ('nd_mecha_2', 201801344),
         ('nd_role_1', 201001152),
         ('nd_role_2', 201002447))
        for nd_name, skin_id in nd_skin_list:
            nd = getattr(self.panel, nd_name)
            role_name = get_lobby_item_belong_name(skin_id)
            nd.lab_name.SetString(role_name)
            skin_name = get_lobby_item_name(skin_id)
            nd.lab_skin_name.SetString(skin_name)
            rare_path = get_skin_rare_degree_icon(skin_id)
            nd.img_s.SetDisplayFrameByPath('', rare_path)
            nd.ResizeAndPosition()

    def on_click_btn(self, *args):
        jump_to_ui_utils.jump_to_lottery('76')