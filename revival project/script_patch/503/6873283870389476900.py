# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BuffInfoUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from common.utils import timer
from common.const import uiconst
RES_DICT = {'frozen': {'img': 'gui/ui_res_2/battle/attack/icon_freeze.png',
              'pro': 'gui/ui_res_2/battle/progress/hp_btn_mech_100.png',
              'lab': 18234
              },
   'immobilized': {'img': 'gui/ui_res_2/battle/attack/icon_paralysis.png',
                   'pro': 'gui/ui_res_2/battle/progress/hp_btn_human_25.png',
                   'lab': 80251
                   }
   }

class BuffInfoUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_paralysis'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def set_res_path(self, res_type):
        if not self.panel or res_type not in RES_DICT:
            return
        res_dict = RES_DICT[res_type]
        self.panel.img_paralysis.SetDisplayFrameByPath('', res_dict['img'])
        self.panel.pro.SetPath('', res_dict['pro'])
        self.panel.lab_debuff.SetString(res_dict['lab'])

    def on_init_panel(self, *args, **kargs):
        self._cur_time = 10.0
        self._all_time = 10.0
        self.timer = None
        return

    def set_cd_time(self, cd_time):
        self._cur_time = cd_time
        self._all_time = cd_time
        if self._all_time > 0:
            self.show()
        else:
            self.hide()

    def update_callback(self, dt):
        if self._cur_time <= 0:
            self.hide()
            return
        self._cur_time = max(0.0, self._cur_time - dt)
        per = int(self._cur_time * 100.0 / self._all_time)
        self.panel.nd_pro.pro.setPercent(per)

    def destroy_timer(self):
        if not self.timer:
            return
        else:
            global_data.game_mgr.unregister_logic_timer(self.timer)
            self.timer = None
            return

    def do_show_panel(self):
        super(BuffInfoUI, self).do_show_panel()
        if not self.timer:
            self.timer = global_data.game_mgr.register_logic_timer(self.update_callback, interval=1, timedelta=True)
        self.hide_main_ui(['FrontSightUI'])
        self.panel.PlayAnimation('show_paralysis')

    def do_hide_panel(self):
        super(BuffInfoUI, self).do_hide_panel()
        self.destroy_timer()
        self.show_main_ui()
        self.panel.StopAnimation('show_paralysis')

    def on_finalize_panel(self):
        self.destroy_timer()
        self.show_main_ui()