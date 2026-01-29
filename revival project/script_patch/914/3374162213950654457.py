# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartArtCheckModelDisplay.py
from __future__ import absolute_import
import six
from six.moves import range
import game3d
import world
import math
from . import ScenePart
import copy
import math3d
from logic.vscene.parts.camera.CameraTrkPlayer import CameraTrkPlayer
from common.algorithm import resloader
from common.utils import pc_platform_utils
from logic.gutils.CameraHelper import get_left_hand_trans
from logic.gutils.dress_utils import get_file_name, clear_spring_anim, init_spring_anim
from common.cfg import confmgr
_HASH_light_info = game3d.calc_string_hash('light_info')
_HASH_outline_alpha = game3d.calc_string_hash('outline_alpha')

def set_model_alpha(model):
    pc_platform_utils.set_display_model_alpha(model, False)


def enable_outline(model):
    pc_platform_utils.set_multi_pass_outline(model, True)


def disable_outline(model):
    pc_platform_utils.disable_multi_pass_outline(model)


def check_add_mesh_valid(org_model, add_model):
    if not org_model or not add_model:
        return False
    return org_model.get_bone_count() == add_model.get_bone_count()


class CArtCheckModel(object):

    def __init__(self, parent, dict_data=None, **kargs):
        self.parent = parent
        self.model_data = dict_data
        self.init_parameters()
        self.process_event(True)
        self.on_change_display_model(self.model_data)

    def init_parameters(self):
        self.conf_hdr = 'zhanshi_human'
        self.conf_light = 'zhanshi'
        self.model_id = None
        self.model_path = None
        self.head_path = None
        self.model = None
        self.shadow_model = None
        self.shadow_model_path = None
        self.camera_trk_path = None
        self.trk_player = None
        self.box_name = 'box_shangcheng_01'
        self.euler_rot_mtx = None
        self.cur_euler_rot = None
        self.target_euler_rot = None
        self.is_same_gis = False
        self.show_anim_name = None
        self.end_anim_name = 'stand_idle'
        self.cur_euler_rot = math3d.vector(0, 0, 0)
        self.target_euler_rot = math3d.vector(0, 0, 0)
        self.socket_model_names = []
        self.socket_to_model_path = {}
        self.pendant_add_mesh_list = []
        self.idx_to_sfx_dict = {}
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'rotate_model_display': self.rotate_model
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_change_display_model(self, dict_data=None):
        if not dict_data:
            return
        else:
            self.model_path = dict_data.get('m_path')
            if not self.model_path:
                return
            scene = global_data.game_mgr.scene
            if scene.is_hdr_enable:
                scene.set_bloom_c_env(self.conf_hdr)
                scene.setup_env_light_info(self.conf_light, 'on_ground')
            self.is_same_gis = self.model_data.get('is_same_gis', False)
            self.shadow_model_path = self.model_path
            self.head_path = self.model_path.replace('h.gim', 'parts/h_head.gim')
            self.show_anim_name = self.model_data.get('show_anim', None)
            self.create_model()
            return

    def create_model(self):
        self.model_id = global_data.model_mgr.create_model(self.model_path, mesh_path_list=[], on_create_func=self.on_load_model_complete)

    def rotate_model(self, rotate_times):
        self.target_euler_rot = math3d.vector(0, self.target_euler_rot.y + rotate_times * math.pi * 2, 0)

    def load_head_model(self):
        if self.is_same_gis:
            self.model.add_mesh(self.head_path)
        else:
            socket_name = 'head'
            socket_model_name = 'socket_model_%s' % socket_name
            self.socket_model_names.append(socket_model_name)
            self.socket_to_model_path[socket_name] = self.head_path
            resloader.load_res_attr(self, socket_model_name, self.head_path, self.on_load_socket_model_complete, (
             socket_model_name, socket_name, None), res_type='MODEL', priority=game3d.ASYNC_HIGH)
        return

    def on_load_socket_model_complete(self, load_model, data, *args):
        if not load_model.valid:
            load_model.destroy()
            return
        model = self.get_model()
        if not model:
            return
        socket_model_name, socket_name, pendant_data = data
        if pendant_data:
            bind_cb = pendant_data.get('bind_cb')
            if bind_cb:
                pendant_data['model'] = load_model
                bind_cb(pendant_data)
        setattr(self, socket_model_name, load_model)
        model.bind(socket_name, load_model, world.BIND_TYPE_ALL)
        set_model_alpha(load_model)
        enable_outline(load_model)
        self.play_show_anim()
        self.init_spring_anim()

    def on_load_model_complete(self, model, *args):
        if not self.parent:
            return
        else:
            self.model = model
            self.model.visible = True
            scn = self.parent.scene()
            if not scn:
                return
            scn.add_object(self.model)
            self.model.all_materials.set_macro('TOP_LIGHT_ENABLE', 'TRUE')
            self.model.all_materials.set_macro('BACK_LIGHT_ENABLE', 'TRUE')
            self.model.all_materials.rebuild_tech()
            self.model.world_position = math3d.vector(0, 0, 0)
            self.euler_rot_mtx = math3d.euler_to_matrix(math3d.vector(0, 0, 0))
            self.model.rotation_matrix = self.euler_rot_mtx
            self.load_head_model()
            self.add_panel_shadow()
            enable_outline(self.model)
            set_model_alpha(self.model)
            callback = self.model_data.get('callback', None)
            if callback:
                callback(model, *args)
            self.change_display_camera()
            return

    def add_pendant_by_add_mesh(self, pendant_data):
        if not self.get_model():
            return
        else:
            pendant_path = pendant_data.get('pendant_path')
            pendant_model = world.model(pendant_path, None)
            add_mesh_callback = pendant_data.get('add_cb')
            state = False
            if check_add_mesh_valid(self.get_model(), pendant_model):
                self.model.remove_mesh(pendant_path)
                self.model.add_mesh(pendant_path)
                self.pendant_add_mesh_list.append(pendant_path)
                if add_mesh_callback:
                    add_mesh_callback(pendant_data)
            elif add_mesh_callback:
                add_mesh_callback(None)
            return

    def add_pendant_by_bind(self, pendant_data):
        if not self.get_model():
            return
        else:
            pendant_path = pendant_data.get('pendant_path')
            socket_name = pendant_data.get('socket_name')
            bind_cb = pendant_data.get('bind_cb')
            idx = pendant_data.get('idx')
            socket_model_name = 'socket_model_%s' % idx
            socket_model = getattr(self, socket_model_name, None)
            if socket_model:
                self.model.unbind(socket_model)
                setattr(self, socket_model_name, None)
                socket_model.destroy()
            self.socket_model_names.append(socket_model_name)
            self.socket_to_model_path[socket_model_name] = (socket_name, pendant_path)
            resloader.load_res_attr(self, socket_model_name, pendant_path, self.on_load_socket_model_complete, (
             socket_model_name, socket_name, pendant_data), res_type='MODEL', priority=game3d.ASYNC_HIGH)
            return

    def delete_pendant_from_add_mesh(self, pendant_data):
        if not self.get_model():
            return
        pendant_path = pendant_data.get('pendant_path')
        self.model.remove_mesh(pendant_path)
        self.pendant_add_mesh_list.remove(pendant_path)

    def delete_pendant_from_bind(self, pendant_data):
        if not self.get_model():
            return
        else:
            idx = pendant_data.get('idx')
            socket_model_name = 'socket_model_%s' % idx
            socket_model = getattr(self, socket_model_name, None)
            if socket_model:
                self.model.unbind(socket_model)
                socket_model.destroy()
                self.socket_to_model_path[socket_model_name] = None
                setattr(self, socket_model_name, None)
            return

    def enable_model_outline(self):
        if not self.get_model():
            return
        else:
            enable_outline(self.model)
            for socket_model_name, _ in six.iteritems(self.socket_to_model_path):
                socket_model = getattr(self, socket_model_name, None)
                if not socket_model:
                    continue
                enable_outline(socket_model)

            return

    def disable_model_outline(self):
        if not self.get_model():
            return
        else:
            disable_outline(self.model)
            for socket_model_name, _ in six.iteritems(self.socket_to_model_path):
                socket_model = getattr(self, socket_model_name, None)
                if not socket_model:
                    continue
                disable_outline(socket_model)

            return

    def add_panel_shadow(self):
        scn = self.parent.scene()
        light = scn.get_light('dir_light')
        if not light:
            return
        else:
            self.shadow_model = world.model(self.shadow_model_path, None)
            self.shadow_model.set_parent(self.model)
            self.shadow_model.position = math3d.vector(0, 0, 0)
            height = self.model.world_position.y
            if self.is_same_gis:
                self.shadow_model.add_mesh(self.head_path)
            else:
                head_model = world.model(self.head_path, None)
                self.shadow_model.bind('head', head_model)
                self.set_panel_shadow(head_model, light.direction, height)
            for i in range(self.shadow_model.get_socket_count()):
                socket_objects = self.shadow_model.get_socket_objects(i)
                for obj in socket_objects:
                    if str(obj.filename).endswith('.gim'):
                        self.set_panel_shadow(obj, light.direction, height)
                    else:
                        obj.visible = False

            self.shadow_model.all_materials.set_technique(1, 'shader/plane_shadow.nfx::TShader')
            self.shadow_model.all_materials.set_var(_HASH_light_info, 'light_info', (light.direction.x, light.direction.y, light.direction.z, height))
            self.shadow_model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 10)
            self.shadow_model.set_inherit_parent_shaderctrl(False)
            return

    def set_panel_shadow(self, model, direction, height):
        model.all_materials.set_technique(1, 'shader/plane_shadow.nfx::TShader')
        model.all_materials.set_var(_HASH_light_info, 'light_info', (direction.x, direction.y, direction.z, height))
        model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 10)
        model.set_inherit_parent_shaderctrl(False)

    def get_model(self):
        if self.model and self.model.valid:
            return self.model
        else:
            return None

    def on_update(self, dt):
        model = self.get_model()
        if not model:
            return
        self.cur_euler_rot.intrp(self.cur_euler_rot, self.target_euler_rot, 0.2)
        self.model.rotation_matrix = self.euler_rot_mtx * math3d.euler_to_matrix(self.cur_euler_rot)

    def play_show_anim(self):
        model = self.get_model()
        if not model:
            return
        anim = self.show_anim_name
        if not model.has_anim(anim):
            anim = 'stand_idle'
            if not model.has_anim('stand_idle'):
                return
        if self.camera_trk_path:
            trk = global_data.track_cache.create_track(self.camera_trk_path)
            scn = global_data.game_mgr.scene
            camera = scn.active_camera
            scn.set_vegetation_visible_range(100000)
            if trk.has_fov_info():
                camera.fov = trk.get_fov(0)
            transform = get_left_hand_trans(trk.get_transform(0))
            camera.world_rotation_matrix = transform.rotation
            camera.world_position = transform.translation
            global_data.emgr.play_camera_trk_event.emit(self.camera_trk_path, left_hand_coordinate=False)
        self.play_animation(anim)
        model.unregister_event(self.end_show_anim, 'end', anim)
        model.register_anim_key_event(anim, 'end', self.end_show_anim)

    def end_show_anim(self, *args):
        model = self.get_model()
        if not model:
            return
        self.parent.scene().active_camera.fov = 30
        self.play_animation(self.end_anim_name, 300, world.TRANSIT_TYPE_DELAY, 0, True)

    def change_display_camera(self):
        model = self.get_model()
        if not model:
            return
        path = model.get_file_path().split('\\')
        if len(path) < 3:
            return
        role_id = path[-3]
        data = confmgr.get('lobby_model_display_conf', 'RoleDisplayCam', 'Content', default={})
        if role_id and role_id in data:
            camera_info = data[role_id]
            global_data.emgr.change_artcheck_display_camera_state.emit([camera_info['near_cam'], camera_info['far_cam'], camera_info['near_mid_cam']])

    def init_spring_anim(self):
        self.clear_spring_anim()
        model = self.get_model()
        file_name = get_file_name(model)
        if not file_name:
            return
        data_file = file_name + '_h'
        data = confmgr.get(data_file)
        conf = data._conf
        if not conf:
            return
        scale = model.scale.x
        if abs(scale - 1) > 0.1:
            return
        init_spring_anim(model, conf)

    def clear_spring_anim(self):
        model = self.get_model()
        file_name = get_file_name(model)
        if not file_name:
            return
        data_file = file_name + '_h'
        data = confmgr.get(data_file)
        conf = data._conf
        if not conf:
            return
        clear_spring_anim(model, conf)

    def play_animation(self, *args):
        self.model.play_animation(*args)
        if self.shadow_model:
            self.shadow_model.play_animation(*args)
        for socket_model_name in self.socket_model_names:
            socket_model = getattr(self, socket_model_name, None)
            if socket_model:
                socket_model.play_animation(*args)

        return

    def change_anim(self, anim_data):
        show_anim = anim_data.get('show_anim')
        end_anim = anim_data.get('end_anim')
        play_camera_trk = anim_data.get('play_camera_trk')
        camera_trk_path = anim_data.get('camera_trk_path')
        if play_camera_trk and camera_trk_path:
            self.camera_trk_path = camera_trk_path
        else:
            self.camera_trk_path = None
        self.show_anim_name = show_anim
        self.end_anim_name = end_anim
        self.play_show_anim()
        return

    def clear_model(self):
        if self.model and self.model.valid:
            self.model.destroy()
        if self.model_id:
            global_data.model_mgr.remove_model_by_id(self.model_id)
        if self.shadow_model and self.shadow_model.valid:
            self.shadow_model.destroy()
            self.shadow_model = None
        self.model_id = None
        self.model = None
        self.clear_spring_anim()
        return

    def on_add_sfx(self, sfx_data):
        if not self.get_model():
            global_data.game_mgr.show_tip('\xe6\xa8\xa1\xe5\x9e\x8b\xe8\xbf\x98\xe6\xb2\xa1\xe5\x8a\xa0\xe8\xbd\xbd\xe5\xae\x8c~\xe5\x88\xab\xe6\x80\xa5')
            return
        else:
            model = self.get_model()
            sfx_path = sfx_data.get('sfx_path')
            idx = sfx_data.get('idx')
            socket_name = sfx_data.get('socket_name')
            second_socket_name = sfx_data.get('second_socket_name')
            cb = sfx_data.get('create_cb', None)

            def callback(sfx, idx=idx, sfx_data=sfx_data):
                sfx_data['sfx'] = sfx
                if cb:
                    cb(idx, sfx_data)

            sfx_id = None
            if second_socket_name:
                obj_list = model.get_socket_objects(socket_name)
                for obj in obj_list:
                    if str(obj.filename).endswith('.gim'):
                        sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, obj, second_socket_name, on_create_func=callback)

            else:
                sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket_name, on_create_func=callback)
            self.idx_to_sfx_dict[idx] = sfx_id
            return

    def on_delete_sfx(self, sfx_data):
        if not self.get_model():
            global_data.game_mgr.show_tip('\xe6\xa8\xa1\xe5\x9e\x8b\xe8\xbf\x98\xe6\xb2\xa1\xe5\x8a\xa0\xe8\xbd\xbd\xe5\xae\x8c~\xe5\x88\xab\xe6\x80\xa5')
            return
        else:
            cb = sfx_data.get('delete_cb', None)
            idx = sfx_data.get('idx')
            if cb:
                cb(idx)
            global_data.sfx_mgr.remove_sfx_by_id(self.idx_to_sfx_dict.get(idx, None))
            return

    def destroy(self):
        self.parent = None
        self.clear_model()
        self.process_event(False)
        if self.trk_player:
            self.trk_player.on_exit()
            self.trk_player = None
        return


class PartArtCheckModelDisplay(ScenePart.ScenePart):
    ENTER_EVENT = {'change_artcheck_model_display_item': 'on_change_display_model',
       'change_artcheck_model_display_anim': 'on_change_display_anim',
       'add_pendant_by_bind': 'on_add_pendant_by_bind',
       'add_pendant_by_add_mesh': 'on_add_pendant_by_add_mesh',
       'delete_pendant_from_add_mesh': 'on_delete_pendant_from_add_mesh',
       'delete_pendant_from_bind': 'on_delete_pendant_from_bind',
       'enable_character_outline': 'on_enable_display_model_outline',
       'disable_character_outline': 'on_disable_display_model_outline',
       'add_sfx': 'on_add_sfx',
       'delete_sfx': 'on_delete_sfx'
       }

    def __init__(self, scene, name):
        super(PartArtCheckModelDisplay, self).__init__(scene, name, True)
        self.model_obj = None
        self.model_data = None
        return

    def on_enter(self):
        import render
        render.enable_dynamic_culling(False)
        scn = self.scene()
        scn.set_adapt_factor(1.0)
        if global_data.is_ue_model and global_data.feature_mgr.is_dynamic_ue_env_config():
            self.scene().load_env('default_nx2_mobile.xml')
            self.scene().viewer_position = math3d.vector(0, 0, 0)

    def on_change_display_anim(self, anim_data):
        if not anim_data or not self.model_obj:
            return
        self.model_obj.change_anim(anim_data)

    def on_change_display_model(self, model_data, force=False):
        if self.model_data == model_data and not force:
            return
        self.clear_model()
        self.model_data = model_data
        self.scene().active_camera.fov = 30
        if self.model_data:
            self.model_obj = CArtCheckModel(self, self.model_data)

    def on_add_pendant_by_bind(self, pendant_data):
        if not self.model_obj:
            return
        self.model_obj.add_pendant_by_bind(pendant_data)

    def on_add_pendant_by_add_mesh(self, pendant_data):
        if not self.model_obj:
            return
        self.model_obj.add_pendant_by_add_mesh(pendant_data)

    def on_delete_pendant_from_bind(self, pendant_data):
        if not self.model_obj:
            return
        self.model_obj.delete_pendant_from_bind(pendant_data)

    def on_delete_pendant_from_add_mesh(self, pendant_data):
        if not self.model_obj:
            return
        self.model_obj.delete_pendant_from_add_mesh(pendant_data)

    def on_enable_display_model_outline(self):
        if not self.model_obj:
            return
        self.model_obj.enable_model_outline()

    def on_disable_display_model_outline(self):
        if not self.model_obj:
            return
        self.model_obj.disable_model_outline()

    def on_add_sfx(self, sfx_data):
        if not self.model_obj:
            return
        self.model_obj.on_add_sfx(sfx_data)

    def on_delete_sfx(self, sfx_data):
        if not self.model_obj:
            return
        self.model_obj.on_delete_sfx(sfx_data)

    def clear_model(self):
        if self.model_obj:
            self.model_obj.destroy()
        self.model_obj = None
        return

    def on_update(self, dt):
        if self.model_obj:
            self.model_obj.on_update(dt)

    def on_exit(self):
        self.clear_model()