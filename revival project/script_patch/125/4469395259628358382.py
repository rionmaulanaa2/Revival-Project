# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComNotice.py
from __future__ import absolute_import
from ..UnitCom import UnitCom

class ComNotice(UnitCom):
    BIND_EVENT = {'E_MECHA_MODULE_DROP_ON_DIE': 'on_mecha_die_drop'
       }

    def __init__(self):
        super(ComNotice, self).__init__()

    def on_mecha_die_drop(self, item_ids):
        from logic.gcommon.common_utils.local_text import get_text_by_id
        from logic.gutils import item_utils
        MODULE_ITEM_COLOR_SHORTHAND = {9908: '#SR',
           9909: '#SB',9910: '#SY',9911: '#SK'}
        for item_id in item_ids:
            color_str = MODULE_ITEM_COLOR_SHORTHAND.get(item_id, '#SR')
            color_name = color_str + item_utils.get_item_name(item_id) + '#n'
            global_data.emgr.battle_show_message_event.emit(get_text_by_id(17011, {'module_name': color_name}))