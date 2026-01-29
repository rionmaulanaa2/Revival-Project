# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LMechaTrans.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component

@component(share=[
 'ComSeats',
 'ComBuffData',
 'ComVehicleData'], client=[
 'ComAttributeClient',
 'ComAddFactorClient',
 'ComDataRenderRotate',
 'ComDataAnimator',
 'ComDataLogicTransform',
 'ComDataAppearance',
 'ComDataCommonMotor',
 'ComDataLogicLod',
 'com_mechatran_appearance.ComMechaTranAppearance',
 'com_character_ctrl.ComAnimMgr',
 'com_character_ctrl.ComBehavior',
 'com_character_ctrl.ComStateData',
 'com_mecha_effect.ComMechaEffectMgr',
 'ComStatusMechaClient',
 'ComHealthMecha',
 'ComMechaWeaponBarClient',
 'com_mechatran_appearance.ComPatternTrans',
 'com_mecha_appearance.ComLodMecha',
 'ComAvatarEvent2GlobalEvent',
 'ComClientSynchronizer',
 'ComController',
 'ComSelectionMechaTrans',
 'ComMechaAtkGun',
 'ComMechaRecoil',
 'ComHumanHurtAppearance',
 'ComTrajectoryAppearance',
 'ComVehiclePhysics',
 'ComVehicleShootCollision',
 'ComControlLeaveAOI',
 'ComPositionChecker',
 'ComInterpolater',
 'ComMechaSound',
 'com_mechatran_appearance.ComMechaTransEffect',
 'ComMessage',
 'ComExplosiveContainerClient',
 'com_hit_hint.ComHitHintMecha',
 'com_camera.ComCameraTarget',
 'ComWaterMechaTrans',
 'ComMoveSyncAnimRateSender',
 'ComCamp',
 'ComMaterialStatus',
 'ComFlagUI',
 'ComMechaMarkView',
 'ComSpeedUp',
 'ComBuffClient',
 'ComMechaActivateClient',
 'ComEmoji',
 'ComEnv',
 'ComThrowableDriver',
 'ComSkillClient',
 'ComFlagUI',
 'ComMechaFuelClient',
 'ComMoveSyncClient',
 'ComHitJudge'])
class LMechaTrans(Unit):

    def init_from_dict(self, bdict):
        super(LMechaTrans, self).init_from_dict(bdict)

    def destroy(self):
        self.send_event('E_ON_LOGIC_DESTROY')
        super(LMechaTrans, self).destroy()