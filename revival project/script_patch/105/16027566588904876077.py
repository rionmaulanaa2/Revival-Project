# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/Movie/MovieAction.py
from __future__ import absolute_import
from .MovieObject import MovieObject
from .Keyframe import Keyframe
import weakref
from copy import deepcopy
CustomTrackcls = {}

def CustomTrack(tracktype):

    def wrapper(cls):
        CustomTrackcls[tracktype] = cls
        return cls

    return wrapper


class MovieAction(MovieObject):
    KeyframeCls = Keyframe
    ACTION_TYPE = ''
    ORDER = 100

    def __init__(self, model, parent_movie_group):
        super(MovieAction, self).__init__()
        self._pathname = ''
        self.m_parentMovieGroup = weakref.ref(parent_movie_group)
        self.frames = []
        self.m_bHasStarted = False
        self.loadFromModel(model)
        self.name = self.properties.get('name', '')

    def updatePlayRate(self, rate):
        pass

    def loadFromModel(self, model):
        self.properties = deepcopy(model.properties)
        self.uuid = model.uuid
        for frame in model.frames:
            f = self.KeyframeCls(frame, self)
            self.frames.append(f)

    @property
    def type(self):
        return ''

    def update(self, n_cur_time, n_interval_time, force=False):
        if not self.m_bHasStarted:
            self.on_enter()

    def on_enter(self):
        self.m_bHasStarted = True

    def on_end(self):
        self.m_bHasStarted = False

    def goto(self, n_cur_time, n_interval_time):
        self.update(n_cur_time, n_interval_time)

    def cancel_goto(self, n_cur_time):
        pass

    def pause(self, flag):
        pass

    def stop_playing(self):
        self.m_bHasStarted = False

    def change_disabled(self, status):
        self.properties['disabled'] = status

    def DeleteFrameByUuid(self, uuid):
        for frame in self.frames:
            if frame.uuid == uuid:
                self.frames.remove(frame)
                return True

        return False

    def SetFrameValue(self, uuid, key, value):
        for frame in self.frames:
            if frame.uuid == uuid:
                if key == 'time':
                    frame._time = value
                elif key == 'duration':
                    frame._duration = value
                else:
                    frame.properties[key] = value
                return True

        return False

    def AddFrameByModel(self, model):
        frameAction = self.KeyframeCls(model, self)
        self.frames.append(frameAction)
        self.frames.sort(key=lambda k: k.time)

    def SetProperty(self, key, value):
        self.properties[key] = value

    def clear_data(self):
        self.m_parentMovieGroup().tracks.remove(self)
        if self in self.m_parentMovieGroup().runningAction:
            self.m_parentMovieGroup().runningAction.remove(self)