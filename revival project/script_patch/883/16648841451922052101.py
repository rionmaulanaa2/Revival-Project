# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/QuickMarkBtnPC.py
from __future__ import absolute_import
from .QuickMarkBtn import QuickMarkBtn
from logic.comsys.map.InteractionInvokeBtnWidget import InteractionInvokeBtnWidget
from logic.comsys.battle.spray.SprayUIPC import SprayUIPC
from logic.comsys.battle.spray.SprayUI import SprayUI
from logic.client.const import game_mode_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode

class QuickMarkBtnPC(QuickMarkBtn):
    HOT_KEY_FUNC_MAP = {'switch_scene_mark.PRESS': 'keyboard_use_mark_ui',
       'switch_scene_mark.CANCEL': 'keyboard_use_mark_ui_cancel',
       'double_mark_item.DOWN_UP': 'keyboard_mark_item',
       'switch_interaction.CANCEL': 'keyboard_use_spray_ui_cancel',
       'switch_interaction.DOWN_UP': 'keyboard_use_spray_ui'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'switch_scene_mark': {'node': 'layer_locate.temp_pc'},'switch_interaction': {'node': 'nd_action_spray.temp_pc'}}

    def show(self):
        BasePanel.show(self)

    def refresh_ui_visible(self):
        self.modify_pve_panel_position()

    @execute_by_mode(True, (game_mode_const.GAME_MODE_PVE, game_mode_const.GAME_MODE_PVE_EDIT))
    def modify_pve_panel_position(self):
        self.panel.nd_custom_1.SetPosition('100%-110', '100%-92')
        self.panel.nd_custom_2.SetPosition('100%-181', '100%-99')
        self.panel.nd_custom_3.SetPosition('100%-31', '100%-85')

    def on_init_panel(self, *args, **kwargs):
        super(QuickMarkBtnPC, self).on_init_panel(*args, **kwargs)
        self.panel.setVisible(False)
        self.panel.nd_custom_1.setVisible(False)
        self.panel.nd_custom_2.setVisible(False)

    def is_click_in_chat_btn(self, touch):
        pass

    def init_widget(self):
        self._inter_invoke_btn_widget = InteractionInvokeBtnWidget(self.panel.btn_action_spray, self.panel, SprayUIPC, self.__class__.__name__)
        self._inter_invoke_btn_widget.decorate_touch_inter_begin_logic(self._on_touch_inter_begin_decorator)
        self.init_spray_event()
        self.hide_mark_btn()
        self.hide_speak_btn()
        self.panel.btn_chat.setVisible(False)
        self.panel.nd_custom_4.setVisible(False)
        from .QuickMarkUIPC import QuickMarkUIPC
        QuickMarkUIPC()
        self.map_mark_sel_btn = None
        self.is_in_mark_func = False

        @self.panel.btn_normal_locate.unique_callback()
        def OnBegin(btn, touch):
            self.is_in_mark_func = True
            ui_inst = global_data.ui_mgr.get_ui('QuickMarkUI')
            if ui_inst:
                ui_inst.on_begin(touch.getLocation())
                ui_inst.enable_mid_map(False)
            return True

        @self.panel.btn_normal_locate.unique_callback()
        def OnDrag(btn, touch):
            touch_wpos = touch.getLocation()
            ui_inst = global_data.ui_mgr.get_ui('QuickMarkUI')
            if ui_inst:
                ui_inst.on_drag(touch_wpos)
            return True

        @self.panel.btn_normal_locate.unique_callback()
        def OnEnd(btn, touch):
            touch_wpos = touch.getLocation()
            self.is_in_mark_func = False
            ui_inst = global_data.ui_mgr.get_ui('QuickMarkUI')
            if ui_inst:
                ui_inst.on_end(touch_wpos)

        @self.panel.btn_normal_camera.callback()
        def OnClick(btn, touch):
            from logic.comsys.share.BattleSceneOnlyUI import BattleSceneOnlyUI
            BattleSceneOnlyUI()

        @self.panel.btn_speak.callback()
        def OnClick(btn, touch):
            self.on_start_speak_to_msg()

        return