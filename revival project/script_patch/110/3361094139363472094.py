# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/redpoint_check_func.py
from __future__ import absolute_import
import six

def check_lobby_red_point(*args, **kwarg):
    if global_data.is_pc_mode:
        return True
    if global_data.player:
        from logic.gcommon import time_utility as tutil
        create_time = global_data.player.get_create_time() or 0
        if tutil.time() - create_time > tutil.ONE_DAY_SECONDS:
            return True
        if global_data.player.get_total_cnt() > 0:
            return True
        if global_data.player.get_death_total_cnt() > 0:
            return True
    return False


def check_func_friend_msg(*args, **kwarg):
    message_data = global_data.message_data
    if message_data:
        return message_data.is_unread_friend_msg()
    return False


def check_func_add_friend(*args, **kwarg):
    message_data = global_data.message_data
    if message_data:
        return message_data.get_apply_friends()
    return False


def check_func_recruit(*args, **kwarg):
    if global_data.is_pc_mode:
        return False
    achi_mgr = global_data.achi_mgr
    if achi_mgr:
        return achi_mgr.get_cur_user_archive_data('recruit_red_point')
    return False


def check_func_intimacy_tab(*args, **kwargs):
    has_intimacy_historical_event_rp = check_func_intimacy_historical_event_tab()
    if has_intimacy_historical_event_rp:
        return True
    from logic.gcommon.const import INTIMACY_MSG_TYPE_OPERATION_FAIL, INTIMACY_MSG_TYPE_BUILD_AGREE, INTIMACY_MSG_TYPE_LEVEL_UP
    achi_mgr = global_data.achi_mgr
    if achi_mgr and achi_mgr.get_cur_user_archive_data('intimacy_tab_red_point'):
        pop_msg_type = (
         INTIMACY_MSG_TYPE_OPERATION_FAIL, INTIMACY_MSG_TYPE_BUILD_AGREE, INTIMACY_MSG_TYPE_LEVEL_UP)
        pop_msg_count = 0
        intimacy_msg_data = global_data.player.intimacy_msg_data
        for msg_type in pop_msg_type:
            pop_msg_count += len(intimacy_msg_data.get(msg_type, {}))

        return pop_msg_count or check_func_intimacy_build(*args, **kwargs) or check_func_intimacy_delete(*args, **kwargs)
    return True


def check_func_intimacy_historical_event_tab(*args, **kwargs):
    from logic.gcommon.const import INTIMACY_HISTORICAL_EVENT_KEY, IDX_INTIMACY_TYPE, IDX_INTIMACY_LV
    from logic.comsys.intimacy.IntimacyHistoricalEventUI import get_data_list
    from logic.gcommon.cdata.intimacy_data import UNLOCK_MEMORY_LV
    if not global_data.player:
        return False
    else:
        message_data = global_data.message_data
        if not message_data:
            return False
        friend_list = message_data.get_friends()
        if friend_list is None:
            return False
        intimacy_data = global_data.player.intimacy_data
        zombie_intimacy_uid_list = []
        for uid in intimacy_data.keys():
            friend_info = friend_list.get(int(uid))
            if not friend_info:
                continue
            intimacy_type = intimacy_data[uid][IDX_INTIMACY_TYPE]
            if intimacy_type is None:
                continue
            data = message_data.get_or_request_intimacy_event_data(global_data.player.uid, uid)
            if data:
                archive_data = global_data.achi_mgr.get_general_archive_data()
                cache_data = archive_data.get_field(INTIMACY_HISTORICAL_EVENT_KEY.format(str(uid)), {})
                data_list = get_data_list(data)
                if cache_data != data_list:
                    return True
            elif data is not None:
                intimacy_level = intimacy_data[uid][IDX_INTIMACY_LV]
                if intimacy_level >= UNLOCK_MEMORY_LV:
                    return True
            elif uid not in zombie_intimacy_uid_list:
                zombie_intimacy_uid_list.append(int(uid))

        if zombie_intimacy_uid_list:
            global_data.player.call_server_method('del_zombie_intimacy', (zombie_intimacy_uid_list,))
        return False


def check_func_apply_friend(*args, **kwarg):
    message_data = global_data.message_data
    if message_data:
        return message_data.get_apply_friends()
    return False


def check_func_intimacy_build(*args, **kwarg):
    from logic.gcommon.const import INTIMACY_MSG_TYPE_BUILD_RECV, INTIMACY_MSG_TYPE_DELETE_RECV
    msg_data = global_data.player.intimacy_msg_data
    build_recv = msg_data.get(INTIMACY_MSG_TYPE_BUILD_RECV, None)
    delete_recv = msg_data.get(INTIMACY_MSG_TYPE_DELETE_RECV, None)
    return build_recv or delete_recv


def check_func_intimacy_delete(*args, **kwarg):
    from logic.gcommon.const import INTIMACY_MSG_TYPE_DELETE_RECV
    return global_data.player.intimacy_msg_data.get(INTIMACY_MSG_TYPE_DELETE_RECV, {})


def check_func_sys_mail(*args, **kwarg):
    message_data = global_data.message_data
    if not message_data:
        return False
    else:
        email_tag = kwarg.get('tag', None)
        unread_count, _ = message_data.get_email_count_inf(tag=email_tag)
        return bool(unread_count) or message_data.is_unget_reward_email(tag=email_tag)


def check_func_sys_tech(*args, **kwarg):
    if not global_data.player:
        return False
    if not global_data.player.has_open_inscription():
        return
    from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
    mecha_open_info = global_data.player.read_mecha_open_info()
    if mecha_open_info['opened_order']:
        for mecha_id in mecha_open_info['opened_order']:
            if global_data.player.has_item_by_no(battle_id_to_mecha_lobby_id(mecha_id)):
                if check_mecha_component_page_has_empty_slot(mecha_id):
                    return True

    return False


def has_mecha_can_install_tech(*args, **kwarg):
    from logic.gutils.mecha_utils import get_own_mecha_lst
    own_mecha_lst = get_own_mecha_lst()
    for mecha_id in own_mecha_lst:
        if check_mecha_component_page_has_empty_slot(mecha_id):
            return True

    return False


def check_mecha_component_page_has_empty_slot(mecha_type):
    if not global_data.player.has_open_inscription():
        return False
    from logic.gutils.mecha_utils import get_own_mecha_lst
    own_mecha_lst = get_own_mecha_lst()
    if mecha_type not in own_mecha_lst:
        return False
    from logic.gutils import inscription_utils
    page_index = global_data.player.get_mecha_cur_page_index(mecha_type)
    empty_slot_dict = inscription_utils.get_empty_slot_list(mecha_type, page_index)
    for p, slot_list in six.iteritems(empty_slot_dict):
        if slot_list:
            return True

    return False


def check_inscription_store_red_point(*args, **kwarg):
    if not global_data.player:
        return False
    if not global_data.player.has_open_inscription():
        return False
    import time
    achi_mgr = global_data.achi_mgr
    if achi_mgr:
        last_time = achi_mgr.get_cur_user_archive_data('inscription_store_open_time')
        from logic.gcommon import time_utility as tutil
        from logic.gutils import inscription_utils
        from logic.gutils import mall_utils
        if not tutil.is_same_day(last_time, time.time()):
            from logic.gcommon import const
            from logic.gcommon.cdata.mecha_component_data import get_com_unlock_lv
            if global_data.player.has_item_by_no(const.REFORM_GEAR):
                lv = global_data.player.get_lv()
                from logic.gcommon.cdata.mecha_component_data import get_component_all_list
                all_list = get_component_all_list()
                items = global_data.player.get_mecha_component_list()
                unown_list, own_list = inscription_utils.get_merged_item_no_all_list(items, all_list)
                for component_no in unown_list:
                    unlock_lv = get_com_unlock_lv(component_no)
                    if unlock_lv and unlock_lv > lv:
                        continue
                    price_info = inscription_utils.get_component_buy_price(component_no)
                    if mall_utils.check_payment(price_info['goods_payment'], price_info['real_price'], pay_tip=False):
                        return True

        else:
            return False


def check_inscription_all_mecha_module_red_point(*args, **kwarg):
    mecha_open_info = global_data.player.read_mecha_open_info()
    for mecha_id in mecha_open_info['opened_order']:
        has_module_red_p = check_inscription_module_red_point(mecha_id)
        if has_module_red_p:
            return True

    return False


def check_inscription_module_red_point(mecha_id):
    from logic.gcommon.item.lobby_item_type import L_ITEM_MMODULE_CARD
    from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
    if not global_data.lobby_red_point_data:
        from logic.comsys.lobby.LobbyRedPointData import LobbyRedPointData
        LobbyRedPointData()
    mecha_id = battle_id_to_mecha_lobby_id(int(mecha_id))
    return global_data.lobby_red_point_data.get_rp_by_type_and_belong(L_ITEM_MMODULE_CARD, mecha_id)


def check_hide_func_lobby_red_dot(*args, **kwarg):
    return not check_lobby_red_point()


def check_pet_red_point(*args, **kwarg):
    if not global_data.player:
        return False
    if not global_data.player.get_pet_daily_state():
        return True