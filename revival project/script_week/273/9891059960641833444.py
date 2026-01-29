# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComRescue.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from ...cdata import status_config
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE
from time import time
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_utils.local_text import get_text_by_id

class ComRescue(UnitCom):
    BIND_EVENT = {'E_ADD_AGONY_PLAYER': 'mark_agony_player',
       'E_TRY_RESCUE': 'rescue',
       'E_CANCEL_RESCUE': 'cancel_rescue',
       'E_STOP_DO_RESCUE': 'stop_rescue',
       'E_INTERRUPT_RESCUE': 'interrupt_rescue',
       'E_PUPPET_START_BE_RESCUING': 'puppet_start_be_rescuing'
       }

    def __init__(self):
        super(ComRescue, self).__init__()
        self._agony_player_set = set()
        self._rescue_id = None
        self._next_check_time = 0
        return

    def destroy(self):
        self._agony_player_set = None
        self._rescue_id = None
        super(ComRescue, self).destroy()
        return

    def mark_agony_player(self, flag, player_id):
        if flag:
            self._agony_player_set.add(player_id)
            if self.ev_g_agony() and self.ev_g_is_groupmate(player_id):
                self.send_event('E_GROUPMATE_DOWN')
        elif player_id in self._agony_player_set:
            self._agony_player_set.remove(player_id)
        need_update = bool(self._agony_player_set)
        if need_update != self.need_update:
            self.need_update = need_update
        if not self.need_update:
            ui = global_data.ui_mgr.get_ui('SceneInteractionUI')
            if ui:
                ui.hide_rescue()

    def enable_recruit(self):
        if not self.battle.recruit_valid():
            return False
        cnt = self.battle.get_max_teammate_num()
        alive_teammate_num = self.ev_g_alive_groupmate_num() or 0
        if alive_teammate_num >= cnt - 1:
            return False
        return True

    def enable_faction_rescue(self, player_id):
        if not self.battle.enable_faction_rescue():
            return False
        if not self.ev_g_is_campmate_by_eid(player_id):
            return False
        return True

    def tick(self, dt):
        now = time()
        if now < self._next_check_time:
            return
        self._next_check_time = now + 0.1
        if not self.ev_g_healthy():
            return
        max_rescue_dis_limit = battle_const.MECHA_RESCUE_DIS if self.ev_g_in_mecha() else battle_const.HUMAN_RESCUE_DIS
        if self._rescue_id:
            player = EntityManager.getentity(self._rescue_id)
            if not player or not player.logic:
                self.interrupt_rescue()
                return
            pos = player.logic.ev_g_position()
            mine_pos = self.ev_g_position()
            if not pos or not mine_pos or not (pos - mine_pos).length < max_rescue_dis_limit:
                self.interrupt_rescue()
        else:
            is_skip_rescue = False
            if self.ev_g_in_mecha:
                mecha = global_data.player.logic.ev_g_control_target()
                if mecha and mecha.logic:
                    is_skip_rescue = not mecha.logic.ev_g_on_ground()
            if is_skip_rescue:
                return
        enable_recruit = self.enable_recruit()
        enable_faction_rescue = self.battle and self.battle.enable_faction_rescue()
        mine_pos = self.ev_g_position()
        ui = global_data.ui_mgr.get_ui('SceneInteractionUI')
        if ui and not self.ev_g_agony():
            for player_id in self._agony_player_set:
                is_teammate = self.ev_g_is_groupmate(player_id)
                is_factionmate = self.ev_g_is_campmate_by_eid(player_id)
                show_by_teammate = is_teammate
                show_by_recruit = not is_teammate and enable_recruit
                show_by_factionmate = enable_faction_rescue and is_factionmate
                if not show_by_teammate and not show_by_recruit and not show_by_factionmate:
                    continue
                player = EntityManager.getentity(player_id)
                if not player or not player.logic or player.logic.ev_g_in_rescue():
                    continue
                pos = player.logic.ev_g_position()
                if pos and mine_pos:
                    dis = (mine_pos - pos).length
                    if dis < max_rescue_dis_limit:
                        visible = bool(is_teammate or is_factionmate)
                        ui.show_rescue(dis, visible)
                        break
            else:
                ui.hide_rescue()

    def rescue(self):
        mine_pos = self.ev_g_position()
        if mine_pos is None:
            ui = global_data.ui_mgr.get_ui('SceneInteractionUI')
            ui.hide_rescue()
            return
        else:
            enable_recruit = self.enable_recruit()
            enable_faction_rescue = self.battle and self.battle.enable_faction_rescue()
            dis_limit = battle_const.MECHA_RESCUE_DIS if self.ev_g_in_mecha() else battle_const.HUMAN_RESCUE_DIS
            for player_id in self._agony_player_set:
                player = EntityManager.getentity(player_id)
                if not self.ev_g_is_groupmate(player_id) and not enable_recruit and not enable_faction_rescue and not self.ev_g_is_campmate_by_eid(player_id):
                    continue
                if not player or not player.logic or player.logic.ev_g_in_rescue():
                    continue
                pos = player.logic.ev_g_position()
                if pos is None:
                    continue
                dis = (mine_pos - pos).length
                if dis < dis_limit:
                    self._try_rescue(player_id)
                    return
            else:
                self.send_event('E_SHOW_MESSAGE', get_text_local_content(18113))
                ui = global_data.ui_mgr.get_ui('SceneInteractionUI')
                ui.hide_rescue()

            return

    def stop_rescue(self, player_id, reason=None):
        self.ev_g_cancel_state(status_config.ST_HELP, True)
        self.send_event('E_ACTION_CANCEL_RESCUE')
        self.send_event('E_CLOSE_PROGRESS', -1)
        ui = global_data.ui_mgr.get_ui('SceneInteractionUI')
        if ui:
            ui.hide_rescue()
        self._unregister_rescue_event()
        self._rescue_id = None
        if reason in [battle_const.RESCUE_CANCEL_REFUSE, battle_const.RESCUE_CANCEL_GIVEUP]:
            if reason == battle_const.RESCUE_CANCEL_REFUSE:
                txt = get_text_by_id(3292)
            else:
                txt = get_text_by_id(3293)
            msg = {'i_type': battle_const.MAIN_NODE_RESCUE_FAILED_REASON,'content_txt': txt}
            global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
            from logic.gcommon.common_const.battle_const import PLAY_TYPE_RECRUITMENT
            from logic.gcommon.common_utils.battle_utils import get_play_type_by_battle_id
            if global_data.battle and get_play_type_by_battle_id(global_data.battle.get_battle_tid()) == PLAY_TYPE_RECRUITMENT:
                global_data.battle.send_player_recruit_message(player_id, battle_const.RECRUITMENT_BATTLE_REJECT)
        return

    def cancel_rescue(self, need_close_progress=True):
        self.ev_g_cancel_state(status_config.ST_HELP, True)
        self.send_event('E_ACTION_CANCEL_RESCUE')
        if need_close_progress:
            self.send_event('E_CLOSE_PROGRESS', -1)
        ui = global_data.ui_mgr.get_ui('SceneInteractionUI')
        if ui:
            ui.hide_rescue()
        self._unregister_rescue_event()
        self._cancel_rescue()
        self._rescue_id = None
        return

    def _try_rescue(self, player_id):
        if not self.ev_g_in_mecha():
            if not self.ev_g_status_check_pass(status_config.ST_HELP):
                return
            if not self.ev_g_status_try_trans(status_config.ST_HELP, True):
                return
        else:
            control_target = self.ev_g_control_target()
            if control_target and control_target.logic:
                if not control_target.logic.ev_g_status_check_pass(mecha_status_config.MC_HELP):
                    return
                if not control_target.logic.ev_g_status_try_trans(mecha_status_config.MC_HELP, True):
                    return
        self.send_event('E_BEGIN_RESCUE')
        target = EntityManager.getentity(player_id)
        if target and target.logic:
            self._rescue_id = player_id
        ui = global_data.ui_mgr.get_ui('SceneInteractionUI')
        if ui:
            ui.begin_rescue()

        def callback():
            self._unregister_rescue_event()
            ui = global_data.ui_mgr.get_ui('SceneInteractionUI')
            if ui:
                ui.hide_rescue()
            self.ev_g_cancel_state(status_config.ST_HELP, True)
            self.send_event('E_ACTION_CANCEL_RESCUE')

        kwargs = {}
        cur_rescue_time = battle_const.RESCUE_TIME * (1 + self.ev_g_attr_get(battle_const.RESCUE_TIME_KEY, 0))
        is_teammate = self.ev_g_is_groupmate(player_id)
        is_factionmate = self.ev_g_is_campmate_by_eid(player_id)
        msg = get_text_by_id(18070) if is_teammate or is_factionmate else get_text_by_id(3288)
        self.send_event('E_SHOW_PROGRESS', cur_rescue_time, (-1), msg, callback, None, **kwargs)
        self._register_rescue_event()
        self.send_event('E_CALL_SYNC_METHOD', 'rescue_groupmate', (player_id,), True)
        return

    def _cancel_rescue(self):
        self.send_event('E_CALL_SYNC_METHOD', 'rescue_cancel', (), True)

    def _register_rescue_event(self):
        regist_event = self.regist_event
        regist_event('E_ENTER_DOOR_INTERACTION_ZONE', self.interrupt_rescue)
        regist_event('E_LEAVE_DOOR_INTERACTION_ZONE', self.interrupt_rescue)
        global_data.emgr.scene_pick_obj_event += self.interrupt_rescue

    def _unregister_rescue_event(self):
        unregist_event = self.unregist_event
        unregist_event('E_ENTER_DOOR_INTERACTION_ZONE', self.interrupt_rescue)
        unregist_event('E_LEAVE_DOOR_INTERACTION_ZONE', self.interrupt_rescue)
        global_data.emgr.scene_pick_obj_event -= self.interrupt_rescue

    def interrupt_rescue(self, *arg, **kwargs):
        self.cancel_rescue()
        self._unregister_rescue_event()

    def puppet_start_be_rescuing(self, puppet_id, rescuer_id):
        if self._rescue_id == puppet_id and rescuer_id != self.unit_obj.id:
            self.interrupt_rescue()