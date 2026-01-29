# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHouseAppearance.py
from __future__ import absolute_import
import six_ex
import six
from ..UnitCom import UnitCom
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from mobile.common.EntityManager import EntityManager
from logic.gcommon.item import item_const
import time
import world
import render
import math3d
import weakref
from logic.gutils.soc_utils import set_model_attach_soc

class ComHouseAppearance(UnitCom):
    BIND_EVENT = {'G_PICK_DATA': 'get_pickobject_detail_conf',
       'G_HOUSE_PICK_MODEL': 'get_pickobject_detail_model',
       'E_HOUSE_ADD_ITEM': 'on_add_item',
       'E_HOUSE_DEL_ITEM': 'on_del_item'
       }
    DROP_MODEL_PATH = 'model_new/items/empty/empty.gim'

    def __init__(self):
        super(ComHouseAppearance, self).__init__()
        self.house_pick_obj_map = {}
        self.house_pick_detail_map = {}
        self.house_drop_obj_map = {}
        self.house_pick_data = {}
        self.house_aabb = math3d.aabb()
        self.house_index = None
        self.house_matrix = None
        self._show_pickobj = False
        self._show_detail = False
        self._house_type = ''
        self.house_obj_check_map = {}
        self.init_house_folder()
        self.detail_obj_task = set()
        self.obj_task = set()
        self.house_drop_timer = None
        return

    def init_house_folder(self):
        if not global_data.player:
            return
        battle = global_data.player.get_battle() or global_data.player.get_joining_battle()
        map_id = str(battle.map_id)
        house_path = confmgr.get('map_config', str(map_id), 'cHousePath')
        house_folder = 'item_control/%s' % house_path
        self.house_folder = house_folder

    def init_from_dict(self, unit_obj, bdict):
        super(ComHouseAppearance, self).init_from_dict(unit_obj, bdict)
        item_datas = bdict.get('item_data', None)
        self.house_index = bdict.get('house_index', None)
        self.extra_pos = bdict.get('extra_pos', [])
        if self.house_index is not None:
            house_list = confmgr.get(self.house_folder + '/' + 'house_info', 'data', default=None)
            if not house_list:
                log_error('[house pick data] house_info.json is need!!!')
                return
            if not (self.house_index >= 0 and self.house_index < len(house_list)):
                import traceback
                log_error('[house_index out of range] index: %s len: %s' % (self.house_index, len(house_list)))
                traceback.print_stack()
                return
            house_info_map = house_list[self.house_index]
            rot = house_info_map['rot']
            pos = house_info_map['pos']
            scale = house_info_map['scale']
            scale = [scale[0], 0, 0, 0, 0, scale[1], 0, 0, 0, 0, scale[2], 0, 0, 0, 0, 1]
            house_mat_data = rot[:-4] + pos + [1]
            scale_matrix = math3d.matrix()
            scale_matrix.set_all(scale)
            self.house_matrix = math3d.matrix()
            self.house_matrix.set_all(house_mat_data)
            self.house_matrix = scale_matrix * self.house_matrix
            if item_datas or self.extra_pos:
                self.create_house_pick_items(item_datas)
            house_type = house_info_map['type']
            try:
                _pos = house_type.index('_')
                house_type = house_type[_pos + 1:]
            except:
                pass

            self._house_type = house_type
        self._add_to_system()
        return

    def reuse(self, share_data):
        super(ComHouseAppearance, self).reuse(share_data)
        self.house_aabb = math3d.aabb()

    def cache(self):
        self._clear()
        super(ComHouseAppearance, self).cache()

    def _model_load_helper(self, path, callback, args):
        self.obj_task.add(world.create_model_async(path, callback, args))

    def _model_detail_load_helper(self, path, callback, args):
        from logic.gutils.mode_utils import get_mapped_res_path
        mapped_path = get_mapped_res_path(path)
        from logic.gutils import scene_utils
        mapped_path = scene_utils.scene_replace_res(mapped_path)
        self.detail_obj_task.add(world.create_model_async(mapped_path, callback, args))

    def get_pickobject_detail_conf(self):
        return self.house_pick_data

    def get_pickobject_detail_model(self):
        return self.house_pick_detail_map

    def on_add_item(self, item_data, drop_anim=None):
        item_id = item_data.get('item_id')
        entity_id = item_data.get('entity_id')
        pos = item_data.get('pos')
        is_appendant = item_data.get('is_appendant', False)
        appendant = item_data.get('appendant', [])
        thrower = item_data.get('thrower', None)
        house_entity_id = self.unit_obj.id
        item_data['house_entity_id'] = house_entity_id
        count = item_data.get('count')
        is_global_pos = item_data.get('is_global_pos', False)
        obj_conf = confmgr.get('item', str(item_id), default=None)
        if obj_conf:
            item_no_conf = {'wid': entity_id,'item_id': item_id,'house_entity_id': house_entity_id,'count': count,'is_appendant': is_appendant,'appendant': appendant,'thrower': thrower}
            item_no_conf.update(obj_conf)
            if is_global_pos:
                pos = math3d.vector(pos[0], pos[1], pos[2])
            else:
                pos = math3d.vector(pos[0], pos[1], pos[2]) * self.house_matrix
            self.house_pick_data[entity_id] = (
             pos, item_no_conf)
            self.house_aabb.merge(pos)
            if self._show_pickobj:
                self._model_load_helper(item_no_conf['fx_res'], self._load_callback, (entity_id, pos, item_no_conf))
            if self._show_detail:
                self._model_detail_load_helper(item_no_conf['res'], self._load_detail_model_callback, (
                 entity_id, pos, drop_anim))
        return

    def on_del_item(self, entity_id):
        if entity_id in self.house_pick_data:
            global_data.emgr.scene_remove_pick_obj_event.emit(entity_id)
            del self.house_pick_data[entity_id]
        from logic.gutils import item_utils
        is_pick_by_avatar = False
        player = global_data.player
        if player and player.logic:
            pick_succ = player.logic.ev_g_pick_succ()
            if pick_succ and entity_id in pick_succ:
                is_pick_by_avatar = True
        if entity_id in self.house_pick_obj_map:
            if is_pick_by_avatar:
                item_utils.show_pick_animation(player, self.house_pick_obj_map[entity_id])
            else:
                self.house_pick_obj_map[entity_id].destroy()
            del self.house_pick_obj_map[entity_id]
        if entity_id in self.house_pick_detail_map:
            if is_pick_by_avatar:
                item_utils.show_pick_animation(player, self.house_pick_detail_map[entity_id])
            else:
                self.house_pick_detail_map[entity_id].destroy()
            del self.house_pick_detail_map[entity_id]
        if entity_id in self.house_drop_obj_map:
            self.house_drop_obj_map[entity_id][0].destroy()
            del self.house_drop_obj_map[entity_id]

    def create_house_pick_items(self, item_datas):
        for eid, item in six.iteritems(item_datas):
            self.on_add_item(item)

        for pos in self.extra_pos:
            pos = math3d.vector(*pos)
            self.house_aabb.merge(pos)

        self.create_house_pick_trigger()

    def create_house_pick_trigger(self):
        scene = self.scene
        mat = math3d.matrix()
        mat.do_translate(self.house_aabb.center)
        center = self.house_aabb.center
        size = self.house_aabb.half * 2.0
        in_trigger = scene.add_scene_trigger_ps(str(self.unit_obj.id) + 'in', center, size + math3d.vector(140, 200, 140) * NEOX_UNIT_SCALE)
        out_trigger = scene.add_scene_trigger_ps(str(self.unit_obj.id) + 'out', center, size + math3d.vector(180, 200, 180) * NEOX_UNIT_SCALE)
        detail_trigger = scene.add_scene_trigger_ps(str(self.unit_obj.id) + 'detail', center, size + math3d.vector(100, 80, 100) * NEOX_UNIT_SCALE)
        in_trigger.add_event(world.SCENE_TRIGGER_CALLBACK)
        out_trigger.add_event(world.SCENE_TRIGGER_CALLBACK)
        detail_trigger.add_event(world.SCENE_TRIGGER_CALLBACK)
        in_trigger.set_callback(self._create_item_models, None)
        out_trigger.set_callback(None, self._release_item_models)
        detail_trigger.set_callback(self._create_detail_models, self._release_detail_models)
        return

    def _create_item_models(self, *args):
        if self._show_pickobj:
            return
        else:
            self._show_pickobj = True
            for entity_id, data in six.iteritems(self.house_pick_data):
                pos, item_conf = data
                fx_res = item_conf.get('fx_res')
                if fx_res is None:
                    continue
                self._model_load_helper(fx_res, self._load_callback, (entity_id, pos, item_conf))

            return

    def _release_item_models(self, *args):
        self._release_detail_models()
        if not self._show_pickobj:
            return
        self._show_pickobj = False
        for entity_id, model in six.iteritems(self.house_pick_obj_map):
            global_data.emgr.scene_remove_pick_obj_event.emit(entity_id)
            if model.valid:
                model.destroy()

        for task in self.obj_task:
            if task.valid:
                task.cancel()

        self.obj_task = set()
        self.house_pick_obj_map.clear()

    def _create_detail_models(self, *args):
        if self._show_detail:
            return
        else:
            self._show_detail = True
            for entity_id, data in six.iteritems(self.house_pick_data):
                pos, item_conf = data
                self._model_detail_load_helper(item_conf['res'], self._load_detail_model_callback, (entity_id, pos, None))

            return

    def _release_detail_models(self, *args):
        if not self._show_detail:
            return
        self._show_detail = False
        for model in six.itervalues(self.house_pick_detail_map):
            if model.valid:
                model.destroy()

        for task in self.detail_obj_task:
            if task.valid:
                task.cancel()

        self.detail_obj_task = set()
        self.house_pick_detail_map.clear()
        for drop_info in six.itervalues(self.house_drop_obj_map):
            model = drop_info[0]
            if model.valid:
                model.destroy()

        self.house_drop_obj_map.clear()

    def _load_callback(self, model, userdata, task):
        entity_id, pos, conf = userdata
        task_cancel = False
        if task in self.obj_task:
            self.obj_task.remove(task)
        else:
            task_cancel = True
        if not model or not model.valid:
            return
        else:
            if not self.house_matrix and self.house_index is None:
                model.destroy()
                return
            if task_cancel or entity_id not in self.house_pick_data:
                model.destroy()
                return
            self.house_pick_obj_map[entity_id] = model
            self.scene.add_object(model)
            model.world_position = pos
            model.render_level = -2
            model.lod_config = (55 * NEOX_UNIT_SCALE, 55 * NEOX_UNIT_SCALE)
            if hasattr(model, 'update_lod_now'):
                model.update_lod_now()
            global_data.emgr.scene_add_pick_obj_event.emit(entity_id, model, conf)
            set_model_attach_soc(model, False)
            return

    def _load_detail_model_callback(self, detail_model, userdata, task):
        entity_id, pos, drop_anim = userdata
        task_cancel = False
        if task in self.detail_obj_task:
            self.detail_obj_task.remove(task)
        else:
            task_cancel = True
        if task_cancel or entity_id not in self.house_pick_data:
            detail_model.destroy()
            return
        else:
            self.house_pick_detail_map[entity_id] = detail_model
            self.scene.add_object(detail_model)
            detail_model.position = pos
            detail_model.render_level = -1
            detail_model.lod_config = (15 * NEOX_UNIT_SCALE, 15 * NEOX_UNIT_SCALE)
            if hasattr(detail_model, 'update_lod_now'):
                detail_model.update_lod_now()
            if drop_anim and self._load_drop_model(entity_id, drop_anim):
                return
            self.scene.add_to_group(detail_model, 'pickable_item')
            detail_model.pickable = True
            global_data.emgr.scene_add_pickable_model_event.emit(detail_model, (entity_id, self.unit_obj.id), None)
            set_model_attach_soc(detail_model, False)
            return

    def _load_drop_model(self, entity_id, drop_anim):
        if entity_id not in self.house_pick_data:
            return False
        else:
            dst_pos, item_conf = self.house_pick_data[entity_id]
            thrower_id = item_conf.get('thrower')
            if not thrower_id:
                return False
            src_pos = None
            thrower = EntityManager.getentity(thrower_id)
            if thrower and thrower.logic:
                src_pos = thrower.logic.ev_g_position()
            src_pos = src_pos or dst_pos
            drop_model = world.model(self.DROP_MODEL_PATH, self.scene)
            self.house_drop_obj_map[entity_id] = (drop_model, time.time(), src_pos, dst_pos)
            anim_name = 'battery_drop' if drop_anim == item_const.ITEM_DROP_ANIM_MECH else 'item_drop'
            drop_model.play_animation(anim_name)
            self.start_drop_timer()
            set_model_attach_soc(drop_model, False)
            return True

    def tick(self, dt):
        now = time.time()
        for eid in six_ex.keys(self.house_drop_obj_map):
            drop_model, init_time, src_pos, dst_pos = self.house_drop_obj_map[eid]
            detail_model = self.house_pick_detail_map.get(eid)
            sfx_model = self.house_pick_obj_map.get(eid)
            if not detail_model or not sfx_model:
                del self.house_drop_obj_map[eid]
                drop_model.destroy()
                continue
            u = min((now - init_time) / 0.7, 1)
            intrp_pos = math3d.vector(0, 0, 0)
            intrp_pos.intrp(src_pos, dst_pos, u)
            pos = intrp_pos + drop_model.get_bone_prs(0)[0]
            detail_model.world_position = pos
            sfx_model.world_position = pos
            if u >= 1:
                del self.house_drop_obj_map[eid]
                drop_model.destroy()
                self.scene.add_to_group(detail_model, 'pickable_item')
                detail_model.pickable = True
                global_data.emgr.scene_add_pickable_model_event.emit(detail_model, (eid, self.unit_obj.id), None)

        if not self.house_drop_obj_map:
            self.stop_drop_timer()
        return

    def _clear(self):
        self.stop_drop_timer()
        str_unit_id = str(self.unit_obj.id)
        self.scene.remove_scene_trigger(str_unit_id + 'in')
        self.scene.remove_scene_trigger(str_unit_id + 'out')
        self.scene.remove_scene_trigger(str_unit_id + 'detail')
        for entity_id, model in six.iteritems(self.house_pick_obj_map):
            global_data.emgr.scene_remove_pick_obj_event.emit(entity_id)
            if model.valid:
                model.destroy()

        for detail_model in six.itervalues(self.house_pick_detail_map):
            global_data.emgr.scene_del_pickable_model_event.emit(detail_model, None)
            if detail_model.valid:
                detail_model.destroy()

        for drop_info in six.itervalues(self.house_drop_obj_map):
            drop_model = drop_info[0]
            if drop_model.valid:
                drop_model.destroy()

        for task in self.obj_task:
            if task.valid:
                task.cancel()

        for task in self.detail_obj_task:
            if task.valid:
                task.cancel()

        self.house_pick_obj_map.clear()
        self.house_pick_detail_map.clear()
        self.house_drop_obj_map.clear()
        self.house_pick_data.clear()
        self.obj_task.clear()
        self.detail_obj_task.clear()
        self.house_aabb = None
        self.house_index = None
        self.house_matrix = None
        self._show_pickobj = False
        self._show_detail = False
        self._remove_from_system()
        return

    def destroy(self):
        self._clear()
        super(ComHouseAppearance, self).destroy()

    def _add_to_system(self):
        scene = self.scene
        system = scene.get_com('PartItemAdaptiveLod')
        if system:
            system.add(self)

    def _remove_from_system(self):
        scene = self.scene
        system = scene.get_com('PartItemAdaptiveLod')
        if system:
            system.remove(self)

    def start_drop_timer(self):
        if self.house_drop_timer:
            return
        self.house_drop_timer = global_data.game_mgr.register_logic_timer(self.tick, 1, timedelta=True)

    def stop_drop_timer(self):
        if not self.house_drop_timer:
            return
        else:
            global_data.game_mgr.unregister_logic_timer(self.house_drop_timer)
            self.house_drop_timer = None
            return