# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEBookWidgetUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gcommon.common_const.scene_const import SCENE_PVE_BOOK_WIDGET_UI
from logic.client.const.lobby_model_display_const import PVE_BOOK_WIDGET_UI
from logic.gcommon.common_const.pve_const import PVE_BOOK_KEY, PVE_BOOK_DEFAULT_BG_PATH
from logic.gutils.item_utils import get_all_lobby_item_by_item_type
from logic.gutils.pve_utils import reset_model_and_cam_pos
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from .PVEBookMonsterWidget import PVEBookMonsterWidget
from .PVEBookBlessWidget import PVEBookBlessWidget
from .PVEBookBreakWidget import PVEBookBreakWidget
import six_ex

class PVEBookWidgetUI(BasePanel):
    DELAY_CLOSE_TAG = 20240105
    PANEL_CONFIG_NAME = 'catalogue/catalogue_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, *args, **kwargs):
        super(PVEBookWidgetUI, self).on_init_panel()
        self.init_params()
        self.init_ui_events()
        self.do_switch_scene()
        self.process_events(True)

    def play_anim(self):
        self.show()
        self.panel.PlayAnimation('in')
        self.hide_main_ui()

    def init_params(self):
        self._disappearing = False
        self._book_bar_wrapper = None
        self._tab_widgets = {}
        self._tab_list = [{'index': 0,'text': 860369,'ui_cls': PVEBookMonsterWidget,'template_path': 'pve/catalogue/i_pve_catalogue_monster','check_redpoint_func': PVEBookWidgetUI.check_monster_red_point}, {'index': 1,'text': 860370,'ui_cls': PVEBookBlessWidget,'template_path': 'pve/catalogue/i_pve_catalogue_energy','check_redpoint_func': PVEBookWidgetUI.check_bless_red_point}, {'index': 2,'text': 860371,'ui_cls': PVEBookBreakWidget,'template_path': 'pve/catalogue/i_pve_catalogue_breakthrough','check_redpoint_func': PVEBookWidgetUI.check_break_red_point}]
        self._tab_btn_dict = {}
        return

    def init_ui(self):
        tab_list = self.panel.tab_list
        tab_list.lab_title.setVisible(False)
        lab_title_pve = tab_list.lab_title_pve
        lab_title_pve.setVisible(True)
        lab_title_pve.setString(get_text_by_id(390))
        self._init_book_bar()
        self._update_tab_red_point()

    def init_ui_events(self):

        @self.panel.top.btn_back.btn_back.unique_callback()
        def OnClick(btn, touch, *args):
            self.play_disappear_anim()

        @self.panel.tab_list.btn_describe.unique_callback()
        def OnClick(btn, touch, *args):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(390, 635414)

    def on_resolution_changed(self):
        super(PVEBookWidgetUI, self).on_resolution_changed()

    def do_switch_scene(self):

        def on_load_scene(*args):
            self.init_ui()

        scene_background_texture = PVE_BOOK_DEFAULT_BG_PATH
        global_data.emgr.show_lobby_relatived_scene.emit(SCENE_PVE_BOOK_WIDGET_UI, PVE_BOOK_WIDGET_UI, finish_callback=on_load_scene, update_cam_at_once=True, belong_ui_name='PVEBookWidgetUI', scene_content_type=SCENE_PVE_BOOK_WIDGET_UI, scene_background_texture=scene_background_texture)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_refresh_pve_book_redpoint': self._update_tab_red_point
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def _init_book_bar(self):
        tab_list = self.panel.tab_list.nd_tab_list.tab_list

        def _init_book_btn(node, data):
            node.btn.SetText(get_text_by_id(data.get('text', '')))
            self._tab_btn_dict[data.get('index')] = node

        def _book_btn_click_cb(ui_item, data, *args):
            index = data.get('index')
            if not self._tab_widgets.get(index):
                template_path = data.get('template_path')
                ui_cls = data.get('ui_cls')
                template_node = global_data.uisystem.load_template_create(template_path, self.panel.temp_content)
                template_node.SetPosition('50%', '50%')
                widget_wrapper = ui_cls(template_node)
                self._tab_widgets[index] = widget_wrapper
            for _index in self._tab_widgets:
                widget = self._tab_widgets[_index]
                if index == _index:
                    widget.show()
                else:
                    widget.hide()

            self._update_tab_red_point()

        self._book_bar_wrapper = WindowTopSingleSelectListHelper(btn_tab_name='btn')
        self._book_bar_wrapper.set_up_list(tab_list, self._tab_list, _init_book_btn, _book_btn_click_cb)
        self._book_bar_wrapper.set_node_click(tab_list.GetItem(0))

    def _update_tab_red_point(self):
        cache_data = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
        for index, btn_tab in six_ex.items(self._tab_btn_dict):
            redpoint_check_func = self._tab_list[index].get('check_redpoint_func')
            if redpoint_check_func:
                btn_tab.img_red.setVisible(redpoint_check_func(cache_data))

    @staticmethod
    def check_red_point():
        cache_data = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
        has_monster_redpoint = PVEBookWidgetUI.check_monster_red_point(cache_data)
        if has_monster_redpoint:
            return True
        has_bless_redpoint = PVEBookWidgetUI.check_bless_red_point(cache_data)
        if has_bless_redpoint:
            return True
        has_break_redpoint = PVEBookWidgetUI.check_break_red_point(cache_data)
        return has_break_redpoint

    @staticmethod
    def check_monster_red_point(self, cache_data=None):
        from logic.gutils.pve_lobby_utils import check_monster_book_redpoint
        return check_monster_book_redpoint(cache_data)

    @staticmethod
    def check_bless_red_point(self, cache_data=None):
        from logic.gutils.pve_lobby_utils import check_all_bless_book_redpoint
        return check_all_bless_book_redpoint(cache_data)

    @staticmethod
    def check_break_red_point(self, cache_data=None):
        from logic.gutils.pve_lobby_utils import check_all_mecha_break_book_redpoint
        return check_all_mecha_break_book_redpoint(cache_data)

    def close(self, *args):
        self.play_disappear_anim()

    def play_disappear_anim(self):
        if self._disappearing:
            return
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime('disappear')

        def delay_call(*args):
            self._disappearing = False
            global_data.ui_mgr.close_ui(self.get_name())
            if global_data.player:
                global_data.emgr.on_pve_mecha_changed.emit(global_data.player.get_pve_select_mecha_id())

        self.panel.StopAnimation('disappear')
        self.panel.DelayCallWithTag(anim_time, delay_call, self.DELAY_CLOSE_TAG)
        self.panel.PlayAnimation('disappear')

    def on_finalize_panel(self):
        self.process_events(False)
        super(PVEBookWidgetUI, self).on_finalize_panel()
        for widget in six_ex.values(self._tab_widgets):
            widget.destroy()
            widget = None

        global_data.emgr.change_model_display_scene_item.emit(None)
        global_data.emgr.leave_current_scene.emit()
        self.show_main_ui()
        reset_model_and_cam_pos(False)
        return