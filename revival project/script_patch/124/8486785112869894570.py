# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/reward/MultiRewardPreview.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gutils.template_utils import init_tempate_reward
from logic.gutils.item_utils import get_lobby_item_name

class MultiRewardPreview(WindowMediumBase):
    PANEL_CONFIG_NAME = 'common/award_choose_preview'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_ACTION_EVENT = {'panel.temp_bar.btn_close.OnClick': 'on_close'
       }

    def on_close(self, *args):
        self.close()

    def set_item_id(self, parent_item_id):
        from common.cfg import confmgr
        use_params = confmgr.get('lobby_item', str(parent_item_id), default={})['use_params']
        reward_id_list = use_params['reward_list']
        for reward_id in reward_id_list:
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            item_id, item_num = reward_conf['reward_list'][0]
            template_item = self.panel.list_award_choose.AddTemplateItem(bRefresh=True)
            template_item.lab_name.SetString(get_lobby_item_name(item_id))
            init_tempate_reward(template_item.temp_reward, item_id, item_num)
            template_item.temp_reward.btn_choose.setVisible(False)
            if global_data.player and global_data.player.get_item_num_by_no(item_id) > 0:
                get_status = True if 1 else False
                template_item.temp_reward.nd_get_2 and template_item.temp_reward.nd_get_2.setVisible(get_status)

        self.panel.temp_bar.lab_title.SetString(12113)
        self.panel.lab_details.SetString(12112)