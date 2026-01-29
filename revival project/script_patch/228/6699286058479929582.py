# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/LuckyBagObtainUI.py
from __future__ import absolute_import
from common.const import uiconst
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gcommon.common_const import statistics_const as sconst

class LuckyBagObtainUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'activity/activity_202101/i_activity_lucky_bag_get'
    TEMPLATE_NODE_NAME = 'nd_task'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'img_spring_01.temp_btn_go.btn_common.OnClick': 'on_click_spring_01',
       'img_spring_02.temp_btn_go.btn_common.OnClick': 'on_click_spring_02'
       }
    GLOBAL_EVENT = {'update_day_stat': 'init_spring_01'
       }

    def on_init_panel(self, *args, **kwargs):
        super(LuckyBagObtainUI, self).on_init_panel(*args, **kwargs)
        global_data.player.request_day_stat(sconst.VICTORY_CNT)
        self.init_spring_01()
        self.init_spring_02()

    def init_spring_01(self, *args):
        victory_cnt = global_data.player.get_day_stat(sconst.VICTORY_CNT, 0)
        victory_cnt = min(victory_cnt, 1)
        self.panel.img_spring_01.temp_btn_go.btn_common.SetEnable(victory_cnt == 0)
        self.panel.img_spring_01.nd_progress.lab_task_progress.SetString('{}/1'.format(victory_cnt))
        self.panel.img_spring_01.nd_progress.progress_task.SetPercentage(victory_cnt / 1.0 * 100)
        if victory_cnt > 0:
            self.panel.img_spring_01.temp_btn_go.btn_common.SetText(606046)
        else:
            self.panel.img_spring_01.temp_btn_go.btn_common.SetText(80284)

    def init_spring_02(self):
        LUCKY_BAG_TASK_ID = (1000001, 1000003)
        finished_task_num = sum((1 for tid in LUCKY_BAG_TASK_ID if global_data.player.is_task_finished(tid)))
        receivable_task_num = sum((1 for tid in LUCKY_BAG_TASK_ID if global_data.player.is_task_reward_receivable(tid)))
        total_task_size = len(LUCKY_BAG_TASK_ID)
        self.panel.img_spring_02.nd_progress.lab_task_progress.SetString('{0}/{1}'.format(finished_task_num, total_task_size))
        self.panel.img_spring_02.nd_progress.progress_task.SetPercentage(finished_task_num / float(total_task_size) * 100)
        if receivable_task_num > 0:
            self.panel.img_spring_02.temp_btn_go.btn_common.SetText(80932)
            return
        if finished_task_num == total_task_size:
            self.panel.img_spring_02.temp_btn_go.btn_common.SetEnable(False)
            self.panel.img_spring_02.temp_btn_go.btn_common.SetText(606046)
            return

    def on_click_spring_01(self, *args):
        from logic.gutils import jump_to_ui_utils
        from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN
        jump_to_ui_utils.jump_to_mode_choose(PLAY_TYPE_CHICKEN)
        self.close()
        global_data.ui_mgr.close_ui('ActivitySpringFestivalMainUI')

    def on_click_spring_02(self, *args):
        from logic.gutils.jump_to_ui_utils import jump_to_task_ui
        from logic.gcommon.common_const.task_const import TASK_TYPE_DAYLY
        jump_to_task_ui(TASK_TYPE_DAYLY)
        self.close()