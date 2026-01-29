# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/LobbySkyboxWidget.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from functools import cmp_to_key
from logic.gutils import mall_utils
from logic.comsys.items_book_ui.SkinItemListWidget import SkinItemListWidget
from logic.comsys.items_book_ui.ItemFilterWidget import ItemFilterWidget
from logic.gutils import items_book_utils
from logic.client.const import items_book_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import item_utils
from common.framework import Functor
from logic.gutils import template_utils
from logic.gutils import lobby_model_display_utils
from logic.gutils import jump_to_ui_utils
import world
from logic.gcommon import time_utility
from logic.gcommon.item.item_const import BATTLE_EFFECT_KILL
from logic.gutils import red_point_utils
from common.cfg import confmgr
ROTATE_FACTOR = 850

class LobbySkyboxWidget(object):
    BALLON_BIND_POINT = 'ballon'
    BALLON_RES_PATH = confmgr.get('script_gim_ref')['ballon_res']

    def __init__(self, parent, panel):
        self.inited = False
        self.parent = parent
        self.panel = panel
        self.skybox_list = []
        self.selected_item_no = None
        self.selected_skin_idx = None
        self.use_skybox_item = None
        self.page_index = items_book_const.PRIVILEGE_ID
        self.init_data()
        self.init_scene()
        self.init_widget()
        self.init_btn_event()
        global_data.emgr.privilege_lobby_skin_change += self.refresh_btn_state
        global_data.emgr.player_leave_visit_scene_event += self.update_preview_btn
        global_data.emgr.player_enter_visit_scene_event += self.update_preview_btn
        return

    def on_click_skin_item(self, index, *args):
        if not self.panel:
            return
        else:
            prev_index = self.selected_skin_idx
            item_widget = self.panel.list_item.GetItem(index)
            item_no = self.data_list[index][0]
            show_new = global_data.lobby_red_point_data.get_rp_by_no(item_no)
            self.selected_item_no = item_no
            self.selected_skin_idx = index
            self.panel.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
            self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
            self.panel.lab_get_method.SetString(item_utils.get_item_access(item_no))
            if show_new:
                global_data.player.req_del_item_redpoint(item_no)
                red_point_utils.show_red_point_template(item_widget.nd_new, False)
            global_data.emgr.select_item_goods.emit(item_no)
            prev_item = self.panel.list_item.GetItem(prev_index)
            if prev_item:
                prev_item.setLocalZOrder(0)
                prev_item.choose.setVisible(False)
            item_widget.setLocalZOrder(2)
            item_widget.choose.setVisible(True)
            lobby_skybox_data = self.data_list[index][1]
            show_pic_path = lobby_skybox_data.get('show_pic_path', None)
            self.panel.img_item.SetDisplayFrameByPath('', show_pic_path)
            self.refresh_btn_state()
            return

    def init_scene(self):
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.ITEMBOOKS_GESTURE_DISPLAY, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def init_widget(self):
        self.panel.btn_preview.setVisible(True)
        self.panel.lab_collect_desc.SetString(15808)
        self.skin_list_widget = SkinItemListWidget(self, self.panel.list_item, self.on_create_skin_item, 1)
        self.skin_list_widget.update_skin_data(self.data_list)
        self.update_preview_btn()

    def init_data(self):
        self.data_dict = {}
        config = items_book_utils.get_items_conf(self.page_index)
        self.data_dict['lobby_skybox'] = config
        _data_list = sorted(six.iteritems(self.data_dict['lobby_skybox']), key=cmp_to_key(--- This code section failed: ---

 102       0  LOAD_GLOBAL           0  'six_ex'
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

    def update_preview_btn(self, *args):
        if global_data.player:
            if global_data.player.is_in_visit_mode():
                self.panel.btn_preview.setVisible(False)
            else:
                self.panel.btn_preview.setVisible(True)

    def on_create_skin_item(self, lst, index, item_widget):
        item_widget.nd_content.setVisible(True)
        skin_no = self.data_list[index][0]
        item_widget.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(skin_no))
        item_widget.lab_name.SetString(item_utils.get_lobby_item_name(skin_no))
        item_widget.choose.setVisible(False)
        if global_data.player:
            is_use = int(skin_no) == int(global_data.player.get_lobby_skybox_id())
            item_widget.img_using.setVisible(is_use)
            self.use_skybox_item = item_widget if is_use else self.use_skybox_item
        item_can_use, limit_left_timestamp = mall_utils.item_can_use_by_item_no(skin_no)
        item_widget.img_lock.setVisible(not item_can_use)
        item_utils.check_skin_tag(item_widget.nd_kind, skin_no)
        item_utils.check_skin_bg_tag(item_widget.img_level, skin_no, is_small_item=True)
        item_widget.bar.SetEnable(True)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
        red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
        template_utils.show_remain_time(item_widget.lab_limited, item_widget.lab_limited, skin_no)
        item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index))
        self.skybox_list.append(item_widget)

    def init_btn_event(self):

        @self.panel.btn_preview.unique_callback()
        def OnClick(btn, touch):
            if global_data.player and global_data.player.is_in_visit_mode():
                return
            from logic.gutils.jump_to_ui_utils import jump_to_lobby_sky_box_preview
            jump_to_lobby_sky_box_preview(item_no=self.selected_item_no)

        @self.panel.btn_go.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if not self.selected_item_no:
                return
            else:
                jump_info = self.data_list[self.selected_skin_idx][1].get('jump_func')
                func_name = jump_info.get('func', None)
                args = jump_info.get('args', [])
                kargs = jump_info.get('kargs', {})
                if func_name:
                    func = getattr(jump_to_ui_utils, func_name, None)
                    if func:
                        func(*args, **kargs)
                self.refresh_btn_state()
                return

        @self.panel.btn_use.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if not self.selected_item_no:
                return
            if not global_data.player:
                return
            global_data.player.change_lobby_skybox(int(self.selected_item_no))
            self.refresh_btn_state()
            self.refresh_use_item_state()

        @self.panel.btn_dismount.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if not self.selected_item_no:
                return
            if not global_data.player:
                return
            global_data.player.change_lobby_skybox(-1)
            self.refresh_btn_state()
            self.refresh_use_item_state()

    def refresh_widget(self):
        if self.selected_item_no is None:
            return
        else:
            if not global_data.player:
                return
            self.init_scene()
            self.refresh_items_state()
            self.refresh_btn_state()
            self.refresh_use_item_state()
            return

    def refresh_items_state(self):
        for idx in range(len(self.skybox_list)):
            skin_no = self.data_list[idx][0]
            item_can_use, _ = mall_utils.item_can_use_by_item_no(skin_no)
            self.skybox_list[idx].img_lock.setVisible(not item_can_use)

    def refresh_btn_state(self):
        item_can_use, _ = mall_utils.item_can_use_by_item_no(self.selected_item_no)
        self.panel.btn_go.setVisible(not item_can_use)
        can_use = global_data.player.get_lobby_skybox_id() != int(self.selected_item_no)
        self.panel.btn_use.setVisible(can_use)
        item_can_dismount = global_data.player.get_lobby_skybox_id() == int(self.selected_item_no)
        self.panel.btn_dismount.setVisible(item_can_dismount)

    def refresh_use_item_state(self):
        if self.use_skybox_item:
            self.use_skybox_item.img_using.setVisible(False)
        use_item = self.panel.list_item.GetItem(self.selected_skin_idx)
        is_use = global_data.player.get_lobby_skybox_id() == int(self.selected_item_no)
        use_item.img_using.setVisible(is_use)
        self.use_skybox_item = use_item if is_use else self.use_skybox_item

    def destroy(self):
        self.inited = False
        self.parent = None
        self.panel = None
        self.skin_list_widget.destroy()
        self.skin_list_widget = None
        self.skybox_list = []
        global_data.emgr.privilege_lobby_skin_change -= self.refresh_btn_state
        global_data.emgr.player_leave_visit_scene_event -= self.update_preview_btn
        global_data.emgr.player_enter_visit_scene_event -= self.update_preview_btn
        return

    def do_hide_panel(self):
        self.panel.StopTimerAction()

    def jump_to_item_no(self, item_no):
        if not item_no:
            return
        try:
            index = -1
            for i, (ino, _) in enumerate(self.skin_list_widget.skins_list):
                if ino == str(item_no):
                    index = i
                    break

            if index >= 0:
                self.skin_list_widget.init_select_item(index)
        except:
            return