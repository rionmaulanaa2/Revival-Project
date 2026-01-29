# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseArmorWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon.item.item_const import BATTLE_DRESS_LIST
import copy
from logic.gutils.item_utils import get_item_name, get_item_desc, get_item_pic_by_item_no
from logic.gutils.template_utils import get_item_quality
from logic.gcommon.common_utils.local_text import get_text_by_id

class ExerciseArmorWidget(BaseUIWidget):
    HEAD_ARMOR_LIST = [
     16541, 16542, 16543]
    BODY_ARMOR_LIST = [16511, 16512, 16513]
    LEGG_ARMOR_LIST = [16601, 16602, 16603]
    SLOT_LIST = [
     HEAD_ARMOR_LIST, BODY_ARMOR_LIST, LEGG_ARMOR_LIST]
    selected_head_idx = -1
    selected_body_idx = -1
    selected_legg_idx = -1
    slot_idx = [
     '0', '1', 'head', 'body', 'legg']
    BAR_RES = 'gui/ui_res_2/battle_train/pnl_daoju_%d.png'

    def __init__(self, parent, panel):
        self.global_events = {}
        super(ExerciseArmorWidget, self).__init__(parent, panel)
        self.init_params()
        self.init_data()
        self.init_right_list()
        self.init_left_list()
        self.parent.armor_widget = self

    def destroy(self):
        self.upload_armor_conf()
        self.init_params()
        super(ExerciseArmorWidget, self).destroy()

    def show(self):
        super(ExerciseArmorWidget, self).show()

    def hide(self):
        super(ExerciseArmorWidget, self).hide()

    def init_params(self):
        self.armor_conf_list = []
        self.ori_armor_conf_list = []
        self.cur_index = 0

    def init_data(self):
        for slot in BATTLE_DRESS_LIST:
            item_data = global_data.player.logic.ev_g_clothing_data_by_pos(slot)
            item_id = item_data['item_id']
            self.armor_conf_list.append(item_id)

        self.ori_armor_conf_list = copy.deepcopy(self.armor_conf_list)

    def init_right_list(self):
        self.panel.temp_item_1.img_bar.SetDisplayFrameByPath('', self.BAR_RES % get_item_quality(self.armor_conf_list[0]))
        self.panel.temp_item_1.img_item.SetDisplayFrameByPath('', get_item_pic_by_item_no(self.armor_conf_list[0]))
        self.panel.temp_item_1.lab_level.SetString(str(get_item_quality(self.armor_conf_list[0])))
        self.panel.temp_item_2.img_bar.SetDisplayFrameByPath('', self.BAR_RES % get_item_quality(self.armor_conf_list[1]))
        self.panel.temp_item_2.img_item.SetDisplayFrameByPath('', get_item_pic_by_item_no(self.armor_conf_list[1]))
        self.panel.temp_item_2.lab_level.SetString(str(get_item_quality(self.armor_conf_list[1])))
        self.panel.temp_item_3.img_bar.SetDisplayFrameByPath('', self.BAR_RES % get_item_quality(self.armor_conf_list[2]))
        self.panel.temp_item_3.img_item.SetDisplayFrameByPath('', get_item_pic_by_item_no(self.armor_conf_list[2]))
        self.panel.temp_item_3.lab_level.SetString(str(get_item_quality(self.armor_conf_list[2])))

    def init_left_list(self):
        self.panel.list_item_2.DeleteAllSubItem()
        self.panel.list_item_2.SetInitCount(3)
        for idx, ui_item in enumerate(self.panel.list_item_2.GetAllItem()):
            item_id = self.HEAD_ARMOR_LIST[idx]
            self.init_left_list_item(ui_item, item_id)
            if item_id == self.armor_conf_list[0]:
                self.switch_left_list_item(2, idx)

            @ui_item.btn_item.unique_callback()
            def OnClick(_btn, _touch, _slot=2, _idx=idx, *args):
                self.on_click_left_item(_slot, _idx)

        for idx, ui_item in enumerate(self.panel.list_item_3.GetAllItem()):
            item_id = self.BODY_ARMOR_LIST[idx]
            self.init_left_list_item(ui_item, item_id)
            if item_id == self.armor_conf_list[1]:
                self.switch_left_list_item(3, idx)

            @ui_item.btn_item.unique_callback()
            def OnClick(_btn, _touch, _slot=3, _idx=idx, *args):
                self.on_click_left_item(_slot, _idx)

        for idx, ui_item in enumerate(self.panel.list_item_4.GetAllItem()):
            item_id = self.LEGG_ARMOR_LIST[idx]
            self.init_left_list_item(ui_item, item_id)
            if item_id == self.armor_conf_list[2]:
                self.switch_left_list_item(4, idx)

            @ui_item.btn_item.unique_callback()
            def OnClick(_btn, _touch, _slot=4, _idx=idx, *args):
                self.on_click_left_item(_slot, _idx)

    def init_left_list_item(self, ui_item, item_id):
        ui_item.img_item.SetDisplayFrameByPath('', get_item_pic_by_item_no(item_id))
        ui_item.lab_name.SetString(get_item_name(item_id))
        ui_item.lab_details.SetString(get_item_desc(item_id))

    def on_switch_tab(self, idx):
        self.parent.temp_bg.list_tab.GetItem(0).list_btn_right.GetItem(self.cur_index).btn_window_tab.SetSelect(False)
        self.parent.temp_bg.list_tab.GetItem(0).list_btn_right.GetItem(idx).btn_window_tab.SetSelect(True)
        self.cur_index = idx

    def on_switch_widget(self):
        self.parent.temp_bg.list_tab.GetItem(0).list_btn_right.SetInitCount(1)
        self.parent.temp_bg.list_tab.GetItem(0).list_btn_right.GetItem(0).btn_window_tab.SetText(80587)

    def on_click_left_item(self, slot, idx):
        self.switch_left_list_item(slot, idx)
        ui_item = getattr(self.panel, 'temp_item_%d' % (slot - 1))
        item_id = self.SLOT_LIST[slot - 2][idx]
        ui_item.img_bar.SetDisplayFrameByPath('', self.BAR_RES % get_item_quality(item_id))
        ui_item.img_item.SetDisplayFrameByPath('', get_item_pic_by_item_no(item_id))
        ui_item.lab_level.SetString(str(get_item_quality(item_id)))
        self.armor_conf_list[slot - 2] = item_id

    def switch_left_list_item--- This code section failed: ---

 133       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_FAST             0  'self'
           6  LOAD_ATTR             1  'panel'
           9  LOAD_CONST            1  'list_item_%d'
          12  LOAD_FAST             1  'slot'
          15  BINARY_MODULO    
          16  CALL_FUNCTION_2       2 
          19  STORE_FAST            3  'ui_list'

 134      22  LOAD_GLOBAL           0  'getattr'
          25  LOAD_GLOBAL           2  'slot_idx'
          28  LOAD_FAST             0  'self'
          31  LOAD_ATTR             2  'slot_idx'
          34  LOAD_FAST             1  'slot'
          37  BINARY_SUBSCR    
          38  BINARY_MODULO    
          39  CALL_FUNCTION_2       2 
          42  STORE_FAST            4  'select_idx'

 135      45  LOAD_FAST             2  'idx'
          48  LOAD_FAST             4  'select_idx'
          51  COMPARE_OP            3  '!='
          54  POP_JUMP_IF_FALSE    91  'to 91'

 136      57  LOAD_FAST             3  'ui_list'
          60  LOAD_ATTR             3  'GetItem'
          63  LOAD_FAST             4  'select_idx'
          66  CALL_FUNCTION_1       1 
          69  STORE_FAST            5  'ui_item'

 137      72  LOAD_FAST             5  'ui_item'
          75  LOAD_ATTR             4  'choose'
          78  LOAD_ATTR             5  'setVisible'
          81  LOAD_GLOBAL           6  'False'
          84  CALL_FUNCTION_1       1 
          87  POP_TOP          
          88  JUMP_FORWARD          0  'to 91'
        91_0  COME_FROM                '88'

 138      91  LOAD_GLOBAL           7  'setattr'
          94  LOAD_GLOBAL           2  'slot_idx'
          97  LOAD_FAST             0  'self'
         100  LOAD_ATTR             2  'slot_idx'
         103  LOAD_FAST             1  'slot'
         106  BINARY_SUBSCR    
         107  BINARY_MODULO    
         108  LOAD_FAST             2  'idx'
         111  CALL_FUNCTION_3       3 
         114  POP_TOP          

 139     115  LOAD_FAST             2  'idx'
         118  LOAD_CONST            3  -1
         121  COMPARE_OP            3  '!='
         124  POP_JUMP_IF_FALSE   161  'to 161'

 140     127  LOAD_FAST             3  'ui_list'
         130  LOAD_ATTR             3  'GetItem'
         133  LOAD_FAST             2  'idx'
         136  CALL_FUNCTION_1       1 
         139  STORE_FAST            5  'ui_item'

 141     142  LOAD_FAST             5  'ui_item'
         145  LOAD_ATTR             4  'choose'
         148  LOAD_ATTR             5  'setVisible'
         151  LOAD_GLOBAL           8  'True'
         154  CALL_FUNCTION_1       1 
         157  POP_TOP          
         158  JUMP_FORWARD          0  'to 161'
       161_0  COME_FROM                '158'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 39

    def upload_armor_conf(self):
        if self.armor_conf_list == self.ori_armor_conf_list:
            return
        if not global_data.player:
            return
        if not global_data.player.get_battle():
            return
        global_data.player.get_battle().call_soul_method('set_exercise_armor', (self.armor_conf_list,))