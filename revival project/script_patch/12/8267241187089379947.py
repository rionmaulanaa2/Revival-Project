# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/RainbowPluginStruct.py
from collections import namedtuple
from ...Meta.TypeMeta import *
EDIT_MODE_GAME = 0
EDIT_MODE_EDIT = 1
TRANSLATE = 0
ROTATE = 1
SCALE = 2
GIZMO_MODE_WORLD = 0
GIZMO_MODE_LOCAL = 1
SubEditMode = namedtuple('SubEditMode', ['Mode', 'ActionName', 'Text'])
CreateEntityData = namedtuple('CreateEntityData', ['ActionName', 'EntityType', 'Text', 'PrefabData', 'EditGroup'])
IconName = namedtuple('IconName', ['Avatar', 'PlayerAvatar', 'Monster', 'NPC', 'Spawn', 'Radar', 'Pet', 'Carrier', 'Other'])

class EditComponent(object):

    def PostInit(self, data):
        pass

    def GetParent(self):
        pass

    def SetParent(self, p):
        pass

    def GetEditName(self):
        return ''

    def SetEditName(self, n):
        pass

    def IsStartEntity(self):
        return False

    def SetStartEntity(self, isStartEntity):
        pass

    def GetEditCategory(self):
        return ''

    def SetEditCategory(self, c):
        pass

    def GetIconName(self):
        return ''

    def SetIconName(self, i):
        pass

    def GetPosition(self):
        pass

    def SetPosition(self, v):
        pass

    def GetDirection(self):
        pass

    def SetDirection(self, v):
        pass

    def GetScale(self):
        pass

    def SetScale(self, v):
        pass

    def GetLocalPosition(self):
        pass

    def SetLocalPosition(self, v):
        pass

    def GetLocalDirection(self):
        pass

    def SetLocalDirection(self, v):
        pass

    def GetLocalScale(self):
        pass

    def SetLocalScale(self, v):
        pass

    def IsEditable(self):
        return False

    def SetEditable(self, editable):
        pass

    def GetTypeName(self):
        return self.__class__.__name__

    def GetBaseClassNames(self):
        return []

    def ConvertToDict(self):
        r = {}
        parent = self.GetParent()
        if parent:
            r['parent'] = parent
            r['localPosition'] = self.GetLocalPosition()
            r['localDirection'] = self.GetLocalDirection()
            r['localScale'] = self.GetLocalScale()
        r['editable'] = self.IsEditable()
        r['editName'] = self.GetEditName()
        r['isStartEntity'] = self.IsStartEntity()
        r['editCategory'] = self.GetEditCategory()
        r['iconName'] = self.GetIconName()
        r['Type'] = self.GetTypeName()
        r['position'] = self.GetPosition()
        r['direction'] = self.GetDirection()
        r['scale'] = self.GetScale()
        r['baseClassNames'] = self.GetBaseClassNames()
        return r

    def ModifyProperty(self, propName, value):
        if propName == 'parent':
            self.SetParent(value)
        elif propName == 'editName':
            self.SetEditName(value)
        elif propName == 'editCategory':
            self.SetEditCategory(value)
        elif propName == 'editable':
            self.SetEditable(value)
        elif propName == 'isStartEntity':
            self.SetStartEntity(value)
        elif propName == 'iconName':
            self.SetIconName(value)
        elif propName == 'position':
            self.SetPosition(value)
        elif propName == 'direction':
            self.SetDirection(value)
        elif propName == 'scale':
            self.SetScale(value)
        elif propName == 'localPosition':
            self.SetLocalPosition(value)
        elif propName == 'localDirection':
            self.SetLocalDirection(value)
        elif propName == 'localScale':
            self.SetLocalScale(value)


del namedtuple