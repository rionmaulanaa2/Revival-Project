# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinImproveWidgetUI.py
from __future__ import absolute_import
import game3d
import math3d
import logic.gcommon.const as gconst
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_MESSAGE
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.client.const import lobby_model_display_const
from logic.gcommon.item import lobby_item_type
from logic.gcommon.common_const import mecha_const
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
from logic.comsys.mecha_display.MechaLobbyModuleWidget import MechaLobbyModuleWidget
from logic.gutils import item_utils
from logic.gutils import dress_utils
from logic.gutils import mecha_skin_utils
from logic.gutils import lobby_model_display_utils
from logic.gutils.screen_effect_utils import create_screen_effect_directly
from logic.gcommon.common_const import scene_const
from logic.gutils.mecha_utils import get_ex_skin_improve_item_no
from logic.gutils.dress_utils import get_mecha_model_h_path, get_mecha_model_path
from logic.gutils.template_utils import init_price_view, show_remain_time
from logic.client.const.lobby_model_display_const import CAM_MODE_NEAR, CAM_MODE_FAR, CAM_DISPLAY_PIC, ROTATE_FACTOR
from logic.vscene.parts.camera.CameraTrkPlayer import CameraTrkPlayer
from logic.comsys.mecha_display.AnimDisplayChangeWidget import AnimDisplayChangeWidget
ICON_PREFIX = 'gui/ui_res_2/battle/mech_main/'
_HASH_DIFFUSE = game3d.calc_string_hash('Tex0')
MECHA_VIEW_MODEL = 0
MECHA_VIEW_PIC = 1
PIC_TEXT_ID = 80820
MODULE_TEXT_ID = 2221
from common.const import uiconst
USE_NEW_BG = False

class SkinImproveWidgetUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/skin_improve'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    HOT_KEY_NEED_SCROLL_SUPPORT = True
    NEED_SCROLL_ALWAYS = True

    def on_init_panel(self):
        self._cur_mecha_id = None
        self._clothing_id = None
        self._cur_mecha_cam_data = None
        self._cur_cam_mode = self._get_init_cam_type()
        self._trk_player = None
        self._cur_view_type = self._get_init_mecha_view_type()
        self._cur_scene_content_type = None
        self.anim_display_change_widget = AnimDisplayChangeWidget(self.panel, self.panel.btn_change)
        self._screen_sfx_id = None
        from .SkinImproveWidget import SkinImproveWidget
        self._skin_improve_widget = SkinImproveWidget(self, self.panel, self.select_ss_level_cb_wrapper, self.panel_close_cb_wrapper, self._on_glass_btn_clicked, self._on_chuchang_btn_clicked, self._get_init_cam_offset_dist())
        self._mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        self.btn_more.setVisible(False)
        self.refresh_view_type_state()
        self._init_ui_event()
        self.hide_main_ui()
        return

    def on_finalize_panel(self):
        self._mecha_skin_conf = None
        if self._screen_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._screen_sfx_id)
            self._screen_sfx_id = None
        self.destroy_widget('anim_display_change_widget')
        self.destroy_widget('_skin_improve_widget')
        if self._trk_player:
            self._trk_player.on_exit()
            self._trk_player = None
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        global_data.emgr.reset_rotate_model_display.emit()
        self.show_main_ui()
        return

    def on_click_close_btn(self):
        self.close()

    def _get_init_mecha_view_type(self):
        ui = global_data.ui_mgr.get_ui('MechaDetails')
        if ui:
            return ui.mecha_view_type
        return MECHA_VIEW_MODEL

    def _get_init_cam_type(self):
        ui = global_data.ui_mgr.get_ui('MechaDetails')
        if ui:
            return ui._cur_cam_mode
        return CAM_MODE_FAR

    def _get_init_cam_offset_dist(self):
        ui = global_data.ui_mgr.get_ui('MechaDetails')
        if ui:
            return ui._cur_cam_offset_distance
        return 0.0

    def _refresh_mecha_display(self, mecha_id, clothing_id, is_change_skin=False, shiny_id=None):
        self.refresh_view_type_state()
        cur_skin_cnf = self._mecha_skin_conf.get(str(self._clothing_id), {})
        self.load_scene(cur_skin_cnf)
        self.update_mecha_img()
        if self._cur_view_type == MECHA_VIEW_PIC:
            global_data.emgr.change_model_display_scene_item.emit(None)
        else:
            self.change_mecha_model(mecha_id, clothing_id, is_change_skin, shiny_id)
        self.refresh_cur_mecha_cam()
        return

    def change_mecha_model(self, mecha_id, clothing_id, is_change_skin, shiny_id):
        item_no = dress_utils.get_mecha_skin_item_no(mecha_id, clothing_id)
        model_data = lobby_model_display_utils.get_lobby_model_data(item_no)
        is_play_show_anim = False
        for data in model_data:
            if not data['mecha_end_ani']:
                continue
            if is_change_skin or not self.panel.isVisible():
                data['show_anim'] = data['mecha_end_ani']
                data['end_anim'] = data['mecha_end_ani']
            else:
                data['show_anim'] = data['mecha_first_ani']
                data['end_anim'] = data['mecha_end_ani']
                is_play_show_anim = True
            data['skin_id'] = clothing_id
            if shiny_id:
                data['shiny_preview'] = shiny_id

        if self._trk_player:
            self._trk_player.on_exit()
            self._trk_player = None

        def create_callback(model, is_play_show_anim=is_play_show_anim, clothing_id=clothing_id, is_change_skin=is_change_skin):
            if is_play_show_anim and mecha_skin_utils.is_ss_level_skin(clothing_id) and not is_change_skin:
                if clothing_id in (201800251, 201800252, 201800253):
                    self.play_camera_trk_anim()
                if mecha_id in (8006, ) and model and model.valid:

                    def animation_cb(*args):
                        screen_sfx = 'effect/fx/mecha/8006/8006_zhanshi_007.sfx'
                        if self._screen_sfx_id:
                            global_data.sfx_mgr.remove_sfx_by_id(self._screen_sfx_id)
                        self._screen_sfx_id = create_screen_effect_directly(screen_sfx)

                    model.unregister_event(animation_cb, 'zhanshi001', 'shopshow02')
                    model.register_anim_key_event('shopshow02', 'zhanshi001', animation_cb)

        global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=create_callback)
        self.anim_display_change_widget.refresh_btn_change_forbidden_time()
        return

    def set_mecha_emoji(self):
        mecha_id = self._cur_mecha_id
        clothing_id = self._clothing_id
        shiny_id = self._shiny_id
        mpath = get_mecha_model_path(mecha_id, clothing_id)
        submesh_path = get_mecha_model_h_path(mecha_id, clothing_id)
        item_no = dress_utils.get_mecha_skin_item_no(mecha_id, clothing_id)
        model_data = lobby_model_display_utils.get_lobby_model_data(item_no)
        honer_count_item_no, _ = get_ex_skin_improve_item_no(clothing_id)
        lobby_item_data = confmgr.get('lobby_item', str(item_no), default={})
        ex_privilege_model_scale = lobby_item_data.get('ex_privilege_model_scale')
        for data in model_data:
            data['mpath'] = mpath
            data['sub_mesh_path_list'] = [submesh_path]
            if clothing_id in (201802152, 201802153, 201802154):
                anim_name = 'idle_s02'
            elif clothing_id == 201801151:
                anim_name = 'j_idle_s01'
            else:
                anim_name = 'idle'
            data['force_end_ani_loop'] = True
            data['show_anim'] = anim_name
            data['end_anim'] = anim_name
            data['skin_id'] = clothing_id
            if shiny_id:
                data['shiny_preview'] = shiny_id
            data['emoji_id'] = honer_count_item_no
            data['mecha_skin_no'] = clothing_id
            data['emoji_scale'] = 0.3
            data['emoji_offset_y'] = -2
            if ex_privilege_model_scale:
                data['model_scale'] = ex_privilege_model_scale

        global_data.emgr.change_model_display_scene_item.emit(model_data)
        self.anim_display_change_widget.refresh_btn_change_forbidden_time()

    def play_camera_trk_anim(self, *args):
        if self._trk_player:
            self._trk_player.on_exit()
        self._trk_player = CameraTrkPlayer()
        track_path = 'effect/fx/mecha/8002/camera/shopshow02.trk'
        self._trk_player.auto_play_track(track_path, None)
        return

    def load_scene(self, skin_cnf):
        scene_path = skin_cnf.get('zhanshi_scene_path')
        display_type = lobby_model_display_const.DEFAULT_LEFT
        if self._cur_mecha_cam_data:
            key = 'far_cam' if self._cur_cam_mode == CAM_MODE_FAR else 'near_cam'
            display_type = str(self._cur_mecha_cam_data[key])
        if scene_path is not None:
            global_data.emgr.show_disposable_lobby_relatived_scene.emit(scene_const.SCENE_SKIN_ZHANSHI, scene_path, display_type, belong_ui_name='SkinImproveWidgetUI')
            cur_scene_content_type = scene_const.SCENE_SKIN_ZHANSHI
            if self._skin_improve_widget:
                self._skin_improve_widget.update_cam_position(is_slerp=False)
        else:
            cur_scene_content_type = scene_const.SCENE_ZHANSHI_UI if USE_NEW_BG else scene_const.SCENE_ZHANSHI
            global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, str(display_type), finish_callback=self._on_change_scene, scene_content_type=cur_scene_content_type, belong_ui_name='SkinImproveWidgetUI')
        self._cur_scene_content_type = cur_scene_content_type
        return

    def _on_change_scene(self, scene_type):
        if self._skin_improve_widget:
            self._skin_improve_widget.on_load_scene()
        from common.utils.ui_utils import s_bg_xRate, s_bg_yRate, s_designWidth, s_designHeight
        if not USE_NEW_BG:
            return
        if not global_data.ex_scene_mgr_agent.is_cur_lobby_relatived_scene(scene_const.SCENE_ZHANSHI_UI):
            return
        self._scene_ui_path = 'mech_display_vx/mech_display_vx_a'
        new_scene = global_data.game_mgr.get_cur_scene()
        background_model = new_scene.get_model('shangcheng_beijing_02_16')
        if background_model and background_model.valid:
            h_w_rate = s_bg_yRate / s_bg_xRate
            old_ui = new_scene.get_ui_panel()
            new_scene.create_ui_panel(self._scene_ui_path, size=(s_designWidth, s_designHeight))
            if not old_ui:
                scene_ui = new_scene.get_ui_panel()
            material = background_model.get_sub_material(0)
            material.set_texture(_HASH_DIFFUSE, 'Tex0', new_scene.get_ui_rt())
            background_model.all_materials.enable_write_alpha = True
            background_model.all_materials.rebuild_tech()
            scale = background_model.scale
            background_model.scale = math3d.vector(scale.x, 0.7 * h_w_rate, 0.52 * h_w_rate)

    def refresh_cur_mecha_cam(self, is_slerp=False):
        if not self._cur_mecha_cam_data:
            return
        if not self._cur_cam_mode:
            return
        self.panel.icon_glass.SetDisplayFrameByPath('', CAM_DISPLAY_PIC[self._cur_cam_mode])
        key = 'far_cam' if self._cur_cam_mode == CAM_MODE_FAR else 'near_cam'
        display_type = str(self._cur_mecha_cam_data[key])
        global_data.emgr.set_lobby_scene_display_type.emit(display_type, is_slerp)
        if self._skin_improve_widget:
            self._skin_improve_widget.update_cam_position(is_slerp=False)

    def _on_glass_btn_clicked(self, *args, **kw):
        if not self._cur_mecha_cam_data:
            return None
        else:
            if self._cur_cam_mode == CAM_MODE_FAR:
                self._cur_cam_mode = CAM_MODE_NEAR
            elif self._cur_cam_mode == CAM_MODE_NEAR:
                self._cur_cam_mode = CAM_MODE_FAR
            global_data.emgr.change_mecha_view_zoom.emit(self._cur_cam_mode)
            self.refresh_cur_mecha_cam(True)
            return self._cur_cam_mode

    def _on_chuchang_btn_clicked(self, *args, **kw):
        pass

    def panel_close_cb_wrapper(self, mecha_id):
        if not global_data.ui_mgr.get_ui('PVEMainUI'):
            global_data.emgr.close_model_display_scene.emit()
            global_data.emgr.leave_current_scene.emit()
        global_data.emgr.mecha_skin_improve_ui_closed.emit(self._cur_mecha_id, self._clothing_id)
        self.close()

    def select_ss_level_cb_wrapper(self, mecha_id, skin_id, shiny_id, is_refresh=False):
        self._clothing_id = skin_id
        self._shiny_id = shiny_id
        self.anim_display_change_widget.on_change_clothing(self._clothing_id)
        if not is_refresh:
            if mecha_id != self._cur_mecha_id:
                return
        self._refresh_mecha_display(self._cur_mecha_id, skin_id, False, shiny_id)

    def on_show_skin_improve(self, cur_mecha_id, c_id):
        if c_id is not None:
            c_id = int(c_id)
        self._cur_mecha_id = cur_mecha_id
        self._clothing_id = c_id
        self._shiny_id = None
        self._skin_improve_widget.set_closing_id(cur_mecha_id, c_id)
        self._update_cur_mecha_cam_data(str(cur_mecha_id))
        self.anim_display_change_widget.on_change_mecha(cur_mecha_id, c_id)
        self.refresh_btn_change()
        self._refresh_mecha_display(self._cur_mecha_id, self._clothing_id, False, self._shiny_id)
        return

    def _update_cur_mecha_cam_data(self, mecha_id):
        self._cur_mecha_cam_data = lobby_model_display_utils.get_mecha_display_cam_data(str(mecha_id))
        if self._skin_improve_widget:
            self._skin_improve_widget.update_cam_data(self._cur_mecha_cam_data, self._cur_scene_content_type)

    def refresh_btn_change(self):
        if self.anim_display_change_widget.get_anim_display_anim_data():
            self.panel.btn_change.setVisible(True)
        else:
            self.panel.btn_change.setVisible(False)

    def do_show_panel(self):
        super(SkinImproveWidgetUI, self).do_show_panel()
        self.on_reset_lobby_model()
        if self._skin_improve_widget:
            self._skin_improve_widget.refresh_model_show()
            self._skin_improve_widget.show()
        self.hide_main_ui()

    def do_hide_panel(self):
        super(SkinImproveWidgetUI, self).do_hide_panel()
        if self._skin_improve_widget:
            self._skin_improve_widget.hide()
        if self._trk_player:
            self._trk_player.on_exit()
            self._trk_player = None
        self.show_main_ui()
        return

    def on_reset_lobby_model(self):
        if self._cur_mecha_id is not None:
            self._refresh_mecha_display(self._cur_mecha_id, self._clothing_id, False, self._shiny_id)
        else:
            cur_scene_content_type = scene_const.SCENE_ZHANSHI_UI if USE_NEW_BG else scene_const.SCENE_ZHANSHI
            global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.DEFAULT_LEFT, finish_callback=self._on_change_scene, scene_content_type=cur_scene_content_type, belong_ui_name='SkinImproveWidgetUI')
            self._cur_scene_content_type = cur_scene_content_type
        return

    def _init_ui_event(self):

        @self.panel.btn_change.callback()
        def OnClick(btn, touch):
            self.anim_display_change_widget.on_click_change()

        @self.panel.btn_pic.callback()
        def OnClick(btn, touch):
            self.switch_mecha_view_type(btn, touch)

    def set_btn_visible(self, visible):
        if visible:
            self.refresh_btn_change()
        else:
            self.panel.btn_change.setVisible(False)
        self.panel.btn_pic.setVisible(visible)
        self.anim_display_change_widget.set_cur_anim_index(0)
        self.anim_display_change_widget.clear_anim_action()
        if visible == False:
            self.panel.nd_mech_pic.setVisible(False)

    def refresh_view_type_state(self):
        self.panel.btn_pic.SetText('')
        if self._cur_view_type == MECHA_VIEW_MODEL:
            self.panel.lab_pic.SetString(get_text_by_id(MODULE_TEXT_ID))
            self.panel.icon_pic.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_visible.png')
        else:
            self.panel.lab_pic.SetString(get_text_by_id(PIC_TEXT_ID))
            self.panel.icon_pic.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_define_equiped.png')

    def refresh_more_list_buttons(self):
        btns_info = [{'name': 80820 if self._cur_view_type == MECHA_VIEW_MODEL else 2221,'OnClick': self.switch_mecha_view_type}]

        def btn_init_cb(btn, info):
            btn.btn_common.SetText(info['name'])

            @btn.btn_common.callback()
            def OnClick(*args):
                self.panel.nd_more.setVisible(False)
                info['OnClick'](*args)

        from logic.gutils import template_utils
        template_utils.init_common_more_btn_list(self.panel.list_button, btns_info, btn_init_cb)

    def update_mecha_img(self):

        def update_btn_show(skin_conf, to_status):
            if not skin_conf.get('chuchang_anim'):
                return

        def update_mecha_pic(skin_conf, to_status):
            self.panel.nd_mech_pic.setVisible(to_status)
            img_path = skin_conf.get('img_path', '')
            self.panel.img_mech.SetDisplayFrameByPath('', img_path)

        is_show = self._cur_view_type == MECHA_VIEW_PIC
        clothing_id = dress_utils.get_mecha_skin_item_no(self._cur_mecha_id, self._clothing_id)
        cur_skin_conf = self._mecha_skin_conf.get(str(clothing_id), {})
        self.panel.btn_glass and self.panel.btn_glass.setVisible(False)
        if is_show:
            update_mecha_pic(cur_skin_conf, True)
            update_btn_show(cur_skin_conf, False)
        else:
            update_mecha_pic(cur_skin_conf, False)
            update_btn_show(cur_skin_conf, True)

    def set_shiny_id(self, shiny_id):
        self._shiny_id = shiny_id

    def get_shiny_id(self):
        return self._shiny_id

    def get_clothing_id(self):
        return self._clothing_id

    def switch_mecha_view_type(self, btn, touch):
        if self._cur_view_type == MECHA_VIEW_MODEL:
            self._cur_view_type = MECHA_VIEW_PIC
        else:
            self._cur_view_type = MECHA_VIEW_MODEL
        global_data.emgr.change_mecha_view_type.emit(self._cur_view_type, self._cur_mecha_id, self._clothing_id, self._shiny_id)
        self._refresh_mecha_display(self._cur_mecha_id, self._clothing_id, False, self._shiny_id)

    def check_can_mouse_scroll(self):
        return bool(self._skin_improve_widget)

    def on_hot_key_mouse_scroll(self, *args, **kw):
        if self._skin_improve_widget:
            self._skin_improve_widget.on_hot_key_mouse_scroll(*args, **kw)