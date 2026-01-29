# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/QTEGuideUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from common.uisys import ui_proxy
import cc
TRK_ACTION_TAG = 16383

class QTEGuideUI(BasePanel):
    PANEL_CONFIG_NAME = 'guide/bg_guide_qte'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_click.OnBegin': 'on_nd_click_begin'
       }

    def on_init_panel(self, *args, **kwargs):
        self.clip_stencil = ui_proxy.trans2ProxyObj(self.panel.nd_clip.getStencil())
        self.clip_stencil.nd_rocker.setVisible(False)
        self.clip_stencil.nd_roll.setVisible(False)
        self.clip_stencil.nd_roll2.setVisible(False)
        self.panel.nd_step_1.setVisible(False)
        self.panel.nd_step_2.setVisible(False)
        self.panel.nd_step_3.setVisible(False)
        self.panel.RecordAnimationNodeState('focusing2')
        self.panel.RecordAnimationNodeState('focusing3')
        self.hide_human_tips()
        self.panel.bg_black.setVisible(False)
        self.is_show_step_1 = False
        self.is_show_step_2 = False
        self.is_show_step_3 = False

    def on_finalize_panel(self):
        self.hide_step_1()
        self.hide_step_2()
        self.hide_step_3()

    def on_resolution_changed(self):
        if self.is_show_step_1:
            self.hide_step_1()
            self.show_step_1()
            return
        if self.is_show_step_2:
            self.hide_step_2()
            self.show_step_2()
            return
        if self.is_show_step_3:
            self.hide_step_3()
            self.show_step_3()
            return
        self.panel.setVisible(False)

    def reposition_step_1(self, rocker_ui):
        rocker_wpos = rocker_ui.panel.nd_custom.ConvertToWorldSpacePercentage(50, 50)
        step_1_pos = self.panel.nd_step_1.convertToNodeSpace(rocker_wpos)
        self.panel.nd_step_1.nd_scale.setPosition(step_1_pos)
        rocker_clip_pos = self.clip_stencil.nd_rocker.getParent().convertToNodeSpace(rocker_wpos)
        rocker_clip_pos.x = rocker_clip_pos.x / self.panel.getScale()
        rocker_clip_pos.y = rocker_clip_pos.y / self.panel.getScale()
        self.clip_stencil.nd_rocker.setPosition(rocker_clip_pos)

    def reposition_step_2(self, posture_ctrl_ui):
        nd_roll_wpos = posture_ctrl_ui.panel.nd_roll.ConvertToWorldSpacePercentage(50, 50)
        step_2_pos = self.panel.nd_step_2.convertToNodeSpace(nd_roll_wpos)
        self.panel.nd_step_2.nd_attack_tips.setPosition(step_2_pos)
        roll_clip_pos = self.clip_stencil.nd_roll.getParent().convertToNodeSpace(nd_roll_wpos)
        roll_clip_pos.x = roll_clip_pos.x / self.panel.getScale()
        roll_clip_pos.y = roll_clip_pos.y / self.panel.getScale()
        self.clip_stencil.nd_roll.setPosition(roll_clip_pos)

    def reposition_step_3(self, mecha_ctrl_ui):
        sub_weapon_wpos = mecha_ctrl_ui.panel.nd_action_custom_4.ConvertToWorldSpacePercentage(50, 50)
        step_3_pos = self.panel.nd_step_3.convertToNodeSpace(sub_weapon_wpos)
        self.panel.nd_step_3.nd_attack_tips.setPosition(step_3_pos)
        sub_weapon_pos = self.clip_stencil.nd_roll2.getParent().convertToNodeSpace(sub_weapon_wpos)
        sub_weapon_pos.x = sub_weapon_pos.x / self.panel.getScale()
        sub_weapon_pos.y = sub_weapon_pos.y / self.panel.getScale()
        self.clip_stencil.nd_roll2.setPosition(sub_weapon_pos)

    def show_step_1(self):
        rocker_ui = global_data.ui_mgr.get_ui('MoveRockerUI')
        if not rocker_ui:
            return
        self.reposition_step_1(rocker_ui)
        self.clip_stencil.nd_rocker.setVisible(True)
        self.panel.nd_clip.CommandDirty()
        self.panel.nd_step_1.setVisible(True)
        self.panel.PlayAnimation('step1')
        rocker_ui.panel.PlayAnimation('button_left')
        self.is_show_step_1 = True

    def hide_step_1(self):
        if not self.is_show_step_1:
            return
        rocker_ui = global_data.ui_mgr.get_ui('MoveRockerUI')
        if not rocker_ui:
            return
        self.is_show_step_1 = False
        rocker_ui.panel.StopAnimation('button_left')
        self.panel.StopAnimation('step1')
        self.panel.nd_step_1.setVisible(False)
        self.clip_stencil.nd_rocker.setVisible(False)
        self.panel.nd_clip.CommandDirty()

    def show_step_2(self):
        posture_ctrl_ui = global_data.ui_mgr.get_ui('PostureControlUI')
        if not posture_ctrl_ui:
            return
        self.reposition_step_2(posture_ctrl_ui)
        self.panel.bg_black.setVisible(True)
        self.clip_stencil.nd_roll.setVisible(True)
        self.panel.nd_clip.CommandDirty()
        self.panel.nd_step_2.setVisible(True)
        action = self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('focusing2')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('focusing2')),
         cc.CallFunc.create(lambda : self.panel.StopAnimation('focusing2')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('step2'))]))
        action.setTag(TRK_ACTION_TAG)
        posture_ctrl_ui.panel.nd_roll.vx.setVisible(True)
        posture_ctrl_ui.panel.PlayAnimation('light')
        self.is_show_step_2 = True

    def hide_step_2(self):
        if not self.is_show_step_2:
            return
        posture_ctrl_ui = global_data.ui_mgr.get_ui('PostureControlUI')
        if not posture_ctrl_ui:
            return
        self.is_show_step_2 = False
        posture_ctrl_ui.panel.StopAnimation('light')
        posture_ctrl_ui.panel.nd_roll.vx.setVisible(False)
        self.panel.stopActionByTag(TRK_ACTION_TAG)
        self.panel.StopAnimation('step2')
        self.panel.StopAnimation('focusing2')
        self.panel.nd_step_2.setVisible(False)
        self.clip_stencil.nd_roll.setVisible(False)
        self.panel.nd_clip.CommandDirty()
        self.panel.bg_black.setVisible(False)

    def show_step_3(self):
        mecha_ctrl_ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if not mecha_ctrl_ui:
            return
        self.reposition_step_3(mecha_ctrl_ui)
        self.panel.bg_black.setVisible(True)
        self.clip_stencil.nd_roll2.setVisible(True)
        self.panel.nd_clip.CommandDirty()
        self.panel.nd_step_3.setVisible(True)
        action = self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('focusing3')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('focusing3')),
         cc.CallFunc.create(lambda : self.panel.StopAnimation('focusing3')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('step3'))]))
        action.setTag(TRK_ACTION_TAG)
        self.is_show_step_3 = True

    def hide_step_3(self):
        if not self.is_show_step_3:
            return
        self.is_show_step_3 = False
        self.panel.stopActionByTag(TRK_ACTION_TAG)
        self.panel.StopAnimation('step3')
        self.panel.StopAnimation('focusing3')
        self.panel.nd_step_3.setVisible(False)
        self.clip_stencil.nd_roll2.setVisible(False)
        self.panel.nd_clip.CommandDirty()
        self.panel.bg_black.setVisible(False)

    def show_human_tips(self, tips_text):
        human_tips_temp = self.panel.temp_human_tips
        human_tips_temp.lab_tips.SetString(tips_text)
        self.panel.temp_human_tips.setVisible(True)

    def hide_human_tips(self):
        self.panel.temp_human_tips.setVisible(False)

    def on_nd_click_begin(self, btn, touch):
        pos = touch.getLocation()
        quit_ui = global_data.ui_mgr.get_ui('BattleRightTopUI')
        if quit_ui and getattr(quit_ui.panel, 'btn_exit', None):
            if quit_ui.panel.btn_exit.IsPointIn(pos):
                return False
        if self.is_show_step_1:
            nd = self.panel.nd_step_1.nd_scale
            if nd.isValid() and nd.IsPointIn(pos):
                return False
        if self.is_show_step_2:
            nd = self.panel.nd_step_2.nd_attack_tips
            if nd.isValid() and nd.IsPointIn(pos):
                return False
            self.panel.stopActionByTag(TRK_ACTION_TAG)
            action = self.panel.runAction(cc.Sequence.create([
             cc.CallFunc.create(lambda : self.panel.StopAnimation('step2')),
             cc.CallFunc.create(lambda : self.panel.RecoverAnimationNodeState('focusing2')),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('focusing2')),
             cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('focusing2') * 2),
             cc.CallFunc.create(lambda : self.panel.StopAnimation('focusing2')),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('step2'))]))
            action.setTag(TRK_ACTION_TAG)
        if self.is_show_step_3:
            nd = self.panel.nd_step_3.nd_attack_tips
            if nd.isValid() and nd.IsPointIn(pos):
                return False
            self.panel.stopActionByTag(TRK_ACTION_TAG)
            action = self.panel.runAction(cc.Sequence.create([
             cc.CallFunc.create(lambda : self.panel.StopAnimation('step3')),
             cc.CallFunc.create(lambda : self.panel.RecoverAnimationNodeState('focusing3')),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('focusing3')),
             cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('focusing3') * 2),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('step3'))]))
            action.setTag(TRK_ACTION_TAG)
        return True