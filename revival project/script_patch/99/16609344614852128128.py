# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHunterCoin.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.cdata import meow_capacity_config
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.battle_const import MAIN_NODE_COMMON_INFO, MAGIC_USE_MAGIC, MAGIC_GET_ITEM
from common.cfg import confmgr
ITEM_GET_MSG = {9952: {'i_type': MAGIC_GET_ITEM,
          'content_txt': get_text_by_id(17898, (int(confmgr.get('c_buff_data', '565', 'Duration', default=50)),)),
          'lab_title': 17528,
          'lab_title2': 17557,
          'icon_path': 'gui/ui_res_2/battle_hunter/icon_battle_hunter_tips_wind.png',
          'bar_path': 'gui/ui_res_2/battle_hunter/img_battle_hunter_tips_stage_purple.png'
          },
   9953: {'i_type': MAGIC_GET_ITEM,
          'content_txt': get_text_by_id(17899, (int(confmgr.get('c_buff_data', '567', 'Duration', default=50)),)),
          'lab_title': 17529,
          'lab_title2': 17558,
          'icon_path': 'gui/ui_res_2/battle_hunter/icon_battle_hunter_tips_violent.png',
          'bar_path': 'gui/ui_res_2/battle_hunter/img_battle_hunter_tips_stage_purple.png'
          },
   9954: {'i_type': MAGIC_GET_ITEM,
          'content_txt': get_text_by_id(17900, (int(confmgr.get('c_buff_data', '572', 'Duration', default=50)),)),
          'lab_title': 17531,
          'lab_title2': 17559,
          'icon_path': 'gui/ui_res_2/battle_hunter/icon_battle_hunter_tips_potion_2.png',
          'bar_path': 'gui/ui_res_2/battle_hunter/img_battle_hunter_tips_stage_green.png'
          },
   9955: {'i_type': MAGIC_GET_ITEM,
          'content_txt': get_text_by_id(17901, (int(confmgr.get('c_buff_data', '571', 'Duration', default=50)),)),
          'lab_title': 17530,
          'lab_title2': 17559,
          'icon_path': 'gui/ui_res_2/battle_hunter/icon_battle_hunter_tips_potion_1.png',
          'bar_path': 'gui/ui_res_2/battle_hunter/img_battle_hunter_tips_stage_purple.png'
          }
   }
ITEM_USE_MSG = {9952: {'i_type': MAGIC_USE_MAGIC,
          'content_txt': 17535,
          'icon_path': 'gui/ui_res_2/battle_hunter/icon_battle_hunter_tips_wind.png',
          'icon_module_path': 'gui/ui_res_2/battle_hunter/img_battle_hunter_tips_lock_line_purple_1.png',
          'bar_module_path': 'gui/ui_res_2/battle_hunter/img_battle_hunter_tips_use_purple.png'
          },
   9953: {'i_type': MAGIC_USE_MAGIC,
          'content_txt': 17536,
          'icon_path': 'gui/ui_res_2/battle_hunter/icon_battle_hunter_tips_violent.png',
          'icon_module_path': 'gui/ui_res_2/battle_hunter/img_battle_hunter_tips_lock_line_purple_1.png',
          'bar_module_path': 'gui/ui_res_2/battle_hunter/img_battle_hunter_tips_use_purple.png'
          },
   9954: {'i_type': MAGIC_USE_MAGIC,
          'content_txt': 17537,
          'icon_path': 'gui/ui_res_2/battle_hunter/icon_battle_hunter_tips_potion_2.png',
          'icon_module_path': 'gui/ui_res_2/battle_hunter/img_battle_hunter_tips_lock_line_green_1.png',
          'bar_module_path': 'gui/ui_res_2/battle_hunter/img_battle_hunter_tips_use_green.png'
          },
   9955: {'i_type': MAGIC_USE_MAGIC,
          'content_txt': 17538,
          'icon_path': 'gui/ui_res_2/battle_hunter/icon_battle_hunter_tips_potion_1.png',
          'icon_module_path': 'gui/ui_res_2/battle_hunter/img_battle_hunter_tips_lock_line_purple_1.png',
          'bar_module_path': 'gui/ui_res_2/battle_hunter/img_battle_hunter_tips_use_purple.png'
          }
   }
BUFF_TO_ITEM = {565: 9952,
   567: 9953,
   572: 9954,
   571: 9955
   }

class ComHunterCoin(UnitCom):
    BIND_EVENT = {'E_UPDATE_MAGIC_COIN_CNT': '_on_update_coin',
       'G_MAGIC_COIN_CNT': 'get_coin_cnt',
       'E_PICK_UP_OTHERS': 'on_pick_up_item',
       'E_ITEMUSE_TRY_RET': 'on_item_use_ret',
       'E_BUFF_DEL_DATA': 'on_del_buff',
       'E_UPDATE_MAGIC_EXCHANGE_TIMES': 'set_exchanged_times',
       'G_MAGIC_EXCHANGE_TIMES': 'get_exchanged_times'
       }

    def __init__(self):
        super(ComHunterCoin, self).__init__(need_update=False)
        self.coin_cnt = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComHunterCoin, self).init_from_dict(unit_obj, bdict)
        self.coin_cnt = bdict.get('cur_magic_coin_cnt', 0)
        self.per_magic_item_cost = bdict.get('per_magic_item_cost', 5)
        self.exchanged_times = bdict.get('exchanged_times', 0)

    def get_coin_cnt(self):
        return (
         self.coin_cnt, self.per_magic_item_cost)

    def get_exchanged_times(self):
        return self.exchanged_times

    def _on_update_coin(self, coin_cnt):
        self.coin_cnt = coin_cnt
        global_data.emgr.update_hunter_coin_count.emit(coin_cnt)

    def on_pick_up_item(self, item_data):
        if not self.ev_g_is_avatar():
            return
        else:
            item_id = item_data.get('item_id', None)
            if item_id in ITEM_GET_MSG:
                global_data.emgr.show_battle_main_message.emit(ITEM_GET_MSG[item_id], MAIN_NODE_COMMON_INFO)
            return

    def on_item_use_ret(self, item_id, ret):
        if not self.ev_g_is_avatar():
            return
        if item_id not in ITEM_USE_MSG:
            return
        if ret:
            global_data.emgr.show_battle_main_message.emit(ITEM_GET_MSG[item_id], MAIN_NODE_COMMON_INFO)
        else:
            global_data.player.logic.send_event('E_SHOW_MESSAGE', get_text_by_id(19055))

    def set_exchanged_times(self, times):
        self.exchanged_times = times
        global_data.emgr.on_magic_exchange_times_change.emit(times)

    def on_del_buff(self, buff_key, buff_id, buff_idx):
        if not self.ev_g_is_avatar():
            return
        if buff_id in BUFF_TO_ITEM:
            item_id = BUFF_TO_ITEM[buff_id]
            global_data.emgr.show_battle_main_message.emit(ITEM_USE_MSG[item_id], MAIN_NODE_COMMON_INFO)