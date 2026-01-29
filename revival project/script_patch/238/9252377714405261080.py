# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVELevelWidgetUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_0, UI_VKB_CLOSE, UI_TYPE_MESSAGE
from .PVESelectLevelWidget import PVESelectLevelWidget
from .PVESelectLevelMechaWidget import PVESelectLevelMechaWidget
from .PVESelectLevelArchiveWidget import PVESelectLevelArchiveWidget
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gcommon.const import SHOP_PAYMENT_ITEM_PVE_KEY, SHOP_PAYMENT_ITEM_PVE_COIN
from logic.client.const.lobby_model_display_const import ROTATE_FACTOR
from logic.gutils.pve_utils import reset_model_and_cam_pos
from logic.comsys.battle.pve.PVELeftTopWidget import PVELeftTopWidget
from logic.comsys.lobby.LobbyVoiceWidget import LobbyVoiceWidget
MAIN_NORMAL_POSITION = [
 -7, 0, 0]

class PVELevelWidgetUI(BasePanel):
    DELAY_CLOSE_TAG = 20231127
    PANEL_CONFIG_NAME = 'pve/select_level_new/select_level_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_0
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }
    GLOBAL_EVENT = {'del_mecha_pose_result_event': 'on_mecha_skin_dress_record_change'
       }

    def on_init_panel(self, *args, **kwargs):
        super(PVELevelWidgetUI, self).on_init_panel()
        if global_data.player:
            global_data.player.check_pve_selected_mecha_is_available()
        self.init_params()
        self.init_ui()
        self.init_ui_event()
        self.hide_main_ui(exceptions=['MainChat'], exception_types=(UI_TYPE_MESSAGE,))

    def init_params(self):
        self._disappearing = False
        self._level_widget = None
        self._mecha_widget = None
        self._pve_left_top_widget = None
        self._voice_widget = None
        self._price_top_widget = None
        self._archive_widget = None
        self._has_change_mecha_skin = False
        self._nd_touch_IDs = []
        return

    def init_ui(self):
        self.panel.PlayAnimation('loop')
        self.panel.PlayAnimation('show_completed')
        self.panel.PlayAnimation('appear')
        self._level_widget = PVESelectLevelWidget(self, self.panel.nd_level)
        self._mecha_widget = PVESelectLevelMechaWidget(self, self.panel)
        self._pve_left_top_widget = PVELeftTopWidget(self, self.panel)
        self._voice_widget = LobbyVoiceWidget(self, self.panel)
        self._archive_widget = None
        self._init_money_widget()
        return

    def is_showing_skin_choose_widget(self):
        if not self._mecha_widget:
            return False
        return self._mecha_widget.is_showing_skin_widget

    def init_ui_event(self):

        @self.panel.nd_mech_touch.unique_callback()
        def OnBegin(layer, touch):
            if len(self._nd_touch_IDs) > 1:
                return False
            tid = touch.getId()
            if tid not in self._nd_touch_IDs:
                self._nd_touch_IDs.append(tid)
            return True

        @self.panel.nd_mech_touch.unique_callback()
        def OnDrag(layer, touch):
            tid = touch.getId()
            if tid not in self._nd_touch_IDs:
                return
            if len(self._nd_touch_IDs) == 1:
                delta_pos = touch.getDelta()
                global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

        @self.panel.nd_mech_touch.unique_callback()
        def OnEnd(layer, touch):
            tid = touch.getId()
            if tid in self._nd_touch_IDs:
                self._nd_touch_IDs.remove(tid)

        @self.panel.nd_main.nd_level.btn_file.unique_callback()
        def OnClick(layer, touch, *args):
            if not self._archive_widget:
                self._archive_widget = PVESelectLevelArchiveWidget(self, self.panel)
            global_data.emgr.reset_rotate_model_display.emit()
            self._archive_widget.init_archive()
            self._archive_widget.refresh_model()
            self.nd_main.setVisible(False)
            self.nd_file.setVisible(True)

        @self.panel.btn_friends.unique_callback()
        def OnClick(layer, touch, *args):
            global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')

        @self.panel.btn_mail.unique_callback()
        def OnClick(layer, touch, *args):
            global_data.ui_mgr.show_ui('MainEmail', 'logic.comsys.message')

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self._init_money_widget
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _init_money_widget--- This code section failed: ---

 130       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  '_price_top_widget'
           6  POP_JUMP_IF_TRUE     64  'to 64'

 131       9  LOAD_GLOBAL           1  'PriceUIWidget'
          12  LOAD_GLOBAL           1  'PriceUIWidget'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'panel'
          21  LOAD_ATTR             3  'list_money'
          24  LOAD_CONST            2  'pnl_title'
          27  LOAD_GLOBAL           4  'False'
          30  CALL_FUNCTION_513   513 
          33  LOAD_FAST             0  'self'
          36  STORE_ATTR            0  '_price_top_widget'

 132      39  LOAD_FAST             0  'self'
          42  LOAD_ATTR             0  '_price_top_widget'
          45  LOAD_ATTR             5  'show_money_types'
          48  LOAD_GLOBAL           6  'SHOP_PAYMENT_ITEM_PVE_KEY'
          51  LOAD_GLOBAL           7  'SHOP_PAYMENT_ITEM_PVE_COIN'
          54  BUILD_LIST_2          2 
          57  CALL_FUNCTION_1       1 
          60  POP_TOP          
          61  JUMP_FORWARD         13  'to 77'

 134      64  LOAD_FAST             0  'self'
          67  LOAD_ATTR             0  '_price_top_widget'
          70  LOAD_ATTR             8  '_on_player_info_update'
          73  CALL_FUNCTION_0       0 
          76  POP_TOP          
        77_0  COME_FROM                '61'

Parse error at or near `CALL_FUNCTION_513' instruction at offset 30

    def on_resolution_changed(self):
        super(PVELevelWidgetUI, self).on_resolution_changed()
        if self._mecha_widget and self._mecha_widget.is_showing_skin_widget:
            self.PlayAnimation('switch')

    def do_show_panel(self):
        super(PVELevelWidgetUI, self).do_show_panel()
        self.process_events(True)
        self.do_switch_scene()
        ui = global_data.ui_mgr.get_ui('PVEMainUI')
        if ui:
            if self._has_change_mecha_skin and self._mecha_widget:
                skin_choose_widget = self._mecha_widget.get_skin_choose_widget()
                if skin_choose_widget:
                    cur_mecha_id, _ = skin_choose_widget.get_current_id()
                    skin_choose_widget.update_nd_skin_choose(cur_mecha_id)
                    self._has_change_mecha_skin = False
            else:
                ui.update_shiny_weapon()
            if self._mecha_widget.is_showing_skin_widget:
                reset_model_and_cam_pos()
            else:
                ui.update_model_and_cam_pos()

    def do_hide_panel(self):
        super(PVELevelWidgetUI, self).do_hide_panel()
        self.process_events(False)

    def do_switch_scene(self):
        from logic.gcommon.common_const.scene_const import SCENE_PVE_MAIN_UI
        from logic.client.const.lobby_model_display_const import PVE_MAIN_UI
        global_data.emgr.show_lobby_relatived_scene.emit(SCENE_PVE_MAIN_UI, PVE_MAIN_UI, belong_ui_name='PVEMainUI')

    def jump_to_chapter(self, chapter, difficulty):
        self._level_widget and self._level_widget.jump_to_chapter(chapter, difficulty)

    def on_mecha_skin_dress_record_change(self):
        self._has_change_mecha_skin = True

    def get_match_info(self):
        if self._level_widget:
            return self._level_widget.get_match_info()
        else:
            return (None, None, None)

    def close(self, *args):
        self.play_disappear_anim()

    def play_disappear_anim(self):
        if self._disappearing:
            return
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime('disappear')

        def delay_call(*args):
            self._disappearing = False
            global_data.ui_mgr.close_ui(self.get_name())

        self.panel.StopAnimation('disappear')
        self.panel.DelayCallWithTag(anim_time, delay_call, self.DELAY_CLOSE_TAG)
        self.panel.PlayAnimation('disappear')

    @staticmethod
    def check_red_point():
        return False

    def on_finalize_panel(self):
        self.process_events(False)
        if self._level_widget:
            self._level_widget.destroy()
            self._level_widget = None
        if self._mecha_widget:
            self._mecha_widget.destroy()
            self._mecha_widget = None
        if self._pve_left_top_widget:
            self._pve_left_top_widget.destroy()
            self._pve_left_top_widget = None
        if self._voice_widget:
            self._voice_widget.destroy()
            self._voice_widget = None
        if self._price_top_widget:
            self._price_top_widget.destroy()
            self._price_top_widget = None
        if self._archive_widget:
            self._archive_widget.destroy()
            self._archive_widget = None
        self._disappearing = None
        self._nd_touch_IDs = None
        self.show_main_ui()
        reset_model_and_cam_pos()
        super(PVELevelWidgetUI, self).on_finalize_panel()
        return