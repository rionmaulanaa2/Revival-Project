# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity520/Activity520PrincessTipsUI.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel

class Activity520PrincessTipsUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202105/520/activity_520_princess_tips'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_click_close_btn(self, *args):
        self.close()

    def on_init_panel(self):
        super(Activity520PrincessTipsUI, self).on_init_panel()
        self.is_in_anim = False
        self._goods_id = None
        self.panel.PlayAnimation('show')
        self.panel.SetTimeOut(2.0, lambda : self.panel.PlayAnimation('loop'))

        @self.panel.btn_close.callback()
        def OnClick(*args):
            self.on_click_close_btn(*args)

        @self.panel.btn_1.callback()
        def OnClick(btn, touch):
            if self.is_in_anim:
                return
            self.panel.StopAnimation('loop')
            self.panel.vx_saoguang_01.setVisible(False)
            self.panel.vx_saoguang_02.setVisible(False)
            self.panel.PlayAnimation('disappear')
            t = self.panel.GetAnimationMaxRunTime('disappear')
            self.is_in_anim = True

            def act():
                self.close()
                from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
                role_or_skin_buy_confirmUI(self._goods_id, check_top_skin=True)

            self.panel.SetTimeOut(t + 0.005, act)

        @self.panel.btn_2.callback()
        def OnClick(btn, touch):
            if self.is_in_anim:
                return
            self.panel.StopAnimation('loop')
            self.panel.vx_saoguang_01.setVisible(False)
            self.panel.vx_saoguang_02.setVisible(False)
            self.panel.PlayAnimation('disappear02')
            t = self.panel.GetAnimationMaxRunTime('disappear02')
            self.is_in_anim = True

            def act2():
                self.close()
                from logic.gutils.jump_to_ui_utils import jump_to_activity
                from logic.gcommon.common_const.activity_const import ACTIVITY_520_SHOOTER
                jump_to_activity(ACTIVITY_520_SHOOTER)

            self.panel.SetTimeOut(t + 0.005, act2)

        return

    def on_finalize_panel(self):
        pass

    def set_target_goods_id(self, target_goods_id):
        self._goods_id = target_goods_id
        from logic.gutils import mall_utils
        prices = mall_utils.get_mall_item_price(target_goods_id, pick_list=('yuanbao', ))
        if prices:
            yuanbao_price = prices[0]
            self.panel.lab_1.SetString(get_text_by_id(608613, {'price': yuanbao_price.get('real_price', 0)}))