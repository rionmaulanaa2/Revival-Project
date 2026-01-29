# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/CameraStatePool.py
from __future__ import absolute_import
import six
import copy
from common.cfg import confmgr
from common.framework import SingletonBase
from data.camera_state_const import *
from . import CameraComponents, CameraStates

class CameraStatePool(SingletonBase):
    __slots__ = ('_cache_dict', '_component_cache_dict')
    ALIAS_NAME = 'camera_state_pool'
    CAMERA_COMPONENT_CLASS = {obj.__name__:obj for obj in six.itervalues(CameraComponents.__dict__) if getattr(obj, 'REGIST', None)}
    CAMERA_STATE_CLASS = {obj.TYPE:obj for obj in six.itervalues(CameraStates.__dict__) if getattr(obj, 'TYPE', None) and hasattr(obj, 'COMS')}
    OBSERVE_CAMERA_STATE_CLASS = {}

    def init(self):
        self._cache_dict = {}
        self._component_cache_dict = {}

    def clear(self):
        for camera_state in six.itervalues(self._cache_dict):
            camera_state.destroy()

        self._cache_dict.clear()
        for camera_component in six.itervalues(self._component_cache_dict):
            camera_component.destroy()

        self._component_cache_dict.clear()
        CameraStatePool.OBSERVE_CAMERA_STATE_CLASS.clear()

    def get_cam_state_class(self, camera_state_type):
        camera_state_class = CameraStatePool.CAMERA_STATE_CLASS.get(camera_state_type, None)
        if not camera_state_class:
            camera_state_type = str(camera_state_type)
            coms = copy.copy(confmgr.get('c_camera_setting', camera_state_type, default={}).get('lComs', []))
            type_dict = {'OBSERVE': False,'TYPE': camera_state_type,'COMS': coms}
            camera_state_class = type('CameraState_' + camera_state_type, (CameraStates.CameraState,), type_dict)
            CameraStatePool.CAMERA_STATE_CLASS[camera_state_type] = camera_state_class
        return camera_state_class

    def get_observe_cam_state_class(self, camera_state_type):
        observe_cam_state_class = CameraStatePool.OBSERVE_CAMERA_STATE_CLASS.get(camera_state_type, None)
        if not observe_cam_state_class:
            camera_state_type = str(camera_state_type)
            cam_state_class = self.get_cam_state_class(camera_state_type)
            coms = copy.copy(cam_state_class.COMS)
            coms.append('ObserveCameraCom')
            type_dict = {'OBSERVE': True,'TYPE': camera_state_type,'COMS': coms}
            observe_cam_state_class = type('Observe_' + cam_state_class.__name__, (cam_state_class,), type_dict)
            CameraStatePool.OBSERVE_CAMERA_STATE_CLASS[camera_state_type] = observe_cam_state_class
        return observe_cam_state_class

    def create_camera_state(self, camera_state_type, is_observe, cam_ctrl, **kwargs):
        cache_key = (
         camera_state_type, is_observe)
        camera_state = self._cache_dict.pop(cache_key, None)
        if camera_state or is_observe:
            com_state_class = self.get_observe_cam_state_class if 1 else self.get_cam_state_class
            camera_state = com_state_class(camera_state_type)(cam_ctrl, **kwargs)
        else:
            camera_state.reuse(cam_ctrl, **kwargs)
        return camera_state

    def destroy_camera_state(self, camera_state):
        cache_key = (
         camera_state.TYPE, camera_state.OBSERVE)
        if global_data.enable_camera_state_cache and cache_key not in self._cache_dict:
            self._cache_dict[cache_key] = camera_state
            camera_state.cache()
        else:
            camera_state.destroy()

    def create_camera_component(self, camera_state, camera_component_name):
        camera_component = self._component_cache_dict.pop(camera_component_name, None)
        if not camera_component:
            camera_component_class = CameraStatePool.CAMERA_COMPONENT_CLASS[camera_component_name]
            camera_component = camera_component_class(camera_state)
        else:
            camera_component.reuse(camera_state)
        return camera_component

    def destroy_camera_component(self, camera_component):
        camera_component_name = camera_component.__class__.__name__
        if global_data.enable_camera_state_cache and camera_component_name not in self._component_cache_dict:
            self._component_cache_dict[camera_component_name] = camera_component
            camera_component.cache()
        else:
            camera_component.destroy()