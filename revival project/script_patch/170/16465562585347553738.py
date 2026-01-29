# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEWeekTaskWidgetUI.py
from __future__ import absolute_import
from common.utils.redpoint_check_func import check_lobby_red_point
from logic.comsys.task.PVEWeekTaskWidget import PVEWeekTaskWidget
from logic.comsys.task.TaskMainUI import TaskMainUI

class PVEWeekTaskWidgetUI(PVEWeekTaskWidget):

    @staticmethod
    def check_red_point():
        return TaskMainUI.check_red_point() and check_lobby_red_point()