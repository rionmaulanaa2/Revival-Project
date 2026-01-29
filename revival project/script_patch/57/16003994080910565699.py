# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCAsyncList.py
from __future__ import absolute_import
from six.moves import range
import six
from common.uisys.ui_proxy import ProxyClass
from .ScrollList import ScrollList
from .CCAsyncContainer import CCAsyncContainer
import time
from logic.manager_agents.manager_decorators import sync_exec

@ProxyClass()
class CCAsyncList(ScrollList):
    ASYNC_LOAD_TAG = 50001

    def __init__(self, node, ContainerType):
        super(CCAsyncList, self).__init__(node, ContainerType)
        self._bStartLoad = False
        self._startVisiIndex = None
        self._endVisiIndex = None
        self._load_time = 0.01
        self._interval_time = 0.03
        self._isRefreshMode = False
        self._fade_in_out_enabled = False
        self._vertical_fade_in_out = 0
        self._fade_parameters = [0.0, 0.0, 1.0, 1.0]
        self._rt = None
        return

    def _registerInnerEvent(self):
        super(CCAsyncList, self)._registerInnerEvent()
        self.UnBindMethod('OnCreateItem')

        @self.callback()
        def OnScrolling(ctrl):
            self._testScrollAndLoad()

    def SyncAttrToContainer--- This code section failed: ---

  43       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('get_ext_data',)
           6  IMPORT_NAME           0  'common.uisys.cocomate'
           9  IMPORT_FROM           1  'get_ext_data'
          12  STORE_FAST            1  'get_ext_data'
          15  POP_TOP          

  44      16  LOAD_FAST             1  'get_ext_data'
          19  LOAD_FAST             3  'fadeInOut'
          22  BUILD_MAP_0           0 
          25  CALL_FUNCTION_257   257 
          28  STORE_FAST            2  'ext_data'

  45      31  LOAD_FAST             2  'ext_data'
          34  LOAD_ATTR             2  'get'
          37  LOAD_CONST            4  'fadeInOut'
          40  LOAD_GLOBAL           3  'False'
          43  CALL_FUNCTION_2       2 
          46  STORE_FAST            3  'fadeInOut'

  46      49  LOAD_FAST             3  'fadeInOut'
          52  POP_JUMP_IF_FALSE   161  'to 161'

  47      55  LOAD_FAST             2  'ext_data'
          58  LOAD_ATTR             2  'get'
          61  LOAD_CONST            5  'fadeInStartPoint'
          64  LOAD_CONST            6  ''
          67  CALL_FUNCTION_2       2 
          70  STORE_FAST            4  'fadeInStartPoint'

  48      73  LOAD_FAST             2  'ext_data'
          76  LOAD_ATTR             2  'get'
          79  LOAD_CONST            7  'fadeInEndPoint'
          82  LOAD_CONST            6  ''
          85  CALL_FUNCTION_2       2 
          88  STORE_FAST            5  'fadeInEndPoint'

  49      91  LOAD_FAST             2  'ext_data'
          94  LOAD_ATTR             2  'get'
          97  LOAD_CONST            8  'fadeOutStartPoint'
         100  LOAD_CONST            9  1.0
         103  CALL_FUNCTION_2       2 
         106  STORE_FAST            6  'fadeOutStartPoint'

  50     109  LOAD_FAST             2  'ext_data'
         112  LOAD_ATTR             2  'get'
         115  LOAD_CONST           10  'fadeOutEndPoint'
         118  LOAD_CONST            9  1.0
         121  CALL_FUNCTION_2       2 
         124  STORE_FAST            7  'fadeOutEndPoint'

  51     127  LOAD_FAST             0  'self'
         130  LOAD_ATTR             4  'SetFadeInOutEnabled'
         133  LOAD_FAST             3  'fadeInOut'
         136  LOAD_CONST           11  1
         139  LOAD_FAST             4  'fadeInStartPoint'
         142  LOAD_FAST             5  'fadeInEndPoint'
         145  LOAD_FAST             6  'fadeOutStartPoint'
         148  LOAD_FAST             7  'fadeOutEndPoint'
         151  BUILD_LIST_4          4 
         154  CALL_FUNCTION_3       3 
         157  POP_TOP          
         158  JUMP_FORWARD          0  'to 161'
       161_0  COME_FROM                '158'

  52     161  LOAD_GLOBAL           5  'super'
         164  LOAD_GLOBAL           6  'CCAsyncList'
         167  LOAD_FAST             0  'self'
         170  CALL_FUNCTION_2       2 
         173  LOAD_ATTR             7  'SyncAttrToContainer'
         176  CALL_FUNCTION_0       0 
         179  POP_TOP          

Parse error at or near `CALL_FUNCTION_257' instruction at offset 25

    def _testScrollAndLoad(self):
        if self._canAyncLoad():
            self.scroll_Load(from_outside=False)

    def scroll_reload(self, item_cnt):
        if not item_cnt:
            self.DeleteAllSubItem()
            return
        if self.GetItemCount() > 0:
            self.set_asyncLoad_refresh_mode(True)
        self.SetInitCount(item_cnt)
        if not self._bStartLoad:
            self.scroll_Load()

    def scroll_Load(self, from_outside=True):
        self._updateVisibleData()
        self._asyncLoad()
        if hasattr(self._obj, 'getIgnorePause') and from_outside:
            if self._fade_in_out_enabled and not self.getIgnorePause():
                self.EnableFadeInOut()

    def sync_scroll_load(self, max_time=10000):
        pre_load_time = self._load_time
        self._load_time = max_time
        self.stopActionByTag(self.ASYNC_LOAD_TAG)
        self._bStartLoad = False
        self._asyncLoad()
        self._load_time = pre_load_time

    def set_asyncLoad_tick_time(self, time):
        self._load_time = time

    def set_asyncLoad_interval_time(self, time):
        self._interval_time = time

    def set_asyncLoad_refresh_mode(self, flag):
        self._isRefreshMode = flag

    def is_loading(self):
        return self._bStartLoad

    def _asyncLoad(self, start_idx=None):
        if self._bStartLoad:
            return
        else:
            self._bStartLoad = True
            self._startLoadTick = time.time()
            if not self._isRefreshMode:
                for i in range(self._startVisiIndex, self._endVisiIndex):
                    item = self._container.DoLoadItem(i)
                    if item:
                        self.OnCreateItem(i, item)
                        self._set_up_ctrl(item)
                    if time.time() - self._startLoadTick > self._load_time and item:

                        def scheduleFun(*args):
                            self._bStartLoad = False
                            self._asyncLoad()

                        self.SetTimeOut(self._interval_time, scheduleFun, tag=self.ASYNC_LOAD_TAG)
                        return

            else:
                start_idx = self._startVisiIndex if start_idx is None else start_idx
                for i in range(start_idx, self._endVisiIndex):
                    item = self.GetItem(i)
                    if not item:
                        item = self._container.DoLoadItem(i)
                    if item:
                        self.OnCreateItem(i, item)
                        self._set_up_ctrl(item)
                    if time.time() - self._startLoadTick > self._load_time and i < self._endVisiIndex:

                        def scheduleFun(*args):
                            self._bStartLoad = False
                            self._asyncLoad(i)

                        self.SetTimeOut(self._interval_time, scheduleFun, tag=self.ASYNC_LOAD_TAG)
                        return

            self._bStartLoad = False
            return

    def _canAyncLoad(self):
        pass

    def _updateVisibleData(self):
        pass

    def DoLoadItem(self, index):
        item = self._container.DoLoadItem(index)
        if item:
            self._set_up_ctrl(item)
            self.OnCreateItem(index, item)
        return item

    def IsAllLoaded(self):
        allItem = self._container.GetAllItem()
        for item in allItem:
            if type(item) in [six.text_type, str, dict]:
                return False

        return True

    def LocatePosByItem(self, index, duration=0):
        item = self.GetItem(index)
        if item is None:
            item = self.DoLoadItem(index)
        if item is None:
            return
        else:
            self.CenterWithNode(item, duration)
            return

    def ForceLoadVisibleRangeItem(self):
        for i in range(self._startVisiIndex, self._endVisiIndex):
            item = self._container.DoLoadItem(i)
            if item:
                self.OnCreateItem(i, item)
                self._set_up_ctrl(item)

    def SetFadeInOutEnabled(self, enable, vertical_fade_in_out, fade_parameters):
        if enable and fade_parameters[1] == 0.0 and fade_parameters[2] == 1.0:
            return
        self._fade_in_out_enabled = enable
        self._vertical_fade_in_out = vertical_fade_in_out
        self._fade_parameters = fade_parameters

    @sync_exec
    def _render_rt(self, dt):
        self.update(dt)
        self._rt.beginWithClear(0, 0, 0, 0)
        if hasattr(self._rt, 'addCommandsForNode'):
            self._rt.addCommandsForNode(self.get())
        else:
            self._rt.visit()
        self._rt.end()

    def EnableFadeInOut(self):
        if hasattr(self._obj, 'setIgnorePause'):
            import cc
            import device_compatibility
            from common.const.uiconst import DEPTH24_STENCIL8_OES
            self.setIgnorePause(True)
            old_parent = self.GetParent()
            old_anchor_point = self.getAnchorPoint()
            old_pos = self.getPosition()
            size = self.getContentSize()
            size = (size.width, size.height)
            pre_mat = self.getWorldToNodeTransform()
            self.retain()
            self.removeFromParent()
            self.setAnchorPoint(cc.Vec2(0, 0))
            self.SetPosition(0, 0)
            self.setTouchAdditionalTransform(pre_mat)
            rt = cc.RenderTexture.create(int(size[0]), int(size[1]), cc.TEXTURE2D_PIXELFORMAT_RGBA8888, DEPTH24_STENCIL8_OES)
            rt.setPosition(0, 0)
            old_parent.addChild(rt)
            sprite = rt.getSprite()
            sprite.setAnchorPoint(old_anchor_point)
            sprite.setPosition(old_pos)
            sprite.getTexture().setAntiAliasTexParameters()
            use_d3d = device_compatibility.IS_DX
            if use_d3d:
                sprite.setFlippedY(False)
            self._rt = rt
            old_parent.setBeforeReleaseCallback(self.ClearFadeInOut)
            self._render_rt(0.0)
            self._render_timer = global_data.game_mgr.register_logic_timer(self._render_rt, interval=1, timedelta=True)
            from logic.comsys.effect.ui_effect import create_shader
            shader = create_shader('fade_in_out', 'fade_in_out')
            shader_state = cc.GLProgramState.create(shader)
            sprite.setGLProgramState(shader_state)
            shader_state.setUniformInt('is_vertical_fadeout', self._vertical_fade_in_out)
            if use_d3d:
                fade_parameters = self._fade_parameters
            else:
                fade_parameters = []
                if not use_d3d:
                    for i in range(3, -1, -1):
                        fade_parameters.append(1.0 - self._fade_parameters[i])

            shader_state.setUniformFloat('fade_in_start_point', fade_parameters[0])
            shader_state.setUniformFloat('fade_in_end_point', fade_parameters[1])
            shader_state.setUniformFloat('fade_out_start_point', fade_parameters[2])
            shader_state.setUniformFloat('fade_out_end_point', fade_parameters[3])
            self.stopActionByTag(self.ASYNC_LOAD_TAG)
            self._bStartLoad = False
            self._asyncLoad()

    def ClearFadeInOut(self):
        if self.getIgnorePause():
            if self._render_timer:
                global_data.game_mgr.unregister_logic_timer(self._render_timer)
                self._render_timer = None
            self._rt = None
            self.setIgnorePause(False)
            self.pause()
            self.release()
        return

    def IsAsync(self):
        return True