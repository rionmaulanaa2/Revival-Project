# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Backend/Model/MontageFrame.py
import weakref
from .ModelBase import MontageModelBase, TIMETICK_PER_SEC

def align2Time(time, FPS=30):
    tick = int(time * TIMETICK_PER_SEC)
    FRAME_TICK_LENGTH = TIMETICK_PER_SEC / FPS
    alignTick = round(float(tick) / FRAME_TICK_LENGTH) * FRAME_TICK_LENGTH
    alignTime = alignTick / TIMETICK_PER_SEC
    return alignTime


class MontageFrame(MontageModelBase):

    def __init__(self, uuid=None):
        super(MontageFrame, self).__init__(uuid)
        self._time = 0
        self._duration = 0
        self.linkedFrameUuid = None
        self._root = None
        return

    def serialize(self):
        data = super(MontageFrame, self).serialize()
        data['time'] = self._time
        data['duration'] = self._duration
        data['linkedFrameUuid'] = self.linkedFrameUuid
        return data

    def deserialize(self, data):
        super(MontageFrame, self).deserialize(data)
        self._time = round(data.get('time'), 3)
        self._duration = round(data.get('duration'), 3)
        self.linkedFrameUuid = data.get('linkedFrameUuid', None)
        return

    @property
    def root(self):
        if not self._root:
            curr = self.parent()
            while curr.parent():
                curr = curr.parent()

            self._root = weakref.ref(curr)
        return self._root

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = round(value, 3)
        self.parent().updateFramesSeq(self)

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = round(value, 3)