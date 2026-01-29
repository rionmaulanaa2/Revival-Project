# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/red_packet_utils.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from logic.gutils.item_utils import get_lobby_item_name
from logic.gcommon.common_const.red_packet_const import CHOOSE_RED_PACKET_COVER, NORMAL_COVER_ITEM_NO
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO, FLASH_EXCHANGE
from logic.gcommon.common_const.red_packet_const import LUCK_SCORE_RED_PACKET, PRIV_RED_PACKET
from logic.gcommon.common_utils.local_text import get_text_by_id
CUR_ID_TO_PAYMENT_ID = {50101109: FLASH_EXCHANGE,
   50101001: SHOP_PAYMENT_YUANBAO
   }
TEXT_TYPE_TO_IDX = {'thanks_text': 1,
   'complaint_text': 2
   }
IDX_TO_TEXT_TYPE = {1: 'thanks_text',
   2: 'complaint_text'
   }

def get_red_packet_danmu_text(idx, text_type):
    text_type = IDX_TO_TEXT_TYPE.get(text_type, 'thanks_text')
    text_list = red_packet_danmu_text_list(text_type)
    if not text_list or len(text_list) < idx:
        return ''
    return get_text_by_id(text_list[idx])


def get_red_packet_cover_info(item_id):
    return confmgr.get('red_packet_conf', 'RedPacketCover', 'Content', str(item_id), default={})


def get_open_packet_cover_list():
    cover_dict = confmgr.get('red_packet_conf', 'RedPacketCover', 'Content', default={})
    cover_list = []
    for packet_item, packet_info in six.iteritems(cover_dict):
        if packet_info.get('cNotShow') == 1:
            continue
        cover_list.append(packet_item)

    return cover_list


def get_all_red_packet_info():
    return confmgr.get('red_packet_conf', 'RedPacketConfig', 'Content', default={})


def get_all_display_red_packet_info():
    display_red_packet_info = {}
    red_packet_info = get_all_red_packet_info()
    for red_packet_type, red_packet_info in six.iteritems(red_packet_info):
        if red_packet_info.get('is_display') == 1:
            display_red_packet_info[red_packet_type] = red_packet_info

    return display_red_packet_info


def get_red_packet_info(red_packet_type):
    return confmgr.get('red_packet_conf', 'RedPacketConfig', 'Content', str(red_packet_type), default={})


def get_red_packet_bless_list():
    bless_dicts = confmgr.get('red_packet_conf', 'RedPacketBlessText', 'Content')
    list = []
    for _, info in six.iteritems(bless_dicts):
        if info.get('is_hide', False):
            continue
        list.append(info.get('text_id'))

    return list


def get_red_packet_bless_info(id):
    return confmgr.get('red_packet_conf', 'RedPacketBlessText', 'Content', str(id), default={})


def init_red_packet_cover_item(packet_item, item_id, show_text=False):
    packet_cover_info = get_red_packet_cover_info(item_id)
    if not packet_cover_info:
        return
    packet_item.bar_down.SetDisplayFrameByPath('', packet_cover_info.get('cBg', 'gui/ui_res_2/chat/red_packet/bar_red_packet_big_mid.png'))
    top = packet_cover_info.get('cBgTop', '')
    if top:
        packet_item.bar_top.setVisible(True)
        packet_item.bar_top.SetDisplayFrameByPath('', top)
    else:
        packet_item.bar_top.setVisible(False)
    icon = packet_cover_info.get('cIcon', '')
    if icon:
        packet_item.img.setVisible(True)
        packet_item.img.SetDisplayFrameByPath('', icon)
    else:
        packet_item.img.setVisible(False)
    if show_text:
        packet_item.lab_wish.setVisible(True)
    else:
        packet_item.lab_wish.setVisible(False)
    packet_item.lab_wish.SetColor(int(packet_cover_info.get('cChatMsgColor', ['0xFFFFFFFF', '0xFFFFFFFF'])[0], 16))


def init_small_red_packet_cover_item(packet_small_item, item_id):
    packet_cover_info = get_red_packet_cover_info(item_id)
    if not packet_cover_info:
        return
    bar = packet_cover_info.get('cBar', 'gui/ui_res_2/chat/red_packet/bar_red_packet_big_top1.png')
    icon = packet_cover_info.get('cIcon', '')
    packet_small_item.bar_bg.SetDisplayFrameByPath('', bar)
    if icon:
        packet_small_item.img.setVisible(True)
        packet_small_item.img.SetDisplayFrameByPath('', icon)
    else:
        packet_small_item.img.setVisible(False)
    packet_small_item.lab_name.SetString(get_lobby_item_name(item_id))


def get_user_setting_red_packet_cover():
    if not global_data.player:
        return str(NORMAL_COVER_ITEM_NO)
    return global_data.achi_mgr.get_cur_user_archive_data(CHOOSE_RED_PACKET_COVER, str(NORMAL_COVER_ITEM_NO))


def set_user_setting_red_packet_cover(item_no):
    global_data.game_mgr.show_tip(81295)
    global_data.achi_mgr.set_cur_user_archive_data(CHOOSE_RED_PACKET_COVER, item_no)
    global_data.emgr.change_red_packet_cover_succeed.emit(item_no)


def init_chat_red_packet(item, red_packet_info, is_other, click_cb=None):
    if not red_packet_info:
        return
    coin_type = red_packet_info.get('coin_type', 2)
    coin_info = get_red_packet_info(coin_type)
    if coin_info:
        cur_id = coin_info.get('cur_id', '50101001')
        if coin_type == PRIV_RED_PACKET:
            icon_path = 'gui/ui_res_2/charge/charge_reward/icon_recharge_reward_chat.png'
            item.temp_red_packet.item.setScale(0.3)
        elif coin_type == LUCK_SCORE_RED_PACKET:
            icon_path = 'gui/ui_res_2/lottery/luck/icon_lottery_luck_item.png'
            item.temp_red_packet.item.setScale(0.3)
        else:
            icon_path = 'gui/ui_res_2/item/groceries/%s.png' % cur_id
            item.temp_red_packet.item.setScale(0.24)
        item.temp_red_packet.item.SetDisplayFrameByPath('', icon_path)
        item.temp_red_packet.lab_name.SetString(81708)
    skin_id = red_packet_info.get('extra_info', {}).get('skin_id', '8000001')
    skin_info = get_red_packet_cover_info(skin_id)
    if skin_info:
        if is_other:
            item.temp_red_packet.bar.SetDisplayFrameByPath('', skin_info.get('cChatBgOther', ''))
        else:
            item.temp_red_packet.bar.SetDisplayFrameByPath('', skin_info.get('cChatBg', ''))
        item.temp_red_packet.lab_wish.SetColor(int(skin_info.get('cChatMsgColor', ['0xFFFFFFFF', '0xFFFFFFFF'])[1], 16))
        icon = skin_info.get('cIcon', '')
        if icon:
            item.temp_red_packet.img.setVisible(True)
            item.temp_red_packet.img.SetDisplayFrameByPath('', icon)
        else:
            item.temp_red_packet.img.setVisible(False)
    if coin_type == LUCK_SCORE_RED_PACKET:
        luck_score = red_packet_info.get('extra_info', {}).get('luck_score')
        item.temp_red_packet.lab_wish.SetString(get_text_by_id(634719).format(luck_score))
    else:
        text_id = red_packet_info.get('extra_info', {}).get('text_idx', 1)
        if not text_id:
            text_id = 1
        text_id = get_red_packet_bless_info(text_id).get('text_id', 634364)
        item.temp_red_packet.lab_wish.SetString(text_id)

    @item.temp_red_packet.nd_touch.unique_callback()
    def OnClick(btn, touch):
        if click_cb:
            click_cb()


def red_packet_danmu_text_list--- This code section failed: ---

 184       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'red_packet_conf'
           9  LOAD_CONST            2  'RedPacketDanmu'
          12  LOAD_CONST            3  'Content'
          15  LOAD_CONST            4  'default'
          18  BUILD_MAP_0           0 
          21  CALL_FUNCTION_260   260 
          24  LOAD_ATTR             1  'get'
          27  LOAD_CONST            5  'text_list'
          30  BUILD_LIST_0          0 
          33  CALL_FUNCTION_2       2 
          36  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_260' instruction at offset 21