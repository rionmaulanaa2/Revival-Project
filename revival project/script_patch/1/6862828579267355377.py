# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/DanmuLinesUI.py
from __future__ import absolute_import
import six
from six.moves import range
import cc
from common.uisys.basepanel import BasePanel
from common.const import uiconst
import random
import re

class Danmu(object):
    __slot__ = ('text', 'expire_duration', 'priority', 'head_pic', 'template', 'tag')

    def __init__(self, text, expire_duration, priority=0, head_pic=None, template=None, custom_item_func=None, tag=None):
        self.text = text
        self.expire_duration = expire_duration
        self.priority = priority
        self.head_pic = head_pic
        self.template = template
        self.custom_item_func = custom_item_func
        self.tag = tag


class DanmuLinesUI(BasePanel):
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'observe/nd_danmu'
    LINE_NUM = 2
    LINE_WIDTH = 50
    MAX_PRIORITY = 10
    MAX_CACHE_NUM = 50
    MAX_SPEED = 250
    MIN_SPEED = 150
    UPDATE_LOGIC_INTERVAL = 0.1
    EXPIRE_DURATION = 5
    MAX_PROTECT_DURATION = 1
    MIN_PROTECT_DURATION = 0.1
    DANMU_TEMPLATE = 'observe/i_lab_danmu'
    IS_PLAY_OPEN_SOUND = False

    def on_init_panel(self, *args, **kwargs):
        self.panel.setLocalZOrder(100)
        self._enable = False
        self._nd_scale = 1.0
        self._font_size = 24
        self._is_in_float = False
        self._tag_danmu_dict = {}
        self._danmu_list = []
        self._forbidden_tag_set = set()
        self.enable_danmu(True)
        self.panel.DelayCallWithTag(self.UPDATE_LOGIC_INTERVAL, self._update_launch_logic, None)
        self.special_message_scale_dict = {re.compile('<emote=\\d+,\\d{1,3}>'): 0.3
           }
        global_data.emgr.on_recv_danmu_msg += self.on_recv_msg
        return

    def on_finalize_panel(self):
        global_data.emgr.on_recv_danmu_msg -= self.on_recv_msg

    def enable_danmu(self, tag):
        old = self._enable
        self._enable = tag
        if old != tag:
            self._reset_state()

    def enable_danmu_of_tag(self, tag, is_enable):
        if is_enable:
            if tag in self._forbidden_tag_set:
                self._forbidden_tag_set.remove(tag)
        else:
            if tag not in self._forbidden_tag_set:
                self._forbidden_tag_set.add(tag)
            if tag in self._tag_danmu_dict:
                for danmu_item in list(self._tag_danmu_dict[tag]):
                    if danmu_item in self._danmu_list:
                        self._danmu_list.remove(danmu_item)
                    danmu_item.Destroy()

            self._tag_danmu_dict[tag] = []

    def on_recv_msg(self, text, priority=0, head_pic=None, template=None, custom_item_func=None, tag=None):
        if not self._enable:
            return
        if tag in self._forbidden_tag_set:
            return
        priority = min(self.MAX_PRIORITY - 1, priority)
        danmu = Danmu(text, self.EXPIRE_DURATION, priority, head_pic, template, custom_item_func, tag)
        self._insert_into_cache(danmu, priority)
        if priority == self.MAX_PRIORITY - 1:
            self._update_launch_logic()

    def _reset_state--- This code section failed: ---

 114       0  BUILD_LIST_0          0 
           3  LOAD_GLOBAL           0  'range'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  'LINE_NUM'
          12  CALL_FUNCTION_1       1 
          15  GET_ITER         
          16  FOR_ITER             12  'to 31'
          19  STORE_FAST            1  'i'
          22  LOAD_CONST            1  ''
          25  LIST_APPEND           2  ''
          28  JUMP_BACK            16  'to 16'
          31  LOAD_FAST             0  'self'
          34  STORE_ATTR            2  '_protect_times'

 116      37  BUILD_LIST_0          0 
          40  LOAD_GLOBAL           0  'range'
          43  LOAD_FAST             0  'self'
          46  LOAD_ATTR             1  'LINE_NUM'
          49  CALL_FUNCTION_1       1 
          52  GET_ITER         
          53  FOR_ITER             12  'to 68'
          56  STORE_FAST            1  'i'
          59  LOAD_CONST            1  ''
          62  LIST_APPEND           2  ''
          65  JUMP_BACK            53  'to 53'
          68  LOAD_FAST             0  'self'
          71  STORE_ATTR            3  '_disappear_times'

 118      74  BUILD_LIST_0          0 
          77  LOAD_FAST             0  'self'
          80  STORE_ATTR            4  '_danmu_cache'

 119      83  SETUP_LOOP           39  'to 125'
          86  LOAD_GLOBAL           0  'range'
          89  LOAD_FAST             0  'self'
          92  LOAD_ATTR             5  'MAX_PRIORITY'
          95  CALL_FUNCTION_1       1 
          98  GET_ITER         
          99  FOR_ITER             22  'to 124'
         102  STORE_FAST            1  'i'

 120     105  LOAD_FAST             0  'self'
         108  LOAD_ATTR             4  '_danmu_cache'
         111  LOAD_ATTR             6  'append'
         114  BUILD_LIST_0          0 
         117  CALL_FUNCTION_1       1 
         120  POP_TOP          
         121  JUMP_BACK            99  'to 99'
         124  POP_BLOCK        
       125_0  COME_FROM                '83'

 121     125  SETUP_LOOP           33  'to 161'
         128  LOAD_GLOBAL           7  'getattr'
         131  LOAD_GLOBAL           2  '_protect_times'
         134  BUILD_LIST_0          0 
         137  CALL_FUNCTION_3       3 
         140  GET_ITER         
         141  FOR_ITER             16  'to 160'
         144  STORE_FAST            2  'item'

 122     147  LOAD_FAST             2  'item'
         150  LOAD_ATTR             8  'Destroy'
         153  CALL_FUNCTION_0       0 
         156  POP_TOP          
         157  JUMP_BACK           141  'to 141'
         160  POP_BLOCK        
       161_0  COME_FROM                '125'

 123     161  BUILD_LIST_0          0 
         164  LOAD_FAST             0  'self'
         167  STORE_ATTR            9  '_danmu_list'

 124     170  BUILD_MAP_0           0 
         173  LOAD_FAST             0  'self'
         176  STORE_ATTR           10  '_tag_danmu_dict'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 137

    def _insert_into_cache(self, danmu, priority=0):
        priority = min(self.MAX_PRIORITY - 1, priority)
        if priority == 0 and len(self._danmu_cache[0]) >= self.MAX_CACHE_NUM:
            return
        self._danmu_cache[priority].append(danmu)

    def _update_launch_logic(self):
        can_launch_index = -1
        while True:
            can_launch_index = self._find_valid_line()
            if can_launch_index is None:
                break
            cur_danmu = self._pop_valid_danmu()
            if cur_danmu is None:
                break
            self._launch_one_danmu(cur_danmu, can_launch_index)

        for i in range(self.LINE_NUM):
            if can_launch_index != i:
                self._protect_times[i] = max(0, self._protect_times[i] - self.UPDATE_LOGIC_INTERVAL)
                self._disappear_times[i] = max(0, self._disappear_times[i] - self.UPDATE_LOGIC_INTERVAL)

        for i, cache in enumerate(self._danmu_cache):
            for danmu in cache:
                danmu.expire_duration -= self.UPDATE_LOGIC_INTERVAL

            self._danmu_cache[i] = [ danmu for danmu in cache if danmu.expire_duration > 0 ]

        return self.UPDATE_LOGIC_INTERVAL

    def _pop_valid_danmu(self):
        for cache in reversed(self._danmu_cache):
            if len(cache) > 0:
                return cache.pop(0)

    def _find_valid_line(self):
        indexes = [
         0, 1]
        random.shuffle(indexes)
        for i in indexes:
            if self._protect_times[i] <= 0:
                return i

    def _launch_one_danmu(self, danmu, index):
        item = global_data.uisystem.load_template_create(danmu.template or self.DANMU_TEMPLATE, self.panel.nd_danmu)
        new_text = '<size=%d> %s</size>' % (self._font_size, danmu.text)
        item.setScale(1.0)
        for sub_pattern, scale in six.iteritems(self.special_message_scale_dict):
            if sub_pattern.match(danmu.text) is not None:
                item.setScale(scale)
                break

        if not danmu.custom_item_func:
            item.lab_bullet_screen.SetString(new_text)
            if danmu.head_pic:
                item.img_head.SetDisplayFrameByPath('', danmu.head_pic)
                item.img_head.setVisible(True)
            else:
                item.img_head.setVisible(False)
            item.lab_bullet_screen.formatText()
            size = item.lab_bullet_screen.getTextContentSize()
        else:
            size = danmu.custom_item_func(item, danmu)
        if danmu.tag:
            self._tag_danmu_dict.setdefault(danmu.tag, [])
            self._tag_danmu_dict[danmu.tag].append(item)
        self._danmu_list.append(item)
        posy = -index * self.LINE_WIDTH * self._nd_scale
        is_max_pri = danmu.priority >= self.MAX_PRIORITY - 1
        if not is_max_pri:
            posx = 0 if 1 else -size.width
            item.SetPosition(posx, posy)
            text_width = size.width
            pos = self._is_in_float or self.panel.nd_danmu.convertToNodeSpace(cc.Vec2(0, 0))
        else:
            wpos = self.panel.ConvertToWorldSpace(0, 0)
            pos = self.panel.nd_danmu.convertToNodeSpace(wpos)
        view_width = abs(pos.x)
        total_width = float(text_width + view_width)
        travel_width = is_max_pri or total_width if 1 else float(view_width)
        if self._disappear_times[index] > 0:
            max_speed = min(self.MAX_SPEED, view_width / self._disappear_times[index])
        else:
            max_speed = self.MAX_SPEED
        speed = random.uniform(self.MIN_SPEED, max_speed * self._nd_scale)
        duration = travel_width / speed

        def _OnFinished(tag=danmu.tag, *args):
            if item in self._danmu_list:
                self._danmu_list.remove(item)
            if tag in self._tag_danmu_dict:
                if item in self._tag_danmu_dict[tag]:
                    del self._tag_danmu_dict[tag][self._tag_danmu_dict[tag].index(item)]
            item.Destroy()

        actions = [
         cc.MoveTo.create(duration, cc.Vec2(-total_width, posy)),
         cc.CallFunc.create(_OnFinished)]
        item.runAction(cc.Sequence.create(actions))
        self._disappear_times[index] = duration
        TEXT_GAP = 100.0
        self._protect_times[index] = (text_width + TEXT_GAP) / speed + random.uniform(self.MIN_PROTECT_DURATION, self.MAX_PROTECT_DURATION)
        return

    def switch_to_float(self, is_float, wpos, size):
        if is_float:
            self._is_in_float = True
            self._reset_state()
            self.panel.setClippingEnabled(True)
            self.update_float_pos(wpos)
            scale = self.panel.getScale()
            import cc
            self.panel.setContentSize(cc.Size(size.width / scale, size.height / scale))
            self.panel.nd_danmu.SetPosition('100%', '90%')
            self.panel.nd_danmu.ChildResizeAndPosition()
            self._nd_scale = 0.5
            self._font_size = 18
        else:
            self._is_in_float = False
            self._reset_state()
            self.panel.setClippingEnabled(False)
            self.panel.ResizeAndPosition()
            self._nd_scale = 1.0
            self._font_size = 24

    def update_float_pos(self, wpos):
        lpos = self.panel.getParent().convertToNodeSpace(wpos)
        self.panel.setPosition(lpos)


def Test():
    interface = global_data.ui_mgr.show_ui('DanmuLinesUI', 'logic.comsys.observe_ui')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x88\xe5\x93\x88')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x881')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x882')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x883')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x884')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x885')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x886')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x887')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x889')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x8810')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x8811')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x8812', 1)
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x8813')
    interface.on_recv_msg('\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xe5\x95\x8a\xe5\x95\x8a\xef\xbc\x8c\xe5\x93\x88\xe5\x93\x8814')