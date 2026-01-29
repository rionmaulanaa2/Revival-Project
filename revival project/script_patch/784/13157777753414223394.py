# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/ItemsBookRoleInfoUI.py
from __future__ import absolute_import
import game3d
import math3d
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gcommon.common_const import scene_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import dress_utils, item_utils, template_utils
from logic.gutils.lobby_model_display_utils import gen_role_seq, get_role_display_cam_data, is_chuchang_scene, get_lobby_model_data
from common.cfg import confmgr
from common.const.uiconst import UI_TYPE_MESSAGE
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.client.const.lobby_model_display_const import CAM_MODE_NEAR, CAM_MODE_FAR, CAM_DISPLAY_PIC, DEFAULT_LEFT, ROLE_VIEW_PIC, ROLE_VIEW_MODEL
import logic.gcommon.const as gconst
from logic.gutils import mall_utils
from logic.gutils import role_utils
from logic.gcommon.item.item_const import FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_OTHER_PENDANT_LIST, FASHION_DECORATION_TYPE_LIST
from logic.client.const.lobby_model_display_const import CHANGE_CAMERA_MODE_CALLBACK_IMMEDIATE, CHANGE_CAMERA_MODE_CALLBACK_ON_END_ANIM, CHANGE_CAMERA_MODE_NONE, CHANGE_CAMERA_MODE_DONT_CHANGE, CHANGE_CAMERA_MODE_KEEP_FAR
from logic.gutils.video_utils import check_play_chuchang_video, get_relative_video_skin_list, get_chuchang_video_path
from logic.comsys.role_profile.ItemsBookWardrobeWidget import ItemsBookWardrobeWidget
from ext_package.ext_decorator import has_skin_ext
from logic.comsys.role_profile.RoleInfoUI import RoleInfoUI, TAG_DRESS, TAG_FILE
from logic.gutils.new_template_utils import SkinCategoryWidget

class ItemsBookRoleInfoUI(RoleInfoUI):

    def on_init_panel(self, *args, **kargs):
        super(ItemsBookRoleInfoUI, self).on_init_panel()
        self.regist_main_ui()
        self.skin_category_widget = None
        self._cur_category_index = 0
        self.panel.nd_tab.setVisible(False)
        self.panel.temp_tab_list.setVisible(False)
        return

    def on_finalize_panel(self):
        super(ItemsBookRoleInfoUI, self).on_finalize_panel()
        self.unregist_main_ui()
        if self.skin_category_widget:
            self.skin_category_widget.destroy()
            self.skin_category_widget = None
        return

    def get_tag_seq(self):
        return [
         TAG_DRESS, TAG_FILE]

    def on_click_btn_last(self, *args):
        if not self.panel.isVisible():
            return
        cur_clothing_id = self.preview_skin or self.force_skin_id
        if cur_clothing_id:
            out_idx = self._cur_category_index
            skin_categpries = self.skin_category_widget.get_skin_categories()
            last_index = len(skin_categpries) - 1 if out_idx == 0 else out_idx - 1
            skins = skin_categpries[last_index][1]
            if skins:
                skin_id = skins[0]
                self._cur_category_index = last_index
                self.force_skin_id = skin_id
                self.preview_skin = 0
                belong_ino = item_utils.get_lobby_item_belong_no(skin_id)
                self.set_role_id(belong_ino)

    def on_click_btn_next(self, *args):
        if not self.panel.isVisible():
            return
        cur_clothing_id = self.preview_skin or self.force_skin_id
        if cur_clothing_id:
            out_idx = self._cur_category_index
            skin_categpries = self.skin_category_widget.get_skin_categories()
            next_index = 0 if out_idx == len(skin_categpries) - 1 else out_idx + 1
            skins = skin_categpries[next_index][1]
            if skins:
                skin_id = skins[0]
                self._cur_category_index = next_index
                self.force_skin_id = skin_id
                self.preview_skin = 0
                belong_ino = item_utils.get_lobby_item_belong_no(skin_id)
                self.set_role_id(belong_ino)

    def set_skin_categories(self, skin_categories):
        if not self.skin_category_widget:
            self.skin_category_widget = SkinCategoryWidget()
        self.skin_category_widget.set_skin_categories(skin_categories)

    def show_skin_details_with_list(self, skin_id, skin_category_list, skins_index):
        self.set_skin_categories(skin_category_list)
        is_visible = len(skin_category_list) > 1
        self.btn_next.setVisible(is_visible)
        self.btn_last.setVisible(is_visible)
        self._cur_category_index = skins_index
        self.force_skin_id = skin_id
        self.preview_skin = 0
        belong_ino = item_utils.get_lobby_item_belong_no(skin_id)
        self.set_role_id(belong_ino)

    def check_show_bond_guide(self):
        return False

    def on_notify_sub_widget(self, widget):
        _, skins = self.skin_category_widget.get_show_skin_category(self.preview_skin or self.force_skin_id)
        if widget:
            if hasattr(widget, 'set_force_skin_list') and widget.set_force_skin_list:
                widget.set_force_skin_list(skins, self.preview_skin or self.force_skin_id)
            else:
                super(ItemsBookRoleInfoUI, self).on_notify_sub_widget(widget)