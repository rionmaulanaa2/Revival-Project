# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/camera_target_com_utils.py
cam_target_coms = {'PLAYER_COMS': [
                 ('ComKingZoneChecker', 'client.com_king'),
                 ('ComKillerCamera', 'client.com_camera'),
                 ('ComMechaModuleInstallEffect', 'client.com_death')],
   'HUMAN_TARGET_COMS': [
                       ('ComHumanTransparentCam', 'client.com_camera'),
                       ('ComStateTrkCam', 'client.com_camera'),
                       ('ComHumanTransparentModel', 'client.com_camera'),
                       ('ComStateTrkCamEvents', 'client.com_camera'),
                       ('ComCameraEvent', 'client.com_camera'),
                       ('ComSpringAnim', 'client.com_character_ctrl'),
                       ('ComVibrate', 'client.com_camera')],
   'NON_HUMAN_TARGET_COMS': [
                           ('ComObserveNonHumanControlTargetGSender', 'client.com_global_sync'),
                           ('ComCamSyncReceiver', 'client'),
                           ('ComCameraEvent', 'client.com_camera'),
                           ('ComVibrate', 'client.com_camera')],
   'MECHA_TARGET_COMS': [
                       ('ComObserveMechaControlTargetGSender', 'client.com_global_sync'),
                       ('ComObserveMechaControlTargetGReceiver', 'client.com_global_sync'),
                       ('ComMechaTransparentCam', 'client.com_camera'),
                       ('ComStateTrkCam', 'client.com_camera'),
                       ('ComMechaTransparentModel', 'client.com_camera'),
                       ('ComShoulderCannonCam', 'client.com_camera'),
                       ('ComMechaShortcut', 'client'),
                       ('ComMechaStateTrkCamEvents', 'client.com_camera'),
                       ('ComDataCameraRotate', 'client')]
   }