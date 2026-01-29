# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/interaction/InteractionBaseUI.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils import items_book_utils
from logic.gutils import item_utils
from logic.gutils.interaction_utils import set_emoji_icon
import math
from common.const import uiconst

class InteractionBaseUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_action_spray_panel'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        super(InteractionBaseUI, self).on_init_panel(*args, **kwargs)
        self.sel_angle = 0
        self.init_widget()
        if 'click_close_callback' in kwargs:
            self.click_close_callback = kwargs['click_close_callback']
        else:
            self.click_close_callback = None
        return

    def init_data(self):
        if self.data_inited:
            return
        self.data_inited = True

    def init_widget(self):
        self.action_dict = {}
        self.select_idx = -1
        self.enable_select = False
        self.data_inited = False
        self.init_event()
        self.init_action_template()
        self.reset_info()
        self.init_angle_to_select_idx()
        self.hide()

    def init_event(self):
        self.btn_close.BindMethod('OnClick', self.on_click_close)

    def on_finalize_panel(self):
        self.click_close_callback = None
        return

    def on_click_close(self, *args):
        self.hide()
        if self.click_close_callback and callable(self.click_close_callback):
            self.click_close_callback()

    def reset_info(self):
        self.on_action_selected(-1)

    @staticmethod
    def get_action_dict():
        player = global_data.player
        if not player:
            return {}
        role_id = global_data.player.get_role()
        return global_data.player.get_role_interaction_data(role_id)

    def show(self):
        super(InteractionBaseUI, self).show()
        self.action_dict = self.get_action_dict()
        self.enable_select = True
        self.reset_info()
        self.init_data()
        self.panel.lab_item.SetString('')
        self.init_action_template()
        self.panel.btn_close.setVisible(True)

    def hide(self):
        super(InteractionBaseUI, self).hide()
        self.enable_select = False
        self.reset_info()
        self.panel.btn_close.setVisible(False)

    def init_action_template(self):
        self.idx_temp_dict = {}
        for temp_idx in range(0, 8):
            item_name = 'temp__action_spray_%d' % (temp_idx + 1)
            temp_item = getattr(self.panel, item_name, None)
            self.init_template_idx(temp_idx, temp_item)

        return

    def init_angle_to_select_idx(self):
        self.angle_list = []
        self.list_idx_to_action_idx_map = {}
        delta_angle = math.pi / 8
        per_item_angle = math.pi / 4
        start_angle = -delta_angle
        angle_idx = 0
        for temp_idx in range(0, 8):
            end_angle = start_angle + per_item_angle
            if end_angle > math.pi:
                end_angle -= math.pi * 2
                self.list_idx_to_action_idx_map[angle_idx] = temp_idx
                angle_idx += 1
                self.angle_list.append([start_angle, math.pi])
                self.list_idx_to_action_idx_map[angle_idx] = temp_idx
                angle_idx += 1
                self.angle_list.append([-math.pi, end_angle])
            else:
                self.list_idx_to_action_idx_map[angle_idx] = temp_idx
                angle_idx += 1
                self.angle_list.append([start_angle, end_angle])
            start_angle = end_angle

        print(self.angle_list)

    def check_action_valid(self, idx):
        raise NotImplementedError

    def init_template_idx(self, idx, temp_item):

        def set_driver_tag--- This code section failed: ---

 129       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_DEREF            0  'temp_item'
           6  LOAD_CONST            1  'bar_driver_head'
           9  CALL_FUNCTION_2       2 
          12  POP_JUMP_IF_FALSE   156  'to 156'
          15  LOAD_DEREF            0  'temp_item'
          18  LOAD_ATTR             1  'bar_driver_head'
        21_0  COME_FROM                '12'
          21  POP_JUMP_IF_FALSE   156  'to 156'

 130      24  LOAD_FAST             0  'item_no'
          27  POP_JUMP_IF_TRUE     50  'to 50'

 131      30  LOAD_DEREF            0  'temp_item'
          33  LOAD_ATTR             1  'bar_driver_head'
          36  LOAD_ATTR             2  'setVisible'
          39  LOAD_GLOBAL           3  'False'
          42  CALL_FUNCTION_1       1 
          45  POP_TOP          

 132      46  LOAD_CONST            0  ''
          49  RETURN_END_IF    
        50_0  COME_FROM                '27'

 133      50  LOAD_CONST            2  ''
          53  LOAD_CONST            3  ('get_interact_role_tag_by_role_id',)
          56  IMPORT_NAME           4  'logic.gutils.item_utils'
          59  IMPORT_FROM           5  'get_interact_role_tag_by_role_id'
          62  STORE_FAST            1  'get_interact_role_tag_by_role_id'
          65  POP_TOP          

 134      66  LOAD_GLOBAL           6  'items_book_utils'
          69  LOAD_ATTR             7  'get_interaction_belong_to_role'
          72  LOAD_ATTR             4  'logic.gutils.item_utils'
          75  LOAD_GLOBAL           8  'True'
          78  CALL_FUNCTION_257   257 
          81  STORE_FAST            2  'role_id'

 135      84  LOAD_FAST             2  'role_id'
          87  POP_JUMP_IF_FALSE   137  'to 137'

 136      90  LOAD_DEREF            0  'temp_item'
          93  LOAD_ATTR             1  'bar_driver_head'
          96  LOAD_ATTR             2  'setVisible'
          99  LOAD_GLOBAL           8  'True'
         102  CALL_FUNCTION_1       1 
         105  POP_TOP          

 137     106  LOAD_DEREF            0  'temp_item'
         109  LOAD_ATTR             1  'bar_driver_head'
         112  LOAD_ATTR             9  'icon_role'
         115  LOAD_ATTR            10  'SetDisplayFrameByPath'
         118  LOAD_CONST            5  ''
         121  LOAD_FAST             1  'get_interact_role_tag_by_role_id'
         124  LOAD_FAST             2  'role_id'
         127  CALL_FUNCTION_1       1 
         130  CALL_FUNCTION_2       2 
         133  POP_TOP          
         134  JUMP_ABSOLUTE       156  'to 156'

 139     137  LOAD_DEREF            0  'temp_item'
         140  LOAD_ATTR             1  'bar_driver_head'
         143  LOAD_ATTR             2  'setVisible'
         146  LOAD_GLOBAL           3  'False'
         149  CALL_FUNCTION_1       1 
         152  POP_TOP          
         153  JUMP_FORWARD          0  'to 156'
       156_0  COME_FROM                '153'

Parse error at or near `CALL_FUNCTION_257' instruction at offset 78

        self.idx_temp_dict[idx] = temp_item
        temp_item.btn_action_spray_sel.EnableCustomState(True)
        is_valid = self.check_action_valid(idx)
        if is_valid:
            action_data = self.action_dict[idx]
            set_emoji_icon(temp_item.temp_icon, action_data)
            temp_item.temp_icon.setVisible(True)
            temp_item.icon_ban.setVisible(False)
            set_driver_tag(action_data)
        elif idx not in self.action_dict or self.action_dict.get(idx, None) == 0:
            temp_item.temp_icon.setVisible(False)
            temp_item.icon_ban.setVisible(False)
            set_driver_tag(None)
        else:
            action_data = self.action_dict[idx]
            set_emoji_icon(temp_item.temp_icon, action_data)
            temp_item.temp_icon.setVisible(True)
            temp_item.icon_ban.setVisible(True)
            set_driver_tag(action_data)
        return

    def on_action_selected(self, idx):
        if idx != self.select_idx:
            self.panel.lab_item.SetString('')
            prev_item = self.idx_temp_dict.get(self.select_idx, None)
            item = self.idx_temp_dict.get(idx, None)
            if prev_item:
                prev_item.btn_action_spray_sel.SetSelect(False)
            if self.check_action_valid(idx):
                item.btn_action_spray_sel.SetSelect(True)
                self.select_idx = idx
            else:
                self.select_idx = -1
        return

    def try_select_action(self, angle):
        if self.enable_select and self.data_inited:
            selected_idx = -1
            for idx, angle_range in enumerate(self.angle_list):
                selected_idx = idx
                if angle_range[0] <= angle < angle_range[1]:
                    break

            temp_idx = self.list_idx_to_action_idx_map[selected_idx]
            item_no = self.action_dict.get(temp_idx, None)
            self.panel.lab_item.SetString(item_utils.get_lobby_item_name(item_no) or '')
            self.on_action_selected(temp_idx)
        return

    def try_action(self):
        raise NotImplementedError

    def set_sel_angle(self, angle):
        self.sel_angle = angle