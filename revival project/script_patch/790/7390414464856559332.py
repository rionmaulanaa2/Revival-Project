# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaCancelUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from common.const import uiconst

class MechaCancelUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_mech_cancel'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    HOT_KEY_FUNC_MAP = {'cancel_action': 'on_cancel'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'cancel_action': {'node': 'btn_cancel.temp_pc'}}
    UI_ACTION_EVENT = {'btn_cancel.OnClick': 'on_cancel'
       }

    def on_init_panel(self, cancel_callback, need_mouse_right_btn_cancel=False):
        self.cancel_callback = cancel_callback
        global_data.emgr.net_reconnect_event += self.on_net_reconnect
        self.mouse_right_btn_cancel = need_mouse_right_btn_cancel
        self.update_cancel_hot_key_show(need_mouse_right_btn_cancel)
        self.init_custom_com()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_net_reconnect(self, *args):
        self.close()

    def on_finalize_panel(self):
        global_data.emgr.net_reconnect_event -= self.on_net_reconnect
        self.destroy_widget('custom_ui_com')

    def on_cancel(self, *args):
        if self.cancel_callback:
            self.cancel_callback()
        self.close()

    def update_cancel_hot_key_show(self, need_mouse_right_btn_cancel):
        if need_mouse_right_btn_cancel:
            self.HOT_KEY_FUNC_MAP_SHOW['mecha_cancel_action'] = {'node': 'btn_cancel.temp_pc'}
            if 'cancel_action' in self.HOT_KEY_FUNC_MAP_SHOW:
                del self.HOT_KEY_FUNC_MAP_SHOW['cancel_action']
        else:
            self.HOT_KEY_FUNC_MAP_SHOW['cancel_action'] = {'node': 'btn_cancel.temp_pc'}
            if 'mecha_cancel_action' in self.HOT_KEY_FUNC_MAP_SHOW:
                del self.HOT_KEY_FUNC_MAP_SHOW['mecha_cancel_action']

    def do_show_panel(self):
        if self.mouse_right_btn_cancel:
            self.HOT_KEY_FUNC_MAP['mecha_cancel_action'] = 'on_cancel'
        elif 'mecha_cancel_action' in self.HOT_KEY_FUNC_MAP:
            del self.HOT_KEY_FUNC_MAP['mecha_cancel_action']
        super(MechaCancelUI, self).do_show_panel()

    def get_cancel_callback(self):
        return self.cancel_callback