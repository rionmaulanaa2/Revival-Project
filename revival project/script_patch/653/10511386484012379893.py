# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/SingleShotUI.py
from __future__ import absolute_import
import world
import math3d
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER, BASE_LAYER_ZORDER
from logic.gcommon.common_const import ui_operation_const as uoc
from .ShotChecker import ShotChecker
import time
from common.const import uiconst

class SingleShotUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/one_shot_ui'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    ONE_SHOT_BTN_TAG = 1005
    UI_ACTION_EVENT = {'one_shot_button.OnBegin': 'on_one_shot_btn_begin',
       'one_shot_button.OnClick': 'on_one_shot_btn_click',
       'one_shot_button.OnEnd': 'on_one_shot_btn_end',
       'one_shot_button.OnDrag': 'on_one_shot_btn_drag',
       'fire_layer.OnDrag': 'on_fire_layer_drag',
       'fire_layer.OnEnd': 'on_fire_layer_end'
       }

    def on_init_panel(self):
        self.one_shot_base_panel = global_data.ui_mgr.create_simple_dialog('battle/one_shot_generate', BASE_LAYER_ZORDER)
        self.add_hide_count('OneShotUI')
        self.process_events(True)
        self.init_shot_event()

    def on_finalize_panel--- This code section failed: ---

  41       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'process_events'
           6  LOAD_GLOBAL           1  'False'
           9  CALL_FUNCTION_1       1 
          12  POP_TOP          

  42      13  LOAD_GLOBAL           2  'hasattr'
          16  LOAD_GLOBAL           1  'False'
          19  CALL_FUNCTION_2       2 
          22  POP_JUMP_IF_FALSE    65  'to 65'
          25  LOAD_FAST             0  'self'
          28  LOAD_ATTR             3  'one_shot_base_panel'
          31  POP_JUMP_IF_FALSE    65  'to 65'
          34  LOAD_FAST             0  'self'
          37  LOAD_ATTR             3  'one_shot_base_panel'
          40  LOAD_ATTR             4  'is_valid'
          43  CALL_FUNCTION_0       0 
        46_0  COME_FROM                '31'
        46_1  COME_FROM                '22'
          46  POP_JUMP_IF_FALSE    65  'to 65'

  43      49  LOAD_FAST             0  'self'
          52  LOAD_ATTR             3  'one_shot_base_panel'
          55  LOAD_ATTR             5  'close'
          58  CALL_FUNCTION_0       0 
          61  POP_TOP          
          62  JUMP_FORWARD          0  'to 65'
        65_0  COME_FROM                '62'

  44      65  LOAD_CONST            0  ''
          68  LOAD_FAST             0  'self'
          71  STORE_ATTR            3  'one_shot_base_panel'
          74  LOAD_CONST            0  ''
          77  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 19

    def process_events(self, is_bind=True):
        emgr = global_data.emgr
        econf = {'set_one_shot_state_event': self.set_one_shot_func_state,
           'one_shot_change_attack_time_event': self.on_change_one_shot_btn_attack_time,
           'one_shot_change_appear_time_event': self.on_change_on_shot_btn_appear_time,
           'firerocker_ope_change_event': self.on_rocker_ope_sel_change_event
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_shot_event(self):
        player = global_data.player
        self.one_shot_open_state = player.read_local_setting(uoc.ONE_SHOT_SETTING_KEY, uoc.ONE_SHOT_DEF_VAL)
        self.one_shot_touch_begin_time = None
        t = player.read_local_setting(uoc.ONE_SHOT_ATTACK_KEY, uoc.ONE_SHOT_BTN_ATTACK_INTERVAL)
        self.one_shot_btn_attack_time = float(t)
        t = player.read_local_setting(uoc.ONE_SHOT_SHOW_KEY, uoc.ONE_SHOT_BTN_SHOW_TIME)
        self.one_shot_touch_btn_appear_time = float(t)
        self.cur_rocker_ope_sel = None
        self.on_rocker_ope_sel_change_event(player.firerocker_ope_setting)

        @self.one_shot_base_panel.fire_layer.callback()
        def OnEnd(layer, touch):
            self.on_on_shot_generate_check(layer, touch)

        @self.one_shot_base_panel.fire_layer_2.callback()
        def OnEnd(layer, touch):
            self.on_on_shot_generate_check(layer, touch)

        return

    def on_one_shot_btn_begin(self, btn, touch):
        if ShotChecker().check_camera_can_shot():
            return False
        self.one_shot_touch_begin_time = time.time()
        return True

    def on_one_shot_btn_click(self, btn, touch):
        if time.time() - self.one_shot_touch_begin_time < self.one_shot_btn_attack_time:
            if not global_data.cam_lplayer:
                return
            if global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos > 0:
                global_data.cam_lplayer.send_event('E_TRY_FIRE')
            else:
                from logic.gcommon.common_utils.local_text import get_text_by_id
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(18001))

    def on_one_shot_btn_end(self, btn, touch):
        self.panel.one_shot_button.stopActionByTag(SingleShotUI.ONE_SHOT_BTN_TAG)
        self.one_shot_btn_timing_action()

    def on_one_shot_btn_drag(self, btn, touch):
        if self.one_shot_open_state:
            self.panel.one_shot_button.stopActionByTag(SingleShotUI.ONE_SHOT_BTN_TAG)
            wpos = touch.getLocation()
            lpos = self.panel.one_shot_button.getParent().convertToNodeSpace(wpos)
            self.panel.one_shot_button.setPosition(lpos)

    def on_fire_layer_drag(self, layer, touch):
        if self.one_shot_open_state and self.panel.one_shot_button.IsVisible():
            wpos = touch.getLocation()
            lpos = self.panel.one_shot_button.getParent().convertToNodeSpace(wpos)
            self.panel.one_shot_button.stopActionByTag(SingleShotUI.ONE_SHOT_BTN_TAG)
            if self.one_shot_base_panel.fire_layer.IsPointIn(wpos) or self.one_shot_base_panel.fire_layer_2.IsPointIn(wpos):
                self.panel.one_shot_button.setPosition(lpos)

    def on_fire_layer_end(self, layer, touch):
        if self.one_shot_open_state:
            self.panel.one_shot_button.stopActionByTag(SingleShotUI.ONE_SHOT_BTN_TAG)
            self.one_shot_btn_timing_action()

    def one_shot_btn_timing_action(self):
        from cocosui import cc

        def _cc_hide_one_shot_ui():
            self.add_hide_count('OneShotUI')

        action = cc.Sequence.create([
         cc.DelayTime.create(self.one_shot_touch_btn_appear_time),
         cc.CallFunc.create(_cc_hide_one_shot_ui)])
        self.panel.stopActionByTag(SingleShotUI.ONE_SHOT_BTN_TAG)
        ac = self.panel.one_shot_button.runAction(action)
        ac.setTag(SingleShotUI.ONE_SHOT_BTN_TAG)

    def set_one_shot_func_state(self, is_open):
        self.one_shot_open_state = is_open

    def on_change_on_shot_btn_appear_time(self, appear_time):
        self.one_shot_touch_btn_appear_time = appear_time

    def on_change_one_shot_btn_attack_time(self, attack_time):
        self.one_shot_btn_attack_time = attack_time

    def on_on_shot_generate_check(self, layer, touch):
        from logic.gcommon.const import MAIN_WEAPON_LIST
        if not global_data.cam_lplayer:
            return
        firerocker_ui = global_data.ui_mgr.get_ui('FireRockerUI')
        if not firerocker_ui.isVisible():
            return
        if self.cur_rocker_ope_sel != uoc.MOVABLE_FIREROCKER:
            if self.one_shot_open_state:
                cur_weapon_pos = global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos
                if cur_weapon_pos in MAIN_WEAPON_LIST:
                    wpos = touch.getLocation()
                    if self.one_shot_base_panel.fire_layer.IsPointIn(wpos) or self.one_shot_base_panel.fire_layer_2.IsPointIn(wpos):
                        lpos = self.panel.one_shot_button.getParent().convertToNodeSpace(wpos)
                        if not self.panel.isVisible():
                            self.add_show_count('OneShotUI')
                        self.panel.one_shot_button.setVisible(True)
                        self.panel.one_shot_button.setPosition(lpos)
                        self.panel.one_shot_button.stopActionByTag(SingleShotUI.ONE_SHOT_BTN_TAG)
                        self.one_shot_btn_timing_action()

    def on_rocker_ope_sel_change_event(self, sel):
        self.cur_rocker_ope_sel = sel