# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapDeathBloodBagWidget.py
from __future__ import absolute_import
import six
from logic.comsys.map.map_widget import MapScaleInterface
from common.utils.cocos_utils import ccp
from mobile.common.EntityManager import EntityManager
from logic.client.const import game_mode_const

class BloodBagMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget, spawn_id):
        super(BloodBagMapMark, self).__init__(parent_nd)
        self.spawn_id = spawn_id
        self.map_panel = ctrl_widget
        self._nd = global_data.uisystem.load_template_create('battle_tdm/i_tdm_map_locate_hp')
        self.parent_nd.AddChild('', self._nd)
        self.sp_dir = ccp(0, 1)

    def on_update(self, pos, scale=1.0):
        x, y, z = pos
        self._nd.img_spot.setScale(scale)
        pos_3 = self.trans_world_position_ex((x, 0, z))
        pos_2 = ccp(pos_3.x, pos_3.y)
        self.set_position(pos_2)


class ScavengeItemMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget, spawn_id):
        super(ScavengeItemMark, self).__init__(parent_nd)
        self.spawn_id = spawn_id
        self.map_panel = ctrl_widget
        self._nd = global_data.uisystem.load_template_create('map/ccb_map_pick_weapon')
        self.parent_nd.AddChild('', self._nd)
        self.sp_dir = ccp(0, 1)

    def on_update(self, pos, scale=1.0):
        x, y, z = pos
        self._nd.nd_mark.setScale(scale)
        pos_3 = self.trans_world_position_ex((x, 0, z))
        pos_2 = ccp(pos_3.x, pos_3.y)
        self.set_position(pos_2)


class MapDeathBloodBagWidget:

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.spawn_entity_id = {}
        self.spawn_info = {}
        self._widgets = {}
        self.process_event(True)
        self.init_spawn_info()
        self.update_nd()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_add_pickable_model_event': self.on_add_model,
           'scene_del_pickable_model_event': self.on_del_model,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)
        for widget in six.itervalues(self._widgets):
            if widget:
                widget.destroy()

        self._widgets = {}

    def init_spawn_info(self):
        battle = global_data.battle
        if not battle:
            return
        self.spawn_info = {}
        born_spawn_data = global_data.game_mode.get_cfg_data('born_spawn_data')
        spawn_lst = self.get_spawn_lst()
        for spawn_id in spawn_lst:
            if str(spawn_id) in born_spawn_data:
                self.spawn_info[spawn_id] = born_spawn_data[str(spawn_id)]

    def on_add_model(self, model, ids, spawn_id):
        if spawn_id in self.spawn_info:
            entity_id = ids[0]
            self.spawn_entity_id[spawn_id] = entity_id
            if self.is_teammate(entity_id):
                self.show_widget(spawn_id)
            else:
                self.del_widget(spawn_id)

    def on_del_model(self, model, spawn_id):
        if spawn_id in self.spawn_entity_id:
            del self.spawn_entity_id[spawn_id]
            self.del_widget(spawn_id)

    def get_spawn_entity_ids(self):
        BattlePrepare = global_data.game_mgr.scene.get_com('PartCompetitionBattlePrepare')
        if not (BattlePrepare and BattlePrepare.battle_prepare):
            return
        if not hasattr(BattlePrepare.battle_prepare, 'spawn_mgr'):
            return
        spawn_mgr = BattlePrepare.battle_prepare.spawn_mgr
        if not spawn_mgr:
            return
        for spawn_id, entity_id in six.iteritems(spawn_mgr.get_spawn_entity_id()):
            self.spawn_entity_id[spawn_id] = entity_id

    def update_nd(self):
        self.get_spawn_entity_ids()
        for spawn_id, entity_id in six.iteritems(self.spawn_entity_id):
            if self.is_teammate(entity_id):
                self.show_widget(spawn_id)
            else:
                self.del_widget(spawn_id)

    def is_teammate(self, entity_id):
        if not entity_id:
            return False
        item_entity = EntityManager.getentity(entity_id)
        if item_entity and item_entity.logic:
            return item_entity.logic.ev_g_is_teammate_item()
        return False

    def show_widget(self, spawn_id):
        if spawn_id not in self._widgets:
            if global_data.game_mode.get_mode_type() == game_mode_const.GAME_MODE_SCAVENGE:
                item_id = 0
                if spawn_id in global_data.death_battle_data.spawn_info:
                    item_id = global_data.death_battle_data.spawn_info[spawn_id].get('item_id', 0)
                if item_id in global_data.game_mode.get_cfg_data('play_data').get('sp_item_list', []):
                    self._widgets[spawn_id] = ScavengeItemMark(self.parent_nd, self.map_panel, spawn_id)
                else:
                    self._widgets[spawn_id] = None
            else:
                self._widgets[spawn_id] = BloodBagMapMark(self.parent_nd, self.map_panel, spawn_id)
        if self._widgets[spawn_id]:
            x, y, z = self.spawn_info[spawn_id].get('pos')
            self._widgets[spawn_id].on_update((x, y, z), 0.4)
        return

    def del_widget(self, spawn_id):
        if spawn_id in self._widgets and self._widgets[spawn_id]:
            self._widgets[spawn_id].destroy()
            del self._widgets[spawn_id]

    def _on_scene_observed_player_setted(self, lplayer):
        self.update_nd()

    def get_spawn_lst(self):
        battle = global_data.battle
        if not battle:
            return []
        born_data = global_data.game_mode.get_born_data()
        temp_spawn_lst = born_data[str(battle.area_id)].get('spawn_lst', [])
        if temp_spawn_lst and isinstance(temp_spawn_lst[0], (list, tuple)):
            spawn_lst = []
            for lst in temp_spawn_lst:
                spawn_lst.extend(lst)

        else:
            spawn_lst = temp_spawn_lst
        return spawn_lst