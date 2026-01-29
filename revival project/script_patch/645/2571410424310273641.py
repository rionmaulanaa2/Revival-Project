# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/gulag_proto.py
from __future__ import absolute_import

def self_enter_gulag_revive_game(synchronizer, game_id, game_detail, scene_detail):
    synchronizer.send_event('E_ENTER_GULAG_GAME', game_id, game_detail, scene_detail)


def other_enter_gulag_revive_game(synchronizer, other_eid, game_id):
    synchronizer.send_event('E_OTHER_ENTER_GULAG_GAME', other_eid, game_id)


def gulag_revive_game_in_queue(synchronizer, in_queue_detail):
    synchronizer.send_event('E_GULAG_GAME_IN_QUEUE', in_queue_detail)


def gulag_revive_game_settle(synchronizer, notify_detail):
    synchronizer.send_event('E_GULAG_GAME_SETTLE', notify_detail)


def refresh_gulag_poison_circle(synchronizer, game_id, show_info):
    global_data.emgr.refresh_gulag_poison_circle.emit(game_id, show_info)


def reduce_gulag_poison_circle(synchronizer, game_id, show_info):
    global_data.emgr.reduce_gulag_poison_circle.emit(game_id, show_info)


def enter_gulag_revive_pending(synchronizer, delay_revive_timestamp):
    synchronizer.send_event('E_GULAG_REVIVE_PENDING', delay_revive_timestamp)


def gulag_groupmate_revive(synchronizer, eid, name):
    synchronizer.send_event('E_GULAG_GROUPMATE_REVIVE', eid, name)


def on_gulag_signal_rate_change(synchronizer, in_gulag_poison, gulag_signal_reduce_rate):
    pass


def self_enter_gulag_scene(synchronizer, scene_no, scene_detail):
    pass


def gulag_force_cancel_sync(synchronizer, is_gulag_canceled):
    global_data.emgr.on_gulag_force_cancel.emit(is_gulag_canceled)
    if is_gulag_canceled:
        small_map = global_data.ui_mgr.get_ui('SmallMapUI')
        if small_map:
            small_map.on_update_can_revive(False, is_canceled=is_gulag_canceled)
        global_data.battle and global_data.battle.update_gulag_cancel_state(True)


def transfer_revive_coin(synchronizer):
    synchronizer.send_event('E_TRANSFER_REVIVE_COIN')