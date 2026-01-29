# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LAvatar.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component
from ext_package.ext_decorator import ext_role_use_org_skin

@component(share=('ComStatusHuman', 'ComHealth', 'ComShield', 'ComBackpackData', 'ComSpd',
                  'ComBuffData', 'ComAtAim', 'ComAttachHolder'), client=(
 'ComAttributeClient',
 'ComAddFactorClient',
 'ComDataRenderRotate',
 'ComDataAppearance',
 'ComDataCommonMotor',
 'ComDataAnimator',
 'ComDataLogicTransform',
 'ComDataLogicLod',
 'ComDataAimIK',
 'com_human_effect.ComHumanEffectMgr',
 'com_character_ctrl.ComHumanStateData',
 'ComWeaponBarClient',
 'ComMessage',
 'ComClientSynchronizer',
 'ComAvatarEvent2GlobalEvent',
 'ComController',
 'ComSelector',
 'ComSelectionHuman',
 'ComHumanCollison',
 'ComCtrlVehicle',
 'ComCtrlTVMissileLogic',
 'ComWeaponController',
 'ComGunShieldLogic',
 'com_parachute.ComParachuteDriver',
 'com_parachute.ComParachuteState',
 'com_parachute.ComParachuteFollow',
 'com_hit_hint.ComHitHintHuman',
 'com_human_logic.ComOpenAimHelper',
 'ComHumanHurtAppearance',
 'ComTrajectoryAppearance',
 'ComShortcut',
 'ComPlayerAI',
 'ComSound',
 'ComThrowableDriver',
 'ComExplosiveContainerClient',
 'ComAgony',
 'ComItemUseClient',
 'ComGroup',
 'ComCamp',
 'ComMaterialStatus',
 'ComAimHelper',
 'ComMap',
 'ComSpectate',
 'ComAgentCapsule',
 'ComBuffClient',
 'ComWaterHuman',
 'ComWeaponEffectHuman',
 'ComCamSyncSender',
 'ComOB',
 'ComCrash',
 'com_global_sync.ComPlayerGlobalReceiver',
 'com_global_sync.ComPlayerGlobalSender',
 'ComBulletScreen',
 'ComQTELocalBattleGuide',
 'ComLocalBattleGuide',
 'ComRemoteBattleGuide',
 'ComDeathBattleGuide',
 'ComSpecialBattleGuide',
 'ComNewbieThirdGuide',
 'ComNewbieFourGuide',
 'ComAttachClient',
 'com_parachute.ComFreeDropCam',
 'ComRunCam',
 'ComCtrlMecha',
 'ComSkillClient',
 'ComSpeedUp',
 'com_camera.ComCameraTarget',
 'ComMoveForce',
 'ComNotice',
 'ComMechaModule',
 'ComBackpackClient',
 'ComFlagUI',
 'ComHumanMarkView',
 'com_character_ctrl.ComSpringAnim',
 ('ComFirepower', 'need_fire_power'),
 'ComEmoji',
 'ComEnv',
 'ComEnvDetect',
 'ComBondGift',
 'ComDetectScene',
 'ComExerciseField',
 'ComModeMgr',
 'ComMoveShadow',
 ('com_granbelm.ComGranbelmRuneClient', 'need_granbelm_rune'),
 'ComMoveSyncClient',
 ('ComSignal', 'need_signal'),
 'ComMoveSyncAnimRateSender',
 'ComHitJudge',
 'ComRogueGift',
 'ComIsland',
 'ComOuterShield',
 'ComHairLogic',
 'ComAntiCheat',
 'ComMeowCoin',
 'ComHunterCoin',
 'ComIntimacy',
 'ComRescue',
 'ComPrivilege',
 'com_concert.ComHumanConcert',
 ('ComFallReturnClient', 'fall_return_left_times'),
 ('ComAICollectLog', 'need_aicollectlog'),
 'ComArmorClient',
 ('pve.ComPveSetting', 'need_pve_com'),
 ('pve.ComPveBless', 'need_pve_com'),
 ('pve.ComPveMechaBreakthrough', 'need_pve_com'),
 ('pve.ComCrystalStone', 'need_pve_com'),
 ('pve.ComPveCoin', 'need_pve_com'),
 ('pve.ComPveStory', 'need_pve_com'),
 ('pve.ComPveItemSet', 'need_pve_com'),
 ('pve.ComPveGainEffectShow', 'need_pve_com'),
 ('pve.ComPveMechaReset', 'need_pve_com')))
class LAvatar(Unit):
    MASK = 0

    @ext_role_use_org_skin
    def init_from_dict(self, bdict):
        self.sd.ref_is_avatar = True
        bdict['enable_sync'] = True
        bdict['is_avatar'] = True
        super(LAvatar, self).init_from_dict(bdict)
        if not global_data.last_bat_disconnect_time:
            self.send_event('E_CHECK_ROTATION_INIT_EVENT')
        global_data.player_sd = self.share_data

    def destroy(self):
        global_data.emgr.player_destroy_event.emit()
        global_data.mecha = None
        global_data.player_sd = None
        super(LAvatar, self).destroy()
        return