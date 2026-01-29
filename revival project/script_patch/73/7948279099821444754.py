# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaReconstructWidget.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import zip
from six.moves import range
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gcommon.const import MECHA_PART_HEAD, MECHA_PART_LEFT_ARM, MECHA_PART_RIGHT_ARM, MECHA_PART_BODY, MECHA_PART_PROPELLER, MECHA_PART_LOWER_BODY, MECHA_COMPONENT_PART_LIST
from logic.gutils.new_template_utils import SingleChooseWidget
from logic.gutils import item_utils, inscription_utils
from logic.gcommon.cdata.mecha_component_data import get_component_unlock_items, get_usable_component_list_by_part
from logic.gcommon.item import item_const
from bson.objectid import ObjectId
from logic.gcommon.cdata.mecha_component_conf import UNLOCK_SLOT_PRICE, UNLOCK_PAGE_PRICE, MAX_PAGE_NUM
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gcommon.const import SHOP_PAYMENT_GOLD, SHOP_PAYMENT_DIAMON
from logic.client.const.lobby_model_display_const import ROTATE_FACTOR
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gutils.template_utils import get_money_rich_text
from logic.gcommon.common_utils.text_utils import check_review_words
from logic.gcommon.cdata.mecha_component_data import part2type
import time
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, battle_id_to_mecha_lobby_id
MAX_RADAR_AXIS_SCORE = 6.0 * 5
PART_LIST = MECHA_COMPONENT_PART_LIST

def get_default_page_name(page_index):
    return get_text_by_id(81789, [int(page_index) + 1])


class MechaReplaceWidget(BaseUIWidget):

    def __init__(self, parent, panel, mecha_type):
        super(MechaReplaceWidget, self).__init__(parent, panel)
        self._mecha_type = mecha_type
        self._page_index = -1
        self._page_used_item_id_list = []
        self._selected_item_no = None
        self._selected_part = None
        self._list_last_selected_item = None
        self._list_last_selected_info = None
        self._selected_slot_idx = None
        self._nd = self.panel.nd_details
        self.init_btn_event()
        self.check_has_unown()
        return

    def check_has_unown(self):
        from logic.gcommon.cdata.mecha_component_data import get_component_list_by_type, get_component_all_list
        all_list = get_component_all_list()
        coms = global_data.player.get_mecha_component_list()
        has_unown = len(coms) != all_list
        self._nd.nd_add.btn_get.setVisible(has_unown)
        self._nd.nd_add_change.btn_get.setVisible(has_unown)

    def init_btn_event(self):

        @self._nd.nd_add.btn_get.callback()
        def OnClick(btn, touch):
            self.goto_bag()

        @self._nd.nd_add_change.btn_get.btn_common.callback()
        def OnClick(btn, touch):
            self.goto_bag()

    def goto_bag(self):
        from logic.gutils.jump_to_ui_utils import jump_to_mecha_inscription_bag
        com_ty = part2type(self._selected_part)
        ui_inst = global_data.ui_mgr.get_ui('InscriptionMainUI')
        if ui_inst:
            jump_to_mecha_inscription_bag(self._mecha_type, com_type=com_ty, only_unowned=True)

    def on_switch_mecha_type(self, mecha_type):
        self._mecha_type = mecha_type
        self._page_index = -1
        self._page_used_item_id_list = []
        self._selected_item_no = None
        self._selected_part = None
        self._selected_slot_idx = None
        return

    def set_info(self, page_index):
        self._page_index = page_index
        page_content = global_data.player.get_mecha_component_page_content_conf(self._mecha_type, self._page_index)
        used_item_id_list = []
        for _, item_id_list in six.iteritems(page_content):
            used_item_id_list.extend([ item_id for item_id in item_id_list if item_id is not None ])

        self._page_used_item_id_list = used_item_id_list
        return

    def _install_callback(self, sel_component_no, is_own):
        part = self._selected_part
        slot_idx = self._selected_slot_idx
        install_item_id = sel_component_no
        if install_item_id:
            name = item_utils.get_lobby_item_name(sel_component_no)
            global_data.player.install_mecha_component(self._mecha_type, self._page_index, part, slot_idx, install_item_id)
            global_data.game_mgr.show_tip(get_text_by_id(81829, {'name': name}))
            global_data.emgr.on_notify_guide_event.emit('inscr_guide_1_finish')
        else:
            log_error("Can't fing suitable item for component item_no ", sel_component_no)

    def _replace_callback(self, sel_component_no, is_own):
        nd = self._nd
        nd.nd_now.setVisible(False)
        nd.nd_change.setVisible(True)
        nd.nd_change.temp_after.setVisible(True)
        inscription_utils.init_component_detail_temp(nd.nd_change.temp_now, self._selected_item_no)
        inscription_utils.init_component_detail_temp(nd.nd_change.temp_after, sel_component_no)

        @nd.nd_change.btn_change.btn_common.callback()
        def OnClick(btn, touch):
            if not global_data.player.has_owned_component(sel_component_no):
                return
            self._install_callback(sel_component_no, True)

    def on_select_component(self, part, slot_idx, com_item_no, is_refresh=False):
        nd = self.panel.nd_details
        self._selected_part = part
        self._selected_slot_idx = slot_idx
        self._selected_item_no = com_item_no
        if com_item_no:
            nd.nd_title.lab_title.SetString(81780)
            nd.nd_now.setVisible(True)
            nd.nd_basic.setVisible(True)
            nd.nd_add.setVisible(False)
            nd.nd_add_change.setVisible(False)
            nd.nd_change.setVisible(False)
            self.on_hide_replace_nd()
            inscription_utils.init_component_slot_temp(nd.nd_now.temp_icon_now, com_item_no)
            nd.nd_now.lab_item_name.SetString(item_utils.get_lobby_item_name(com_item_no))
            nd.nd_now.lab_sort.SetString(inscription_utils.get_com_sort_name(com_item_no))
            inscr_buff_list = inscription_utils.get_component_id_buff_list(com_item_no)
            inscription_utils.init_desc_list(nd.nd_now.nd_desc, inscr_buff_list)

            @nd.nd_basic.btn_change.callback()
            def OnClick(btn, touch):
                nd.nd_basic.setVisible(False)
                nd.nd_add_change.setVisible(True)
                self.set_component_list(nd.nd_add_change.list_inscription_change, nd.nd_add_change.nd_empty, part, slot_idx, com_item_no, self._replace_callback)
                global_data.emgr.on_notify_guide_event.emit('inscr_guide_1_finish')

            global_data.emgr.on_notify_guide_event.emit('inscr_guide_choose_tech')
        else:
            nd.nd_title.lab_title.SetString(81782)
            nd.nd_add_change.setVisible(False)
            nd.nd_change.setVisible(False)
            self.on_hide_replace_nd()
            nd.nd_add.setVisible(True)
            nd.nd_now.setVisible(False)
            nd.nd_basic.setVisible(False)
            self.set_component_list(nd.nd_add.list_inscription_select, nd.nd_add.nd_empty, part, slot_idx, com_item_no, self._install_callback, is_refresh)

    def on_check_component_slot_changed(self):
        self.refresh_list_show()

    def set_component_list(self, ls, nd_empty, part, slot_id, sel_com_id, callback, is_refresh=False):
        all_list = inscription_utils.filter_list_by_plan(get_usable_component_list_by_part(part))
        component_items = inscription_utils.get_player_component_list_by_parts([part], self._page_used_item_id_list)
        unown_list, own_list = inscription_utils.get_merged_item_no_all_list(component_items, all_list)
        count = len(own_list)
        nd_empty.setVisible(count == 0)
        if count != ls.GetItemCount():
            ls.SetInitCount(count)
        for idx, item_no in enumerate(own_list):
            ui_item = ls.GetItem(idx)
            if not ui_item:
                continue
            ui_item.nd_normal.setVisible(True)
            ui_item.nd_none.setVisible(False)
            if self._list_last_selected_info == item_no:
                ui_item.nd_select.setVisible(True)
                self.set_choose(ui_item, True)
                self._list_last_selected_item = ui_item
            inscription_utils.init_component_detail_temp(ui_item, item_no)

            @ui_item.callback()
            def OnClick(btn, touch, component_no=item_no, ui_item=ui_item):
                if self._list_last_selected_item is not None:
                    if self._list_last_selected_item.nd_select:
                        self._list_last_selected_item.nd_select.setVisible(False)
                    self.set_choose(self._list_last_selected_item, False)
                ui_item.nd_select.setVisible(True)
                self._list_last_selected_item = ui_item
                self.set_choose(self._list_last_selected_item, True)
                self._list_last_selected_info = component_no
                if callback:
                    callback(component_no, True)
                return

    def on_buy_good_success(self, item_no):
        self.refresh_list_show()
        self.check_has_unown()

    def refresh_list_show(self):
        if self._list_last_selected_item:
            if self._list_last_selected_item.nd_select:
                self._list_last_selected_item.nd_select.setVisible(False)
            self.set_choose(self._list_last_selected_item, False)
        self._list_last_selected_item = None
        if not self._nd.isVisible():
            return
        else:
            part = self._selected_part
            slot_idx = self._selected_slot_idx
            com_item_no = self._selected_item_no
            nd = self._nd
            old_vis = nd.nd_add_change.isVisible()
            self.on_select_component(part, slot_idx, self._selected_item_no, True)
            nd.nd_add_change.setVisible(old_vis)
            if old_vis:
                nd.nd_basic.setVisible(False)
                nd.nd_add_change.setVisible(True)
                if self._list_last_selected_info:
                    nd.nd_change.setVisible(True)
                    nd.nd_change.temp_after.setVisible(True)
                self.set_component_list(nd.nd_add_change.list_inscription_change, nd.nd_add_change.nd_empty, part, slot_idx, com_item_no, self._replace_callback, is_refresh=True)
            return

    def on_hide_replace_nd(self):
        self._list_last_selected_info = None
        if self._list_last_selected_item and self._list_last_selected_item.nd_select:
            self._list_last_selected_item.nd_select.setVisible(False)
            self.set_choose(self._list_last_selected_item, False)
        self._list_last_selected_item = None
        return

    def set_choose(self, slot_detail_nd, is_select):
        pass


class MechaPageListWidget(BaseUIWidget):
    PAGE_DATA = 0
    PAGE_RECOMMEND = 1
    RECOMMEND_PLAN_COUNT = 2

    def __init__(self, parent, panel, mecha_type):
        super(MechaPageListWidget, self).__init__(parent, panel)
        self._mecha_type = mecha_type
        self._page_index = -1
        self._page_type = MechaPageListWidget.PAGE_DATA
        self._page_name_dict = {}
        self._unlock_page_num = 1
        self._hide_time = 0
        self._nd = self.panel.nd_define
        self._list_sview = None
        self.init_page_panel()

        @self.panel.nd_define.btn_change.callback()
        def OnClick(btn, touch):
            if not self.panel.nd_change_list.isVisible():
                self.change_page_type(MechaPageListWidget.PAGE_DATA)
                self.show_list()
            else:
                self.hide_list()

        @self.panel.btn_rename.callback()
        def OnClick(btn, touch):
            self.show_change_page_name_ui(self._page_index)

        @self.panel.temp_list.nd_close.callback()
        def OnClick(btn, touch):
            self.hide_list()

        return

    def destroy(self):
        super(MechaPageListWidget, self).destroy()
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        self._nd = None
        return

    def is_visible(self):
        return super(MechaPageListWidget, self).is_visible() and self.panel.nd_change_list.isVisible()

    def show_list(self):
        if time.time() - self._hide_time < 0.01:
            return
        self.panel.nd_change_list.setVisible(True)
        self.panel.icon_arrow.setRotation(180)
        self.panel.PlayAnimation('change_list')
        self.refresh_page_show()
        if self.panel.nd_change_list.isVisible() and self._page_type == self.PAGE_RECOMMEND:
            global_data.emgr.on_notify_guide_event.emit('inscr_guide_choose_recommend2')

    def hide_list(self):
        self._hide_time = time.time()
        global_data.emgr.on_notify_hide_guide_event.emit('inscr_guide_choose_recommend2')
        self.panel.StopAnimation('change_list')
        self.panel.nd_change_list.setVisible(False)
        self.panel.icon_arrow.setRotation(0)

    def init_page_panel(self):
        from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
        self._list_sview = InfiniteScrollWidget(self.panel.temp_list.list_item, self.panel, up_limit=500, down_limit=500)
        self._list_sview.set_custom_add_item_func(self.add_scroll_elem)
        self._list_sview.set_template_init_callback(self.init_page_ui_item)
        self.panel.temp_list.list_sort.SetInitCount(2)
        all_tab_item = self.panel.temp_list.list_sort.GetAllItem()
        tab_list = [2246, 80567]
        for ind, ui_item in enumerate(all_tab_item):
            ui_item.btn_tab.SetText(tab_list[ind])

            @ui_item.btn_tab.callback()
            def OnClick(btn, touch, ind=ind):
                self.change_page_type(ind)

        self.change_page_type(self._page_type)

    def change_page_type(self, page_type):
        all_tab_item = self.panel.temp_list.list_sort.GetAllItem()
        for ind, ui_item in enumerate(all_tab_item):
            if ind == page_type:
                ui_item.btn_tab.SetSelect(True)
            else:
                ui_item.btn_tab.SetSelect(False)

        self._page_type = page_type
        self.refresh_page_show()
        if self.panel.nd_change_list.isVisible() and page_type == self.PAGE_RECOMMEND:
            global_data.emgr.on_notify_guide_event.emit('inscr_guide_choose_recommend2')
        else:
            global_data.emgr.on_notify_hide_guide_event.emit('inscr_guide_choose_recommend2')
            return

    def refresh_page_show(self):
        if not self.panel.nd_change_list.isVisible():
            return
        if self._page_type == MechaPageListWidget.PAGE_DATA:
            all_data_list = [ str(i) for i in range(MAX_PAGE_NUM) ]
        else:
            all_data_list = [ str(i + 1) for i in range(MechaPageListWidget.RECOMMEND_PLAN_COUNT) ]
        self._list_sview.update_data_list(all_data_list)
        self._list_sview.refresh_showed_item(has_diff_size=True)
        self._list_sview.update_scroll_view()

    def set_page_ui_show(self, cur_page_index, unlock_page_num, page_name_dict):
        self._page_index = cur_page_index
        self._page_name_dict = page_name_dict
        self._unlock_page_num = unlock_page_num
        page_name = self._page_name_dict.get(cur_page_index) or get_default_page_name(cur_page_index)
        self.panel.nd_define.btn_change.lab_name.SetString(page_name)
        if self.panel.nd_change_list.isVisible():
            self.refresh_page_show()

    def show_change_page_name_ui(self, page_index):
        from logic.comsys.message.CommonInputDialog import CommonInputDialog
        global_data.ui_mgr.close_ui('CommonInputDialog')
        ui = CommonInputDialog(title=get_text_by_id(81817), desc_text=get_text_by_id(81817), cost_text='', placeholder=get_text_by_id(81818), max_length=50, send_callback=lambda new_name: self.change_page_name(page_index, new_name))

    def change_page_name(self, page_index, new_page_name):
        flag, msg = check_review_words(new_page_name)
        if not flag:
            global_data.player.notify_client_message((get_text_by_id(81921),))
            return
        global_data.player.edit_component_page_name(self._mecha_type, page_index, new_page_name)
        global_data.ui_mgr.close_ui('CommonInputDialog')

    def add_scroll_elem(self, data, is_back_item, index=-1):
        item_widget = global_data.uisystem.load_template_create(self.panel.temp_list.list_item.GetTemplatePath())
        self.init_page_ui_item(item_widget, data)
        if is_back_item:
            panel = self.panel.temp_list.list_item.AddControl(item_widget, bRefresh=True)
        else:
            panel = self.panel.temp_list.list_item.AddControl(item_widget, 0, bRefresh=True)
        return panel

    def init_page_ui_item(self, ui_item, page_index):
        if self._page_type == MechaPageListWidget.PAGE_DATA:
            self.init_page_ui_item_data(ui_item, page_index)
        else:
            ui_item.InitConfContentSize()

    def init_com_list_by_page_content(self, ui_item, page_content):
        from logic.gcommon.cdata.mecha_component_data import part2type
        ui_item.list_item.SetInitCount(len(PART_LIST) * item_const.COMPONENT_SLOT_CNT_PER_PART)
        ui_item.list_item.setSwallowTouches(False)
        com_ui_item_list = ui_item.list_item.GetAllItem()
        for ind, com_ui_item in enumerate(com_ui_item_list):
            part_ind = int(ind / item_const.COMPONENT_SLOT_CNT_PER_PART)
            part = str(PART_LIST[part_ind])
            slot_index = ind % item_const.COMPONENT_SLOT_CNT_PER_PART
            unlock_slot_list = global_data.player.get_unlock_slot_idx(part)
            slot_item_id_list = page_content.get(part, [None] * item_const.COMPONENT_SLOT_CNT_PER_PART)
            component_item_no = slot_item_id_list[slot_index]
            if component_item_no:
                com_ui_item.img_empty.setVisible(False)
                com_ui_item.img_lock.setVisible(False)
                inscription_utils.init_component_slot_temp(com_ui_item.temp_item, component_item_no, show_tips=True)
            else:
                is_lock = slot_index not in unlock_slot_list
                com_type = part2type(int(part))
                inscription_utils.init_component_slot_temp(com_ui_item.temp_item, None, is_lock=is_lock, com_type=com_type)

        return

    def init_com_list(self, ui_item, item_no_list, empty_slot_dict=None):
        sorted_item_nos = sorted(item_no_list, reverse=True)
        from logic.gcommon.cdata.mecha_component_data import part2type
        com_type_list_dict = {}
        if empty_slot_dict:
            for p, slot_index_list in six.iteritems(empty_slot_dict):
                com_ty = part2type(p)
                com_type_list_dict.setdefault(com_ty, 0)
                com_type_list_dict[com_ty] += len(slot_index_list)

        for com_ty in list(six_ex.keys(com_type_list_dict)):
            if com_type_list_dict[com_ty] == 0:
                com_type_list_dict.pop(com_ty)

        len_sorted_item_nos = len(sorted_item_nos)
        ui_item.list_item.SetInitCount(len_sorted_item_nos + len(com_type_list_dict))
        com_type_key_list = sorted(six_ex.keys(com_type_list_dict))
        ui_item.list_item.setSwallowTouches(False)
        com_ui_item_list = ui_item.list_item.GetAllItem()
        for ind, com_ui_item in enumerate(com_ui_item_list):
            if ind < len_sorted_item_nos:
                item_no = sorted_item_nos[ind]
                com_ui_item.img_empty.setVisible(False)
                inscription_utils.init_component_slot_temp(com_ui_item.temp_item, item_no, show_tips=True)
            else:
                com_type = com_type_key_list[ind - len_sorted_item_nos]
                inscription_utils.init_component_slot_temp(com_ui_item.temp_item, None, is_lock=False, com_type=com_type)
                com_ui_item.img_empty.setVisible(True)

        return

    def init_page_ui_item_data(self, ui_item, page_index):
        is_lock = int(page_index) >= self._unlock_page_num
        if not is_lock:
            ui_item.InitConfContentSize()
            ui_item.nd_lock.InitConfContentSize()
            ui_item.nd_lock.setVisible(False)
            ui_item.nd_content.setVisible(True)
            ui_item.btn_rename.setVisible(True)
            page_content = global_data.player.get_mecha_component_page_content_conf(self._mecha_type, page_index)
            if page_index == self._page_index:
                ui_item.nd_using.setVisible(True)
                ui_item.btn_use.setVisible(False)
            else:
                ui_item.nd_using.setVisible(False)
                ui_item.btn_use.setVisible(True)

                @ui_item.btn_use.btn_common.callback()
                def OnClick(btn, touch):
                    global_data.player.set_active_insc_page(self._mecha_type, page_index)
                    global_data.game_mgr.show_tip(get_text_by_id(81831))
                    self.hide_list()

            self.init_com_list_by_page_content(ui_item, page_content)
            page_name = self._page_name_dict.get(page_index) or get_default_page_name(page_index)
            ui_item.lab_item_name.SetString(page_name)

            @ui_item.btn_rename.callback()
            def OnClick(btn, touch):
                self.show_change_page_name_ui(page_index)

            @ui_item.btn_check.callback()
            def OnClick(btn, touch):
                cur_page_item_id_list = inscription_utils.get_used_com_item_id_list(self._mecha_type, page_index)
                page_attr_dict = inscription_utils.get_component_list_inscr_add_dict(cur_page_item_id_list)
                self.show_page_details(page_attr_dict)

        else:
            ui_item.setContentSize(ui_item.nd_lock.getContentSize())
            ui_item.nd_lock.SetPosition('50%', '50%')
            ui_item.nd_lock.setVisible(True)
            ui_item.nd_content.setVisible(False)
            ui_item.lab_plan.SetString(get_default_page_name(page_index))
            price_info_list = [
             {'original_price': UNLOCK_PAGE_PRICE,
                'real_price': UNLOCK_PAGE_PRICE,
                'discount_price': None,
                'goods_payment': SHOP_PAYMENT_DIAMON
                }]
            template_utils.splice_price(ui_item.temp_price, price_info_list)

            @ui_item.btn_unlock.btn_common.callback()
            def OnClick(btn, touch):
                dlg = SecondConfirmDlg2()

                def on_cancel():
                    dlg.close()

                def on_confirm():
                    dlg.close()
                    if mall_utils.check_payment(SHOP_PAYMENT_DIAMON, UNLOCK_PAGE_PRICE):
                        global_data.player.unlock_component_page(self._mecha_type)

                price_text = template_utils.get_money_rich_text_ex(price_info_list)
                dlg.confirm(content=get_text_by_id(81821, {'cost': price_text}), cancel_callback=on_cancel, confirm_callback=on_confirm, unique_callback=on_cancel)

        return

    def on_switch_mecha_type(self, mecha_type):
        self._mecha_type = mecha_type

    def show_page_details(self, page_attr_dict):
        inscription_utils.set_ability_list(self.panel.temp_list.nd_check.list_num, self.panel.temp_list.nd_check.nd_empty, page_attr_dict)
        self.panel.temp_list.nd_check.setVisible(True)

        @self.panel.temp_list.nd_check_close.callback()
        def OnClick(btn, touch):
            self.panel.temp_list.nd_check.setVisible(False)

    def hide_page_details(self):
        self.panel.temp_list.nd_check.setVisible(False)


class MechaReconstructWidget(BaseUIWidget):
    TAB_GRAPH = 1
    TAB_DETAILS = 2

    def __init__(self, parent, panel, mecha_type):
        self.global_events = {'mecha_component_update_event': self.on_mecha_component_update_event,
           'mecha_component_slot_update_event': self.on_mecha_slot_update_event,
           'mecha_component_purchase_success': self.on_buy_good_success,
           'mecha_component_slot_unlocked_event': self.on_slot_unlocked,
           'mecha_component_change_page_name': self._on_page_name_changed,
           'mecha_unlock_page_event': self._on_page_unlock,
           'mecha_component_change_active_page': self._on_change_active_page
           }
        super(MechaReconstructWidget, self).__init__(parent, panel)
        self.init_param()
        self.init_ui_event()
        self._draw_node = None
        self._second_draw_node = None
        self._block_refresh_slot = False
        self._page_used_item_id_list = []
        self._page_attr_dict = {}
        self._old_score_list = None
        self._score_list = None
        self._cur_tab_type = self.TAB_GRAPH
        self._cur_page_content = {}
        self.init_radar_draw_node()
        self.init_radar_score_node([ get_text_by_id(tid) for tid in (81783, 81784,
                                                                     81785, 81786,
                                                                     81787, 81788) ])
        self.init_single_choose_widget()
        self._mechaReplaceWidget = MechaReplaceWidget(self, panel, mecha_type)
        self._mechaPageListWidget = MechaPageListWidget(self, panel, mecha_type)
        self._has_first_show = False
        return

    def init_single_choose_widget(self):
        self.single_choose_widget = SingleChooseWidget()
        self.single_choose_widget.SetCallbacks(self.on_select_status_change, self.on_select_status_ui_update)
        allItem = []
        for part in self.PART_LIST:
            part_nd = self.get_part_nd(part)
            for slot_idx in range(self.INSCR_ND_NUM):
                slot_nd = getattr(part_nd, 'temp_%s' % (slot_idx + 1))
                allItem.append(slot_nd)

        self.single_choose_widget.init(self.panel, allItem, ui_item_btn_name=None)
        return

    def destroy(self):
        self._draw_node = None
        self._second_draw_node = None
        if self.single_choose_widget:
            self.single_choose_widget.destroy()
            self.single_choose_widget = None
        if self._mechaReplaceWidget:
            self._mechaReplaceWidget.destroy()
            self._mechaReplaceWidget = None
        if self._mechaPageListWidget:
            self._mechaPageListWidget.destroy()
            self._mechaPageListWidget = None
        super(MechaReconstructWidget, self).destroy()
        return

    def on_select_status_change(self, idx, is_sel):
        pass

    def on_select_status_ui_update(self, ui_item, is_sel):
        if is_sel:
            ui_item.PlayAnimation('choose')
        ui_item.nd_select.setVisible(is_sel)

    def get_mecha_inscription_page_conf(self, mecha_id):
        return global_data.player.get_mecha_default_component_page(mecha_id)

    def get_part_nd(self, part):
        if part is None:
            return
        else:
            part_2_node_dic = {MECHA_PART_HEAD: self.panel.nd_1,
               MECHA_PART_RIGHT_ARM: self.panel.nd_2,
               MECHA_PART_LEFT_ARM: self.panel.nd_3,
               MECHA_PART_BODY: self.panel.nd_4,
               MECHA_PART_LOWER_BODY: self.panel.nd_5,
               MECHA_PART_PROPELLER: self.panel.nd_6
               }
            return part_2_node_dic.get(int(part))

    def _on_rotate_drag(self, layer, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def _on_end_touch(self, layer, touch):
        from common.utils.ui_utils import get_scale
        if layer.GetMovedDistance() > get_scale('10w'):
            return
        else:
            if not self.single_choose_widget:
                return
            if self.single_choose_widget:
                self.single_choose_widget.SetSelectedIndex(None)
            self.switch_mecha_detail_show(False)
            if self.single_choose_widget.GetSelect() is None:
                from logic.gcommon.const import MECHA_PART_MAP, MECHA_PART_NONE
                global_data.emgr.operate_sfx_model.emit(0, {'vertex_color_mask': MECHA_PART_MAP[MECHA_PART_NONE]})
            return

    def on_switch_to_mecha_type(self, mecha_type):
        self._old_score_list = None
        self._score_list = None
        self._cur_mecha_id = mecha_type
        conf = self._mecha_conf[str(mecha_type)]
        mecha_name = conf.get('name_mecha_text_id', '')
        is_own = global_data.player.has_item_by_no(battle_id_to_mecha_lobby_id(mecha_type))
        self.panel.nd_main.nd_bottom.nd_define.setVisible(is_own)
        self.refresh_unlock_lv()
        self._mechaReplaceWidget.on_switch_mecha_type(mecha_type)
        self._mechaPageListWidget.on_switch_mecha_type(mecha_type)
        self.refresh_ui_show()
        return

    def _copy_one_layer_page_dict(self, dic):
        new_dict = {}
        for k, v in six.iteritems(dic):
            new_dict[k] = list(v)

        return new_dict

    def refresh_ui_show(self, show_change=False):
        self.refresh_page_para()
        self.refresh_page_ui()
        self.switch_mecha_detail_show(False)
        if self.single_choose_widget:
            self.single_choose_widget.SetSelectedIndex(None)
        from logic.gcommon.const import MECHA_PART_MAP, MECHA_PART_NONE
        global_data.emgr.operate_sfx_model.emit(0, {'vertex_color_mask': MECHA_PART_MAP[MECHA_PART_NONE]})
        cur_mecha_inscript_conf = global_data.player.get_mecha_component_page_content_conf(self._cur_mecha_id, self._page_index)
        self._page_used_item_id_list = inscription_utils.get_used_com_item_id_list(self._cur_mecha_id, self._page_index)
        self.refresh_btn_show()
        self._page_attr_dict = inscription_utils.get_component_list_inscr_add_dict(self._page_used_item_id_list)
        self.refresh_component_details(self._page_used_item_id_list)
        for part in self.PART_LIST:
            inscr_item_id_list = cur_mecha_inscript_conf.get(str(part), [])
            old_inscr_item_id_list = self._cur_page_content.get(str(part), [])
            part_nd = self.get_part_nd(part)
            if part_nd:
                for slot_idx in range(self.INSCR_ND_NUM):
                    component_item_no = inscr_item_id_list[slot_idx] if slot_idx < len(inscr_item_id_list) else None
                    slot_nd = getattr(part_nd, 'temp_%s' % (slot_idx + 1))
                    if slot_nd:
                        slot_show_change = False
                        if show_change:
                            old_com_id = old_inscr_item_id_list[slot_idx] if slot_idx < len(old_inscr_item_id_list) else None
                            slot_show_change = old_com_id != component_item_no
                        self.init_component_slot_nd(part, slot_idx, component_item_no, slot_nd, show_change=slot_show_change)

        self._cur_page_content = self._copy_one_layer_page_dict(cur_mecha_inscript_conf)
        self.check_head_guide()
        return

    def check_head_guide(self):
        is_unown = not global_data.player.has_item_by_no(battle_id_to_mecha_lobby_id(self._cur_mecha_id))
        if is_unown:
            global_data.emgr.on_notify_hide_guide_event.emit('inscr_guide_left_arm')
            return
        else:
            inscr_item_id_list = self._cur_page_content.get(str(MECHA_PART_HEAD), [])
            index = 0
            index_item_id = None
            if len(inscr_item_id_list) > index:
                index_item_id = inscr_item_id_list[index]
            if index_item_id is not None:
                global_data.emgr.on_notify_guide_event.emit('inscr_guide_left_arm')
            return

    def on_mecha_component_update_event(self, mecha_id, page_index):
        if self._block_refresh_slot:
            return
        if self._cur_mecha_id == mecha_id and page_index == self._page_index:
            self.refresh_ui_show(show_change=True)
            self._mechaReplaceWidget.on_check_component_slot_changed()

    def on_mecha_slot_update_event(self, mecha_id, page_idx, part, slot_idx, item_id, old_item_id):
        if not (self._cur_mecha_id == mecha_id and page_idx == self._page_index):
            return
        else:
            if old_item_id == None and item_id != None:
                page_content = global_data.player.get_mecha_component_page_content_conf(self._cur_mecha_id, self._page_index)
                nxt_part, nxt_slot_idx = int(part), int(slot_idx)
                for idx in range(item_const.COMPONENT_SLOT_CNT_PER_PART * len(self.PART_LIST)):
                    nxt_part, nxt_slot_idx = self.get_part_slot_idx_next_pos(nxt_part, nxt_slot_idx)
                    part_item_list = page_content.get(str(nxt_part), [])
                    unlock_slot_list = global_data.player.get_unlock_slot_idx(nxt_part)
                    if nxt_slot_idx not in unlock_slot_list:
                        continue
                    if nxt_slot_idx < len(part_item_list):
                        slot_item_id = part_item_list[nxt_slot_idx]
                    else:
                        slot_item_id = None
                    if not slot_item_id:
                        self.select_part_slot(nxt_part, nxt_slot_idx)
                        return

            return

    def get_part_slot_idx_next_pos(self, part, slot_idx):
        if slot_idx < item_const.COMPONENT_SLOT_CNT_PER_PART - 1:
            return (part, slot_idx + 1)
        else:
            part_index = self.PART_LIST.index(int(part))
            return (
             self.PART_LIST[(part_index + 1) % len(self.PART_LIST)], 0)

    def show_attr_dict_change(self, old_dict, new_dict):
        att_change_list, attr_base_factor = inscription_utils.show_attr_dict_change(old_dict, new_dict)
        if len(att_change_list) > 5 or len(att_change_list) <= 0:
            return
        from logic.comsys.mecha_display.MechaInscriptionChangeUI import MechaInscriptionChangeUI
        ui = MechaInscriptionChangeUI()
        ui.show_attr_change(att_change_list)

    def change_close_btn_to_back(self):
        ui_inst = global_data.ui_mgr.get_ui('InscriptionMainUI')
        if ui_inst:

            def _callback():
                ui_inst = global_data.ui_mgr.get_ui('InscriptionMainUI')
                ui_inst.set_temp_btn_back_callback(None)
                self.switch_mecha_detail_show(False)
                return

            ui_inst.set_temp_btn_back_callback(_callback)

    def switch_mecha_detail_show(self, is_show):
        if is_show:
            self.panel.nd_content.setVisible(False)
            self.panel.nd_details.setVisible(True)
            self.change_close_btn_to_back()
            self.refresh_component_details(self._page_used_item_id_list)
        else:
            self.panel.nd_details.setVisible(False)
            ui_inst = global_data.ui_mgr.get_ui('InscriptionMainUI')
            ui_inst.set_temp_btn_back_callback(None)
            if self._mechaReplaceWidget:
                self._mechaReplaceWidget.on_hide_replace_nd()
            self.panel.nd_content.setVisible(True)
            global_data.emgr.on_notify_hide_guide_event.emit('inscr_guide_choose_tech')
        return

    def refresh_page_para(self):
        default_component_page_conf = global_data.player.get_mecha_component_page_conf(self._cur_mecha_id)
        if not default_component_page_conf:
            self._page_index = str(0)
            self._page_name = get_default_page_name(self._page_index)
            self._page_name_dict = {self._page_index: self._page_name}
            self._page_num = 1
        else:
            page_index, page_num, page_name_dict = default_component_page_conf
            self._page_index = page_index
            self._page_name_dict = page_name_dict
            self._page_num = page_num
            page_name = page_name_dict.get(page_index, '')
            if not page_name:
                page_name = get_default_page_name(self._page_index)
            self._page_name = page_name
        self._mechaReplaceWidget.set_info(self._page_index)
        self._mechaPageListWidget.set_page_ui_show(self._page_index, self._page_num, self._page_name_dict)

    def refresh_page_ui(self):
        pass

    def select_part_slot(self, part, slot_idx):
        part_nd = self.get_part_nd(part)
        if not part_nd:
            return
        else:
            slot_nd = getattr(part_nd, 'temp_%s' % (slot_idx + 1))
            if not slot_nd:
                return
            slot_nd.nd_btn.OnClick(None)
            return

    def init_component_slot_nd(self, part, slot_idx, com_item_no, slot_nd=None, show_change=False):
        if not slot_nd:
            part_nd = self.get_part_nd(part)
            if not part_nd:
                return
            slot_nd = getattr(part_nd, 'temp_%s' % (slot_idx + 1))
            if not slot_nd:
                return
        slot_nd.nd_btn.SetSwallowTouch(True)
        if show_change:
            slot_nd.PlayAnimation('change')
        is_unown = not global_data.player.has_item_by_no(battle_id_to_mecha_lobby_id(self._cur_mecha_id))

        @slot_nd.nd_btn.callback()
        def OnClick(btn, touch):
            if not global_data.player.has_item_by_no(battle_id_to_mecha_lobby_id(self._cur_mecha_id)):
                global_data.game_mgr.show_tip(get_text_by_id(81876))
                return
            unlock_index_list = global_data.player.get_unlock_slot_idx(part)
            is_lock = slot_idx not in unlock_index_list
            if is_lock:
                unlock_lv = self.get_part_slot_unlock_lv(part, slot_idx)
                global_data.game_mgr.show_tip(get_text_by_id(868033, {'lv': unlock_lv}))
                return
            self.single_choose_widget.set_ui_item_select_status_by_ui_item(slot_nd, True)
            from logic.gcommon.const import MECHA_PART_MAP
            if int(part) in self.PART_LIST:
                global_data.emgr.operate_sfx_model.emit(0, {'vertex_color_mask': MECHA_PART_MAP[part]})
            self.switch_mecha_detail_show(True)
            self._mechaReplaceWidget.on_select_component(part, slot_idx, com_item_no)

        unlock_slot_list = global_data.player.get_unlock_slot_idx(part)
        is_lock = slot_idx not in unlock_slot_list or is_unown
        if not com_item_no and not is_lock:
            slot_nd.temp_red.setVisible(True)
        else:
            slot_nd.temp_red.setVisible(False)
        unlock_lv = None
        if is_lock and not is_unown:
            unlock_lv = self.get_part_slot_unlock_lv(part, slot_idx)
            if unlock_lv != self._next_unlock_lv:
                unlock_lv = None
        inscription_utils.init_component_slot_temp(slot_nd, com_item_no, is_lock, unlock_lv, com_type=part2type(int(part)), show_full=com_item_no is not None, need_name=True)
        return

    def get_part_slot_unlock_lv(self, part, slot):
        return self.lv_unlock_dict.get(part, {}).get(slot, None)

    def get_total_unlocked_slot_num(self, mecha_id):
        count = 0
        for part in self.PART_LIST:
            unlock_index_list = global_data.player.get_unlock_slot_idx(part)
            count += len(unlock_index_list)

        return count

    def init_radar_score_node(self, title_list):
        for idx, title in enumerate(title_list):
            nd = getattr(self.panel.temp_details, 'nd_data%s' % (idx + 1))
            if nd:
                nd.lab_title.SetString(str(title))

    def init_radar_draw_node(self):
        from common.utils.cocos_utils import ccp
        radar = self.panel.temp_details.nd_radar
        from common.uisys.uielment.CCDrawNode import CCDrawNode
        if not self._draw_node:
            _draw_node = CCDrawNode.Create()
            _draw_node.setAnchorPoint(ccp(0.5, 0.5))
            radar.AddChild('', _draw_node, 10, -1)
            _draw_node.SetPosition('50%', '50%')
            self._draw_node = _draw_node
        if not self._second_draw_node:
            _draw_node = CCDrawNode.Create()
            _draw_node.setAnchorPoint(ccp(0.5, 0.5))
            radar.AddChild('', _draw_node, 1, -1)
            _draw_node.SetPosition('50%', '50%')
            self._second_draw_node = _draw_node

    @staticmethod
    def show_radar(draw_node, score_list=(50, 50, 89, 100, 76), color=[7328498, 6997491, 6799339, 6470372, 8051701, 9102070], opacity=255, max_score=100.0):
        draw_node.clear()
        NUM = 5
        import cc
        from common.utils.cocos_utils import ccc4fFromHex_ex
        import math
        LINE_WIDTH = 1
        LINE_COLOR = cc.Color4F(1, 1, 1, 0)
        PER_ANGLE = 360 / NUM
        START_ANGLE = 126
        angles = [ math.radians(START_ANGLE - PER_ANGLE * idx) for idx in range(NUM) ]
        scale = 2.0
        MAX_LINE_LENGTH = 110 * scale
        lengths = [ score / max_score * MAX_LINE_LENGTH for score in score_list ]
        verts = [ cc.Vec2(math.cos(ang) * length, math.sin(ang) * length) for ang, length in zip(angles, lengths) ]
        draw_node.setOpacity(int(opacity))
        draw_node.setScale(1 / scale)
        if type(color) in [list, tuple]:
            tri_angles = []
            for idx, v in enumerate(verts):
                tri_angles.append([v, verts[(idx + 1) % len(verts)], cc.Vec2(0, 0)])

            for index, tri_verts in enumerate(tri_angles):
                draw_node.drawPolygon(tri_verts, ccc4fFromHex_ex(color[index]), LINE_WIDTH * scale, LINE_COLOR)

        else:
            draw_node.drawPolygon(verts, ccc4fFromHex_ex(color), LINE_WIDTH * scale, LINE_COLOR)

    def init_param(self):
        self._cur_mecha_id = None
        self.INSCR_ND_NUM = 1
        self.PART_LIST = PART_LIST
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        from logic.gcommon.cdata.mecha_component_conf import lv_unlock_data
        lv_unlock_dict = {}
        for unlock_lv, unlock_part_slot in six.iteritems(lv_unlock_data):
            unlock_part, unlock_slot = unlock_part_slot
            lv_unlock_dict.setdefault(unlock_part, {})
            lv_unlock_dict[unlock_part][unlock_slot] = unlock_lv

        self.lv_unlock_dict = lv_unlock_dict
        self.refresh_unlock_lv()
        return

    def refresh_unlock_lv(self):
        self._next_unlock_lv = self.get_next_lv_unlock_slot()

    def get_next_lv_unlock_slot(self):
        cur_lv = global_data.player.get_lv()
        from logic.gcommon.cdata.mecha_component_conf import lv_unlock_data
        for unlock_lv in sorted(six_ex.keys(lv_unlock_data)):
            if unlock_lv > cur_lv:
                unlock_part, unlock_slot_count = lv_unlock_data[unlock_lv]
                unlock_slot_index = unlock_slot_count - 1
                unlock_slot_list = global_data.player.get_unlock_slot_idx(unlock_part)
                is_lock = unlock_slot_index not in unlock_slot_list
                if is_lock:
                    return unlock_lv

        return None

    def init_ui_event(self):

        def _on_show_last_mecha():
            if self.parent:
                self.parent._on_show_last_mecha()

        def _on_show_next_mecha():
            if self.parent:
                self.parent._on_show_next_mecha()

        self.panel.btn_last_mech.BindMethod('OnClick', lambda btn, touch: _on_show_last_mecha())
        self.panel.btn_next_mech.BindMethod('OnClick', lambda btn, touch: _on_show_next_mecha())
        self.panel.temp_btn_out.btn_common.BindMethod('OnClick', lambda btn, touch: self.clear_cur_page())
        self.panel.nd_content.nd_basic.btn_change.BindMethod('OnClick', lambda btn, touch: self._switch_component_details(self.TAB_GRAPH))
        self.panel.nd_content.nd_basic.btn_change_detail.BindMethod('OnClick', lambda btn, touch: self._switch_component_details(self.TAB_DETAILS))
        self.panel.nd_details.btn_close.BindMethod('OnClick', lambda btn, touch: self.switch_mecha_detail_show(False))
        self.panel.nd_touch.BindMethod('OnDrag', self._on_rotate_drag)
        self.panel.nd_touch.BindMethod('OnEnd', self._on_end_touch)

    def refresh_btn_show(self):
        if self._page_used_item_id_list:
            self.panel.temp_btn_out.setVisible(True)
        else:
            self.panel.temp_btn_out.setVisible(False)

    def quick_fill_page(self):
        self.switch_mecha_detail_show(False)
        page_dict = {}
        page_content = global_data.player.get_mecha_component_page_content_conf(self._cur_mecha_id, self._page_index)
        used_item_id_list = []
        for _, item_id_list in six.iteritems(page_content):
            used_item_id_list.extend([ item_id for item_id in item_id_list if item_id is not None ])

        for part in self.PART_LIST:
            part_item_list = page_content.get(str(part), [])
            page_dict[str(part)] = part_item_list
            unlock_slot_list = global_data.player.get_unlock_slot_idx(part)
            for slot_idx in range(item_const.COMPONENT_SLOT_CNT_PER_PART):
                if slot_idx not in unlock_slot_list:
                    continue
                if slot_idx < len(part_item_list):
                    slot_item_id = part_item_list[slot_idx]
                else:
                    slot_item_id = None
                if slot_item_id:
                    continue
                component_items = inscription_utils.get_player_component_list_by_parts([part], used_item_id_list)
                sorted_component_items = sorted(component_items)
                if not sorted_component_items:
                    break
                install_item_no = sorted_component_items[0]
                if len(page_dict[str(part)]) > slot_idx:
                    page_dict[str(part)][slot_idx] = install_item_no
                else:
                    for i in range(len(page_dict[str(part)]), item_const.COMPONENT_SLOT_CNT_PER_PART):
                        page_dict[str(part)].append(None)

                    page_dict[str(part)][slot_idx] = install_item_no
                used_item_id_list.append(install_item_no)

        global_data.player.upload_component_page_by_dict(self._cur_mecha_id, self._page_index, page_dict)
        self.refresh_ui_show()
        return

    def clear_cur_page(self):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
        dlg = SecondConfirmDlg2()

        def on_confirm():
            dlg.close()
            if global_data.player:
                global_data.player.upload_component_page_by_dict(self._cur_mecha_id, self._page_index, {})
                global_data.game_mgr.show_tip(get_text_by_id(81827))

        dlg.confirm(content=get_text_by_id(81830), confirm_callback=on_confirm)

    def _switch_component_details(self, to_tab):
        self._cur_tab_type = to_tab
        if to_tab == self.TAB_DETAILS:
            is_show = True
            self.panel.nd_content.nd_basic.nd_details.temp_details.setVisible(False)
        else:
            self.panel.nd_content.nd_basic.nd_details.temp_details.setVisible(True)
            is_show = False
        if hasattr(self.panel.nd_content.nd_basic.nd_details, 'temp_num_details') and self.panel.nd_content.nd_basic.nd_details.temp_num_details:
            self.panel.nd_content.nd_basic.nd_details.temp_num_details.setVisible(is_show)
        self.refresh_component_details(self._page_used_item_id_list)

    def refresh_component_details(self, used_item_id_list, sec_used_item_id_list=None):
        self.panel.nd_content.nd_basic.btn_change.SetSelect(self._cur_tab_type == self.TAB_GRAPH)
        self.panel.nd_content.nd_basic.btn_change_detail.SetSelect(self._cur_tab_type == self.TAB_DETAILS)
        if not self.panel.nd_content.nd_basic.nd_details.temp_details.isVisible():
            if not (hasattr(self.panel.nd_content.nd_basic.nd_details, 'temp_num_details') and self.panel.nd_content.nd_basic.nd_details.temp_num_details):
                global_data.uisystem.load_template_create('mech_display/inscription/i_mech_info_inscription_details_num', self.panel.nd_content.nd_basic.nd_details, name='temp_num_details')
            nd = self.panel.nd_content.nd_basic.nd_details.temp_num_details
            inscr_buff_dict = self._page_attr_dict
            inscription_utils.set_ability_list(nd.list_ability, nd.nd_empty, inscr_buff_dict)
        else:
            score_dict = inscription_utils.cal_radar_score(used_item_id_list)
            s_keys = [item_const.INSCR_ATK, item_const.INSCR_FAULT_TOL, item_const.INSCR_SURVIVAL,
             item_const.INSCR_RECOVER, item_const.INSCR_MOB]
            OFFSET = 5
            max_score = MAX_RADAR_AXIS_SCORE + OFFSET
            score_list = [ score_dict.get(k, 0) + OFFSET for k in s_keys ]
            text_list = (81783, 81784, 81785, 81786, 81787)
            if sec_used_item_id_list is None:
                if self._score_list != score_list:
                    self._old_score_list = self._score_list
                    self._score_list = score_list
            score_text = ''
            for index, t_id in enumerate(text_list):
                score_text += get_text_by_id(t_id) + str(score_list[index])

            MechaReconstructWidget.show_radar(self._draw_node, score_list=score_list, max_score=max_score)
            if sec_used_item_id_list:
                _old_score_dict = inscription_utils.cal_radar_score(sec_used_item_id_list)
                _old_score_list = [ _old_score_dict.get(k, 0) + OFFSET for k in s_keys ]
            else:
                _old_score_list = self._old_score_list
            if _old_score_list:
                self._second_draw_node.setVisible(True)
                color = [4427007, 4427007, 4427007, 4427007, 4427007, 4427007]
                opa = 114.75
                MechaReconstructWidget.show_radar(self._second_draw_node, color=color, opacity=opa, score_list=_old_score_list, max_score=max_score)
            else:
                self._second_draw_node.setVisible(False)
        return

    def show(self):
        super(MechaReconstructWidget, self).show()
        if not self._has_first_show:
            self._has_first_show = True

    def hide(self):
        super(MechaReconstructWidget, self).hide()

    def on_buy_good_success(self, item_no):
        from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_NEW_MECHA_COMPONENT
        if item_utils.get_lobby_item_type(item_no) == L_ITEM_TYPE_NEW_MECHA_COMPONENT:
            self._mechaReplaceWidget.on_buy_good_success(item_no)

    def on_slot_unlocked(self, part, slot_idx):
        self.refresh_unlock_lv()
        self.refresh_ui_show()

    def _on_page_name_changed(self, mecha_id, page_idx, name):
        self.refresh_page_para()

    def _on_page_unlock(self, mecha_id):
        if str(self._cur_mecha_id) == str(mecha_id):
            self.refresh_page_para()

    def _on_change_active_page(self, mecha_id, page_idx):
        if str(self._cur_mecha_id) == str(mecha_id):
            self.refresh_ui_show()
            self._mechaReplaceWidget.on_check_component_slot_changed()

    def show_recommend_page(self):
        if not self._mechaPageListWidget.is_visible():
            self._mechaPageListWidget.show_list()
        self._mechaPageListWidget.change_page_type(MechaPageListWidget.PAGE_RECOMMEND)

    def hide_recommend_page(self):
        if self._mechaPageListWidget.is_visible():
            self._mechaPageListWidget.hide_list()
        self._mechaPageListWidget.change_page_type(MechaPageListWidget.PAGE_DATA)