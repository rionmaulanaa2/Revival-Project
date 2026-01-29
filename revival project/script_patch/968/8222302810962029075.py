# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/BattleControlUIPC.py
from __future__ import absolute_import
import six_ex
import six
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
from logic.gutils import rocker_utils
import logic.gcommon.const as g_const
from logic.gcommon.common_const import collision_const
import collision
import math
import cc
from logic.gcommon.common_const.skill_const import SKILL_ROLL, SKILL_MECHATRANS_RUSH, SKILL_AIR_JUMP, SKILL_MOTORCYCLE_RUSH
from logic.client.const import pc_const
from logic.gutils import pc_utils
from common.const import uiconst
from logic.gutils.climb_utils import check_climb
from common.cfg import confmgr
from logic.gcommon.cdata.status_config import ST_USE_ITEM, ST_SKATE_MOVE, ST_SKATE, ST_JUMP_1
from common.uisys.uielment.CCSprite import CCSprite
from data import hot_key_def
from logic.gcommon.common_const import skill_const as sconst
from logic.gcommon.common_const import mecha_const as mconst
import common.utils.timer as timer
from logic.client.const import game_mode_const
PROGRESS_BAR_LIST = {3: 'battle/i_progress_pc',
   4: 'battle/i_progress2_pc',
   2: 'battle/i_progress3_pc'
   }
TYPE_PLAYER = 0
TYPE_CONTROL_TARGET = 1

class ActionBtnBase(object):
    GLOBAL_EVENT = {}

    def process_global_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        for event, func_name in six.iteritems(self.GLOBAL_EVENT):
            func = getattr(self, func_name)
            if func and callable(func):
                econf[event] = func

        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def __init__(self, nd, action_id, state_id, action_info):
        self.nd = nd
        self.action_id = action_id
        self.action_info = action_info
        self.bind_state_id = state_id
        self.process_global_event(True)
        icon = action_info.get('action_icon', {}).get(action_id, None)
        if icon and isinstance(self.nd.icon_skill, CCSprite):
            self.nd.icon_skill.SetDisplayFrameByPath('', icon)
        self.switch_hot_key_show(True)
        text_id = action_info.get('action_text', {}).get(action_id, None)
        if text_id:
            self.nd.lab_skill.SetString(text_id)
            self.nd.lab_skill.setVisible(True)
        self.bind_skill_id = action_info.get('action_skill', {}).get(action_id, None)
        self.ltarget = None
        self.progress_bar = None
        self.progress_bar_elem = []
        return

    def check_skill(self):
        action_info = self.action_info
        action_id = self.action_id
        skill_id = action_info.get('action_skill', {}).get(action_id, None)
        if skill_id and self.ltarget:
            self.uinit_progress_event()
            self.init_skill_btn(self.ltarget, skill_id)
        return

    def switch_hot_key_show(self, is_show):
        if is_show:
            hot_key_func_name = self.action_info.get('action_hotkey', {}).get(self.action_id, None)
            if hot_key_func_name:
                self.nd.temp_pc.setVisible(True)
            else:
                self.nd.temp_pc.setVisible(False)
            from logic.gutils.hot_key_utils import get_hot_key_short_display_name_ex, set_hot_key_common_tip
            set_hot_key_common_tip(self.nd.temp_pc, hot_key_func_name)
        else:
            self.nd.temp_pc.setVisible(False)
        return

    def refresh_hot_key_label(self):
        hot_key_func_name = self.action_info.get('action_hotkey', {}).get(self.action_id, None)
        from logic.gutils.hot_key_utils import get_hot_key_short_display_name_ex, set_hot_key_common_tip
        set_hot_key_common_tip(self.nd.temp_pc, hot_key_func_name)
        return

    def init(self):
        pass

    def destroy(self):
        if self.progress_bar:
            self.progress_bar.Destroy(True)
            self.progress_bar = None
        self.uinit_progress_event()
        self.ltarget = None
        self.progress_bar_elem = []
        self.nd = None
        self.process_global_event(False)
        return

    def get_is_action_enable(self):
        return True

    def enable_action(self):
        global_data.emgr.posture_ui_action_enable_event.emit(self.action_id, True)

    def disable_action(self):
        global_data.emgr.posture_ui_action_enable_event.emit(self.action_id, False)

    def on_player_setted(self, lplayer):
        new_ltarget = None
        target_type = self.action_info.get('target_type', {}).get(self.action_id, TYPE_PLAYER)
        if target_type == TYPE_PLAYER:
            new_ltarget = lplayer
        elif lplayer:
            control_target = lplayer.ev_g_control_target()
            new_ltarget = control_target.logic if control_target else None
        if self.ltarget != new_ltarget:
            if self.ltarget and self.ltarget.is_valid():
                self.uinit_progress_event()
            self.ltarget = new_ltarget
            if self.ltarget:
                self.check_skill()
        return

    def on_control_target_setted(self, lplayer):
        target_type = self.action_info.get('target_type', {}).get(self.action_id, TYPE_PLAYER)
        if target_type == TYPE_CONTROL_TARGET:
            self.on_player_setted(lplayer)

    def init_skill_btn(self, ltarget, skill_id):
        if not ltarget.ev_g_skill(skill_id):
            return
        no_progress_btn = self.action_info.get('no_progress_btn', [])
        if self.action_id in no_progress_btn:
            return
        percent = ltarget.ev_g_energy(skill_id)
        recover = ltarget.ev_g_energy_recover(skill_id)
        cost = ltarget.ev_g_energy_cost(skill_id)
        skill_conf = confmgr.get('skill_conf', str(skill_id))
        cd_type = skill_conf.get('cd_type', mconst.CD_TYPE_COUNTDOWN)
        if cd_type == mconst.CD_TYPE_PROGRESS:
            self.setup_progress_display(ltarget, skill_id)
        self.recover = recover
        self.cost = cost
        nd_useless = self.nd.nd_useless

        def on_energy_change(key, p):
            if key != skill_id:
                return
            if cd_type == mconst.CD_TYPE_PROGRESS:
                self.show_progress(p, self.cost)
            else:
                self.show_count_down(nd_useless, p, self.recover)

        def on_skill_attr_update(update_skill_id, *args):
            if skill_id != update_skill_id:
                return
            if self.ltarget and self.ltarget.is_valid():
                if cd_type == mconst.CD_TYPE_PROGRESS:
                    self.setup_progress_display(self.ltarget, skill_id)
                    self.cost = self.ltarget.ev_g_energy_cost(skill_id)
                else:
                    self.recover = self.ltarget.ev_g_energy_recover(skill_id)

        on_energy_change(skill_id, percent)
        self.on_energy_change = on_energy_change
        self.on_skill_attr_update = on_skill_attr_update
        regist_func = self.ltarget.regist_event
        regist_func('E_ENERGY_CHANGE', self.on_energy_change)
        regist_func('E_UPDATE_SKILL_ATTR', self.on_skill_attr_update)

    def setup_progress_display(self, lentity, skill_id):
        skill_conf = confmgr.get('skill_conf', str(skill_id))
        bar_number = lentity.ev_g_energy_segment(skill_id)
        bar_number = bar_number if skill_conf['cost_mp_type'] == sconst.MP_COST_PER_TIMES else 1
        if self.progress_bar and self.progress_bar.bar_number == bar_number:
            return
        else:
            if self.progress_bar:
                self.progress_bar.Destroy(True)
                self.progress_bar = None
            if bar_number not in PROGRESS_BAR_LIST:
                return
            progress_temp = PROGRESS_BAR_LIST[bar_number]
            self.progress_bar = global_data.uisystem.load_template_create(progress_temp, self.nd.nd_progress)
            self.progress_bar.bar_number = bar_number
            if bar_number > 1:
                self.progress_bar_elem = [ getattr(self.progress_bar, 'img_use{0}'.format(i)) for i in range(1, bar_number + 1) ]
            return

    def show_progress(self, percent, cost):
        if percent < 0:
            percent = 0 if 1 else percent
            return self.progress_bar or None
        nd_progress, bar_number = self.progress_bar, self.progress_bar.bar_number
        if bar_number > 1:
            cur_visible_bar = int(percent / cost)
            bar_len = len(self.progress_bar_elem)
            for idx in range(cur_visible_bar):
                if idx >= bar_len:
                    break
                self.progress_bar_elem[idx].setVisible(True)

            for idx in range(cur_visible_bar, bar_number):
                if idx >= bar_len:
                    break
                self.progress_bar_elem[idx].setVisible(False)

        else:
            nd_progress.img_progress_full.setVisible(percent >= 1.0)
        last_progress = nd_progress.progress.getPercentage()
        now_progress = percent * 100
        nd_progress.progress.SetPercentage(now_progress)
        if percent >= 1.0 and last_progress != now_progress:
            self.nd.PlayAnimation(self.get_enable_ani_name())

    def show_count_down(self, nd_cd, percent, recover_rate):
        label, progress = nd_cd.lab_cd_time, nd_cd.progress_cd
        nd_cd.setVisible(percent < 1 and percent != 0)
        left_time = (1 - percent) / recover_rate
        last_progress = progress.getPercentage()
        now_progress = (1 - percent) * 100
        progress.SetPercentage(now_progress)
        if left_time <= 0:
            left_time = 0
            if last_progress != now_progress:
                self.nd.PlayAnimation(self.get_enable_ani_name())
        label.SetString('%.1f' % left_time, 1)

    def get_enable_ani_name(self):
        return self.action_info.get(self.action_id, {}).get('action_ani', {}).get('enbale_ani', 'enable')

    def uinit_progress_event--- This code section failed: ---

 259       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'ltarget'
           6  POP_JUMP_IF_TRUE     13  'to 13'

 260       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

 261      13  LOAD_FAST             0  'self'
          16  LOAD_ATTR             0  'ltarget'
          19  LOAD_ATTR             1  'unregist_event'
          22  STORE_FAST            1  'unregist_func'

 262      25  LOAD_GLOBAL           2  'hasattr'
          28  LOAD_GLOBAL           1  'unregist_event'
          31  CALL_FUNCTION_2       2 
          34  POP_JUMP_IF_FALSE    74  'to 74'
          37  LOAD_FAST             0  'self'
          40  LOAD_ATTR             3  'on_energy_change'
        43_0  COME_FROM                '34'
          43  POP_JUMP_IF_FALSE    74  'to 74'

 263      46  LOAD_FAST             1  'unregist_func'
          49  LOAD_CONST            2  'E_ENERGY_CHANGE'
          52  LOAD_FAST             0  'self'
          55  LOAD_ATTR             3  'on_energy_change'
          58  CALL_FUNCTION_2       2 
          61  POP_TOP          

 264      62  LOAD_CONST            0  ''
          65  LOAD_FAST             0  'self'
          68  STORE_ATTR            3  'on_energy_change'
          71  JUMP_FORWARD          0  'to 74'
        74_0  COME_FROM                '71'

 265      74  LOAD_GLOBAL           2  'hasattr'
          77  LOAD_GLOBAL           3  'on_energy_change'
          80  CALL_FUNCTION_2       2 
          83  POP_JUMP_IF_FALSE   123  'to 123'
          86  LOAD_FAST             0  'self'
          89  LOAD_ATTR             5  'on_skill_attr_update'
        92_0  COME_FROM                '83'
          92  POP_JUMP_IF_FALSE   123  'to 123'

 266      95  LOAD_FAST             1  'unregist_func'
          98  LOAD_CONST            4  'E_UPDATE_SKILL_ATTR'
         101  LOAD_FAST             0  'self'
         104  LOAD_ATTR             5  'on_skill_attr_update'
         107  CALL_FUNCTION_2       2 
         110  POP_TOP          

 267     111  LOAD_CONST            0  ''
         114  LOAD_FAST             0  'self'
         117  STORE_ATTR            5  'on_skill_attr_update'
         120  JUMP_FORWARD          0  'to 123'
       123_0  COME_FROM                '120'
         123  LOAD_CONST            0  ''
         126  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 31

    def on_add_skill(self, skill_id, skill_data=None):
        if self.bind_skill_id == skill_id:
            self.check_skill()


class ChangeWeaponActionBtn(ActionBtnBase):
    GLOBAL_EVENT = {'on_wpbar_switch_cur_event': 'on_weapon_in_hand_changed',
       'on_weapon_mode_switched': '_on_weapon_mode_switched'
       }

    def init(self):
        super(ChangeWeaponActionBtn, self).init()

        @self.nd.callback()
        def OnClick(btn, touch):
            self._on_click_change_mode_btn()

        self._update_change_mode_ui()

    def get_is_action_enable(self):
        cur_weapon = global_data.player.logic.share_data.ref_wp_bar_cur_weapon
        if cur_weapon and cur_weapon.is_multi_wp():
            return True
        else:
            return False

    def on_weapon_in_hand_changed(self, *args):
        if not (global_data.player and global_data.player.logic):
            return
        self._update_change_mode_ui()

    def _on_click_change_mode_btn(self, *args):
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_SWITCH_WEAPON_MODE')

    def _update_change_mode_ui(self):
        if not (global_data.player and global_data.player.logic):
            return
        cur_weapon = global_data.player.logic.share_data.ref_wp_bar_cur_weapon
        if cur_weapon and cur_weapon.is_multi_wp():
            self.enable_action()
            self._update_mode_btn_pic(cur_weapon)
        else:
            self.disable_action()

    def _on_weapon_mode_switched(self, *args):
        cur_weapon = global_data.player.logic.share_data.ref_wp_bar_cur_weapon
        if cur_weapon and cur_weapon.is_multi_wp():
            self._update_mode_btn_pic(cur_weapon)

    def _update_mode_btn_pic(self, weapon):
        wp_id = weapon.get_item_id()
        mode_pic = confmgr.get('firearm_res_config', str(wp_id), 'cModeBtnPic')
        if mode_pic:
            self.nd.icon_skill.SetDisplayFrameByPath('', mode_pic)


class LeaveSkateBoardActionBtn(ActionBtnBase):

    def init(self):
        super(LeaveSkateBoardActionBtn, self).init()

        @self.nd.btn_skill.callback()
        def OnClick(btn, touch):
            self.on_click_get_off_btn(btn, touch)

    def on_click_get_off_btn(self, btn, touch):
        from logic.gcommon.cdata.status_config import ST_USE_ITEM, ST_SKATE_MOVE, ST_SKATE, ST_JUMP_1
        if global_data.player and global_data.player.logic:
            lplayer = global_data.player.logic
            if lplayer.ev_g_get_state(ST_JUMP_1):
                return
            lplayer.send_event('E_LEAVE_ATTACHABLE_ENTITY')


class HumanRollActionBtn(ActionBtnBase):
    GLOBAL_EVENT = {'on_player_unequip_rush_bone_event': 'check_roll_btn_appearance',
       'on_player_equip_rush_bone_event': 'check_roll_btn_appearance'
       }

    def get_is_action_enable(self):
        if global_data.player and global_data.player.logic:
            return global_data.player.logic.ev_g_skill(SKILL_ROLL)
        return False

    def init(self):
        super(HumanRollActionBtn, self).init()
        self.check_roll_btn_appearance()

        @self.nd.btn_skill.callback()
        def OnClick(btn, touch):
            self.on_roll_clicked(btn, touch)

    def check_roll_btn_appearance(self, *args):
        from logic.gcommon.const import ROLL_NORMAL_PATH, ROLL_SEL_PATH, BONE_RUSH_NORMAL_PATH, BONE_RUSH_SEL_PATH
        if self.ltarget and self.ltarget.is_valid():
            if self.ltarget.ev_g_is_equip_rush_bone():
                self.nd.icon_skill.SetDisplayFrameByPath('', BONE_RUSH_NORMAL_PATH)
            else:
                self.nd.icon_skill.SetDisplayFrameByPath('', ROLL_NORMAL_PATH)

    def on_roll_clicked(self, *args):
        if not global_data.player:
            return
        player = global_data.player.logic
        if not player:
            return
        if not player.ev_g_can_cast_skill(SKILL_ROLL):
            return
        if not player.ev_g_is_equip_rush_bone():
            if not player.ev_g_status_check_pass(status_config.ST_ROLL):
                return
            player.send_event('E_CTRL_ROLL')
        else:
            player.send_event('E_CTRL_RUSH')


class HumanJumpActionBtn(ActionBtnBase):
    GLOBAL_EVENT = {'on_player_add_jump_max_stage_event': 'check_jump_btn_appearance'
       }

    def get_is_action_enable(self):
        if global_data.player and global_data.player.logic:
            return global_data.player.logic.ev_g_skill(SKILL_AIR_JUMP) and global_data.player.logic.ev_g_jump_max_stage() > 1
        return False

    def init(self):
        super(HumanJumpActionBtn, self).init()

        @self.nd.btn_skill.callback()
        def OnClick(btn, touch):
            self.on_jump_clicked(btn, touch)

        self.check_jump_btn_appearance()

    def check_jump_btn_appearance(self, *args):
        from logic.gcommon.const import BONE_JUMP_PATHS
        if self.ltarget and self.ltarget.is_valid():
            max_stage = self.ltarget.ev_g_jump_max_stage()
            if max_stage not in BONE_JUMP_PATHS:
                max_stage = 1
            path_list = BONE_JUMP_PATHS.get(max_stage, [])
            if path_list:
                self.nd.icon_skill.SetDisplayFrameByPath('', path_list[0])
            self.reset_air_jump_cost()

    def reset_air_jump_cost(self, *args):
        if not self.ltarget:
            return
        if self.ltarget.ev_g_jump_max_stage() == 1:
            self.disable_action()
            return

    def on_jump_clicked(self, *args):
        if not global_data.player:
            return
        player = global_data.player.logic
        if not player:
            return
        if not player.ev_g_can_cast_skill(SKILL_AIR_JUMP):
            return
        from logic.gutils.climb_utils import on_begin_jump_btn_exc
        on_begin_jump_btn_exc()


class CarTransform(ActionBtnBase):

    def get_is_action_enable(self):
        if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_in_mecha('MechaTrans'):
            return True

    def init(self):
        super(CarTransform, self).init()

        @self.nd.btn_skill.callback()
        def OnClick(btn, touch):
            self.use_car_transform()

    def use_car_transform(self):
        from logic.gutils.hot_key_utils import use_car_transform
        use_car_transform(None, None)
        return


class CarRush(ActionBtnBase):
    GLOBAL_EVENT = {'mecha_trans_pattern_handle_event': 'check_mecha_trans_pattern'
       }

    def get_is_action_enable(self):
        if not (global_data.player and global_data.player.logic):
            return False
        if global_data.player.logic.ev_g_in_mecha('Motorcycle'):
            return True
        control_target = global_data.player.logic.ev_g_control_target()
        if control_target and control_target.logic:
            pattern = control_target.logic.ev_g_pattern()
            if pattern == mconst.MECHA_TYPE_VEHICLE:
                return True
        return False

    def check_mecha_trans_pattern(self, pattern, *args, **kwargs):
        if self.get_is_action_enable():
            self.enable_action()
        else:
            self.disable_action()

    def init(self):
        super(CarRush, self).init()

        @self.nd.btn_skill.callback()
        def OnClick(btn, touch):
            self.use_car_rush()

    def use_car_rush(self):
        from logic.gutils.hot_key_utils import use_car_rush
        use_car_rush(None, None)
        return


class MotorcycleRush(ActionBtnBase):
    GLOBAL_EVENT = {'mecha_trans_pattern_handle_event': 'check_mecha_trans_pattern'
       }

    def get_is_action_enable(self):
        if not (global_data.player and global_data.player.logic):
            return False
        if not global_data.player.logic.ev_g_in_mecha('Motorcycle'):
            return False
        control_target = global_data.player.logic.ev_g_control_target()
        if control_target and control_target.logic:
            if control_target.logic.sd.ref_avatar_seat_idx == 0:
                return True
        return False

    def check_mecha_trans_pattern(self, pattern, *args, **kwargs):
        if self.get_is_action_enable():
            self.enable_action()
        else:
            self.disable_action()

    def init(self):
        super(MotorcycleRush, self).init()

        @self.nd.btn_skill.callback()
        def OnClick(btn, touch):
            self.use_car_rush()

    def use_car_rush(self):
        from logic.gutils.hot_key_utils import use_car_rush
        use_car_rush(None, None)
        return


class CarOff(ActionBtnBase):

    def get_is_action_enable(self):
        if global_data.player and global_data.player.logic and (global_data.player.logic.ev_g_in_mecha('MechaTrans') or global_data.player.logic.ev_g_in_mecha('Motorcycle')):
            return True

    def init(self):
        super(CarOff, self).init()

        @self.nd.btn_skill.callback()
        def OnClick(btn, touch):
            self.get_off_vehicle()

    def get_off_vehicle(self):
        from logic.gutils.hot_key_utils import get_off_vehicle_or_skateboard
        get_off_vehicle_or_skateboard(None, None)
        return


class SwitchSeat(ActionBtnBase):

    def get_is_action_enable(self):
        if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_in_mecha('Motorcycle'):
            return True

    def init(self):
        super(SwitchSeat, self).init()

        @self.nd.btn_skill.callback()
        def OnClick(btn, touch):
            self.switch_seat()

    def switch_seat(self):
        from logic.gutils.hot_key_utils import on_switch_seat
        on_switch_seat()


class Reload(ActionBtnBase):

    def get_is_action_enable(self):
        if not (global_data.player and global_data.player.logic):
            return False
        if not global_data.player.logic.ev_g_in_mecha('Motorcycle'):
            return False
        control_target = global_data.player.logic.ev_g_control_target()
        if control_target and control_target.logic:
            if control_target.logic.sd.ref_avatar_seat_idx == 2:
                return False
        return True

    def init(self):
        super(Reload, self).init()

        @self.nd.btn_skill.callback()
        def OnClick(btn, touch):
            self.reload()

    def reload(self):
        from logic.gutils.hot_key_utils import on_reload
        on_reload()


class BattleControlUIPC(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_posture_pc'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    ENABLE_HOT_KEY_SUPPORT = True
    GLOBAL_EVENT = {'on_observer_enter_state_event': 'on_observer_enter_state',
       'on_leave_state_event': 'on_observer_leave_state',
       'posture_ui_action_enable_event': 'on_posture_ui_action_enable_changed',
       'switch_control_target_event': 'on_control_target_changed_event',
       'on_skill_init_complete_event': 'on_skill_init_complete',
       'on_add_skill_event': 'on_add_skill',
       'player_change_seat_event': 'on_player_change_seat',
       'on_remove_skill_event': 'on_remove_skill'
       }
    BUTTONS_CONF = {'action_icon': {'btn_roll': 'gui/ui_res_2/battle/icon/icon_roll_nml.png','btn_skate_off': 'gui/ui_res_2/battle/icon/icon_skateboard_off.png',
                       'btn_jump': 'gui/ui_res_2/battle/icon/jump_2_nml.png',
                       'car_off': 'gui/ui_res_2/battle/icon/mech_out.png',
                       'car_rush': 'gui/ui_res_2/battle/drive/icon_vehical_speedup_nml.png',
                       'motorcycle_rush': 'gui/ui_res_2/battle/drive/icon_vehical_speedup_nml.png',
                       'car_transform': 'gui/ui_res_2/battle/drive/icon_vehical_change_nml.png',
                       'switch_seat': 'gui/ui_res_2/battle/drive/icon_vehical_change_nml.png',
                       'motorcycle_off': 'gui/ui_res_2/battle/icon/vehicle_out.png',
                       'reload': 'gui/ui_res_2/battle/icon/icon_reload_bullet.png'
                       },
       'action_text': {'btn_skate_off': 80415,
                       'car_off': 80379,
                       'car_transform': 80063,
                       'switch_seat': 18256,
                       'motorcycle_off': 80379,
                       'reload': 920527
                       },
       'action_widget': {'btn_roll': HumanRollActionBtn,
                         'btn_skate_off': LeaveSkateBoardActionBtn,
                         'btn_jump': HumanJumpActionBtn,
                         'btn_change_weapon': ChangeWeaponActionBtn,
                         'car_transform': CarTransform,
                         'car_rush': CarRush,
                         'motorcycle_rush': MotorcycleRush,
                         'car_off': CarOff,
                         'motorcycle_off': CarOff,
                         'switch_seat': SwitchSeat,
                         'reload': Reload
                         },
       'action_hotkey': {'btn_skate_off': hot_key_def.GET_OFF_SKATEBOARD_OR_VEHICLE,'btn_change_weapon': hot_key_def.SWITCH_GUN_MODE,
                         'btn_jump': hot_key_def.HUMAN_JUMP,
                         'btn_roll': hot_key_def.HUMAN_ROLL,
                         'car_transform': hot_key_def.CAR_TRANSFORM,
                         'car_rush': hot_key_def.CAR_RUSH,
                         'motorcycle_rush': hot_key_def.CAR_RUSH,
                         'car_off': hot_key_def.GET_OFF_SKATEBOARD_OR_VEHICLE,
                         'motorcycle_off': hot_key_def.GET_OFF_SKATEBOARD_OR_VEHICLE,
                         'switch_seat': hot_key_def.SWITCH_SEAT,
                         'reload': hot_key_def.RELOAD
                         },
       'action_skill': {'btn_roll': SKILL_ROLL,
                        'car_rush': SKILL_MECHATRANS_RUSH,
                        'motorcycle_rush': SKILL_MOTORCYCLE_RUSH,
                        'btn_jump': SKILL_AIR_JUMP
                        },
       'target_type': {'car_rush': TYPE_CONTROL_TARGET,
                       'motorcycle_rush': TYPE_CONTROL_TARGET
                       }
       }
    ACTION_BUTTON_LIST = [
     'btn_skate_off', 'btn_change_weapon', 'btn_roll', 'car_rush', 'motorcycle_rush', 'car_transform', 'car_off', 'btn_jump', 'switch_seat', 'motorcycle_off', 'reload']
    STATE_2_ACTION_BUTTON_DICT = {ST_SKATE: 'btn_skate_off'
       }
    LOGIC_CHECKING_ACTION_LIST = [
     'btn_change_weapon', 'btn_roll', 'btn_jump', 'car_off', 'car_rush', 'motorcycle_rush', 'car_transform', 'switch_seat', 'motorcycle_off', 'reload']

    def on_init_panel(self, *args, **kwargs):
        self._action_widget_dict = {}
        self._action_show_list = []
        self._action_priority_dict = {}
        self._action_nd_dict = {}
        self._is_inited = False
        self._valid_show_list = []
        self._lplayer = None
        self._accumulate_timer = None
        for idx, action_name in enumerate(self.ACTION_BUTTON_LIST):
            self._action_priority_dict[action_name] = idx

        if global_data.player and global_data.player.logic:
            self.init_action_list(global_data.player.logic)
        self.process_events(True)
        return

    def on_finalize_panel(self):
        self.process_events(False)
        for action_id, action_widget in six.iteritems(self._action_widget_dict):
            if action_widget:
                action_widget.destroy()

        self._action_widget_dict = {}
        self._action_show_list = []
        self._action_priority_dict = {}
        self._action_nd_dict = {}
        if self._accumulate_timer:
            global_data.game_mgr.unregister_logic_timer(self._accumulate_timer)
        self._accumulate_timer = None
        return

    def process_events(self, is_bind=True):
        emgr = global_data.emgr
        econf = {'scene_player_setted_event': self.on_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def check_valid_show_list(self):
        if not (global_data.player and global_data.player.logic):
            return
        if not global_data.player.logic.ev_g_in_mecha():
            if global_data.player and global_data.player.logic.ev_g_get_state(ST_SKATE):
                self._valid_show_list = [
                 'btn_skate_off', 'btn_change_weapon']
            else:
                self._valid_show_list = [
                 'btn_roll', 'btn_change_weapon', 'btn_jump']
        elif global_data.player.logic.ev_g_in_mecha('MechaTrans'):
            self._valid_show_list = [
             'car_transform', 'car_rush', 'car_off']
        elif global_data.player.logic.ev_g_in_mecha('Motorcycle'):
            self._valid_show_list = [
             'motorcycle_rush', 'switch_seat', 'motorcycle_off', 'reload']
        else:
            self._valid_show_list = []

    def check_self_govern_widget(self):
        for idx, action_name in enumerate(self.LOGIC_CHECKING_ACTION_LIST):
            if action_name not in self._valid_show_list:
                continue
            if action_name in self._action_widget_dict:
                widget = self._action_widget_dict[action_name]
                if widget.get_is_action_enable():
                    self.show_action(action_name)
                else:
                    self.hide_action(action_name)

    def on_observer_enter_state(self, new_state):
        if new_state in self.STATE_2_ACTION_BUTTON_DICT:
            self.show_action(self.STATE_2_ACTION_BUTTON_DICT[new_state])
            self.check_valid_show_list()
            self.check_self_govern_widget()
            self.refresh_ui()

    def on_observer_leave_state(self, leave_state, new_st=None):
        if leave_state in self.STATE_2_ACTION_BUTTON_DICT:
            self.hide_action(self.STATE_2_ACTION_BUTTON_DICT[leave_state])
            self.check_valid_show_list()
            self.check_self_govern_widget()
            self.refresh_ui()

    def show_action(self, action_name):
        if action_name not in self._action_show_list:
            self._action_show_list.append(action_name)

    def hide_action(self, action_name):
        if action_name in self._action_show_list:
            self._action_show_list.remove(action_name)

    def on_posture_ui_action_enable_changed(self, action_name, enable):
        old_show_list = list(self._action_show_list)
        if enable:
            self.show_action(action_name)
        else:
            self.hide_action(action_name)
        if old_show_list != self._action_show_list:
            self.refresh_ui()

    def init_action_list(self, lplayer):
        if not lplayer:
            return
        else:
            for idx, action_name in enumerate(self.LOGIC_CHECKING_ACTION_LIST):
                if action_name not in self._action_widget_dict:
                    nd = self.create_action_node(action_name)
                    self._action_nd_dict[action_name] = nd
                    self.panel.ccb_skill.AddControl(nd, bRefresh=False)
                    self.panel.ccb_skill.RecycleItem(nd)
                    widget = self.create_action_widget(action_name, nd, None, self.BUTTONS_CONF)
                    widget.init()
                    self._action_widget_dict[action_name] = widget

            self._action_show_list = []
            for state, action_name in six.iteritems(self.STATE_2_ACTION_BUTTON_DICT):
                if lplayer.ev_g_is_in_any_state((state,)):
                    self._action_show_list.append(action_name)

            for action_name in self.LOGIC_CHECKING_ACTION_LIST:
                widget = self._action_widget_dict.get(action_name, None)
                if widget:
                    if widget.get_is_action_enable():
                        self._action_show_list.append(action_name)

            self.refresh_ui()
            self._is_inited = True
            return

    def sort_action_show_list(self):
        self._action_show_list = sorted(self._action_show_list, key=--- This code section failed: ---

 833       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  '_action_priority_dict'
           6  LOAD_ATTR             1  'get'
           9  LOAD_ATTR             1  'get'
          12  CALL_FUNCTION_2       2 
          15  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 12
)

    def refresh_ui(self):
        self.sort_action_show_list()
        self.panel.ccb_skill.RecycleAllItem()
        for action_name in self._action_show_list:
            if action_name not in self._valid_show_list:
                continue
            if action_name not in self._action_nd_dict:
                nd = self.create_action_node(action_name)
                self._action_nd_dict[action_name] = nd
                self.panel.ccb_skill.AddControl(nd, bRefresh=False)
            else:
                nd = self._action_nd_dict[action_name]
                if not self.panel.ccb_skill.ReuseItemByNode(nd, bRefresh=False):
                    log_error('reuse ccb_skill failed')
            if action_name not in self._action_widget_dict:
                state_id = self.STATE_2_ACTION_BUTTON_DICT.get(action_name, None)
                widget = self.create_action_widget(action_name, nd, state_id, self.BUTTONS_CONF)
                widget.init()
                self._action_widget_dict[action_name] = widget
                if not widget.get_is_action_enable():
                    self.panel.ccb_skill.RecycleItem(nd)

        self.panel.ccb_skill.RefreshItemPos()
        global_data.emgr.battle_control_ui_pc_refresh_event.emit()
        return

    def create_action_node(self, action_name):
        nd = global_data.uisystem.load_template_create('battle/i_fight_posture_pc_item')
        return nd

    def create_action_widget(self, action_name, nd, state, action_info):
        widget_class = self.BUTTONS_CONF['action_widget'].get(action_name)
        if widget_class:
            widget = widget_class(nd, action_name, state, action_info)
            if global_data.player and global_data.player.logic:
                widget.on_player_setted(global_data.player.logic)
            else:
                widget.on_player_setted(None)
            return widget
        else:
            return
            return

    def on_player_setted(self, lplayer):
        self.unbind_shot_event(self._lplayer)
        self._lplayer = lplayer
        if lplayer:
            self.bind_shot_event(lplayer)

    def on_control_target_changed_event(self, *args, **kwargs):
        self.panel.SetTimeOut(0.01, lambda : self.do_on_control_target_changed())

    def do_on_control_target_changed(self):
        if global_data.player and global_data.player.logic:
            for action_id, action_widget in six.iteritems(self._action_widget_dict):
                if action_widget:
                    action_widget.on_control_target_setted(global_data.player.logic)

        self.check_valid_show_list()
        self.check_self_govern_widget()
        self.refresh_ui()

    def on_skill_init_complete(self):
        if not (global_data.player and global_data.player.logic):
            return
        lplayer = global_data.player.logic
        if lplayer:
            if not self._is_inited:
                self.init_action_list(lplayer)
            for action_id, action_widget in six.iteritems(self._action_widget_dict):
                if action_widget:
                    action_widget.on_player_setted(lplayer)

        self.check_valid_show_list()
        self.check_self_govern_widget()
        self.refresh_ui()

    def on_add_skill(self, skill_id, ext_data=None):
        old_list = list(self._action_show_list)
        for action_id, action_widget in six.iteritems(self._action_widget_dict):
            if action_widget:
                action_widget.on_add_skill(skill_id)

        self.check_self_govern_widget()
        if old_list != self._action_show_list:
            self.refresh_ui()

    def on_player_change_seat(self):
        self.check_self_govern_widget()
        self.refresh_ui()

    def on_remove_skill(self, skill_id):
        old_list = list(self._action_show_list)
        self.check_self_govern_widget()
        if old_list != self._action_show_list:
            self.refresh_ui()

    def on_refresh_hot_key_imp(self):
        for action_id, action_widget in six.iteritems(self._action_widget_dict):
            if action_widget:
                action_widget.refresh_hot_key_label()

    def bind_shot_event(self, target):
        if target and target.is_valid():
            target.regist_event('E_LEAVE_STATE', self.on_leave_state)
            target.regist_event('E_CTRL_ACCUMULATE', self.on_accumulate)

    def unbind_shot_event(self, target):
        if target and target.is_valid():
            target.unregist_event('E_LEAVE_STATE', self.on_leave_state)
            target.unregist_event('E_CTRL_ACCUMULATE', self.on_accumulate)

    def on_leave_state(self, leave_state, new_st=None):
        if isinstance(leave_state, set) and status_config.ST_WEAPON_ACCUMULATE in leave_state or isinstance(leave_state, int) and status_config.ST_WEAPON_ACCUMULATE == leave_state:
            self.hide_accumulate_ui()

    def on_accumulate(self, flag):
        if flag:
            self.show_accumulate_ui()
        else:
            self.hide_accumulate_ui()

    def show_accumulate_ui(self):
        if not self._lplayer:
            return
        cur_weapon = self._lplayer.share_data.ref_wp_bar_cur_weapon
        if cur_weapon and cur_weapon.is_accumulate_gun():
            if self._accumulate_timer:
                global_data.game_mgr.unregister_logic_timer(self._accumulate_timer)
            if cur_weapon.get_accumulate_max_time() > 0.0:
                self._accumulate_timer = global_data.game_mgr.register_logic_timer(self.on_end_weapon, interval=cur_weapon.get_accumulate_max_time(), times=1, mode=timer.CLOCK)
            if global_data.cam_lplayer and not global_data.cam_lplayer.sd.ref_in_aim:
                ui = global_data.ui_mgr.show_ui('MechaAccumulateUI', 'logic.comsys.mecha_ui')
                ui.set_weapon_id(cur_weapon.iType)

    def hide_accumulate_ui(self):
        ui = global_data.ui_mgr.get_ui('MechaAccumulateUI')
        if ui:
            ui.delay_close()
        if self._accumulate_timer:
            global_data.game_mgr.unregister_logic_timer(self._accumulate_timer)
        self._accumulate_timer = None
        return

    def on_end_weapon(self):
        self.hide_accumulate_ui()
        if self._lplayer:
            self._lplayer.send_event('E_STOP_AUTO_FIRE')

    def on_hot_key_state_closed(self):
        for action_id, action_widget in six.iteritems(self._action_widget_dict):
            if action_widget:
                action_widget.switch_hot_key_show(False)

    def on_hot_key_state_opened(self):
        for action_id, action_widget in six.iteritems(self._action_widget_dict):
            if action_widget:
                action_widget.switch_hot_key_show(True)

    def check_show_nd_guide(self):
        self.hide_nd_guide()
        if not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            return
        if not global_data.player or not global_data.player.logic:
            return
        if global_data.player.logic.ev_g_spectate_target():
            return
        battle_times = global_data.player.get_total_cnt()
        if battle_times > 1:
            return
        control_target = global_data.player.logic.ev_g_control_target()
        if not (control_target and control_target.logic and control_target.logic.ev_g_is_mechatran()):
            return
        if control_target.logic.ev_g_pattern() == mconst.MECHA_PATTERN_VEHICLE:
            return
        is_first_joining = global_data.player.logic.ev_g_is_first_joining_veh_mecha()
        if not is_first_joining:
            return
        global_data.player.logic.send_event('E_SET_IS_FIRST_JOINING_VEH_MECHA', False)
        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(15.0),
         cc.CallFunc.create(lambda : self.show_nd_guide()),
         cc.DelayTime.create(3.0),
         cc.CallFunc.create(lambda : self.hide_nd_guide())]))

    def hide_nd_guide(self):
        self.panel.nd_guide.setVisible(False)
        if self.panel.IsPlayingAnimation('change'):
            self.panel.StopAnimation('change')

    def show_nd_guide(self):
        if not self._lplayer:
            return
        control_target = self._lplayer.ev_g_control_target()
        if not (control_target and control_target.logic and control_target.logic.ev_g_is_mechatran()):
            return
        if control_target.logic.ev_g_pattern() == mconst.MECHA_PATTERN_VEHICLE:
            return
        self.panel.nd_guide.setVisible(True)
        if not self.panel.IsPlayingAnimation('change'):
            self.panel.PlayAnimation('change')

    def set_action_btn_visible_by_name(self, btn_name, visible):
        if btn_name not in six_ex.keys(self._action_nd_dict):
            return
        if btn_name not in self._action_show_list:
            return
        if btn_name not in self._valid_show_list:
            return
        self._action_nd_dict[btn_name].setVisible(visible)