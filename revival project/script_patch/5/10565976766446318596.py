# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCAsyncContainer.py
from __future__ import absolute_import
from six.moves import range
import six
from common.uisys.ui_proxy import ProxyClass
from .CCContainer import CCContainer
import math
from .CCNode import CCNode
from common.utils.cocos_utils import ccp

@ProxyClass()
class CCAsyncContainer(CCContainer):

    def __init__(self, node):
        super(CCAsyncContainer, self).__init__(node)
        self._arrUpdatePos = []
        self._is_item_model_init = False

    def SetInitCount(self, nCurCount):
        nCount = len(self._child_item)
        if nCurCount == nCount:
            return
        else:
            if nCurCount > nCount:
                if self._customizeConf and len(self._customizeConf) > nCount:
                    uisystem = global_data.uisystem
                    for i in range(nCurCount - nCount):
                        if len(self._customizeConf) > i + nCount:
                            info = self._customizeConf[i + nCount]
                        else:
                            info = None
                        if info:
                            template = uisystem.load_template(info['template'], info.get('template_info', None))
                            self.AddItem(template, None, False)
                        else:
                            self.AddItem(self._templateConf, None, False)

                else:
                    for i in range(nCurCount - nCount):
                        self.AddItem(self._templateConf, None, False)

            else:
                for i in range(nCount - nCurCount):
                    self.DeleteItemIndex(nCount - i - 1, False)

            self._refreshItemPos()
            return

    def AddItem(self, conf, index=None, bRefresh=True):
        if index:
            self._child_item.insert(index, conf)
        else:
            self._child_item.append(conf)
        self._nUnit = math.ceil(len(self._child_item) * 1.0 / self._nNumPerUnit)
        if bRefresh:
            self._refreshItemPos()

    def DeleteAllSubItem(self):
        if len(self._child_item) == 0:
            return
        for v in self._child_item:
            if isinstance(v, CCNode):
                v.Destroy()

        self._child_item = []
        self._nUnit = 0
        self._refreshItemPos()
        return True

    def DeleteItemIndex(self, index, bRefresh=True):
        if isinstance(self._child_item[index], CCNode):
            self._child_item[index].Destroy()
        del self._child_item[index]
        self._nUnit = math.ceil(len(self._child_item) * 1.0 / self._nNumPerUnit)
        if bRefresh:
            self._refreshItemPos()

    def DoLoadItem(self, index):
        if index >= len(self._child_item):
            return
        else:
            conf = self._child_item[index]
            if type(conf) == dict:
                cahce_item = None
                if self._enable_global_item_pool and global_data.item_cache_without_check:
                    cahce_item = global_data.item_cache_without_check.pop_item_by_json(self._templatePath, lambda cache_node: self._nodeContainer.AddChild(None, cache_node))
                if not cahce_item:
                    ctrl = global_data.uisystem.create_item(conf)
                    self._nodeContainer.AddChild(None, ctrl)
                else:
                    ctrl = cahce_item
                ctrl.setAnchorPoint(ccp(0, 1))
                ctrl.setPosition(*self._arrUpdatePos[index])
                self._arrUpdatePos[index] = None
                self._child_item[index] = ctrl
                return ctrl
            if type(conf) in [six.text_type, str]:
                cahce_item = None
                if self._enable_global_item_pool and global_data.item_cache_without_check:
                    cahce_item = global_data.item_cache_without_check.pop_item_by_json(self._templatePath, lambda cache_node: self._nodeContainer.AddChild(None, cache_node))
                if not cahce_item:
                    from common.uisys import cocomate
                    if not self._is_item_model_init:
                        cocomate.do_cocomate_layout(self._list_view.getItemModel(), True, True)
                        self._is_item_model_init = True
                    new_item = self._list_view.getItemModel().clone()
                    cocomate.bind_child(new_item, is_clone=True)
                    bind_item = cocomate.get_cocomate_node_by_cocos_node(new_item)
                    ctrl = bind_item
                    self._nodeContainer.AddChild(None, ctrl)
                else:
                    ctrl = cahce_item
                ctrl.setAnchorPoint(ccp(0, 1))
                ctrl.setPosition(*self._arrUpdatePos[index])
                self._arrUpdatePos[index] = None
                self._child_item[index] = ctrl
                return ctrl
            return

    def GetItem(self, index):
        item = super(CCAsyncContainer, self).GetItem(index)
        if type(item) == dict:
            return None
        else:
            if type(item) in (six.text_type, str):
                return None
            return item
            return None

    def csb_init_with_scrollview(self, list_view):
        super(CCAsyncContainer, self).csb_init_with_scrollview(list_view)
        from common.uisys.cocomate import get_csb_filename, LAYOUT_COCOMATE_COMPONENT_NAME
        self._templateSetting = get_csb_filename(list_view.getItemModel().getFileName())
        self._templateConf = self._templateSetting
        self._list_view = list_view
        self.SetInitCount = self.SetInitCount_CSB
        sz = list_view.getItemModel().getContentSize()
        self.SetCtrlSize(sz.width, sz.height)

    def Destroy(self, is_remove=True):
        super(CCAsyncContainer, self).Destroy(is_remove)
        self._list_view = None
        return

    def SetInitCount_CSB(self, nCurCount):
        nCount = len(self._child_item)
        from common.uisys import cocomate
        if nCurCount == nCount:
            return
        else:
            if nCurCount > nCount:
                if self._customizeConf and len(self._customizeConf) > nCount:
                    for i in range(nCurCount - nCount):
                        ui_item = self._customizeConf[i + nCount]
                        if ui_item:
                            new_item = ui_item.clone()
                            new_item.setVisible(True)
                            cocomate.bind_child(new_item, is_clone=True)
                            bind_item = cocomate.get_cocomate_node_by_cocos_node(new_item)
                            self.AddItemNode(bind_item, None, False)
                        else:
                            self.AddTemplateItem(None, False)

                else:
                    for i in range(nCurCount - nCount):
                        self.AddTemplateItem(None, False)

            else:
                for i in range(nCount - nCurCount):
                    self.DeleteItemIndex(nCount - i - 1, False)

            self._refreshItemPos()
            return