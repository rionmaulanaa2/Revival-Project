# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Backend/Transaction/TrackMeta/__init__.py
from .TrackMetaBase import TrackMetaBase, TCustomFloat, TCustomCue, TFloat, TTransform, TResource, TBool, TInt, TStr, TCamTransform, TrackMeta, TVectorBase, TColor3, TVector3, TColor4, TVector4
from sunshine.SunshineSDK.Meta.TypeMeta import ClassMeta, PDict, PVector2, PVector3, PVector4
from sunshine.SunshineSDK.Meta.ClassMetaManager import RegisterClassMeta

def updateSunshineTrackMeta(meta, properties):
    className = meta.getTrackClassMetaName(meta.attrs['trackName'])

    class CustomMeta(ClassMeta):
        MontageMeta = True
        CLASS_NAME = className
        PROPERTIES = properties

    RegisterClassMeta(CustomMeta())


def updateSunshineFrameMeta(meta, properties):
    className = meta.getFrameClassMetaName(meta.attrs['trackName'])

    class CustomMeta(ClassMeta):
        MontageMeta = True
        CLASS_NAME = className
        PROPERTIES = properties

    RegisterClassMeta(CustomMeta())