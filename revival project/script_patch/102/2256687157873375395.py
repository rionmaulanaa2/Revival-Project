# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_occupy_tower_appearance/ComOccupyTowerAppearance.py
from __future__ import absolute_import
import six
from logic.gcommon.component.client.ComBaseModelAppearance import ComBaseModelAppearance
import math3d
import world
from mobile.common.EntityManager import EntityManager
import weakref
import logic.gcommon.time_utility as t_util
from common.cfg import confmgr

class ComOccupyTowerAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ON_PLAYER_OCCUPYING': '_on_occupying',
       'E_UPDATE_OCCUPY_TOWER': 'update_occupy_tower_helper'
       })
    MODEL_PATH = confmgr.get('script_gim_ref')['item_mecha_signal']
    NEUTRAL_SFX = 'effect/fx/scenes/common/biaozhi/signal.sfx'
    OCCUPIED_SFX = [
     'effect/fx/scenes/common/biaozhi/signal_blue_start.sfx',
     'effect/fx/scenes/common/biaozhi/signal_red_start.sfx',
     'effect/fx/scenes/common/biaozhi/signal_yellow_start.sfx']
    OCCUPYING_SFX = 'effect/fx/scenes/common/chongdian/chongdian_lianxian.sfx'

    def __init__(self):
        super(ComOccupyTowerAppearance, self).__init__()
        self._control_faction = None
        self._sfx_id = None
        self._occupying_sfx_dict = {}
        self._last_ctrl_faction = None
        self._kongtou_sfx_id = None
        self._on_radar_puppets = []
        self.perspective_timer = None
        self._control_timestamp = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComOccupyTowerAppearance, self).init_from_dict(unit_obj, bdict)
        self._last_ctrl_faction = None
        control_faction = bdict.get('control_faction', None)
        self._control_faction = control_faction
        self._grap_faction = bdict.get('grap_faction', None)
        self._grap_entities = bdict.get('grap_entities', None)
        self._occupy_id = str(bdict.get('npc_id', None) or -1)
        self._control_timestamp = bdict.get('control_timestamp', 0) or 0
        occupy_id = self._occupy_id
        occupy_cfg = global_data.game_mode.get_cfg_data('king_occupy_data')
        zone_config = occupy_cfg.get(str(occupy_id), {})
        self.zone_radian_time = zone_config.get('zone_radian_time', 5)
        self.zone_radian_length = zone_config.get('zone_radian_length', [100, 100])
        self.zone_center = zone_config.get('position', [0, 0, 0])
        return

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rot = bdict.get('rot', [0, 0, 0, 1])
        return (
         self.MODEL_PATH, None, (pos, rot, bdict))

    def on_load_model_complete(self, model, userdata):
        pos, rot = userdata[0], userdata[1]
        pos = math3d.vector(pos[0], pos[1], pos[2])
        mat = math3d.rotation_to_matrix(math3d.rotation(rot[0], rot[1], rot[2], rot[3]))
        model.world_position = pos
        model.rotation_matrix = mat
        model.active_collision = True
        if not self._control_faction:
            self._kongtou_sfx_id = global_data.sfx_mgr.create_sfx_in_scene('effect/fx/robot/common/kongtou_big.sfx', pos)
        self._update_occupy_tower(self._control_faction, self._grap_faction, self._grap_entities)

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
        if not self.OCCUPYING_SFX:
            return
        socket_name = 'gliding'
        if target.logic.ev_g_is_in_mecha():
            control_target = target.logic.ev_g_control_target()
            if control_target and control_target.logic and control_target.__class__.__name__ == 'Mecha':
                socket_name = 'part_point0'
                model = control_target.logic.ev_g_model()
        if not model or not model.valid:
            return

        def create_cb(sfx):
            if model and model.valid:
                sfx.endpos_attach(model, socket_name, True)

        if not self.model:
            return
        mat = self.model.get_socket_matrix('fx_buff', world.SPACE_TYPE_WORLD)
        if mat and mat.translation:
            sfx_id = global_data.sfx_mgr.create_sfx_in_scene(self.OCCUPYING_SFX, mat.translation, on_create_func=create_cb)
            self._occupying_sfx_dict[target.id] = sfx_id

    def _remove_occupying_sfx(self, target):
        target_id = target.id
        sfx_id = self._occupying_sfx_dict.get(target_id, None)
        if sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
            self._occupying_sfx_dict.pop(target_id)
        return

    def update_occupy_tower_helper(self, control_faction_id, grap_faction_id, entities):
        if control_faction_id and control_faction_id != self._last_ctrl_faction:
            self._control_timestamp = t_util.get_server_time()
        self._update_occupy_tower(control_faction_id, grap_faction_id, entities)

    def _update_occupy_tower(self, control_faction_id, grap_faction_id, entities):
        self.clear_all_occupying_sfx()
        self._on_been_ctrl(control_faction_id)
        if grap_faction_id and entities:
            for entity_id in entities:
                self._on_occupying(entity_id, True)

    def _on_been_ctrl(self, faction_id):
        if faction_id and faction_id == self._last_ctrl_faction:
            return
        else:
            self._last_ctrl_faction = faction_id
            self.on_update_camp_occupy()
            if self._sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self._sfx_id)
            if not faction_id:
                self._sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.NEUTRAL_SFX, self.model, 'fx_root')
                return
            if self._kongtou_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self._kongtou_sfx_id)
                self._kongtou_sfx_id = None
            camp_data = global_data.king_battle_data.get_camp().get(faction_id, None)
            if camp_data:
                occupied_sfx_path = self.OCCUPIED_SFX[camp_data.side]
                self._sfx_id = global_data.sfx_mgr.create_sfx_on_model(occupied_sfx_path, self.model, 'fx_root')
                if global_data.player and global_data.player.logic:
                    my_faction_id = global_data.player.logic.ev_g_camp_id()
                    if my_faction_id == faction_id:
                        global_data.sound_mgr.play_ui_sound('successful_occupation')
            return

    def clear_all_occupying_sfx(self):
        for sfx_id in six.itervalues(self._occupying_sfx_dict):
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._occupying_sfx_dict.clear()

    def destroy(self):
        self.hide_radar_effect()
        self.clear_all_occupying_sfx()
        self._last_ctrl_faction = None
        if self._kongtou_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._kongtou_sfx_id)
            self._kongtou_sfx_id = None
        if self._sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._sfx_id)
            self._sfx_id = None
        super(ComOccupyTowerAppearance, self).destroy()
        return

    def on_update_camp_occupy(self):
        if not global_data.cam_lplayer:
            return
        if self._last_ctrl_faction != global_data.cam_lplayer.ev_g_camp_id():
            return
        _cur_in_occupy_zone_list = []
        if global_data.cam_lplayer:
            _cur_in_occupy_zone_list = global_data.cam_lplayer.ev_g_cur_in_occupy_zone_list()
        my_occupy_id = self._occupy_id
        if my_occupy_id in _cur_in_occupy_zone_list:
            self.show_radar_effect(my_occupy_id)

    def show_radar_effect(self, occupy_id):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        self.hide_radar_effect()
        zone_radian_time = self.zone_radian_time
        cur_time = t_util.get_server_time()
        remain_show_time = zone_radian_time - (cur_time - self._control_timestamp)
        if remain_show_time <= 0:
            return
        zone_radian_length = self.zone_radian_length
        zone_center = self.zone_center
        from common.utils.timer import CLOCK
        puppets = EntityManager.get_entities_by_type('Puppet')
        for puppet_id, puppet in six.iteritems(puppets):
            if puppet and puppet.logic:
                if global_data.cam_lplayer and puppet.id == global_data.cam_lplayer.id:
                    continue
                p_cont = puppet.logic.ev_g_control_target()
                if p_cont and p_cont.logic:
                    pos = p_cont.logic.ev_g_position()
                    if not pos:
                        continue
                    if zone_radian_length[0] * NEOX_UNIT_SCALE > abs(pos.x - zone_center[0]) and zone_radian_length[1] * NEOX_UNIT_SCALE > abs(pos.z - zone_center[2]):
                        p_cont.logic.send_event('E_SHOW_PERSPECTIVE_MARK', -1)
                        self._on_radar_puppets.append(weakref.ref(p_cont.logic))

        if self._on_radar_puppets:
            global_data.game_mgr.unregister_logic_timer(self.perspective_timer)
            self.perspective_timer = global_data.game_mgr.register_logic_timer(func=self.hide_radar_effect, interval=remain_show_time, times=1, mode=CLOCK)

    def hide_radar_effect(self):
        global_data.game_mgr.unregister_logic_timer(self.perspective_timer)
        self.perspective_timer = None
        for lpuppet_ref in self._on_radar_puppets:
            lpuppet = lpuppet_ref()
            if lpuppet and lpuppet.is_valid():
                lpuppet.send_event('E_HIDE_PERSPECTIVE_MARK')

        self._on_radar_puppets = []
        return