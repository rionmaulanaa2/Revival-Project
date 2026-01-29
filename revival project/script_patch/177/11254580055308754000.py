# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseItemWidget.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
import copy
from logic.gutils.new_template_utils import init_top_tab_list
from logic.gutils.template_utils import get_item_quality
from logic.gutils.item_utils import get_item_name, get_item_desc, get_item_max_overlay, get_item_pic_by_item_no
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock

class ExerciseItemWidget(BaseUIWidget):
    selected_tab_idx = -1
    selected_item_idx = -1
    BAR_RES = 'gui/ui_res_2/battle_train/pnl_daoju_%d.png'

    def __init__(self, parent, panel):
        self.global_events = {}
        super(ExerciseItemWidget, self).__init__(parent, panel)
        self.init_params()
        self.init_data()
        self.init_right_list()
        self.init_ui_event()
        self.init_tab()
        self.parent.item_widget = self
        self.panel.list_tab.GetItem(0).btn_tab.OnClick(TouchMock())

    def destroy(self):
        self.upload_item_conf()
        self.init_params()
        super(ExerciseItemWidget, self).destroy()

    def show(self):
        super(ExerciseItemWidget, self).show()

    def hide(self):
        super(ExerciseItemWidget, self).hide()

    def init_params(self):
        self.item_conf_dict = {}
        self.right_item_dict = {}
        self.cur_index = 0

    def init_data(self):
        map_data = confmgr.get('game_mode/exercise/c_map_exercise_conf')
        self.tab_data = map_data['Item']['Content']
        self.all_item_list = self.tab_data.get('1').get('item_list')
        self.item_conf_dict = {}
        for item_id in self.all_item_list:
            item_count = global_data.player.logic.ev_g_item_count(item_id) if global_data.player and global_data.player.logic else 0
            if item_count > 0:
                self.item_conf_dict[item_id] = item_count

        self.ori_item_conf_dict = copy.deepcopy(self.item_conf_dict)
        self.right_item_dict = copy.deepcopy(self.item_conf_dict)
        self.tab_list_data = []
        for idx in range(len(self.tab_data)):
            self.tab_list_data.append({'text': self.tab_data[str(idx + 1)]['tab_text']})

    def init_right_list(self):
        self.panel.list_item.DeleteAllSubItem()
        if self.right_item_dict:
            self.panel.list_item.SetInitCount(len(self.right_item_dict))
            for idx, item_id in enumerate(self.right_item_dict):
                ui_item = self.panel.list_item.GetItem(idx)
                ui_item.setTag(item_id)
                item_quality = get_item_quality(item_id)
                item_bar = self.BAR_RES % item_quality
                item_pic = get_item_pic_by_item_no(item_id)
                item_count = self.right_item_dict[item_id]
                ui_item.img_bar.SetDisplayFrameByPath('', item_bar)
                ui_item.img_item.SetDisplayFrameByPath('', item_pic)
                ui_item.lab_quantity.SetString(str(item_count))

    def init_ui_event(self):

        @self.panel.nd_right.btn_delete.unique_callback()
        def OnClick(_btn, _touch, *args):
            self.on_click_delete_all()

    def init_tab(self):
        init_top_tab_list(self.panel.list_tab, self.tab_list_data, self.on_click_tab)

    def on_switch_tab(self, idx):
        self.parent.temp_bg.list_tab.GetItem(0).list_btn_right.GetItem(self.cur_index).btn_window_tab.SetSelect(False)
        self.parent.temp_bg.list_tab.GetItem(0).list_btn_right.GetItem(idx).btn_window_tab.SetSelect(True)
        self.cur_index = idx

    def on_switch_widget(self):
        self.parent.temp_bg.list_tab.GetItem(0).list_btn_right.SetInitCount(1)
        self.parent.temp_bg.list_tab.GetItem(0).list_btn_right.GetItem(0).btn_window_tab.SetText(920735)

    def on_click_tab(self, tab_item, idx):
        if idx == self.selected_tab_idx:
            return
        self.selected_item_idx = -1
        self.selected_tab_idx = idx
        tab_item_list = self.tab_data[str(idx + 1)]['item_list']
        self.panel.list_item_2.DeleteAllSubItem()
        self.panel.list_item_2.SetInitCount(len(tab_item_list))
        all_items = self.panel.list_item_2.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            item_id = tab_item_list[idx]
            item_quality = get_item_quality(item_id)
            item_bar = self.BAR_RES % item_quality
            item_pic = get_item_pic_by_item_no(item_id)
            item_name = get_item_name(item_id)
            item_desc = get_item_desc(item_id)
            ui_item.bar_item.SetDisplayFrameByPath('', item_bar)
            ui_item.img_item.SetDisplayFrameByPath('', item_pic)
            ui_item.lab_name.SetString(item_name)
            ui_item.lab_details.SetString(item_desc)
            ui_item.setTag(item_id)
            if item_id in self.right_item_dict:
                ui_item.nd_selected.setVisible(True)
            else:
                ui_item.nd_selected.setVisible(False)

            @ui_item.btn_item.unique_callback()
            def OnClick(_btn, _touch, _idx=idx, _item_id=item_id, _ui_item=ui_item):
                self.on_click_left_item(_idx, _item_id, _ui_item)

    def on_click_left_item(self, idx, item_id, ui_item):
        self.switch_left_item(idx)
        if item_id not in self.right_item_dict:
            self.add_item_to_right_list(item_id, ui_item)
        else:
            self.remove_item_from_right_list(item_id, ui_item)

    def switch_left_item(self, idx):
        if idx != self.selected_item_idx:
            if self.selected_item_idx != -1:
                ui_item = self.panel.list_item_2.GetItem(self.selected_item_idx)
                ui_item.nd_choose.setVisible(False)
            self.selected_item_idx = idx
            if idx != -1:
                ui_item = self.panel.list_item_2.GetItem(idx)
                ui_item.nd_choose.setVisible(True)
        else:
            self.selected_item_idx = -1
            ui_item = self.panel.list_item_2.GetItem(idx)
            ui_item.nd_choose.setVisible(False)

    def add_item_to_right_list(self, item_id, btn):
        if item_id not in self.right_item_dict:
            self.right_item_dict[item_id] = 0
            ui_item = self.panel.list_item.AddTemplateItem(bRefresh=True)
            ui_item.setTag(item_id)
            item_quality = get_item_quality(item_id)
            item_bar = self.BAR_RES % item_quality
            item_pic = get_item_pic_by_item_no(item_id)
            item_count = get_item_max_overlay(item_id)
            self.right_item_dict[item_id] = item_count
            ui_item.img_bar.SetDisplayFrameByPath('', item_bar)
            ui_item.img_item.SetDisplayFrameByPath('', item_pic)
            ui_item.lab_quantity.SetString(str(item_count))
            btn.nd_selected.setVisible(True)
            btn.nd_choose.setVisible(True)

    def remove_item_from_right_list(self, item_id, btn):
        if item_id in self.right_item_dict:
            self.right_item_dict.pop(item_id)
            self.panel.list_item.DeleteItemByTag(item_id, bRefresh=True)
            btn.nd_selected.setVisible(False)
            btn.nd_choose.setVisible(False)

    def on_click_delete_all(self, *args):
        if not self.right_item_dict:
            return
        self.switch_left_item(-1)
        for item_id in self.right_item_dict:
            self.panel.list_item.DeleteItemByTag(item_id, bRefresh=False)
            ui_item = self.panel.list_item_2.GetItemByTag(item_id)
            if ui_item:
                ui_item.nd_choose.setVisible(False)
                ui_item.nd_selected.setVisible(False)

        self.panel.list_item._refreshItemPos()
        self.right_item_dict = {}

    def upload_item_conf(self):
        if self.right_item_dict == self.ori_item_conf_dict:
            return
        if not global_data.player:
            return
        if not global_data.player.get_battle():
            return
        self.item_conf_dict = copy.deepcopy(self.right_item_dict)
        self.item_conf_dict.update({9925: 1})
        global_data.player.get_battle().call_soul_method('set_exercise_items', (self.item_conf_dict,))