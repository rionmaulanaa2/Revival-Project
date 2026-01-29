# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/mall_buy_confirm_func.py
from __future__ import absolute_import
import logic.client.const.mall_const as m_const
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
NEED_CONFIRM_GOODS_DICT = {m_const.CLAN_CHANGE_NAME_GOODS_ID: 'confirm_change_name'
   }

def confirm_change_name(goods_id, call_back=None):
    from logic.gutils.clan_utils import is_clan_commander
    if not global_data.player or not global_data.player.is_in_clan():
        SecondConfirmDlg2().confirm(content=800118, confirm_callback=call_back)
    elif global_data.player.is_in_clan() and not is_clan_commander():
        SecondConfirmDlg2().confirm(content=800119, confirm_callback=call_back)
    else:
        call_back()


def goods_buy_need_confirm(goods_id, call_back=None):
    if goods_id in NEED_CONFIRM_GOODS_DICT:
        func_name = NEED_CONFIRM_GOODS_DICT[goods_id]
        func = globals()[func_name]
        func(goods_id, call_back)
        return True
    else:
        return False