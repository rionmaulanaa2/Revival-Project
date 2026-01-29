# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/BattleFightMeowPC.py
from __future__ import absolute_import
from .BattleFightMeow import BattleFightMeowBase
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
import cc

class BattleFightMeowPC(BattleFightMeowBase):
    PANEL_CONFIG_NAME = 'battle/fight_coin_pc'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1

    def on_init_panel(self, *args, **kwargs):
        super(BattleFightMeowPC, self).on_init_panel(*args, **kwargs)
        if global_data.feature_mgr.is_support_pc_mouse_hover():
            self.panel.nd_custom.set_hover_enable(True)
            self.panel.nd_custom.BindMethod('OnHoverEnter', self.on_enter_slider_btn)
            self.panel.nd_custom.BindMethod('OnHoverExit', self.on_exit_slider_btn)
        else:
            listener = cc.EventListenerMouse.create()
            listener.setOnMouseMoveCallback(self._on_mouse_move)
            cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(listener, self.panel.get())

    def leave_screen(self):
        super(BattleFightMeowPC, self).leave_screen()
        global_data.ui_mgr.close_ui('BattleFightMeowPC')

    def _on_mouse_move(self, event):
        wpos = event.getLocationInView()
        from common.utils.cocos_utils import neox_pos_to_cocos
        wpos = cc.Vec2(*neox_pos_to_cocos(wpos.x, wpos.y))
        if self.panel.nd_custom.IsPointIn(wpos):
            self.on_enter_slider_btn()
        else:
            self.on_exit_slider_btn()

    def on_enter_slider_btn(self, *args):
        self.panel.bag_coin.setVisible(True)

    def on_exit_slider_btn(self, *args):
        self.panel.bag_coin.setVisible(False)