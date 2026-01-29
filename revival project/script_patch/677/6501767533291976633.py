# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/RoleBondTipsUI.py
from __future__ import absolute_import
import time
import game3d
import common.utilities
from common.cfg import confmgr
from logic.gutils import bond_utils
from logic.gcommon.cdata import bond_config
from common.uisys.basepanel import BasePanel
from logic.entities.avatarmembers.impBond import impBond
from common.const.uiconst import TOP_ZORDER, UI_TYPE_CONFIRM
from common.const.property_const import *
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import role_head_utils
from common.const import uiconst

class RoleBondTipsUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/role_bond_tips'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    UI_ACTION_EVENT = {'panel.OnClick': 'close'
       }

    def on_init_panel(self, role_id, event_info):
        self._timer = None
        self.panel.PlayAnimation('appear')
        self.init_widget(role_id, event_info)
        return

    def init_widget(self, role_id, event_info):
        self.panel.nd_level.setVisible(False)
        self.panel.temp_dialogue.setVisible(False)
        if event_info.get(impBond.BOND_STRENGTH, None):
            self.show_add_exp(role_id, event_info)
        elif event_info.get('dialog_id', None):
            self.role_show_chat(role_id, event_info.get('dialog_id'))
        else:
            self.register_timer(1)
        return

    def on_finalize_panel(self):
        self.unregister_timer()

    def register_timer(self, interval):
        from common.utils.timer import CLOCK
        tm = global_data.game_mgr.get_logic_timer()
        self.unregister_timer()
        self._timer = tm.register(func=self.close, interval=interval, times=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer:
            tm = global_data.game_mgr.get_logic_timer()
            tm.unregister(self._timer)
        self._timer = None
        return

    def show_add_exp(self, role_id, event_info):
        self.panel.nd_level.setVisible(True)
        old_lv, new_lv = event_info[impBond.BOND_LEVEL]
        old_exp, new_exp = event_info[impBond.BOND_STRENGTH]
        add_exp = bond_config.get_added_strength(old_lv, old_exp, new_lv, new_exp)
        if add_exp == 0:
            self.panel.img_plus.setVisible(False)
            self.panel.lab_plus.SetString('')
        else:
            self.panel.img_plus.setVisible(True)
            self.panel.lab_plus.SetString('{}'.format(add_exp))
        nxt_level, nxt_exp = bond_config.get_nxt_bond_level_strength(old_lv)
        new_nxt_level, new_nxt_exp = bond_config.get_nxt_bond_level_strength(new_lv)
        self.panel.lab_num.SetString('{}/{}'.format(old_exp, nxt_exp))
        old_percent = common.utilities.safe_percent(old_exp, nxt_exp)
        new_percent = common.utilities.safe_percent(new_exp, new_nxt_exp)
        self.panel.progress_exp.setPercent(old_percent)
        unit_time = 1.0
        if old_lv != new_lv:

            def end_cb():
                self.panel.lab_level.SetString('{}'.format(new_lv))
                self.panel.lab_num.SetString('{}/{}'.format(new_exp, new_nxt_exp))
                self.panel.progress_exp.setPercent(0.0)
                self.panel.progress_exp.SetPercent(new_percent, time=(new_percent - 0.0) / 100.0 * unit_time)

            self.panel.progress_exp.SetPercent(100.0, time=(100.0 - old_percent) / 100.0 * unit_time, end_cb=end_cb)
        else:

            def end_cb():
                self.panel.lab_num.SetString('{}/{}'.format(new_exp, new_nxt_exp))

            self.panel.progress_exp.SetPercent(new_percent, time=(new_percent - old_percent) / 100.0 * unit_time, end_cb=end_cb)
        self.panel.lab_level.SetString('LV.{}'.format(old_lv))
        dialog_id = bond_utils.get_gift_dialog_id(role_id, bond_exp=add_exp)
        self.role_show_chat(role_id, dialog_id)

    def role_show_chat(self, role_id, dialog_id):
        from logic.gutils import item_utils
        self.panel.temp_dialogue.setVisible(True)
        dialog_conf = confmgr.get('role_dialog_config', 'role_{}_dialog'.format(role_id), 'Content', str(dialog_id), default={})
        text = dialog_conf.get('content_text_id')
        show_time = dialog_conf.get('show_time', 2)
        show_time += 10
        self.panel.temp_dialogue.lab_name.SetString(item_utils.get_lobby_item_name(role_id))
        if dialog_conf:
            self.panel.temp_dialogue.lab_dialogue.SetString(text)
            self.panel.temp_dialogue.PlayAnimation('play')
        else:
            self.panel.temp_dialogue.setVisible(False)
        self.register_timer(show_time)