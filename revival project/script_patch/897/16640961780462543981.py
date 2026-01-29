# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/KillSfxFunctionWidget.py
from __future__ import absolute_import
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
from logic.comsys.items_book_ui.FunctionWidgetBase import FunctionWidgetBase
ROTATE_FACTOR = 850

class KillSfxFunctionWidget(FunctionWidgetBase):

    def __init__(self, parent, panel):
        super(KillSfxFunctionWidget, self).__init__(parent, panel)
        self.selected_skin_list = None
        self.init_widget()
        return

    def destroy(self):
        super(KillSfxFunctionWidget, self).destroy()
        self.selected_skin_list = []
        self._sfx_get_use_buy_widget.destroy()
        self._sfx_get_use_buy_widget = None
        self.data_dict = None
        return

    def set_data(self, data_list, data_dict):
        self.selected_skin_list = data_list
        self.data_dict = data_dict

    def on_clear_effect(self):
        self.panel.StopTimerAction()
        global_data.emgr.change_model_display_scene_tag_effect.emit('')

    def on_update_scene(self):
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.ITEMBOOKS_GESTURE_DISPLAY, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def is_panel_visible(self):
        ui_parent = global_data.ui_mgr.get_ui('ItemsBookMainUI')
        return ui_parent and ui_parent.panel.isVisible()

    def init_widget(self):
        self._sfx_get_use_buy_widget = KillSfxGetUseBuyWidget(self, self.panel.btn_buy_1, self.panel.btn_use, self.panel.btn_cancle, self.panel.btn_go, self.panel.temp_price, self.panel.nd_killsfx.btn_go.lab_get_method)

    def on_click_skin_item(self, index, *args):
        if not self.panel:
            return
        else:
            if self.sel_before_cb:
                self.sel_before_cb(self.get_parent_selected_item_index(), index)
            item_widget = self.panel.list_item.GetItem(index)
            sfx_no = self.selected_skin_list[index]
            selected_item_no = sfx_no
            show_new = global_data.lobby_red_point_data.get_rp_by_no(sfx_no)
            self._show_sfx(sfx_no)
            self.panel.lab_name.SetString(item_utils.get_lobby_item_name(sfx_no))
            self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(sfx_no))
            if show_new:
                global_data.player.req_del_item_redpoint(sfx_no)
                red_point_utils.show_red_point_template(item_widget.nd_new, False)
            global_data.emgr.select_item_goods.emit(sfx_no)
            skin_config_dict = items_book_utils.get_items_conf_by_config_name('KillSfxConfig')
            goods_id = skin_config_dict.get(sfx_no, {}).get('goods_id', None)
            self._sfx_get_use_buy_widget.update_target_item_no(selected_item_no, goods_id)
            if self.sel_callback:
                self.sel_callback()
            return

    def on_create_skin_item(self, lst, index, item_widget):
        valid = index < len(self.selected_skin_list) and self.selected_skin_list[index] is not None
        item_widget.img_driver_tag.setVisible(False)
        if valid:
            item_widget.nd_kind.setVisible(True)
            item_widget.img_level.setVisible(True)
            item_widget.nd_content.setVisible(True)
            item_widget.bar.SetEnable(True)
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
            item_widget.bar.SetNoEventAfterMove(True)
            item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index))
            item_widget.bar.UnBindMethod('OnBegin')
            item_widget.bar.UnBindMethod('OnDrag')
            item_widget.bar.UnBindMethod('OnEnd')
            item_widget.bar.UnBindMethod('OnCancel')
            fix_expire_time = 0
            item_widget.lab_limited.stopAllActions()
            if fix_expire_time:
                pass
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

    def _show_sfx(self, sfx_item_no):
        if not self.is_panel_visible():
            return
        else:
            conf = self.data_dict.get(str(sfx_item_no), {})
            sfx_path = conf.get('sfx_path', '')
            sfx_scale = conf.get('sfx_scale', 1.0)
            one_time = conf.get('time', 5550 / 1000.0)
            offset = conf.get('sfx_offset', None)
            self._show_sfx_2(sfx_path, sfx_scale, one_time, offset)
            return

    def _show_sfx_2(self, sfx_path, sfx_scale, one_time, offset):

        def single_show():
            if sfx_path:
                global_data.emgr.change_model_display_scene_tag_effect.emit(sfx_path, sfx_scale=sfx_scale, offset=offset)

        single_show()

        def start_loop():
            if self.panel:
                self.panel.StopTimerAction()
                self.panel.TimerAction(lambda t: single_show(), duration_sec=10000000, interval=one_time)

        start_loop()