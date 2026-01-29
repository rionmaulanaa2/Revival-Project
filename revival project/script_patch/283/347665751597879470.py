# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/EmojiListWidget.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from logic.gutils import items_book_utils
from logic.gutils import item_utils
from logic.gutils import mall_utils
from logic.client.const import items_book_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gcommon.item import lobby_item_type
from common.cfg import confmgr
from logic.comsys.items_book_ui.InteractionListWidgetBase import InteractionListWidgetBase
from logic.comsys.items_book_ui.ListSelectWidget import ListSelectWidget
ROTATE_FACTOR = 850

class EmojiListWidget(InteractionListWidgetBase):
    TAB_INDEX = items_book_const.EMOJI_ID
    TAB_ITEM_TYPE = lobby_item_type.L_ITEM_TYPE_EMOTICON
    DEFAULT_FILTER_STR_ID = 81383
    PATTERN_FILTER_STR_ID = 81384

    def init_widget(self):
        self.init_auto_emoji_widget()
        super(EmojiListWidget, self).init_widget()
        self.init_touch_widget()
        self.init_switch_emoji_mode_widget()

    def init_touch_widget(self):
        self.panel.nd_touch.BindMethod('OnDrag', self.on_drag_touch_layer)

    def init_auto_emoji_widget(self):
        auto_emoji_config = confmgr.get('auto_emoji', default={})
        moment_list = auto_emoji_config.get('moment_list', [])
        self.panel.temp_list.setVisible(False)
        item_list = self.panel.temp_list.nd_expression_auto.list_expression_auto
        item_list.SetInitCount(len(moment_list))
        for idx, ui_item in enumerate(item_list.GetAllItem()):
            moment_id = moment_list[idx]
            moment_info = auto_emoji_config.get(moment_id)
            name_text_id = moment_info.get('iTextID')
            ui_item.lab_scene.SetString(name_text_id)

        self._list_select_widget = ListSelectWidget(self, item_list)

    def init_switch_emoji_mode_widget(self):
        list_tab = self.panel.nd_tab.list_tab
        list_tab.SetInitCount(2)
        btn_manual = list_tab.GetItem(0).btn_tab
        btn_auto = list_tab.GetItem(1).btn_tab
        btn_manual.lab_tab.SetString(609660)
        btn_auto.lab_tab.SetString(609661)

        @btn_manual.unique_callback()
        def OnClick(btn, touch, _btn_manual=btn_manual, _btn_auto=btn_auto):
            self.on_click_btn_manual(_btn_manual, _btn_auto)

        @btn_auto.unique_callback()
        def OnClick(btn, touch, _btn_manual=btn_manual, _btn_auto=btn_auto):
            self.on_click_btn_auto(_btn_manual, _btn_auto)

        self.on_click_btn_manual(btn_manual, btn_auto)

    def on_drag_touch_layer(self, btn, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def show_item_detail(self, item_no):
        print('str item_no', item_no)
        if not self.panel:
            return
        valid = bool(item_no) and str(item_no) in self.role_interaction_info
        self.panel.lab_name.setVisible(valid)
        self.panel.lab_describe.setVisible(valid)
        if not valid:
            return
        self.panel.lab_name.SetString(items_book_utils.get_filter_item_show_name(self.TAB_INDEX, item_no))
        self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
        role_data = global_data.player.get_item_by_no(self.selected_role_id)
        default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(self.selected_role_id), 'default_skin')
        fashion_data = role_data.get_fashion() if role_data else {}
        dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT, default_skin)
        show_anim = 's_emptyhand_idle'
        end_anim = 's_emptyhand_idle'
        is_manage = self.interaction_state != items_book_const.INTERACTION_STATE_DISPLAY
        model_data = lobby_model_display_utils.get_items_book_interaction_model_data(self.selected_role_id, dressed_clothing_id, show_anim, is_manage, end_anim)
        model_data[0]['emoji_id'] = item_no
        global_data.emgr.change_model_display_scene_item.emit(model_data)
        self._get_use_buy_widget.update_target_item_no(item_no, self.interaction_state)

    def init_scene(self):
        config_index = lobby_model_display_const.ITEMBOOKS_GESTURE_DISPLAY if self.interaction_state == items_book_const.INTERACTION_STATE_DISPLAY else lobby_model_display_const.ITEMBOOKS_GESTURE_MANAGE
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, config_index, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def update_scene(self):
        self.init_scene()

    def refresh_widget(self):
        if self.selected_role_id is not None:
            self.update_scene()
            self.update_role_data(self.selected_role_id)
            self.update_role_redpoints()
        return

    def update_role_data(self, role_id, state_changed=False, data_changed=False):
        super(EmojiListWidget, self).update_role_data(role_id, state_changed, data_changed)
        if not state_changed:
            if self.get_interaction_state() == items_book_const.INTERACTION_STATE_DISPLAY:
                if self.is_auto_mode:
                    self.panel.PlayAnimation('disappear_manage_list')
                    ani = 'disappear_manage_list'
                else:
                    self.panel.PlayAnimation('disappear_manage')
                    ani = 'disappear_manage'
            elif self.is_auto_mode:
                self.panel.PlayAnimation('show_manage_list')
                ani = 'show_manage_list'
            else:
                self.panel.PlayAnimation('show_manage')
                ani = 'show_manage'
            self.panel.FastForwardToAnimationTime(ani, self.panel.GetAnimationMaxRunTime(ani))

    def on_state_changed(self):
        if self.get_interaction_state() == items_book_const.INTERACTION_STATE_DISPLAY:
            if self.is_auto_mode:
                self.panel.PlayAnimation('disappear_manage_list')
            else:
                self.panel.PlayAnimation('disappear_manage')
        elif self.is_auto_mode:
            self.panel.PlayAnimation('show_manage_list')
        else:
            self.panel.PlayAnimation('show_manage')
        self.update_scene()

    def on_click_btn_manual(self, btn_manual, btn_auto):
        self.is_auto_mode = False
        self.panel.temp_round.setVisible(True)
        self.panel.temp_list.setVisible(False)
        btn_manual.SetSelect(True)
        btn_auto.SetSelect(False)
        self.update_interaction_list(True, 0)

    def on_click_btn_auto(self, btn_manual, btn_auto):
        self.is_auto_mode = True
        self.panel.temp_round.setVisible(False)
        self.panel.temp_list.setVisible(True)
        btn_auto.SetSelect(True)
        btn_manual.SetSelect(False)
        self.update_interaction_list(True, 0)

    def get_cur_select_widget(self):
        if not self.is_auto_mode:
            return self._round_select_widget
        return self._list_select_widget

    def quick_fill_list_select_widget(self, role_interaction_data, using_interaction_data, item_count):
        auto_emoji_config = confmgr.get('auto_emoji', default={})
        moment_list = auto_emoji_config.get('moment_list', [])
        item_idx = 0
        item_list = self.panel.temp_list.nd_expression_auto.list_expression_auto
        moment_count = item_list.GetItemCount()
        for idx in range(0, moment_count):
            moment_id = moment_list[idx]
            if moment_id in role_interaction_data and role_interaction_data[moment_id] != 0:
                continue
            while item_idx < item_count:
                item_no = self.auto_match_list[item_idx]
                item_idx += 1
                can_use, _ = mall_utils.item_can_use_by_item_no(item_no)
                is_using = int(item_no) in using_interaction_data
                if can_use and not is_using:
                    global_data.player.try_set_interaction_data(int(self.selected_role_id), moment_id, item_no)
                    global_data.player.req_del_item_redpoint(int(item_no))
                    break

    def on_data_empty(self):
        super(EmojiListWidget, self).on_data_empty()
        self.panel.StopAnimation('show_manage_list')
        self.panel.StopAnimation('disappear_manage_list')
        self.panel.temp_list.setVisible(False)
        self.panel.nd_tab.setVisible(False)

    def on_data_exist(self):
        is_manage = self.interaction_state == items_book_const.INTERACTION_STATE_MANAGE_DISPLAY
        if self.is_showing_empty:
            if is_manage:
                ani_name = 'show_manage'
            else:
                ani_name = 'disappear_manage_list' if self.is_auto_mode else 'disappear_manage'
            self.panel.PlayAnimation(ani_name)
        self.is_showing_empty = False
        self.panel.nd_tab.setVisible(True)