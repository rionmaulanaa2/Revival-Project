# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/spectate_proto.py


def sepctate_obj(synchronizer, obj_id, is_star=False):
    synchronizer.send_event('E_SPECTATE_OBJ', obj_id)
    if is_star:
        global_data.emgr.battle_show_message_event.emit(get_text_by_id(19170))
    global_data.emgr.recruit_be_rescued.emit(False)


def battle_stars(synchronizer, stars_info):
    global_data.emgr.update_battle_stars_event.emit(stars_info)


def update_cur_observe_ui(synchronizer):
    global_data.emgr.update_cur_observe_ui.emit()


def spectate_battle_finish(synchronizer, battle_type, winner_names, rank=None, detail_info=None):
    global_data.emgr.spectate_battle_finish_event.emit(battle_type, winner_names, rank, detail_info)


def set_has_spectator(synchronizer, has_spectator):
    synchronizer.send_event('E_SET_HAS_SPECTATOR', has_spectator)


def like_ret(synchronizer, like_eid, cnt_like_cnt):
    pass


def be_liked_info(synchronizer, obj_id, has_liked, liked_cnt):
    synchronizer.send_event('E_SPECTATE_LIKE_DATA', has_liked, liked_cnt)
    global_data.emgr.on_update_observer_like_data_event.emit(has_liked, liked_cnt)


def set_spectator_num(synchronizer, name, num):
    synchronizer.send_event('E_SPECTATOR_NUM', num)
    if synchronizer.unit_obj.__class__.__name__ == 'LAvatar':
        global_data.emgr.on_observer_num_changed.emit(num, name)
    if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_spectate_target() == synchronizer.unit_obj.get_owner():
        global_data.emgr.on_target_observer_num_changed.emit(num, name)


def quit_spectate(synchronizer):
    synchronizer.send_event('E_QUIT_SPECTATE_SYNC')


def on_sync_spectate_event(synchronizer, event_name, arg_list, arg_dict):
    is_in_spectate = False
    if global_data.player and global_data.player.logic:
        is_in_spectate = global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate()
    if not is_in_spectate and arg_dict['sync_id'] == synchronizer.unit_obj.id:
        return
    arg_dict['is_sync'] = True
    synchronizer.send_event(event_name, *arg_list, **arg_dict)