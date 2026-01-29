# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Rank/BattleRankProgressUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.const import uiconst

class BattleRankProgressUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_point/fight_point'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    SPEED = 1
    RANK_SPEED = 1

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.refresh_progress()

    def on_finalize_panel(self):
        pass

    def init_parameters(self):
        self.rank_data = [
         (1, 990), (2, 881), (3, 772), (4, 663), (5, 554), (6, 445), (7, 336), (8, 227), (9, 118), (10, 109), (11, 90), (12, 81), (13, 52), (14, 23)]
        self.rank_percentage = {}
        for data in self.rank_data[:5]:
            rank, point = data
            self.rank_percentage[rank] = self.point_to_percentage(point)

    def init_event(self):
        pass

    def point_to_percentage(self, point):
        f_rank, f_point = self.rank_data[0]
        l_rank, l_point = self.rank_data[len(self.rank_data) - 1]
        return 1.0 * (point - l_point) / (f_point - l_point) * 100

    def refresh_progress(self):
        f_rank, f_point = self.rank_data[0]
        self.set_rank_show('temp_first_point', f_rank, f_point)
        l_rank, l_point = self.rank_data[len(self.rank_data) - 1]
        self.set_rank_show('temp_last_point', l_rank, l_point)
        w_rank, w_point = self.rank_data[3]
        old_percentage = self.panel.progress_eliminate.getPercentage()
        new_percentage = self.point_to_percentage(w_point)
        time = abs(new_percentage - old_percentage) / self.SPEED
        print('?????????????????????????', new_percentage, time)
        self.panel.progress_eliminate.SetPercentageWithAni(new_percentage, time)
        self.set_rank_show('temp_eliminate', w_rank, w_point)
        rank, point = self.rank_data[3]
        self.set_rank_show('temp_my_point', rank, point)
        self.goto_rank('temp_my_point', 3)

    def set_rank_show(self, uiname, rank, point):
        getattr(self.panel, uiname).lab_rank.setString('%st' % rank)
        getattr(self.panel, uiname).lab_point.setString(str(point))

    def goto_rank(self, uiname, rank):
        rank, point = self.rank_data[rank - 1]
        end_percentage = self.point_to_percentage(point)
        if rank not in self.rank_percentage:
            self.rank_percentage[rank] = end_percentage
        time = abs(end_percentage - self.rank_percentage[rank]) / self.SPEED

        def refresh_rank(pass_time):
            if self.rank_percentage[rank] < end_percentage:
                self.rank_percentage[rank] += self.SPEED
            elif self.rank_percentage[rank] > end_percentage:
                self.rank_percentage[rank] -= self.SPEED
            self.set_rank_position(uiname, self.rank_percentage[rank])

        def refresh_rank_finsh():
            self.rank_percentage[rank] = end_percentage
            self.set_rank_position(uiname, self.rank_percentage[rank])

        getattr(self.panel, uiname).StopTimerAction()
        getattr(self.panel, uiname).TimerAction(refresh_rank, time, callback=refresh_rank_finsh)

    def set_rank_position(self, uiname, percentage):
        x = self.get_percentage_position_x(percentage)
        _, rank_y = getattr(self.panel, uiname).GetPosition()
        getattr(self.panel, uiname).SetPosition(x, rank_y)

    def get_percentage_position_x(self, percentage):
        w, _ = self.panel.progress_eliminate.GetContentSize()
        x, _ = self.panel.progress_eliminate.GetPosition()
        return x - w * 0.5 + 1.0 * percentage / 100 * w