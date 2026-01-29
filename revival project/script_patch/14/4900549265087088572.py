# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/NewbieBondMechaConfirmUI.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gutils.template_utils import init_tempate_reward
from logic.gutils.item_utils import get_lobby_item_name
from common.cfg import confmgr

class NewbieBondMechaConfirmUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'activity/activity_202206/comeback_sys/i_backflow_mecha_tips'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_ACTION_EVENT = {'panel.temp_window.img_window_bg.temp_btn_1.btn_common_big.OnClick': 'on_close',
       'panel.temp_window.img_window_bg.temp_btn_2.btn_common_big.OnClick': 'on_confirm',
       'panel.temp_window.btn_close.OnClick': 'on_close'
       }

    def config(self, reward_id, callback):
        self.callback = callback
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        item_id, item_num = reward_conf['reward_list'][0]
        dir = 'gui/ui_res_2/item/role_head/%s.png' % ('3021' + str(item_id % 10000))
        mecha_name = get_lobby_item_name(item_id)
        self.panel.pic.SetDisplayFrameByPath('', dir)
        text = get_text_by_id(611426)
        text = text.format(mechaname=mecha_name)
        self.panel.lab_tips.setString(text)

    def on_init_panel(self, *args, **kwargs):
        super(NewbieBondMechaConfirmUI, self).on_init_panel(*args, **kwargs)

    def on_close(self, *args):
        self.callback(False, True)
        self.close()

    def on_confirm(self, *args):
        self.callback(True)
        self.close()