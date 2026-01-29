# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonCoreRewardWidget.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils.template_utils import init_tempate_mall_i_item
from .SeasonBaseUIWidget import SeasonBaseUIWidget
from .BattlePassDisplayWidget import BattlePassDisplayWidget

class SeasonCoreRewardWidget(SeasonBaseUIWidget):

    def re_display(self):
        if not self._displaying_item_no:
            global_data.emgr.change_model_display_scene_item.emit(None)
            return
        else:
            self._display_widget.display_award(self._displaying_item_no, reset_display_type=True)
            return

    def __init__(self, parent_ui, panel, close_call_back=None):
        self.global_events = {'season_pass_open_type': self._init_card_buy_btn
           }
        super(SeasonCoreRewardWidget, self).__init__(parent_ui, panel)
        self.panel.setVisible(True)
        self._displaying_item_no = None
        self._close_call_back = close_call_back
        self._select_item = None
        self._display_widget = BattlePassDisplayWidget(display_cb=self._display_cb)
        self._init_panel()
        return

    def _init_panel(self):
        self._low_core_award_lst = []
        self._high_core_award_lst = []
        self._init_ui_event()
        self._init_award_list()
        self.panel.PlayAnimation('appear')
        first_item = self.panel.list_advanced_award.GetItem(0)
        if not first_item:
            first_item = self.panel.list_basis_award.GetItem(0)
        if first_item and not first_item == self._select_item:
            first_item.btn_choose.OnClick(None)
        return

    def _init_ui_event(self):
        self.panel.btn_close.BindMethod('OnClick', self.on_click_close)
        self._init_card_buy_btn()
        from logic.gcommon.common_const.battlepass_const import ROTATE_FACTOR

        def on_model_drag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

        self.panel.nd_special_reward.BindMethod('OnDrag', on_model_drag)

    def _init_card_buy_btn(self, *args):
        if global_data.player:
            if global_data.player.has_buy_final_card():
                self.panel.btn_advanced.UnBindMethod('OnClick')
                self.panel.btn_buy_card.setVisible(False)
                self.panel.btn_buy_card.UnBindMethod('OnClick')
            else:
                self.panel.btn_buy_card.setVisible(True)
                self.panel.btn_advanced.BindMethod('OnClick', self._on_click_buy_card)
                self.panel.btn_buy_card.BindMethod('OnClick', self._on_click_buy_card)

    def _init_award_list(self):
        from logic.gutils.battle_pass_utils import get_now_season_pass_data
        sp_data = get_now_season_pass_data()
        reward_lst_nodes = [self.panel.list_basis_award, self.panel.list_advanced_award]
        for reward_lst in reward_lst_nodes:
            if reward_lst == self.panel.list_basis_award:
                self._low_core_award_lst = self._get_item_info_lst(sp_data.low_core_data, sp_data.low_core_info)
                cap = len(self._low_core_award_lst)
            else:
                self._high_core_award_lst = self._get_item_info_lst(sp_data.high_core_data, sp_data.high_core_info)
                cap = len(self._high_core_award_lst)
            reward_lst.BindMethod('OnCreateItem', self._on_create_callback)
            reward_lst.SetInitCount(cap)

    def _on_create_callback(self, lv, idx, ui_item):
        if lv == self.panel.list_basis_award:
            item_no, item_num = self._low_core_award_lst[idx]
        else:
            item_no, item_num = self._high_core_award_lst[idx]

        def on_click_callback(sel_item=ui_item, data=item_no):
            self._displaying_item_no = data
            self._display_widget.display_award(data)
            if self._select_item and self._select_item.isValid():
                self._select_item.btn_choose.SetSelect(False)
            self._select_item = sel_item
            self._select_item.btn_choose.SetSelect(True)

        init_tempate_mall_i_item(ui_item, item_no, item_num=item_num, callback=on_click_callback)

    def _display_cb(self, is_model, item_no):
        super(SeasonCoreRewardWidget, self)._display_cb(is_model, item_no)
        item_name = item_utils.get_lobby_item_name(item_no)
        item_desc = item_utils.get_lobby_item_desc(item_no)
        if is_model:
            self.panel.nd_special_reward.img_bar.lab_name.SetString(item_name)
            self.panel.nd_special_reward.lab_describe.SetString(item_desc)
            self.panel.nd_special_reward.img_bar.lab_name.setVisible(True)
        else:
            pic_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
            self.panel.nd_common_reward.nd_item.nd_cut.img_item.SetDisplayFrameByPath('', pic_path)
            self.panel.nd_common_reward.lab_name.SetString(item_name)
            self.panel.nd_common_reward.lab_describe.SetString(item_desc)
        self.panel.nd_special_reward.setVisible(is_model)
        self.panel.nd_common_reward.setVisible(not is_model)

    def _get_item_info_lst(self, reward_lst, reward_info):
        ret = []
        for reward_id in reward_lst:
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            item_id_lst = reward_conf.get('reward_list', [])
            idx_lst = reward_info.get(str(reward_id), [])
            for idx in idx_lst:
                if idx < len(item_id_lst):
                    ret.append(item_id_lst[idx])

        return ret

    def _on_click_buy_card(self, *args):
        from logic.gutils.battle_pass_utils import get_buy_season_card_ui_name
        if global_data.player and not global_data.player.has_buy_final_card():
            global_data.ui_mgr.show_ui(get_buy_season_card_ui_name(), 'logic.comsys.battle_pass')

    def on_click_close(self, *args):
        if self._display_widget:
            self._display_widget.clear_model_display()
        if self._close_call_back:
            self._close_call_back(False)
        self._close_call_back = None
        self.destroy()
        return

    def destroy(self):
        self.destroy_widget('_display_widget')
        if self.panel and self.panel.isValid():
            self.panel.Destroy()
        self.panel = None
        self._sp_data = None
        super(SeasonCoreRewardWidget, self).destroy()
        return