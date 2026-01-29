# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartZoneTriggerManager.py
from __future__ import absolute_import
import six_ex
from . import ScenePart
import math3d
TRIGGER_UPDATE_FRAME = 10
import world
from common.utils.timer import CLOCK
from mobile.common.EntityManager import EntityManager
from mobile.common.IdManager import IdManager
from logic.gutils.CameraHelper import check_in_room
UPDATE_MIN_TIME = 0.5

class PartZoneTriggerManager(ScenePart.ScenePart):
    TRIGGER_NUM = 0
    ENTER_EVENT = {'scene_remove_door_trigger_event': 'remove_scene_trigger',
       'scene_add_door_trigger_event': 'add_scene_trigger',
       'net_login_reconnect_event': 'on_net_login_reconnect',
       'scene_add_agent_robot': 'on_add_agent_robot',
       'scene_del_agent_robot': 'on_del_agent_robot'
       }

    def __init__(self, scene, name):
        super(PartZoneTriggerManager, self).__init__(scene, name)
        self.trigger_map = {}
        from logic.gcommon.common_const.ui_operation_const import MAX_DOOR_SIZE
        grid_with = (MAX_DOOR_SIZE[0] * MAX_DOOR_SIZE[0] + MAX_DOOR_SIZE[2] * MAX_DOOR_SIZE[2]) ** 0.5
        self.grid_manager = world.gridobject_manager(int(grid_with))
        self._pri_list = []
        self.is_entered_door_zone = False
        self.refresh_timer_id = 0
        self.trigger_changed = True
        self.grid_x = None
        self.grid_y = None
        self.agent_robot = set()
        return

    def init_refresh_trigger_timer(self):
        self.refresh_timer_id = global_data.game_mgr.register_logic_timer(self.refresh_trigger, UPDATE_MIN_TIME, mode=CLOCK)

    def on_enter(self):
        self.init_refresh_trigger_timer()

    def on_exit(self):
        global_data.game_mgr.unregister_logic_timer(self.refresh_timer_id)

    def _add_zone_trigger_obj(self, parent_id, entity_id, scene_trigger):
        self.trigger_changed = True
        self.trigger_map[parent_id, entity_id] = scene_trigger

    def _remove_zone_trigger_obj(self, parent_id, entity_id):
        self.trigger_changed = True
        if (parent_id, entity_id) in self.trigger_map:
            del self.trigger_map[parent_id, entity_id]

    def refresh_trigger(self):
        scn = self.scene()
        if not scn:
            return
        else:
            player = scn.get_player()
            if player and player == global_data.cam_lplayer:
                pos = player.ev_g_position()
                if not pos:
                    return
                self.robot_refresh_trigger(player)
                grid_list = self.grid_manager.acquire_obj_list(pos)
                tmp_entered_zone = []
                for str_id in grid_list:
                    house_id, door_id = str_id.split('_', 1)
                    pobj = self.trigger_map.get((house_id, door_id), None)
                    if pobj:
                        if pobj.on_enter_zone(pos):
                            tmp_entered_zone.append(pobj)

                tmp_entered_zone = sorted(tmp_entered_zone, key=lambda a: a.get_dist(pos))
                if len(tmp_entered_zone) > 0:
                    self.is_entered_door_zone = True
                    pobj = tmp_entered_zone[0]
                    dist = pobj.get_dist(pos)
                    player.send_event('E_ENTER_DOOR_INTERACTION_ZONE', pobj.house_id, pobj.id, dist, pobj.open_state)
                elif self.is_entered_door_zone:
                    player.send_event('E_LEAVE_DOOR_INTERACTION_ZONE')
                    self.is_entered_door_zone = False
                self.trigger_changed = False
            return

    def on_add_agent_robot(self, robot_id):
        if robot_id in self.agent_robot:
            return
        self.agent_robot.add(robot_id)

    def on_del_agent_robot(self, robot_id):
        if robot_id in self.agent_robot:
            self.agent_robot.remove(robot_id)

    def robot_refresh_trigger(self, player):
        for eid in self.agent_robot:
            robot = EntityManager.getentity(eid)
            if not robot:
                return
            pos = robot.logic.ev_g_position()
            if not pos:
                continue
            for str_id in self.grid_manager.acquire_obj_list(pos):
                house_id, door_id = str_id.split('_', 1)
                pobj = self.trigger_map.get((house_id, door_id), None)
                if pobj and pobj.on_enter_zone(pos) and not pobj.open_state:
                    house_obj = EntityManager.getentity(IdManager.str2id(house_id))
                    if house_obj:
                        from logic.gcommon.const import DOOR_STATE_OPEN_IN
                        player.send_event('E_CALL_SYNC_METHOD', 'set_door_state', (house_obj.id, int(door_id), DOOR_STATE_OPEN_IN), True)

        return

    def add_scene_trigger(self, house_id, entity_id, trigger_pos, zone_entity):
        house_id = str(house_id)
        entity_id = str(entity_id)
        if (
         house_id, entity_id) in self.trigger_map:
            return
        self._add_zone_trigger_obj(house_id, entity_id, zone_entity)
        self.grid_manager.add_obj(str(house_id) + '_' + str(entity_id), trigger_pos)

    def remove_scene_trigger(self, house_id, entity_id):
        house_id = str(house_id)
        entity_id = str(entity_id)
        self._remove_zone_trigger_obj(house_id, entity_id)
        self.grid_manager.remove_obj(str(house_id) + '_' + str(entity_id))

    def test_add_door(self):
        pos = (-118, 346.68, -114.57)
        from mobile.common.EntityFactory import EntityFactory
        entity = EntityFactory.instance().create_entity('DoorNPC', 123456)
        entity.init_from_dict({'position': pos,'model_name': 'test_men02_110580'})
        entity.on_add_to_battle(123456)

    def test_remove_door(self):
        from mobile.common.EntityManager import EntityManager
        door_entity = EntityManager.getentity(123456)
        if door_entity:
            door_entity.on_remove_from_battle()
            door_entity.destroy()

    def show_all_active_triggers(self, alive_time=10):
        import world
        _points = [math3d.vector(-0.5, -0.5, 0.5), math3d.vector(0.5, -0.5, 0.5), math3d.vector(0.5, -0.5, -0.5), math3d.vector(-0.5, -0.5, -0.5)]
        pts = list(_points)
        pts.extend([ pt + math3d.vector(0, 1, 0) for pt in _points ])
        six_face_idx = {
         (3, 2, 1, 0),
         (0, 1, 5, 4),
         (5, 1, 2, 6),
         (0, 4, 7, 3),
         (2, 3, 7, 6),
         (4, 5, 6, 7)}
        pts_list = []
        for face in six_face_idx:
            quad = []
            quad.extend([ (pts[idx].x, pts[idx].y, pts[idx].z) for idx in face ])
            quad.append(16711680)
            pts_list.append(tuple(quad))

        for tri in six_ex.values(self.trigger_map):
            transform = tri.get_transform()
            pri = world.primitives(world.get_active_scene())
            pri.create_poly4(pts_list)
            pri.world_position = math3d.vector(15.999996, 361.349731, -45.0) + math3d.vector(0, 25, 0)
            pri.world_transformation = transform

    def show_all_active_trigger_wireframe(self, alive_time=10):
        import world
        _points = [math3d.vector(-0.5, -0.5, 0.5), math3d.vector(0.5, -0.5, 0.5), math3d.vector(0.5, -0.5, -0.5), math3d.vector(-0.5, -0.5, -0.5)]
        pts = list(_points)
        pts.extend([ pt + math3d.vector(0, 1, 0) for pt in _points ])
        line_idx = [0, 1, 2, 0, 3, 2, 6, 3, 7, 6, 1, 5, 6, 4, 7, 0, 4, 5, 0]
        pts_list = []
        for idx in line_idx:
            pts_list.append((pts[idx].x, pts[idx].y, pts[idx].z, 16711680))

        for tri in six_ex.values(self.trigger_map):
            transform = tri.get_transform()
            pri = world.primitives(world.get_active_scene())
            pri.create_line_strip(pts_list)
            pri.world_transformation = transform
            self._pri_list.append(pri)

    def _destroy_all_pri(self):
        for pri in self._pri_list:
            pri.remove_from_parent()

        self._pri_list = []

    def on_net_login_reconnect(self, *args):
        self.init_refresh_trigger_timer()