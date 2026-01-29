# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/cinematic/resdata.py
from __future__ import absolute_import
import six_ex
from six.moves import range
import game3d
import math3d
import world
import audio
import render
import tinyxml
import sys
from .datacommon import *
from . import datadefines
from . import cinecallback
from . import spline
from . import eventdata

class LightRes(object):

    def __init__(self):
        self._light = None
        self._enable = False
        self._ambient = math3d.vector(0.0, 0.0, 0.0)
        self._diffuse = math3d.vector(255, 255, 255)
        self._intensity = 1
        self._range = 100
        self._pos = math3d.vector(0.0, 0.0, 0.0)
        self._cutoff_power = 5
        return

    def clear(self):
        self._light = None
        return

    def set_light(self, light):
        self._light = light
        self.get_light_state()

    def update_light(self):
        if self._light and self._enable:
            self._light.enable = self._enable
            self._light.ambient = (self._ambient.x, self._ambient.y, self._ambient.z)
            self._light.diffuse = (self._diffuse.x, self._diffuse.y, self._diffuse.z)
            self._light.intensity = self._intensity
            self._light.range = self._range
            self._light.cutoff_power = self._cutoff_power
            self._light.position = self._pos + datadefines.Cinematic.instance().get_offset()

    def update_pos(self):
        if self._light and self._enable:
            self._light.position = self._pos + datadefines.Cinematic.instance().get_offset()

    def get_light_state(self):
        if self._light:
            self._old_enable = self._light.enable
            self._old_ambient = self._light.ambient
            self._old_diffuse = self._light.diffuse
            self._old_intensity = self._light.intensity
            self._old_range = self._light.range
            self._old_cutoff_power = self._light.cutoff_power
            self._old_pos = self._light.position

    def restore_light_state(self):
        if self._light and '_old_ambient' in self.__dict__:
            self._light.enable = self._old_enable
            self._light.ambient = self._old_ambient
            self._light.diffuse = self._old_diffuse
            self._light.intensity = self._old_intensity
            self._light.range = self._old_range
            self._light.cutoff_power = self._old_cutoff_power
            self._light.position = self._old_pos

    def read(self, doc_node):
        if not doc_node:
            return
        self._enable = True if get_attribute(doc_node, 'enable') == 'True' else False
        self._ambient.from_string(get_attribute(doc_node, 'ambient'))
        self._diffuse.from_string(get_attribute(doc_node, 'diffuse'))
        self._intensity = float(get_attribute(doc_node, 'intensity'))
        self._range = float(get_attribute(doc_node, 'range'))
        self._pos.from_string(get_attribute(doc_node, 'pos'))
        self._cutoff_power = float(get_attribute(doc_node, 'cutoff_power', 5.0))
        self.update_light()

    def write(self, doc_node):
        doc_node.SetAttribute('enable', str(self._enable))
        doc_node.SetAttribute('ambient', self._ambient.to_string())
        doc_node.SetAttribute('diffuse', self._diffuse.to_string())
        doc_node.SetAttribute('intensity', '%f' % self._intensity)
        doc_node.SetAttribute('range', '%f' % self._range)
        doc_node.SetAttribute('pos', self._pos.to_string())
        doc_node.SetAttribute('cutoff_power', '%f' % self._cutoff_power)


class ResObjBase(object):

    def __init__(self, id=None):
        if not id:
            id = get_uuid()
        self._id = id
        self._res_type = RES_TYPE_BASE
        self._name = ''
        self._key_nodes = []
        self._event_nodes = {}
        self._enable = True
        self._available = True

    def sort_by_time(self):
        self._key_nodes.sort(key=lambda node: node._time)
        for event in six_ex.values(self._event_nodes):
            event.sort(key=lambda node: node._time)

    def release_res_obj(self):
        for event in self._key_nodes:
            event.release()

        self._key_nodes = []
        self._event_nodes.clear()

    def append_event(self, e):
        self._key_nodes.append(e)
        e._res_obj_id = self._id
        if e._etype not in self._event_nodes:
            self._event_nodes[e._etype] = []
        self._event_nodes[e._etype].append(e)

    def remove_event(self, e):
        self._key_nodes.remove(e)
        self._event_nodes[e._etype].remove(e)

    def read(self, doc_node):
        self._name = get_attribute(doc_node, 'name')
        self._res_type = int(get_attribute(doc_node, 'res_type'))
        self._id = get_attribute(doc_node, 'id')
        enable = get_attribute(doc_node, 'enable')
        self._enable = False if enable == 'False' else True

    def read_finish(self):
        self.sort_by_time()

    def write(self, doc_node):
        doc_node.SetAttribute('name', self._name)
        doc_node.SetAttribute('res_type', self._res_type)
        doc_node.SetAttribute('id', self._id)
        doc_node.SetAttribute('e_count', self._key_nodes.__len__())
        doc_node.SetAttribute('enable', str(self._enable))

    def execute_type(self):
        return EXECUTE_TYPE_DIRECT

    def copy(self, res):
        self._enable = res._enable

    def update(self, time):
        pass

    def do_single_frame(self, time, playing=False):
        self.sort_by_time()
        for events in six_ex.values(self._event_nodes):
            n = len(events)
            for idx, event in enumerate(events):
                if not event._active:
                    continue
                if event._time <= time and (idx + 1 < n and events[idx + 1]._time > time or idx == n - 1):
                    event.single_execute_update(time, playing)
                    break

        if self.execute_type() == EXECUTE_TYPE_INTERP:
            self.update(time)


class ResObjectSpaceobjBase(ResObjBase):

    def __init__(self, id=None):
        ResObjBase.__init__(self, id)
        self._scn_idx = -1

    def read(self, doc_node):
        ResObjBase.read(self, doc_node)
        self._scn_idx = int(get_attribute(doc_node, 'scn_idx', '-1'))

    def write(self, doc_node):
        ResObjBase.write(self, doc_node)
        doc_node.SetAttribute('scn_idx', str(self._scn_idx))

    def copy(self, res):
        ResObjBase.copy(self, res)
        self._scn_idx = res._scn_idx

    def whole_move(self, delta_pos):
        for e_data in self._key_nodes:
            if isinstance(e_data, eventdata.EventPosRotInfoBase):
                e_data._pos += delta_pos

        self.read_finish()

    def part_move(self, delta_pos, time):
        pre_idx = -1
        n = len(self._key_nodes)
        for idx, e_data in enumerate(self._key_nodes):
            if e_data._time <= time and (idx + 1 < n and self._key_nodes[idx + 1]._time > time or idx == n - 1):
                pre_idx = idx

        pre_prs_idx = pre_idx
        while pre_prs_idx >= 0:
            e_data = self._key_nodes[pre_prs_idx]
            if not isinstance(e_data, eventdata.EventPosRotInfoBase):
                pre_prs_idx -= 1
                continue
            else:
                e_data._pos += delta_pos
                break

        next_prs_idx = pre_idx + 1
        while next_prs_idx < n:
            e_data = self._key_nodes[next_prs_idx]
            if not isinstance(e_data, eventdata.EventPosRotInfoBase):
                next_prs_idx += 1
                continue
            else:
                e_data._pos += delta_pos
                break

        self.read_finish()


class ResObjCharacter(ResObjectSpaceobjBase):

    def __init__(self, id=None):
        ResObjectSpaceobjBase.__init__(self, id)
        self._res_type = RES_TYPE_CHARACTER
        self._name = ''
        self._res_obj_path = ''
        self._char_model = None
        self._model_in_scene = False
        self._spline = spline.SplinePosRot([])
        self._is_player = False
        self._player_position = math3d.vector(0, 0, 0)
        self._player_rotation = math3d.matrix()
        self._player_scale = math3d.vector(0, 0, 0)
        self._player_visible = True
        self._changed_visible = False
        self._is_scene_model = False
        return

    def update_player_transform(self):
        for event in self._key_nodes:
            if isinstance(event, eventdata.EventPosRotInfoBase):
                self._player_position = math3d.vector(event._pos)
                self._player_rotation = math3d.rotation_to_matrix(event._rot)
                break

    def show_suffix(self, show):
        self._spline.visible = show

    def get_character(self):
        return self._char_model

    def release_res_obj(self):
        super(ResObjCharacter, self).release_res_obj()
        if self._char_model:
            if not self._is_player:
                self._char_model.destroy()
            else:
                self._char_model.position = self._player_position
                self._char_model.rotation_matrix = self._player_rotation
                self._char_model.scale = self._player_scale
                if self._changed_visible:
                    self._char_model.visible = self._player_visible
            self._char_model = None
            self._model_in_scene = False
            self._is_player = False
        self._spline = None
        return

    def append_event(self, e):
        ResObjectSpaceobjBase.append_event(self, e)
        if e._etype == EVENT_TYPE_CHARACTER_WAYPOINT:
            self._spline.add_key(e)

    def remove_event(self, e):
        ResObjectSpaceobjBase.remove_event(self, e)
        if e._etype == EVENT_TYPE_CHARACTER_WAYPOINT:
            self._spline.remove_key(e)

    def show_model(self):
        if self._is_scene_model:
            return
        scn = datadefines.Cinematic.instance().get_scene_by_idx(self._scn_idx)
        if self._model_in_scene and self._char_model:
            if self._char_model.get_scene() is not scn:
                self.hide_model()
        if not self._model_in_scene and self._char_model:
            if self._is_player and datadefines.g_game_mode:
                self._char_model.visible = True
                self._changed_visible = self._player_visible == False
            else:
                scn.add_object(self._char_model)
                self._char_model.cast_shadow = True
            self._model_in_scene = True

    def hide_model(self):
        if self._is_scene_model:
            return
        if self._model_in_scene and self._char_model:
            if self._is_player and datadefines.g_game_mode:
                self._char_model.visible = False
                self._changed_visible = self._player_visible == True
            else:
                self._char_model.remove_from_parent()
            self._model_in_scene = False

    def load_model_sync(self, res_obj, userData, currentTask):
        try:
            self._char_model = res_obj
            self._model_in_scene = False
            self._available = True
        except:
            self._char_model = None

        return

    def load_model(self):
        try:
            if self._res_obj_path.endswith('.gim'):
                if datadefines.g_game_mode:
                    world.create_model_async(self._res_obj_path, self.load_model_sync)
                    self._available = False
                else:
                    self._char_model = world.model(self._res_obj_path, None)
                    self._model_in_scene = False
            else:
                scn = datadefines.Cinematic.instance().get_scene_by_idx(self._scn_idx)
                self._char_model = scn.get_model(self._res_obj_path)
                self._model_in_scene = True
                self._is_scene_model = True
        except:
            self._char_model = None

        return

    def set_path(self, path):
        self._res_obj_path = path
        if self._is_player:
            datadefines.Cinematic.instance().set_player_path(path)

    def read(self, doc_node):
        ResObjectSpaceobjBase.read(self, doc_node)
        is_player = get_attribute(doc_node, 'is_player', 'False')
        spline_type = int(get_attribute(doc_node, 'spline_type', SPLINE_TYPE_LINE))
        self._spline.set_intrp_type(spline_type)
        if is_player == 'True':
            self._is_player = True if 1 else False
            self.set_path(get_attribute(doc_node, 'res_obj_path'))
            self._is_player or self.load_model()
        else:
            self._char_model = cinecallback.get_player_model_callback()
            self._player_position = math3d.vector(self._char_model.position)
            self._player_rotation = math3d.matrix(self._char_model.rotation_matrix)
            self._player_scale = math3d.vector(self._char_model.scale)
            self._player_visible = self._char_model.visible
            self._model_in_scene = False

    def read_finish(self):
        self._spline.set_intrp_type(self._spline.get_intrp_type())
        if not datadefines.g_game_mode:
            self.update_player_transform()

    def write(self, doc_node):
        ResObjectSpaceobjBase.write(self, doc_node)
        doc_node.SetAttribute('res_obj_path', self._res_obj_path)
        doc_node.SetAttribute('is_player', str(self._is_player))
        doc_node.SetAttribute('spline_type', '%d' % self._spline.get_intrp_type())

    def execute_type(self):
        return EXECUTE_TYPE_INTERP

    def update(self, time):
        if not self._char_model:
            return
        if len(self._spline.get_keynodes()) > 0:
            pos = self._spline.get_position(time)
            rot = self._spline.get_rotation(time)
            self._char_model.position = pos + datadefines.Cinematic.instance().get_offset()
            self._char_model.rotation_matrix = math3d.rotation_to_matrix(rot)

    def copy(self, res):
        ResObjectSpaceobjBase.copy(self, res)
        self._res_obj_path = res._res_obj_path
        self._is_player = False
        self.load_model()


class ResObjAudio(ResObjBase):

    def __init__(self, id=None):
        ResObjBase.__init__(self, id)
        self._res_type = RES_TYPE_AUDIO
        self._name = ''
        self._res_obj_path = ''
        self._audio = None
        return

    def release_res_obj(self):
        if self._audio:
            file_path, audio_event = self._res_obj_path.split(':')
            self._audio = None
        super(ResObjAudio, self).release_res_obj()
        return

    def read(self, doc_node):
        ResObjBase.read(self, doc_node)
        self._res_obj_path = get_attribute(doc_node, 'res_obj_path')
        self.load_model()

    def load_model(self):
        try:
            file_path, audio_event = self._res_obj_path.split(':')
            audio.load_events(file_path)
            self._audio = audio.event(audio_event)
        except:
            self._audio = None

        return

    def write(self, doc_node):
        ResObjBase.write(self, doc_node)
        doc_node.SetAttribute('res_obj_path', self._res_obj_path)

    def copy(self, res):
        ResObjBase.copy(self, res)
        self._res_obj_path = res._res_obj_path
        self.load_model()


class ResObjSfx(ResObjectSpaceobjBase):

    def __init__(self, id=None):
        ResObjectSpaceobjBase.__init__(self, id)
        self._res_type = RES_TYPE_SFX
        self._name = ''
        self._res_obj_path = ''
        self._sfx = None
        self._in_scn = False
        self._spline = spline.SplinePosRot([])
        return

    def append_event(self, e):
        ResObjectSpaceobjBase.append_event(self, e)
        if e._etype == EVENT_TYPE_SFX_WAYPOINT:
            self._spline.add_key(e)

    def remove_event(self, e):
        ResObjectSpaceobjBase.remove_event(self, e)
        if e._etype == EVENT_TYPE_SFX_WAYPOINT:
            self._spline.remove_key(e)

    def release_res_obj(self):
        if self._sfx:
            self.hide_sfx()
            self._sfx.destroy()
            self._sfx = None
        super(ResObjSfx, self).release_res_obj()
        return

    def hide_sfx(self):
        if self._sfx and self._in_scn:
            self._sfx.shutdown()
            self._sfx.remove_from_parent()
            self._in_scn = False

    def show_sfx(self):
        scn = datadefines.Cinematic.instance().get_scene_by_idx(self._scn_idx)
        if self._in_scn and self._sfx:
            if self._sfx.get_scene() is not scn:
                self.hide_sfx()
        if self._sfx and not self._in_scn:
            scn.add_object(self._sfx)
        self._in_scn = True

    def read(self, doc_node):
        ResObjectSpaceobjBase.read(self, doc_node)
        self._res_obj_path = get_attribute(doc_node, 'res_obj_path')
        spline_type = int(get_attribute(doc_node, 'spline_type', SPLINE_TYPE_LINE))
        self._spline.set_intrp_type(spline_type)
        self.load_model()

    def load_model_sync(self, res_obj, userData, currentTask):
        self._sfx = res_obj
        self._available = True

    def load_model(self):
        try:
            if datadefines.g_game_mode:
                world.create_sfx_async(self._res_obj_path, self.load_model_sync)
                self._available = False
            else:
                self._sfx = world.sfx(self._res_obj_path, scene=None)
                self._sfx.shutdown()
        except:
            self._sfx = None

        return

    def write(self, doc_node):
        ResObjectSpaceobjBase.write(self, doc_node)
        doc_node.SetAttribute('res_obj_path', self._res_obj_path)
        doc_node.SetAttribute('spline_type', '%d' % self._spline.get_intrp_type())

    def copy(self, res):
        ResObjectSpaceobjBase.copy(self, res)
        self._res_obj_path = res._res_obj_path
        self.load_model()

    def execute_type(self):
        return EXECUTE_TYPE_INTERP

    def update(self, time):
        if not self._sfx:
            return
        if EVENT_TYPE_SFX_RATE in self._event_nodes:
            sfx_rate_list = self._event_nodes[EVENT_TYPE_SFX_RATE]
            idx = find_obj_idx_in_sorted_list_prev_time(sfx_rate_list, time)
            rate = 1.0
            if idx >= 0:
                node1 = sfx_rate_list[idx]
                rate = node1._rate
                if len(sfx_rate_list) > idx + 1:
                    node2 = sfx_rate_list[idx + 1]
                    if node2._time - node1._time > 0.0:
                        ratio = (time - node1._time) / (node2._time - node1._time)
                        rate = rate * (1.0 - ratio) + node2._rate * ratio
            self._sfx.frame_rate = rate
        if len(self._spline.get_keynodes()) > 0:
            pos = self._spline.get_position(time)
            rot = self._spline.get_rotation(time)
            self._sfx.position = pos + datadefines.Cinematic.instance().get_offset()
            self._sfx.rotation_matrix = math3d.rotation_to_matrix(rot)


class ResObjDialogue(ResObjBase):

    def __init__(self, id=None):
        ResObjBase.__init__(self, id)
        self._res_type = RES_TYPE_DIALOGUE


class ResObjSubtitle(ResObjBase):

    def __init__(self, id=None):
        ResObjBase.__init__(self, id)
        self._res_type = RES_TYPE_SUBTITLE


class ResObjScreen(ResObjBase):

    def __init__(self, id=None):
        ResObjBase.__init__(self, id)
        self._res_type = RES_TYPE_SCREEN
        self._name = ''
        self._process_name = 'screen_filter'
        self._factor_name = 'screen_color'
        self._factor_type = 'color'
        self._mtl_idx = 0
        self._var_name_hash = {}
        self._tex_param_info = []
        self._tex_name = ''
        self._tex = None
        self._spline = spline.SplineVec3W([])
        return

    def release_res_obj(self):
        self.set_screen_filter_active(False)
        super(ResObjScreen, self).release_res_obj()
        self._spline = None
        return

    def append_event(self, e):
        ResObjBase.append_event(self, e)
        self._spline.add_key(e)

    def modify_screen_filter(self, value):
        name = self._process_name
        factor = self._factor_name
        mat = global_data.display_agent.get_post_effect_pass_mtl(name, self._mtl_idx)
        if mat:
            if factor not in self._var_name_hash:
                self._var_name_hash[factor] = game3d.calc_string_hash(factor)
            strid = self._var_name_hash.get(factor)
            mat.set_var(self._var_name_hash[factor], factor, value)

    def set_texture(self, tex):
        self._tex_name = tex
        tex_type = 0
        if self._process_name == 'color_grading':
            tex_type = render.TEXTURE_TYPE_LUT
        self._tex = render.texture(tex, type=tex_type)

    def set_screen_filter_active(self, is_active):
        name = self._process_name
        global_data.display_agent.set_post_effect_active(name, is_active)
        if self._tex and is_active:
            mat = global_data.display_agent.get_post_effect_pass_mtl(name, self._tex_param_info[1])
            if mat:
                if self._tex_param_info[0] not in self._var_name_hash:
                    self._var_name_hash[self._tex_param_info[0]] = game3d.calc_string_hash(self._tex_param_info[0])
                mat.set_texture(self._var_name_hash[self._tex_param_info[0]], self._tex_param_info[0], self._tex)

    def execute_type(self):
        return EXECUTE_TYPE_INTERP

    def read(self, doc_node):
        super(ResObjScreen, self).read(doc_node)
        prc_name = get_attribute(doc_node, 'process_name')
        if prc_name:
            self._process_name = prc_name
        fct_name = get_attribute(doc_node, 'factor_name')
        if fct_name:
            self._factor_name = fct_name
        fct_type = get_attribute(doc_node, 'factor_type')
        if fct_type:
            self._factor_type = fct_type
        self._tex_name = get_attribute(doc_node, 'texture', '')
        if self._tex_name:
            self._tex = render.texture(self._tex_name)
            tex_param_name = get_attribute(doc_node, 'tex_param_name', 'Tex')
            tex_param_mtl_idx = int(get_attribute(doc_node, 'tex_param_mtl_idx', '0'))
            self._tex_param_info = [tex_param_name, tex_param_mtl_idx]
        self._mtl_idx = int(get_attribute(doc_node, 'mtl_idx', '0'))

    def write(self, doc_node):
        super(ResObjScreen, self).write(doc_node)
        doc_node.SetAttribute('process_name', self._process_name)
        doc_node.SetAttribute('factor_name', self._factor_name)
        doc_node.SetAttribute('factor_type', self._factor_type)
        doc_node.SetAttribute('mtl_idx', self._mtl_idx)
        doc_node.SetAttribute('texture', self._tex_name)
        if self._tex_name and len(self._tex_param_info) >= 2:
            doc_node.SetAttribute('tex_param_name', self._tex_param_info[0])
            doc_node.SetAttribute('tex_param_mtl_idx', self._tex_param_info[1])

    def update(self, time):
        if self._key_nodes.__len__() > 0:
            if self._key_nodes[0]._time > time:
                return
            al = []
            v = self._spline.get_vec3(time)
            w = self._spline.get_w(time)
            if self._factor_type == 'vector':
                al = (
                 v.x, v.y, y.z)
            elif self._factor_type == 'float':
                al = w
            elif self._factor_type == 'color':
                al = (
                 v.x, v.y, v.z, w)
            self.modify_screen_filter(al)

    def copy(self, res):
        ResObjBase.copy(self, res)
        self._process_name = res._process_name
        self._factor_type = res._factor_type
        self._factor_name = res._factor_name


class ResObjCamera(ResObjectSpaceobjBase):

    def __init__(self, id=None):
        ResObjectSpaceobjBase.__init__(self, id)
        self._name = ''
        self._res_type = RES_TYPE_CAMERA_TRACK
        self._spline = spline.SplinePosRotFov([])
        self._cur_focus_event = None
        self._auto_forward = False
        self._z_far = -1.0
        return

    def execute_type(self):
        return EXECUTE_TYPE_INTERP

    def read(self, doc_node):
        ResObjectSpaceobjBase.read(self, doc_node)
        if datadefines.Cinematic.instance().get_version() < 513:
            spline_type = SPLINE_TYPE_LINE
        else:
            spline_type = int(get_attribute(doc_node, 'spline_type', SPLINE_TYPE_BEZIER))
        self._spline.set_intrp_type(spline_type)
        self._auto_forward = True if get_attribute(doc_node, 'auto_forward', 'False') == 'True' else False
        self._z_far = float(get_attribute(doc_node, 'z_far', '-1.0'))

    def write(self, doc_node):
        ResObjectSpaceobjBase.write(self, doc_node)
        doc_node.SetAttribute('spline_type', '%d' % self._spline.get_intrp_type())
        doc_node.SetAttribute('auto_forward', str(self._auto_forward))
        doc_node.SetAttribute('z_far', str(self._z_far))

    def append_event(self, e):
        ResObjectSpaceobjBase.append_event(self, e)
        if e._etype == EVENT_TYPE_CAMERA_TRACK_NODE:
            self._spline.add_key(e)

    def remove_event(self, e):
        ResObjectSpaceobjBase.remove_event(self, e)
        if e._etype == EVENT_TYPE_CAMERA_TRACK_NODE:
            self._spline.remove_key(e)
        elif e._etype == EVENT_TYPE_CAMERA_FOCUS and self._cur_focus_event == e:
            self.remove_focus_event()

    def update(self, time):
        if self == datadefines.Cinematic.instance().get_cur_track() and self._key_nodes.__len__() > 0 and self._scn_idx == datadefines.Cinematic.instance().get_cur_scn_idx():
            fov = self._spline.get_fov(time)
            pos = self._spline.get_position(time) + datadefines.Cinematic.instance().get_offset()
            rot = None
            if self._cur_focus_event and self._cur_focus_event._focus_ratio < 0:
                cam_pos, cam_rot_mat, cam_fov = datadefines.Cinematic.instance().get_camera_param()
                rot_mat = None
                if not self._cur_focus_event.is_end_focus():
                    idx = find_obj_idx_in_sorted_list_next_time(self._event_nodes[EVENT_TYPE_CAMERA_FOCUS], time)
                    next_event = None
                    if idx >= 0:
                        next_event = self._event_nodes[EVENT_TYPE_CAMERA_FOCUS][idx]
                    rot_mat = self._cur_focus_event.get_cur_rot_mat(cam_rot_mat, pos, next_event, time)
                    rot = math3d.matrix_to_rotation(rot_mat)
                else:
                    target_rot = self._spline.get_rotation(time, self._auto_forward)
                    rot = self._cur_focus_event.get_end_cur_rot(cam_rot_mat, target_rot)
            else:
                rot = self._spline.get_rotation(time, self._auto_forward)
                rot_mat = math3d.rotation_to_matrix(rot)
                if self._cur_focus_event:
                    idx = find_obj_idx_in_sorted_list_next_time(self._event_nodes[EVENT_TYPE_CAMERA_FOCUS], time)
                    next_event = None
                    if idx >= 0:
                        next_event = self._event_nodes[EVENT_TYPE_CAMERA_FOCUS][idx]
                    rot_mat = self._cur_focus_event.get_cur_rot_mat(rot_mat, pos, next_event, time)
                    rot = math3d.matrix_to_rotation(rot_mat)
            datadefines.Cinematic.instance().set_camera_param(pos, rot, fov)
            if self._z_far > 0.0:
                cam = datadefines.Cinematic.instance().get_camera()
                old_z = cam.z_range
                cam.z_range = (old_z[0], self._z_far)
        return

    def do_single_frame(self, time, playing):
        self.remove_focus_event()
        super(ResObjCamera, self).do_single_frame(time, playing)

    def copy(self, res):
        ResObjectSpaceobjBase.copy(self, res)
        self._spline.set_intrp_type(res._spline.get_intrp_type())

    def read_finish(self):
        self._spline.set_intrp_type(self._spline.get_intrp_type())

    def set_focus_event(self, e):
        self._cur_focus_event = e

    def remove_focus_event(self):
        self._cur_focus_event = None
        return


class ResObjDirector(ResObjBase):

    def __init__(self, id=None):
        ResObjBase.__init__(self, id)
        self._res_type = RES_TYPE_DIRECTOR

    def do_single_frame(self, time, playing):
        self.sort_by_time()
        if len(self._key_nodes) > 0 and self._key_nodes[0]._time > time:
            datadefines.Cinematic.instance().change_scene(-1)
        else:
            super(ResObjDirector, self).do_single_frame(time, playing)


class ResObjSceneConfig(ResObjBase):

    def __init__(self, id=None):
        ResObjBase.__init__(self, id)
        self._res_type = RES_TYPE_SCENE_CONFIG
        self._extra_scenes_paths = []

    def set_scene_path(self, idx, path):
        self._extra_scenes_paths[idx] = path
        datadefines.Cinematic.instance().set_extra_scene(path, idx)

    def read(self, doc_node):
        super(ResObjSceneConfig, self).read(doc_node)
        extra_scenes_node = get_child_doc(doc_node, 'extra_scenes')
        count = get_attribute(extra_scenes_node, 'count', '0')
        count = int(count)
        for i in range(0, count):
            scene_i = get_child_doc(extra_scenes_node, 'scene_%d' % i)
            path = get_attribute(scene_i, 'path', '')
            self._extra_scenes_paths.append(path)

        datadefines.Cinematic.instance().set_extra_scene_paths(self._extra_scenes_paths)

    def write(self, doc_node):
        super(ResObjSceneConfig, self).write(doc_node)
        extra_scenes_node = doc_node.InsertEndChild(tinyxml.TiXmlElement('extra_scenes'))
        count = len(self._extra_scenes_paths)
        extra_scenes_node.SetAttribute('count', str(count))
        for i in range(0, count):
            scene_i = extra_scenes_node.InsertEndChild(tinyxml.TiXmlElement('scene_%d' % i))
            scene_i.SetAttribute('path', self._extra_scenes_paths[i])

    def get_extra_scenes_path_list(self):
        return self._extra_scenes_paths

    def do_single_frame(self, time, playing):
        super(ResObjSceneConfig, self).do_single_frame(time, playing)
        if EVENT_TYPE_SCENE_CHANGE in self._event_nodes:
            scn_change_events = self._event_nodes[EVENT_TYPE_SCENE_CHANGE]
            if len(scn_change_events) > 0 and scn_change_events[0]._time > time:
                datadefines.Cinematic.instance().change_scene(-1)
        if EVENT_TYPE_FOG in self._event_nodes:
            fog_events = self._event_nodes[EVENT_TYPE_FOG]
            if len(fog_events) > 0 and fog_events[0]._time > time:
                datadefines.Cinematic.instance().reset_fog()


class ResObjFlashMovie(ResObjBase):

    def __init__(self, id=None):
        ResObjBase.__init__(self, id)
        self._res_type = RES_TYPE_FLASHMOVIE
        self._flash_movie = None
        self._res_obj_path = ''
        return

    def read(self, doc_node):
        super(ResObjFlashMovie, self).read(doc_node)
        self._res_obj_path = get_attribute(doc_node, 'movie_path')
        self.load_movie()

    def load_movie(self):
        if self._flash_movie:
            flashui.destroy_movie(self._flash_movie)
            self._flash_movie = None
        self._flash_movie = flashui.create_movie(self._res_obj_path)
        if self._flash_movie:
            import Scaleform
            self._flash_movie.get_gfx_movie().SetViewAlignment(Scaleform.GFx.Movie.Align_TopLeft)
            self._flash_movie.get_gfx_movie().SetViewScaleMode(Scaleform.GFx.Movie.SM_ShowAll)
            self._flash_movie.get_gfx_movie().SetVisible(False)
            self._flash_movie.get_gfx_movie().SetPlayState(Scaleform.GFx.State_Stopped)
        return

    def write(self, doc_node):
        super(ResObjFlashMovie, self).write(doc_node)
        doc_node.SetAttribute('movie_path', self._res_obj_path)

    def release_res_obj(self):
        if self._flash_movie:
            flashui.destroy_movie(self._flash_movie)
            self._flash_movie = None
        super(ResObjFlashMovie, self).release_res_obj()
        return

    def copy(self, res):
        ResObjBase.copy(self, res)
        self._res_obj_path = res._res_obj_path
        self.load_movie()


class ResObjSpeedRate(ResObjBase):

    def __init__(self, id=None):
        ResObjBase.__init__(self, id)
        self._res_type = RES_TYPE_SPEED_RATE

    def execute_type(self):
        return EXECUTE_TYPE_INTERP

    def release_res_obj(self):
        ResObjBase.release_res_obj(self)
        datadefines.Cinematic.instance().set_speed_rate(1.0)

    def update(self, time):
        if self._key_nodes.__len__() > 0:
            event_nodes = self._event_nodes[EVENT_TYPE_SPEED_RATE]
            idx1 = find_obj_idx_in_sorted_list_prev_time(event_nodes, time)
            idx2 = find_obj_idx_in_sorted_list_next_time(event_nodes, time)
            if idx1 < 0 and idx2 < 0:
                return
            if idx1 < 0:
                return
            if idx2 < 0:
                datadefines.Cinematic.instance().set_speed_rate(event_nodes[idx1]._speed_rate)
                return
            event1 = event_nodes[idx1]
            event2 = event_nodes[idx2]
            if event2._time == event1._time:
                datadefines.Cinematic.instance().set_speed_rate(event_nodes[idx1]._speed_rate)
                return
            u = (time - event1._time) / (event2._time - event1._time)
            sr = event1._speed_rate * (1 - u) + event2._speed_rate * u
            datadefines.Cinematic.instance().set_speed_rate(sr)

    def do_single_frame(self, time, playing):
        self.sort_by_time()
        if len(self._key_nodes) > 0 and self._key_nodes[0]._time > time:
            datadefines.Cinematic.instance().set_speed_rate(1.0)
        else:
            super(ResObjSpeedRate, self).do_single_frame(time, playing)


class ResObjAction(ResObjBase):

    def __init__(self, id=None):
        ResObjBase.__init__(self, id)
        self._res_type = RES_TYPE_ACTION

    def do_single_frame(self, time, playing):
        pass


class ResObjMgr(object):

    def __init__(self):
        self._e_dict = {}
        self._e_dict[RES_TYPE_BASE] = ResObjBase
        self._e_dict[RES_TYPE_CAMERA_TRACK] = ResObjCamera
        self._e_dict[RES_TYPE_CHARACTER] = ResObjCharacter
        self._e_dict[RES_TYPE_AUDIO] = ResObjAudio
        self._e_dict[RES_TYPE_SFX] = ResObjSfx
        self._e_dict[RES_TYPE_DIALOGUE] = ResObjDialogue
        self._e_dict[RES_TYPE_SCREEN] = ResObjScreen
        self._e_dict[RES_TYPE_SUBTITLE] = ResObjSubtitle
        self._e_dict[RES_TYPE_DIRECTOR] = ResObjDirector
        self._e_dict[RES_TYPE_SCENE_CONFIG] = ResObjSceneConfig
        self._e_dict[RES_TYPE_FLASHMOVIE] = ResObjFlashMovie
        self._e_dict[RES_TYPE_SPEED_RATE] = ResObjSpeedRate
        self._e_dict[RES_TYPE_ACTION] = ResObjAction

    def get_type_class(self, res_type):
        if res_type in self._e_dict:
            return self._e_dict[res_type]

    @staticmethod
    def instance():
        global _res_obj_mgr_inst
        try:
            _res_obj_mgr_inst
        except:
            _res_obj_mgr_inst = ResObjMgr()

        return _res_obj_mgr_inst