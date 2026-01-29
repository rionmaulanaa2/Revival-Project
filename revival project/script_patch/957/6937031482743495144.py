# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartPickableManager.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from . import ScenePart
import weakref
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.vscene.parts.PartBoxManager import PartBoxManager
from logic.vscene.parts.PartPickableModelManager import PartPickableModelManager
from logic.gutils import item_utils
from logic.gcommon.item.item_const import SCENEBOX_ST_OPENED
from logic.gcommon.item.item_utility import is_deadbox
from common.utils.cocos_utils import cocos_pos_to_neox
from logic.gcommon.item import client_item_pick_check_handler
import logic.gcommon.common_utils.item_config as item_conf
import math3d
PICKER_UPDATE_FRAME = 10
GRID_WIDTH = int(NEOX_UNIT_SCALE * 25.0)
ONLY_SHOW_IN_MECHA = [9902]
BOX_CHECK_DIS = 30 * NEOX_UNIT_SCALE
PICK_ABLE_DIS = 3 * NEOX_UNIT_SCALE

class PickableObj(object):

    def __init__(self, eid, model, data):
        self.id = eid
        self.model = weakref.ref(model)
        self.data = data


class PartPickableManager(ScenePart.ScenePart):
    PICKABLE_TYPE_CONF = {'ak47': [
              'model/scene/pvp/common/barrel.gim']
       }
    INIT_EVENT = {'scene_pick_obj_event': 'pick_obj_common',
       'on_player_parachute_stage_changed': 'on_player_parachute_stage_changed',
       'scene_pick_model': 'pick_obj_model',
       'scene_add_pick_obj_event': 'add_pick_obj',
       'scene_mod_pick_obj_event': 'mod_pick_obj',
       'scene_remove_pick_obj_event': 'remove_pick_obj',
       'scene_set_special_pick_request_pos_event': 'set_special_request_pos_event',
       'switch_judge_camera_event': 'switch_judge_camera',
       'set_pickable_manager_get_pos_type': 'set_pickable_manager_get_pos_type'
       }

    def __init__(self, scene, name):
        super(PartPickableManager, self).__init__(scene, name, True)
        import world
        from common.utils.gridobject_manager import GridObjectManager
        if scene.is_pve_scene():
            grid_width = GRID_WIDTH * 2 if 1 else GRID_WIDTH
            self.grid_manager = world.gridobject_manager(grid_width)
            self.is_support_grid_map_to_auto_obj = global_data.feature_mgr.is_support_grid_map_to_auto_obj()
            self.py_grid_manager = self.is_support_grid_map_to_auto_obj or GridObjectManager(grid_width)
        else:
            self.py_grid_manager = None
        self.pickable_map = {}
        self.pickable_set = None
        self.delete_list = []
        self.rogue_box_set = set()
        self.update_frame_count = 0
        self._specified_grid_request_pos = None
        self.get_pos_from_model = False
        from logic.gutils import judge_utils
        self.is_judge_ob = judge_utils.is_ob()
        if self.is_judge_ob:
            self.get_quest_pos_func = self.get_quest_pos_for_judge
        else:
            self.get_quest_pos_func = self.get_quest_pos
        return

    def on_pre_load(self):
        self._part_ui_list = (
         (
          True, 'PickUI', 'logic.comsys.battle', ()),
         (
          True, 'BagUI', 'logic.comsys.control_ui', ()))
        self.add_to_loading_wrapper()

    def on_load(self):
        self.create_pick_ui()
        PartBoxManager()
        PartPickableModelManager()

    def on_enter(self):
        self.create_ui()
        self.scene().set_lod_use_player_pos(1, True)
        self.set_pickable_manager_get_pos_type(False)
        self.pve_fix = global_data.game_mode.is_pve()

    def on_player_parachute_stage_changed(self, stage):
        from logic.gutils.template_utils import set_ui_list_visible_helper
        if not global_data.player or not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.id != global_data.player.id:
            return
        if global_data.player.logic.ev_g_is_parachute_stage_land():
            set_ui_list_visible_helper(['PickUI', 'BagUI'], True, 'PARACHUTE')
        else:
            ui_inst = global_data.ui_mgr.get_ui('BagUI')
            if ui_inst:
                ui_inst.disappear()
            set_ui_list_visible_helper(['PickUI', 'BagUI'], False, 'PARACHUTE')

    def on_exit(self):
        self.destroy_ui()
        global_data.box_mgr and global_data.box_mgr.finalize()
        global_data.pickable_model_mgr and global_data.pickable_model_mgr.finalize()
        self.get_quest_pos_func = None
        return

    def create_pick_ui(self, *args):
        from logic.comsys.battle.PickUI import PickUI
        pick_ui = PickUI()
        if global_data.is_pc_mode:
            from logic.comsys.control_ui.BagUIPC import BagUIPC
            BagUIPC(pick_ui.panel, player=pick_ui.player)
        else:
            from logic.comsys.control_ui.BagUI import BagUI
            BagUI(pick_ui.panel, player=pick_ui.player)

    def create_ui(self, *args):
        pass

    def destroy_ui(self, *args):
        global_data.ui_mgr.close_ui('BagUI')
        global_data.ui_mgr.close_ui('PickUI')

    def is_auto_obj(self, entity_id):
        conf = self.get_pickable_obj_conf(entity_id)
        return bool(conf.get('auto_use', 0) and conf.get('auto_pick', 0))

    def add_pick_obj(self, entity_id, model, conf):
        if entity_id is None:
            log_error('entity_id is None')
            import traceback
            traceback.print_stack()
            return
        else:
            obj = PickableObj(entity_id, model, conf)
            self.pickable_map[entity_id] = obj
            is_auto_obj = self.is_auto_obj(entity_id)
            if self.py_grid_manager:
                self.grid_manager.add_obj(str(entity_id), model.world_position)
                if is_auto_obj:
                    self.py_grid_manager.add_obj(str(entity_id), model.world_position, True)
            else:
                self.grid_manager.add_obj(str(entity_id), model.world_position, is_auto_obj)
            item_id = obj.data.get('item_id', 1)
            if item_utils.is_package_item(item_id):
                from logic.gutils.item_utils import is_rouge_box, is_pve_box
                if is_rouge_box(item_id) or is_pve_box(item_id):
                    self.rogue_box_set.add(str(entity_id))
            return

    def mod_pick_obj(self, entity_id, conf):
        if entity_id in self.pickable_map:
            self.pickable_map[entity_id].data.update(conf)

    def remove_pick_obj(self, entity_id):
        if entity_id in self.pickable_map:
            del self.pickable_map[entity_id]
        if entity_id in self.rogue_box_set:
            self.rogue_box_set.remove(entity_id)
        is_auto_obj = self.is_auto_obj(entity_id)
        if self.py_grid_manager:
            self.grid_manager.remove_obj(str(entity_id))
            if is_auto_obj:
                self.py_grid_manager.remove_obj(str(entity_id), is_auto_obj)
        else:
            self.grid_manager.remove_obj(str(entity_id), is_auto_obj)

    def pick_object(self):
        player = self.get_player()
        if not player:
            return
        else:
            player_pos = player.ev_g_position()
            delete_list = []
            not_valid_obj = []
            for wid, pobj in six.iteritems(self.pickable_map):
                tobj = pobj.model()
                if tobj is None:
                    not_valid_obj.append(wid)
                    continue
                dis_vec = player_pos - tobj.position
                if dis_vec.length < 50.0:
                    delete_list.append((wid, tobj))

            if delete_list:
                model = player.ev_g_model()
                forward = model.world_transformation.forward
                player_pos = player.ev_g_position()
                min_angle = None
                min_angle_obj = None
                min_id = None
                for wid, obj in delete_list:
                    obj_dir = obj.position - player_pos
                    obj_dir.y = 0
                    obj_dir.normalize()
                    angle = obj_dir.dot(forward)
                    if not min_angle or angle > min_angle:
                        min_angle = angle
                        min_angle_obj = obj
                        min_id = wid

                if min_angle_obj:
                    conf = self.get_pickable_obj_conf(min_id)
                    self.pick_obj_model(min_id)
                    item_utils.pick_obj(player, min_id)
            if not_valid_obj:
                print('not valid objs: %s' % str(not_valid_obj))
            return

    def on_update(self, dt):
        self.update_auto_use_pickable()
        if self.update_frame_count == 0:
            self.update_frame_count = PICKER_UPDATE_FRAME
            self.update_pickable()
        self.update_frame_count -= 1

    def get_pickable_obj_conf(self, e_id):
        pobj = self.pickable_map.get(e_id, None)
        if pobj is None:
            return {}
        else:
            conf = pobj.data
            return conf

    def get_pickable_list(self, is_auto=False):
        check_pos = self.get_quest_pos_func()
        if not check_pos:
            return []
        else:
            import bson.objectid as objectid
            pickable_list = []
            player_pos = check_pos
            if not player_pos:
                return []
            if is_auto:
                if self.py_grid_manager:
                    grid_list = self.py_grid_manager.acquire_auto_obj_list(player_pos)
                else:
                    grid_list = self.grid_manager.acquire_auto_obj_list(player_pos)
            else:
                grid_list = self.grid_manager.acquire_obj_list(player_pos)
                if hasattr(global_data.battle, 'get_cargos'):
                    grid_list = set(grid_list)
                    train_cargos_list = global_data.battle.get_cargos()
                    for cargo in train_cargos_list:
                        if cargo not in grid_list:
                            grid_list.add(cargo)

                    grid_list = tuple(grid_list)
            if self.pve_fix:
                dist = PICK_ABLE_DIS * 5.5
            else:
                dist = PICK_ABLE_DIS * 0.34
                if global_data.player and global_data.player.logic:
                    if global_data.player.logic.ev_g_in_mecha():
                        dist = PICK_ABLE_DIS
            pick_range_factor = 0
            if global_data.player and global_data.player.logic:
                pick_range_factor = global_data.player.logic.ev_g_add_attr('pick_range_factor')
            dist = dist * (1 + pick_range_factor)
            if dist > 5000:
                grid_list = six.iterkeys(self.pickable_map)
            for str_entity_id in grid_list:
                entity_id = objectid.ObjectId(str_entity_id)
                pobj = self.pickable_map.get(entity_id, None)
                if pobj is None:
                    continue
                obj_model = pobj.model()
                if not obj_model or not obj_model.valid:
                    continue
                dis_vec = player_pos - obj_model.position
                if dis_vec.length - obj_model.bounding_box.x < dist * 2:
                    if self.pve_fix:
                        y_limit = 10.0 * NEOX_UNIT_SCALE * (1 + pick_range_factor)
                    else:
                        y_limit = 3.0 * NEOX_UNIT_SCALE
                    if abs(player_pos.y - obj_model.position.y) <= y_limit:
                        pickable_list.append([entity_id, 1])

            return pickable_list

    def update_auto_use_pickable(self):
        player = self.get_player()
        if not player:
            return
        else:
            auto_pickable_list = self.get_pickable_list(is_auto=True)
            for eid, num in auto_pickable_list:
                conf = self.get_pickable_obj_conf(eid)
                faction_id = conf.get('faction_id', -1)
                if faction_id > 0 and faction_id != player.ev_g_group_id():
                    continue
                if not self.check_can_pick(player, conf.get('item_id', 0)):
                    continue
                house_entity_id = conf.get('house_entity_id', None)
                item_utils.pick_obj(player, eid, None, -1, house_entity_id, None)

            return

    def check_can_pick(self, unit_obj, item_id):
        conf = item_conf.get_use_by_id(item_id)
        if conf:
            check_handler_name = conf.get('cClientPickCheckHandler')
            check_args = conf.get('cClientPickCheckArgs', {})
            if check_handler_name:
                check_handler = getattr(client_item_pick_check_handler, check_handler_name)
                if callable(check_handler):
                    ret = check_handler(unit_obj, item_id, check_args)
                    if not ret:
                        return False
        return True

    def update_pickable(self):
        check_pos = self.get_quest_pos_func()
        if not check_pos:
            return []
        else:
            import bson.objectid as objectid
            box_list = []
            grid_list = self.grid_manager.acquire_obj_list(check_pos)
            pickable_list = self.get_pickable_list()
            box_candidates = set(grid_list) | self.rogue_box_set
            for str_entity_id in box_candidates:
                entity_id = objectid.ObjectId(str_entity_id)
                pobj = self.pickable_map.get(entity_id, None)
                if pobj is None:
                    continue
                obj_model = pobj.model()
                if not obj_model or not obj_model.valid:
                    continue
                item_id = pobj.data.get('item_id', 1)
                if not item_utils.is_package_item(item_id):
                    continue
                dis_vec = check_pos - obj_model.position
                box_check_dis = item_utils.get_hint_distance(item_id, default=BOX_CHECK_DIS)
                if global_data.player and global_data.player.logic:
                    box_check_dis = box_check_dis * (1.0 + global_data.player.logic.ev_g_attr_get('box_check_dis_factor', 0))
                if dis_vec.length <= box_check_dis:
                    box_list.append(weakref.ref(pobj))

            conf_list = []
            pickable_set = {}
            changed = False
            group_id = global_data.player.logic.ev_g_group_id() if global_data.player and global_data.player.logic else None
            for eid, num in pickable_list:
                conf = self.get_pickable_obj_conf(eid)
                faction_id = conf.get('faction_id', -1)
                if faction_id > 0 and faction_id != group_id:
                    continue
                if self.is_auto_obj(eid):
                    continue
                if conf and conf.get('status', None) == SCENEBOX_ST_OPENED and not is_deadbox(conf.get('item_id')):
                    continue
                conf_list.append((eid, conf))
                pickable_set[eid] = conf
                if 'changed' in conf and conf['changed']:
                    changed = True
                    del conf['changed']

            if changed or self.pickable_set != pickable_set:
                self.pickable_set = pickable_set
                global_data.emgr.scene_update_pick_info_event.emit(conf_list)
            global_data.emgr.scene_update_box_info_event.emit(box_list)
            return

    def pick_obj_common(self, item_no=None, package_part=None, put_pos=-1, house_entity_id=None, parent_entity_id=None):
        player = global_data.player.logic
        if not player.ev_g_status_check_pass('ST_PICK'):
            return
        else:
            if item_no is None:
                self.pick_object()
            else:
                self.pick_specific_object(item_no, package_part, put_pos, house_entity_id, parent_entity_id)
            return

    def pick_obj_model(self, entity_id):
        pobj = self.pickable_map.get(entity_id, None)
        player = global_data.player.logic
        if pobj is not None and player is not None:
            model = pobj.model()
            player_model = player.ev_g_model()
            if model and player_model:
                player.send_event('E_TRY_PICK_UP', model.world_position, player_model.world_position)
                return
            import math3d
            pos = math3d.vector(0, 0, 0)
            player.send_event('E_TRY_PICK_UP', pos, pos)
        return

    def pick_specific_object(self, item_no, package_part=None, put_pos=-1, house_entity_id=None, parent_entity_id=None):
        if item_no in self.pickable_map or parent_entity_id in self.pickable_map:
            player = global_data.player.logic
            eid = parent_entity_id or item_no
            pobj = self.pickable_map.get(eid, None)
            if pobj is None:
                conf = {}
            else:
                conf = pobj.data
                self.pick_obj_model(eid)
            house_entity_id = conf.get('house_entity_id', None)
            item_utils.pick_obj(player, item_no, package_part, put_pos, house_entity_id, parent_entity_id)
        return

    def test_add_pickable_weapons(self):
        pos = self.get_quest_pos_func()
        if not pos:
            return
        import common.cfg.confmgr as confmgr
        conf = confmgr.get('firearm_config')
        import world
        import random
        item_num = 100
        import math3d
        scn = self.scene()

        def _get_landscape_height--- This code section failed: ---

 498       0  LOAD_DEREF            0  'math3d'
           3  LOAD_ATTR             0  'vector'
           6  LOAD_ATTR             1  'scene_col'
           9  LOAD_FAST             1  'z'
          12  CALL_FUNCTION_3       3 
          15  STORE_FAST            2  'start_p'

 499      18  LOAD_DEREF            0  'math3d'
          21  LOAD_ATTR             0  'vector'
          24  LOAD_ATTR             2  'hit_by_ray'
          27  LOAD_FAST             1  'z'
          30  CALL_FUNCTION_3       3 
          33  STORE_FAST            3  'end_p'

 500      36  LOAD_DEREF            1  'scn'
          39  LOAD_ATTR             1  'scene_col'
          42  LOAD_ATTR             2  'hit_by_ray'
          45  LOAD_FAST             2  'start_p'
          48  LOAD_FAST             3  'end_p'
          51  CALL_FUNCTION_2       2 
          54  STORE_FAST            4  'result'

 501      57  LOAD_FAST             4  'result'
          60  LOAD_CONST            3  ''
          63  BINARY_SUBSCR    
          64  POP_JUMP_IF_FALSE    83  'to 83'

 502      67  LOAD_FAST             4  'result'
          70  LOAD_CONST            4  1
          73  BINARY_SUBSCR    
          74  LOAD_ATTR             3  'y'
          77  STORE_FAST            5  'y'
          80  JUMP_FORWARD          6  'to 89'

 504      83  LOAD_CONST            5  400
          86  STORE_FAST            5  'y'
        89_0  COME_FROM                '80'

 505      89  LOAD_FAST             5  'y'
          92  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_3' instruction at offset 12

        pos_list = []
        for idx in range(item_num):
            x = random.choice(range(-100, 100))
            z = random.choice(range(-100, 100))
            y = _get_landscape_height(pos.x + x, pos.z + z)
            print('pos', x, y, z)
            pos_list.append((x, y, z))

        def test_add_drop(id, pos, type, data):
            from mobile.common.EntityFactory import EntityFactory
            entity = EntityFactory.instance().create_entity('Pickable', id)
            entity.init_from_dict({'mtype': 'ak47','pos': pos,'data': data})
            entity.on_add_to_battle(global_data.player.battle_id)

        for idx in range(item_num):
            key = random.choice(['1', '2', '3', '4'])
            val = conf._conf[key]
            val.update({'iBulletNum': random.randint(0, 50),'iBolted': 0})
            test_add_drop(idx + 1000, pos_list[idx], key, val)

    def get_player(self):
        return global_data.cam_lplayer

    def get_quest_pos(self):
        if global_data.cam_lplayer:
            return global_data.cam_lplayer.ev_g_position()

    def get_quest_pos_from_model(self):
        if global_data.cam_lplayer:
            model = global_data.cam_lplayer.ev_g_model()
            if model:
                return model.world_position

    def get_quest_pos_for_judge(self):
        if self._specified_grid_request_pos:
            return self._specified_grid_request_pos
        if global_data.cam_lplayer:
            return global_data.cam_lplayer.ev_g_position()

    def get_quest_pos_from_model_for_judge(self):
        if self._specified_grid_request_pos:
            return self._specified_grid_request_pos
        if global_data.cam_lplayer:
            model = global_data.cam_lplayer.ev_g_model()
            if model:
                return model.world_position

    def set_special_request_pos_event(self, pos):
        self._specified_grid_request_pos = pos
        self.pickable_set = None
        global_data.emgr.scene_update_pick_info_event.emit([])
        return

    def on_touch_tap(self, touches):
        if not global_data.is_judge_ob:
            return
        else:
            if not global_data.is_in_judge_camera:
                return
            location = touches.getLocation()
            x, y = cocos_pos_to_neox(location.x, location.y)
            if global_data.feature_mgr.is_support_scene_pick_bounding_box_offset():
                model = self.scene().pick_ex(x, y, 'paradrop_item', 1, None, None, math3d.vector(1, 1, 1))[0]
            else:
                model = self.scene().pick(x, y, 'paradrop_item', 1)[0]
            if model:
                global_data.emgr.scene_set_special_pick_request_pos_event.emit(model.world_position)
            elif self._specified_grid_request_pos:
                global_data.emgr.scene_set_special_pick_request_pos_event.emit(None)
            return

    def switch_judge_camera(self, enable, *args):
        if not enable:
            if self._specified_grid_request_pos:
                global_data.emgr.scene_set_special_pick_request_pos_event.emit(None)
        return

    def set_pickable_manager_get_pos_type(self, from_model):
        self.get_pos_from_model = from_model
        if self.is_judge_ob:
            if from_model:
                self.get_quest_pos_func = self.get_quest_pos_from_model_for_judge
            else:
                self.get_quest_pos_func = self.get_quest_pos_for_judge
        elif from_model:
            self.get_quest_pos_func = self.get_quest_pos_from_model
        else:
            self.get_quest_pos_func = self.get_quest_pos