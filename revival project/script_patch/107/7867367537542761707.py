# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/MontPath/Manager/DollyTrackPathManagerImp.py
from __future__ import absolute_import
from six.moves import range
import MontageSDK
from MontageSDK.Lib.MontPathManager import PathManger
from .MontPathManagerImp import MontPathManagerImp
from MontageImp.MontPath.Manager.ModelProxy import ModelProxy
from MontageSDK.Backend.utils.Formula import cubicSplineInterpolation, intersectedPos
from ...TrackImp.UniHelper import euler_angle_to_rotation_matrix
import math3d
import world

@PathManger
class DollyTrackManagerImp(MontPathManagerImp):
    SYSTEM = 'DollyTrack'

    def __init__(self):
        super(DollyTrackManagerImp, self).__init__()
        self.mode = self.MODE[0]
        self.wayPoints = []
        self.cubicSplineParams = []

    @property
    def wayNodes(self):
        return self._node_rendered

    def UpdateNodePos(self, node):
        nodes = [ wnode.model for wnode in self.wayNodes ]
        if node not in nodes:
            return
        dollyTrackProxy = MontageSDK.Interface.getEdittimeMedia().getProxy(self.pathUuid)
        if not dollyTrackProxy:
            return
        position = node.world_position
        nodeIndex = nodes.index(node)
        self.wayPoints[nodeIndex]['X'] = position.x
        self.wayPoints[nodeIndex]['Y'] = position.y
        self.wayPoints[nodeIndex]['Z'] = position.z
        dollyTrackProxy.setProperty('wayPoints', self.wayPoints)
        self.RefreshCameraPath()

    def SetWaypointToEditor(self, index):
        data = {'translation': [
                         self.wayPoints[index]['X'],
                         self.wayPoints[index]['Y'],
                         self.wayPoints[index]['Z']],
           'rotation': [
                      self.wayPoints[index]['Roll'],
                      self.wayPoints[index]['Pitch'],
                      self.wayPoints[index]['Yaw']]
           }
        MontageSDK.ExtendPlugin.Server.updateCameraPathNode(self.pathUuid, index + 1, data, 'DollyTrack')

    def RefreshCameraPath(self):
        if self._initCurve():
            self.updateGraphicViews()

    def _initCurve(self):
        dollyTrackProxy = MontageSDK.Interface.getEdittimeMedia().getProxy(self.pathUuid)
        if not dollyTrackProxy:
            return False
        self.wayPoints = dollyTrackProxy.getProperty('wayPoints')
        if not self.wayPoints or len(self.wayPoints) < 2:
            return False
        xPoints, yPoints, zPoints = [], [], []
        rollPoints, pitchPoints, yawPoints = [], [], []
        for i in range(len(self.wayPoints)):
            xPoints.append([i, self.wayPoints[i]['X']])
            yPoints.append([i, self.wayPoints[i]['Y']])
            zPoints.append([i, self.wayPoints[i]['Z']])
            rollPoints.append([i, self.wayPoints[i]['Roll']])
            pitchPoints.append([i, self.wayPoints[i]['Pitch']])
            yawPoints.append([i, self.wayPoints[i]['Yaw']])

        paramsx = cubicSplineInterpolation(xPoints, 0, 0)
        paramsy = cubicSplineInterpolation(yPoints, 0, 0)
        paramsz = cubicSplineInterpolation(zPoints, 0, 0)
        paramsroll = cubicSplineInterpolation(rollPoints, 0, 0)
        paramspitch = cubicSplineInterpolation(pitchPoints, 0, 0)
        paramsyaw = cubicSplineInterpolation(yawPoints, 0, 0)
        self.cubicSplineParams = [paramsx, paramsy, paramsz, paramsroll, paramspitch, paramsyaw]
        return True

    def updateGraphicViews(self, add_time=None):
        samplePoints = self._createSameplePoints()
        line_points = []
        self._initLines()
        self._initVirtualNode()
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

        if len(line_points) >= 2:
            self._line.create_line(line_points)
            self._line.visible = True
        else:
            self._line.visible = False
        self.last_update_index = 0
        i = 0
        for i, point in enumerate(self.wayPoints):
            if i < len(self._node_rendered):
                node = self._node_rendered[i]
            else:
                node = ModelProxy(self.CAMERA_VIRTUAL_MODEL, lambda obj, *args: world.get_active_scene().add_object(obj))
                self._node_rendered.append(node)
            node.visible = True
            node.pickable = True
            self.updateNodeTransform(node, i)

        for node in self._node_rendered[i + 1:]:
            node.visible = False

        if self._virtual_node and self._virtual_node.valid:
            self._virtual_node.visible = True
            self.updateVirtualNode(MontageSDK.Interface.timelineman.getSceneTime(moviekey='EditorPreview'))
        return

    def _createSameplePoints(self):
        if len(self.wayPoints) < 2 or not self.cubicSplineParams:
            return []
        paramsx, paramsy, paramsz, a, b, c = self.cubicSplineParams
        samplePoints = []
        sampleRate = 0.01
        for pi in range(len(paramsx)):
            t = 0
            while t <= 1:
                x = paramsx[pi][0] * t ** 3 + paramsx[pi][1] * t ** 2 + paramsx[pi][2] * t + paramsx[pi][3]
                y = paramsy[pi][0] * t ** 3 + paramsy[pi][1] * t ** 2 + paramsy[pi][2] * t + paramsy[pi][3]
                z = paramsz[pi][0] * t ** 3 + paramsz[pi][1] * t ** 2 + paramsz[pi][2] * t + paramsz[pi][3]
                samplePoints.append([x, y, z])
                t = t + sampleRate

        return samplePoints

    def updateNodeTransform(self, node, progress):
        transform = self._calcTransOnCurve(progress)
        if not transform:
            return False
        position = transform[:3]
        rotation = transform[3:]
        node.position = math3d.vector(*position)
        rot_vec = math3d.vector(rotation[1], rotation[2], rotation[0])
        m4_rotation = euler_angle_to_rotation_matrix(rot_vec)
        node.world_rotation_matrix = m4_rotation

    def _calcTransOnCurve(self, progress):
        if not self.cubicSplineParams:
            return False
        paramx, paramy, paramz, paramroll, parampitch, paramyaw = self.cubicSplineParams
        progress = min(progress, len(paramx))
        isec = int(progress)
        if isec < 1:
            t = progress
        else:
            t = round(progress % isec, 3)
        if t == 0:
            point = self.wayPoints[isec]
            return [
             point['X'], point['Y'], point['Z'], point['Roll'], point['Pitch'], point['Yaw']]
        paramx, paramy, paramz = paramx[isec], paramy[isec], paramz[isec]
        paramroll, parampitch, paramyaw = paramroll[isec], parampitch[isec], paramyaw[isec]
        x = paramx[0] * t ** 3 + paramx[1] * t ** 2 + paramx[2] * t + paramx[3]
        y = paramy[0] * t ** 3 + paramy[1] * t ** 2 + paramy[2] * t + paramy[3]
        z = paramz[0] * t ** 3 + paramz[1] * t ** 2 + paramz[2] * t + paramz[3]
        roll = paramroll[0] * t ** 3 + paramroll[1] * t ** 2 + paramroll[2] * t + paramroll[3]
        pitch = parampitch[0] * t ** 3 + parampitch[1] * t ** 2 + parampitch[2] * t + parampitch[3]
        yaw = paramyaw[0] * t ** 3 + paramyaw[1] * t ** 2 + paramyaw[2] * t + paramyaw[3]
        return [
         x, y, z, roll, pitch, yaw]

    def updateVirtualNode(self, time, isPaused=None, groupName=None):
        groupName = groupName or 'EditorPreview'
        if groupName != 'EditorPreview':
            return
        if not self.pathUuid:
            return
        if self._virtual_node and self._virtual_node.valid:
            dollyTrackProxy = MontageSDK.Interface.getEdittimeMedia().getProxy(self.pathUuid)
            progress = self._getIntersectedValue(dollyTrackProxy, time)
            self.updateNodeTransform(self._virtual_node, progress)
            self._virtual_node.visible = True

    def update(self):
        pass

    def _getIntersectedValue(self, trackProxy, time):
        frames = trackProxy.getFrames()
        if len(frames) == 0:
            return 0
        return float(intersectedPos(time, frames)[0][1])