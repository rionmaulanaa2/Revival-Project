# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8029.py
from __future__ import absolute_import
import math3d
import world
import math
import time
from .StateBase import StateBase
from .ShootLogic import Reload
from common.utils.timer import CLOCK
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import UP_BODY, LOW_BODY
from logic.gcommon.common_const.mecha_const import MECHA_8029_FORM_HUNT, MECHA_8029_FORM_SCOUT
from .ShootLogic import AccumulateShoot
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN3, SOUND_TYPE_MECHA_FOOTSTEP
from .ShootLogic import WeaponFire
from common.cfg import confmgr
from .Logic8009 import Run8009
from logic.gcommon import editor
from logic.gcommon.common_utils.bcast_utils import E_SWITCH_WEAPON, E_EXECUTE_MECHA_ACTION_SOUND
from logic.gcommon.common_const.ui_operation_const import SHOTGUN_FIRE_ON_RELEASE_8029, SHOTGUN_FIRE_ON_NOT_AUTO_8029, TRANSLATION_USE_PHANTOM_FORWARD_8029
from logic.comsys.battle.BattleUtils import can_fire
from logic.comsys.control_ui.ShotChecker import ShotChecker
from logic.gutils.mecha_utils import get_mecha_call_pos
from logic.gcommon import time_utility as tutil
from logic.client.const import camera_const

class Run8029(Run8009):

    def begin_run_anim(self):
        self.enter_state_running_time_stamp = time.time()
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        if self.forbid_default_up_body_anim:
            if self.ev_g_is_showing_default_up_body_anim():
                self.send_event('E_POST_ACTION', self.run_anim, UP_BODY, 7, loop=True, ignore_sufix=self.run_ignore_sufix, keep_phase=True)
            if not self.keep_default_up_body_anim:
                self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', self.run_anim, 7)
        self.send_event('E_POST_ACTION', self.run_anim, LOW_BODY, self.run_anim_dir_type, loop=True, ignore_sufix=self.run_ignore_sufix, yaw_list=self.run_anim_yaw_list, keep_phase=True)
        self.sd.ref_is_in_run = True

    def exit(self, enter_states):
        super(Run8029, self).exit(enter_states)
        self.sd.ref_is_in_run = False


@editor.state_exporter({('max_aim_time_after_fire', 'param'): {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe5\x90\x8e\xe4\xbf\x9d\xe6\x8c\x81aim\xe5\x8a\xa8\xe4\xbd\x9c\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe6\x97\xb6\xe9\x95\xbf'}})
class WeaponFire8029(WeaponFire):
    BIND_EVENT = WeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'G_CHECK_CONTINUE_FIRE': 'check_can_continue_fire'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        global_data.emgr.update_shotgun_fire_on_release_8029 += self.on_update_shotgun_on_release
        global_data.emgr.update_shotgun_fire_not_auto_8029 += self.on_update_shotgun_on_not_auto
        super(WeaponFire8029, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.sd.ref_hold_aim = False
        self.sd.ref_cur_state = bdict.get('shape_form', MECHA_8029_FORM_SCOUT)

    def destroy(self):
        global_data.emgr.update_shotgun_fire_on_release_8029 -= self.on_update_shotgun_on_release
        global_data.emgr.update_shotgun_fire_not_auto_8029 -= self.on_update_shotgun_on_not_auto
        super(WeaponFire8029, self).destroy()

    def read_data_from_custom_param(self):
        super(WeaponFire8029, self).read_data_from_custom_param()
        self.max_aim_time_after_fire = self.custom_param.get('max_aim_time_after_fire', 5.0)
        self.is_replace_stand_and_shoot_anim = self.custom_param.get('is_replace_stand_and_shoot_anim', False)
        self.replace_anim = self.custom_param.get('replace_anim', 'shotgun_aim')
        if self.sd.ref_cur_state == MECHA_8029_FORM_SCOUT:
            self.auto_fire = True
            self.fire_on_release = False
        else:
            self.auto_fire = not global_data.player.get_setting_2(SHOTGUN_FIRE_ON_NOT_AUTO_8029)
            self.fire_on_release = not self.auto_fire and global_data.player.get_setting_2(SHOTGUN_FIRE_ON_RELEASE_8029)

    def enter(self, leave_states):
        super(WeaponFire8029, self).enter(leave_states)
        if self.is_replace_stand_and_shoot_anim:
            self.send_event('E_KEEP_AIM', self.replace_anim, True)
        self.sd.ref_hold_aim = True

    def check_can_continue_fire(self):
        if not self.sd.ref_is_robot and (ShotChecker().check_camera_can_shot() or not can_fire()):
            return False
        if self.ev_g_reloading():
            return False
        if self.ev_g_weapon_reloading(self.weapon_pos):
            return False
        if not self.ev_g_is_weapon_enable(self.weapon_pos) or self.ev_g_is_diving():
            return False
        if not self.auto_fire or not self.fire_on_release:
            return False
        return self.ev_g_is_action_down('action1')

    def on_update_shotgun_on_release(self, flag):
        if self.sd.ref_cur_state != MECHA_8029_FORM_HUNT:
            return
        self.fire_on_release = flag and not self.auto_fire

    def on_update_shotgun_on_not_auto(self, flag):
        if self.sd.ref_cur_state != MECHA_8029_FORM_HUNT:
            return
        self.auto_fire = not flag
        self.fire_on_release = flag and not self.auto_fire

    def action_btn_down(self, ignore_reload=False):
        if not self.sd.ref_is_robot and (ShotChecker().check_camera_can_shot() or not can_fire()):
            return False
        if self.ev_g_reloading():
            return False
        if self.ev_g_weapon_reloading(self.weapon_pos):
            return False
        self.is_continue_fire = True
        self.want_to_fire = True
        if not self.check_can_active() or not self.ev_g_is_weapon_enable(self.weapon_pos) or self.ev_g_is_diving():
            self.is_continue_fire = False
            self.can_not_fire_attack()
            return False
        if not self.fire_on_release or self.auto_fire:
            if not self.try_weapon_attack_begin():
                self.is_continue_fire = False
                return False
            if self.is_active:
                self.re_enter()
            self.can_fire_attack()
        if not self.is_active:
            self.active_self()
        super(WeaponFire, self).action_btn_down()
        return True

    def action_btn_up(self):
        self.is_continue_fire = False
        self.want_to_fire = False
        if self.fire_on_release and not self.auto_fire:
            if not self.check_can_active() or not self.ev_g_is_weapon_enable(self.weapon_pos) or self.ev_g_is_diving():
                return False
            self.try_weapon_attack_begin()
        if not self.try_weapon_attack_end():
            return False
        super(WeaponFire, self).action_btn_up()
        return True

    def on_fire(self, f_cdtime, weapon_pos, fired_socket_index=None):
        super(WeaponFire8029, self).on_fire(f_cdtime, weapon_pos, fired_socket_index)
        if weapon_pos != self.weapon_pos:
            return
        if self.sd.ref_cur_state == MECHA_8029_FORM_HUNT:
            self.send_event('E_KEEP_AIM', self.replace_anim, False)
            if self.auto_fire:
                self.try_weapon_attack_end()

    def exit(self, enter_states):
        super(WeaponFire8029, self).exit(enter_states)
        self.sd.ref_hold_aim = False
        self.send_event('E_CLEAR_UP_BODY_ANIM')


SWITCH_ICON = {MECHA_8029_FORM_SCOUT: ('gui/ui_res_2/battle/mech_main/icon_mech8029_2_1.png', 'gui/ui_res_2/battle/mech_main/icon_mech8029_1_1.png'),
   MECHA_8029_FORM_HUNT: ('gui/ui_res_2/battle/mech_main/icon_mech8029_2_2.png', 'gui/ui_res_2/battle/mech_main/icon_mech8029_1_2.png')
   }

@editor.state_exporter({('change_time', 'param'): {'zh_name': '\xe6\x8d\xa2\xe6\x9e\xaa\xe6\x97\xb6\xe9\x95\xbf'},('change_anim_rate', 'param'): {'zh_name': '\xe6\x8d\xa2\xe6\x9e\xaa\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x80\x9f\xe7\x8e\x87'}})
class SwitchWeapon8029(StateBase):
    STATE_INFO = {MECHA_8029_FORM_SCOUT: {'weapon_pos': PART_WEAPON_POS_MAIN1,
                               'finish_model_state': 1,
                               'switch_model_state': 5,
                               'switch_model_state_run': 8,
                               'voice': 'm_8029_change_shotgun'
                               },
       MECHA_8029_FORM_HUNT: {'weapon_pos': PART_WEAPON_POS_MAIN3,
                              'finish_model_state': 2,
                              'switch_model_state': 6,
                              'switch_model_state_run': 9,
                              'voice': 'm_8029_change_rifle'
                              }
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(SwitchWeapon8029, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.sd.ref_cur_state = bdict.get('shape_form', MECHA_8029_FORM_SCOUT)
        self.state_anim = ()
        self.is_finish = False

    def on_post_init_complete(self, *args):
        self.on_switch_finish()

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 800951)
        self.change_anim = self.custom_param.get('change_anim', 'rifle_change')
        self.default_up_idle = self.custom_param.get('default_up_idle', 'rifle_idle')
        self.change_time = self.custom_param.get('change_time', 1.0)
        self.change_anim_rate = self.custom_param.get('change_anim_rate', 1.0)
        self.change_anim_run = self.custom_param.get('change_anim_run', 'shotgun_change_run')

    def enter(self, leave_states):
        super(SwitchWeapon8029, self).enter(leave_states)
        self.is_finish = False
        if self.sd.ref_cur_state == MECHA_8029_FORM_SCOUT:
            self.sd.ref_cur_state = MECHA_8029_FORM_HUNT
        else:
            self.sd.ref_cur_state = MECHA_8029_FORM_SCOUT
        self.send_event('E_DO_SKILL', self.skill_id, self.sd.ref_cur_state)
        if self.sd.ref_is_in_run:
            self.send_event('E_REFRESH_WEAPON_STATE', self.STATE_INFO[self.sd.ref_cur_state]['switch_model_state_run'])
            self.send_event('E_POST_ACTION', self.change_anim_run, UP_BODY, 1, timeScale=self.change_anim_rate)
        else:
            self.send_event('E_REFRESH_WEAPON_STATE', self.STATE_INFO[self.sd.ref_cur_state]['switch_model_state'])
            self.send_event('E_POST_ACTION', self.change_anim, UP_BODY, 7, timeScale=self.change_anim_rate)
        self.send_event('E_SWITCH_WEAPON', self.sd.ref_cur_state)
        self.play_sound()
        self.delay_call(self.change_time / self.change_anim_rate, self.on_switch_finish)

    def update(self, dt):
        if self.sd.ref_is_in_run and self.sd.ref_up_body_anim != self.change_anim_run and not self.is_finish:
            self.send_event('E_REFRESH_WEAPON_STATE', self.STATE_INFO[self.sd.ref_cur_state]['switch_model_state_run'])
            self.send_event('E_POST_ACTION', self.change_anim_run, UP_BODY, 1, timeScale=self.change_anim_rate, keep_phase=True, blend_time=0)
        elif not self.sd.ref_is_in_run and self.sd.ref_up_body_anim != self.change_anim and not self.is_finish:
            self.send_event('E_REFRESH_WEAPON_STATE', self.STATE_INFO[self.sd.ref_cur_state]['switch_model_state'])
            self.send_event('E_POST_ACTION', self.change_anim, UP_BODY, 7, timeScale=self.change_anim_rate, keep_phase=True, blend_time=0)
        super(SwitchWeapon8029, self).update(dt)

    def on_switch_finish(self):
        self.is_finish = True
        self.state_anim = (self.change_anim, self.change_anim_run)
        self.send_event('E_REFRESH_STATE_PARAM', self.sd.ref_cur_state)
        self.send_event('E_REFRESH_CUR_WEAPON_BULLET', self.STATE_INFO[self.sd.ref_cur_state]['weapon_pos'])
        self.send_event('E_LOAD_GUN', self.STATE_INFO[self.sd.ref_cur_state]['weapon_pos'])
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_SWITCH_WEAPON, (self.sd.ref_cur_state,)], True)
        self.send_event('E_SET_ACTION_ICON', 'action1', SWITCH_ICON[self.sd.ref_cur_state][1], 'show')
        self.send_event('E_SET_ACTION_ICON', 'action2', SWITCH_ICON[self.sd.ref_cur_state][1], 'show')
        self.send_event('E_SET_ACTION_ICON', 'action3', SWITCH_ICON[self.sd.ref_cur_state][1], 'show')
        self.send_event('E_REFRESH_WEAPON_STATE', self.STATE_INFO[self.sd.ref_cur_state]['finish_model_state'])
        self.is_active and self.disable_self()

    def play_sound(self):
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, (self.STATE_INFO[self.sd.ref_cur_state]['voice'], 'nf'), 0, 1, 1, SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         E_EXECUTE_MECHA_ACTION_SOUND, (1, (self.STATE_INFO[self.sd.ref_cur_state]['voice'], 'nf'), 0, 1, 1, SOUND_TYPE_MECHA_FOOTSTEP)], True)

    def exit(self, enter_states):
        super(SwitchWeapon8029, self).exit(enter_states)
        self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', None)
        if self.sd.ref_up_body_anim in self.state_anim:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        return

    def action_btn_down(self):
        if not self.check_can_active():
            return
        if not self.check_can_cast_skill():
            return
        if self.is_active:
            return
        self.active_self()
        super(SwitchWeapon8029, self).action_btn_down()
        return True

    def refresh_action_param(self, action_param, custom_param):
        super(SwitchWeapon8029, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.read_data_from_custom_param()


class AccumulateShoot8029(AccumulateShoot):
    BIND_EVENT = AccumulateShoot.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ON_TOUCH_GROUND': 'on_touch_ground',
       'E_LOGIC_ON_GROUND': 'on_touch_ground'
       })
    STATE_INFO = {MECHA_8029_FORM_SCOUT: {'show_model_state': 3,
                               'end_model_state': 1
                               },
       MECHA_8029_FORM_HUNT: {'show_model_state': 4,
                              'end_model_state': 2
                              }
       }

    def read_data_from_custom_param(self):
        super(AccumulateShoot8029, self).read_data_from_custom_param()
        self.fire_anim = self.custom_param.get('fire_anim', 'rifle_fire_anim')
        self.fire_time = self.custom_param.get('fire_time', 0.2)
        self.all_up_body_anim.add(self.fire_anim)

    def refresh_action_param(self, action_param, custom_param):
        super(AccumulateShoot8029, self).refresh_action_param(action_param, custom_param)
        self.send_event('E_SWITCH_ACTION_BIND_SKILL_ID', self.bind_action_id, self.skill_id)

    def enter(self, leave_states):
        super(AccumulateShoot8029, self).enter(leave_states)
        if not self.sd.ref_on_ground:
            self.send_event('E_ADD_BLACK_STATE', {MC_MOVE, MC_STAND})
        self.send_event('E_REFRESH_WEAPON_STATE', self.STATE_INFO[self.sd.ref_cur_state]['show_model_state'])
        self.delay_call(self.pre_time, lambda : self.send_event('E_REFRESH_SUB_MODEL_ANIM', 'open', 'rifle_vice_hand'))

    def exit(self, enter_states):
        super(AccumulateShoot8029, self).exit(enter_states)
        self.send_event('E_REFRESH_SUB_MODEL_ANIM', 'close', 'rifle_vice_hand')
        self.send_event('E_REFRESH_WEAPON_STATE', self.STATE_INFO[self.sd.ref_cur_state]['end_model_state'])

    def on_touch_ground(self, *args):
        if not self.is_active:
            return
        self.send_event('E_CLEAR_BLACK_STATE')

    def action_btn_up(self):
        self.btn_down = False
        if self.sub_state == self.SUB_ST_POST:
            super(AccumulateShoot, self).action_btn_cancel()
            return
        if not self.is_active:
            self.need_trigger_up = True
            return False
        if self._force_pre:
            end_pre = self.pre_time < self.elapsed_time
            self.acted = end_pre
        else:
            self.acted = True
        if not self.acted:
            self._skip_acc_state = True
            self.delay_call(self.pre_time - self.elapsed_time, self._fire_action)
        else:
            self._fire_action()
        self.action_hold = False
        super(AccumulateShoot, self).action_btn_up()
        return True

    def _fire_action(self):
        if self.skill_id:
            self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_ACC_SKILL_END')
        self.acc_skill_ended = True
        if self.hover_skill_id:
            self.send_event('E_END_SKILL', self.hover_skill_id)
        self.send_event('E_POST_ACTION', self.fire_anim, UP_BODY, 1, timeScale=1.0)
        self.ev_g_try_weapon_attack_end(self.weapon_pos)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        self.delay_call(self.fire_time, self._post_action)

    def _post_action(self):
        self.acted = True
        self.send_event('E_ENABLE_AIM_IK', False)
        self.send_event('E_REFRESH_SUB_MODEL_ANIM', 'close', 'rifle_vice_hand')
        acc_level, max_level = self.ev_g_accumulate_level(self.weapon_pos)
        post_anim = self.post_anim
        if self.acc_post_anim:
            post_anim = self.acc_post_anim[acc_level]
        if post_anim:
            self.send_event('E_ANIM_RATE', UP_BODY, self.post_anim_rate)
            self.send_event('E_ANIM_RATE', LOW_BODY, self.post_anim_rate)
            self.sub_state = self.SUB_ST_POST
            if self.extern_bone_tree:
                self.send_event('E_POST_EXTERN_ACTION', post_anim, True, subtree=self.extern_bone_tree)
            else:
                if self.use_up_anim_states:
                    self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', self.use_up_anim_states, post_anim, loop=False)
                else:
                    self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, post_anim, loop=False)
                if self.hold_time_scale != 1.0:
                    self.send_event('E_POST_ACTION', post_anim, UP_BODY, 1, timeScale=1.0)
                else:
                    self.send_event('E_POST_ACTION', post_anim, UP_BODY, 1)
                if self.sub_bone_tree:
                    self.send_event('E_POST_EXTERN_ACTION', post_anim, True, subtree=self.sub_bone_tree)
                if not self.use_up_anim_states:
                    self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
            if self.forbid_state:
                self.send_event('E_ADD_BLACK_STATE', self.forbid_state)
                if MC_MOVE in self.forbid_state:
                    self.send_event('E_BRAKE')
            if self.save_gravity != 0.0:
                self.send_event('E_GRAVITY', self.save_gravity)
                self.save_gravity = 0.0
        return


class Phantom(StateBase):
    BIND_EVENT = {'E_UPDATE_USE_STATE': 'on_update_use_state',
       'E_UPDATE_CORE_STATE': 'on_update_core_state',
       'E_UPDATE_PHANTOM_STATE': 'on_update_phantom_state'
       }
    PHANTOM_VOICE = {0: 'm_8029_ray_flash',
       1: 'm_8029_ray_start'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Phantom, self).init_from_dict(unit_obj, bdict, sid, info)
        self.is_wait_translate = False
        self._max_stage = 2
        self._cur_stage = 0
        self._phantom_id = None
        self._last_cast_time = -1
        self.trigger_end_transfrom_timer = None
        self.read_data_from_custom_param()
        return

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 800951)
        skill_conf = confmgr.get('skill_conf', str(self.skill_id))
        ext_info = skill_conf.get('ext_info', {})
        self.trigger_skill_max_duration = ext_info.get('continue_time', 5)
        self.can_translate_duration = self.custom_param.get('can_translate_duration', 1.0)

    def action_btn_down(self):
        if self.is_active:
            return
        if self._cur_stage >= self._max_stage:
            return
        if not self.check_can_active():
            return
        if not self.check_can_cast_skill():
            return
        self.active_self()
        super(Phantom, self).action_btn_down()
        return True

    def enter(self, leave_states):
        super(Phantom, self).enter(leave_states)
        if self._cur_stage == 0:
            self.play_sound(1)
            self._cur_stage += 1
            self.is_wait_translate = True
            self.send_event('E_DO_SKILL', self.skill_id, self._cur_stage, True, None)
            self.on_update_phantom_timer()
            self.delay_call(self.can_translate_duration, self.on_wait_translate)
            self.send_event('E_BEGIN_PHANTIOM_SFX')
        elif self._cur_stage == 1:
            trans = self.translation()
            if trans:
                if self._max_stage == self._cur_stage:
                    self.skill_end()
                else:
                    self.delay_call(self.can_translate_duration, self.on_wait_translate)
        elif self._cur_stage == 2:
            if self._max_stage == self._cur_stage:
                self.disable_self()
            trans = self.translation()
            if trans:
                self.skill_end()
        else:
            self.disable_self()
        return

    def skill_end(self):
        self.clear_timer()
        self.reset_skill()
        self.disable_self()

    def on_wait_translate(self):
        self.is_wait_translate = False
        self.send_event('E_SET_ACTION_ICON', 'action6', 'gui/ui_res_2/battle/mech_main/icon_mech8029_3.png')
        self.disable_self()

    def on_update_use_state(self, stage, last_cast_time=-1):
        self._cur_stage = stage
        self._last_cast_time = last_cast_time
        self.on_update_phantom_timer()

    def on_update_core_state(self, max_stage):
        self._max_stage = max_stage
        if self._max_stage <= self._cur_stage:
            self.skill_end()

    def on_update_phantom_state(self, phantom_id):
        self._phantom_id = phantom_id

    def check_can_translate(self):
        if not self._phantom_id or not global_data.battle:
            return (False, None)
        else:
            phantom_entity = global_data.battle.get_entity(self._phantom_id)
            if phantom_entity and phantom_entity.logic:
                position = phantom_entity.logic.ev_g_position()
                yaw = phantom_entity.logic.ev_g_phantom_yaw()
                ignore_cids = []
                character_cid = phantom_entity.logic.ev_g_character_cid()
                col_cid = phantom_entity.logic.ev_g_cid()
                if character_cid:
                    ignore_cids.append(character_cid)
                if col_cid:
                    ignore_cids.append(col_cid)
                valid, pos = get_mecha_call_pos(position, None, True, ignore_cids=ignore_cids)
                if valid:
                    return (position, yaw)
                else:
                    global_data.emgr.battle_show_message_event.emit(get_text_by_id(83339))
                    return (
                     False, None)

            return (
             False, None)

    def play_sound(self, stage):
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, (self.PHANTOM_VOICE[stage], 'nf'), 0, 1, 1, SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         E_EXECUTE_MECHA_ACTION_SOUND, (1, (self.PHANTOM_VOICE[stage], 'nf'), 0, 1, 1, SOUND_TYPE_MECHA_FOOTSTEP)], True)

    def translation(self):
        trans_pos, yaw = self.check_can_translate()
        if trans_pos is not False:
            self._cur_stage += 1
            self.is_wait_translate = True
            self.play_sound(0)
            self.send_event('E_CANCEL_SUPER_JUMP')
            self.send_event('E_CLEAR_SPEED')
            self.send_event('E_CLEAR_ACC_INFO')
            self.send_event('E_DO_SKILL', self.skill_id, self._cur_stage, True, trans_pos)
            self.send_event('E_UPDATE_TRANSLATION_SFX', trans_pos)
            self.send_event('E_UPDATE_TRANSLATION_SFX', self.ev_g_position())
            if global_data.player and global_data.player.get_setting_2(TRANSLATION_USE_PHANTOM_FORWARD_8029):
                part_ctrl = global_data.game_mgr.scene.get_com('PartCtrl')
                if part_ctrl:
                    part_cam = global_data.game_mgr.scene.get_com('PartCamera')
                    if part_cam:
                        cur_camera_state = part_cam.get_cur_camera_state_type()
                        if cur_camera_state in camera_const.FREE_CAMERA_LIST:
                            global_data.emgr.switch_to_last_camera_state_event.emit()
                    cur_yaw = self.ev_g_yaw() or 0
                    part_ctrl.rotate_camera(yaw - cur_yaw, 0, force=True)
            return True
        else:
            self.disable_self()
            return False

    def on_update_phantom_timer(self):
        self.clear_timer()
        if self._cur_stage == 0 or self._cur_stage == self._max_stage:
            self.reset_skill()
            return
        else:
            self.send_event('E_SHOW_MECHA_LEFT_PROGRESS', None, None, self.trigger_skill_max_duration)
            self.send_event('E_REPLACE_DASH_ICON', 'gui/ui_res_2/battle/mech_main/icon_mech8029_4.png')
            duration = self.trigger_skill_max_duration
            if self._last_cast_time != -1:
                duration = self.trigger_skill_max_duration - (tutil.time() - self._last_cast_time)
            if duration <= 0:
                self.reset_skill()
            else:
                self.trigger_end_transfrom_timer = global_data.game_mgr.register_logic_timer(self.reset_skill, duration, times=1, mode=CLOCK)
            return

    def clear_timer(self):
        if self.trigger_end_transfrom_timer:
            global_data.game_mgr.unregister_logic_timer(self.trigger_end_transfrom_timer)
            self.trigger_end_transfrom_timer = None
        return

    def reset_skill(self):
        skill_obj = self.ev_g_skill(self.skill_id)
        if not skill_obj:
            return
        else:
            self._cur_stage = 0
            self._phantom_id = None
            self._last_cast_time = -1
            self.send_event('E_HIDE_MECHA_LEFT_PROGRESS')
            self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
            self.send_event('E_SET_ACTION_ICON', 'action6', 'gui/ui_res_2/battle/mech_main/icon_mech8029_4.png')
            return

    def destroy(self):
        self.clear_timer()
        super(Phantom, self).destroy()


@editor.state_exporter({('anim_duration', 'param'): {'zh_name': '\xe4\xb8\x8a\xe8\x86\x9b\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x95\xbf'}})
class ShotGunLoad(StateBase):
    BIND_EVENT = {'E_LOADING': 'on_loading',
       'E_SET_START_LOAD_TIME': 'set_start_load_time'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        global_data.emgr.update_shotgun_fire_not_auto_8029 += self.on_update_shotgun_fire_not_auto
        super(ShotGunLoad, self).init_from_dict(unit_obj, bdict, sid, info)
        self.load_time_manual = self.custom_param.get('load_time_manual', 0.5)
        self.load_time_auto = self.custom_param.get('load_time_auto', 1.0)
        self.anim_duration = self.custom_param.get('anim_duration', 1.2)
        self.anim_name = self.custom_param.get('anim_name', 'shotgun_load')
        self.anim_dir = self.custom_param.get('anim_dir', 7)
        self.start_load_time = self.custom_param.get('start_load_time', 0.2)
        self.final_start_load_time = 0
        self.sd.ref_is_loaded = True
        self.load_time = self.load_time_manual if global_data.player.get_setting_2(SHOTGUN_FIRE_ON_NOT_AUTO_8029) else self.load_time_auto

    def on_loading(self):
        if self.sd.ref_cur_state != MECHA_8029_FORM_HUNT:
            return
        if self.ev_g_reloading():
            return
        self.sd.ref_is_loaded = False
        self.active_self()

    def set_start_load_time(self, start_load_time):
        self.final_start_load_time = start_load_time

    def on_update_shotgun_fire_not_auto(self, flag):
        self.load_time = flag and self.load_time_manual if 1 else self.load_time_auto

    def enter(self, leave_states):
        super(ShotGunLoad, self).enter(leave_states)
        self.send_event('E_ENABLE_AIM_IK', False)
        self.send_event('E_ANIM_RATE', UP_BODY, self.anim_duration / self.load_time)
        self.send_event('E_POST_ACTION', self.anim_name, UP_BODY, self.anim_dir, loop=False)
        self.delay_call(self.load_time + self.final_start_load_time, self.on_loaded)

    def on_loaded(self):
        self.sd.ref_is_loaded = True

    def check_transitions(self):
        if self.sd.ref_is_loaded:
            continue_fire, _ = self.ev_g_continue_fire() or (False, None)
            if self.ev_g_check_continue_fire():
                self.send_event('E_ADD_WHITE_STATE', {MC_SHOOT}, self.sid)
                return MC_SHOOT
            self.disable_self()
        return

    def exit(self, enter_states):
        super(ShotGunLoad, self).exit(enter_states)
        self.sd.ref_is_loaded = True
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.final_start_load_time = self.start_load_time

    def destroy(self):
        global_data.emgr.update_shotgun_fire_on_release_8029 -= self.on_update_shotgun_fire_not_auto
        super(ShotGunLoad, self).destroy()


class Reload8029(Reload):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8029, self).init_from_dict(unit_obj, bdict, sid, state_info)

    def read_data_from_custom_param(self):
        super(Reload8029, self).read_data_from_custom_param()
        weapon_id = self.custom_param.get('weapon_id', '802903')
        self.max_bullet_cnt = confmgr.get('firearm_config', weapon_id, 'iMagSize', default=1.0)

    def enter(self, leave_states):
        super(Reload8029, self).enter(leave_states)
        if self.sd.ref_cur_state == MECHA_8029_FORM_HUNT:
            self.send_event('E_REFRESH_WEAPON_STATE', 7)

    def exit(self, enter_states):
        super(Reload8029, self).exit(enter_states)
        if self.sd.ref_cur_state == MECHA_8029_FORM_HUNT:
            self.send_event('E_REFRESH_WEAPON_STATE', 2)

    def on_reloading_bullet(self, time, times, weapon_pos):
        super(Reload8029, self).on_reloading_bullet(time, times, weapon_pos)

    def check_transitions(self):
        if self.reloaded:
            self.disable_self()
            if self.sd.ref_cur_state == MECHA_8029_FORM_HUNT:
                self.send_event('E_LOADING')

    def on_reloaded(self, weapon_pos, cur_bullet_cnt):
        if cur_bullet_cnt >= self.max_bullet_cnt and self.sd.ref_cur_state == MECHA_8029_FORM_HUNT:
            self.reloaded = True
        if self.sd.ref_cur_state != MECHA_8029_FORM_HUNT:
            self.reloaded = True
        continue_fire, fire_weapon_pos = self.ev_g_continue_fire() or (False, None)
        if continue_fire and fire_weapon_pos == weapon_pos:
            if self.ev_g_try_weapon_attack_begin(self.weapon_pos):
                self.continue_fire = True
        return

    def play_anim(self):
        is_loop = self.sd.ref_cur_state == MECHA_8029_FORM_HUNT
        time_scale = self.timer_rate if self.sd.ref_cur_state != MECHA_8029_FORM_HUNT else 1.0
        if self.use_up_anim_bone:
            self.send_event('E_REPLACE_UP_BONE_MASK', self.use_up_anim_states, self.use_up_anim_bone)
        if self.bind_action_id:
            self.send_event('E_START_ACTION_CD', self.bind_action_id, self.reload_time)
        if self.reload_anim:
            if self.extern_bone_tree:
                self.send_event('E_POST_EXTERN_ACTION', self.reload_anim, True, subtree=self.extern_bone_tree, timeScale=self.timer_rate, blend_time=self.extern_enter_blend_time)
            else:
                self.send_event('E_POST_ACTION', self.reload_anim, UP_BODY, self.reload_anim_dir, loop=is_loop, timeScale=time_scale)
                if self.sub_bone_tree:
                    self.send_event('E_POST_EXTERN_ACTION', self.reload_anim, True, subtree=self.sub_bone_tree, timeScale=self.timer_rate, blend_time=self.extern_enter_blend_time)


class KeepAimTimer(StateBase):
    BIND_EVENT = {'E_KEEP_AIM': 'on_keep_aim',
       'E_JUMP': 'enter_jump',
       'E_ON_TOUCH_GROUND': 'on_ground'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(KeepAimTimer, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self._keep_timer = None
        self.replace_anim = None
        self.last_keep_aim_time = -1
        return

    def read_data_from_custom_param(self):
        self.max_aim_time_after_fire = self.custom_param.get('max_aim_time_after_fire', 5.0)

    def enter(self, leave_states):
        super(KeepAimTimer, self).enter(leave_states)

    def on_keep_aim(self, replace_anim, play_anim):
        self.last_keep_aim_time = self.elapsed_time
        self.replace_anim = replace_anim
        self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', replace_anim, anim_dir=7)
        if play_anim:
            self.send_event('E_POST_ACTION', replace_anim, UP_BODY, 7, loop=True)
        if not self.is_active:
            self.active_self()

    def enter_jump(self, jump_speed):
        if self.sd.ref_cur_state != MECHA_8029_FORM_HUNT:
            return
        if self.is_active:
            self.send_event('E_POST_ACTION', self.replace_anim, UP_BODY, 1, loop=False)

    def on_ground(self, *args):
        if self.sd.ref_cur_state != MECHA_8029_FORM_HUNT:
            return
        if self.ev_g_reloading():
            return
        if self.is_active:
            self.send_event('E_POST_ACTION', self.replace_anim, UP_BODY, 7, loop=True)

    def clear_default_aim_anim(self):
        if self.sd.ref_cur_state != MECHA_8029_FORM_HUNT:
            return
        if self.sd.ref_hold_aim:
            self.on_keep_aim(self.replace_anim, False)
            return
        self.disable_self()

    def update(self, dt):
        super(KeepAimTimer, self).update(dt)
        if self.elapsed_time - self.last_keep_aim_time >= self.max_aim_time_after_fire:
            self.clear_default_aim_anim()

    def exit(self, enter_states):
        super(KeepAimTimer, self).exit(enter_states)
        self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', None)
        if self.sd.ref_up_body_anim == self.replace_anim:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.replace_anim = None
        self._keep_timer = None
        return