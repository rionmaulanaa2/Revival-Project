# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinDefineShareFullScreenModelUI.py
from __future__ import absolute_import
import six_ex
from common.uisys.basepanel import BasePanel
from common.const.uiconst import GUIDE_LAYER_ZORDER, UI_VKB_CUSTOM
from common.cfg import confmgr
from logic.gutils.skin_define_utils import get_default_skin_define_anim, init_action_list, delete_action_list
import copy
from logic.gcommon.common_const.scene_const import SCENE_SKIN_DEFINE
from logic.client.const.lobby_model_display_const import SKIN_DEFINE
import math3d
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.lobby_model_display_utils import get_lobby_model_data
from logic.gutils.dress_utils import get_mecha_model_path, get_mecha_model_h_path
from logic.gcommon.common_utils import decal_utils
from logic.gutils.skin_define_utils import get_main_skin_id, load_model_decal_data, load_model_color_data
from common.const.uiconst import UI_TYPE_MESSAGE
from common.utils.cocos_utils import ccp
import cc
from logic.gutils.role_head_utils import init_role_head
from logic.gcommon.common_utils.local_text import get_text_by_id

class SkinDefineShareFullScreenModelUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/mech_define_display'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_back_btn',
       'btn_action.OnClick': 'on_click_action'
       }

    def on_init_panel(self, *args, **kwargs):
        self._callback = None
        self.action_conf = copy.deepcopy(confmgr.get('skin_define_action'))
        self.no_action_tag = True
        self.panel.PlayAnimation('appear')
        self.mecha_id = None
        self.skin_id = 1
        self.panel.temp_btn_use.setVisible(False)
        self.hide_main_ui(exception_types=(UI_TYPE_MESSAGE,))
        self._touch_start_dist = 0
        self._nd_touch_IDs = []
        self._nd_touch_poses = {}
        self.init_touch_event()
        return

    def setBackFunctionCallback(self, callback):
        self._callback = callback

    def on_click_back_btn--- This code section failed: ---

  62       0  LOAD_GLOBAL           0  'delete_action_list'
           3  LOAD_GLOBAL           1  'False'
           6  LOAD_GLOBAL           1  'False'
           9  CALL_FUNCTION_257   257 
          12  POP_TOP          

  63      13  LOAD_FAST             0  'self'
          16  LOAD_ATTR             2  'close'
          19  CALL_FUNCTION_0       0 
          22  POP_TOP          

Parse error at or near `CALL_FUNCTION_257' instruction at offset 9

    def set_designer_info(self, head_frame, head_photo, name, title):
        if head_frame and head_photo:
            self.panel.nd_designer.setVisible(True)
            init_role_head(self.panel.nd_designer.temp_head, head_frame, head_photo)
        self.panel.nd_designer.temp_head.lab_name.SetString(name)
        self.panel.nd_designer.temp_head.SetEnable(False)
        if title != '':
            self.panel.lab_skin_name.SetString(title)
            self.panel.lab_skin_name.setVisible(True)
        else:
            self.panel.lab_skin_name.setVisible(False)

    def set_mecha_info(self, mecha_id, skin_id, color_data, decal_data):
        self.mecha_id = mecha_id
        self.skin_id = skin_id
        self.color_data = color_data
        self.decal_data = decal_data
        mecha_text = confmgr.get('mecha_display', 'HangarConfig', 'Content').get(str(mecha_id), {}).get('name_mecha_text_id', '')
        skin_text = item_utils.get_lobby_item_name(skin_id)
        self.panel.lab_mech_name.SetString(get_text_by_id(mecha_text) + '-' + skin_text)
        self.do_switch_scene()

    def do_switch_scene(self):
        new_scene_type = SCENE_SKIN_DEFINE
        display_type = SKIN_DEFINE

        def on_load_scene(*args):
            camera_ctrl = global_data.game_mgr.scene.get_com('PartSkinDefineCamera')
            if not camera_ctrl:
                return
            else:
                y = 10.0
                y_offset = confmgr.get('skin_define_camera').get(str(self.mecha_id), {}).get('iYOffset', None)
                if not y_offset:
                    log_error('180.xlsx sheet.CameraY => current mecha_id not exit!!!')
                else:
                    y = y_offset
                camera_ctrl.decal_camera_ctrl.center_pos = math3d.vector(0, y, 0)
                camera_ctrl.decal_camera_ctrl._is_active = True
                camera = global_data.game_mgr.scene.active_camera
                camera.position = math3d.vector(0, y, 0)
                camera_ctrl.decal_camera_ctrl.default_pos = math3d.vector(0, y, 0)
                return

        global_data.emgr.show_lobby_relatived_scene.emit(new_scene_type, display_type, finish_callback=on_load_scene, belong_ui_name='SkinDefineShareFullScreenModelUI')
        self.init_model()

    def init_model(self):

        def on_load_model(model, *args):
            global_data.emgr.handle_skin_define_model.emit(get_default_skin_define_anim(self.skin_id), 0)
            if self.color_data:
                self.load_color_data(model, self.skin_id, self.color_data)
            if self.decal_data:
                self.load_decal_data(model, self.skin_id, self.decal_data)
            self.init_action_list()

        item_type = item_utils.get_lobby_item_type(self.skin_id)
        b_show_model = item_type in (L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN)
        if b_show_model and item_type == L_ITEM_TYPE_MECHA_SKIN:
            model_data = get_lobby_model_data(self.skin_id, is_get_player_data=False)
            model_path = get_mecha_model_path(None, self.skin_id)
            submesh_path = get_mecha_model_h_path(None, self.skin_id)
            for data in model_data:
                data['mpath'] = model_path
                data['sub_mesh_path_list'] = [submesh_path]
                data['skin_id'] = self.skin_id

            global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=on_load_model)
        return

    def load_decal_data(self, model, skin_id, decal_list):
        if decal_list and len(decal_list[0]) < 9:
            decal_list = decal_utils.decode_decal_list(decal_list)
        load_model_decal_data(model, skin_id, decal_list, lod_level=0, create_high_quality_decal=True)

    def load_color_data(self, model, skin_id, color_dict):
        if color_dict and isinstance(color_dict, dict):
            color_dict = decal_utils.decode_color(color_dict)
        load_model_color_data(model, skin_id, color_dict)

    def set_action_list_vis(self, is_visible):
        self.panel.btn_action.setVisible(is_visible)

    def on_click_action(self, *args):
        if self.no_action_tag:
            return
        if self.panel.actione_list.isVisible():
            self.hide_action_list()
        else:
            self.show_action_list()

    def show_action_list(self):
        self.panel.actione_list.setVisible(True)
        self.panel.btn_action.img_icon.setRotation(180)

    def hide_action_lsit(self):
        self.panel.actione_list.setVisible(False)
        self.panel.btn_action.img_icon.setRotation(0)

    def init_action_list(self):
        action_list = self.action_conf.get(str(self.skin_id), {}).get('cAction', [])
        if not action_list:
            action_list = self.action_conf.get(str(self.mecha_id), {}).get('cAction', [])
            if not action_list:
                log_error('\xe6\x90\x9e\xe9\x94\xa4\xe5\xad\x90\xef\xbc\x9f \xe8\xa1\xa8\xe9\x83\xbd\xe4\xb8\x8d\xe5\xa1\xab\xef\xbc\x9f')
                self.no_action_tag = True
                self.set_action_list_vis(False)
                return
        self.no_action_tag = False
        init_action_list(self, action_list)

    def on_finalize_panel(self):
        self.panel.PlayAnimation('disappear')
        global_data.emgr.change_model_display_scene_item.emit(None)
        global_data.emgr.leave_current_scene.emit()
        self.show_main_ui()
        if self._callback:
            self._callback()
        self._callback = None
        self._touch_start_dist = 0
        self._nd_touch_IDs = []
        self._nd_touch_poses = {}
        super(SkinDefineShareFullScreenModelUI, self).on_finalize_panel()
        return

    def ui_vkb_custom_func(self):
        self.on_click_back_btn()

    def init_touch_event(self):
        touch_layer = self.panel.nd_mech_touch
        touch_layer.EnableDoubleClick(False)
        touch_layer.BindMethod('OnBegin', self._on_nd_touch_begin)
        touch_layer.BindMethod('OnDrag', self._on_nd_touch_drag)
        touch_layer.BindMethod('OnEnd', self._on_nd_touch_end)

    def _on_nd_touch_begin(self, layer, touch):
        if len(self._nd_touch_IDs) >= 2:
            return False
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._nd_touch_IDs:
            self._nd_touch_poses[tid] = touch_wpos
            self._nd_touch_IDs.append(tid)
        if len(self._nd_touch_IDs) >= 2:
            layer.SetSwallowTouch(True)
            pts = six_ex.values(self._nd_touch_poses)
            self._touch_start_dist = ccp(pts[0].x - pts[1].x, pts[0].y - pts[1].y).getLength()
        else:
            layer.SetSwallowTouch(False)
        return True

    def _on_nd_touch_drag(self, layer, touch):
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._nd_touch_IDs:
            return
        if len(self._nd_touch_IDs) == 1:
            pass
        elif len(self._nd_touch_IDs) >= 2:
            self._nd_touch_poses[tid] = touch_wpos
            pts = six_ex.values(self._nd_touch_poses)
            vec = cc.Vec2(pts[0])
            vec.subtract(pts[1])
            cur_dist = vec.getLength()
            ratio = cur_dist - self._touch_start_dist
            global_data.emgr.skin_define_camera_scale.emit(ratio)

    def _on_nd_touch_end(self, layer, touch):
        tid = touch.getId()
        if tid in self._nd_touch_IDs:
            self._nd_touch_IDs.remove(tid)
            del self._nd_touch_poses[tid]