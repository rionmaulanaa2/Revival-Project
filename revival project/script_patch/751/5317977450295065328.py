# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVESelectLevelSkinWidget.py
from __future__ import absolute_import
from logic.gutils.dress_utils import DEFAULT_CLOTHING_ID
from .PVEMechaChooseWidget import PVEMechaChooseWidget
from .PVESkinChooseWidget import PVESkinChooseWidget
from logic.gutils.pve_utils import update_model_and_cam_pos
NORMAL_POSITION = [
 -130, 0, 0]

class PVESelectLevelSkinWidget(object):

    def __init__(self, parent, panel):
        self._parent = parent
        self._panel = panel
        self.init_params()
        self.init_ui()
        self.init_ui_event()
        self.process_events(True)

    def init_params(self):
        self._need_update_model_and_cam_pos = None
        return

    def init_ui(self):
        self._mecha_choose_widget = PVEMechaChooseWidget(self._parent, self._panel.list_mecha)
        self._skin_choose_widget = PVESkinChooseWidget(self._parent, self._panel.nd_skin_choose)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_pve_main_model_load_complete': self.on_pve_main_model_load_complete
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_ui_event(self):

        @self._panel.btn_back.callback()
        def OnClick(btn, touch):
            if global_data.player:
                _, clothing_id = self._skin_choose_widget.get_current_id()
                pve_mecha_id = global_data.player.get_pve_selected_mecha_item_id() if global_data.player else None
                model_id = global_data.player.get_pve_using_mecha_skin(pve_mecha_id) if global_data.player else DEFAULT_CLOTHING_ID
                if clothing_id == model_id:
                    update_model_and_cam_pos(NORMAL_POSITION, NORMAL_POSITION)
                else:
                    self._need_update_model_and_cam_pos = True
                    global_data.emgr.on_pve_mecha_show_changed.emit(global_data.player.get_pve_select_mecha_id())
                global_data.emgr.on_pve_select_skin_widget_hide.emit()
                self._parent.panel.PlayAnimation('revert')
            return

    def on_pve_main_model_load_complete(self, *args):
        if self._need_update_model_and_cam_pos:
            update_model_and_cam_pos(NORMAL_POSITION, NORMAL_POSITION)
            self._need_update_model_and_cam_pos = False

    def get_skin_choose_widget(self):
        return self._skin_choose_widget

    def get_current_id(self):
        if self._skin_choose_widget:
            return self._skin_choose_widget.get_current_id()
        else:
            return (None, None)
            return None

    def destroy(self):
        self.process_events(False)
        self._need_update_model_and_cam_pos = None
        if self._mecha_choose_widget:
            self._mecha_choose_widget.destroy()
            self._mecha_choose_widget = None
        if self._skin_choose_widget:
            self._skin_choose_widget.destroy()
            self._skin_choose_widget = None
        return