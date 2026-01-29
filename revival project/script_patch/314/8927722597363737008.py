# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/ExDescibeWidget.py
from __future__ import absolute_import
from common.cfg import confmgr
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils.mecha_skin_utils import get_mecha_conf_ex_weapon_sfx_id
from logic.gutils import item_utils

class ExDescibeWidget(BaseUIWidget):

    def __init__(self, parent_ui, panel):
        super(ExDescibeWidget, self).__init__(parent_ui, panel)
        self._mecha_skin_id = None
        self._is_previewing = False
        self.shiny_weapon_id = None
        self.mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        self._init_panel()
        return

    def refresh_mecha_skin_id(self, skin_id, go_to_func=None):
        self._mecha_skin_id = skin_id
        self._go_to_func = go_to_func
        self.panel.PlayAnimation('show')
        self.refresh_panel()

    def refresh_panel(self):
        if self._mecha_skin_id is None:
            return
        else:
            self.shiny_weapon_id = get_mecha_conf_ex_weapon_sfx_id(self._mecha_skin_id)
            if not global_data.player or global_data.player.get_item_by_no(self.shiny_weapon_id):
                self.panel.btn_view.setVisible(False)
                self.panel.btn_go.setVisible(False)
                self.panel.nd_more.SetContentSize(186, 110)
                self.panel.nd_more.ChildResizeAndPosition()
            else:
                self.panel.btn_view.setVisible(True)
                self.panel.btn_go.setVisible(True)
                self.panel.nd_more.SetContentSize(186, 240)
            self.panel.nd_more.ChildResizeAndPosition()
            return

    def destroy(self):
        self._go_to_func = None
        super(ExDescibeWidget, self).destroy()
        return

    def _clear_preview_sate(self):
        self._is_previewing = False
        self.panel.btn_view.btn_common.SetText(608104)
        if not global_data.player or not global_data.player.get_item_by_no(self.shiny_weapon_id):
            global_data.emgr.show_shiny_weapon_sfx.emit(self._mecha_skin_id, None, self.shiny_weapon_id)
        return

    def _init_panel(self):

        @self.panel.btn_ex.unique_callback()
        def OnClick(*args):
            nd_more_is_opening = self.panel.nd_more.IsVisible()
            self.panel.nd_more.setVisible(not nd_more_is_opening)
            if nd_more_is_opening:
                self._clear_preview_sate()

        @self.panel.nd_more.nd_close.unique_callback()
        def OnClick(*args):
            if self.panel.nd_more.IsVisible():
                self.panel.nd_more.setVisible(False)
                self._clear_preview_sate()

        @self.panel.btn_info.unique_callback()
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(608114, 608115)

        @self.panel.btn_video.btn_common.unique_callback()
        def OnClick(*args):
            if self.shiny_weapon_id is None:
                return
            else:
                import game3d
                video_url = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(self._mecha_skin_id), 'shiny_weapon_video_website', default=None)
                if video_url:
                    game3d.open_url(video_url)
                else:
                    global_data.game_mgr.show_tip(10063)
                return

        @self.panel.btn_view.btn_common.unique_callback()
        def OnClick(*args):
            if self._mecha_skin_id is None:
                return
            else:
                if self._is_previewing:
                    self._clear_preview_sate()
                else:
                    self._is_previewing = True
                    self.mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
                    shiny_id = get_mecha_conf_ex_weapon_sfx_id(self._mecha_skin_id)
                    if shiny_id:
                        global_data.emgr.show_shiny_weapon_sfx.emit(self._mecha_skin_id, shiny_id, None)
                    self.panel.btn_view.btn_common.SetText(608105)
                return

        @self.panel.btn_go.btn_common.unique_callback()
        def OnClick(*args):
            if self._go_to_func is None:
                from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
                jump_to_display_detail_by_item_no(self._mecha_skin_id)
            else:
                self._go_to_func(self._mecha_skin_id)
            return