# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/ActiveGiftAdUI.py
import common.const.uiconst as ui_const
from common.uisys.basepanel import BasePanel
from logic.gutils.template_utils import init_price_template
from logic.gutils.template_utils import init_setting_slider3
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gutils.mall_utils import check_yuanbao
from logic.gutils import item_utils, task_utils
from common.cfg import confmgr
from .SeasonPassActiveGiftUI import TASK_LIST

class ActiveGiftAdUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/active_gift/i_battle_pass_active_gift_describe'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = ui_const.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_back.OnClick': 'on_close',
       'btn_go.OnClick': 'on_go'
       }

    def on_init_panel(self, *args):
        self.panel.PlayAnimation('appear')
        total_rewatd_num = 0
        for task_id in TASK_LIST:
            reward_id = task_utils.get_task_reward(task_id)
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            if len(reward_list) < 1:
                return
            item_id, item_num = reward_list[0]
            total_rewatd_num += item_num

        self.panel.lab_total.SetString(get_text_by_id(635163).format(total_rewatd_num))

    def on_close(self, *args):
        self.close()

    def on_go(self, *args):
        from .SeasonPassActiveGiftUI import SeasonPassActiveGiftUI
        ui = SeasonPassActiveGiftUI(None, None)
        self.close()
        return