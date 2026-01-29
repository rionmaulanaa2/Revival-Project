# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEMechaUpgradePanel.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_CUSTOM, UI_TYPE_MESSAGE
from common.utilities import get_rome_num
from common.cfg import confmgr

class PVEMechaUpgradePanel(BasePanel):
    DELAY_CLOSE_TAG = 20231106
    PANEL_CONFIG_NAME = 'pve/mecha/pve_mecha_upgrade'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CUSTOM

    def on_init_panel(self, mecha_id, new_level, add_cnt, *args, **kwargs):
        super(PVEMechaUpgradePanel, self).on_init_panel()
        self.init_params(mecha_id, new_level, add_cnt)
        self.init_ui()
        self.init_ui_events()

    def init_params(self, mecha_id, new_level, add_cnt):
        self._disappearing = False
        self._mecha_id = mecha_id
        self._new_level = new_level
        self._add_cnt = add_cnt

    def init_ui(self):
        self.panel.PlayAnimation('show_completed')
        self.panel.PlayAnimation('appear')
        self.init_mecha_upgrade_info()

    def init_ui_events(self):

        @self.panel.unique_callback()
        def OnClick(btn, touch):
            self.play_disappear_anim()

    def init_mecha_upgrade_info(self):
        effect_info = global_data.player.get_add_upgrade_mecha_effect(self._mecha_id, self._new_level)
        conf = confmgr.get('mecha_upgrade_effect_data', str(effect_info['effect_id']))
        self.panel.lab_level_skill.setString(get_rome_num(effect_info['effect_level']))
        self.panel.icon_skill.SetDisplayFrameByPath('', conf.get('icon'))
        self.panel.lab_level_before.setString(str(self._new_level - self._add_cnt))
        self.panel.lab_level_now.setString(str(self._new_level))

    def play_disappear_anim(self):
        if self._disappearing:
            return
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime('disappear')

        def delay_call(*args):
            self._disappearing = False
            self.close()

        self.panel.StopAnimation('disappear')
        self.panel.DelayCallWithTag(anim_time, delay_call, self.DELAY_CLOSE_TAG)
        self.panel.PlayAnimation('disappear')

    def on_finalize_panel(self):
        super(PVEMechaUpgradePanel, self).on_finalize_panel()
        self._disappearing = None
        self._mecha_id = None
        self._new_level = None
        return