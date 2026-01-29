# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Meta/LayoutAttributes.py
__all__ = [
 'LayoutRoot', 'Category', 'TableList', 'Group', 'BoxGroup', 'VerticalGroup', 'HorizontalGroup', 'ToggleGroup', 'TitleGroup', 'PropertyItem',
 'Br', 'HelpBox', 'Head', 'TableMatrix', 'TabGroup', 'TriangularMatrix', 'GridGroup', 'ResponsiveGroup', 'ProgressBar', 'GridGroupItem', 'Title',
 'register_layout', 'GetLayoutCls']
_Items = {}

def register_layout(cls):
    _type = cls.TYPE or cls.__name__
    if _type not in _Items:
        _Items[_type] = cls
    return cls


def GetLayoutCls(layoutType):
    return _Items.get(layoutType)


class _LayoutItem(object):
    TYPE = None
    VALUE_ATTR = None
    DEFAULT_ATTRS = {}

    def __init__(self, visibleCondition='', **kwargs):
        self._type = self.TYPE or self.__class__.__name__
        kwargs['visibleCondition'] = visibleCondition
        self.kwargs = kwargs
        self.children = []

    def __getitem__(self, item):
        if not isinstance(item, tuple):
            self.children = [
             item]
        else:
            self.children = item
        return self

    def Serialize(self, lite=False):
        children = [ c.Serialize(lite) for c in self.children ]
        if not lite:
            res = {'type': self._type}
            res.update(self.kwargs)
            if children:
                res['children'] = children
        else:
            attrs = {k:self.kwargs[k] for k in self.kwargs if k not in self.DEFAULT_ATTRS or self.kwargs[k] != self.DEFAULT_ATTRS[k]}
            if not children:
                if len(attrs) == 0:
                    return self._type
                if len(attrs) == 1:
                    if self.VALUE_ATTR is not None and self.VALUE_ATTR in attrs:
                        return {self._type: attrs[self.VALUE_ATTR]}
            res = {'type': self._type}
            res.update(attrs)
            if children:
                res['children'] = children
        return res


@register_layout
class TableList(_LayoutItem):
    DEFAULT_ATTRS = {'showIndexLabels': False,
       'overflow': 'scroll',
       'maxHeight': 200,
       'minHeight': 100,
       'showPaging': True,
       'numberOfItemsPerPage': 15
       }

    def __init__(self, name, **kwargs):
        super(TableList, self).__init__(name=name, **kwargs)


@register_layout
class TableMatrix(_LayoutItem):
    DEFAULT_ATTRS = {'horizontalTitle': '',
       'verticalTitle': '',
       'drawElementMethod': None,
       'resizableColumns': True,
       'itemHeight': 20,
       'isReadOnly': False,
       'transpose': False
       }


@register_layout
class TriangularMatrix(_LayoutItem):
    DEFAULT_ATTRS = {}


@register_layout
class Group(_LayoutItem):

    def __init__(self, name, **kwargs):
        super(Group, self).__init__(name=name, **kwargs)


@register_layout
class TabGroup(Group):
    Top = 0
    Bottom = 1
    Left = 2
    Right = 3
    DEFAULT_ATTRS = {'tabPosition': Top
       }


@register_layout
class BoxGroup(Group):
    DEFAULT_ATTRS = {'enableFolding': True}

    def __init__(self, name, enableFolding=True, **kwargs):
        super(BoxGroup, self).__init__(name, enableFolding=enableFolding, **kwargs)


@register_layout
class VerticalGroup(Group):

    def __init__(self, name, **kwargs):
        super(VerticalGroup, self).__init__(name, **kwargs)


@register_layout
class HorizontalGroup(Group):

    def __init__(self, name, **kwargs):
        super(HorizontalGroup, self).__init__(name, **kwargs)


@register_layout
class ResponsiveGroup(Group):
    DEFAULT_ATTRS = {'rowSpacing': 1,
       'columnSpacing': 1,
       'minimumColumnWidth': -1
       }

    def __init__(self, name, **kwargs):
        super(ResponsiveGroup, self).__init__(name, **kwargs)


@register_layout
class ToggleGroup(Group):
    DEFAULT_ATTRS = {'enableFolding': False}

    def __init__(self, name, enableFolding=False, **kwargs):
        super(ToggleGroup, self).__init__(name, enableFolding=enableFolding, **kwargs)


@register_layout
class TitleGroup(Group):

    def __init__(self, name, **kwargs):
        super(TitleGroup, self).__init__(name, **kwargs)


@register_layout
class GridGroup(Group):

    def __init__(self, name, enableFolding=False, **kwargs):
        super(GridGroup, self).__init__(name, enableFolding=enableFolding, **kwargs)


@register_layout
class GridGroupItem(Group):

    def __init__(self, enableFolding=False, **kwargs):
        super(GridGroupItem, self).__init__(name='', nenableFolding=enableFolding, **kwargs)


@register_layout
class LayoutRoot(_LayoutItem):
    TYPE = 'Root'

    def __init__(self, **kwargs):
        super(LayoutRoot, self).__init__(**kwargs)


@register_layout
class Category(_LayoutItem):

    def __init__(self, name, **kwargs):
        super(Category, self).__init__(name=name, **kwargs)


@register_layout
class PropertyItem(_LayoutItem):
    TYPE = 'Property'
    VALUE_ATTR = 'attr'

    def __init__(self, attr, **kwargs):
        super(PropertyItem, self).__init__(attr=attr, **kwargs)


@register_layout
class Br(_LayoutItem):

    def __init__(self, space=12, **kwargs):
        super(Br, self).__init__(space=space, **kwargs)


@register_layout
class HelpBox(_LayoutItem):
    TYPE_INFO = 'Info'
    TYPE_WARNING = 'Warning'
    TYPE_ERROR = 'Error'
    TYPE_NONE = 'None'
    DEFAULT_ATTRS = {'infoType': TYPE_INFO}
    VALUE_ATTR = 'message'

    def __init__(self, message, infoType=TYPE_INFO, detailMessage='', **kwargs):
        super(HelpBox, self).__init__(message=message, infoType=infoType, detailMessage=detailMessage, **kwargs)


@register_layout
class Head(_LayoutItem):
    VALUE_ATTR = 'text'

    def __init__(self, text, **kwargs):
        super(Head, self).__init__(text=text, **kwargs)


@register_layout
class Title(_LayoutItem):
    VALUE_ATTR = 'text'
    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'center'

    def __init__(self, text, subTitle='', alignment=None, bold=True, horizontalLine=False, **kwargs):
        super(Title, self).__init__(text=text, subTitle=subTitle, alignment=alignment, bold=bold, horizontalLine=horizontalLine, **kwargs)


class ProgressBar(object):

    def __init__(self, text='%p%', segmentNum=1, radioLevel=None, colorLevel=None, **kwargs):
        self.data = {'text': text,
           'segmentNum': segmentNum,
           'radioLevel': radioLevel if radioLevel is not None else [],
           'colorLevel': colorLevel if colorLevel is not None else []
           }
        self.data.update(kwargs)
        return


if __name__ == '__main__':
    layout = LayoutRoot()[Category('UnCategorized')[PropertyItem('testInt'), HelpBox('What are you doing', visibleCondition='p["testInt"] > 0')], Category('Whatever')[PropertyItem('enabled'), Br(), Head('This is a head'), HorizontalGroup('Horizontal Group 1')[BoxGroup('Box Group 1')[PropertyItem('strategy'), PropertyItem('targets')], BoxGroup('Box Group 2')[PropertyItem('Start'), PropertyItem('Stop')], BoxGroup('Box Group 3')]]]
    d = layout.Serialize(True)
    import yaml
    print yaml.safe_dump(d, sort_keys=False, allow_unicode=True)