# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_beacon_tower/ComBeaconTowerAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.client.ComBaseModelAppearance import ComBaseModelAppearance
from mobile.common.EntityManager import EntityManager
import math3d
import collision
import render
import game3d
from logic.gcommon.common_const import battle_const
import world

class ComBeaconTowerAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_UPDATE_BEACON_TOWER': '_update_beacon_tower',
       'E_ON_PLAYER_OCCUPYING': '_on_occupying'
       })

    def __init__(self):
        super(ComBeaconTowerAppearance, self).__init__()
        self._beacon_tower_conf = {}
        self._start_sfx_list = []
        self._end_sfx_list = []
        self._neutral_sfx = None
        self._sfx_id = None
        self._last_faction = None
        self._occupying_sfx_dict = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        self._beacon_tower_id = bdict.get('npc_id', None)
        beacon_conf = self._get_beacon_tower_conf()
        if beacon_conf:
            self._start_sfx_list = beacon_conf.get('occupied_start_sfx', [])
            self._end_sfx_list = beacon_conf.get('occupied_end_sfx', [])
            self._neutral_sfx = beacon_conf.get('neutral_sfx', [])
        self._occupying_entity_ids = bdict.get('occupying_entity_ids', [])
        self._state = bdict.get('state', battle_const.BEACON_NEUTRAL)
        self._last_faction = bdict.get('faction_id', None)
        self._occupying_sfx_path = 'effect/fx/scenes/common/chongdian/chongdian_lianxian.sfx'
        super(ComBeaconTowerAppearance, self).init_from_dict(unit_obj, bdict)
        return

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rot = bdict.get('rot', [0, 0, 0, 1])
        model_path = self._beacon_tower_conf['model_path']
        return (
         model_path, None, (pos, rot, bdict))

    def _get_beacon_tower_conf(self):
        from common.cfg import confmgr
        if self._beacon_tower_conf:
            return self._beacon_tower_conf
        self._beacon_tower_conf = confmgr.get('beacon_tower_config', str(self._beacon_tower_id))
        return self._beacon_tower_conf

    def on_load_model_complete(self, model, userdata):
        pos, rot = userdata[0], userdata[1]
        pos = math3d.vector(pos[0], pos[1], pos[2])
        mat = math3d.rotation_to_matrix(math3d.rotation(rot[0], rot[1], rot[2], rot[3]))
        model.world_position = pos
        model.rotation_matrix = mat
        model.active_collision = True
        self._update_beacon_tower(self._state, self._last_faction)
        for entity_id in self._occupying_entity_ids:
            entity = EntityManager.getentity(entity_id)
            self._add_occupying_sfx(entity)

    def _update_beacon_tower(self, state, faction_id):
        if self._sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._sfx_id)
        if state == battle_const.BEACON_OCCUPIED and faction_id is not None:
            camp_data = global_data.king_battle_data.get_camp().get(faction_id, None)
            if camp_data:
                sfx_path = self._start_sfx_list[camp_data.side]
                self._sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, self.model, 'fx_root')
        else:

            def recover_neutral(sfx):
                if self._sfx_id:
                    global_data.sfx_mgr.remove_sfx_by_id(self._sfx_id)
                self._sfx_id = global_data.sfx_mgr.create_sfx_on_model(self._neutral_sfx, self.model, 'fx_root')

            if self._last_faction is not None:
                camp_data = global_data.king_battle_data.get_camp().get(self._last_faction, None)
                if camp_data:
                    sfx_path = self._end_sfx_list[camp_data.side]
                    self._sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, self.model, 'fx_root', on_remove_func=recover_neutral)
            else:
                recover_neutral(None)
        self._last_faction = faction_id
        return

    def _on_occupying(self, entity_id, is_occupying):
        entity = EntityManager.getentity(entity_id)
        if not entity:
            return
        if is_occupying and entity_id not in self._occupying_sfx_dict:
            self._add_occupying_sfx(entity)
        elif not is_occupying and entity_id in self._occupying_sfx_dict:
            self._remove_occupying_sfx(entity)

    def _add_occupying_sfx(self, target):
        if not target or not target.logic:
            return
        model = target.logic.ev_g_model()
        if not self._occupying_sfx_path:
            return
        socket_name = 'gliding'
        if target.logic.ev_g_is_in_mecha():
            control_target = target.logic.ev_g_control_target()
            if control_target.__class__.__name__ == 'LMecha':
                socket_name = 'part_point0'
                model = control_target.ev_g_model()
        if not model or not model.valid:
            return

        def create_cb(sfx):
            if model and model.valid and self.is_valid():
                sfx.endpos_attach(model, socket_name, True)
                self._occupying_sfx_dict[target.id] = sfx
            else:
                global_data.sfx_mgr.remove_sfx(sfx)

        mat = self.model.get_socket_matrix('fx_buff', world.SPACE_TYPE_WORLD)
        if mat and mat.translation:
            global_data.sfx_mgr.create_sfx_in_scene(self._occupying_sfx_path, mat.translation, on_create_func=create_cb)

    def _remove_occupying_sfx(self, target):
        target_id = target.id
        sfx = self._occupying_sfx_dict.get(target_id, None)
        if sfx:
            global_data.sfx_mgr.remove_sfx(sfx)
            self._occupying_sfx_dict.pop(target_id)
        return