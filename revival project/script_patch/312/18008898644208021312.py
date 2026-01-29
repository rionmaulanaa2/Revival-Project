# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/ScrollList.py
from __future__ import absolute_import
from six.moves import range
import six
import math
from common.uisys.ui_proxy import ProxyClass
from .CCScrollView import CCScrollView
from .CCContainer import CCContainer
from .CCNode import CCNode
from common.utils.cocos_utils import ccp

class ScrollRecycleHelper(object):

    def AutoAddAndRemoveItem(self, s_index, data_list, data_count, add_msg_func, up_limit=100, down_limit=160, del_msg_func=None, is_only_add=False):
        s_count = self.GetItemCount()
        in_height = self.getInnerContainerSize().height
        out_height = self.getContentSize().height
        up_edge = out_height + up_limit
        down_edge = -down_limit
        pos_y = self.getInnerContainer().getPositionY()
        if in_height == out_height:
            return s_index
        item = self.GetItem(0)
        if not item:
            return s_index
        last_item = self.GetItem(s_count - 1)
        if not last_item:
            return s_index
        last_item_height = last_item.getContentSize().height
        first_item_height = self.GetItem(0).getContentSize().height
        vert_indent = self.GetVertIndent()
        top_y = pos_y + in_height - first_item_height
        down_y = pos_y
        if top_y > up_edge and not is_only_add:
            while top_y > up_edge:
                old_y = self.getInnerContainer().getPositionY()
                height = self.GetItem(0).getContentSize().height + vert_indent
                for idx in range(self.GetNumPerUnit()):
                    s_count -= 1
                    del_item = self.GetItem(0)
                    if del_msg_func:
                        del_msg_func(del_item, 0)
                        self.DetachItemIndex(0)
                    else:
                        self.DeleteItemIndex(0, False)

                self._container._refreshItemPos()
                self._refreshItemPos()
                top_y -= height
                new_y = self.getInnerContainer().getPositionY()
                posy = old_y
                self.getInnerContainer().setPositionY(posy)

        if down_y + last_item_height + vert_indent < down_edge and not is_only_add:
            while down_y + last_item_height + vert_indent < down_edge:
                height = self.GetCtrlSize().height + vert_indent
                old_y = self.getInnerContainer().getPositionY()
                for idx in range(self.GetNumPerUnit()):
                    s_count -= 1
                    s_index -= 1
                    del_item = self.GetItem(s_count)
                    height = del_item.getContentSize().height + vert_indent
                    if del_msg_func:
                        del_msg_func(del_item, s_count)
                        self.DetachItemIndex(s_count)
                    else:
                        self.DeleteItemIndex(s_count, False)

                self._container._refreshItemPos()
                self._refreshItemPos()
                down_y += height
                last_item_height = height
                posy = height + old_y
                self.getInnerContainer().setPositionY(posy)

        if top_y + first_item_height + vert_indent < up_edge and s_index - s_count + 1 > 0 and s_index - s_count + 1 < data_count:
            while top_y + first_item_height + vert_indent < up_edge and s_index - s_count + 1 > 0:
                old_y = self.getInnerContainer().getPositionY()
                height = self.GetCtrlSize().height
                old_row_num = math.ceil(s_count / float(self.GetNumPerUnit()))
                for idx in range(self.GetNumPerUnit()):
                    if s_index - s_count + 1 > 0:
                        s_count += 1
                        data = data_list[s_index - s_count + 1]
                        chat_pnl = add_msg_func(data, False, s_index - s_count + 1)
                        height = chat_pnl.getContentSize().height + vert_indent

                new_y = self.getInnerContainer().getPositionY()
                posy = new_y + (old_y - new_y)
                self._container._refreshItemPos()
                self._refreshItemPos()
                self.getInnerContainer().setPositionY(posy)
                new_row_num = math.ceil(s_count / float(self.GetNumPerUnit()))
                if new_row_num <= old_row_num:
                    height = 0
                top_y += height
                first_item_height = self.GetItem(0).getContentSize().height

        if down_y > down_edge and s_index < data_count - 1:
            while down_y > down_edge and s_index < data_count - 1:
                old_row_num = math.ceil(s_count / float(self.GetNumPerUnit()))
                height = self.GetCtrlSize().height + vert_indent
                old_y = self.getInnerContainer().getPositionY()
                for idx in range(self.GetNumPerUnit()):
                    if s_index < data_count - 1:
                        s_count += 1
                        s_index += 1
                        data = data_list[s_index]
                        chat_pnl = add_msg_func(data, True, s_index)
                        height = chat_pnl.getContentSize().height + vert_indent

                new_row_num = math.ceil(s_count / float(self.GetNumPerUnit()))
                if new_row_num <= old_row_num:
                    height = 0
                down_y -= height
                self._container._refreshItemPos()
                self._refreshItemPos()
                self.getInnerContainer().setPositionY(old_y - height)

        return s_index

    def AutoAddAndRemoveItemHorizontal(self, s_index, data_list, data_count, add_msg_func, left_limit=100, right_limit=160):
        s_count = self.GetItemCount()
        in_width = self.getInnerContainerSize().width
        out_width = self.getContentSize().width
        left_edge = -left_limit
        right_edge = out_width + right_limit
        pos_x = self.getInnerContainer().getPositionX()
        if pos_x > 0 or pos_x + in_width < out_width or in_width == out_width:
            return s_index
        first_item = self.GetItem(0)
        if not first_item:
            return s_index
        last_item = self.GetItem(s_count - 1)
        if not last_item:
            return s_index
        last_item_width = last_item.getContentSize().width
        first_item_width = first_item.getContentSize().width
        horz_indent = self.GetHorzIndent()
        left_x = pos_x
        right_x = pos_x + in_width
        if left_x < left_edge:
            while left_x < left_edge:
                old_x = self.getInnerContainer().getPositionX()
                s_count -= 1
                self.DeleteItemIndex(0)
                self.getInnerContainer().setPositionX(old_x + first_item_width)
                left_x = old_x + first_item_width

        elif left_x > left_edge + first_item_width and 0 <= s_index - s_count < data_count:
            while left_x > left_edge + first_item_width and s_index - s_count >= 0:
                old_x = self.getInnerContainer().getPositionX()
                data = data_list[s_index - s_count]
                s_count += 1
                add_msg_func(self, data, False, s_index - s_count + 1)
                self.getInnerContainer().setPositionX(old_x - first_item_width - horz_indent)
                left_x = old_x - first_item_width - horz_indent

        if right_x > right_edge:
            while right_x > right_edge:
                s_count -= 1
                s_index -= 1
                self.DeleteItemIndex(s_count)
                right_x -= last_item_width + horz_indent

        elif right_x + last_item_width < right_edge and s_index + 1 < data_count:
            while right_x + last_item_width < right_edge and s_index + 1 < data_count:
                s_count += 1
                s_index += 1
                data = data_list[s_index]
                add_msg_func(self, data, True, s_index)
                right_x += last_item_width + horz_indent

        return s_index

    def AutoAddAndRemoveItem_MulCol(self, s_index, data_list, data_count, add_msg_func, up_limit=100, down_limit=160, del_msg_func=None, ignore_height_check=False):
        s_count = self.GetItemCount()
        in_height = self.getInnerContainerSize().height
        out_height = self.getContentSize().height
        up_edge = out_height + up_limit
        down_edge = -down_limit
        pos_y = self.getInnerContainer().getPositionY()
        if not ignore_height_check:
            if pos_y + in_height < out_height or in_height == out_height:
                return s_index
        item = self.GetItem(0)
        if not item:
            return s_index
        last_item = self.GetItem(s_count - 1)
        if not last_item:
            return s_index
        last_item_height = last_item.getContentSize().height
        first_item_height = self.GetItem(0).getContentSize().height
        top_y = pos_y + in_height - first_item_height
        down_y = pos_y
        if top_y > up_edge:
            old_y = self.getInnerContainer().getPositionY()
            for idx in range(self.GetNumPerUnit()):
                s_count -= 1
                del_item = self.GetItem(0)
                if del_msg_func:
                    del_msg_func(del_item, 0)
                self.DeleteItemIndex(0)

            new_y = self.getInnerContainer().getPositionY()
            posy = old_y
            self.getInnerContainer().setPositionY(posy)
        elif top_y + first_item_height < up_edge and s_index - s_count + 1 > 0 and s_index - s_count + 1 < data_count:
            while top_y + first_item_height < up_edge and s_index - s_count + 1 > 0:
                old_y = self.getInnerContainer().getPositionY()
                height = self.GetCtrlSize().height
                for idx in range(self.GetNumPerUnit()):
                    if s_index - s_count + 1 > 0:
                        s_count += 1
                        data = data_list[s_index - s_count + 1]
                        chat_pnl = add_msg_func(data, False, s_index - s_count + 1)
                        height = chat_pnl.getContentSize().height

                new_y = self.getInnerContainer().getPositionY()
                posy = new_y + (old_y - new_y)
                self.getInnerContainer().setPositionY(posy)
                top_y += height
                first_item_height = self.GetItem(0).getContentSize().height

        if down_y + last_item_height < down_edge:
            s_count -= 1
            s_index -= 1
            old_y = self.getInnerContainer().getPositionY()
            old_in_height = self.getInnerContainerSize().height
            del_item = self.GetItem(s_count)
            if del_msg_func:
                del_msg_func(del_item, s_count)
            self.DeleteItemIndex(s_count)
            new_in_height = self.getInnerContainerSize().height
            new_y = self.getInnerContainer().getPositionY()
            height = old_in_height - new_in_height
            posy = height + old_y
            self.getInnerContainer().setPositionY(posy)
        elif down_y > down_edge and s_index < data_count - 1:
            while down_y > down_edge and s_index < data_count - 1:
                s_count += 1
                s_index += 1
                old_y = self.getInnerContainer().getPositionY()
                old_in_height = self.getInnerContainerSize().height
                data = data_list[s_index]
                chat_pnl = add_msg_func(data, True, s_index)
                height = chat_pnl.getContentSize().height
                down_y -= height
                self._container._refreshItemPos()
                self._refreshItemPos()
                new_in_height = self.getInnerContainerSize().height
                self.getInnerContainer().setPositionY(old_y - (new_in_height - old_in_height))

        return s_index

    def AutoAddAndRemoveItemEx(self, s_index, data_list, data_count, add_msg_func, pos_index, show_count, up_limit=100):
        s_count = show_count
        in_height = self.getInnerContainerSize().height
        out_height = self.getContentSize().height
        up_edge = out_height + up_limit
        pos_y = self.getInnerContainer().getPositionY()
        if in_height == out_height:
            return s_index
        item = self.GetItem(pos_index)
        if not item:
            return s_index
        index_item_height = item.getContentSize().height
        index_item_pos_y = item.getPosition().y
        top_y = pos_y + in_height + index_item_pos_y
        while top_y > up_edge and s_index + 1 < data_count:
            old_y = self.getInnerContainer().getPositionY()
            self.DeleteItemIndex(pos_index)
            s_index += 1
            data = data_list[s_index]
            chat_pnl = add_msg_func(data, pos_index + show_count - 1)
            height = chat_pnl.getContentSize().height
            posy = old_y - height
            self.getInnerContainer().setPositionY(posy)
            top_y -= height

        while top_y + index_item_height < up_edge and s_index - s_count > 0:
            old_y = self.getInnerContainer().getPositionY()
            self.DeleteItemIndex(pos_index + show_count - 1)
            s_index -= 1
            data = data_list[s_index - show_count]
            chat_pnl = add_msg_func(data, pos_index)
            height = chat_pnl.getContentSize().height
            posy = old_y + height
            self.getInnerContainer().setPositionY(posy)
            top_y += height

        return s_index

    def AutoAddAndRemoveItem_chat(self, s_index, data_list, data_count, add_msg_func, up_limit=100, down_limit=160):
        s_count = self.GetItemCount()
        in_height = self.getInnerContainerSize().height
        out_height = self.getContentSize().height
        up_edge = out_height + up_limit
        down_edge = -down_limit
        pos_y = self.getInnerContainer().getPositionY()
        if in_height == out_height:
            return s_index
        else:
            item = self.GetItem(0)
            if not item:
                return s_index
            last_item = self.GetItem(s_count - 1)
            if not last_item:
                return s_index
            last_item_height = last_item.getContentSize().height
            first_item_height = self.GetItem(0).getContentSize().height
            top_y = pos_y + in_height - first_item_height
            down_y = pos_y
            if top_y > up_edge:
                while top_y > up_edge:
                    if not self.GetItem(0):
                        break
                    old_y = self.getInnerContainer().getPositionY()
                    s_count -= 1
                    height = self.GetItem(0).getContentSize().height
                    self.DeleteItemIndex(0)
                    self.getInnerContainer().setPositionY(old_y)
                    top_y -= height

            elif top_y + first_item_height < up_edge and s_index - s_count + 1 > 0 and s_index - s_count + 1 < data_count:
                old_y = self.getInnerContainer().getPositionY()
                while top_y + first_item_height < up_edge and s_index - s_count + 1 > 0:
                    data = data_list[s_index - s_count]
                    chat_pnl = add_msg_func(data, False, s_index - s_count)
                    if chat_pnl is None:
                        del data_list[s_index - s_count]
                        s_index -= 1
                        data_count -= 1
                        continue
                    s_count += 1
                    height = chat_pnl.getContentSize().height
                    self._container._refreshItemPos()
                    self._refreshItemPos()
                    self.getInnerContainer().setPositionY(old_y)
                    top_y += height
                    first_item_height = self.GetItem(0).getContentSize().height

            if down_y + last_item_height < down_edge:
                while down_y + last_item_height < down_edge:
                    s_count -= 1
                    s_index -= 1
                    old_y = self.getInnerContainer().getPositionY()
                    height = self.GetItem(s_count).getContentSize().height
                    self.DeleteItemIndex(s_count)
                    posy = height + old_y
                    self.getInnerContainer().setPositionY(posy)
                    down_y += height
                    last_item_height = height

            elif down_y > down_edge and s_index < data_count - 1:
                while down_y > down_edge and s_index < data_count - 1:
                    old_y = self.getInnerContainer().getPositionY()
                    data = data_list[s_index + 1]
                    chat_pnl = add_msg_func(data, True, s_index + 1)
                    if chat_pnl is None:
                        del data_list[s_index + 1]
                        data_count -= 1
                        continue
                    s_count += 1
                    s_index += 1
                    height = chat_pnl.getContentSize().height
                    down_y -= height
                    self._container._refreshItemPos()
                    self._refreshItemPos()
                    self.getInnerContainer().setPositionY(old_y - height)

            return s_index


@ProxyClass()
class ScrollList(CCScrollView, ScrollRecycleHelper):

    def __init__(self, node, ContainerType):
        self._containerType = ContainerType
        super(ScrollList, self).__init__(node)

    def _registerInnerEvent(self):
        super(ScrollList, self)._registerInnerEvent()
        self.SetContainer(self._containerType.Create())
        self._container.setAnchorPoint(ccp(0, 1))

    def csb_init(self):
        super(ScrollList, self).csb_init()

    def SyncAttrToContainer--- This code section failed: ---

 474       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('cocomate',)
           6  IMPORT_NAME           0  'common.uisys'
           9  IMPORT_FROM           1  'cocomate'
          12  STORE_FAST            1  'cocomate'
          15  POP_TOP          

 478      16  LOAD_FAST             0  'self'
          19  LOAD_ATTR             2  'getMargin'
          22  CALL_FUNCTION_0       0 
          25  STORE_FAST            2  'margin'

 479      28  LOAD_FAST             2  'margin'
          31  LOAD_ATTR             3  'left'
          34  STORE_FAST            3  'horzBorder'

 480      37  LOAD_FAST             2  'margin'
          40  LOAD_ATTR             4  'top'
          43  STORE_FAST            4  'vertBorder'

 481      46  LOAD_FAST             2  'margin'
          49  LOAD_ATTR             5  'right'
          52  STORE_FAST            5  'horzIndent'

 482      55  LOAD_FAST             2  'margin'
          58  LOAD_ATTR             6  'bottom'
          61  STORE_FAST            6  'vertIndent'

 483      64  LOAD_FAST             0  'self'
          67  LOAD_ATTR             7  'getLayoutUnits'
          70  CALL_FUNCTION_0       0 
          73  STORE_FAST            7  'numPerUnit'

 485      76  LOAD_FAST             0  'self'
          79  STORE_FAST            8  'obj'

 486      82  LOAD_FAST             8  'obj'
          85  LOAD_ATTR             8  'SetNumPerUnit'
          88  LOAD_FAST             7  'numPerUnit'
          91  CALL_FUNCTION_1       1 
          94  POP_TOP          

 487      95  LOAD_FAST             8  'obj'
          98  LOAD_ATTR             9  'SetHorzBorder'
         101  LOAD_FAST             3  'horzBorder'
         104  CALL_FUNCTION_1       1 
         107  POP_TOP          

 488     108  LOAD_FAST             8  'obj'
         111  LOAD_ATTR            10  'SetVertBorder'
         114  LOAD_FAST             4  'vertBorder'
         117  CALL_FUNCTION_1       1 
         120  POP_TOP          

 489     121  LOAD_FAST             8  'obj'
         124  LOAD_ATTR            11  'SetHorzIndent'
         127  LOAD_FAST             5  'horzIndent'
         130  CALL_FUNCTION_1       1 
         133  POP_TOP          

 490     134  LOAD_FAST             8  'obj'
         137  LOAD_ATTR            12  'SetVertIndent'
         140  LOAD_FAST             6  'vertIndent'
         143  CALL_FUNCTION_1       1 
         146  POP_TOP          

 498     147  LOAD_FAST             0  'self'
         150  LOAD_ATTR            13  '_container'
         153  LOAD_ATTR            14  'csb_init_with_scrollview'
         156  LOAD_FAST             0  'self'
         159  CALL_FUNCTION_1       1 
         162  POP_TOP          

 502     163  LOAD_CONST            1  ''
         166  LOAD_CONST            2  ('cocomate',)
         169  IMPORT_NAME           0  'common.uisys'
         172  IMPORT_FROM           1  'cocomate'
         175  STORE_FAST            1  'cocomate'
         178  POP_TOP          

 504     179  LOAD_FAST             1  'cocomate'
         182  LOAD_ATTR            15  'get_ext_data'
         185  LOAD_ATTR             3  'left'
         188  CALL_FUNCTION_2       2 
         191  STORE_FAST            9  'initCount'

 505     194  LOAD_FAST             9  'initCount'
         197  POP_JUMP_IF_FALSE   216  'to 216'

 506     200  LOAD_FAST             0  'self'
         203  LOAD_ATTR            16  'SetInitCount'
         206  LOAD_FAST             9  'initCount'
         209  CALL_FUNCTION_1       1 
         212  POP_TOP          
         213  JUMP_FORWARD          0  'to 216'
       216_0  COME_FROM                '213'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 188

    def SetContentSize(self, sw, sh):
        pass

    def _refreshItemPos(self):
        pass

    def SetNumPerUnit(self, nNum):
        self._container.SetNumPerUnit(nNum)
        self._refreshItemPos()

    def SetHorzBorder(self, nBorder):
        self._container.SetHorzBorder(nBorder)
        self._refreshItemPos()

    def SetVertBorder(self, nBorder):
        self._container.SetVertBorder(nBorder)
        self._refreshItemPos()

    def SetHorzIndent(self, nIndent):
        self._container.SetHorzIndent(nIndent)
        self._refreshItemPos()

    def SetVertIndent(self, nIndent):
        self._container.SetVertIndent(nIndent)
        self._refreshItemPos()

    def GetNumPerUnit(self):
        return self._container.GetNumPerUnit()

    def GetVertIndent(self):
        return self._container.GetVertIndent()

    def GetHorzIndent(self):
        return self._container.GetHorzIndent()

    def GetHorzBorder(self):
        return self._container.GetHorzBorder()

    def GetVertBorder(self):
        return self._container.GetVertBorder()

    def GetItem(self, index):
        return self._container.GetItem(index)

    def GetCtrlSize(self):
        return self._container.GetCtrlSize()

    def GetItemCount(self):
        return self._container.GetItemCount()

    def GetAllItem(self):
        return self._container.GetAllItem()

    def GetAllValidItem(self):
        allItems = self._container.GetAllItem()
        return [ i if 1 else None for i in allItems if type(i) not in (six.text_type, str, dict) ]

    def getIndexByItem(self, item):
        return self._container.getIndexByItem(item)

    def SetTemplate(self, templateName, templateInfo=None):
        self._container.SetTemplate(templateName, templateInfo)

    def GetTemplateSetting(self):
        return self._container.GetTemplateSetting()

    def SetTemplateConf(self, conf):
        self._container.SetTemplateConf(conf)

    def GetTemplateConf(self):
        return self._container.GetTemplateConf()

    def GetTemplatePath(self):
        return self._container.GetTemplatePath()

    def SetCustomizeConf(self, customizeConf):
        self._container.SetCustomizeConf(customizeConf)

    def SetInitCount(self, nCurCount):
        addCtrls = self._container.SetInitCount(nCurCount)
        if addCtrls is not None:
            for ctrl in addCtrls:
                self._set_up_ctrl(ctrl)

        self._refreshItemPos()
        return

    def RefreshItemPos(self):
        self._container.RefreshItemPos()
        self._refreshItemPos()

    def SetItemSizeGetter(self, template_size_getter):
        self._container.SetItemSizeGetter(template_size_getter)

    def AddItem(self, conf, index=None, bRefresh=True):
        ret = self._container.AddItem(conf, index, bRefresh)
        self._set_up_ctrl(ret)
        if bRefresh:
            self._refreshItemPos()
        return ret

    def AddControl(self, ctrl, index=None, bRefresh=True, bSetupCtrl=True):
        ret = self._container.AddControl(ctrl, index, bRefresh)
        if bSetupCtrl:
            self._set_up_ctrl(ret)
        if bRefresh:
            self._refreshItemPos()
        return ret

    def AddTemplateItem(self, index=None, bRefresh=True):
        ret = self._container.AddTemplateItem(index, bRefresh)
        self._set_up_ctrl(ret)
        if bRefresh:
            self._refreshItemPos()
        return ret

    def DeleteItem(self, nd, bRefresh=True):
        self._container.DeleteItem(nd, bRefresh)
        if bRefresh:
            self._refreshItemPos()

    def DeleteItemIndex(self, index=None, bRefresh=True):
        self._container.DeleteItemIndex(index, bRefresh)
        if bRefresh:
            self._refreshItemPos()

    def DetachItemIndex(self, index=None, bRefresh=True):
        self._container.DetachItemIndex(index, bRefresh)
        if bRefresh:
            self._refreshItemPos()

    def DeleteAllSubItem(self):
        self._container.DeleteAllSubItem()
        self._refreshItemPos()

    def StopAllSubItemActionByTag(self, tag_id):
        self._container.StopAllSubItemActionByTag(tag_id)

    def TransferAllSubItem(self):
        self._container._child_item = []
        self._container._nUnit = 0
        self._container._refreshItemPos()
        self._refreshItemPos()

    def RecycleItem(self, nd, bRefresh=True):
        self._container.RecycleItem(nd, bRefresh)
        if bRefresh:
            self._refreshItemPos()

    def RecycleAllItem(self):
        self._container.RecycleAllItem()

    def ReuseItem(self, bRefresh=True):
        return self._container.ReuseItem()

    def ReverseItem(self):
        self._container.ReverseItem()

    def LocatePosByItem(self, index, duration=0):
        item = self.GetItem(index)
        if item is None:
            return
        else:
            self.CenterWithNode(item, duration)
            return

    def Destroy(self, is_remove=True):
        super(ScrollList, self).Destroy(is_remove)
        self._container = None
        return

    def DeleteItemByTag(self, Tag, bRefresh=True):
        self._container.DeleteItemByTag(Tag, bRefresh)
        if bRefresh:
            self._refreshItemPos()

    def GetItemByTag(self, tag):
        return self._container.GetItemByTag(tag)

    def EnableItemAutoPool(self, enable):
        self._container.EnableItemAutoPool(enable)

    def EnableGlobalItemAutoPool(self, enable):
        self._container._enable_global_item_pool = enable

    def FitViewSizeToContainerSize(self):
        self.InitConfContentSize()

    def IsAsync(self):
        return False