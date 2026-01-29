# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/Movie/MovieGroupEntityBase.py
from ..Utils.Matrix import Matrix
from .MovieGroup import MovieGroup

class MovieGroupEntityBase(MovieGroup):

    def __init__(self, data, blackboard):
        super(MovieGroupEntityBase, self).__init__(data, blackboard)
        self.transform = None
        self.localTransform = Matrix()
        self.parentTransform = Matrix()
        return

    def calcTransform(self, data):
        m = Matrix()
        if 'Rotation' in data:
            m.createfromDegrees((data['Rotation'].get('Roll', 0), data['Rotation'].get('Pitch', 0), data['Rotation'].get('Yaw', 0)))
        if 'Scale' in data:
            m.setScale((data['Scale'].get('X', 1), data['Scale'].get('Y', 1), data['Scale'].get('Z', 1)))
        if 'Translation' in data:
            m.setTranslate((data['Translation'].get('X', 0), data['Translation'].get('Y', 0), data['Translation'].get('Z', 0)))
        self.localTransform = m
        if self.parentTransform is not None:
            self.transform = self.localTransform.mul(self.parentTransform)
        else:
            self.transform = self.localTransform
        return

    def applyCustomData(self, data):
        super(MovieGroupEntityBase, self).applyCustomData(data)
        if 'Transform' in data:
            self.calcTransform(data['Transform'])
        for group in self.chilrenGroups:
            if isinstance(group, MovieGroupEntityBase):
                group.parentTransform = self.transform