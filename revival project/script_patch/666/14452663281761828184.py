# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/LobbyMusicFunctionWidget.py
from __future__ import absolute_import
from logic.gutils import mall_utils
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
from logic.gutils import red_point_utils
from common.cfg import confmgr
from logic.gcommon.item.item_const import DEFAULT_LOBBY_BGM
from logic.comsys.items_book_ui.MiaomiaoItemGoUseDismountWidget import MiaomiaoItemGoUseDismountWidget

class LobbyMusicFunctionWidget(object):

    def __init__(self, parent, panel):
        self.inited = False
        self.parent = parent
        self.panel = panel
        self.use_music_item = None
        self.selected_item_no = None
        self.selected_skin_idx = None
        self.sel_callback = None
        self.sel_before_cb = None
        self.page_index = items_book_const.LOBBY_MUSIC_ID
        self.is_enable = False
        self.bind_event(True)
        self.init_widget()
        return

    def set_switch_enable(self, val):
        self.is_enable = val

    def bind_event(self, bind):
        e_conf = {'lobby_bgm_change_success': self.refresh_goods_ids,
           'player_item_update_event': self.refresh_goods_ids,
           'refresh_item_red_point': self.refresh_goods_ids
           }
        if bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def init_widget(self):
        self._miaomiao_go_use_dismount_widget = MiaomiaoItemGoUseDismountWidget(self, self.panel.btn_go, self.panel.btn_use, self.panel.btn_dismount, self.panel.btn_preview, self.panel.temp_price)

    def on_click_skin_item(self, index, item_no, *args):
        if not self.panel:
            return
        prev_index = self.selected_skin_idx
        item_widget = self.panel.list_item.GetItem(index)
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
        show_pic_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
        self.panel.img_item.setVisible(True)
        self.panel.img_item.SetDisplayFrameByPath('', show_pic_path)
        self.refresh_btn_state()
        music = item_utils.get_lobby_item_res_path(item_no) or 'bar'
        global_data.sound_mgr.play_music(music)
        if self.sel_callback:
            self.sel_callback()

    def init_scene(self):
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.ITEMBOOKS_GESTURE_DISPLAY, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def on_create_skin_item(self, lst, index, item_widget, skin_no):
        item_widget.nd_content.setVisible(True)
        show_pic = item_utils.get_lobby_item_pic_by_item_no(skin_no)
        item_widget.item.SetDisplayFrameByPath('', show_pic)
        item_widget.lab_name.SetString(item_utils.get_lobby_item_name(skin_no))
        item_widget.choose.setVisible(False)
        cur_bgm_item_no = global_data.player.get_lobby_bgm() or DEFAULT_LOBBY_BGM
        if global_data.player:
            is_use = int(skin_no) == int(cur_bgm_item_no)
            item_widget.img_using.setVisible(is_use)
        item_utils.check_skin_tag(item_widget.nd_kind, skin_no)
        item_can_use, limit_left_timestamp = mall_utils.item_can_use_by_item_no(skin_no)
        item_widget.nd_lock.setVisible(not item_can_use)
        item_widget.bar.SetEnable(True)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
        red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
        template_utils.show_remain_time(item_widget.lab_limited, item_widget.lab_limited, skin_no)
        item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index, skin_no))

    def refresh_widget(self):
        if not global_data.player:
            return
        self.refresh_items_state()

    def refresh_items_state(self):
        if not self.is_enable:
            return
        if self.parent:
            self.parent.sub_require_refresh_skin_list(self)

    def get_music_item_no(self):
        cur_bgm_item_no = global_data.player.get_lobby_bgm() or DEFAULT_LOBBY_BGM
        return cur_bgm_item_no

    def refresh_btn_state(self):
        if not self.selected_item_no:
            return
        else:
            if self._miaomiao_go_use_dismount_widget:
                self._miaomiao_go_use_dismount_widget.init_event()
                page_config = items_book_utils.get_items_conf(self.page_index)
                music_data = page_config.get(self.selected_item_no, {})
                goods_id = music_data.get('goods_id', None)
                self._miaomiao_go_use_dismount_widget.update_target_item_no(self.selected_item_no, goods_id)
            return

    def destroy(self):
        self.bind_event(False)
        self.sel_callback = None
        self.sel_before_cb = None
        self.inited = False
        self.parent = None
        self.panel = None
        global_data.emgr.lobby_bgm_change.emit(-1)
        return

    def do_hide_panel(self):
        global_data.emgr.lobby_bgm_change.emit(-1)

    def refresh_goods_ids(self, *args):
        if self.parent:
            self.parent.sub_require_refresh_skin_list(self)

    @property
    def selected_skin_idx(self):
        return self.parent.selected_skin_idx

    @selected_skin_idx.setter
    def selected_skin_idx(self, val):
        self.parent.selected_skin_idx = val

    def set_select_callback(self, before_cb, cb):
        self.sel_before_cb = before_cb
        self.sel_callback = cb

    def on_clear_effect(self):
        self.do_hide_panel()

    def on_update_scene(self):
        self.init_scene()

    def get_def_select_item_no(self):
        if global_data.player:
            cur_use_miaomiao_no = self.get_music_item_no()
            return cur_use_miaomiao_no
        else:
            return None