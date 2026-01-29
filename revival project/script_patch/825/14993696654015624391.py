# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/intimacy_utils.py
from __future__ import absolute_import
import six
from logic.gutils.role_head_utils import PlayerInfoManager, init_dan_info
from common.const.property_const import U_ID, C_NAME, SEX, INTIMACY_DATA
from logic.gcommon.const import INTIMACY_NAME_MAP, IDX_INTIMACY_PT, IDX_INTIMACY_LV, IDX_INTIMACY_TYPE, IDX_INTIMACY_NAME, INTIMACY_BADGE_LV, INTIMACY_TEAM_SHOW_LV, INTIMACY_MSG_TYPE_BUILD_RECV, INTIMACY_MSG_TYPE_DELETE_RECV, INTIMACY_RELATION_TYPE_LOVERS, INTIMACY_RELATION_TYPE_PARTNER, INTIMACY_RELATION_TYPE_MECHAFRD, INTIMACY_RELATION_TYPE_BESTIE, INTIMACY_ERR_SAME_UID, INTIMACY_ERR_NOT_FRD, INTIMACY_ERR_WRONG_TYPE, INTIMACY_ERR_EXIST_RELATION, INTIMACY_ERR_NUM_LIMIT, INTIMACY_ERR_UNENOUGH_INTIMACY, INTIMACY_ERR_NOT_CD, INTIMACY_ERR_ALREADY_SEND, INTIMACY_MEMORY_RELATION_EVENTS
from logic.gcommon.cdata.intimacy_data import get_intimacy_pt, get_upgrade_intimacy_pt, UNLOCK_MEMORY_LV
from logic.gcommon.time_utility import ONE_DAY_SECONDS, get_server_time, get_day_start_timestamp
from logic.gcommon.const import INTIMACY_HISTORICAL_EVENT_KEY
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gutils.template_utils import set_sex_node_img
OPERATION_FAIL_TEXT = {INTIMACY_ERR_SAME_UID: 3237,
   INTIMACY_ERR_NOT_FRD: 3238,
   INTIMACY_ERR_WRONG_TYPE: 3239,
   INTIMACY_ERR_EXIST_RELATION: 3240,
   INTIMACY_ERR_NUM_LIMIT: 3241,
   INTIMACY_ERR_UNENOUGH_INTIMACY: 3243,
   INTIMACY_ERR_NOT_CD: 3242
   }
INTIMACY_PIC = {INTIMACY_RELATION_TYPE_LOVERS: 'gui/ui_res_2/friend/intimacy/icon_lover_big.png',
   INTIMACY_RELATION_TYPE_PARTNER: 'gui/ui_res_2/friend/intimacy/icon_cooperate_big.png',
   INTIMACY_RELATION_TYPE_MECHAFRD: 'gui/ui_res_2/friend/intimacy/icon_friends_big.png',
   INTIMACY_RELATION_TYPE_BESTIE: 'gui/ui_res_2/friend/intimacy/icon_bestie_big.png'
   }
INTIMACY_ICON = {INTIMACY_RELATION_TYPE_LOVERS: 'gui/ui_res_2/friend/intimacy/icon_lover.png',
   INTIMACY_RELATION_TYPE_PARTNER: 'gui/ui_res_2/friend/intimacy/icon_cooperate.png',
   INTIMACY_RELATION_TYPE_MECHAFRD: 'gui/ui_res_2/friend/intimacy/icon_friends.png',
   INTIMACY_RELATION_TYPE_BESTIE: 'gui/ui_res_2/friend/intimacy/icon_bestie.png'
   }
INTIMACY_BADGE = {INTIMACY_RELATION_TYPE_LOVERS: 'gui/ui_res_2/friend/intimacy/badge/lover0%d.png',
   INTIMACY_RELATION_TYPE_PARTNER: 'gui/ui_res_2/friend/intimacy/badge/partner0%d.png',
   INTIMACY_RELATION_TYPE_MECHAFRD: 'gui/ui_res_2/friend/intimacy/badge/mechabro0%d.png',
   INTIMACY_RELATION_TYPE_BESTIE: 'gui/ui_res_2/friend/intimacy/badge/bestie0%d.png'
   }
INTIMACY_FRAME = {INTIMACY_RELATION_TYPE_LOVERS: 'gui/ui_res_2/friend/intimacy/frame_friend_intimacy_lover.png',
   INTIMACY_RELATION_TYPE_PARTNER: 'gui/ui_res_2/friend/intimacy/frame_friend_intimacy_cooperate.png',
   INTIMACY_RELATION_TYPE_MECHAFRD: 'gui/ui_res_2/friend/intimacy/frame_friend_intimacy_friend.png',
   INTIMACY_RELATION_TYPE_BESTIE: 'gui/ui_res_2/friend/intimacy/frame_friend_intimacy_bestie.png'
   }
INTIMACY_REQUEST_FRAME = {INTIMACY_RELATION_TYPE_LOVERS: 'gui/ui_res_2/friend/intimacy/frame_friend_request_lover.png',
   INTIMACY_RELATION_TYPE_PARTNER: 'gui/ui_res_2/friend/intimacy/frame_friend_request_cooperate.png',
   INTIMACY_RELATION_TYPE_MECHAFRD: 'gui/ui_res_2/friend/intimacy/frame_friend_request_friends.png',
   INTIMACY_RELATION_TYPE_BESTIE: 'gui/ui_res_2/friend/intimacy/frame_friend_request_bestie.png'
   }
INTIMACY_EVENT_FRAME = {INTIMACY_RELATION_TYPE_LOVERS: 'gui/ui_res_2/friend/intimacy/frame_friend_event_color_lover.png',
   INTIMACY_RELATION_TYPE_PARTNER: 'gui/ui_res_2/friend/intimacy/frame_friend_event_color_cooperate.png',
   INTIMACY_RELATION_TYPE_MECHAFRD: 'gui/ui_res_2/friend/intimacy/frame_friend_event_color_friends.png',
   INTIMACY_RELATION_TYPE_BESTIE: 'gui/ui_res_2/friend/intimacy/frame_friend_event_color_bestie.png'
   }
INTIMACY_BAR = {INTIMACY_RELATION_TYPE_LOVERS: 'gui/ui_res_2/friend/intimacy/bar_friend_event_color_lover.png',
   INTIMACY_RELATION_TYPE_PARTNER: 'gui/ui_res_2/friend/intimacy/bar_friend_event_color_cooperate.png',
   INTIMACY_RELATION_TYPE_MECHAFRD: 'gui/ui_res_2/friend/intimacy/bar_friend_event_color_friends.png',
   INTIMACY_RELATION_TYPE_BESTIE: 'gui/ui_res_2/friend/intimacy/bar_friend_event_color_bestie.png'
   }

def get_relation_by_uid(uid):
    if uid is None:
        return
    else:
        if not global_data.player:
            return
        uid = int(uid)
        relation_data = global_data.player.intimacy_relation_data
        for relation_type, uid_list in six.iteritems(relation_data):
            if uid in uid_list:
                return relation_type

        return


def get_intimacy_level_by_uid(uid):
    intimacy_data = global_data.player.intimacy_data
    return intimacy_data.get(str(uid), [0, None, None, 0, -1])[IDX_INTIMACY_LV]


def has_relation_with_uid_by_type(relation_type, uid):
    if not global_data.player:
        return False
    relation_data = global_data.player.intimacy_relation_data
    try:
        uid = int(uid)
    except:
        return False

    return uid in relation_data.get(relation_type, [])


def get_intimacy_icon_by_type(intimacy_type):
    return INTIMACY_ICON.get(intimacy_type)


def init_intimacy_icon(item, intimacy_type, intimacy_level=0, show_level=False):
    if intimacy_type not in INTIMACY_ICON:
        item.setVisible(False)
        return
    item.img_intimacy.SetDisplayFrameByPath('', INTIMACY_ICON[intimacy_type])
    show_level = False
    item.panel_level.setVisible(show_level)
    if show_level:
        item.lab_intimacy.SetString(str(intimacy_level))


def init_intimacy_pic(icon, intimacy_type):
    if intimacy_type not in INTIMACY_PIC:
        icon.setVisible(False)
        return
    icon.SetDisplayFrameByPath('', INTIMACY_PIC[intimacy_type])


def init_intimacy_frame(item, intimacy_type):
    if intimacy_type not in INTIMACY_FRAME:
        item.setVisible(False)
        return
    item.pnl_bg.frame.SetDisplayFrameByPath('', INTIMACY_FRAME[intimacy_type])


def init_intimacy_request_frame(item, intimacy_type):
    if intimacy_type not in INTIMACY_REQUEST_FRAME:
        item.setVisible(False)
        return
    item.SetDisplayFrameByPath('', INTIMACY_REQUEST_FRAME[intimacy_type])


def init_intimacy_event_frame(item, intimacy_type):
    if intimacy_type not in INTIMACY_EVENT_FRAME:
        item.setVisible(False)
        return
    item.SetDisplayFrameByPath('', INTIMACY_EVENT_FRAME[intimacy_type])


def init_intimacy_event_bar(item, intimacy_type, event_name):
    if intimacy_type not in INTIMACY_BAR:
        item.setVisible(False)
        return
    if event_name in INTIMACY_MEMORY_RELATION_EVENTS:
        item.SetDisplayFrameByPath('', INTIMACY_BAR[intimacy_type])
    else:
        item.SetDisplayFrameByPath('', 'gui/ui_res_2/friend/intimacy/bar_friend_event_color_normal.png')


def init_intimacy_icon_with_uid(item, uid, show_level=True, team_show_limit=True):
    intimacy_type = get_relation_by_uid(uid)
    level = get_intimacy_level_by_uid(uid)
    show = intimacy_type is not None and (not team_show_limit or level >= INTIMACY_TEAM_SHOW_LV)
    item.setVisible(show)
    if show:
        init_intimacy_icon(item, intimacy_type, level, show_level=show_level)
    return show


def init_intimacy_icon_with_uid_list(item, uid_list, show_level=True):
    relation_order = global_data.player.intimacy_relation_order
    cur_relation_idx = len(relation_order)
    cur_uid = None
    for uid in uid_list:
        relation = get_relation_by_uid(uid)
        if relation not in relation_order:
            continue
        intimacy_lv = get_intimacy_level_by_uid(uid)
        if intimacy_lv < INTIMACY_TEAM_SHOW_LV:
            continue
        relation_idx = relation_order.index(relation)
        if relation_idx < cur_relation_idx:
            cur_relation_idx = relation_idx
            cur_uid = uid
        if cur_relation_idx == 0:
            break

    if cur_uid is None:
        item.setVisible(False)
    else:
        init_intimacy_icon_with_uid(item, cur_uid, show_level)
    return


def get_intimacy_badge(intimacy_type, intimacy_lv):
    if intimacy_type not in INTIMACY_BADGE:
        return
    badge_path = INTIMACY_BADGE[intimacy_type]
    badge_lv = 0
    for idx, lv in enumerate(INTIMACY_BADGE_LV):
        if intimacy_lv >= lv:
            badge_lv += 1
        else:
            break

    if badge_lv == 0:
        return
    badge_path = badge_path % badge_lv
    return badge_path


def get_intimacy_badge_with_uid(uid):
    intimacy_type = get_relation_by_uid(uid)
    intimacy_lv = get_intimacy_level_by_uid(uid)
    return get_intimacy_badge(intimacy_type, intimacy_lv)


def init_intimacy_my_item(item, uid, friend_info, intimacy_info, del_req_sent=False, show_btn=False, gift_callback=None, manage_callback=None, show_remark=False, is_intimacy_panel=False):
    if not intimacy_info[IDX_INTIMACY_TYPE]:
        item.setVisible(False)
        return
    else:
        player_info_manager = PlayerInfoManager()
        item.lab_name.SetString(str(friend_info[C_NAME]))
        if item.lab_name2:
            remark = show_remark and friend_info.get('remark', '')
            item.lab_name2.setVisible(bool(remark))
            if remark:
                item.lab_name2.SetString('(%s)' % remark)

        @item.temp_head.callback()
        def OnClick(btn, touch):
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            ui.refresh_by_uid(int(friend_info[U_ID]))
            ui.set_position(touch.getLocation())

        update_head_info = global_data.message_data.get_role_head_info(uid)
        frame = update_head_info.get('head_frame', None)
        photo = update_head_info.get('head_photo', None)
        if frame and photo:
            friend_info['head_frame'] = frame
            friend_info['head_photo'] = photo
        player_info_manager.add_head_item_auto(item.temp_head, uid, 0, friend_info)
        player_info_manager.add_dan_info_item(item.temp_tier, uid)
        init_dan_info(item.temp_tier, uid)
        set_sex_node_img(item.img_gender, friend_info.get(SEX, None))
        intimacy_name = intimacy_info[IDX_INTIMACY_NAME]
        if intimacy_name is None:
            intimacy_name = get_text_by_id(INTIMACY_NAME_MAP[intimacy_info[IDX_INTIMACY_TYPE]])
        item.lab_intimacy.SetString(str(intimacy_name))
        badge_path = get_intimacy_badge(intimacy_info[IDX_INTIMACY_TYPE], intimacy_info[IDX_INTIMACY_LV])
        item.img_badge.setVisible(bool(badge_path))
        item.img_badge.SetDisplayFrameByPath('', badge_path)
        item.lab_value_num.SetString(str(get_intimacy_pt(intimacy_info)))
        if not is_intimacy_panel:
            init_intimacy_icon(item.temp_intimacy, intimacy_info[IDX_INTIMACY_TYPE], intimacy_info[IDX_INTIMACY_LV], show_level=True)
        item.lab_remove_tips.setVisible(del_req_sent)
        show_btn = show_btn and not del_req_sent
        item.btn_gift.setVisible(show_btn)
        item.btn_manage.setVisible(show_btn)
        if show_btn:
            item.btn_gift.BindMethod('OnClick', lambda btn, touch: callable(gift_callback) and gift_callback())
            item.btn_manage.BindMethod('OnClick', lambda btn, touch: callable(manage_callback) and manage_callback(touch))
        return


def init_intimacy_my_item_new(item, uid, friend_info, intimacy_info, del_req_sent=False, show_btn=False, gift_callback=None, manage_callback=None, show_remark=False):
    if not intimacy_info[IDX_INTIMACY_TYPE]:
        item.setVisible(False)
        return
    init_intimacy_my_item(item, uid, friend_info, intimacy_info, del_req_sent, show_btn, gift_callback, manage_callback, show_remark, True)
    init_intimacy_frame(item, intimacy_info[IDX_INTIMACY_TYPE])
    badge_path = get_intimacy_badge(intimacy_info[IDX_INTIMACY_TYPE], intimacy_info[IDX_INTIMACY_LV])
    item.img_badge.setVisible(bool(badge_path))
    item.img_badge.SetDisplayFrameByPath('', badge_path)
    item.lab_level.SetString('Lv.{}'.format(str(intimacy_info[IDX_INTIMACY_LV])))
    current_pt = str(intimacy_info[IDX_INTIMACY_PT])
    upgrade_pt = str(get_upgrade_intimacy_pt(intimacy_info))
    item.lab_value_num.SetString(get_text_by_id(634087) + current_pt + '/' + upgrade_pt)
    init_intimacy_pic(item.temp_intimacy.img_intimacy, intimacy_info[IDX_INTIMACY_TYPE])


def init_intimacy_event_item(item, player_uid, other_uid, data):
    nd_lock = item.nd_lock
    lab_day = item.lab_day
    btn_day = item.btn_day
    lab_recall = btn_day.lab_recall
    is_mine = player_uid == global_data.player.uid
    if data:
        nd_lock.setVisible(False)
        lab_day.setVisible(True)
        now = get_day_start_timestamp(get_server_time())
        built_time_stamp = data.get('unlock_time', now)
        built_time = get_day_start_timestamp(built_time_stamp)
        delta_day = int(now - built_time) // ONE_DAY_SECONDS
        lab_day.SetString(get_text_by_id(860274).format(delta_day + 1))
        if is_mine:
            btn_day.BindMethod('OnClick', lambda btn, touch: callable(intimacy_event_cb) and intimacy_event_cb(uid=other_uid, data=data))
            archive_data = global_data.achi_mgr.get_general_archive_data()
            cache_data = archive_data.get_field(INTIMACY_HISTORICAL_EVENT_KEY.format(str(other_uid)), {})
            from logic.comsys.intimacy.IntimacyHistoricalEventUI import get_data_list
            data_list = get_data_list(data)
            if cache_data != data_list:
                btn_day.img_new.setVisible(True)
            else:
                btn_day.img_new.setVisible(False)
        else:
            btn_day.img_new.setVisible(False)
    else:
        if is_mine:
            intimacy_level = global_data.player.intimacy_data.get(str(other_uid))[IDX_INTIMACY_LV] if global_data.player else 0
        else:
            player_inf = global_data.message_data.get_player_detail_inf(player_uid)
            if player_inf:
                intimacy_data = player_inf.get('intimacy_data', {})
                intimacy_level = intimacy_data.get(str(other_uid))[IDX_INTIMACY_LV]
            else:
                intimacy_level = 0
        nd_lock.setVisible(True)
        lab_day.setVisible(False)
        btn_day.img_new.setVisible(False)
        if intimacy_level >= UNLOCK_MEMORY_LV:
            lab_recall.SetString(get_text_by_id(860266))
            if is_mine:
                nd_lock.temp_red.setVisible(True)

                @nd_lock.callback()
                def OnClick(btn, touch):

                    def confirm_callback():
                        global_data.player.request_unlock_intimacy_memory(other_uid)

                    SecondConfirmDlg2().confirm(content=get_text_by_id(860267), confirm_callback=confirm_callback)

        else:
            lab_recall.SetString(get_text_by_id(860273).format(UNLOCK_MEMORY_LV))


def intimacy_event_cb(uid, data):

    def confirm_callback(has_unlock=False):
        ui = global_data.ui_mgr.show_ui('IntimacyHistoricalEventUI', 'logic.comsys.intimacy')
        ui.set_data(uid, data)
        if not has_unlock:
            global_data.player.request_unlock_intimacy_memory(uid)

    unlocker_uid = data.get('unlocker_uid')
    follower_uid = data.get('follower_uid')
    if global_data.player.uid == unlocker_uid or follower_uid:
        confirm_callback(True)
    else:
        SecondConfirmDlg2().confirm(content=get_text_by_id(860268), confirm_callback=confirm_callback)


def init_intimacy_build_item(item, uid, friend_info, intimacy_info, waiting_response=False, show_btn=False, build_callback=None, show_remark=False):
    player_info_manager = PlayerInfoManager()
    item.lab_name.SetString(str(friend_info[C_NAME]))
    if item.lab_name2:
        remark = show_remark and friend_info.get('remark', '')
        item.lab_name2.setVisible(bool(remark))
        if remark:
            item.lab_name2.SetString('(%s)' % remark)

    @item.temp_head.callback()
    def OnClick(btn, touch):
        ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
        ui.refresh_by_uid(int(friend_info[U_ID]))
        ui.set_position(touch.getLocation())

    update_head_info = global_data.message_data.get_role_head_info(uid)
    frame = update_head_info.get('head_frame', None)
    photo = update_head_info.get('head_photo', None)
    if frame and photo:
        friend_info['head_frame'] = frame
        friend_info['head_photo'] = photo
    player_info_manager.add_head_item_auto(item.temp_head, uid, 0, friend_info)
    player_info_manager.add_dan_info_item(item.temp_tier, uid)
    init_dan_info(item.temp_tier, uid)
    set_sex_node_img(item.img_gender, friend_info.get(SEX, None))
    item.lab_value_num.SetString(str(get_intimacy_pt(intimacy_info)))
    item.lab_waiting_tips.setVisible(waiting_response)
    show_btn = show_btn and not waiting_response
    item.btn_build.setVisible(show_btn)
    if show_btn:
        item.btn_build.BindMethod('OnClick', lambda btn, touch: callable(build_callback) and build_callback())
    return


def init_intimacy_request_item(item, uid, friend_info, intimacy_info, accept_callback=None, refuse_callback=None, request_data=None):
    if request_data['m_type'] == INTIMACY_MSG_TYPE_BUILD_RECV:
        item.lab_intimacy.SetString(get_text_by_id(INTIMACY_NAME_MAP[request_data['i_type']]))
        init_intimacy_icon(item.temp_intimacy, request_data['i_type'], show_level=False)
        init_intimacy_build_item(item.temp_build, uid, friend_info, intimacy_info, False)
    elif request_data['m_type'] == INTIMACY_MSG_TYPE_DELETE_RECV:
        init_intimacy_my_item(item.temp_remove, uid, friend_info, intimacy_info, show_btn=False)
    item.btn_accept.btn_common.BindMethod('OnClick', lambda btn, touch: callable(accept_callback) and accept_callback())
    item.btn_refuse.btn_common.BindMethod('OnClick', lambda btn, touch: callable(refuse_callback) and refuse_callback())