# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoCoin.py
from __future__ import absolute_import
from __future__ import print_function
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_TYPE_MESSAGE
from logic.gcommon import const

class BattleInfoCoin(BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle/fight_get_coin'
    UI_TYPE = UI_TYPE_MESSAGE

    def init_parameters(self):
        super(BattleInfoCoin, self).init_parameters()
        self.playing_up = False
        self.up_message_sequence = []
        self.cur_kill_panel = None
        return

    def add_message(self, *args):
        coin_num, reason = args
        print(coin_num, 'reason:', reason)
        if reason == const.SYS_ADD_COIN:
            self.up_message_sequence.append(coin_num)
            self.process_next_up_message()
        else:
            self.message_sequence.append((coin_num, reason))
            self.process_next_message()

    def process_next_message(self):
        if not self.playing:
            if len(self.message_sequence) > 0:
                message = self.message_sequence.pop(0)
                self.playing = True
                self.process_one_message(message, self.finish_cb)
        self.check_finish()

    def process_next_up_message(self):
        if not self.playing_up:
            if len(self.up_message_sequence) > 0:
                message = self.up_message_sequence.pop(0)
                self.playing_up = True
                self.process_one_up_message(message, self.finish_cb_up)
        self.check_finish()

    def finish_cb_up(self):
        if self and self.is_valid():
            self.playing_up = False
            self.process_next_up_message()

    def process_one_up_message(self, coin_num, finish_cb):
        nd_coin = self.panel.nd_coin_rank
        self.play_effect(nd_coin, finish_cb, coin_num)

    def process_one_message(self, message, finish_cb):
        coin_num, reason = message
        nd_coin = self.panel.nd_coin_kill
        self.play_effect(nd_coin, finish_cb, coin_num)

    def play_effect(self, nd_coin, finish_cb, coin_num):
        nd_coin.lab_kill_coin.SetString('+{}'.format(coin_num))
        time = nd_coin.GetAnimationMaxRunTime('coin_get')

        def finished():
            if self and self.is_valid():
                nd_coin.setVisible(False)
                finish_cb()

        nd_coin.stopAllActions()
        nd_coin.SetTimeOut(time, finished)
        nd_coin.PlayAnimation('coin_get')
        nd_coin.setVisible(True)

    def check_finish(self):
        if not self.playing and not self.playing_up and len(self.message_sequence) <= 0 and len(self.up_message_sequence) <= 0:
            if self.on_process_done:
                self.on_process_done()
            else:
                self.close()