# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/__init__.py
from __future__ import absolute_import
RuntimeInitiated = False
TickManager = None
Interface = None
Castmanager = None
ExtendPlugin = None
PluginReady = False
Montage = None
CurvePathManager = None
PreviewManager = None
ResManager = None
Initiated = False
NoSetCineData = False
from .Consts import *

class Instances(object):

    @property
    def RuntimeInitiated(self):
        global RuntimeInitiated
        return RuntimeInitiated

    @RuntimeInitiated.setter
    def RuntimeInitiated(self, runtimeInitiated):
        global RuntimeInitiated
        RuntimeInitiated = runtimeInitiated

    @property
    def TickManager(self):
        global TickManager
        return TickManager

    @TickManager.setter
    def TickManager(self, tickManager):
        global TickManager
        TickManager = tickManager

    @property
    def Interface(self):
        global Interface
        return Interface

    @Interface.setter
    def Interface(self, interface):
        global Interface
        Interface = interface

    @property
    def Castmanager(self):
        global Castmanager
        return Castmanager

    @Castmanager.setter
    def Castmanager(self, castmanager):
        global Castmanager
        Castmanager = castmanager

    @property
    def PluginReady(self):
        global PluginReady
        return PluginReady

    @PluginReady.setter
    def PluginReady(self, pluginReady):
        global PluginReady
        PluginReady = pluginReady

    @property
    def ExtendPlugin(self):
        global ExtendPlugin
        return ExtendPlugin

    @ExtendPlugin.setter
    def ExtendPlugin(self, extendPlugin):
        global ExtendPlugin
        ExtendPlugin = extendPlugin

    @property
    def Montage(self):
        global Montage
        return Montage

    @Montage.setter
    def Montage(self, montage):
        global Montage
        Montage = montage

    @property
    def PreviewManager(self):
        global PreviewManager
        return PreviewManager

    @PreviewManager.setter
    def PreviewManager(self, previewManager):
        global PreviewManager
        PreviewManager = previewManager

    @property
    def ResManager(self):
        global ResManager
        return ResManager

    @ResManager.setter
    def ResManager(self, resManager):
        global ResManager
        ResManager = resManager

    @property
    def Initiated(self):
        global Initiated
        return Initiated

    @Initiated.setter
    def Initiated(self, initiated):
        global Initiated
        Initiated = initiated


_Instances = Instances()