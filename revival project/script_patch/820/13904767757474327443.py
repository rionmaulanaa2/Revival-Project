# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LSeat.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component

@component(share=[
 'ComEventForward'], client=[
 'ComAttributeClient',
 'ComAddFactorClient',
 'ComDataRenderRotate',
 'ComDataAnimator',
 'ComDataLogicTransform',
 'ComDataAppearance',
 'ComDataCommonMotor',
 'ComSeatClient',
 'com_character_ctrl.ComAnimMgr',
 'com_character_ctrl.ComBehavior',
 'com_character_ctrl.ComStateData',
 'ComStatusSeatClient',
 'ComMechaWeaponBarClient',
 'ComAvatarEvent2GlobalEvent',
 'ComClientSynchronizer',
 'ComController',
 'ComMechaAtkGun',
 'ComMechaRecoil',
 'ComHumanHurtAppearance',
 'ComTrajectoryAppearance',
 'ComControlLeaveAOI',
 'ComInterpolater',
 'ComMechaSound',
 'ComMoveSyncAnimRateSender'])
class LSeat(Unit):

    def init_from_dict(self, bdict):
        super(LSeat, self).init_from_dict(bdict)

    def destroy(self):
        self.send_event('E_ON_LOGIC_DESTROY')
        super(LSeat, self).destroy()