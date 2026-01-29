# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCLayer.py
from __future__ import absolute_import
import cc
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode, CCNodeCreator, Empty
from common.utils.ui_utils import get_scale, default_cancel_dist
BATTLE_WIDGET_NAME_MAP = {'btn_close': 'battle_back',
   'close': 'battle_back',
   'btn_back': 'battle_back',
   'back': 'battle_back'
   }
MENU_WIDGET_NAME_MAP = {'btn_close': 'menu_back',
   'close': 'menu_back',
   'btn_back': 'menu_back',
   'back': 'menu_back'
   }

def play_ui_sound_by_widget_name(sound_name, widget_name):
    from logic.vscene import scene_type
    if not sound_name:
        if global_data.scene_type == scene_type.SCENE_TYPE_BATTLE:
            sound_name = BATTLE_WIDGET_NAME_MAP.get(widget_name, 'battle_click')
        else:
            sound_name = MENU_WIDGET_NAME_MAP.get(widget_name, 'menu_click')
    if global_data.sound_mgr:
        global_data.sound_mgr.play_ui_sound(sound_name)


def dummy_empty_touch_callback(event_type, touch):
    return False


@ProxyClass(cc.Node)
class CCLayer(CCNode):
    PRESS_NEED_TIME = 0.5
    PRESS_ACTION_TAG = 10001
    DOUBLE_CLICK_INTERVAL = 0.3
    DOUBLE_CLICK_ACTION_TAG = 10002

    def __init__(self, node):
        super(CCLayer, self).__init__(node)
        from common.utils.ui_utils import default_cancel_dist
        self._bNoEventAfterMove = False
        self._nNoEventMoveDist = 0
        self._nMovedDist = 0
        self._press_enable = False
        self._press_action = None
        self._bEnableDoubleClick = False
        self._last_click_time = 0.0
        self._last_click_pos = None
        self._bInPressTouch = False
        self._bInTouch = False
        self._passedTouchId = None
        self._drag_action = None
        self._last_drag_pos = None
        self._last_drag_touch = None
        self._hasAddedTouchEvent = False
        self._double_click_cancel_dist = default_cancel_dist
        self._in_hover = False
        self._press_need_time = self.PRESS_NEED_TIME
        self._propagateTouchEvents = False
        self._touch_begin_time = 0
        self._touch_end_time = 0
        return

    def _registerInnerEvent(self):
        super(CCLayer, self)._registerInnerEvent()
        self.UnBindMethod('OnBegin')
        self.UnBindMethod('OnDrag')
        self.UnBindMethod('OnEnd')
        self.UnBindMethod('OnClick')
        self.UnBindMethod('OnUpOutside')
        self.UnBindMethod('OnCancel')
        self.UnBindMethod('OnPressed')
        self.UnBindMethod('OnPressedWithNum')
        self.UnBindMethod('OnDoubleClick')
        self.UnBindMethod('OnSingleClick')
        self.UnBindMethod('OnDisableCancel')

        def _default_onbegin(*args):
            return True

        self.BindMethod('OnBegin', _default_onbegin)

    def _OnBegin(self, touch):
        return self.OnBegin(touch)

    def _OnEnd(self, touch):
        return self.OnEnd(touch)

    def _OnCancel(self, touch):
        return self.OnCancel(touch)

    def _OnClick(self, touch, *args, **kwargs):
        import time
        if self._bEnableDoubleClick:
            cur_time = time.time()
            if cur_time - self._last_click_time < CCLayer.DOUBLE_CLICK_INTERVAL and touch.getLocation().distance(touch.getStartLocation()) < self._double_click_cancel_dist:
                self.stopActionByTag(CCLayer.DOUBLE_CLICK_ACTION_TAG)
                self.OnDoubleClick(self._last_click_pos, touch.getLocation())
                self._last_click_time = 0
            else:
                wpos = touch.getLocation()
                self._last_click_pos = wpos
                if touch.getLocation().distance(touch.getStartLocation()) < self._double_click_cancel_dist:
                    self._last_click_time = cur_time

                def single_callback(touch=touch):
                    self.OnSingleClick(wpos)

                self.SetTimeOut(CCLayer.DOUBLE_CLICK_INTERVAL, single_callback, tag=CCLayer.DOUBLE_CLICK_ACTION_TAG)
        if self._enable_click_sound:
            sound_name = self._click_sound_name2 if self._click_sound_name2 else self._click_sound_name
            play_ui_sound_by_widget_name(sound_name, self.widget_name)
        gds = global_data.game_mgr.gds
        if gds:
            gds.set_save_energy_mode(False)
        touch_begin_time = self._touch_begin_time
        touch_end_time = self._touch_end_time
        busy_reconnect_bg_time = global_data.busy_reconnect_bg_time
        last_avatar_destroy_stack = global_data.last_avatar_destroy_stack
        self.OnClick(touch)

    def HandleTouchMove(self, bEnable, bSwallow, bNoEventAfterMove, move_dist=None, bForceHandleTouch=False):
        from common.utils.ui_utils import default_cancel_dist
        self.SetSwallowTouch(bSwallow)
        self.SetNoEventAfterMove(bNoEventAfterMove, default_cancel_dist if move_dist is None else move_dist)
        self.SetEnableTouch(bEnable)
        self.SetForceHandleTouch(bForceHandleTouch)
        return

    def SetForceHandleTouch(self, bForceHandleTouch):
        self.setForceHandleTouch(bForceHandleTouch)

    def SetEnableTouch(self, bEnable):
        if self.isTouchEnabled() == bEnable:
            return
        self.setTouchEnabled(bEnable)
        self.SetEnableTouchWithoutCheck(bEnable)

    def SetPassedTouchId(self, touchId):
        self._passedTouchId = touchId

    def SetEnableTouchWithoutCheck(self, bEnable):
        import time
        if bEnable:

            def OnTouchCancel(touch):
                self.stopActionByTag(CCLayer.PRESS_ACTION_TAG)
                self._OnCancel(touch)
                self._nMovedDist = 0
                self._bInPressTouch = False
                self._bInTouch = False

            def _OnTouchCallBack(touchType, touch):
                if touchType == cc.NODE_TOUCHEVENTTYPE_BEGAN:
                    self._touch_begin_time = time.time()
                    ret = self._OnBegin(touch)
                    if ret is None:
                        ret = True
                    if self._passedTouchId is not None:
                        if touch.getId() != self._passedTouchId:
                            return True
                    self._bInTouch = bool(ret)
                    if self._press_enable:
                        self._press_action = self.runAction(cc.Sequence.create([
                         cc.DelayTime.create(self._press_need_time),
                         cc.CallFunc.create(self.StartPress)]))
                        self._press_action.setTag(CCLayer.PRESS_ACTION_TAG)
                        self._bInPressTouch = True
                    if self.OnDrag != Empty:
                        self._StartDrag(touch)
                    return bool(ret)
                else:
                    if touchType == cc.NODE_TOUCHEVENTTYPE_MOVED:
                        if self._passedTouchId is not None:
                            if touch.getId() != self._passedTouchId:
                                return True
                        self._nMovedDist = self._nMovedDist + touch.getDelta().length()
                        if self.IsMovedDistance():
                            if not self._propagateTouchEvents:
                                self.SetEnableTouch(False)
                                self.SetEnableTouch(True)
                                OnTouchCancel(touch)
                                return True
                            else:
                                self._OnCancel(touch)
                                self.stopActionByTag(CCLayer.PRESS_ACTION_TAG)
                                return True

                        self._RecordDrag(touch)
                        return True
                    if touchType == cc.NODE_TOUCHEVENTTYPE_ENDED:
                        self._touch_end_time = time.time()
                        if self._passedTouchId is not None:
                            if touch.getId() != self._passedTouchId:
                                return True
                        touchPoint = touch.getLocation()
                        self.stopActionByTag(CCLayer.PRESS_ACTION_TAG)
                        self._StopDrag()
                        self._OnEnd(touch)
                        if self.IsPointIn(touchPoint):
                            if not self.IsMovedDistance():
                                self._OnClick(touch)
                        else:
                            self.OnUpOutside(touch)
                        self._nMovedDist = 0
                        self._bInPressTouch = False
                        return True
                    if touchType == cc.NODE_TOUCHEVENTTYPE_CANCELED:
                        if self._passedTouchId is not None:
                            if touch.getId() != self._passedTouchId:
                                return True
                        OnTouchCancel(touch)
                        self._StopDrag()
                        return True
                    return True

            self._hasAddedTouchEvent = True
            self.addNodeTouchEventListener(_OnTouchCallBack)
        else:

            def OnDisableCancel():
                self.stopActionByTag(CCLayer.PRESS_ACTION_TAG)
                self.OnDisableCancel()
                self._nMovedDist = 0
                self._bInPressTouch = False

            if self._bInPressTouch or self._bInTouch:
                OnDisableCancel()

    def GetEnableTouch(self):
        return self.isTouchEnabled()

    def SetSwallowTouch(self, bSwallowTouch):
        self.setSwallowTouches(bSwallowTouch)

    def GetSwallowTouch(self):
        return self.isSwallowTouches()

    def SetNoEventAfterMove(self, flag, move_dist=default_cancel_dist):
        self._bNoEventAfterMove = flag
        from common.utils.ui_utils import default_cancel_dist
        self._nNoEventMoveDist = get_scale(move_dist) if move_dist != default_cancel_dist else default_cancel_dist

    def IsMovedDistance(self):
        return self._bNoEventAfterMove is True and self._nMovedDist > self._nNoEventMoveDist

    def IsOverCancelDistance(self):
        return self._nMovedDist > self._nNoEventMoveDist

    def GetMovedDistance(self):
        return self._nMovedDist

    def IsMoved(self):
        return self._nMovedDist > 0

    def _StartDrag(self, touch):
        self._drag_action = self.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.01),
         cc.CallFunc.create(self._DragTrigger)])))
        self._last_drag_pos = touch.getLocationInView()
        self._last_drag_touch = None
        return

    def _StopDrag(self):
        if self._drag_action:
            self.stopAction(self._drag_action)
            self._drag_action = None
        self._last_drag_pos = None
        self._last_drag_touch = None
        return

    def _RecordDrag(self, touch):
        self._last_drag_touch = touch

    def _DragTrigger(self):
        if self._last_drag_touch is not None and self._last_drag_touch.isValid():
            if self._last_drag_pos is not None:
                self._last_drag_touch.setPrevTouchPos(self._last_drag_pos.x, self._last_drag_pos.y)
            self.OnDrag(self._last_drag_touch)
            self._last_drag_pos = self._last_drag_touch.getLocationInView()
        self._last_drag_touch = None
        return

    def SetPressEnable(self, enable):
        self._press_enable = enable

    def SetPressNeedTime(self, need_time):
        self._press_need_time = need_time

    def StartPress(self):
        self.OnPressed()
        self._press_click_cnt = 0
        self._press_action = self.runAction(cc.Sequence.create([
         cc.DelayTime.create(self._press_need_time),
         cc.CallFunc.create(self.PressTrigger)]))
        self._press_action.setTag(CCLayer.PRESS_ACTION_TAG)

    def PressTrigger(self):
        self._press_click_cnt += 1
        self.OnPressedWithNum(self._press_click_cnt)
        self._press_action = self.runAction(cc.Sequence.create([
         cc.DelayTime.create(0.1),
         cc.CallFunc.create(self.PressTrigger)]))
        self._press_action.setTag(CCLayer.PRESS_ACTION_TAG)

    def EnableDoubleClick(self, enable):
        self._bEnableDoubleClick = enable

    def set_hover_enable(self, enable):
        if not global_data.feature_mgr.is_support_pc_mouse_hover():
            return
        if self.isHoverEnabled() == enable:
            return
        if enable:

            def hover_cb(event_type):
                if event_type == cc.NODE_HOVEREVENTTYPE_ENTER:
                    self._on_hover_enter()
                elif event_type == cc.NODE_HOVEREVENTTYPE_EXIT:
                    self._on_hover_exit()
                elif event_type == cc.NODE_HOVEREVENTTYPE_CANCEL:
                    self._on_hover_exit()

            self.setNodeHoverEventListener(hover_cb)
        else:
            self._on_hover_exit()
        self.setHoverEnabled(enable)

    def _on_hover_enter--- This code section failed: ---

 385       0  LOAD_GLOBAL           0  'True'
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            1  '_in_hover'

 387       9  LOAD_GLOBAL           2  'hasattr'
          12  LOAD_GLOBAL           1  '_in_hover'
          15  CALL_FUNCTION_2       2 
          18  POP_JUMP_IF_FALSE    49  'to 49'
          21  LOAD_GLOBAL           3  'callable'
          24  LOAD_FAST             0  'self'
          27  LOAD_ATTR             4  'OnHoverEnter'
          30  CALL_FUNCTION_1       1 
        33_0  COME_FROM                '18'
          33  POP_JUMP_IF_FALSE    49  'to 49'

 388      36  LOAD_FAST             0  'self'
          39  LOAD_ATTR             4  'OnHoverEnter'
          42  CALL_FUNCTION_0       0 
          45  POP_TOP          
          46  JUMP_FORWARD          0  'to 49'
        49_0  COME_FROM                '46'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 15

    def _on_hover_exit--- This code section failed: ---

 391       0  LOAD_GLOBAL           0  'False'
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            1  '_in_hover'

 393       9  LOAD_GLOBAL           2  'hasattr'
          12  LOAD_GLOBAL           1  '_in_hover'
          15  CALL_FUNCTION_2       2 
          18  POP_JUMP_IF_FALSE    49  'to 49'
          21  LOAD_GLOBAL           3  'callable'
          24  LOAD_FAST             0  'self'
          27  LOAD_ATTR             4  'OnHoverExit'
          30  CALL_FUNCTION_1       1 
        33_0  COME_FROM                '18'
          33  POP_JUMP_IF_FALSE    49  'to 49'

 394      36  LOAD_FAST             0  'self'
          39  LOAD_ATTR             4  'OnHoverExit'
          42  CALL_FUNCTION_0       0 
          45  POP_TOP          
          46  JUMP_FORWARD          0  'to 49'
        49_0  COME_FROM                '46'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 15

    def Destroy(self, is_remove=True):
        if self._hasAddedTouchEvent:
            self.addNodeTouchEventListener(dummy_empty_touch_callback)
            self._hasAddedTouchEvent = False
        super(CCLayer, self).Destroy(is_remove)

    def Detach(self):
        if self._hasAddedTouchEvent:
            self.addNodeTouchEventListener(dummy_empty_touch_callback)
            self._hasAddedTouchEvent = False
        super(CCLayer, self).Detach()


class CCLayerCreator(CCNodeCreator):
    COM_NAME = 'CCLayer'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'touchEnabled', False),
     (
      'swallow', True),
     (
      'noEventAfterMove', False),
     ('move_dist', '10w'),
     (
      'forceHandleTouch', False)]

    @staticmethod
    def create(parent, root, touchEnabled, swallow, noEventAfterMove, move_dist, forceHandleTouch):
        obj = CCLayer.Create()
        obj.HandleTouchMove(touchEnabled, swallow, noEventAfterMove, move_dist, forceHandleTouch)
        return obj