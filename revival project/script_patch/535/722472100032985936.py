# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LPuppet.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component
from common.cfg import confmgr
from logic.gcommon.common_utils.battle_utils import is_battle_signal_open

@component(share=('ComStatusHuman', 'ComHealth', 'ComShield', 'ComBackpackData', 'ComBuffData',
                  'ComAtAim', 'ComAttachHolder'), client=(
 'ComAttributeClient',
 'ComAddFactorClient',
 'ComDataRenderRotate',
 'ComDataAppearance',
 'ComDataCommonMotor',
 'ComDataAnimator',
 'ComDataLogicTransform',
 'ComDataLogicLod',
 'ComDataLogicMovementFullFps',
 'com_human_effect.ComHumanEffectMgr',
 'com_character_ctrl.ComHumanStateData',
 'ComWeaponBarClient',
 'ComAvatarEvent2GlobalEvent',
 'ComClientSynchronizer',
 'ComController',
 'ComHumanCollison',
 'ComCtrlVehicle',
 'ComCtrlTVMissileLogic',
 'ComSelector',
 'ComSelectionHuman',
 'ComHumanHurtAppearance',
 'ComTrajectoryAppearance',
 'ComShortcut',
 'ComSound',
 'ComShieldBloodSimUI',
 'ComAgony',
 'ComInterpolater',
 'ComGroup',
 'ComCamp',
 'ComMaterialStatus',
 'ComMap',
 'ComThrowableDriver',
 'ComWeaponController',
 'ComGunShieldLogic',
 'ComHumanBloodUI',
 'ComCamSyncReceiver',
 'ComCrash',
 'ComBuffClient',
 'ComWeaponEffectHuman',
 'com_parachute.ComParachuteState',
 'com_parachute.ComParachuteFollow',
 'ComParachuteDriverGhost',
 'ComAgentCapsuleGhost',
 'ComCtrlMecha',
 'ComSpeedUp',
 'ComSkillClient',
 'ComObserve',
 'com_camera.ComCameraTarget',
 'com_hit_hint.ComHitHintHuman',
 'ComMoveForce',
 'ComMechaModule',
 'ComFlagUI',
 'ComHumanMarkView',
 'ComPuppetSpectated',
 'ComEmoji',
 'ComEnv',
 'ComModeMgr',
 ('com_granbelm.ComGranbelmRuneClient', 'need_granbelm_rune'),
 'ComMoveSyncClient',
 ('ComSignal', 'need_signal'),
 'ComIsland',
 'ComOuterShield',
 'ComRogueGift',
 'ComHairLogic',
 ('ComFallReturnClient', 'fall_return_left_times'),
 'ComArmorClient',
 'ComHunterCoin',
 ('pve.ComPveBless', 'need_pve_com'),
 ('pve.ComCrystalStone', 'need_pve_com'),
 ('pve.ComPveCoin', 'need_pve_com'),
 ('pve.ComPveGainEffectShow', 'need_pve_com')))
class LPuppet(Unit):
    MASK = 0

    def init_from_dict(self, bdict):
        self.sd.ref_is_avatar = False
        bdict['enable_sync'] = False
        self.filter_com(bdict)
        super(LPuppet, self).init_from_dict(bdict)
        self.send_event('S_YAW_WITH_CAM', 0)

    def filter_com(self, bdict):
        battle = self.get_battle()
        if battle:
            map_data_conf = confmgr.get('map_config', str(battle.map_id), default={})
            if map_data_conf.get('iNeedGranbelmRune', 0):
                bdict['need_granbelm_rune'] = True
        if is_battle_signal_open():
            bdict['need_signal'] = True
        if global_data.game_mode:
            if global_data.game_mode.is_pve():
                bdict['need_pve_com'] = True

    def destroy(self, *args, **kwargs):
        global_data.emgr.puppet_destroy_event.emit(self.id)
        super(LPuppet, self).destroy()