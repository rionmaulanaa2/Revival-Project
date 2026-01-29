# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/observe_zorder_helper.py
from __future__ import absolute_import
from logic.gcommon.common_const.ui_operation_const import OBSERVE_TOUCHABLE_ZORDER, OBSERVE_UI_ZORDER, OBSERVE_UNTOUCH_ZORDER
from common.const import uiconst

def check_set_observe_show_panel_zorder(target_panel, can_touch, observe_ui_zorder=uiconst.BASE_LAYER_ZORDER):
    if can_touch:
        if target_panel.on_get_template_zorder() == observe_ui_zorder:
            target_panel.panel.setLocalZOrder(OBSERVE_TOUCHABLE_ZORDER)
        elif target_panel.on_get_template_zorder() < observe_ui_zorder:
            log_error('Target panel %s can not be set to touchable!!!' % target_panel.get_name())
    elif target_panel.on_get_template_zorder() == observe_ui_zorder:
        target_panel.panel.setLocalZOrder(OBSERVE_UNTOUCH_ZORDER)
    elif target_panel.on_get_template_zorder() > observe_ui_zorder:
        log_error('Target panel %s can not be set to untouchable!!!' % target_panel.get_name())