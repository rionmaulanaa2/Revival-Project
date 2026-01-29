# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/RecallMechaChooseUI.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gutils.template_utils import init_tempate_reward
from logic.gutils.item_utils import get_lobby_item_name

class RecallMechaChooseUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'common/award_choose'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_ACTION_EVENT = {'panel.temp_bar.btn_close.OnClick': 'on_close',
       'panel.temp_bar.temp_btn_sure.btn_major.OnClick': 'on_confirm'
       }

    def on_init_panel(self, *args, **kwargs):
        self.selected_item = None
        self.callback = None
        self.panel.temp_bar.nd_like.setVisible(False)
        self.panel.temp_bar.nd_muti_choose.setVisible(False)
        self.panel.temp_bar.temp_num.setVisible(False)
        return

    def on_close(self, *args):
        self.close()

    def config(self, parent_item_id, call_back):
        self.panel.list_award_choose.SetInitCount(0)
        from common.cfg import confmgr
        use_params = confmgr.get('lobby_item', str(parent_item_id), default={})['use_params']
        reward_id_list = use_params['reward_list']
        i = 0
        for reward_id in reward_id_list:
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            item_id, item_num = reward_conf['reward_list'][0]
            template_item = self.panel.list_award_choose.AddTemplateItem(bRefresh=True)
            template_item.lab_name.SetString(get_lobby_item_name(item_id))
            init_tempate_reward(template_item.temp_reward, item_id, item_num)
            template_item.temp_reward.bind_item_no = item_id
            template_item.temp_reward.bind_item_idx = i
            template_item.temp_reward.btn_choose.setVisible(True)
            if global_data.player and global_data.player.get_item_num_by_no(item_id) > 0:
                get_status = True if 1 else False
                template_item.temp_reward.nd_get_2 and template_item.temp_reward.nd_get_2.setVisible(get_status)
                self.set_click_callback(template_item.temp_reward, item_id)
                i += 1

        self.panel.temp_bar.lab_title.SetString(634299)
        self.panel.lab_details.SetString(12112)
        self.callback = call_back
        self.udpate_use_btn()

    def on_confirm(self, *args):
        if self.callback and self.selected_item:
            self.callback(self.selected_item.bind_item_idx, self.selected_item.bind_item_no)
        self.close()

    def udpate_use_btn(self):
        if self.selected_item:
            self.panel.temp_btn_sure.btn_major.SetEnable(True)
        else:
            self.panel.temp_btn_sure.btn_major.SetEnable(False)

    def click_callback(self, item):
        if self.selected_item and self.selected_item.btn_choose:
            self.selected_item.btn_choose.SetSelect(False)
        self.selected_item = item
        if self.selected_item and self.selected_item.btn_choose:
            self.selected_item.btn_choose.SetSelect(True)
        self.udpate_use_btn()

    def set_click_callback(self, temp_item_ui, item_id):
        temp_item_ui.btn_choose.SetPressEnable(True)
        p_touch = [
         None]

        @temp_item_ui.btn_choose.unique_callback()
        def OnBegin(btn, touch):
            p_touch[0] = touch
            return True

        @temp_item_ui.btn_choose.callback()
        def OnPressedWithNum(ctrl, num):
            position = p_touch[0].getLocation()
            global_data.emgr.show_item_desc_ui_event.emit(item_id, None, directly_world_pos=position, extra_info={'show_jump': False})
            return

        @temp_item_ui.btn_choose.callback()
        def OnClick(ctrl, touch):
            self.click_callback(temp_item_ui)

        return