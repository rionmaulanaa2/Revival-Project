# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/ProjectionKillFunctionWidget.py
from __future__ import absolute_import
from logic.gutils import mall_utils
from logic.comsys.items_book_ui.ProjectionKillGetUseBuyWidget import ProjectionKillGetUseBuyWidget
from logic.gutils import items_book_utils
from logic.client.const import items_book_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import item_utils
from common.framework import Functor
from logic.gutils import lobby_model_display_utils
from logic.gcommon import time_utility
from logic.gcommon.item.item_const import BATTLE_EFFECT_KILL
from logic.gutils import red_point_utils
from common.cfg import confmgr
from logic.comsys.items_book_ui.FunctionWidgetBase import FunctionWidgetBase
from logic.gutils.mecha_utils import ProjectionKillModel
from logic.gutils.mecha_skin_utils import get_mecha_skin_no_by_item_no
from logic.gutils.template_utils import set_ui_show_picture
ROTATE_FACTOR = 850

class ProjectionKillFunctionWidget(FunctionWidgetBase):

    def __init__(self, parent, panel):
        super(ProjectionKillFunctionWidget, self).__init__(parent, panel)
        self.selected_skin_list = None
        self._projection_kill_model = None
        self.init_widget()
        return

    def destroy(self):
        super(ProjectionKillFunctionWidget, self).destroy()
        self.selected_skin_list = []
        self._projection_kill_get_use_buy_widget.destroy()
        self._projection_kill_get_use_buy_widget = None
        self.data_dict = None
        if self._projection_kill_model:
            self._projection_kill_model.destroy()
            self._projection_kill_model = None
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
        self._projection_kill_get_use_buy_widget = ProjectionKillGetUseBuyWidget(self, self.panel.btn_buy_1, self.panel.btn_use, self.panel.btn_cancle, self.panel.btn_go, self.panel.temp_price, self.panel.nd_killsfx.btn_go.lab_get_method)

    def on_click_skin_item(self, index, *args):
        if not self.panel:
            return
        else:
            if not self.selected_skin_list:
                return
            if self.sel_before_cb:
                self.sel_before_cb(self.get_parent_selected_item_index(), index)
            item_widget = self.panel.list_item_kill.GetItem(index)
            projection_kill_no = self.selected_skin_list[index]
            selected_item_no = projection_kill_no
            show_new = global_data.lobby_red_point_data.get_rp_by_no(projection_kill_no)
            self._show_model(projection_kill_no)
            self.panel.lab_name.SetString(item_utils.get_lobby_item_name(projection_kill_no))
            self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(projection_kill_no))
            if show_new:
                global_data.player.req_del_item_redpoint(projection_kill_no)
                red_point_utils.show_red_point_template(item_widget.nd_new, False)
            global_data.emgr.select_item_goods.emit(projection_kill_no)
            skin_config_dict = items_book_utils.get_items_conf_by_config_name('KillSfxConfig')
            goods_id = skin_config_dict.get(projection_kill_no, {}).get('goods_id', None)
            self._projection_kill_get_use_buy_widget.update_target_item_no(selected_item_no, goods_id)
            if self.sel_callback:
                self.sel_callback()
            return

    def on_create_skin_item(self, lst, index, item_widget):
        no_destroy = not item_widget.IsDestroyed()
        valid = index < len(self.selected_skin_list) and self.selected_skin_list[index] is not None and no_destroy
        if valid:
            projection_kill_no = self.selected_skin_list[index]
            mecha_skin_no = get_mecha_skin_no_by_item_no(projection_kill_no)
            set_ui_show_picture(mecha_skin_no, mecha_nd=item_widget.img_pic)
            item_widget.choose.setVisible(False)
            cur_projection_kill_no = None
            if global_data.player:
                cur_projection_kill_no = global_data.player.get_current_selected_projection_kill_no()
            item_widget.img_using.setVisible(str(cur_projection_kill_no) == str(projection_kill_no))
            item_can_use, _ = mall_utils.item_can_use_by_item_no(projection_kill_no)
            item_widget.icon_lock.setVisible(not item_can_use)
            item_utils.check_skin_tag(item_widget.temp_level, projection_kill_no)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(projection_kill_no)
            red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
            item_widget.bar.SetEnable(True)
            item_widget.bar.SetNoEventAfterMove(True)
            item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index))
            item_widget.bar.UnBindMethod('OnBegin')
            item_widget.bar.UnBindMethod('OnDrag')
            item_widget.bar.UnBindMethod('OnEnd')
            item_widget.bar.UnBindMethod('OnCancel')
        item_widget.setVisible(valid)
        return

    def _show_model(self, projection_kill_no):
        if not self.is_panel_visible():
            return
        mecha_skin_no = get_mecha_skin_no_by_item_no(projection_kill_no)
        self._projection_kill_model = ProjectionKillModel(projection_kill_no, mecha_skin_no)