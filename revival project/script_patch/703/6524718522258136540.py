# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/GlideEffectListFunctionWidget.py
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gutils import red_point_utils
import math3d
import time
from logic.gutils.skin_define_utils import get_default_skin_define_anim, init_action_list, delete_action_list
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.lobby_model_display_utils import get_lobby_model_data
from logic.gutils.dress_utils import get_mecha_model_path, get_mecha_model_h_path
from logic.comsys.items_book_ui.FunctionWidgetBase import FunctionWidgetBase
from common.framework import Functor
from logic.gutils import items_book_utils
from logic.client.const import items_book_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.comsys.common_ui.WidgetExtModelPic import WidgetExtModelPic
from logic.gutils import lobby_model_display_utils
from logic.gcommon.item.item_const import DEFAULT_GLIDE_EFFECT
from logic.gcommon.const import GEV_ONLY_ME, GEV_ONLY_FRIEND, GEV_ALL
from six.moves import range
from ext_package.ext_decorator import has_skin_ext
from logic.comsys.items_book_ui.GlideSceneHelper import GlideSceneHelper
import math
COMMON_KEY = 'common_key'
TITLE_ROW_OTHER = 'TITLE_ROW_OTHER'

class GlideEffectListFunctionWidget(FunctionWidgetBase):

    def __init__(self, parent, panel):
        super(GlideEffectListFunctionWidget, self).__init__(parent, panel)
        self.widget_ext_model_pic = WidgetExtModelPic(panel)
        self.selected_effect_list = []
        self.data_dict = {}
        self.own_func = None
        self._update_timer = None
        self.process_event(True)
        self.init_param()
        self.init_vehicle_skin()
        self.init_vis_check()
        self._glide_scene_helper = GlideSceneHelper()
        return

    def init_vis_check(self):
        from logic.gutils.template_utils import init_common_single_choose
        if global_data.player:
            is_select = global_data.player.glide_effect_visibility == GEV_ONLY_FRIEND
        else:
            is_select = True
        init_common_single_choose(self.panel.temp_choose, self.set_vis_check, is_select)

    def set_vis_check(self, is_enable):
        if global_data.player:
            if is_enable:
                global_data.player.change_glide_effect_visibility(GEV_ONLY_FRIEND)
            else:
                global_data.player.change_glide_effect_visibility(GEV_ALL)

    def init_param(self):
        self._cur_vehicle_skin = None
        self._cur_select_glide_effect_id = None
        self._cur_use_glide_effect_id = None
        self.kind_sfx_dict = {}
        self.kind_sfx_dict_org = {}
        return

    def on_clear_effect(self):
        self.update_widget(False)
        self.panel.temp_choose.setVisible(False)
        all_item = self.parent.get_show_list().GetAllItem()
        for item in all_item:
            self.on_clear_title_item(item)

        self.kind_sfx_dict = {}
        if self._glide_scene_helper:
            self._glide_scene_helper.clear()

    def on_update_scene(self):
        self.update_widget(True)

    def destroy(self):
        if self.widget_ext_model_pic:
            self.widget_ext_model_pic.destroy()
            self.widget_ext_model_pic = None
        self.selected_effect_list = []
        if self._glide_scene_helper:
            self._glide_scene_helper.destroy()
            self._glide_scene_helper = None
        self.data_dict = {}
        self.kind_sfx_dict = {}
        self.kind_sfx_dict_org = {}
        self.own_func = None
        self.process_event(False)
        self.exit_effect_scene()
        super(GlideEffectListFunctionWidget, self).destroy()
        return

    def set_data(self, data_list, data_dict, own_func=None):
        self.selected_effect_list = data_list
        self.data_dict = data_dict
        self.own_func = own_func
        self.kind_sfx_dict = {}
        self.kind_sfx_dict_org = {}

    def init_vehicle_skin(self):
        if global_data.player:
            parachute_type = '1051668'
            item_fashion_no = global_data.player.get_glide_show_aircaft_id() or items_book_utils.get_item_fashion_no(parachute_type)
            skin_id = item_fashion_no
            self.on_switch_to_parachute_type(skin_id)
            global_data.player.set_glide_show_aircaft_id(None)
        else:
            skin_id = 208200300
            self.on_switch_to_parachute_type(skin_id)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'vehicle_sfx_chagne': self.on_vehicle_sfx_chagne,
           'player_item_update_event': self._on_buy_good_success
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_vehicle_sfx_chagne(self):
        old_effect_id = self._cur_select_glide_effect_id
        self._cur_use_glide_effect_id = global_data.player.get_aircraft_skin_glide_effect(self._cur_vehicle_skin)
        self.update_use_btn_status()
        self.play_cur_select_effect()
        self.parent.sub_require_refresh_skin_list(self)

    def _on_buy_good_success(self):
        self.init_glide_effect_data()

    def on_switch_to_parachute_type(self, skin_id):
        if self._cur_vehicle_skin == skin_id:
            return
        self._cur_vehicle_skin = skin_id
        self.init_glide_effect_data()

    def update_widget(self, is_show):
        if is_show:
            self.init_glide_effect_data()
            self.do_switch_scene()
        else:
            self.exit_effect_scene()

    def exit_effect_scene(self):
        self.panel.nd_touch.UnBindMethod('OnDrag')
        if self._glide_scene_helper:
            self._glide_scene_helper.clear()
        global_data.emgr.clear_glide_sfx_for_lobby_model_event.emit()
        global_data.emgr.change_model_display_scene_item.emit(None)
        global_data.emgr.leave_current_scene.emit()
        return

    def init_glide_effect_data(self):
        self._cur_use_glide_effect_id = int(global_data.player.get_aircraft_skin_glide_effect(self._cur_vehicle_skin))
        if self._cur_select_glide_effect_id is None:
            self._cur_select_glide_effect_id = self._cur_use_glide_effect_id
        return

    def get_default_select_item_no(self):
        return str(self._cur_select_glide_effect_id)

    def preprocess_data(self, data_list, own_func):
        aircraft_sfx_dict, sorted_aircraft_sfx_keys = self.get_all_aircraft_sfx_dict(data_list, own_func)
        count_per_row = self.parent.get_show_list().GetNumPerUnit()
        result_data_list = []
        for aircraft_id in sorted_aircraft_sfx_keys:
            glide_list = aircraft_sfx_dict[aircraft_id]
            if len(glide_list) % count_per_row != 0:
                glide_list.extend([None] * (count_per_row - len(glide_list) % count_per_row))
            result_data_list.extend(glide_list)

        return result_data_list

    def get_all_aircraft_sfx_dict(self, data_list, own_func):

        def get_sort_id(x):
            return confmgr.get('glide_effect_conf', 'GlideSkinInfo', 'Content', str(x), 'sort_id', default=0)

        def sort_key_func(x):
            return [
             own_func(x) if x else 0, get_sort_id(x) if x else 0, x or '0']

        glide_conf = confmgr.get('glide_effect_conf', 'GlideSkinInfo', 'Content', default=[])
        aircraft_sfx = {}
        for effect_id in data_list:
            effect_conf = glide_conf.get(effect_id, {})
            bind_aircrafts = effect_conf.get('bind_aircrafts')
            if bind_aircrafts:
                for aircraft_id in bind_aircrafts:
                    if aircraft_id not in aircraft_sfx:
                        aircraft_sfx.setdefault(aircraft_id, [])
                    aircraft_sfx[aircraft_id].append(effect_id)

            else:
                aircraft_sfx.setdefault(COMMON_KEY, [])
                aircraft_sfx[COMMON_KEY].append(effect_id)

        for key in aircraft_sfx.keys():
            glide_list = aircraft_sfx[key]
            aircraft_sfx[key] = sorted(glide_list, key=sort_key_func, reverse=True)

        def key_func(aircraft_id):
            glide_list = aircraft_sfx[aircraft_id]
            has_own_any = any([ own_func(x) for x in glide_list ])
            sort_id = max([ get_sort_id(x) for x in glide_list ])
            return [
             has_own_any, sort_id, aircraft_id]

        sorted_aircraft_sfx_keys = sorted(aircraft_sfx.keys(), key=key_func, reverse=True)
        return (
         aircraft_sfx, sorted_aircraft_sfx_keys)

    def on_create_skin_item(self, lst, index, item_widget):
        if not self.kind_sfx_dict:
            kind_sfx_dict, sorted_kind_keys = self.get_all_aircraft_sfx_dict(self.selected_effect_list, self.own_func)
            self.kind_sfx_dict = {}
            self.kind_sfx_dict_org = kind_sfx_dict
            count_per_row = self.parent.get_show_list().GetNumPerUnit()
            calc_index = 0
            for key in sorted_kind_keys:
                for i in range(count_per_row - 1):
                    self.kind_sfx_dict[calc_index + i + 1] = TITLE_ROW_OTHER

                self.kind_sfx_dict[calc_index] = key
                org_list = [ i for i in kind_sfx_dict[key] if i is not None ]
                len_org_list = len(org_list)
                if len_org_list % count_per_row != 0:
                    len_org_list = len_org_list + count_per_row - len_org_list % count_per_row
                calc_index += len_org_list

        valid = index < len(self.selected_effect_list) and self.selected_effect_list[index] is not None
        item_widget.img_driver_tag.setVisible(False)
        if valid:
            effect_id = self.selected_effect_list[index]
            if item_widget:
                title_info = self.kind_sfx_dict.get(index, None)
                if title_info is not None and len(self.kind_sfx_dict_org) > len([COMMON_KEY]):
                    if title_info != TITLE_ROW_OTHER:
                        nd_kind_title = global_data.uisystem.load_template_create('catalogue/i_catalogue_tail_item', item_widget, name='kind_title')
                        aircraft_id = title_info
                        if aircraft_id != COMMON_KEY:
                            nd_kind_title.lab_title.SetString(item_utils.get_lobby_item_name(aircraft_id))
                        else:
                            nd_kind_title.lab_title.SetString(18801)
                        w, h = item_widget.GetContentSize()
                        item_widget.SetContentSize(w, 166)
                        nd_kind_title.SetPosition(0, 118)
                    else:
                        w, h = item_widget.GetContentSize()
                        item_widget.SetContentSize(w, 166)
                else:
                    w, h = item_widget.GetContentSize()
                    item_widget.SetContentSize(w, 118)
                item_widget.nd_kind.setVisible(True)
                item_widget.img_level.setVisible(True)
                item_widget.nd_content.setVisible(True)
                item_widget.bar.SetEnable(True)
                from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
                img_path = get_lobby_item_pic_by_item_no(effect_id)
                item_widget.item.SetDisplayFrameByPath('', img_path)
                str_cur_use_glide_effect_id = str(self._cur_use_glide_effect_id)
                item_widget.img_using.setVisible(effect_id == str_cur_use_glide_effect_id)
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
            title_info = self.kind_sfx_dict.get(index, None)
            if title_info is not None:
                w, h = item_widget.GetContentSize()
                item_widget.SetContentSize(w, 166)
        if item_widget.nd_empty:
            item_widget.nd_empty.setVisible(not valid)
        return

    def on_create_empty_skin_item(self, lst, index, item_widget):
        title_info = self.kind_sfx_dict.get(index, None)
        if title_info is not None:
            w, h = item_widget.GetContentSize()
            item_widget.SetContentSize(w, 166)
        return

    def on_clear_title_item(self, item_widget):
        if item_widget:
            if item_widget.kind_title:
                item_widget.kind_title.Destroy()
            item_widget.SetContentSize(118, 118)

    def on_click_skin_item(self, index, effect_id, show_new, *args):
        if not self.panel:
            return
        prev_index = self.get_parent_selected_item_index()
        if self.sel_before_cb:
            self.sel_before_cb(prev_index, index)
        item_widget = self.parent.get_show_list().GetItem(index)
        self.change_effect_choose(item_widget, effect_id)
        if show_new:
            global_data.player.req_del_item_redpoint(effect_id)
            red_point_utils.show_red_point_template(item_widget.nd_new, False)
        if self.sel_callback:
            self.sel_callback()

    def update_use_btn_status(self):
        if self._cur_select_glide_effect_id == 0:
            return
        self.panel.temp_btn_use.btn_common.BindMethod('OnClick', self._on_click_use_effect)
        select_sfx = global_data.player.get_aircraft_skin_glide_effect(self._cur_vehicle_skin)
        is_serve_use = select_sfx == self._cur_select_glide_effect_id
        is_enable_btn = not is_serve_use
        sfx_item = global_data.player.get_item_by_no(int(self._cur_select_glide_effect_id))
        vehicle_skin_item = global_data.player.get_item_by_no(int(self._cur_vehicle_skin))
        if sfx_item:
            self.panel.temp_choose.setVisible(True)
            self.panel.temp_btn_use.lab_get_method.setVisible(False)
            if is_serve_use:
                text = get_text_by_id(2213)
            elif vehicle_skin_item:
                text = get_text_by_id(2212)
            else:
                is_enable_btn = False
                text = get_text_by_id(81030)
        else:
            self.panel.temp_choose.setVisible(False)
            if item_utils.can_jump_to_ui(self._cur_select_glide_effect_id):
                text = get_text_by_id(2222)
            else:
                is_enable_btn = False
                text = get_text_by_id(80828)
            self.panel.temp_btn_use.lab_get_method.setVisible(True)
        self.panel.temp_btn_use.btn_common.SetText(text)
        item_no = self._cur_select_glide_effect_id
        self.panel.lab_name.SetStringWithAdapt(item_utils.get_lobby_item_name(item_no))
        self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
        self.panel.temp_btn_use.btn_common.SetShowEnable(is_enable_btn)

    def change_effect_choose(self, choose_item_widget=None, effect_id=None):
        self._cur_select_glide_effect_id = int(effect_id)
        if self._glide_scene_helper:
            self._glide_scene_helper.update_skin_and_glide(self._cur_vehicle_skin, effect_id)
        self.update_use_btn_status()

    def _on_click_use_effect(self, *args):
        item_no = self._cur_select_glide_effect_id
        vehicle_skin_item = global_data.player.get_item_by_no(self._cur_vehicle_skin)
        sfx_item = global_data.player.get_item_by_no(int(item_no))
        if not vehicle_skin_item:
            if sfx_item:
                return
        if not sfx_item:
            item_utils.jump_to_ui(item_no)
            return
        if global_data.player:
            global_data.player.set_aircraft_skin_glide_effect(int(self._cur_vehicle_skin), int(self._cur_select_glide_effect_id))

    def play_cur_select_effect(self):
        if self._glide_scene_helper:
            self._glide_scene_helper.update_skin_and_glide(self._cur_vehicle_skin, self._cur_select_glide_effect_id)

    def do_switch_scene(self):
        self.init_touch_widget()
        from logic.gcommon.common_const.scene_const import SCENE_GLIDE_EFFECT
        from logic.client.const.lobby_model_display_const import GLIDE_EFFECT_DISPLAY
        new_scene_type = SCENE_GLIDE_EFFECT
        display_type = GLIDE_EFFECT_DISPLAY

        def on_load_scene(*args):
            camera_ctrl = global_data.game_mgr.scene.get_com('PartModelDisplayFollowCamera')
            if not camera_ctrl:
                return
            from logic.gutils.item_utils import ext_can_show_model
            if not has_skin_ext() and not ext_can_show_model(self._cur_vehicle_skin):
                self.widget_ext_model_pic.ext_show_item_model({}, in_item_id=self._cur_vehicle_skin)
            else:
                self.widget_ext_model_pic.ext_not_show_no_model()
                if self._glide_scene_helper:
                    self._glide_scene_helper.show_player_model(self._cur_vehicle_skin, self._cur_select_glide_effect_id)

        global_data.emgr.show_lobby_relatived_scene.emit(new_scene_type, display_type, finish_callback=on_load_scene, belong_ui_name=self.__class__.__name__)

    def init_touch_widget(self):
        self.panel.nd_touch.BindMethod('OnDrag', self.on_drag_touch_layer)

    def on_drag_touch_layer(self, btn, touch):
        ROTATE_FACTOR = 850
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def test(self):
        import objgraph
        a = objgraph.by_type('GlideEffectListFunctionWidget')[-1]
        global_data.emgr.play_model_display_track_event.emit('model_new/niudan/xin/camera/danchou.trk', None, reset_init_transform=True)
        global_data.track_cache.clear_cache()
        a.panel.StopTimerAction()
        global_data.emgr.change_model_display_scene_item.emit(None)
        a.init_model()
        return

    def test2(self):
        import objgraph
        a = objgraph.by_type('GlideEffectListFunctionWidget')[-1]
        a.show_player_model()