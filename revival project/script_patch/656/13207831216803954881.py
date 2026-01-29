# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSpectate.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager
from logic.comsys.battle.Settle.EndTransitionUI import EndTransitionUI

class ComSpectate(UnitCom):
    BIND_EVENT = {'E_REQ_SPECTATE': '_req_spectate',
       'E_REQ_SPECTATE_GROUPMATE': '_req_spectate_groupmate',
       'E_SPECTATE_OBJ': '_spectate_obj',
       'G_SPECTATE_TARGET': '_get_spectate_target',
       'G_SPECTATE_TARGET_ID': '_get_spectate_target_id',
       'G_IS_IN_SPECTATE': '_is_in_spectate',
       'E_SET_KILLER_ID_NAME': '_set_killer',
       'G_KILLER_ID': '_get_killer',
       'G_KILLER_ID_NAME': '_get_killer_id_info',
       'G_BATTLE_STARS': '_req_battle_stars',
       'E_REQ_SPECTATE_STAR': '_req_spectate_star',
       'E_LIKE_SPECTATE_TARGET': '_like_spectate_target',
       'G_SPECTATE_LIKE_DATA': '_g_spectate_like_data',
       'E_SPECTATE_LIKE_DATA': '_set_spectate_like_data',
       'E_QUIT_SPECTATE_SYNC': '_on_quit_spectate',
       'E_SPECTATOR_NUM': '_set_spectator_num',
       'G_SPECTATOR_NUM': '_get_spectator_num'
       }

    def __init__(self):
        super(ComSpectate, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComSpectate, self).init_from_dict(unit_obj, bdict)
        self.spectate_id = bdict.get('spectate_obj', None)
        self.killer_id = bdict.get('killer', None)
        self.killer_name = bdict.get('killer_name', '')
        self._has_avatar_liked = bdict.get('sp_obj_be_liked', False)
        self._battle_like_cnt = bdict.get('sp_obj_liked_cnt', 0)
        self._is_outsider = bdict.get('is_outsider', False)
        self._spectator_num = bdict.get('spectator_num', 0)
        self._be_like_num = bdict.get('be_like_num', 0)
        self.transition_before_observe = False
        return

    def on_init_complete(self):
        if self.spectate_id:
            self._spectate_obj(self.spectate_id, False)
        if self.unit_obj.__class__.__name__ == 'LAvatar':
            global_data.emgr.on_observer_num_changed.emit(self._spectator_num)

    def _req_spectate(self, delay_time=0, transition_before_observe=False):
        self.send_event('E_CALL_SYNC_METHOD', 'req_spectate', (delay_time,), True)
        self.transition_before_observe = transition_before_observe

    def _req_spectate_groupmate(self, groupmate_id):
        self.send_event('E_CALL_SYNC_METHOD', 'req_spectate_groupmate', (groupmate_id,), True)

    def _spectate_obj(self, obj_id, need_check=True, allow_none_target=False):
        if global_data.ex_scene_mgr_agent.check_settle_scene_active():
            return
        else:
            if not global_data.game_mode or not global_data.battle:
                return
            if global_data.game_mode.is_pve() and global_data.battle.is_settled():
                return
            if self.transition_before_observe:
                self.transition_before_observe = False
                EndTransitionUI(callback=lambda _oid=obj_id: self._spectate_obj(_oid), need_close_self=True)
                return
            if global_data.is_in_judge_camera:
                if global_data.player.manual_required_spectate_id == str(obj_id):
                    global_data.emgr.try_switch_judge_camera_event.emit(False, is_force=True)
                else:
                    self.spectate_id = obj_id
                    return
            global_data.emgr.notify_begin_spectate_successfully.emit()
            global_data.emgr.before_observe_target_changed.emit(self.spectate_id)
            self.spectate_id = obj_id
            global_data.emgr.after_observe_target_changed.emit(self.spectate_id)
            if obj_id is None and not allow_none_target:
                return
            if global_data.player and self.unit_obj and self.unit_obj.id == global_data.player.id:
                new_cam_lplayer = None
                if obj_id is None:
                    if global_data.player and not global_data.player.is_in_global_spectate():
                        if global_data.player and global_data.player.logic:
                            new_cam_lplayer = global_data.player.logic
                global_data.emgr.set_observe_target_id_event.emit(obj_id, allow_none_target, new_cam_lplayer)
            return

    def _get_spectate_target(self):
        if self.spectate_id:
            get_entity = EntityManager.getentity
            ent = get_entity(self.spectate_id)
            if ent and ent.logic:
                return ent
        else:
            return None
        return None

    def _get_spectate_target_id(self):
        return self.spectate_id

    def _is_in_spectate(self):
        return self.spectate_id is not None

    def _on_quit_spectate(self):
        if not self._is_in_spectate():
            return
        else:
            self._spectate_obj(None, allow_none_target=True)
            return

    def _set_killer(self, id, name):
        self.killer_id = id
        self.killer_name = name

    def _get_killer(self):
        return self.killer_id

    def _get_killer_id_info(self):
        return (
         self.killer_id, self.killer_name)

    def _req_battle_stars(self):
        self.send_event('E_CALL_SYNC_METHOD', 'req_battle_stars', (), True)

    def _req_spectate_star(self, star_id):
        self.send_event('E_CALL_SYNC_METHOD', 'req_spectate_star', (star_id,), True)

    def _like_spectate_target(self):
        if self.spectate_id:
            self.send_event('E_CALL_SYNC_METHOD', 'try_like', (self.spectate_id,), True)

    def _g_spectate_like_data(self):
        return (
         self._has_avatar_liked, self._battle_like_cnt)

    def _set_spectate_like_data(self, has_avatar_like, _battle_like_cnt):
        self._has_avatar_liked = has_avatar_like
        self._battle_like_cnt = _battle_like_cnt

    def _set_spectator_num(self, num):
        self._spectator_num = num

    def _get_spectator_num(self):
        return self._spectator_num