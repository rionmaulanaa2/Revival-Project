# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/TrackImp/DollyTrack.py
from __future__ import absolute_import
from six.moves import range
from UniCineDriver.Movie.MovieObject import MovieGroupCls, MovieTrackCls
from UniCineDriver.Movie.MovieActionKeyframe import MovieActionKeyframe
from .UniGameInterface import set_cur_camera_params
from MontageSDK.Backend.utils.Formula import cubicSplineInterpolation
from MontageSDK.Backend.utils.Matrix import Matrix
import math3d

@MovieTrackCls('DollyTrack')
class UDollyTrack(MovieActionKeyframe):

    def __init__(self, model, parent_movie_group):
        super(UDollyTrack, self).__init__(model, parent_movie_group)
        self.wayPoints = model.properties.get('wayPoints', [])
        self.previewCamera = model.parent.parent.properties.get('previewCamera', None)
        self.m_parentMovieGroup().blackBoard.setdefault('cameramap', {})[str(self.name)] = self
        self.transform = None
        self.customData = {}
        return

    def update(self, n_cur_time, n_interval_time, force=False):
        super(UDollyTrack, self).update(n_cur_time, n_interval_time, force=False)
        if self.m_parentMovieGroup().blackBoard['_targetCamera'] == self.name and len(self.wayPoints) > 0:
            progress = self.m_parentMovieGroup().customData.get('DollyTrack', 0)
            cameraTrans = self._calcCameraTrans(progress)
            m = Matrix()
            m.createfromDegrees(cameraTrans[3:])
            m.setTranslate(cameraTrans[:3])
            self.transform = m

    def _calcCameraTrans(self, progress):
        isec = int(progress)
        ratio = progress - isec
        isec = min(isec, len(self.wayPoints) - 1)
        if isec >= len(self.wayPoints) - 1:
            point = self.wayPoints[-1]
            return [
             point['X'], point['Y'], point['Z'], point['Roll'], point['Pitch'], point['Yaw']]
        xPoints, yPoints, zPoints = [], [], []
        rollPoints, pitchPoints, yawPoints = [], [], []
        for i in range(len(self.wayPoints)):
            xPoints.append([i, self.wayPoints[i]['X']])
            yPoints.append([i, self.wayPoints[i]['Y']])
            zPoints.append([i, self.wayPoints[i]['Z']])
            rollPoints.append([i, self.wayPoints[i]['Roll']])
            pitchPoints.append([i, self.wayPoints[i]['Pitch']])
            yawPoints.append([i, self.wayPoints[i]['Yaw']])

        paramx = cubicSplineInterpolation(xPoints, 0, 0)
        paramy = cubicSplineInterpolation(yPoints, 0, 0)
        paramz = cubicSplineInterpolation(zPoints, 0, 0)
        paramroll = cubicSplineInterpolation(rollPoints, 0, 0)
        parampitch = cubicSplineInterpolation(pitchPoints, 0, 0)
        paramyaw = cubicSplineInterpolation(yawPoints, 0, 0)
        paramx, paramy, paramz = paramx[isec], paramy[isec], paramz[isec]
        paramroll, parampitch, paramyaw = paramroll[isec], parampitch[isec], paramyaw[isec]
        x = paramx[0] * ratio ** 3 + paramx[1] * ratio ** 2 + paramx[2] * ratio + paramx[3]
        y = paramy[0] * ratio ** 3 + paramy[1] * ratio ** 2 + paramy[2] * ratio + paramy[3]
        z = paramz[0] * ratio ** 3 + paramz[1] * ratio ** 2 + paramz[2] * ratio + paramz[3]
        roll = paramroll[0] * ratio ** 3 + paramroll[1] * ratio ** 2 + paramroll[2] * ratio + paramroll[3]
        pitch = parampitch[0] * ratio ** 3 + parampitch[1] * ratio ** 2 + parampitch[2] * ratio + parampitch[3]
        yaw = paramyaw[0] * ratio ** 3 + paramyaw[1] * ratio ** 2 + paramyaw[2] * ratio + paramyaw[3]
        return [
         x, y, z, roll, pitch, yaw]