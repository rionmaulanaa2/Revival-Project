# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8023AimUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2
from logic.gcommon.common_const.mecha_const import MECHA_8023_FORM_PISTOL, MECHA_8023_FORM_SNIPE
from logic.gcommon.common_const.buff_const import BUFF_ID_MECHA_8023_SPEED_UP
from logic.gcommon.cdata.mecha_status_config import MC_RELOAD, MC_TRANSFORM
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon import time_utility
from common.utils.timer import CLOCK
ASSOCIATE_UI_LIST = [
 'FrontSightUI']
from common.const import uiconst
weapon_info = {MECHA_8023_FORM_PISTOL: {'btn_icon': (
                                       ('action1', 'gui/ui_res_2/battle/mech_main/icon_mech8023_1.png', 'show'),
                                       ('action2', 'gui/ui_res_2/battle/mech_main/icon_mech8023_1.png', 'show'),
                                       ('action3', 'gui/ui_res_2/battle/mech_main/icon_mech8023_1.png', 'show'),
                                       ('action4', 'gui/ui_res_2/battle/mech_main/icon_mech8023_2.png', '')),
                            'anim': 'show_sec',
                            'weapon_pos': PART_WEAPON_POS_MAIN1
                            },
   MECHA_8023_FORM_SNIPE: {'btn_icon': (
                                      ('action1', 'gui/ui_res_2/battle/mech_main/icon_mech8023_3.png', 'show'),
                                      ('action2', 'gui/ui_res_2/battle/mech_main/icon_mech8023_3.png', 'show'),
                                      ('action3', 'gui/ui_res_2/battle/mech_main/icon_mech8023_3.png', 'show'),
                                      ('action4', 'gui/ui_res_2/battle/mech_main/icon_mech8023_4.png', '')),
                           'anim': 'show',
                           'weapon_pos': PART_WEAPON_POS_MAIN2
                           }
   }

class Mecha8023AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8023'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON,
       PART_WEAPON_POS_MAIN2: MAIN_WEAPON
       }
    MECHA_EVENT = {'E_SWITCH_WEAPON': 'switch_weapon',
       'E_SET_STEALTH_TIME': 'refresh_sub_prog',
       'E_OPEN_AIM_CAMERA': 'on_open_aim_camera',
       'E_SHOW_ACC_WP_TRACK': 'hide_aim_ui',
       'E_STOP_ACC_WP_TRACK': 'show_aim',
       'E_RELOADING': 'hide_aim_ui',
       'E_LEAVE_STATE': 'on_leave_state',
       'E_BUFF_ADD_DATA': 'on_add_buff',
       'E_BUFF_DEL_DATA': 'on_del_buff',
       'E_START_SWITCH_WEAPON': 'on_switch_weapon'
       }
    IS_FULLSCREEN = True

    def on_init_panel(self):
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.init_parameters()
        self.init_aim_spread_mgr()
        self.init_bullet_widget()
        self.hide_main_ui(self.ASSOCIATE_UI_LIST)
        self.init_front_sight_extra_info()
        self.panel.nd_sub.setVisible(False)
        self.sub_visible = False
        self.mark_entities = set()
        global_data.emgr.add_entity_screen_mark += self.on_add_mark

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

    def disappear(self):
        self.panel.PlayAnimation('disappear')
        delay = self.panel.GetAnimationMaxRunTime('disappear')
        self.panel.SetTimeOut(delay, lambda : self.close())

    def init_parameters(self):
        self.is_shooting = False
        self.hide_aim = False
        self.switch_start_ts = 0
        self.switch_dur = 0
        self.switch_timer_id = None
        super(Mecha8023AimUI, self).init_parameters()
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            for event, func_name in six.iteritems(self.MECHA_EVENT):
                func = getattr(self, func_name)
                callable(func) and regist_func(event, func)

            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            weapon_form = self.mecha.ev_g_weapon_form()
            if weapon_form in weapon_info:
                wp_pos = weapon_info[weapon_form]['weapon_pos']
                if global_data.is_pc_mode:
                    self.mecha.send_event('E_REFRESH_CUR_WEAPON_BULLET', wp_pos)
                elif self.bullet_widget:
                    self.bullet_widget.weapon_bullet_changed(wp_pos, is_force=True)
            self.switch_weapon()

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            for event, func_name in six.iteritems(self.MECHA_EVENT):
                func = getattr(self, func_name)
                unregist_func(event, func)

        self.mecha = None
        return

    def hide_aim_ui(self, *args):
        self.panel.nd_aim.setVisible(False)
        self.panel.nd_sub_aim.setVisible(False)
        self.stop_update_front_sight_extra_info()

    def switch_weapon(self):
        if not self.mecha:
            return
        weapon_form = self.mecha.ev_g_weapon_form()
        self.show_aim()
        for action, icon_path, anim_name in weapon_info[weapon_form]['btn_icon']:
            self.mecha.send_event('E_SET_ACTION_ICON', action, icon_path, anim_name)

        self.aim_spread_mgr.set_weapon_pos(weapon_info[weapon_form]['weapon_pos'])
        self.aim_spread_mgr and self.aim_spread_mgr._on_spread()
        self.start_explode_instant(weapon_form)

    def refresh_sub_prog(self):
        cur_time = time_utility.time()
        left_time = max(0, self.sub_end_time - cur_time)
        show = left_time > 0
        if self.sub_visible != show:
            self.panel.PlayAnimation('show_sub' if show else 'disappear_sub')
            self.sub_visible = show
        if show:
            self.panel.prog_sub_left.SetPercentage(left_time * 100.0 / self.sub_duration)
            self.panel.nd_sub.lab_value.SetString('%.1f' % left_time)

    def on_add_buff--- This code section failed: ---

 165       0  LOAD_FAST             2  'buff_id'
           3  LOAD_GLOBAL           0  'BUFF_ID_MECHA_8023_SPEED_UP'
           6  COMPARE_OP            3  '!='
           9  POP_JUMP_IF_FALSE    16  'to 16'

 166      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 167      16  LOAD_FAST             4  'data'
          19  LOAD_ATTR             1  'get'
          22  LOAD_CONST            1  'add_time'
          25  CALL_FUNCTION_1       1 
          28  STORE_FAST            6  'add_time'

 168      31  LOAD_FAST             6  'add_time'
          34  POP_JUMP_IF_TRUE     41  'to 41'

 169      37  LOAD_CONST            0  ''
          40  RETURN_END_IF    
        41_0  COME_FROM                '34'

 170      41  LOAD_FAST             4  'data'
          44  LOAD_ATTR             1  'get'
          47  LOAD_CONST            2  'duration'
          50  CALL_FUNCTION_1       1 
          53  LOAD_FAST             0  'self'
          56  STORE_ATTR            2  'sub_duration'

 171      59  LOAD_FAST             0  'self'
          62  LOAD_ATTR             2  'sub_duration'
          65  POP_JUMP_IF_TRUE     72  'to 72'

 172      68  LOAD_CONST            0  ''
          71  RETURN_END_IF    
        72_0  COME_FROM                '65'

 173      72  LOAD_FAST             6  'add_time'
          75  LOAD_FAST             0  'self'
          78  LOAD_ATTR             2  'sub_duration'
          81  BINARY_ADD       
          82  LOAD_FAST             0  'self'
          85  STORE_ATTR            3  'sub_end_time'

 174      88  LOAD_GLOBAL           4  'getattr'
          91  LOAD_GLOBAL           3  'sub_end_time'
          94  LOAD_CONST            0  ''
          97  CALL_FUNCTION_3       3 
         100  POP_JUMP_IF_TRUE    136  'to 136'

 175     103  LOAD_GLOBAL           6  'global_data'
         106  LOAD_ATTR             7  'game_mgr'
         109  LOAD_ATTR             8  'register_logic_timer'
         112  LOAD_FAST             0  'self'
         115  LOAD_ATTR             9  'refresh_sub_prog'
         118  LOAD_CONST            4  'interval'
         121  LOAD_CONST            5  1
         124  CALL_FUNCTION_257   257 
         127  LOAD_FAST             0  'self'
         130  STORE_ATTR           10  'sub_prog_timer'
         133  JUMP_FORWARD          0  'to 136'
       136_0  COME_FROM                '133'
         136  LOAD_CONST            0  ''
         139  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 97

    def on_del_buff(self, buff_key, buff_id, buff_idx):
        if buff_id != BUFF_ID_MECHA_8023_SPEED_UP:
            return
        self.sub_duration = 0
        self.sub_end_time = 0
        self.refresh_sub_prog()
        self.clear_sub_prog_timer()

    def clear_sub_prog_timer--- This code section failed: ---

 186       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_3       3 
          12  POP_JUMP_IF_FALSE    46  'to 46'

 187      15  LOAD_GLOBAL           2  'global_data'
          18  LOAD_ATTR             3  'game_mgr'
          21  LOAD_ATTR             4  'unregister_logic_timer'
          24  LOAD_FAST             0  'self'
          27  LOAD_ATTR             5  'sub_prog_timer'
          30  CALL_FUNCTION_1       1 
          33  POP_TOP          

 188      34  LOAD_CONST            0  ''
          37  LOAD_FAST             0  'self'
          40  STORE_ATTR            5  'sub_prog_timer'
          43  JUMP_FORWARD          0  'to 46'
        46_0  COME_FROM                '43'
          46  LOAD_CONST            0  ''
          49  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9

    def on_open_aim_camera(self, is_open):
        self.hide_aim = is_open
        if is_open:
            self.panel.nd_aim.setVisible(False)
            self.panel.nd_sub_aim.setVisible(False)
        else:
            self.show_aim(no_anim=True)

    def show_aim(self, weapon_form=None, no_anim=False):
        if not self.mecha:
            return
        else:
            if self.hide_aim:
                self.panel.nd_aim.setVisible(False)
                self.panel.nd_sub_aim.setVisible(False)
                return
            if weapon_form is None:
                weapon_form = self.mecha.ev_g_weapon_form()
            if weapon_form == MECHA_8023_FORM_PISTOL and not self.panel.nd_sub_aim.isVisible():
                self.panel.nd_aim.setVisible(False)
                if no_anim:
                    self.panel.nd_sub_aim.setVisible(True)
                else:
                    self.panel.PlayAnimation('show_sec')
            elif weapon_form == MECHA_8023_FORM_SNIPE and not self.panel.nd_aim.isVisible():
                self.panel.nd_sub_aim.setVisible(False)
                if no_anim:
                    self.panel.nd_aim.setVisible(True)
                else:
                    self.panel.PlayAnimation('show')
            self.aim_spread_mgr._on_spread()
            self.start_explode_instant(weapon_form)
            return

    def on_leave_state(self, state, *args):
        if state in (MC_RELOAD,):
            self.show_aim(no_anim=True)
        elif state == MC_TRANSFORM:
            self.on_switch_weapon_finish()

    def start_explode_instant(self, weapon_form):
        if weapon_form not in weapon_info:
            self.stop_update_front_sight_extra_info()
        else:
            self.start_update_front_sight_extra_info(weapon_info[weapon_form]['weapon_pos'])

    def on_add_mark(self, entity_id, *args):
        self.panel.temp_mark_tip.setVisible(True)
        self.panel.PlayAnimation('show_mark_tip')

    def on_del_mark(self, entity_id):
        if entity_id not in self.mark_entities:
            return
        self.mark_entities.remove(entity_id)
        self.panel.nd_mark_cnt.setVisible(bool(self.mark_entities))
        self.panel.lab_mark_cnt.SetString(str(len(self.mark_entities)))

    def on_switch_weapon(self, switch_dur):
        self.switch_start_ts = time_utility.time()
        self.switch_dur = switch_dur
        if not self.switch_timer_id:
            self.switch_timer_id = global_data.game_mgr.register_logic_timer(self.switch_prog_tick, interval=0.05, mode=CLOCK)
        self.panel.StopAnimation('disappear_prog')
        self.panel.PlayAnimation('show_prog')

    def switch_prog_tick(self):
        cur_time = time_utility.time()
        elapsed_time = cur_time - self.switch_start_ts
        percent = min(1.0, max(0.0, elapsed_time / self.switch_dur)) * 100.0
        self.panel.switch_prog.prog.SetPercentage(percent)

    def on_switch_weapon_finish(self):
        if self.switch_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.switch_timer_id)
            self.switch_timer_id = None
        self.panel.StopAnimation('show_prog')
        self.panel.PlayAnimation('disappear_prog')
        return

    def on_finalize(self):
        super(Mecha8023AimUI, self).on_finalize()
        self.clear_sub_prog_timer()
        self.mark_entities = None
        if self.switch_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.switch_timer_id)
            self.switch_timer_id = None
        global_data.emgr.add_entity_screen_mark -= self.on_add_mark
        return