# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotterySlotMachineUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_cur_lang_name
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc
NUMBER_KEY = 'number'
DISCOUNT_KEY = 'discount'
DEFAULT_SHOW_TEXT = '?'

class LotterySlotMachineUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/i_collection_activity/cswz_pet/open_cswz_pet_lottery'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'panel.btn_open.OnClick': 'on_click_btn_open',
       'panel.btn_close.OnClick': 'on_click_btn_close'
       }
    GLOBAL_EVENT = {'receive_slot_machine_ret_event': 'on_receive_slot_machine_ret'
       }
    SLOT_MACHINE_TAG = 2024032913

    def on_init_panel(self, lottery_id=None):
        self.lottery_id = lottery_id
        self.update_slot_machine_display()
        self.update_btn_open()
        archive_key_open = 'opened_lottery_{}'.format(self.lottery_id)
        if global_data.achi_mgr:
            global_data.achi_mgr.set_cur_user_archive_data(archive_key_open, True)

    def update_slot_machine_display(self):
        player = global_data.player
        if not player or not player.get_slot_machine_record(str(self.lottery_id)):
            self.panel.bar_bg_0.lab_num.SetString(DEFAULT_SHOW_TEXT)
            self.panel.bar_bg_1.lab_num.SetString(DEFAULT_SHOW_TEXT)
            self.panel.bar_bg_2.lab_num.SetString(DEFAULT_SHOW_TEXT)
            return
        init_number = player.get_slot_machine_init_number(str(self.lottery_id))
        number = player.get_slot_machine_number(str(self.lottery_id))
        discount = player.get_slot_machine_discount(str(self.lottery_id))
        self.panel.bar_bg_0.lab_num.SetString(str(int(init_number / 10)))
        self.panel.bar_bg_1.lab_num.SetString(str(int(init_number % 10)))
        if get_cur_lang_name() == 'cn':
            self.panel.bar_bg_2.lab_num.SetString(str(discount))
        else:
            self.panel.bar_bg_2.lab_num.SetString(str(10 - discount))
        self.panel.lab_tips_times.SetString(get_text_by_id(860410).format(num=number))

    def update_btn_open(self):
        player = global_data.player
        if player and not player.get_slot_machine_record(str(self.lottery_id)):
            show_open = True
        else:
            show_open = False
        self.panel.btn_open.setVisible(show_open)
        self.panel.lab_tips_discount.setVisible(not show_open)
        self.panel.lab_tips_times.setVisible(not show_open)

    def on_finalize_panel(self):
        self.panel.stopActionByTag(self.SLOT_MACHINE_TAG)
        global_data.emgr.player_money_info_update_event.emit()
        super(LotterySlotMachineUI, self).on_finalize_panel()

    def on_click_btn_close(self, *args):
        self.close()

    def on_click_btn_open(self, *args):
        player = global_data.player
        if not player or not self.lottery_id:
            return
        if self.panel.IsPlayingAnimation('show'):
            return
        if player.get_slot_machine_record(str(self.lottery_id)):
            return
        player.start_slot_machine(self.lottery_id)

    def on_receive_slot_machine_ret(self, *args):
        player = global_data.player
        if not player or not self.lottery_id:
            return
        record = player.get_slot_machine_record(str(self.lottery_id))
        if not record:
            return
        act_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show')),
         cc.CallFunc.create(lambda : self.update_btn_open()),
         cc.CallFunc.create(lambda : global_data.emgr.player_money_info_update_event.emit())]
        act = cc.Sequence.create(act_list)
        act.setTag(self.SLOT_MACHINE_TAG)
        self.panel.runAction(act)
        self.update_slot_machine_display()