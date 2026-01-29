# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCContainer.py
from __future__ import absolute_import
from six.moves import range
import cc
from .CCNode import CCNode
from common.uisys.ui_proxy import ProxyClass
import math
from common.utils.cocos_utils import CCSize, CCSizeZero, ccp

@ProxyClass()
class CCContainer(CCNode):

    def __init__(self, node):
        super(CCContainer, self).__init__(node)
        self._child_item = []
        self._child_item_pool = []
        self._nHorzBorder = 0
        self._nVertBorder = 0
        self._nHorzIndent = 0
        self._nVertIndent = 0
        self._nNumPerUnit = 1
        self._nUnit = 0
        self._inverse_order = False
        self._templateConf = None
        self._templateSetting = (None, None)
        self._ctrlSize = None
        self._customizeConf = None
        self._item_size_getter = None
        self._enable_item_pool = False
        self._enable_global_item_pool = False
        self._had_update_auto_fit_in_this_frame = False
        return

    def csb_init_with_scrollview(self, list_view):
        if list_view:
            margin = list_view.GetMargin()
            self._nHorzBorder = margin.left
            self._nVertBorder = margin.top
            self._nHorzIndent = margin.right
            self._nVertIndent = margin.bottom
            self._nNumPerUnit = list_view.GetNumPerUnit()
        from common.uisys.cocomate import wrap_cocos_node, init_clone_base_node
        from .CCScrollView import VIEW_CUSTOMIZED_CHILD_TAG
        children = list_view.getInnerContainer().getProtectedChildrenByTag(VIEW_CUSTOMIZED_CHILD_TAG)
        for node in children:
            if not node.isVisible():
                log_error('CUSTOMIZED_CHILD is hide!!!!!')
            node.setVisible(False)

        self._customizeConf = [ init_clone_base_node(node) for node in children ]

    def _registerInnerEvent(self):
        super(CCContainer, self)._registerInnerEvent()
        self.AddChild('_nodeContainer', CCNode.Create())

    def SetContentSize(self, sw, sh):
        return self.getContentSize()

    def ForceSetContentSize(self, sw, sh):
        size = self.CalcSize(sw, sh)
        self.setContentSize(size)
        return size

    def _refreshItemPos(self, is_cal_visible=False):
        pass

    def GetUnitNum(self):
        return self._nUnit

    def GetNumPerUnit(self):
        return self._nNumPerUnit

    def GetHorzBorder(self):
        return self._nHorzBorder

    def GetVertBorder(self):
        return self._nVertBorder

    def GetHorzIndent(self):
        return self._nHorzIndent

    def GetVertIndent(self):
        return self._nVertIndent

    def GetTemplateConf(self):
        return self._templateConf

    def GetCtrlSize(self):
        return self._ctrlSize

    def SetCtrlSize(self, w, h):
        self._ctrlSize = CCSize(w, h)

    def SetNumPerUnit(self, nNum, is_refresh=True):
        if self._nNumPerUnit != nNum:
            self._nNumPerUnit = nNum
            self._nUnit = math.ceil(len(self._child_item) * 1.0 / self._nNumPerUnit)
            if is_refresh:
                self._refreshItemPos()

    def SetHorzBorder(self, nBorder):
        if self._nHorzBorder != nBorder:
            self._nHorzBorder = nBorder
            self._refreshItemPos()

    def SetVertBorder(self, nBorder):
        if self._nVertBorder != nBorder:
            self._nVertBorder = nBorder
            self._refreshItemPos()

    def SetHorzIndent(self, nIndent):
        if self._nHorzIndent != nIndent:
            self._nHorzIndent = nIndent
            self._refreshItemPos()

    def SetVertIndent(self, nIndent):
        if self._nVertIndent != nIndent:
            self._nVertIndent = nIndent
            self._refreshItemPos()

    def GetItem(self, index):
        try:
            return self._child_item[index]
        except:
            return None

        return None

    def GetItemCount(self):
        return len(self._child_item)

    def GetAllItem(self):
        return self._child_item

    def SetTemplate(self, templateName, templateInfo=None):
        if self._templateSetting == (templateName, templateInfo):
            return
        self._templatePath = templateName
        self._templateSetting = (templateName, templateInfo)
        self.SetTemplateConf(global_data.uisystem.load_template(templateName, templateInfo))

    def GetTemplateSetting(self):
        return self._templateSetting

    def GetTemplatePath(self):
        return self._templatePath

    def SetTemplateConf(self, conf):
        self._templateConf = conf
        try:
            self._ctrlSize = CCSize(conf['size']['width'], conf['size']['height'])
        except:
            self._ctrlSize = CCSizeZero

    def SetCustomizeConf(self, customizeConf):
        self._customizeConf = customizeConf

    def GetCustomizeConf(self):
        return self._customizeConf

    def SetInitCount(self, nCurCount):
        nCount = len(self._child_item)
        if nCurCount == nCount:
            if callable(self._item_size_getter):
                self._refreshItemPos()
            return
        else:
            ret = []
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
                            ret.append(self.AddItem(template, nCount + i, False))
                        else:
                            ret.append(self.AddTemplateItem(nCount + i, False))

                else:
                    for i in range(nCurCount - nCount):
                        ret.append(self.AddTemplateItem(nCount + i, False))

            else:
                for i in range(nCount - nCurCount):
                    self.DeleteItemIndex(nCount - i - 1, False)

            self._refreshItemPos()
            self.UpdateAutoFitChild()
            return ret

    def UpdateAutoFitChild--- This code section failed: ---

 213       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'nd_auto_fit'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_TRUE     16  'to 16'

 214      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 216      16  LOAD_FAST             0  'self'
          19  LOAD_ATTR             1  'nd_auto_fit'
          22  JUMP_IF_TRUE_OR_POP    28  'to 28'
          25  LOAD_CONST            0  ''
        28_0  COME_FROM                '22'
          28  STORE_FAST            1  'nd_auto_fit'

 217      31  LOAD_FAST             0  'self'
          34  LOAD_ATTR             3  'GetChildren'
          37  CALL_FUNCTION_0       0 
          40  STORE_FAST            2  'children'

 218      43  LOAD_FAST             2  'children'
          46  POP_JUMP_IF_TRUE     53  'to 53'

 219      49  LOAD_CONST            0  ''
          52  RETURN_END_IF    
        53_0  COME_FROM                '46'

 220      53  SETUP_LOOP          143  'to 199'
          56  LOAD_FAST             2  'children'
          59  GET_ITER         
          60  FOR_ITER            135  'to 198'
          63  STORE_FAST            3  'child'

 221      66  LOAD_FAST             1  'nd_auto_fit'
          69  LOAD_FAST             3  'child'
          72  COMPARE_OP            3  '!='
          75  POP_JUMP_IF_FALSE    91  'to 91'

 222      78  LOAD_FAST             3  'child'
          81  LOAD_ATTR             4  'ResizeAndPosition'
          84  CALL_FUNCTION_0       0 
          87  POP_TOP          
          88  JUMP_BACK            60  'to 60'

 224      91  LOAD_FAST             0  'self'
          94  LOAD_ATTR             5  'getContentSize'
          97  CALL_FUNCTION_0       0 
         100  STORE_FAST            4  'size'

 225     103  LOAD_FAST             1  'nd_auto_fit'
         106  LOAD_ATTR             6  'getAnchorPoint'
         109  CALL_FUNCTION_0       0 
         112  STORE_FAST            5  'anchor'

 226     115  LOAD_FAST             4  'size'
         118  LOAD_ATTR             7  'width'
         121  LOAD_FAST             5  'anchor'
         124  LOAD_ATTR             8  'x'
         127  BINARY_MULTIPLY  
         128  STORE_FAST            6  'x_pos'

 227     131  LOAD_FAST             4  'size'
         134  LOAD_ATTR             9  'height'
         137  LOAD_FAST             5  'anchor'
         140  LOAD_ATTR            10  'y'
         143  BINARY_MULTIPLY  
         144  STORE_FAST            7  'y_pos'

 228     147  LOAD_FAST             1  'nd_auto_fit'
         150  LOAD_ATTR            11  'setPosition'
         153  LOAD_GLOBAL          12  'cc'
         156  LOAD_ATTR            13  'Vec2'
         159  LOAD_FAST             6  'x_pos'
         162  LOAD_FAST             7  'y_pos'
         165  CALL_FUNCTION_2       2 
         168  CALL_FUNCTION_1       1 
         171  POP_TOP          

 229     172  LOAD_FAST             1  'nd_auto_fit'
         175  LOAD_ATTR            14  'setContentSize'
         178  LOAD_FAST             4  'size'
         181  CALL_FUNCTION_1       1 
         184  POP_TOP          

 230     185  LOAD_FAST             1  'nd_auto_fit'
         188  LOAD_ATTR            15  'ChildResizeAndPosition'
         191  CALL_FUNCTION_0       0 
         194  POP_TOP          
         195  JUMP_BACK            60  'to 60'
         198  POP_BLOCK        
       199_0  COME_FROM                '53'

 231     199  LOAD_FAST             0  'self'
         202  LOAD_ATTR            16  '_refreshItemPos'
         205  CALL_FUNCTION_0       0 
         208  POP_TOP          
         209  LOAD_CONST            0  ''
         212  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def SetInverse(self, inverse):
        self._inverse_order = inverse
        self._refreshItemPos()

    def RefreshItemPos(self, is_cal_visible=False):
        self._refreshItemPos(is_cal_visible=is_cal_visible)

    def AddControl(self, ctrl, index=None, bRefresh=True):
        self._nodeContainer.AddChild(None, ctrl)
        ctrl.setAnchorPoint(ccp(0, 1))
        if index is not None and index != len(self._child_item) + 1:
            self._child_item.insert(index, ctrl)
        else:
            self._child_item.append(ctrl)
        self._nUnit = math.ceil(len(self._child_item) * 1.0 / self._nNumPerUnit)
        if bRefresh:
            self._refreshItemPos()
            if not self._had_update_auto_fit_in_this_frame:
                self.DelayCall(0.015, self.CheckUpdateAutoFitChild)
            self._had_update_auto_fit_in_this_frame = True
        return ctrl

    def CheckUpdateAutoFitChild(self):
        self.UpdateAutoFitChild()
        self._had_update_auto_fit_in_this_frame = False

    def _getItemContentSize(self, idx, item):
        if callable(self._item_size_getter):
            return self._item_size_getter(idx, item)
        else:
            return item.GetContentSize()

    def SetItemSizeGetter(self, template_size_getter):
        self._item_size_getter = template_size_getter

    def ReverseItem(self):
        if self._child_item:
            self._child_item.reverse()
            self._refreshItemPos()

    def AddItemNode(self, item, index, bRefresh=True, conf=None):
        ret = self.AddControl(item, index, bRefresh)
        if self._templateConf:
            templateConfPath = self._templateConf.get('ccbFile', None) or self._templateConf.get('recorded_template_path', None)
        else:
            templateConfPath = ''
        if conf:
            addPath = conf.get('ccbFile', None) or conf.get('recorded_template_path', None)
        else:
            addPath = ''
        if templateConfPath == addPath and ret:
            global_data.uisystem.BindWidgetSoundName(self._templatePath, ret)
        return ret

    def AddItem(self, conf, index=None, bRefresh=True):
        item = global_data.uisystem.create_item(conf)
        ret = self.AddItemNode(item, index, bRefresh, conf)
        return ret

    def AddTemplateItem(self, index=None, bRefresh=True):
        if self._enable_item_pool:
            item = self.GetReuseItem()
            if item:
                return self.AddItemNode(item, index, bRefresh, item.GetConf())
        if self._enable_global_item_pool and global_data.item_cache_without_check:
            item = global_data.item_cache_without_check.pop_item_by_json(self._templatePath, lambda cache_node: self.AddItemNode(cache_node, index, bRefresh, cache_node.GetConf()))
            if item:
                return item
        return self.AddItem(self._templateConf, index, bRefresh)

    def DeleteAllSubItem(self):
        if len(self._child_item) == 0:
            return
        if not self._enable_item_pool:
            for v in self._child_item:
                v.Destroy()

        else:
            self.RecycleAllItem(False)
        self._child_item = []
        self._nUnit = 0
        self._refreshItemPos()
        return True

    def StopAllSubItemActionByTag(self, tag_id):
        for nd_item in self._child_item:
            nd_item.stopActionByTag(tag_id)

        for nd_item in self._child_item_pool:
            nd_item.stopActionByTag(tag_id)

    def DeleteItem(self, nd, refresh=True):
        if nd in self._child_item:
            index = self._child_item.index(nd)
            self.DeleteItemIndex(index, refresh)

    def DeleteItemIndex(self, index, bRefresh=True):
        if not self._enable_item_pool:
            self._child_item[index].Destroy()
            del self._child_item[index]
            self._nUnit = math.ceil(len(self._child_item) * 1.0 / self._nNumPerUnit)
        else:
            nd = self._child_item[index]
            self.RecycleItem(nd, refresh=False)
        if bRefresh:
            self._refreshItemPos()

    def DetachItemIndex(self, index, bRefresh=True):
        child_item = self._child_item[index]
        if child_item and child_item.isValid():
            child_item.Detach()
        del self._child_item[index]
        self._nUnit = math.ceil(len(self._child_item) * 1.0 / self._nNumPerUnit)
        if bRefresh:
            self._refreshItemPos()

    def RecycleAllItem(self, refresh=True):
        self._child_item_pool += self._child_item
        for item in self._child_item:
            item.setVisible(False)

        self._child_item = []
        self._nUnit = 0
        if refresh:
            self._refreshItemPos()

    def RecycleItem(self, nd, refresh=True):
        if nd in self._child_item:
            nd.setVisible(False)
            self._child_item.remove(nd)
            self._nUnit = math.ceil(len(self._child_item) * 1.0 / self._nNumPerUnit)
            if refresh:
                self._refreshItemPos()
            self._child_item_pool.append(nd)
            return True
        else:
            return False

    def ReuseItemByNode(self, node, bRefresh=True):
        if not self._child_item_pool:
            return None
        else:
            if node not in self._child_item_pool:
                return None
            self._child_item_pool.remove(node)
            ctrl = node
            ctrl.setVisible(True)
            self._child_item.append(ctrl)
            self._nUnit = math.ceil(len(self._child_item) * 1.0 / self._nNumPerUnit)
            if bRefresh:
                self._refreshItemPos()
            return ctrl

    def ReuseItem(self, bRefresh=True):
        if not self._child_item_pool:
            return None
        else:
            ctrl = self._child_item_pool.pop()
            ctrl.setVisible(True)
            self._child_item.append(ctrl)
            self._nUnit = math.ceil(len(self._child_item) * 1.0 / self._nNumPerUnit)
            if bRefresh:
                self._refreshItemPos()
            return ctrl

    def GetReuseItem(self):
        if not self._child_item_pool:
            return None
        else:
            ctrl = self._child_item_pool.pop()
            ctrl.setVisible(True)
            return ctrl

    def Destroy(self, is_remove=True):
        if self._enable_global_item_pool and global_data.item_cache_without_check:
            for ui_item in self._child_item:
                if isinstance(ui_item, CCNode):
                    global_data.item_cache_without_check.put_back_item_to_cache(ui_item, self._templatePath)

            for ui_item in self._child_item_pool:
                if isinstance(ui_item, CCNode):
                    global_data.item_cache_without_check.put_back_item_to_cache(ui_item, self._templatePath)

        super(CCContainer, self).Destroy(is_remove)
        self._child_item = []
        self._child_item_pool = []
        self._item_size_getter = None
        self._had_update_auto_fit_in_this_frame = False
        return

    def DeleteItemByTag(self, tag, bRefresh=True):
        idx, del_idx = (0, -1)
        for child in self._child_item:
            if child.getTag() == tag:
                del_idx = idx
                break
            idx += 1

        if del_idx >= 0:
            self.DeleteItemIndex(del_idx, bRefresh)

    def GetItemByTag(self, tag):
        for child in self._child_item:
            if child.getTag() == tag:
                return child

        return None

    def getIndexByItem(self, item):
        for index, child in enumerate(self._child_item):
            if child == item:
                return index

        return None

    def EnableItemAutoPool(self, enable):
        self._enable_item_pool = enable

    def EnableGlobalItemAutoPool(self, enable):
        self._enable_global_item_pool = enable