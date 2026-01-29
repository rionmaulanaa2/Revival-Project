# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/GranbelmAdvanceVx.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
import cc
from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN
from logic.gutils.jump_to_ui_utils import jump_to_mode_choose
ANIM_DELAY_TIME = {'loop_gear': 0.8,
   'loop_button': 0.83,
   'loop_light': 3
   }
from common.const import uiconst

class GranbelmAdvanceVx(BasePanel):
    PANEL_CONFIG_NAME = 'activity/open_202004/open_granbelm_kv_vx'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn_go'
       }

    def on_init_panel(self, *args, **kwargs):
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.DelayTime.create(ANIM_DELAY_TIME['loop_gear']),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop_gear')),
         cc.DelayTime.create(ANIM_DELAY_TIME['loop_button'] - ANIM_DELAY_TIME['loop_gear']),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop_button')),
         cc.DelayTime.create(ANIM_DELAY_TIME['loop_light'] - ANIM_DELAY_TIME['loop_button']),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop_light'))]))

    def on_click_btn_go(self, *args):
        self.close()
        global_data.ui_mgr.close_ui('GranbelmAdvance')
        jump_to_mode_choose(PLAY_TYPE_CHICKEN)