# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaBulletReloadUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gutils import mecha_utils
ASSOCIATE_UI_LIST = [
 'BulletReloadUI']
from common.const import uiconst

class MechaBulletReloadUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/mech_fight_bullet_reload'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'reload_button.OnClick': 'on_click_reload_button'
       }

    def on_init_panel(self):
        self.panel.setLocalZOrder(BASE_LAYER_ZORDER)
        self.init_parameters()
        self.init_event()
        self.hide_main_ui(ASSOCIATE_UI_LIST)
        from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
        UIDistorterHelper().apply_ui_distort(self.__class__.__name__)

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.show_main_ui()
        self.player = None
        return

    def init_parameters(self):
        self.player = None
        self.count_down = {'reload': 0
           }
        self.cd_timer = {'reload': None
           }
        emgr = global_data.emgr
        if global_data.player:
            self.on_player_setted(global_data.player.logic)
        emgr.scene_player_setted_event += self.on_player_setted
        econf = {}
        emgr.bind_events(econf)
        return

    def init_event(self):
        pass

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        if self.player:
            self.bind_ui_event(self.player)

    def on_mecha_setted(self, mecha):
        if mecha:
            regist_func = mecha.regist_event
            regist_func('E_RELOADING', self.on_reload_bullet)
            regist_func('E_SET_ACTION_VISIBLE', self.on_action_ui_show)
            self.init_event()

    def bind_ui_event(self, target):
        if target:
            pass

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            mecha = global_data.mecha
            if mecha and mecha.logic:
                unregist_func = mecha.logic.unregist_event
                unregist_func('E_RELOADING', self.on_reload_bullet)
                unregist_func('E_SET_ACTION_VISIBLE', self.on_action_ui_show)

    def on_click_reload_button(self, btn, touch):
        self.panel.PlayAnimation('reload_click')
        if self.count_down['reload'] > 0:
            return
        mecha = global_data.mecha
        if mecha and mecha.logic:
            mecha = mecha.logic
            mecha.send_event('E_TRY_RELOAD')

    def on_reload_bullet(self, reload_time, times, *args):
        if self.cd_timer['reload']:
            return
        nd = self.panel.reload_shield
        mecha_utils.start_count_down(self, nd, nd.reload_time, nd.progress_reload, reload_time, 'reload')
        global_data.emgr.on_reload_bullet_event.emit(reload_time, times)

    def on_action_ui_show(self, action, visible):
        if action == 'action8':
            self.panel.setVisible(visible)