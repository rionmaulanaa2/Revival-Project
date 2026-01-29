# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/HalloweenInvitation.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from logic.gutils.item_utils import get_lobby_item_name

class HalloweenInvitation(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/bg_halloween_receive'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.1

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)

    def set_content(self):
        goods_ids = [
         201001146, 201001244, 201001346]
        role_ids = [11, 12, 13]
        for i, goods_id in enumerate(goods_ids):
            role_id = role_ids[i]
            name_text = get_lobby_item_name(role_id)
            skin_text = get_lobby_item_name(goods_id)
            nd = getattr(self.panel, 'temp_name_' + str(i + 1)).lab_name
            nd.SetString(name_text + '\xc2\xb7' + '<color=0Xff9c00ff>' + skin_text)

        @self.panel.btn_receive.callback()
        def OnClick(*args):
            from logic.gutils.jump_to_ui_utils import jump_to_lottery

    def hide_go_node(self):
        self.panel.nd_content.go_node.setVisible(False)