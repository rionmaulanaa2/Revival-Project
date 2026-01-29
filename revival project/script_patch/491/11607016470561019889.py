# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_item/ComPickableAppearance.py
from __future__ import absolute_import
import six
import world
import game3d
import math3d
import collision
import weakref
from logic.gcommon.component.UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager
from logic.gutils import item_utils
from common.cfg import confmgr
from logic.gcommon.common_const.collision_const import GROUP_STATIC_SHOOTUNIT, GROUP_CAN_SHOOT, WATER_MASK, TERRAIN_GROUP, WATER_GROUP, GROUP_SHOOTUNIT
from logic.gcommon.common_const.collision_const import HUMAN
from logic.gcommon.item.item_const import FLOAT_HEIGHT, ITEM_DROP_ANIM_MECH, ITEM_DROP_ANIM_BOX, ITEM_NO_ACE_STAR
from logic.gcommon.const import NEOX_UNIT_SCALE
import common.utils.timer as timer
from logic.gcommon import time_utility
from logic.gcommon.common_const.collision_const import GROUP_STATIC_SHOOTUNIT, WATER_GROUP
from logic.gcommon.item.item_const import SCENEBOX_ST_OPENED
from logic.gcommon.item.item_utility import is_deadbox, is_scenebox
import logic.gcommon.common_const.collision_const as collision_const
from logic.gutils.soc_utils import set_model_attach_soc
from logic.gutils import battle_flag_utils
_HASH = game3d.calc_string_hash('Tex0')

class ComPickableAppearance(UnitCom):
    BIND_EVENT = {'E_SHOW_MODEL': '_on_show_model',
       'E_MODEL_LOADED': '_on_model_loaded',
       'E_BEFORE_DESTROY_MODEL': '_on_before_destroy_model',
       'E_SCENE_BOX_STAT_CHANGE': 'on_scene_box_stat_change',
       'G_IS_DEADBOX': 'is_deadbox',
       'G_IS_SCENEBOX': 'is_scenebox',
       'E_REMOVE_CHILD_ITEM': ('_bind_deadbox_sfx', 999),
       'E_PICKABLE_ITEM_COUNT': ('_bind_deadbox_sfx', 999),
       'E_REJOIN_GRID': 'rejoin_grid',
       'G_IS_PVE_ITEM': '_is_pve_item'
       }
    ExtendFuncNames = [
     'get_model_file_config',
     'get_model_col_config']
    LOD_CONFIG = (
     55 * NEOX_UNIT_SCALE, 55 * NEOX_UNIT_SCALE)
    PICK_CONF_PATH = 'item'

    def __init__(self):
        super(ComPickableAppearance, self).__init__()
        self._imp_init()
        self._model = None
        self.ex_privilege_sfx = None
        self.ex_privilege_model = None
        self.ex_privilege_timer = None
        return

    def reuse(self, share_data):
        super(ComPickableAppearance, self).reuse(share_data)
        self._imp_init()

    def cache(self):
        self._imp_destroy()
        super(ComPickableAppearance, self).cache()

    def init_from_dict(self, unit_obj, bdict):
        super(ComPickableAppearance, self).init_from_dict(unit_obj, bdict)
        self.spawn_id = bdict.get('spawn_id')
        self._item_id = bdict.get('item_id', 1)
        x, y, z = bdict.get('position', [0, 0, 0])
        self._item_pos = math3d.vector(x, y, z)
        self._is_package_item = item_utils.is_package_item(self._item_id)
        path = 'box_res' if self._is_package_item else self.PICK_CONF_PATH
        conf = confmgr.get(path, str(self._item_id), default=None)
        if conf is not None:
            self._item_cfg.update(conf)
        self._thrower_id = bdict.get('thrower')
        self._owner_id = bdict.get('owner')
        self._show_sfx = bdict.get('show_sfx', False)
        self.projection_kill = bdict.get('projection_kill', {})
        self._dogtag_visible = True
        self._sfx_deadbox_id = None
        self._dynamic_sfxs = []
        self.is_pve_item = global_data.game_mode.is_pve()
        return

    def destroy(self):
        self._imp_destroy()
        super(ComPickableAppearance, self).destroy()
        self.ex_privilege_timer and global_data.game_mgr.get_logic_timer().unregister(self.ex_privilege_timer)
        self.ex_privilege_timer = None
        return

    def rejoin_grid(self):
        if self._model:
            global_data.emgr.scene_remove_pick_obj_event.emit(self.unit_obj.id)
            global_data.emgr.scene_add_pick_obj_event.emit(self.unit_obj.id, self._model, self.ev_g_pick_data())

    def _on_model_loaded(self, model):
        self._model = model
        self.unit_obj.set_model_attr('world_position', self._item_pos)
        if not self.is_pve_item:
            global_data.emgr.scene_add_pick_obj_event.emit(self.unit_obj.id, model, self.ev_g_pick_data())
        elif not self._show_sfx:
            global_data.emgr.scene_add_pick_obj_event.emit(self.unit_obj.id, model, self.ev_g_pick_data())
        model_scale = 1
        if self._item_cfg and 'model_scale' in self._item_cfg:
            if self._item_cfg['model_scale'] > 0.05:
                model_scale = self._item_cfg['model_scale']
        self._model.scale = math3d.vector(model_scale, model_scale, model_scale)
        col_conf = self.get_model_col_config()
        if col_conf:
            col_size = math3d.vector(col_conf[0] * model_scale, col_conf[1] * model_scale, col_conf[2] * model_scale)
            y_offset = col_conf[3]
            self._col = collision.col_object(collision.BOX, col_size, 0, 0, 0)
            self.scene.scene_col.add_object(self._col)
            self._col.mask = collision_const.GROUP_CHARACTER_INCLUDE | collision_const.GROUP_SKATE_INCLUDE | collision_const.GROUP_STATIC_SHOOTUNIT
            self._col.group = collision_const.GROUP_CHARACTER_INCLUDE | collision_const.GROUP_SKATE_INCLUDE | collision_const.GROUP_STATIC_SHOOTUNIT
            self._col.position = math3d.vector(model.position.x, model.position.y + y_offset, model.position.z)
            self._col.rotation_matrix = model.rotation_matrix
        if self._show_sfx and not is_deadbox(self._item_id):
            self._drop_model_to_pos(model)
        else:
            world.get_active_scene().add_to_group(model, 'pickable_item')
            self.unit_obj.set_model_attr('pickable', True)
            global_data.emgr.scene_add_pickable_model_event.emit(model, (self.unit_obj.id,), self.spawn_id)
            if is_deadbox(self._item_id) and self._show_sfx:
                self.unit_obj.call_model_func('play_animation', 'down')
            else:
                is_open = self.ev_g_scene_box_is_open()
                if self.is_rougebox() or self.is_pve_box():
                    if not is_open:
                        sfxs = self._item_cfg.get('pickable_sfxs', {})
                        for socket_name in sfxs:
                            sfx_path = sfxs[socket_name]
                            self._dynamic_sfxs.append(global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket_name))

                elif is_open:
                    if self._item_id not in (6070, ):
                        self.unit_obj.call_model_func('play_animation', 'open')
                    else:
                        self.unit_obj.call_model_func('play_animation', 'idle')
                elif self._item_id not in (6070, ):
                    self.unit_obj.call_model_func('play_animation', 'idle')
                else:
                    self.unit_obj.call_model_func('play_animation', 'move_f', -1.0, world.TRANSIT_TYPE_DEFAULT, 0, 1)
        if is_deadbox(self._item_id) and self.projection_kill:
            self.ex_privilege_sfx and global_data.sfx_mgr.remove_sfx_by_id(self.ex_privilege_sfx)
            ex_sfx_path = confmgr.get('script_gim_ref')['ex_privilege_projection_sfx']
            new_pos = math3d.vector(self._item_pos.x, self._item_pos.y + 5, self._item_pos.z)
            self.ex_privilege_sfx = global_data.sfx_mgr.create_sfx_in_scene(ex_sfx_path, new_pos)
            self.ex_privilege_model and global_data.model_mgr.remove_model_by_id(self.ex_privilege_model)
            ex_model_path = confmgr.get('script_gim_ref')['ex_privilege_projection_model']

            def _model_load_callback(ex_model):
                projection_id = self.projection_kill.get('projection_kill_no')
                data = confmgr.get('projection_kill_conf', 'ProjectionKillConfig', 'Content', str(projection_id))
                ex_privilege_info = global_data.ui_rt_mgr.create_ui_rt(projection_id, data)
                if not ex_privilege_info:
                    return
                _, tex, panel = ex_privilege_info
                battle_flag_utils.init_projection_kill_template(self.projection_kill, panel)
                ex_model.all_materials.set_texture(_HASH, 'Tex0', tex)
                ex_model.scale = math3d.vector(0.5, 0.5, 0.7)
                model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 10)
                game3d.delay_exec(100, lambda : global_data.ui_rt_mgr.update_ui_rt(projection_id))
                self._play_ex_sfx()

            new_pos = math3d.vector(self._item_pos.x, self._item_pos.y + 10, self._item_pos.z)
            self.ex_privilege_model = global_data.model_mgr.create_model_in_scene(ex_model_path, new_pos, on_create_func=_model_load_callback)
        set_model_attach_soc(model, False)
        self._bind_fx_model()
        self._bind_deadbox_sfx()

    def on_box_return_to_animation(self, model, anim_name, key, anim):
        self.unit_obj.call_model_func('play_animation', anim)

    def _play_ex_sfx(self):

        def on_play_ex_sfx():
            model = global_data.model_mgr.get_model_by_id(self.ex_privilege_model)
            if not (model and model.valid):
                return
            projection_id = self.projection_kill.get('projection_kill_no')
            data = confmgr.get('projection_kill_conf', 'ProjectionKillConfig', 'Content', str(projection_id))
            ex_privilege_info = global_data.ui_rt_mgr.create_ui_rt(projection_id, data)
            if not ex_privilege_info:
                return
            _, tex, _ = ex_privilege_info
            battle_flag_utils.play_projection_kill_sfx(model, tex)

        self.ex_privilege_timer and global_data.game_mgr.get_logic_timer().unregister(self.ex_privilege_timer)
        self.ex_privilege_timer = global_data.game_mgr.get_logic_timer().register(func=on_play_ex_sfx, mode=timer.CLOCK, interval=5)

    def _on_show_model(self, *args):
        unit_model = self.unit_obj.get_model_obj()
        if unit_model and unit_model.valid:
            if not self._item_cfg.get('not_lod'):
                unit_model.lod_config = self.LOD_CONFIG

    def _on_before_destroy_model(self, model):
        if self._fx_model:
            global_data.model_mgr.remove_model(self._fx_model)
            self._fx_model = None
        global_data.emgr.scene_del_pickable_model_event.emit(model, self.spawn_id)
        player = global_data.player
        if player and player.logic:
            pick_succ = player.logic.ev_g_pick_succ()
            if pick_succ and self.unit_obj.id in pick_succ:

                def model_destroy_handler(_model):
                    _model.visible = True
                    cur_posision = _model.world_position
                    _model.remove_from_parent()
                    world.get_active_scene().add_object(_model)
                    _model.world_position = cur_posision
                    item_utils.show_pick_animation(player, _model)

                self.unit_obj.set_model_destroy_handler(model_destroy_handler)
        return

    def on_scene_box_stat_change(self, status):
        if status == SCENEBOX_ST_OPENED:
            is_rb = self.is_rougebox() or self.is_pve_box()
            if not is_rb:
                if self._item_id not in (6070, ):
                    self.unit_obj.call_model_func('play_animation', 'open')
                else:
                    self.unit_obj.call_model_func('play_animation', 'open')
                    self.unit_obj.call_model_func('register_anim_key_event', 'open', 'end', self.on_box_return_to_animation, 'idle')
            unit_model = self.unit_obj.get_model_obj()
            if unit_model and unit_model.valid:
                if is_rb:
                    all_sockets_obj = unit_model.get_all_objects_on_sockets()
                    for one_sfx in all_sockets_obj:
                        one_sfx.visible = False

                unit_id = self.unit_obj.id
                unit_model_ref = weakref.ref(unit_model)
                data = self.ev_g_pick_data()
                global_data.emgr.scene_open_box_event.emit(unit_id, unit_model_ref, data)

    def is_deadbox(self):
        return is_deadbox(self._item_id)

    def is_scenebox(self):
        return is_scenebox(self._item_id)

    def is_rougebox(self):
        from logic.gutils.item_utils import is_rouge_box
        return is_rouge_box(self._item_id)

    def is_pve_box(self):
        from logic.gutils.item_utils import is_pve_box
        return is_pve_box(self._item_id)

    def _is_pve_item(self):
        return self.is_pve_item

    def get_model_file_config(self):
        res_path = self._item_cfg.get('res', '')
        from logic.gutils.mode_utils import get_mapped_res_path
        return (
         get_mapped_res_path(res_path), [])

    def get_model_col_config(self):
        return self._item_cfg.get('col_info', None)

    def refresh_dogtab_visible(self):
        if not global_data.cam_lplayer or not self._fx_model or not item_utils.is_dogtag_by_item_id(self._item_id):
            return
        pickable_item_data = self.ev_g_pick_data()
        faction_id = pickable_item_data.get('faction_id', -1)
        self._dogtag_visible = faction_id < 0 or global_data.cam_lplayer.ev_g_is_campmate(faction_id)
        self._fx_model.visible = self._dogtag_visible

    def _imp_init(self):
        self._item_id = None
        self._item_pos = math3d.vector(0, 0, 0)
        self._item_cfg = {}
        self._is_package_item = False
        self._fx_model = None
        self._drop_model = None
        self._thrower_id = None
        self._owner_id = None
        self._intrp_timer = None
        self._col = None
        return

    def _imp_destroy(self):
        if self._intrp_timer:
            global_data.game_mgr.unregister_logic_timer(self._intrp_timer)
            self._intrp_timer = None
        if self._drop_model:
            global_data.model_mgr.remove_model(self._drop_model)
            self._drop_model = None
        self.clear_sfx_deadbox()
        global_data.emgr.scene_remove_pick_obj_event.emit(self.unit_obj.id)
        self._col and self.scene.scene_col.remove_object(self._col)
        self._col = None
        for sfx_id in self._dynamic_sfxs:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        del self._dynamic_sfxs[:]
        self.ex_privilege_sfx and global_data.sfx_mgr.remove_sfx_by_id(self.ex_privilege_sfx)
        self.ex_privilege_sfx = None
        self.ex_privilege_model and global_data.model_mgr.remove_model_by_id(self.ex_privilege_model)
        self.ex_privilege_model = None
        return

    def clear_sfx_deadbox(self):
        if self._sfx_deadbox_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._sfx_deadbox_id)
        self._sfx_deadbox_id = None
        return

    def _bind_fx_model(self):
        model_path = self._item_cfg.get('fx_res', None)
        if not model_path:
            conf = confmgr.get(self.PICK_CONF_PATH, str(self._item_id), default={})
            model_path = conf.get('fx_res', None)
        if not model_path:
            return
        else:

            def create_cb(model, use_idx):
                if not self.is_enable(use_idx) or not self.unit_obj.is_model_valid():
                    global_data.model_mgr.remove_model(model)
                    return
                self._fx_model = model
                model.set_parent(self.unit_obj.get_model_obj())
                set_model_attach_soc(model, False)
                self.refresh_dogtab_visible()
                model.render_level = 7

            func = lambda model, use_idx=self.use_idx: create_cb(model, use_idx)
            global_data.model_mgr.create_model(model_path, on_create_func=func)
            return

    def _bind_deadbox_sfx(self, *args):
        unit_model = self.unit_obj.get_model_obj()
        if not unit_model:
            return
        if not is_deadbox(self._item_id):
            return
        self.clear_sfx_deadbox()
        pickable_item_data = self.ev_g_pick_data()
        all_item = pickable_item_data.get('all_item', {})
        if not all_item:
            return
        max_quality = 0
        for _entity_id, _item_data in six.iteritems(all_item):
            if not _item_data:
                continue
            item_id = _item_data['item_id']
            if item_id == ITEM_NO_ACE_STAR:
                continue
            iQuality = item_utils.get_deadbox_quality(item_id)
            max_quality = max(max_quality, iQuality)

        if self.ev_g_scene_box_is_open():
            state = 'open' if 1 else 'idle'
            sfx_path = item_utils.get_deadbox_quality_sfx(max_quality, state)
            return sfx_path or None
        self._sfx_deadbox_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, unit_model, 'fx_root')

    def _drop_model_to_pos(self, model):
        self.unit_obj.set_model_attr('visible', False)
        drop_model_path = 'model_new/items/empty/empty.gim'
        func = lambda model, use_idx=self.use_idx: self._on_create_drop_model(model, use_idx)
        global_data.model_mgr.create_model(drop_model_path, on_create_func=func)

    def _on_create_drop_model(self, model, use_idx):
        if not self.is_enable(use_idx):
            global_data.model_mgr.remove_model(model)
            return
        else:
            if not self.unit_obj.is_model_valid():
                global_data.model_mgr.remove_model(model)
                return
            world.get_active_scene().add_object(model)
            src_pos = dst_pos = self._item_pos
            thrower_ent = EntityManager.getentity(self._thrower_id)
            if thrower_ent and thrower_ent.logic:
                src_pos = thrower_ent.logic.ev_g_position()
                if src_pos is None:
                    src_pos = self._item_pos
            self.unit_obj.set_model_attr('world_position', src_pos)
            self.unit_obj.set_model_attr('visible', True)
            model.world_position = src_pos
            unit_model = self.unit_obj.get_model_obj()
            intrp_time = time_utility.get_server_time()
            intrp_thresh = 1.0 if self.is_pve_item else 0.7

            def intrp_cb(*args):
                delta = time_utility.get_server_time() - intrp_time
                u = min(delta / intrp_thresh, 1)
                intrp_pos = math3d.vector(0, 0, 0)
                intrp_pos.intrp(src_pos, dst_pos, u)
                model.position = intrp_pos
                pos = intrp_pos + model.get_bone_prs(0)[0]
                if self.is_pve_item:
                    fix_height = math3d.vector(0, -800 * (u - 0.5) ** 2 + 200, 0)
                    pos += fix_height
                if G_POS_CHANGE_MGR:
                    self.notify_pos_change(pos + math3d.vector(0, -8, 0))
                else:
                    self.send_event('E_POSITION', pos + math3d.vector(0, -8, 0))
                if u == 1:
                    global_data.model_mgr.remove_model(model)
                    if unit_model and unit_model.valid:
                        world.get_active_scene().add_to_group(unit_model, 'pickable_item')
                        self.unit_obj.set_model_attr('pickable', True)
                        if self.is_pve_item:
                            global_data.emgr.scene_add_pick_obj_event.emit(self.unit_obj.id, self._model, self.ev_g_pick_data())
                        global_data.emgr.scene_add_pickable_model_event.emit(unit_model, (self.unit_obj.id,), self.spawn_id)
                    self._intrp_timer = None
                    return timer.RELEASE
                else:
                    return

            self._intrp_timer = global_data.game_mgr.register_logic_timer(intrp_cb, 1)
            anim_name = 'battery_drop' if self._show_sfx == ITEM_DROP_ANIM_MECH else 'item_drop'
            model.play_animation(anim_name)
            return