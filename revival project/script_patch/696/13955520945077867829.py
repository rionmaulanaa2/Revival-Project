# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Backend/Transaction/MontageEvents.py
from .. import PrintFunc

class MontageEvent(object):
    OP_ADD = 'ADD'
    OP_DEL = 'DEL'
    OP_MOD = 'MOD'

    def __init__(self, op, senderuuid, propertydir, oldvalue, newvalue):
        super(MontageEvent, self).__init__()
        self.op = op
        self.propertyDir = propertydir
        self.proxyuuid = senderuuid
        self.senderuuid = senderuuid
        self.oldvalue = oldvalue
        self.newvalue = newvalue
        self.handled = False

    def prefixedCopy(self, prefix):
        event = MontageEvent(self.op, self.senderuuid, self.propertyDir, self.oldvalue, self.newvalue)
        event.handled = self.handled
        event.propertyDir.insert(0, prefix)
        return event

    def printLog(self, srcsystem):
        PrintFunc('%s %s %s %s %s %s %s' % (srcsystem, self.op, self.proxyuuid[:4], self.senderuuid[:4], str(self.propertyDir), str(self.oldvalue), str(self.newvalue)))