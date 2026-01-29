# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/BpAdvisementUI.py
from __future__ import absolute_import
from common.const import uiconst
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gutils import jump_to_ui_utils
from logic.gutils.battle_pass_utils import get_buy_season_card_ui_name

class BpAdvisementUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/s4_s9/open_bp_award'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'panel.btn_buy.OnClick': '_on_click_buy_season_pass'
       }

    def set_level(self, battle_pass_type, old_lv, new_lv):
        self.bp_type = battle_pass_type
        self.old_lv = old_lv
        self.new_lv = new_lv

    def on_init_panel(self):
        self.bp_type = None

        @self.panel.btn_close.callback()
        def OnClick(btn, touch):
            self.close()

        from logic.gutils.item_utils import get_lobby_item_name, get_skin_rare_degree_icon
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

        def spine_anim():
            self.panel.vx_spine_01.setVisible(True)
            self.panel.vx_spine_02.setVisible(True)
            self.panel.vx_spine_01.setAnimation(0, 'in', False)
            self.panel.vx_spine_01.addAnimation(0, 'idle', True)
            self.panel.vx_spine_02.setAnimation(0, 'in', False)
            self.panel.vx_spine_02.addAnimation(0, 'idle', True)

        from logic.gutils.battle_pass_utils import get_now_season_pass_data
        season_data = get_now_season_pass_data()
        open_reward = season_data.four_core_reward
        for idx, item_id in enumerate(open_reward):
            tag_node = getattr(self.panel.nd_content, 'img_tag_%s' % (idx + 1), None)
            if tag_node:
                tag_node.img_tag.tag.lab_name.SetString(get_lobby_item_name(item_id))
                tag_node.temp_level.bar_level.SetDisplayFrameByPath('', get_skin_rare_degree_icon(item_id))

        return

    def _on_click_buy_season_pass(self, *args):
        jump_to_ui_utils.jump_to_buy_season_pass_card()
        ui = global_data.ui_mgr.get_ui(get_buy_season_card_ui_name())
        if ui and self.bp_type is not None:
            ui.set_level(self.bp_type, self.old_lv, self.new_lv)
            self.bp_type = None
        self.close()
        return

    def on_finalize_panel(self):
        if self.bp_type is not None:
            ui = global_data.ui_mgr.show_ui('SeasonPassLevelUp', 'logic.comsys.battle_pass')
            if ui:
                ui.set_level(self.bp_type, self.old_lv, self.new_lv)
            self.bp_type = None
        return