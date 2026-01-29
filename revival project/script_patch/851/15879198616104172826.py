# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/NoticeUI.py
from __future__ import absolute_import
import six_ex
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER, UI_TYPE_MESSAGE
from time import time
from common.uisys.uielment.CCRichText import CCRichText
MESSAGE_SHOW_TIME = 3
MESSAGE_APPEAR = 0.3
MESSAGE_DISAPPEAR = 0.3
MESSAGE_MAX_COUNT = 3
from common.const import uiconst

class NoticeUI(BasePanel):
    PANEL_CONFIG_NAME = 'notice/sys_feedback'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_MESSAGE

    def on_init_panel(self):
        self.init_event()
        self.init_widget()

    def init_event(self):
        self._message_list = []
        self._appear_pos = self.panel.appear.getPosition()
        self._disappear_pos = self.panel.disappear.getPosition()
        self._additional_margin = 2
        self._height = 46

    def init_widget(self):
        panel = self.panel
        panel.appear.setVisible(False)
        panel.disappear.setVisible(False)

    def check_massage_count(self):
        if len(self._message_list) > MESSAGE_MAX_COUNT:
            self.pop_message()

    def on_resolution_changed(self):
        self.pop_message()

    def add_message(self, message_text):
        import cc
        MARGIN = 46
        if type(message_text) not in [str, six.text_type, int, six_ex.long_type]:
            from common.uisys.uielment.CCNode import CCNode
            feed_item = message_text
        else:
            feed_item = global_data.uisystem.load_template_create('notice/i_sys_feedback_item')
            rt_msg = feed_item.lab_notice
            rt_msg.SetString(message_text)
            rt_msg.formatText()
            height = max(rt_msg.getVirtualRendererSize().height + MARGIN, feed_item.bar.getContentSize().height)
            feed_item.bar.SetContentSize(feed_item.bar.getContentSize().width, height)
            rt_msg.ReConfPosition()
        self.panel.AddChild(None, feed_item)
        feed_item.setPosition(self._appear_pos)
        if self._message_list:
            message_all_height_list = [ item.bar.getContentSize().height + self._additional_margin for item, _ in self._message_list ]
            message_height = sum(message_all_height_list)
        else:
            message_height = 0
        target_pos = cc.Vec2(self._disappear_pos.x, self._disappear_pos.y - message_height)
        feed_item.stopAllActions()
        if self._message_list:
            feed_item.runAction(cc.Sequence.create([
             cc.MoveTo.create(MESSAGE_APPEAR, target_pos),
             cc.CallFunc.create(self.check_massage_count)]))
        else:
            feed_item.runAction(cc.Sequence.create([
             cc.MoveTo.create(MESSAGE_APPEAR, target_pos),
             cc.DelayTime.create(MESSAGE_SHOW_TIME),
             cc.CallFunc.create(self.pop_message)]))
        self._message_list.append((feed_item, time()))
        return

    def pop_message(self):
        if not self._message_list:
            return
        feed_item, create_time = self._message_list.pop(0)
        import cc
        feed_item.stopAllActions()
        feed_item.setPosition(self._disappear_pos)
        feed_item.PlayAnimation('replace')

        def _cc_remove():
            self.remove_item(feed_item)

        feed_item.runAction(cc.Sequence.create([
         cc.DelayTime.create(MESSAGE_DISAPPEAR),
         cc.CallFunc.create(_cc_remove)]))
        above_height = 0
        for index, item_info in enumerate(self._message_list):
            item, create_time = item_info
            target_pos = cc.Vec2(self._disappear_pos.x, self._disappear_pos.y - above_height)
            above_height += item.bar.getContentSize().height + self._additional_margin
            item.stopAllActions()
            if index == 0:
                left_time = MESSAGE_SHOW_TIME + MESSAGE_APPEAR - time() + create_time
                if left_time <= 0:
                    left_time = 0.01
                item.runAction(cc.Sequence.create([
                 cc.MoveTo.create(MESSAGE_DISAPPEAR, target_pos),
                 cc.CallFunc.create(self.check_massage_count),
                 cc.DelayTime.create(left_time),
                 cc.CallFunc.create(self.pop_message)]))
            else:
                item.runAction(cc.MoveTo.create(MESSAGE_DISAPPEAR, target_pos))

    def remove_item(self, item_widget):
        item_widget.removeFromParent()