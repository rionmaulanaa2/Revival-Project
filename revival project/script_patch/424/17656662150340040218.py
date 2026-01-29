# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/RoleSkinBuyShowUI.py
from __future__ import absolute_import
import six
from six.moves import range
import math3d
import logic.gcommon.const as gconst
from common.cfg import confmgr
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from common.const.uiconst import UI_TYPE_MESSAGE
from common.uisys.basepanel import BasePanel
from logic.client.const.lobby_model_display_const import CAM_MODE_NEAR, CAM_MODE_FAR, DEFAULT_LEFT, GET_DECORATION_DISPLAY_CAMERA
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_DRESS_PARTS, FASHION_OTHER_PENDANT_LIST, FASHION_DECORATION_TYPE_LIST, FASHION_MAIN_PENDANT_LIST
from logic.gutils import dress_utils, lobby_model_display_utils, template_utils
from logic.gcommon.item import lobby_item_type
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
EXCEPT_HIDE_UI_LIST = []
ROTATE_FACTOR = 850

class RoleSkinBuyShowUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/get_define_display'
    UI_VKB_TYPE = UI_VKB_CLOSE
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_close_btn',
       'nd_mech_touch.OnDrag': '_on_rotate_drag',
       'temp_btn_use.btn_common_big.OnClick': 'on_click_btn_use'
       }
    GLOBAL_EVENT = {'leave_get_model_display_ui': 'show_up'
       }

    def on_init_panel(self, *args, **kargs):
        self.hide_main_ui(exceptions=EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))
        self.role_id = None
        self.top_skin_id = None
        self.preview_decoration = {}
        self.preview_skin = 0
        self.new_skin = 0
        self.preview_decoration = {}
        self.new_decoration = {}
        self._is_in_full_screen_mode = False
        self.cur_cam_mode = CAM_MODE_FAR
        self._close_callback = None
        self.panel.btn_full_screen.BindMethod('OnClick', self.on_click_btn_full_screen)
        self._screen_capture_helper = ScreenFrameHelper()
        ui_display = global_data.ui_mgr.get_ui('GetModelDisplayUI')
        cond_1 = ui_display and ui_display.is_showing_model_item()
        if cond_1:
            self.hide()
        return

    def show_up(self):
        self.show()

    def on_finalize_panel(self):
        if self._close_callback:
            self._close_callback()
            self._close_callback = None
        self.destroy_widget('_screen_capture_helper')
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        global_data.emgr.reset_rotate_model_display.emit()
        self.show_main_ui()
        return

    def set_close_callback(self, cb):
        self._close_callback = cb

    def set_role_top_skin(self, role_id, top_skin_id, preview_skin, new_skin, preview_decoration, new_decoration):
        self.role_id = role_id
        self.top_skin_id = top_skin_id
        self.preview_skin = preview_skin
        self.new_skin = new_skin
        self.preview_decoration = dict(preview_decoration)
        self.new_decoration = new_decoration
        if not self.isPanelVisible():
            return
        self.init_preview_model()
        self.update_ui_show()

    def update_ui_show(self):
        from logic.gcommon.item.lobby_item_type import ITEM_TYPE_DEC
        restrict_info = confmgr.get('pendant', 'SkinRestrict', default={})
        items = global_data.player.get_items_by_type_list(ITEM_TYPE_DEC)
        valid_items = []
        for it in items:
            item_no = it.get_item_no()
            if not restrict_info.get(str(item_no), {}).get('is_invisible_in_list', False):
                valid_items.append(it)

        item_count = len(valid_items)
        self.panel.lab_get.SetString(get_text_by_id(81706, {'num': item_count}))
        all_dec = {}
        all_dec.update(self.preview_decoration)
        all_dec.update(self.new_decoration)
        keys = sorted(six.iterkeys(all_dec))
        sort_decoration = [ all_dec[k] for k in keys ]
        sort_decoration = [ dec_id for dec_id in sort_decoration if not restrict_info.get(str(dec_id), {}).get('is_invisible_in_list', False) ]
        final_skin = self.new_skin or self.preview_skin
        from logic.gutils import item_utils
        name_text = item_utils.get_lobby_item_name(final_skin)
        self.panel.lab_skin_name.SetString(name_text)
        self.panel.img_level.SetDisplayFrameByPath('', item_utils.get_skin_rare_degree_icon(final_skin))
        for idx in range(0, 8):
            ui_item = getattr(self.panel, 'temp_%d' % (idx + 1))
            if ui_item:
                if idx < len(sort_decoration):
                    item_no = sort_decoration[idx]
                    self.init_dec_item(ui_item, item_no)
                else:
                    self.init_dec_item(ui_item, None)

        return

    def init_dec_item(self, ui_item, item_no):
        if item_no:
            from logic.gutils import item_utils
            res_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
            ui_item.img_decorate.SetDisplayFrameByPath('', res_path)
            rare_degress = item_utils.get_item_rare_degree(item_no)
            q_pic = template_utils.get_quality_frame_circle_pic(rare_degress)
            ui_item.frame_circle.SetDisplayFrameByPath('', q_pic)
            rotate_pic = 'gui/ui_res_2/mech_display/frame_reward/frame_rotate_%s.png' % template_utils.QUALITY_COLOR_NAME.get(rare_degress, 'white')
            ui_item.frame_rotate.SetDisplayFrameByPath('', rotate_pic)
            ui_item.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
            is_new = item_no in six.itervalues(self.new_decoration) or item_no == self.new_skin
            ui_item.img_new.setVisible(is_new)
            ui_item.setVisible(True)
        else:
            ui_item.setVisible(False)

    def init_preview_model(self):
        self.update_role_view()

    def on_reset_lobby_model(self):
        self.update_role_view()

    def refresh_relatived_scene(self):
        if self.role_id:
            role_cam_data = lobby_model_display_utils.get_role_display_cam_data(self.role_id, self.preview_skin)
            key = 'far_cam' if self.cur_cam_mode == CAM_MODE_FAR else 'near_cam'
            display_type = str(role_cam_data.get(key, DEFAULT_LEFT))
        else:
            display_type = DEFAULT_LEFT
        from logic.gcommon.common_const import scene_const
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, GET_DECORATION_DISPLAY_CAMERA, scene_content_type=scene_const.SCENE_GET_DECORATION_DISPLAY)

    def do_show_panel(self):
        super(RoleSkinBuyShowUI, self).do_show_panel()
        if self.preview_skin or self.new_skin:
            self.on_reset_lobby_model()
            self.update_ui_show()
        if self.panel.IsVisible():
            self.panel.PlayAnimation('appear')
            self.panel.SetTimeOut(self.panel.GetAnimationMaxRunTime('appear'), lambda : self.panel.PlayAnimation('loop'))

    def on_buy_good_success(self):
        self.check_role_status()

    def update_role_view(self):
        global_data.emgr.change_model_display_scene_item.emit(None)
        self.refresh_relatived_scene()
        model_data = self.get_preview_model_data()
        global_data.emgr.change_model_display_scene_item.emit(model_data)
        return

    def get_preview_model_data(self, other_preview_decoration=None):
        role_id = self.role_id
        skin_id = self.preview_skin
        mpath = dress_utils.get_role_model_path_by_lod(role_id, skin_id, 'h')
        item_no = dress_utils.get_role_item_no(role_id, skin_id)
        preview_decoration = dict(self.preview_decoration)
        if other_preview_decoration:
            preview_decoration.update(other_preview_decoration)
        if mpath is not None:
            head_id = preview_decoration.get(FASHION_POS_HEADWEAR)
            bag_id = preview_decoration.get(FASHION_POS_BACK)
            suit_id = preview_decoration.get(FASHION_POS_SUIT_2)
            other_pendants = [ preview_decoration.get(pos) for pos in FASHION_OTHER_PENDANT_LIST ]
            model_data = lobby_model_display_utils.get_lobby_model_data(item_no, skin_id=self.preview_skin, head_id=head_id, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants)
            return model_data
        else:
            return

    def on_click_close_btn(self, *args):
        self.close()

    def on_click_btn_use(self, *args):

        def cb(*args):
            self.panel.temp_btn_use.setVisible(True)
            self.panel.temp_btn_close.setVisible(True)
            self.panel.btn_full_screen.setVisible(True)

        if self._screen_capture_helper:
            self.panel.temp_btn_use.setVisible(False)
            self.panel.temp_btn_close.setVisible(False)
            self.panel.btn_full_screen.setVisible(False)
            self._screen_capture_helper.take_screen_shot([self.__class__.__name__], self.panel, custom_cb=cb)

    def _on_rotate_drag(self, layer, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def on_click_btn_full_screen(self, *args):
        if not self._is_in_full_screen_mode:
            self.panel.StopAnimation('disappear_full_screen')
            self.panel.StopAnimation('appear_full_screen')
            self.panel.PlayAnimation('appear_full_screen')
        else:
            self.panel.StopAnimation('disappear_full_screen')
            self.panel.StopAnimation('appear_full_screen')
            self.panel.PlayAnimation('disappear_full_screen')
        self._is_in_full_screen_mode = not self._is_in_full_screen_mode