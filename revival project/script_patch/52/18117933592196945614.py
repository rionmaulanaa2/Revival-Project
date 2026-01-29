# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Backend/Model/MontageModel.py
from .MontageTrack import MontageTrack
DEFAULT_FPS = 30

class MontageModel(MontageTrack):

    def __init__(self, uuid=None):
        super(MontageModel, self).__init__(uuid)
        self.engine = -1
        self.FPS = DEFAULT_FPS
        self.properties['name'] = 'root'

    def serialize(self):
        data = super(MontageModel, self).serialize()
        data['engine'] = self.engine
        data['FPS'] = self.FPS
        return data

    def deserialize(self, data):
        super(MontageModel, self).deserialize(data)
        self.engine = data['engine']
        if 'FPS' in data:
            self.FPS = data['FPS']

    def removeModel(self, uuid):
        pass

    @staticmethod
    def reParent(track, parentTrack):
        if not isinstance(track, MontageTrack) or not isinstance(parentTrack, MontageTrack):
            return False
        else:
            if track.parent() == parentTrack:
                return True
            if track == parentTrack:
                return False
            if track.hasDescent(parentTrack):
                return False
            if track.parent() is not None:
                track.parent().delChild(track.uuid)
            success = parentTrack.addChild(track)
            return success

    @staticmethod
    def changeRow(track, srcRow, desRow):
        temp = track.children.pop(srcRow)
        if desRow > srcRow:
            desRow -= 1
        track.children.insert(desRow, temp)

    def clear(self):
        super(MontageModel, self).clear()
        self.properties = {'name': 'root'}