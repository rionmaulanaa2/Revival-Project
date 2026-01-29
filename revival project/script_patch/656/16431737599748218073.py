# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LMechaRobot.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component

@component(share=[
 'ComSeats',
 'ComBuffData',
 'ComShield'], client=[
 'ComAddFactorClient',
 'ComAttributeClient',
 'ComDataRenderRotate',
 'ComDataAppearance',
 'ComDataAnimator',
 'ComDataCommonMotor',
 'ComDataLogicTransform',
 'ComDataLogicLod',
 'ComMechaModel',
 'com_mecha_effect.ComMechaEffectMgr',
 'com_character_ctrl.ComBehavior',
 'com_character_ctrl.ComAnimMgr',
 'com_character_ctrl.ComInput',
 'com_character_ctrl.ComStateData',
 'ComAIAgent',
 'ComSyncAIClient',
 'com_ai_ctrl.ComRemoteMechaMove',
 'ComClientSynchronizer',
 'ComTrajectoryAppearance',
 'ComStatusMechaClient',
 'ComHealthMecha',
 'ComSelectionMecha',
 'ComMechaWeaponBarClient',
 'ComMechaCollison',
 'ComBuffClient',
 'ComMechaInjureClient',
 'ComCamp',
 'ComMaterialStatus',
 'ComMechaAtkGun',
 'ComHumanHurtAppearance',
 'ComMechaBloodUI',
 'ComStateSimui',
 'ComMechaRecoil',
 'ComMechaActivateClient',
 'ComControlLeaveAOI',
 'ComSkillClient',
 'ComThrowableDriver',
 'ComMechaShieldCollision',
 'ComExplosiveContainerClient',
 'com_hit_hint.ComHitHintMecha',
 'ComHitFlag',
 'com_mecha_appearance.ComHitFlagAppearance',
 'ComFlagUI',
 'ComMechaMarkView',
 'ComCamp',
 'ComSpeedUp',
 'ComOuterShield',
 'ComMechaSound',
 'ComAgony',
 'ComMechaFuelClient',
 'ComAIDebugUI',
 'ComAIHelper',
 'ComMoveShadow',
 'ComEmoji',
 'ComMechaBlind'])
class LMechaRobot(Unit):

    def init_from_dict(self, bdict):
        super(LMechaRobot, self).init_from_dict(bdict)

    def is_mecha(self):
        return True

    def on_init_complete(self):
        super(LMechaRobot, self).on_init_complete()
        global_data.agent_mecha = self.get_owner()

    def destroy(self):
        self.send_event('E_ON_LOGIC_DESTROY')
        super(LMechaRobot, self).destroy()