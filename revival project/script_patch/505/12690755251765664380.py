# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/GuideHelperUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import GUIDE_LAYER_ZORDER
from common.const import uiconst
from logic.gutils import guide_utils
from common.framework import Functor

class GuideHelperUI(BasePanel):
    PANEL_CONFIG_NAME = 'guide/guide_force_ui'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        self._touch_area_list = []
        self._nd_action_list_dict = {}
        self._from_guide_name = ''
        self._has_else_action = False
        self._trigger_else_action = False
        self.panel.BindMethod('OnBegin', self.on_check_guide)
        self.panel.BindMethod('OnEnd', lambda btn, touch: self.on_check_guide_on_end(btn, touch))
        self.panel.BindMethod('OnClick', lambda btn, touch: self.on_check_guide_on_action(btn, touch, 'OnClick'))
        self.panel.BindMethod('OnCancel', self._on_touch_cancel)

    def on_finalize_panel(self):
        self._touch_area_list = []

    def set_touch_area_list(self, nd_list):
        self._touch_area_list = nd_list
        self.panel.SetSwallowTouch(True)

    def on_check_guide(self, btn, touch):
        if not self._touch_area_list and not self._nd_action_list_dict:
            return False
        pos = touch.getLocation()
        for nd in self._touch_area_list:
            if nd.isValid():
                if nd.IsPointIn(pos):
                    return False

        self._trigger_else_action = True
        for nd, nd_click_action in six.iteritems(self._nd_action_list_dict):
            if nd == '_else_':
                continue
            if nd.isValid():
                if nd.IsPointIn(pos):
                    self._trigger_else_action = False
                    return False

        return True

    def on_check_guide_on_end(self, btn, touch):
        self.on_check_guide_on_action(btn, touch, 'OnEnd')
        self._trigger_else_action = False

    def on_check_guide_on_action(self, btn, touch, click_filter='OnClick'):
        pos = touch.getLocation()
        for nd, nd_click_action in six.iteritems(self._nd_action_list_dict):
            if nd == '_else_':
                continue
            if nd.isValid():
                if not nd.IsPointIn(pos):
                    continue
                if click_filter == 'OnClick':
                    self.check_execute_action(nd_click_action, click_filter)

        if self._has_else_action:
            else_action = self._nd_action_list_dict.get('_else_')
            self.check_execute_action(else_action, click_filter)

    def check_execute_action(self, nd_click_action, click_filter):
        has_execute = False
        for click_type, action_list in six.iteritems(nd_click_action):
            if click_filter == click_type:
                for action in action_list:
                    action_func_name = action[0]
                    action_func = getattr(guide_utils, action_func_name)
                    if callable(action_func):
                        self.panel.SetTimeOut(0.01, lambda : action_func(self._from_guide_name, action))
                    else:
                        log_error('check_execute_action: failed to execute!', action_func_name)

        return has_execute

    def set_click_action_list(self, from_guide_name, nd_action_list_dict):
        self._from_guide_name = from_guide_name
        self._nd_action_list_dict = nd_action_list_dict
        if self._nd_action_list_dict:
            self.panel.SetSwallowTouch(False)
        self._has_else_action = '_else_' in self._nd_action_list_dict

    def _on_touch_cancel(self, btn, touch):
        self._trigger_else_action = False