# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/MontPath/Manager/MontPathManagerImp.py
from __future__ import absolute_import
import MontageSDK
from MontageImp.MontPath.Manager.ModelProxy import ModelProxy
from MontageSDK.Lib.MontPathManager import MontPathManagerBase, PathManger
from MontageSDK.Backend.utils.Formula import intersectedPos, binarySearchLeft
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
    TECH = render.technique(1, 'shader/ui/ui_pure_color.nfx', 'TShader')
    if key not in MAT_DICT:
        MAT_DICT[key] = render.material(TECH)
    return MAT_DICT[key]


@PathManger
class MontPathManagerImp(MontPathManagerBase):
    SYSTEM = 'CameraActor'
    SINGLE_TICK_DUR = 1 / 30.0
    RAIL_WIDTH_HALF = 0.2
    CAMERA_VIRTUAL_MODEL = 'model/xiangji/xiangji.gim'
    MODE = ('RAIL', 'LINE')

    def __init__(self):
        super(MontPathManagerImp, self).__init__()
        self.showPath = {'Camera': True,'Entity': True}
        self.pathType = ''
        self.mode = self.MODE[1]
        self.pathUuid = ''
        self.time_array = []
        self.transformProxy = None
        self._line = None
        self._node_rendered = []
        self._node_proxies = []
        self.last_update_index = 0
        self._virtual_node = None
        self.m_AxisEdit = None
        self.editFrame = None
        global_data.montage_editor.add_editor_update_func(lambda dtTime: self.update())
        return

    def update(self):
        curTime = MontageSDK.Interface.timelineman.getSceneTime(moviekey='EditorPreview')
        self.updateVirtualNode(curTime)

    @property
    def virtual_node(self):
        if self._virtual_node and self._virtual_node.valid:
            return self._virtual_node
        else:
            return None

    def _initLines(self):
        if self._line is not None:
            return
        else:
            self._line = world.primitives(world.get_active_scene())
            material = get_material(0)
            self._line.set_material(material)
            material.set_var(game3d.calc_string_hash('color'), 'color', (1.0, 1.0,
                                                                         0.0, 0.8))
            return

    def _initVirtualNode(self):

        def virtual_node_callback(obj, *args):
            self._virtual_node = obj
            world.get_active_scene().add_object(self._virtual_node)
            self._virtual_node.visible = False
            self._virtual_node.pickable = True

        if self._virtual_node is None or not self._virtual_node.valid:
            world.create_model_async(self.CAMERA_VIRTUAL_MODEL, virtual_node_callback)
        return

    def updateVirtualNode(self, time, isPaused=None, groupName=None):
        groupName = groupName or 'EditorPreview'
        if groupName != 'EditorPreview':
            return
        if not self.pathUuid or not self.pathType:
            return
        if self._virtual_node and self._virtual_node.valid:
            self.updateNodeTransform(self._virtual_node, time=time)
            self._virtual_node.visible = self.showPath[self.pathType]

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

    def setShowPath(self, pathType, isShow):
        self.showPath[pathType] = isShow
        self.RefreshCameraPath()

    def RemoveCurvePath(self, uuid):
        if uuid in self.paths:
            self.paths[uuid].clear()
            self.paths.pop(uuid)

    def SetCameraPath(self, uuids, callback=True):
        if not len(uuids) == 1:
            self.clear()
            return
        if uuids[0] == self.pathUuid:
            return
        self.clear()
        self.pathUuid = uuids[0]
        proxy = MontageSDK.Interface.getEdittimeMedia().getProxy(self.pathUuid)
        self.pathType = 'Camera' if proxy and proxy.trackType == 'CameraActor' else 'Entity'
        self.RefreshCameraPath()
        MontageSDK.Interface.cineEpisodeTimeChanged += self.updateVirtualNode

    def RefreshCameraPath(self):
        if not self.pathUuid:
            return
        cameraProxy = MontageSDK.Interface.getEdittimeMedia().getProxy(self.pathUuid)
        if not cameraProxy or not cameraProxy.isValid():
            return
        if 'Transform' not in cameraProxy:
            return
        self.transformProxy = cameraProxy['Transform']
        timeArray = []
        for child in self._getBottomChildrenWithoutScale():
            for f in child.getFrames():
                if f.getTime() in timeArray:
                    continue
                toAdd = binarySearchLeft(timeArray, f.getTime())
                timeArray.insert(toAdd, f.getTime())

        self.time_array = timeArray
        self.updateGraphicViews()

    def RefreshCameraPathByEdit(self):
        if not self._virtual_node or not self._virtual_node.valid:
            return
        position = self._virtual_node.world_position
        if not self.transformProxy:
            return
        curTime = MontageSDK.Interface.timelineman.getSceneTime(moviekey='EditorPreview')
        if self.transformProxy.isValid():
            self.editFrame = self.transformProxy.replaceFrame({'Translation': {'X': position.x,
                               'Y': position.y,
                               'Z': position.z
                               },
               'Rotation': {'Roll': math.degrees(self._virtual_node.world_rotation_matrix.roll),
                            'Pitch': math.degrees(self._virtual_node.world_rotation_matrix.pitch),
                            'Yaw': math.degrees(self._virtual_node.world_rotation_matrix.yaw)
                            }
               }, time=curTime)
            self.updateGraphicViews(curTime)

    def updateGraphicViews(self, add_time=None):
        if not self.transformProxy or not self.transformProxy.isValid() or len(self.time_array) == 0:
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
                self._line.visible = self.showPath[self.pathType]
            else:
                self._line.visible = False
            self.last_update_index = 0
            if len(self.time_array) > len(self._node_rendered):
                isNewNode = True
            else:
                isNewNode = False
            i = 0
            for i, time in enumerate(self.time_array):
                if i < len(self._node_rendered):
                    node = self._node_rendered[i]
                else:
                    node = ModelProxy(self.CAMERA_VIRTUAL_MODEL, lambda obj, *args: world.get_active_scene().add_object(obj))
                    node.pickable = False
                    self._node_rendered.append(node)
                node.visible = self.showPath[self.pathType]
                self.updateNodeTransform(node, time)

            for node in self._node_rendered[i + 1:]:
                node.visible = False

            if self._virtual_node and self._virtual_node.valid:
                self._virtual_node.visible = self.showPath[self.pathType]
                self.updateVirtualNode(MontageSDK.Interface.timelineman.getSceneTime(moviekey='EditorPreview'))
            return

    def updateNodeTransform(self, node, time):
        if not self.transformProxy.isValid():
            return
        position = self._getIntersectedValue(self.transformProxy['Translation'], time)
        rotation = self._getIntersectedValue(self.transformProxy['Rotation'], time)
        node.position = math3d.vector(*position)
        rot_vec = math3d.vector(rotation[1], rotation[2], rotation[0])
        m4_rotation = euler_angle_to_rotation_matrix(rot_vec)
        node.world_rotation_matrix = m4_rotation

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
                    frames = trackProxy[childType].getFrames()
                    if len(frames) == 0:
                        valueList.append(0.0)
                    else:
                        valueList.append(float(intersectedPos(time, trackProxy[childType].getFrames())[0][1]))
                else:
                    valueList.append(0.0)

            return valueList

    def clear(self):
        self.pathUuid = ''
        self.pathType = ''
        if self._line is not None:
            self._line.visible = False
        for node in self._node_rendered:
            node.destroy()

        self._node_rendered = []
        if self._virtual_node is not None:
            self._virtual_node.destroy()
            self._virtual_node = None
        MontageSDK.Interface.cineEpisodeTimeChanged -= self.updateVirtualNode
        return

    def SetCurvePathCurPos(self, time):
        from MontageSDK.Lib import MontGameInterface as MGI
        MGI.getGameInterface().SelectEntityByModel(None)
        self.updateVirtualNode(time)
        return

    def UpdateNodeEditToGame(self):
        pathId = self.pathUuid
        frameProxys = self.editFrame
        if not pathId or not frameProxys:
            return
        else:
            data = {'translation': {'X': frameProxys['Translation']['X'].getValue(),
                               'Y': frameProxys['Translation']['Y'].getValue(),
                               'Z': frameProxys['Translation']['Z'].getValue()
                               },
               'rotation': {'Roll': frameProxys['Rotation']['Roll'].getValue(),
                            'Pitch': frameProxys['Rotation']['Pitch'].getValue(),
                            'Yaw': frameProxys['Rotation']['Yaw'].getValue()
                            }
               }
            time = MontageSDK.Interface.timelineman.getSceneTime(moviekey='EditorPreview')
            MontageSDK.ExtendPlugin.Server.UpdateCameraPathNode(pathId, time, data)
            self.editFrame = None
            return