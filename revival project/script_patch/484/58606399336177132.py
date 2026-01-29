# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/MontCameraBlendHelper.py
from __future__ import absolute_import
import math3d
import MontageSDK
from MontageSDK.Lib.MontEventManager import getMontEventMgrInstance as MontEventMgr
from .TrackImp.UniGameInterface import set_cur_camera_params
from .TrackImp.UniHelper import get_active_scene, euler_angle_to_rotation_matrix, rotation_matrix_to_euler_angle, standardize_degree
BLEND_GROUPNAME = 'Blend'

def getCurCamera():
    if MontageSDK.RuntimeInitiated:
        cur_scn = get_active_scene()
        camera = cur_scn.active_camera
    else:
        camera = None
    return camera


def getCurCameraTransform():
    camera = getCurCamera()
    return {'Translation': camera.world_position,'Rotation': rotation_matrix_to_euler_angle(camera.world_rotation_matrix)}


def setCurCameraTransform(translation, rotation):
    camera = getCurCamera()
    camera.world_position = translation
    camera.world_rotation_matrix = euler_angle_to_rotation_matrix(rotation)


class MontCameraBlendHelper(object):

    def __init__(self):
        super(MontCameraBlendHelper, self).__init__()
        self.isBlending = False
        self.isBlendIn = False
        self.isBlendOut = False
        self.blendTime = None
        self.blendDuration = None
        self.startTransform = None
        self.endTransform = None
        self.blendInFinished = None
        self._originTransform = None
        return

    def _reset(self):
        self.isBlendIn = False
        self.isBlendOut = False
        self.blendTime = None
        self.blendDuration = None
        self.startTransform = None
        self.endTransform = None
        self.blendInFinished = None
        self._originTransform = None
        return

    def PlayMontWithBlender(self, fileName, blendParam):
        if not fileName or self.isBlending:
            return False
        self._reset()
        interface = MontageSDK.Interface
        self.isBlendIn = blendParam.get('In', False)
        self.isBlendOut = blendParam.get('Out', False)
        ret = interface.LoadMontFileToTransactionMediator(fileName, groupName=BLEND_GROUPNAME)
        if ret is False:
            return False
        group = interface.getMontageGroupByName(BLEND_GROUPNAME)
        if group.media.blendIn <= 0:
            self.isBlendIn = False
        if group.media.blendOut <= 0:
            self.isBlendOut = False
        if self.isBlendIn or self.isBlendOut:
            self._originTransform = getCurCameraTransform()
            MontEventMgr().registerCinematicEvent(self.blendInCamera, eventType='PRE_ASYNC', groupName=BLEND_GROUPNAME)
            MontEventMgr().registerCinematicEvent(self.blendOutCamera, eventType='POST_POP', groupName=BLEND_GROUPNAME)
        config = {'startTime': 0.0,'previewCamera': 'Shot','isPause': False}
        noAsync = interface.PrePlayCinematics(groupName=BLEND_GROUPNAME, config=config, force=True)
        if noAsync:
            result = interface.PreviewCinematics(group.cineData, 0, False, groupName=BLEND_GROUPNAME)
            if result and group.media.getProperty('currentBranch'):
                interface.SwitchToBranch(BLEND_GROUPNAME, group.media.getProperty('currentBranch'), force=True)

    def blendInCamera(self, groupName, callback, config=None):
        self.isBlending = True
        global_data.montage_editor.add_editor_update_func(self.blendUpdate)
        interface = MontageSDK.Interface
        if not self.isBlendIn:
            return callback(groupName, config)
        self.blendInFinished = lambda : callback(groupName, config)
        self.startTransform = getCurCameraTransform()
        self.endTransform = {}
        group = interface.getMontageGroupByName(groupName)
        media = group.media
        self.endTransform['Translation'] = math3d.vector(*media.initTransform['Translation'])
        rot_vec = media.initTransform['Rotation']
        rot_vec = (
         rot_vec[1], rot_vec[2], rot_vec[0])
        startRot, endRot = self.rotationVecNormalize(self.startTransform['Rotation'], math3d.vector(*rot_vec))
        self.startTransform['Rotation'] = startRot
        self.endTransform['Rotation'] = endRot
        self.blendDuration = media.blendIn
        self.blendTime = 0

    def blendOutCamera(self, groupName, endTransform=None):
        if endTransform is None:
            endTransform = self._originTransform
        if self.isBlendOut:
            self.startTransform = getCurCameraTransform()
            self.endTransform = endTransform
            startRot, endRot = self.rotationVecNormalize(self.startTransform['Rotation'], endTransform['Rotation'])
            self.startTransform['Rotation'] = startRot
            self.endTransform['Rotation'] = endRot
            interface = MontageSDK.Interface
            group = interface.getMontageGroupByName(groupName)
            media = group.media
            self.blendDuration = media.blendOut
            self.blendTime = 0
        else:
            set_cur_camera_params(endTransform['Translation'], endTransform['Rotation'])
            self.blendOutFinished()
        return

    def blendOutFinished(self):
        global_data.montage_editor.remove_editor_update_func(self.blendUpdate())
        self.isBlending = False

    def blendUpdate(self, dtsecond):
        if self.blendTime is not None:
            if 0 < self.blendTime < self.blendDuration + 1e-05:
                self.linearBlendUpdate(self.blendTime)
            elif self.blendTime >= self.blendDuration + 1e-05:
                if callable(self.blendInFinished):
                    self.blendInFinished()
                    self.blendInFinished = None
                else:
                    self.blendOutFinished()
                self.blendTime = None
                return
            self.blendTime += dtsecond
        return

    def linearBlendUpdate(self, curTime):
        currTransform = {}
        for key in ['Translation', 'Rotation']:
            currVec = math3d.vector(0, 0, 0)
            currVec.intrp(self.startTransform[key], self.endTransform[key], curTime / self.blendDuration)
            currTransform[key] = currVec

        setCurCameraTransform(currTransform['Translation'], currTransform['Rotation'])

    def rotationVecNormalize(self, start_vec, end_vec):

        def standardize_vec(vec):
            for comp in ['x', 'y', 'z']:
                setattr(vec, comp, standardize_degree(getattr(vec, comp)))

            return vec

        start_vec = standardize_vec(start_vec)
        end_vec = standardize_vec(end_vec)
        for comp in ['x', 'y', 'z']:
            comp_diff = getattr(start_vec, comp) - getattr(end_vec, comp)
            if comp_diff > 180:
                setattr(start_vec, comp, getattr(start_vec, comp) - 360)
            elif comp_diff < -180:
                setattr(start_vec, comp, getattr(start_vec, comp) + 360)

        return (
         start_vec, end_vec)