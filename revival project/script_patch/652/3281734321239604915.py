# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/PressBtnComponent.py
from __future__ import absolute_import
from common.utils.cocos_utils import ccp

class PressBtnComponent(object):
    ADD_ACT_TAG = 19010701
    SUB_ACT_TAG = 19010702

    def __init__(self, panel, *arg):
        self.panel = panel
        self._num_change_cb = None
        self._max_cb = None
        return

    def set_args(self, *arg):
        self.arg = arg[0]
        self.break_change = False
        self.per_num = self.arg.get('per_num', 1)
        self.min_num = self.arg.get('min_num')
        self.max_num = self.arg.get('max_num')
        self.press_event = self.arg.get('press_event', True)
        self.begin_num = self.arg.get('begin_num', self.min_num)
        self.num = self.begin_num
        self.begin_ttf = self.arg.get('begin_ttf', self.begin_num)
        self.delay_time = self.arg.get('delay_time', 0.03)
        self.start_timer_time = self.arg.get('start_timer_time', 0.5)
        self.enable_keyboard = self.arg.get('enable_keyboard', False)
        self.keyboard_wpos = self.arg.get('keyboard_wpos', ccp(200, 200))
        self.max_tips = 81920
        self._init()

    def destroy(self):
        if self.panel:
            self.panel.stopAllActions()
            self.panel.btn_minus.stopAllActions()
            self.panel.btn_plus.stopAllActions()
        self.panel = None
        self._num_change_cb = None
        self._max_cb = None
        return

    def _init(self):
        self.regist_btn_evn()
        self.set_begin_status()

    def set_min_num(self, min_num):
        self.min_num = min_num
        self.set_btn_plus_minus_enable()

    def set_max_num(self, max_num):
        self.max_num = max_num
        self.set_btn_plus_minus_enable()

    def set_num(self, num):
        self.num = max(min(num, self.max_num), self.min_num)
        self.set_btn_plus_minus_enable()
        self.OnNumChange()

    def set_max_tips(self, tips):
        self.max_tips = tips

    def get_num(self):
        return self.num

    def regist_btn_evn(self):
        panel = self.panel

        @panel.btn_minus.callback()
        def OnBegin(btn, touch):
            btn.SetSelect(True)
            if not self.press_event:
                return True
            flag = False
            btn.SetTimeOut(self.start_timer_time, lambda flag=flag: self.start_num_change_timer(flag), self.SUB_ACT_TAG)
            self.break_change = False
            return True

        @panel.btn_minus.callback()
        def OnEnd(btn, touch):
            btn.SetSelect(False)
            if not self.press_event:
                return
            self.break_change = True
            btn.stopActionByTag(self.SUB_ACT_TAG)

        @panel.btn_minus.callback()
        def OnClick(btn, touch):
            self.num += self.per_num * -1
            self.num = max(self.num, self.min_num)
            self.set_btn_plus_minus_enable()
            self.OnNumChange()

        @panel.btn_minus.callback()
        def OnCancel(btn, touch):
            if not self.press_event:
                return True
            self.break_change = True
            btn.stopActionByTag(self.SUB_ACT_TAG)
            btn.SetSelect(False)
            return True

        @panel.btn_plus.callback()
        def OnBegin(btn, touch):
            btn.SetSelect(True)
            if not self.press_event:
                return True
            flag = True
            self.break_change = False
            btn.SetTimeOut(self.start_timer_time, lambda flag=flag: self.start_num_change_timer(flag), self.ADD_ACT_TAG)
            return True

        @panel.btn_plus.callback()
        def OnEnd(btn, touch):
            btn.SetSelect(False)
            if not self.press_event:
                return
            self.break_change = True
            btn.stopActionByTag(self.ADD_ACT_TAG)

        @panel.btn_plus.callback()
        def OnCancel(btn, touch):
            if not self.press_event:
                return
            self.break_change = True
            btn.stopActionByTag(self.ADD_ACT_TAG)
            btn.SetSelect(False)
            return True

        @panel.btn_plus.callback()
        def OnClick(btn, touch):
            self.num += self.per_num * 1
            if self.num > self.max_num:
                if callable(self._max_cb):
                    self._max_cb(self.max_num)
                global_data.game_mgr.show_tip(get_text_local_content(self.max_tips))
            self.num = min(self.max_num, self.num)
            self.set_btn_plus_minus_enable()
            self.OnNumChange()

    def set_begin_status(self):
        panel = self.panel
        panel.lab_num.setString(str(self.begin_ttf))
        self.set_btn_plus_minus_enable()

    def set_num_change_callback(self, callback):
        self._num_change_cb = callback

    def set_max_callback(self, max_callback):
        self._max_cb = max_callback

    def OnNumChange(self):
        if self._num_change_cb:
            self._num_change_cb(self.get_num())

    def start_num_change_timer(self, flag):
        panel = self.panel
        panel.DelayCall(self.delay_time, lambda flag: self.change_num(flag), flag)

    def change_num(self, flag):
        panel = self.panel
        mul = 1
        if not flag:
            mul = -1
        self.num += self.per_num * mul
        next_delay_time = None
        if self.num < self.min_num:
            self.break_change = True
            self.num = self.min_num
        if self.num > self.max_num:
            self.break_change = True
            self.num = self.max_num
        if self.num <= self.max_num and self.num >= self.min_num and not self.break_change:
            next_delay_time = self.delay_time
        self.OnNumChange()
        self.set_btn_plus_minus_enable()
        return next_delay_time

    def set_btn_plus_minus_enable(self):
        panel = self.panel
        flag = self.num < self.max_num
        panel.btn_plus.SetShowEnable(flag)
        flag = self.num > self.min_num
        panel.btn_minus.SetShowEnable(flag)