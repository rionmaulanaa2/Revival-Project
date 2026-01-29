# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/InteractionListWidgetBase.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from functools import cmp_to_key
from logic.gutils import mall_utils
from logic.gutils import items_book_utils
from logic.gutils import item_utils
from logic.comsys.items_book_ui.SkinItemListWidget import SkinItemListWidget
from logic.comsys.items_book_ui.RoleItemSelectWidget import RoleItemSelectWidget
from logic.comsys.items_book_ui.RoundSelectWidget import RoundSelectWidget
from logic.comsys.items_book_ui.ListSelectWidget import ListSelectWidget
from logic.client.const import items_book_const
from common.framework import Functor
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.comsys.items_book_ui.InteractionGetUseBuyWidget import InteractionGetUseBuyWidget
from logic.comsys.items_book_ui.ItemFilterWidget import ItemFilterWidget
from logic.gcommon.item import lobby_item_type
from logic.gutils import red_point_utils
DRAG_DELTA = 0.05
DRAG_TAN = 1.303

class InteractionListWidgetBase(object):
    TAB_INDEX = items_book_const.SPRAY_ID
    TAB_ITEM_TYPE = lobby_item_type.L_ITEM_TYPE_SPRAY
    DEFAULT_FILTER_STR_ID = 608138
    PATTERN_FILTER_STR_ID = 81364

    def __init__(self, parent, panel):
        self.selected_item_index = None
        self.role_interaction_info = None
        self._list_select_widget = None
        self.inited = False
        self.is_auto_mode = False
        self.parent = parent
        self.panel = panel
        self.selected_role_id = self.get_parent_select_role()
        self.interaction_state = self.get_parent_interaction_state() or items_book_const.INTERACTION_STATE_MANAGE_DISPLAY
        self.drag_item_no = None
        self.is_showing_empty = False
        self.auto_match_list = []
        self.init_scene()
        self.init_event()
        self.init_widget()
        return

    def init_scene(self):
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.WEAPON_SHOW, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def update_scene(self):
        pass

    def init_event(self):
        self.panel.btn_manage.BindMethod('OnClick', self.on_click_manage)
        self.panel.btn_quick_manage.BindMethod('OnClick', self.on_click_quick_match)

    def get_parent_select_role(self):
        return self.parent.selected_role_id

    def get_parent_interaction_state(self):
        return self.parent.interaction_state

    def get_cur_select_widget(self):
        return self._round_select_widget

    def update_parent_select_role(self):
        if self.parent:
            self.parent.selected_role_id = self.selected_role_id

    def update_parent_interaction_state(self):
        self.parent.interaction_state = self.interaction_state

    def reset_descs(self):
        self.panel.lab_name.setVisible(False)
        self.panel.lab_describe.setVisible(False)
        if hasattr(self.panel, 'img_item') and self.panel.img_item:
            self.panel.img_item.setVisible(False)

    def update_role_redpoints(self):
        if self.role_select_widget:
            self.role_select_widget.update_red_point(None)
        return

    def update_role_data(self, role_id, state_changed=False, data_changed=False):
        role_change = role_id != self.selected_role_id
        is_init = state_changed or role_id != self.selected_role_id or not self.inited
        self.inited = True
        self.selected_role_id = role_id
        self.update_parent_select_role()
        select_index = is_init or self.selected_item_index if 1 else None
        self.role_interaction_info = items_book_utils.get_interaction_item_info(role_id, self.TAB_ITEM_TYPE)
        if is_init or data_changed:
            self._round_select_widget.udpate_selected_role_id(self.selected_role_id)
            self._list_select_widget and self._list_select_widget.udpate_selected_role_id(self.selected_role_id)
        self.interaction_own_info = {}
        for k, v in six.iteritems(self.role_interaction_info):
            can_use, _ = mall_utils.item_can_use_by_item_no(k)
            if can_use:
                self.interaction_own_info[k] = 1

        self.role_interaction_info_list = sorted(six_ex.keys(self.role_interaction_info), key=cmp_to_key(lambda x, y: six_ex.compare(int(x), int(y))))
        self.role_interaction_own_list = sorted(six_ex.keys(self.interaction_own_info), key=cmp_to_key(lambda x, y: six_ex.compare(int(x), int(y))))
        self.update_own_count()
        if role_change or state_changed:
            self.get_cur_select_widget().update_parent_selected_item_no(None)
        if state_changed:
            self.on_state_changed()
        self._item_filter_widget.set_itemlist(self.role_interaction_info_list)
        self.reset_descs()
        self.update_interaction_list(is_init, select_index)
        return

    def update_select_item_collect_count(self):
        desc_str, skin_str = self._item_filter_widget.get_selected_item_str()
        self.panel.lab_collect_skin.SetString(skin_str)
        self.panel.lab_collect_desc.SetString(desc_str)

    def on_state_changed(self):
        if self.get_interaction_state() == items_book_const.INTERACTION_STATE_DISPLAY:
            self.panel.PlayAnimation('disappear_manage')
        else:
            self.panel.PlayAnimation('show_manage')

    def on_drag_set_interaction(self, idx, item_no):
        global_data.player.try_set_interaction_data(int(self.selected_role_id), idx, item_no)

    def on_click_set_interaction(self, idx):
        selected_item_index = self.selected_item_index
        if selected_item_index is None:
            return
        else:
            global_data.player.try_set_interaction_data(int(self.selected_role_id), idx, self.data_list[self.selected_item_index])
            self.selected_item_index = None
            self.update_role_data(self.selected_role_id)
            self.get_cur_select_widget().update_parent_selected_item_no(None)
            return

    def show_item_detail(self, item_no):
        valid = bool(item_no) and str(item_no) in self.role_interaction_info
        if not self.panel:
            return
        self.panel.lab_name.setVisible(valid)
        self.panel.lab_describe.setVisible(valid)
        self.panel.img_item.setVisible(valid)
        if not valid:
            return
        self.panel.lab_name.SetString(items_book_utils.get_filter_item_show_name(items_book_const.SPRAY_ID, item_no))
        self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
        self.panel.img_item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
        self._get_use_buy_widget.update_target_item_no(item_no, self.interaction_state)

    def on_delete_interaction(self, idx):
        global_data.player.try_set_interaction_data(int(self.selected_role_id), idx, 0)

    def update_total_count(self):
        all_items = items_book_utils.get_interaction_item_info(None, self.TAB_ITEM_TYPE)
        own_count = 0
        for k, v in six.iteritems(all_items):
            can_use, _ = mall_utils.item_can_use_by_item_no(k)
            if can_use:
                own_count += 1

        self.panel.lab_collect.SetString('%d/%d' % (own_count, len(all_items)))
        return

    def on_change_interaction_data(self, role_id):
        if str(role_id) != str(self.selected_role_id):
            return
        self.update_role_data(self.selected_role_id, data_changed=True)

    def on_click_manage(self, *args):
        if not self.panel:
            return
        display_state = items_book_const.INTERACTION_STATE_DISPLAY
        new_state = display_state if self.interaction_state != display_state else items_book_const.INTERACTION_STATE_MANAGE_DISPLAY
        self.panel.btn_manage.SetText(items_book_utils.get_manage_state_text_id(new_state))
        self.panel.btn_manage.SetSelect(new_state == items_book_const.INTERACTION_STATE_MANAGE_DISPLAY)
        self.interaction_state = new_state
        self.update_parent_interaction_state()
        self.update_role_data(self.selected_role_id, True)

    def update_auto_match_list(self):
        self.auto_match_list = sorted(self.data_list, key=cmp_to_key(self.cmp_auto_match_item))

    def cmp_auto_match_item(self, item_no1, item_no2):
        rare_degree1 = item_utils.get_item_rare_degree(item_no1)
        rare_degree2 = item_utils.get_item_rare_degree(item_no2)
        degree_cmp_res = six_ex.compare(rare_degree2, rare_degree1)
        if degree_cmp_res != 0:
            return degree_cmp_res
        return six_ex.compare(int(item_no1), int(item_no2))

    def on_select_filter_item(self):
        self.update_interaction_list(False, 0)

    def update_interaction_list(self, is_init, select_index):
        self.data_list = self._item_filter_widget.get_selected_degree_items(sort_by_can_use=True)
        self.update_select_item_collect_count()
        self.update_auto_match_list()
        self.panel.nd_empty.setVisible(not bool(self.data_list))
        if not self.data_list:
            self.on_data_empty()
        else:
            self.on_data_exist()
        self._interaction_list_widget.update_skin_data(self.data_list, is_init, select_index)

    def on_data_exist(self):
        is_manage = self.interaction_state == items_book_const.INTERACTION_STATE_MANAGE_DISPLAY
        if self.is_showing_empty:
            ani_name = 'show_manage' if is_manage else 'disappear_manage'
            self.panel.PlayAnimation(ani_name)
        self.is_showing_empty = False

    def on_data_empty(self):
        self.is_showing_empty = True
        self.panel.StopAnimation('show_manage')
        self.panel.StopAnimation('disappear_manage')
        self.panel.temp_round.setVisible(False)
        if self.panel.img_item:
            self.panel.img_item.setVisible(False)
        self.init_scene()

    def update_own_count(self):
        self.panel.lab_collect_skin.SetString('%d/%d' % (len(self.interaction_own_info), len(self.role_interaction_info)))

    def init_desc_item(self):
        self.panel.nd_empty.setVisible(False)
        if self.interaction_state == items_book_const.INTERACTION_STATE_DISPLAY:
            self.panel.btn_quick_manage.setVisible(False)
            self.panel.temp_round.setPosition(self.panel.temp_origin.getPosition())
            self.panel.temp_round.setVisible(False)
            self.panel.temp_round.setOpacity(255)
            if self.panel.img_item:
                self.panel.img_item.setPosition(self.panel.img_origin.getPosition())
                self.panel.img_item.setVisible(True)
                self.panel.img_item.setOpacity(255)
        else:
            self.panel.btn_quick_manage.setVisible(True)
            self.panel.PlayAnimation('show_manage')
        self.show_item_detail(0)
        self.panel.btn_manage.EnableCustomState(True)
        self.panel.btn_manage.SetText(items_book_utils.get_manage_state_text_id(self.interaction_state))
        self.panel.btn_manage.SetSelect(self.interaction_state == items_book_const.INTERACTION_STATE_MANAGE_DISPLAY)

    def init_widget(self, role_item_cls=RoleItemSelectWidget):
        self.init_desc_item()
        self._item_filter_widget = ItemFilterWidget(self, self.panel.choose_list, self.panel.btn_change, self.DEFAULT_FILTER_STR_ID, self.PATTERN_FILTER_STR_ID, self.on_select_filter_item, self.panel.img_arrow)
        self._get_use_buy_widget = InteractionGetUseBuyWidget(self, self.panel.btn_buy_1, self.panel.btn_use, self.panel.btn_go, self.panel.temp_price, self.panel.lab_get_method)
        self._round_select_widget = RoundSelectWidget(self, self.panel.temp_round)
        self._interaction_list_widget = SkinItemListWidget(self, self.panel.list_item, self.on_create_interation_item, 12)
        self.role_select_widget = role_item_cls(self, self.panel.temp_right_tab.list_right, self.TAB_ITEM_TYPE, self.update_role_data)
        self.role_select_widget.init_select_item(self.role_select_widget.get_role_idx_in_list(self.selected_role_id))
        self.update_total_count()

    def unselect_item(self, *args):
        if not self.panel:
            return
        else:
            prev_item = self.panel.list_item.GetItem(self.selected_item_index)
            if prev_item:
                prev_item.setLocalZOrder(0)
                prev_item.choose.setVisible(False)
            self.selected_item_index = None
            return

    def on_select_item(self, index, *args):
        if not self.panel:
            return
        if index >= len(self.data_list):
            return
        item_no = self.data_list[index]
        item_widget = self.panel.list_item.GetItem(index)
        self.unselect_item()
        self.selected_item_index = index
        item_widget.setLocalZOrder(2)
        item_widget.choose.setVisible(True)
        red_point_utils.show_red_point_template(item_widget.nd_new, False)
        self.show_item_detail(item_no)
        global_data.player.req_del_item_redpoint(int(item_no))

    def on_select_manage_item(self, index, btn, touch, *args):
        if index >= len(self.data_list):
            return
        else:
            item_no = self.data_list[index]
            if items_book_utils.is_interaction_item_setted(item_no, self.selected_role_id, self.is_auto_mode):
                self.get_cur_select_widget().update_parent_selected_item_no(None)
                self.unselect_item()
                self.show_item_detail(item_no)
                return
            if bool(touch):
                self.get_cur_select_widget().update_parent_selected_item_no(self.data_list[index])
                self.on_select_item(index)
            else:
                self.show_item_detail(item_no)
            return

    def bind_widget_event(self, item_widget, index):
        if self.interaction_state == items_book_const.INTERACTION_STATE_DISPLAY:
            item_widget.bar.BindMethod('OnClick', Functor(self.on_select_item, index))
            item_widget.bar.UnBindMethod('OnBegin')
            item_widget.bar.UnBindMethod('OnDrag')
            item_widget.bar.UnBindMethod('OnEnd')
            item_widget.bar.UnBindMethod('OnCancel')
        else:
            item_widget.bar.BindMethod('OnClick', Functor(self.on_select_manage_item, index))
            item_widget.bar.BindMethod('OnBegin', Functor(self.on_begin_select_item, self.data_list[index]))
            item_widget.bar.BindMethod('OnDrag', Functor(self.on_drag_select_item, self.data_list[index]))
            item_widget.bar.BindMethod('OnEnd', Functor(self.on_end_select_item, None, self.data_list[index]))
            item_widget.bar.BindMethod('OnCancel', Functor(self.on_end_select_item, None, self.data_list[index]))
        return

    def on_create_display_interaction_item(self, lst, index, item_widget):
        valid = index < len(self.data_list)
        if valid:
            item_widget.nd_content.setVisible(True)
            item_no = self.data_list[index]
            item_widget.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
            item_widget.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
            item_widget.choose.setVisible(False)
            if global_data.player:
                interaction_data = global_data.player.get_role_interaction_data(self.selected_role_id, self.is_auto_mode)
            else:
                interaction_data = {}
            is_using = int(item_no) in six_ex.values(interaction_data)
            item_widget.img_using.setVisible(is_using)
            can_use, _ = mall_utils.item_can_use_by_item_no(item_no)
            item_widget.img_lock.setVisible(not can_use)
            item_utils.check_skin_tag(item_widget.nd_kind, item_no)
            item_utils.check_skin_bg_tag(item_widget.img_level, item_no, is_small_item=True)
            item_widget.bar.SetEnable(True)
            red_point_utils.show_red_point_template(item_widget.nd_new, False)
            item_widget.bar.SetSwallowTouch(False)
            item_widget.bar.SetNoEventAfterMove(False, '5w')
            self.bind_widget_event(item_widget, index)
            has_item = global_data.player.get_item_by_no(int(item_no))
            show_new = bool(has_item) and has_item.rp
            red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.img_level.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)
        item_widget.nd_empty.setVisible(not valid)

    def on_create_interation_item(self, lst, index, item_widget):
        self.on_create_display_interaction_item(lst, index, item_widget)

    def get_interaction_state(self):
        return self.interaction_state

    def set_interaction_state(self, state):
        self.interaction_state = state

    def destroy(self):
        if self._round_select_widget:
            self._round_select_widget.destroy()
            self._round_select_widget = None
        self.role_select_widget.destroy()
        self.role_select_widget = None
        self._interaction_list_widget.destroy()
        self._interaction_list_widget = None
        self._item_filter_widget.destroy()
        self._item_filter_widget = None
        self.panel = None
        self.parent = None
        self.data_dict = None
        return

    def on_begin_select_item(self, item_no, btn, touch, *args):
        self.unselect_item()
        self.get_cur_select_widget().update_parent_selected_item_no(None)
        can_use, _ = mall_utils.item_can_use_by_item_no(item_no)
        if self.interaction_state == items_book_const.INTERACTION_STATE_MANAGE_MOVE_ITEM:
            self.on_end_select_item(None, item_no, btn, touch, *args)
            return
        else:
            if can_use:
                self.interaction_state = items_book_const.INTERACTION_STATE_MANAGE_MOVE_ITEM
            else:
                self.interaction_state = items_book_const.INTERACTION_STATE_MANAGE_DISPLAY
            return True

    def show_drag_item(self, item_no):
        self.panel.drag_item.setVisible(True)
        self.panel.drag_item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
        self.show_item_detail(item_no)

    def hide_drag_item(self):
        self.panel.drag_item.setVisible(False)

    def on_drag_item(self, item_no, wpos):
        lpos = self.panel.drag_item.getParent().convertToNodeSpace(wpos)
        self.panel.drag_item.setPosition(lpos)
        item_index = self.get_cur_select_widget().check_drag_pos(wpos)
        return item_index

    def on_drag_select_item(self, item_no, btn, touch, *args):
        if not self.parent:
            return
        else:
            if self.interaction_state != items_book_const.INTERACTION_STATE_MANAGE_MOVE_ITEM:
                self.on_end_select_item(None, item_no, btn, touch)
                return
            if not self.panel.drag_item.isVisible() and not btn.GetSwallowTouch():
                pos = touch.getLocation()
                beg_pos = touch.getStartLocation()
                dx = pos.x - beg_pos.x
                dy = pos.y - beg_pos.y
                if abs(dx) + abs(dy) < DRAG_DELTA * 1.1:
                    return
                if abs(dx) >= abs(dy):
                    btn.SetSwallowTouch(True)
                    self.show_drag_item(item_no)
                else:
                    btn.SetSelect(False)
                    btn.SetEnableTouch(False)
                    btn.SetEnableTouch(True)
                    btn.SetSwallowTouch(False)
                    return
            wpos = touch.getLocation()
            self.on_drag_item(item_no, wpos)
            if not btn.GetSwallowTouch():
                btn.SetSwallowTouch(True)
            return

    def on_end_select_item(self, index, item_no, btn, touch, *args):
        if not self.panel:
            return
        else:
            btn.SetSwallowTouch(False)
            self.panel.drag_item.setVisible(False)
            if self.interaction_state == items_book_const.INTERACTION_STATE_MANAGE_MOVE_ITEM:
                self.interaction_state = items_book_const.INTERACTION_STATE_MANAGE_DISPLAY
                wpos = touch.getLocation()
                drag_index = self.on_drag_item(item_no, wpos)
                if index is not None and drag_index is None:
                    self.on_drag_set_interaction(index, 0)
                elif drag_index is not None:
                    self.on_drag_set_interaction(drag_index, item_no)
                self.get_cur_select_widget().update_parent_selected_item_no(None)
            return

    def on_red_point_update(self, item_no):
        self.role_select_widget.update_red_point(item_no)

    def on_click_quick_match(self, *args):
        self.quick_match_items()

    def quick_match_items(self):
        player = global_data.player
        if self.selected_role_id is None or self.data_list is None:
            return
        else:
            if not player:
                return
            role_interaction_data = player.get_role_interaction_data(self.selected_role_id, self.is_auto_mode)
            item_idx = 0
            item_count = len(self.data_list)
            using_interaction_data = set(six_ex.values(role_interaction_data))
            if self.is_auto_mode:
                self.quick_fill_list_select_widget(role_interaction_data, using_interaction_data, item_count)
            else:
                self.quick_fill_round_select_widget(role_interaction_data, using_interaction_data, item_count)
            return

    def quick_fill_round_select_widget(self, role_interaction_data, using_interaction_data, item_count):
        item_idx = 0
        for idx in range(0, 8):
            if idx in role_interaction_data and role_interaction_data[idx] != 0:
                continue
            while item_idx < item_count:
                item_no = self.auto_match_list[item_idx]
                item_idx += 1
                can_use, _ = mall_utils.item_can_use_by_item_no(item_no)
                is_using = int(item_no) in using_interaction_data
                if can_use and not is_using:
                    global_data.player.try_set_interaction_data(int(self.selected_role_id), idx, item_no)
                    global_data.player.req_del_item_redpoint(int(item_no))
                    break

    def quick_fill_list_select_widget(self, role_interaction_data, using_interaction_data, item_count):
        pass

    def jump_to_item_no(self, item_no):
        if self.role_select_widget and hasattr(self.role_select_widget, 'jump_to_item_no'):
            self.role_select_widget.jump_to_item_no(item_no)