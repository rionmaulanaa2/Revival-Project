# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/advertising/TemplateLottery1.py
from __future__ import absolute_import
from logic.comsys.activity.SimpleAdvance import SimpleAdvance

class TemplateLottery1(SimpleAdvance):
    PANEL_CONFIG_NAME = ''
    APPEAR_ANIM = 'appear'
    LOOP_ANIM = 'loop'
    LASTING_TIME = 0.5
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn',
       'btn_close.OnClick': 'close'
       }
    NEED_GAUSSIAN_BLUR = False
    ND_SKIN_LIST = ()
    LOTTERY_ID = None

    def set_content(self):
        from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_belong_name, get_skin_rare_degree_icon
        for idx, skin_id in enumerate(self.ND_SKIN_LIST):
            nd = getattr(self.panel, 'img_tag_%s' % (idx + 1))
            if not nd:
                continue
            if nd.lab_name:
                role_name = get_lobby_item_belong_name(skin_id)
                nd.lab_name.SetString(role_name)
            if nd.skin_name:
                skin_name = get_lobby_item_name(skin_id)
                nd.skin_name.SetString(skin_name)
            rare_path = get_skin_rare_degree_icon(skin_id)
            nd.img_level.SetDisplayFrameByPath('', rare_path)
            nd.ResizeAndPosition()

    def on_click_btn(self, *args):
        from logic.gutils import jump_to_ui_utils
        jump_to_ui_utils.jump_to_lottery(self.LOTTERY_ID)