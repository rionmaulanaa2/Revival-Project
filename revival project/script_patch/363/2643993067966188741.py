# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/MiaomiaoFunctionWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gutils import mall_utils
from logic.comsys.items_book_ui.SkinItemListWidget import SkinItemListWidget
from logic.comsys.items_book_ui.MiaomiaoItemGoUseDismountWidget import MiaomiaoItemGoUseDismountWidget
from logic.comsys.items_book_ui.ItemFilterWidget import ItemFilterWidget
from logic.gutils import items_book_utils
from logic.client.const import items_book_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import item_utils
from common.framework import Functor
from logic.gutils import template_utils
from logic.gutils import lobby_model_display_utils
import world
from logic.gcommon import time_utility
from logic.gcommon.item.item_const import BATTLE_EFFECT_KILL
from logic.gutils import red_point_utils
from common.cfg import confmgr
ROTATE_FACTOR = 850

class MiaomiaoFunctionWidget(object):

    def __init__(self, parent, panel):
        self.inited = False
        self.parent = parent
        self.panel = panel
        self.selected_item_no = None
        self.cur_show_model_item_no = None
        self.sel_before_cb = None
        self.sel_callback = None
        self.page_index = items_book_const.MIAOMIAO_ID
        self.is_enable = False
        self.init_widget()
        global_data.emgr.miaomiao_lobby_skin_change += self.on_lobby_skin_change
        return

    def set_switch_enable(self, val):
        self.is_enable = val
        if val:
            self.panel.img_item.setVisible(False)

    def is_panel_visible(self):
        ui_parent = global_data.ui_mgr.get_ui('ItemsBookMainUI')
        return ui_parent and ui_parent.panel.isVisible()

    def init_scene(self):
        if not self.is_panel_visible():
            return
        else:
            self.return_lobby_scene()
            global_data.emgr.clear_lobby_mecha_display_event.emit()
            global_data.emgr.change_model_display_scene_item.emit(None)
            global_data.emgr.move_camera_to_display_mecha_position_event.emit()
            self.panel.nd_touch.BindMethod('OnDrag', self._on_rotate_drag)
            return

    def _on_rotate_drag(self, layer, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_fixed_point_camera_event.emit(-delta_pos.x / ROTATE_FACTOR, 0)

    def return_lobby_scene(self):
        for i in range(len(global_data.ex_scene_mgr_agent.scene_stack)):
            global_data.emgr.leave_current_scene.emit()

        global_data.emgr.reset_rotate_model_display.emit()

    def init_widget(self):
        self._miaomiao_go_use_dismount_widget = MiaomiaoItemGoUseDismountWidget(self, self.panel.btn_go, self.panel.btn_use, self.panel.btn_dismount, self.panel.btn_preview, self.panel.temp_price)

    def on_lobby_skin_change(self, item_no=-1):
        if not self.is_enable:
            return
        if not self.is_panel_visible():
            return
        if item_no != self.selected_item_no:
            if self.parent:
                self.parent.sub_require_refresh_skin_list(self)

    def on_click_skin_item(self, index, item_no, *args):
        if not self.panel:
            return
        else:
            prev_index = self.selected_skin_idx
            self.selected_skin_idx = index
            item_widget = self.panel.list_item.GetItem(index)
            self.selected_item_no = item_no
            show_new = global_data.lobby_red_point_data.get_rp_by_no(item_no)
            self.panel.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
            self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
            self.panel.lab_get_method.SetString(item_utils.get_item_access(item_no))
            if show_new:
                global_data.player.req_del_item_redpoint(item_no)
                red_point_utils.show_red_point_template(item_widget.nd_new, False)
            global_data.emgr.select_item_goods.emit(item_no)
            prev_item = self.panel.list_item.GetItem(prev_index)
            if prev_item:
                prev_item.setLocalZOrder(0)
                prev_item.choose.setVisible(False)
            item_widget.setLocalZOrder(2)
            miaomiao_config = items_book_utils.get_items_conf(self.page_index)
            miaomiao_data = miaomiao_config.get(item_no, {})
            goods_id = miaomiao_data.get('goods_id', None)
            item_widget.choose.setVisible(True)
            self._miaomiao_go_use_dismount_widget.init_event()
            self._miaomiao_go_use_dismount_widget.update_target_item_no(self.selected_item_no, goods_id)
            show_pic_path = miaomiao_data.get('show_pic_path', None)
            global_data.emgr.miaomiao_lobby_skin_change.emit(item_no)
            if self.sel_callback:
                self.sel_callback()
            return

    def on_create_skin_item(self, lst, index, item_widget, skin_no):
        valid = skin_no
        if valid:
            item_widget.nd_content.setVisible(True)
            item_widget.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(skin_no))
            item_widget.lab_name.SetString(item_utils.get_lobby_item_name(skin_no))
            item_widget.choose.setVisible(False)
            cur_use_miaomiao_no = None
            if global_data.player:
                cur_use_miaomiao_no = global_data.player.get_lobby_skin()
            item_widget.img_using.setVisible(str(cur_use_miaomiao_no) == str(skin_no))
            item_can_use, limit_left_timestamp = mall_utils.item_can_use_by_item_no(skin_no)
            item_widget.nd_lock.setVisible(not item_can_use)
            item_utils.check_skin_tag(item_widget.nd_kind, skin_no)
            item_widget.bar.SetEnable(True)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
            red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
            template_utils.show_remain_time(item_widget.lab_limited, item_widget.lab_limited, skin_no)
            item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index, skin_no))
        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)
        if item_widget.nd_empty:
            item_widget.nd_empty.setVisible(not valid)
        return

    def do_hide_panel(self):
        global_data.emgr.miaomiao_lobby_skin_change.emit(-1)
        global_data.emgr.reset_lobby_camera_from_free.emit()
        global_data.emgr.lobby_mecha_display_reset.emit()
        self.panel.nd_touch.UnBindMethod('OnDrag')

    def destroy(self):
        self.do_hide_panel()
        self.inited = False
        self._miaomiao_go_use_dismount_widget.destroy()
        self._miaomiao_go_use_dismount_widget = None
        self.sel_before_cb = None
        self.sel_callback = None
        self.panel = None
        self.parent = None
        return

    @property
    def selected_skin_idx(self):
        return self.parent.selected_skin_idx

    @selected_skin_idx.setter
    def selected_skin_idx(self, val):
        self.parent.selected_skin_idx = val

    def set_select_callback(self, before_cb, cb):
        self.sel_before_cb = before_cb
        self.sel_callback = cb

    def on_clear_effect(self):
        self.do_hide_panel()

    def on_update_scene(self):
        self.init_scene()

    def get_def_select_item_no(self):
        if global_data.player:
            cur_use_miaomiao_no = global_data.player.get_lobby_skin()
            return cur_use_miaomiao_no
        else:
            return None