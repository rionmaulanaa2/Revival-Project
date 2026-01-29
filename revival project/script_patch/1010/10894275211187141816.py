# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/Utils/Matrix.py
from __future__ import absolute_import
from six.moves import range
from math import cos, sin, acos, asin, atan2, sqrt, degrees, radians

class MatrixBase(object):

    def mul(self, matrix_rhs):
        raise NotImplementedError

    def createfromDegrees(self, roll_pitch_yaw):
        raise NotImplementedError

    def createfromRadians(self, roll_pitch_yaw):
        raise NotImplementedError

    def inverse(self):
        raise NotImplementedError

    def rotation(self):
        raise NotImplementedError

    def translate(self):
        raise NotImplementedError

    def setTranslate(self, translate):
        raise NotImplementedError

    def scale(self):
        raise NotImplementedError

    def setScale(self, scale):
        raise NotImplementedError

    def roll(self):
        raise NotImplementedError

    def yaw(self):
        raise NotImplementedError

    def pitch(self):
        raise NotImplementedError

    def roll_radian(self):
        raise NotImplementedError

    def yaw_radian(self):
        raise NotImplementedError

    def pitch_radian(self):
        raise NotImplementedError


class UniMatrix(MatrixBase):

    def __init__(self):
        self.matrix_ = [
         [
          1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]

    def mul(self, matrix_rhs):
        m = UniMatrix()
        m.matrix_[0][0], m.matrix_[1][1], m.matrix_[2][2], m.matrix_[3][3] = (0.0,
                                                                              0.0,
                                                                              0.0,
                                                                              0.0)
        for idxr in range(0, 4):
            for idxc in range(0, 4):
                for idx in range(0, 4):
                    m.matrix_[idxr][idxc] += self.matrix_[idxr][idx] * matrix_rhs.matrix_[idx][idxc]

        return m

    def createfromDegrees(self, roll_pitch_yaw):
        matrix = UniMatrix()
        roll, pitch, yaw = [ radians(d) for d in roll_pitch_yaw ]
        cos_yaw = cos(yaw)
        cos_roll = cos(roll)
        cos_pitch = cos(pitch)
        sin_yaw = sin(yaw)
        sin_roll = sin(roll)
        sin_pitch = sin(pitch)
        matrix.matrix_[0][0] = cos_yaw * cos_roll + sin_roll * sin_pitch * sin_yaw
        matrix.matrix_[1][0] = cos_roll * sin_yaw * sin_pitch - cos_yaw * sin_roll
        matrix.matrix_[2][0] = cos_pitch * sin_yaw
        matrix.matrix_[0][1] = cos_pitch * sin_roll
        matrix.matrix_[1][1] = cos_pitch * cos_roll
        matrix.matrix_[2][1] = -1 * sin_pitch
        matrix.matrix_[0][2] = cos_yaw * sin_pitch * sin_roll - sin_yaw * cos_roll
        matrix.matrix_[1][2] = sin_yaw * sin_roll + cos_yaw * cos_roll * sin_pitch
        matrix.matrix_[2][2] = cos_yaw * cos_pitch
        self.matrix_ = matrix.matrix_

    def createfromRadians(self, roll_pitch_yaw):
        matrix_roll = UniMatrix()
        matrix_pitch = UniMatrix()
        matrix_yaw = UniMatrix()
        costheta = cos(roll_pitch_yaw[0])
        sintheta = sin(roll_pitch_yaw[0])
        matrix_roll.matrix_[0][0] = costheta
        matrix_roll.matrix_[0][1] = sintheta
        matrix_roll.matrix_[1][0] = -sintheta
        matrix_roll.matrix_[1][1] = costheta
        matrix_roll.matrix_[2][2] = 1
        costheta = cos(roll_pitch_yaw[1])
        sintheta = sin(roll_pitch_yaw[1])
        matrix_pitch.matrix_[0][0] = 1
        matrix_pitch.matrix_[1][1] = costheta
        matrix_pitch.matrix_[1][2] = sintheta
        matrix_pitch.matrix_[2][1] = -sintheta
        matrix_pitch.matrix_[2][2] = costheta
        costheta = cos(roll_pitch_yaw[2])
        sintheta = sin(roll_pitch_yaw[2])
        matrix_yaw.matrix_[0][0] = costheta
        matrix_yaw.matrix_[0][2] = -sintheta
        matrix_yaw.matrix_[1][1] = 1
        matrix_yaw.matrix_[2][0] = sintheta
        matrix_yaw.matrix_[2][2] = costheta
        matrix = matrix_roll.mul(matrix_pitch.mul(matrix_yaw))
        self.matrix_ = matrix.matrix_

    def inverse(self):
        invMatrix = UniMatrix()
        m00, m01, m02, m03 = (self.matrix_[0][0], self.matrix_[0][1], self.matrix_[0][2], self.matrix_[0][3])
        m10, m11, m12, m13 = (self.matrix_[1][0], self.matrix_[1][1], self.matrix_[1][2], self.matrix_[1][3])
        m20, m21, m22, m23 = (self.matrix_[2][0], self.matrix_[2][1], self.matrix_[2][2], self.matrix_[2][3])
        m30, m31, m32, m33 = (self.matrix_[3][0], self.matrix_[3][1], self.matrix_[3][2], self.matrix_[3][3])
        det = 0
        det += m00 * (m11 * m22 - m12 * m21)
        det -= m01 * (m10 * m22 - m12 * m20)
        det += m02 * (m10 * m21 - m11 * m20)
        if det == 0:
            return invMatrix
        rcp = 1 / det
        invMatrix.matrix_[0][0] = rcp * (m11 * m22 - m12 * m21)
        invMatrix.matrix_[0][1] = -rcp * (m01 * m22 - m02 * m21)
        invMatrix.matrix_[0][2] = rcp * (m01 * m12 - m02 * m11)
        invMatrix.matrix_[1][0] = -rcp * (m10 * m22 - m12 * m20)
        invMatrix.matrix_[1][1] = rcp * (m00 * m22 - m02 * m20)
        invMatrix.matrix_[1][2] = -rcp * (m00 * m12 - m02 * m10)
        invMatrix.matrix_[2][0] = rcp * (m10 * m21 - m11 * m20)
        invMatrix.matrix_[2][1] = -rcp * (m00 * m21 - m01 * m20)
        invMatrix.matrix_[2][2] = rcp * (m00 * m11 - m01 * m10)
        invMatrix.matrix_[3][0] = -(m30 * invMatrix.matrix_[0][0] + m31 * invMatrix.matrix_[1][0] + m32 * invMatrix.matrix_[2][0])
        invMatrix.matrix_[3][1] = -(m30 * invMatrix.matrix_[0][1] + m31 * invMatrix.matrix_[1][1] + m32 * invMatrix.matrix_[2][1])
        invMatrix.matrix_[3][2] = -(m30 * invMatrix.matrix_[0][2] + m31 * invMatrix.matrix_[1][2] + m32 * invMatrix.matrix_[2][2])
        return invMatrix

    def rotation(self):
        r = []
        for idx in range(0, 3):
            l = self.matrix_
            r.append(l[idx][0:3])

        return r

    def setRotation(self, rotation):
        for idxr in range(0, 3):
            for idxc in range(0, 3):
                self.matrix_[idxr][idxc] = rotation[idxr][idxc]

    def translate(self):
        return self.matrix_[3][0:3]

    def setTranslate(self, translate):
        for idx in range(0, 3):
            self.matrix_[3][idx] = translate[idx]

    def scale(self):
        m = self.matrix_
        scale = []
        for i in range(0, 3):
            len = sqrt(m[i][0] * m[i][0] + m[i][1] * m[i][1] + m[i][2] * m[i][2])
            scale.append(len)

        return scale

    def setScale(self, scale):
        m = self.matrix_
        for i in range(0, 3):
            len = sqrt(m[i][0] * m[i][0] + m[i][1] * m[i][1] + m[i][2] * m[i][2])
            for j in range(0, 3):
                m[i][j] = m[i][j] / len * scale[i]

    def normalize(self, line):
        acc = 0.0
        for ele in line:
            acc += ele ** 2

        acc = sqrt(acc)
        ret = []
        for ele in line:
            ret.append(ele / acc)

        return ret

    def roll(self):
        rotation = self.rotation()
        r0 = rotation[0]
        r2 = rotation[2]
        r0 = self.normalize(r0)
        r2 = self.normalize(r2)
        zdirxzlen = sqrt(r2[2] ** 2 + r2[0] ** 2)
        if zdirxzlen == 0.0:
            return 0.0
        else:
            acarg = (r2[2] * r0[0] - r2[0] * r0[2]) / zdirxzlen
            if acarg > 1.0:
                return 0.0
            if acarg <= -1:
                return 180.0
            roll = degrees(acos(acarg))
            if r0[1] < 0:
                return -roll
            return roll

    def yaw(self):
        rotation = self.rotation()
        r2 = rotation[2]
        r2 = self.normalize(r2)
        return degrees(atan2(r2[0], r2[2]))

    def pitch(self):
        r2 = self.rotation()[2]
        r2 = self.normalize(r2)
        return degrees(-asin(r2[1]))

    def roll_radian(self):
        rotation = self.rotation()
        r0 = rotation[0]
        r2 = rotation[2]
        r0 = self.normalize(r0)
        r2 = self.normalize(r2)
        zdirxzlen = sqrt(r2[2] ** 2 + r2[0] ** 2)
        if zdirxzlen == 0.0:
            return 0.0
        else:
            acarg = (r2[2] * r0[0] - r2[0] * r0[2]) / zdirxzlen
            if acarg > 1.0:
                return 0.0
            if acarg <= -1:
                return 3.1415926
            roll = acos(acarg)
            if r0[1] < 0:
                return -roll
            return roll

    def yaw_radian(self):
        rotation = self.rotation()
        r2 = rotation[2]
        r2 = self.normalize(r2)
        return atan2(r2[0], r2[2])

    def pitch_radian(self):
        r2 = self.rotation()[2]
        r2 = self.normalize(r2)
        return -asin(r2[1])


_RegisteredMatrix = UniMatrix

class Matrix(object):

    def __new__(cls, *args, **kwargs):
        global _RegisteredMatrix
        return _RegisteredMatrix()


def RegisterMatrix(matrixCls):
    global _RegisteredMatrix
    if issubclass(matrixCls, MatrixBase):
        _RegisteredMatrix = matrixCls