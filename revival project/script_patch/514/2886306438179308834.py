# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/cinematic/datadefines.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
import math
import math3d
import game3d
import world
import audio
import tinyxml
import render
from . import cinecallback
cineaction = six_ex.LazyImporter('cinematic.cineaction')
from .datacommon import *
resdata = six_ex.LazyImporter('cinematic.resdata')
eventdata = six_ex.LazyImporter('cinematic.eventdata')
g_game_mode = True
_HASH_screen_color = game3d.calc_string_hash('screen_color')

def get_max_name_sn(obj_list, default_prefix):
    max_sn = 0
    for obj in obj_list:
        s = obj._name.split('_')
        if s.__len__() == 2 and s[0] == default_prefix and s[1].isdigit():
            n = int(s[1])
            if n >= max_sn:
                max_sn = n + 1

    return max_sn


def get_max_number_sn(event_list):
    max_sn = 0
    for event in event_list:
        n = event._number
        if n >= max_sn:
            max_sn = n + 1

    return max_sn


class Cinematic(object):

    def __init__(self):
        self._cinema_filename = ''
        self._camera = None
        self._old_camera_pos = math3d.vector(0, 0, 0)
        self._old_camera_rot = math3d.rotation(0, 0, 0, 1)
        self._old_camera_fov = 45
        self._old_camera_zrange = (0.0, 0.0)
        self._on_set_camera = lambda pos, rot, fov: True
        self._on_get_camera = lambda : False
        self._all_res_objects = []
        self._last_time = 0.0
        self._cur_time = 0.0
        self._is_playing = False
        self._active_track_name = ''
        self._cur_track = None
        self._first_ready_to_play = True
        self._scene = None
        self._scn_file_path = ''
        self._ori_fog_info = []
        self._extra_scene = []
        self._extra_scene_paths = []
        self._on_change_scene = lambda scn: None
        self._cur_scn_idx = -1
        self._cine_total_length = DEFAULT_TIME_LENGTH
        self._smooth_in_time = 1000.0
        self._smooth_out_time = 1000.0
        self._started_black_filter = False
        self._start_black_enable = True
        self._end_black_enable = True
        self._camera_smooth_in = False
        self._camera_smooth_out = False
        self._old_view_range = 0
        self._old_view_position = math3d.vector(0.0, 0.0, 0.0)
        self._scn_offset = math3d.vector(0.0, 0.0, 0.0)
        self._light_res = None
        self._player_path = 'model/warrior/male.gim'
        self._frame_time_mul = 1.0
        self._tex_level = -1
        self._relative_to_player = False
        return

    def get_version(self):
        return self._version

    def clear(self):
        print('clear last cinema file-----', self._cinema_filename)
        cineaction.clear()
        self._cinema_filename = ''
        self.reset_fog()
        for obj in self._all_res_objects:
            obj.release_res_obj()

        self._all_res_objects = []
        need_restore = True
        if self._cur_scn_idx >= 0 and self.get_scene_by_idx(self._cur_scn_idx):
            need_restore = False
        self.unload_extra_scene()
        if self._scene:
            if need_restore:
                self._camera = self._scene.active_camera
                self._camera.z_range = self._old_camera_zrange
                self._camera.fov = self._old_camera_fov
                self._camera.world_position = self._old_camera_pos
                self._camera.world_rotation_matrix = math3d.rotation_to_matrix(self._old_camera_rot)
                self._camera = None
                self._scene.viewer_position = self._old_view_position
            self._old_view_range = 0
            self._scene = None
        self.set_speed_rate(1.0)
        self._last_time = 0.0
        self._cur_time = 0.0
        self._is_playing = False
        self._first_ready_to_play = True
        self._active_track_name = ''
        self._cur_track = None
        self._player_path = 'model/warrior/male.gim'
        self._cine_total_length = DEFAULT_TIME_LENGTH
        self._scn_offset = math3d.vector(0.0, 0.0, 0.0)
        if self._light_res:
            self._light_res.restore_light_state()
            self._light_res.clear()
        self._light_res = None
        if self._tex_level >= 0:
            render.set_texture_skip_level('.+\\\\lightmap\\\\[^\\\\]+.dds', self._tex_level)
            self._tex_level = -1
        return

    @staticmethod
    def instance():
        global _cinematic_inst
        try:
            _cinematic_inst
        except:
            _cinematic_inst = Cinematic()

        return _cinematic_inst

    def get_camera(self):
        return self._camera

    def set_camera_param(self, pos, rot, fov):
        if not self._on_set_camera(pos, rot, fov):
            return
        self._camera.world_position = pos
        self._camera.world_rotation_matrix = math3d.rotation_to_matrix(rot)
        self._camera.set_perspect(fov, self._camera.aspect, *self._camera.z_range)
        if not self._scene.scene_col:
            point = pos
        else:
            hit, point, normal, fraction, color, objs = self._scene.scene_col.hit_by_ray(pos, pos + self._camera.world_rotation_matrix.forward * 660)
            if not hit:
                point = pos
        audio.set_3d_listener(point, self._camera.world_rotation_matrix.forward, self._camera.world_rotation_matrix.up)

    def get_camera_param(self, use_rot_mat=True):
        re = self._on_get_camera()
        if re:
            return (re[0], re[1] if use_rot_mat else math3d.matrix_to_rotation(re[1]), re[2])
        return (
         self._camera.world_position, self._camera.world_rotation_matrix if use_rot_mat else math3d.matrix_to_rotation(self._camera.world_rotation_matrix), self._camera.fov)

    def get_old_camera_param(self):
        return (
         self._old_camera_pos, self._old_camera_rot, self._old_camera_fov)

    def set_camera_param_callback(self, f):
        self._on_set_camera = f

    def get_camera_param_callback(self, f):
        self._on_get_camera = f

    def get_scene(self):
        return self._scene

    def get_cur_scene(self):
        return self.get_scene_by_idx(self._cur_scn_idx)

    def set_scene(self, scene, scene_path):
        self._scene = scene
        self._scn_file_path = scene_path
        self._ori_fog_info = self._scene.get_fog()
        self._cur_time = 0.0
        self._is_playing = False
        self._camera = scene.active_camera
        self._old_view_range = self._scene.view_range
        self._old_view_position = self._scene.viewer_position
        self._light_res = resdata.LightRes()
        self._light_res.set_light(cinecallback.light_callback(scene))
        self._old_camera_pos = math3d.vector(self._camera.world_position)
        self._old_camera_rot = math3d.matrix_to_rotation(self._camera.world_rotation_matrix)
        self._old_camera_fov = self._camera.fov
        self._old_camera_zrange = self._camera.z_range
        self._camera.z_range = (1.0, self._old_camera_zrange[1])

    def get_offset(self):
        if self._cur_scn_idx < 0:
            return self._scn_offset
        return math3d.vector(0.0, 0.0, 0.0)

    def get_scene_size(self):
        if self._scene:
            max_p, min_p = self._scene.get_bounding()
            cnt_x = (max_p.x + min_p.x) / 2
            cnt_z = (max_p.z + min_p.z) / 2
            return (
             cnt_x + 1600, cnt_z + 1600, cnt_x - 1600, cnt_z - 1600)
        else:
            return (0, 0, 0, 0)

    def load_extra_scene(self):
        path_n = len(self._extra_scene_paths)
        scn_n = len(self._extra_scene)
        if scn_n < path_n:
            self._extra_scene = []
            for path in self._extra_scene_paths:
                scn = None
                if path:
                    scn = load_scene_common(path, not g_game_mode)
                self._extra_scene.append(scn)

        return

    def unload_extra_scene(self):
        self.change_scene(-1)
        self._extra_scene = []
        self._extra_scene_paths = []
        self._cur_scn_idx = -1

    def set_change_scene_call_back(self, cb):
        self._on_change_scene = cb

    def set_extra_scene_paths(self, extra_scene_path_list):
        self._extra_scene_paths = extra_scene_path_list
        self.load_extra_scene()

    def set_extra_scene(self, path, idx):
        print('set_extra_scene', path, idx)
        while len(self._extra_scene_paths) <= idx:
            self._extra_scene_paths.append('')

        while len(self._extra_scene) <= idx:
            self._extra_scene.append(None)

        if self._extra_scene[idx] is not None:
            print('error!!!!!!exist', self._extra_scene[idx])
            return
        else:
            scn = load_scene_common(path, False)
            self._extra_scene[idx] = scn
            self._extra_scene_paths[idx] = path
            return

    def get_scene_by_idx(self, scene_idx):
        if scene_idx < 0 or scene_idx >= len(self._extra_scene):
            return self._scene
        scn = self._extra_scene[scene_idx]
        if scn:
            return scn
        return self._scene

    def get_cur_scn_idx(self):
        if self._cur_scn_idx < 0:
            return -1
        return self._cur_scn_idx

    def change_scene(self, scene_idx):
        if self._cur_scn_idx == scene_idx or self._cur_scn_idx < 0 and scene_idx < 0:
            return
        else:
            scn = None
            if scene_idx < 0:
                scn = self._scene
            else:
                if scene_idx < len(self._extra_scene):
                    scn = self._extra_scene[scene_idx]
                if scn is None:
                    return
            self._on_change_scene(scn)
            world.set_active_scene(scn)
            self._cur_scn_idx = scene_idx
            self._camera = scn.active_camera
            return

    def set_speed_rate(self, sr):
        if self._frame_time_mul != sr:
            self._frame_time_mul = sr
            game3d.set_speed_rate(sr)

    def get_loading_progress(self):
        if not self._scene:
            return (0, 1.0)
        sp = self._scene.get_progress()
        if sp < 1.0:
            return (1, sp)
        progress = 0.0
        total_progress = 0.0
        for scn in self._extra_scene:
            if scn:
                p = scn.get_progress()
                progress += p
                total_progress += 1.0

        if total_progress > progress + 0.001:
            return (2, progress / total_progress)
        return (3, 1.0)

    def is_ready_to_play(self):
        if self._camera_smooth_in:
            return True
        if self._scene.get_progress() < 1.0:
            return False
        extra_scn_num = len(self._extra_scene_paths)
        if len(self._extra_scene) < len(self._extra_scene_paths):
            return False
        for res in self._all_res_objects:
            if res._available == False:
                return False

        progress = 0.0
        total_progress = 0.0
        for scn in self._extra_scene:
            if scn:
                p = scn.get_progress()
                if p < 1.0:
                    scn.update()
                progress += p
                total_progress += 1.0

        if not g_game_mode:
            if progress < total_progress - 0.001:
                return False
        return True

    def read(self, file_name):
        self._cinema_filename = file_name
        doc = tinyxml.TiXmlDocument()
        import C_file
        buf = C_file.get_res_file(file_name, '')
        doc.Parse(buf)
        root = doc.RootElement()
        self._cine_total_length = float(get_attribute(root, 'length'))
        self._active_track_name = get_attribute(root, 'active_track')
        self._scn_file_path = get_attribute(root, 'scene')
        self._version = int(get_attribute(root, 'version', '0x0101'), 16)
        if get_attribute(root, 'start_black_enable'):
            self._start_black_enable = True if get_attribute(root, 'start_black_enable') == 'True' else False
            self._end_black_enable = True if get_attribute(root, 'end_black_enable') == 'True' else False
            self._smooth_in_time = float(get_attribute(root, 'start_black_time'))
            self._smooth_out_time = float(get_attribute(root, 'end_black_time'))
        self._camera_smooth_in = True if get_attribute(root, 'camera_smooth_in') == 'True' else False
        self._camera_smooth_out = True if get_attribute(root, 'camera_smooth_out') == 'True' else False
        if get_attribute(root, 'relative_to_player') == 'True':
            self._relative_to_player = True if 1 else False
            player_res = None
            res_obj_nodes = get_child_doc(root, 'res_objects')
            res_obj_count = int(get_attribute(res_obj_nodes, 'res_obj_count'))
            for i in range(res_obj_count):
                name_i = '%s_%d' % ('res_obj', i)
                res_node_i = get_child_doc(res_obj_nodes, name_i)
                res_type = int(get_attribute(res_node_i, 'res_type'))
                e_count = int(get_attribute(res_node_i, 'e_count'))
                rid = get_attribute(res_node_i, 'id')
                obj_class = resdata.ResObjMgr.instance().get_type_class(res_type)
                obj = obj_class(rid)
                obj.read(res_node_i)
                self.add_res_obj(obj)
                ids = {}
                for j in range(e_count):
                    key_j = '%s_%d' % ('key', j)
                    key_node_j = get_child_doc(res_node_i, key_j)
                    e_type = int(get_attribute(key_node_j, 'e_type'))
                    eid = get_attribute(key_node_j, 'id')
                    if eid in ids:
                        print('error: conflict-----', eid)
                    else:
                        e_class = eventdata.EventMgr.instance().get_type_class(e_type)
                        e = e_class(eid)
                        e.read(key_node_j)
                        obj.append_event(e)
                        ids[eid] = True

                obj.read_finish()
                if obj._res_type == RES_TYPE_CHARACTER:
                    if obj._is_player:
                        player_res = obj

            self._light_res or print('Failed to load light resource. Try to call set(scn) first.')
            return
        else:
            light_node = get_child_doc(root, 'light')
            if self._relative_to_player:
                self.transform_player_to_scene(player_res)
            return

    def transform_scene_to_player(self, player_res):
        if player_res:
            pos, rot, scale = player_res._player_position, player_res._player_rotation, player_res._player_scale
            mat = math3d.matrix()
            mat.translation = pos
            mat.rotation = rot
            mat.inverse()
            for res in self._all_res_objects:
                if isinstance(res, resdata.ResObjectSpaceobjBase):
                    if res._scn_idx == player_res._scn_idx:
                        for e in res._key_nodes:
                            if isinstance(e, eventdata.EventPosRotInfoBase):
                                e._pos = e._pos * mat
                                e._rot = math3d.matrix_to_rotation(math3d.rotation_to_matrix(e._rot) * mat.rotation)
                                if hasattr(e, '_ctrl1'):
                                    e._ctrl1 = e._ctrl1 * mat
                                    e._ctrl2 = e._ctrl2 * mat

        else:
            print('error: relative_to_player but no player')

    def transform_player_to_scene(self, player_res):
        if player_res:
            pos, rot, scale = player_res._player_position, player_res._player_rotation, player_res._player_scale
            mat = math3d.matrix()
            mat.translation = pos
            mat.rotation = rot
            for res in self._all_res_objects:
                if isinstance(res, resdata.ResObjectSpaceobjBase):
                    if res._scn_idx == player_res._scn_idx:
                        for e in res._key_nodes:
                            if isinstance(e, eventdata.EventPosRotInfoBase):
                                e._pos = e._pos * mat
                                e._rot = math3d.matrix_to_rotation(math3d.rotation_to_matrix(e._rot) * mat.rotation)
                                if hasattr(e, '_ctrl1'):
                                    e._ctrl1 = e._ctrl1 * mat
                                    e._ctrl2 = e._ctrl2 * mat

        else:
            print('error: relative_to_player but no player')

    def write(self, file_name):
        doc = tinyxml.TiXmlDocument()
        root = tinyxml.TiXmlElement('cinematic')
        root = doc.InsertEndChild(root)
        root.SetAttribute('scene', self._scn_file_path)
        root.SetAttribute('length', '%f' % self._cine_total_length)
        root.SetAttribute('active_track', self._active_track_name)
        root.SetAttribute('version', '513')
        root.SetAttribute('start_black_enable', str(self._start_black_enable))
        root.SetAttribute('end_black_enable', str(self._end_black_enable))
        root.SetAttribute('start_black_time', '%f' % self._smooth_in_time)
        root.SetAttribute('end_black_time', '%f' % self._smooth_out_time)
        root.SetAttribute('camera_smooth_in', str(self._camera_smooth_in))
        root.SetAttribute('camera_smooth_out', str(self._camera_smooth_out))
        root.SetAttribute('relative_to_player', str(self._relative_to_player))
        player_res = None
        if self._relative_to_player:
            for res in self._all_res_objects:
                if res._res_type == RES_TYPE_CHARACTER:
                    if res._is_player:
                        res.update_player_transform()
                        player_res = res

            self.transform_scene_to_player(player_res)
        res_obj_count = self._all_res_objects.__len__()
        res_obj_nodes = root.InsertEndChild(tinyxml.TiXmlElement('res_objects'))
        res_obj_nodes.SetAttribute('res_obj_count', '%d' % res_obj_count)
        i = 0
        for obj in self._all_res_objects:
            name_i = '%s_%d' % ('res_obj', i)
            res_node_i = res_obj_nodes.InsertEndChild(tinyxml.TiXmlElement(name_i))
            obj.sort_by_time()
            obj.write(res_node_i)
            i = i + 1
            key_count = obj._key_nodes.__len__()
            j = 0
            for e in obj._key_nodes:
                key_j = '%s_%d' % ('key', j)
                key_node_j = res_node_i.InsertEndChild(tinyxml.TiXmlElement(key_j))
                e.write(key_node_j)
                j = j + 1

        light_node = root.InsertEndChild(tinyxml.TiXmlElement('light'))
        self._light_res.write(light_node)
        doc.SaveFile(file_name)
        if self._relative_to_player:
            self.transform_player_to_scene(player_res)
        return

    def pre_load(self, fn, scene, tex_quality):
        self.clear()
        if tex_quality < 0:
            tex_quality = 0
        if tex_quality > 3:
            tex_quality = 3
        tex_level = {0: 3,1: 1,2: 0,3: 0}[tex_quality]
        render.set_texture_skip_level('.+\\\\lightmap\\\\[^\\\\]+.dds', min(3, tex_level + 2))
        self._tex_level = tex_level
        self.set_scene(scene, '')
        try:
            self.read(fn)
        except:
            self.clear()
            return

        if self._scene:
            if self._start_black_enable:
                self._cur_time = -self._smooth_in_time
                self.do_black_filter_update()

    def play_ext(self, fn, scene):
        if self._cinema_filename != fn:
            self._tex_level = -1
            self.clear()
            self.set_scene(scene, '')
            try:
                self.read(fn)
            except:
                print('error: cinema read file failed:', fn)
                self.clear()
                return

        self.play()

    def play(self):
        if self._is_playing:
            self.cancel()
        self._is_playing = True
        self._first_ready_to_play = True
        self._scn_offset = cinecallback.get_scene_offset_callback(self._scn_file_path)
        self._scn_offset.y = 0
        for obj in self._all_res_objects:
            if obj._res_type == RES_TYPE_DIRECTOR:
                if obj._key_nodes:
                    self._active_track_name = obj._key_nodes[0]._track_name

        track_name = self._active_track_name
        for obj in self._all_res_objects:
            if obj._res_type == RES_TYPE_CAMERA_TRACK and obj._name == track_name:
                self._cur_track = obj
            if obj._res_type == RES_TYPE_CHARACTER:
                obj.hide_model()
            elif obj._res_type == RES_TYPE_SFX:
                obj.hide_sfx()
            elif obj._res_type == RES_TYPE_SCREEN:
                obj.set_screen_filter_active(False)
            elif obj._res_type == RES_TYPE_CAMERA_TRACK:
                obj.remove_focus_event()
                for e in obj._key_nodes:
                    if e._etype == EVENT_TYPE_CAMERA_TRACK_NODE and e._start_position == True:
                        e._pos = math3d.vector(self._old_camera_pos)
                        e._rot = self._old_camera_rot
                        e._fov = self._old_camera_fov

        if (self._start_black_enable or self._camera_smooth_in) and self._cur_time == 0:
            self._cur_time = -self._smooth_in_time
        if self._cur_track:
            self.set_scene_viewer(self._cur_track)

    def direct_play(self):
        self._is_playing = True

    def is_playing(self):
        return self._is_playing

    def cancel(self):
        self._is_playing = False
        self._cur_time = 0.0
        self._last_time = 0.0
        self.shutdown_all_postprocess()
        self.change_scene(-1)
        self.set_speed_rate(1.0)
        self.reset_fog()

    def reset_fog(self):
        if self._scene and self._ori_fog_info:
            self._scene.set_fog(*self._ori_fog_info)

    def shutdown_all_postprocess(self):
        global_data.display_agent.set_post_effect_active('screen_filter', False)
        self._started_black_filter = False
        for obj in self._all_res_objects:
            if obj._res_type == RES_TYPE_SCREEN:
                obj.set_screen_filter_active(False)

    def set_scene_viewer(self, track):
        if EVENT_TYPE_CAMERA_TRACK_NODE in track._event_nodes:
            e = track._event_nodes[EVENT_TYPE_CAMERA_TRACK_NODE][0]
            self._scene.viewer_position = e._pos

    def do_black_filter_update(self):
        enable = False
        alpha = 0.0
        if self._cur_time < 0.0 and self._start_black_enable and self._smooth_in_time > 0:
            enable = True
            alpha = -self._cur_time / self._smooth_in_time
        elif self._end_black_enable and self._cur_time >= self._cine_total_length - self._smooth_out_time and self._smooth_out_time > 0:
            enable = True
            alpha = (self._cur_time - self._cine_total_length + self._smooth_out_time) / self._smooth_out_time
        global_data.display_agent.set_post_effect_active('screen_filter', True)
        self._started_black_filter = enable
        mat = global_data.display_agent.get_post_effect_pass_mtl('screen_filter', 0)
        if mat:
            mat.set_var(_HASH_screen_color, 'screen_color', (0.0, 0.0, 0.0, alpha))

    def do_camera_smooth_update(self):
        if g_game_mode:
            percent = 1.0
            if self._camera_smooth_in and self._cur_time < 0.0 and self._smooth_in_time > 0:
                percent = (self._smooth_in_time + self._cur_time) / self._smooth_in_time
            elif self._camera_smooth_out and self._smooth_out_time > 0 and self._cur_time >= self._cine_total_length - self._smooth_out_time:
                percent = 1.0 - (self._cur_time - self._cine_total_length + self._smooth_out_time) / self._smooth_out_time
            if percent < 1.0:
                pos, rot, fov = self.get_camera_param(False)
                cur_pos = math3d.vector(0, 0, 0)
                cur_pos.intrp(self._old_camera_pos, pos, percent)
                cur_rot = math3d.rotation(0, 0, 0, 1)
                cur_rot.slerp(self._old_camera_rot, rot, percent)
                self.set_camera_param(cur_pos, cur_rot, fov)

    def update(self, frame_time=1000.0 / 30.0):
        for obj in self._all_res_objects:
            if obj._res_type == RES_TYPE_CHARACTER:
                if obj._is_scene_model and not obj._char_model:
                    obj.load_model()

        cineaction.update()
        if not self._is_playing:
            return False
        if self._cur_time > self._cine_total_length:
            self.cancel()
            return False
        frame_time *= self._frame_time_mul
        if self.is_ready_to_play() or not self._first_ready_to_play:
            self.do_black_filter_update()
            if self._first_ready_to_play:
                self._first_ready_to_play = False
                l = self._last_time
                c = self._cur_time
                self._last_time = 0.1
                self._cur_time = 0.2
                self.do_single_frame()
                self._last_time = l
                self._cur_time = c
            else:
                self.do_frame()
            self._last_time = self._cur_time
            self._cur_time += frame_time
        elif not self._camera_smooth_in:
            global_data.display_agent.set_post_effect_active('screen_filter', True)
            mat = global_data.display_agent.get_post_effect_pass_mtl('screen_filter', 0)
            if mat:
                mat.set_var(_HASH_screen_color, 'screen_color', (0.0, 0.0, 0.0, 1.0))
        return True

    def do_frame(self):
        self._light_res.update_pos()
        for obj in self._all_res_objects:
            if not obj._enable:
                continue
            for e in obj._key_nodes:
                if e._active and e._time >= self._last_time and e._time < self._cur_time:
                    e.execute()

            if obj.execute_type() == EXECUTE_TYPE_INTERP:
                obj.update(self._last_time)

        self.do_camera_smooth_update()

    def do_single_frame(self, playing=False):
        self._light_res.update_pos()
        for obj in self._all_res_objects:
            if not obj._enable:
                continue
            obj.do_single_frame(self._cur_time, playing)

    def set_cur_time(self, time, playing=False):
        if self.is_ready_to_play():
            self._last_time = self._cur_time
            self._cur_time = time
            self.do_single_frame(playing)

    def get_cur_time(self):
        return self._cur_time

    def get_cur_track(self):
        return self._cur_track

    def set_active_track(self, trk_name):
        self._active_track_name = trk_name
        for obj in self._all_res_objects:
            if obj._res_type == RES_TYPE_CAMERA_TRACK and obj._name == trk_name:
                self._cur_track = obj
                break

    def add_res_obj(self, res_obj):
        self._all_res_objects.append(res_obj)

    def del_res_obj(self, res_obj):
        res_obj.release_res_obj()
        self._all_res_objects.remove(res_obj)

    def find_res_obj(self, res_obj_id):
        for res_obj in self._all_res_objects:
            if res_obj._id == res_obj_id:
                return res_obj

        return None

    def find_res_obj_by_name(self, res_obj_name):
        for res_obj in self._all_res_objects:
            if res_obj._name == res_obj_name:
                return res_obj

        return None

    def get_all_res_objs(self):
        return self._all_res_objects

    def set_player_model(self, res_obj_name, model):
        obj = self.find_res_obj_by_name(res_obj_name)
        if obj:
            obj._char_model = model

    def set_player_path(self, path):
        self._player_path = path

    def get_default_res_name(self, res_type):
        default_name_table = {RES_TYPE_CAMERA_TRACK: 'track',
           RES_TYPE_CHARACTER: 'character',
           RES_TYPE_AUDIO: 'audio',
           RES_TYPE_SFX: 'sfx',
           RES_TYPE_DIALOGUE: 'dialogue',
           RES_TYPE_SCREEN: 'screenfilter',
           RES_TYPE_SUBTITLE: 'subtitle',
           RES_TYPE_DIRECTOR: 'director',
           RES_TYPE_SCENE_CONFIG: 'scene',
           RES_TYPE_FLASHMOVIE: 'flash',
           RES_TYPE_SPEED_RATE: 'speed_rate',
           RES_TYPE_ACTION: 'action'
           }
        obj_list = []
        for obj in self._all_res_objects:
            if obj._res_type == res_type:
                obj_list.append(obj)

        default_prefix = default_name_table[res_type]
        max_sn = get_max_name_sn(obj_list, default_prefix)
        return default_prefix + '_' + str(max_sn)

    def get_default_event_name(self):
        e_list = []
        for obj in self._all_res_objects:
            e_list.extend(obj._key_nodes)

        max_sn = get_max_number_sn(e_list)
        return max_sn