# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/HpInfoUI.py
from __future__ import absolute_import
import six_ex
import six
from common.uisys.basepanel import BasePanel
import world
import cc
from common.const.uiconst import HP_ZORDER
from common.utils.cocos_utils import ccp
from logic.gutils import template_utils
from logic.gcommon.common_const import ui_battle_const as ubc
from common.framework import Functor
from common.utils.timer import CLOCK
from logic.gcommon.common_const.ui_battle_const import HP_TAIL_SLOW_TIME, HP_BAR_NORMAL_PERCENT, HP_BAR_WARNING_PERCENT
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.common_const import battle_const
from common.const import uiconst
import math

class HpInfoBaseUI(BasePanel):
    DLG_ZORDER = HP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'lv_up_hp_notice': '_on_lv_up'
       }

    def on_init_panel(self):
        self.panel.temp_hp.hp_tail.setVisible(True)
        self.init_event()
        self.init_custom_com()
        self.panel.temp_hp.hp_tail.SetEnableCascadeOpacityRecursion(True)
        self.panel.temp_hp.nd_light.SetEnableCascadeOpacityRecursion(True)
        self.panel.temp_hp.hp_tail.setOpacity(0)
        self.panel.temp_hp.nd_light.setOpacity(0)
        self.buff_com = None
        self.init_buff_com()
        self.init_temp_signal()
        self.hide_ui()
        return

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_resolution_changed(self):
        self.panel.temp_hp.middle.setPositionY(self.panel.temp_hp.middle.getPosition().y + 15)

    def on_finalize_panel--- This code section failed: ---

  56       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'destroy_widget'
           6  LOAD_CONST            1  'buff_com'
           9  CALL_FUNCTION_1       1 
          12  POP_TOP          

  57      13  LOAD_FAST             0  'self'
          16  LOAD_ATTR             1  'unbind_player'
          19  CALL_FUNCTION_0       0 
          22  POP_TOP          

  58      23  LOAD_CONST            0  ''
          26  LOAD_FAST             0  'self'
          29  STORE_ATTR            3  'player'

  59      32  LOAD_FAST             0  'self'
          35  LOAD_ATTR             4  'custom_ui_com'
          38  POP_JUMP_IF_FALSE    66  'to 66'

  60      41  LOAD_FAST             0  'self'
          44  LOAD_ATTR             4  'custom_ui_com'
          47  LOAD_ATTR             5  'destroy'
          50  CALL_FUNCTION_0       0 
          53  POP_TOP          

  61      54  LOAD_CONST            0  ''
          57  LOAD_FAST             0  'self'
          60  STORE_ATTR            4  'custom_ui_com'
          63  JUMP_FORWARD          0  'to 66'
        66_0  COME_FROM                '63'

  62      66  LOAD_GLOBAL           6  'getattr'
          69  LOAD_GLOBAL           2  'None'
          72  BUILD_MAP_0           0 
          75  CALL_FUNCTION_3       3 
          78  STORE_FAST            1  'ani_dict'

  63      81  SETUP_LOOP           45  'to 129'
          84  LOAD_GLOBAL           7  'six'
          87  LOAD_ATTR             8  'iteritems'
          90  LOAD_FAST             1  'ani_dict'
          93  CALL_FUNCTION_1       1 
          96  GET_ITER         
          97  FOR_ITER             28  'to 128'
         100  UNPACK_SEQUENCE_2     2 
         103  STORE_FAST            2  '_'
         106  STORE_FAST            3  'nd'

  64     109  LOAD_FAST             3  'nd'
         112  LOAD_ATTR             9  'Destroy'
         115  LOAD_CONST            3  'is_remove'
         118  LOAD_GLOBAL          10  'True'
         121  CALL_FUNCTION_256   256 
         124  POP_TOP          
         125  JUMP_BACK            97  'to 97'
         128  POP_BLOCK        
       129_0  COME_FROM                '81'
         129  LOAD_CONST            0  ''
         132  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 75

    def init_parameters(self):
        self.hp_progress_width = self.panel.temp_hp.nd_light.getContentSize().width
        self.player = None
        self._is_danger_flashing = False
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        self.add_hide_count(self.__class__.__name__)
        spectate_target = None
        if global_data.player and global_data.player.logic:
            spectate_target = global_data.player.logic.ev_g_spectate_target()
        if spectate_target and spectate_target.logic:
            self.on_player_setted(spectate_target.logic)
        elif player:
            self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted
        emgr.scene_camera_player_setted_event += self._on_scene_cam_player_setted
        emgr.settle_stage_event += self.on_create_settle_stage_ui
        self.signal_left_time = None
        self.cur_parachute_stage = None
        return

    def _on_scene_cam_player_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        tm = global_data.game_mgr.get_logic_timer()
        timer_list = ['_hp_head_line_timer', '_hp_tail_timer', '_hp_danger_flash_timer']
        for tname in timer_list:
            inst = getattr(self, tname, None)
            if inst:
                tm.unregister(inst)
                setattr(self, tname, None)

        self.unbind_player()
        if player:
            self.player = player
            self.add_show_count(self.__class__.__name__)
            self.bind_hp_ui(self.player)
            self.init_hp_bars()
            self.init_signal_bar()
            if self.player.ev_g_death():
                self.on_death()
            elif self.player.ev_g_agony():
                self.on_knock_down()
        else:
            self.player = None
        return

    def on_create_settle_stage_ui(self, *args):
        pass

    def unbind_player(self):
        if self.player and self.player.is_valid():
            self.unbind_hp_ui(self.player)
            self.player = None
        return

    def init_event(self):
        self.init_parameters()

    def init_hp_bars(self):
        self.max_hp = self.player.share_data.ref_max_hp
        self.cur_hp = self.player.share_data.ref_hp
        self._old_hp = self.cur_hp
        self.cur_shield = 0
        self.max_shield = 0
        self.dest_shield = 0
        self.shield_speed = 0
        self.outer_shield = self.player.ev_g_outer_shield()
        self._hp_head_line_timer = None
        self._hp_tail_timer = None
        self._hp_head_line_alpha = 0
        self._hp_tail = self.cur_hp
        self._hp_danger_flash_timer = None
        percent = template_utils.get_human_cur_hp_percent(self.cur_hp, self.max_hp, self.get_show_shield(), self.get_show_shield_max())
        self.panel.temp_hp.hp_tail.SetPercent(percent)
        self.is_recovered_by_drug = False
        self.is_recovered_by_energy = False
        self.drug_recover_data = {}
        self.energy_recover_data = {}
        self.hp_status = None
        self.is_knocked_down = False
        self.stop_agony_and_death_effect()
        self._cur_dark_effect_vars = None
        self.init_hp_events()
        bar = self.panel.temp_hp.hp_recover
        bar.setVisible(False)
        bar.SetPercent(0)
        bar = self.panel.temp_hp.hp_energy
        bar.setVisible(False)
        bar.SetPercent(0)
        self.panel.temp_hp.nd_light.setOpacity(0)
        self.on_max_hp_changed(self.max_hp, self.cur_hp)
        if self.outer_shield > 0:
            self.on_outer_shield_changed(self.outer_shield)
        return

    def get_show_shield(self):
        return self.cur_shield + self.outer_shield

    def get_show_shield_max(self):
        return self.max_shield + self.outer_shield

    def change_shield(self, new_shield, add_from_dmg=False):
        self.cur_shield = new_shield
        self.on_hp_changed(self.cur_hp)
        self.panel.temp_hp.lab_hp_full.SetString('/' + str(int(math.ceil(self.max_hp + self.get_show_shield_max()) * global_data.game_mode.get_mode_scale())))

    def on_set_shield_max(self, shiled_max):
        self.max_shield = shiled_max
        self.cur_shield = shiled_max
        self.panel.temp_hp.hp_shield.setVisible(self.get_show_shield_max() > 0)
        self.on_hp_changed(self.cur_hp)
        self.panel.temp_hp.lab_hp_full.SetString('/' + str(int(math.ceil(self.max_hp + self.get_show_shield_max()) * global_data.game_mode.get_mode_scale())))

    def on_outer_shield_changed(self, outer_shield_hp):
        self.outer_shield = outer_shield_hp
        self.panel.temp_hp.hp_shield.setVisible(self.get_show_shield_max() > 0)
        if not self.is_knocked_down:
            self.on_hp_changed(self.cur_hp)
        else:
            self.panel.temp_hp.lab_hp.SetString(str(int(math.ceil(self.cur_hp) * global_data.game_mode.get_mode_scale())))
        self.panel.temp_hp.lab_hp_full.SetString('/' + str(int(math.ceil(self.max_hp + self.get_show_shield_max()) * global_data.game_mode.get_mode_scale())))

    def play_harm_show_ani(self, index):
        key = 'line_%d' % index
        if key in self.ani_nodes:
            return
        else:
            nd_line = getattr(self.panel.temp_hp, 'line_%d' % index, None)
            if not nd_line:
                return
            nd = global_data.uisystem.load_template_create('battle/i_hp_shield_dec')
            self.panel.temp_hp.nd_line.AddChild('', nd)
            nd.setPosition(nd_line.getPosition())
            nd.PlayAnimation('harm_show')
            self.ani_nodes[key] = nd
            self.panel.temp_hp.SetTimeOut(nd.GetAnimationPlayTimes('harm_show'), Functor(self.destroy_ani_node, key))
            return

    def destroy_ani_node(self, key):
        if key in self.ani_nodes:
            nd = self.ani_nodes[key]
            nd.Destroy(is_remove=True)
            del self.ani_nodes[key]

    def init_hp_events(self):

        @self.panel.temp_hp.hp_progress.unique_callback()
        def OnSetPercentage(pr, percent):
            if not self.is_knocked_down:
                hp_status = self.get_hp_bar_status(percent)
                if self.hp_status != hp_status:
                    pic_path = self.get_hp_bar_status_background(hp_status)
                    self.hp_status = hp_status
                    self.panel.temp_hp.hp_progress.SetPath('', pic_path)
                    self.panel.temp_hp.hp_progress.setPercent(percent + 0.01)
                    light_pc_path = self.get_hp_light_status_background(hp_status)
                    self.panel.temp_hp.nd_light.img_light.SetDisplayFrameByPath('', light_pc_path)
                    if self.hp_status == ubc.HP_BAR_DANGER_PERCENT:
                        self.panel.temp_hp.PlayAnimation('red_blink')
                    else:
                        self.panel.temp_hp.StopAnimation('red_blink')
                if self.is_recovered_by_drug:
                    self._update_hp_recover_bar_pos(percent)
            self._update_hp_energy_bar_pos()

        @self.panel.temp_hp.hp_energy.unique_callback()
        def OnSetPercentage(pr, percent):
            if self.is_recovered_by_drug:
                self._update_hp_recover_bar_pos()

    def _update_hp_recover_bar_pos(self, percent=None):
        from common.utils.cocos_utils import ccp
        if not self.is_recovered_by_energy:
            x, y = self.panel.temp_hp.hp_progress.GetPercentagePosition(percent)
        else:
            x, y = self.panel.temp_hp.hp_energy.GetPercentagePosition()
        lpos = self.panel.temp_hp.hp_recover.getParent().convertToNodeSpace(ccp(x, y))
        old_pos = self.panel.temp_hp.hp_recover.getPosition()
        self.panel.temp_hp.hp_recover.SetPosition(lpos.x, old_pos.y)

    def _update_hp_energy_bar_pos(self):
        from common.utils.cocos_utils import ccp
        x, y = self.panel.temp_hp.hp_progress.GetPercentagePosition()
        lpos = self.panel.temp_hp.hp_energy.getParent().convertToNodeSpace(ccp(x, y))
        self.panel.temp_hp.hp_energy.setPositionX(lpos.x)

    def on_hp_changed(self, new_hp, mod_hp=None, ani_time=0.0):
        tm = global_data.game_mgr.get_logic_timer()
        self._old_hp = self.cur_hp
        self.cur_hp = max(min(new_hp, self.max_hp), 0)
        sum_shield = self.get_show_shield()
        sum_shield_max = self.get_show_shield_max()
        self.panel.temp_hp.lab_hp.SetString(str(int(math.ceil(self.cur_hp + sum_shield) * global_data.game_mode.get_mode_scale())))
        percent = template_utils.get_human_cur_hp_percent(self.cur_hp, self.max_hp, sum_shield, sum_shield_max)
        self.panel.temp_hp.hp_progress.SetPercentageWithAni(percent, ani_time)
        shield_percent = template_utils.get_human_cur_shield_percent(self.cur_hp, self.max_hp, sum_shield, sum_shield_max)
        self.panel.temp_hp.hp_shield.setPercent(shield_percent)
        if self.cur_hp < self._old_hp and self.panel:
            slow_count = HP_TAIL_SLOW_TIME * 30.0

            def hp_diff_cb(*args):
                if not self.panel:
                    return
                else:
                    dec = (self._old_hp - self.cur_hp) / slow_count
                    self._hp_tail -= dec
                    self._hp_tail_alpha -= 255 / slow_count
                    self._hp_tail_alpha = int(self._hp_tail_alpha)
                    if self._hp_tail <= self.cur_hp:
                        self._hp_tail = self.cur_hp
                    if self._hp_tail_alpha <= 0:
                        self._hp_tail_alpha = 0
                    hp_tail_percent = self._hp_tail * 100.0 / self.max_hp
                    self.panel.temp_hp.hp_tail.SetPercent(hp_tail_percent)
                    self.panel.temp_hp.hp_tail.setOpacity(self._hp_tail_alpha)
                    if self._hp_tail - self.cur_hp <= 0.01:
                        tm.unregister(self._hp_tail_timer)
                        self._hp_tail_timer = None
                    return

            if self._hp_tail_timer:
                tm.unregister(self._hp_tail_timer)
                self._hp_tail_timer = None
                self._hp_tail = self._old_hp
                hp_tail_percent = self._old_hp * 100.0 / self.max_hp
                self.panel.temp_hp.hp_tail.SetPercent(hp_tail_percent)
            self._hp_tail_alpha = 255
            self.panel.temp_hp.hp_tail.setOpacity(self._hp_tail_alpha)
            self._hp_tail_timer = tm.register(func=hp_diff_cb, interval=0.033, times=-1, mode=CLOCK)

            def hp_head_line_cb(*args):
                if not self.panel:
                    return
                else:
                    self._hp_head_line_alpha -= 255 / slow_count
                    self._hp_head_line_alpha = int(self._hp_head_line_alpha)
                    if self._hp_head_line_alpha < 0:
                        self._hp_head_line_alpha = 0
                    self.panel.temp_hp.nd_light.setOpacity(self._hp_head_line_alpha)
                    if self._hp_head_line_alpha == 0:
                        tm.unregister(self._hp_head_line_timer)
                        self._hp_head_line_timer = None
                    return

            if self._hp_head_line_timer:
                tm.unregister(self._hp_head_line_timer)
                self._hp_head_line_timer = None
                self.panel.temp_hp.nd_light.setOpacity(0)
            self._hp_head_line_alpha = 255
            self.panel.temp_hp.nd_light.setOpacity(self._hp_head_line_alpha)
            head_line_x = self.panel.temp_hp.hp_progress.getPercent() / 100.0 * self.hp_progress_width
            self.panel.temp_hp.nd_light.img_light.setPositionX(head_line_x)
            self._hp_head_line_timer = tm.register(func=hp_head_line_cb, interval=0.033, times=-1, mode=CLOCK)
        else:
            self._hp_tail = self.cur_hp
            self.panel.temp_hp.hp_tail.SetPercent(percent)
        if percent < 15:
            self.start_hp_bar_flash()
        else:
            self.stop_hp_bar_flash()
        return

    def start_hp_bar_flash(self):
        tm = global_data.game_mgr.get_logic_timer()
        if self._is_danger_flashing:
            return
        self._is_danger_flashing = True
        self.panel.temp_hp.img_danger.setVisible(True)
        self.panel.temp_hp.PlayAnimation('danger')

        def continue_danger(*args):
            if not self.panel:
                return
            else:
                self.panel.temp_hp.StopAnimation('danger')
                self.panel.temp_hp.PlayAnimation('continue_danger')
                self._hp_danger_flash_timer = None
                return

        self._hp_danger_flash_timer = tm.register(func=continue_danger, interval=3, times=1, mode=CLOCK)

    def stop_hp_bar_flash(self):
        if self._is_danger_flashing:
            tm = global_data.game_mgr.get_logic_timer()
            self.panel.temp_hp.img_danger.setVisible(False)
            self.panel.temp_hp.StopAnimation('danger')
            self.panel.temp_hp.StopAnimation('continue_danger')
            if self._hp_danger_flash_timer:
                tm.unregister(self._hp_danger_flash_timer)
                self._hp_danger_flash_timer = None
            self._is_danger_flashing = False
        return

    def on_max_hp_changed(self, max_hp, hp, *args):
        if not self.player:
            return
        self.max_hp = float(max_hp)
        self.cur_hp = float(hp)
        self.on_hp_changed(self.cur_hp)
        self.panel.temp_hp.lab_hp_full.SetString('/' + str(int(math.ceil(self.max_hp + self.get_show_shield_max()) * global_data.game_mode.get_mode_scale())))

    def on_hp_init(self, cur_hp, max_hp):
        self.max_hp = float(max_hp)
        self.on_hp_changed(cur_hp)
        self.panel.temp_hp.lab_hp_full.SetString('/' + str(int(math.ceil(self.max_hp + self.get_show_shield_max()) * global_data.game_mode.get_mode_scale())))

    def get_hp_bar_status(self, percent):
        if percent >= ubc.HP_BAR_NORMAL_PERCENT:
            return ubc.HP_BAR_NORMAL_PERCENT
        else:
            if percent >= ubc.HP_BAR_WARNING_PERCENT:
                return ubc.HP_BAR_WARNING_PERCENT
            return ubc.HP_BAR_DANGER_PERCENT

    def get_hp_bar_status_background(self, status):
        pic_dict = {ubc.HP_BAR_NORMAL_PERCENT: 'gui/ui_res_2/battle/progress/hp_100.png',
           ubc.HP_BAR_WARNING_PERCENT: 'gui/ui_res_2/battle/progress/hp_75.png',
           ubc.HP_BAR_DANGER_PERCENT: 'gui/ui_res_2/battle/progress/hp_25.png'
           }
        return pic_dict.get(status, 'gui/ui_res_2/battle/progress/hp_25.png')

    def get_hp_light_status_background(self, status):
        pic_dict = {ubc.HP_BAR_NORMAL_PERCENT: 'gui/ui_res_2/battle/progress/hp_light_100.png',
           ubc.HP_BAR_WARNING_PERCENT: 'gui/ui_res_2/battle/progress/hp_light_100.png',
           ubc.HP_BAR_DANGER_PERCENT: 'gui/ui_res_2/battle/progress/hp_light_25.png'
           }
        return pic_dict.get(status, 'gui/ui_res_2/battle/progress/hp_light_25.png')

    def on_knock_down(self):
        self.panel.temp_hp.PlayAnimation('red_blink')
        self.is_knocked_down = True
        self.panel.temp_hp.hp_progress.SetPath('', 'gui/ui_res_2/battle/progress/hp_0.png')
        self.panel.temp_hp.sp_knock_down.setVisible(True)
        self.panel.temp_hp.hp_progress.stopAllActions()
        effect_dict = {'render_vars': {'DarkBegin': 0.5,'DarkAlpha': 1.0,'DarkIntensity': 2.55}}
        self._cur_dark_effect_vars = effect_dict
        global_data.emgr.show_screen_effect.emit('DarkCornerEffect', effect_dict)
        if global_data.player and global_data.player.logic and not global_data.player.logic.ev_g_is_in_spectate():
            if not global_data.is_pc_mode:
                global_data.ui_mgr.show_ui('SOSUI', 'logic.comsys.control_ui')

    def on_knock_down_hp_changed(self, hp):
        hp = float(hp)
        self.panel.temp_hp.hp_progress.SetPercentageWithAni(hp / self.max_hp * 100, 0.4)
        THRES = self.max_hp * 0.3
        if hp >= THRES:
            effect_dict = {'render_vars': {'DarkBegin': (hp - THRES) / (self.max_hp - THRES) * 0.5,'DarkAlpha': 1.0,'DarkIntensity': 2.55}}
        else:
            effect_dict = {'render_vars': {'DarkAlpha': hp / THRES * 0.5 + 0.5}}
        if self._cur_dark_effect_vars:
            self.show_dark_corner_effect_with_transfer(self._cur_dark_effect_vars, effect_dict, 0.3)
        else:
            self._cur_dark_effect_vars = effect_dict
            global_data.emgr.show_screen_effect.emit('DarkCornerEffect', self._cur_dark_effect_vars)

    def on_teammate_stop_rescue(self, *args):
        if self.player:
            is_dying = self.player.ev_g_agony()
            if self.is_knocked_down and not is_dying:
                self.on_revive()

    def on_revive(self):
        self.is_knocked_down = False
        cur_percent = self.panel.temp_hp.hp_progress.getPercent()
        self.panel.temp_hp.hp_progress.SetPercentage(0)
        self.panel.temp_hp.hp_progress.SetPercentage(cur_percent)
        self.stop_agony_and_death_effect()

    def stop_agony_and_death_effect(self):
        self.panel.temp_hp.sp_knock_down.setVisible(False)
        self._cur_dark_effect_vars = None
        self.panel.temp_hp.nd_dark_effect.StopTimerAction()
        self.panel.temp_hp.nd_gray_effect.StopTimerAction()
        self.panel.temp_hp.nd_gray_effect.stopAllActions()
        global_data.emgr.hide_screen_effect.emit('DarkCornerEffect')
        global_data.emgr.hide_screen_effect.emit('GrayEffect')
        self.panel.temp_hp.StopAnimation('red_blink')
        global_data.ui_mgr.close_ui('SOSUI')
        return

    @execute_by_mode(False, (game_mode_const.GAME_MODE_SNATCHEGG,))
    def on_death(self, *arg):
        self._cur_dark_effect_vars = None
        self.panel.temp_hp.nd_dark_effect.StopTimerAction()
        self.panel.temp_hp.img_danger.setVisible(False)
        self.stop_hp_bar_flash()
        global_data.emgr.hide_screen_effect.emit('DarkCornerEffect')
        global_data.emgr.i_am_dead.emit()
        self.panel.temp_hp.StopAnimation('red_blink')
        self.show_gray_effect_ani(0.7, 0.05, 1, delay=0.5)
        global_data.ui_mgr.close_ui('SOSUI')
        return

    def bind_hp_ui(self, target):
        target.regist_event('E_HEALTH_HP_CHANGE', self.on_hp_changed)
        target.regist_event('E_HEALTH_HP_INIT', self.on_hp_init)
        target.regist_event('E_DEATH', self.on_death)
        target.regist_event('E_AGONY', self.on_knock_down)
        target.regist_event('E_AGONY_HP', self.on_knock_down_hp_changed)
        target.regist_event('E_ON_SAVED', self.on_teammate_stop_rescue)
        target.regist_event('E_REVIVE', self.on_revive)
        target.regist_event('E_MAX_HP_CHANGED', self.on_max_hp_changed)
        target.regist_event('E_SET_SHIELD', self.change_shield)
        target.regist_event('E_SET_SHIELD_MAX', self.on_set_shield_max)
        target.regist_event('E_OUTER_SHIELD_HP_CHANGED', self.on_outer_shield_changed, 100)
        target.regist_event('E_SIGNAL_INIT', self.on_signal_init)
        target.regist_event('E_SIGNAL_CHANGE', self.on_signal_changed)

    def unbind_hp_ui(self, target):
        if target and target.unregist_event:
            target.unregist_event('E_HEALTH_HP_CHANGE', self.on_hp_changed)
            target.unregist_event('E_HEALTH_HP_INIT', self.on_hp_init)
            target.unregist_event('E_DEATH', self.on_death)
            target.unregist_event('E_AGONY', self.on_knock_down)
            target.unregist_event('E_AGONY_HP', self.on_knock_down_hp_changed)
            target.unregist_event('E_ON_SAVED', self.on_teammate_stop_rescue)
            target.unregist_event('E_REVIVE', self.on_revive)
            target.unregist_event('E_MAX_HP_CHANGED', self.on_max_hp_changed)
            target.unregist_event('E_SET_SHIELD', self.change_shield)
            target.unregist_event('E_SET_SHIELD_MAX', self.on_set_shield_max)
            target.unregist_event('E_OUTER_SHIELD_HP_CHANGED', self.on_outer_shield_changed)
            target.unregist_event('E_SIGNAL_INIT', self.on_signal_init)
            target.unregist_event('E_SIGNAL_CHANGE', self.on_signal_changed)

    def show_dark_corner_effect_with_transfer(self, cur_vars, target_vars, times):

        def _set_dark_corner_effect_with_t(t):
            effect_dict = self.cal_dark_corner_vars_with_time(cur_vars['render_vars'], target_vars['render_vars'], t / times)
            self._cur_dark_effect_vars = {'render_vars': effect_dict}
            global_data.emgr.show_screen_effect.emit('DarkCornerEffect', self._cur_dark_effect_vars)

        def _callback():
            self._cur_dark_effect_vars = dict(cur_vars)
            self._cur_dark_effect_vars.update(target_vars)
            global_data.emgr.show_screen_effect.emit('DarkCornerEffect', self._cur_dark_effect_vars)

        self.panel.temp_hp.nd_dark_effect.StopTimerAction()
        self.panel.temp_hp.nd_dark_effect.TimerAction(_set_dark_corner_effect_with_t, times, _callback)

    def cal_dark_corner_vars_with_time(self, start_vars, end_vars, t):
        mid_var = dict(end_vars)
        for var_name in six_ex.keys(start_vars):
            start_val = start_vars[var_name]
            end_val = end_vars.get(var_name, start_val)
            mid_val = (end_val - start_val) * t + start_val
            mid_var[var_name] = mid_val

        return mid_var

    def show_gray_effect_ani(self, start_factor, end_factor, times, delay=0.5):

        def _gray_effect_with_time(t):
            factor = (end_factor - start_factor) * t / times + start_factor
            global_data.emgr.show_screen_effect.emit('GrayEffect', {'gray_factor': factor})

        self.panel.temp_hp.nd_gray_effect.StopTimerAction()

        def _cc_show_gray():
            self.panel.temp_hp.nd_gray_effect.TimerAction(_gray_effect_with_time, times)

        self.panel.temp_hp.nd_gray_effect.SetTimeOut(0.1, _cc_show_gray)

    @execute_by_mode(False, game_mode_const.Hide_ArmorBuffUI)
    def init_buff_com(self):
        from logic.comsys.battle.ArmorBuffWidget import ArmorBuffWidget
        self.buff_com = ArmorBuffWidget(self.panel.temp_hp.middle)

    @execute_by_mode(True, game_mode_const.Hide_ArmorBuffUI)
    def hide_ui(self):
        self.panel.temp_hp.list_armor.setVisible(False)

    def get_armor_item(self, pos):
        return self.panel.temp_hp.list_armor.GetItem(pos)

    def change_ui_data(self):
        nd = getattr(self.panel, 'temp_hp')
        scale = nd.getScale()
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        return (
         w_pos, scale, 'nd_helmet')

    def _on_lv_up(self, *args):
        self.panel.temp_hp.PlayAnimation('upgrade')

    def init_temp_signal(self):
        if battle_utils.is_battle_signal_open():
            self.panel.temp_hp.temp_signal.setVisible(True)
            self.panel.temp_hp.temp_signal.nd_signal.setVisible(True)
            self.panel.temp_hp.temp_signal.nd_signal.img_status_normal.setVisible(True)
            self.panel.temp_hp.temp_signal.nd_signal.img_status_hurt.setVisible(False)
            self.panel.temp_hp.temp_signal.RecordAnimationNodeState('loop')
            self.panel.temp_hp.middle.setPositionY(self.panel.temp_hp.middle.getPosition().y + 15)
            return
        self.panel.temp_hp.temp_signal.setVisible(False)

    def init_signal_bar(self):
        if battle_utils.is_battle_signal_open():
            self.max_signal = self.player.ev_g_max_signal()
            self.cur_signal = self.player.ev_g_signal()
            self.signal_left_time = self.player.ev_g_signal_left_time()
            self.refresh_signal_ui()

    def on_signal_init(self, cur_signal, max_signal, left_time):
        self.max_signal = cur_signal
        self.cur_signal = max_signal
        self.signal_left_time = left_time
        self.refresh_signal_ui()

    def on_signal_changed(self, cur_signal, percent, left_time):
        self.cur_signal = cur_signal
        self.signal_left_time = left_time
        self.refresh_signal_ui()

    def refresh_signal_ui(self):
        percent = float(self.cur_signal) / self.max_signal * 100
        self.panel.temp_hp.temp_signal.img_signal_bar.prog_signal.SetPercent(percent)
        if percent >= battle_const.BATTLE_SIGNAL_SHOW_UP_TIP_MIN_PERCENT:
            self.panel.temp_hp.temp_signal.nd_signal.img_status_normal.setVisible(True)
            self.panel.temp_hp.temp_signal.nd_signal.img_status_hurt.setVisible(False)
        else:
            self.panel.temp_hp.temp_signal.nd_signal.img_status_hurt.setVisible(True)
            self.panel.temp_hp.temp_signal.nd_signal.img_status_normal.setVisible(False)
        if 0 < self.cur_signal <= battle_const.BATTLE_SIGNAL_WARNING_LEFT_VALUE_MIN:
            if not self.panel.temp_hp.temp_signal.IsPlayingAnimation('loop'):
                self.panel.temp_hp.temp_signal.PlayAnimation('loop')
        elif self.panel.temp_hp.temp_signal.IsPlayingAnimation('loop'):
            self.panel.temp_hp.temp_signal.StopAnimation('loop')
            self.panel.temp_hp.temp_signal.RecoverAnimationNodeState('loop')


class HpInfoUI(HpInfoBaseUI):
    PANEL_CONFIG_NAME = 'battle\\hp_mp'

    def leave_screen(self):
        super(HpInfoUI, self).leave_screen()
        global_data.ui_mgr.close_ui('HpInfoUI')

    def change_ui_data_three(self):
        nd = self.panel.temp_hp.temp_signal
        scale = nd.getScale()
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        return (
         w_pos, scale, 'nd_signal_tips')

    def add_show_count(self, key='_default', count=1, is_check=True):
        super(HpInfoUI, self).add_show_count(key, count, is_check)

    def add_hide_count(self, key='_default', count=1, no_same_key=True, is_check=True):
        super(HpInfoUI, self).add_hide_count(key, count, no_same_key, is_check)