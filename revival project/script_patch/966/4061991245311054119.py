# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/WeaponListWidget.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from six.moves import range
from logic.gutils import mall_utils
from logic.comsys.items_book_ui.ItemCategoryListWidget import ItemCategoryListWidget
from logic.comsys.items_book_ui.SkinItemListWidget import SkinItemListWidget
from logic.comsys.items_book_ui.WeaponDetailsWidget import WeaponDetailsWidget
from logic.comsys.items_book_ui.SkinGetUseBuyWidget import SkinGetUseBuyWidget
from logic.comsys.items_book_ui.ItemFilterWidget import ItemFilterWidget
from common.cfg import confmgr
from logic.gutils import items_book_utils
from logic.client.const import items_book_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import item_utils
from common.framework import Functor
from logic.gutils import template_utils
from logic.gutils import lobby_model_display_utils
from common.utils.timer import RELEASE
from logic.gutils import red_point_utils
from logic.comsys.common_ui.WidgetExtModelPic import WidgetExtModelPic
from logic.comsys.items_book_ui.ItemsBookCommonChooseWidget import ItemsBookCommonChooseWidget
from logic.comsys.items_book_ui.ItemsBookOwnBtnWidget import ItemsBookOwnBtnWidget
import time
import math3d
ROTATE_FACTOR = 850
WEAPON_KIND_ALL = -1

class WeaponListWidget(WidgetExtModelPic):

    def __init__(self, parent, panel):
        super(WeaponListWidget, self).__init__(panel)
        self.inited = False
        self.parent = parent
        self.panel = panel
        self.selected_item_no = None
        self.selected_skin_list = None
        self.page_index = items_book_const.WEAPON_ID
        self.selected_skin_idx = None
        self.selected_skin_no = None
        self._show_wp_class = []
        self.last_create_item_timestamp = 0.0
        self.light_anim_played = False
        self.light_anim_timer = -1
        self.in_anim_timer_ids = dict()
        self.skin_item_loaded_count = 0
        self._chose_class = WEAPON_KIND_ALL
        self.is_in_expand_mode = False
        self._cam_position_start = None
        self._cam_position_end = None
        self._model_center_pos = None
        self._cam_move_length = 0.0
        self._cur_cam_offset = 0.0
        self._model_offset = math3d.vector(0, 0, 0)
        self._own_widget = ItemsBookOwnBtnWidget(self.panel.btn_tick, self.on_click_own_btn)
        self.init_data()
        self.init_scene()
        self.init_widget()
        return

    def init_scene(self):

        def finish_cb(new_scene, *args):
            if self._cam_position_start is None:
                cam = new_scene.active_camera
                if cam:
                    self._cam_position_start = cam.world_position
                else:
                    self._cam_position_start = None
                self._try_update_cam_pos_info()
            return

        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.WEAPON_SHOW, update_cam_at_once=True, scene_content_type=scene_const.SCENE_ITEM_BOOK, finish_callback_ex=finish_cb)
        global_data.emgr.change_model_display_scene_item.emit(None)
        self._update_model_center_pos(None)
        return

    def init_data(self):
        self.data_dict = {}
        weapon_config = items_book_utils.get_items_conf(items_book_const.WEAPON_ID)
        self.data_dict['weapon'] = weapon_config
        self.init_weapon_skins()

    def init_weapon_skins(self):
        skin_dict = {}
        skin_category = {}
        conf = confmgr.get('items_book_conf', 'WeaponSkinConfig', 'Content', default={})
        for item_no in six.iterkeys(self.data_dict['weapon']):
            _skins = items_book_utils.get_items_skins_by_item_no(items_book_const.WEAPON_ID, item_no)
            skins = []
            for skin_id in _skins:
                if not item_utils.can_open_show(skin_id, owned_should_show=True):
                    continue
                if conf.get(skin_id, {}).get('is_owned_show', False) and global_data.player.get_item_num_by_no(int(skin_id)) <= 0:
                    continue
                skins.append(skin_id)

            skin_dict[item_no] = skins

        self.data_dict['weapon_skins'] = skin_dict
        skin_category = confmgr.get('items_book_conf', 'WeaponTabConfig', 'Content', default={})
        self.data_dict['weapon_skin_category'] = skin_category
        self.class_option_list = [ {'name': skin_category[i]['tab_name_id'],'index': i} for i in sorted(six_ex.keys(skin_category)) ]
        self.class_option_list.insert(0, {'name': 80566,'index': WEAPON_KIND_ALL})

    def init_widget(self):
        self.update_collect_data()
        self._weapon_details_widget = WeaponDetailsWidget(self, self.panel.btn_details)
        self._skin_get_use_buy_widget = SkinGetUseBuyWidget(self, self.panel.btn_buy_1, self.panel.btn_use, self.panel.btn_go, self.panel.temp_price, self.panel.lab_get_method)
        self._skin_list_widget = SkinItemListWidget(self, self.panel.list_skin, self.on_create_skin_item, 4, need_set_opacity_zero=True)
        self._category_list_widget = ItemCategoryListWidget(self, self.panel.temp_right_tab, self.data_dict['weapon'], self.click_category_item_callback, items_book_const.WEAPON_ID, need_show_outline_pic=True)
        self._weapon_kind_widget = ItemsBookCommonChooseWidget(self.panel.choose_list_weapon, self.panel.temp_btn.btn_arrow, self.class_option_list, 0, self.on_choose_class, func_btn=self.panel.temp_btn.btn)
        self.init_touch_widget()

    def on_click_own_btn(self, *args):
        self.update_show_list_on_condition_changed()

    def get_show_list_on_condition(self):
        from logic.gutils.items_book_utils import get_sorted_item_list
        all_list = self.data_dict['weapon_skins'][self.selected_item_no]
        if self._own_widget.get_own_switch():
            selected_skin_list = self._own_widget.get_data_has_own(all_list)
        else:
            selected_skin_list = all_list
        return get_sorted_item_list(selected_skin_list, sort_by_can_use=True)

    def update_show_list_on_condition_changed(self):
        self.selected_skin_list = self.get_show_list_on_condition()
        if self._skin_list_widget:
            self._skin_list_widget.update_skin_data(self.selected_skin_list, False, 0)

    def on_choose_class(self, choose_class):
        if choose_class == self._chose_class:
            return
        self._chose_class = choose_class
        if self._chose_class == WEAPON_KIND_ALL:
            self._category_list_widget.refresh_widget(self.data_dict['weapon'])
        else:
            skin_category = self.data_dict['weapon_skin_category']
            valid_wps = skin_category[self._chose_class]['second_tabs']
            wp_dict = {}
            for i in valid_wps:
                i = str(i)
                wp_dict[i] = self.data_dict['weapon'][i]

            self._show_wp_class = wp_dict
            self._category_list_widget.refresh_widget(wp_dict)

    def init_touch_widget(self):
        from logic.comsys.items_book_ui.NodeDragHelper import NodeDragHelper
        helper = NodeDragHelper()
        helper.set_single_finger_drag(self.on_drag_touch_layer)
        helper.set_double_finger_drag(self.on_double_drag_touch_layer)
        self._node_drag_helper = helper
        self.panel.nd_touch.BindMethod('OnBegin', self._on_rotate_begin)
        self.panel.nd_touch.BindMethod('OnDrag', self._on_rotate_drag)
        self.panel.nd_touch.BindMethod('OnEnd', self._on_rotate_end)
        self.panel.btn_full_screen.setVisible(False)
        self.panel.btn_more.BindMethod('OnClick', self.on_click_expand_btn)

    def _on_rotate_begin(self, btn, touch):
        return self._node_drag_helper.on_begin(touch)

    def _on_rotate_drag(self, btn, touch):
        self._node_drag_helper and self._node_drag_helper.on_drag(touch)

    def _on_rotate_end(self, btn, touch):
        self._node_drag_helper and self._node_drag_helper.on_end(touch)

    def on_drag_touch_layer(self, delta):
        global_data.emgr.rotate_model_display.emit(-delta.x / ROTATE_FACTOR)

    def on_double_drag_touch_layer(self, delta):
        from logic.comsys.mecha_display.MechaDetails import MechaDetails
        delta = delta / MechaDetails.CAM_SCALE_TOUCH_SEN_FACTOR
        self._on_cam_pos_scroll_delta(delta)

    def on_click_full_screen(self, btn, touch):
        from logic.comsys.common_ui.FullScreenBackUI import FullScreenBackUI
        ui = FullScreenBackUI()
        if not ui:
            return
        ui.setBackFunctionCallback(self.recover_from_full_screen)
        self.parent.parent.move_out()
        self.panel.PlayAnimation('disappear')

    def on_click_expand_btn(self, btn, touch):
        if not self.panel:
            return
        self.is_in_expand_mode = not self.is_in_expand_mode
        if self.is_in_expand_mode:
            self.panel.list_skin.SetNumPerUnit(2)
            self.panel.PlayAnimation('list_more')
        else:
            self.panel.list_skin.SetNumPerUnit(1)
            self.panel.PlayAnimation('list_normal')
        self.panel.list_skin.FitViewSizeToContainerSize()
        self.update_expand_camera(need_slerp=True)

    def update_nd_dir_pos(self):
        self.panel.nd_dir.setContentSize(self.panel.list_skin.getContentSize())
        self.panel.nd_dir.ChildResizeAndPosition()

    def recover_from_full_screen(self):
        self.parent.parent.move_in()
        self.panel.PlayAnimation('in')

    def on_click_skin_item(self, index, *args):
        if not self.panel:
            return
        else:
            prev_index = self.selected_skin_idx
            self.selected_skin_idx = index
            item_widget = self.panel.list_skin.GetItem(index)
            skin_no = self.selected_skin_list[index]
            self.selected_skin_no = skin_no
            show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
            model_data = lobby_model_display_utils.get_lobby_model_data(skin_no)

            def load_cb(l_model):
                self._update_model_center_pos(l_model)

            self.ext_show_item_model(model_data, in_item_id=skin_no, in_load_callback=load_cb)
            if show_new:
                global_data.player.req_del_item_redpoint(skin_no)
                red_point_utils.show_red_point_template(item_widget.nd_new, False)
            global_data.emgr.select_item_goods.emit(skin_no)
            self.panel.lab_name.SetString(items_book_utils.get_filter_item_show_name(items_book_const.WEAPON_ID, self.selected_item_no, skin_no))
            prev_item = self.panel.list_skin.GetItem(prev_index)
            if prev_item:
                prev_item.setLocalZOrder(0)
                prev_item.choose.setVisible(False)
            item_widget.setLocalZOrder(2)
            weapon_config_dict = items_book_utils.get_items_skin_conf(items_book_const.WEAPON_ID)
            goods_id = weapon_config_dict.get(skin_no, {}).get('goods_id', None)
            item_widget.choose.setVisible(True)
            self._skin_get_use_buy_widget.update_target_item_no(self.selected_item_no, skin_no, goods_id)
            return

    def _check_play_light_animation(self):
        if time.time() - self.last_create_item_timestamp > 0.1:
            for i in range(self.skin_item_loaded_count):
                item = self.panel.list_skin.GetItem(i)
                item and item.PlayAnimation('light')

            self.light_anim_played = True
            self.light_anim_timer = -1
            return RELEASE

    def _play_in_animation(self, index):
        self.in_anim_timer_ids.pop(index)
        if self.panel and self.panel.isValid():
            item = self.panel.list_skin.GetItem(index)
            item and item.PlayAnimation('in')

    def _clear_anim_timer(self):
        if self.light_anim_timer != -1:
            global_data.game_mgr.unregister_logic_timer(self.light_anim_timer)
            self.light_anim_timer = -1
        if self.in_anim_timer_ids:
            for timer_id in six.itervalues(self.in_anim_timer_ids):
                global_data.game_mgr.unregister_logic_timer(timer_id)

            self.in_anim_timer_ids.clear()

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
            item_utils.check_skin_bg_tag(item_widget.img_level, skin_no)
            item_widget.bar.SetEnable(True)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
            red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
            template_utils.show_remain_time(item_widget.lab_limited, item_widget.lab_limited, skin_no)
            item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index))
            if index == 0:
                item_widget.PlayAnimation('in')
            else:
                timer_id = global_data.game_mgr.register_logic_timer(self._play_in_animation, args=(index,), interval=2 * index, times=1)
                if index in self.in_anim_timer_ids:
                    global_data.game_mgr.unregister_logic_timer(self.in_anim_timer_ids[index])
                self.in_anim_timer_ids[index] = timer_id
            self.skin_item_loaded_count = index + 1
            self.last_create_item_timestamp = time.time()
            if self.light_anim_timer == -1 and not self.light_anim_played:
                self.light_anim_timer = global_data.game_mgr.register_logic_timer(self._check_play_light_animation, interval=1)
        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.img_level.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)
        if item_widget.nd_empty:
            item_widget.nd_empty.setVisible(not valid)

    def update_collect_data(self):
        self.collect_dict = {}
        weapon_config_dict = items_book_utils.get_items_skin_conf(items_book_const.WEAPON_ID)
        self.collect_count = [0, len(weapon_config_dict)]
        for k, v in six.iteritems(self.data_dict['weapon_skins']):
            item_skin_count = 0
            for skin in v:
                item_can_use, limit_left_timestamp = mall_utils.item_can_use_by_item_no(skin)
                if item_can_use:
                    item_skin_count += 1

            self.collect_dict[k] = (
             item_skin_count, len(v))
            self.collect_count[0] += item_skin_count

        self.update_collect_num()
        self.update_select_item_collect_count(*tuple(self.collect_count))

    def update_collect_num(self):
        if not self.selected_item_no:
            self.panel.nd_sort.lab_collect.SetString('')
            self.panel.nd_sort.lab_name.SetString('')
        else:
            self.panel.lab_collect.SetString('%d/%d' % tuple(self.collect_dict[self.selected_item_no]))
            self.panel.nd_sort.lab_name.SetString(item_utils.get_lobby_item_name(self.selected_item_no))

    def refresh_widget(self):
        if self.selected_item_no is None:
            return
        else:
            self.init_scene()
            self.init_data()
            if self._chose_class == WEAPON_KIND_ALL:
                self._category_list_widget.refresh_widget(self.data_dict['weapon'])
            else:
                self._category_list_widget.refresh_widget(self._show_wp_class)
            return

    def update_select_item_collect_count(self, own_count, all_skin):
        self.panel.temp_prog.lab_got.SetString('%d/%d' % (own_count, all_skin))
        self.panel.temp_prog.prog.SetPercentage(int(own_count / float(all_skin) * 100))

    def click_category_item_callback(self, index, data):
        self.last_create_item_timestamp = 0.0
        self.light_anim_played = False
        self._clear_anim_timer()
        self.skin_item_loaded_count = 0
        is_same_item = self.selected_item_no == data[0]
        self.selected_item_no = data[0]
        self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(self.selected_item_no))
        skin_list = self.get_show_list_on_condition()
        self.selected_skin_list = skin_list
        item_fashion_no = items_book_utils.get_item_fashion_no(self.selected_item_no)
        if self.selected_skin_no and str(self.selected_skin_no) in self.selected_skin_list:
            select_idx = self.selected_skin_list.index(str(self.selected_skin_no))
        else:
            select_idx = is_same_item or 0 if 1 else self.selected_skin_idx
        if select_idx is None or not is_same_item:
            try:
                item_index = self.selected_skin_list.index(str(item_fashion_no))
            except:
                item_index = select_idx

        else:
            item_index = select_idx
        self._skin_list_widget.update_skin_data(self.selected_skin_list, not is_same_item, item_index)
        self._weapon_details_widget.set_detail_item_no(self.selected_item_no)
        self.update_collect_num()
        return

    def destroy(self):
        super(WeaponListWidget, self).destroy()
        self.inited = False
        self._weapon_details_widget.destroy()
        self._weapon_details_widget = None
        self._category_list_widget.destroy()
        self._category_list_widget = None
        self._skin_list_widget.destroy()
        self._skin_list_widget = None
        self._skin_get_use_buy_widget.destroy()
        self._skin_get_use_buy_widget = None
        self._node_drag_helper = None
        if self._weapon_kind_widget:
            self._weapon_kind_widget.destroy()
            self._weapon_kind_widget = None
        if self._own_widget:
            self._own_widget.destroy()
            self._own_widget = None
        self.panel = None
        self.parent = None
        self.data_dict = None
        self._show_wp_class = []
        self._clear_anim_timer()
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

            else:
                print('can not jump, no belong_no', item_no)
            return

    def check_can_mouse_scroll(self):
        return True

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        from logic.comsys.mecha_display.MechaDetails import MechaDetails
        delta = delta / MechaDetails.CAM_SCALE_MOUSE_SEN_FACTOR
        self._on_cam_pos_scroll_delta(delta)

    def _on_cam_pos_scroll_delta(self, delta):
        self._modify_cur_cam_offset_dist(delta)
        self._update_cam_position(is_slerp=True)

    def _set_cur_cam_offset(self, offset):
        length = self._cam_move_length
        offset = min(length, max(0.0, offset))
        self._cur_cam_offset = offset

    def _modify_cur_cam_offset_dist(self, offset):
        self._set_cur_cam_offset(self._cur_cam_offset + offset)

    def _update_cam_position(self, is_slerp):
        pos = self._get_cam_position(self._cur_cam_offset)
        if pos is not None:
            global_data.emgr.change_model_display_scene_cam_pos.emit(pos, is_slerp=is_slerp)
            return True
        else:
            return False
            return

    def _get_cam_position(self, offset_dist):
        far, near = self._cam_position_start, self._cam_position_end
        if far is None or near is None:
            return
        else:
            import math3d
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

    def _update_model_center_pos(self, l_model):
        if not l_model:
            self._model_center_pos = None
        else:
            self._model_center_pos = l_model.get_cam_look_at_position(default=None)
        self.update_expand_camera()
        self._try_update_cam_pos_info()
        return

    def _try_update_cam_pos_info(self):
        self._cam_move_length = 0.0
        self._cam_position_end = None
        if not self._cam_position_start or not self._model_center_pos:
            return
        else:
            SAFE_DISTANCE = 20
            _model_center_pos = self._model_center_pos - self._model_offset
            direction = _model_center_pos - self._cam_position_start
            direction.normalize()
            cam_end_pos = _model_center_pos - direction * SAFE_DISTANCE
            if direction.dot(cam_end_pos - self._cam_position_start) <= 0:
                return
            self._cam_position_end = cam_end_pos
            self._cam_move_length = (cam_end_pos - self._cam_position_start).length
            self._set_cur_cam_offset(self._cur_cam_offset)
            return

    def update_expand_camera(self, need_slerp=False):
        model_offset = self.get_off_position()
        global_data.emgr.change_model_display_off_position.emit(model_offset, is_slerp=need_slerp)
        self._model_offset = math3d.vector(*model_offset)

    def get_off_position(self, off=True):
        if self.is_in_expand_mode:
            off_position = [
             5, 0, 0]
        else:
            off_position = [
             0, 0, 0]
        return off_position