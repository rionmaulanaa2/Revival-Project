# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaControlMain.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_NO_EFFECT
import logic.gcommon.common_const.ui_operation_const as uoc
from data.camera_state_const import AIM_MODE
from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
from .MechaControlBtn.MechaControlBtn import ControlBtn, ControlBtnWithCopyFunc
from .MechaControlBtn.MechaControlBtn import ControlBtnPC
from logic.gutils import character_ctrl_utils
from logic.gcommon.cdata import mecha_status_config
from common.cfg import confmgr
from logic.client.const import pc_const
from logic.gutils import pc_utils
from logic.gutils import mecha_utils
from logic.gutils.client_unit_tag_utils import preregistered_tags
from data.mecha_sens_open_scheme import check_scope_main_weapon_sensitivity_opened, check_scope_sub_weapon_sensitivity_opened, check_special_form_main_weapon_sensitivity_opened, check_special_form_sub_weapon_sensitivity_opened
import copy
import cc
import game
from logic.gcommon.common_const.ui_operation_const import DRAG_DASH_BTN_8018, DRAG_DASH_BTN_8026, DRAG_DASH_BTN_8027
ASSOCIATE_UI_LIST = [
 'FireRockerUI', 'FightLeftShotUI', 'PostureControlUI', 'WeaponBarSelectUI', 'BulletReloadUI', 'FFAWeaponBulletUI']
ALL_ACTION_NUMBER = 8
EXT_SKIL_BTNS = ['action7']
ALL_ACTIONS = [ 'action{}'.format(i) for i in range(1, ALL_ACTION_NUMBER + 1) ]
PVE_VISIBLE_ACTIONS = {8013: {'visible_btn_pc': ['action1', 'action2', 'action4', 'action5', 'action6', 'action8'],'visible_btn': [
                        'action1', 'action2', 'action4', 'action5', 'action6', 'action8']
          }
   }
ENABLE_DRAY_BTN_SETTING = {8018: {'action6': DRAG_DASH_BTN_8018},8026: {'action6': DRAG_DASH_BTN_8026},8027: {'action6': DRAG_DASH_BTN_8027}}

class MechaControlMain(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/mech_control_main'
    DLG_ZORDER = BASE_LAYER_ZORDER
    ENABLE_HOT_KEY_SUPPORT = True
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'fire_move.OnDrag': 'on_fire_move_drag',
       'fire_move.OnBegin': 'on_fire_move_begin',
       'fire_move.OnEnd': 'on_fire_move_end'
       }
    UNAVAILABLE_ACTION_IDS = []
    DEFAULT_ACT_TEMPLATE = {'action1': 'i_mech_fire',
       'action2': 'i_mech_fire',
       'action3': 'i_mech_fire',
       'action4': 'i_mech_sub_skill',
       'action5': 'i_mech_posture',
       'action6': 'i_mech_posture',
       'action7': 'i_mech_sp_skill',
       'action8': 'i_mech_posture'
       }
    GLOBAL_EVENT = {'pc_hotkey_hint_display_option_changed': '_on_pc_hotkey_hint_display_option_changed',
       'pc_hotkey_hint_switch_toggled': '_on_pc_hotkey_hint_switch_toggled'
       }

    def on_init_panel(self):
        self.custom_ui_com = None
        self.panel.setLocalZOrder(uoc.FIRE_LOCAL_ZORDER)
        self.action_temp = {}
        self.init_parameters()
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())
        return

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.destroy_action_btn()
        self.show_main_ui()
        self.player = None
        self.mecha = None
        self.destroy_widget('custom_ui_com')
        self.clear_special_temp()
        return

    def clear_special_temp(self):
        if not self.action_temp:
            return
        for act_id, temp_name in six.iteritems(self.action_temp):
            if act_id in self.UNAVAILABLE_ACTION_IDS:
                continue
            old_temp = getattr(self.panel, act_id)
            pos = old_temp.GetPosition()
            old_scale = old_temp.getScale()
            parent = old_temp.GetParent()
            parent.DestroyChild(act_id)
            new_temp = global_data.uisystem.load_template_create('battle_mech/{}'.format(self.DEFAULT_ACT_TEMPLATE[act_id]))
            parent.AddChild(act_id, new_temp)
            setattr(self.panel, act_id, new_temp)
            new_temp.SetPosition(*pos)
            new_temp.setScale(old_scale)

        self.action_temp = {}

    def enter_screen(self):
        super(MechaControlMain, self).enter_screen()
        self.hide_main_ui(ASSOCIATE_UI_LIST)
        self.bind_emgr_events(True)
        self.init_parameters()
        if not self.custom_ui_com:
            self.init_custom_com()

    def leave_screen(self):
        super(MechaControlMain, self).leave_screen()
        self.bind_emgr_events(False)
        self.on_finalize_panel()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_parameters(self):
        self.player = None
        self.mecha = None
        self.mecha_id = None
        self.action_btns = {}
        self.action_rocker = {}
        self.clear_special_temp()
        self.action_anim_done = False
        self.enable_copy_action = True
        self.ACTION_SHOW_ORDER = []
        if global_data.is_pc_mode:
            self.ACTION_SHOW_ORDER = [
             ('action1', )]
        else:
            self.ACTION_SHOW_ORDER = [
             ('action1', 'action2', 'action3', 'action4'), ('action8', ), ('action6', ), ('action5', ), ('action7', )]
        self.ACTION_SHOW_DELAY = 0.25
        self.enable_trace = False
        self.enable_3d_touch = False
        self.sst_3d_touch = None
        self.action1_rocker_cache = True
        self.is_3d_touch_btn_down = False
        self.left_fire_ope = uoc.LEFT_FIRE_ALWAYS_OPEN
        self.left_fire_ope_move = uoc.LF_ONLY_SHOT
        self._forbidden_draggable_btn = set()
        self.on_aim = False
        self.move_skill_disabled = False
        self.second_weapon_disabled = False
        return

    def bind_emgr_events(self, bind):
        emgr = global_data.emgr
        events = {'scene_player_setted_event': self.on_player_setted,
           'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        if not global_data.is_pc_mode:
            events.update({'firerocker_ope_change_event': self.set_fire_rocker_opt,
               'app_3d_touch_switch_event': self.support_3d_touch,
               'threed_touch_change_event': self.set_3d_touch_opt,
               'threed_touch_pressure_change_event': self.set_3d_touch_percent,
               'left_fire_ope_change_event': self.set_left_fire_ope,
               'mecha_sens_val_changed': self._on_mecha_sens_val_changed,
               'update_mecha_sensitivity_type': self._check_mecha_sens
               })
        if bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def _initialize_weapon_sensitivity_opened_parameters(self):
        mecha_id = self.mecha_id
        if mecha_id:
            self.scope_main_weapon_sensitivity_opened = check_scope_main_weapon_sensitivity_opened(mecha_id)
            self.scope_sub_weapon_sensitivity_opened = check_scope_sub_weapon_sensitivity_opened(mecha_id)
            self.special_form_main_weapon_sensitivity_opened = check_special_form_main_weapon_sensitivity_opened(mecha_id)
            self.special_form_sub_weapon_sensitivity_opened = check_special_form_sub_weapon_sensitivity_opened(mecha_id)
        else:
            self.scope_main_weapon_sensitivity_opened, self.scope_sub_weapon_sensitivity_opened = False, False
            self.special_form_main_weapon_sensitivity_opened, self.special_form_sub_weapon_sensitivity_opened = False, False

    def init_event(self, mecha=None):
        if not mecha:
            ctrl_target = global_data.player.logic.ev_g_control_target()
            if ctrl_target.__class__.__name__ == 'MechaTrans':
                mecha = ctrl_target.logic
        if mecha:
            if self.mecha:
                return
            if not self.custom_ui_com:
                self.init_custom_com()
            self.mecha = mecha
            if mecha.__class__.__name__ == 'LMecha' and not global_data.is_pc_mode:
                self.mecha_id = mecha.sd.ref_mecha_id
            else:
                self.mecha_id = None
            self._initialize_weapon_sensitivity_opened_parameters()
            self.check_enable_copy()
            self.init_action_btn()
        return

    def check_enable_copy(self):
        if global_data.player and global_data.player.in_local_battle() or global_data.player.in_new_local_battle():
            self.enable_copy_action = False
            return
        if not global_data.is_pc_mode and self.mecha and self.mecha.MASK & preregistered_tags.VEHICLE_TAG_VALUE == 0:
            self.enable_copy_action = True
        else:
            self.enable_copy_action = False

    def refresh_temp_pc_show(self, act_id=None):
        if not global_data.is_pc_control_enable:
            return
        else:
            if act_id is not None:
                nd = getattr(self.panel, act_id)
                parent = nd.GetParent()
                nd_temp_pc = getattr(parent, 'temp_pc')
                if nd_temp_pc:
                    nd_temp_pc.setVisible(nd.isVisible())
                return
            for action_id in ALL_ACTIONS:
                nd = getattr(self.panel, action_id)
                parent = nd.GetParent()
                nd_temp_pc = getattr(parent, 'temp_pc')
                if nd_temp_pc:
                    nd_temp_pc.setVisible(nd.isVisible())

            return

    def init_enable_drag_btn(self):
        info = ENABLE_DRAY_BTN_SETTING.get(self.mecha_id)
        if not info:
            return
        for act_id, setting_key in six.iteritems(info):
            enable = False
            if global_data.player:
                enable = global_data.player.get_setting_2(setting_key)
            self._enable_weapon_rocker_drag(act_id, enable)

    def init_action_btn(self, target_action=None, clear_visible=True):
        if not global_data.is_pc_mode:
            self.init_weapon_rocker_draggable()
        self.init_enable_drag_btn()
        if self.action_btns and not target_action:
            return
        else:
            if target_action:
                if target_action in self.action_btns and self.action_btns[target_action] != None:
                    log_error('init_action_btn with an none empty action_btn!', target_action, self.action_btns)
            for action_id in ALL_ACTIONS:
                if action_id in self.UNAVAILABLE_ACTION_IDS:
                    continue
                if target_action and action_id != target_action:
                    continue
                nd = getattr(self.panel, action_id)
                nd.setVisible(False)
                parent = nd.GetParent()
                nd_temp_pc = getattr(parent, 'temp_pc')
                if nd_temp_pc:
                    nd_temp_pc.setVisible(False)

            self.hide_all_copy_nd()
            shape_id = self.mecha.ev_g_shape_id()
            action_config = confmgr.get('mecha_conf', 'ActionConfig', 'Content', shape_id)
            if not action_config:
                return
            old_action_temp = self.action_temp
            if old_action_temp:
                self.clear_special_temp()
            self.action_temp = action_config.get('action_temp', None)
            if self.action_temp:
                for act_id, temp_name in six.iteritems(self.action_temp):
                    if act_id in self.UNAVAILABLE_ACTION_IDS:
                        continue
                    if target_action and act_id != target_action:
                        continue
                    old_temp = getattr(self.panel, act_id)
                    pos = old_temp.GetPosition()
                    parent = old_temp.GetParent()
                    old_scale = old_temp.getScale()
                    parent.DestroyChild(act_id)
                    new_temp = global_data.uisystem.load_template_create('battle_mech/{}'.format(temp_name))
                    parent.AddChild(act_id, new_temp)
                    setattr(self.panel, act_id, new_temp)
                    new_temp.SetPosition(*pos)
                    new_temp.setScale(old_scale)

            action_map = action_config['action_map']
            rocker_btn = action_config.get('rocker_btn', [])
            for act_id, st_id in six.iteritems(action_map):
                if act_id in self.UNAVAILABLE_ACTION_IDS:
                    continue
                if target_action and act_id != target_action:
                    continue
                if isinstance(st_id, str):
                    st_id = mecha_status_config.desc_2_num[st_id]
                if global_data.is_pc_mode:
                    self.action_btns[act_id] = ControlBtnPC(getattr(self.panel, act_id), act_id, st_id, action_config)
                else:
                    self.action_btns[act_id] = self.check_copy_func(getattr(self.panel, act_id), act_id, st_id, action_config)
                    self.action_btns[act_id].enableRocker(act_id in rocker_btn and act_id not in self._forbidden_draggable_btn)

            if not global_data.is_pc_mode:
                self._check_main_weapon_rocker_sens()
                self._check_sub_weapon_rocker_sens()
            if global_data.is_pc_mode:
                visible_btn_str = 'visible_btn_pc' if 1 else 'visible_btn'
                if global_data.game_mode and global_data.game_mode.is_pve():
                    action_config = PVE_VISIBLE_ACTIONS.get(self.mecha_id) or action_config
                if clear_visible:
                    self.visible_btns = copy.deepcopy(action_config[visible_btn_str])
                if not global_data.is_pc_mode:
                    self.update_left_ope_btn_visibility()
                if not self.action_anim_done and not global_data.is_pc_mode and not self.mecha.share_data.ref_forbid_show_action_anim:
                    self.show_action_anim()
                else:
                    if self.mecha.share_data.ref_forbid_show_action_anim:
                        self.action_anim_done = True
                    for action_id in self.visible_btns:
                        self.action_btns[action_id].setVisible(True)

                    self.refresh_temp_pc_show()
                self.action1_rocker_cache = global_data.is_pc_mode or 'action1' in rocker_btn
                self.init_fire_rocker_setting()
                self.set_left_fire_ope()
            return

    def show_action_anim(self):
        if len(self.ACTION_SHOW_ORDER) <= 0:
            self.action_anim_done = True
            self.refresh_temp_pc_show()
            return
        actions = self.ACTION_SHOW_ORDER.pop(0)
        can_show = False
        for action_id in actions:
            if action_id in self.visible_btns and action_id not in self.UNAVAILABLE_ACTION_IDS:
                can_show = True
                break

        if can_show:
            self.process_one_anim(actions)
        else:
            self.show_action_anim()

    def process_one_anim(self, actions):
        for action_id in actions:
            if action_id in self.action_btns:
                nd = self.action_btns[action_id].nd
                self.action_btns[action_id].stop_btn()
                nd.PlayAnimation('show')
                self.action_btns[action_id].setVisible(action_id in self.visible_btns)

        def finished():
            if self and self.is_valid():
                self.show_action_anim()

        self.panel.stopAllActions()
        self.panel.SetTimeOut(self.ACTION_SHOW_DELAY, finished)

    def destroy_action_btn(self):
        for action_id, control_btn in six.iteritems(self.action_btns):
            control_btn.destroy()
            del control_btn
            self.action_btns[action_id] = None

        self.action_btns = {}
        return

    def destroy_single_action_btn(self, act_id):
        if act_id in self.action_btns:
            control_btn = self.action_btns[act_id]
            if control_btn:
                if self.mecha:
                    control_btn.unbind_events(self.mecha)
                control_btn.destroy()
                del control_btn
                self.action_btns[act_id] = None
                del self.action_btns[act_id]
        return

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        if self.player:
            self.bind_player_event(self.player)
        else:
            self.mecha = None
            self.mecha_id = None
            self._initialize_weapon_sensitivity_opened_parameters()
            self._check_mecha_sens()
        return

    def bind_player_event(self, target):
        regist_func = target.regist_event

    def on_mecha_setted(self, mecha):
        if mecha:
            self.init_event(mecha)
            self.bind_mecha_event(mecha)
            if mecha.MASK & preregistered_tags.VEHICLE_TAG_VALUE == 0:
                UIDistorterHelper().apply_ui_distort(self.__class__.__name__)
            mecha.send_event('E_MECHA_CONTROL_MAIN_INIT_COMPLETE')
            global_data.player.logic.send_event('E_MECHA_CONTROL_MAIN_INIT_COMPLETE')
            global_data.emgr.mecha_control_main_ui_event.emit()

    def bind_mecha_event(self, mecha):
        regist_func = mecha.regist_event
        regist_func('E_SET_ACTION_VISIBLE', self.on_set_action_visible)
        regist_func('E_SET_ACTION_NB_VISIBLE', self.on_set_action_nb_visible)
        regist_func('E_SET_ACTION_OFFSET', self.on_set_action_offset)
        regist_func('G_SET_ACTION_ROCKER', self.on_set_action_rocker)
        regist_func('E_RESET_ACTION_ROCKER', self.on_reset_action_rocker)
        regist_func('E_START_ACTION_CD', self.on_start_action_cd)
        regist_func('E_STOP_ACTION_CD', self.on_stop_action_cd)
        regist_func('E_SWITCH_BEHAVIOR', self.on_switch_behavior)
        regist_func('E_SWITCH_ACTION', self.on_switch_action)
        regist_func('E_SWITCH_ACTION_BIND_SKILL_ID', self.on_switch_action_bind_skill_id)
        regist_func('E_ADD_ACTION_SUB_SKILL_ID', self.on_add_action_sub_skill_id)
        regist_func('E_DEL_ACTION_SUB_SKILL_ID', self.on_del_action_sub_skill_id)
        regist_func('E_SET_ACTION_ENABLE', self.on_set_action_enable)
        regist_func('E_SET_ACTION_FORBIDDEN', self.on_set_action_forbidden)
        regist_func('E_SET_ACTIONS_FORBIDDEN', self.on_set_actions_forbidden)
        regist_func('E_SET_ACTION_SELECTED', self.on_set_action_selected)
        regist_func('E_SET_ACTION_CUSTOM_STATE', self.on_set_custom_state)
        regist_func('E_SET_ACTION_ICON', self.on_set_action_icon)
        regist_func('E_SHOW_ACTION_PROGRESSS', self.on_show_action_progress)
        regist_func('E_DISABLE_MOVE_SKILL', self.on_disable_move_skill)
        regist_func('E_DISABLE_SECOND_WEAPON', self.on_disable_second_weapon)
        regist_func('E_ENABLE_ROCKER_DRAG', self._enable_weapon_rocker_drag)
        regist_func('G_DRAGGED_DIR', self.get_dragged_dir)
        regist_func('E_USE_BTN_DRAG_HELPER', self.use_btn_drag_helper)
        regist_func('E_ACTIVE_BALL_DRIVER', self.on_trans_to_ball, 99)
        regist_func('E_DISABLE_BALL_DRIVER', self.on_trans_to_human, 99)
        for btn in six.itervalues(self.action_btns):
            btn.bind_events(mecha)

        if global_data.move_rocker_simple:
            global_data.move_rocker_simple.on_player_setted(mecha)

    def unbind_ui_event(self, target):
        if not self.mecha:
            return
        else:
            unregist_func = self.mecha.unregist_event
            unregist_func('E_SET_ACTION_VISIBLE', self.on_set_action_visible)
            unregist_func('E_SET_ACTION_NB_VISIBLE', self.on_set_action_nb_visible)
            unregist_func('E_SET_ACTION_OFFSET', self.on_set_action_offset)
            unregist_func('E_SET_ACTION_ROCKER', self.on_set_action_rocker)
            unregist_func('E_RESET_ACTION_ROCKER', self.on_reset_action_rocker)
            unregist_func('E_START_ACTION_CD', self.on_start_action_cd)
            unregist_func('E_STOP_ACTION_CD', self.on_stop_action_cd)
            unregist_func('E_SWITCH_BEHAVIOR', self.on_switch_behavior)
            unregist_func('E_SWITCH_ACTION', self.on_switch_action)
            unregist_func('E_SWITCH_ACTION_BIND_SKILL_ID', self.on_switch_action_bind_skill_id)
            unregist_func('E_ADD_ACTION_SUB_SKILL_ID', self.on_add_action_sub_skill_id)
            unregist_func('E_DEL_ACTION_SUB_SKILL_ID', self.on_del_action_sub_skill_id)
            unregist_func('E_SET_ACTION_ENABLE', self.on_set_action_enable)
            unregist_func('E_SET_ACTION_SELECTED', self.on_set_action_selected)
            unregist_func('E_SET_ACTION_CUSTOM_STATE', self.on_set_custom_state)
            unregist_func('E_SET_ACTION_ICON', self.on_set_action_icon)
            unregist_func('G_SET_ACTION_ROCKER', self.on_set_action_rocker)
            unregist_func('E_SET_ACTION_FORBIDDEN', self.on_set_action_forbidden)
            unregist_func('E_SET_ACTIONS_FORBIDDEN', self.on_set_actions_forbidden)
            unregist_func('E_SHOW_ACTION_PROGRESSS', self.on_show_action_progress)
            unregist_func('E_DISABLE_MOVE_SKILL', self.on_disable_move_skill)
            unregist_func('E_DISABLE_SECOND_WEAPON', self.on_disable_second_weapon)
            unregist_func('E_ENABLE_ROCKER_DRAG', self._enable_weapon_rocker_drag)
            unregist_func('G_DRAGGED_DIR', self.get_dragged_dir)
            unregist_func('E_USE_BTN_DRAG_HELPER', self.use_btn_drag_helper)
            unregist_func('E_ACTIVE_BALL_DRIVER', self.on_trans_to_ball)
            unregist_func('E_DISABLE_BALL_DRIVER', self.on_trans_to_human)
            for btn in six.itervalues(self.action_btns):
                btn.unbind_events(self.mecha)

            if global_data.move_rocker_simple:
                global_data.move_rocker_simple.on_player_setted(None)
            if not target or not target.is_valid():
                return
            return

    def on_switch_behavior(self, shape_id, *args):
        self.action_anim_done = True
        action_config = confmgr.get('mecha_conf', 'ActionConfig', 'Content', shape_id)
        if not action_config or action_config.get('action_temp', None):
            for btn in six.itervalues(self.action_btns):
                btn.unbind_events(self.mecha)

            self.destroy_action_btn()
            self.init_action_btn()
            for btn in six.itervalues(self.action_btns):
                btn.bind_events(self.mecha)

        else:
            action_map = action_config['action_map']
            rocker_btn = action_config.get('rocker_btn', [])
            for act_id, st_id in six.iteritems(action_map):
                if act_id in self.UNAVAILABLE_ACTION_IDS:
                    continue
                if isinstance(st_id, str):
                    st_id = mecha_status_config.desc_2_num[st_id]
                if act_id in self.action_btns:
                    self.action_btns[act_id].unbind_events(self.mecha, is_init=False)
                    self.action_btns[act_id].bind_state_id = st_id
                    self.action_btns[act_id].refresh_action_icon_and_extend_ui(act_id, action_config)
                    self.action_btns[act_id].bind_events(self.mecha, st_id, is_init=False)
                else:
                    if global_data.is_pc_mode:
                        self.action_btns[act_id] = ControlBtnPC(getattr(self.panel, act_id), act_id, st_id, action_config)
                    else:
                        self.action_btns[act_id] = self.check_copy_func(getattr(self.panel, act_id), act_id, st_id, action_config)
                        self.action_btns[act_id].enableRocker(act_id in rocker_btn and act_id not in self._forbidden_draggable_btn)
                    self.action_btns[act_id].bind_events(self.mecha)

            if global_data.is_pc_mode:
                visible_btn_key = 'visible_btn_pc' if 1 else 'visible_btn'
                if global_data.game_mode and global_data.game_mode.is_pve():
                    action_config = PVE_VISIBLE_ACTIONS.get(self.mecha_id) or action_config
                self.visible_btns = copy.deepcopy(action_config[visible_btn_key])
                for action_id in EXT_SKIL_BTNS:
                    state_id = character_ctrl_utils.get_bind_state_id(shape_id, action_id)
                    if not state_id:
                        continue
                    skill_id = self.mecha.ev_g_bind_skill(state_id)
                    if skill_id and self.mecha.ev_g_skill(skill_id):
                        self.visible_btns.append(action_id)

                global_data.is_pc_mode or self.update_left_ope_btn_visibility()
            visible_actions = set(self.visible_btns)
            for act_id in ALL_ACTIONS:
                if act_id in self.UNAVAILABLE_ACTION_IDS:
                    continue
                self.action_btns[act_id].setVisible(act_id in visible_actions)

            self.refresh_temp_pc_show()
        global_data.player.logic.send_event('E_MECHA_CONTROL_MAIN_REINIT_COMPLETE')
        return

    def on_switch_action(self, action, state_id, keep_alive=True):
        if isinstance(state_id, str):
            state_id = mecha_status_config.desc_2_num[state_id]
        if state_id == self.action_btns[action].bind_state_id:
            return
        btn = self.action_btns[action]
        shape_id = self.mecha.ev_g_shape_id()
        action_config = confmgr.get('mecha_conf', 'ActionConfig', 'Content', shape_id)
        rocker_btn = action_config.get('rocker_btn', [])
        btn.unbind_events(self.mecha, is_init=False)
        btn.bind_state_id = state_id
        btn.bind_events(self.mecha, state_id, is_init=False)
        if not global_data.is_pc_mode:
            self._check_main_weapon_rocker_sens()
            self._check_sub_weapon_rocker_sens()
        if not global_data.is_pc_mode:
            self.action1_rocker_cache = 'action1' in rocker_btn
            self.init_fire_rocker_setting()
            self.set_left_fire_ope()
        global_data.emgr.mecha_switch_action.emit(action, state_id)

    def on_switch_action_bind_skill_id(self, action_id, skill_id):
        if action_id in self.action_btns:
            self.action_btns[action_id].switch_action_bind_skill_id(skill_id)

    def on_add_action_sub_skill_id(self, action_id, skill_id):
        if action_id in self.action_btns:
            self.action_btns[action_id].add_action_sub_skill_id(skill_id)

    def on_del_action_sub_skill_id(self, action_id):
        if action_id in self.action_btns:
            self.action_btns[action_id].del_action_sub_skill_id()

    def on_set_action_visible(self, action_id, visible, force=False):
        if not self.action_anim_done and not force:
            return
        if action_id in self.action_btns:
            action_btn = self.action_btns[action_id]
            action_btn.setVisible(visible)
            self.refresh_temp_pc_show(action_id)
            if not action_btn.isVisible() and action_id in self.visible_btns:
                self.visible_btns.remove(action_id)

    def all_actions_cancel(self):
        from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
        for action_btn in six_ex.values(self.action_btns):
            if action_btn.rocker.btn_pushing:
                layer = action_btn.nd.bar
                layer.OnCancel(TouchMock())

    def on_set_action_nb_visible(self, action_id, visible):
        if action_id in self.action_btns:
            action_btn = self.action_btns[action_id]
            action_btn.is_nb_visible = visible
            action_btn.setVisible(visible)
            self.refresh_temp_pc_show(action_id)
            if not action_btn.isVisible() and action_id in self.visible_btns:
                self.visible_btns.remove(action_id)

    def on_set_action_offset(self, action_id, offset):
        if action_id in self.action_btns:
            self.action_btns[action_id].setOffset(offset)

    def on_set_action_rocker(self, action_id, enbale_rocker, use_drag_helper=True):
        if action_id in self.action_btns:
            self.action_btns[action_id].enableRocker(enbale_rocker and action_id not in self._forbidden_draggable_btn)
            self.action_btns[action_id].use_drag_helper = use_drag_helper
        return True

    def on_reset_action_rocker(self, action_id):
        if action_id in self.action_btns:
            self.action_btns[action_id].resetRocker()

    def on_start_action_cd(self, action_id, cd_time, init_time=0):
        if action_id in self.action_btns:
            self.action_btns[action_id].startCountDown(cd_time, init_time)

    def on_stop_action_cd(self, action_id):
        if action_id in self.action_btns:
            self.action_btns[action_id].stopCountDown()

    def on_set_action_enable(self, action_id, enable):
        if action_id in self.action_btns:
            self.action_btns[action_id].setEnable(enable)

    def on_set_actions_forbidden(self, action_ids, forbidden, reason=None):
        for action_id in action_ids:
            if action_id in self.action_btns:
                self.action_btns[action_id].setForbidden(forbidden, reason=reason)

    def on_set_action_forbidden(self, action_id, forbidden, reason=None):
        if action_id in self.action_btns:
            self.action_btns[action_id].setForbidden(forbidden, reason=reason)

    def on_set_action_selected(self, action_id, selected):
        if action_id in self.action_btns:
            btn = self.action_btns[action_id]
            return btn.setSelected(selected)

    def on_set_custom_state(self, action_id, enable):
        if action_id in self.action_btns:
            btn = self.action_btns[action_id]
            return btn.enableCustomState(enable)

    def on_set_action_icon(self, action_id, icon_path, show_anim_name=''):
        if action_id in self.action_btns:
            btn = self.action_btns[action_id]
            return btn.setIcon(icon_path, show_anim_name)

    def on_show_action_progress(self, action_id, show_progress):
        if action_id in self.action_btns:
            btn = self.action_btns[action_id]
            return btn.set_action_show_progress(show_progress)

    def on_disable_move_skill(self, disabled):
        if not self.mecha_id:
            return
        self.move_skill_disabled = disabled
        for action_id, btn in six.iteritems(self.action_btns):
            is_move_skill = action_id in ('action5', 'action6')
            state_id = btn.bind_state_id
            skill_id = self.mecha.ev_g_bind_skill(state_id)
            skill = self.mecha.ev_g_skill(skill_id)
            if skill:
                if skill.is_move_skill == -1:
                    if is_move_skill:
                        skill.is_move_skill = 1 if 1 else 0
                    else:
                        is_move_skill = bool(skill.is_move_skill)
                btn.setForbidden(is_move_skill and disabled, 'disable_move_skill')

    def get_dragged_dir(self, action_id):
        if action_id in self.action_btns:
            if type(self.action_btns[action_id]) == ControlBtnWithCopyFunc:
                btn_org = self.action_btns[action_id].get_normal_nd()
                btn_copy = self.action_btns[action_id].get_copy_nd()
                if btn_copy.last_success_action_time > btn_org.last_success_action_time:
                    return btn_copy.btn_dragged_dir
                else:
                    return btn_org.btn_dragged_dir

            else:
                return self.action_btns[action_id].btn_dragged_dir

    def use_btn_drag_helper(self, action_id, flag):
        if action_id in self.action_btns:
            self.action_btns[action_id].use_drag_helper = flag

    def init_test_move_logic(self):
        self._cur_move_node = self.panel.action1

        @self.panel.callback()
        def OnDrag(btn, touch):
            lpos = self.panel.convertToNodeSpace(touch.getLocation())
            log_error('getLocation', touch.getLocation())
            self._cur_move_node.setPosition(lpos)

    def switch_test_move_node(self):
        distort_type, node_list = UIDistorterHelper().get_ui_parameter(self.__class__.__name__)
        for idx, node_name in enumerate(node_list):
            node = getattr(self.panel, node_name)
            if node:
                if node == self._cur_move_node:
                    if idx + 1 >= len(node_list):
                        log_error('cur node', node_list[0])
                        self._cur_move_node = getattr(self.panel, node_list[0])
                    else:
                        log_error('cur node', node_list[idx + 1])
                        self._cur_move_node = getattr(self.panel, node_list[idx + 1])
                    break

    def init_fire_rocker_setting(self):
        self.enable_trace = global_data.player.get_setting(uoc.FIREROCKER_OPE_KEY) == uoc.MOVABLE_FIREROCKER
        self.enable_3d_touch = False
        if self.check_can_open_3d_touch() and global_data.player.get_setting(uoc.ThreeD_TOUCH_TOGGLE_KEY):
            self.enable_3d_touch = True
        self.sst_3d_touch = global_data.player.get_setting(uoc.ThreeD_TOUCH_PERCENT_KEY)
        self.refresh_action1_button_ui()

    def refresh_action1_button_ui(self):
        if 'action1' not in self.action_btns:
            return
        else:
            if self.enable_trace and not global_data.is_pc_mode:
                if self.enable_3d_touch:
                    self.action_btns['action1'].setVisible(False)
                    self.action_btns['action1'].setOnBeginCallback(None)
                    self.action_btns['action1'].setOnBeginCallback(None)
                else:

                    def begin_cb(btn, touch):
                        self.panel.action1.stopAllActions()

                    def end_cb(btn, touch):
                        self.reset_fire_rocker()

                    self.action_btns['action1'].setVisible(True)
                    self.action_btns['action1'].setOnBeginCallback(begin_cb)
                    self.action_btns['action1'].setOnBeginCallback(end_cb)
                self.on_set_action_rocker('action1', False)
                self.action_btns['action1'].setSwallowTouch(False)
            else:
                self.action_btns['action1'].setVisible(True)
                self.action_btns['action1'].setOnBeginCallback(None)
                self.action_btns['action1'].setOnBeginCallback(None)
                self.on_set_action_rocker('action1', self.action1_rocker_cache)
                self.action_btns['action1'].setSwallowTouch(True)
            return

    def set_fire_rocker_opt(self, val):
        self.enable_trace = val == uoc.MOVABLE_FIREROCKER
        self.refresh_action1_button_ui()

    def support_3d_touch(self, is_open):
        cur_enable_3d_touch = False
        if is_open and global_data.player.get_setting(uoc.ThreeD_TOUCH_TOGGLE_KEY):
            cur_enable_3d_touch = True
        if cur_enable_3d_touch ^ self.enable_3d_touch:
            self.refresh_action1_button_ui()

    def check_can_open_3d_touch(self):
        from common.platform.device_info import DeviceInfo
        device_info = DeviceInfo.get_instance()
        return device_info.is_open_3d_touch()

    def set_3d_touch_opt(self, is_open):
        cur_enable_3d_touch = False
        if self.check_can_open_3d_touch() and is_open:
            cur_enable_3d_touch = True
        if cur_enable_3d_touch ^ self.enable_3d_touch:
            self.refresh_action1_button_ui()

    def set_3d_touch_percent(self, val):
        self.sst_3d_touch = val

    def on_fire_move_begin(self, layer, touch):
        if self.enable_trace:
            if self.enable_3d_touch:
                self._try_3d_touch_btn_down(layer, touch)
            else:
                self.panel.action1.stopAllActions()
        return True

    def on_fire_move_drag(self, layer, touch):
        if self.enable_trace:
            if self.enable_3d_touch:
                self._try_3d_touch_btn_down(layer, touch)
            else:
                self.set_action1_position(touch)

    def on_fire_move_end(self, layer, touch):
        if self.enable_trace:
            if self.enable_3d_touch:
                self._try_3d_touch_btn_down(layer, touch, is_touch_end=True)
            else:
                self.reset_fire_rocker()
        return True

    def set_action1_position(self, touch):
        wpos = touch.getLocation()
        lpos = self.panel.action1.getParent().convertToNodeSpace(wpos)
        sz = self.panel.action1.getContentSize()
        anchor = self.panel.action1.getAnchorPoint()
        self.panel.action1.SetPosition(lpos.x - (0.5 - anchor.x) * sz.width, lpos.y - (0.5 - anchor.y) * sz.height)
        UIDistorterHelper().apply_node_distort('MECHA_BUTTON', self.panel.action1, self.panel, '%s-action1' % self.__class__.__name__)

    def reset_fire_rocker(self, delay=0.8):
        old_pos = self.panel.action1_pos.getPosition()
        delay_act = cc.DelayTime.create(delay)
        move_act = cc.MoveTo.create(0.05, old_pos)
        self.panel.action1.stopAllActions()

        def cb():
            UIDistorterHelper().apply_node_distort('MECHA_BUTTON', self.panel.action1, self.panel, '%s-action1' % self.__class__.__name__)

        func_act = cc.CallFunc.create(cb)
        self.panel.action1.runAction(cc.Sequence.create([delay_act, move_act, func_act]))

    def check_trigger_rocker_touch_force(self, touch):
        force = touch.getPressure()
        max_force = touch.getMaxPressure()
        if force >= max_force * self.sst_3d_touch:
            return True
        return False

    def _try_3d_touch_btn_down(self, btn, touch, is_touch_end=False):
        if not self.enable_3d_touch:
            return
        if 'action1' not in self.action_btns:
            return
        wpos = touch.getLocation()
        self.panel.nd_3d_touch.SetPosition(wpos.x, wpos.y)
        is_trigger = self.check_trigger_rocker_touch_force(touch) and not is_touch_end
        if is_trigger and not self.is_3d_touch_btn_down:
            self.is_3d_touch_btn_down = True
            self.panel.nd_3d_touch.setVisible(True)
            self.panel.PlayAnimation('3d_touch')
            self.action_btns['action1'].on_begin(btn, touch)
        elif not is_trigger and self.is_3d_touch_btn_down:
            self.is_3d_touch_btn_down = False
            self.panel.nd_3d_touch.setVisible(False)
            self.panel.StopAnimation('3d_touch')
            self.action_btns['action1'].on_end(btn, touch)

    def set_left_fire_ope(self, val=None):
        if 'action2' not in self.action_btns:
            return
        else:
            is_support_move_and_shot = 'action3' in self.action_btns
            if val is None:
                val = global_data.player.get_setting(uoc.LF_OPE_KEY)
            self.left_fire_ope = val[0]
            self.left_fire_ope_move = val[1]
            if self.left_fire_ope == uoc.LEFT_FIRE_ALWAYS_OPEN:
                self.action_btns['action2'].setVisible(self.left_fire_ope_move == uoc.LF_ONLY_SHOT)
                if is_support_move_and_shot:
                    self.action_btns['action3'].setVisible(self.left_fire_ope_move == uoc.LF_SHOT_AND_MOVE)
            elif self.left_fire_ope == uoc.LEFT_FIRE_SHOW_WHEN_AIM:
                self.action_btns['action2'].setVisible(self.left_fire_ope_move == uoc.LF_ONLY_SHOT and self.on_aim)
                if is_support_move_and_shot:
                    self.action_btns['action3'].setVisible(self.left_fire_ope_move == uoc.LF_SHOT_AND_MOVE and self.on_aim)
            elif self.left_fire_ope == uoc.LEFT_FIRE_ALWAYS_CLOSE:
                if is_support_move_and_shot:
                    self.action_btns['action3'].setVisible(False)
                self.action_btns['action2'].setVisible(False)
            else:
                log_error('left_fire_ope = %d, invalid !!!!', self.left_fire_ope)
            self.refresh_action3_button_ui()
            return

    def refresh_action3_button_ui(self):
        if 'action3' not in self.action_btns:
            return
        if not global_data.is_pc_mode:
            self.on_set_action_rocker('action3', True, False)

    def update_left_ope_btn_visibility(self):
        left_vis_btns, left_unvis_btns = self.get_left_ope_visible_action_btn()
        for act in left_vis_btns:
            if act not in self.visible_btns:
                self.visible_btns.append(act)

        for act in left_unvis_btns:
            if act in self.visible_btns:
                self.visible_btns.remove(act)

    def get_left_ope_visible_action_btn(self, val=None):
        is_support_move_and_shot = 'action3' in self.action_btns
        if val is None:
            val = global_data.player.get_setting(uoc.LF_OPE_KEY)
        left_actions = [
         'action2', 'action3']

        def get_visible_list():
            self.left_fire_ope = val[0]
            self.left_fire_ope_move = val[1]
            if self.left_fire_ope == uoc.LEFT_FIRE_ALWAYS_OPEN:
                ret = [
                 'action2']
                if is_support_move_and_shot:
                    if self.left_fire_ope_move == uoc.LF_SHOT_AND_MOVE:
                        ret = [
                         'action3']
                return ret
            else:
                if self.left_fire_ope == uoc.LEFT_FIRE_SHOW_WHEN_AIM:
                    ret = [
                     'action2']
                    if is_support_move_and_shot:
                        if self.on_aim:
                            if self.left_fire_ope_move == uoc.LF_SHOT_AND_MOVE:
                                ret = [
                                 'action3']
                    return ret
                if self.left_fire_ope == uoc.LEFT_FIRE_ALWAYS_CLOSE:
                    return []
                return []

        vis_btns = get_visible_list()
        unvis_btns = []
        for act in left_actions:
            if act not in vis_btns:
                unvis_btns.append(act)

        return (vis_btns, unvis_btns)

    @staticmethod
    def _get_normal_stick_switch_val(mecha_id):
        shoot_stick_switch_val = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SHOOT_STICK_SWITCH_MECHA_VAL_KEY)
        if shoot_stick_switch_val:
            main_weapon_stick_switch_val = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
            sub_weapon_stick_switch_val = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
        else:
            main_weapon_stick_switch_val, sub_weapon_stick_switch_val = False, False
        return (main_weapon_stick_switch_val, sub_weapon_stick_switch_val)

    def get_weapon_rocker_draggable(self):
        if global_data.is_pc_mode:
            return (False, False)
        else:
            mecha_id = self.mecha_id
            if mecha_id is not None:
                main_weapon_stick_switch_val, sub_weapon_stick_switch_val = self._get_normal_stick_switch_val(mecha_id)
                if self.on_aim:
                    if not mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCOPE_SAME_AS_NORMAL_KEY):
                        if self.scope_main_weapon_sensitivity_opened:
                            main_weapon_stick_switch_val = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCOPE_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
                        if self.scope_sub_weapon_sensitivity_opened:
                            sub_weapon_stick_switch_val = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCOPE_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
                elif self.mecha and self.mecha.sd.ref_use_mecha_special_form_sensitivity:
                    if not mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SPECIAL_FORM_SAME_AS_NORMAL_KEY):
                        if self.special_form_main_weapon_sensitivity_opened:
                            main_weapon_stick_switch_val = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SPECIAL_FORM_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
                        if self.special_form_sub_weapon_sensitivity_opened:
                            sub_weapon_stick_switch_val = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SPECIAL_FORM_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
                return (
                 main_weapon_stick_switch_val, sub_weapon_stick_switch_val)
            return (
             True, True)
            return

    def init_weapon_rocker_draggable(self):
        self.set_weapon_rocker_draggable(*self.get_weapon_rocker_draggable())

    def _check_mecha_sens(self):
        self._check_weapon_rocker_draggable()
        self._check_main_weapon_rocker_sens()
        self._check_sub_weapon_rocker_sens()

    def _check_weapon_rocker_draggable(self):
        self.set_weapon_rocker_draggable(*self.get_weapon_rocker_draggable())

    def _check_main_weapon_rocker_sens(self):
        btn = self._get_action_btn('action1')
        if btn is None:
            return
        else:
            mecha_id = self.mecha_id
            if mecha_id is not None:
                from logic.gutils import mecha_utils
                btn_drag_base_val_spec = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_MAIN_WEAPON_STICK_MECHA_VAL_KEY)
                btn_rocker_as_screen = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY)
                if self.on_aim and self.scope_main_weapon_sensitivity_opened:
                    if not mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCOPE_SAME_AS_NORMAL_KEY):
                        btn_drag_base_val_spec = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCOPE_MAIN_WEAPON_STICK_MECHA_VAL_KEY)
                        btn_rocker_as_screen = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCOPE_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY)
                elif self.mecha and self.mecha.sd.ref_use_mecha_special_form_sensitivity and self.special_form_main_weapon_sensitivity_opened:
                    if not mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SPECIAL_FORM_SAME_AS_NORMAL_KEY):
                        btn_drag_base_val_spec = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SPECIAL_FORM_MAIN_WEAPON_STICK_MECHA_VAL_KEY)
                        btn_rocker_as_screen = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SPECIAL_FORM_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY)
            else:
                btn_drag_base_val_spec = None
                btn_rocker_as_screen = False
            btn.set_drag_base_val_specific(btn_drag_base_val_spec)
            btn.set_rocker_as_screen(btn_rocker_as_screen)
            return

    def _check_sub_weapon_rocker_sens(self):
        btn = self._get_action_btn('action4')
        if btn is None:
            return
        else:
            mecha_id = self.mecha_id
            if mecha_id is not None:
                from logic.gutils import mecha_utils
                btn_drag_base_val_spec = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SUB_WEAPON_STICK_MECHA_VAL_KEY)
                btn_rocker_as_screen = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SUB_WEAPON_ROCKER_AS_SCREEN_KEY)
                if self.on_aim and self.scope_sub_weapon_sensitivity_opened:
                    if not mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCOPE_SAME_AS_NORMAL_KEY):
                        btn_drag_base_val_spec = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCOPE_SUB_WEAPON_STICK_MECHA_VAL_KEY)
                        btn_rocker_as_screen = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCOPE_SUB_WEAPON_ROCKER_AS_SCREEN_KEY)
                elif self.mecha and self.mecha.sd.ref_use_mecha_special_form_sensitivity and self.special_form_sub_weapon_sensitivity_opened:
                    if not mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SPECIAL_FORM_SAME_AS_NORMAL_KEY):
                        btn_drag_base_val_spec = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SPECIAL_FORM_SUB_WEAPON_STICK_MECHA_VAL_KEY)
                        btn_rocker_as_screen = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SPECIAL_FORM_SUB_WEAPON_ROCKER_AS_SCREEN_KEY)
            else:
                btn_drag_base_val_spec = None
                btn_rocker_as_screen = False
            btn.set_drag_base_val_specific(btn_drag_base_val_spec)
            btn.set_rocker_as_screen(btn_rocker_as_screen)
            return

    def _enable_weapon_rocker_drag(self, action_id, enable):
        if enable:
            action_id in self._forbidden_draggable_btn and self._forbidden_draggable_btn.remove(action_id)
        else:
            self._forbidden_draggable_btn.add(action_id)
        self.refresh_forbidden_draggable_btn({action_id}, enable)

    def set_weapon_rocker_draggable(self, main_weapon_rocker_draggable, sub_weapon_rocker_draggable):
        self._enable_weapon_rocker_drag('action1', main_weapon_rocker_draggable)
        self._enable_weapon_rocker_drag('action4', sub_weapon_rocker_draggable)

    def on_weapon_rocker_draggable_change(self, val):
        self._check_weapon_rocker_draggable()

    def _on_mecha_sens_val_changed(self, mecha_id, val_key):
        if self.mecha_id != mecha_id:
            return
        else:
            if val_key is None or val_key in (
             uoc.SST_SHOOT_STICK_SWITCH_MECHA_VAL_KEY, uoc.SST_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY, uoc.SST_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY,
             uoc.SST_SCOPE_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY, uoc.SST_SCOPE_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY, uoc.SST_SCOPE_SAME_AS_NORMAL_KEY,
             uoc.SST_SPECIAL_FORM_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY, uoc.SST_SPECIAL_FORM_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY, uoc.SST_SPECIAL_FORM_SAME_AS_NORMAL_KEY):
                self._check_weapon_rocker_draggable()
            if val_key is None or val_key in (
             uoc.SST_MAIN_WEAPON_STICK_MECHA_VAL_KEY, uoc.SST_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY,
             uoc.SST_SCOPE_MAIN_WEAPON_STICK_MECHA_VAL_KEY, uoc.SST_SCOPE_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY, uoc.SST_SCOPE_SAME_AS_NORMAL_KEY,
             uoc.SST_SPECIAL_FORM_MAIN_WEAPON_STICK_MECHA_VAL_KEY, uoc.SST_SPECIAL_FORM_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY, uoc.SST_SPECIAL_FORM_SAME_AS_NORMAL_KEY):
                self._check_main_weapon_rocker_sens()
            if val_key is None or val_key in (
             uoc.SST_SUB_WEAPON_STICK_MECHA_VAL_KEY, uoc.SST_SUB_WEAPON_ROCKER_AS_SCREEN_KEY,
             uoc.SST_SCOPE_SUB_WEAPON_STICK_MECHA_VAL_KEY, uoc.SST_SCOPE_SUB_WEAPON_ROCKER_AS_SCREEN_KEY, uoc.SST_SCOPE_SAME_AS_NORMAL_KEY,
             uoc.SST_SPECIAL_FORM_SUB_WEAPON_STICK_MECHA_VAL_KEY, uoc.SST_SPECIAL_FORM_SUB_WEAPON_ROCKER_AS_SCREEN_KEY, uoc.SST_SPECIAL_FORM_SAME_AS_NORMAL_KEY):
                self._check_sub_weapon_rocker_sens()
            return

    def refresh_forbidden_draggable_btn(self, btns, enable):
        for act_id in btns:
            if act_id in self.action_btns:
                action_btn = self.action_btns[act_id]
                self.on_set_action_rocker(act_id, enable, action_btn.use_drag_helper)

    def on_camera_switch_to_state(self, state, *args):
        self.on_aim = state == AIM_MODE
        if not global_data.is_pc_mode:
            self.set_left_fire_ope()

    def on_change_ui_custom_data(self):
        if self.enable_trace:
            UIDistorterHelper().apply_node_distort('MECHA_BUTTON', self.panel.action1, self.panel, '%s-action1' % self.__class__.__name__)
        elif self.mecha:
            if self.mecha.__class__.__name__ != 'LMechaTrans':
                UIDistorterHelper().apply_ui_distort(self.__class__.__name__)
        self.refresh_all_copy_node()
        for action_btn in six_ex.values(self.action_btns):
            action_btn.refresh_rocker()

        ui = global_data.ui_mgr.get_ui('GuideUI')
        if ui:
            param = self.change_ui_data()
            ui.on_change_ui_inform_guide_mixed(param)

    def change_ui_data(self):
        scale_type_adjust_list = []
        pos_type_adjust_list = []
        need_to_adjust_scale_type_nodes = (
         ('nd_action_custom_1', 'nd_step_16', None), ('nd_action_custom_4', 'nd_step_17', None),
         ('nd_action_custom_6', 'nd_move_skill', None), ('nd_action_custom_1', 'nd_step_3', None),
         ('nd_action_custom_7', 'nd_skill_tips', None))
        for source_nd_name, target_nd_name, target_scale_nd_name in need_to_adjust_scale_type_nodes:
            nd = getattr(self.panel, source_nd_name)
            w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
            scale = nd.getScale()
            scale_type_adjust_list.append((w_pos, scale, target_nd_name, target_scale_nd_name))

        ret_dict = {'scale_type': scale_type_adjust_list,
           'pos_type': pos_type_adjust_list
           }
        return ret_dict

    def _on_pc_hotkey_hint_display_option_changed(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), now, pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_switch_toggled(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(now, pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    PC_KEY_HINT_RELEATED_UI_NAMES = ('nd_action_custom_5', 'nd_action_custom_8')

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

    def on_hot_key_state_opened(self):
        self.check_hot_key_shoot_buttons_show()
        self.refresh_temp_pc_show()
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def on_hot_key_state_closed(self):
        self.panel.nd_action_custom_1.setVisible(True)
        self.panel.nd_action_custom_1.temp_pc.setVisible(False)
        self.panel.nd_action_custom_2.setVisible(True)
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def check_hot_key_shoot_buttons_show(self):
        if not global_data.is_pc_control_enable:
            return
        self.panel.nd_action_custom_1.setVisible(False)
        if self.mecha and self.mecha.ev_g_shape_id() == '8012' and self.mecha.sd.ref_is_ball_mode:
            self.panel.nd_action_custom_1.setVisible(True)
        self.panel.nd_action_custom_2.setVisible(False)

    def on_trans_to_ball(self, *args):
        self.check_hot_key_shoot_buttons_show()

    def on_trans_to_human(self, *args):
        self.check_hot_key_shoot_buttons_show()

    def keyboard_use_special_skill(self, msg, keycode):
        from logic.vscene.parts.ctrl import InputMockHelper
        if self.panel.nd_rot.nd_special and self.panel.nd_rot.nd_special.isVisible():
            btn = getattr(self.panel.nd_rot.nd_special, 'btn')
            if btn:
                if msg in [game.MSG_KEY_DOWN, game.MSG_MOUSE_DOWN]:
                    btn.OnBegin(InputMockHelper.TouchMock())
                else:
                    t = InputMockHelper.TouchMock()
                    btn.OnEnd(t)
                    btn.OnClick(t)

    def _get_action_btn(self, act_id):
        return self.action_btns.get(act_id, None)

    def on_resolution_changed(self):
        self.on_change_ui_custom_data()

    def check_copy_func(self, nd, act_id, st_id, action_config):
        btn = ControlBtn(nd, act_id, st_id, action_config)
        if global_data.is_pc_mode or not self.enable_copy_action:
            return btn
        else:
            cCopyNodeId = confmgr.get('c_action_copy_node_conf', str(act_id), 'cCopyNodeId', default=None)
            if self.custom_ui_com:
                conf = self.custom_ui_com.get_conf_by_node_id(cCopyNodeId)
                if conf:
                    node_conf = confmgr.get('c_panel_node_custom_conf', str(cCopyNodeId))
                    nd_name = node_conf['cAdjustNode'] or node_conf['cNodeName']
                    hang_one = getattr(self.panel.nd_copy, nd_name)
                    for child in hang_one.GetChildren():
                        child.Destroy()

                    for child in nd.GetParent().GetChildren():
                        new_node = child.CreateCopy(hang_one, name=child.GetName())

                    widget = global_data.uisystem.re_create_item(getattr(hang_one, str(act_id)), root=None, tmp_path=nd.GetTemplatePath())
                    btn_with_copy = ControlBtnWithCopyFunc(btn)
                    btn_with_copy.set_copy_nd(getattr(getattr(self.panel.nd_copy, nd_name), act_id))
                    btn_with_copy.set_copy_nd_vis(False)
                    return btn_with_copy
            return btn

    def refresh_all_copy_node(self):
        if global_data.is_pc_mode:
            return
        else:
            if not self.custom_ui_com:
                return
            for action_id in list(six_ex.keys(self.action_btns)):
                control_btn = self.action_btns[action_id]
                cCopyNodeId = confmgr.get('c_action_copy_node_conf', str(action_id), 'cCopyNodeId', default=None)
                conf = self.custom_ui_com.get_conf_by_node_id(cCopyNodeId)
                need_show_copy_node = self.enable_copy_action and conf
                if type(control_btn) == ControlBtnWithCopyFunc:
                    if need_show_copy_node:
                        control_btn.set_copy_nd_vis(action_id in self.visible_btns)
                    else:
                        control_btn.set_copy_nd_vis(False)
                elif need_show_copy_node:
                    self.destroy_single_action_btn(action_id)
                    self.init_action_btn(action_id, False)
                    if self.mecha:
                        self.action_btns[action_id].bind_events(self.mecha)

            return

    def hide_all_copy_nd(self):
        if global_data.is_pc_mode:
            return
        else:
            for act_id in ALL_ACTIONS:
                cCopyNodeId = confmgr.get('c_action_copy_node_conf', str(act_id), 'cCopyNodeId', default=None)
                node_conf = confmgr.get('c_panel_node_custom_conf', str(cCopyNodeId))
                nd_name = node_conf['cAdjustNode'] or node_conf['cNodeName']
                hang_one = getattr(self.panel.nd_copy, nd_name)
                if hang_one:
                    nd = getattr(hang_one, act_id)
                    if nd:
                        nd.setVisible(False)
                        parent = nd.GetParent()
                        nd_temp_pc = getattr(parent, 'temp_pc')
                        if nd_temp_pc:
                            nd_temp_pc.setVisible(False)

            return

    def on_disable_second_weapon(self, disabled):
        self.second_weapon_disabled = disabled
        for action_id, btn in six.iteritems(self.action_btns):
            is_second_weapon = action_id in ('action4', )
            btn.setForbidden(is_second_weapon and disabled, 'disable_second_weapon_by_buff')