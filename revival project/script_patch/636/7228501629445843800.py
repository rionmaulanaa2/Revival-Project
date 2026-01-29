# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Backend/utils/DOFConverter.py
import math

class DOFCalc(object):

    def __init__(self, calcFunc):
        self.calcFunc = calcFunc

    def __get__(self, instance, owner=None):
        value = instance.__dict__[self.calcFunc.__name__] = self.calcFunc(instance)
        return value


class DOFConverter(object):
    c = 0.035

    def __init__(self, focalLength, focalDis, aperture):
        self.focalLength = focalLength
        self.focalDis = focalDis
        self.aperture = aperture
        self._dn = None
        self._df = None
        return

    @property
    def _DN(self):
        if self._dn is not None:
            return self._dn
        else:
            f = self.focalLength
            s = self.focalDis * 1000
            N = self.aperture
            div = f ** 2 - self.c * N * f + self.c * N * s
            if div == 0:
                return 999999
            if div < 0:
                return 0
            self._dn = s * f ** 2 / div
            return self._dn

    @property
    def _DF(self):
        if self._df is not None:
            return self._df
        else:
            f = self.focalLength
            s = self.focalDis * 1000
            N = self.aperture
            div = f ** 2 + self.c * N * f - self.c * N * s
            if div == 0:
                return 999999
            if div < 0:
                return 999999
            self._df = s * f ** 2 / div
            return self._df

    @DOFCalc
    def Fov(self):
        if self.focalDis <= 0:
            return 42.968
        return 180 / math.pi * 2 * math.atan(12 / self.focalLength)

    @DOFCalc
    def FocalDistance(self):
        return self._DN * 0.001

    @DOFCalc
    def FocalRegion(self):
        return (self._DF - self._DN) * 0.001

    @DOFCalc
    def NearTransitionRegion(self):
        return max(0.5, self._DN * 0.0005)

    @DOFCalc
    def FarTransitionRegion(self):
        return 5

    @DOFCalc
    def Blurriness(self):
        if self.aperture < 0:
            self.aperture = 0
        blur = -math.sqrt(0.1 * self.aperture) + 1.2
        if blur < 0:
            return 0
        return blur