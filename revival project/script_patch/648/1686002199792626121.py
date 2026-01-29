# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/QuickMarkBtn.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.comsys.battle.spray.SprayUI import SprayUI
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc
from logic.vscene.parts.ctrl.ShortcutFunctionalityMutex import claim_shortcut_functionality, unclaim_shortcut_functionality, try_claim_shortcut_functionality, try_unclaim_shortcut_functionality
from data import hot_key_def
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
from common.utils.time_utils import get_time
from logic.gutils.hot_key_utils import get_hot_key_extra_arg
import game
from logic.comsys.map.InteractionInvokeBtnWidget import InteractionInvokeBtnWidget
from common.const import uiconst
from logic.gcommon.common_utils import parachute_utils

class QuickMarkBtn(MechaDistortHelper, BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle/fight_locate_btn'
    DLG_ZORDER = BASE_LAYER_ZORDER - 1
    HOT_KEY_FUNC_MAP = {'switch_scene_mark.PRESS': 'keyboard_use_mark_ui',
       'switch_scene_mark.CANCEL': 'keyboard_use_mark_ui_cancel',
       'double_mark_item.DOWN_UP': 'keyboard_mark_item',
       'switch_interaction.CANCEL': 'keyboard_use_spray_ui_cancel',
       'switch_interaction.DOWN_UP': 'keyboard_use_spray_ui',
       'open_fight_chat_dialog': 'on_keyboard_open_chat_dialog'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'switch_scene_mark': {'node': 'layer_locate.temp_pc'},'switch_interaction': {'node': 'nd_action_spray.temp_pc'},'open_fight_chat_dialog': {'node': 'btn_chat.temp_pc'},'switch_interaction': {'node': 'layer_camera.temp_pc'}}

    def on_init_panel(self, *args, **kwargs):
        self._inter_invoke_btn_widget = None
        super(QuickMarkBtn, self).on_init_panel(*args, **kwargs)
        self.interaction_cd_time = 5
        self.interaction_cd_state = False
        self.init_widget()
        self.init_custom_com()
        self._mouse_listener = None
        self._mouse_position = None
        self._mouse_prev_position = None
        self._quick_mark_mouse_position = None
        self._double_mark_item_down_time = None
        self.process_event(True)
        bat = global_data.player.get_battle()
        if bat and bat.is_in_settle_celebrate_stage():
            self.on_celebrate_win()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_player_setted_event': self.on_cam_player_setted,
           'scene_observed_player_setted_event': self.on_enter_observe,
           'on_success_interaction_event': self.on_success_interaction,
           'is_click_in_chat_btn_event': self.is_click_in_chat_btn,
           'celebrate_win_stage_event': self.on_celebrate_win,
           'on_player_parachute_stage_changed': self.on_player_parachute_stage_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def show_img_tips(self, show):
        self.panel.img_tips.setVisible(show)

    def on_cam_player_setted(self, *args):
        self.on_ctrl_target_changed()
        if global_data.cam_lplayer:
            if global_data.cam_lplayer.ev_g_is_avatar():
                self.add_show_count(self.__class__.__name__)
            else:
                self.add_hide_count(self.__class__.__name__)

    def switch_to_mecha--- This code section failed: ---

  93       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'modify_panel_position'
           6  LOAD_CONST            1  'in_mecha'
           9  LOAD_GLOBAL           1  'True'
          12  CALL_FUNCTION_256   256 
          15  POP_TOP          

  94      16  LOAD_GLOBAL           2  'super'
          19  LOAD_GLOBAL           3  'QuickMarkBtn'
          22  LOAD_FAST             0  'self'
          25  CALL_FUNCTION_2       2 
          28  LOAD_ATTR             4  'switch_to_mecha'
          31  CALL_FUNCTION_0       0 
          34  POP_TOP          

  96      35  LOAD_FAST             0  'self'
          38  LOAD_ATTR             5  'refresh_ui_visible'
          41  CALL_FUNCTION_0       0 
          44  POP_TOP          

  97      45  LOAD_GLOBAL           6  'hasattr'
          48  LOAD_GLOBAL           2  'super'
          51  CALL_FUNCTION_2       2 
          54  POP_JUMP_IF_FALSE    82  'to 82'
          57  LOAD_FAST             0  'self'
          60  LOAD_ATTR             7  'custom_ui_com'
        63_0  COME_FROM                '54'
          63  POP_JUMP_IF_FALSE    82  'to 82'

  98      66  LOAD_FAST             0  'self'
          69  LOAD_ATTR             7  'custom_ui_com'
          72  LOAD_ATTR             8  'refresh_all_custom_ui_conf'
          75  CALL_FUNCTION_0       0 
          78  POP_TOP          
          79  JUMP_FORWARD          0  'to 82'
        82_0  COME_FROM                '79'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 51

    def switch_to_non_mecha--- This code section failed: ---

 101       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'modify_panel_position'
           6  LOAD_CONST            1  'in_mecha'
           9  LOAD_GLOBAL           1  'False'
          12  CALL_FUNCTION_256   256 
          15  POP_TOP          

 102      16  LOAD_GLOBAL           2  'super'
          19  LOAD_GLOBAL           3  'QuickMarkBtn'
          22  LOAD_FAST             0  'self'
          25  CALL_FUNCTION_2       2 
          28  LOAD_ATTR             4  'switch_to_non_mecha'
          31  CALL_FUNCTION_0       0 
          34  POP_TOP          

 104      35  LOAD_FAST             0  'self'
          38  LOAD_ATTR             5  'refresh_ui_visible'
          41  CALL_FUNCTION_0       0 
          44  POP_TOP          

 105      45  LOAD_GLOBAL           6  'hasattr'
          48  LOAD_GLOBAL           2  'super'
          51  CALL_FUNCTION_2       2 
          54  POP_JUMP_IF_FALSE    82  'to 82'
          57  LOAD_FAST             0  'self'
          60  LOAD_ATTR             7  'custom_ui_com'
        63_0  COME_FROM                '54'
          63  POP_JUMP_IF_FALSE    82  'to 82'

 106      66  LOAD_FAST             0  'self'
          69  LOAD_ATTR             7  'custom_ui_com'
          72  LOAD_ATTR             8  'refresh_all_custom_ui_conf'
          75  CALL_FUNCTION_0       0 
          78  POP_TOP          
          79  JUMP_FORWARD          0  'to 82'
        82_0  COME_FROM                '79'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 51

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_enter_observe(self, *args):
        self.close()

    def on_success_interaction(self, *args):
        self.interaction_cd_state = True
        self.panel.progress_acton_spray_cd.setVisible(True)
        self.panel.progress_acton_spray_cd.SetPercentage(100)
        self.panel.progress_acton_spray_cd.SetPercentageWithAni(0, self.interaction_cd_time, self.on_cd_count_down_end)
        print('on_success_interaction')

    def on_cd_count_down_end(self):
        self.interaction_cd_state = False
        self.panel.progress_acton_spray_cd.setVisible(False)
        print('count down end')

    @execute_by_mode(True, game_mode_const.Hide_MarkBtn)
    def hide_mark_btn(self):
        self.panel.nd_custom_2.setVisible(False)

    @execute_by_mode(True, game_mode_const.Hide_ChatBtn)
    def hide_btn_chat(self):
        self.panel.btn_chat.setVisible(False)

    def hide_speak_btn(self):
        from logic.gutils.chat_utils import is_support_voice_translate
        mode_type = global_data.game_mode.get_mode_type()
        if mode_type in (game_mode_const.GAME_MODE_EXERCISE, game_mode_const.GAME_MODE_ARMRACE, game_mode_const.GAME_MODE_CONCERT) or not is_support_voice_translate():
            if self.panel.nd_custom_4:
                self.panel.nd_custom_4.setVisible(False)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_EXERCISE,))
    def modify_panel_position(self, in_mecha=False):
        if in_mecha:
            self.panel.nd_custom_1.SetPosition('100%-110', '100%-173')
        else:
            self.panel.nd_custom_1.SetPosition('100%-181', '100%-154')

    def refresh_widget(self):
        from logic.gutils import judge_utils
        mode_type = global_data.game_mode.get_mode_type()
        if mode_type == game_mode_const.GAME_MODE_EXERCISE:
            self.panel.btn_chat.setVisible(False)
        if judge_utils.is_ob():
            self.panel.btn_chat.setVisible(False)

    def init_spray_event(self):
        if global_data.battle and global_data.battle.get_is_round_competition():
            self.panel.nd_action_spray.setVisible(False)
        self.panel.btn_action_spray.BindMethod('OnBegin', self._inter_invoke_btn_widget.on_touch_inter_begin)
        self.panel.btn_action_spray.BindMethod('OnDrag', self._inter_invoke_btn_widget.on_touch_inter_drag)
        self.panel.btn_action_spray.BindMethod('OnEnd', self._inter_invoke_btn_widget.on_touch_inter_end)
        self.panel.btn_action_spray.BindMethod('OnCancel', self._inter_invoke_btn_widget.on_touch_inter_cancel)

    def _on_touch_inter_begin_decorator(self, func):

        def wrapped(*args, **kwargs):
            if self.interaction_cd_state:
                global_data.game_mgr.show_tip(get_text_by_id(608119))
                return False
            return func(*args, **kwargs)

        return wrapped

    def init_widget(self):
        self._inter_invoke_btn_widget = InteractionInvokeBtnWidget(self.panel.btn_action_spray, self.panel, SprayUI, self.__class__.__name__)
        self._inter_invoke_btn_widget.decorate_touch_inter_begin_logic(self._on_touch_inter_begin_decorator)
        self.init_spray_event()
        self.hide_btn_chat()
        self.hide_mark_btn()
        self.hide_speak_btn()
        self.refresh_widget()
        from .QuickMarkUI import QuickMarkUI
        QuickMarkUI()
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

        @self.panel.btn_chat.callback()
        def OnClick(btn, touch):
            global_data.emgr.open_fight_chat_ui_event.emit()

        @self.panel.btn_normal_camera.callback()
        def OnClick(btn, touch):
            from logic.comsys.share.BattleSceneOnlyUI import BattleSceneOnlyUI
            BattleSceneOnlyUI()

        if self.panel.btn_speak:

            @self.panel.btn_speak.callback()
            def OnClick(btn, touch):
                self.on_start_speak_to_msg()

        return

    def do_hide_panel(self):
        super(QuickMarkBtn, self).do_hide_panel()
        if self._inter_invoke_btn_widget:
            self._inter_invoke_btn_widget.on_switch_interactio_key_cancel()

    def on_start_speak_to_msg(self):
        if global_data.ui_mgr.get_ui('FightTalkUI'):
            global_data.ui_mgr.close_ui('FightTalkUI')
            return
        from .FightTalkUI import FightTalkUI
        FightTalkUI()

    def on_change_ui_custom_data(self):
        if self._in_mecha_state:
            UIDistorterHelper().apply_ui_distort(self.__class__.__name__)

    def on_keyboard_open_chat_dialog(self, msg, keycode):
        global_data.emgr.open_fight_chat_ui_event.emit()

    def is_click_in_chat_btn(self, touch):
        return self.panel.btn_chat.IsPointIn(touch.getLocation())

    def on_finalize_panel(self):
        self.process_event(False)
        self.destroy_widget('custom_ui_com')
        global_data.ui_mgr.close_ui('SprayUI')
        self._inter_invoke_btn_widget.destory()
        self._inter_invoke_btn_widget = None
        return

    def keyboard_use_spray_ui(self, msg, keycode):
        if global_data.battle and global_data.battle.get_is_round_competition():
            return False
        bat = global_data.player.get_battle()
        if bat and bat.is_in_settle_celebrate_stage():
            self._inter_invoke_btn_widget.on_switch_interactio_key_cancel()
            from logic.comsys.share.BattleSceneOnlyUI import BattleSceneOnlyUI
            BattleSceneOnlyUI()
        else:
            return self._inter_invoke_btn_widget.on_switch_interactio_key_down_up(msg, keycode)

    def keyboard_use_spray_ui_cancel(self):
        bat = global_data.player.get_battle()
        if not (bat and bat.is_in_settle_celebrate_stage()):
            return self._inter_invoke_btn_widget.on_switch_interactio_key_cancel()

    @execute_by_mode(False, game_mode_const.Hide_MarkBtn)
    def keyboard_use_mark_ui(self, msg, keycode):
        try:
            is_pick_ui_show = global_data.ui_mgr.get_ui('PickUI').is_on_show()
        except:
            is_pick_ui_show = False

        if is_pick_ui_show:
            return
        if msg in [game.MSG_KEY_DOWN, game.MSG_MOUSE_DOWN]:
            from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
            pos = self.panel.CalcPosition('50%', '50%')
            self._quick_mark_mouse_position = cc.Vec2(*pos)
            trigger_ui_btn_event(self.__class__.__name__, 'btn_normal_locate', 'OnBegin', self._quick_mark_mouse_position)
            global_data.mouse_mgr.set_cursor_move_enable(True)
            self.reg_mouse_event()
        else:
            if not self.is_in_mark_func:
                return
            from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
            trigger_ui_btn_event(self.__class__.__name__, 'btn_normal_locate', 'OnEnd', self._quick_mark_mouse_position)
            global_data.mouse_mgr.set_cursor_move_enable(False)
            self.unreg_mouse_event()

    def keyboard_use_mark_ui_cancel(self):
        if not self.is_in_mark_func:
            return
        pos = self.panel.CalcPosition('50%', '50%')
        from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
        trigger_ui_btn_event(self.__class__.__name__, 'btn_normal_locate', 'OnEnd', cc.Vec2(*pos))
        global_data.mouse_mgr.set_cursor_move_enable(False)
        self.unreg_mouse_event()

    @execute_by_mode(False, game_mode_const.Hide_MarkBtn)
    def keyboard_mark_item(self, msg, keycode):
        if msg in [game.MSG_KEY_DOWN, game.MSG_MOUSE_DOWN]:
            self._double_mark_item_down_time = get_time()
        elif self._double_mark_item_down_time is not None and get_time() - self._double_mark_item_down_time < get_hot_key_extra_arg('double_mark_item', 'invoke_max_time', default=0.1):
            ui_inst = global_data.ui_mgr.get_ui('QuickMarkUI')
            from logic.gcommon.common_const.battle_const import MARK_NORMAL, MARK_GOTO, MARK_DANGER, MARK_RES, MARK_NONE, MARK_GATHER, MARK_WAY_QUICK
            if ui_inst:
                ui_inst.set_scene_map_mark(MARK_GOTO)
            self._double_mark_item_down_time = None
        return

    def on_mouse_move(self, event):
        from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
        pos = event.getLocation()
        self._mouse_position = pos
        delta = None
        if self._mouse_prev_position is not None:
            delta = cc.Vec2(pos.x - self._mouse_prev_position.x, pos.y - self._mouse_prev_position.y)
        if delta is None:
            delta = cc.Vec2(0.0, 0.0)
        self._quick_mark_mouse_position = cc.Vec2(self._quick_mark_mouse_position.x + delta.x, self._quick_mark_mouse_position.y + delta.y)
        _pos = cc.Vec2(self._quick_mark_mouse_position.x, self._quick_mark_mouse_position.y)
        trigger_ui_btn_event(self.__class__.__name__, 'btn_normal_locate', 'OnDrag', _pos)
        self._mouse_prev_position = self._mouse_position
        return

    def is_pc_op_mode(self):
        return global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable()

    def reg_mouse_event(self, skip_pc_control_enable_test=False):
        if self._mouse_listener:
            return
        else:
            if not skip_pc_control_enable_test:
                if not self.is_pc_op_mode():
                    return
            self._mouse_listener = cc.EventListenerMouse.create()
            self._mouse_prev_position = None
            self._mouse_listener.setOnMouseMoveCallback(self.on_mouse_move)
            cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(self._mouse_listener, self.panel.get())
            return

    def unreg_mouse_event(self):
        if self._mouse_listener:
            cc.Director.getInstance().getEventDispatcher().removeEventListener(self._mouse_listener)
            self._mouse_listener = None
        return

    def refresh_ui_visible(self):
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.ev_g_in_mecha('Mecha'):
            self.hide()
        else:
            self.show()

    def show(self):
        if global_data.cam_lplayer and not global_data.cam_lplayer.ev_g_in_mecha('Mecha'):
            BasePanel.show(self)

    def on_celebrate_win(self):
        self.panel.nd_custom_camera.setVisible(True)
        self.panel.layer_locate.setVisible(False)
        self.panel.PlayAnimation('camera_tips_show')
        self.panel.SetTimeOut(6.0, lambda : self.panel.PlayAnimation('camera_tips_hide'))

    def on_player_parachute_stage_changed(self, stage):
        self.panel.nd_custom_1.setVisible(stage != parachute_utils.STAGE_PLANE)
        self.panel.nd_custom_2.nd_rot_2.setVisible(stage != parachute_utils.STAGE_PLANE)


class QuickMarkBtnMecha(QuickMarkBtn):
    PANEL_CONFIG_NAME = 'battle/fight_locate_btn_mecha'

    def show(self):
        from logic.client.const.game_mode_const import GAME_MODE_PVES
        if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_in_mecha('Mecha'):
            BasePanel.show(self)
        if global_data.game_mode.get_mode_type() in GAME_MODE_PVES:
            self.panel.nd_custom_2.setVisible(False)
            if self.panel.nd_custom_4:
                self.panel.nd_custom_4.setVisible(False)

    def refresh_ui_visible(self):
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.ev_g_in_mecha('Mecha'):
            self.show()
        else:
            self.hide()