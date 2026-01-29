# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/battleprepare/BestRoleModelAppearance.py
from __future__ import absolute_import
import game3d
import world
from common.algorithm import resloader
from logic.gutils import dress_utils
from logic.gutils.role_skin_utils import load_improved_skin_model_and_effect, load_normal_skin_model_and_effect, clear_role_skin_model_and_effect
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_OTHER_PENDANT_LIST, FASHION_POS_WEAPON_SFX
import math3d
from common.utils import pc_platform_utils
from common.cfg import confmgr
import render
from common.utilities import get_utf8_length
import collision
from logic.gcommon.common_const.collision_const import MASK_CHARACTER_ROBOT, GROUP_CHARACTER_ROBOT
from logic.manager_agents.manager_decorators import sync_exec
import cc
from common.utils.timer import CLOCK, RELEASE
import random
import weakref
import six
_HASH = game3d.calc_string_hash('Tex0')

class BaseBestModelAppearance(object):
    INIT_EVENT = {}

    def __init__(self, index, obj_id, name, chushegntai_model):
        self._index = index
        self.obj_id = obj_id
        self._show_name = name
        self.space_node = None
        self.model = None
        self.improved_skin_sfx_id = None
        self.sub_model_list = []
        self.skin_sfx_list = []
        self.skin_timer_list = []
        self.model_id = None
        self.model_col = None
        self.panel = None
        self.tex = None
        self.rt = None
        self._chushegntai_model = chushegntai_model
        self.init_name()
        self._is_event_binded = False
        self._bind_event()
        return

    def _bind_event(self):
        if not self._is_event_binded:
            einfo = {}
            for event_name, func_name in six.iteritems(self.INIT_EVENT):
                einfo[event_name] = getattr(self, func_name)

            global_data.emgr.bind_events(einfo)
            self._is_event_binded = True

    def _unbind_event(self):
        if self._is_event_binded:
            einfo = {}
            for event_name, func_name in six.iteritems(self.INIT_EVENT):
                einfo[event_name] = getattr(self, func_name)

            global_data.emgr.unbind_events(einfo)
            self._is_event_binded = False

    def _get_model(self):
        if self.model and self.model.valid:
            return self.model
        else:
            return None

    def init_name(self):
        resource_path = 'battle_before/hot_ranking_name'
        self.panel = global_data.uisystem.load_template_create(resource_path)
        self.panel.retain()
        size = self.panel.getContentSize()
        scale = 1.0
        render_texture_size = (size.width * scale, size.height * scale)
        self.panel.setAnchorPoint(cc.Vec2(0, 0))
        if game3d.get_render_device() not in (game3d.DEVICE_GLES, game3d.DEVICE_GL):
            self.panel.setScale(scale)
            self.panel.SetPosition(0, 0)
        else:
            self.panel.setScaleX(scale)
            self.panel.setScaleY(-scale)
            self.panel.SetPosition(0, size.height * scale)
        self.tex = render.texture.create_empty(int(render_texture_size[0]), int(render_texture_size[1]), render.PIXEL_FMT_A8R8G8B8, True)
        self.rt = cc.RenderTexture.createWithITexture(self.tex)
        self.rt.retain()

    def add_model_col(self, model):
        col = collision.col_object(collision.CAPSULE, model.bounding_box)
        col.mask = MASK_CHARACTER_ROBOT
        col.group = GROUP_CHARACTER_ROBOT
        scn = world.get_active_scene()
        scn.scene_col.add_object(col)
        self.model_col = col

    def update_pos(self, index=None):
        if index is not None:
            if self._index == index:
                return
            self._index = index
        if not self.tex:
            return
        else:
            mingpai_model = self._chushegntai_model.get_socket_obj('mingpai_0' + str(self._index + 1), 0)
            mingpai_model.get_sub_material('chushengtai_mingpai_02').set_texture(_HASH, 'Tex0', self.tex)
            mingpai_model.enable_instancing(False)
            self.panel.lab_name.setString(self._show_name)
            self._draw_ui_to_rt(self.rt, self.panel)
            world_matrix = self._chushegntai_model.get_socket_matrix(self._index, world.SPACE_TYPE_WORLD)
            if self.model:
                self.model.world_position = world_matrix.translation
                self.model.world_rotation_matrix = world_matrix.rotation
                if self.model_col:
                    pos = self.model.world_position
                    self.model_col.position = math3d.vector(pos.x, pos.y + self.model.bounding_box.y, pos.z)
            return

    @sync_exec
    def _draw_ui_to_rt(self, rt, panel):
        if not panel or not panel.isValid():
            return
        rt.beginWithClear(0, 0, 0, 0)
        if hasattr(rt, 'addCommandsForNode'):
            rt.addCommandsForNode(panel.get())
        else:
            panel.visit()
        rt.end()

    def destroy_model(self):
        clear_role_skin_model_and_effect(self.model, clear_trigger_interval=True, improved_skin_id=self.improved_skin_sfx_id)
        if self.model_id:
            global_data.model_mgr.remove_model_by_id(self.model_id)
            self.model_id = None
        self.model = None
        return

    def destroy(self):
        self.destroy_model()
        if self.model_col:
            scn = world.get_active_scene()
            scn.scene_col.remove_object(self.model_col)
        if self.rt:
            self.rt.release()
        self.rt = None
        self.tex = None
        if self.panel:
            self.panel.release()
            self.panel = None
        self._unbind_event()
        return


class BestRoleModelAppearance(BaseBestModelAppearance):

    def __init__(self, index, chushegntai_model, force_info_list=None):
        role_info_list = force_info_list or global_data.battle.get_top_nb_role_info() if 1 else force_info_list
        role_info = role_info_list[index]
        fashion_data = role_info[3]
        self._role_id = role_info[1]
        self._role_kwargs = {}
        role_name = role_info[2]
        obj_id = role_info[0]
        if len(role_info) > 4:
            self._role_kwargs = role_info[4]
        self.head_pendant_random_anim_timer = None
        self.head_pendant_anim_index = 0
        self.head_pendant_model = None
        self.improved_skin_sfx_id = None
        self.sub_model_list = []
        self.skin_sfx_list = []
        self.skin_timer_list = []
        self.ready_for_improved_skin_flag = 0
        self.can_load_improved_skin_res = False
        super(BestRoleModelAppearance, self).__init__(index, obj_id, role_name, chushegntai_model)
        self.load_model(self._role_id, fashion_data)
        return

    def _check_load_improved_skin_model_and_effect(self, model):
        if not self.can_load_improved_skin_res:
            return
        if self.ready_for_improved_skin_flag != 0:
            return
        load_improved_skin_model_and_effect(model, self.improved_skin_sfx_id, auto_load_trigger_at_intervals_res=True, lod_level='l')

    def modify_ready_for_improved_skin_flag(self, model, offset):
        if self.improved_skin_sfx_id is None:
            return
        else:
            self.ready_for_improved_skin_flag += offset
            self._check_load_improved_skin_model_and_effect(model)
            return

    def load_model(self, role_id, fashion_data):
        self.dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
        self.improved_skin_sfx_id = fashion_data.get(FASHION_POS_WEAPON_SFX)
        path = dress_utils.get_role_model_path_by_lod(role_id, self.dressed_clothing_id, lod_level='l')
        if not path:
            return
        res_path = path.replace('l.gim', 'empty.gim')
        mesh_path_list = [path]
        self.suit_id = fashion_data.get(FASHION_POS_SUIT_2)
        self.head_id = fashion_data.get(FASHION_POS_HEADWEAR)
        self.bag_id = fashion_data.get(FASHION_POS_BACK)
        self.other_pendant_list = sorted([ fashion_data.get(p) for p in FASHION_OTHER_PENDANT_LIST if fashion_data.get(p) ])
        self.head_id, self.bag_id, self.suit_id, self.other_pendant_list = dress_utils.get_real_dec_dict_with_check_completion_and_replacement(self.dressed_clothing_id, self.head_id, self.bag_id, self.suit_id, self.other_pendant_list, self.improved_skin_sfx_id)
        self.head_pendant_type, self.head_res_path, self.pendant_socket_name, self.pendant_socket_res_path, self.head_pendant_l_same_gis, self.pendant_random_anim_list, self.bag_socket_name, self.bag_model_path, self.bag_socket_name2, self.bag_model_path2, self.bag_pendant_l_same_gis, self.pendant_data_list = dress_utils.get_pendant_res_lod_conf('l', res_path, self.dressed_clothing_id, self.head_id, self.bag_id, self.suit_id, self.other_pendant_list)
        mesh_path_list.append(self.head_res_path)
        if self.head_pendant_l_same_gis:
            mesh_path_list.append(self.pendant_socket_res_path)
        if self.bag_model_path:
            if self.bag_pendant_l_same_gis or not self.bag_socket_name:
                mesh_path_list.append(self.bag_model_path)
        if self.bag_model_path2:
            if self.bag_pendant_l_same_gis or not self.bag_socket_name2:
                mesh_path_list.append(self.bag_model_path2)
        if self.other_pendant_list and self.pendant_data_list:
            for pendant_data in self.pendant_data_list:
                if pendant_data.get('head_pendant_l_same_gis'):
                    mesh_path_list.append(pendant_data.get('res_path'))
                elif pendant_data.get('res_path') and not pendant_data.get('socket_name'):
                    mesh_path_list.append(pendant_data.get('res_path'))

        self.model_id = global_data.model_mgr.create_model_in_scene(res_path, mesh_path_list=mesh_path_list, on_create_func=self.on_load_model_complete)

    def on_load_model_complete(self, model, *args):
        if not model or not model.valid:
            return
        else:
            if not self._chushegntai_model or not self._chushegntai_model.valid:
                self.destroy_model()
                return
            if not self.improved_skin_sfx_id:
                load_normal_skin_model_and_effect(model, self.dressed_clothing_id, 'l')
            self.model = model
            force_scale = self._role_kwargs.get('scale')
            scale = confmgr.get('role_info', 'RoleInfo', 'Content', str(self._role_id), 'lobby_model_scale')
            scale = scale or 1
            scale = scale * 1.6 if force_scale is None else force_scale
            model.scale = math3d.vector(scale, scale, scale)
            if model:
                model.cast_shadow = True
                model.receive_shadow = True
            self.ready_for_improved_skin_flag = 0
            self.can_load_improved_skin_res = False
            self.load_socket_bag(self.bag_model_path, self.bag_socket_name, model)
            self.load_socket_bag(self.bag_model_path2, self.bag_socket_name2, model)
            if self.pendant_socket_res_path:
                if self.pendant_socket_res_path.endswith('.sfx'):
                    global_data.sfx_mgr.create_sfx_on_model(self.pendant_socket_res_path, model, self.pendant_socket_name)
                else:
                    self.load_head_socket_model(model)
            if any(self.other_pendant_list) and self.pendant_data_list:
                self.load_other_pendant(self.pendant_data_list, model)
            if pc_platform_utils.is_pc_hight_quality():
                pc_platform_utils.set_multi_pass_outline(model)
            self.can_load_improved_skin_res = True
            self._check_load_improved_skin_model_and_effect(model)
            if global_data.is_ue_model:
                model.mirror_reflect = global_data.game_mgr.gds.get_actual_quality() > 1
                if global_data.player:
                    pc_platform_utils.set_model_write_alpha(model, not global_data.player.is_in_battle(), 1.0)
            model.all_materials.set_macro('RIM_LIGHT_ENABLE', 'TRUE')
            model.all_materials.rebuild_tech()
            hair_model = model.get_socket_obj('gj_hair', 0)
            if hair_model and hair_model.has_anim('s_emptyhand_idle'):
                hair_model.play_animation('s_emptyhand_idle', -1.0, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_LOOP)
            model.play_animation('s_emptyhand_idle', -1.0, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_LOOP)
            self.add_model_col(model)
            self.update_pos()
            return

    def load_socket_bag(self, res_path, socket_name, model):
        if self.bag_pendant_l_same_gis:
            return
        if res_path and socket_name:
            self.modify_ready_for_improved_skin_flag(model, 1)
            socket_model_name = 'socket_model_%s' % socket_name
            resloader.load_res_attr(self, socket_model_name, res_path, self.on_load_bag_pendant_model_complete, socket_name, res_type='MODEL', priority=game3d.ASYNC_HIGH)

    def on_load_bag_pendant_model_complete(self, load_model, data, *args):
        if not load_model.valid:
            load_model.destroy()
            return
        model = self._get_model()
        if not model:
            return
        socket_name = data
        model.bind(socket_name, load_model, world.BIND_TYPE_ALL)
        self.modify_ready_for_improved_skin_flag(model, -1)

    def load_head_socket_model(self, model):
        if self.head_pendant_l_same_gis:
            return
        socket_model_name = 'socket_model_%s' % self.pendant_socket_name
        self.modify_ready_for_improved_skin_flag(model, 1)
        resloader.load_res_attr(self, socket_model_name, self.pendant_socket_res_path, self.on_load_head_pendant_model_complete, self.pendant_socket_name, res_type='MODEL', priority=game3d.ASYNC_HIGH)

    def _play_head_pendant_model_anim(self):
        if not self.pendant_random_anim_list:
            self.head_pendant_random_anim_timer = None
            return RELEASE
        else:
            if not self.head_pendant_model:
                self.head_pendant_random_anim_timer = None
                return RELEASE
            head_pendant_model = self.head_pendant_model()
            if not head_pendant_model or not head_pendant_model.valid:
                self.head_pendant_random_anim_timer = None
                return RELEASE
            anim_name, min_duration, max_duration = self.pendant_random_anim_list[self.head_pendant_anim_index * 3:self.head_pendant_anim_index * 3 + 3]
            self.head_pendant_anim_index = (self.head_pendant_anim_index + 1) % 2
            duration = random.uniform(min_duration, max_duration)
            head_pendant_model.play_animation(anim_name)
            self.head_pendant_random_anim_timer = global_data.game_mgr.register_logic_timer(self._play_head_pendant_model_anim, interval=duration, times=1, mode=CLOCK)
            return

    def on_load_head_pendant_model_complete(self, load_model, data, *args):
        if not load_model.valid:
            load_model.destroy()
            return
        model = self._get_model()
        if not model:
            return
        pendant_socket_name = data
        model.bind(pendant_socket_name, load_model, world.BIND_TYPE_ALL)
        self.modify_ready_for_improved_skin_flag(model, -1)
        self.head_pendant_model = weakref.ref(load_model)
        self.head_pendant_anim_index = 0
        self._play_head_pendant_model_anim()

    def load_other_pendant(self, other_pendant_list, model):
        for pendant_data in other_pendant_list:
            if pendant_data.get('head_pendant_l_same_gis'):
                continue
            res_path = pendant_data.get('res_path')
            socket_name = pendant_data.get('socket_name')
            if socket_name:
                self.load_other_pendant_model(res_path, socket_name, model)

    def load_other_pendant_model(self, res_path=None, socket_name=None, model=None):
        if res_path and socket_name:
            self.modify_ready_for_improved_skin_flag(model, 1)
            socket_model_name = 'socket_model_%s_%s' % (socket_name, res_path)
            resloader.load_res_attr(self, socket_model_name, res_path, self.on_load_other_pendant_model_complete, socket_name, res_type='MODEL', priority=game3d.ASYNC_HIGH)

    def on_load_other_pendant_model_complete(self, load_model, data, *args):
        if not load_model.valid:
            load_model.destroy()
            return
        model = self._get_model()
        if not model:
            return
        socket_name = data
        model.bind(socket_name, load_model, world.BIND_TYPE_ALL)
        self.modify_ready_for_improved_skin_flag(model, -1)

    def destroy(self):
        super(BestRoleModelAppearance, self).destroy()
        self.head_pendant_model = None
        if self.head_pendant_random_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.head_pendant_random_anim_timer)
            self.head_pendant_random_anim_timer = None
        return


class BestRoleModelAppearanceConcert(BestRoleModelAppearance):

    def on_load_model_complete(self, model, *args):
        super(BestRoleModelAppearanceConcert, self).on_load_model_complete(model, *args)
        if not model or not model.valid:
            return
        sockets = ['hair', 'hair_99']
        for s in sockets:
            m = model.get_socket_obj(s, 0)
            if m:
                m.visible = True