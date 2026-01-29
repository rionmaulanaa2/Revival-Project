# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/StateChangeUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import world
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.cdata.status_config import ST_MECHA_BOARDING, ST_MECH_EJECTION
from logic.gcommon.common_const import mecha_const as mconst
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from common.cfg import confmgr
from logic.comsys.effect import ui_effect
from logic.gcommon.cdata import driver_lv_data
from common.utils.timer import RELEASE, CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
import math3d
import cc
from logic.gutils.mecha_utils import calc_mecha_acc_charing_target_progress
from logic.gcommon.const import NEWBIE_STAGE_MECHA_BATTLE, NEWBIE_STAGE_HUMAN_BATTLE
ANIM_FRAME_COUNT = 11
from common.const import uiconst

class StateChangeBaseUI(BasePanel):
    SHOW_HP_PERCENT = 0.4
    HIDE_HP_PERCENT = 0.45
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_change_to_human.OnClick': 'on_click_human_btn',
       'btn_change_to_mech.OnClick': 'on_click_mech_btn'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'summon_call_mecha': {'node': ['btn_change_to_human.temp_pc', 'btn_change_to_mech.temp_pc']}}
    GLOBAL_EVENT = {'improvise_highlight_reenterable': '_on_play_improvise_highlight_ui_efx'
       }

    def on_init_panel(self):
        from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.init_parameters()
        self.init_custom_com()
        self.frame = 0
        self.hide_ui()
        self.panel.RecordAnimationNodeState('change_to_mech')
        self.panel.RecordAnimationNodeState('renovate')
        self.panel.RecordAnimationNodeState('change_to_man')
        if self.in_improvise_mode:
            ready_left_time = global_data.improvise_battle_data.get_cur_round_ready_left_time()
            if ready_left_time:
                self._on_play_improvise_highlight_ui_efx(ready_left_time)

    @execute_by_mode(True, game_mode_const.Hide_RoleLevel)
    def hide_ui(self):
        self.panel.bar_level.setVisible(False)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel--- This code section failed: ---

  71       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'unbind_ui_event'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  'player'
          12  CALL_FUNCTION_1       1 
          15  POP_TOP          

  72      16  LOAD_CONST            0  ''
          19  LOAD_FAST             0  'self'
          22  STORE_ATTR            1  'player'

  73      25  LOAD_GLOBAL           3  'hasattr'
          28  LOAD_GLOBAL           1  'player'
          31  CALL_FUNCTION_2       2 
          34  POP_JUMP_IF_FALSE    71  'to 71'
          37  LOAD_FAST             0  'self'
          40  LOAD_ATTR             4  'custom_ui_com'
        43_0  COME_FROM                '34'
          43  POP_JUMP_IF_FALSE    71  'to 71'

  74      46  LOAD_FAST             0  'self'
          49  LOAD_ATTR             4  'custom_ui_com'
          52  LOAD_ATTR             5  'destroy'
          55  CALL_FUNCTION_0       0 
          58  POP_TOP          

  75      59  LOAD_CONST            0  ''
          62  LOAD_FAST             0  'self'
          65  STORE_ATTR            4  'custom_ui_com'
          68  JUMP_FORWARD          0  'to 71'
        71_0  COME_FROM                '68'

  76      71  LOAD_GLOBAL           6  'global_data'
          74  LOAD_ATTR             7  'ui_mgr'
          77  LOAD_ATTR             8  'close_ui'
          80  LOAD_CONST            2  'MechaSummonUI'
          83  CALL_FUNCTION_1       1 
          86  POP_TOP          

  77      87  LOAD_FAST             0  'self'
          90  LOAD_ATTR             9  'release_ani_timer'
          93  CALL_FUNCTION_0       0 
          96  POP_TOP          
          97  LOAD_CONST            0  ''
         100  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 31

    def init_parameters(self):
        self.show_once_ex_privilege = True
        self.speed_rate = 1
        self.cd_type = None
        self._move_ani_timer = None
        self.last_mecha_btn_pos = None
        self.count_down = 0
        self.cd_type = mconst.RECALL_CD_TYPE_GETMECHA
        self.cd_timer = None
        self.is_changing = False
        self.mecha_state = False
        self.mecha_hp, self.mecha_hp_max = (0, 0)
        self.cur_mecha_lv = 1
        self.panel.nd_change_to_mech.SetEnableCascadeOpacityRecursion(True)
        self._cur_recall_time = 0
        self.player = None
        self._cur_hp_percent = 0
        self.level = 0
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        self.show_charge = False
        self.camp_id = None
        emgr.update_camp_occupy_info += self.king_boost_charge
        self.in_exercise = global_data.game_mode.get_mode_type() == game_mode_const.GAME_MODE_EXERCISE
        self.in_improvise_mode = global_data.game_mode.get_mode_type() == game_mode_const.GAME_MODE_IMPROVISE
        self.in_concert_mode = global_data.game_mode.get_mode_type() == game_mode_const.GAME_MODE_CONCERT
        self.spectate_target = None
        self._has_charging_buff = False
        self._has_charger_stub = False
        if global_data.player and global_data.player.logic:
            self.spectate_target = global_data.player.logic.ev_g_spectate_target()
        if self.spectate_target and self.spectate_target.logic:
            self.on_player_setted(self.spectate_target.logic)
        elif player:
            self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted
        emgr.scene_observed_player_setted_event += self.on_player_setted
        econf = {'on_observer_hp_change_event': self.on_observe_hp_change,
           'on_observer_charging_event': self.on_observer_charging
           }
        emgr.bind_events(econf)
        return

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        self.panel.StopAnimation('change_to_mech', True)
        if player:
            self.init_event()
            self.bind_ui_event(self.player)
            global_data.emgr.on_init_state_change_ui.emit()
        elif self.cd_timer:
            self.panel.nd_useless.stopAction(self.cd_timer)
            self.cd_timer = None
        if global_data.player and global_data.player.logic and global_data.cam_lplayer and global_data.cam_lplayer != global_data.player.logic:
            self.panel.SetTouchEnabledRecursion(False)
        return

    def on_change_state(self, mecha_state=True):
        if mecha_state:
            self.check_show_nd_guide()
        self.mecha_state = mecha_state
        if mecha_state:
            self.check_hp_percent(False)
        else:
            self.hide_low_hp_hint()
        self.is_changing = False
        has_mecha_bound = True
        if self.player:
            has_mecha_bound = bool(self.player.ev_g_get_fixed_mecha())
        if self.in_improvise_mode:
            has_mecha_bound = True
        mecha = global_data.mecha
        self.panel.StopAnimation('change_to_mech')
        self.panel.StopAnimation('change_to_man')
        self.release_ani_timer()
        if mecha_state:
            self.panel.RecoverAnimationNodeState('change_to_mech')
        else:
            self.panel.RecoverAnimationNodeState('change_to_man')
        if not has_mecha_bound:
            self.panel.btn_change_to_human.setVisible(mecha_state)
            self.panel.btn_change_to_mech.setVisible(False)
        else:
            self.panel.btn_change_to_human.setVisible(mecha_state)
            self.panel.btn_change_to_mech.setVisible(not mecha_state)
        self.mecha_ok(not self.cd_timer and not self.mecha_state)
        if self.mecha_state:
            self.on_hp_changed(0, 0)
        else:
            self.on_mecha_hp_changed(self.mecha_hp, self.mecha_hp_max)
        if self.mecha_state:
            if self.player and self.player.ev_g_mecha_recall_times() == 1 and self._cur_recall_time == 0 and not global_data.is_in_judge_camera:
                self.panel.PlayAnimation('show_2')
                global_data.emgr.play_virtual_anchor_voice.emit('vo9')
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH) and self.player and self.player.ev_g_get_state(ST_MECH_EJECTION):
            self.panel.btn_change_to_mech.setVisible(False)
        self.process_local_battle_btn_visible()

    def init_event(self):
        self.count_down = 0
        bind_mecha_id = self.player.ev_g_get_bind_mecha()
        self.set_bind_mecha(self.player.ev_g_get_bind_mecha_type())
        from mobile.common.EntityManager import EntityManager
        cont_mecha = EntityManager.getentity(bind_mecha_id)
        control_target = self.player.ev_g_control_target()
        mecha_state = control_target and control_target.logic and control_target.logic.sd.ref_is_mecha and not control_target.logic.ev_g_is_mechatran()
        cur_hp, max_hp, cur_shield, max_shield = self.player.ev_g_mecha_hp_init()
        if max_hp <= 0:
            cur_hp, max_hp = (100, 100)
        if not mecha_state and cont_mecha and cont_mecha.logic:
            cur_hp = cont_mecha.logic.share_data.ref_hp
            max_hp = cont_mecha.logic.share_data.ref_max_hp
            cur_shield = cont_mecha.logic.ev_g_shield()
            max_shield = cont_mecha.logic.ev_g_max_shield()
        self.on_change_state(mecha_state is True)
        cd_type, total_cd, left_time = self.player.ev_g_get_change_state()
        self.on_mecha_hp_changed(cur_hp + cur_shield, max_hp + max_shield)
        self.on_update_change_cd(cd_type, total_cd, left_time)
        mecha_exp = self.player.ev_g_attr_get('mecha_exp', 0) or self.player.ev_g_mecha_exp_init()
        self.on_mecha_exp_changed(mecha_exp)
        self._cur_recall_time = self.player.ev_g_mecha_recall_times()
        if self.mecha_state:
            self.on_hp_changed(None, None)
        self.camp_id = self.player.ev_g_camp_id()
        self.king_boost_charge()
        flag = True if global_data.game_mode and global_data.game_mode.is_ace_coin_enable() else False
        self.panel.lab_level.setVisible(flag)
        self.level = self.player.ev_g_attr_get('driver_level') or 0
        self.on_player_level_changed(self.level)
        return

    def bind_ui_event(self, target):
        regist_func = target.regist_event
        regist_func('E_FIGHT_STATE_CHANGED', self.on_change_state)
        regist_func('E_STATE_CHANGE_CD', self.on_update_change_cd)
        regist_func('E_RECALL_SUCESS', self.on_recall_result)
        regist_func('E_HEALTH_HP_CHANGE', self.on_hp_changed)
        regist_func('E_ON_JOIN_MECHA', self.on_join_mecha)
        regist_func('E_ON_LEAVE_MECHA', self.on_leave_mecha)
        regist_func('E_MECHA_EXP_CHANGE', self.on_mecha_exp_changed)
        regist_func('E_PLAYER_LEVEL_UP', self.on_player_level_changed)
        regist_func('S_CALL_MECHA_SPEED_RATE', self.set_speed_rate)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
            unregist_func('E_FIGHT_STATE_CHANGED', self.on_change_state)
            unregist_func('E_STATE_CHANGE_CD', self.on_update_change_cd)
            unregist_func('E_RECALL_SUCESS', self.on_recall_result)
            unregist_func('E_HEALTH_HP_CHANGE', self.on_hp_changed)
            unregist_func('E_ON_JOIN_MECHA', self.on_join_mecha)
            unregist_func('E_ON_LEAVE_MECHA', self.on_leave_mecha)
            unregist_func('E_MECHA_EXP_CHANGE', self.on_mecha_exp_changed)
            unregist_func('E_PLAYER_LEVEL_UP', self.on_player_level_changed)
            unregist_func('S_CALL_MECHA_SPEED_RATE', self.set_speed_rate)

    def on_join_mecha(self, *args):
        self.switch_call_mecha()
        self.set_human_btn_selected(False)

    def ex_privilege_call_mecha(self):
        from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        from logic.gutils.item_utils import get_lobby_item_name
        mecha_item_no = battle_id_to_mecha_lobby_id(int(global_data.cam_lplayer.ev_g_get_bind_mecha_type()))
        item = global_data.player.get_item_by_no(mecha_item_no)
        clothing = item.get_fashion()
        mecha_skin = clothing.get(FASHION_POS_SUIT)
        import logic.gcommon.common_utils.bcast_utils as bcast
        info = (get_text_by_id(634776).format(playername=global_data.cam_lplayer.ev_g_char_name(), itemtype=get_lobby_item_name(mecha_skin)), mecha_skin, {})
        global_data.emgr.battle_broadcast_event.emit(*info)
        global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_BATTLE_BROADCAST, info])

    def on_leave_mecha(self, *args):
        if not (self.panel and self.panel.isValid()):
            return
        else:
            is_bind_mecha = bool(self.player.ev_g_get_fixed_mecha())
            if self.panel is not None:
                if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH):
                    if not (self.player and self.player.ev_g_get_state(ST_MECH_EJECTION)):
                        self.panel.PlayAnimation('change_to_mech')
                elif is_bind_mecha:
                    self.panel.PlayAnimation('change_to_mech')
                self.switch_call_mecha()
                cur_hp, max_hp, cur_shield, max_shield = self.player.ev_g_mecha_hp_init()
                self.on_mecha_hp_changed(cur_hp + cur_shield, max_hp + max_shield)
            return

    def switch_call_mecha(self, *args):
        if not self.player:
            return
        mecha_type = self.player.ev_g_get_bind_mecha_type()
        self.set_bind_mecha(mecha_type)

    def mecha_ok(self, is_ok):
        pass

    def is_change_btn_clickable(self):
        if not self.player:
            return False
        if self.spectate_target:
            return False
        if self.is_changing:
            return False
        is_share = global_data.mecha and global_data.mecha.is_share()
        if self.count_down > 0 and not is_share:
            global_data.emgr.battle_show_message_event.emit(get_text_by_id(18165))
            return False
        if global_data.player.in_local_battle():
            from logic.gcommon.common_const import mecha_const
            cd_type, total_cd, left_time = self.player.ev_g_get_change_state()
            if cd_type == mecha_const.RECOVER_CD_TYPE_DISABLE:
                global_data.game_mgr.show_tip(get_text_by_id(1018))
                return False
        return True

    def set_human_btn_selected(self, flag):
        if flag:
            path = 'gui/ui_res_2/battle/mech_main/btn_mech_change_2.png'
        else:
            path = 'gui/ui_res_2/battle/mech_main/btn_mech_change.png'
        self.panel.img_bg.SetDisplayFrameByPath('', path)

    def on_click_human_btn(self, btn, touch, *args):
        if not self.is_change_btn_clickable():
            return
        mecha = global_data.mecha
        if mecha and mecha.logic:
            if mecha.is_share() and mecha.logic.ev_g_is_diving():
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(19755))
                return
            if mecha.logic.ev_g_is_mechatran():
                return
            if not mecha.logic.ev_g_status_check_pass(mecha_status_config.MC_DRIVER_LEAVING):
                return
            if not mecha.logic.ev_g_on_ground():
                return
            self.is_changing = True
            if self.player and self.player.ev_g_in_mecha():
                self.player.send_event('E_TRY_LEAVE_MECHA')
            if not mecha.is_share():
                self.mecha_ok(False)
                self.set_human_btn_selected(True)

                def cb(*args):
                    if self and self.is_valid():
                        if self.count_down > 0:
                            self.panel.nd_useless.setVisible(True)

                self.panel.DelayCall(self.panel.GetAnimationMaxRunTime('change_to_mech'), cb)
            self.hide_nd_guide()
            global_data.emgr.try_leave_mecha_in_local_editor.emit()

    def on_click_mech_btn(self, btn, touch, *args):
        if not self.is_change_btn_clickable():
            return
        else:
            if self.in_concert_mode and global_data.battle and not global_data.battle.is_wait_player():
                return
            if self.in_improvise_mode and not global_data.player.logic.ev_g_get_bind_mecha():
                bind_mecha_type = global_data.improvise_battle_data.get_cur_round_mecha_type_id()
                if bind_mecha_type:
                    from logic.gutils.mecha_utils import try_call_mecha_in_mecha_trans, summon_mecha_call_back
                    try_call_mecha_in_mecha_trans(self.player, lambda ui_obj=self, call_mecha_id=bind_mecha_type, force=False, valid_pos=None: summon_mecha_call_back(ui_obj, call_mecha_id, force, valid_pos))
                    return
            from logic.gutils.mecha_utils import try_call_mecha_in_mecha_trans
            self.is_changing = try_call_mecha_in_mecha_trans(self.player, self.try_call_mecha)
            return

    def try_call_mecha(self, force=False, valid_pos=None):
        if not self or not self.is_valid() or not self.player or not self.player.is_valid():
            return False
        else:
            from logic.gutils.mecha_utils import CallMecha
            near = 2.5 * NEOX_UNIT_SCALE if force else None
            if valid_pos:
                res, pos = True, valid_pos
            else:
                res, pos = CallMecha(near)
            if res:
                if not self.player.ev_g_status_check_pass(ST_MECHA_BOARDING) and not force:
                    global_data.emgr.battle_show_message_event.emit(get_text_by_id(18164))
                    return False
                self.player.send_event('E_LEAVE_ATTACHABLE_ENTITY')
                ui = global_data.ui_mgr.get_ui('AttachableDriveUI')
                if ui:
                    ui.close()
                self.player.send_event('E_CTRL_STAND', is_break_run=False)
                self.player.ev_g_status_try_trans(ST_MECHA_BOARDING, force=force)
                yaw = self.player.ev_g_yaw()
                global_data.emgr.enable_camera_yaw.emit(False)
                self.player.send_event('E_CALL_SYNC_METHOD', 'try_recall', ((pos.x, pos.y, pos.z), yaw), True)
                self.is_changing = True
                if self.cd_type != mconst.RECOVER_CD_TYPE_DISABLE:
                    self.play_move_animation()
                    self.panel.PlayAnimation('change_to_man')
                global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                       'mecha_confirm'))
                global_data.emgr.try_summon_mecha_in_local_editor.emit(self.player.ev_g_get_bind_mecha_type(), (pos.x, pos.y, pos.z))
                is_in_island = global_data.battle and global_data.battle.is_in_island()
                if is_in_island and self.show_once_ex_privilege:
                    self.show_once_ex_privilege = False
                    self.ex_privilege_call_mecha()
                return True
            global_data.emgr.battle_show_message_event.emit(get_text_by_id(18074))
            self.is_changing = False
            return False
            return

    def on_update_change_cd(self, cd_type, total_cd, left_time):
        self.cd_type = cd_type
        self.panel.nd_useless.setVisible(False)

        def reset():
            if self and self.is_valid():
                self.count_down = 0
                self.panel.nd_useless.setVisible(False)
                self.panel.icon_small_2.setVisible(True)
                self.panel.img_lock.setVisible(False)
                self.panel.StopAnimation('lock')
                self.panel.lab_unable.setVisible(False)
                self.mecha_ok(True)
                if cd_type == mconst.RECALL_CD_TYPE_DIE:
                    self.panel.mech_hp.SetPercent(100)
                if self.cd_timer:
                    self.panel.nd_useless.stopAction(self.cd_timer)
                    self.cd_timer = None
                self.panel.PlayAnimation('enable')
            return

        if cd_type != mconst.RECALL_CD_TYPE_GETMECHA:
            if cd_type == mconst.RECOVER_CD_TYPE_DISABLE:
                self.panel.PlayAnimation('lock')
                ui_effect.set_gray(self.panel.nd_change_to_mech, True)
            else:
                self.panel.icon_small_2.setVisible(True)
                self.panel.img_lock.setVisible(False)
                ui_effect.set_gray(self.panel.nd_change_to_mech, False)
                self.panel.lab_unable.setVisible(False)
            if total_cd <= 0:
                if cd_type == mconst.RECALL_CD_TYPE_DIE:
                    self.panel.mech_hp.SetPercent(100)
                    reset()
                self.panel.icon_small_2.setVisible(True)
                self.panel.img_lock.setVisible(False)
                return

            def cb(dt):
                mecha = global_data.mecha
                is_share = mecha and mecha.is_share()
                self.panel.nd_useless.setVisible(not is_share)
                self.count_down = left_time - dt
                self.panel.lab_cd.SetString('%.1f' % self.count_down)
                self.panel.cd.SetPercentage(self.count_down * 100.0 / total_cd)
                if cd_type == mconst.RECALL_CD_TYPE_DIE and not is_share:
                    self.panel.mech_hp.SetPercent((total_cd - self.count_down) * 100.0 / total_cd)
                if self.count_down <= 0:
                    reset()

            self.cd_type = cd_type
            self.count_down = left_time
            if self.cd_timer:
                self.panel.nd_useless.stopAction(self.cd_timer)
                self.cd_timer = None
            if left_time > 0:
                self.cd_timer = self.panel.nd_useless.TimerAction(cb, left_time, reset, interval=0.05)
                cb(0)
            elif cd_type == mconst.RECALL_CD_TYPE_DIE:
                self.panel.mech_hp.SetPercent(100)
                self.panel.icon_small_2.setVisible(True)
                self.panel.img_lock.setVisible(False)
            elif cd_type != mconst.RECOVER_CD_TYPE_DISABLE:
                self.panel.icon_small_2.setVisible(True)
                self.panel.img_lock.setVisible(False)
            self.panel.nd_useless.setVisible(left_time > 0)
            self.mecha_ok(not self.cd_timer and not self.mecha_state)
        return

    def on_mecha_hp_changed(self, cur_hp, max_hp):
        if max_hp <= 0:
            return
        if self.player:
            ret = self.player.ev_g_get_change_state()
            if ret:
                cd_type, total_cd, left_time = ret
                if cd_type == mconst.RECALL_CD_TYPE_DIE:
                    if left_time <= 0:
                        self.panel.mech_hp.SetPercent(100)
                    return
        self.mecha_hp, self.mecha_hp_max = cur_hp, max_hp
        if not self.mecha_state:
            self.panel.mech_hp.SetPath('', 'gui/ui_res_2/battle/progress/hp_btn_mech_100.png')
            self.panel.mech_hp.SetPercent(0)
            self.panel.mech_hp.SetPercent(cur_hp * 100.0 / max_hp)

    def set_mecha_hp(self, percent):
        if self.cd_type == mconst.RECALL_CD_TYPE_NORMAL:
            percent = min(100, max(0, percent))
            self.panel.mech_hp.SetPercent(percent)

    def on_mecha_exp_changed(self, mecha_exp):
        from logic.gutils import mecha_utils
        self.cur_mecha_lv = mecha_utils.get_mecha_cur_lv(mecha_exp, self.cur_mecha_lv)

    def on_player_level_changed(self, level, *args):
        self.panel.lab_level.SetString('Lv' + str(level))
        if level == driver_lv_data.MAX_DRIVER_LEVEL:
            self.panel.lab_level.SetColor('#SO')
        if level > self.level:
            self.panel.PlayAnimation('level_up')
        self.level = level

    def on_hp_changed(self, hp, mod):
        if self.mecha_state and self.player and self.player.is_valid():
            percent = self.player.ev_g_health_percent() * 100
            dis_percent = 100 if percent > 75 else (75 if percent > 25 else 25)
            self.panel.people_hp.SetPath('', 'gui/ui_res_2/battle/progress/hp_btn_human_{}.png'.format(dis_percent))
            self.panel.people_hp.SetPercent(0)
            self.panel.people_hp.SetPercent(percent)

    def on_cancel_enter_mecha(self, *args):
        self.is_changing = False
        self.panel.StopAnimation('change_to_mech', True)

    def on_recall_result(self, ret, err_code=None):
        self.is_changing = ret or False
        self.on_change_state(False)
        if err_code and err_code > 0:
            err_code = err_code if 1 else 18165
            global_data.emgr.battle_show_message_event.emit(get_text_by_id(err_code))

    def check_hp_percent(self, need_check_last=True):
        if self.player:
            if self.player.ev_g_is_in_spectate():
                return
            new_percent = self.player.ev_g_health_percent() or 0
            if need_check_last and self._cur_hp_percent:
                if self._cur_hp_percent >= self.SHOW_HP_PERCENT > new_percent:
                    self.show_low_hp_hint()
            elif new_percent < self.SHOW_HP_PERCENT:
                self.show_low_hp_hint()
            if new_percent >= self.HIDE_HP_PERCENT:
                self.hide_low_hp_hint()
            self._cur_hp_percent = new_percent

    def show_low_hp_hint(self):
        if self.player:
            self.set_role_pic(self.player.ev_g_role_id(), True)

    def hide_low_hp_hint(self):
        if self.player:
            self.set_role_pic(self.player.ev_g_role_id(), False)

    def set_role_pic(self, role_id, is_in_danger):
        if not role_id:
            return
        key = 'mech_call_low_hp_icon' if is_in_danger else 'mech_call_icon'
        pic_path = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), key) or ''
        self.panel.img_change_to_man.SetDisplayFrameByPath('', pic_path)

    def on_observe_hp_change(self, hp, mod):
        self.check_hp_percent()

    def on_observer_charging(self, is_on_charging, bf_data):
        if is_on_charging:
            self.panel.PlayAnimation('charge')
            charging_total_progress = calc_mecha_acc_charing_target_progress(self.player, bf_data, self.speed_rate)
            if charging_total_progress > 0:
                self.panel.mech_full.setVisible(True)
                self.panel.mech_full.SetPercent(charging_total_progress)
                self._has_charging_buff = True
            if not bf_data:
                self._has_charger_stub = True
        else:
            if not bf_data:
                self._has_charger_stub = False
            else:
                self._has_charging_buff = False
            if not self._has_charging_buff and not self._has_charger_stub:
                self.panel.StopAnimation('charge')
            self.panel.nd_charge_vx.setVisible(False)
            if not self._has_charging_buff:
                self.panel.mech_full.setVisible(False)

    def set_speed_rate(self, rate):
        self.speed_rate = rate

    def set_bind_mecha(self, mecha_id):
        if not mecha_id:
            return
        from logic.gutils.item_utils import get_mecha_role_pic
        pic_path = get_mecha_role_pic(mecha_id, True)
        self.panel.nd_change_to_mech.SetDisplayFrameByPath('', pic_path)

    def king_boost_charge(self):
        if global_data.game_mode.get_mode_type() != 'king' or not self.player or self.camp_id is None:
            return
        else:
            level_condition = global_data.king_battle_data.camp[self.camp_id].occupy_num > 0
            cd_condition = self.cd_type == mconst.RECALL_CD_TYPE_DIE and self.count_down > 0
            show_charge = not self.mecha_state and cd_condition and level_condition
            if self.show_charge ^ show_charge:
                self.on_observer_charging(show_charge, None)
                self.show_charge = show_charge
            return

    def release_ani_timer(self):
        if self._move_ani_timer:
            global_data.game_mgr.unregister_logic_timer(self._move_ani_timer)
            self._move_ani_timer = None
        if self.last_mecha_btn_pos:
            self.panel.nd_change_mech_custom.setPosition(cc.Vec2(self.last_mecha_btn_pos.x, self.last_mecha_btn_pos.y))
            self.last_mecha_btn_pos = None
        return

    def play_move_animation(self):
        self.release_ani_timer()
        end_pos = self.panel.nd_change_custom.getPosition()
        end_pos = math3d.vector(end_pos.x, end_pos.y, 0)
        init_pos = self.panel.nd_change_mech_custom.getPosition()
        last_mecha_btn_pos = math3d.vector(init_pos.x, init_pos.y, 0)
        move_vec = end_pos - last_mecha_btn_pos
        start_time = global_data.game_time

        def move_animation--- This code section failed: ---

 702       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'panel'
           6  JUMP_IF_FALSE_OR_POP    21  'to 21'
           9  LOAD_DEREF            0  'self'
          12  LOAD_ATTR             0  'panel'
          15  LOAD_ATTR             1  'isValid'
          18  CALL_FUNCTION_0       0 
        21_0  COME_FROM                '6'
          21  POP_JUMP_IF_TRUE     28  'to 28'

 703      24  LOAD_GLOBAL           2  'RELEASE'
          27  RETURN_END_IF    
        28_0  COME_FROM                '21'

 704      28  LOAD_GLOBAL           3  'global_data'
          31  LOAD_ATTR             4  'game_time'
          34  LOAD_DEREF            1  'start_time'
          37  BINARY_SUBTRACT  
          38  STORE_FAST            0  'pass_time'

 705      41  LOAD_DEREF            0  'self'
          44  LOAD_ATTR             5  'last_mecha_btn_pos'
          47  LOAD_DEREF            2  'move_vec'
          50  LOAD_FAST             0  'pass_time'
          53  BINARY_MULTIPLY  
          54  BINARY_ADD       
          55  STORE_FAST            1  'cur_pos'

 706      58  LOAD_DEREF            0  'self'
          61  LOAD_ATTR             0  'panel'
          64  LOAD_ATTR             6  'nd_change_mech_custom'
          67  LOAD_ATTR             7  'setPosition'
          70  LOAD_GLOBAL           8  'cc'
          73  LOAD_ATTR             9  'Vec2'
          76  LOAD_FAST             1  'cur_pos'
          79  LOAD_ATTR            10  'x'
          82  LOAD_FAST             1  'cur_pos'
          85  LOAD_ATTR            11  'y'
          88  CALL_FUNCTION_2       2 
          91  CALL_FUNCTION_1       1 
          94  POP_TOP          

 707      95  POP_TOP          
          96  POP_TOP          
          97  POP_TOP          
          98  COMPARE_OP            5  '>='
         101  POP_JUMP_IF_FALSE   151  'to 151'

 708     104  LOAD_DEREF            0  'self'
         107  LOAD_ATTR             0  'panel'
         110  LOAD_ATTR             6  'nd_change_mech_custom'
         113  LOAD_ATTR             7  'setPosition'
         116  LOAD_GLOBAL           8  'cc'
         119  LOAD_ATTR             9  'Vec2'
         122  LOAD_DEREF            0  'self'
         125  LOAD_ATTR             5  'last_mecha_btn_pos'
         128  LOAD_ATTR            10  'x'
         131  LOAD_DEREF            0  'self'
         134  LOAD_ATTR             5  'last_mecha_btn_pos'
         137  LOAD_ATTR            11  'y'
         140  CALL_FUNCTION_2       2 
         143  CALL_FUNCTION_1       1 
         146  POP_TOP          

 709     147  LOAD_GLOBAL           2  'RELEASE'
         150  RETURN_END_IF    
       151_0  COME_FROM                '101'

Parse error at or near `POP_TOP' instruction at offset 95

        self._move_ani_timer = global_data.game_mgr.register_logic_timer(move_animation, interval=1, times=-1)
        self.last_mecha_btn_pos = last_mecha_btn_pos

    def _on_play_improvise_highlight_ui_efx(self, duration):
        if not hasattr(self.panel, 'renovate') or not self.panel.renovate:
            return
        delay_tag = 31415926
        self.panel.renovate.stopActionByTag(delay_tag)
        self.panel.StopAnimation('renovate')
        self.panel.PlayAnimation('renovate')

        def cb():
            self.panel.StopAnimation('renovate')
            self.panel.RecoverAnimationNodeState('renovate')

        self.panel.renovate.DelayCallWithTag(duration, cb, delay_tag)

    def check_show_nd_guide(self):
        if global_data.is_pc_mode:
            return
        self.hide_nd_guide()
        if global_data.player and global_data.player.in_local_battle():
            return
        if not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            return
        if not global_data.player or not global_data.player.logic:
            return
        if global_data.player.logic.ev_g_spectate_target():
            return
        battle_times = global_data.player.get_total_cnt()
        if battle_times > 1:
            return
        is_first_calling = global_data.player.logic.ev_g_is_first_calling()
        if not is_first_calling:
            return
        global_data.player.logic.send_event('E_SET_IS_FIRST_CALLING', False)
        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(60.0),
         cc.CallFunc.create(lambda : self.show_nd_guide()),
         cc.DelayTime.create(5.0),
         cc.CallFunc.create(lambda : self.hide_nd_guide())]))

    def hide_nd_guide(self):
        if not self.panel.nd_guide.isVisible():
            return
        self.panel.nd_guide.setVisible(False)
        if self.panel.IsPlayingAnimation('change_player'):
            self.panel.StopAnimation('change_player')

    def show_nd_guide(self):
        if not self.player:
            return
        if not self.player.ev_g_in_mecha('Mecha'):
            return
        self.panel.nd_guide.setVisible(True)
        if not self.panel.IsPlayingAnimation('change_player'):
            self.panel.PlayAnimation('change_player')

    def show_guide_mecha_call_disable_tip(self):
        if self.cd_timer:
            self.panel.nd_useless.stopAction(self.cd_timer)
            self.cd_timer = None
        self.count_down = 0
        self.on_update_change_cd(mconst.RECOVER_CD_TYPE_DISABLE, 0, 0)
        self.panel.nd_guide_mech.setVisible(True)
        self.panel.PlayAnimation('show_guide')
        return

    def hide_guide_mecha_call_disable_tip(self):
        self.panel.StopAnimation('show_guide')
        self.panel.nd_guide_mech.setVisible(False)

    def set_change_state_btn_visible(self, visible_to_human, visible_to_mech):
        self.panel.btn_change_to_human.setVisible(visible_to_human)
        self.panel.btn_change_to_mech.setVisible(visible_to_mech)

    def process_local_battle_btn_visible(self):
        if not global_data.player or not global_data.player.logic:
            return
        global_data.player.logic.send_event('E_GUIDE_MECHA_STATE_CHANGE')
        if not global_data.player.in_local_battle():
            return
        if not global_data.battle:
            return
        battle_type = global_data.battle.get_battle_tid()
        if battle_type in [NEWBIE_STAGE_HUMAN_BATTLE]:
            self.panel.btn_change_to_human.setVisible(False)
            self.panel.btn_change_to_mech.setVisible(False)
        elif battle_type == NEWBIE_STAGE_MECHA_BATTLE:
            visible_to_human, visible_to_mecha = global_data.player.logic.ev_g_guide_statechange_visible()
            self.panel.btn_change_to_human.setVisible(visible_to_human)
            self.panel.btn_change_to_mech.setVisible(visible_to_mecha)

    def on_change_ui_custom_data(self):
        ui = global_data.ui_mgr.get_ui('GuideUI')
        if ui:
            param = self.change_ui_data()
            ui.on_change_ui_inform_guide_mixed(param)

    def change_ui_data(self):
        scale_type_adjust_list = []
        pos_type_adjust_list = []
        need_to_adjust_scale_type_nodes = (('nd_change_custom', 'nd_getoff_mech', None), )
        for source_nd_name, target_nd_name, target_scale_nd_name in need_to_adjust_scale_type_nodes:
            nd = getattr(self.panel, source_nd_name)
            w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
            scale = nd.getScale()
            scale_type_adjust_list.append((w_pos, scale, target_nd_name, target_scale_nd_name))

        ret_dict = {'scale_type': scale_type_adjust_list,
           'pos_type': pos_type_adjust_list
           }
        return ret_dict


class StateChangeUI(StateChangeBaseUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_mech_change'