# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/red_packet/RedPacketUI.py
from __future__ import absolute_import
import six
import time
import math
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.const.uiconst import UI_VKB_CLOSE
from logic.gutils.red_packet_utils import init_red_packet_cover_item, get_red_packet_info, red_packet_danmu_text_list, TEXT_TYPE_TO_IDX, get_red_packet_danmu_text, get_red_packet_bless_info
from logic.gutils.role_head_utils import init_role_head_auto
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.item_utils import get_money_icon, get_lobby_item_pic_by_item_no
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
from random import randint
from logic.comsys.observe_ui.DanmuLinesUI import DanmuLinesUI
from logic.gcommon.common_const.red_packet_const import RED_PACKET_DANMU_SEND_INTERVAL, RED_PACKET_DAY_RECV_MAX_COUNT, LUCK_SCORE_RED_PACKET, LUCK_RED_PACKET_DAY_RECV_MAX_COUNT
from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_INTIMACY
from logic.gcommon.common_const.chat_const import CHAT_CHANNEL_NAME
from functools import cmp_to_key

class RedPacketUI(BasePanel):
    PANEL_CONFIG_NAME = 'chat/red_packet/open_red_packet'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_btn_close'
       }
    GLOBAL_EVENT = {'claim_red_packet_succeed': 'on_claim_red_packet_succeed',
       'send_red_packet_dammu': 'on_send_red_packet_dammu'
       }
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, pid, packet_info, channel, **kwargs):
        self.regist_main_ui()
        self.channel = channel
        self.pid = pid
        self.packet_info = packet_info
        self.red_packet_sender_info = self.packet_info.get('red_packet_sender_info', {})
        self.red_packet_info = self.red_packet_sender_info.get('red_packet_info', {})
        self.red_packet_status = self.packet_info.get('red_packet_status', {})
        self._last_send_time = -1
        self.danmu_widget = DanmuLinesUI()
        self.danmu_widget.enable_danmu(False)
        self._is_click_opened = False
        self.is_empty = False
        self.init_red_packet_info()

    def init_red_packet_info(self, is_open=False):
        allocate_recv = True
        if global_data.player:
            recv_cnt = global_data.player.get_red_packet_day_recv_count()
            if recv_cnt >= RED_PACKET_DAY_RECV_MAX_COUNT:
                allocate_recv = False
                global_data.game_mgr.show_tip(634360)
            recv_luck_cnt = global_data.player.get_red_packet_day_luck_recv_count()
            if recv_luck_cnt >= LUCK_RED_PACKET_DAY_RECV_MAX_COUNT:
                allocate_recv = False
                global_data.game_mgr.show_tip(634360)
        if self.red_packet_status:
            spilt_count = self.red_packet_info.get('split_count', 1)
            avt_len = len(self.red_packet_status.get('avt_info_dict', {}))
            if spilt_count == avt_len:
                self.is_empty = True
        avt_info_dict = self.red_packet_status.get('avt_info_dict', {})
        if global_data.player and str(global_data.player.uid) in avt_info_dict:
            self.init_claimed_red_packet(is_open)
        elif self.is_empty or not allocate_recv:
            self.init_empty_red_packet(is_open)
        else:
            self.init_open_red_packet()

    def init_open_red_packet(self):
        self.panel.PlayAnimation('show')
        self.panel.nd_step_1.setVisible(True)
        self.panel.nd_step_2.setVisible(False)
        self.panel.nd_step_3.setVisible(False)
        if not self.red_packet_info:
            return
        text_id = self.red_packet_info.get('extra_info', {}).get('text_idx', 1)
        skin_id = self.red_packet_info.get('extra_info', {}).get('skin_id', '80000001')
        init_red_packet_cover_item(self.panel.nd_step_1.temp_item, skin_id, True)
        if not text_id:
            text_id = 1
        self.panel.nd_step_1.temp_item.lab_wish.SetString(get_red_packet_bless_info(text_id).get('text_id', 634364))
        self.panel.nd_step_1.temp_item.btn_choose.BindMethod('OnClick', lambda btn, touch: self.on_click_open_red_packet())
        self.panel.temp_item.PlayAnimation('loop')
        self.panel.temp_item.PlayAnimation('saoguang_loop')

    def init_empty_red_packet(self, is_open=False):
        if not is_open:
            self.panel.nd_step_1.setVisible(False)
        self.panel.nd_step_2.setVisible(True)
        self.panel.nd_step_3.setVisible(False)
        self.panel.nd_thank.setVisible(True)
        self.panel.temp_btn.btn_common.SetText(634388)
        self.panel.temp_item.btn_choose.SetEnable(False)
        self.text_type = 'complaint_text'
        self.init_send_text(self.text_type)
        self.init_common_claimed_red_packet(self.panel.nd_step_2, False)

    def init_claimed_red_packet(self, is_open=False):
        if not is_open:
            self.panel.nd_step_1.setVisible(False)
        self.panel.nd_step_2.setVisible(False)
        self.panel.nd_step_3.setVisible(True)
        self.panel.nd_thank.setVisible(True)
        self.text_type = 'thanks_text'
        self.panel.temp_btn.btn_common.SetText(634389)
        self.panel.temp_item.btn_choose.SetEnable(False)
        if self.red_packet_info:
            text_id = self.red_packet_info.get('extra_info', {}).get('text_idx', 1)
            self.panel.nd_step_3.bar_bg.lab_wish.SetString(get_red_packet_bless_info(text_id).get('text_id', 634364))
        self.init_send_text(self.text_type)
        self.init_common_claimed_red_packet(self.panel.nd_step_3, True)

    def init_common_claimed_red_packet(self, nd, show_cur_id_item=False):
        avt_info_dict = self.red_packet_status.get('avt_info_dict', {})
        red_packet_conf = get_red_packet_info(self.red_packet_info.get('coin_type', 3))
        random_item_list = red_packet_conf.get('random_item_list')

        def _sort_func(player_id):
            player_info = avt_info_dict[player_id]
            item_no = player_info.get('claim_item_no', 50101002)
            item_num = player_info.get('claim_item_num', 0)
            item_info = [item_no, item_num]
            index = random_item_list.index(item_info)
            return index

        avt_uid_list = list(set(self.red_packet_status.get('avt_uid_list', [])[:]))
        if random_item_list:
            avt_uid_list.sort(key=_sort_func)
        split_count = self.red_packet_info.get('split_count', 1)
        coin_num = self.red_packet_info.get('coin_num', 100)
        nd.bar_bg.lab_name.SetString(self.red_packet_sender_info.get('char_name', ''))
        init_role_head_auto(nd.bar_bg.temp_head, self.red_packet_sender_info.get('uid', ''), 0, self.red_packet_sender_info)
        nd.bar_bg.temp_head.BindMethod('OnClick', lambda btn, touch, uid=self.red_packet_sender_info.get('uid', ''): self.on_click_player_simple_inf(uid, ''))
        nd.bar_bg.lab_tips_got.SetString('<color=FFB94CFF>{}</color>/<color=FFE3E3FF>{}</color>'.format(len(avt_info_dict), split_count) + get_text_by_id(80866))
        if split_count - len(avt_info_dict) == 0:
            nd.bar_bg.lab_tips_remain.SetString(get_text_by_id(610321) + '<color=FFB94CFF><size=22>{}</size></color>/<color=FFE3E3FF>{}</color>'.format(str(split_count - len(avt_info_dict)), split_count))
        else:
            nd.bar_bg.lab_tips_remain.SetString(get_text_by_id(610321) + '<color=FFB94CFF>{}</color>/<color=FFE3E3FF>{}</color>'.format(str(split_count - len(avt_info_dict)), split_count))
        nd.bar_bg.list_info.SetInitCount(len(avt_info_dict))
        idx = 0
        for uid in avt_uid_list:
            uid = str(uid)
            if uid not in avt_info_dict:
                continue
            player_info = avt_info_dict[uid]
            item = nd.bar_bg.list_info.GetItem(idx)
            item_no = player_info.get('claim_item_no', 50101002)
            item_num = player_info.get('claim_item_num', 0)
            if global_data.player and str(global_data.player.uid) == uid:
                init_tempate_mall_i_item(nd.bar_bg.temp_item, item_no, item_num)
                item.lab_name.SetColor(16768600)
            else:
                item.lab_name.SetColor(4916485)
            item.lab_name.SetString(player_info.get('char_name'))
            item.item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(item_no))
            item.lab_num.SetString('x' + str(item_num))
            item.BindMethod('OnClick', lambda btn, touch, uid=uid: self.on_click_player_simple_inf(uid, ''))
            idx += 1

        self.danmu_widget.enable_danmu(True)

    def init_send_text(self, text_type):
        self.danmu_list = red_packet_danmu_text_list(text_type)
        self.select_danmu_idx = randint(0, len(self.danmu_list) - 1)
        self.select_danmu = self.danmu_list[self.select_danmu_idx]
        self.panel.nd_thank.lab_wish.SetString(self.select_danmu)
        self.panel.btn_random.BindMethod('OnClick', lambda btn, touch: self.on_click_random_danmu_text())
        self.panel.temp_btn.btn_common.BindMethod('OnClick', lambda btn, touch: self.on_click_send_danmu_text())

    def on_click_random_danmu_text(self):
        if len(self.danmu_list) <= 1:
            return
        while True:
            self.select_danmu_idx = randint(0, len(self.danmu_list) - 1)
            if self.select_danmu != self.danmu_list[self.select_danmu_idx]:
                self.select_danmu = self.danmu_list[self.select_danmu_idx]
                self.panel.nd_thank.lab_wish.SetString(self.select_danmu)
                return

    def on_click_send_danmu_text(self):
        cur_time = time.time()
        if cur_time - self._last_send_time < RED_PACKET_DANMU_SEND_INTERVAL:
            global_data.game_mgr.show_tip(get_text_by_id(11008, {'time': str(int(math.ceil(RED_PACKET_DANMU_SEND_INTERVAL - (cur_time - self._last_send_time))))}))
            return
        self._last_send_time = cur_time
        if not global_data.player:
            return
        global_data.game_mgr.show_tip(get_text_by_id(609010))
        global_data.player.send_red_packet_chat(self.channel, self.pid, self.select_danmu_idx, TEXT_TYPE_TO_IDX.get(self.text_type, 1))

    def on_claim_red_packet_succeed(self, flag, pid, count, item_no, packet_info):
        if pid != self.red_packet_info.get('pid', None):
            return
        else:
            self.panel.temp_item.StopAnimation('loop')
            self.panel.temp_item.StopAnimation('saoguang_loop')
            self.panel.temp_item.PlayAnimation('out')
            self.red_packet_status = packet_info
            self.panel.img_shadow.setVisible(False)
            self.init_red_packet_info(True)
            return

    def on_click_open_red_packet(self):
        if not global_data.player:
            return
        if self._is_click_opened:
            return
        self._is_click_opened = True
        global_data.player.claim_red_packet(self.channel, self.red_packet_info.get('pid'), self.red_packet_info.get('stub_id'))

    def on_send_red_packet_dammu(self, player_name, danmu_info):
        pid = danmu_info.get('pid', 0)
        if pid != self.pid:
            return
        text_idx = danmu_info.get('text_idx', 0)
        text_type = danmu_info.get('text_type', 1)
        text = get_red_packet_danmu_text(text_idx, text_type)
        global_data.emgr.on_recv_danmu_msg.emit(player_name + ':' + text)

    def on_click_btn_close(self, *args):
        self.close()

    def on_click_player_simple_inf(self, uid, report_msg):
        ui = global_data.ui_mgr.get_ui('OpenBoxUI')
        if ui:
            return
        if not global_data.player:
            return
        uid = int(uid)
        if uid == global_data.player.uid:
            return
        ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
        ui.set_extra_btns([BTN_TYPE_INTIMACY])
        ui.refresh_by_uid(uid)
        channel_name = CHAT_CHANNEL_NAME.get(self.channel, 'unknown')
        ui.set_chat_source(uid, channel_name, report_msg)

    def on_finalize_panel(self):
        if not self.is_empty and global_data.player:
            global_data.player.search_red_packet_info([self.pid])
        self.unregist_main_ui()
        if self.danmu_widget:
            self.danmu_widget.close()