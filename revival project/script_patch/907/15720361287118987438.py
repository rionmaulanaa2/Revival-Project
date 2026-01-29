# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/Movie/DirectorGroup/MovieActionShot.py
from ..MovieObject import MovieTrackCls
from ..MovieActionSpan import MovieActionSpan

@MovieTrackCls('Shot')
class ShotKeySpan(MovieActionSpan):

    def __init__(self, model, parent_movie_group):
        super(ShotKeySpan, self).__init__(model, parent_movie_group)
        self.needGoto = False
        self.playrateUpdated = False
        self.currentCamName = ''
        self.currentSceneTime = 0
        self.currentPlayRate = 1
        self.currentSceneInterval = 0
        self._lastspan = None
        self.m_parentMovieGroup().blackBoard['_Shot'] = self
        self.cameraChange = False
        return

    def updateCurrentSceneTime(self, n_cur_time):
        curspan = self._lastspan
        curprop = curspan.properties
        dt = n_cur_time - curspan.time
        newtime = curprop['scenestart'] + dt * curprop['sceneduration'] / curspan.duration
        self.currentSceneInterval = newtime - self.currentSceneTime
        self.currentSceneTime = newtime

    def update(self, n_cur_time, n_interval_time, force=False):
        super(ShotKeySpan, self).update(n_cur_time, n_interval_time, force=force)
        curspan = self._curspans[0]
        if self._lastspan is not curspan:
            if curspan.duration == 0:
                return
            if self._lastspan:
                if self._lastspan.properties['scenestart'] + self._lastspan.properties['sceneduration'] != curspan.properties['scenestart']:
                    self.needGoto = True
            newplayrate = curspan.properties['sceneduration'] / curspan.duration
            if newplayrate != self.currentPlayRate:
                self.currentPlayRate = newplayrate
                self.playrateUpdated = True
            self._lastspan = curspan
        else:
            self.needGoto = False
            self.playrateUpdated = False
        if self.currentCamName != str(curspan.properties['name']):
            self.cameraChange = True
        else:
            self.cameraChange = False
        self.currentCamName = str(curspan.properties['name'])
        self.updateCurrentSceneTime(n_cur_time)

    def loadFromModel(self, model):
        super(ShotKeySpan, self).loadFromModel(model)
        montFPS = self.m_parentMovieGroup().blackBoard['_montFPS']
        for frame in self.frames:
            frame_prop = frame.properties
            frame_prop['scenestart'] = round(frame_prop['scenestart'] * montFPS, 3)
            frame_prop['sceneduration'] = round(frame_prop['sceneduration'] * montFPS, 3)