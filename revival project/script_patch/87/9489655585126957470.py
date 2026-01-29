# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAgony.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.cdata import status_config
from ...time_utility import time
import logic.gcommon.common_const.animation_const as animation_const
from logic.client.const import game_mode_const
from logic.gutils.client_unit_tag_utils import preregistered_tags

class ComAgony(UnitCom):
    BIND_EVENT = {'E_HEALTH_HP_EMPTY': 'dying',
       'T_AGONY': 'dying',
       'T_DEFEATED': 'defeated',
       'T_DEATH': 'die',
       'G_DEATH': 'is_dead',
       'G_AGONY': 'is_agony',
       'G_DEFEATED': 'is_defeated',
       'G_HEALTHY': 'is_healthy',
       'E_AGONY_HP': 'on_hp_change',
       'E_START_BE_RESCUE': 'start_rescue',
       'E_STOP_RESCUE': 'stop_rescue',
       'G_IN_RESCUE': 'in_rescue',
       'E_ON_SAVED': 'on_saved',
       'E_REVIVE': ('on_revive', -10),
       'G_AGONY_HP_PERCENT': '_get_agony_hp_percent',
       'G_AGONY_HP': '_get_agony_hp',
       'G_DEFEATED_TIMESTAMP': '_get_defeated_timestamp',
       'E_SIGNAL_EMPTY': 'dying'
       }

    def __init__(self):
        super(ComAgony, self).__init__()
        self._agony_degree = 0
        self._agony_hp = 0
        self._is_dead = False
        self._is_defeated = False
        self._revive_timestamp = None
        self._rescuer_id = None
        self._last_killer_info = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComAgony, self).init_from_dict(unit_obj, bdict)
        self._agony_degree = bdict.get('agony_degree', 0)
        self._agony_hp = bdict.get('agony_hp', 0)
        self._is_dead = bdict.get('is_dead', False)
        self._is_defeated = bdict.get('is_defeated', False)
        self._is_agony = bdict.get('is_agony', False)
        self._rescuer_id = bdict.get('rescuer_id', None)
        self._revive_timestamp = bdict.get('revive_timestamp', None)
        self._last_killer_info = bdict.get('last_killer_info', {})
        return

    def on_init_complete(self):
        if self._is_dead:
            self.send_event('E_DEATH', None)
        elif self._is_defeated and self._revive_timestamp is not None:
            revive_time = max(0, self._revive_timestamp - time())
            killer_id = None
            if self._last_killer_info and 'trigger_id' in self._last_killer_info:
                killer_id = self._last_killer_info['trigger_id']
            self.send_event('E_DEFEATED', revive_time, killer_id, self._last_killer_info)
        elif self._is_agony:
            self.ev_g_status_try_trans(status_config.ST_DOWN)
            self._on_agony_changed()
        if self.ev_g_is_avatar():
            self.unit_obj.regist_event('E_GROUPMATE_DOWN', self._check_can_give_up)
        return

    def destroy(self):
        if global_data.player and global_data.player.logic and not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_EXERCISE):
            global_data.player.logic.send_event('E_ADD_AGONY_PLAYER', False, self.unit_obj.id)
        super(ComAgony, self).destroy()

    def is_dead(self):
        return self._is_dead

    def is_agony(self):
        return self._is_agony

    def is_defeated(self):
        return self._is_defeated

    def is_healthy(self):
        return not (self._is_dead or self._is_agony or self._is_defeated)

    def on_hp_change(self, hp):
        self._agony_hp = hp

    def dying(self):
        if self._is_dead or self._is_agony or self._is_defeated:
            return
        self.ev_g_status_try_trans(status_config.ST_DOWN)
        self.send_event('E_ACTION_SYNC_RC_STATUS', animation_const.STATE_DOWN)
        self._is_agony = True
        if self.ev_g_parachuting() or self.ev_g_is_parachute_stage_free_drop():
            position = self.ev_g_position() or self.ev_g_model_position()
            if position:
                self.send_event('E_LAND', position)
        self._on_agony_changed()

    def defeated(self, revive_time, killer_id, is_agony, killer_info):
        if self._is_dead or self._is_defeated:
            return
        self.ev_g_status_try_trans(status_config.ST_DEAD)
        self._is_defeated = True
        self._revive_timestamp = revive_time
        self._is_agony = is_agony
        self._agony_hp = 0
        self.send_event('E_DEFEATED', revive_time, killer_id, killer_info)
        self._on_agony_changed()

    def die(self, killer_id, kill_effect_id=None):
        if self._is_dead:
            return
        else:
            self.ev_g_status_try_trans(status_config.ST_DEAD)
            self._is_agony = False
            self._agony_hp = 0
            self._is_defeated = False
            self._revive_timestamp = None
            self._is_dead = True
            self.send_event('E_DEATH', killer_id, kill_effect_id)
            self._rescuer_id = None
            self._on_agony_changed()
            return

    def start_rescue(self, rescuer_id, rescue_time):
        self._rescuer_id = rescuer_id
        if self.ev_g_is_avatar():
            global_data.emgr.play_game_voice.emit('behelp')
            is_mate = self.ev_g_is_groupmate(rescuer_id)
            if global_data.player and global_data.player.logic:
                if is_mate:
                    cancel_cb = None
                    refuse_cb = None
                else:
                    cancel_cb = None
                    refuse_cb = lambda *args: self.send_event('E_CALL_SYNC_METHOD', 'refuse_rescue', ())
                if is_mate:
                    msg = get_text_by_id(18230) if 1 else get_text_by_id(3289)
                    self._check_can_give_up()
                    global_data.player.logic.send_event('E_SHOW_PROGRESS', rescue_time, -2, msg, cancel_callback=cancel_cb, refuse_callback=refuse_cb, is_stranger_rescue=True)
            elif global_data.player and rescuer_id == global_data.player.id:
                global_data.emgr.play_game_voice.emit('help')
            if self.ev_g_is_avatar() or global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_PUPPET_START_BE_RESCUING', self.unit_obj.id, rescuer_id)
        return

    def stop_rescue(self, rescuer_id, reason=None):
        if rescuer_id and rescuer_id == self._rescuer_id:
            self._rescuer_id = None
            if global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_CLOSE_PROGRESS', -2)
        if self.ev_g_is_avatar():
            self._check_can_give_up()
        return

    def in_rescue(self):
        return bool(self._rescuer_id)

    def on_saved(self):
        if self.ev_g_is_avatar():
            global_data.emgr.play_game_voice.emit('behelped')
        elif global_data.player and global_data.player.id == self._rescuer_id:
            global_data.emgr.play_game_voice.emit('helped')
        self.ev_g_cancel_state(status_config.ST_DEAD)
        self.send_event('E_REMOVE_TRIGGER_STATE', status_config.ST_DEAD)
        self._agony_hp = 0
        self._is_agony = False
        self._is_defeated = False
        self._revive_timestamp = None
        self._rescuer_id = None
        self.send_event('E_SUCCESS_SAVED')
        self.ev_g_cancel_state(status_config.ST_DOWN)
        self.send_event('E_REMOVE_TRIGGER_STATE', status_config.ST_DOWN)
        self._on_agony_changed()
        return

    def on_revive(self):
        self.ev_g_cancel_state(status_config.ST_DEAD)
        self.send_event('E_REMOVE_TRIGGER_STATE', status_config.ST_DEAD)
        self._agony_hp = 0
        self._is_agony = False
        self._is_defeated = False
        self._revive_timestamp = None
        self._is_dead = False
        self.ev_g_cancel_state(status_config.ST_DOWN)
        self.send_event('E_REMOVE_TRIGGER_STATE', status_config.ST_DOWN)
        self.send_event('E_SUCCESS_SAVED')
        if not self.ev_g_is_avatar():
            self.send_event('E_ENABLE_ANIM')
            self.send_event('E_ON_REVIVE')
        global_data.emgr.player_revived.emit(self.unit_obj.id)
        return

    def _get_defeated_timestamp(self):
        return self._revive_timestamp

    def _get_agony_hp_percent(self):
        return self._agony_hp * 1.0 / self.unit_obj.ev_g_max_hp()

    def _get_agony_hp(self):
        return self._agony_hp

    def _on_agony_changed(self):
        if self._is_agony:
            self.send_event('E_AGONY')
        if self.ev_g_is_avatar():
            self._check_can_give_up()
        elif self.unit_obj.MASK & preregistered_tags.HUMAN_TAG_VALUE and not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_EXERCISE):
            global_data.player.logic.send_event('E_ADD_AGONY_PLAYER', self._is_agony, self.unit_obj.id)

    def _check_can_give_up(self):
        visible = False
        if self._is_agony:
            if self._rescuer_id and not self.ev_g_is_groupmate(self._rescuer_id):
                visible = True
            visible = visible or not self.ev_g_has_healthy_groupmate()
            visible = visible or self.ev_g_can_gulag_revive()
        global_data.emgr.recruit_be_rescued.emit(visible)