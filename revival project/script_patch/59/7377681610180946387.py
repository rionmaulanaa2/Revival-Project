# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/LobbySkyboxPreViewUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gutils import mall_utils
from logic.gutils import item_utils
from common.cfg import confmgr
from logic.gutils.jump_to_ui_utils import JUMP_MALL_UI_TO_BE_CLOSE
EXCEPTIONS_UI = [
 'LobbyRockerUI', 'MoveRockerUI']

class LobbySkyboxPreViewUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/lobby_skin_preview'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_back.OnClick': 'close'
       }
    GLOBAL_EVENT = {'privilege_lobby_skin_change': 'refresh_btn_state'
       }
    EXCEPTIONS_UI = [
     'LobbyRockerUI', 'MoveRockerUI']

    def on_init_panel(self, item_no):
        self.item_no = int(item_no)
        self.item_can_use = False
        self.cache_show_count = {}
        self.panel.lab_title.SetString(611567)
        self.panel.temp_price.setVisible(False)
        self.panel.lab_get_method.setVisible(True)
        self.panel.btn_use.lab_btn.setVisible(True)
        self.panel.btn_use.lab_btn.SetColor(0)
        self.panel.btn_left.setVisible(False)
        self.panel.btn_right.setVisible(False)
        self.refresh_item_info(self.item_no)
        self.refresh_btn_state()
        self.init_btn_state()
        self.return_lobby_scene()
        self.hide_main_ui(exceptions=EXCEPTIONS_UI)
        global_data.emgr.privilege_lobby_skin_change_force.emit(self.item_no)

    def init_btn_state(self):

        @self.panel.btn_use.btn_common.unique_callback()
        def OnClick(btn, touch):
            if not self.item_no:
                return
            if not global_data.player:
                return
            if self.item_can_use:
                global_data.player.change_lobby_skybox(self.item_no)
            self.refresh_btn_state()

        @self.panel.btn_dismount.btn_common.unique_callback()
        def OnClick(btn, touch):
            if not self.item_no:
                return
            if not global_data.player:
                return
            global_data.player.change_lobby_skybox(-1)
            self.refresh_btn_state()

    def refresh_item_info(self, item_no):
        self.panel.lab_skin_name.SetString(item_utils.get_lobby_item_desc(item_no))
        self.panel.temp_item.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
        self.panel.temp_item.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
        self.panel.lab_get_method.SetString(item_utils.get_item_access(item_no))

    def refresh_btn_state(self):
        self.item_can_use, _ = mall_utils.item_can_use_by_item_no(self.item_no)
        can_use = global_data.player.get_lobby_skybox_id() != self.item_no
        self.panel.btn_use.setVisible(can_use or self.item_can_use)
        self.panel.btn_use.btn_common.lab_btn.SetString(80338)
        if self.item_can_use:
            self.panel.btn_use.btn_common.SetEnable(True)
        else:
            self.panel.btn_use.btn_common.SetEnable(False)
        item_can_dismount = global_data.player.get_lobby_skybox_id() == self.item_no
        self.panel.btn_dismount.setVisible(item_can_dismount)
        if item_can_dismount:
            self.panel.btn_dismount.btn_common.SetEnable(False)
            self.panel.btn_dismount.btn_common.SetText(2213)

    def cache_ui_show_count(self):
        for ui_name in self.EXCEPTIONS_UI:
            ui = global_data.ui_mgr.get_ui(ui_name)
            if ui:
                self.cache_show_count[ui_name] = ui.get_show_count_dict()
                ui.clear_show_count_dict()

    def recover_ui_show_count(self):
        if not self.cache_show_count:
            return
        for ui_name in self.EXCEPTIONS_UI:
            ui = global_data.ui_mgr.get_ui(ui_name)
            if ui:
                show_count = ui.get_show_count_dict()
                show_count.update(self.cache_show_count.get(ui_name))
                ui.set_show_count_dict(show_count)

        self.cache_show_count = {}

    def do_show_panel(self):
        super(LobbySkyboxPreViewUI, self).do_show_panel()
        self.return_lobby_scene()
        self.cache_ui_show_count()

    def do_hide_panel(self):
        super(LobbySkyboxPreViewUI, self).do_hide_panel()
        self.recover_ui_show_count()

    def return_lobby_scene(self):
        for i in range(len(global_data.ex_scene_mgr_agent.scene_stack)):
            global_data.emgr.leave_current_scene.emit()

        global_data.emgr.reset_rotate_model_display.emit()

    def on_finalize_panel(self):
        if global_data.player and self.item_no != global_data.player.get_lobby_skybox_id():
            global_data.emgr.privilege_lobby_skin_change_force.emit(-1)
        self.show_main_ui()
        self.recover_ui_show_count()
        if global_data.player and self.item_no != global_data.player.get_lobby_skybox_id():
            global_data.emgr.privilege_lobby_skin_change_force.emit(-1)