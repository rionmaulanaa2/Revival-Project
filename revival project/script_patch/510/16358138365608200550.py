# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/PCQTEGuideUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from common.uisys import ui_proxy
import cc
TRK_ACTION_TAG = 16383

class PCQTEGuideUI(BasePanel):
    PANEL_CONFIG_NAME = 'guide/bg_guide_qte_pc'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        self.clip_stencil = ui_proxy.trans2ProxyObj(self.panel.nd_clip.getStencil())
        self.clip_stencil.nd_q.setVisible(False)
        self.clip_stencil.nd_action_custom_4.setVisible(False)
        self.panel.nd_step_1.setVisible(False)
        self.panel.nd_step_2.setVisible(False)
        self.panel.nd_step_3.setVisible(False)
        self.hide_human_tips()
        self.panel.bg_black.setVisible(False)
        self.is_show_step_1 = False
        self.is_show_step_2 = False
        self.is_show_step_3 = False

    def on_finalize_panel(self):
        self.hide_step_1()
        self.hide_step_2()
        self.hide_step_3()
        super(PCQTEGuideUI, self).on_finalize_panel()

    def on_resolution_changed(self):
        if self.is_show_step_2:
            self.hide_step_2()
            self.show_step_2()
            return
        if self.is_show_step_3:
            self.hide_step_3()
            self.show_step_3()
            return
        self.panel.setVisible(False)

    def reposition_step_2(self, posture_ctrl_ui):
        nd_roll = posture_ctrl_ui.panel.ccb_skill.GetItem(0)
        nd_roll_wpos = nd_roll.ConvertToWorldSpacePercentage(50, 50)
        nd_q_pos = self.clip_stencil.nd_q.getParent().convertToNodeSpace(nd_roll_wpos)
        nd_q_pos.x = nd_q_pos.x / self.panel.getScale()
        nd_q_pos.y = nd_q_pos.y / self.panel.getScale()
        self.clip_stencil.nd_q.setPosition(nd_q_pos)

    def reposition_step_3(self, mecha_ctrl_ui):
        sub_weapon_wpos = mecha_ctrl_ui.panel.nd_action_custom_4.ConvertToWorldSpacePercentage(50, 50)
        nd_action_custom_pos = self.clip_stencil.nd_action_custom_4.getParent().convertToNodeSpace(sub_weapon_wpos)
        nd_action_custom_pos.x = nd_action_custom_pos.x / self.panel.getScale()
        nd_action_custom_pos.y = nd_action_custom_pos.y / self.panel.getScale()
        self.clip_stencil.nd_action_custom_4.setPosition(nd_action_custom_pos)

    def show_step_1(self):
        self.panel.nd_step_1.setVisible(True)
        self.panel.PlayAnimation('step1')
        self.is_show_step_1 = True

    def hide_step_1(self):
        self.panel.nd_step_1.setVisible(False)
        self.panel.StopAnimation('step1')
        self.is_show_step_1 = False

    def show_step_2(self):
        battle_ctrl_ui = global_data.ui_mgr.get_ui('BattleControlUIPC')
        if not battle_ctrl_ui:
            log_error('Cant find opened ui: BattleControlUIPC')
            return
        self.reposition_step_2(battle_ctrl_ui)
        self.panel.bg_black.setVisible(True)
        self.clip_stencil.nd_q.setVisible(True)
        self.panel.nd_clip.CommandDirty()
        self.panel.nd_step_2.setVisible(True)
        self.panel.PlayAnimation('step2')
        self.is_show_step_2 = True

    def hide_step_2(self):
        if not self.is_show_step_2:
            return
        self.is_show_step_2 = False
        self.panel.nd_step_2.setVisible(False)
        self.clip_stencil.nd_q.setVisible(False)
        self.panel.nd_clip.CommandDirty()
        self.panel.bg_black.setVisible(False)
        self.panel.StopAnimation('step2')

    def show_step_3(self):
        mecha_ctrl_ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if not mecha_ctrl_ui:
            return
        self.reposition_step_3(mecha_ctrl_ui)
        self.panel.bg_black.setVisible(True)
        self.clip_stencil.nd_action_custom_4.setVisible(True)
        self.panel.nd_clip.CommandDirty()
        self.panel.nd_step_3.setVisible(True)
        self.panel.PlayAnimation('step3')
        self.is_show_step_3 = True

    def hide_step_3(self):
        if not self.is_show_step_3:
            return
        self.is_show_step_3 = False
        self.panel.nd_step_3.setVisible(False)
        self.clip_stencil.nd_action_custom_4.setVisible(False)
        self.panel.nd_clip.CommandDirty()
        self.panel.bg_black.setVisible(False)

    def show_human_tips(self, tips_text):
        human_tips_temp = self.panel.temp_human_tips
        human_tips_temp.lab_tips.SetString(tips_text)
        self.panel.temp_human_tips.setVisible(True)

    def hide_human_tips(self):
        self.panel.temp_human_tips.setVisible(False)