# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/MechaCallSfxListWidget.py
from __future__ import absolute_import
import six_ex
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, battle_id_to_mecha_lobby_id
from logic.gutils import red_point_utils
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.comsys.items_book_ui.ItemsBookOwnBtnWidget import ItemsBookOwnBtnWidget
from logic.gutils.skin_define_utils import get_default_skin_define_anim, init_action_list, delete_action_list
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.lobby_model_display_utils import get_lobby_model_data
from logic.gutils.dress_utils import get_mecha_model_path, get_mecha_model_h_path

class MechaCallSfxListWidget(object):

    def __init__(self, parent, panel):
        self.inited = False
        self.parent = parent
        self.panel = panel
        self._own_widget = ItemsBookOwnBtnWidget(self.panel.btn_tick, self.on_click_own_btn)
        self._org_effect_list = []
        self.process_event(True)
        self.init_param()
        self._cur_mecha_id = None
        self.refresh_widget()
        return

    def destroy(self):
        self.process_event(False)
        if self._own_widget:
            self._own_widget.destroy()
            self._own_widget = None
        self.exit_effect_scene()
        return

    def refresh_widget(self):
        if global_data.player:
            mecha_type = global_data.player.get_lobby_selected_mecha_id()
            mecha_item_id = global_data.player.get_lobby_selected_mecha_item_id()
            clothing_id = global_data.player.get_mecha_fashion(mecha_item_id)
            self.skin_id = clothing_id
            self.on_switch_to_mecha_type(mecha_type)
            self.update_widget(True)
        else:
            self.skin_id = 201800100
            self.on_switch_to_mecha_type(8001)
            self.update_widget(True)

    def do_hide_panel(self):
        self.update_widget(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'role_sfx_chagne': self.on_role_sfx_chagne,
           'player_item_update_event': self._on_buy_good_success
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_param(self):
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._cur_mecha_id = None
        self._cur_select_mecha_effect_id = None
        self._cur_use_mecha_effect_id = None
        self._effect_id_to_index_dict = {}
        self.ori_camera_radius = 5.5 * NEOX_UNIT_SCALE
        return

    def on_switch_to_mecha_type(self, mecha_type):
        if self._cur_mecha_id == mecha_type:
            return
        self._cur_mecha_id = mecha_type
        self.init_mecha_effect_lst()

    def update_widget(self, is_show):
        if is_show:
            self.init_mecha_effect_lst()
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
        self._org_effect_list = []
        for idx, effect_id in enumerate(sorted(six_ex.keys(conf))):
            if not item_utils.can_open_show(effect_id):
                continue
            self._org_effect_list.append(effect_id)

        return

    def init_mecha_effect_lst(self):
        self.init_mecha_effect_data()
        self.update_use_btn_status()
        self._effect_id_to_index_dict = {}
        conf = confmgr.get('display_enter_effect')
        conf = conf.get('Content', {})
        from logic.gutils.items_book_utils import get_sorted_item_list
        all_list = self._org_effect_list
        if self._own_widget.get_own_switch():
            selected_effect_list = self._own_widget.get_data_has_own(all_list)
        else:
            selected_effect_list = all_list
        self._effect_lst = get_sorted_item_list(selected_effect_list, sort_by_can_use=True)
        nd_list = self.panel.list_fx
        nd_list.SetInitCount(len(self._effect_lst))
        nd_list.EnableItemAutoPool(True)
        index = 0
        owned_effect_cnt = 0
        str_cur_select_mecha_effect_id = str(self._cur_select_mecha_effect_id)
        str_cur_use_mecha_effect_id = str(self._cur_use_mecha_effect_id)
        for idx, effect_id in enumerate(self._effect_lst):
            belong_id = item_utils.get_lobby_item_belong_no(effect_id)
            item_widget = nd_list.GetItem(idx)
            item_widget.nd_special.setVisible(False)
            if belong_id:
                if mecha_lobby_id_2_battle_id(belong_id) == self._cur_mecha_id:
                    mecha_id = mecha_lobby_id_2_battle_id(belong_id)
                    item_widget.nd_special.setVisible(True)
                    item_widget.nd_special.lab_mech.SetString(self._mecha_conf[str(mecha_id)].get('name_mecha_text_id', ''))
                else:
                    continue
            if item_widget:
                one_config = conf.get(effect_id, {})
                iconPath = one_config.get('iconPath', '')
                item_widget.img_fx.SetDisplayFrameByPath('', iconPath)
                item_widget.nd_using.setVisible(effect_id == str_cur_use_mecha_effect_id)
                item_widget.btn_choose.SetSelect(effect_id == str_cur_select_mecha_effect_id)
                show_new = global_data.lobby_red_point_data.get_rp_by_no(effect_id)
                red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
                if global_data.player:
                    has = global_data.player.has_item_by_no if 1 else (lambda : False)
                    is_owned = has(int(effect_id))
                    item_widget.nd_lock.setVisible(not is_owned)
                    if is_owned:
                        owned_effect_cnt += 1
                    self._effect_id_to_index_dict[effect_id] = index

                    @item_widget.btn_choose.unique_callback()
                    def OnClick(btn, touch, index=index, item_widget=item_widget, effect_id=effect_id, show_new=show_new):
                        self.change_effect_choose(item_widget, effect_id)
                        if show_new:
                            global_data.player.req_del_item_redpoint(effect_id)
                            red_point_utils.show_red_point_template(item_widget.nd_new, False)

                index += 1

        self.update_effect_cnt(owned_effect_cnt, len(self._org_effect_list))

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
                self.panel.lab_get_method.setVisible(False)
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
                self.panel.lab_get_method.setVisible(True)
                self.panel.lab_get_method.SetString(cur_select_display_enter_config['getMethod'])
            self.panel.temp_btn_use.btn_common.SetText(text)
            item_no = cur_select_display_enter_config['itemNo']
            self.panel.lab_name.SetStringWithAdapt(item_utils.get_lobby_item_name(item_no))
            self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
            self.panel.temp_btn_use.btn_common.SetShowEnable(is_enable_btn)
            return

    def change_effect_choose(self, choose_item_widget=None, effect_id=None):
        all_items = self.panel.list_fx.GetAllItem()
        for item_widget in all_items:
            item_widget.btn_choose.SetSelect(False)

        self._cur_select_mecha_effect_id = effect_id
        choose_item_widget.btn_choose.SetSelect(True)
        conf = confmgr.get('display_enter_effect')
        conf = conf.get('Content', {})
        display_enter_config = conf.get(effect_id, {})
        sound_name = display_enter_config.get('cSfxSoundName', '')
        global_data.emgr.change_model_preview_effect.emit(display_enter_config['lobbyCallOutSfxPath'], sound_name)
        select_sfx = None
        cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
        cur_mecha_item = global_data.player.get_item_by_no(cur_mecha_item_id)
        if cur_mecha_item:
            select_sfx = cur_mecha_item.get_sfx()
        self.update_use_btn_status()
        return

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

    def on_role_sfx_chagne(self, sfx_id, effect_id):
        self._cur_use_mecha_effect_id = effect_id
        self.update_use_btn_status()
        self.play_cur_select_effect()
        all_items = self.panel.list_fx.GetAllItem()
        items_count = len(all_items)
        str_cur_use_mecha_effect_id = str(self._cur_use_mecha_effect_id)
        index = 0
        for effect_id in self._effect_lst:
            if index >= items_count:
                break
            item_widget = all_items[index]
            if item_widget:
                item_widget.nd_using.setVisible(effect_id == str_cur_use_mecha_effect_id)
            index += 1

    def _on_buy_good_success(self):
        self.init_mecha_effect_lst()

    def jump_to_item_no(self, effect_id):
        effect_id = str(effect_id)
        idx = self._effect_id_to_index_dict.get(effect_id, 0)
        item_widget = self.panel.list_fx.GetItem(idx)
        self.panel.list_fx.LocatePosByItem(idx)
        self.change_effect_choose(item_widget, effect_id)
        if global_data.lobby_red_point_data.get_rp_by_no(effect_id):
            global_data.player.req_del_item_redpoint(effect_id)
            red_point_utils.show_red_point_template(item_widget.nd_new, False)

    def play_cur_select_effect(self):
        conf = confmgr.get('display_enter_effect')
        conf = conf.get('Content', {})
        display_enter_config = conf.get(str(self._cur_select_mecha_effect_id), {})
        sound_name = display_enter_config.get('cSfxSoundName', '')
        if not display_enter_config.get('lobbyCallOutSfxPath'):
            return
        global_data.emgr.change_model_preview_effect.emit(display_enter_config['lobbyCallOutSfxPath'], sound_name)

    def update_effect_cnt(self, owned_cnt, total_cnt):
        self.panel.lab_collect.SetString('{0}/{1}'.format(owned_cnt, total_cnt))
        self.panel.temp_prog.lab_got.SetString('%d/%d' % (owned_cnt, total_cnt))
        self.panel.temp_prog.prog.SetPercentage(int(owned_cnt / float(total_cnt) * 100))

    def mock_click_use_effect(self):
        self._on_click_use_effect()

    def get_cur_select_mecha_effect_id(self):
        return self._cur_select_mecha_effect_id

    def on_click_own_btn(self, *args):
        self.init_mecha_effect_lst()

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
            camera_ctrl.decal_camera_ctrl._is_active = True
            camera_ctrl.decal_camera_ctrl.radius = 90
            global_data.emgr.enable_decal_camera_scl.emit(False)

        global_data.emgr.show_lobby_relatived_scene.emit(new_scene_type, display_type, finish_callback=on_load_scene, belong_ui_name='MechaCallSfxListWidget')
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