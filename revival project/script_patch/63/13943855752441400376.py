# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/MechaCallSfxListFunctionWidget.py
from __future__ import absolute_import
import six_ex
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, battle_id_to_mecha_lobby_id
from logic.gutils import red_point_utils
import math3d
from logic.gutils.skin_define_utils import get_default_skin_define_anim, init_action_list, delete_action_list
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.lobby_model_display_utils import get_lobby_model_data
from logic.gutils.dress_utils import get_mecha_model_path, get_mecha_model_h_path
from logic.comsys.items_book_ui.FunctionWidgetBase import FunctionWidgetBase
from common.framework import Functor

class MechaCallsfxListFunctionWidget(FunctionWidgetBase):

    def __init__(self, parent, panel):
        super(MechaCallsfxListFunctionWidget, self).__init__(parent, panel)
        self.selected_skin_list = []
        self.data_dict = {}
        self.process_event(True)
        self.init_param()
        self.init_mecha_skin()

    def init_param(self):
        self._cur_mecha_id = None
        self._cur_select_mecha_effect_id = None
        self._cur_use_mecha_effect_id = None
        return

    def on_clear_effect(self):
        self.update_widget(False)

    def on_update_scene(self):
        self.update_widget(True)

    def destroy(self):
        super(MechaCallsfxListFunctionWidget, self).destroy()
        self.selected_skin_list = []
        self.data_dict = {}
        self.process_event(False)
        self.exit_effect_scene()

    def set_data(self, data_list, data_dict):
        self.selected_skin_list = data_list
        self.data_dict = data_dict

    def init_mecha_skin(self):
        if global_data.player:
            mecha_type = global_data.player.get_lobby_selected_mecha_id()
            mecha_item_id = global_data.player.get_lobby_selected_mecha_item_id()
            clothing_id = global_data.player.get_mecha_fashion(mecha_item_id)
            self.skin_id = clothing_id
            self.on_switch_to_mecha_type(mecha_type)
        else:
            self.skin_id = 201800100
            self.on_switch_to_mecha_type(8001)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'role_sfx_chagne': self.on_role_sfx_chagne
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_role_sfx_chagne(self, sfx_id, effect_id):
        old_effect_id = self._cur_select_mecha_effect_id
        self._cur_use_mecha_effect_id = effect_id
        self.update_use_btn_status()
        self.parent.sub_require_refresh_skin_list(self)

    def on_switch_to_mecha_type(self, mecha_type):
        if self._cur_mecha_id == mecha_type:
            return
        self._cur_mecha_id = mecha_type
        self.init_mecha_effect_data()

    def update_widget(self, is_show):
        if is_show:
            self.init_mecha_effect_data()
            self.do_switch_scene()
        else:
            self.exit_effect_scene()

    def exit_effect_scene(self):
        global_data.emgr.change_model_display_scene_item.emit(None)
        if global_data.feature_mgr.is_support_model_decal():
            global_data.emgr.exit_decal_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        global_data.emgr.enable_decal_camera_scl.emit(True)
        return

    def init_mecha_effect_data(self):
        conf = confmgr.get('display_enter_effect')
        conf = conf.get('Content', {})
        cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
        cur_mecha_item = global_data.player.get_item_by_no(cur_mecha_item_id)
        select_sfx = None
        if cur_mecha_item:
            select_sfx = cur_mecha_item.get_sfx()
        self._cur_use_mecha_effect_id = select_sfx or six_ex.keys(conf)[0]
        if self._cur_select_mecha_effect_id is None:
            self._cur_select_mecha_effect_id = self._cur_use_mecha_effect_id
        return

    def on_create_skin_item(self, lst, index, item_widget):
        valid = index < len(self.selected_skin_list) and self.selected_skin_list[index] is not None
        item_widget.img_driver_tag.setVisible(False)
        if valid:
            effect_id = self.selected_skin_list[index]
            belong_id = item_utils.get_lobby_item_belong_no(effect_id)
            if belong_id:
                log_error('no support for exclusive effect id')
            if item_widget:
                item_widget.nd_kind.setVisible(True)
                item_widget.img_level.setVisible(True)
                item_widget.nd_content.setVisible(True)
                item_widget.bar.SetEnable(True)
                conf = confmgr.get('display_enter_effect')
                conf = conf.get('Content', {})
                one_config = conf.get(effect_id, {})
                iconPath = one_config.get('iconPath', '')
                item_widget.item.SetDisplayFrameByPath('', iconPath)
                str_cur_select_mecha_effect_id = str(self._cur_select_mecha_effect_id)
                str_cur_use_mecha_effect_id = str(self._cur_use_mecha_effect_id)
                item_widget.img_using.setVisible(effect_id == str_cur_use_mecha_effect_id)
                show_new = global_data.lobby_red_point_data.get_rp_by_no(effect_id)
                red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
                has = global_data.player.has_item_by_no if global_data.player else (lambda : False)
                is_owned = has(int(effect_id))
                item_widget.img_lock.setVisible(not is_owned)
                item_utils.check_skin_tag(item_widget.nd_kind, effect_id)
                item_utils.check_skin_bg_tag(item_widget.img_level, effect_id, is_small_item=True)
                item_widget.bar.SetNoEventAfterMove(True)
                item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index, effect_id, show_new))
                item_widget.bar.UnBindMethod('OnBegin')
                item_widget.bar.UnBindMethod('OnDrag')
                item_widget.bar.UnBindMethod('OnEnd')
                item_widget.bar.UnBindMethod('OnCancel')
        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.img_level.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)
            item_widget.bar.UnBindMethod('OnClick')
        if item_widget.nd_empty:
            item_widget.nd_empty.setVisible(not valid)
        return

    def on_click_skin_item(self, index, effect_id, show_new, *args):
        if not self.panel:
            return
        prev_index = self.get_parent_selected_item_index()
        if self.sel_before_cb:
            self.sel_before_cb(prev_index, index)
        item_widget = self.panel.list_item.GetItem(index)
        self.change_effect_choose(item_widget, effect_id)
        if show_new:
            global_data.player.req_del_item_redpoint(effect_id)
            red_point_utils.show_red_point_template(item_widget.nd_new, False)
        if self.sel_callback:
            self.sel_callback()

    def update_use_btn_status(self):
        if self._cur_select_mecha_effect_id == 0:
            return
        else:
            self.panel.temp_btn_use.btn_common.BindMethod('OnClick', self._on_click_use_effect)
            conf = confmgr.get('display_enter_effect')
            conf = conf.get('Content', {})
            cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
            cur_mecha_item = global_data.player.get_item_by_no(cur_mecha_item_id)
            select_sfx = None
            if cur_mecha_item:
                select_sfx = cur_mecha_item.get_sfx()
            cur_select_display_enter_config = conf.get(str(self._cur_select_mecha_effect_id), {})
            is_serve_use = select_sfx == cur_select_display_enter_config['itemNo']
            is_enable_btn = not is_serve_use
            sfx_item = global_data.player.get_item_by_no(cur_select_display_enter_config['itemNo'])
            if sfx_item:
                self.panel.temp_btn_use.lab_get_method.setVisible(False)
                if is_serve_use:
                    text = get_text_by_id(2213)
                else:
                    if cur_mecha_item:
                        text = get_text_by_id(2212)
                    else:
                        is_enable_btn = False
                        text = get_text_by_id(81030)
                    belong_id = item_utils.get_lobby_item_belong_no(self._cur_select_mecha_effect_id)
                    if belong_id:
                        mecha_id = mecha_lobby_id_2_battle_id(belong_id)
                        if mecha_id != self._cur_mecha_id:
                            text = get_text_by_id(81308)
                            is_enable_btn = False
            else:
                if item_utils.can_jump_to_ui(cur_select_display_enter_config['itemNo']):
                    text = get_text_by_id(2222)
                else:
                    is_enable_btn = False
                    text = get_text_by_id(80828)
                self.panel.temp_btn_use.lab_get_method.setVisible(True)
                self.panel.temp_btn_use.lab_get_method.SetString(cur_select_display_enter_config['getMethod'])
            self.panel.temp_btn_use.btn_common.SetText(text)
            item_no = cur_select_display_enter_config['itemNo']
            self.panel.lab_name.SetStringWithAdapt(item_utils.get_lobby_item_name(item_no))
            self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
            self.panel.temp_btn_use.btn_common.SetShowEnable(is_enable_btn)
            return

    def change_effect_choose(self, choose_item_widget=None, effect_id=None):
        self._cur_select_mecha_effect_id = effect_id
        conf = confmgr.get('display_enter_effect')
        conf = conf.get('Content', {})
        display_enter_config = conf.get(effect_id, {})
        sound_name = display_enter_config.get('cSfxSoundName', '')
        global_data.emgr.change_model_preview_effect.emit(display_enter_config['lobbyCallOutSfxPath'], sound_name)
        self.update_use_btn_status()

    def _on_click_use_effect(self, *args):
        conf = confmgr.get('display_enter_effect')
        conf = conf.get('Content', {})
        one_config = conf.get(str(self._cur_select_mecha_effect_id), {})
        cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
        cur_mecha_item = global_data.player.get_item_by_no(cur_mecha_item_id)
        sfx_item = global_data.player.get_item_by_no(one_config['itemNo'])
        if not cur_mecha_item:
            if sfx_item:
                return
        if not sfx_item:
            item_utils.jump_to_ui(one_config['itemNo'])
            return
        from logic.comsys.mecha_display.MechaEnterEffectUseUI import MechaEnterEffectUseUI
        MechaEnterEffectUseUI(mecha_id=self._cur_mecha_id, effect_id=self._cur_select_mecha_effect_id)

    def play_cur_select_effect(self):
        conf = confmgr.get('display_enter_effect')
        conf = conf.get('Content', {})
        display_enter_config = conf.get(str(self._cur_select_mecha_effect_id), {})
        sound_name = display_enter_config.get('cSfxSoundName', '')
        if not display_enter_config.get('lobbyCallOutSfxPath'):
            return
        global_data.emgr.change_model_preview_effect.emit(display_enter_config['lobbyCallOutSfxPath'], sound_name)

    def do_switch_scene(self):
        from logic.gcommon.common_const.scene_const import SCENE_SKIN_DEFINE
        from logic.client.const.lobby_model_display_const import SKIN_DEFINE
        new_scene_type = SCENE_SKIN_DEFINE
        display_type = SKIN_DEFINE

        def on_load_scene(*args):
            camera_ctrl = global_data.game_mgr.scene.get_com('PartSkinDefineCamera')
            if not camera_ctrl:
                return
            pos = math3d.vector(0, 15, 0)
            camera_ctrl.decal_camera_ctrl.center_pos = pos
            camera_ctrl.decal_camera_ctrl.default_pos = pos
            camera_ctrl.decal_camera_ctrl.offset_angle = 8
            camera_ctrl.decal_camera_ctrl._is_active = True
            camera_ctrl.decal_camera_ctrl.radius = 85
            global_data.emgr.enable_decal_camera_scl.emit(False)

        global_data.emgr.show_lobby_relatived_scene.emit(new_scene_type, display_type, finish_callback=on_load_scene, belong_ui_name='MechaCallsfxListFunctionWidget')
        self.init_model()

    def init_model(self):

        def on_load_model(model, *args):
            global_data.emgr.handle_skin_define_model.emit(get_default_skin_define_anim(self.skin_id), 0)

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