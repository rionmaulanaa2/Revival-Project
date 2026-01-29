# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Lib/MontCueHandler.py
from __future__ import absolute_import
import json
from .. import _Instances
from .. import Consts

class MontageCueHandler(object):

    def Handle(self, trigger, cueinput, ent=None, cuetype=None):
        raise NotImplementedError


class CustomFloatHandler(MontageCueHandler):

    def __init__(self):
        super(CustomFloatHandler, self).__init__()

    def Handle(self, trigger, cueinput, ent=None, cuetype=None):
        cuedata = json.loads(cueinput)
        datatype = cuedata['DataType']
        if _Instances.TickManager is not None:
            _Instances.TickManager.registerValueToTick(datatype, cuedata)
        return


Handlers = {Consts.MONTAGE_CUSTOMFLOAT_CUEID: CustomFloatHandler()
   }

def registerCueHandler(cueId, cueHandler):
    global Handlers
    if isinstance(cueId, list):
        for cue in cueId:
            registerCueHandler(cue, cueHandler)

    else:
        if cueId in Handlers:
            _Instances.Interface.PrintFunc('CueId already exist, cannot register!')
            return
        Handlers[cueId] = cueHandler


def signalNotifyCallback(trigger, cuetype, cueinput, ent=None):
    if cuetype in Handlers:
        Handlers[cuetype].Handle(trigger, cueinput, ent, cuetype)