# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/barrage_utils.py
from __future__ import absolute_import
import math
import math3d
from math import pi, sin, cos, floor, atan2

def get_array_seq(t_array, idx):
    x, y, z = t_array
    xy = x * y
    z_idx = floor(idx / xy)
    xy_idx = idx - z_idx * xy
    y_idx = floor(xy_idx / y)
    x_idx = idx - z_idx * xy - y_idx * y
    return (
     x_idx, y_idx, z_idx)


def calc_array_seq(t_array, ori_seq):
    x, y, z = t_array
    x_idx, y_idx, z_idx = ori_seq
    z_fix_idx = z_idx
    x_fix_idx = x_idx - (x - 1) * 1.0 / 2
    y_fix_idx = y_idx - (y - 1) * 1.0 / 2
    return (
     x_fix_idx, y_fix_idx, z_fix_idx)


def calc_array_radian(seq):
    x, y, z = seq
    ret = atan2(y, x)
    return ret


def calc_round_seq(t_round, idx):
    r, t, z = t_round
    rt = r * t
    z_idx = floor(idx / (rt + 1))
    rt_idx = idx - (rt + 1) * z_idx
    if rt_idx == 0:
        t_idx = 0
        r_idx = 0
    else:
        t_idx = floor((rt_idx - 1) / r)
        r_idx = idx - z_idx * (rt + 1) - t_idx * r
    return (
     r_idx, t_idx, z_idx)


def calc_round_radian(seq, series):
    r, t, z = seq
    theta = 2 * pi / series
    ret = theta * t
    return ret


def get_colume_seq(t_colume, idx):
    t, c, z = t_colume
    z_idx = floor(idx / c)
    c_idx = idx - c * z_idx
    return (
     c_idx, z_idx)


def calc_colume_seq(t_colume, ori_seq):
    t, c, z = t_colume
    c_idx, z_idx = ori_seq
    c_fix_idx = c_idx - c / 2.0
    return (
     c_fix_idx, z_idx)


def calc_colume_radian(scope, count, seq):
    c, z = seq
    theta = scope * pi / 180.0 / count
    ret = theta * c
    return ret


def calc_colume_dir(ori_dir, radian):
    x, y, z = ori_dir.x, 0, ori_dir.z
    ret_x = x * cos(radian) + z * sin(radian)
    ret_y = 0
    ret_z = -x * sin(radian) + z * cos(radian)
    return math3d.vector(ret_x, ret_y, ret_z)


def get_sphere_seq(t_sphere, idx):
    theta, phi, series, size = t_sphere
    series_idx = floor(idx / size)
    size_idx = idx - size * series_idx
    return (
     series_idx, size_idx)


def calc_sphere_seq(t_sphere, ori_seq):
    theta, phi, series, size = t_sphere
    series_idx, size_idx = ori_seq
    series_fix_idx = series_idx - (series - 1) / 2.0
    size_fix_idx = size_idx - (size - 1) / 2.0
    return (
     series_fix_idx, size_fix_idx)


def calc_sphere_radian(t_sphere, seq):
    t_theta, t_phi, series, size = t_sphere
    series_idx, size_idx = seq
    per_theta = t_theta * pi / 180.0 / series
    per_phi = t_phi * pi / 180.0 / size
    theta = per_theta * series_idx
    phi = per_phi * size_idx
    return (
     theta, phi)


def calc_sphere_dir(ori_dir, up, right, theta, phi):
    mat_1 = math3d.matrix.make_rotation(up, theta)
    mat_2 = math3d.matrix.make_rotation(right, phi)
    ret = ori_dir * mat_1 * mat_2
    return ret