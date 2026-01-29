# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LMonster.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component

@component(share=('ComHealth', 'ComStatusMonster', 'ComBuffData'), client=[
 'ComDataRenderRotate',
 'ComDataAnimator',
 'ComDataAppearance',
 'ComDataCommonMotor',
 'ComDataLogicTransform',
 'ComDataLogicLod',
 'ComClientSynchronizer',
 'ComMonsterAppearance',
 'ComAIAgent',
 'ComSyncAIClient',
 'ComMoveShadow',
 'com_ai_ctrl.ComRemoteMonsterMove',
 'com_hit_hint.ComHitHintMonster',
 'ComTrajectoryAppearance',
 'ComMuzzleAppearance',
 'ComMonsterCollision',
 'com_character_ctrl.ComBehavior',
 'com_character_ctrl.ComAnimMgr',
 'com_character_ctrl.ComInput',
 'ComExplosiveContainerClient',
 'ComMonsterSound',
 'ComAgony',
 'ComMonsterLogic',
 'ComCamp',
 'ComMonsterMarkView',
 'ComAIDebugUI',
 'ComThrowableDriver',
 'ComBuffClient',
 'ComMechaActivateClient',
 'ComHitFlag',
 'ComMonsterEffect',
 'ComFlagUI',
 'ComMaterialStatus',
 'ComAddFactorClient',
 ('ComHumanHurtAppearance', 'pve_com'),
 ('ComPVEMonsterSkillClient', 'pve_com'),
 ('ComPVEMonsterEventDock', 'pve_com'),
 ('ComHitStun', 'pve_com'),
 ('ComPVEMonsterHitTip', 'pve_com'),
 ('ComPVEMonsterData', 'pve_com'),
 ('ComPVEMonsterShake', 'pve_com'),
 ('ComPVEMonsterPosChecker', 'pve_com'),
 ('ComMoveSyncAnimRateSender', 'pve_com'),
 ('ComStateSimui', 'pve_com'),
 ('ComSpeedUp', 'pve_com')])
class LMonster(Unit):

    def init_from_dict(self, bdict):
        super(LMonster, self).init_from_dict(bdict)

    def is_monster(self):
        return True