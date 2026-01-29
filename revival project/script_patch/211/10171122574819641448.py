# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathAttentionUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
from common.const import uiconst

class DeathAttentionUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_tdm/fight_tdm_attention'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.init_panel()

    def on_finalize_panel(self):
        pass

    def init_event(self):
        emgr = global_data.emgr
        econf = {}
        emgr.bind_events(econf)

    def init_parameters(self):
        self._cur_stage = 1
        self._stage_color = ['#SG', '#SB', '#SP', '#SO']
        res_dir = 'gui/ui_res_2/battle_tdm/'
        self._stage_tex = ['progress_tdm_attention1.png', 'progress_tdm_attention2.png', 'progress_tdm_attention3.png', 'progress_tdm_attention4.png']
        self._stage_tex = [ '%s%s' % (res_dir, path) for path in self._stage_tex ]
        self._stage_range = [
         [
          0, 600],
         [
          600, 1200],
         [
          1200, 1500],
         [
          1500, 1500]]
        self._last_refresh_time = 0
        self._refresh_interval = 0.3

    def init_panel(self):
        self.set_stage_percent(1, 0)

    def stop_all_action(self):
        self.panel.stopAllActions()
        for i in range(1, len(self._stage_color) + 1):
            aniName = 'attention_upgrade%d' % i
            keepAniName = 'attention_keep%d' % i
            self.panel.StopAnimation(aniName)
            self.panel.StopAnimation(keepAniName)

    def set_stage_percent(self, stage, percent):
        import time
        now = time.time()
        if now - self._last_refresh_time < self._refresh_interval:
            return
        self._last_refresh_time = now
        stage_color = self._stage_color
        self.panel.lab_attention.SetColor(stage_color[stage - 1])
        self.panel.progress_attention.SetColor(stage_color[stage - 1])
        self.panel.progress_attention.SetProgressTexture(self._stage_tex[stage - 1])
        self.panel.lab_attention.SetString(get_text_by_id(19423) + ': %s' % str(stage))
        self.panel.progress_attention.SetPercentageWithAni(percent, 0.2)
        if stage == 1:
            self.stop_all_action()
            for child in self.panel.img_stage.GetChildren():
                child.setVisible(False)

            return
        if self._cur_stage != stage:
            aniName = 'attention_upgrade%d' % stage
            max_time = self.panel.GetAnimationMaxRunTime(aniName)

            def finished():
                if self and self.is_valid():
                    keepAniName = 'attention_keep%d' % stage
                    self.panel.PlayAnimation(keepAniName)

            self.panel.SetTimeOut(max_time, finished)
            self.panel.PlayAnimation(aniName)
        self._cur_stage = stage

    def set_fire_power(self, fire_power):
        stage = 1
        percent = 0
        for i, l_range in enumerate(self._stage_range):
            if l_range[0] == l_range[1]:
                stage = i + 1
                percent = 100.0
                break
            if l_range[0] <= fire_power < l_range[1]:
                stage = i + 1
                percent = float(fire_power - l_range[0]) / float(l_range[1] - l_range[0]) * 100.0
                break

        self.set_stage_percent(stage, percent)