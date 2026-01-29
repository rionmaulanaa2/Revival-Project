# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/CreditCompensateUI.py
from __future__ import absolute_import
from logic.gutils.scene_utils import is_in_lobby
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils import template_utils

class CreditCompensateUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'role/i_role_compensate'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_get.btn_common_big.OnClick': '_on_click_receive'
       }
    GLOBAL_EVENT = {'lobby_scene_pause_event': '_lobby_scene_event'
       }

    def init_data(self, game_id, reward_id, param):
        self._reward_id = reward_id
        self._game_id = game_id
        from common.cfg import confmgr
        content_id = confmgr.get('credit_conf', 'CreditCommon', 'Content', 'compensation_reward_content', 'common_param')
        self.panel.content.SetString(get_text_local_content(content_id).format(char_name=param['char_name']))
        item_no, item_cnt = confmgr.get('common_reward_data', str(reward_id), 'reward_list')[0]
        template_utils.init_tempate_mall_i_item(self.panel.temp_reward, item_no, item_num=item_cnt, show_tips=True)

    def on_init_panel(self):
        super(CreditCompensateUI, self).on_init_panel()
        self._game_id = None
        self._reward_id = None
        cur_scene = global_data.game_mgr.scene
        if not is_in_lobby(cur_scene.scene_type):
            self.add_hide_count()
        return

    def _on_click_receive(self, *args):
        if self._game_id and global_data.player:
            global_data.player.request_credit_compensation_reward(self._game_id)
        self.close()

    def _lobby_scene_event(self, pause_flag):
        if not pause_flag:
            self.clear_show_count_dict()

    def on_finalize_panel(self):
        self.set_custom_close_func(None)
        return