# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/StateLogic.py
from __future__ import absolute_import
import six
import math
import math3d
import world
from .StateBase import StateBase, clamp
from logic.gcommon.cdata.mecha_status_config import *
from logic.gutils import item_utils
from logic.gcommon.const import NEOX_UNIT_SCALE
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import buff_const
import logic.gcommon.common_const.animation_const as animation_const
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.component.client.com_character_ctrl.ComAnimMgr import DEFAULT_ANIM_NAME
from logic.gutils import character_action_utils
from logic.gutils.client_unit_tag_utils import preregistered_tags
from logic.gcommon.common_const.character_anim_const import *
import common.utils.timer as timer
from logic.gcommon.cdata import speed_physic_arg
import logic.gcommon.cdata.status_config as status_config
import logic.gcommon.cdata.mecha_status_config as mecha_status_config
from logic.gcommon.common_const.buff_const import BUFF_ID_USE_ITEM_SPEED_DOWN
from common.cfg import confmgr
from common.platform.dctool import interface
from logic.gcommon.common_utils import battle_utils
from logic.gcommon import editor

class Die(StateBase):
    BIND_EVENT = {'E_HEALTH_HP_EMPTY': 'on_die',
       'E_DEATH': 'on_die'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Die, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.tick_interval = self.custom_param.get('tick_interval', 0.2)

    def enter(self, leave_states):
        self.send_event('E_ON_DIE')
        if self.ev_g_is_avatar():
            item_utils.set_drop_pos(self)
        super(Die, self).enter(leave_states)
        self.send_event('E_CLEAR_UP_BODY_ANIM')

    def exit(self, enter_states):
        super(Die, self).exit(enter_states)

    def on_die(self, *args):
        self.send_event('E_CLEAR_SPEED')
        self.active_self()
        if self.ev_g_is_avatar():
            self.active_self()
        else:
            self.enter(set())
            self.update(0.03)
            self.send_event('E_DISABLE_ANIM')


class HumanDie(Die):
    BIND_EVENT = {'E_REVIVE': 'revive',
       'E_DEATH': 'on_die',
       'E_DEFEAT': 'on_defeated',
       'E_ANIM_MGR_INIT': 'on_anim_mgr_init'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(HumanDie, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.killer_id = 0
        self.kill_effect_id = 0
        self._die_timer_id = None
        self.anim_duration = self.custom_param.get('anim_duration', 2)
        self._die_action = self.custom_param.get('die_action', None)
        is_dead = bdict.get('is_dead', False) or bdict.get('is_defeated', False)
        return

    def on_anim_mgr_init(self):
        if not self.ev_g_get_state(self.sid):
            return
        self.on_exit()

    def enter(self, leave_states):
        self.send_event('E_SWITCH_STATUS', animation_const.STATE_DIE)
        self.send_event('E_ROCK_STOP')
        self.send_event('E_CLEAR_SPEED')
        if self.ev_g_is_avatar():
            item_utils.set_drop_pos(self)
        super(Die, self).enter(leave_states)
        self.send_event('E_CLEAR_UP_BODY_ANIM')

    def on_enter(self):
        pass

    def on_exit(self, *args):
        self._die_timer_id = None
        if not self.ev_g_get_state(self.sid):
            return
        else:
            self.send_event('E_UNBIND_ALL_WEAPON')
            self.send_event('E_HIDE_MODEL')
            return

    def on_defeated(self, killer_id=0, kill_effect_id=0, *args):
        self.on_die(killer_id, kill_effect_id, True)

    def on_die(self, killer_id=0, kill_effect_id=0, is_defeated=False):
        super(HumanDie, self).on_die(killer_id, kill_effect_id, is_defeated)
        self.killer_id = killer_id
        self.kill_effect_id = kill_effect_id
        g_signal = self.ev_g_signal()
        if battle_utils.is_battle_signal_open() and g_signal is not None and g_signal <= 0 and killer_id is None:
            pass
        elif self._die_action:
            clip_name, part, blend_dir, kwargs = self._die_action
            self.send_event('E_POST_ACTION', clip_name, (LOW_BODY if part == 'lower' else UP_BODY), blend_dir, **kwargs)
        if self._die_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._die_timer_id)
            self._die_timer_id = None
        self._die_timer_id = global_data.game_mgr.register_logic_timer(self.on_exit, self.anim_duration, times=1, mode=timer.CLOCK)
        self.send_event('E_SHOW_DIE_SFX', self.killer_id, self.kill_effect_id)
        signal = self.ev_g_signal()
        if not signal:
            signal = 0 if 1 else signal
            ballon_res_path = battle_utils.is_battle_signal_open() and signal <= 0 and killer_id is None or confmgr.get('script_gim_ref')['ballon_res']
            self.ev_g_load_model(ballon_res_path, self.die_ballon_model_load_callback)
        self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)
        return

    def revive(self, *args):
        self.send_event('E_UNBIND_MODEL', 'ballon')
        self.send_event('E_UNBIND_MODEL', 'root')
        self.send_event('E_SHOW_MODEL')

    def die_ballon_model_load_callback(self, ballon_model, *args):
        if not self.is_active:
            return
        if not self.ev_g_get_state(self.sid):
            return
        model = self.ev_g_model()
        if not model:
            return
        if self.ev_g_in_mecha():
            self.send_event('E_SHOW_MODEL')
        if not model.visible:
            ballon_model.destroy()
            return
        bind_point = 'ballon'
        ballon_model.remove_from_parent()
        model.bind(bind_point, ballon_model, world.BIND_TYPE_TRANSLATE)


class Hit(StateBase):
    LIGHT_HIT = 0
    HEAVY_HIT = 1
    BIND_EVENT = {'S_HP': 'take_damage'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Hit, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.tick_interval = self.custom_param.get('tick_interval', 0.2)
        self.hit_type = self.LIGHT_HIT
        self.hit_thresh = self.custom_param.get('hit_thresh', 300)
        self.hit_anim = self.custom_param.get('hit_anim', ('hit', 'hit'))
        self.hit_anim_len = self.custom_param.get('hit_anim_duration', (0.7, 0.7))
        self.cur_hp = self.ev_g_hp()

    def enter(self, leave_states):
        super(Hit, self).enter(leave_states)
        self.send_event('E_POST_ADD_ANIMATION', True, self.hit_anim[self.hit_type], 'idle', is_base_first_frame=False)
        self.delay_call(self.hit_anim_len[self.hit_type], self.hit_end)

    def hit_end(self):
        self.disable_self()

    def exit(self, enter_states):
        self.send_event('E_POST_ADD_ANIMATION', False, blend_time=0.2)
        super(Hit, self).exit(enter_states)

    def take_damage(self, cur_hp):
        if not (self.ev_g_is_agent() or self.ev_g_is_avatar()):
            return
        if self.is_active:
            return
        damage = self.cur_hp - cur_hp
        self.cur_hp = cur_hp
        self.hit_type = self.LIGHT_HIT if damage < self.hit_thresh else self.HEAVY_HIT
        self.active_self()


class Immobilize(StateBase):
    BIND_EVENT = {'E_IMMOBILIZED': 'on_immobilized'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Immobilize, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.tick_interval = self.custom_param.get('tick_interval', 1)
        self._immobilized = False
        self.fall = True

    def enter(self, leave_states):
        super(Immobilize, self).enter(leave_states)
        self.send_event('E_CLEAR_SPEED')
        if not self.fall:
            self.send_event('E_ACTION_SYNC_ACC', 0)
            self.send_event('E_GRAVITY', 0)
            self.send_event('E_VERTICAL_SPEED', 0)

    def exit(self, enter_states):
        super(Immobilize, self).exit(enter_states)
        self._immobilized = False

    def check_transitions(self):
        if not self._immobilized:
            self.disable_self()
            if self.sd.ref_on_ground:
                return MC_STAND
            else:
                return MC_JUMP_2

    def on_immobilized(self, immobilized, fall=True, is_soft=False):
        if not self.ev_g_is_avatar() and not self.ev_g_is_agent():
            return
        self._immobilized = immobilized
        if immobilized:
            self.fall = bool(fall)
            self.active_self()
        else:
            self.send_event('E_RESET_GRAVITY')


class OnFrozen(StateBase):
    BIND_EVENT = {'E_ON_FROZEN': 'on_frozen'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(OnFrozen, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.tick_interval = self.custom_param.get('tick_interval', 1)
        self._frozen = False
        self.fall = True

    def enter(self, leave_states):
        super(OnFrozen, self).enter(leave_states)
        self.send_event('E_CLEAR_SPEED')
        if not self.fall:
            self.send_event('E_VERTICAL_SPEED', 0)
            self.send_event('E_ACTION_SYNC_ACC', 0)
            self.send_event('E_GRAVITY', 0)

    def exit(self, enter_states):
        super(OnFrozen, self).exit(enter_states)
        self._frozen = False

    def check_transitions(self):
        if not self._frozen:
            self.disable_self()
            if self.sd.ref_on_ground:
                return MC_STAND
            else:
                return MC_JUMP_2

    def on_frozen(self, frozen, fall=True):
        if not self.ev_g_is_avatar() and not self.ev_g_is_agent():
            return
        self._frozen = frozen
        if frozen:
            self.send_event('E_CLEAR_SPEED')
            self.fall = fall
            self.active_self()
            self.sd.ref_socket_res_agent and self.sd.ref_socket_res_agent.freeze_follow_model_anim()
        else:
            self.send_event('E_RESET_GRAVITY')
            self.sd.ref_socket_res_agent and self.sd.ref_socket_res_agent.recover_follow_model_anim()


@editor.state_exporter({('min_h_speed', 'meter'): {'zh_name': '\xe5\x9f\xba\xe7\xa1\x80\xe5\x87\xbb\xe9\x80\x80\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x80\x9f\xe5\xba\xa6\xe6\x9c\x80\xe5\xb0\x8f\xe5\x80\xbc'},('max_h_speed', 'meter'): {'zh_name': '\xe5\x9f\xba\xe7\xa1\x80\xe5\x87\xbb\xe9\x80\x80\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x80\x9f\xe5\xba\xa6\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbc'},('min_v_speed', 'meter'): {'zh_name': '\xe5\x9f\xba\xe7\xa1\x80\xe5\x87\xbb\xe9\x80\x80\xe5\x9e\x82\xe7\x9b\xb4\xe9\x80\x9f\xe5\xba\xa6\xe6\x9c\x80\xe5\xb0\x8f\xe5\x80\xbc'},('max_v_speed', 'meter'): {'zh_name': '\xe5\x9f\xba\xe7\xa1\x80\xe5\x87\xbb\xe9\x80\x80\xe5\x9e\x82\xe7\x9b\xb4\xe9\x80\x9f\xe5\xba\xa6\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbc'},('gravity', 'meter'): {'zh_name': '\xe5\x87\xbb\xe9\x80\x80\xe9\x87\x8d\xe5\x8a\x9b\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'}})
class BeatBack(StateBase):
    BIND_EVENT = {'E_BEAT_BACK': 'on_beat_back'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(BeatBack, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.tick_interval = self.custom_param.get('tick_interval', 1)
        self.max_h_speed = self.custom_param.get('max_h_speed', 40) * NEOX_UNIT_SCALE
        self.min_h_speed = self.custom_param.get('min_h_speed', 10) * NEOX_UNIT_SCALE
        self.max_v_speed = self.custom_param.get('max_v_speed', 40) * NEOX_UNIT_SCALE
        self.min_v_speed = self.custom_param.get('min_v_speed', 10) * NEOX_UNIT_SCALE
        self.max_affect_dist = self.custom_param.get('max_affect_dist', 15) * NEOX_UNIT_SCALE
        self.h_affect_dist = (self.min_v_speed / self.max_v_speed + 1) * self.max_affect_dist
        self.v_affect_dist = (self.min_h_speed / self.min_h_speed + 1) * self.max_affect_dist
        self.gravity = self.custom_param.get('gravity', 50) * NEOX_UNIT_SCALE
        self.from_pos = None
        self.coe_v = 1
        self.coe_h = 1
        self.effect_type = 0
        return

    def enter(self, leave_states):
        super(BeatBack, self).enter(leave_states)
        self.send_event('E_ON_BEAT_BACK', True)
        self.cal_physic_param(self.from_pos)

    def exit(self, enter_states):
        super(BeatBack, self).exit(enter_states)
        self.send_event('E_ON_BEAT_BACK', False)

    def on_beat_back(self, from_pos, coe_v, coe_h, effect_type):
        if not self.ev_g_is_avatar() and not self.ev_g_is_agent():
            return
        self.coe_v, self.coe_h, self.effect_type = coe_v, coe_h, effect_type
        self.from_pos = from_pos
        self.active_self()

    def cal_physic_param(self, from_pos):
        cur_pos = self.ev_g_position()
        dist = cur_pos - from_pos
        dist.y = 0
        if dist.is_zero:
            dist = -self.ev_g_forward()
        h_dir = dist
        dist = dist.length
        h_dir.normalize()
        if self.effect_type == buff_const.BEAT_BACK_EFFECT_TYPE_DISTANCE:
            v_speed = (self.v_affect_dist - dist) / self.v_affect_dist * self.max_v_speed
            v_speed = clamp(v_speed, self.min_v_speed, self.max_v_speed)
            h_speed = (self.h_affect_dist - dist) / self.h_affect_dist * self.max_h_speed
            h_speed = clamp(h_speed, self.min_h_speed, self.max_h_speed)
        else:
            v_speed = self.max_v_speed
            h_speed = self.max_h_speed
        self.send_event('E_GRAVITY', self.gravity)
        self.send_event('E_JUMP', v_speed * self.coe_v)
        self.sd.ref_cur_speed = h_speed * self.coe_h
        self.send_event('E_SET_WALK_DIRECTION', h_dir * h_speed * self.coe_h)
        t_vector = math3d.vector(0, v_speed, 0) + h_dir * h_speed
        self.send_event('E_ACTION_SYNC_VEL', t_vector * (self.coe_v + self.coe_h))


class Born(StateBase):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Born, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.anim_duration = self.custom_param.get('anim_duration', 2)

    def check_transitions(self):
        if self.elapsed_time > self.anim_duration:
            self.disable_self()
            return MC_STAND


class UseItem(StateBase):
    BIND_EVENT = {'E_LEAVE_STATE': 'leave_states'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(UseItem, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._is_cancel = False

    def leave_states(self, leave_state, new_state=None):
        if leave_state == self.sid:
            if new_state:
                self.cacel_use_item()

    def enter(self, leave_states):
        super(UseItem, self).enter(leave_states)
        self._is_cancel = False

    def exit(self, enter_states):
        super(UseItem, self).exit(enter_states)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        if enter_states:
            self.cacel_use_item()

    def cacel_use_item(self):
        if self._is_cancel:
            return
        self._is_cancel = True
        driver = EntityManager.getentity(self.ev_g_driver())
        if driver and driver.logic:
            cur_sing_id = driver.logic.ev_g_cur_singing_id()
            if cur_sing_id:
                driver.logic.send_event('E_ITEMUSE_CANCEL', cur_sing_id)


class HumanUseItem(StateBase):
    BIND_EVENT = {'E_ITEMUSE_PRE': '_begin_item_pre',
       'E_ITEMUSE_END': '_end_item_pre',
       'E_ITEMUSE_CANCEL_RES': '_end_item_pre',
       'E_ITEMUSE_CANCEL': '_cancel_use',
       'E_ENTER_CROUCH': 'enter_crouch',
       'E_LEAVE_CROUCH': 'leave_crouch',
       'E_LEAVE_STATE': 'leave_states'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(HumanUseItem, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._pre_item_id = None
        self._item_pre_duration = 0
        self._item_pre_sfx_id = None
        self.stand_anim = self.custom_param.get('stand_anim', DEFAULT_ANIM_NAME)
        self.crouch_anim = self.custom_param.get('crouch_anim', DEFAULT_ANIM_NAME)
        self.stand_bandage_anim = self.custom_param.get('stand_bandage_anim', DEFAULT_ANIM_NAME)
        self.crouch_bandage_anim = self.custom_param.get('crouch_bandage_anim', DEFAULT_ANIM_NAME)
        return

    def leave_states(self, leave_state, new_state=None):
        if leave_state == self.sid:
            hand_action = self.ev_g_hand_action()
            if hand_action in (animation_const.HAND_STATE_USE_ITEM, animation_const.HAND_STATE_USE_BANDAGE):
                self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)
            if self._item_pre_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self._item_pre_sfx_id)
                self._item_pre_sfx_id = None
        return

    def get_anim(self):
        hand_action = self.ev_g_hand_action()
        if hand_action == animation_const.HAND_STATE_USE_BANDAGE:
            if self.ev_g_is_crouch():
                return self.crouch_bandage_anim
            else:
                return self.stand_bandage_anim

        else:
            if self.ev_g_is_crouch():
                return self.crouch_anim
            return self.stand_anim
        return self.stand_anim

    def _begin_item_pre(self, item_id, duration, start_time, hand_action=None):
        from data.item_use_var import ALL_USABLE_ID_LIST
        pre_duration = duration - start_time
        if item_id not in ALL_USABLE_ID_LIST:
            return
        self._pre_item_id = item_id
        if not self.ev_g_status_check_pass(status_config.ST_USE_ITEM):
            return
        self._item_pre_duration = pre_duration or 1
        control_target = self.ev_g_control_target()
        if not self.ev_g_is_in_mecha() and self.ev_g_is_avatar():
            self.send_event('E_TRY_USE_STATUS_SUC', item_id, duration, start_time)
        if self.ev_g_get_state(status_config.ST_SWIM):
            return
        if hand_action:
            self.send_event('E_HAND_ACTION', hand_action)
        self.send_event('E_HIDE_ALL_GUN')
        control_target = self.ev_g_control_target()
        if self.ev_g_is_in_mecha() and control_target.logic:
            is_success = control_target.logic.ev_g_trans_status(mecha_status_config.MC_USE_ITEM, sync=True)
            if is_success:
                control_target.logic.send_event('E_BUFF_SPD_ADD_STANDALONE', BUFF_ID_USE_ITEM_SPEED_DOWN)
                if self.ev_g_is_avatar():
                    self.send_event('E_TRY_USE_STATUS_SUC', item_id, duration, start_time)
            elif self.ev_g_is_avatar():
                self.send_event('E_TRY_USE_STATUS_FAILED', item_id, duration, start_time)
        else:
            self.send_event('E_ACTIVE_STATE', status_config.ST_USE_ITEM)
            clip_name = self.get_anim()
            time_scale = self.ev_g_get_anim_length(clip_name) / (self._item_pre_duration or 1)
            self.send_event('E_POST_ACTION', clip_name, UP_BODY, 1, loop=False, timeScale=time_scale)
            if hand_action == animation_const.HAND_STATE_USE_ITEM:
                use_item_effect = {'effect/fx/niudan/quanxi/rw_quanxi_daoju_01.sfx': ['rw_quanxi_daoju']}
                all_sfx_ids = []
                self.send_event('E_CREATE_MODEL_EFFECT', use_item_effect, is_sync=True, all_sfx_ids=all_sfx_ids)
                if all_sfx_ids:
                    self._item_pre_sfx_id = all_sfx_ids[0]

    def _cancel_use(self, *args):
        self.send_event('E_BUFF_SPD_DEL_STANDALONE', BUFF_ID_USE_ITEM_SPEED_DOWN)
        self.end_mecha_item_pre()

    def end_mecha_item_pre(self):
        control_target = self.ev_g_control_target()
        if control_target and control_target.logic and control_target.logic.MASK & preregistered_tags.MECHA_VEHICLE_TAG_VALUE:
            control_target.logic.send_event('E_BUFF_SPD_DEL_STANDALONE', BUFF_ID_USE_ITEM_SPEED_DOWN)
            control_target.logic.send_event('E_DISABLE_STATE', mecha_status_config.MC_USE_ITEM)

    def _end_item_pre(self, item_id=None, new_state=None):
        if item_id is not None:
            if self._pre_item_id != item_id:
                return
        self.disable_self()
        self.send_event('E_BUFF_SPD_DEL_STANDALONE', BUFF_ID_USE_ITEM_SPEED_DOWN)
        self.end_mecha_item_pre()
        self.send_event('E_SHOW_ALL_GUN')
        self._pre_item_id = None
        hand_action = self.ev_g_hand_action()
        if hand_action in (animation_const.HAND_STATE_USE_ITEM, animation_const.HAND_STATE_USE_BANDAGE):
            self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)
        if new_state != status_config.ST_HELP:
            self.send_event('E_CLOSE_PROGRESS', item_id)
        return

    def enter(self, leave_states):
        super(HumanUseItem, self).enter(leave_states)
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        if not self.ev_g_get_state(status_config.ST_SKATE):
            self.send_event('E_BUFF_SPD_ADD_STANDALONE', BUFF_ID_USE_ITEM_SPEED_DOWN)

    def exit(self, enter_states):
        super(HumanUseItem, self).exit(enter_states)
        self.send_event('E_BUFF_SPD_DEL_STANDALONE', BUFF_ID_USE_ITEM_SPEED_DOWN)

    def enter_crouch(self, leave_state):
        if not self.is_active:
            return
        leave_state = set(leave_state)
        if leave_state & character_action_utils.CROUCH_STATE:
            return
        clip_name = self.crouch_anim
        time_scale = 1
        if self._item_pre_duration > 0:
            time_scale = self.ev_g_get_anim_length(clip_name) / self._item_pre_duration
        self.send_event('E_POST_ACTION', clip_name, UP_BODY, 1, loop=False, timeScale=time_scale, keep_phase=True)

    def leave_crouch(self, new_state):
        if not self.is_active:
            return
        if new_state & character_action_utils.CROUCH_STATE:
            return
        clip_name = self.get_anim()
        time_scale = 1
        if self._item_pre_duration > 0:
            time_scale = self.ev_g_get_anim_length(clip_name) / self._item_pre_duration
        self.send_event('E_POST_ACTION', clip_name, UP_BODY, 1, loop=False, timeScale=time_scale, keep_phase=True)


class Help(StateBase):
    BIND_EVENT = {'E_ACTION_CANCEL_RESCUE': 'cancel_rescue',
       'E_ENABLE_HELP_ANIM': 'enable_help_anim'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Help, self).init_from_dict(unit_obj, bdict, sid, info)
        self._is_interrupt_by_other_state = True
        self._is_play_anim = True
        allow_move = self.custom_param.get('allow_move', 0)
        if allow_move:
            self.forbid_state = set()
        else:
            self.forbid_state = set([MC_MOVE, MC_RUN])
        anim_param = self.custom_param.get('anim', ('idle', 'lower', 1, {'loop': True}))
        if anim_param:
            self.anim, self.anim_part, self.anim_blend_type, self.anim_kwargs = anim_param
        else:
            self.anim = None
        self.anim_part = LOW_BODY if self.anim_part == 'lower' else UP_BODY
        return

    def enter(self, leave_states):
        self._is_interrupt_by_other_state = True
        super(Help, self).enter(leave_states)
        self.send_event('E_BRAKE')
        if self._is_play_anim and self.anim:
            self.send_event('E_POST_ACTION', self.anim, self.anim_part, self.anim_blend_type, **self.anim_kwargs)

    def exit(self, enter_states):
        self.send_event('E_CLEAR_BLACK_STATE')
        if self._is_interrupt_by_other_state:
            if self.ev_g_is_avatar():
                from mobile.common.EntityManager import EntityManager
                driver_id = self.ev_g_driver()
                driver = EntityManager.getentity(driver_id)
                if driver and driver.logic:
                    driver.logic.send_event('E_INTERRUPT_RESCUE')
        super(Help, self).exit(enter_states)

    def check_transitions(self):
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero:
            return MC_MOVE

    def action_btn_down(self):
        self.active_self()
        super(Help, self).action_btn_down()

    def cancel_rescue(self):
        self._is_interrupt_by_other_state = False
        self.disable_self()

    def enable_help_anim(self, enable):
        self._is_play_anim = enable


class HumanHelp(StateBase):
    BIND_EVENT = {'E_BEGIN_RESCUE': 'begin_rescue',
       'E_ACTION_CANCEL_RESCUE': 'cancel_rescue',
       'E_ANIM_MGR_INIT': 'on_anim_mgr_init'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(HumanHelp, self).init_from_dict(unit_obj, bdict, sid, info)
        self._stand_to_squat_anim_duration = 0
        self._stage = 0
        self.stand_to_help_anim = self.custom_param.get('stand_to_help', DEFAULT_ANIM_NAME)
        self.help_anim = self.custom_param.get('help', DEFAULT_ANIM_NAME)
        self._is_stand_before_help = True

    def enter(self, leave_states):
        super(HumanHelp, self).enter(set())
        self.send_event('E_ROCK_STOP')
        self.send_event('E_CLEAR_SPEED')

    def on_anim_mgr_init(self):
        anim_state = self.ev_g_attr_get('human_state')
        if anim_state == animation_const.STATE_SQUAT_HELP:
            if self.ev_g_is_avatar():
                self.active_self()
            else:
                self.ev_g_status_try_trans(self.sid)
                self.begin_rescue()

    def update(self, dt):
        super(HumanHelp, self).update(dt)
        if self._stage == 0:
            last_elapsed_time = self.elapsed_time
            if last_elapsed_time < self._stand_to_squat_anim_duration and self.elapsed_time >= self._stand_to_squat_anim_duration:
                self.send_event('E_UNBIND_ALL_WEAPON')
                self._stage = 1
                self.send_event('E_POST_ACTION', self.help_anim, LOW_BODY, 1, loop=True)

    def check_transitions(self):
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero:
            return self.status_config.MC_MOVE

    def begin_rescue(self):
        if self.ev_g_in_mecha():
            control_target = self.ev_g_control_target()
            if control_target and control_target.logic:
                control_target.logic.ev_g_try_enter(MC_HELP)
            return
        clip_name = self.help_anim
        self._is_stand_before_help = not self.ev_g_is_in_any_state(character_action_utils.CROUCH_STATE)
        if not self._is_stand_before_help:
            self._stage = 1
            self.send_event('E_UNBIND_ALL_WEAPON')
        else:
            self._stage = 0
            clip_name = self.stand_to_help_anim
            self._stand_to_squat_anim_duration = self.ev_g_get_anim_length(clip_name) * 0.9
        self.send_event('E_SWITCH_STATUS', animation_const.STATE_SQUAT_HELP)
        loop = self._stage > 0
        self.send_event('E_POST_ACTION', clip_name, LOW_BODY, 1, loop=loop)
        self.active_self()

    def cancel_rescue(self):
        if self.ev_g_in_mecha():
            control_target = self.ev_g_control_target()
            if control_target and control_target.logic:
                control_target.logic.send_event('E_ACTION_CANCEL_RESCUE')
            return
        self.send_event('E_REEQUIP_WEAPON')
        if not self.is_active:
            return
        if self._is_stand_before_help:
            self.send_event('E_CTRL_STAND')
        else:
            self.send_event('E_CTRL_SQUAT')


class ActionResHelper(object):

    def __init__(self):
        self._item_pre_sfx_id_dict = {}
        self._item_socket_model_id_dict = {}
        self._res_effect_created_list = []
        self._cache_ani_list = []

    def process_anim_cache(self, unit_obj, model, t_acts, is_cache):
        if not model:
            return
        else:
            ani_list = []
            for one_action_info in t_acts:
                anim_info = one_action_info[1].get('anim_info', None)
                if not anim_info:
                    continue
                clip_name = anim_info[0]
                ani_list.append(clip_name)

            if is_cache:
                self._cache_ani_list.extend(ani_list)
            else:
                for clip_name in ani_list:
                    if clip_name in self._cache_ani_list:
                        self._cache_ani_list.remove(clip_name)

            if ani_list:
                unit_obj.send_event('E_CACHE_MODEL_ANI_LIST', ani_list, is_cache, is_sync=True)
            return

    def clear_res(self, unit_obj):
        if self._item_pre_sfx_id_dict:
            for sfx_id_list in six.itervalues(self._item_pre_sfx_id_dict):
                for sfx_id in sfx_id_list:
                    global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

            self._item_pre_sfx_id_dict = {}
        for model_id_list in six.itervalues(self._item_socket_model_id_dict):
            for model_id in model_id_list:
                global_data.model_mgr.remove_model_by_id(model_id)

        self._item_socket_model_id_dict = {}
        for res_effect in self._res_effect_created_list:
            if res_effect and unit_obj:
                unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_REMOVE_RES_EFFECT, (res_effect,)], True)

        if self._cache_ani_list:
            if unit_obj:
                unit_obj.send_event('E_CACHE_MODEL_ANI_LIST', self._cache_ani_list, False, is_sync=True)
            self._cache_ani_list = []

    def parse_action_callback(self, sub_id, action_info, res_create_func, action_func, empty_func):
        if action_info:
            res_effect = action_info.get('res_effect', {})
            anim_info = action_info.get('anim_info', [None, None, None, None])
            clip_name, part, blend_dir, kwargs = anim_info
            if res_effect:
                all_sfx_ids = []
                all_model_ids = []
                if res_create_func:
                    res_create_func(res_effect, is_sync=True, all_sfx_ids=all_sfx_ids, all_model_ids=all_model_ids)
                    self._res_effect_created_list.append(res_effect)
                self._item_pre_sfx_id_dict.setdefault(sub_id, [])
                self._item_pre_sfx_id_dict[sub_id].extend(all_sfx_ids)
                self._item_socket_model_id_dict.setdefault(sub_id, [])
                self._item_socket_model_id_dict[sub_id].extend(all_model_ids)
            if clip_name:
                if action_func:
                    action_func(clip_name, part, blend_dir, **kwargs)
        elif empty_func:
            empty_func()
        return


class HumanPerformCustom(StateBase):
    BIND_EVENT = {'E_PERFORM_UNMOVABLE_ACTION_START': '_perform_unmovable_action',
       'E_PERFORM_UNMOVABLE_ACTION_END': '_end_perform_unmovable_action',
       'E_PERFORM_UNMOVABLE_ACTION_CANCEL': '_end_perform_unmovable_action',
       'E_LEAVE_STATE': 'leave_states'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(HumanPerformCustom, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._unique_action_name = ''
        self._action_res_helper = ActionResHelper()

    def leave_states(self, leave_state, new_state=None):
        if leave_state == self.sid:
            self.clear_state()
            self._unique_action_name = ''

    def clear_state(self):
        self.reset_sub_state_timer()
        self.reset_sub_states_callback()
        if self._action_res_helper:
            self._action_res_helper.clear_res(self.unit_obj)

    def _perform_unmovable_action(self, unique_name, time_action_info_list, time_action_setting_conf=None, state_camera_conf=None):
        if not self.ev_g_status_check_pass(status_config.ST_CUSTOM_ACTIONS):
            return
        self._unique_action_name = unique_name
        control_target = self.ev_g_control_target()
        if self.ev_g_is_in_mecha() and control_target.logic:
            return
        if state_camera_conf:
            self.state_camera_conf = state_camera_conf
            global_data.emgr.camera_set_pitch_event.emit(0)
            self.send_event('E_CAM_PITCH', 0)
        else:
            self.state_camera_conf = {}
        self.send_event('E_UNBIND_ALL_WEAPON')
        self.clear_state()
        self.send_event('E_ACTIVE_STATE', status_config.ST_CUSTOM_ACTIONS)
        if time_action_setting_conf and time_action_setting_conf.get('need_cache_anim'):
            self._action_res_helper.process_anim_cache(self.unit_obj, self.ev_g_model(), time_action_info_list, True)
        sub_id = 0
        for idx, time_action_info in enumerate(time_action_info_list):
            t, action_info = time_action_info

            def cb(sub_id=sub_id, action_info=action_info):
                self.parse_action_callback(sub_id, action_info)

            self.register_substate_callback(sub_id, t, cb)

    def update(self, dt):
        super(HumanPerformCustom, self).update(dt)

    def parse_action_callback(self, sub_id, action_info):

        def create_res_func(res_effect, is_sync, all_sfx_ids, all_model_ids):
            self.send_event('E_CREATE_RES_EFFECT', res_effect, None, is_sync, all_sfx_ids, all_model_ids)
            return

        def action_func(clip_name, part, blend_dir, **kwargs):
            self.send_event('E_POST_ACTION', clip_name, part, blend_dir, **kwargs)

        def empty_func():
            self._end_perform_unmovable_action()

        self._action_res_helper.parse_action_callback(sub_id, action_info, create_res_func, action_func, empty_func)

    def _end_perform_unmovable_action(self, unique_name=None, new_state=None):
        if unique_name is not None:
            if self._unique_action_name != unique_name:
                return
        self.disable_self()
        self.send_event('E_REEQUIP_WEAPON')
        self._unique_action_name = None
        return

    def enter(self, leave_states):
        super(HumanPerformCustom, self).enter(leave_states)
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)

    def exit(self, enter_states):
        super(HumanPerformCustom, self).exit(enter_states)
        self.send_event('E_CLEAR_UP_BODY_ANIM', DEFAULT_UP_BODY_BONE)


class HumanContinueAction(StateBase):
    BIND_EVENT = {'E_PERFORM_CONTINUE_ACTION_START': '_perform_continue_action',
       'E_PERFORM_CONTINUE_ACTION_CHANGE': '_perform_continue_action_change',
       'E_PERFORM_CONTINUE_ACTION_EXTEND': '_perform_continue_action_extend',
       'E_PERFORM_CONTINUE_ACTION_END': '_end_perform_continue_action',
       'E_PERFORM_CONTINUE_ACTION_CANCEL': '_end_perform_continue_action',
       'G_IS_IN_PERFORM_CONTINUE_ACTION': '_get_is_in_perform_continue_action',
       'G_CONTINUE_ACTION_LAST_TIME': '_get_continue_action_last_time',
       'G_CONTINUE_ACTION_NAME': '_get_continue_action_tag',
       'E_LEAVE_STATE': 'leave_states'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(HumanContinueAction, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._unique_action_name = ''
        self._to_be_action_name = ''
        self._remain_time = 0
        self._action_res_helper = ActionResHelper()

    def leave_states(self, leave_state, new_state=None):
        if leave_state == self.sid:
            self._end_perform_continue_action()
            self.clear_state()

    def clear_state(self):
        self.reset_sub_state_timer()
        self.reset_sub_states_callback()
        if self._action_res_helper:
            self._action_res_helper.clear_res(self.unit_obj)

    def _get_is_in_perform_continue_action(self, unique_name):
        if self._unique_action_name == unique_name:
            return True
        else:
            return False

    def _perform_continue_action_extend(self, unique_name, extend_time):
        if self._unique_action_name != unique_name:
            return
        self._remain_time = self.sub_sid_timer + extend_time

    def _perform_continue_action_change(self, unique_name, duration, time_action_info_list, time_action_setting_conf=None):
        if self.ev_g_is_in_any_state(status_config.ST_CONTINUE_ACTION):
            self._unique_action_name = unique_name
            self._remain_time = self.sub_sid_timer + duration
            self.clear_state()
            sub_id = 0
            if time_action_setting_conf and time_action_setting_conf.get('need_cache_anim'):
                self._action_res_helper.process_anim_cache(self.unit_obj, self.ev_g_model(), time_action_info_list, True)
            for idx, time_action_info in enumerate(time_action_info_list):
                t, action_info = time_action_info

                def cb(sub_id=sub_id, action_info=action_info):
                    self.parse_action_callback(sub_id, action_info)

                self.register_substate_callback(sub_id, t + self.sub_sid_timer, cb)

    def _perform_continue_action(self, unique_name, duration, time_action_info_list, time_action_setting_conf=None):
        if not self.ev_g_status_check_pass(status_config.ST_CONTINUE_ACTION):
            return
        control_target = self.ev_g_control_target()
        if self.ev_g_is_in_mecha() and control_target.logic:
            return
        is_diff_start = self._to_be_action_name != unique_name or self._remain_time != duration
        if is_diff_start:
            self._to_be_action_name = unique_name
            self._remain_time = duration
            self.clear_state()
        self.send_event('E_ACTIVE_STATE', status_config.ST_CONTINUE_ACTION)
        if is_diff_start:
            if time_action_setting_conf and time_action_setting_conf.get('need_cache_anim'):
                self._action_res_helper.process_anim_cache(self.unit_obj, self.ev_g_model(), time_action_info_list, True)
            sub_id = 0
            for idx, time_action_info in enumerate(time_action_info_list):
                t, action_info = time_action_info

                def cb(sub_id=sub_id, action_info=action_info):
                    self.parse_action_callback(sub_id, action_info)

                self.register_substate_callback(sub_id, t, cb)

    def update(self, dt):
        super(HumanContinueAction, self).update(dt)
        if self.sub_sid_timer > self._remain_time:
            self._end_perform_continue_action()

    def parse_action_callback(self, sub_id, action_info):

        def create_res_func(res_effect, is_sync, all_sfx_ids, all_model_ids):
            self.send_event('E_CREATE_RES_EFFECT', res_effect, None, is_sync, all_sfx_ids, all_model_ids)
            return

        def action_func(clip_name, part, blend_dir, **kwargs):
            self.send_event('E_POST_ACTION', clip_name, part, blend_dir, **kwargs)

        def empty_func():
            self._end_perform_continue_action()

        self._action_res_helper.parse_action_callback(sub_id, action_info, create_res_func, action_func, empty_func)

    def _end_perform_continue_action(self, unique_name=None, new_state=None):
        if unique_name is not None:
            if self._unique_action_name != unique_name:
                return
        self.disable_self()
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self._unique_action_name = None
        return

    def _get_continue_action_last_time(self):
        return self.sub_sid_timer

    def _get_continue_action_tag(self):
        return self._unique_action_name

    def enter(self, leave_states):
        self._unique_action_name = self._to_be_action_name
        super(HumanContinueAction, self).enter(leave_states)
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)

    def exit(self, enter_states):
        super(HumanContinueAction, self).exit(enter_states)
        self.send_event('E_CLEAR_UP_BODY_ANIM', DEFAULT_UP_BODY_BONE)
        self._to_be_action_name = ''