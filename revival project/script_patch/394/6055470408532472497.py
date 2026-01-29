# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/RainbowEntityEditComponent.py
import math
try:
    from typing import Type
except ImportError:
    Type = None

from ..RainbowPluginStruct import EditComponent
from ....Meta.ClassMetaManager import GetClassMeta
from ....Meta.TypeMeta import *
from ....Meta.PropertyObject import PropertyObject, sunshine_property_object, RegisterPropertyObjectMeta
__all__ = [
 'RegisterEditComponentClass', 'sunshine_edit_component', 'GetEditComponentClass', 'RainbowEntityEditComponent']
_EditComponentClasses = {}

def RegisterEditComponentClass(clz):
    if clz.ENTITY_CLASS not in _EditComponentClasses:
        _EditComponentClasses[clz.ENTITY_CLASS] = clz


def sunshine_edit_component(clz):
    RegisterPropertyObjectMeta(clz)
    RegisterEditComponentClass(clz)
    return clz


def GetEditComponentClass(className):
    return _EditComponentClasses.get(className)


@sunshine_property_object
class RainbowEntityEditComponent(EditComponent, PropertyObject):
    ENTITY_CLASS = ''
    editName = ''
    editable = False
    isStartEntity = False
    editCategory = ''
    typeCategory = ''
    iconName = 'Other'
    parent = ''
    position = [0.0, 0.0, 0.0]
    direction = [0.0, 0.0, 0.0]
    scale = [1.0, 1.0, 1.0]
    localPosition = [0.0, 0.0, 0.0]
    localDirection = [0.0, 0.0, 0.0]
    localScale = [1.0, 1.0, 1.0]
    baseClassNames = []
    PROPERTIES = OrderedProperties([
     (
      'editName', PStr(text='\xe5\x90\x8d\xe7\xa7\xb0')),
     (
      'editable', PBool(text='\xe7\xbc\x96\xe8\xbe\x91\xe5\xaf\xb9\xe8\xb1\xa1')),
     (
      'isStartEntity', PBool(text='\xe5\x88\x9d\xe5\xa7\x8b\xe5\xaf\xb9\xe8\xb1\xa1', sort=3, tip='\xe5\xaf\xb9\xe8\xb1\xa1\xe6\x98\xaf\xe5\x90\xa6\xe5\x9c\xa8\xe5\x8a\xa0\xe8\xbd\xbd\xe5\x90\x8e\xe8\x87\xaa\xe5\x8a\xa8\xe5\x88\x9b\xe5\xbb\xba\xef\xbc\x9f')),
     (
      'editCategory', PEnum(text='\xe7\xbc\x96\xe8\xbe\x91\xe5\x88\x86\xe7\xbb\x84', enumType='EditCategory', editable=False)),
     (
      'typeCategory', PEnum(text='\xe7\xb1\xbb\xe5\x9e\x8b\xe5\x88\x86\xe7\xbb\x84', enumType='TypeCategory', editable=False)),
     (
      'iconName', PEnum(text='\xe5\x9b\xbe\xe6\xa0\x87', enumType='IconName', editable=False)),
     (
      'parent', PStr(text='\xe7\x88\xb6\xe5\xaf\xb9\xe8\xb1\xa1ID', editable=False)),
     (
      'baseClassNames', PArray(text='\xe7\xbb\xa7\xe6\x89\xbf\xe5\x9f\xba\xe7\xb1\xbb', editable=False, childAttribute=PStr())),
     (
      'position', PVector3(text='\xe4\xbd\x8d\xe7\xbd\xae', editable=False)),
     (
      'direction', PVector3(text='\xe6\x97\x8b\xe8\xbd\xac', editable=False)),
     (
      'scale', PVector3(text='\xe7\xbc\xa9\xe6\x94\xbe', editable=False)),
     (
      'localPosition', PVector3(text='\xe7\x9b\xb8\xe5\xaf\xb9\xe4\xbd\x8d\xe7\xbd\xae', editable=False)),
     (
      'localDirection', PVector3(text='\xe7\x9b\xb8\xe5\xaf\xb9\xe6\x97\x8b\xe8\xbd\xac', editable=False)),
     (
      'localScale', PVector3(text='\xe7\x9b\xb8\xe5\xaf\xb9\xe7\xbc\xa9\xe6\x94\xbe', editable=False))])

    def __init__(self, data=None):
        if data:
            PropertyObject.__init__(self, data)
        self._entity = None
        self._nameIndex = {}
        return

    @property
    def entity(self):
        return self._entity

    def Bind(self, entity):
        self._entity = entity
        self.baseClassNames = []
        import inspect
        bases = inspect.getmro(self._entity.__class__)
        if bases and len(bases) > 1:
            for base in bases[1:]:
                self.baseClassNames.append(base.__name__)

        self._UpdateEditName()

    def _UpdateEditName(self):
        if not self.editName:
            classMeta = GetClassMeta(self._entity.__class__.__name__)
            if classMeta:
                name = classMeta.editorMeta.get('text')
                if name:
                    index = self._nameIndex.get(name, 0) + 1
                    self.editName = '%s %4d' % (name, index)
                    self._nameIndex[name] = index
        else:
            splitList = self.editName.split(' ')
            if len(splitList) == 2 and splitList[1].isdigit():
                name, index = splitList[0], int(splitList[1])
                currIndex = self._nameIndex.setdefault(name, 0)
                if currIndex <= index:
                    self._nameIndex[name] = index + 1

    def Destroy(self):
        self._entity = None
        return

    def IsEditable(self):
        return self.editable

    def SetEditable(self, editable):
        self.editable = editable

    def GetParent(self):
        return self.parent

    def SetParent(self, p):
        self.parent = p

    def GetEditName(self):
        return self.editName

    def SetEditName(self, n):
        self.editName = n

    def IsStartEntity(self):
        return self.isStartEntity

    def SetStartEntity(self, isStartEntity):
        self.isStartEntity = isStartEntity

    def GetEditCategory(self):
        return self.editCategory

    def SetEditCategory(self, c):
        self.editCategory = c

    def GetIconName(self):
        return self.iconName

    def SetIconName(self, i):
        self.iconName = i

    def GetPosition(self):
        return self.position

    def SetPosition(self, v):
        self.position = v

    def GetDirection(self):
        return self.direction

    def SetDirection(self, v):
        self.direction = v

    def GetScale(self):
        return self.scale

    def SetScale(self, v):
        self.scale = v

    def GetLocalPosition(self):
        return self.localPosition

    def SetLocalPosition(self, v):
        self.localPosition = v

    def GetLocalDirection(self):
        return self.localDirection

    def SetLocalDirection(self, v):
        self.localDirection = v

    def GetLocalScale(self):
        return self.localScale

    def SetLocalScale(self, v):
        self.localScale = v

    def GetTypeName(self):
        return self.__class__.__name__

    def CheckIfSelected(self, x, y):
        return False

    def EnterSelectedState(self):
        pass

    def LeaveSelectedState(self):
        pass

    def GetBaseClassNames(self):
        return self.baseClassNames