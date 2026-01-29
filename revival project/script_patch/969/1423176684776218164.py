# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/FullScreenBackUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import GUIDE_LAYER_ZORDER, UI_VKB_CLOSE
from common.cfg import confmgr
from logic.gutils.skin_define_utils import init_action_list, delete_action_list
import copy

class FullScreenBackUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/full_screen'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'on_click_back_btn',
       'btn_zoom.OnClick': 'on_click_zoom_btn',
       'btn_action.OnClick': 'on_click_action'
       }

    def on_init_panel(self, need_guide_action=False, *args, **kwargs):
        self._callback = None
        self._zoom_callback = None
        self.action_conf = copy.deepcopy(confmgr.get('skin_define_action'))
        self.no_action_tag = True
        self.panel.PlayAnimation('appear')
        if need_guide_action:
            self.is_guided_action = global_data.achi_mgr.get_cur_user_archive_data('skin_define_full_screen_action')
            if not self.is_guided_action:
                global_data.ui_mgr.show_ui('SkinDefineGuideFullScreenActionUI', 'logic.comsys.mecha_display')
                self.is_guided_action = True
        self.mecha_id = None
        self.skin_id = 1
        return

    def setBackFunctionCallback(self, callback):
        self._callback = callback

    def setZoomButtonCallback(self, callback):
        self._zoom_callback = callback

    def on_click_back_btn(self, *args):
        if self.mecha_id is not None:
            delete_action_list(self)
        self.close()
        return

    def on_click_zoom_btn(self, *args):
        if self._zoom_callback:
            ret = self._zoom_callback()
            if ret:
                self.panel.btn_zoom.icon.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/icon/icon_zoom_in.png')
            else:
                self.panel.btn_zoom.icon.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/icon/icon_zoom_out.png')

    def set_zoom_btn_visible(self, is_visible):
        self.panel.btn_zoom.setVisible(is_visible)

    def set_mecha_info(self, mecha_id, skin_id):
        self.mecha_id = mecha_id
        self.skin_id = skin_id
        self.init_action_list()

    def set_action_list_vis(self, is_visible):
        self.panel.btn_action.setVisible(is_visible)

    def on_click_action(self, *args):
        if self.no_action_tag:
            return
        if self.panel.actione_list.isVisible():
            self.hide_action_list()
        else:
            self.show_action_list()

    def show_action_list(self):
        self.panel.actione_list.setVisible(True)
        self.panel.btn_action.img_icon.setRotation(180)

    def hide_action_lsit(self):
        self.panel.actione_list.setVisible(False)
        self.panel.btn_action.img_icon.setRotation(0)

    def init_action_list(self):
        action_list = self.action_conf.get(str(self.skin_id), {}).get('cAction', [])
        if not action_list:
            action_list = self.action_conf.get(str(self.mecha_id), {}).get('cAction', [])
            if not action_list:
                log_error('\xe6\x90\x9e\xe9\x94\xa4\xe5\xad\x90\xef\xbc\x9f \xe8\xa1\xa8\xe9\x83\xbd\xe4\xb8\x8d\xe5\xa1\xab\xef\xbc\x9f')
                self.no_action_tag = True
                self.set_action_list_vis(False)
                return
        self.no_action_tag = False
        init_action_list(self, action_list)

    def on_finalize_panel(self):
        self.panel.PlayAnimation('disappear')
        self._zoom_callback = None
        if self._callback:
            self._callback()
        self._callback = None
        return