# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/Movie/MovieActionKeyframe.py
from __future__ import absolute_import
from .MovieAction import MovieAction
from ..Utils.Formula import binarySearchLeft, InterpValueCachedt

def getInterpValue(dt3, dt2, dt, x1, x2, y1, y2, curveparams, nextcurveparams):
    rmode = nextcurveparams.get('leftTangentMode', 1)
    lmode = curveparams.get('rightTangentMode', 1)
    atan = nextcurveparams.get('arriveTan', 0)
    ltan = curveparams.get('leaveTan', 0)
    value = InterpValueCachedt(dt3, dt2, dt, x1, y1, x2, y2, lmode, rmode, ltan, atan)
    return value


class MovieActionKeyframe(MovieAction):
    ACTION_TYPE = 'Key'

    def update(self, n_cur_time, n_interval_time, force=False):
        self.calculate_keyframe(n_cur_time)
        super(MovieActionKeyframe, self).update(n_cur_time, n_interval_time, force=force)

    def calculate_keyframe(self, nCurTime):
        if len(self.frames) == 0:
            value = self.properties.get('default', 0)
        else:
            index = binarySearchLeft(self.frames, nCurTime, lambda x: x.time)
            keyframe = self.frames[max(index - 1, 0)]
            nextkeyframe = self.frames[min(index, len(self.frames) - 1)]
            x1 = keyframe.time
            x2 = nextkeyframe.time
            dt = nCurTime - x1
            dt2 = dt * dt
            dt3 = dt2 * dt
            y1 = keyframe.properties['value']
            y2 = nextkeyframe.properties['value']
            curveparams = keyframe.properties
            nextcurveparams = nextkeyframe.properties
            value = getInterpValue(dt3, dt2, dt, x1, x2, y1, y2, curveparams, nextcurveparams)
        self.m_parentMovieGroup().setCustomData(self._pathname.split('/'), value)


class MovieActionTriggerKeyframe(MovieAction):
    ACTION_TYPE = 'Key'

    def __init__(self, model, parent_movie_group):
        super(MovieActionTriggerKeyframe, self).__init__(model, parent_movie_group)
        self.m_nCurNodeIndex = -1

    def reset(self):
        pass

    def stop_playing(self):
        super(MovieActionTriggerKeyframe, self).stop_playing()
        self.m_nCurNodeIndex = 0

    def update(self, n_cur_time, n_interval_time, force=False):
        CurNodeIndex = binarySearchLeft(self.frames, n_cur_time, lambda x: x.time) - 1
        if CurNodeIndex != self.m_nCurNodeIndex:
            self.m_nCurNodeIndex = CurNodeIndex
            if self.m_nCurNodeIndex < 0:
                self.reset()
            elif self.m_nCurNodeIndex < len(self.frames):
                node = self.frames[self.m_nCurNodeIndex]
                self.trigger(node.properties)

    def trigger(self, data):
        pass