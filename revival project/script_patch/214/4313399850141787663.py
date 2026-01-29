# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/Movie/Keyframe.py
from __future__ import absolute_import
import weakref
from copy import deepcopy
from .MovieObject import MovieObject

class Keyframe(MovieObject):

    def __init__(self, model, parent_movie_action):
        super(Keyframe, self).__init__()
        self.parentMovieAction = weakref.ref(parent_movie_action)
        self.montFPS = self.parentMovieAction().m_parentMovieGroup().blackBoard['_montFPS']
        self.uuid = model.uuid
        self._time = model._time
        self._duration = model.duration
        self.properties = deepcopy(model.properties)

    @property
    def time(self):
        return self._time * self.montFPS

    @property
    def duration(self):
        return self._duration * self.montFPS

    @property
    def endtime(self):
        return self.time + self.duration

    def Type(self):
        return 'Keyframe'

    @property
    def type(self):
        return 'Keyframe'