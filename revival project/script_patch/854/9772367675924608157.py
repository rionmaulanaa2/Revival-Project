# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/NormalAttendSignUI.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name
from logic.gcommon.common_const.activity_const import SIGN_STATE_WAIT_SIGN, SIGN_STATE_WAIT_REMEDY, SIGN_STATE_GET_REWARD, SIGN_STATE_INVALID, RETRO_SIGN_COST
import logic.gcommon.time_utility as tutil
from logic.gutils.mall_utils import check_payment
import logic.gcommon.const as gconst

class NormalAttendSignUI(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/sign_7d_common'

    def set_content(self):
        self.refresh_list_reward()

    def refresh_list_reward(self):
        start_time, reward_status, day_no = global_data.player.get_normal_attend_info()
        if day_no > 7:
            day_no = 7
        self.panel.lab_describe.SetString(606053)
        for i, item in enumerate(self.panel.list_sign_6.GetAllItem()):
            self.init_item(item, i + 1, reward_status[i], day_no)

        self.init_item(self.panel.list_sign_7, 7, reward_status[6], day_no)
        show_btn_sign = True
        btn_sign = self.panel.temp_btn_sign
        btn_resign = self.panel.temp_btn_resign
        if reward_status[day_no - 1] == SIGN_STATE_WAIT_SIGN:
            btn_sign.btn_common_big.SetEnable(True)
            btn_sign.btn_common_big.SetText(604007)

            @btn_sign.btn_common_big.unique_callback()
            def OnClick(btn, touch):
                global_data.player and global_data.player.daily_sign()

        else:
            remedy_day_no = None
            for i, status in enumerate(reward_status):
                if status == SIGN_STATE_WAIT_REMEDY:
                    remedy_day_no = i + 1
                    break

            if remedy_day_no:
                show_btn_sign = False
                btn_resign.btn_common_big.SetText(604008)
                self.panel.lab_coin.SetString(str(RETRO_SIGN_COST))

                @btn_resign.btn_common_big.unique_callback()
                def OnClick(btn, touch, day_no=remedy_day_no):
                    self.try_resign_in(day_no)

            else:
                btn_sign.btn_common_big.SetEnable(False)
                btn_sign.btn_common_big.SetText(604010)
        btn_sign.setVisible(show_btn_sign)
        btn_resign.setVisible(not show_btn_sign)
        return

    def init_item(self, item, item_day, status, day_no):
        reward_id = str(18000010 + item_day)
        item_no, item_cnt = confmgr.get('common_reward_data', reward_id, 'reward_list')[0]
        pic_path = get_lobby_item_pic_by_item_no(item_no)
        item.img_item.SetDisplayFrameByPath('', pic_path)
        if item_cnt > 1:
            item.lab_num.setVisible(True)
            item.lab_num.SetString('x' + str(item_cnt))
        else:
            item.lab_num.setVisible(False)
        name = get_lobby_item_name(item_no)
        item.lab_name.SetString(name)
        item.lab_day.SetString(606053 + item_day)
        item.nd_today.setVisible(item_day == day_no)
        item.nd_get.setVisible(status == SIGN_STATE_GET_REWARD)
        item.nd_sign.setVisible(status == SIGN_STATE_WAIT_REMEDY)
        item.StopAnimation('get_tips')
        item.nd_get_tips.setVisible(False)
        if item_day == day_no and status == SIGN_STATE_WAIT_SIGN:
            item.PlayAnimation('get_tips')
        if status in (SIGN_STATE_GET_REWARD, SIGN_STATE_INVALID) or status == SIGN_STATE_WAIT_SIGN and item_day != day_no:

            @item.callback()
            def OnClick(layer, touch, index=item_day - 1, item_no=item_no):
                x, y = layer.GetPosition()
                w, h = layer.GetContentSize()
                dx = 0 if index < 6 else 0.5 * w
                dy = 1.3 * h if index < 6 else 0.65 * h
                wpos = layer.GetParent().ConvertToWorldSpace(x - dx, y - dy)
                global_data.emgr.show_item_desc_ui_event.emit(item_no, wpos)

        elif status == SIGN_STATE_WAIT_REMEDY:

            @item.unique_callback()
            def OnClick(btn, touch, day_no=item_day):
                self.try_resign_in(day_no)

        else:

            @item.unique_callback()
            def OnClick(btn, touch):
                if global_data.player:
                    global_data.player.daily_sign()

    def try_resign_in(self, day_no):
        if not check_payment(gconst.SHOP_PAYMENT_GOLD, RETRO_SIGN_COST):
            return
        cb = lambda day_no=day_no: global_data.player.remedy_sign(day_no)
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
        SecondConfirmDlg2().confirm(content=get_text_by_id(604009).format(RETRO_SIGN_COST), confirm_callback=cb)