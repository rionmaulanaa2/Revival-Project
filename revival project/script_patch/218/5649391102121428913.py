# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/MontPath/Manager/MontEntityPathManagerImp.py
from __future__ import absolute_import
from montage import MontageSDK
from montage.MontageSDK.Lib.MontPathManager import MontPathManagerBase, PathManger
from montage.MontageSDK.Backend.utils.Formula import intersectedPos, binarySearchLeft
import world
import render
import math3d
import math
import game3d
from ...TrackImp.UniHelper import euler_angle_to_rotation_matrix
TECH = None
MAT_DICT = {}

def get_material(key=0):
    global TECH
    TECH = render.technique(1, 'shader/ui/ui_pure_color.nfx', 'TShader', None)
    if key not in MAT_DICT:
        MAT_DICT[key] = render.material(TECH)
    return MAT_DICT[key]


@PathManger
class MontEntityPathManagerImp(MontPathManagerBase):
    SYSTEM = 'EntityActor'
    SINGLE_TICK_DUR = 1 / 30.0
    RAIL_WIDTH_HALF = 0.2
    MODE = ('RAIL', 'LINE')

    def __init__(self):
        super(MontEntityPathManagerImp, self).__init__()
        self.mode = self.MODE[1]
        self.pathUuid = ''
        self.time_array = []
        self._line = None
        self.editFrame = None
        return

    @property
    def transformProxy(self):
        media = MontageSDK.Helper.media['EditorPreview']
        try:
            return media.getProxy(self.pathUuid)['Transform']
        except AttributeError:
            return None

        return None

    def SetCameraPath(self, uuids, callback=True):
        if not len(uuids) == 1:
            self.clear()
            return
        if uuids[0] == self.pathUuid:
            return
        self.clear()
        self.pathUuid = uuids[0]
        self.RefreshEntityPath()

    def RefreshEntityPath(self):
        if not self.pathUuid:
            return
        if not self.transformProxy:
            return
        timeArray = []
        for child in self._getBottomChildrenWithoutScale():
            for f in child.getFrames():
                if f.getTime() in timeArray:
                    continue
                toAdd = binarySearchLeft(timeArray, f.getTime())
                timeArray.insert(toAdd, f.getTime())

        self.time_array = timeArray
        if len(self.time_array) < 2:
            return
        self.updateGraphicViews()

    def RefreshEntityPathByEdit(self):
        movieGroup = MontageSDK.Interface.entities.get(self.pathUuid)
        if movieGroup and movieGroup.model:
            new_position = movieGroup.model.world_position
            track = self.transformProxy['Translation']
            time = MontageSDK.Interface.uniMgr.getSceneTime(moviekey='EditorPreview')
            self.editFrame = track.replaceFrame({'X': new_position.x,'Y': new_position.y,'Z': new_position.z}, time)
            self.updateGraphicViews(add_time=time)

    def updateGraphicViews(self, add_time=None):
        if not self.transformProxy or not self.transformProxy.isValid():
            self.clear()
            return
        else:
            curTime = self.time_array[0]
            maxTime = self.time_array[-1]
            if add_time is not None:
                if add_time < curTime:
                    curTime = add_time
                elif add_time > maxTime:
                    maxTime = add_time
            samplePoints = []
            while curTime <= maxTime:
                position = self._getIntersectedValue(self.transformProxy['Translation'], curTime)
                samplePoints.append(position)
                curTime += round(self.SINGLE_TICK_DUR, 3)

            line_points = []
            self._initLines()
            last_pos = None
            last_vert_left = None
            last_vert_right = None
            for pos in samplePoints:
                pos = math3d.vector(*pos)
                if last_pos:
                    if self.mode == self.MODE[0]:
                        dir_vec = math3d.vector3_normalize(pos - last_pos)
                        dir_left = math3d.vector3_normalize(math3d.Vector3(dir_vec.z, 0, -dir_vec.x))
                        dir_right = math3d.vector3_normalize(math3d.Vector3(-dir_vec.z, 0, dir_vec.x))
                        cur_vert_left = pos + dir_left * self.RAIL_WIDTH_HALF
                        cur_vert_right = pos + dir_right * self.RAIL_WIDTH_HALF
                        if last_vert_left is None and last_vert_right is None:
                            last_vert_left = last_pos + dir_left * 1
                            last_vert_right = last_pos + dir_right * 1
                        line_points.append(((cur_vert_left,), (last_vert_left, 0), 0))
                        line_points.append(((cur_vert_left,), (cur_vert_right, 0), 0))
                        line_points.append(((last_vert_right,), (cur_vert_right, 0), 0))
                        last_vert_left = cur_vert_left
                        last_vert_right = cur_vert_right
                    else:
                        line_points.append(((pos,), (last_pos, 0), 0))
                last_pos = pos

            self._line.create_line(line_points)
            self._line.visible = True
            return

    def clear(self):
        if self._line:
            self._line.visible = False
            self.pathUuid = ''

    def UpdateNodeEditToGame(self):
        pathId = self.pathUuid
        frameProxys = self.editFrame
        if not pathId or not frameProxys:
            return
        else:
            data = {'translation': {'X': frameProxys['X'].getValue(),
                               'Y': frameProxys['Y'].getValue(),
                               'Z': frameProxys['Z'].getValue()
                               }
               }
            time = MontageSDK.Interface.uniMgr.getSceneTime(moviekey='EditorPreview')
            MontageSDK.ExtendPlugin.Server.UpdateCameraPathNode(pathId, time, data)
            self.editFrame = None
            return

    def _initLines(self):
        if self._line is not None:
            return
        else:
            self._line = world.primitives(world.get_active_scene())
            material = get_material(0)
            self._line.set_material(material)
            material.set_var(game3d.calc_string_hash('color'), 'color', (1.0, 0.0,
                                                                         1.0, 0.8))
            return

    def _getIntersectedValue(self, trackProxy, time):
        if trackProxy is None or trackProxy.trackType not in ('Translation', 'Rotation'):
            MontageSDK.Interface.PrintFunc("[ERROR]don't try getIntersectedValue in [CameraPathMgr] for this type of track proxy", trackProxy)
            return
        else:
            if trackProxy.trackType == 'Translation':
                childTypes = [
                 'X', 'Y', 'Z']
            else:
                childTypes = [
                 'Roll', 'Pitch', 'Yaw']
            valueList = []
            for childType in childTypes:
                if trackProxy[childType]:
                    valueList.append(float(intersectedPos(time, trackProxy[childType].getFrames())[0][1]))
                else:
                    valueList.append(0.0)

            return valueList

    def _getBottomChildrenWithoutScale(self):
        children = []
        if self.transformProxy is None:
            return children
        else:
            if 'Translation' in self.transformProxy:
                children.extend(self.transformProxy['Translation'].getChildren())
            if 'Rotation' in self.transformProxy:
                children.extend(self.transformProxy['Rotation'].getChildren())
            return children