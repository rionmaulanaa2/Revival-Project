# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMessage.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gutils.chat_utils import format_history_data

class ComMessage(UnitCom):
    BIND_EVENT = {'E_SHOW_TIP': 'show_tip',
       'E_SHOW_STRING_TIP': 'show_string_tip',
       'E_SHOW_PACK_MSG': 'show_pack_msg',
       'E_SHOW_MESSAGE': 'show_message',
       'E_SHOW_PROGRESS': 'show_progress',
       'E_CLOSE_PROGRESS': 'close_progress',
       'E_SET_DEBUG': 'set_debug',
       'E_DEBUG_MESSAGE': 'show_debug_message',
       'E_ADD_GROUP_HISTORY_MSG': 'add_group_history_msg',
       'G_GROUP_HISTORY_MSG': 'get_group_history_msg'
       }

    def __init__(self):
        super(ComMessage, self).__init__()
        self._debug = False
        self._history_group_msg = []

    def init_from_dict(self, unit_obj, bdict):
        super(ComMessage, self).init_from_dict(unit_obj, bdict)
        self._history_group_msg = bdict.get('group_history_msg', [])

    def on_init_complete(self):
        self.set_group_history_msg()

    def show_tip(self, tid):
        global_data.emgr.battle_show_message_event.emit(get_text_local_content(tid))

    def show_string_tip(self, tip_str):
        global_data.emgr.battle_show_message_event.emit(tip_str)

    def show_pack_msg(self, msg):
        global_data.emgr.battle_show_message_event.emit(unpack_text(msg))

    def show_message(self, fmt, *args, **kwargs):
        global_data.emgr.battle_show_message_event.emit(fmt.format(*args, **kwargs))

    def show_progress(self, time, item_id, msg, callback=None, cancel_callback=None, start_time=0, icon_path=None, **kwargs):
        global_data.emgr.battle_show_progress_event.emit(time, item_id, msg, callback, start_time, cancel_callback, icon_path, **kwargs)

    def close_progress(self, item_id=None):
        global_data.emgr.battle_close_progress_event.emit(item_id)

    def show_main_battle_message(self, msg, itype):
        global_data.emgr.show_battle_main_message.emit(msg, itype)

    def set_debug(self, debug):
        self._debug = debug

    def show_debug_message(self, fmt, *args, **kwargs):
        if self._debug:
            self.show_message(fmt, *args, **kwargs)

    def set_group_history_msg(self):
        self._history_group_msg = [ (eid, name, format_history_data(msg)) for eid, name, msg in self._history_group_msg ]
        self._refresh_history_msg()

    def add_group_history_msg(self, eid, name, msg):
        msg = format_history_data(msg)
        self._history_group_msg.append((eid, name, msg))
        if len(self._history_group_msg) > 20:
            self._history_group_msg.pop(0)
        self._refresh_history_msg()

    def get_group_history_msg(self):
        return self._history_group_msg

    def _refresh_history_msg(self):
        ui = global_data.ui_mgr.get_ui('FightChatUI')
        ui and ui.init_history_msg(self._history_group_msg)