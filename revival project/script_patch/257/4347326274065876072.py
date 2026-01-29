# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDeathDoorAppearance.py
from __future__ import absolute_import
import six
import world
import math3d
import math
from mobile.common.EntityManager import EntityManager
from .ComBaseModelAppearance import ComBaseModelAppearance
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const.building_const import B_LIGHT_SHIELD
from logic.gutils import judge_utils
from common.cfg import confmgr

class ComDeathDoorAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_BUILDING_CHANGE_HP': '_on_hp_change',
       'E_BUILDING_DONE': '_on_building_done',
       'E_HITED': '_on_hited',
       'E_ADD_THROW_OBJ': '_on_add_throw_obj',
       'E_DEL_THROW_OBJ': '_on_del_throw_obj',
       'E_DOOR_STATE_CHANGE': 'on_door_state_change',
       'G_HP_POSITION': '_on_get_hp_pos',
       'G_DOOR_ROT_MAT': '_on_get_door_rot_mat',
       'G_DOOR_POS': '_on_get_door_pos',
       'G_IS_TEAMMATE_DOOR': '_is_teammate'
       })

    def __init__(self):
        super(ComDeathDoorAppearance, self).__init__()
        self._thow_objs = {}
        self.door_model_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        self.faction_id = bdict.get('faction_id')
        self.npc_id = bdict.get('npc_id')
        super(ComDeathDoorAppearance, self).init_from_dict(unit_obj, bdict)
        door_cfg_data = global_data.game_mode.get_cfg_data('door_data')
        self.door_info = door_cfg_data.get(str(self.npc_id))
        pos = self.door_info.get('pos')
        rot = self.door_info.get('rot')
        scale = self.door_info.get('scale')
        self.door_pos = math3d.vector(*pos)
        self.door_rot_mat = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180, math.pi * rot[1] / 180, math.pi * rot[2] / 180))
        self.door_scale = math3d.vector(*scale)
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_refresh_death_sfx_event': self.refresh_door_model
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_get_door_rot_mat(self):
        return self.door_rot_mat

    def _on_get_door_pos(self):
        return self.door_pos

    def reuse(self, share_data):
        super(ComDeathDoorAppearance, self).reuse(share_data)
        self._thow_objs = {}

    def cache(self):
        super(ComDeathDoorAppearance, self).cache()

    def get_player_group_id(self):
        from logic.gutils import judge_utils
        if judge_utils.is_ob():
            obed_unit = judge_utils.get_ob_target_unit()
        else:
            obed_unit = global_data.player and global_data.player.logic
        if obed_unit:
            return obed_unit.ev_g_group_id()

    def _is_teammate(self):
        return self.get_player_group_id() == self.faction_id

    def get_model_info(self, unit_obj, bdict):
        model_path = self.door_info.get('model_path')
        if type(model_path) in (list, tuple) and len(model_path) > 1:
            model_path = model_path[0] if self._is_teammate() else model_path[1]
        return (model_path, None, None)

    def on_load_model_complete(self, model, userdata):
        model.world_position = self.door_pos
        model.rotation_matrix = self.door_rot_mat
        model.scale = self.door_scale

    def on_door_state_change(self, is_destroyed):
        if self.model and self.model.valid:
            self.model.visible = not is_destroyed

    def _on_building_done(self):
        self._build_done = True

    def _on_hp_change(self, hp):
        if not self.model or not self.model.valid:
            return
        self.send_event('E_HEALTH_HP_CHANGE', hp)

    def _on_hited(self):
        global_data.sound_mgr.play_sound_optimize('Play_props', self.unit_obj, self.door_pos, ('props_action',
                                                                                               'sidou_shield_hit'))

    def on_model_destroy(self):
        self.notify_thow_obj()
        self.process_event(False)

    def _on_get_hp_pos(self):
        return self.model.position

    def _on_add_throw_obj(self, eid):
        self._thow_objs[eid] = True

    def _on_del_throw_obj(self, eid):
        if eid in self._thow_objs:
            del self._thow_objs[eid]

    def notify_thow_obj(self):
        for eid in six.iterkeys(self._thow_objs):
            obj = EntityManager.getentity(eid)
            if obj and obj.logic:
                obj.logic.send_event('E_RESET_POSITION')

        self._thow_objs.clear()

    def refresh_door_model(self):
        self.send_event('E_LOAD_MODEL_FROM_BDICT')