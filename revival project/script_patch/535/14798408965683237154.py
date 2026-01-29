# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Backend/Model/MontageTrack.py
import weakref
from ..utils.Formula import binarySearchLeft
from .ModelBase import MontageModelBase
from .MontageFrame import MontageFrame

class MontageTrack(MontageModelBase):

    def __init__(self, uuid=None):
        super(MontageTrack, self).__init__(uuid)
        self.children = []
        self.frames = []

    def serialize(self):
        data = super(MontageTrack, self).serialize()
        data['children'] = [ t.serialize() for t in self.children ]
        data['frames'] = [ f.serialize() for f in self.frames ]
        return data

    def deserialize(self, data):
        super(MontageTrack, self).deserialize(data)
        for t in data['children']:
            track = MontageTrack(uuid=t.get('uuid'))
            track.deserialize(t)
            self.addChild(track)

        for f in data['frames']:
            frame = self.createFrame(uuid=f.get('uuid'))
            frame.deserialize(f)

        self.frames.sort(key=lambda k: k.time)

    def clear(self):
        super(MontageTrack, self).clear()
        del self.children[:]
        del self.frames[:]

    def addChild(self, track):
        if track.parent is not None and track.parent() != self:
            return False
        else:
            track.parent = weakref.ref(self)
            self.children.append(track)
            return True

    def delChild(self, uuid):
        for i, t in enumerate(self.children):
            if t.uuid == uuid:
                t.parent = None
                self.children.pop(i)
                return True

        return False

    def hasDescent(self, track):
        if track in self.children:
            return True
        for t in self.children:
            if t.hasDescent(track):
                return True

        return False

    def createFrame(self, uuid=None):
        f = MontageFrame(uuid)
        f.parent = weakref.ref(self)
        self.frames.append(f)
        return f

    def removeFrame(self, uuid):
        for i, f in enumerate(self.frames):
            if f.uuid == uuid:
                f.parent = None
                self.frames.pop(i)
                return True

        return False

    def findModel(self, uuid):
        if uuid == self.uuid:
            return self
        else:
            for track in self.children:
                m = track.findModel(uuid)
                if m is not None:
                    return m

            for frame in self.frames:
                if frame.uuid == uuid:
                    return frame

            return

    def updateFramesSeq(self, frame):
        self.frames.remove(frame)
        index = binarySearchLeft(self.frames, frame.time, lambda f: f.time)
        self.frames.insert(index, frame)