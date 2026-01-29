# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/ItemsBookMechaDetails.py
from __future__ import absolute_import
from logic.gutils import mecha_skin_utils
from logic.client.const.lobby_model_display_const import CAM_MODE_NEAR, CAM_MODE_FAR, ROTATE_FACTOR
from logic.comsys.mecha_display.MechaDetails import MechaDetails
from logic.gutils.new_template_utils import SkinCategoryWidget
from logic.gutils import items_book_utils

class MechaDetailsForItemsBook(MechaDetails):

    def on_init_panel(self, *args, **kwargs):
        self.regist_main_ui()
        self.skin_category_widget = None
        self._cur_category_index = 0
        super(MechaDetailsForItemsBook, self).on_init_panel(*args, **kwargs)
        return

    def on_finalize_panel(self):
        self.unregist_main_ui()
        super(MechaDetailsForItemsBook, self).on_finalize_panel()
        if self.skin_category_widget:
            self.skin_category_widget.destroy()
            self.skin_category_widget = None
        return

    def init_parameters(self):
        super(MechaDetailsForItemsBook, self).init_parameters()
        self.tab_list_data = [
         {'text': 81356,
            'widget_func': self.init_mecha_basic_widget,
            'widget_template': 'mech_display/i_mech_info_basic'
            }]

    def init_tab_list(self):
        super(MechaDetailsForItemsBook, self).init_tab_list()
        self.panel.tab_list.nd_tab_bg.setVisible(False)
        self.panel.tab_list.nd_tab_list.setVisible(False)

    def init_mecha_basic_widget(self, nd):
        from logic.comsys.mecha_display.ItemsBookMechaBasicInfoWidget import ItemsBookMechaBasicInfoWidget
        return ItemsBookMechaBasicInfoWidget(self, nd)

    def set_skin_categories(self, skin_categories):
        if not self.skin_category_widget:
            self.skin_category_widget = SkinCategoryWidget()
        self.skin_category_widget.set_skin_categories(skin_categories)

    def _on_show_last_mecha(self, *args):
        if not self.panel.isVisible():
            return
        else:
            if not global_data.player:
                return
            if not global_data.video_player.is_in_init_state():
                global_data.video_player.stop_video(ignore_cb=True)
            if self._cur_cam_mode == CAM_MODE_NEAR:
                self._cur_cam_mode = CAM_MODE_FAR
                self.refresh_cur_mecha_cam()
            if self.cur_clothing_id:
                out_idx = self._cur_category_index
                skin_categpries = self.skin_category_widget.get_skin_categories()
                last_index = len(skin_categpries) - 1 if out_idx == 0 else out_idx - 1
                skins = skin_categpries[last_index][1]
                if skins:
                    self._cur_category_index = last_index
                    cloth_id = skins[0]
                    self.show_mecha_details(None, False, force_clothing_id=cloth_id)
            return

    def _on_show_next_mecha(self, *args):
        if not self.panel.isVisible():
            return
        else:
            if not global_data.player:
                return
            if not global_data.video_player.is_in_init_state():
                global_data.video_player.stop_video(ignore_cb=True)
            if self._cur_cam_mode == CAM_MODE_NEAR:
                self._cur_cam_mode = CAM_MODE_FAR
                self.refresh_cur_mecha_cam()
            if self.cur_clothing_id:
                out_idx = self._cur_category_index
                skin_categpries = self.skin_category_widget.get_skin_categories()
                next_index = 0 if out_idx == len(skin_categpries) - 1 else out_idx + 1
                skins = skin_categpries[next_index][1]
                if skins:
                    self._cur_category_index = next_index
                    cloth_id = skins[0]
                    self.show_mecha_details(None, False, force_clothing_id=cloth_id)
            return

    def show_skin_details_with_list(self, skin_id, skin_category_list, category_index):
        self.set_skin_categories(skin_category_list)
        self._cur_category_index = category_index
        self.show_mecha_details(None, False, skin_id)
        return

    def on_notify_sub_widget(self, widget):
        _, skins = self.skin_category_widget.get_show_skin_category(self.cur_clothing_id)
        if widget:
            widget.on_switch_skin_category(skins, self.cur_clothing_id)

    def set_cur_clothing_id(self, clothing_id):
        super(MechaDetailsForItemsBook, self).set_cur_clothing_id(clothing_id)
        old_clothing_id = self.cur_clothing_id
        self.cur_clothing_id = clothing_id
        self._cur_mecha_id = mecha_skin_utils.get_mecha_battle_id_by_skin_id(self.cur_clothing_id)
        self.anim_display_change_widget.on_change_mecha(self._cur_mecha_id, clothing_id)
        if old_clothing_id != self.cur_clothing_id:
            self.anim_display_change_widget.on_change_clothing(self.cur_clothing_id)
        self._update_cur_mecha_cam_data(self._cur_mecha_id, self.cur_clothing_id)


class ItemsBookMechaDetails(MechaDetailsForItemsBook):
    pass