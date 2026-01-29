# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCScrollView.py
from __future__ import absolute_import
import ccui
import cc
import ccext
import math
from common.uisys.ui_proxy import ProxyClass, trans2ProxyObj
from .CCNode import CCNode, CCNodeCreator
from common.utils.cocos_utils import ccp, CCPointZero, CCRect, uiscrollview_dir_map
INSTANT_ACTION_TIME_THRESHOLD = 0.02
VIEW_CHILD_TAG = 57778888
VIEW_CUSTOMIZED_CHILD_TAG = 57778889

@ProxyClass(ccui.ScrollView)
class CCScrollView(CCNode):

    def __init__(self, node):
        super(CCScrollView, self).__init__(node)
        self.is_can_scissor = False
        import game3d
        if game3d.get_platform() == game3d.PLATFORM_WIN32 or global_data.is_android_pc:
            from logic.gutils.ui_event_utils import AddScrollviewWheelEvent
            direction = self.getDirection()
            self._mouse_listener = AddScrollviewWheelEvent(self, direction == ccui.SCROLLVIEW_DIRECTION_HORIZONTAL)
        else:
            self._mouse_listener = None
        return

    def IsClippingEnabled(self):
        return self.isClippingEnabled()

    def Destroy(self, is_remove=True):
        if self._mouse_listener:
            from logic.gutils.ui_event_utils import RemoveMouseWheelEvent
            RemoveMouseWheelEvent(self._mouse_listener)
            self._mouse_listener = None
        super(CCScrollView, self).Destroy(is_remove)
        return

    def DisableDefaultMouseEvent(self):
        if self._mouse_listener:
            from logic.gutils.ui_event_utils import RemoveMouseWheelEvent
            RemoveMouseWheelEvent(self._mouse_listener)
            self._mouse_listener = None
        return

    def _registerInnerEvent(self):
        super(CCScrollView, self)._registerInnerEvent()
        self.inner_container = trans2ProxyObj(self.getInnerContainer())
        self.UnBindMethod('OnScrolling')
        self.UnBindMethod('OnScrolled')
        self.UnBindMethod('OnScrollToTop')
        self.UnBindMethod('OnScrollToBottom')
        self.UnBindMethod('OnScrollToLeft')
        self.UnBindMethod('OnScrollToRight')
        self.UnBindMethod('OnScrollBounceTop')
        self.UnBindMethod('OnScrollBounceBottom')
        self.UnBindMethod('OnScrollBounceLeft')
        self.UnBindMethod('OnScrollBounceRight')

        def OnScrollEvent(scrollview, event):
            if not (scrollview and scrollview.isValid()):
                return
            if event == ccui.SCROLLVIEW_EVENT_SCROLLING:
                self.OnScrolling()
            elif event == ccui.SCROLLVIEW_EVENT_SCROLL_TO_TOP:
                self.OnScrollToTop()
            elif event == ccui.SCROLLVIEW_EVENT_SCROLL_TO_BOTTOM:
                self.OnScrollToBottom()
            elif event == ccui.SCROLLVIEW_EVENT_SCROLL_TO_LEFT:
                self.OnScrollToLeft()
            elif event == ccui.SCROLLVIEW_EVENT_SCROLL_TO_RIGHT:
                self.OnScrollToRight()
            elif event == ccui.SCROLLVIEW_EVENT_BOUNCE_TOP:
                self.OnScrollBounceTop()
            elif event == ccui.SCROLLVIEW_EVENT_BOUNCE_BOTTOM:
                self.OnScrollBounceBottom()
            elif event == ccui.SCROLLVIEW_EVENT_BOUNCE_LEFT:
                self.OnScrollBounceLeft()
            elif event == ccui.SCROLLVIEW_EVENT_BOUNCE_RIGHT:
                self.OnScrollBounceRight()

        self.addEventListener(OnScrollEvent)

    def SetContentSize(self, sw, sh):
        size = self.CalcSize(sw, sh)
        self.setContentSize(size)
        return size

    def SetInnerContentSize(self, sw, sh):
        size = self.CalcSize(sw, sh)
        self.setInnerContainerSize(size)
        return size

    def GetInnerContentSize(self):
        return self.getInnerContainerSize()

    def GetContentSize(self):
        size = self.getContentSize()
        return (
         size.width, size.height)

    def ScrollToTop(self, duration=0.01, attenuated=False):
        if duration > INSTANT_ACTION_TIME_THRESHOLD:
            self.scrollToTop(duration, attenuated)
        else:
            self.jumpToTop()

    def ScrollToBottom(self, duration=0.01, attenuated=False):
        if duration > INSTANT_ACTION_TIME_THRESHOLD:
            self.scrollToBottom(duration, attenuated)
        else:
            self.jumpToBottom()

    def ScrollToLeft(self, duration=0.01, attenuated=False):
        if duration > INSTANT_ACTION_TIME_THRESHOLD:
            self.scrollToLeft(duration, attenuated)
        else:
            self.jumpToLeft()

    def ScrollToRight(self, duration=0.01, attenuated=False):
        if duration > INSTANT_ACTION_TIME_THRESHOLD:
            self.scrollToRight(duration, attenuated)
        else:
            self.jumpToRight()

    def ResetContentOffset(self, duration=0.01, attenuated=False):
        minOffset = self.MinContainerOffset()
        curPos = self.GetContentOffset()
        self.SetContentOffsetInDuration(ccp(min(max(minOffset.x, curPos.x), 0), min(max(minOffset.y, curPos.y), 0)), duration, attenuated)

    def MinContainerOffset(self):
        viewSz = self.getContentSize()
        contentSz = self.getInnerContainerSize()
        return ccp(0, viewSz.height - contentSz.height)

    def IsLeftMost(self, margin=5):
        offset = self.GetContentOffset()
        if margin > 0 - offset.x:
            return True
        else:
            return False

    def IsRightMost(self, margin=5):
        viewSz = self.getContentSize()
        contentSz = self.getInnerContainerSize()
        min_offset = viewSz.width - contentSz.width
        offset = self.GetContentOffset()
        if margin > offset.x - min_offset:
            return True
        else:
            return False

    def IsTopMost(self, margin=5):
        viewSz = self.getContentSize()
        contentSz = self.getInnerContainerSize()
        min_offset = viewSz.height - contentSz.height
        offset = self.GetContentOffset()
        if margin > offset.y - min_offset:
            return True
        else:
            return False

    def IsBottomMost(self, margin=5):
        offset = self.GetContentOffset()
        if margin > 0 - offset.y:
            return True
        else:
            return False

    def SetContentOffset(self, pos):
        self.inner_container.setPosition(pos)

    def SetContentOffsetInDuration(self, pos, duration=0.01, attenuated=True, bound_check=False, over_edge=False):
        viewSize = self.getContentSize()
        contentSize = self.GetInnerContentSize()
        scale = 1.0
        max_off_x = contentSize.width * scale - viewSize.width
        max_off_y = contentSize.height * scale - viewSize.height
        ver_percent = (1 + pos.y / max_off_y) * 100 if max_off_y else 0
        hor_percent = -(pos.x / max_off_x) * 100 if max_off_x else 0
        if bound_check:
            if over_edge and self.isBounceEnabled():
                added_hort_percent = 100.0 / max_off_y if max_off_y else 50
                added_vert_percent = 100.0 / max_off_x if max_off_x else 50
            else:
                added_hort_percent = 0
                added_vert_percent = 0
            ver_percent = min(max(0 - added_vert_percent, ver_percent), 100 + added_vert_percent)
            hor_percent = min(max(0 - added_hort_percent, hor_percent), 100 + added_hort_percent)
        if self.getDirection() == ccui.SCROLLVIEW_DIRECTION_VERTICAL:
            if duration <= INSTANT_ACTION_TIME_THRESHOLD:
                self.jumpToPercentVertical(ver_percent)
            else:
                self.scrollToPercentVertical(ver_percent, duration, attenuated)
        elif self.getDirection() == ccui.SCROLLVIEW_DIRECTION_HORIZONTAL:
            if duration <= INSTANT_ACTION_TIME_THRESHOLD:
                self.jumpToPercentHorizontal(hor_percent)
            else:
                self.scrollToPercentHorizontal(hor_percent, duration, attenuated)
        elif duration <= INSTANT_ACTION_TIME_THRESHOLD:
            self.jumpToPercentBothDirection(ccp(hor_percent, ver_percent))
        else:
            self.scrollToPercentBothDirection(ccp(hor_percent, ver_percent), duration, attenuated)

    def GetContentOffset(self):
        return self.getInnerContainer().getPosition()

    def CenterWithPosByAnchor(self, x, y, default_content_size=None, default_view_size=None):
        viewSize = default_view_size or self.getContentSize()
        contentSize = default_content_size or self.getInnerContainerSize()
        anchor_x = x / contentSize.width
        anchor_y = y / contentSize.height
        self.inner_container.setAnchorPoint(ccp(anchor_x, anchor_y))
        self.inner_container.setPosition(ccp(viewSize.width / 2, viewSize.height / 2))
        yaw = global_data.cam_data.yaw or 0
        self.inner_container.setRotation(-yaw * 180 / math.pi)

    def CenterWithPos(self, x, y, duration=0.01, default_content_size=None, default_view_size=None):
        viewSize = default_view_size or self.getContentSize()
        contentSize = default_content_size or self.getInnerContainerSize()
        max_off_x = contentSize.width - viewSize.width
        max_off_y = contentSize.height - viewSize.height
        x_off = -min(max(x - viewSize.width / 2, 0), max_off_x)
        y_off = -min(max(y - viewSize.height / 2, 0), max_off_y)
        if duration > INSTANT_ACTION_TIME_THRESHOLD:
            self.SetContentOffsetInDuration(ccp(x_off, y_off), duration)
        else:
            self.inner_container.setPosition(ccp(x_off, y_off))

    def CenterWithNode(self, node, duration=0.01):
        w, h = node.GetContentSize()
        worldPos = node.convertToWorldSpace(ccp(w / 2, h / 2))
        scrolPos = self.GetInnerContainer().convertToNodeSpace(worldPos)
        self.CenterWithPos(scrolPos.x, scrolPos.y, duration)

    def TopWithPos(self, x, y, duration=0.01, default_content_size=None, default_view_size=None):
        viewSize = default_view_size or self.getContentSize()
        contentSize = default_content_size or self.getInnerContainerSize()
        max_off_x = contentSize.width - viewSize.width
        max_off_y = contentSize.height - viewSize.height
        x_off = -min(max(x - viewSize.width / 2, 0), max_off_x)
        y_off = -min(max(y - viewSize.height, 0), max_off_y)
        if duration > INSTANT_ACTION_TIME_THRESHOLD:
            self.SetContentOffsetInDuration(ccp(x_off, y_off), duration)
        else:
            self.inner_container.setPosition(ccp(x_off, y_off))

    def TopWithNode(self, node, duration=0.01):
        w, h = node.GetContentSize()
        worldPos = node.convertToWorldSpace(ccp(w / 2, h))
        scrolPos = self.GetInnerContainer().convertToNodeSpace(worldPos)
        self.TopWithPos(scrolPos.x, scrolPos.y, duration)

    def _set_up_ctrl(self, ctrl):
        from common.utils.ui_utils import get_scale
        ctrl.SetClipObjectRecursion(self)
        win_size = cc.Director.getInstance().getWinSize()
        win_w = win_size.width
        ctrl.SetNoEventAfterMoveRecursion(True, get_scale('1w') * win_w / 50)

    def SetContainer(self, container):
        self._set_up_ctrl(container)
        self.getInnerContainer().removeAllChildren()
        self.AddChild('_container', container)
        sz = container.getContentSize()
        self.SetInnerContentSize(sz.width, sz.height)
        self._container = container
        container.ignoreAnchorPointForPosition(False)
        container.setAnchorPoint(ccp(0, 0))
        container.SetPosition(0, 0)
        self.ResetContentOffset()

    def GetContainer(self):
        return self._container

    def GetInnerContainer(self):
        return self.getInnerContainer()

    def IsNodeVisible(self, node, selfRect=None):
        lb = node.convertToWorldSpace(CCPointZero)
        rt = node.convertToWorldSpace(ccp(*node.GetContentSize()))
        if selfRect is None:
            selfLB = self.convertToWorldSpace(CCPointZero)
            selfRT = self.convertToWorldSpace(ccp(*self.GetContentSize()))
            selfRect = CCRect(selfLB.x, selfLB.y, selfRT.x - selfLB.x, selfRT.y - selfLB.y)
        return selfRect.intersectsRect(CCRect(lb.x, lb.y, rt.x - lb.x, rt.y - lb.y))

    def GetVisibleRange(self):
        direction = self.getDirection()
        if direction == ccui.SCROLLVIEW_DIRECTION_HORIZONTAL:
            ctrlW = self._container.GetCtrlSize().width
            viewSize = self.getContentSize()
            offset = self.GetContentOffset()
            calcWidth = -offset.x - self._container.GetHorzBorder()
            nWidth = ctrlW + self._container.GetHorzIndent()
            nUnitStart = calcWidth // nWidth
            nUnitEnd = (calcWidth + viewSize.width) // nWidth
        else:
            ctrlH = self._container.GetCtrlSize().height
            contentSize = self.GetInnerContentSize()
            viewSize = self.getContentSize()
            offset = self.GetContentOffset()
            calcHeight = contentSize.height + offset.y - self._container.GetVertBorder()
            nHeight = ctrlH + self._container.GetVertIndent()
            nUnitStart = (calcHeight - viewSize.height) // nHeight
            nUnitEnd = calcHeight // nHeight
        maxIndex = self._container.GetItemCount()
        return (
         min(max(nUnitStart, 0), maxIndex), min(max(nUnitEnd, 0), maxIndex))

    def SetContainerScale(self, scale, zoom_anchor_x=0, zoom_anchor_y=0):
        sz = self._container.getContentSize()
        old_scale = self._container.getScale()
        zoom_center = (sz.width * old_scale * zoom_anchor_x, sz.height * old_scale * zoom_anchor_y)
        offset = self.GetContentOffset()
        center_offset = (zoom_center[0] + offset.x, zoom_center[1] + offset.y)
        new_sz = (sz.width * scale, sz.height * scale)
        zoom_center2 = (new_sz[0] * zoom_anchor_x, new_sz[1] * zoom_anchor_y)
        new_offset = (center_offset[0] - zoom_center2[0], center_offset[1] - zoom_center2[1])
        self._container.setScale(scale)
        self.SetInnerContentSize(new_sz[0], new_sz[1])
        self.SetContentOffsetInDuration(ccp(new_offset[0], new_offset[1]), bound_check=True)

    def SetClippingType(self, clipping_type):
        if self.is_can_scissor:
            self.setClippingType(clipping_type)

    def IsUseScissor(self):
        cur_iter = self
        index = 0
        while cur_iter:
            if cur_iter.getRotation() != 0.0 or cur_iter.getSkewX() != 0.0 or cur_iter.getSkewY() != 0.0:
                return False
            cur_iter = cur_iter.getParent()
            if cur_iter == global_data.cocos_scene:
                break
            index += 1
            if index > 4:
                break

        return True

    def SetTouchEnabled(self, bEnable):
        self.setTouchEnabled(bEnable)

    def SetClippingEnabled(self, flag):
        return self.setClippingEnabled(flag)

    def GetScollViewChildren(self):
        ret = []
        if self._obj.isValid():
            for child in self._obj.getInnerContainer().getProtectedChildrenByTag(VIEW_CHILD_TAG):
                ret.append(trans2ProxyObj(child))

        return ret

    def SyncAttrToContainer(self):
        from common.uisys import cocomate
        inner_root = cocomate.get_cocomate_node_by_cocos_node(self.inner_container.getChildren()[0])
        self._container = inner_root

    def GetNumPerUnit(self):
        return self.inner_container.getLayoutUnits()

    def SetNumPerUnit(self, num):
        self.inner_container.setLayoutUnits(num)

    def GetMargin(self):
        return self.inner_container.getMargin()

    def SetMargin(self, le=None, t=None, r=None, b=None):
        ori_margin = self.GetMargin()
        ori_margin.setMargin(ori_margin.left if le is None else le, ori_margin.top if t is None else t, ori_margin.right if r is None else r, ori_margin.bottom if b is None else b)
        self.inner_container.setMargin(ori_margin)
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


class CCScrollViewCreator(CCNodeCreator):
    COM_NAME = 'CCScrollView'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('container', ''),
     (
      'direction', ccext.SCROLLVIEW_DIRECTION_BOTH),
     (
      'bounces', True)]
    ATTR_INIT = CCNodeCreator.ATTR_INIT + [
     'container']

    @staticmethod
    def set_attr_group_container(obj, parent, root, container, direction, bounces):
        if container:
            container = global_data.uisystem.load_template_create(container)
            obj.SetContainer(container)
        obj.setDirection(uiscrollview_dir_map(direction))
        obj.setBounceEnabled(bounces)

    @staticmethod
    def create(parent, root):
        return CCScrollView.Create()