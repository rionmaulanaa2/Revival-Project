# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8023SubUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BETWEEN_BG_AND_BSCALE_PLATE_ZORDER
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
from logic.comsys.battle.AimScopeAdjust.AimScopeAdjustUIWidget import AimScopeAdjustUIWidget
from data import hot_key_def
from common.const import uiconst
from logic.gutils.mecha_utils import get_fire_end_distance
from common.utils.timer import CLOCK
import logic.gcommon.common_utils.bcast_utils as bcast

class Mecha8023SubUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8023_sub'
    DLG_ZORDER = BETWEEN_BG_AND_BSCALE_PLATE_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    HOT_KEY_NEED_SCROLL_SUPPORT = True
    HOT_KEY_FUNC_MAP_SHOW = {hot_key_def.MOUSE_WHEEL_MSG: {'node': 'temp_pc'}}
    UI_ACTION_EVENT = {}
    MECHA_EVENT = {'E_OPEN_AIM_CAMERA': 'on_open_aim_camera',
       'E_FIRE': 'on_fire',
       'E_8023_POWERFUL_SNIPE': 'enable_powerful_shoot',
       'E_8023_POWERFUL_SNIPE_END': 'disable_powerful_shoot',
       'E_8023_OPEN_AIM_FIRE': 'on_fire',
       'E_PLAY_VICTORY_CAMERA': 'on_victory'
       }
    IS_FULLSCREEN = True

    def on_init_panel(self):
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.init_parameters()
        self.init_event()
        self.init_custom_com()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {}, ui_custom_panel_name='MechaAimScopeAdjustUI')

    def on_finalize_panel--- This code section failed: ---

  51       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'unbind_ui_event'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  'player'
          12  CALL_FUNCTION_1       1 
          15  POP_TOP          

  52      16  LOAD_CONST            0  ''
          19  LOAD_FAST             0  'self'
          22  STORE_ATTR            1  'player'

  53      25  LOAD_FAST             0  'self'
          28  LOAD_ATTR             3  'aim_scope_adjust_ui_widget'
          31  LOAD_CONST            0  ''
          34  COMPARE_OP            9  'is-not'
          37  POP_JUMP_IF_FALSE    65  'to 65'

  54      40  LOAD_FAST             0  'self'
          43  LOAD_ATTR             3  'aim_scope_adjust_ui_widget'
          46  LOAD_ATTR             4  'on_finalize_panel'
          49  CALL_FUNCTION_0       0 
          52  POP_TOP          

  55      53  LOAD_CONST            0  ''
          56  LOAD_FAST             0  'self'
          59  STORE_ATTR            3  'aim_scope_adjust_ui_widget'
          62  JUMP_FORWARD          0  'to 65'
        65_0  COME_FROM                '62'

  56      65  LOAD_GLOBAL           5  'hasattr'
          68  LOAD_GLOBAL           1  'player'
          71  CALL_FUNCTION_2       2 
          74  POP_JUMP_IF_FALSE   111  'to 111'
          77  LOAD_FAST             0  'self'
          80  LOAD_ATTR             6  'custom_ui_com'
        83_0  COME_FROM                '74'
          83  POP_JUMP_IF_FALSE   111  'to 111'

  57      86  LOAD_FAST             0  'self'
          89  LOAD_ATTR             6  'custom_ui_com'
          92  LOAD_ATTR             7  'destroy'
          95  CALL_FUNCTION_0       0 
          98  POP_TOP          

  58      99  LOAD_CONST            0  ''
         102  LOAD_FAST             0  'self'
         105  STORE_ATTR            6  'custom_ui_com'
         108  JUMP_FORWARD          0  'to 111'
       111_0  COME_FROM                '108'
         111  LOAD_CONST            0  ''
         114  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 71

    def init_parameters(self):
        self.player = None
        self.mecha = None
        self.is_open = False
        self._showing_core = False
        self.update_dist_timer = None
        emgr = global_data.emgr
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)
        self.aim_scope_adjust_ui_widget = None
        self.panel.nd_adjust.setVisible(False)
        return

    def init_event(self):
        if not self.mecha:
            return

    def on_cam_lplayer_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        if self.player:
            self.bind_ui_event(self.player)
        if global_data.player and self.player:
            if global_data.player.id != player.id:
                self.on_enter_observe(True)
            else:
                self.on_enter_observe(False)
        self.on_camera_switch_to_state(global_data.game_mgr.scene.get_com('PartCamera').get_cur_camera_state_type())

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            for event, func_name in six.iteritems(self.MECHA_EVENT):
                func = getattr(self, func_name, None)
                callable(func) and regist_func(event, func)

            self.init_event()
        return

    def bind_ui_event(self, target):
        if target:
            regist_func = target.regist_event

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            for event, func_name in six.iteritems(self.MECHA_EVENT):
                func = getattr(self, func_name, None)
                unregist_func(event, func)

        self.mecha = None
        return

    def _try_init_aim_scope_adjust_ui_widget(self, aim_scope_id, magnification_triplet):
        if self.aim_scope_adjust_ui_widget is not None:
            return
        else:
            if aim_scope_id and isinstance(magnification_triplet, tuple) and len(magnification_triplet) == 3 and magnification_triplet[1] != magnification_triplet[2]:
                self.aim_scope_adjust_ui_widget = AimScopeAdjustUIWidget()
                self.aim_scope_adjust_ui_widget.on_init_panel(self.panel.nd_adjust, self.panel, aim_scope_id, magnification_triplet[0], magnification_triplet[1], magnification_triplet[2], self.panel.btn_adjust, self.panel.prog_adjust, self.panel.nd_btn_turn, {'prog_adjust_floor': 0,
                   'prog_adjust_ceil': 100,
                   'turn_adjust_floor': -33,
                   'turn_adjust_ceil': 33
                   })
            return

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        if self.aim_scope_adjust_ui_widget:
            self.aim_scope_adjust_ui_widget.on_hot_key_mouse_scroll(delta)

    def check_can_mouse_scroll(self):
        if not self.panel.nd_sniper.isVisible():
            return False
        if not (self.aim_scope_adjust_ui_widget and self.aim_scope_adjust_ui_widget.can_drag):
            return False
        return True

    def on_open_aim_camera(self, is_open):
        if is_open == self.is_open:
            return
        else:
            self.is_open = is_open
            if self.is_open:
                self.panel.nd_core.setVisible(False)
                self.panel.StopAnimation('disappear_sniper')
                self.panel.PlayAnimation('show_sniper')
                if self.mecha.ev_g_powerful_snipe():
                    self.enable_powerful_shoot()
                cam_part = global_data.game_mgr.scene.get_com('PartCamera')
                if cam_part:
                    self._try_init_aim_scope_adjust_ui_widget(cam_part.get_cur_camera_aim_scope_id(), cam_part.get_cur_camera_magnification_triplet())
                self.update_dist_timer = global_data.game_mgr.register_logic_timer(self.update_dist, interval=0.1, times=-1, mode=CLOCK)
            else:
                self.panel.StopAnimation('show_sniper')
                self.panel.PlayAnimation('disappear_sniper')
                self.panel.nd_sniper.StopTimerAction()
                self.disable_powerful_shoot()
                global_data.game_mgr.unregister_logic_timer(self.update_dist_timer)
                self.update_dist_timer = None
            self.panel.nd_sniper.setVisible(is_open)
            if self.aim_scope_adjust_ui_widget is not None:
                self.aim_scope_adjust_ui_widget.setVisible(is_open)
            return

    def on_victory(self, *args):
        self.on_open_aim_camera(False)

    def on_fire(self, *args):
        self.disable_powerful_shoot()
        if not self.is_open:
            return
        self.panel.PlayAnimation('sub_fire')

    def on_enter_observe(self, is_observe):
        pass

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        self.cur_camera_state_type = state
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')

    def enable_powerful_shoot(self, *args):
        self.panel.PlayAnimation('show_core')
        self._showing_core = True

    def disable_powerful_shoot(self):
        self.panel.StopAnimation('show_core')
        if self._showing_core:
            self.panel.PlayAnimation('disappear_core')
            self._showing_core = False

    def update_dist(self):
        if not self.mecha:
            return
        dist = int(get_fire_end_distance(self.mecha))
        self.panel.lab_nun.SetString(str(dist))