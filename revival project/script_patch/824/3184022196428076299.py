# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/MontEditComponent.py
from __future__ import absolute_import
from six.moves import range
import math
from MontageSDK.Lib.MontGameInterface import MontEditComponent
from MontageSDK.Lib.VirtualObj import BaseVirtualObj

def rotation_matrix_to_euler_angle(m4_rotation):
    pitch = math.degrees(m4_rotation.pitch)
    yaw = math.degrees(m4_rotation.yaw)
    roll = math.degrees(m4_rotation.roll)
    return (
     roll, pitch, yaw)


class MontEditComponentImp(MontEditComponent):

    def __init__(self, entity):
        super(MontEditComponentImp, self).__init__(entity)
        if isinstance(self.e, BaseVirtualObj):
            self.SetEditType(self.EDITTYPE_VIRTUAL)
        else:
            self.SetEditType(self.EDITTYPE_RECRUITED)

    def GetEditType(self):
        if isinstance(self.e, BaseVirtualObj):
            return self.EDITTYPE_VIRTUAL
        else:
            if self.e.model:
                return self.editType
            return self.EDITTYPE_INVALID

    def GetName(self):
        name = self.e.name
        return name

    def GetPosition(self):
        if self.e.model:
            translation = self.e.model.world_position
            return {'X': round(translation.x, 3),'Y': round(translation.y, 3),'Z': round(translation.z, 3)}
        else:
            return {}

    def GetRotation(self):
        if self.e.model:
            mat = self.e.model.world_rotation_matrix
            rot = rotation_matrix_to_euler_angle(mat)
            return {'Roll': round(rot[0], 3),
               'Pitch': round(rot[1], 3),
               'Yaw': round(rot[2], 3)
               }
        else:
            return {}

    def GetScale(self):
        if self.e.model:
            scale = self.e.model.world_scale
            return {'X': round(scale.x, 3),'Y': round(scale.y, 3),'Z': round(scale.z, 3)}
        else:
            return {}

    def GetGuid(self):
        return ''

    def GetSocketList(self):
        if self.e.model:
            sockets = []
            if hasattr(self.e.model, 'get_socket_count'):
                for n_index in range(self.e.model.get_socket_count()):
                    sockets.append(self.e.model.get_socket_name(n_index))

            return sockets
        else:
            return []

    def GetBonesList(self):
        bones = []
        boneParentIDs = []
        if self.e.model and hasattr(self.e.model, 'get_skeleton_component'):
            skeletonComponent = self.e.model.get_skeleton_component()
            if skeletonComponent:
                for index in range(skeletonComponent.get_joint_count()):
                    bones.append(skeletonComponent.get_joint_name(index))
                    boneParentIDs.append(skeletonComponent.get_joint_parent_index(index))

        return (
         bones, boneParentIDs)

    def GetGroup(self):
        import world
        scene = world.get_active_scene()
        groups = scene.get_object_groups()
        for group in groups:
            modelList = scene.get_models_in_group(group)
            for model in modelList:
                if self.e.model is model:
                    return 'Group_' + group

        return 'Uncategorized'

    def ConvertToDict(self):
        data = super(MontEditComponentImp, self).ConvertToDict()
        bones, boneParentIDs = self.GetBonesList()
        data['MontageInfo'].update({'Type': self.GetEditType(),
           'sockets': self.GetSocketList(),
           'bones': bones,
           'boneParentIDs': boneParentIDs
           })
        data['MontageInfo']['Edit']['editCategory'] = self.GetGroup()
        return data