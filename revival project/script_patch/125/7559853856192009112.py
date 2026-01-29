# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/NumberChangeWidget.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.BaseUIWidget import BaseUIWidget

class NumberChangeWidget(BaseUIWidget):

    def set_number(self, set_num):
        if self._num == set_num:
            return
        if set_num > self._max_num:
            set_num = self._max_num
        length = len(str(set_num))
        set_num_str = '0' * (self._total_digit - length) + str(set_num)
        is_continuous_zero = True
        for x in range(self._total_digit):
            item = self.panel.GetItem(x)
            old_digit = item.lab_after.getString()
            digit = set_num_str[x]
            if digit != '0':
                is_continuous_zero = False
            if is_continuous_zero and digit == '0':
                item.lab_after.SetColor('#SC')
            else:
                item.lab_after.SetColor(10617051)
            if self.is_first_set:
                item.lab_after.setString(digit)
                item.lab_before.setString(old_digit)
            elif old_digit != digit:
                anim_time = item.GetAnimationMaxRunTime('refresh')
                item.PlayAnimation('refresh')

                def cb_1(node=item):
                    after_str = node.lab_after.getString()
                    node.lab_before.setString(after_str)

                def cb_2(node=item, num=digit, old_num=old_digit):
                    node.lab_after.setString(num)
                    node.lab_before.setString(old_num)

                item.SetTimeOut(anim_time, cb_1)
                item.SetTimeOut(0.04, cb_2)

        self._num = set_num
        self.is_first_set = False

    def __init__(self, parent_ui, panel):
        super(NumberChangeWidget, self).__init__(parent_ui, panel)
        self._total_digit = self.panel.GetItemCount()
        self._max_num = int('9' * self._total_digit)
        self.is_first_set = True
        self._num = 0
        for item in self.panel.GetAllItem():
            item.lab_after.setString('0')