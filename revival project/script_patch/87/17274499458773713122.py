# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/CommonTips.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
import time
from common.uisys.richtext import richtext
from cocosui import cc, ccui, ccs
import common.const.uiconst
from common.const.property_const import *
import common.utilities

class Tips(object):

    def __init__(self, parent_nd, allow_cb=None, finish_cb=None, check_has_next_cb=None):
        self._parent_nd = parent_nd
        self._allow_cb = allow_cb
        self._finish_cb = finish_cb
        self._check_has_next_cb = check_has_next_cb
        self._is_bind = False
        self._msg_data = None
        self._color = None
        self._nd = self._gen_tips_nd()
        self._nd.setVisible(False)
        self._nd.retain()
        self.use = 0
        return

    def get_msg_data(self):
        return self._msg_data

    def _gen_tips_nd(self):
        raise NotImplementedError

    def is_valid(self):
        return self._is_bind and self._nd is not None

    def bind(self, msg_data, color=None):
        if self._is_bind or not self._nd:
            return
        self._is_bind = True
        self._msg_data = msg_data
        self._color = color
        self._nd.setVisible(True)
        if not self._nd.getParent():
            self._parent_nd.AddChild('', self._nd)
        self.on_show()

    def unbind(self):
        if not self._is_bind or not self._nd:
            return
        else:
            self._is_bind = False
            self._nd.setVisible(False)
            self._nd.removeFromParent()
            self._msg_data = None
            self._color = None
            return

    def on_show(self):
        pass

    def on_other_tips_show(self):
        pass

    def on_other_tips_need_show(self):
        pass

    def _cc_allow_callback(self):
        if self._allow_cb:
            self._allow_cb()

    def _cc_finish_callback(self):
        if self._finish_cb:
            self._finish_cb()

    def _cc_check_has_next_cb_callback(self):
        if self._check_has_next_cb:
            self._check_has_next_cb()

    def destroy(self):
        if not self._nd:
            return
        else:
            self.unbind()
            self._nd.Destroy()
            self._nd.release()
            self._nd = None
            self._parent_nd = None
            self._finish_cb = None
            self._allow_cb = None
            self.msg_data = None
            return


class TipsManager(object):

    def __init__(self, parent_nd, tips_cls, color=None, max_msg_num=3, max_cache_num=3, preload_tip_num=0):
        self._parent_nd = parent_nd
        self._max_msg_num = max_msg_num
        self._can_showing_msg = True
        self._color = color
        self._on_fly_msg_nds = []
        self._message_queue = []
        self._max_cache_num = max_cache_num
        self._tip_cls = tips_cls
        preload_tip_num = min(preload_tip_num, max_cache_num) if global_data.enable_battle_ui_cache else 0
        self._tip_cache = [ self.__gen_tip_nd() for i in range(preload_tip_num) ]

    def destroy(self):
        for msg_nd in self._on_fly_msg_nds:
            msg_nd.destroy()

        self._on_fly_msg_nds = []
        for msg_nd in self._tip_cache:
            msg_nd.destroy()

        self._tip_cache = []
        self._message_queue = []
        self._max_msg_num = 3
        self._parent_nd = None
        self._can_showing_msg = False
        self._tip_cls = None
        return

    def allow_all_tips_show(self):
        if self._parent_nd:
            self._parent_nd.setVisible(True)

    def stop_all_tips_show(self):
        if self._parent_nd:
            self._parent_nd.setVisible(False)

    def set_max_msg_show_num(self, num):
        self._max_msg_num = num

    def allow_show_tips(self):
        self._can_showing_msg = True
        self._check_show_next_tips()

    def finish_show_tips(self):
        if len(self._on_fly_msg_nds) > 0:
            msg_nd = self._on_fly_msg_nds.pop(0)
            self.__cache_tip_nd(msg_nd)
        self._can_showing_msg = True
        self._check_show_next_tips()

    def check_has_tips_need_show(self):
        if len(self._message_queue) > 0:
            for fly_msg_nd in self._on_fly_msg_nds:
                fly_msg_nd.on_other_tips_need_show()

    def __gen_tip_nd(self):
        allow_cb = self.allow_show_tips
        finish_cb = self.finish_show_tips
        check_next_cb = self.check_has_tips_need_show
        return self._tip_cls(self._parent_nd, allow_cb, finish_cb, check_next_cb)

    def __get_tip_nd(self):
        if global_data.enable_battle_ui_cache and self._tip_cache:
            return self._tip_cache.pop()
        return self.__get_tip_nd()

    def __cache_tip_nd(self, tip_nd):
        if global_data.enable_battle_ui_cache and len(self._tip_cache) < self._max_cache_num:
            tip_nd.unbind()
            self._tip_cache.append(tip_nd)
        else:
            tip_nd.destroy()

    def add_tips(self, tips_data):
        if tips_data in self._message_queue:
            self._message_queue.remove(tips_data)
        self._message_queue.append(tips_data)
        self._check_show_next_tips()

    def _check_show_next_tips(self):
        _on_fly_battle_report_num = len(self._on_fly_msg_nds)
        if _on_fly_battle_report_num >= self._max_msg_num:
            return
        if not self._can_showing_msg:
            return
        self.show_tip()

    def show_tip(self):
        if self._message_queue:
            self._can_showing_msg = False
            tips_data = self._message_queue.pop(0)
            msg_nd = self.__get_tip_nd()
            msg_nd.bind(tips_data, self._color)
            for fly_msg_nd in self._on_fly_msg_nds:
                fly_msg_nd.on_other_tips_show()

            self._on_fly_msg_nds.append(msg_nd)