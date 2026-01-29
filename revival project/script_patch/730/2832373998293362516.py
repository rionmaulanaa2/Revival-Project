# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ChangeClanName.py
from __future__ import absolute_import
import common.const.uiconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.gcommon.common_utils.ui_gameplay_utils import check_clan_name

class ChangeClanName(WindowSmallBase):
    PANEL_CONFIG_NAME = 'crew/crew_change_name'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'panel'

    def on_init_panel(self, *args, **kargs):
        super(ChangeClanName, self).on_init_panel()
        from common.cfg import confmgr
        import logic.comsys.common_ui.InputBox as InputBox
        name_limit = confmgr.get('clan_data', 'name_limit')
        self._input_box = InputBox.InputBox(self.panel.panel.inputbox, max_length=name_limit, placeholder=get_text_by_id(800024), need_sp_length_func=True)
        self._input_box.set_rise_widget(self.panel)
        self.panel.temp_price.temp_price.DeleteAllSubItem()
        self.panel.temp_price.temp_price.AddTemplateItem()

        @self.panel.panel.confirm.btn_common_big.callback()
        def OnClick(*args):
            clan_name = self._input_box.get_text()
            if not check_clan_name(clan_name):
                return
            global_data.player.change_clan_name(clan_name)

        @self.panel.panel.img_window_bg.btn_close.callback()
        def OnClick(*args):
            self.close()

        global_data.emgr.clan_mod_name += self.close

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        global_data.emgr.clan_mod_name -= self.close
        return