# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathBloodBagUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
from mobile.common.EntityManager import EntityManager
from common.utils.cocos_utils import getScreenSize
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.platform.device_info import DeviceInfo
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from common.utils.ui_utils import get_scale
import math3d
import cc
import math

class BloodBagLocateUI(object):

    def __init__(self, parent, spawn_id, scale):
        self.parent = parent
        self.spawn_id = spawn_id
        self._nd = global_data.uisystem.load_template_create('battle_tdm/battle_tdm_locate_hp')
        self._nd.setVisible(False)
        self._nd.setPosition(0, 0)
        self.space_nd = CCUISpaceNode.Create()
        self.space_nd.AddChild('', self._nd)
        horizontal_margin = 140 * scale
        vertical_margin = 80 * scale
        top_margin = get_scale('40w')
        self.space_nd.set_enable_limit_in_screen(True, horizontal_margin, horizontal_margin, top_margin, vertical_margin)
        self.space_nd.set_screen_check_margin(0, 0, top_margin, 0)
        self.run_timer = None
        self.on_tick()
        return

    def on_finalize_panel(self):
        self.clear_run_timer()
        self._nd and self._nd.Destroy()
        self._nd = None
        self.space_nd and self.space_nd.Destroy()
        self.space_nd = None
        return

    def update_wrapper(self, pos):
        if not pos:
            return
        x, y, z = pos
        self.position = math3d.vector(x, y + 10, z)
        self.space_nd.set_assigned_world_pos(self.position)

    def update_nd_pos(self):
        if not self.position:
            return
        cam = global_data.game_mgr.scene.active_camera
        if not cam:
            return
        is_in_screen = self.space_nd.get_is_in_screen()
        dist = cam.position - self.position
        dist = dist.length / NEOX_UNIT_SCALE
        max_dist = 1000
        scale = max(0.5, (max_dist - dist) * 1.0 / max_dist)
        self._nd.setScale(scale)
        lplayer = global_data.cam_lplayer
        if lplayer:
            player_pos = lplayer.ev_g_position()
            dist = (player_pos - self.position).length / NEOX_UNIT_SCALE
            if global_data.mecha and global_data.mecha.logic:
                percent = global_data.mecha.logic.ev_g_health_percent() * 100
            else:
                percent = lplayer.ev_g_health_percent() * 100
            self._nd.setVisible(dist <= 50 and percent <= 50 and not is_in_screen)
            self._nd.nd_simple.setVisible(True)
            if not is_in_screen:
                target_camera_pos = cam.world_to_camera(self.position)
                angle = math.atan2(target_camera_pos.y, target_camera_pos.x)
                angle = angle * 180 / math.pi
                if angle < 0:
                    angle += 360
                self._nd.nd_simple.dir.setRotation(-angle + 90)

    def on_tick(self):
        self.clear_run_timer()
        self.run_timer = global_data.game_mgr.get_logic_timer().register(func=self.update_nd_pos, interval=1)

    def clear_run_timer(self):
        self.run_timer and global_data.game_mgr.get_logic_timer().unregister(self.run_timer)
        self.run_timer = None
        return


class DeathBloodBagUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.panel.setLocalZOrder(1)
        self.init_parameters()
        self.process_event(True)
        self.init_spawn_info()
        self.update_nd()

    def on_finalize_panel(self):
        for widget in six.itervalues(self._widgets):
            widget.on_finalize_panel()

        self._widgets = {}
        self.process_event(False)

    def init_parameters(self):
        self.spawn_entity_id = {}
        self.spawn_info = {}
        self._widgets = {}

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
            self._widgets[spawn_id] = BloodBagLocateUI(self, spawn_id, self.panel.getScale())
        x, y, z = self.spawn_info[spawn_id].get('pos')
        self._widgets[spawn_id].update_wrapper((x, y, z))

    def del_widget(self, spawn_id):
        if spawn_id in self._widgets:
            self._widgets[spawn_id].on_finalize_panel()
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