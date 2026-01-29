# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/client/udata_gift.py
from __future__ import absolute_import
from logic.gcommon.common_const import shop_const
import logic.gcommon.time_utility as tutil
from common.cfg import confmgr

class LotteryTenTry(object):
    lobby_tips = 1
    lottery_tips = 2

    def __init__(self, bdict):
        self.update_from_dict(bdict)

    def update_from_dict(self, bdict):
        self.lottery_id = bdict.get('lottery_id', 0)
        self.state = bdict.get('state', shop_const.UDATA_LOTTERY_10_TRY_STATE_CHANCE)
        self.items = bdict.get('items', None)
        self.tip_state = bdict.get('tip_state', 0)
        self.finish_time = bdict.get('finish_time', 0)
        self.archive_key = 'Lottery_10_Try_' + str(self.finish_time)
        return

    def wait_determine(self, lottery_id):
        if self.lottery_id != lottery_id:
            return False
        if not self.get_left_time():
            return False
        return self.state == shop_const.UDATA_LOTTERY_10_TRY_STATE_CHANCE

    def wait_pay(self, lottery_id):
        if self.lottery_id != lottery_id:
            return False
        if not self.get_left_time():
            return False
        return self.state == shop_const.UDATA_LOTTERY_10_TRY_STATE_DEFINITE_ITEM

    def preview_reward(self, open_box=True):
        if self.state != shop_const.UDATA_LOTTERY_10_TRY_STATE_DEFINITE_ITEM:
            return
        else:
            lottery_ui = global_data.ui_mgr.get_ui('LotteryMainUI')
            if not lottery_ui or not lottery_ui.cur_lottery_id:
                return
            from logic.gutils.item_utils import get_item_chip_data
            own_cache = set()
            final_item_list = []
            ori_item_list = []
            for item_no, item_num in self.items:
                chip_data = get_item_chip_data(item_no)
                if 'chip_id' not in chip_data:
                    final_item_list.append((item_no, item_num))
                    ori_item_list.append(None)
                    continue
                if global_data.player.has_item_by_no(item_no) or item_no in own_cache:
                    final_item_list.append((chip_data['chip_id'], chip_data['chip_rate']))
                    ori_item_list.append((item_no, item_num))
                else:
                    final_item_list.append((item_no, item_num))
                    ori_item_list.append(None)
                own_cache.add(item_no)

            conf = confmgr.get('lobby_item_rare_degree_count').get_conf()
            for index, (item_id, count) in enumerate(final_item_list):
                if str(item_id) in conf and ori_item_list[index] and ori_item_list[index][0] in conf[str(item_id)]['ignore_smash_item_list']:
                    ori_item_list[index] = None

            if open_box:
                from logic.client.const.mall_const import CONTINUAL_LOTTERY_COUNT
                global_data.emgr.set_cur_lucky_draw_info.emit(lottery_ui.cur_lottery_id, CONTINUAL_LOTTERY_COUNT)
                global_data.emgr.receive_lottery_result.emit(final_item_list, ori_item_list, {}, is_10_try=True)
            else:
                ui = global_data.ui_mgr.show_ui('LotteryTenTryResult', 'logic.comsys.lottery')
                ui.set_reward_result(self.lottery_id, final_item_list, ori_item_list)
            return

    def get_left_time(self):
        return max(0, self.finish_time - tutil.get_server_time())

    def show_result_tips(self, nd):
        tips_state = global_data.achi_mgr.get_cur_user_archive_data(self.archive_key, 0)
        if tips_state & self.lottery_tips:
            nd.DestroyChild('tips')
        else:
            tips_nd = global_data.uisystem.load_template_create('common/i_common_tips_riko_right', parent=nd, name='tips')
            tips_nd.PlayAnimation('activity_tips')

            @tips_nd.nd_touch_bg.callback()
            def OnClick(*args):
                nd.DestroyChild('tips')

            tips_state |= self.lottery_tips
            global_data.achi_mgr.set_cur_user_archive_data(self.archive_key, tips_state)

    def show_lobby_tips(self):
        if self.state != shop_const.UDATA_LOTTERY_10_TRY_STATE_CHANCE:
            return False
        tips_state = global_data.achi_mgr.get_cur_user_archive_data(self.archive_key, 0)
        if tips_state & self.lobby_tips:
            return False
        tips_state |= self.lobby_tips
        global_data.achi_mgr.set_cur_user_archive_data(self.archive_key, tips_state)
        return True

    def get_determine_lottery_id(self):
        if self.state != shop_const.UDATA_LOTTERY_10_TRY_STATE_CHANCE:
            return 0
        if not self.get_left_time():
            return 0
        return self.lottery_id