# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/FireRockerUI.py
from __future__ import absolute_import
import cc
import math3d
import world
import common.utils.timer as timer
from .ShotChecker import ShotChecker
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
from logic.client.const import camera_const
from logic.gcommon.cdata import status_config
from logic.gcommon.common_const import ui_operation_const
from logic.gcommon.common_const import weapon_const
from logic.gcommon.common_const.ui_operation_const import MOVABLE_FIREROCKER, FIXED_FIREROCKER, ALL_FIX_ROCKER
from logic.gcommon.const import PART_WEAPON_POS_NONE, MAIN_WEAPON_LIST
MAIN_WEAPON_LIST_AND_NONE = (
 PART_WEAPON_POS_NONE,) + MAIN_WEAPON_LIST

class FireRockerUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fire_rocker'
    ACT_CHECK_TAG = 180224
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    CHECK_FORCE_MIN_VALUE = 0.3
    UI_ACTION_EVENT = {'fire_move.OnDrag': 'on_fire_move_drag',
       'fire_move.OnBegin': 'on_fire_move_begin',
       'fire_move.OnEnd': 'on_fire_move_end',
       'fire_move.OnCancel': 'on_fire_move_end',
       'shot_bar.OnBegin': 'shot_bar_on_begin',
       'shot_bar.OnDrag': 'shot_bar_on_drag',
       'shot_bar.OnEnd': 'shot_bar_on_end',
       'shot_bar.OnCancel': 'shot_bar_on_end',
       'shot_button.OnBegin': 'shot_button_on_begin',
       'shot_button.OnEnd': 'shot_button_on_end',
       'shot_button.OnCancel': 'shot_button_on_end'
       }
    GLOBAL_EVENT = {'sst_common_changed_event': 'on_sst_common_changed',
       'player_user_setting_changed_event': 'on_user_setting_changed',
       'restart_avatar_fire_by_ui': 'restart_fire'
       }
    ENABLE_HOT_KEY_SUPPORT = True

    def on_init_panel(self):
        self.panel.setLocalZOrder(ui_operation_const.FIRE_LOCAL_ZORDER)
        self.last_finger_move_vec = None
        self.is_start_auto_fire = False
        self.is_try_shot_success = False
        self.is_player_first_setted = True
        self.is_rocker_enable = False
        self.cur_rocker_ope_sel = None
        self.is_trying_fire = False
        self.sst_setting_map = {}
        self.auto_aim_fire_setting = [ui_operation_const.MANUAL_SNIPER_RIFLE_FAST_AIM_AND_FIRE_KEY, ui_operation_const.SNIPER_RIFLE_FAST_AIM_AND_RELEASE_FIRE_KEY,
         ui_operation_const.AUTO_FAST_AIM_AND_FIRE_KEY]
        ShotChecker()
        self.init_custom_com()
        self.player = None
        self.add_associate_vis_ui('AimRockerUI')
        self.init_other_event()
        self.init_parameters()
        self.init_rocker()
        self.init_visible_event()
        return

    def init_parameters(self):
        self.last_vec = None
        self.is_rocking = False
        self.touch_begin_pos = None
        self.init_weapon_rocker_draggable()
        scn = world.get_active_scene()
        player = scn.get_player()
        self.add_hide_count('FireRockerUI')
        if player:
            self.on_player_setted(player)
        global_data.emgr.scene_player_setted_event += self.on_player_setted
        self.accumulate_timer = None
        return

    def init_rocker(self):
        self.panel.shot_bar.SetNoEventAfterMove(False)
        span_scale = self.panel.shot_bar.getScale()
        rocker_scale = self.panel.nd_rocker_center.getScale()
        max_width = self.panel.shot_bar.ConvertToWorldSpacePercentage(100, 50).x
        mid_width = self.panel.shot_bar.ConvertToWorldSpacePercentage(50, 50).x
        local_radius = 0.9 * (max_width - mid_width)
        self.spawn_radius = local_radius

    def reset_fire_icon(self):
        from logic.gutils.weapon_utils import is_in_fast_aim_and_fire_mode
        if not self.player:
            return
        cur_weapon = self.player.share_data.ref_wp_bar_cur_weapon
        in_fast_aim_and_fire = is_in_fast_aim_and_fire_mode(cur_weapon)
        if in_fast_aim_and_fire:
            self.panel.icon_shot.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/icon/icon_shot_nml_aim.png')
        else:
            self.panel.icon_shot.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/icon/icon_shot_nml.png')

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {ui_operation_const.FIREROCKER_OPE_KEY: 'cur_rocker_ope_sel'})

    def init_rocker_sensitivity(self):
        uoc = ui_operation_const
        self.sst_setting_map = {}
        sst_ket_list = [uoc.SST_FROCKER_KEY, uoc.SST_SCR_KEY, uoc.SST_AIM_RD_KEY, uoc.SST_AIM_2M_KEY,
         uoc.SST_AIM_4M_KEY, uoc.SST_AIM_6M_KEY, uoc.SST_MECHA_07_KEY]
        for key in sst_ket_list:
            self.sst_setting_map[key] = list(self.player.get_owner().get_setting(key))

    def on_player_setted(self, player):
        self.unbind_shot_event(self.player)
        self.player = player
        if player:
            if self.is_player_first_setted:
                self.init_shot_event()
                self.is_player_first_setted = False
                self.add_show_count('FireRockerUI')
            self.init_rocker_sensitivity()
            self.bind_shot_event(self.player)
            self.update_shot_ui_by_player_status()
            self.reset_fire_icon()

    def set_rocker_center_pos(self, move_pos, center_pos, move_node, radius):
        import math3d
        import cc
        move_vec = math3d.vector2(move_pos.x - center_pos.x, move_pos.y - center_pos.y)
        move_vec_length = move_vec.length
        if move_vec_length > radius:
            move_vec = move_vec * (radius / move_vec_length)
        spawn_pt = move_node.getParent().convertToNodeSpace(cc.Vec2(center_pos.x + move_vec.x, center_pos.y + move_vec.y))
        move_node.setPosition(spawn_pt)

    def stop_rocker(self):
        self.panel.stopActionByTag(self.ACT_CHECK_TAG)
        self.is_try_shot_success = False
        self.panel.nd_rocker_center.SetPosition('50%', '50%')
        span_center = self.panel.nd_rocker_center.ConvertToWorldSpacePercentage(50, 50)
        self.panel.nd_rocker_center.getParent().convertToNodeSpace(span_center)
        self.last_vec = None
        self.is_rocker_enable = False
        if self.player:
            self.player.send_event('E_RELEASE_FIRE_ROCK')
        self.last_finger_move_vec = None
        if self.cur_rocker_ope_sel != MOVABLE_FIREROCKER:
            self.panel.shot_bar.setOpacity(0)
        self.panel.shot_button.SetSelect(False)
        return

    def init_other_event(self):
        partcam = global_data.game_mgr.scene.get_com('PartCamera')
        if partcam:
            self.on_camera_switch_to_state(partcam.get_cur_camera_state_type())
        else:
            self.on_camera_switch_to_state(camera_const.THIRD_PERSON_MODEL)
        emgr = global_data.emgr
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)
        global_data.emgr.settle_stage_event += self.battle_end

    def on_rocker_ope_sel_change_event(self, sel):
        if sel == MOVABLE_FIREROCKER:
            self.panel.shot_bar.SetEnableTouch(False)
            self.panel.shot_bar.setVisible(False)
            self.panel.shot_empty_button.SetSwallowTouch(False)
        else:
            self.panel.shot_bar.SetEnableTouch(True)
            self.panel.shot_bar.setOpacity(0)
            self.panel.shot_bar.SetEnableCascadeOpacityRecursion(True)
            self.panel.shot_bar.setVisible(True)
            self.panel.shot_empty_button.SetSwallowTouch(True)
            self._end_auto_fire()
            old_pos = self.panel.nd_shot_empty_button_pos.getPosition()
            self.panel.shot_empty_button.stopAllActions()
            self.panel.shot_empty_button.setPosition(old_pos)
        self.cur_rocker_ope_sel = sel
        self.on_3d_touch_ope_changed_event(global_data.player.get_setting(ui_operation_const.ThreeD_TOUCH_TOGGLE_KEY))
        self.custom_ui_com.refresh_all_custom_ui_conf()

    def init_shot_event(self):
        self.cur_weapon_pos = self.player.share_data.ref_wp_bar_cur_pos
        self.cur_weapon_data = {}
        self.cur_aim_lens = None
        self.cur_rocker_ope_sel = None
        self.on_rocker_ope_sel_change_event(self.player.get_owner().firerocker_ope_setting)
        self.is_3d_touch_trigger_fire = False
        self.on_3d_touch_ope_changed_event(self.player.get_owner().is_open_3d_touch)
        emgr = global_data.emgr
        econf = {'firerocker_ope_change_event': self.on_rocker_ope_sel_change_event,
           'threed_touch_change_event': self.on_3d_touch_ope_changed_event
           }
        emgr.bind_events(econf)
        return

    def shot_bar_on_begin(self, btn, touch):
        if self.cur_rocker_ope_sel in [FIXED_FIREROCKER, ALL_FIX_ROCKER]:
            self.is_trying_fire = True
            self.play_touch_effect(global_data.is_key_mocking_ui_event or 'click' if 1 else None, 'fire_click', self.panel.right_rocker.getPosition(), self.panel.right_rocker.getScale())
            self.panel.shot_bar.setOpacity(255)
            if self.player:
                self.player.send_event('E_IS_KEEP_DOWN_FIRE', True)
            is_suc = self._start_touch_auto_fire()
            if not is_suc:
                self.panel.DelayCallWithTag(0.05, self._cc_check_can_trigger_act, self.ACT_CHECK_TAG)
        return True

    def check_start_shot(self):
        is_suc = self._check_can_trigger_act()
        if not is_suc:
            self.panel.DelayCallWithTag(0.05, self._cc_check_can_trigger_act, self.ACT_CHECK_TAG)

    def _check_can_trigger_act(self):
        if not self.check_can_shot():
            return False
        if not self.is_try_shot_success:
            self.try_start_shot()
            return self.is_try_shot_success
        return True

    def _cc_check_can_trigger_act(self):
        if not self._check_can_trigger_act():
            return 0.05
        return 0

    def shot_button_on_begin(self, btn, touch):
        from logic.gcommon.common_const.ui_operation_const import MOVABLE_FIREROCKER
        if self.cur_rocker_ope_sel == MOVABLE_FIREROCKER:
            self.is_trying_fire = True
            pos_p = self.panel.right_rocker.getPosition()
            pos_c = self.panel.shot_empty_button.getPosition()
            size = self.panel.shot_empty_button.getContentSize()
            pos_c.x -= size.width / 2
            pos_c.y -= size.height / 2
            pos = cc.Vec2(pos_p.x + pos_c.x, pos_p.y + pos_c.y)
            self.play_touch_effect(global_data.is_key_mocking_ui_event or 'click' if 1 else None, 'fire_click', pos, self.panel.right_rocker.getScale())
            self.stop_firerocker_reset_action()
            is_suc = self._start_touch_auto_fire()
            if not is_suc:
                self.panel.DelayCallWithTag(0.05, self._cc_check_can_trigger_act, self.ACT_CHECK_TAG)
        return True

    def shot_button_on_end(self, btn, touch):
        from logic.gcommon.common_const.ui_operation_const import MOVABLE_FIREROCKER
        if self.cur_rocker_ope_sel == MOVABLE_FIREROCKER:
            self.is_trying_fire = False
            self._end_auto_fire()
            self.run_firerock_reset_action()

    def _start_touch_auto_fire(self):
        span_center = self.panel.shot_bar.ConvertToWorldSpacePercentage(50, 50)
        npos = self.panel.nd_rocker_center.getParent().convertToNodeSpace(span_center)
        self.panel.nd_rocker_center.setPosition(npos)
        self.is_rocker_enable = True
        self.panel.nd_rocker_center.setVisible(True)
        is_suc = self._check_can_trigger_act()
        if not is_suc:
            return False
        else:
            return True

    def try_start_shot(self):
        if self.is_try_shot_success:
            return False
        if self.player:
            cur_weapon_pos = self.player.share_data.ref_wp_bar_cur_pos
            if cur_weapon_pos in MAIN_WEAPON_LIST:
                if not self.is_start_auto_fire:
                    if self.player.ev_g_status_check_pass(status_config.ST_SHOOT) and self.player.ev_g_is_can_fire():
                        if global_data.is_allow_sideways:
                            self.player.send_event('E_START_FIRE_ROCKER')
                        else:
                            self.player.send_event('E_START_AUTO_FIRE', right_mode=True)
                        self.is_start_auto_fire = True
                        self.is_try_shot_success = True
                        return True
            elif cur_weapon_pos == PART_WEAPON_POS_NONE:
                if not self.is_start_auto_fire:
                    return False
        return False

    def _on_check_3d_touch_fire_btn(self, btn, touch):
        if not self.player:
            return
        if not self.player.get_owner().is_open_3d_touch:
            return
        cur_weapon_pos = self.player.share_data.ref_wp_bar_cur_pos
        is_trigger = self.check_trigger_rocker_touch_force(touch)
        if is_trigger:
            if not self.check_can_shot():
                return
            if self.is_start_auto_fire or self.is_3d_touch_trigger_fire:
                if self.is_3d_touch_trigger_fire:
                    self.show_3d_touch_ani(True, touch.getLocation())
                return
            if cur_weapon_pos in MAIN_WEAPON_LIST_AND_NONE:
                if cur_weapon_pos == PART_WEAPON_POS_NONE:
                    pass
                elif self.player.ev_g_status_check_pass(status_config.ST_SHOOT) and self.player.ev_g_is_can_fire():
                    self.player.send_event('E_START_AUTO_FIRE', right_mode=True)
                    self.is_start_auto_fire = True
                    self.is_3d_touch_trigger_fire = True
                    self.show_3d_touch_ani(True, touch.getLocation())
        else:
            self.finish_3d_touch()

    def finish_3d_touch(self):
        if not self.player:
            return
        else:
            cur_weapon_pos = self.player.share_data.ref_wp_bar_cur_pos
            if self.is_3d_touch_trigger_fire:
                if cur_weapon_pos in MAIN_WEAPON_LIST_AND_NONE:
                    if cur_weapon_pos == PART_WEAPON_POS_NONE:
                        self.player.send_event('E_ATTACK_END')
                    elif global_data.is_allow_sideways:
                        self.player.send_event('E_END_FIRE_ROCKER')
                    else:
                        self.player.send_event('E_STOP_AUTO_FIRE', right_mode=True)
                self.is_start_auto_fire = False
                self.is_3d_touch_trigger_fire = False
                self.show_3d_touch_ani(False, None)
            return

    def check_trigger_rocker_touch_force(self, touch):
        force = touch.getPressure()
        max_force = touch.getMaxPressure()
        if max_force > self.CHECK_FORCE_MIN_VALUE:
            trigger_percent = self.player.get_owner().trigger_percent_3d_touch
            if force >= max_force * trigger_percent:
                return True

    def shot_bar_on_drag(self, btn, touch):
        if not self.is_rocker_enable:
            return
        else:
            if not self._weapon_rocker_draggable:
                return
            delta_vec = touch.getDelta()
            vec_temp = math3d.vector2(delta_vec.x, delta_vec.y)
            if vec_temp.length > 0:
                if self.last_finger_move_vec is None:
                    vec_temp.normalize()
                self.last_finger_move_vec = vec_temp
            elif self.last_finger_move_vec:
                if not self.last_finger_move_vec.is_zero:
                    vec_temp = self.last_finger_move_vec
                    vec_temp.normalize()
                    self.last_finger_move_vec = math3d.vector2(0, 0)
            else:
                return
            pt = touch.getLocation()
            rocker_center = self.panel.shot_bar.ConvertToWorldSpacePercentage(50, 50)
            self.set_rocker_center_pos(pt, rocker_center, self.panel.nd_rocker_center, self.spawn_radius)
            if self.player:
                scene = world.get_active_scene()
                ctrl = scene.get_com('PartCtrl')
                x_delta = vec_temp.x
                y_delta = vec_temp.y
                ctrl.on_touch_slide(x_delta, y_delta, None, pt, True, kwargs={'center_pos': rocker_center})
            return

    def shot_bar_on_end(self, btn, touch):
        self.is_trying_fire = False
        if self.player:
            self.player.send_event('E_IS_KEEP_DOWN_FIRE', False)
        if not self.is_rocker_enable:
            return
        if self.cur_rocker_ope_sel != MOVABLE_FIREROCKER:
            self.panel.shot_bar.setOpacity(0)
            self._end_auto_fire()
            if self.is_rocker_enable:
                self.stop_rocker()
                return

    def _end_auto_fire(self):
        if not self.player:
            return
        if not self.is_rocker_enable:
            return
        self._on_normal_end_rocker()

    def _on_normal_end_rocker--- This code section failed: ---

 448       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'panel'
           6  LOAD_ATTR             1  'stopActionByTag'
           9  LOAD_FAST             0  'self'
          12  LOAD_ATTR             2  'ACT_CHECK_TAG'
          15  CALL_FUNCTION_1       1 
          18  POP_TOP          

 449      19  LOAD_GLOBAL           3  'False'
          22  LOAD_FAST             0  'self'
          25  STORE_ATTR            4  'is_try_shot_success'

 451      28  LOAD_FAST             0  'self'
          31  LOAD_ATTR             5  'player'
          34  POP_JUMP_IF_TRUE     41  'to 41'

 452      37  LOAD_CONST            0  ''
          40  RETURN_END_IF    
        41_0  COME_FROM                '34'

 453      41  LOAD_CONST            1  ''
          44  LOAD_CONST            2  ('const',)
          47  IMPORT_NAME           6  'logic.gcommon'
          50  IMPORT_FROM           7  'const'
          53  STORE_FAST            1  'const'
          56  POP_TOP          

 454      57  LOAD_FAST             0  'self'
          60  LOAD_ATTR             8  'cur_weapon_pos'
          63  STORE_FAST            2  'cur_weapon_pos'

 455      66  LOAD_GLOBAL           9  'hasattr'
          69  LOAD_GLOBAL           3  'False'
          72  CALL_FUNCTION_2       2 
          75  POP_JUMP_IF_FALSE   380  'to 380'
          78  LOAD_FAST             0  'self'
          81  LOAD_ATTR            10  'is_rocker_enable'
        84_0  COME_FROM                '75'
          84  POP_JUMP_IF_FALSE   380  'to 380'

 456      87  LOAD_FAST             2  'cur_weapon_pos'
          90  LOAD_GLOBAL          11  'MAIN_WEAPON_LIST'
          93  COMPARE_OP            6  'in'
          96  POP_JUMP_IF_FALSE   173  'to 173'

 457      99  LOAD_FAST             0  'self'
         102  LOAD_ATTR            12  'is_start_auto_fire'
         105  POP_JUMP_IF_FALSE   213  'to 213'

 458     108  LOAD_GLOBAL          13  'global_data'
         111  LOAD_ATTR            14  'is_allow_sideways'
         114  POP_JUMP_IF_FALSE   136  'to 136'

 459     117  LOAD_FAST             0  'self'
         120  LOAD_ATTR             5  'player'
         123  LOAD_ATTR            15  'send_event'
         126  LOAD_CONST            4  'E_END_FIRE_ROCKER'
         129  CALL_FUNCTION_1       1 
         132  POP_TOP          
         133  JUMP_FORWARD         22  'to 158'

 461     136  LOAD_FAST             0  'self'
         139  LOAD_ATTR             5  'player'
         142  LOAD_ATTR            15  'send_event'
         145  LOAD_CONST            5  'E_STOP_AUTO_FIRE'
         148  LOAD_CONST            6  'right_mode'
         151  LOAD_GLOBAL          16  'True'
         154  CALL_FUNCTION_257   257 
         157  POP_TOP          
       158_0  COME_FROM                '133'

 462     158  LOAD_GLOBAL           3  'False'
         161  LOAD_FAST             0  'self'
         164  STORE_ATTR           12  'is_start_auto_fire'
         167  JUMP_ABSOLUTE       213  'to 213'
         170  JUMP_FORWARD         40  'to 213'

 463     173  LOAD_FAST             2  'cur_weapon_pos'
         176  LOAD_GLOBAL          17  'PART_WEAPON_POS_NONE'
         179  COMPARE_OP            2  '=='
         182  POP_JUMP_IF_FALSE   213  'to 213'

 464     185  LOAD_FAST             0  'self'
         188  LOAD_ATTR             5  'player'
         191  LOAD_ATTR            15  'send_event'
         194  LOAD_CONST            7  'E_ATTACK_END'
         197  CALL_FUNCTION_1       1 
         200  POP_TOP          

 465     201  LOAD_GLOBAL           3  'False'
         204  LOAD_FAST             0  'self'
         207  STORE_ATTR           12  'is_start_auto_fire'
         210  JUMP_FORWARD          0  'to 213'
       213_0  COME_FROM                '210'
       213_1  COME_FROM                '170'

 466     213  LOAD_FAST             0  'self'
         216  LOAD_ATTR            18  'is_3d_touch_trigger_fire'
         219  POP_JUMP_IF_FALSE   358  'to 358'

 467     222  LOAD_FAST             0  'self'
         225  LOAD_ATTR            12  'is_start_auto_fire'
         228  POP_JUMP_IF_FALSE   330  'to 330'

 468     231  LOAD_FAST             2  'cur_weapon_pos'
         234  LOAD_GLOBAL          11  'MAIN_WEAPON_LIST'
         237  COMPARE_OP            6  'in'
         240  POP_JUMP_IF_FALSE   296  'to 296'

 469     243  LOAD_GLOBAL          13  'global_data'
         246  LOAD_ATTR            14  'is_allow_sideways'
         249  POP_JUMP_IF_FALSE   271  'to 271'

 470     252  LOAD_FAST             0  'self'
         255  LOAD_ATTR             5  'player'
         258  LOAD_ATTR            15  'send_event'
         261  LOAD_CONST            4  'E_END_FIRE_ROCKER'
         264  CALL_FUNCTION_1       1 
         267  POP_TOP          
         268  JUMP_ABSOLUTE       327  'to 327'

 472     271  LOAD_FAST             0  'self'
         274  LOAD_ATTR             5  'player'
         277  LOAD_ATTR            15  'send_event'
         280  LOAD_CONST            5  'E_STOP_AUTO_FIRE'
         283  LOAD_CONST            6  'right_mode'
         286  LOAD_GLOBAL          16  'True'
         289  CALL_FUNCTION_257   257 
         292  POP_TOP          
         293  JUMP_ABSOLUTE       330  'to 330'

 473     296  LOAD_FAST             2  'cur_weapon_pos'
         299  LOAD_GLOBAL          17  'PART_WEAPON_POS_NONE'
         302  COMPARE_OP            2  '=='
         305  POP_JUMP_IF_FALSE   330  'to 330'

 474     308  LOAD_FAST             0  'self'
         311  LOAD_ATTR             5  'player'
         314  LOAD_ATTR            15  'send_event'
         317  LOAD_CONST            7  'E_ATTACK_END'
         320  CALL_FUNCTION_1       1 
         323  POP_TOP          
         324  JUMP_ABSOLUTE       330  'to 330'
         327  JUMP_FORWARD          0  'to 330'
       330_0  COME_FROM                '327'

 475     330  LOAD_GLOBAL           3  'False'
         333  LOAD_FAST             0  'self'
         336  STORE_ATTR           18  'is_3d_touch_trigger_fire'

 476     339  LOAD_FAST             0  'self'
         342  LOAD_ATTR            19  'show_3d_touch_ani'
         345  LOAD_GLOBAL           3  'False'
         348  LOAD_CONST            0  ''
         351  CALL_FUNCTION_2       2 
         354  POP_TOP          
         355  JUMP_FORWARD          0  'to 358'
       358_0  COME_FROM                '355'

 477     358  LOAD_GLOBAL           3  'False'
         361  LOAD_FAST             0  'self'
         364  STORE_ATTR           12  'is_start_auto_fire'

 478     367  LOAD_FAST             0  'self'
         370  LOAD_ATTR            21  'stop_rocker'
         373  CALL_FUNCTION_0       0 
         376  POP_TOP          
         377  JUMP_FORWARD          0  'to 380'
       380_0  COME_FROM                '377'
         380  LOAD_CONST            0  ''
         383  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 72

    def on_fire_move_drag(self, layer, touch):
        from logic.gcommon.common_const.ui_operation_const import MOVABLE_FIREROCKER
        if self.cur_rocker_ope_sel == MOVABLE_FIREROCKER:
            wpos = touch.getLocation()
            lpos = self.panel.shot_empty_button.getParent().convertToNodeSpace(wpos)
            sz = self.panel.shot_empty_button.getContentSize()
            anchor = self.panel.shot_empty_button.getAnchorPoint()
            valid_pos = True
            btn = self._get_visible_aim_button()
            if btn:
                if btn.IsPointIn(wpos):
                    valid_pos = False
            if valid_pos:
                self.panel.shot_empty_button.SetPosition(lpos.x - (0.5 - anchor.x) * sz.width, lpos.y - (0.5 - anchor.y) * sz.height)
            self.stop_firerocker_reset_action()
            self._on_check_3d_touch_fire_btn(layer, touch)

    def on_fire_move_begin(self, layer, touch):
        if self.cur_rocker_ope_sel == MOVABLE_FIREROCKER:
            self._on_check_3d_touch_fire_btn(layer, touch)
        return True

    def on_fire_move_end(self, layer, touch):
        if self.cur_rocker_ope_sel == MOVABLE_FIREROCKER:
            self.run_firerock_reset_action()
            self.finish_3d_touch()

    def run_firerock_reset_action(self):
        import cc
        old_pos = self.panel.nd_shot_empty_button_pos.getPosition()
        self.panel.shot_empty_button.stopAllActions()
        delay_act = cc.DelayTime.create(0.8)
        move_act = cc.MoveTo.create(0.1, old_pos)
        self.panel.shot_empty_button.runAction(cc.Sequence.create([
         delay_act, move_act]))

    def stop_firerocker_reset_action(self):
        self.panel.shot_empty_button.stopAllActions()

    def on_weapon_in_hand_changed(self, weapon):
        if not self.player:
            return
        from logic.gcommon import const
        cur_weapon_pos = self.player.share_data.ref_wp_bar_cur_pos
        self.cur_weapon_pos = cur_weapon_pos
        if self.cur_weapon_pos == const.PART_WEAPON_POS_NONE:
            self.panel.shot_button.setVisible(False)
        elif self.cur_weapon_pos != const.PART_WEAPON_POS_BOMB:
            self.panel.shot_button.setVisible(True)
        self.reset_fire_icon()

    def on_leave_state(self, leave_state, new_st=None):
        if isinstance(leave_state, set) and status_config.ST_WEAPON_ACCUMULATE in leave_state or isinstance(leave_state, int) and status_config.ST_WEAPON_ACCUMULATE == leave_state:
            self.hide_accumulate_ui()

    def on_weapon_data_changed(self, pos):
        pass

    def on_weapon_data_switched(self, *args):
        self.cur_weapon_pos = self.player.share_data.ref_wp_bar_cur_pos

    def on_finalize_panel(self):
        self.on_player_setted(None)
        if self.custom_ui_com:
            self.custom_ui_com.destroy()
            self.custom_ui_com = None
        return

    def on_camera_switch_to_state(self, state, *args):
        self.cur_camera_state_type = state
        if state == camera_const.AIM_MODE:
            if self.player:
                from logic.gcommon.const import ATTACHEMNT_AIM_POS
                len_attr_data = self.player.ev_g_attachment_attr(ATTACHEMNT_AIM_POS)
                if len_attr_data:
                    self.cur_aim_lens = len_attr_data.get('iType')

    def check_can_shot(self):
        from logic.comsys.battle.BattleUtils import can_fire
        if not can_fire():
            return False
        return not self.check_camera_can_shot()

    def check_camera_can_shot(self):
        return ShotChecker().check_camera_can_shot()

    def on_change_firerock_sensitivity(self, setting_list):
        self.sst_frocker_setting = list(setting_list)

    def on_change_aim_rd_sensitivity(self, setting_list):
        self.sst_aim_rd_setting = list(setting_list)

    def on_change_aim_2m_sensitivity(self, setting_list):
        self.sst_aim_2m_setting = list(setting_list)

    def on_change_aim_4m_sensitivity(self, setting_list):
        self.sst_aim_4m_setting = list(setting_list)

    def on_change_aim_6m_sensitivity(self, setting_list):
        self.sst_aim_6m_setting = list(setting_list)

    def on_change_mecha_07_sensitivity(self, setting_list):
        self.sst_mecha_07_setting = list(setting_list)

    def bind_shot_event(self, target):
        target.regist_event('E_WPBAR_SWITCH_CUR', self.on_weapon_in_hand_changed)
        target.regist_event('E_WEAPON_DATA_SWITCHED', self.on_weapon_data_switched, 10)
        target.regist_event('E_LEAVE_STATE', self.on_leave_state)
        target.regist_event('E_CTRL_ACCUMULATE', self.on_accumulate)

    def unbind_shot_event(self, target):
        if target and target.is_valid():
            target.unregist_event('E_WPBAR_SWITCH_CUR', self.on_weapon_in_hand_changed)
            target.unregist_event('E_WEAPON_DATA_SWITCHED', self.on_weapon_data_switched)
            target.unregist_event('E_LEAVE_STATE', self.on_leave_state)
            target.unregist_event('E_CTRL_ACCUMULATE', self.on_accumulate)

    def update_shot_ui_by_player_status(self):
        if self.player:
            self.on_weapon_in_hand_changed(self.player.share_data.ref_wp_bar_cur_pos)

    def modify_aim_rotate_dist_by_sensitivity(self, x_delta, y_delta, pos, rocker_center):
        if self.cur_aim_lens is None:
            log_error('There is not lens when get aim rocker move!')
            return (
             x_delta, y_delta)
        else:
            aim_type_dict = weapon_const.aim_type_dict
            if self.cur_aim_lens not in aim_type_dict:
                log_error('Unsupport lens!')
            setting_key = aim_type_dict.get(self.cur_aim_lens, ui_operation_const.SST_AIM_RD_KEY)
            settings = self.sst_setting_map[setting_key]
            x_scale = settings[ui_operation_const.SST_IDX_RIGHT] if pos.x >= rocker_center.x else settings[ui_operation_const.SST_IDX_LEFT]
            x_delta *= settings[ui_operation_const.SST_IDX_BASE] * x_scale
            y_scale = settings[ui_operation_const.SST_IDX_UP] if pos.y >= rocker_center.y else settings[ui_operation_const.SST_IDX_DOWN]
            y_delta *= settings[ui_operation_const.SST_IDX_BASE] * y_scale
            return (
             x_delta, y_delta)

    def init_visible_event(self):
        if global_data.ui_mgr.get_ui('BigMapUI'):
            self.add_hide_count('BigMapUI')
        if not (global_data.player and global_data.player.logic):
            return
        if global_data.player.logic.ev_g_is_in_any_state((status_config.ST_SWIM,)):
            self.add_hide_count('swim')

    def on_3d_touch_ope_changed_event(self, is_toggle):
        from common.platform.device_info import DeviceInfo
        device_info = DeviceInfo.get_instance()
        is_can_open = device_info.is_open_3d_touch()
        self.panel.right_rocker.setVisible(True)
        if self.cur_rocker_ope_sel == MOVABLE_FIREROCKER:
            if is_toggle and is_can_open:
                self.panel.right_rocker.setVisible(False)

    def show_3d_touch_ani(self, is_show, wpos):
        if is_show:
            lpos = self.panel.nd_3d_touch.getParent().convertToNodeSpace(wpos)
            self.panel.nd_3d_touch.setPosition(lpos)
            if not self.panel.nd_3d_touch.isVisible():
                self.panel.nd_3d_touch.setVisible(True)
                self.panel.PlayAnimation('3d_touch')
        else:
            self.panel.nd_3d_touch.setVisible(False)
            self.panel.StopAnimation('3d_touch')

    def do_hide_panel(self):
        super(FireRockerUI, self).do_hide_panel()
        self._on_normal_end_rocker()

    def do_show_panel(self):
        super(FireRockerUI, self).do_show_panel()

    def battle_end(self, *args):
        self._on_normal_end_rocker()
        self.finish_3d_touch()

    def on_accumulate(self, flag):
        if flag:
            self.show_accumulate_ui()
        else:
            self.hide_accumulate_ui()

    def show_accumulate_ui(self):
        cur_weapon = self.player.share_data.ref_wp_bar_cur_weapon
        if cur_weapon and cur_weapon.is_accumulate_gun():
            if self.accumulate_timer:
                global_data.game_mgr.unregister_logic_timer(self.accumulate_timer)
            if cur_weapon.get_accumulate_max_time() > 0.0:
                self.accumulate_timer = global_data.game_mgr.register_logic_timer(self.on_end_weapon, interval=cur_weapon.get_accumulate_max_time(), times=1, mode=timer.CLOCK)
            if not global_data.cam_lplayer.sd.ref_in_aim:
                if global_data.ui_mgr.get_ui('MechaAccumulateUI'):
                    global_data.ui_mgr.close_ui('MechaAccumulateUI')
                ui = global_data.ui_mgr.show_ui('MechaAccumulateUI', 'logic.comsys.mecha_ui')
                ui.set_weapon_id(cur_weapon.iType)

    def hide_accumulate_ui(self):
        ui = global_data.ui_mgr.get_ui('MechaAccumulateUI')
        if ui:
            ui.delay_close()
        if self.accumulate_timer:
            global_data.game_mgr.unregister_logic_timer(self.accumulate_timer)
        self.accumulate_timer = None
        return

    def on_end_weapon(self):
        self.hide_accumulate_ui()
        self.player.send_event('E_STOP_AUTO_FIRE', right_mode=True)

    def change_ui_data(self):
        nd = getattr(self.panel, 'shot_empty_button')
        scale = nd.getScale()
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        return (
         w_pos, None, 'nd_step_3')

    def on_sst_common_changed(self, sst_type, settings):
        self.sst_setting_map[sst_type] = settings

    def on_user_setting_changed(self, key, val):
        if key in self.auto_aim_fire_setting:
            self.reset_fire_icon()

    def on_hot_key_opened_state(self):
        super(FireRockerUI, self).on_hot_key_opened_state()
        self.remove_associate_vis_ui('AimRockerUI')

    def on_hot_key_closed_state(self):
        super(FireRockerUI, self).on_hot_key_closed_state()
        self.add_associate_vis_ui('AimRockerUI')

    def init_weapon_rocker_draggable(self):
        disable_drag = False
        self.set_weapon_rocker_draggable(not disable_drag)

    def set_weapon_rocker_draggable(self, val):
        if global_data.is_pc_mode:
            val = False
        self._weapon_rocker_draggable = val

    def on_weapon_rocker_draggable_change(self, val):
        self.set_weapon_rocker_draggable(not val)

    def _get_visible_aim_button(self):
        ui = global_data.ui_mgr.get_ui('AimRockerUI')
        if ui:
            btn = ui.get_aim_button()
            if not btn.isVisible():
                return None
            else:
                return btn

        else:
            return None
        return None

    def restart_fire(self):
        if self.is_trying_fire:
            self.shot_bar_on_end(None, None)
            self.shot_button_on_end(None, None)
            self.shot_bar_on_begin(None, None)
            self.shot_button_on_begin(None, None)
        return