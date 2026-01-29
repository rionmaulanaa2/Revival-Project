# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/LobbyItemPreviewUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import item_utils
from logic.gutils.template_utils import init_tempate_reward
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc, get_lobby_item_use_parms
from common.const.uiconst import DIALOG_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gutils.mall_utils import item_has_owned_by_item_no
from logic.gutils import jump_to_ui_utils

class LobbyItemPreviewUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/award_choose_preview_new'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    GLOBAL_EVENT = {'receive_reward_info_from_server_event': 'update_receive_reward_info'
       }

    def on_init_panel(self, item_no, need_probability=False):
        super(LobbyItemPreviewUI, self).on_init_panel()
        self.need_probability = need_probability
        self.item_no = 0
        self.init_params(item_no)
        self.init_bg(item_no)
        self.init_item_list()

    def on_finalize_panel(self):
        self.reward_list = []
        self.reward_data = {}
        super(LobbyItemPreviewUI, self).on_finalize_panel()

    def init_params(self, item_no):
        self.item_no = item_no
        self.cur_index = -1
        self.cur_item_id = 0
        self.reward_list = []
        self.reward_data = {}
        use_params = confmgr.get('lobby_item', str(item_no), default={}).get('use_params', {})
        if self.need_probability:
            reward_id = use_params.get('reward_id', -1)
            random_reward_data = global_data.player.get_random_reward_data(reward_id)
            if random_reward_data is None:
                return
            for item_id, random_data in six.iteritems(random_reward_data):
                min_num = random_data.get('min_num', 0)
                max_num = random_data.get('max_num', 0)
                if min_num != max_num:
                    item_num = str(min_num) + '~' + str(max_num) if 1 else min_num
                    self.reward_data[item_id] = (
                     item_id, item_num, random_data.get('rate', 0))
                    self.reward_list.append(item_id)

        else:
            self.reward_list = use_params.get('reward_list', [])
            self.reward_data = {}
            for i, reward_id in enumerate(self.reward_list):
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                item_id, item_num = reward_conf['reward_list'][0]
                self.reward_data[reward_id] = (item_id, item_num, 1)

        return

    def update_receive_reward_info(self):
        if self.item_no:
            self.init_params(self.item_no)
            self.init_bg(self.item_no)
            self.init_item_list()

    def init_bg(self, item_no):
        self.panel.temp_bar.lab_title.SetString(get_lobby_item_name(item_no))
        self.panel.list_content.SetInitCount(1)
        self.panel.lab_tips.SetString(get_lobby_item_desc(item_no))
        self.panel.lab_rate.setVisible(self.need_probability)

        @self.panel.temp_bar.btn_close.callback()
        def OnClick(btn, touch):
            self.close()

    def init_item_list(self):
        list_award = self.panel.list_award_choose
        list_award.SetInitCount(len(self.reward_list))
        list_award.SetVertIndent(0 if self.need_probability else -6)
        for i, item in enumerate(list_award.GetAllItem()):
            item_id = self.reward_data[self.reward_list[i]][0]
            owned = item_has_owned_by_item_no(item_id)
            init_tempate_reward(item.temp_reward, item_id, self.reward_data[self.reward_list[i]][1], isget=owned)
            item.temp_reward.lab_rate.SetString('%.2f' % (self.reward_data[self.reward_list[i]][2] * 100) + '%')
            item.temp_reward.lab_rate.setVisible(self.need_probability)

            @item.temp_reward.btn_choose.callback()
            def OnClick(btn, touch, idx=i):
                self.on_click_item(idx)

        self.on_click_item(0)

        @self.panel.btn_preview.callback()
        def OnClick(*args):
            self.on_click_btn_preview()

    def on_click_item(self, idx):
        list_reward = self.panel.list_award_choose
        list_len = list_reward.GetItemCount()
        if idx >= len(self.reward_list):
            return
        if idx == self.cur_index:
            return
        if idx >= list_len:
            return
        if self.cur_index != -1 and self.cur_index < list_len:
            list_reward.GetItem(self.cur_index).temp_reward.btn_choose.SetSelect(False)
        list_reward.GetItem(idx).temp_reward.btn_choose.SetSelect(True)
        self.cur_index = idx
        item_id = self.reward_data[self.reward_list[idx]][0]
        self.cur_item_id = item_id
        init_tempate_reward(self.panel.temp_item, item_id)
        self.panel.lab_name.SetString(get_lobby_item_name(item_id))
        rate_str = get_text_by_id(81059) + ': <fontname=gui/fonts/g93_num.ttf>{}</fontname>'.format('%.2f' % (self.reward_data[self.reward_list[idx]][2] * 100) + '%')
        self.panel.lab_rate.SetString(rate_str)
        self.panel.list_content.GetItem(0).lab_describe.SetString(get_lobby_item_desc(item_id))
        use_params = get_lobby_item_use_parms(item_id) or {}
        show_btn_preview = use_params.get('show_btn_preview', False)
        if show_btn_preview:
            self.panel.btn_preview.setVisible(True)
        else:
            self.panel.btn_preview.setVisible(False)

    def on_click_btn_preview(self, *args):
        if self.cur_item_id:
            jump_to_ui_utils.jump_to_display_detail_by_item_no(self.cur_item_id)