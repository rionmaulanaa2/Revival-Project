# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/ItemsBookPageTabWidget.py
from __future__ import absolute_import
import six_ex
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import items_book_utils
from logic.client.const import items_book_const
from logic.gcommon.item import lobby_item_type
from common.cfg import confmgr
from logic.gutils import red_point_utils
from logic.gutils.system_unlock_utils import is_sys_unlocked, SYSTEM_CREDIT, SYSTEM_CAREER, show_sys_unlock_tips
PAGE_RP_TYPE = {items_book_const.MECHA_ID: [
                             lobby_item_type.L_ITEM_TYPE_MECHA_SKIN],
   items_book_const.ROLE_ID: [
                            lobby_item_type.L_ITEM_TYPE_ROLE_SKIN],
   items_book_const.WEAPON_ID: [
                              lobby_item_type.L_ITME_TYPE_GUNSKIN],
   items_book_const.VEHICLE_ID: [
                               lobby_item_type.L_ITEM_YTPE_VEHICLE_SKIN],
   items_book_const.PERSONALIZATION_ID: [
                                       lobby_item_type.L_ITEM_TYPE_GESTURE, lobby_item_type.L_ITEM_TYPE_EMOTICON,
                                       lobby_item_type.L_ITEM_TYPE_SPRAY, lobby_item_type.L_ITEM_KILL_SFX, lobby_item_type.L_ITEM_MECHA_SFX, lobby_item_type.L_ITEM_GLIDE_EFFECT],
   items_book_const.LOBBY_ID: [
                             lobby_item_type.L_ITEM_TYPE_LOBBY_SKIN, lobby_item_type.L_ITEM_TYPE_MUSIC],
   items_book_const.PET_ID: [
                           lobby_item_type.L_ITEM_TYPE_PET_SKIN]
   }

class ItemsBookPageTabWidget(object):

    def __init__(self, parent):
        self.parent = parent
        self.panel = parent.panel
        self.init_parameters()
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        self.cur_tab_item_widget = None
        self._page_type_to_widget = {}
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'refresh_item_red_point': self.refresh_page_tab
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_page_tab(self):
        tablist = self.panel.tab_list.tab_list
        all_items = tablist.GetAllItem()
        tab_conf = confmgr.get('items_book_conf', 'TabConfig', 'Content')
        tab_type_lst = [ i for i in six_ex.keys(tab_conf) if tab_conf[i].get('is_not_page') != 1 ]
        for index, item_widget in enumerate(all_items):
            tab_type = tab_type_lst[index]
            self.show_red_point(item_widget, tab_type)

    def show_red_point(self, item_widget, tab_type):
        rp_types = PAGE_RP_TYPE.get(tab_type, [])
        show_rp = False
        for i_type in rp_types:
            show_rp = show_rp or global_data.lobby_red_point_data.get_rp_by_type_with_click_time_check(i_type)

        if not show_rp:
            tab_info = items_book_utils.get_items_book_list_widget_info(tab_type)
            tab_cls = tab_info[2]
            if tab_cls and hasattr(tab_cls, 'get_widget_red_points'):
                show_rp = tab_cls.get_widget_red_points()
        red_point_utils.show_red_point_template(item_widget.img_red, show_rp)

    def init_page_tab(self):
        self._page_type_to_widget = {}
        tab_conf = confmgr.get('items_book_conf', 'TabConfig', 'Content')
        tab_type_lst = [ i for i in six_ex.keys(tab_conf) if tab_conf[i].get('is_not_page') != 1 ]
        tablist = self.panel.tab_list.tab_list
        tablist.SetInitCount(len(tab_type_lst))
        tablist.setSwallowTouches(False)
        all_items = tablist.GetAllItem()
        for index, item_widget in enumerate(all_items):
            tab_type = tab_type_lst[index]
            tab_info = tab_conf.get(tab_type)
            self._page_type_to_widget[tab_type] = item_widget
            if not tab_info:
                continue
            tab_name_id = tab_info.get('tab_name_id')
            item_widget.btn.SetText(get_text_by_id(tab_name_id))
            item_widget.btn.setSwallowTouches(False)
            self.show_red_point(item_widget, tab_type)
            item_widget.btn.EnableCustomState(True)
            if tab_type == items_book_const.MEDAL_ID:
                if not is_sys_unlocked(SYSTEM_CAREER):
                    item_widget.img_lock.setVisible(True)
                    item_widget.btn.SetText('')
                    item_widget.lab_lock.SetString(get_text_by_id(tab_name_id))
                else:
                    item_widget.img_lock.setVisible(False)
                    item_widget.lab_lock.SetString('')

            @item_widget.btn.unique_callback()
            def OnClick(btn, touch, tab_type=tab_type, item_widget=item_widget):
                if tab_type == items_book_const.MEDAL_ID:
                    if SYSTEM_CAREER and not is_sys_unlocked(SYSTEM_CAREER):
                        show_sys_unlock_tips(SYSTEM_CAREER)
                        return False
                if self.cur_tab_item_widget:
                    self.cur_tab_item_widget.btn.SetSelect(False)
                    self.cur_tab_item_widget.StopAnimation('continue')
                    self.cur_tab_item_widget.RecoverAnimationNodeState('continue')
                item_widget.PlayAnimation('click')
                item_widget.btn.SetSelect(True)
                item_widget.RecordAnimationNodeState('continue')
                item_widget.PlayAnimation('continue')
                self.cur_tab_item_widget = item_widget
                self.parent.set_selected_page(tab_type)

    def select_tab_page(self, item_no):
        item_type = items_book_utils.item_no_to_items_book_type(item_no)
        if not item_type:
            return
        self.select_tab_page_by_item_type(item_type)

    def select_tab_page_by_item_type(self, page_type):
        widget = self._page_type_to_widget.get(page_type)
        if widget:
            widget.btn.OnClick(None)
        else:
            tablist = self.panel.tab_list.tab_list
            widget = tablist.GetItem(0)
            widget and widget.btn.OnClick(None)
        return