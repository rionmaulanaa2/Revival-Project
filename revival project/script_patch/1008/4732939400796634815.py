# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/Messiah/MessiahEditComponent.py
import MType
from ..RainbowEntityEditComponent import RainbowEntityEditComponent, sunshine_edit_component
from .EntityUtils import GetIEntity

@sunshine_edit_component
class MessiahEntityEditComponent(RainbowEntityEditComponent):
    ENTITY_CLASS = 'object'

    def PostInit(self, data):
        super(MessiahEntityEditComponent, self).PostInit(data)
        if 'position' in data:
            self.SetPosition(data['position'])
        if 'direction' in data:
            self.SetDirection(data['direction'])
        if 'scale' in data:
            self.SetScale(data['scale'])

    def EnterSelectedState(self):
        GetIEntity(self.entity).IsSelected = True

    def LeaveSelectedState(self):
        GetIEntity(self.entity).IsSelected = False

    def _GetTransform(self):
        return GetIEntity(self.entity).Transform

    def _SetTransform(self, transform):
        GetIEntity(self.entity).Transform = transform

    def GetPosition(self):
        translation = self._GetTransform().translation
        return [
         translation.x, translation.y, translation.z]

    def SetPosition(self, v):
        super(MessiahEntityEditComponent, self).SetPosition(v)
        transform = self._GetTransform()
        transform.translation = MType.Vector3(*v)
        self._SetTransform(transform)

    def GetDirection(self):
        transform = self._GetTransform()
        return (
         transform.roll, transform.pitch, transform.yaw)

    def SetDirection(self, v):
        super(MessiahEntityEditComponent, self).SetDirection(v)
        transform = self._GetTransform()
        transform.roll, transform.pitch, transform.yaw = v
        self._SetTransform(transform)

    def GetScale(self):
        scale = self._GetTransform().scale
        return [
         scale.x, scale.y, scale.z]

    def SetScale(self, v):
        super(MessiahEntityEditComponent, self).SetScale(v)
        transform = self._GetTransform()
        transform.scale = MType.Vector3(*v)
        self._SetTransform(transform)