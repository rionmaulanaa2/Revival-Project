# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LMecha.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component

@component(share=[
 'ComSeats',
 'ComBuffData',
 'ComShield'], client=[
 'ComAttributeClient',
 'ComAddFactorClient',
 'ComDataRenderRotate',
 'ComDataAnimator',
 'ComDataAppearance',
 'ComDataCommonMotor',
 'ComDataLogicTransform',
 'ComDataLogicLod',
 'ComDataAimIK',
 'ComDataLogicMovementFullFps',
 'ComMechaModel',
 'com_character_ctrl.ComAnimMgr',
 'com_character_ctrl.ComInput',
 'com_character_ctrl.ComBehavior',
 'com_character_ctrl.ComStateData',
 'ComMoveSyncAnimRateSender',
 'com_mecha_effect.ComMechaEffectMgr',
 'ComMechaFootIK',
 'ComHumanHurtAppearance',
 'ComTrajectoryAppearance',
 'ComStatusMechaClient',
 'ComHealthMecha',
 'ComMechaWeaponBarClient',
 'ComClientSynchronizer',
 'ComAvatarEvent2GlobalEvent',
 'ComMechaCollison',
 'ComMechaStaticCollision',
 'ComBuffClient',
 'ComMechaInjureClient',
 'ComCamp',
 'ComMaterialStatus',
 'ComMechaAtkGun',
 'ComThrowableDriver',
 'ComMechaRecoil',
 'ComMechaSound',
 'ComMechaRepair',
 'ComMechaActivateClient',
 'ComControlLeaveAOI',
 'ComSkillClient',
 'ComMechaShieldCollision',
 'ComMechaBloodUI',
 'ComStateSimui',
 'ComExplosiveContainerClient',
 'ComMechaAimHelper',
 'ComWaterMecha',
 'ComAimLockedUI',
 'com_camera.ComCameraTarget',
 'com_hit_hint.ComHitHintMecha',
 'com_camera.ComCamClipAni',
 'ComCamSyncSender',
 'ComParabolaTrackAppearance',
 'ComMoveForce',
 'ComHitFlag',
 'com_mecha_appearance.ComHitFlagAppearance',
 'ComJumpTrack',
 'ComMessage',
 'ComFlagUI',
 'ComMechaMarkView',
 'ComSpeedUp',
 'ComMechaFuelClient',
 'ComMechaSkillFuelClient',
 'ComOuterShield',
 'ComSelectionMecha',
 'ComEmoji',
 'ComEnv',
 'ComModeMgr',
 'com_character_ctrl.ComSpringAnim',
 'ComMoveSyncClient',
 'ComSpectateSyncClient',
 'ComMechaModuleBuff',
 'ComHitJudge',
 'ComAICollectLogMecha',
 'ComHeatMagazine',
 'ComMechaBlind'])
class LMecha(Unit):

    def init_from_dict(self, bdict):
        import game3d
        bdict['model_sync_priority'] = game3d.ASYNC_ULTIMATE_HIGH
        super(LMecha, self).init_from_dict(bdict)

    def destroy(self):
        self.send_event('E_ON_LOGIC_DESTROY')
        super(LMecha, self).destroy()