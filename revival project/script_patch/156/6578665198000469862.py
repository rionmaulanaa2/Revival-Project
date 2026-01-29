# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/KothMoneyWidget.py
from __future__ import absolute_import
from logic.gutils import item_utils
from logic.gcommon import const
from logic.gutils import koth_shop_utils

class KothMoneyWidget(object):
    WIDGET_CONF = 'battle_koth/i_koth_currency'

    def __init__(self, parent):
        self.panel = global_data.uisystem.load_template_create(self.WIDGET_CONF, parent)
        self.process_event(True)
        self.panel.setVisible(False)

    def get_global_data_event_confs(self):
        return {'update_koth_money_info_event': self.update_koth_money_info}

    def update_koth_money_info(self, entity_id, money_dict):
        if not global_data.cam_lplayer:
            return
        self.panel.setVisible(True)
        if entity_id == global_data.cam_lplayer.id:
            koth_shop_utils.init_koth_own_money2(self.panel, money_dict)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = self.get_global_data_event_confs()
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)
        if self.panel:
            self.panel.Destroy()
        self.panel = None
        return

    def init_widget(self):
        self.init_player_money_label()

    def init_player_money_label(self):
        if not global_data.cam_lplayer:
            return
        self.panel.setVisible(True)
        money_info = global_data.king_battle_data.get_money_info(global_data.cam_lplayer.id)
        self.money_dict = money_info
        koth_shop_utils.init_koth_own_money2(self.panel, money_info)