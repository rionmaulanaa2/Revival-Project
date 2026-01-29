# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/GooseBearHappyPush/GooseBearHappyPushGuideUI.py
from __future__ import absolute_import
from __future__ import print_function
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_NO_EFFECT, UI_VKB_CLOSE
import cc

class GooseBearHappyPushGuideUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_happy_push/guide_battle_happy_push'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_touch.OnClick': 'on_close'
       }
    GLOBAL_EVENT = {}
    STEP_ALL = 2352911
    STEP_1 = 2352912

    def on_init_panel(self):
        self.delay_time = 0
        self.cur_step = 0
        self.panel.nd_step_1.setVisible(False)
        self.panel.nd_step_2.setVisible(False)
        self.panel.nd_touch.setVisible(False)

    def start_show(self):
        self.panel.stopActionByTag(self.STEP_ALL)
        self.panel.stopActionByTag(self.STEP_1)
        ac_list = [
         cc.DelayTime.create(self.delay_time),
         cc.CallFunc.create(lambda : self.panel.nd_touch.setVisible(True)),
         cc.CallFunc.create(lambda : self.panel.nd_step_1.setVisible(True)),
         cc.CallFunc.create(lambda : self.panel.nd_step_2.setVisible(False)),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show_step_1')),
         cc.DelayTime.create(5),
         cc.CallFunc.create(lambda : self.panel.nd_step_1.setVisible(False)),
         cc.CallFunc.create(lambda : self.panel.nd_step_2.setVisible(True)),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show_step_2')),
         cc.DelayTime.create(5),
         cc.CallFunc.create(lambda : global_data.achi_mgr.set_cur_user_archive_data('GooseBearHappyPushGuideUI_END', True)),
         cc.CallFunc.create(lambda : self.on_close())]
        act = cc.Sequence.create(ac_list)
        act.setTag(self.STEP_ALL)
        self.panel.runAction(act)
        print('-------------------start_show------------------------')

    def step_1_finish(self):
        self.panel.stopActionByTag(self.STEP_ALL)
        self.panel.stopActionByTag(self.STEP_1)
        ac_list = [
         cc.CallFunc.create(lambda : self.panel.nd_step_1.setVisible(False)),
         cc.CallFunc.create(lambda : self.panel.nd_step_2.setVisible(True)),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show_step_2')),
         cc.DelayTime.create(5),
         cc.CallFunc.create(lambda : global_data.achi_mgr.set_cur_user_archive_data('GooseBearHappyPushGuideUI_END', True)),
         cc.CallFunc.create(lambda : self.on_close())]
        act = cc.Sequence.create(ac_list)
        act.setTag(self.STEP_1)
        self.panel.runAction(act)

    def step_2_finish(self):
        self.panel.stopActionByTag(self.STEP_ALL)
        self.panel.stopActionByTag(self.STEP_1)
        global_data.achi_mgr.set_cur_user_archive_data('GooseBearHappyPushGuideUI_END', True)
        self.close()

    def delay_show(self, delay_time):
        self.delay_time = delay_time
        self.start_show()

    def on_close(self, *args):
        if self.cur_step == 0:
            self.step_1_finish()
            self.cur_step = 1
        elif self.cur_step == 1:
            self.step_2_finish()
            self.cur_step = 2
        else:
            self.panel.stopActionByTag(self.STEP_ALL)
            self.panel.stopActionByTag(self.STEP_1)
            self.close()