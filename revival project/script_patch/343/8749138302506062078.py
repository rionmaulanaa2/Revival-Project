# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/cinematic/eventdata.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from . import datadefines
from . import cinecallback
from .datacommon import *
from . import resdata
import math
import render
import tinyxml
from . import cineaction

class EventMgr(object):

    def __init__(self):
        self._e_dict = {}
        self._e_dict[EVENT_TYPE_BASE] = EventBase
        self._e_dict[EVENT_TYPE_CAMERA_TRACK_NODE] = EventCameraNode
        self._e_dict[EVENT_TYPE_CAMERA_FOCUS] = EventCameraFocus
        self._e_dict[EVENT_TYPE_CHARACTER] = EventCharacter
        self._e_dict[EVENT_TYPE_CHARACTER_ANIM] = EventCharacterAnim
        self._e_dict[EVENT_TYPE_CHARACTER_WAYPOINT] = EventCharacterWaypoint
        self._e_dict[EVENT_TYPE_AUDIO] = EventAudio
        self._e_dict[EVENT_TYPE_SFX] = EventSfx
        self._e_dict[EVENT_TYPE_SFX_RATE] = EventSfxRate
        self._e_dict[EVENT_TYPE_SFX_WAYPOINT] = EventSfxWaypoint
        self._e_dict[EVENT_TYPE_DIALOGUE] = EventDialogue
        self._e_dict[EVENT_TYPE_SCREEN_FILTER] = EventScreenFilter
        self._e_dict[EVENT_TYPE_SUBTITLE] = EventSubtitle
        self._e_dict[EVENT_TYPE_CAMERA_TRACK] = EventCameraTrack
        self._e_dict[EVENT_TYPE_SCENE_CHANGE] = EventSceneChange
        self._e_dict[EVENT_TYPE_FOG] = EventFog
        self._e_dict[EVENT_TYPE_FLASH_DIRECT] = EventFlashDirect
        self._e_dict[EVENT_TYPE_FLASH_FUNCTION] = EventFlashFunction
        self._e_dict[EVENT_TYPE_SPEED_RATE] = EventSpeedRate
        self._e_dict[EVENT_TYPE_BUILD_IN_ACTION] = EventBuildinAction

    def get_type_class(self, e_type):
        if e_type in self._e_dict:
            return self._e_dict[e_type]

    @staticmethod
    def instance():
        global _eventmgr_inst
        try:
            _eventmgr_inst
        except:
            _eventmgr_inst = EventMgr()

        return _eventmgr_inst


class EventBase(object):

    def __init__(self, eid=None):
        self._etype = EVENT_TYPE_BASE
        self._name = '\xe4\xba\x8b\xe4\xbb\xb6'
        self._time = 0
        self._active = True
        if not eid:
            eid = get_uuid()
        self._id = eid
        self._res_obj_id = ''
        self._number = 0

    def editor_init_info(self):
        pass

    def release(self):
        pass

    def execute(self):
        pass

    def get_obj(self):
        obj = datadefines.Cinematic.instance().find_res_obj(self._res_obj_id)
        return obj

    def single_execute_update(self, time, playing=False):
        self.execute()

    def read(self, doc_node):
        import math
        self._etype = int(get_attribute(doc_node, 'e_type'))
        self._name = get_attribute(doc_node, 'name')
        self._time = math.floor(float(get_attribute(doc_node, 'time')))
        self._active = True if get_attribute(doc_node, 'active') == 'True' else False
        self._res_obj_id = get_attribute(doc_node, 'id')
        number = get_attribute(doc_node, 'number')
        if number:
            self._number = int(number)
        else:
            try:
                self._number = int(self._name.split('_')[1])
            except:
                pass

    def write(self, doc_node):
        import math
        doc_node.SetAttribute('e_type', self._etype)
        doc_node.SetAttribute('name', self._name)
        doc_node.SetAttribute('id', self._id)
        doc_node.SetAttribute('time', '%f' % math.floor(self._time))
        doc_node.SetAttribute('active', str(self._active))
        doc_node.SetAttribute('res_obj_id', self._res_obj_id)
        doc_node.SetAttribute('number', self._number)

    def copy(self, event):
        self._active = event._active

    def clone(self, same_id=True):
        c = EventMgr.instance().get_type_class(self._etype)
        clone_re = c()
        if same_id:
            clone_re._id = self._id
        clone_re._name = self._name
        clone_re._time = self._time
        clone_re._number = self._number
        clone_re._res_obj_id = self._res_obj_id
        clone_re.copy(self)
        return clone_re


class EventPosRotInfoBase(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._pos = math3d.vector(0, 0, 0)
        self._rot = math3d.rotation(0, 0, 0, 1)

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        pos = get_attribute(doc_node, 'pos')
        if not pos:
            pos = get_attribute(doc_node, 'place')
        if pos:
            self._pos.from_string(pos)
        rot = get_attribute(doc_node, 'rot')
        if not rot:
            rot = get_attribute(doc_node, 'rotation')
        if rot:
            self._rot.from_string(rot)
        self._pos.from_string(pos)
        self._rot.from_string(rot)

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('pos', self._pos.to_string())
        doc_node.SetAttribute('rot', self._rot.to_string())

    def copy(self, event):
        EventBase.copy(self, event)
        self._pos = math3d.vector(event._pos)
        self._rot = math3d.rotation(event._rot.x, event._rot.y, event._rot.z, event._rot.w)


class EventPosRotScaleInfoBase(EventPosRotInfoBase):

    def __init__(self, eid=None):
        EventPosRotInfoBase.__init__(self, eid)
        self._scale = math3d.vector(1, 1, 1)

    def read(self, doc_node):
        EventPosRotInfoBase.read(self, doc_node)
        scale = get_attribute(doc_node, 'scale')
        if scale:
            self._scale.from_string(scale)

    def write(self, doc_node):
        EventPosRotInfoBase.write(self, doc_node)
        doc_node.SetAttribute('scale', self._scale.to_string())

    def copy(self, event):
        EventPosRotInfoBase.copy(self, event)
        self._scale = math3d.vector(event._scale)


class EventCharacter(EventPosRotScaleInfoBase):

    def __init__(self, eid=None):
        EventPosRotScaleInfoBase.__init__(self, eid)
        self._etype = EVENT_TYPE_CHARACTER
        self._do_what = 'show'

    def editor_init_info(self):
        obj = self.get_obj()
        if not obj or not obj._char_model:
            return
        self._pos = obj._char_model.position - datadefines.Cinematic.instance().get_offset()
        self._rot = math3d.matrix_to_rotation(obj._char_model.rotation_matrix)

    def execute(self):
        obj = self.get_obj()
        if not obj._char_model:
            return
        if self._do_what == 'hide':
            obj.hide_model()
        elif self._do_what == 'show':
            obj.show_model()
        elif self._do_what == 'postprocess_off':
            obj._char_model.enable_postprocess = False
        elif self._do_what == 'postprocess_on':
            obj._char_model.enable_postprocess = True
        obj._char_model.position = self._pos + datadefines.Cinematic.instance().get_offset()
        obj._char_model.scale = self._scale
        obj._char_model.rotation_matrix = math3d.rotation_to_matrix(self._rot)

    def read(self, doc_node):
        EventPosRotScaleInfoBase.read(self, doc_node)
        hide = get_attribute(doc_node, 'hide')
        if hide:
            self._do_what = 'hide' if hide == 'True' else 'show'
        else:
            do_what = get_attribute(doc_node, 'do_what')
            if do_what:
                self._do_what = do_what

    def write(self, doc_node):
        EventPosRotScaleInfoBase.write(self, doc_node)
        doc_node.SetAttribute('do_what', str(self._do_what))

    def copy(self, event):
        EventPosRotScaleInfoBase.copy(self, event)
        self._do_what = event._do_what


class EventCharacterAnim(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_CHARACTER_ANIM
        self._anim = ''
        self._start_time = 0.0
        self._speed_rate = 1.0
        self._transit_time = 0.0

    def get_anim_list(self):
        obj = self.get_obj()
        if obj:
            return obj._char_model.get_anim_names()
        else:
            return None
            return None

    def execute(self):
        obj = self.get_obj()
        if not obj._char_model:
            return
        obj.show_model()
        transit = 16 if self._transit_time > 0.0 or self._transit_time < -0.99 else 0
        obj._char_model.play_animation(self._anim, self._transit_time, transit, self._start_time, 2, self._speed_rate)

    def single_execute_update(self, time, playing=False):
        obj = self.get_obj()
        if not obj._char_model:
            return
        obj.show_model()
        delta_time = (time - self._time) * self._speed_rate
        if self._transit_time > 0.0 or self._transit_time < -0.99:
            transit = 16 if 1 else 0
            obj._char_model.play_animation(self._anim, self._transit_time, transit, self._start_time + delta_time, 2, self._speed_rate)
            playing or obj._char_model.stop_animation()

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        self._anim = get_attribute(doc_node, 'anim')
        tran = get_attribute(doc_node, 'use_transit')
        if tran == 'True':
            self._transit_time = -1.0
        else:
            try:
                self._transit_time = float(tran)
            except:
                self._transit_time = 0.0

        self._start_time = float(get_attribute(doc_node, 'start_time', '0.0'))
        self._speed_rate = float(get_attribute(doc_node, 'speed_rate', '1.0'))

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('anim', self._anim)
        doc_node.SetAttribute('use_transit', str(self._transit_time))
        doc_node.SetAttribute('start_time', '%f' % self._start_time)
        doc_node.SetAttribute('speed_rate', '%f' % self._speed_rate)

    def copy(self, event):
        EventBase.copy(self, event)
        self._anim = event._anim
        self._start_time = event._start_time
        self._speed_rate = event._speed_rate
        self._transit_time = event._transit_time


class EventCharacterWaypoint(EventPosRotInfoBase):

    def __init__(self, eid=None):
        EventPosRotInfoBase.__init__(self, eid)
        self._etype = EVENT_TYPE_CHARACTER_WAYPOINT
        self._ctrl1 = math3d.vector(0, 0, 0)
        self._ctrl2 = math3d.vector(0, 0, 0)

    def editor_init_info(self):
        obj = self.get_obj()
        if not obj or not obj._char_model:
            return
        self._pos = obj._char_model.position - datadefines.Cinematic.instance().get_offset()
        self._rot = math3d.matrix_to_rotation(obj._char_model.rotation_matrix)

    def execute(self):
        obj = self.get_obj()
        if not obj._char_model:
            return
        obj.show_model()
        obj._char_model.position = self._pos + datadefines.Cinematic.instance().get_offset()
        obj._char_model.rotation_matrix = math3d.rotation_to_matrix(self._rot)


class EventAudio(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_AUDIO
        self._do_what = 'start'

    def execute(self):
        audio = self.get_obj()._audio
        if self._do_what == 'start':
            audio.start()
        elif self._do_what == 'stop':
            audio.stop()

    def single_execute_update(self, time, playing=False):
        pass

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        self._do_what = get_attribute(doc_node, 'do_what', 'restart')

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('do_what', self._do_what)

    def copy(self, event):
        EventBase.copy(self, event)
        self._do_what = event._do_what


class EventSfx(EventPosRotScaleInfoBase):

    def __init__(self, eid=None):
        EventPosRotScaleInfoBase.__init__(self, eid)
        self._etype = EVENT_TYPE_SFX
        self._do_what = 'restart'

    def editor_init_info(self):
        obj = self.get_obj()
        if not obj or not obj._sfx:
            return
        self._pos = obj._sfx.position - datadefines.Cinematic.instance().get_offset()
        self._rot = math3d.matrix_to_rotation(obj._sfx.rotation_matrix)

    def execute(self):
        obj = self.get_obj()
        if not obj._sfx:
            return
        if self._do_what == 'restart':
            obj.show_sfx()
            obj._sfx.position = self._pos + datadefines.Cinematic.instance().get_offset()
            obj._sfx.scale = self._scale
            obj._sfx.rotation_matrix = math3d.rotation_to_matrix(self._rot)
            obj._sfx.restart()
        elif self._do_what == 'shutdown':
            obj.hide_sfx()
        elif self._do_what == 'postprocess_off':
            obj._sfx.enable_postprocess = False
        elif self._do_what == 'postprocess_on':
            obj._sfx.enable_postprocess = True

    def single_execute_update(self, time, playing=False):
        pass

    def read(self, doc_node):
        EventPosRotScaleInfoBase.read(self, doc_node)
        self._do_what = get_attribute(doc_node, 'do_what', 'restart')

    def write(self, doc_node):
        EventPosRotScaleInfoBase.write(self, doc_node)
        doc_node.SetAttribute('do_what', self._do_what)

    def copy(self, event):
        EventPosRotScaleInfoBase.copy(self, event)
        self._do_what = event._do_what


class EventSfxRate(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_SFX_RATE
        self._rate = 1.0

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        self._rate = float(get_attribute(doc_node, 'rate', '1.0'))

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('rate', str(self._rate))

    def copy(self, event):
        EventBase.copy(self, event)
        self._rate = event._rate


class EventSfxWaypoint(EventPosRotInfoBase):

    def __init__(self, eid=None):
        EventPosRotInfoBase.__init__(self, eid)
        self._etype = EVENT_TYPE_SFX_WAYPOINT
        self._ctrl1 = math3d.vector(0, 0, 0)
        self._ctrl2 = math3d.vector(0, 0, 0)

    def editor_init_info(self):
        obj = self.get_obj()
        if not obj or not obj._sfx:
            return
        self._pos = obj._sfx.position - datadefines.Cinematic.instance().get_offset()
        self._rot = math3d.matrix_to_rotation(obj._sfx.rotation_matrix)


class EventDialogue(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_DIALOGUE
        self._text = ''
        self._model_typeid = 0
        self._model_name = ''
        self._duration = 0.0

    def execute(self):
        if cinecallback.dlgwnd_callback:
            cinecallback.dlgwnd_callback(self._text, self._model_typeid, self._model_name, self._duration)

    def single_execute_update(self, time, playing=False):
        pass

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        self._text = get_attribute(doc_node, 'text')
        self._model_typeid = int(get_attribute(doc_node, 'model_typeid'))
        self._model_name = get_attribute(doc_node, 'model_name')
        self._duration = float(get_attribute(doc_node, 'duration'))

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('text', self._text)
        doc_node.SetAttribute('model_typeid', '%d' % self._model_typeid)
        doc_node.SetAttribute('model_name', self._model_name)
        doc_node.SetAttribute('duration', '%f' % self._duration)

    def copy(self, event):
        EventBase.copy(self, event)
        self._text = event._text
        self._model_typeid = event._model_typeid
        self._model_name = event._model_name
        self._duration = event._duration


class EventSubtitle(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_SUBTITLE
        self._text = ''
        self._duration = 0.0

    def execute(self):
        if cinecallback.subtitle_wnd_callback:
            cinecallback.subtitle_wnd_callback(self._text, self._duration)

    def single_execute_update(self, time, playing=False):
        pass

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        self._text = get_attribute(doc_node, 'text')
        self._duration = float(get_attribute(doc_node, 'duration'))

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('text', self._text)
        doc_node.SetAttribute('duration', '%f' % self._duration)

    def copy(self, event):
        EventBase.copy(self, event)
        self._text = event._text
        self._duration = event._duration


class EventCameraNode(EventPosRotInfoBase):

    def __init__(self, eid=None):
        EventPosRotInfoBase.__init__(self, eid)
        self._etype = EVENT_TYPE_CAMERA_TRACK_NODE
        self._fov = 45.0
        self._start_position = False
        self._scene_view_id = None
        self._ctrl1 = math3d.vector(0, 0, 0)
        self._ctrl2 = math3d.vector(0, 0, 0)
        return

    def update_time(self, time):
        obj = self.get_obj()
        obj._spline.set_node_time(self, time)

    def __repr__(self):
        return repr((self._name, self._time, self._pos, self._rot))

    def read(self, doc_node):
        EventPosRotInfoBase.read(self, doc_node)
        start = get_attribute(doc_node, 'start_pos')
        if start:
            self._start_position = True if start == 'True' else False
        if self._start_position:
            self._pos, self._rot, self._fov = datadefines.Cinematic.instance().get_old_camera_param()
        else:
            fov = get_attribute(doc_node, 'fov')
            if fov:
                self._fov = float(fov)
        if datadefines.Cinematic.instance().get_version() >= 513:
            ctrl1 = get_attribute(doc_node, 'ctrl1')
            self._ctrl1.from_string(ctrl1)
            ctrl2 = get_attribute(doc_node, 'ctrl2')
            self._ctrl2.from_string(ctrl2)

    def write(self, doc_node):
        EventPosRotInfoBase.write(self, doc_node)
        doc_node.SetAttribute('start_pos', str(self._start_position))
        doc_node.SetAttribute('fov', '%f' % self._fov)
        doc_node.SetAttribute('ctrl1', self._ctrl1.to_string())
        doc_node.SetAttribute('ctrl2', self._ctrl2.to_string())

    def copy(self, event):
        EventPosRotInfoBase.copy(self, event)
        self._fov = event._fov
        self._start_position = event._start_position
        self._ctrl1 = math3d.vector(event._ctrl1)
        self._ctrl2 = math3d.vector(event._ctrl2)


class EventCameraFocus(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_CAMERA_FOCUS
        self._focus_obj = ''
        self._focus_model_socket = ''
        self._focus_range = math.radians(10.0)
        self._focus_speed = math.radians(-1.0) / 30.0
        self._keep_up_vec = math3d.vector(0, 1, 0)
        self._focus_ratio = -1.0

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        self._focus_obj = get_attribute(doc_node, 'focus_obj')
        self._focus_model_socket = get_attribute(doc_node, 'focus_socket')
        self._focus_range = float(get_attribute(doc_node, 'focus_range'))
        self._focus_speed = float(get_attribute(doc_node, 'focus_speed'))
        self._focus_ratio = float(get_attribute(doc_node, 'focus_ratio', '-1.0'))

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('focus_obj', self._focus_obj)
        doc_node.SetAttribute('focus_socket', self._focus_model_socket)
        doc_node.SetAttribute('focus_range', str(self._focus_range))
        doc_node.SetAttribute('focus_speed', str(self._focus_speed))
        doc_node.SetAttribute('focus_ratio', str(self._focus_ratio))

    def is_end_focus(self):
        return self._focus_obj == ''

    def get_valid_focus_obj(self):
        res_obj = datadefines.Cinematic.instance().find_res_obj_by_name(self._focus_obj)
        if res_obj and res_obj._res_type == RES_TYPE_CHARACTER and res_obj._scn_idx == self.get_obj()._scn_idx:
            model_obj = res_obj.get_character()
            if model_obj.get_scene():
                return model_obj
        return None

    def _focus_speed_impl(self, focus_pos, last_rotmat, cam_pos, next_focus_event, cur_time):
        cur_focus_range = self._focus_range
        cur_focus_speed = self._focus_speed
        if next_focus_event:
            if next_focus_event._time - self._time > 0.0:
                ratio = (cur_time - self._time) / (next_focus_event._time - self._time)
                cur_focus_range = cur_focus_range * (1.0 - ratio) + next_focus_event._focus_range * ratio
                cur_focus_speed = cur_focus_speed * (1.0 - ratio) + next_focus_event._focus_speed * ratio
        cur_focus_speed *= datadefines.Cinematic.instance()._frame_time_mul
        last_forward = last_rotmat.forward
        target_forward = focus_pos - cam_pos
        cos_v = last_forward.dot(target_forward) / (last_forward.length * target_forward.length)
        angle = 0.0
        if abs(cos_v) < 1.0:
            angle = math.acos(cos_v)
        if angle < cur_focus_range:
            return last_rotmat
        a = cur_focus_speed
        if cur_focus_speed <= 0.0 or cur_focus_speed > angle:
            a = angle
        axis = last_forward.cross(target_forward)
        if axis.is_zero:
            return last_rotmat
        axis.normalize()
        rot_mat = math3d.matrix.make_rotation(axis, a)
        re = last_rotmat * rot_mat
        return math3d.matrix.make_orient(re.forward, self._keep_up_vec)

    def _focus_ratio_impl(self, focus_pos, last_rotmat, cam_pos, next_focus_event, cur_time):
        cur_ratio = self._focus_ratio
        cur_focus_range = self._focus_range
        if next_focus_event:
            if next_focus_event._time - self._time > 0.0:
                time_ratio = (cur_time - self._time) / (next_focus_event._time - self._time)
                cur_focus_range = cur_focus_range * (1.0 - time_ratio) + next_focus_event._focus_range * time_ratio
                cur_ratio = cur_ratio * (1.0 - time_ratio) + next_focus_event._focus_ratio * time_ratio
        print('ssss', cur_ratio)
        if cur_ratio <= 0.0:
            return last_rotmat
        last_forward = last_rotmat.forward
        target_forward = focus_pos - cam_pos
        cos_v = last_forward.dot(target_forward) / (last_forward.length * target_forward.length)
        angle = 0.0
        if abs(cos_v) < 1.0:
            angle = math.acos(cos_v)
        if angle < cur_focus_range:
            return last_rotmat
        print('ssadf', angle)
        a = angle * cur_ratio
        axis = last_forward.cross(target_forward)
        if axis.is_zero:
            return last_rotmat
        axis.normalize()
        rot_mat = math3d.matrix.make_rotation(axis, a)
        re = last_rotmat * rot_mat
        return math3d.matrix.make_orient(re.forward, self._keep_up_vec)

    def get_cur_rot_mat(self, last_rotmat, cam_pos, next_focus_event, cur_time):
        model_obj = self.get_valid_focus_obj()
        if model_obj:
            focus_pos = None
            if self._focus_model_socket:
                mat = model_obj.get_socket_matrix(self._focus_model_socket, world.SPACE_TYPE_WORLD)
                if mat:
                    focus_pos = mat.translation
            if not focus_pos:
                focus_pos = model_obj.world_position
            if self._focus_ratio >= 0.0:
                return self._focus_ratio_impl(focus_pos, last_rotmat, cam_pos, next_focus_event, cur_time)
            else:
                return self._focus_speed_impl(focus_pos, last_rotmat, cam_pos, next_focus_event, cur_time)

        return last_rotmat

    def get_end_cur_rot(self, last_rotmat, target_rot):
        last_rot = math3d.matrix_to_rotation(last_rotmat)
        last_forward = last_rot.get_forward()
        target_forward = target_rot.get_forward()
        cos_v = last_forward.dot(target_forward) / (last_forward.length * target_forward.length)
        angle = 0.0
        if abs(cos_v) < 1.0:
            angle = math.acos(cos_v)
        cur_focus_speed = self._focus_speed * datadefines.Cinematic.instance()._frame_time_mul
        if cur_focus_speed <= 0.0 or cur_focus_speed > angle:
            self.get_obj().remove_focus_event()
            return target_rot
        re_rot = math3d.rotation(0, 0, 0, 1)
        re_rot.slerp(last_rot, target_rot, cur_focus_speed / angle)
        return re_rot

    def execute(self):
        self.get_obj().set_focus_event(self)

    def copy(self, event):
        super(EventCameraFocus, self).copy(event)
        self._focus_obj = event._focus_obj
        self._focus_model_socket = event._focus_model_socket
        self._focus_range = event._focus_range
        self._focus_speed = event._focus_speed
        self._focus_ratio = event._focus_ratio


class EventScreenFilter(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_SCREEN_FILTER
        self._pos = math3d.vector(0.0, 0.0, 0.0)
        self._w = 0.0
        self._filter_active = True

    def execute(self):
        obj = datadefines.Cinematic.instance().find_res_obj(self._res_obj_id)
        obj.set_screen_filter_active(self._filter_active)
        if self._filter_active:
            obj.modify_screen_filter((self._pos.x, self._pos.y, self._pos.z, self._w))

    def read(self, doc_node):
        super(EventScreenFilter, self).read(doc_node)
        w = get_attribute(doc_node, 'w')
        if w:
            self._w = float(w)
        color = get_attribute(doc_node, 'v')
        if color:
            self._pos.from_string(color)
        filter_active = get_attribute(doc_node, 'filter_active')
        if filter_active:
            self._filter_active = True if filter_active == 'True' else False

    def write(self, doc_node):
        super(EventScreenFilter, self).write(doc_node)
        doc_node.SetAttribute('w', '%f' % self._w)
        doc_node.SetAttribute('v', self._pos.to_string())
        doc_node.SetAttribute('filter_active', str(self._filter_active))

    def copy(self, event):
        EventBase.copy(self, event)
        self._w = event._w
        self._pos = math3d.vector(event._pos)


class EventCameraTrack(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_CAMERA_TRACK
        self._track_name = ''

    def execute(self):
        datadefines.Cinematic.instance().set_active_track(self._track_name)

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        self._track_name = get_attribute(doc_node, 'track_name')

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('track_name', self._track_name)

    def copy(self, event):
        EventBase.copy(self, event)
        self._track_name = event._track_name


class EventSceneChange(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_SCENE_CHANGE
        self._change_scene_idx = -1

    def execute(self):
        datadefines.Cinematic.instance().change_scene(self._change_scene_idx)

    def copy(self, event):
        EventBase.copy(self, event)
        self._change_scene_idx = event._change_scene_idx

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        self._change_scene_idx = int(get_attribute(doc_node, 'scene_idx'))

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('scene_idx', str(self._change_scene_idx))


class EventFog(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_FOG
        self._scene_idx = -1
        self._fog_info = [render.RS_FOG_PIXEL, render.RS_FOG_LINEAR, 4278190080L, 400.0, 1000.0, -200.0, -40.0, -250.0, 0.9]
        if not datadefines.g_game_mode:
            self._scene_idx = datadefines.Cinematic.instance().get_cur_scn_idx()
            scn = datadefines.Cinematic.instance().get_scene_by_idx(self._scene_idx)
            fog_info = scn.get_fog()
            self._fog_info = [ i for i in fog_info ]

    def execute(self):
        scn = datadefines.Cinematic.instance().get_scene_by_idx(self._scene_idx)
        scn.set_fog(*self._fog_info)

    def copy(self, event):
        EventBase.copy(self, event)
        self._scene_idx = event._scene_idx
        for i in range(len(event._fog_info)):
            self._fog_info[i] = event._fog_info[i]

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        self._scene_idx = int(get_attribute(doc_node, 'scene_idx'))
        self._fog_info[0] = int(get_attribute(doc_node, 'fog_type'))
        self._fog_info[1] = int(get_attribute(doc_node, 'fog_mode'))
        self._fog_info[2] = int(get_attribute(doc_node, 'fog_color'))
        self._fog_info[3] = float(get_attribute(doc_node, 'fog_start'))
        self._fog_info[4] = float(get_attribute(doc_node, 'fog_end'))
        self._fog_info[5] = float(get_attribute(doc_node, 'fog_density'))
        self._fog_info[6] = float(get_attribute(doc_node, 'fog_hight_begin'))
        self._fog_info[7] = float(get_attribute(doc_node, 'fog_hight_end'))
        self._fog_info[8] = float(get_attribute(doc_node, 'fog_shader_density'))

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('scene_idx', str(self._scene_idx))
        doc_node.SetAttribute('fog_type', str(self._fog_info[0]))
        doc_node.SetAttribute('fog_mode', str(self._fog_info[1]))
        doc_node.SetAttribute('fog_color', str(self._fog_info[2]))
        doc_node.SetAttribute('fog_start', str(self._fog_info[3]))
        doc_node.SetAttribute('fog_end', str(self._fog_info[4]))
        doc_node.SetAttribute('fog_density', str(self._fog_info[5]))
        doc_node.SetAttribute('fog_hight_begin', str(self._fog_info[6]))
        doc_node.SetAttribute('fog_hight_end', str(self._fog_info[7]))
        doc_node.SetAttribute('fog_shader_density', str(self._fog_info[8]))


class EventFlashDirect(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_FLASH_DIRECT
        self._do_what = ''
        self._invoke_fun = ''
        self._params = []

    def execute(self):
        flash_movie = self.get_obj()._flash_movie
        if flash_movie:
            import flashui
            import Scaleform
            if self._do_what == 'start':
                flash_movie.get_gfx_movie().SetVisible(True)
                flash_movie.get_gfx_movie().GotoFrame(0)
                flash_movie.get_gfx_movie().SetPlayState(Scaleform.GFx.State_Playing)
            elif self._do_what == 'stop':
                flash_movie.get_gfx_movie().SetVisible(False)
                flash_movie.get_gfx_movie().SetPlayState(Scaleform.GFx.State_Stopped)
            elif self._do_what == 'invoke':
                try:
                    flash_movie.get_gfx_movie().Invoke(self._invoke_fun, tuple(self._params))
                except:
                    pass

    def single_execute_update(self, time, playing=False):
        pass

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        self._do_what = get_attribute(doc_node, 'do_what', 'start')
        if self._do_what == 'invoke':
            invoke_node = get_child_doc(doc_node, 'invoke_info')
            self._invoke_fun = get_attribute(invoke_node, 'invoke_fun', 'fun_not_found')
            params_num = int(get_attribute(invoke_node, 'num'))
            self._params = []
            if params_num > 0:
                for i in range(params_num):
                    param_i_node = get_child_doc(invoke_node, 'params_%d' % i)
                    type_name = get_attribute(param_i_node, 't', 'str')
                    value = get_attribute(param_i_node, 'v', 'nothing')
                    expression = "real_value = %s('%s')" % (type_name, value)
                    exec expression
                    self._params.append(real_value)

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('do_what', self._do_what)
        if self._do_what == 'invoke':
            invoke_node = doc_node.InsertEndChild(tinyxml.TiXmlElement('invoke_info'))
            invoke_node.SetAttribute('invoke_fun', str(self._invoke_fun))
            l = len(self._params)
            invoke_node.SetAttribute('num', str(l))
            if l > 0:
                for i in range(l):
                    param_i_node = invoke_node.InsertEndChild(tinyxml.TiXmlElement('params_%d' % i))
                    param_i_node.SetAttribute('v', str(self._params[i]))
                    str_t = str(type(self._params[i]))
                    str_t = str_t[7:-2]
                    param_i_node.SetAttribute('t', str_t)

    def copy(self, event):
        EventBase.copy(self, event)
        self._do_what = event._do_what
        self._invoke_fun = event._invoke_fun
        self._params = []
        for i in event._params:
            self._params.append(i)


class EventFlashFunction(EventFlashDirect):

    def __init__(self, eid=None):
        EventFlashDirect.__init__(self, eid)
        self._etype = EVENT_TYPE_FLASH_FUNCTION
        self._do_what = 'invoke'
        self._invoke_fun = 'StartPlay'
        self._params = ['']


class EventSpeedRate(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_SPEED_RATE
        self._speed_rate = 1.0

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        self._speed_rate = float(get_attribute(doc_node, 'speed_rate'))

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('speed_rate', str(self._speed_rate))

    def copy(self, event):
        EventBase.copy(self, event)
        self._speed_rate = event._speed_rate


class EventBuildinAction(EventBase):

    def __init__(self, eid=None):
        EventBase.__init__(self, eid)
        self._etype = EVENT_TYPE_BUILD_IN_ACTION
        self._action_name = ''
        self._action_args = []

    def read(self, doc_node):
        EventBase.read(self, doc_node)
        self._action_name = get_attribute(doc_node, 'action_name')
        self._action_args = []
        if self._action_name not in cineaction.BUILD_IN_ACTION_DICT:
            return
        action = cineaction.BUILD_IN_ACTION_DICT[self._action_name]
        args_info = action['params']
        arg_n = len(args_info)
        args_node = get_child_doc(doc_node, 'args')
        for i in range(arg_n):
            arg_i = 'arg_%d' % i
            arg_i_node = get_child_doc(args_node, arg_i)
            arg_type = args_info[i]['type']
            str_arg = get_attribute(arg_i_node, 'value')
            v = cineaction.str2value(arg_type, str_arg)
            self._action_args.append(v)

    def write(self, doc_node):
        EventBase.write(self, doc_node)
        doc_node.SetAttribute('action_name', self._action_name)
        if self._action_name not in cineaction.BUILD_IN_ACTION_DICT:
            return
        action = cineaction.BUILD_IN_ACTION_DICT[self._action_name]
        args_info = action['params']
        arg_n = len(args_info)
        args_node = doc_node.InsertEndChild(tinyxml.TiXmlElement('args'))
        for i in range(arg_n):
            arg_i = 'arg_%d' % i
            argi_node = args_node.InsertEndChild(tinyxml.TiXmlElement(arg_i))
            arg_type = args_info[i]['type']
            str_arg = cineaction.value2str(arg_type, self._action_args[i])
            argi_node.SetAttribute('value', str_arg)

    def copy(self, event):
        EventBase.copy(self, event)
        self._action_name = event._action_name
        self._action_args = []
        for arg in event._action_args:
            self._action_args.append(arg)

    def execute(self):
        cineaction.action_run(cineaction.BUILD_IN_ACTION, (self._action_name, self._action_args))