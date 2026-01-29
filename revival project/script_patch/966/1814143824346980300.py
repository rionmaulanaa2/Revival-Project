# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LPuppetRobot.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component
import logic.gcommon.const as const
from ext_package.ext_decorator import ext_role_use_org_skin

@component(share=('ComStatusHuman', 'ComHealth', 'ComShield', 'ComBackpackData', 'ComSpd',
                  'ComBuffData', 'ComAtAim', 'ComAttachHolder'), client=('ComAttributeClient',
                                                                         'ComAddFactorClient',
                                                                         'ComDataRenderRotate',
                                                                         'ComDataAppearance',
                                                                         'ComDataCommonMotor',
                                                                         'ComDataAnimator',
                                                                         'ComDataLogicTransform',
                                                                         'ComDataLogicLod',
                                                                         'com_human_effect.ComHumanEffectMgr',
                                                                         'com_character_ctrl.ComHumanStateData',
                                                                         'ComWeaponBarClient',
                                                                         'ComAvatarEvent2GlobalEvent',
                                                                         'ComAIAgentHuman',
                                                                         'com_human_logic.ComRemoteControlHuman',
                                                                         'com_ai_ctrl.ComRemoteRobotMove',
                                                                         'ComSyncAIClient',
                                                                         'ComClientSynchronizer',
                                                                         'ComController',
                                                                         'ComHumanCollison',
                                                                         'ComCtrlVehicle',
                                                                         'ComCtrlTVMissileLogic',
                                                                         'ComSelector',
                                                                         'ComSelectionHuman',
                                                                         'ComHumanHurtAppearance',
                                                                         'ComTrajectoryAppearance',
                                                                         'ComSound',
                                                                         'ComAgony',
                                                                         'ComInterpolater',
                                                                         'ComGroup',
                                                                         'ComCamp',
                                                                         'ComShieldBloodSimUI',
                                                                         'ComMaterialStatus',
                                                                         'ComThrowableDriver',
                                                                         'ComWeaponController',
                                                                         'ComGunShieldLogic',
                                                                         'ComHumanBloodUI',
                                                                         'ComCamSyncReceiver',
                                                                         'ComCrash',
                                                                         'ComBuffClient',
                                                                         'ComWeaponEffectHuman',
                                                                         'com_parachute.ComParachuteState',
                                                                         'ComParachuteDriverGhost',
                                                                         'ComAIHelper',
                                                                         'ComAttachClient',
                                                                         'ComCtrlMecha',
                                                                         'ComSpeedUp',
                                                                         'ComSkillClient',
                                                                         'com_hit_hint.ComHitHintHuman',
                                                                         'ComMoveForce',
                                                                         'ComFlagUI',
                                                                         'ComHumanMarkView',
                                                                         'ComAIDebugUI',
                                                                         'ComMechaModule',
                                                                         'ComMoveShadow',
                                                                         'ComMoveSyncClient',
                                                                         'ComWaterHuman',
                                                                         'ComOuterShield',
                                                                         'ComHairLogic',
                                                                         'ComEmoji',
                                                                         'ComEnv',
                                                                         'ComArmorClient'))
class LPuppetRobot(Unit):

    def init_from_dict(self, bdict):
        self.sd.ref_is_avatar = False
        bdict['enable_sync'] = False
        super(LPuppetRobot, self).init_from_dict(bdict)
        self.send_event('S_YAW_WITH_CAM', 0)

    def is_robot(self):
        return True

    def on_init_complete(self):
        super(LPuppetRobot, self).on_init_complete()
        global_data.agent_robot = self.get_owner()

    def destroy(self, *args, **kwargs):
        global_data.emgr.puppet_destroy_event.emit(self.id)
        super(LPuppetRobot, self).destroy()