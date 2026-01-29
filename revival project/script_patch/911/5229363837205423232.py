# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/PickUIListView.py
from __future__ import absolute_import
import six

class CListViewMgr:
    UI_MAX_NUM = {'battle/i_pick_title': 10,'battle/i_item_empty': 5,
       'battle/i_item_4': 150
       }

    def __init__(self, ref_panel):
        self.ref_panel = ref_panel
        self.item_pool = {}
        self.item_conf = {}

    def on_destroy(self):
        for items in six.itervalues(self.item_pool):
            for item in items:
                item.release()

        self.item_pool = {}
        self.item_conf = {}

    def get_free_item(self, uiname, index=None, bRefresh=True):
        panel = self.ref_panel()
        if not panel:
            return
        listobj = panel.lv_pickable_list
        if uiname in self.item_pool and self.item_pool[uiname]:
            item_widget = self.item_pool[uiname].pop()
            listobj.AddControl(item_widget, index=index, bRefresh=bRefresh)
            item_widget.release()
            return item_widget
        if uiname not in self.item_conf:
            self.item_conf[uiname] = global_data.uisystem.load_template(uiname)
        item_widget = listobj.AddItem(self.item_conf[uiname], index=index, bRefresh=bRefresh)
        item_widget._pick_ui_name = uiname
        return item_widget

    def recycle_item(self):
        panel = self.ref_panel()
        if not panel:
            return
        listobj = panel.lv_pickable_list
        for item_widget in listobj.GetAllItem():
            if item_widget._pick_ui_name not in self.item_pool:
                self.item_pool[item_widget._pick_ui_name] = []
            if len(self.item_pool[item_widget._pick_ui_name]) < self.UI_MAX_NUM.get(item_widget._pick_ui_name, 50):
                item_widget.retain()
                item_widget.removeFromParent()
                self.item_pool[item_widget._pick_ui_name].append(item_widget)
            else:
                item_widget.Destroy()

        listobj.TransferAllSubItem()

    def auto_additem(self, s_next_index, data_list, data_count, add_msg_func, up_limit=100, down_limit=160):
        panel = self.ref_panel()
        if not panel:
            return s_next_index
        if not data_list:
            return s_next_index
        listobj = panel.lv_pickable_list
        s_count = listobj.GetItemCount()
        in_height = listobj.getInnerContainerSize().height
        out_height = listobj.getContentSize().height
        up_edge = out_height + up_limit
        down_edge = -down_limit
        pos_y = listobj.getInnerContainer().getPositionY()
        item = listobj.GetItem(0)
        if not item:
            first_item_height = 0
        else:
            first_item_height = listobj.GetItem(0).getContentSize().height
        top_y = pos_y + in_height - first_item_height
        down_y = pos_y
        if top_y + first_item_height < up_edge and s_next_index - s_count > 0:
            while top_y + first_item_height < up_edge and s_next_index - s_count > 0:
                old_y = listobj.getInnerContainer().getPositionY()
                data_index = s_next_index - 1 - s_count
                data = data_list[data_index]
                chat_pnl = add_msg_func(data, False)
                chat_pnl.data_index_tag = data_index
                height = chat_pnl.getContentSize().height
                listobj.getInnerContainer().setPositionY(old_y)
                top_y += height
                first_item_height = listobj.GetItem(0).getContentSize().height
                s_count += 1

        if down_y > down_edge and s_next_index < data_count:
            while down_y > down_edge and s_next_index < data_count:
                data_index = s_next_index
                old_y = listobj.getInnerContainer().getPositionY()
                data = data_list[data_index]
                chat_pnl = add_msg_func(data, True)
                chat_pnl.data_index_tag = data_index
                height = chat_pnl.getContentSize().height
                down_y -= height
                listobj._container._refreshItemPos()
                listobj._refreshItemPos()
                listobj.getInnerContainer().setPositionY(old_y - height)
                s_count += 1
                s_next_index += 1

        return s_next_index

    def get_list_position_y(self, data_list):
        panel = self.ref_panel()
        if not panel:
            return (None, 0, None)
        else:
            if not data_list:
                return (None, 0, None)
            listobj = panel.lv_pickable_list
            s_count = listobj.GetItemCount()
            if not s_count:
                return (None, 0, None)
            old_y = listobj.getInnerContainer().getPositionY()
            height = 0
            visible_end_index = 0
            data_index = 0
            in_height = listobj.getInnerContainerSize().height
            top_y = old_y + in_height
            view_h = listobj.GetContentSize()[1]
            while view_h < top_y:
                height = listobj.GetItem(visible_end_index).getContentSize().height
                top_y -= height
                visible_end_index += 1

            visible_end_y = top_y + height
            if visible_end_index:
                visible_end_index -= 1
                data_index = listobj.GetItem(visible_end_index).data_index_tag
            entity_id = None
            if len(data_list[data_index][-1]) > 1:
                entity_id = data_list[data_index][-1][0]
            return (entity_id, data_index, visible_end_y)

    def get_visible_end_data_index(self, entity_id, data_index, data_list):
        data_index = min(data_index, len(data_list) - 1)
        if entity_id is None:
            return data_index
        else:
            for i, data in enumerate(data_list):
                if len(data[-1]) > 1 and data[-1][0] == entity_id:
                    return i

            return data_index