# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/PersonalizationListWidget.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from logic.gutils import items_book_utils
from logic.gutils import item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.items_book_ui.ItemCategoryListWidget import ItemCategoryListWidget
from logic.comsys.items_book_ui.SkinItemListWidget import SkinItemListWidget
from logic.comsys.items_book_ui.ProjectionKillListWidget import ProjectionKillListWidget
from logic.client.const import items_book_const
from common.framework import Functor
from logic.gutils import red_point_utils
from logic.gcommon.item import lobby_item_type
from logic.gutils.mecha_skin_utils import get_mecha_skin_no_by_item_no
from logic.comsys.items_book_ui.InteractFunctionWidget import InteractFunctionWidget
from logic.comsys.items_book_ui.KillSfxFunctionWidget import KillSfxFunctionWidget
from logic.comsys.items_book_ui.ProjectionKillFunctionWidget import ProjectionKillFunctionWidget
from logic.comsys.items_book_ui.ItemsBookOwnBtnWidget import ItemsBookOwnBtnWidget
from logic.comsys.items_book_ui.MechaCallSfxListFunctionWidget import MechaCallsfxListFunctionWidget
from logic.comsys.items_book_ui.GlideEffectListFunctionWidget import GlideEffectListFunctionWidget
from logic.comsys.items_book_ui.GuangmuFunctionWidget import GuangmuFunctionWidget
OUTLINE_ICON_PATH = 'gui/ui_res_2/catalogue/outline/%s.png'
DRAG_DELTA = 0.05
DRAG_TAN = 1.303

class PersonalizationListWidget(object):

    def __init__(self, parent, panel):
        self.parent = parent
        self.panel = panel
        self.interaction_state = None
        self.selected_personal_type = None
        self.selected_item_index = None
        self.last_view_item_no = None
        self.data_list = None
        self._own_widget = ItemsBookOwnBtnWidget(self.panel.btn_tick, self.on_click_own_btn, need_cache=False)
        self.init_data()
        self.init_widget()
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'del_item_red_point_list': self.on_red_point_list_update
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_widget(self):
        self.interact_function_widget = None
        self.killsfx_function_widget = None
        self.callsfx_function_widget = None
        self.glide_effect_function_widget = None
        self.projection_kill_function_widget = None
        self.guangmu_widget = None
        self.sync_list_view = None
        self.panel.list_item.EnableItemAutoPool(True)
        self._interaction_list_widget = SkinItemListWidget(self, self.panel.list_item, self.on_create_interation_item, 3, self._on_select_equip_item)
        self._projection_kill_list_widget = ProjectionKillListWidget(self, self.panel.list_item_kill, self.on_create_projection_kill_item, 3, self._on_select_equip_item)
        self._guangmu_list_widget = SkinItemListWidget(self, self.panel.list_item_long, self.on_create_interation_item, 3, self._on_select_equip_item)
        self.init_sync_list()
        self._category_list_widget = ItemCategoryListWidget(self, self.panel.temp_right_tab, self.category_name_id_list, self.click_category_item_callback, items_book_const.PERSONALIZATION_ID, self.on_create_category_item, need_show_outline_pic=True)
        self._category_list_widget.init_widget()
        return

    def _on_select_equip_item(self, lst, index, item_widget):
        list_item = self.get_show_list()
        if not list_item.IsAsync():
            item_widget.bar.OnClick(item_widget.bar)
        elif index < list_item.GetItemCount():
            item_widget = list_item.GetItem(index)
            if not item_widget:
                item_widget = list_item.DoLoadItem(index)
            item_widget.bar.OnClick(item_widget.bar)

    def destroy(self):
        if self.selected_personal_type != 'all_type':
            widget = self.get_type_widget(self.selected_personal_type)
            widget and widget.on_clear_effect()
        if self.on_select_item_before_callback:
            prev_index = self.selected_item_index
            self.on_select_item_before_callback(prev_index, None)
        if self._category_list_widget:
            self._category_list_widget.destroy()
            self._category_list_widget = None
        if self._interaction_list_widget:
            self._interaction_list_widget.destroy()
            self._interaction_list_widget = None
        if self._guangmu_list_widget:
            self._guangmu_list_widget.destroy()
            self._guangmu_list_widget = None
        if self.sync_list_view:
            self.sync_list_view.destroy()
            self.sync_list_view = None
        if self._projection_kill_list_widget:
            self._projection_kill_list_widget.destroy()
            self._projection_kill_list_widget = None
        if self.interact_function_widget:
            self.interact_function_widget.destroy()
            self.interact_function_widget = None
        if self.killsfx_function_widget:
            self.killsfx_function_widget.destroy()
            self.killsfx_function_widget = None
        if self.projection_kill_function_widget:
            self.projection_kill_function_widget.destroy()
            self.projection_kill_function_widget = None
        if self.callsfx_function_widget:
            self.callsfx_function_widget.destroy()
            self.callsfx_function_widget = None
        if self.glide_effect_function_widget:
            self.glide_effect_function_widget.destroy()
            self.glide_effect_function_widget = None
        if self.guangmu_widget:
            self.guangmu_widget.destroy()
            self.guangmu_widget = None
        if self._own_widget:
            self._own_widget.destroy()
            self._own_widget = None
        self.panel = None
        self.parent = None
        self.data_dict = None
        self.process_event(False)
        return

    def init_data(self):
        self.data_dict = {}
        self.category_name_id_list = [
         (
          lobby_item_type.L_ITEM_TYPE_GUANGMU, 860448),
         (
          lobby_item_type.L_ITEM_TYPE_GESTURE, 81235),
         (
          lobby_item_type.L_ITEM_TYPE_MECHA_GESTURE, 860398),
         (
          lobby_item_type.L_ITEM_TYPE_SPRAY, 81233),
         (
          lobby_item_type.L_ITEM_TYPE_EMOTICON, 81234),
         (
          lobby_item_type.L_ITEM_KILL_SFX, 81402),
         (
          lobby_item_type.L_ITEM_MECHA_SFX, 634006),
         (
          lobby_item_type.L_ITEM_GLIDE_EFFECT, 634700),
         (
          lobby_item_type.L_ITEM_TYPE_PROJECTION_KILL, 83416)]
        self.empty_text_id_dict = {lobby_item_type.L_ITEM_TYPE_GESTURE: 81264,
           lobby_item_type.L_ITEM_TYPE_MECHA_GESTURE: 860399,
           lobby_item_type.L_ITEM_TYPE_PROJECTION_KILL: 83447,
           lobby_item_type.L_ITEM_TYPE_GUANGMU: 633894
           }
        self.show_interact_list = [
         lobby_item_type.L_ITEM_TYPE_GESTURE,
         lobby_item_type.L_ITEM_TYPE_MECHA_GESTURE,
         lobby_item_type.L_ITEM_TYPE_SPRAY,
         lobby_item_type.L_ITEM_TYPE_EMOTICON]
        self.show_nd_callsfx_list = [
         lobby_item_type.L_ITEM_MECHA_SFX,
         lobby_item_type.L_ITEM_GLIDE_EFFECT]
        self.show_nd_killsfx_list = [
         lobby_item_type.L_ITEM_KILL_SFX,
         lobby_item_type.L_ITEM_TYPE_PROJECTION_KILL]
        self.list_item_kill_show_list = [
         lobby_item_type.L_ITEM_TYPE_PROJECTION_KILL]
        self.list_item_sync_show_list = [
         lobby_item_type.L_ITEM_GLIDE_EFFECT]
        self.category_icon_list = [
         'img_guangmu',
         'icon_action',
         'img_mecha',
         'icon_graffiti',
         'icon_emoji',
         'icon_effect_kill',
         'icon_effect_entrance',
         '2081668',
         'icon_projection_kill']
        self.degree_dict = {}
        self.item_type_table_list = [
         lobby_item_type.L_ITEM_TYPE_GESTURE,
         lobby_item_type.L_ITEM_TYPE_MECHA_GESTURE,
         lobby_item_type.L_ITEM_TYPE_SPRAY,
         lobby_item_type.L_ITEM_TYPE_EMOTICON,
         lobby_item_type.L_ITEM_KILL_SFX,
         lobby_item_type.L_ITEM_GLIDE_EFFECT]
        self.type_dict = {}
        self.data_list = []
        for idx in range(len(self.category_name_id_list)):
            item_config_name = self.category_name_id_list[idx][0]
            if item_config_name == 'all_type':
                continue
            item_no_dict = items_book_utils.get_interaction_item_info(None, item_config_name)
            key = self.category_name_id_list[idx][0]
            item_no_dict = self.get_show_item_no_dict(item_no_dict)
            self.type_dict[key] = item_no_dict
            self.data_dict.update(item_no_dict)

        return

    def get_show_item_no_dict(self, item_no_dict):
        ret_dict = {}
        for item_no, data in six.iteritems(item_no_dict):
            if not item_utils.can_open_show(item_no, owned_should_show=True):
                continue
            ret_dict[item_no] = data

        return ret_dict

    def on_click_own_btn(self, *args):
        self.refresh_show_list()

    def on_create_category_item(self, lst, index, item_widget):
        if not self.panel:
            return
        item_widget.btn.EnableCustomState(True)
        item_widget.btn.SetText(get_text_by_id(self.category_name_id_list[index][1]))
        icon_path = OUTLINE_ICON_PATH % self.category_icon_list[index]
        item_widget.btn.icon.SetDisplayFrameByPath('', icon_path)
        item_widget.btn.icon_sel.SetDisplayFrameByPath('', icon_path)
        item_widget.btn.icon.setVisible(True)
        item_widget.btn.icon_sel.setVisible(False)
        item_widget.btn.SetSelect(False)
        show_new = global_data.lobby_red_point_data.get_rp_by_type(self.category_name_id_list[index][0])
        red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
        item_widget.btn.BindMethod('OnClick', Functor(self._category_list_widget.on_click_category_item, index))

    def on_create_interation_item(self, lst, index, item_widget):
        valid = index < len(self.data_list) and self.data_list[index] is not None
        if valid:
            item_no = self.data_list[index]
            item_type = item_utils.get_lobby_item_type(item_no)
            widget = self.get_type_widget(item_type)
            if widget:
                widget.on_create_skin_item(lst, index, item_widget)
        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.img_level.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)
            if self.selected_personal_type != 'all_type':
                widget = self.get_type_widget(self.selected_personal_type)
                if widget:
                    widget.on_create_empty_skin_item(lst, index, item_widget)
        item_widget.nd_empty and item_widget.nd_empty.setVisible(not valid)
        return

    def on_remove_interation_item(self, lst, index, item_widget):
        if index < len(self.data_list):
            if self.selected_personal_type != 'all_type':
                widget = self.get_type_widget(self.selected_personal_type)
                if widget:
                    widget.on_remove_skin_item(lst, index, item_widget)

    def on_create_projection_kill_item(self, lst, index, item_widget):
        valid = index < len(self.data_list) and self.data_list[index] is not None
        if valid:
            item_no = self.data_list[index]
            item_type = item_utils.get_lobby_item_type(item_no)
            if item_type == lobby_item_type.L_ITEM_TYPE_PROJECTION_KILL:
                self.projection_kill_function_widget.on_create_skin_item(lst, index, item_widget)
        item_widget.setVisible(valid)
        return

    def click_category_item_callback(self, index, data):
        is_same_item = self.selected_personal_type == data[0]
        if not is_same_item:
            if self.on_select_item_before_callback:
                prev_index = self.selected_item_index
                self.on_select_item_before_callback(prev_index, None)
        old_selected_personal_type = self.selected_personal_type
        if old_selected_personal_type is not None:
            widget = self.get_type_widget_with_init(old_selected_personal_type)
            if widget:
                widget.on_clear_effect()
                if hasattr(widget, 'on_leave_page'):
                    widget.on_leave_page()
        self.selected_personal_type = data[0]
        widget = self.get_type_widget_with_init(self.selected_personal_type)
        if widget:
            widget.on_update_scene()
        if self.selected_personal_type != lobby_item_type.L_ITEM_KILL_SFX:
            if self.selected_personal_type not in [lobby_item_type.L_ITEM_TYPE_EMOTICON, 'all_type']:
                self.interact_function_widget and self.interact_function_widget.switch_auto_mode(False)
            else:
                self.interact_function_widget and self.interact_function_widget.switch_auto_mode(True)
        self.panel.nd_interact.setVisible(self.selected_personal_type in self.show_interact_list)
        is_guangmu = self.selected_personal_type == lobby_item_type.L_ITEM_TYPE_GUANGMU
        self.panel.nd_guangmu.setVisible(is_guangmu)
        self.panel.nd_guangmu_bg.setVisible(is_guangmu)
        self.panel.list_item.setVisible(self.selected_personal_type not in self.list_item_sync_show_list and self.selected_personal_type not in self.list_item_kill_show_list and not is_guangmu)
        self.panel.list_item_sync.setVisible(self.selected_personal_type in self.list_item_sync_show_list)
        self.panel.list_item_kill.setVisible(self.selected_personal_type in self.list_item_kill_show_list)
        self.panel.list_item_long.setVisible(is_guangmu)
        if is_guangmu:
            size = self.panel.nd_skin.GetContentSize()
            self.panel.nd_skin.SetContentSize(210, size[1])
            self.panel.nd_skin.ChildResizeAndPosition()
        else:
            self.panel.nd_skin.ResizeAndPosition()
        list_item_list = [
         self.panel.list_item, self.panel.list_item_sync, self.panel.list_item_kill, self.panel.list_item_long]
        for i in range(len(list_item_list)):
            if self.get_show_list() != list_item_list[i]:
                list_item_list[i].SetInitCount(0)

        self.panel.nd_callsfx.setVisible(self.selected_personal_type in self.show_nd_callsfx_list)
        self.panel.nd_killsfx.setVisible(self.selected_personal_type in self.show_nd_killsfx_list)
        select_idx = is_same_item or 0 if 1 else self.selected_item_index
        self.refresh_show_list(is_same_item, select_idx)
        return

    def refresh_show_list(self, is_same_item=True, select_idx=0, sel_item_no=None):
        own_func = self._own_widget.has_item

        def sort_key_func(x):
            return [
             own_func(x) if x else 0, item_utils.get_item_rare_degree(x) if x else 0, x]

        _list_item = self.get_show_list()
        count_per_row = _list_item.GetNumPerUnit()
        check_has_own = self._own_widget.get_own_switch()
        own_count = 0
        all_count = 0
        if self.selected_personal_type == 'all_type':
            all_selected_type_list = []
            all_type_display_order = self.item_type_table_list
            for _type in all_type_display_order:
                type_dict = self.type_dict[_type]
                selected_type_list = six_ex.keys(type_dict)
                all_count += len(selected_type_list)
                if check_has_own:
                    selected_type_list = [ i for i in selected_type_list if own_func(i) ]
                    own_count += len(selected_type_list)
                else:
                    own_count += len([ i for i in selected_type_list if own_func(i) ])
                selected_type_list = sorted(selected_type_list, key=sort_key_func, reverse=True)
                remain = len(selected_type_list) % count_per_row
                if remain > 0:
                    round_count = count_per_row - remain
                    for i in range(round_count):
                        selected_type_list.append(None)

                all_selected_type_list.extend(selected_type_list)

        else:
            selected_dict = self.type_dict[self.selected_personal_type]
            selected_type_list = six_ex.keys(selected_dict)
            all_count += len(selected_type_list)
            if check_has_own:
                selected_type_list = [ i for i in selected_type_list if own_func(i) ]
                own_count += len(selected_type_list)
            else:
                own_count += len([ i for i in selected_type_list if own_func(i) ])
            widget = self.get_type_widget(self.selected_personal_type)
            if widget and hasattr(widget, 'preprocess_data'):
                all_selected_type_list = widget.preprocess_data(selected_type_list, own_func)
            else:
                all_selected_type_list = sorted(selected_type_list, key=lambda x: sort_key_func(x), reverse=True)
        self.data_list = all_selected_type_list
        is_empty = not bool(self.data_list)
        self.panel.nd_empty.setVisible(is_empty)
        self.panel.nd_skin.nd_empty.setVisible(is_empty)
        if is_empty:
            self.panel.nd_empty.lab_empty.setString(get_text_by_id(self.empty_text_id_dict[self.selected_personal_type]))
        if not self.data_list:
            if self.selected_personal_type in self.show_interact_list:
                self.interact_function_widget and self.interact_function_widget.on_data_empty()
            elif self.selected_personal_type in self.show_nd_callsfx_list:
                self.panel.nd_callsfx.setVisible(False)
            elif self.selected_personal_type in self.show_nd_killsfx_list:
                self.panel.nd_killsfx.setVisible(False)
            self.panel.nd_guangmu.setVisible(False)
            self.panel.nd_item_describe.setVisible(False)
            if self.selected_personal_type in self.list_item_kill_show_list:
                self.projection_kill_function_widget.on_clear_effect()
                self.projection_kill_function_widget.on_update_scene()
            elif self.selected_personal_type in self.list_item_sync_show_list:
                pass
        else:
            if self.selected_personal_type in self.show_interact_list:
                self.interact_function_widget and self.interact_function_widget.on_data_exist()
            elif self.selected_personal_type == lobby_item_type.L_ITEM_TYPE_GUANGMU:
                self.panel.nd_guangmu.setVisible(True)
            self.panel.nd_item_describe.setVisible(True)
        if sel_item_no is not None:
            if sel_item_no in self.data_list:
                select_idx = self.data_list.index(sel_item_no)
        else:
            widget = self.get_type_widget_with_init(self.selected_personal_type)
            if self.selected_personal_type == lobby_item_type.L_ITEM_GLIDE_EFFECT:
                widget.set_data(self.data_list, self.data_dict, own_func)
            else:
                widget.set_data(self.data_list, self.data_dict)
            if widget:
                sel_item_no = widget.get_default_select_item_no()
                if sel_item_no in self.data_list:
                    select_idx = self.data_list.index(sel_item_no)
        self.update_skin_data(self.data_list, not is_same_item, select_idx)
        self.update_select_item_collect_count(own_count, all_count)
        return

    def update_skin_list(self, is_init, select_index):
        self.update_skin_data(self.data_list, True, select_index)

    def update_skin_data(self, skins_list, is_init, select_index):
        if self.selected_personal_type in self.list_item_sync_show_list:
            self.sync_list_view.update_data_list(self.data_list)

            def refresh_func(ui_item, data, index):
                self.on_create_interation_item(self.panel.list_item_sync, index, ui_item)

            self.sync_list_view.refresh_showed_item(refresh_func=refresh_func)
            self.sync_list_view.update_scroll_view()
            self.sync_list_view.top_with_index(select_index, None)
            if select_index is not None and select_index >= 0:
                item_widget = self.sync_list_view.get_list_item(select_index)
                if item_widget:
                    item_widget.bar.OnClick(item_widget.bar)
        elif self.selected_personal_type in self.list_item_kill_show_list:
            if select_index is not None and select_index >= 0:
                self._projection_kill_list_widget.update_skin_data(self.data_list, True, select_index)
        elif self.selected_personal_type == lobby_item_type.L_ITEM_TYPE_GUANGMU:
            if select_index is not None and select_index >= 0:
                self._guangmu_list_widget.update_skin_data(self.data_list, True, select_index)
        elif select_index is not None and select_index >= 0:
            self._interaction_list_widget.update_skin_data(self.data_list, True, select_index)
        return

    def update_select_item_collect_count(self, own_count, all_count):
        self.panel.temp_prog.lab_got.SetString(str(own_count) + '/' + str(all_count))
        self.panel.temp_prog.prog.SetPercentage(int(own_count / float(all_count) * 100) if all_count > 0 else 0)
        self.panel.lab_collect.SetString(str(own_count) + '/' + str(all_count))

    def jump_to_item_no(self, item_no):
        if item_no is None:
            return
        else:
            cat_idx = self._get_category_idx_by_item_no(item_no)
            if cat_idx is None:
                return
            self._category_list_widget.click_item(cat_idx)
            idx_in_cat = self._get_idx_in_cat_by_item_no(item_no)
            if idx_in_cat is None:
                return
            if self.selected_personal_type == lobby_item_type.L_ITEM_TYPE_GUANGMU:
                self._guangmu_list_widget.click_item(idx_in_cat)
            elif self.selected_personal_type not in self.list_item_sync_show_list:
                self._interaction_list_widget.click_item(idx_in_cat)
            else:
                self.sync_list_view.top_with_index(idx_in_cat, None)
                select_index = idx_in_cat
                if select_index is not None and select_index >= 0:
                    item_widget = self.sync_list_view.get_list_item(select_index)
                    if item_widget:
                        item_widget.bar.OnClick(item_widget.bar)
            return

    def _get_category_idx_by_item_no(self, item_no):
        cat_id = self._get_category_id_by_item_no(item_no)
        if cat_id is None:
            return
        else:
            for idx, cat_info in enumerate(self.category_name_id_list):
                if cat_info[0] == cat_id:
                    return idx

            return

    def _get_category_id_by_item_no(self, item_no):
        for cat_name, item_info_dict in six.iteritems(self.type_dict):
            if item_info_dict.get(str(item_no)) is not None:
                return cat_name

        return

    def _get_idx_in_cat_by_item_no(self, item_no):
        try:
            return self.data_list.index(str(item_no))
        except:
            pass

        return None

    def on_select_item_callback(self, *args):
        index = self.selected_item_index
        if index is None:
            return
        else:
            valid = index < len(self.data_list) and self.data_list[index] is not None
            if valid:
                item_no = self.data_list[index]
                item_type = item_utils.get_lobby_item_type(item_no)
                self.panel.nd_interact.setVisible(item_type in self.show_interact_list)
                self.panel.nd_callsfx.setVisible(item_type in self.show_nd_callsfx_list)
                self.panel.nd_killsfx.setVisible(item_type in self.show_nd_killsfx_list)
            return

    def on_select_item_before_callback(self, prev_idx, idx):
        old_item_type = None
        if prev_idx is not None and prev_idx < len(self.data_list):
            old_item_no = self.data_list[prev_idx]
            if old_item_no:
                old_item_type = item_utils.get_lobby_item_type(old_item_no)
            _list_item = self.get_show_list()
            prev_item = _list_item.GetItem(prev_idx)
            if prev_item:
                prev_item.setLocalZOrder(0)
                prev_item.choose.setVisible(False)
        self.selected_item_index = idx
        if idx is not None and idx < len(self.data_list):
            self.last_view_item_no = self.data_list[idx]
        _list_item = self.get_show_list()
        item_widget = _list_item.GetItem(idx)
        if item_widget:
            item_widget.setLocalZOrder(2)
            item_widget.choose.setVisible(True)
        return

    def set_last_view_item_no(self, item_no):
        self.last_view_item_no = item_no

    def on_change_interaction_data(self, role_id):
        self.interact_function_widget and self.interact_function_widget.update_role_data(data_changed=True)
        self.refresh_show_list(select_idx=self.selected_item_index, sel_item_no=self.last_view_item_no)

    def sub_require_refresh_skin_list(self, widget):
        if not (self.panel and self.panel.isValid()):
            return
        if widget not in self.get_in_effect_widgets():
            return
        self.update_skin_data(self.data_list, False, self.selected_item_index)

    def get_in_effect_widgets(self, target_type=None):
        if target_type is None:
            target_type = self.selected_personal_type
        if target_type == 'all_type':
            return [self.interact_function_widget, self.killsfx_function_widget]
        else:
            return [
             self.get_type_widget(target_type)]
            return

    def get_type_widget(self, target_type=None):
        dic = {lobby_item_type.L_ITEM_KILL_SFX: self.killsfx_function_widget,
           lobby_item_type.L_ITEM_MECHA_SFX: self.callsfx_function_widget,
           lobby_item_type.L_ITEM_TYPE_EMOTICON: self.interact_function_widget,
           lobby_item_type.L_ITEM_TYPE_SPRAY: self.interact_function_widget,
           lobby_item_type.L_ITEM_TYPE_GESTURE: self.interact_function_widget,
           lobby_item_type.L_ITEM_TYPE_MECHA_GESTURE: self.interact_function_widget,
           lobby_item_type.L_ITEM_GLIDE_EFFECT: self.glide_effect_function_widget,
           lobby_item_type.L_ITEM_TYPE_PROJECTION_KILL: self.projection_kill_function_widget,
           lobby_item_type.L_ITEM_TYPE_GUANGMU: self.guangmu_widget
           }
        return dic.get(target_type)

    def get_type_widget_with_init(self, target_type=None):
        widget = self.get_type_widget(target_type)
        if widget is not None:
            return widget
        else:
            if target_type == lobby_item_type.L_ITEM_KILL_SFX:
                self.killsfx_function_widget = KillSfxFunctionWidget(self, self.panel)
                self.killsfx_function_widget.set_select_callback(self.on_select_item_before_callback, self.on_select_item_callback)
            elif target_type == lobby_item_type.L_ITEM_MECHA_SFX:
                self.callsfx_function_widget = MechaCallsfxListFunctionWidget(self, self.panel)
                self.callsfx_function_widget.set_select_callback(self.on_select_item_before_callback, self.on_select_item_callback)
            elif target_type in [lobby_item_type.L_ITEM_TYPE_EMOTICON, lobby_item_type.L_ITEM_TYPE_SPRAY, lobby_item_type.L_ITEM_TYPE_GESTURE, lobby_item_type.L_ITEM_TYPE_MECHA_GESTURE]:
                self.interact_function_widget = InteractFunctionWidget(self, self.panel)
                self.interact_function_widget.set_select_callback(self.on_select_item_before_callback, self.on_select_item_callback)
                self.interact_function_widget.update_role_data()
            elif target_type == lobby_item_type.L_ITEM_GLIDE_EFFECT:
                self.glide_effect_function_widget = GlideEffectListFunctionWidget(self, self.panel)
                self.glide_effect_function_widget.set_select_callback(self.on_select_item_before_callback, self.on_select_item_callback)
            elif target_type == lobby_item_type.L_ITEM_TYPE_PROJECTION_KILL:
                self.projection_kill_function_widget = ProjectionKillFunctionWidget(self, self.panel)
                self.projection_kill_function_widget.set_select_callback(self.on_select_item_before_callback, self.on_select_item_callback)
            elif target_type == lobby_item_type.L_ITEM_TYPE_GUANGMU:
                self.guangmu_widget = GuangmuFunctionWidget(self, self.panel)
                self.guangmu_widget.set_select_callback(self.on_select_item_before_callback, self.on_select_item_callback)
            widget = self.get_type_widget(target_type)
            return widget

    def refresh_widget(self):
        if self.selected_item_index is None:
            return
        else:
            select_idx = self.selected_item_index
            self.refresh_show_list(True, select_idx or 0)
            self._category_list_widget.refresh_widget(self.category_name_id_list)
            return

    def do_hide_panel(self):
        self.panel.StopTimerAction()
        self.guangmu_widget.on_clear_effect()

    def init_sync_list(self):
        from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
        self.sync_list_view = InfiniteScrollWidget(self.panel.list_item_sync, self.panel)
        self.sync_list_view.set_custom_add_item_func(self.add_scroll_elem)
        self.sync_list_view.set_custom_del_item_func(self.on_remove_scroll_item)
        self.sync_list_view.enable_item_auto_pool(True)

    def add_scroll_elem(self, data, is_back_item=True, index=-1):
        if is_back_item:
            panel = self.panel.list_item_sync.AddTemplateItem(bRefresh=False)
        else:
            panel = self.panel.list_item_sync.AddTemplateItem(0, bRefresh=False)
        self.on_create_interation_item(self.panel.list_item_sync, index, panel)

    def on_remove_scroll_item(self, ui_item, index):
        if ui_item and ui_item.isValid():
            self.on_remove_interation_item(self.panel.list_item_sync, index, ui_item)

    def get_show_list(self):
        if self.selected_personal_type in self.list_item_sync_show_list:
            return self.panel.list_item_sync
        else:
            if self.selected_personal_type in self.list_item_kill_show_list:
                return self.panel.list_item_kill
            if self.selected_personal_type == lobby_item_type.L_ITEM_TYPE_GUANGMU:
                return self.panel.list_item_long
            return self.panel.list_item

    def on_red_point_list_update(self, *args):
        list_right = self.panel.temp_right_tab.list_right
        all_tab_items = list_right.GetAllItem()
        for index, tab_widget in enumerate(all_tab_items):
            red_point_utils.show_red_point_template(tab_widget.nd_new, False)

        list_item = self.get_show_list()
        for index in range(len(self.data_list)):
            item_widget = list_item.GetItem(index)
            if item_widget:
                red_point_utils.show_red_point_template(item_widget.nd_new, False)