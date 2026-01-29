# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/GestureListWidget.py
from __future__ import absolute_import
from logic.gutils import items_book_utils
from logic.gutils import item_utils
from logic.client.const import items_book_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gcommon.item import lobby_item_type
from common.cfg import confmgr
from logic.comsys.items_book_ui.InteractionListWidgetBase import InteractionListWidgetBase
ROTATE_FACTOR = 850

class GestureListWidget(InteractionListWidgetBase):
    TAB_INDEX = items_book_const.GESTURE_ID
    TAB_ITEM_TYPE = lobby_item_type.L_ITEM_TYPE_GESTURE
    DEFAULT_FILTER_STR_ID = 81385
    PATTERN_FILTER_STR_ID = 81386

    def init_widget(self):
        super(GestureListWidget, self).init_widget()
        self.init_touch_widget()

    def init_touch_widget(self):
        self.panel.nd_touch.BindMethod('OnDrag', self.on_drag_touch_layer)

    def on_drag_touch_layer(self, btn, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def show_item_detail(self, item_no):
        valid = bool(item_no) and str(item_no) in self.role_interaction_info
        if not self.panel:
            return
        else:
            self.panel.lab_name.setVisible(valid)
            self.panel.lab_describe.setVisible(valid)
            if not valid:
                return
            self.panel.lab_name.SetString(items_book_utils.get_filter_item_show_name(items_book_const.GESTURE_ID, item_no))
            self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
            role_data = global_data.player.get_item_by_no(self.selected_role_id)
            default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(self.selected_role_id), 'default_skin')
            fashion_data = role_data.get_fashion() if role_data else {}
            dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT, default_skin)
            show_anim = self.role_interaction_info[str(item_no)]['action_name']
            end_anim = self.role_interaction_info[str(item_no)].get('idle_name', None)
            is_manage = self.interaction_state != items_book_const.INTERACTION_STATE_DISPLAY
            model_data = lobby_model_display_utils.get_items_book_interaction_model_data(self.selected_role_id, dressed_clothing_id, show_anim, is_manage, end_anim)
            global_data.emgr.change_model_display_scene_item.emit(model_data)
            self._get_use_buy_widget.update_target_item_no(item_no, self.interaction_state)
            return

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

    def on_state_changed(self):
        super(GestureListWidget, self).on_state_changed()
        self.update_scene()