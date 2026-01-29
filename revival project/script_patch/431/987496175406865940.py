# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/DriverVehicleWidget.py
from __future__ import absolute_import
import six
from logic.gutils import mall_utils
from logic.comsys.items_book_ui.ItemCategoryListWidget import ItemCategoryListWidget
from logic.comsys.items_book_ui.SkinItemListWidget import SkinItemListWidget
from logic.comsys.items_book_ui.SkinGetUseBuyWidget import SkinGetUseBuyWidget
from logic.comsys.items_book_ui.ItemFilterWidget import ItemFilterWidget
from logic.gutils import items_book_utils
from logic.client.const import items_book_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import item_utils
from common.framework import Functor
from logic.gutils import template_utils
from logic.gutils import lobby_model_display_utils
from logic.gutils import red_point_utils
from logic.gutils.skate_appearance_utils import SkateAppearanceAgent
from logic.comsys.common_ui.WidgetExtModelPic import WidgetExtModelPic
from logic.comsys.items_book_ui.ItemsBookOwnBtnWidget import ItemsBookOwnBtnWidget
from logic.comsys.items_book_ui.GlideSceneHelper import GlideSceneHelper
from logic.gcommon.item.item_const import AIRCRAFT_SKIN_TYPE
from logic.comsys.common_ui.MechaTransformUIWidget import MechaTransformUIWidget
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_UNKONW_ITEM
ROTATE_FACTOR = 850
SKATE_LOBBY_ITEM_NO = '1051666'

class DriverVehicleWidget(WidgetExtModelPic):

    def __init__(self, parent, panel):
        self.skate_appearance_agent = None
        super(DriverVehicleWidget, self).__init__(panel)
        self.inited = False
        self.parent = parent
        self.panel = panel
        self.selected_item_no = None
        self.selected_skin_list = None
        self.page_index = items_book_const.VEHICLE_ID
        self.selected_skin_idx = None
        self._glide_scene_helper = None
        self._has_entered_scene = False
        self._own_widget = ItemsBookOwnBtnWidget(self.panel.btn_tick, self.on_click_own_btn)
        self._mecha_transform_ui_widget = MechaTransformUIWidget(self, self.panel)
        self.init_data()
        self.init_scene()
        self.init_widget()
        return

    def on_click_own_btn(self, *args):
        self.update_show_on_condition()

    def init_scene(self):
        if self._has_entered_scene:
            global_data.emgr.clear_glide_sfx_for_lobby_model_event.emit()
            global_data.emgr.change_model_display_scene_item.emit(None)
            global_data.emgr.leave_current_scene.emit()
            self._has_entered_scene = False
        if AIRCRAFT_SKIN_TYPE == self.selected_item_no:
            from logic.gcommon.common_const.scene_const import SCENE_GLIDE_EFFECT
            from logic.client.const.lobby_model_display_const import GLIDE_EFFECT_DISPLAY
            new_scene_type = SCENE_GLIDE_EFFECT
            display_type = GLIDE_EFFECT_DISPLAY

            def on_load_scene(*args):
                camera_ctrl = global_data.game_mgr.scene.get_com('PartModelDisplayFollowCamera')
                if not camera_ctrl:
                    return
                else:
                    if self._glide_scene_helper:
                        if self.selected_skin_list and self.selected_skin_idx is not None:
                            skin_no = self.selected_skin_list[self.selected_skin_idx]
                            _cur_use_glide_effect_id = int(global_data.player.get_aircraft_skin_glide_effect(skin_no))
                            self._glide_scene_helper.show_player_model(skin_no, _cur_use_glide_effect_id)
                    return

            global_data.emgr.show_lobby_relatived_scene.emit(new_scene_type, display_type, finish_callback=on_load_scene, belong_ui_name=self.__class__.__name__)
            global_data.emgr.change_model_display_scene_item.emit(None)
            self._has_entered_scene = True
        else:
            global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.WEAPON_SHOW, scene_content_type=scene_const.SCENE_ITEM_BOOK)
            global_data.emgr.change_model_display_scene_item.emit(None)
            self._has_entered_scene = True
        return

    def do_hide_panel(self):
        if self._glide_scene_helper:
            self._glide_scene_helper.clear()
            global_data.emgr.clear_glide_sfx_for_lobby_model_event.emit()
            global_data.emgr.leave_current_scene.emit()

    def init_data(self):
        self.data_dict = {}
        config = items_book_utils.get_items_conf(self.page_index)
        self.data_dict['vehicle'] = config
        self.init_vehicle_skins()

    def init_vehicle_skins(self):
        skin_dict = {}
        for item_no in six.iterkeys(self.data_dict['vehicle']):
            _skins = items_book_utils.get_items_skins_by_item_no(self.page_index, item_no)
            skins = []
            for skin_id in _skins:
                if not item_utils.can_open_show(skin_id, owned_should_show=True):
                    continue
                skins.append(skin_id)

            skin_dict[item_no] = skins

        self.data_dict['vehicle_skins'] = skin_dict

    def init_widget(self):
        self.update_collect_data()
        self._skin_get_use_buy_widget = SkinGetUseBuyWidget(self, self.panel.btn_buy_1, self.panel.btn_use, self.panel.btn_go, self.panel.temp_price, self.panel.lab_get_method)
        self._skin_list_widget = SkinItemListWidget(self, self.panel.list_skin, self.on_create_skin_item, 6)
        self._category_list_widget = ItemCategoryListWidget(self, self.panel.temp_right_tab, self.data_dict['vehicle'], self.click_category_item_callback, items_book_const.VEHICLE_ID, need_show_outline_pic=True)
        self.init_touch_widget()

    def init_touch_widget(self):
        self.panel.nd_touch.BindMethod('OnDrag', self.on_drag_touch_layer)

    def on_drag_touch_layer(self, btn, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def on_click_skin_item(self, index, *args):
        if not self.panel:
            return
        else:
            prev_index = self.selected_skin_idx
            self.selected_skin_idx = index
            item_widget = self.panel.list_skin.GetItem(index)
            skin_no = self.selected_skin_list[index]
            show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
            model_data = lobby_model_display_utils.get_lobby_model_data(skin_no)
            if skin_no:
                item_type = item_utils.get_lobby_item_type(skin_no)
            else:
                item_type = L_ITEM_TYPE_UNKONW_ITEM
            if self.selected_item_no != AIRCRAFT_SKIN_TYPE:

                def load_cb(l_model):
                    if self.skate_appearance_agent:
                        self.skate_appearance_agent.on_skate_model_loaded(l_model.get_model(), need_handle_common_socket=False)

                self.ext_show_item_model(model_data, in_item_id=skin_no, in_load_callback=load_cb)
            else:
                from ext_package.ext_decorator import has_skin_ext
                from logic.gutils.item_utils import ext_can_show_model
                if not has_skin_ext() and not ext_can_show_model(skin_no, item_type):
                    self.ext_show_item_model(model_data, in_item_id=skin_no)
                elif self._glide_scene_helper:
                    _cur_use_glide_effect_id = int(global_data.player.get_aircraft_skin_glide_effect(skin_no))
                    self._glide_scene_helper.show_player_model(skin_no, _cur_use_glide_effect_id)
            self.panel.lab_name.SetString(items_book_utils.get_filter_item_show_name(self.page_index, self.selected_item_no, skin_no))
            self._mecha_transform_ui_widget.refresh_transform_data_with_lobby_item(skin_no, item_type)
            if show_new:
                global_data.player.req_del_item_redpoint(skin_no)
                red_point_utils.show_red_point_template(item_widget.nd_new, False)
            global_data.emgr.select_item_goods.emit(skin_no)
            prev_item = self.panel.list_skin.GetItem(prev_index)
            if prev_item:
                prev_item.setLocalZOrder(0)
                prev_item.choose.setVisible(False)
            item_widget.setLocalZOrder(2)
            skin_config_dict = items_book_utils.get_items_skin_conf(self.page_index)
            goods_id = skin_config_dict.get(skin_no, {}).get('goods_id', None)
            item_widget.choose.setVisible(True)
            self._skin_get_use_buy_widget.update_target_item_no(self.selected_item_no, skin_no, goods_id)
            item_can_use, _ = mall_utils.item_can_use_by_item_no(skin_no)
            return

    def on_create_skin_item(self, lst, index, item_widget):
        valid = index < len(self.selected_skin_list) and self.selected_item_no
        if valid:
            item_widget.nd_content.setVisible(True)
            skin_no = self.selected_skin_list[index]
            item_widget.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(skin_no))
            item_widget.lab_name.SetString(item_utils.get_lobby_item_name(skin_no))
            item_widget.choose.setVisible(False)
            item_fashion_no = items_book_utils.get_item_fashion_no(self.selected_item_no)
            item_widget.img_using.setVisible(item_fashion_no == int(skin_no))
            item_can_use, limit_left_timestamp = mall_utils.item_can_use_by_item_no(skin_no)
            item_widget.img_lock.setVisible(not item_can_use)
            item_utils.check_skin_tag(item_widget.nd_kind, skin_no)
            item_utils.check_skin_bg_tag(item_widget.img_level, skin_no, is_small_item=True)
            item_widget.bar.SetEnable(True)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
            red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
            template_utils.show_remain_time(item_widget.lab_limited, item_widget.lab_limited, skin_no)
            item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index))
        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.img_level.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)
        if item_widget.nd_empty:
            item_widget.nd_empty.setVisible(not valid)

    def get_show_list_on_condition(self):
        from logic.gutils.items_book_utils import get_sorted_item_list
        all_list = self.data_dict['vehicle_skins'][self.selected_item_no]
        if self._own_widget.get_own_switch():
            selected_skin_list = self._own_widget.get_data_has_own(all_list)
        else:
            selected_skin_list = all_list
        return get_sorted_item_list(selected_skin_list, sort_by_can_use=True)

    def update_show_on_condition(self):
        self.selected_skin_list = self.get_show_list_on_condition()
        self._skin_list_widget.update_skin_data(self.selected_skin_list, False, 0)

    def update_collect_data(self):
        self.collect_dict = {}
        skin_config_dict = items_book_utils.get_items_skin_conf(self.page_index)
        self.collect_count = [0, len(skin_config_dict)]
        for k, v in six.iteritems(self.data_dict['vehicle_skins']):
            item_skin_count = 0
            for skin in v:
                item_can_use, limit_left_timestamp = mall_utils.item_can_use_by_item_no(skin)
                if item_can_use:
                    item_skin_count += 1

            self.collect_dict[k] = (
             item_skin_count, len(v))
            self.collect_count[0] += item_skin_count

        self.update_collect_num()
        self.update_select_item_collect_count()

    def update_collect_num(self):
        if not self.selected_item_no:
            return
        self.panel.nd_sort.lab_collect.SetString('%d/%d' % tuple(self.collect_dict[self.selected_item_no]))

    def refresh_widget(self):
        if self.selected_item_no is None:
            return
        else:
            self.init_scene()
            self.init_data()
            self._category_list_widget.refresh_widget(self.data_dict['vehicle'])
            self.update_collect_num()
            self.update_select_item_collect_count()
            return

    def update_select_item_collect_count(self):
        own_count, all_skin = self.collect_count
        self.panel.temp_prog.lab_got.SetString('%d/%d' % (own_count, all_skin))
        self.panel.temp_prog.prog.SetPercentage(int(own_count / float(all_skin) * 100))

    def click_category_item_callback(self, index, data):
        is_same_item = self.selected_item_no == data[0]
        self.selected_item_no = data[0]
        if self.selected_item_no == SKATE_LOBBY_ITEM_NO:
            self.skate_appearance_agent = SkateAppearanceAgent()
        elif self.skate_appearance_agent:
            self.skate_appearance_agent.destroy()
            self.skate_appearance_agent = None
        if self.selected_item_no == AIRCRAFT_SKIN_TYPE:
            if not self._glide_scene_helper:
                self._glide_scene_helper = GlideSceneHelper('item_books_vehicle')
                self._glide_scene_helper.update_init_rotation(2.92, 0.08)
        elif self._glide_scene_helper:
            self._glide_scene_helper.destroy()
            self._glide_scene_helper = None
        self.init_scene()
        select_idx = is_same_item or 0 if 1 else self.selected_skin_idx
        self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(self.selected_item_no))
        self.selected_skin_list = self.get_show_list_on_condition()
        item_fashion_no = items_book_utils.get_item_fashion_no(self.selected_item_no)
        if select_idx is None or not is_same_item:
            try:
                item_index = self.selected_skin_list.index(str(item_fashion_no))
            except:
                item_index = select_idx

        else:
            item_index = select_idx
        self._skin_list_widget.update_skin_data(self.selected_skin_list, not is_same_item, item_index)
        self.update_collect_num()
        return

    def destroy(self):
        super(DriverVehicleWidget, self).destroy()
        if self.skate_appearance_agent:
            self.skate_appearance_agent.destroy()
            self.skate_appearance_agent = None
        if self._glide_scene_helper:
            self._glide_scene_helper.destroy()
            self._glide_scene_helper = None
        if self._has_entered_scene:
            global_data.emgr.clear_glide_sfx_for_lobby_model_event.emit()
            global_data.emgr.change_model_display_scene_item.emit(None)
            global_data.emgr.leave_current_scene.emit()
            self._has_entered_scene = False
        self.inited = False
        self._category_list_widget.destroy()
        self._category_list_widget = None
        self._skin_list_widget.destroy()
        self._skin_list_widget = None
        self._skin_get_use_buy_widget.destroy()
        self._skin_get_use_buy_widget = None
        if self._own_widget:
            self._own_widget.destroy()
            self._own_widget = None
        self.panel = None
        self.parent = None
        self.data_dict = None
        return

    def jump_to_item_no(self, item_no):
        if not item_no:
            return
        else:
            belong_no = item_utils.get_lobby_item_belong_no(item_no)
            if belong_no:
                index = None
                data_list = [ int(x[0]) for x in self._category_list_widget.data_list ]
                for idx, category_item_no in enumerate(data_list):
                    if int(belong_no) == int(category_item_no):
                        index = idx
                        break

                if index is None:
                    return
                self._category_list_widget.init_select_item(index)
                try:
                    skin_index = self._skin_list_widget.skins_list.index(str(item_no))
                    self._skin_list_widget.init_select_item(skin_index)
                except:
                    return

            return

    def test_all_model(self):

        def check_model_sockets_object(obj, sockets, opt_sockets=()):
            socket_kind = []
            model = obj.get_model()
            for socket in sockets:
                if not model.has_socket(socket):
                    for opt_socket in opt_sockets:
                        if model.has_socket(opt_socket):
                            socket_models = model.get_socket_objects(opt_socket)
                            if socket_models:
                                sub_model = socket_models[0]
                                if sub_model.has_socket(socket):
                                    socket_kind.append([opt_socket, socket])

                else:
                    socket_kind.append([socket])

            return socket_kind

        self.__index = 0

        def check(*args):
            if self.__index < len(self.selected_skin_list):
                item_no = self.selected_skin_list[self.__index]
                self.__index += 1
                model_data = lobby_model_display_utils.get_lobby_model_data(item_no)

                def trk_callback():
                    pass

                def load_cb(l_model, model_data=model_data):
                    global_data.emgr.change_glide_sfx_tag_effect_event.emit(item_no, 203900001)
                    global_data.emgr.play_model_display_track_event.emit('effect/trk/fxq_001.trk', trk_callback, revert=False, time_scale=1.0, is_additive=False)

                self.ext_show_item_model(model_data, in_item_id=item_no, in_load_callback=load_cb)
            else:
                self.panel.StopTimerAction()

        self.panel.TimerAction(check, 1000000, interval=5)