# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEBookCommonWidget.py
from logic.gutils.template_utils import WindowTopSingleSelectListHelper, FrameLoaderTemplate
from logic.gutils.item_utils import get_lobby_item_rare_degree_pic_by_rare_degree
from logic.gutils.pve_utils import set_bless_elem_type_icon
from logic.gcommon.common_const.pve_const import PVE_BOOK_KEY
OWN_ICON_PATH_LIST = [
 'gui/ui_res_2/pve/catalogue/common/icon_pve_catalogue_type_1.png', 'gui/ui_res_2/pve/catalogue/common/icon_pve_catalogue_type_0.png']

class PVEBookCommonWidget(object):

    def __init__(self, panel):
        self._panel = panel
        self._cur_select_item = None
        self._cur_select_index = 0
        self._frame_loader_template = None
        self._first_unlock_key_list = []
        self.init_params()
        self.init_ui()
        self.init_ui_event()
        self.process_events(True)
        return

    def init_params(self):
        pass

    def init_ui(self):
        self._init_progress_widget()

    def init_ui_event(self):

        @self._panel.btn_show.unique_callback()
        def OnClick(btn, touch):
            icon_arrow = self._panel.icon_arrow
            list_item = self._panel.list_item
            is_in_expand_mode = icon_arrow.getRotation() == 180
            if is_in_expand_mode:
                icon_arrow.setRotation(0)
                list_item.SetNumPerUnit(2)
                self._panel.PlayAnimation('list_less')
            else:
                icon_arrow.setRotation(180)
                list_item.SetNumPerUnit(4)
                self._panel.PlayAnimation('list_more')
            list_item.FitViewSizeToContainerSize()

        @self._panel.btn_got.unique_callback()
        def OnClick(btn, touch):
            self._is_showing_own = not self._is_showing_own
            icon_path = OWN_ICON_PATH_LIST[0] if self._is_showing_own else OWN_ICON_PATH_LIST[1]
            self._panel.icon_dot.SetDisplayFrameByPath('', icon_path)
            self._cur_select_index = 0
            self._update_select()
            self._panel.list_item.ScrollToTop()

    def process_events(self, is_bind):
        pass

    def _init_progress_widget(self):
        temp_prog = self._panel.temp_prog
        temp_prog.lab_got.SetString('{}/{}'.format(self._own_count, self._all_count))
        temp_prog.prog.SetPercentage(float(self._own_count) / self._all_count * 100)

    def _update_select(self):
        pass

    def _update_list_item(self):
        if self._cur_select_item:
            self._cur_select_item.nd_content.choose.setVisible(False)
            self._cur_select_item = None
        self._destroy_frame_loader_template()
        self._frame_loader_template = FrameLoaderTemplate(self._panel.list_item, len(self._cur_conf_list), self._init_list_item, self._write_local_cache_data)
        return

    def _init_list_item(self, item, cur_index):
        conf = self._cur_conf_list[cur_index]
        degree = conf.get('degree', 0)
        if degree:
            item.img_level.SetDisplayFrameByPath('', get_lobby_item_rare_degree_pic_by_rare_degree(degree, True))
        item.item.SetDisplayFrameByPath('', conf.get('icon', ''))
        lab_name = item.lab_name
        if lab_name:
            item.lab_name.SetString(get_text_by_id(conf.get('type_id')))
        set_bless_elem_type_icon(item.tag, conf.get('bless_id'))
        has_unlock = conf.get('has_unlock', False)
        item.img_lock.setVisible(not has_unlock)
        first_unlock_key = conf.get('first_unlock_key')
        item.temp_red.setVisible(bool(first_unlock_key))
        if first_unlock_key:
            item.PlayAnimation('loop')
            self._first_unlock_key_list.append(first_unlock_key)
            del conf['first_unlock_key']
        btn_choose = item.btn

        @btn_choose.unique_callback()
        def OnClick(btn, touch):
            if self._cur_select_item == item:
                return
            self._on_click_btn_choose(cur_index, item)

        if cur_index == self._cur_select_index:
            self._on_click_btn_choose(cur_index, item)

    def _write_local_cache_data(self):
        if self._first_unlock_key_list:
            archive_data = global_data.achi_mgr.get_general_archive_data()
            old_book_local_cache = archive_data.get_field(PVE_BOOK_KEY, [])
            cur_book_local_cache = old_book_local_cache + self._first_unlock_key_list
            archive_data.set_field(PVE_BOOK_KEY, cur_book_local_cache)
            self._first_unlock_key_list = []

    def _on_click_btn_choose(self, cur_index, item):
        pass

    def _update_cur_select_item(self, item):
        if self._cur_select_item == item:
            return
        else:
            if self._cur_select_item != None:
                self._cur_select_item.nd_content.choose.setVisible(False)
                temp_red = item.temp_red
                if temp_red.isVisible():
                    item.temp_red.setVisible(False)
                    global_data.emgr.on_refresh_pve_book_redpoint.emit()
            self._cur_select_item = item
            self._cur_select_index = self._panel.list_item.GetAllItem().index(item)
            item.nd_content.choose.setVisible(True)
            return

    def show(self):
        self._panel.setVisible(True)

    def hide(self):
        self._panel.setVisible(False)

    def _destroy_frame_loader_template(self):
        if self._frame_loader_template:
            self._frame_loader_template.destroy()
            self._frame_loader_template = None
        return

    def destroy(self):
        self.process_events(False)
        self._panel and self._panel.Destroy()
        self._panel = None
        self._destroy_frame_loader_template()
        return