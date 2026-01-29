# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/PostureControlUI.py
from __future__ import absolute_import
from six.moves import range
import world
import math3d
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.client.const.camera_const import POSTURE_STAND, POSTURE_SQUAT, POSTURE_GROUND, POSTURE_JUMP
from logic.gcommon.cdata import status_config
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.common_const.ui_operation_const import LEFT_CONTROL_ZORDER
from logic.gcommon.common_const.ui_operation_const import OPE_POSTURE_SEPARATE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.rocker_widget_utils import RockerWidget
from logic.gutils import rocker_utils
import logic.gcommon.const as g_const
from logic.gcommon.common_const import collision_const
import collision
import math
from logic.gcommon.common_const.skill_const import SKILL_ROLL, SKILL_AIR_JUMP
from logic.client.const import pc_const
from logic.gutils import pc_utils
from common.const import uiconst
from logic.gutils.character_ctrl_utils import check_climb, try_jump
import logic.gutils.character_ctrl_utils as character_ctrl_utils
from logic.gutils.guide_utils import get_change_ui_data_for_guide_ui
STAMINA_MAP = {2: 'battle/i_fight_roll_3',
   3: 'battle/i_fight_roll_1',
   4: 'battle/i_fight_roll_2'
   }

class PostureControlUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_posture'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_jump.OnBegin': 'on_begin_jump_btn',
       'btn_jump.OnEnd': 'on_end_jump_btn',
       'btn_squat.OnBegin': 'on_begin_squat_btn',
       'btn_squat.OnEnd': 'on_end_squat_btn',
       'btn_roll.OnBegin': 'on_roll_begin'
       }
    ENABLE_HOT_KEY_SUPPORT = True
    UI_CLICK_SALOG_DIC = {'btn_roll.OnEnd': '3'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'human_roll': {'node': 'btn_roll.temp_pc'},'human_squat': {'node': 'btn_squat.temp_pc'},'human_jump': {'node': 'btn_jump.temp_pc'}}
    GLOBAL_EVENT = {'pc_hotkey_hint_display_option_changed': '_on_pc_hotkey_hint_display_option_changed',
       'pc_hotkey_hint_switch_toggled': '_on_pc_hotkey_hint_switch_toggled'
       }

    def init(self, parent=None, *arg, **kwargs):
        if global_data.player.in_local_battle():
            self.on_begin_jump_btn = self._on_begin_jump_btn
            self.on_begin_squat_btn = self._on_begin_squat_btn
            self.on_roll_begin = self._on_roll_begin
        else:
            self.on_begin_jump_btn = self.on_begin_jump_btn_exc
            self.on_begin_squat_btn = self.on_begin_squat_btn_exc
            self.on_roll_begin = self.on_roll_begin_exc
        super(PostureControlUI, self).init(parent=parent, *arg, **kwargs)

    def on_init_panel(self):
        self.btn_dragged = False
        self.btn_dragged_dir = None
        self.roll_rocker_center_wpos = self.panel.nd_real_roll.light_roll.ConvertToWorldSpacePercentage(50, 50)
        self.roll_rocker_widget = None
        self.panel.setLocalZOrder(LEFT_CONTROL_ZORDER)
        self.init_separate_posture_buttons()
        self.init_parameters()
        self.init_ui()
        self.init_event()
        self.check_visible()
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())
        return

    def on_hot_key_state_opened(self):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def on_hot_key_state_closed(self):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_display_option_changed(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), now, pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_switch_toggled(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(now, pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    PC_KEY_HINT_RELEATED_UI_NAMES = ('btn_jump', 'nd_squat')

    def _update_pc_key_hint_related_uis_visibility(self, hint_switch, display_option, pc_op_mode):
        if not self.PC_KEY_HINT_RELEATED_UI_NAMES:
            return
        show = pc_utils.should_pc_key_hint_related_uis_show(pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_ICON, hint_switch, display_option, pc_op_mode)
        for ui_name in self.PC_KEY_HINT_RELEATED_UI_NAMES:
            if not hasattr(self.panel, ui_name):
                continue
            ui = getattr(self.panel, ui_name)
            if not ui or not ui.isValid():
                continue
            ui.setVisible(show)

    def init_rocker--- This code section failed: ---

 125       0  LOAD_GLOBAL           0  'RockerWidget'
           3  LOAD_FAST             0  'self'
           6  LOAD_ATTR             1  'panel'
           9  LOAD_ATTR             2  'nd_real_roll'
          12  LOAD_ATTR             3  'light_roll'

 126      15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             1  'panel'
          21  LOAD_ATTR             4  'btn_roll'

 127      24  LOAD_FAST             0  'self'
          27  LOAD_ATTR             1  'panel'
          30  LOAD_ATTR             4  'btn_roll'
          33  CALL_FUNCTION_3       3 
          36  LOAD_FAST             0  'self'
          39  STORE_ATTR            5  'roll_rocker_widget'

 129      42  LOAD_GLOBAL           6  'getattr'
          45  LOAD_GLOBAL           1  'panel'
          48  LOAD_GLOBAL           7  'False'
          51  CALL_FUNCTION_3       3 
          54  POP_JUMP_IF_FALSE    66  'to 66'
          57  LOAD_FAST             0  'self'
          60  LOAD_ATTR             8  'is_rocker_dash'
          63  JUMP_FORWARD         18  'to 84'
          66  LOAD_GLOBAL           9  'global_data'
          69  LOAD_ATTR            10  'player'
          72  LOAD_ATTR            11  'get_setting'
          75  LOAD_GLOBAL          12  'uoc'
          78  LOAD_ATTR            13  'ROCKER_DASH'
          81  CALL_FUNCTION_1       1 
        84_0  COME_FROM                '63'
          84  LOAD_FAST             0  'self'
          87  LOAD_ATTR             5  'roll_rocker_widget'
          90  STORE_ATTR           14  'enable_drag'

 130      93  LOAD_FAST             0  'self'
          96  LOAD_ATTR             5  'roll_rocker_widget'
          99  LOAD_ATTR            15  'set_begin_callback'
         102  LOAD_FAST             0  'self'
         105  LOAD_ATTR            16  'on_roll_begin'
         108  CALL_FUNCTION_1       1 
         111  POP_TOP          

 131     112  LOAD_FAST             0  'self'
         115  LOAD_ATTR             5  'roll_rocker_widget'
         118  LOAD_ATTR            17  'set_drag_callback'
         121  LOAD_FAST             0  'self'
         124  LOAD_ATTR            18  'on_roll_drag'
         127  CALL_FUNCTION_1       1 
         130  POP_TOP          

 132     131  LOAD_FAST             0  'self'
         134  LOAD_ATTR             5  'roll_rocker_widget'
         137  LOAD_ATTR            19  'set_end_callback'
         140  LOAD_FAST             0  'self'
         143  LOAD_ATTR            20  'on_roll_end'
         146  CALL_FUNCTION_1       1 
         149  POP_TOP          

 133     150  LOAD_GLOBAL           7  'False'
         153  LOAD_FAST             0  'self'
         156  STORE_ATTR           21  'btn_dragged'

 134     159  LOAD_CONST            0  ''
         162  LOAD_FAST             0  'self'
         165  STORE_ATTR           23  'btn_dragged_dir'
         168  LOAD_CONST            0  ''
         171  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 51

    def on_roll_begin_exc(self, btn, touch):
        self.play_touch_effect(global_data.is_key_mocking_ui_event or 'roll_click' if 1 else None, 'click', self.panel.nd_roll.getPosition(), self.panel.nd_roll.getScale())
        if not self.is_rocker_dash:
            self.on_roll_clicked()
        return True

    def _on_roll_begin(self, btn, touch):
        if global_data.is_pc_mode:
            guide_id = global_data.player.get_lbs_step()
            if guide_id is None:
                return True
        return self.on_roll_begin_exc(btn, touch)

    def on_roll_drag(self, btn, touch):
        self.btn_dragged = True

    def on_roll_end(self, btn, touch):
        if self.is_rocker_dash:
            if not self.btn_dragged and self.player:
                self.btn_dragged_dir = self.player.sd.ref_rocker_dir
                if self.btn_dragged_dir is not None and self.btn_dragged_dir.length <= 0:
                    self.btn_dragged_dir = math3d.vector(0, 0, 1)
            else:
                x = touch.getLocation().x - self.roll_rocker_center_wpos.x
                z = touch.getLocation().y - self.roll_rocker_center_wpos.y
                self.btn_dragged_dir = math3d.vector(x, 0, z)
                self.btn_dragged_dir.normalize()
            self.btn_dragged = False
            self.on_roll_clicked()
        return

    def get_roll_dir(self):
        r_dir = None
        if self.btn_dragged_dir:
            r_dir = math3d.vector(self.btn_dragged_dir)
            self.btn_dragged_dir = None
        return r_dir

    def on_roll_clicked(self, *args):
        if not global_data.player:
            return
        player = global_data.player.logic
        if not player:
            return
        from logic.gutils.move_utils import can_roll
        if not can_roll():
            return
        if not player.ev_g_can_cast_skill(SKILL_ROLL):
            return
        if not player.ev_g_is_equip_rush_bone():
            player.send_event('E_CLICK_ROLL')
            if not player.ev_g_status_check_pass(status_config.ST_ROLL):
                return
            player.send_event('E_CTRL_ROLL')
        else:
            player.send_event('E_CTRL_RUSH')

    def reset_skills_cost(self, *args):
        self.reset_roll_cost()
        self.reset_air_jump_cost()

    def reset_skill_stamina(self, skill_nd, skill_id):
        if not self.player:
            return
        stamina_count = self.player.ev_g_energy_segment(skill_id)
        if stamina_count > 0:
            self._stamina_count[skill_id] = stamina_count
            template_path = STAMINA_MAP.get(stamina_count, 'battle/i_fight_roll_1')
            cur_template_path = skill_nd.GetTemplatePath()
            if cur_template_path != template_path:
                widget_name = skill_nd.GetName()
                p = skill_nd.GetParent()
                skill_nd.Destroy()
                ret = global_data.uisystem.load_template_create(template_path, parent=p, root=self.panel, name=widget_name)
            return True
        return False

    def reset_roll_cost(self, *args):
        need_change = self.reset_skill_stamina(self.panel.nd_real_roll, SKILL_ROLL)
        if need_change:
            self.on_roll_stamina_changed(self.player.ev_g_energy(SKILL_ROLL) * 100.0)
        self.init_rocker()

    def reset_air_jump_cost(self, *args):
        if not self.player:
            return
        if self.player.ev_g_jump_max_stage() == 1:
            self.panel.nd_jump_roll.setVisible(False)
            self.panel.btn_icon_jump.setScale(1)
            return
        self.panel.nd_jump_roll.setVisible(True)
        need_change = self.reset_skill_stamina(self.panel.nd_jump_roll, SKILL_AIR_JUMP)
        if need_change:
            self.on_air_jump_stamina_changed(self.player.ev_g_energy(SKILL_AIR_JUMP) * 100)

    def on_roll_stamina_changed(self, stamina):
        self.panel.nd_real_roll.progress.SetPercentage(stamina)
        roll_stamina_count = self._stamina_count[SKILL_ROLL]
        valid_roll_num = int(stamina / 100.0 * roll_stamina_count)
        for i in range(roll_stamina_count):
            index = i + 1
            stamina_pointer = getattr(self.panel.nd_real_roll, 'img_use%d' % index, None)
            stamina_pointer and stamina_pointer.setVisible(index <= valid_roll_num)

        return

    def on_air_jump_stamina_changed(self, stamina):
        self.panel.nd_jump_roll.progress.SetPercentage(stamina)
        jump_stamina_count = self._stamina_count[SKILL_AIR_JUMP]
        valid_roll_num = int(stamina / 100.0 * jump_stamina_count)
        for i in range(jump_stamina_count):
            index = i + 1
            stamina_pointer = getattr(self.panel.nd_jump_roll, 'img_use%d' % index, None)
            stamina_pointer and stamina_pointer.setVisible(index <= valid_roll_num)

        return

    def init_global_event(self):
        global_data.emgr.on_player_jump_on_ground += self.on_posture_stand
        global_data.emgr.on_player_roll_stamina_changed += self.on_roll_stamina_changed
        global_data.emgr.on_player_air_jump_stamina_changed += self.on_air_jump_stamina_changed
        global_data.emgr.on_player_unequip_rush_bone_event += self.check_roll_btn_appearance
        global_data.emgr.on_player_equip_rush_bone_event += self.check_roll_btn_appearance
        global_data.emgr.on_player_add_jump_max_stage_event += self.check_jump_btn_appearance

    def init_event(self):
        self.init_global_event()

    def on_finalize_panel(self):
        self.unbind_posture_ui_event(self.player)
        self.player = None
        if self.custom_ui_com:
            self.custom_ui_com.destroy()
            self.custom_ui_com = None
        if self.roll_rocker_widget:
            self.roll_rocker_widget.destroy()
            self.roll_rocker_widget = None
        return

    def init_ui(self):
        self.panel.nd_real_roll.progress.SetPercentage(0)

    def init_stamina_parameters(self):
        self._stamina_count = {SKILL_ROLL: 3,
           SKILL_AIR_JUMP: 0
           }

    def init_parameters(self):
        self.init_stamina_parameters()
        self.player = None
        self.is_player_first_setted = False
        self.cur_up_show_posture = None
        self.cur_down_show_posture = None
        self.cur_camera_state = None
        self.init_custom_com()
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        if player:
            self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted
        econf = {'player_enable_rocker_dash': self.on_rocker_dash
           }
        emgr.bind_events(econf)
        self.is_rocker_dash = global_data.player.get_setting(uoc.ROCKER_DASH)
        self.sst_frocker_setting = None
        self.last_finger_move_vec = None
        return

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {uoc.OPE_POSTURE_KEY: 'cur_posture_sel'})

    def on_player_setted(self, player):
        self.unbind_posture_ui_event(self.player)
        self.player = player
        if self.player:
            if not self.is_player_first_setted:
                self.init_posture_btn_select()
                self.is_player_first_setted = True
            self.reset_skills_cost()
            self.bind_posture_ui_event(self.player)
            self.check_roll_btn_appearance()
            self.check_jump_btn_appearance()

    def on_rocker_dash(self, flag):
        self.is_rocker_dash = flag
        if self.roll_rocker_widget:
            self.roll_rocker_widget.enable_drag = self.is_rocker_dash

    def on_posture_stand(self, *args):
        if self.cur_posture_sel == OPE_POSTURE_SEPARATE:
            self.update_sel_separate_posture_btn(POSTURE_STAND)

    def on_posture_squat(self):
        if self.cur_posture_sel == OPE_POSTURE_SEPARATE:
            self.update_sel_separate_posture_btn(POSTURE_SQUAT)

    def on_posture_ground(self, *args):
        pass

    def on_posture_jump(self, *args):
        if self.cur_posture_sel == OPE_POSTURE_SEPARATE:
            self.update_sel_separate_posture_btn(POSTURE_JUMP)

    def on_leave_jump(self, *args):
        if self.cur_posture_sel == OPE_POSTURE_SEPARATE:
            self.update_sel_separate_posture_btn(POSTURE_STAND)

    def bind_posture_ui_event(self, target):
        if target:
            target.regist_event('E_STAND', self.on_posture_stand)
            target.regist_event('E_SQUAT', self.on_posture_squat)
            target.regist_event('E_JUMP', self.on_posture_jump)
            target.regist_event('E_LEAVE_JUMP', self.on_leave_jump)
            target.regist_event('E_SKILL_INIT_COMPLETE', self.reset_skills_cost)
            target.regist_event('E_LEAVE_SKATE', self._off_skate)
            target.regist_event('E_BOARD_SKATE', self._on_skate)

    def unbind_posture_ui_event(self, target):
        if target and target.is_valid():
            target.unregist_event('E_STAND', self.on_posture_stand)
            target.unregist_event('E_SQUAT', self.on_posture_squat)
            target.unregist_event('E_JUMP', self.on_posture_jump)
            target.unregist_event('E_LEAVE_JUMP', self.on_leave_jump)
            target.unregist_event('E_SKILL_INIT_COMPLETE', self.reset_skills_cost)
            target.unregist_event('E_LEAVE_SKATE', self._off_skate)
            target.unregist_event('E_BOARD_SKATE', self._on_skate)

    def _try_jump(self, low=False):
        if not self.player:
            return
        if self.player.ev_g_is_crouch():
            character_ctrl_utils.try_squat_to_stand(self.player)
        elif low:
            self.player.send_event('E_CTRL_JUMP_LOW')
        else:
            try_jump(self.player)

    def _try_squat(self):
        if not self.player:
            return
        if self.player.ev_g_is_stand():
            character_ctrl_utils.try_stand_to_squat(self.player)
        elif self.player.ev_g_is_crouch():
            character_ctrl_utils.try_squat_to_stand(self.player)

    def init_posture_btn_select(self):
        if not self.player:
            return
        else:
            self.cur_posture_sel = None
            global_data.emgr.posture_ope_ui_change_event += self.on_switch_posture_ope
            self.on_switch_posture_ope(self.player.get_owner().cur_posture_setting)
            return

    def on_switch_posture_ope(self, new_ope_sel):
        if self.cur_posture_sel != new_ope_sel:
            if new_ope_sel == OPE_POSTURE_SEPARATE:
                self.panel.right_2.setVisible(True)
                self.panel.right.setVisible(False)
            self.cur_posture_sel = new_ope_sel
            self.custom_ui_com.refresh_custom_ui_conf(uoc.OPE_POSTURE_KEY)

    def on_begin_squat_btn_exc(self, btn, *args):
        self.play_touch_effect(global_data.is_key_mocking_ui_event or 'squat_click' if 1 else None, 'click', self.panel.nd_squat.getPosition(), self.panel.nd_squat.getScale())
        self._set_posture_btn_sel(POSTURE_SQUAT, True)
        self._try_squat()
        return True

    def _on_begin_squat_btn(self, btn, *args):
        if global_data.is_pc_mode:
            guide_id = global_data.player.get_lbs_step()
            if guide_id is None:
                return True
        return self.on_begin_squat_btn_exc(btn, *args)

    def on_begin_jump_btn_exc(self, btn, *args):
        self.play_touch_effect(global_data.is_key_mocking_ui_event or 'jump_click' if 1 else None, 'click', self.panel.nd_jump.getPosition(), self.panel.nd_jump.getScale())
        self._set_posture_btn_sel(POSTURE_JUMP, True)
        from logic.gutils.climb_utils import on_begin_jump_btn_exc
        on_begin_jump_btn_exc()
        return True

    def _on_begin_jump_btn(self, btn, *args):
        if global_data.is_pc_mode:
            guide_id = global_data.player.get_lbs_step()
            if guide_id is None:
                return True
        return self.on_begin_jump_btn_exc(btn, *args)

    def silence_climb(self):
        from logic.gutils.climb_utils import silence_climb
        return silence_climb()

    def silence_jump(self, low=False):
        from logic.gutils.climb_utils import silence_jump
        return silence_jump(low)

    def check_climb(self):
        from logic.gutils.climb_utils import check_climb
        return check_climb()

    def on_end_squat_btn(self, *args):
        self._set_posture_btn_sel(POSTURE_SQUAT, False)
        self._set_posture_btn_sel(self.cur_sel_posture, True)

    def on_end_jump_btn(self, *args):
        self._set_posture_btn_sel(POSTURE_JUMP, False)
        self._set_posture_btn_sel(self.cur_sel_posture, True)

    def init_separate_posture_buttons(self):
        self.cur_sel_posture = None
        self.panel.btn_jump.EnableCustomState(True)
        self.panel.btn_icon_jump.EnableCustomState(True)
        self.panel.btn_squat.EnableCustomState(True)
        self.panel.btn_icon_squat.EnableCustomState(True)
        self.panel.btn_roll.EnableCustomState(True)
        self.panel.btn_roll.set_sound_enable(False)
        return

    def update_sel_separate_posture_btn(self, cur_posture):
        if self.cur_sel_posture:
            self._set_posture_btn_sel(self.cur_sel_posture, False)
        self.cur_sel_posture = cur_posture
        self._set_posture_btn_sel(self.cur_sel_posture, True)

    def _set_posture_btn_sel(self, posture, is_sel):
        if posture == POSTURE_JUMP:
            self.panel.btn_jump.SetSelect(is_sel)
            self.panel.btn_icon_jump.SetSelect(is_sel)
        elif posture == POSTURE_STAND:
            pass
        elif posture == POSTURE_SQUAT:
            self.panel.btn_squat.SetSelect(is_sel)
            self.panel.btn_icon_squat.SetSelect(is_sel)
        elif posture == POSTURE_GROUND:
            return

    def check_visible(self):
        if not (global_data.player and global_data.player.logic):
            return
        if global_data.player.logic.ev_g_get_state(status_config.ST_SWIM):
            self.add_hide_count('swim')

    def check_roll_btn_appearance(self, *args):
        from logic.gcommon.const import ROLL_NORMAL_PATH, ROLL_SEL_PATH, BONE_RUSH_NORMAL_PATH, BONE_RUSH_SEL_PATH
        if self.player:
            if self.player.ev_g_is_equip_rush_bone():
                self.panel.btn_icon_roll.SetFrames('', [BONE_RUSH_NORMAL_PATH, BONE_RUSH_SEL_PATH, BONE_RUSH_NORMAL_PATH], False, None)
            else:
                self.panel.btn_icon_roll.SetFrames('', [ROLL_NORMAL_PATH, ROLL_SEL_PATH, ROLL_NORMAL_PATH], False, None)
        return

    def check_jump_btn_appearance(self, *args):
        if not self.player:
            return
        else:
            if self.player.ev_g_get_state(status_config.ST_SKATE):
                self._on_skate()
            else:
                from logic.gcommon.const import BONE_JUMP_PATHS
                max_stage = self.player.ev_g_jump_max_stage()
                if max_stage not in BONE_JUMP_PATHS:
                    max_stage = 1
                path_list = BONE_JUMP_PATHS.get(max_stage, [])
                if path_list:
                    self.panel.btn_icon_jump.SetFrames('', path_list, False, None)
                self.reset_air_jump_cost()
            return

    def _off_skate(self, *args):
        self.check_jump_btn_appearance()

    def _on_skate(self, *args):
        from logic.gcommon.const import BONE_JUMP_PATHS
        path_list = BONE_JUMP_PATHS.get(1, [])
        if path_list:
            self.panel.btn_icon_jump.SetFrames('', path_list, False, None)
        self.panel.nd_jump_roll.setVisible(False)
        return

    def on_change_ui_custom_data(self):
        ui = global_data.ui_mgr.get_ui('GuideUI')
        if ui:
            param = self.change_ui_data()
            ui.on_change_ui_inform_guide_mixed(param)

    def change_ui_data(self):
        need_to_adjust_scale_type_nodes = (('right_2.nd_jump', 'nd_jump_tips', None), )
        return get_change_ui_data_for_guide_ui(need_to_adjust_scale_type_nodes, self.panel)