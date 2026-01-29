# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/prepare/FightPrepareInteractUI.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from common.const import uiconst
from logic.gcommon import time_utility as tutil
import math
COUNTDOWN_TAG = 1

class FightPrepareInteractUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_before/fight_interact'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_click.OnClick': 'on_click_interact_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        super(FightPrepareInteractUI, self).on_init_panel(*args, **kwargs)
        self.interact_cd_time = 5
        self.panel.img_prog.setVisible(False)
        self.panel.lab_prog.SetString('')
        self.interact_cd_state = False

    def on_click_interact_btn(self, btn, touch):
        if self.interact_cd_state:
            return
        if not global_data.player:
            return
        if not global_data.player.logic:
            return
        from common.cfg import confmgr
        import random
        from logic.gutils.role_head_utils import get_head_frame_res_path, get_head_photo_res_path
        _text_list = confmgr.get('born_island_quick_chat', 'content', default=[])
        text = get_text_by_id(int(random.choice(_text_list)))
        global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'battle_encourage_teammates', (text,))
        self.on_success_send()

    def on_success_send(self):
        self.panel.img_prog.setVisible(True)
        self.panel.img_prog.SetContentSize(92, 20)
        self.interact_cd_state = True
        self._send_time = tutil.get_server_time()
        self.panel.lab_prog.SetString(str(int(math.ceil(self.interact_cd_time))))
        self.update_countdown()
        self.panel.DelayCallWithTag(0.3, self.update_countdown, COUNTDOWN_TAG)

    def update_countdown(self):
        delta = self._send_time + self.interact_cd_time - tutil.get_server_time()
        percent = max(min(float(delta) / self.interact_cd_time, 1.0), 0.0)
        y = 92 * percent + 20
        delta = int(math.ceil(max(0, delta)))
        if delta == 0:
            self.panel.img_prog.setVisible(False)
            self.panel.lab_prog.SetString('')
            self.interact_cd_state = False
            return 0.0
        else:
            self.panel.img_prog.SetContentSize(92, int(y))
            self.panel.lab_prog.SetString(str(delta))
            return 0.5

    def on_finalize_panel(self):
        super(FightPrepareInteractUI, self).on_finalize_panel()