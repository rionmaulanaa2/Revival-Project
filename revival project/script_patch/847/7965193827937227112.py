# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/KillSfxWidget.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from logic.gutils import mall_utils
from logic.comsys.items_book_ui.SkinItemListWidget import SkinItemListWidget
from logic.comsys.items_book_ui.KillSfxGetUseBuyWidget import KillSfxGetUseBuyWidget
from logic.comsys.items_book_ui.ItemFilterWidget import ItemFilterWidget
from logic.gutils import items_book_utils
from logic.client.const import items_book_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import item_utils
from common.framework import Functor
from logic.gutils import template_utils
from logic.gutils import lobby_model_display_utils
import world
from logic.gcommon import time_utility
from logic.gcommon.item.item_const import BATTLE_EFFECT_KILL
from logic.gutils import red_point_utils
from common.cfg import confmgr
ROTATE_FACTOR = 850

class KillSfxWidget(object):
    BALLON_BIND_POINT = 'ballon'
    BALLON_RES_PATH = confmgr.get('script_gim_ref')['ballon_res']

    def __init__(self, parent, panel):
        self.inited = False
        self.parent = parent
        self.panel = panel
        self.selected_item_no = None
        self.selected_skin_list = None
        self.cur_show_model_item_no = None
        self.page_index = items_book_const.KILL_SFX_ID
        self.selected_skin_idx = None
        self.init_data()
        self.init_widget()
        self.init_buttons()
        return

    def init_buttons(self):
        import cc

        @self.panel.btn_details.unique_callback()
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(81402, 81412)
            x, y = self.panel.btn_details.GetPosition()
            wpos = self.panel.btn_details.GetParent().ConvertToWorldSpace(x, y)
            dlg.set_node_pos(wpos, cc.Vec2(1, 1))

    def is_panel_visible(self):
        ui_parent = global_data.ui_mgr.get_ui('ItemsBookMainUI')
        return ui_parent and ui_parent.panel.isVisible()

    def init_scene(self):
        if not self.is_panel_visible():
            return
        else:
            global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.ITEMBOOKS_GESTURE_DISPLAY, scene_content_type=scene_const.SCENE_ITEM_BOOK)
            global_data.emgr.change_model_display_scene_item.emit(None)
            return

    def init_data(self):
        self.data_dict = {}
        config = items_book_utils.get_items_conf(self.page_index)
        self.data_dict['kill_effect'] = config
        _data_list = sorted(six.iteritems(self.data_dict['kill_effect']), key=cmp_to_key(--- This code section failed: ---

  72       0  LOAD_GLOBAL           0  'six_ex'
           3  LOAD_ATTR             1  'compare'
           6  LOAD_GLOBAL           2  'int'
           9  LOAD_GLOBAL           1  'compare'
          12  BINARY_SUBSCR    
          13  CALL_FUNCTION_1       1 
          16  LOAD_GLOBAL           2  'int'
          19  LOAD_FAST             1  'y'
          22  LOAD_CONST            1  ''
          25  BINARY_SUBSCR    
          26  CALL_FUNCTION_1       1 
          29  CALL_FUNCTION_2       2 
          32  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 29
))
        self.data_list = []
        for i, info in enumerate(_data_list):
            if item_utils.can_open_show(info[0], owned_should_show=True):
                self.data_list.append(info)

    def init_widget(self):
        self._item_filter_widget = ItemFilterWidget(self, self.panel.choose_list, self.panel.btn_change, 81413, 81414, self.on_select_filter_item, self.panel.img_arrow)
        self._sfx_get_use_buy_widget = KillSfxGetUseBuyWidget(self, self.panel.btn_buy_1, self.panel.btn_use, self.panel.btn_go, self.panel.temp_price, self.panel.lab_get_method)
        self._skin_list_widget = SkinItemListWidget(self, self.panel.list_item, self.on_create_skin_item, 6)
        self.init_touch_widget()
        self.on_default_select(self.data_list)

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
            item_widget = self.panel.list_item.GetItem(index)
            sfx_no = self.selected_skin_list[index]
            self.selected_item_no = sfx_no
            show_new = global_data.lobby_red_point_data.get_rp_by_no(sfx_no)
            self._show_sfx(sfx_no)
            self.panel.lab_name.SetString(item_utils.get_lobby_item_name(sfx_no))
            self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(sfx_no))
            if show_new:
                global_data.player.req_del_item_redpoint(sfx_no)
                red_point_utils.show_red_point_template(item_widget.nd_new, False)
            global_data.emgr.select_item_goods.emit(sfx_no)
            prev_item = self.panel.list_item.GetItem(prev_index)
            if prev_item:
                prev_item.setLocalZOrder(0)
                prev_item.choose.setVisible(False)
            item_widget.setLocalZOrder(2)
            skin_config_dict = items_book_utils.get_items_skin_conf(self.page_index)
            goods_id = skin_config_dict.get(sfx_no, {}).get('goods_id', None)
            item_widget.choose.setVisible(True)
            self._sfx_get_use_buy_widget.update_target_item_no(self.selected_item_no, goods_id)
            return

    def on_create_skin_item(self, lst, index, item_widget):
        valid = index < len(self.selected_skin_list) and self.selected_item_no
        if valid:
            item_widget.nd_content.setVisible(True)
            skin_no = self.selected_skin_list[index]
            item_widget.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(skin_no))
            item_widget.lab_name.SetString(item_utils.get_lobby_item_name(skin_no))
            item_widget.choose.setVisible(False)
            cur_kill_effect_no = None
            if global_data.player:
                cur_kill_effect_no = global_data.player.get_battle_effect_item_by_type(BATTLE_EFFECT_KILL)
            item_widget.img_using.setVisible(str(cur_kill_effect_no) == str(skin_no))
            item_can_use, limit_left_timestamp = mall_utils.item_can_use_by_item_no(skin_no)
            item_widget.img_lock.setVisible(not item_can_use)
            item_utils.check_skin_tag(item_widget.nd_kind, skin_no)
            item_utils.check_skin_bg_tag(item_widget.img_level, skin_no, is_small_item=True)
            item_widget.bar.SetEnable(True)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
            red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
            template_utils.show_remain_time(item_widget.lab_limited, item_widget.lab_limited, skin_no)
            item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index))
            fix_expire_time = item_utils.get_lobby_item_fix_expire_time(skin_no)
            item_widget.lab_limited.stopAllActions()
            if fix_expire_time:
                item_widget.lab_limited.setVisible(True)
                self.init_count_down_time(item_widget, fix_expire_time)
            else:
                item_widget.lab_limited.setVisible(False)
        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.img_level.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)
        if item_widget.nd_empty:
            item_widget.nd_empty.setVisible(not valid)
        return

    def init_count_down_time(self, ui_item, end_time):

        def show_count_down():
            now = time_utility.get_server_time()
            seconds = end_time - now
            if seconds < -1:
                self.refresh_widget()
                return
            text = time_utility.get_readable_time_day_hour_minitue(seconds)
            ui_item.lab_limited.SetString(text)
            ui_item.lab_limited.DelayCall(5, lambda : show_count_down())

        show_count_down()

    def refresh_widget(self):
        if self.selected_item_no is None:
            return
        else:
            old_data_list = self.data_list
            self.init_scene()
            self.init_data()
            if old_data_list == self.data_list:
                self._skin_list_widget.update_skin_data(self.selected_skin_list, False, self.selected_skin_idx)
                self.update_select_item_collect_count()
            else:
                self.selected_item_no = None
                self.on_default_select(self.data_list)
            return

    def update_select_item_collect_count(self):
        if not self.selected_item_no:
            return
        desc_str, skin_str = self._item_filter_widget.get_selected_item_str()
        self.panel.lab_collect_skin.SetString(skin_str)
        self.panel.lab_collect_desc.SetString(desc_str)

    def on_default_select(self, data):
        is_same_item = self.selected_item_no == data[0]
        self.selected_item_no = data[0]
        select_idx = is_same_item or 0 if 1 else self.selected_skin_idx
        self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(self.selected_item_no))
        self._item_filter_widget.set_itemlist([ sort_item_data[0] for sort_item_data in self.data_list ])
        self.selected_skin_list = self._item_filter_widget.get_selected_degree_items()
        item_index = select_idx
        if global_data.player:
            cur_kill_effect_no = global_data.player.get_battle_effect_item_by_type(BATTLE_EFFECT_KILL)
            try:
                item_index = self.selected_skin_list.index(str(cur_kill_effect_no))
            except:
                pass

        self._skin_list_widget.update_skin_data(self.selected_skin_list, not is_same_item, item_index)
        self.update_select_item_collect_count()

    def on_select_filter_item(self):
        self.selected_skin_list = self._item_filter_widget.get_selected_degree_items()
        item_index = 0
        if global_data.player:
            cur_kill_effect_no = global_data.player.get_battle_effect_item_by_type(BATTLE_EFFECT_KILL)
            try:
                item_index = self.selected_skin_list.index(str(cur_kill_effect_no))
            except:
                pass

        self._skin_list_widget.update_skin_data(self.selected_skin_list, False, item_index)
        self.update_select_item_collect_count()

    def do_hide_panel(self):
        self.panel.StopTimerAction()
        global_data.emgr.change_model_display_scene_tag_effect.emit('')

    def destroy(self):
        global_data.emgr.change_model_display_scene_tag_effect.emit('')
        self.inited = False
        self.panel.StopTimerAction()
        self._skin_list_widget.destroy()
        self._skin_list_widget = None
        self._sfx_get_use_buy_widget.destroy()
        self._sfx_get_use_buy_widget = None
        self._item_filter_widget.destroy()
        self._item_filter_widget = None
        self.panel = None
        self.parent = None
        self.data_dict = None
        return

    def jump_to_item_no(self, item_no):
        if not item_no:
            return
        try:
            skin_index = self._skin_list_widget.skins_list.index(str(item_no))
            self._skin_list_widget.init_select_item(skin_index)
        except:
            return

    def _show_sfx(self, sfx_item_no):
        if not self.is_panel_visible():
            return
        else:
            conf = self.data_dict['kill_effect'].get(str(sfx_item_no), {})
            sfx_path = conf.get('sfx_path', '')
            sfx_scale = conf.get('sfx_scale', 1.0)
            one_time = conf.get('time', 5550 / 1000.0)
            offset = conf.get('sfx_offset', None)

            def single_show():
                if sfx_path:
                    global_data.emgr.change_model_display_scene_tag_effect.emit(sfx_path, sfx_scale=sfx_scale, offset=offset)

            single_show()

            def start_loop():
                if self.panel:
                    self.panel.StopTimerAction()
                    self.panel.TimerAction(lambda t: single_show(), duration_sec=10000000, interval=one_time)

            start_loop()
            return