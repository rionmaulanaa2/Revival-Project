# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/EndLikeNoticeUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER, UI_TYPE_MESSAGE
from time import time
from common.uisys.uielment.CCRichText import CCRichText
from logic.gutils.role_head_utils import set_role_head_photo
MESSAGE_SHOW_TIME = 3
MESSAGE_APPEAR = 0.3
MESSAGE_DISAPPEAR = 0.3
MESSAGE_MAX_COUNT = 4
from common.const import uiconst

class EndLikeNoticeUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_like_notice'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_MESSAGE

    def on_init_panel(self):
        self.init_event()
        self.init_widget()

    def init_event(self):
        self._message_list = []
        self._message_appear_time_list = []
        self._appear_pos = self.panel.appear.getPosition()
        self._disappear_pos = self.panel.disappear.getPosition()
        self._additional_margin = 2

    def init_widget(self):
        panel = self.panel
        panel.appear.setVisible(False)
        panel.disappear.setVisible(False)

    def on_resolution_changed(self):
        self.pop_message()

    def add_message(self, message_text, photo_no, is_teammate=True):
        import cc
        feed_item = global_data.uisystem.load_template_create('end/i_end_like_notice')
        set_role_head_photo(feed_item.temp_head, photo_no)
        feed_item.bar_red.setVisible(not is_teammate)
        feed_item.bar_blue.setVisible(is_teammate)
        like_msg = feed_item.lab_like
        like_msg.SetString(message_text)
        self.panel.AddChild(None, feed_item)
        feed_item.setVisible(False)
        feed_item.setPosition(self._appear_pos)
        if self._message_list:
            message_all_height_list = [ item.getContentSize().height + self._additional_margin for item in self._message_list ]
            message_height = sum(message_all_height_list)
        else:
            message_height = 0
        target_pos = cc.Vec2(self._disappear_pos.x, self._disappear_pos.y - message_height)
        feed_item.stopAllActions()
        if self._message_list:
            if len(self._message_list) < MESSAGE_MAX_COUNT:
                feed_item.setVisible(True)
            feed_item.runAction(cc.Sequence.create([
             cc.MoveTo.create(MESSAGE_APPEAR, target_pos)]))
        else:
            feed_item.setVisible(True)
            feed_item.runAction(cc.Sequence.create([
             cc.MoveTo.create(MESSAGE_APPEAR, target_pos),
             cc.DelayTime.create(MESSAGE_SHOW_TIME),
             cc.CallFunc.create(self.pop_message)]))
        self._message_list.append(feed_item)
        self._message_appear_time_list.append(time())
        return

    def pop_message(self):
        if not self._message_list or not self._message_appear_time_list:
            return
        feed_item = self._message_list.pop(0)
        self._message_appear_time_list.pop(0)
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
        for index, item in enumerate(self._message_list):
            create_time = self._message_appear_time_list[index]
            target_pos = cc.Vec2(self._disappear_pos.x, self._disappear_pos.y - above_height)
            above_height += item.getContentSize().height + self._additional_margin
            item.stopAllActions()
            if index == 0:
                left_time = MESSAGE_SHOW_TIME + MESSAGE_APPEAR - time() + create_time
                if left_time <= 0:
                    left_time = 0.01
                item.runAction(cc.Sequence.create([
                 cc.MoveTo.create(MESSAGE_DISAPPEAR, target_pos),
                 cc.DelayTime.create(left_time),
                 cc.CallFunc.create(self.pop_message)]))
            elif index < MESSAGE_MAX_COUNT:
                if not item.isVisible():
                    item.setVisible(True)
                    self._message_appear_time_list[index] = time()
                item.runAction(cc.MoveTo.create(MESSAGE_DISAPPEAR, target_pos))
            else:
                item.runAction(cc.MoveTo.create(MESSAGE_DISAPPEAR, target_pos))

    def remove_item(self, item_widget):
        item_widget.removeFromParent()