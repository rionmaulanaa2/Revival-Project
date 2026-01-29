# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202201/SpringFreeMechaUI.py
from __future__ import absolute_import
from logic.comsys.activity.SimpleAdvance import SimpleAdvance

class SpringFreeMechaUI(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/activity_202201/spring_mecha_free/i_spring_mecha_free'
    APPEAR_ANIM = ''
    NEED_GAUSSIAN_BLUR = False
    LASTING_TIME = 0.5
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }

    def on_init_panel(self, *args):
        super(SpringFreeMechaUI, self).on_init_panel(*args)
        global_data.emgr.receive_task_reward_succ_event += self.set_content

    def on_finalize_panel(self):
        global_data.emgr.receive_task_reward_succ_event -= self.set_content
        super(SpringFreeMechaUI, self).on_finalize_panel()

    def set_content(self, *args):
        from logic.gutils.advance_utils import set_free_mecha_content
        set_free_mecha_content(self.panel, False)

    def get_close_node(self):
        return ()