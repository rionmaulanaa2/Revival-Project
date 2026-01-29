# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/LocalBattleServer.py
from __future__ import absolute_import
from mobile.common.EntityManager import Dynamic
from logic.entities.BaseClientEntity import BaseClientEntity
import logic.gcommon.common_utils.idx_utils as idx_utils
from mobile.common.EntityFactory import EntityFactory
from mobile.common.IdManager import IdManager
from logic.comsys.guide_ui.GuideSetting import GuideSetting
import collision
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE

def merge_sync_handler_dict(d1, d2):
    d = d1.copy()
    d.update(d2)
    return d


@Dynamic
class LocalBattleServer(BaseClientEntity):
    RPC_HANDLER = {'loaded_battle': '_lbs_loaded_battle',
       'quit_battle': '_lbs_quit_battle',
       'sync_battle': '_lbs_sync_battle',
       'sync_battle_time': '_lbs_sync_battle_time'
       }
    SYNC_BATTLE_HANDLER = {'move_sync_all': '_lbs_move_sync_all',
       'sync_ack_check': '_lbs_sync_ack_check',
       'acc_cam_yaw': '_lbs_acc_cam_yaw',
       'acc_cam_pitch': '_lbs_acc_cam_pitch',
       'cam_state': '_lbs_cam_state'
       }
    DISCARD_BATTLE_SYNC = {
     'move_sync_all', 'acc_yaw', 'trigger_head_pitch', 'sync_move_state', 'try_trans_status', 'force_yaw',
     'sync_ack_check', 'acc_cam_yaw', 'acc_cam_yaw', 'acc_cam_pitch', 'cam_state', 'swt_act_st',
     'bcast_evt', 'bcast_evt_crs_server', 'set_aim_target', 'upload_timer_acc_ratio'}

    def __init__(self, entityid):
        super(LocalBattleServer, self).__init__(entityid)

    def init_from_dict(self, bdict):
        super(LocalBattleServer, self).init_from_dict(bdict)
        self._local_aoi_id = 0
        self.local_battle = None
        self._local_battle_data = None
        return

    def get_local_aoi_id(self):
        self._local_aoi_id += 1
        return self._local_aoi_id

    def set_local_battle(self, battle):
        self.local_battle = battle
        self.on_set_local_battle()

    def on_set_local_battle(self):
        pass

    def get_local_battle(self):
        return self.local_battle

    def _lbs_loaded_battle(self, *args):
        params = {'entity_id': global_data.player.id,
           'entity_aoi_id': self.get_local_aoi_id(),
           'entity_dict': self.get_player_init_dict()
           }
        self.join_local_battle()
        global_data.player.call_new_local_battle_rpc_method('add_entity', params)

    def _lbs_quit_battle(self, *args):
        self.on_quit_battle(*args)

    def _lbs_sync_battle(self, method_pack):
        for sync_id, sync_method_pack in method_pack:
            for method_name, param in sync_method_pack:
                method_name = idx_utils.s_idx_2_method_name(method_name)
                if method_name in self.DISCARD_BATTLE_SYNC:
                    continue
                handle_name = self.SYNC_BATTLE_HANDLER.get(method_name, None)
                if handle_name is None:
                    continue
                handle_func = getattr(self, handle_name, None)
                if handle_func is None:
                    continue
                handle_func(*param)

        return

    def _lbs_sync_battle_time(self, f_send, last_rtt):
        params = {'f_send': f_send,'f_stamp': f_send,
           'game_ver': 0
           }
        global_data.player.call_local_avatar_rpc_method('on_sync_battle_time', params)

    def _lbs_add_entity(self, entity_type, init_dict):
        entity_obj = EntityFactory.instance().create_entity(entity_type, IdManager.genid())
        entity_obj.init_from_dict(init_dict)
        params = {'entity_id': entity_obj.id,
           'entity_aoi_id': self.get_local_aoi_id(),
           'entity_dict': init_dict
           }
        if global_data.player:
            global_data.player.call_new_local_battle_rpc_method('add_entity', params)
            return entity_obj

    def _lbs_destroy_entity(self, entity_id):
        params = (entity_id,)
        if global_data.player:
            global_data.player.call_new_local_battle_method_direct('destroy_entity', params)

    def _lbs_send_event(self, evt, *args):
        player = global_data.player
        if not player or not player.logic:
            log_error('lbs_send_event - player is: %s or lplayer is None' % player)
            return
        player.logic.send_event(evt, *args)

    def _lbs_get_value(self, evt):
        player = global_data.player
        if not player or not player.logic:
            log_error('lbs_get_value - player is: %s or lplayer is None' % player)
            return None
        else:
            return player.logic.get_value(evt)

    def join_local_battle(self):
        pass

    def on_quit_battle(self, *args):
        pass

    def get_client_dict(self):
        pass

    def get_player_init_dict(self):
        pass

    def get_usual_mecha_ids(self):
        return [
         8001]

    def save_local_battle_data(self, key, value):
        info = self._get_local_battle_data()
        info[key] = value
        GuideSetting().local_battle_data = info

    def _get_local_battle_data(self):
        try:
            if self._local_battle_data is None:
                self._local_battle_data = GuideSetting().local_battle_data
            return self._local_battle_data
        except:
            return GuideSetting().local_battle_data

        return

    def _lbs_is_hit(self, start_pos, end_pos):
        hit_by_ray = global_data.game_mgr.scene.scene_col.hit_by_ray
        ret = hit_by_ray(start_pos, end_pos, 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, True)
        if ret and ret[0]:
            return True
        return False