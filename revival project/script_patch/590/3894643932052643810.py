# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Meta/__init__.py
from __future__ import absolute_import
from sunshine.SunshineSDK.Meta.TypeMeta import OrderedProperties
from sunshine.SunshineSDK.Meta.TypeMeta import PInt, PFloat, PBool, PStr, PEnum, PVector2, PVector3, PVector4, PColor, PRes, PFile, PButton, PArray, PDict, PCustom
from sunshine.SunshineSDK.Meta.EnumMeta import DefEnum
from sunshine.SunshineSDK.Meta.ClassMetaManager import GetClassMeta, RegisterClassMeta
try:
    from PluginManager import PluginManager
    if PluginManager.hasPlugin('Montage'):
        from Montage.Backend.Transaction.TrackMeta.TrackMetaBase import GetTrackMetaCls, TSceneRootBase, TMontageRootBase, TRootBase, TFloat, TBool, EditorTrackColorType
        from Montage.Backend.Transaction.TrackMeta import TCustomCue, TCustomFloat, TrackMeta, TrackMetaBase, TResource, TColor3, updateSunshineFrameMeta, updateSunshineTrackMeta
        from Montage.Backend.Transaction.MontageProxy import MontageTrackProxy
        from I18n import translate
        from .CustomTrack import *
        from .PostProcessTrack import TPostProcess, TPostProcessRoot
except ImportError:
    from MontageSDK.Backend.Transaction.TrackMeta.TrackMetaBase import GetTrackMetaCls, TSceneRootBase, TMontageRootBase, TRootBase, TFloat, TBool, EditorTrackColorType
    from MontageSDK.Backend.Transaction.TrackMeta import TCustomCue, TCustomFloat, TrackMeta, TrackMetaBase, TResource, TColor3, updateSunshineFrameMeta, updateSunshineTrackMeta
    from MontageSDK.Backend.Transaction.MontageProxy import MontageTrackProxy
    translate = lambda x, y: y
    from .CustomTrack import *
    from .PostProcessTrack import TPostProcess, TPostProcessRoot