# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/art_check_ui/ArtCheckMechaDisplayUI.py
from __future__ import absolute_import
import math3d
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel, MAIN_UI_LIST
from common.const import uiconst
from logic.gcommon.common_const import scene_const
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.lobby_model_display_utils import is_chuchang_scene, get_mecha_display_cam_data, get_cam_position
from logic.client.const.lobby_model_display_const import CAM_MODE_NEAR, CAM_MODE_FAR, DEFAULT_LEFT, MECHA_CHUCHANG
from logic.comsys.mecha_display.AnimDisplayChangeWidget import AnimDisplayChangeWidget
EXCEPT_HIDE_UI_LIST = []
HIDE_UI_LIST = {
 'ArtCheckMainUI'}
ROTATE_FACTOR = 850
CAM_DISPLAY = {CAM_MODE_FAR: '3',
   CAM_MODE_NEAR: '9'
   }

class ArtCheckMechaDisplayUI(BasePanel):
    PANEL_CONFIG_NAME = 'art_check/art_check_display'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_role_touch.OnDrag': 'on_rotate_drag',
       'btn_change.OnClick': 'on_click_change'
       }

    def on_init_panel(self, *args, **kargs):
        self.init_panel()
        self.init_parameters()
        self.anim_display_change_widget = AnimDisplayChangeWidget(self.panel, self.panel.btn_change)

    def init_parameters(self):
        self._cur_mecha_id = None
        self.disappearing = False
        self.cur_cam_mode = CAM_MODE_FAR
        self.display_type = CAM_DISPLAY.get(self.cur_cam_mode)
        self._cam_offset = [0, 0, 0]
        self._cur_cam_offset_distance = 0.0
        self._cur_mecha_cam_data = None
        self._cur_scene_content_type = None
        self.cur_model_data = None
        return

    def init_panel(self):
        self.hide_main_ui(ui_list=MAIN_UI_LIST | HIDE_UI_LIST, exceptions=EXCEPT_HIDE_UI_LIST, exception_types=())
        self.panel.btn_glass.setVisible(False)
        self.panel.btn_close.setVisible(False)

    def on_rotate_drag(self, layer, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def _on_cam_pos_scroll_delta(self, delta):
        self._modify_cur_cam_offset_dist(delta)
        self._update_cam_position(is_slerp=True)

    def _update_cam_position(self, is_slerp):
        if is_chuchang_scene():
            return
        else:
            pos = self._get_cam_position(0.0)
            if pos is not None:
                offset_pos = math3d.vector(*self._cam_offset)
                global_data.emgr.change_model_display_scene_cam_pos.emit(pos + offset_pos, is_slerp=is_slerp)
                return True
            return False
            return

    def _get_cam_position(self, offset_dist):
        far, near, length = self._cam_position_bounds
        if far is None or near is None:
            return
        else:
            diff = near - far
            if diff.length_sqr < offset_dist * offset_dist:
                return math3d.vector(near)
            if offset_dist < 0:
                return math3d.vector(far)
            direction = math3d.vector(diff)
            if direction.is_zero:
                return
            direction.normalize()
            offset = direction * offset_dist
            return far + offset
            return

    def _update_cur_mecha_cam_data(self, mecha_id):
        self._cur_mecha_cam_data = get_mecha_display_cam_data(str(mecha_id))
        self._try_update_cam_position_bounds()
        self._cur_cam_offset_distance = 0.0

    def _try_update_cam_position_bounds(self):
        far_display_type = str(self._cur_mecha_cam_data['far_cam'])
        near_display_type = str(self._cur_mecha_cam_data['near_cam'])
        near_mid_display_type = str(self._cur_mecha_cam_data['near_mid_cam'])
        self._cam_offset = [0, self._cur_mecha_cam_data.get('cam_voffset', 0), 0]
        skin_offset = self._cur_mecha_cam_data.get('skin_offset', None)
        if skin_offset:
            self._cam_offset = skin_offset
        far_pos = get_cam_position(self._cur_scene_content_type, far_display_type)
        near_pos = get_cam_position(self._cur_scene_content_type, near_display_type)
        near_mid_pos = get_cam_position(self._cur_scene_content_type, near_mid_display_type)
        self._cam_position_bounds = (far_pos, near_pos, (far_pos - near_pos).length)
        return

    def load_scene(self, scene_path=None):
        display_type = DEFAULT_LEFT
        if self._cur_mecha_cam_data:
            if self.cur_cam_mode == CAM_MODE_FAR:
                key = 'far_cam' if 1 else 'near_cam'
                display_type = str(self._cur_mecha_cam_data[key])
            if scene_path is not None:
                global_data.emgr.show_disposable_lobby_relatived_scene.emit(scene_const.SCENE_SKIN_ZHANSHI, scene_path, display_type, belong_ui_name='MechaDetails')
                cur_scene_content_type = scene_const.SCENE_SKIN_ZHANSHI
                async_load = False
            else:
                cur_scene_content_type = scene_const.SCENE_ZHANSHI_MECHA
                global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, str(display_type), finish_callback=self._on_change_scene, scene_content_type=cur_scene_content_type, belong_ui_name='MechaDetails', is_slerp=False)
                async_load = True
            self._cur_scene_content_type = cur_scene_content_type
            async_load or self._update_cam_position(is_slerp=False)
        return

    def change_lobby_model_display(self, model_data, load_model_cb=None, chuchang_trk=None, chuchang_scn=None):
        self._cur_mecha_id = model_data[0]['mecha_id']
        self._update_cur_mecha_cam_data(self._cur_mecha_id)
        self.anim_display_change_widget.on_change_mecha(self._cur_mecha_id, None)
        self.anim_display_change_widget.set_cur_anim_index(0)
        self.load_scene()
        if chuchang_trk:
            for data in model_data:
                data['by_mecha_chuchang'] = True
                data['end_anim'] = None

            scene_type = scene_const.SCENE_MECHA_CHUCHANG
            scene_path = chuchang_scn or confmgr.get('script_gim_ref', 'default_chuchang_scene_path')
            display_type = MECHA_CHUCHANG
            global_data.emgr.show_disposable_lobby_relatived_scene.emit(scene_type, scene_path, display_type)
            global_data.emgr.set_mecha_chuchang_trk.emit(chuchang_trk, True)

            def create_callback(model):
                if callable(load_model_cb):
                    load_model_cb(model)
                show_anim = model_data[0]['show_anim']

                def trk_end(*args):
                    transition_ui = global_data.ui_mgr.get_ui('BlackFadeUI')
                    if not transition_ui:
                        from logic.comsys.mecha_display.BlackFadeUI import BlackFadeUI
                        transition_ui = BlackFadeUI()
                    transition_ui.show_transition(global_data.emgr.end_mecha_chuchang_scene.emit)

                if model.has_anim(show_anim):
                    model.register_anim_key_event(show_anim, 'end', trk_end)
                    global_data.emgr.play_camera_trk_event.emit(chuchang_trk, left_hand_coordinate=False)
                else:
                    trk_end()

            global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=create_callback)
            self.anim_display_change_widget.stop_forbidden_timer()
            self.anim_display_change_widget.disable_btn_change()
            return
        else:

            def create_callback(model):
                if callable(load_model_cb):
                    load_model_cb(model)

            def try_load_model():
                ret = global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=create_callback)
                if len(ret):
                    self.anim_display_change_widget.refresh_btn_change_forbidden_time()
                    if model_data == self.cur_model_data:
                        global_data.emgr.refresh_mecha_skin_res_appearance.emit()
                    else:
                        self.cur_model_data = model_data
                else:
                    global_data.game_mgr.next_exec(try_load_model)

            try_load_model()
            if len(model_data) > 0:
                first_model_data = model_data[0]
                self._display_model_info = {'model_path': first_model_data.get('mpath'),'sub_mesh_path_list': first_model_data.get('sub_mesh_path_list', [])}
            return

    def _on_change_scene(self, scene_type):
        self._update_cam_position(is_slerp=False)

    def on_click_change(self, btn, touch):
        self.anim_display_change_widget.on_click_change()

    def _on_click_back_btn(self, *args):
        if self.disappearing:
            return
        self.disappearing = True
        global_data.emgr.reset_rotate_model_display.emit()
        self.close()

    def on_reset_lobby_model(self):
        if self._cur_mecha_id is not None:
            self.change_lobby_model_display(self._cur_mecha_id, self.cur_clothing_id)
        else:
            cur_scene_content_type = scene_const.SCENE_ZHANSHI_MECHA
            global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, DEFAULT_LEFT, finish_callback=self._on_change_scene, scene_content_type=cur_scene_content_type, belong_ui_name='MechaDetails')
            self._cur_scene_content_type = cur_scene_content_type
        return

    def on_finalize_panel(self):
        super(ArtCheckMechaDisplayUI, self).on_finalize_panel()
        global_data.emgr.change_model_display_scene_item.emit(None)
        global_data.game_mgr.next_exec(global_data.emgr.leave_current_scene.emit)
        global_data.emgr.change_mecha_view_type.emit(False)
        self.show_main_ui()
        return