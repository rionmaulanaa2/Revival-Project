# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/TrackImp/LightingTracks.py
from __future__ import absolute_import
import math3d
import world
from . import UniHelper
from UniCineDriver.Movie.MovieActionKeyframe import MovieActionTriggerKeyframe
from .EntityBase import UEntityBase
from UniCineDriver.Movie.MovieObject import MovieGroupCls, MovieTrackCls
import MontageSDK
PROPERTY_HANDLERS = {}

class PropertyHandler(object):

    def __init__(self, propertyName):
        self.propertyName = propertyName

    def __call__(self, func):
        PROPERTY_HANDLERS[self.propertyName] = func
        return func


class LightTrack(UEntityBase):

    def __init__(self, data, blackboard):
        super(LightTrack, self).__init__(data, blackboard)
        self.hidden = False
        self.m_light = None
        return

    @property
    def model(self):
        return self.light

    @property
    def light(self):
        if self.m_light and self.m_light.valid:
            return self.m_light

    def afterinit(self):
        model = super(LightTrack, self).afterinit()
        if model:
            self.m_light = model
        if self.m_light is None:
            self.m_light = self.createLight()
        self.afterEditorInit()
        return

    def applyCustomData(self, data):
        super(LightTrack, self).applyCustomData(data)
        if self.light:
            for propertyName, setFunc in PROPERTY_HANDLERS.items():
                if hasattr(self, setFunc.__name__):
                    boundFunc = getattr(self, setFunc.__name__)
                    if propertyName in data:
                        boundFunc(data[propertyName])
                    else:
                        boundFunc()

    def goto(self, n_cur_time, n_interval_time):
        super(LightTrack, self).goto(n_cur_time, n_interval_time)
        if 'Transform' in self.customData:
            self.updateEntityTransform()

    def update(self, n_cur_time, n_interval_time, force=False):
        super(LightTrack, self).update(n_cur_time, n_interval_time, force=force)
        if n_interval_time != 0 or force:
            if 'Transform' in self.customData:
                self.updateEntityTransform()

    def clear_data(self):
        ret = super(LightTrack, self).clear_data()
        if not ret and self.m_light:
            self.m_light.destroy()
        self.m_light = None
        return

    def updateEntityTransform(self):
        if self.light:
            self.light.position = math3d.vector(*self.transform.translate())
            self.light.scale = math3d.vector(*self.transform.scale())
            v3_rot = math3d.vector(self.transform.pitch(), self.transform.yaw(), self.transform.roll())
            m4_rotation = UniHelper.euler_angle_to_rotation_matrix(v3_rot)
            self.light.world_rotation_matrix = m4_rotation

    @PropertyHandler('Intensity')
    def setIntensity(self, intensity=5.0):
        self.light.intensity = intensity

    @PropertyHandler('Range')
    def setRange(self, range=5.0):
        self.light.range = range

    @PropertyHandler('Color')
    def setColor(self, color={}):
        self.light.color = self.formatColor(color)

    def setHidden(self, hidden):
        self.hidden = hidden
        self.updateEnable()

    def formatColor(self, color):
        return (
         color.get('R', 0), color.get('G', 0), color.get('B', 0))

    def createLight(self):
        pass

    def updateEnable(self):
        if self.light:
            self.light.enable = not self.hidden


@MovieGroupCls('PointLight')
class PointLightTrack(LightTrack):

    def __init__(self, data, blackboard):
        super(PointLightTrack, self).__init__(data, blackboard)

    def createLight(self):
        return UniHelper.get_active_scene().create_light(world.LIGHT_TYPE_POINT)


@MovieGroupCls('DirectionLight')
class DirectionLightTrack(LightTrack):

    def createLight(self):
        return UniHelper.get_active_scene().create_light(world.LIGHT_TYPE_DIRECTION)

    def updateEntityTransform(self):
        if self.light:
            self.light.position = math3d.vector(*self.transform.translate())
            self.light.scale = math3d.vector(*self.transform.scale())
            v3_rot = math3d.vector(self.transform.pitch(), self.transform.yaw(), self.transform.roll())
            m4_rotation = UniHelper.euler_angle_to_rotation_matrix(v3_rot)
            self.light.world_rotation_matrix = m4_rotation


@MovieGroupCls('SpotLight')
class SpotLightTrack(DirectionLightTrack):

    def createLight(self):
        return UniHelper.get_active_scene().create_light(world.LIGHT_TYPE_SPOT)

    @PropertyHandler('InnerAngle')
    def setInnerAngle(self, innerAngle=60.0):
        self.light.inner_angle = innerAngle

    @PropertyHandler('OutAngle')
    def setOuterAngle(self, outerAngle=90.0):
        self.light.outer_angle = outerAngle


@MovieGroupCls('RectLight')
class RectLightTrack(LightTrack):

    def createLight(self):
        return UniHelper.get_active_scene().create_light(world.LIGHT_TYPE_RECT)

    @PropertyHandler('Height')
    def setHeight(self, height=10.0):
        self.light.rect_height = height

    @PropertyHandler('Width')
    def setWidth(self, width=10.0):
        self.light.rect_width = width


@MovieTrackCls('Hidden', 'PointLight')
@MovieTrackCls('Hidden', 'SpotLight')
class LightTrackHidden(MovieActionTriggerKeyframe):

    def __init__(self, model, parent_movie_group):
        super(LightTrackHidden, self).__init__(model, parent_movie_group)
        self._needUpdate = False
        self.lastData = False

    def trigger(self, data):
        self.lastData = self.m_parentMovieGroup().hidden
        self.m_parentMovieGroup().setHidden(data['value'])

    def reset(self):
        self.m_parentMovieGroup().setHidden(self.lastData)