# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/BagHumanItemWidget.py
from __future__ import absolute_import
import six
from logic.gutils import item_utils
from logic.gutils import template_utils
from logic.gcommon.item.backpack_item_type import B_ITEM_TYPE_BACK_HOME_ID
import cc

class BagHumanItemWidget(object):

    def __init__(self, nd_item, method_dict):
        self.init_parameters(nd_item)
        self.init_methods(method_dict)
        self.init_extra_part()
        self.init_widget()

    def init_parameters(self, nd_item):
        self._nd_item = nd_item
        self._nd_item_list = nd_item.item_bag.item_list
        self._nd_empty = nd_item.item_bag.img_empty_bag

    def init_methods(self, method_dict):
        self._on_item_click = method_dict.get('item_click', None)
        self._on_item_drag = method_dict.get('item_drag', None)
        self._on_item_end = method_dict.get('item_end', None)
        return

    def init_extra_part(self):
        pass

    def init_widget(self):
        item_list = self.get_human_item_list()
        count = len(item_list)
        self._nd_item_list.DeleteAllSubItem()
        self._nd_item_list._container._refreshItemPos()
        self._nd_item_list._refreshItemPos()
        self._nd_item_list.SetInitCount(count)
        item_ui_list = self._nd_item_list.GetAllItem()
        item_list = sorted(item_list, key=--- This code section failed: ---

  39       0  LOAD_GLOBAL           0  'item_utils'
           3  LOAD_ATTR             1  'item_sort_key'
           6  LOAD_ATTR             1  'item_sort_key'
           9  BINARY_SUBSCR    
          10  CALL_FUNCTION_1       1 
          13  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `BINARY_SUBSCR' instruction at offset 9
, reverse=True)
        for idx, item in enumerate(item_list):
            eid, item_data = item
            item_ui = item_ui_list[idx]
            self.init_human_item(item_ui, item_data)

        self._nd_item_list.setVisible(True)
        self._nd_empty.setVisible(count == 0)

    def init_human_item(self, item_ui, item_data):
        item_ui.btn_bar.SetSwallowTouch(False)
        item_ui.btn_bar.SetNoEventAfterMove(False, '5w')
        icon_path = 'gui/ui_res_2/battle/panel/pnl_item_nml.png' if item_data else 'gui/ui_res_2/battle/panel/pnl_item_empty.png'
        item_ui.btn_bar.SetFrames('', [icon_path, icon_path], False, None)
        template_utils.init_item4_new(item_ui, item_data, is_show_max_count=True)
        item_ui.btn_recourse_mark.setVisible(False)

        @item_ui.btn_bar.unique_callback()
        def OnClick(btn, touch):
            self._on_item_click(btn, touch, item_data)

        @item_ui.btn_bar.unique_callback()
        def OnDrag(btn, touch):
            item_ui.btn_bar.SetSwallowTouch(True)
            self._on_item_drag(btn, touch, item_data)

        @item_ui.btn_bar.unique_callback()
        def OnEnd(btn, touch):
            item_ui.btn_bar.SetSwallowTouch(False)
            self._on_item_end(btn, touch, item_data)

        return

    def get_human_item_list(self):
        from logic.gutils.new_template_utils import is_mecha_related_item
        if not global_data.player or not global_data.player.logic:
            return []
        item_dict = global_data.player.logic.ev_g_others()
        if not item_dict:
            return []
        item_list = []
        for eid, item_data in six.iteritems(item_dict):
            item_id = item_data.get('item_id')
            if not is_mecha_related_item(item_id) and item_id != B_ITEM_TYPE_BACK_HOME_ID:
                item_list.append((eid, item_data))

        return item_list

    def resize_height_by_item_cnt(self, delta_h):
        bag = self._nd_item
        bag_bg = bag.bag_bg
        item_bag = bag.item_bag
        item_list = item_bag.item_list
        bag_region = item_bag.bag_region
        title_bar = bag.title_bar
        nd_slider = bag.nd_slider
        slider_bg = nd_slider.slider_bg
        ui_list = [
         bag_bg, item_list, bag_region, nd_slider, slider_bg, bag]
        for ui_item in ui_list:
            scale_y = ui_item.getScaleY()
            if scale_y <= 0:
                scale_y = 1 if 1 else scale_y
                ui_item.SetContentSize(ui_item.GetContentSize()[0], ui_item.GetContentSize()[1] - delta_h / scale_y)

        title_bar.SetPosition(title_bar.GetPosition()[0], title_bar.GetPosition()[1] - delta_h)

    def destroy(self):
        self._nd_item = None
        self._nd_item_list = None
        self._nd_empty = None
        return


class BagHumanItemMobileWidget(BagHumanItemWidget):

    def init_parameters(self, nd_item):
        self._nd_item = nd_item
        self._nd_item_list = nd_item.item_bag.item_list
        self._nd_empty = nd_item.empty_human
        nd_item.item_bag.setVisible(True)

    def init_methods(self, method_dict):
        super(BagHumanItemMobileWidget, self).init_methods(method_dict)
        self._on_item_double_click = method_dict.get('item_double_click', None)
        self._on_btn_use_click = method_dict.get('btn_use_click', None)
        self._on_btn_discard_click = method_dict.get('btn_discard_click', None)
        return

    def init_extra_part(self):
        self.item_use_temp = global_data.uisystem.load_template('battle_bag/i_bag_function')
        ctrl_sz = self._nd_item_list.GetCtrlSize()
        self.package_item_size = (ctrl_sz.width, ctrl_sz.height)
        self.package_item_choose_size = (self.package_item_size[0], self.package_item_size[1] + 50)

    def init_human_item(self, item_ui, item_data):
        if not item_ui.extra_part:
            extra = global_data.uisystem.create_item(self.item_use_temp, parent=item_ui)
            extra.setPosition(cc.Vec2(0, 0))
            setattr(item_ui, 'extra_part', extra)
        item_ui.extra_part.setVisible(False)
        item_no = item_data.get('item_id') if item_data else 0
        item_ui.btn_bar.EnableDoubleClick(True)
        item_ui.extra_part.btn_discard.SetEnable(self.check_can_discard(item_no))
        super(BagHumanItemMobileWidget, self).init_human_item(item_ui, item_data)

        @item_ui.btn_bar.unique_callback()
        def OnBegin(btn, touch, data=item_data):
            return data is not None

        @item_ui.btn_bar.unique_callback()
        def OnDoubleClick(btn, last_pos, cur_pos, data=item_data):
            self._on_item_double_click(btn, last_pos, cur_pos, data)

        @item_ui.extra_part.btn_use.unique_callback()
        def OnClick(btn, touch, data=item_data):
            self._on_btn_use_click(btn, touch, data)

        @item_ui.extra_part.btn_discard.unique_callback()
        def OnClick(btn, touch, data=item_data):
            self._on_btn_discard_click(btn, touch, data)

    def check_can_discard(self, item_no):
        if item_utils.is_bullet(item_no):
            return False
        return True

    def resize_height_by_item_cnt(self, delta_h):
        bag = self._nd_item
        bag_bg = bag.human_bg
        item_bag = bag.item_bag
        item_list = item_bag.item_list
        bag_region = item_bag.bag_region
        title_bar = bag.title_bar
        ui_list = [
         bag_bg, item_list, bag_region, bag]
        for ui_item in ui_list:
            scale_y = ui_item.getScaleY()
            if scale_y <= 0:
                scale_y = 1 if 1 else scale_y
                ui_item.SetContentSize(ui_item.GetContentSize()[0], ui_item.GetContentSize()[1] - delta_h / scale_y)

        title_bar.SetPosition(title_bar.GetPosition()[0], title_bar.GetPosition()[1] - delta_h)

    def process_extra_part(self, last_item_ui, item_ui):
        if last_item_ui and last_item_ui.isValid():
            extra_part = getattr(last_item_ui, 'extra_part')
            if extra_part and extra_part.isValid():
                last_item_ui.extra_part.setVisible(False)
                last_item_ui.SetContentSize(self.package_item_size[0], self.package_item_size[1])
                offset = self.package_item_size[1] - self.package_item_choose_size[1]
                for child in last_item_ui.getChildren():
                    if child and child.isValid():
                        pos = child.getPosition()
                        child.setPosition(cc.Vec2(pos.x, pos.y + offset))

        if item_ui and item_ui.isValid():
            extra_part = getattr(item_ui, 'extra_part')
            if extra_part and extra_part.isValid():
                item_ui.extra_part.setVisible(True)
                item_ui.SetContentSize(self.package_item_choose_size[0], self.package_item_choose_size[1])
                offset = self.package_item_choose_size[1] - self.package_item_size[1]
                for child in item_ui.getChildren():
                    if child and child.isValid():
                        pos = child.getPosition()
                        child.setPosition(cc.Vec2(pos.x, pos.y + offset))

        self._nd_item_list._container._refreshItemPos()
        self._nd_item_list._refreshItemPos()

    def on_extra_part_btn_change(self, lplayer, item_ui, item_data):
        if item_ui and item_ui.isValid() and item_data:
            extra_part = getattr(item_ui, 'extra_part')
            if extra_part and extra_part.isValid():
                btn_use = getattr(extra_part, 'btn_use')
                if btn_use and btn_use.isValid():
                    item_ui.extra_part.btn_use.EnableCustomState(not item_utils.check_can_use(lplayer, item_data))
                    item_ui.extra_part.btn_use.SetShowEnable(item_utils.check_can_use(lplayer, item_data))

    def refresh_item_list_postion(self):
        self._nd_item_list._container._refreshItemPos()
        self._nd_item_list._refreshItemPos()