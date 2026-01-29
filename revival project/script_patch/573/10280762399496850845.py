# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanAnnounceUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils import clan_utils
from logic.gutils import template_utils
from common.cfg import confmgr

class ClanAnnounceUI(BasePanel):
    PANEL_CONFIG_NAME = 'crew/i_crew_announcement'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    GLOBAL_EVENT = {'clan_mod_intro': 'on_clan_mod_intro'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, *args, **kargs):
        self._input_box = None

        @self.panel.panel.btn_close.callback()
        def OnClick(*args):
            self.close()

        self.init_widget()
        return

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        return

    def do_show_panel(self):
        super(ClanAnnounceUI, self).do_show_panel()

    def on_clan_mod_intro(self):
        self.init_widget()

    def on_confirm(self, *args):
        pass

    def init_widget(self):
        import logic.comsys.common_ui.InputBox as InputBox
        from logic.gcommon.common_utils.text_utils import check_review_words
        info = global_data.player.get_clan_info()
        max_length = confmgr.get('clan_data', 'intro_limit', default=100)
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        self._input_box = InputBox.InputBox(self.panel.panel.inputbox, placeholder=10047, input_callback=self.input_callback, max_length=max_length, need_sp_length_func=True)
        self._input_box.set_rise_widget(self.panel)
        self._input_box.set_text(info['intro'])

        @self.panel.confirm.btn_common_big.callback()
        def OnClick(*args):
            text = self._input_box.get_text()
            if not text:
                text = ''
            else:
                flag, text = check_review_words(text)
                if not flag:
                    global_data.game_mgr.show_tip(get_text_by_id(800094), True)
                    return
            global_data.player.change_clan_intro(text)
            self.close()

        return

    def input_callback(self, text):
        pass