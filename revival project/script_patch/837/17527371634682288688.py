# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/Movie/MovieActionSpan.py
from __future__ import absolute_import
from .MovieAction import MovieAction

class MovieActionSpan(MovieAction):
    ACTION_TYPE = 'Span'

    def __init__(self, model, parent_movie_group):
        super(MovieActionSpan, self).__init__(model, parent_movie_group)
        self.m_nTimeStart = 0
        self.m_nTimeEnd = 0
        self.m_nOverlapTime = 0
        self.m_bHasStarted = False
        self._curspans = []

    @property
    def length(self):
        return self.m_nTimeEnd - self.m_nTimeStart

    def update_when_pausing(self):
        pass

    def onSpanFrameEnter(self, frame):
        pass

    def onSpanFrameLeave(self, frame):
        pass

    def goto(self, n_cur_time, n_interval_time):
        lastspan = self._curspans[0] if self._curspans else None
        trigger = self.update(n_cur_time, n_interval_time)
        if trigger is None:
            trigger = not self.m_parentMovieGroup().blackBoard.get('_pause')
        curspan = self._curspans[0] if self._curspans else None
        if trigger is False and curspan != lastspan:
            if lastspan:
                self.onSpanFrameLeave(lastspan)
            if curspan:
                self.onSpanFrameEnter(curspan)
        return

    def update(self, n_cur_time, n_interval_time, force=False):
        super(MovieActionSpan, self).update(n_cur_time, n_interval_time, force=force)
        trigger = not self.m_parentMovieGroup().blackBoard.get('_pause')
        self._maintainCurrentSpans(n_cur_time, trigger=trigger)
        self.outputCustomData()
        return trigger

    def _maintainCurrentSpans(self, n_cur_time, trigger=True):
        lastspans = set(self._curspans)
        self._curspans = self.currentSpan(n_cur_time)
        if trigger:
            curspans = set(self._curspans)
            toleave = lastspans.difference(curspans)
            toadd = curspans.difference(lastspans)
            for frame in toleave:
                self.onSpanFrameLeave(frame)

            for frame in toadd:
                self.onSpanFrameEnter(frame)

    def outputCustomData(self):
        if len(self._curspans) == 0:
            return
        curspan = self._curspans[0]
        parent = self.m_parentMovieGroup()
        for k, v in curspan.properties.items():
            parent.setCustomData(self._pathname.split('/') + [k], v)

    def on_end(self):
        super(MovieActionSpan, self).on_end()
        for frame in self._curspans:
            self.onSpanFrameLeave(frame)

        self._curspans = []

    def currentSpan(self, curTime):
        spans = []
        for frame in self.frames:
            if frame.time <= curTime < frame.endtime:
                spans.append(frame)

        return spans

    def is_in_range(self, n_cur_time):
        curspan = self.currentSpan(n_cur_time)
        return len(curspan) > 0

    def is_started(self):
        return self.m_bHasStarted

    def change_disabled(self, status):
        super(MovieActionSpan, self).change_disabled(status)
        if status:
            for span in self._curspans:
                self.onSpanFrameLeave(span)

        self._curspans = []
        if not status:
            self._maintainCurrentSpans(self.m_parentMovieGroup().blackBoard['_lasttime'])