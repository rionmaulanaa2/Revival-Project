# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityExclusiveMecha.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityCollect import ActivityBase
from logic.gutils.activity_utils import get_left_time, is_activity_in_limit_time
from logic.gutils.template_utils import init_common_reward_list
from logic.gutils.mall_utils import is_pc_global_pay, limite_pay, is_steam_pay, get_pc_charge_price_str, get_charge_price_str, adjust_price
from common.cfg import confmgr
from logic.gutils.template_utils import get_left_info
from logic.gutils.task_utils import get_task_name, get_task_conf_by_id
from logic.gutils.jump_to_ui_utils import jump_to_web_charge, jump_to_lottery
from logic.client.const import mall_const

class ActivityExclusiveMecha(ActivityBase):

    def on_init_panel(self):
        super(ActivityExclusiveMecha, self).on_init_panel()

        @self.panel.btn_go.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils import jump_to_ui_utils
            key = 'v7l90YM95v6pRAVSAseygOAnpT3ObxWw'
            data_id = str(self._activity_type)
            web_url = 'https://interact2.webapp.163.com/g93jijia'
            inner_web_url = 'https://test-interact2.webapp.163.com/g93jijia'
            jump_to_ui_utils.jump_to_share_website(key, data_id, web_url, inner_web_url)

    def on_finalize_panel(self):
        if global_data.player:
            global_data.player.query_exclusive_mecha_info()