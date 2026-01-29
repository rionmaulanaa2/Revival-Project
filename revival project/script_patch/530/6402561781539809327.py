# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/ObtainCareerTitleUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CUSTOM
from logic.comsys.role.ObtainCareerTitleBgUI import ObtainCareerTitleBgUI
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import refresh_career_title_node
from logic.gutils import title_utils

class ObtainCareerTitleUI(BasePanel):
    PANEL_CONFIG_NAME = 'role/get_achievement'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    IS_FULLSCREEN = True
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'temp_close.btn_back.OnClick': '_try_close',
       'temp_use.btn_common_big.OnClick': '_on_use_btn_clicked',
       'temp_share.btn_common_big.OnClick': '_on_share_btn_clicked'
       }

    def on_init_panel(self):
        self.hide()

        def show_bg():
            ObtainCareerTitleBgUI()

        self.panel.DelayCall(0.5, show_bg)
        self.hide_main_ui()
        self.init_parameters()

    def init_parameters(self):
        self._ready = False
        self._to_show_titld_item_no_list = []
        self._showing_title_item_no = None
        self._screen_capture_helper = ScreenFrameHelper()
        return

    def ui_vkb_custom_func(self, *argv):
        self._try_close()

    def on_finalize_panel(self):
        self.show_main_ui()
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
            self._screen_capture_helper = None
        global_data.ui_mgr.close_ui('ObtainCareerTitleBgUI')
        super(ObtainCareerTitleUI, self).on_finalize_panel()
        return

    def append_title(self, title_item_no):
        if title_item_no is None:
            return
        else:
            self._to_show_titld_item_no_list.append(title_item_no)
            return

    def _try_show_one_title(self):
        if not self._to_show_titld_item_no_list:
            return False
        self._showing_title_item_no = self._to_show_titld_item_no_list.pop(0)
        self._show_one_title(self._showing_title_item_no)
        return True

    def _show_one_title(self, title_item_no):
        self.panel.lab_get.SetString(get_text_by_id(910004, args={'title_type_name': title_utils.get_title_type_name(title_item_no)}))
        refresh_career_title_node(self.panel.temp_name, title_item_no)
        self.panel.PlayAnimation('show')

    def ready(self):
        self.show()
        self._ready = True
        result = self._try_show_one_title()
        if not result:
            self.close()

    def _try_close(self, *argv):
        if not self._ready:
            return
        result = self._try_show_one_title()
        if not result:
            self.close()

    def _request_change_title(self):
        if self._showing_title_item_no is None:
            return
        else:
            if global_data.player:
                global_data.player.try_set_title(self._showing_title_item_no)
            return

    def _on_use_btn_clicked(self, *argv):
        if not self._ready:
            return
        self._request_change_title()
        self._try_close()

    def _on_share_btn_clicked(self, *argv):
        if not self._ready:
            return
        ui_names = [self.__class__.__name__, 'ObtainCareerTitleBgUI']

        def cb(*args):
            self.panel.temp_close.setVisible(True)
            self.panel.nd_control.setVisible(True)

        if self._screen_capture_helper:
            self.panel.temp_close.setVisible(False)
            self.panel.nd_control.setVisible(False)
            self._screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=cb)