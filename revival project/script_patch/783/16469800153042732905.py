# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEBookBreakWidget.py
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from logic.gutils.pve_lobby_utils import check_mecha_break_book_redpoint
from logic.gutils.item_utils import get_mecha_name_by_id
from logic.gutils.pve_utils import get_pve_mecha_id_list, get_effect_desc_text
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gcommon.common_const.pve_const import PVE_BOOK_KEY
from .PVEBookCommonWidget import PVEBookCommonWidget
from common.utilities import get_rome_num
from common.cfg import confmgr
import six_ex
import copy
MECHA_ICON_PATH = 'gui/ui_res_2/item/mecha/{}.png'
OWN_ICON_PATH_LIST = [
 'gui/ui_res_2/pve/catalogue/common/icon_pve_catalogue_type_1.png', 'gui/ui_res_2/pve/catalogue/common/icon_pve_catalogue_type_0.png']

class PVEBookBreakWidget(PVEBookCommonWidget):

    def init_params(self):
        self._cur_select_tab = None
        self._cur_select_mecha_type = None
        self._cur_select_btn_dot = None
        self._mecha_id_list = get_pve_mecha_id_list()
        self._cur_conf_list = None
        all_break_conf = copy.deepcopy(confmgr.get('mecha_breakthrough_data', default={}))
        self._break_dict = {}
        self._own_break_dict = {}
        self._is_showing_own = False
        self._all_count = 0
        self._own_count = 0
        book_local_cache = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
        for mecha_id in self._mecha_id_list:
            temp_break_conf = all_break_conf.get(str(mecha_id))
            if temp_break_conf:
                break_conf = []
                own_break_conf = []
                for slot_id, slot_info in six_ex.items(temp_break_conf):
                    slot_info['slot_id'] = slot_id
                    slot_info['icon'] = slot_info.get('1', {}).get('icon', '')
                    self._all_count += 1
                    break_conf.append(slot_info)
                    has_unlock = global_data.player and global_data.player.has_unlock_breakthrough_book(mecha_id, slot_id)
                    if has_unlock:
                        book_cache_key_str = '%s_%s' % (mecha_id, slot_id)
                        if book_cache_key_str not in book_local_cache:
                            slot_info['first_unlock_key'] = book_cache_key_str
                        slot_info['has_unlock'] = True
                        self._own_count += 1
                        own_break_conf.append(slot_info)

                self._break_dict[mecha_id] = break_conf
                self._own_break_dict[mecha_id] = own_break_conf

        def sort_function(x):
            first_unlock = bool(x.get('first_unlock_key', ''))
            has_unlock = x.get('has_unlock', False)
            slot_id = x.get('slot_id', 0)
            return (
             first_unlock, has_unlock, slot_id)

        for break_conf_list in six_ex.values(self._break_dict):
            break_conf_list.sort(key=lambda x: sort_function(x), reverse=True)

        for break_conf_list in six_ex.values(self._own_break_dict):
            break_conf_list.sort(key=lambda x: sort_function(x), reverse=True)

        return

    def init_ui(self):
        super(PVEBookBreakWidget, self).init_ui()
        self._init_break_bar()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_refresh_pve_book_redpoint': self._update_break_btn_redpoint
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def _init_break_bar(self):
        list_tab = self._panel.list_tab

        def _init_break_btn(node, mecha_id):
            node.btn_tab.SetText(get_mecha_name_by_id(mecha_id))
            self._update_break_btn_redpoint(node, mecha_id)

        def _break_btn_click_cb(btn_tab, mecha_id, index):
            if self._cur_select_tab:
                if self._cur_select_tab.temp_red.isVisible():
                    global_data.emgr.on_refresh_pve_book_redpoint.emit()
            self._cur_select_tab = btn_tab
            self._cur_select_mecha_type = mecha_id
            self._update_select()

        self._break_bar_wrapper = WindowTopSingleSelectListHelper()
        self._break_bar_wrapper.set_up_list(list_tab, self._mecha_id_list, _init_break_btn, _break_btn_click_cb)
        self._break_bar_wrapper.set_node_click(list_tab.GetItem(0))

    def _update_break_btn_redpoint(self, btn_tab=None, mecha_id=None):
        if not btn_tab:
            btn_tab = self._cur_select_tab
        if not mecha_id:
            mecha_id = self._cur_select_mecha_type
        btn_tab.temp_red.setVisible(check_mecha_break_book_redpoint(mecha_id))

    def _update_select(self):
        if self._is_showing_own:
            break_dict = self._own_break_dict if 1 else self._break_dict
            self._cur_conf_list = break_dict.get(self._cur_select_mecha_type, {})
            self._cur_select_index = 0
            self._update_list_item()
            self._panel.list_item.ScrollToTop()
            self._cur_conf_list or self._panel.lab_name.SetString('\xef\xbc\x9f\xef\xbc\x9f\xef\xbc\x9f')
            self._show_empty_widget()

    def _on_click_btn_choose(self, cur_index, item):
        self._update_cur_select_item(item)
        self._update_list_dot_level(cur_index)

    def _update_list_dot_level(self, cur_index):
        self._cur_select_btn_dot = None
        list_dot_level = self._panel.list_dot_level
        list_dot_level.DeleteAllSubItem()
        list_dot_level.setVisible(True)
        cur_break_conf = self._cur_conf_list[cur_index]
        for level, break_conf in six_ex.items(cur_break_conf):
            if level == 'slot_id' or level == 'has_unlock' or level == 'first_unlock' or level == 'icon':
                continue
            item = list_dot_level.AddTemplateItem()
            item.lab_level.SetString(get_rome_num(int(level)))
            btn_dot = item.btn_dot
            btn_dot.EnableCustomState(True)

            @btn_dot.unique_callback()
            def OnClick(btn, touch, level=level):
                self._on_click_btn_dot(btn, cur_index, level)

            if int(level) == 1:
                self._on_click_btn_dot(btn_dot, cur_index, 1)

        return

    def _on_click_btn_dot(self, btn, cur_index, level):
        if btn == self._cur_select_btn_dot:
            return
        if self._cur_select_btn_dot:
            self._cur_select_btn_dot.SetSelect(False)
        self._cur_select_btn_dot = btn
        btn.SetSelect(True)
        self._update_break_info(cur_index, level)

    def _update_break_info(self, cur_index, level):
        cur_break_conf = self._cur_conf_list[cur_index][str(level)]
        lab_name = self._panel.lab_name
        lab_name.setVisible(True)
        lab_name.SetString(get_text_by_id(cur_break_conf.get('name_id')))
        lobby_mecha_id = battle_id_to_mecha_lobby_id(int(self._cur_select_mecha_type))
        self._panel.temp_mecha.img_mecha.SetDisplayFrameByPath('', MECHA_ICON_PATH.format(lobby_mecha_id))
        has_unlock = self._cur_conf_list[cur_index].get('has_unlock', False)
        if has_unlock:
            self._panel.bar_describe.setVisible(True)
            self._panel.lab_describe.SetString(get_effect_desc_text(cur_break_conf['desc_id'], cur_break_conf.get('attr_text_conf', []), pve_mecha_base_info={}))
            img_item = self._panel.img_item
            img_item.setVisible(True)
            img_item.SetDisplayFrameByPath('', cur_break_conf.get('icon', ''))
            self._panel.nd_lock.setVisible(False)
            list_data = self._panel.list_data
            list_data.DeleteAllSubItem()
            list_data.setVisible(True)
            item = list_data.AddTemplateItem(0)
            slot_id = self._cur_conf_list[cur_index].get('slot_id')
            item.lab_title.SetString(get_text_by_id(860373))
            choose_break_cnt = global_data.player.get_choose_breakthrough_cnt(self._cur_select_mecha_type, slot_id) if global_data.player else 0
            item.lab_data.SetString(str(choose_break_cnt))
        else:
            self._show_empty_widget()

    def _show_empty_widget(self):
        self._panel.img_item.setVisible(False)
        self._panel.nd_lock.setVisible(True)
        self._panel.bar_lock.setVisible(True)
        self._panel.bar_describe.setVisible(False)
        self._panel.list_dot_level.setVisible(False)
        self._panel.list_data.setVisible(False)
        self._panel.lab_name.setVisible(False)