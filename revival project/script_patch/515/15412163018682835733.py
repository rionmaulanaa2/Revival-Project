# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/TenBenefitsUI.py
from __future__ import absolute_import
from logic.gcommon.common_const import activity_const
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.comsys.activity.SpringFestival.ActivityTenBenefits import TenBenefitsBase

class TenBenefitsUI(SimpleAdvance, TenBenefitsBase):
    PANEL_CONFIG_NAME = 'activity/open_202101/open_ten_benefits'
    APPEAR_ANIM = 'show'
    NEED_GAUSSIAN_BLUR = False
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'close'
       }

    def __init__(self, *arg, **kwargs):
        TenBenefitsBase.__init__(self, *arg, **kwargs)

    def on_custom_template_create(self, *args, **kwargs):
        self._custom_template_info = None
        if G_IS_NA_PROJECT:
            self._custom_template_info = {'temp_ten_benefits': {'template_info': {'nd_list': {'ccbFile': 'activity/activity_202101/i_activity_ten_benefits_item_overseas'}}}}
        return

    def set_content(self):
        self._activity_type = activity_const.ACTIVITY_SPRING_TEN_BENEFITS
        self._init_panel(root_panel=self.panel.temp_ten_benefits)
        self.panel.temp_ten_benefits.img_bg.SetPosition('50%98', '50%')
        self.panel.temp_ten_benefits.img_mask.SetPosition('50%98', '50%')

    def on_finalize_panel(self):
        SimpleAdvance.on_finalize_panel(self)
        self._finalize_panel()

    def on_resolution_changed(self):
        self._on_resolution_changed()