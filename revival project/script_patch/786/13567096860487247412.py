# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/Utils/Const.py
CurveColor = [
 '#FF0000',
 '#FFA500',
 '#FFD700',
 '#FFFF00',
 '#008000',
 '#0000FF',
 '#00FFFF',
 '#1E90FF',
 '#9400D3',
 '#EE82EE',
 '#FF00FF',
 '#FF1493',
 '#DC143C',
 '#708090',
 '#D2B48C',
 '#CD853F',
 '#4B0082']

class TangentMode(object):
    Auto = 1
    FreeSmooth = 2
    Flat = 4 | FreeSmooth
    Broken = 8
    Free = 1024
    Linear = 2048
    Constant = 4096
    Weighted = 8192
    CoLinearModes = Auto | FreeSmooth | Flat
    CoLinearModeList = (Auto, FreeSmooth, Flat)
    BrokenModes = Free | Linear | Constant
    BrokenModeList = (Free, Linear, Constant)


class InterpolateMode(object):
    Constant = 0
    Linear = 1
    CubicSpline = 2