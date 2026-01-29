# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEBookBlessWidget.py
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from logic.gutils.pve_lobby_utils import check_bless_type_book_redpoint
from logic.gutils.item_utils import get_mecha_name_by_id
from logic.gutils.pve_utils import set_bless_elem_type_icon, get_effect_desc_text_without_mecha_info, get_bless_elem_desc, get_bless_elem_attr_conf, get_bless_elem_res
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gcommon.common_const.pve_const import PVE_BOOK_KEY
from .PVEBookCommonWidget import PVEBookCommonWidget
from common.utilities import get_rome_num
from common.cfg import confmgr
import six_ex
import copy
MECHA_ICON_PATH = 'gui/ui_res_2/item/mecha/{}.png'

class PVEBookBlessWidget(PVEBookCommonWidget):

    def init_params(self):
        self._cur_select_tab = None
        self._cur_select_type = None
        self._cur_conf_list = None
        all_bless_conf = copy.deepcopy(confmgr.get('bless_data', default={}))
        self._bless_dict = {}
        self._type_id_list = []
        self._own_bless_dict = {}
        self._is_showing_own = False
        self._all_count = 0
        self._own_count = 0
        book_local_cache = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
        for bless_id, bless_conf in six_ex.items(all_bless_conf):
            if bless_conf.get('limit_inner', 0) == 1 or bless_conf.get('hide_in_gallery', 0) == 1:
                continue
            self._all_count += 1
            bless_conf['bless_id'] = bless_id
            bless_conf['degree'] = 0
            belong_type_id = bless_conf.get('belong_type_id')
            if belong_type_id:
                if self._bless_dict.get(belong_type_id) is None:
                    self._bless_dict[belong_type_id] = []
                    self._type_id_list.append(belong_type_id)
                self._bless_dict[belong_type_id].append(bless_conf)
                has_unlock = global_data.player and global_data.player.has_unlock_bless_book(bless_id)
                if has_unlock:
                    book_cache_key_str = str(bless_id)
                    if book_cache_key_str not in book_local_cache:
                        bless_conf['first_unlock_key'] = book_cache_key_str
                    bless_conf['has_unlock'] = True
                    self._own_count += 1
                    if self._own_bless_dict.get(belong_type_id) is None:
                        self._own_bless_dict[belong_type_id] = []
                    self._own_bless_dict[belong_type_id].append(bless_conf)

        def sort_function(x):
            first_unlock = bool(x.get('first_unlock_key', ''))
            has_unlock = x.get('has_unlock', False)
            bless_id = x.get('bless_id')
            choose_blesses_cnt = global_data.player.get_choose_blesses_cnt(bless_id) if global_data.player else 0
            return (
             first_unlock, has_unlock, choose_blesses_cnt, -int(bless_id))

        for bless_conf_list in six_ex.values(self._bless_dict):
            bless_conf_list.sort(key=lambda x: sort_function(x), reverse=True)

        for bless_conf_list in six_ex.values(self._own_bless_dict):
            bless_conf_list.sort(key=lambda x: sort_function(x), reverse=True)

        bless_type_conf = confmgr.get('pve_catalogue_conf', 'BlessTypeConf', 'Content', default={})

        def type_sort_function(x):
            return bless_type_conf.get(str(x), {}).get('sort', 0)

        self._type_id_list.sort(key=lambda x: type_sort_function(x), reverse=True)
        return

    def init_ui(self):
        super(PVEBookBlessWidget, self).init_ui()
        self._init_bless_bar()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_refresh_pve_book_redpoint': self._update_bless_btn_redpoint
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def _init_bless_bar(self):
        list_tab = self._panel.list_tab

        def _init_bless_btn(node, data):
            node.btn_tab.SetText(get_text_by_id(data))
            self._update_bless_btn_redpoint(node, data)

        def _bless_btn_click_cb(btn_tab, data, index):
            if self._cur_select_tab:
                if self._cur_select_tab.temp_red.isVisible():
                    global_data.emgr.on_refresh_pve_book_redpoint.emit()
            self._cur_select_tab = btn_tab
            self._cur_select_type = data
            self._update_select()

        self._bless_bar_wrapper = WindowTopSingleSelectListHelper()
        self._bless_bar_wrapper.set_up_list(list_tab, self._type_id_list, _init_bless_btn, _bless_btn_click_cb)
        self._bless_bar_wrapper.set_node_click(list_tab.GetItem(0))

    def _update_bless_btn_redpoint(self, btn_tab=None, bless_type=None):
        if not btn_tab:
            btn_tab = self._cur_select_tab
        if not bless_type:
            bless_type = self._cur_select_type
        btn_tab.temp_red.setVisible(check_bless_type_book_redpoint(bless_type))

    def _update_select(self):
        if self._is_showing_own:
            bless_dict = self._own_bless_dict if 1 else self._bless_dict
            self._cur_conf_list = bless_dict.get(self._cur_select_type, {})
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
        cur_bless_conf = self._cur_conf_list[cur_index]
        max_level = cur_bless_conf.get('max_level', 1)
        if max_level == 1:
            self._panel.list_dot_level.setVisible(False)
            self._update_bless_info(cur_index, 1)
        else:
            list_dot_level = self._panel.list_dot_level
            list_dot_level.DeleteAllSubItem()
            list_dot_level.setVisible(True)
            for index in range(max_level):
                level = index + 1
                item = list_dot_level.AddTemplateItem()
                item.lab_level.SetString(get_rome_num(level))
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
        self._update_bless_info(cur_index, level)

    def _update_bless_info(self, cur_index, level):
        cur_bless_conf = self._cur_conf_list[cur_index]
        bless_id = cur_bless_conf['bless_id']
        lab_name = self._panel.lab_name
        lab_name.setVisible(True)
        lab_name.SetString(get_text_by_id(cur_bless_conf.get('name_id')))
        set_bless_elem_type_icon(self._panel.icon_type, bless_id)
        has_unlock = cur_bless_conf.get('has_unlock', False)
        if has_unlock:
            img_item = self._panel.img_item
            img_item.setVisible(True)
            img_item.SetDisplayFrameByPath('', cur_bless_conf.get('icon', ''))
            self._panel.nd_lock.setVisible(False)
            lab_introduce = self._panel.lab_introduce
            lab_introduce.setVisible(True)
            lab_introduce.SetString(get_effect_desc_text_without_mecha_info(cur_bless_conf['desc_id'], cur_bless_conf.get('attr_text_conf', []), level))
            elem_id = cur_bless_conf.get('elem_id', None)
            if elem_id:
                self._panel.bar_describe.setVisible(True)
                self._panel.lab_describe.SetString(get_effect_desc_text_without_mecha_info(get_bless_elem_desc(elem_id), get_bless_elem_attr_conf(elem_id), 1))
            else:
                self._panel.bar_describe.setVisible(False)
            list_mecha = self._panel.list_mecha
            list_mecha.DeleteAllSubItem()
            suggest_mecha = cur_bless_conf.get('suggest_mecha')
            if suggest_mecha:
                self._panel.pnl_recommend.setVisible(True)
                for mecha_id in cur_bless_conf.get('suggest_mecha'):
                    item = list_mecha.AddTemplateItem()
                    lobby_mecha_id = battle_id_to_mecha_lobby_id(mecha_id)
                    item.img_mecha.SetDisplayFrameByPath('', MECHA_ICON_PATH.format(lobby_mecha_id))
                    item.lab_name_mecha.SetString(get_mecha_name_by_id(mecha_id))

            else:
                self._panel.pnl_recommend.setVisible(False)
            list_data = self._panel.list_data
            list_data.DeleteAllSubItem()
            list_data.setVisible(True)
            item = list_data.AddTemplateItem(0)
            item.lab_title.SetString(get_text_by_id(860373))
            choose_blesses_cnt = global_data.player.get_choose_blesses_cnt(bless_id) if global_data.player else 0
            item.lab_data.SetString(str(choose_blesses_cnt))
        else:
            self._show_empty_widget()
        return

    def _show_empty_widget(self):
        self._panel.img_item.setVisible(False)
        self._panel.icon_type.setVisible(False)
        self._panel.nd_lock.setVisible(True)
        self._panel.lab_introduce.setVisible(False)
        self._panel.bar_describe.setVisible(False)
        self._panel.pnl_recommend.setVisible(False)
        self._panel.list_dot_level.setVisible(False)
        self._panel.list_data.setVisible(False)
        self._panel.lab_name.setVisible(False)