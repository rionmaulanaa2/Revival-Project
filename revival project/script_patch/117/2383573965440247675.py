# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySSSecondAccumulateLottery.py
from __future__ import absolute_import
from logic.gutils import task_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.item_utils import get_item_rare_degree
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.item_utils import REWARD_RARE_COLOR
from logic.gcommon.item import item_const
import cc
from logic.gutils.reward_item_ui_utils import refresh_item_info
from logic.comsys.activity.ActivitySSAccumulateLottery import ActivitySSAccumulateLottery

class ActivitySSSecondAccumulateLottery(ActivitySSAccumulateLottery):

    def __init__(self, dlg, activity_type):
        super(ActivitySSSecondAccumulateLottery, self).__init__(dlg, activity_type)

    def update_receive_img(self, sub_item_widget, has_receive, is_receivable):
        img_node_path = 'gui/ui_res_2/lottery/lottery_activity/activity_s2_new/activity_s2_new_bones/img_progresspoint2.png'
        if has_receive:
            img_node_path = 'gui/ui_res_2/lottery/lottery_activity/activity_s2_new/activity_s2_new_bones/img_progresspoint1.png'
        elif is_receivable:
            img_node_path = 'gui/ui_res_2/lottery/lottery_activity/activity_s2_new/activity_s2_new_bones/img_progresspoint3.png'
        sub_item_widget.img_node.SetDisplayFrameByPath('', img_node_path)