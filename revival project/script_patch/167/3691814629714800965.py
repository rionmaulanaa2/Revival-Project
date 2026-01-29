# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/NewCCUIListView.py
from __future__ import absolute_import
import six
import ccui
import cc
import ccext
from common.utils.cocos_utils import CCSize, ccp
from common.uisys.ui_proxy import ProxyClass, trans2ProxyObj
from .CCScrollView import CCScrollView
from .ScrollList import ScrollRecycleHelper
from common.uisys.uielment.CCNode import CCNode
from common.uisys.uielment.CCHorzAsyncList import CCHorzAsyncList
from common.uisys.uielment.CCVerAsyncList import CCVerAsyncList
from common.uisys.uielment.CCHorzAsyncContainer import CCHorzAsyncContainer
from common.uisys.uielment.CCVerAsyncContainer import CCVerAsyncContainer

class FakeContainer(object):

    def __init__(self, inner_container, sv):
        self._inner_container = inner_container
        self._sv = sv

    def destroy(self):
        self._inner_container = None
        self._sv = None
        return

    def GetContentSize(self):
        sz = self._sv.getBoundsContentSize()
        return (
         sz.width, sz.height)

    def getContentSize(self):
        return self._sv.getBoundsContentSize()

    def __getattr__(self, aname):
        attr = getattr(self._inner_container, aname)
        if attr is None:
            raise AttributeError(aname)
        else:
            return attr
        return


@ProxyClass(ccui.ListView)
class NewCCUIListView(CCScrollView, ScrollRecycleHelper):
    DIRE_VERTICAL = 1
    DIRE_HORIZONTAL = 2
    DIRE_BOTH = 3

    def __init__(self, node):
        self._direction = node.getDirection()
        from common.uisys import cocomate
        self._is_item_model_init = False
        self.item_model = node.getItemModel()
        super(NewCCUIListView, self).__init__(node)
        self.removeAllItems()
        self.mate_items = list()
        self._bottom_margin = 0
        self._layoutCount = 0
        self._layoutItemIdx = 0
        self.item_init_func, self.item_update_func = (None, None)
        self._inverse_order = False
        self._customizeConf = []
        self._container = FakeContainer(self.inner_container, self)
        self.scroll_enabled = False
        self._enable_item_pool = False
        self._child_item_pool = []
        self._to_be_release_pool = []
        return None

    def SyncAttrToContainer--- This code section failed: ---

  80       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('wrap_cocos_node', 'init_clone_base_node', 'do_cocomate_layout')
           6  IMPORT_NAME           0  'common.uisys.cocomate'
           9  IMPORT_FROM           1  'wrap_cocos_node'
          12  STORE_FAST            1  'wrap_cocos_node'
          15  IMPORT_FROM           2  'init_clone_base_node'
          18  STORE_FAST            2  'init_clone_base_node'
          21  IMPORT_FROM           3  'do_cocomate_layout'
          24  STORE_FAST            3  'do_cocomate_layout'
          27  POP_TOP          

  81      28  LOAD_CONST            3  1
          31  LOAD_CONST            4  ('VIEW_CUSTOMIZED_CHILD_TAG',)
          34  IMPORT_NAME           4  'CCScrollView'
          37  IMPORT_FROM           5  'VIEW_CUSTOMIZED_CHILD_TAG'
          40  STORE_FAST            4  'VIEW_CUSTOMIZED_CHILD_TAG'
          43  POP_TOP          

  82      44  LOAD_FAST             0  'self'
          47  LOAD_ATTR             6  'getInnerContainer'
          50  CALL_FUNCTION_0       0 
          53  LOAD_ATTR             7  'getProtectedChildrenByTag'
          56  LOAD_FAST             4  'VIEW_CUSTOMIZED_CHILD_TAG'
          59  CALL_FUNCTION_1       1 
          62  STORE_FAST            5  'children'

  83      65  SETUP_LOOP           52  'to 120'
          68  LOAD_FAST             5  'children'
          71  GET_ITER         
          72  FOR_ITER             44  'to 119'
          75  STORE_FAST            6  'node'

  84      78  LOAD_FAST             6  'node'
          81  LOAD_ATTR             8  'isVisible'
          84  CALL_FUNCTION_0       0 
          87  POP_JUMP_IF_TRUE    103  'to 103'

  85      90  LOAD_GLOBAL           9  'log_error'
          93  LOAD_CONST            5  'CUSTOMIZED_CHILD is hide on default!!!!!'
          96  CALL_FUNCTION_1       1 
          99  POP_TOP          
         100  JUMP_FORWARD          0  'to 103'
       103_0  COME_FROM                '100'

  86     103  LOAD_FAST             6  'node'
         106  LOAD_ATTR            10  'setVisible'
         109  LOAD_GLOBAL          11  'False'
         112  CALL_FUNCTION_1       1 
         115  POP_TOP          
         116  JUMP_BACK            72  'to 72'
         119  POP_BLOCK        
       120_0  COME_FROM                '65'

  87     120  BUILD_LIST_0          0 
         123  LOAD_FAST             5  'children'
         126  GET_ITER         
         127  FOR_ITER             18  'to 148'
         130  STORE_FAST            6  'node'
         133  LOAD_FAST             2  'init_clone_base_node'
         136  LOAD_FAST             6  'node'
         139  CALL_FUNCTION_1       1 
         142  LIST_APPEND           2  ''
         145  JUMP_BACK           127  'to 127'
         148  LOAD_FAST             0  'self'
         151  STORE_ATTR           12  '_customizeConf'

  89     154  LOAD_CONST            1  ''
         157  LOAD_CONST            6  ('cocomate',)
         160  IMPORT_NAME          13  'common.uisys'
         163  IMPORT_FROM          14  'cocomate'
         166  STORE_FAST            7  'cocomate'
         169  POP_TOP          

  90     170  LOAD_FAST             7  'cocomate'
         173  LOAD_ATTR            15  'get_ext_data'
         176  LOAD_ATTR             7  'getProtectedChildrenByTag'
         179  CALL_FUNCTION_2       2 
         182  STORE_FAST            8  'initCount'

  91     185  LOAD_FAST             8  'initCount'
         188  POP_JUMP_IF_FALSE   207  'to 207'

  92     191  LOAD_FAST             0  'self'
         194  LOAD_ATTR            16  'SetInitCount'
         197  LOAD_FAST             8  'initCount'
         200  CALL_FUNCTION_1       1 
         203  POP_TOP          
         204  JUMP_FORWARD         33  'to 240'

  95     207  LOAD_FAST             0  'self'
         210  LOAD_ATTR            17  '_FixMinContentSize'
         213  CALL_FUNCTION_0       0 
         216  POP_TOP          

  96     217  LOAD_FAST             0  'self'
         220  LOAD_ATTR            18  'DoLayout'
         223  LOAD_GLOBAL          19  'True'
         226  CALL_FUNCTION_1       1 
         229  POP_TOP          

  97     230  LOAD_FAST             0  'self'
         233  LOAD_ATTR            20  'UpdateAutoFitChild'
         236  CALL_FUNCTION_0       0 
         239  POP_TOP          
       240_0  COME_FROM                '204'

  98     240  LOAD_GLOBAL          21  'setattr'
         243  LOAD_FAST             0  'self'
         246  LOAD_ATTR            22  'inner_container'
         249  LOAD_CONST            8  '_child_item'
         252  LOAD_FAST             0  'self'
         255  LOAD_ATTR            23  'mate_items'
         258  CALL_FUNCTION_3       3 
         261  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 179

    def csb_init(self):
        super(NewCCUIListView, self).csb_init()
        self.scroll_enabled = self.GetTypeName() in ('CCHorzTemplateList', 'CCVerTemplateList')
        if not self.scroll_enabled:
            self.SetTouchEnabled(False)

    @property
    def item_count(self):
        return self.mate_items.__len__()

    def SetSkipInvisible(self, skip):
        self.setSkipInvisible(skip)

    def GetVisibleItemCount(self):
        return len([ x.IsVisible() for x in self.mate_items ])

    def SetLayoutCount(self, nMinCount, item_idx):
        self._layoutCount = nMinCount
        self._layoutItemIdx = item_idx

    def _OnItemsCountChange(self):
        while self.item_count < self._layoutCount:
            item = self.GetItem(self._layoutItemIdx) or self.item_model
            new_item = self._InsertItem(item=item.clone(), trigger=False)
            new_item.SetVisible(False)

    def SetItemIdx(self, idx, new_idx):
        item = self.mate_items.pop(idx)
        cocos_item = item.get()
        cocos_item.retain()
        self.removeItem(idx)
        self.insertCustomItem(cocos_item, new_idx)
        cocos_item.release()
        self.mate_items.insert(new_idx, item)

    def DoItemsUpdate(self):
        if self.item_update_func:
            for item in self.mate_items:
                self.item_update_func(item, self)

    def UpdateSelfContentSize(self, force=False):
        sz = self.GetInnerContainer().getContentSize()
        width = sz.width
        height = sz.height
        if self.scroll_enabled:
            if not force:
                return
            if self.GetDirection() == self.DIRE_HORIZONTAL:
                self.SetContentSize(self.GetContentSize()[0], max(self.GetContentSize()[1], height))
            elif self.GetDirection() == self.DIRE_VERTICAL:
                self.SetContentSize(max(self.GetContentSize()[0], width), self.GetContentSize()[1])
        elif self.GetDirection() == self.DIRE_HORIZONTAL:
            self.SetContentSize(width, max(self.GetContentSize()[1], height))
        elif self.GetDirection() == self.DIRE_VERTICAL:
            self.SetContentSize(max(self.GetContentSize()[0], width), height)

    def GetDirection(self):
        return self.getDirection()

    def PushBackItem(self, index):
        from common.uisys import cocomate
        if index < len(self._customizeConf):
            new_item = self._customizeConf[index].clone()
            new_item.setVisible(True)
            cocomate.bind_child(new_item, is_clone=False)
            bind_item = cocomate.get_cocomate_node_by_cocos_node(new_item)
            self.pushBackCustomItem(bind_item.get())
            self.mate_items.append(bind_item)
            self._OnItemsCountChange()
            return bind_item
        else:
            return self.PushDefaultItem()

    def PushDefaultItem(self):
        item = self.PullItemFromPool()
        self.pushBackCustomItem(item.get())
        self.check_temp_release_pool(item)
        self.mate_items.append(item)
        self._OnItemsCountChange()
        return item

    def PullItemFromPool(self):
        bind_item = self._GetReuseItem()
        if not bind_item:
            from common.uisys import cocomate
            if not self._is_item_model_init:
                cocomate.bind_names(None, self.item_model, None, None, None)
                cocomate.do_cocomate_layout(self.item_model, True, True)
                self._is_item_model_init = True
            new_item = self.item_model.clone()
            cocomate.bind_child(new_item, is_clone=True)
            bind_item = cocomate.get_cocomate_node_by_cocos_node(new_item)
        return bind_item

    def RemoveLastItem(self):
        ui_item = self.mate_items.pop(-1)
        ui_item and ui_item.Destroy(False)
        self.removeLastItem()
        self._OnItemsCountChange()

    def _FixMinContentSize(self):
        if self.GetNumPerUnit() == 1:
            model_size = self.item_model.getContentSize()
            ori_size = self.GetContentSize()
            if self.scroll_enabled:
                if self.GetDirection() == self.DIRE_VERTICAL and ori_size[0] < model_size.width:
                    self.SetContentSize(model_size.width + self.GetHorzBorder() * 2, ori_size[1])
                elif self.GetDirection() == self.DIRE_HORIZONTAL and ori_size[1] < model_size.height:
                    self.SetContentSize(ori_size[0], model_size.height + self.GetVertBorder() * 2)
            elif self.GetDirection() == self.DIRE_VERTICAL:
                self.SetContentSize(model_size.width + self.GetHorzBorder() * 2, 0)
            elif self.GetDirection() == self.DIRE_HORIZONTAL:
                self.SetContentSize(0, model_size.height + self.GetVertBorder() * 2)

    def SetInverse(self, inverse):
        self._inverse_order = inverse
        self.inner_container.setLayoutInverse(inverse)
        self.inner_container._refreshItemPos()

    def DoLayout(self, force=False, update=False):
        force and self._ZeroContentSize()
        self.forceDoLayout() if force else self.doLayout()
        self.UpdateSelfContentSize(force)
        update and self.DoItemsUpdate()

    def _ZeroContentSize(self):
        if self.GetNumPerUnit() <= 1:
            return
        if not self.scroll_enabled:
            if self.GetDirection() == self.DIRE_HORIZONTAL:
                self.SetContentSize(self.GetContentSize()[0], 0)
            elif self.GetDirection() == self.DIRE_VERTICAL:
                self.SetContentSize(0, self.GetContentSize()[1])
            else:
                self.SetContentSize(0, 0)
            return

    def _set_up_ctrl(self, ctrl):
        ctrl.SetNoEventAfterMoveRecursion(True, 10)

    def _InsertItem(self, index=None, item=None, trigger=True):
        from common.uisys import cocomate
        if index is None:
            index = self.item_count if 1 else index
            if item:
                isinstance(item, CCNode) or cocomate.bind_child(item)
                item = cocomate.get_cocomate_node_by_cocos_node(item)
        else:
            item = self.PullItemFromPool()
        self._set_up_ctrl(item)
        self.insertCustomItem(item.get(), index)
        self.check_temp_release_pool(item)
        self.mate_items.insert(index, item)
        trigger and self._OnItemsCountChange()
        return item

    def SetForceH(self, height):
        pass

    def ForceSetContentSize(self, sw, sh):
        size = self.CalcSize(sw, sh)
        self.setContentSize(size)
        return size

    def _PopItem(self, index=-1):
        if index == -1:
            self.RemoveLastItem()
            return
        ui_item = self.mate_items.pop(index)
        ui_item.Destroy(False)
        self.removeItem(index)
        self._OnItemsCountChange()

    def SetContentSize(self, sw, sh):
        size = self.CalcSize(sw, sh)
        self.setContentSize(size)
        return size

    def FitViewSizeToContainerSize(self):
        sz = self.getContentSize()
        if self._direction == self.DIRE_VERTICAL:
            W = self.getBoundsWidth(True)
            sz.width = W
            self.setContentSize(sz)
            return sz
        else:
            H = self.getBoundsHeight(True)
            sz.height = H
            self.setContentSize(sz)
            return sz

    def _refreshItemPos(self, is_cal_scale=False):
        if not self.scroll_enabled:
            sz = self.getContentSize()
            if self._direction == self.DIRE_HORIZONTAL:
                W = self.getBoundsWidth(True)
                sz.width = W
                self.setContentSize(sz)
            else:
                H = self.getBoundsHeight(True)
                sz.height = H
                self.setContentSize(sz)
        elif self._direction == self.DIRE_VERTICAL:
            W, H = self.GetContentSize()
            CW, CH = self._container.GetContentSize()
            if W != CW:
                W = CW
                self.setContentSize(CCSize(W, H))
            sz = CCSize(max(CW, W), max(CH, H))
            self.SetInnerContentSize(sz.width, sz.height + self._bottom_margin)
            self._container.SetPosition(0, sz.height + self._bottom_margin)
        else:
            W, H = self.GetContentSize()
            CW, CH = self._container.GetContentSize()
            if H != CH:
                H = CH
                self.setContentSize(CCSize(W, H))
            sz = CCSize(max(CW, W), max(CH, H))
            self.SetInnerContentSize(sz.width, sz.height)
            self._container.SetPosition(0, sz.height)
        self.requestRefreshView()
        self.forceDoLayout()

    def GetItem(self, index, no_create=False):
        if index is None:
            return
        else:
            try:
                return self.mate_items[index]
            except IndexError:
                if no_create and index >= 0 and self.item_model is not None:
                    self.SetInitCount(index + 1)
                    return self.GetItem(index)
                return

            return

    def GetCtrlSize(self):
        if self.item_model:
            return self.item_model.getContentSize()
        return cc.Size(0, 0)

    def GetItemCount(self):
        return self.mate_items.__len__()

    def GetAllItem(self):
        return self.mate_items

    def getIndexByItem(self, item):
        try:
            return self.mate_items.index(item)
        except:
            return None

        return None

    def SetTemplate(self, templateName, templateInfo=None):
        if self._templateSetting == (templateName, templateInfo):
            return
        self._templatePath = templateName
        self._templateSetting = (templateName, templateInfo)
        nd = global_data.uisystem.load_template_create(templateName, templateInfo)
        self.setItemModel(nd.get())

    def GetTemplateSetting(self):
        return self._templateSetting

    def SetTemplateConf(self, conf):
        raise ValueError('unsupport function!')

    def GetTemplateConf(self):
        raise ValueError('unsupport function!')

    def GetTemplatePath(self):
        return self.item_model.getFileName()

    def SetCustomizeConf(self, customizeConf):
        raise ValueError('to be support!!!')

    def SetInitCount(self, count, need_load=True):
        ret = []
        if count > self.item_count and self.item_model is None:
            return ret
        else:
            if count == self.item_count:
                return ret
            while self.item_count > count:
                self.RemoveLastItem()

            while self.item_count < count:
                new_item = self.PushBackItem(self.item_count)
                ret.append(new_item)

            self._FixMinContentSize()
            self.DoLayout(True)
            self.UpdateAutoFitChild()
            return ret

    def UpdateAutoFitChild--- This code section failed: ---

 436       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'nd_auto_fit'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_TRUE     16  'to 16'

 437      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 438      16  LOAD_FAST             0  'self'
          19  LOAD_ATTR             1  'nd_auto_fit'
          22  JUMP_IF_TRUE_OR_POP    28  'to 28'
          25  LOAD_CONST            0  ''
        28_0  COME_FROM                '22'
          28  STORE_FAST            1  'nd_auto_fit'

 439      31  LOAD_FAST             0  'self'
          34  LOAD_ATTR             3  'GetScollViewChildren'
          37  CALL_FUNCTION_0       0 
          40  STORE_FAST            2  'children'

 440      43  LOAD_FAST             2  'children'
          46  POP_JUMP_IF_TRUE     53  'to 53'

 441      49  LOAD_CONST            0  ''
          52  RETURN_END_IF    
        53_0  COME_FROM                '46'

 442      53  SETUP_LOOP          149  'to 205'
          56  LOAD_FAST             2  'children'
          59  GET_ITER         
          60  FOR_ITER            141  'to 204'
          63  STORE_FAST            3  'child'

 443      66  LOAD_FAST             1  'nd_auto_fit'
          69  LOAD_FAST             3  'child'
          72  COMPARE_OP            3  '!='
          75  POP_JUMP_IF_FALSE    91  'to 91'

 444      78  LOAD_FAST             3  'child'
          81  LOAD_ATTR             4  'ResizeAndPosition'
          84  CALL_FUNCTION_0       0 
          87  POP_TOP          
          88  JUMP_BACK            60  'to 60'

 446      91  LOAD_FAST             0  'self'
          94  LOAD_ATTR             5  'GetInnerContainer'
          97  CALL_FUNCTION_0       0 
         100  LOAD_ATTR             6  'getContentSize'
         103  CALL_FUNCTION_0       0 
         106  STORE_FAST            4  'size'

 447     109  LOAD_FAST             1  'nd_auto_fit'
         112  LOAD_ATTR             7  'getAnchorPoint'
         115  CALL_FUNCTION_0       0 
         118  STORE_FAST            5  'anchor'

 448     121  LOAD_FAST             4  'size'
         124  LOAD_ATTR             8  'width'
         127  LOAD_FAST             5  'anchor'
         130  LOAD_ATTR             9  'x'
         133  BINARY_MULTIPLY  
         134  STORE_FAST            6  'x_pos'

 449     137  LOAD_FAST             4  'size'
         140  LOAD_ATTR            10  'height'
         143  LOAD_FAST             5  'anchor'
         146  LOAD_ATTR            11  'y'
         149  BINARY_MULTIPLY  
         150  STORE_FAST            7  'y_pos'

 450     153  LOAD_FAST             1  'nd_auto_fit'
         156  LOAD_ATTR            12  'setPosition'
         159  LOAD_GLOBAL          13  'cc'
         162  LOAD_ATTR            14  'Vec2'
         165  LOAD_FAST             6  'x_pos'
         168  LOAD_FAST             7  'y_pos'
         171  CALL_FUNCTION_2       2 
         174  CALL_FUNCTION_1       1 
         177  POP_TOP          

 451     178  LOAD_FAST             1  'nd_auto_fit'
         181  LOAD_ATTR            15  'setContentSize'
         184  LOAD_FAST             4  'size'
         187  CALL_FUNCTION_1       1 
         190  POP_TOP          

 452     191  LOAD_FAST             1  'nd_auto_fit'
         194  LOAD_ATTR            16  'ChildResizeAndPosition'
         197  CALL_FUNCTION_0       0 
         200  POP_TOP          
         201  JUMP_BACK            60  'to 60'
         204  POP_BLOCK        
       205_0  COME_FROM                '53'
         205  LOAD_CONST            0  ''
         208  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def RefreshItemPos(self, force=False):
        self._refreshItemPos()

    def AddTemplateItem(self, index=None, bRefresh=True):
        if self._enable_item_pool:
            item = self._GetReuseItem()
            if item:
                self.AddItemNode(item, index, bRefresh, item.GetTemplatePath())
                return item
        index = self.item_count if index is None else index
        self._InsertItem(index)
        self._FixMinContentSize()
        self.DoLayout(update=bRefresh)
        return self.GetItem(index)

    def DeleteItem(self, nd, refresh=True):
        if nd in self.mate_items:
            index = self.mate_items.index(nd)
            self.DeleteItemIndex(index, refresh)

    def DeleteItemIndex(self, index, bRefresh=True):
        if not self._enable_item_pool:
            self._PopItem(index)
        else:
            nd = self.mate_items[index]
            self.RecycleItem(nd, refresh=False)
        bRefresh and self.DoLayout()

    def DeleteAllSubItem(self):
        if not self._enable_item_pool:
            self.removeAllItems()
            self.mate_items = list()
            self._OnItemsCountChange()
        else:
            self.RecycleAllItem(True)
        self.DoLayout()

    def TransferAllSubItem(self):
        self.removeAllItems()
        self.mate_items = list()
        self._container._refreshItemPos()
        self._refreshItemPos()

    def LocatePosByItem(self, index, duration=0):
        item = self.GetItem(index)
        if item is None:
            return
        else:
            self.CenterWithNode(item, duration)
            return

    def Destroy(self, is_remove=True):
        super(NewCCUIListView, self).Destroy(is_remove)
        for ui_item in self.mate_items:
            ui_item.Destroy(False)

        for ui_item in self._child_item_pool:
            ui_item.Destroy(False)
            ui_item.release()

        if self._to_be_release_pool:
            log_error('list has leakage!!!!', self.widget_name, self._to_be_release_pool)
            for ui_item in self._to_be_release_pool:
                ui_item.Destroy(False)
                ui_item.release()

            self._to_be_release_pool = []
        if is_remove:
            self.removeAllItems()
        self.mate_items = list()
        self._child_item_pool = []

    def DeleteItemByTag(self, Tag, bRefresh=True):
        for ind, item in enumerate(self.mate_items):
            if item.getTag() == Tag:
                self.DeleteItemIndex(ind, bRefresh)

    def GetItemByTag(self, tag):
        for item in self.mate_items:
            if item.getTag() == tag:
                return item

        return None

    def AddItem(self, conf, index=None, bRefresh=True):
        if index is None:
            index = self.item_count if 1 else index
            if type(conf) not in [str, six.text_type]:
                raise ValueError('csb only support template path!')
            csb_path = conf
            if self.item_model and self.GetCSBFileName(self.item_model.getFileName()) == csb_path:
                item = self._InsertItem(index)
                return item
        nd = global_data.uisystem.load_template_create(csb_path)
        self._InsertItem(index, nd)
        self._FixMinContentSize()
        self.DoLayout(update=bRefresh)
        return nd

    def AddControl(self, ctrl, index=None, bRefresh=True, bSetupCtrl=True):
        index = self.item_count if index is None else index
        item = self._InsertItem(index, ctrl)
        self._FixMinContentSize()
        self.DoLayout(update=bRefresh)
        return item

    def SetItemSizeGetter(self, template_size_getter):
        self._container.SetItemSizeGetter(template_size_getter)

    def AddItemNode(self, item, index, bRefresh=True, conf=None):
        ret = self.AddControl(item, index, bRefresh)
        if self._templatePath == conf and ret:
            global_data.uisystem.BindWidgetSoundName(self._templatePath, ret)
        return ret

    def RecycleAllItem(self, refresh=True):
        self._child_item_pool += self.mate_items
        for item in self.mate_items:
            item.retain()
            item.setVisible(False)

        self.removeAllItems()
        self.mate_items = []
        if refresh:
            self._refreshItemPos()

    def RecycleItem(self, nd, refresh=True):
        if nd in self.mate_items:
            nd.setVisible(False)
            index = self.mate_items.index(nd)
            self.mate_items.remove(nd)
            if refresh:
                self._refreshItemPos()
            nd.retain()
            self.removeItem(index)
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
            ctrl = node
            ctrl.setVisible(True)
            self._child_item_pool.remove(ctrl)
            self._to_be_release_pool.append(ctrl)
            self.AddControl(ctrl, bRefresh=False)
            if bRefresh:
                self._refreshItemPos()
            return ctrl

    def check_temp_release_pool(self, item):
        if not self._to_be_release_pool:
            return
        if item in self._to_be_release_pool:
            self._to_be_release_pool.remove(item)
            item.release()

    def ReuseItem(self, bRefresh=True):
        if not self._child_item_pool:
            return None
        else:
            ctrl = self._child_item_pool.pop()
            self._to_be_release_pool.append(ctrl)
            self.AddControl(ctrl, bRefresh=False)
            ctrl.setVisible(True)
            if bRefresh:
                self._refreshItemPos()
            return ctrl

    def _GetReuseItem(self):
        if not self._child_item_pool:
            return None
        else:
            ctrl = self._child_item_pool.pop()
            ctrl.setVisible(True)
            self._to_be_release_pool.append(ctrl)
            return ctrl

    def DetachItemIndex(self, index=None, bRefresh=True):
        nd = self.mate_items[index]
        self.RecycleItem(nd, refresh=False)
        bRefresh and self.DoLayout()

    def EnableItemAutoPool(self, enable):
        self._enable_item_pool = enable
        self.setSkipInvisible(True)

    def SetClippingEnabled(self, flag):
        return self.setClippingEnabled(flag)

    def GetScollViewChildren(self):
        from .CCScrollView import VIEW_CHILD_TAG
        ret = []
        if self._obj.isValid():
            for child in self._obj.getInnerContainer().getProtectedChildrenByTag(VIEW_CHILD_TAG):
                ret.append(trans2ProxyObj(child))

        return ret

    def GetNumPerUnit(self):
        return self.inner_container.getLayoutUnits()

    def SetNumPerUnit(self, num, is_refresh=True):
        self.inner_container.setLayoutUnits(num)
        if not self.scroll_enabled:
            self.FitViewSizeToContainerSize()

    def GetMargin(self):
        return self.inner_container.getMargin()

    def SetMargin(self, le=None, t=None, r=None, b=None):
        ori_margin = self.GetMargin()
        ori_margin.setMargin(ori_margin.left if le is None else le, ori_margin.top if t is None else t, ori_margin.right if r is None else r, ori_margin.bottom if b is None else b)
        self.setMargin(ori_margin)
        return

    def GetHorzBorder(self):
        return self.GetMargin().left

    def GetVertBorder(self):
        return self.GetMargin().top

    def GetHorzIndent(self):
        return self.GetMargin().right

    def GetVertIndent(self):
        return self.GetMargin().bottom

    def SetHorzBorder(self, nBorder):
        self.SetMargin(le=nBorder)

    def SetVertBorder(self, nBorder):
        self.SetMargin(t=nBorder)

    def SetHorzIndent(self, nIndent):
        self.SetMargin(r=nIndent)

    def SetVertIndent(self, nIndent):
        self.SetMargin(b=nIndent)

    def SetLayoutType(self, l_type):
        return self.setLayoutType(l_type)

    def GetLayoutType(self):
        return self.getLayoutType()

    def SetExtraBottomMargin(self, margin):
        W, H = self.GetContentSize()
        CW, CH = self._container.GetContentSize()
        width, height = max(CW, W), max(CH, H)
        pos = self.GetContentOffset()
        self.SetInnerContentSize(width, height + margin)
        self._container.SetPosition(0, height + margin)
        old_margin = self._bottom_margin
        self._bottom_margin = margin
        self.SetContentOffset(ccp(pos.x, pos.y - (margin - old_margin)))
        for child in self.GetChildren():
            if child.widget_name != '_container':
                if margin:
                    posy = child.getPositionY()
                    child.setPositionY(posy + (margin - old_margin))
                else:
                    child.ReConfPosition()


@ProxyClass(ccui.Widget)
class CCHorzAsyncContainer_CSB(CCHorzAsyncContainer):
    pass


@ProxyClass(ccui.Widget)
class CCVerAsyncContainer_CSB(CCVerAsyncContainer):
    pass


@ProxyClass(ccui.ListView)
class CCHorzAsyncList_CSB(CCHorzAsyncList):

    def __init__(self, node):
        super(CCHorzAsyncList, self).__init__(node, CCHorzAsyncContainer_CSB)
        self._lastScrollOffset = None
        self._left_visible_range = 1
        self._right_visible_range = 2
        return


@ProxyClass(ccui.ListView)
class CCVerAsyncList_CSB(CCVerAsyncList):

    def __init__(self, node):
        super(CCVerAsyncList, self).__init__(node, CCVerAsyncContainer_CSB)
        self._lastScrollOffset = None
        return